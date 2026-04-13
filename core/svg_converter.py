"""
SVG-to-Excalidraw Converter

Parses SVG path data and converts it to Excalidraw element dicts.
Supports M, L, H, V, C, S, Q, T, A, Z path commands.

Algorithm:
  1. Tokenize SVG path 'd' attribute into commands + parameters
  2. Tessellate Bezier curves and arcs into polylines
  3. Simplify polylines via Ramer-Douglas-Peucker
  4. Classify closed shapes (ellipse, rectangle, or line)
  5. Generate Excalidraw element dicts
"""

import json
import math
import re
import xml.etree.ElementTree as ET
from typing import Any, Dict, List, Optional, Tuple

from . import engine

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
CUBIC_STEPS = 8  # Samples per cubic Bezier segment
QUAD_STEPS = 6   # Samples per quadratic Bezier segment
ARC_STEPS = 36   # Samples per arc segment

RDP_MIN_EPSILON = 0.3           # Absolute minimum for RDP simplification
RDP_RELATIVE_SCALE = 0.015     # Relative scale for RDP simplification

CIRCLE_RADIAL_TOL = 0.10       # 10% radial distance tolerance
CIRCLE_AREA_TOL = 0.12         # 12% area ratio tolerance (pi/4)
RECT_ASPECT_TOL = 0.12         # 12% aspect ratio tolerance
POINT_MERGE_DIST = 0.5         # Distance threshold for vertex dedup

# ---------------------------------------------------------------------------
# Path Tokenizer
# ---------------------------------------------------------------------------
_TOKEN_RE = re.compile(
    r"[MmLlHhVvCcSsQqTtAaZz]|-?\d*\.?\d+(?:[eE][+-]?\d+)?"
)

Command = Tuple[str, List[float]]


def _tokenize_path(d: str) -> List[Command]:
    """Parse SVG path 'd' attribute into a list of (command, params) tuples."""
    tokens = _TOKEN_RE.findall(d)
    commands: List[Command] = []
    current_cmd = ""
    current_nums: List[float] = []

    def _flush() -> None:
        if current_cmd:
            commands.append((current_cmd, current_nums[:]))
            current_nums.clear()

    for tok in tokens:
        if tok.isalpha():
            _flush()
            current_cmd = tok
        else:
            current_nums.append(float(tok))

    _flush()
    return commands


# ---------------------------------------------------------------------------
# Path Execution — builds polylines from commands
# ---------------------------------------------------------------------------
def _parse_path_commands(
    cmds: List[Command],
) -> List[List[Tuple[float, float]]]:
    """Execute SVG path commands, returning a list of polylines (one per subpath)."""
    polylines: List[List[Tuple[float, float]]] = []
    current: List[Tuple[float, float]] = []
    cx, cy = 0.0, 0.0   # Current point
    sx, sy = 0.0, 0.0   # Subpath start point
    prev_cmd = ""
    prev_cp1: Optional[Tuple[float, float]] = None  # Previous cubic control point
    prev_qp: Optional[Tuple[float, float]] = None   # Previous quadratic control point

    def _needs_move() -> None:
        nonlocal current
        if current:
            polylines.append(current)
        current = []

    for cmd, nums in cmds:
        # --- MoveTo ---
        if cmd in ("M", "m"):
            _needs_move()
            i = 0
            while i + 1 < len(nums):
                if cmd == "M":
                    cx, cy = nums[i], nums[i + 1]
                else:
                    cx += nums[i]
                    cy += nums[i + 1]
                if i == 0:
                    sx, sy = cx, cy
                current.append((cx, cy))
                prev_cmd = "M" if i == 0 else "L"
                i += 2

        # --- LineTo ---
        elif cmd in ("L", "l"):
            i = 0
            while i + 1 < len(nums):
                if cmd == "L":
                    cx, cy = nums[i], nums[i + 1]
                else:
                    cx += nums[i]
                    cy += nums[i + 1]
                current.append((cx, cy))
                prev_cmd = "L"
                i += 2

        # --- Horizontal LineTo ---
        elif cmd in ("H", "h"):
            for val in nums:
                if cmd == "H":
                    cx = val
                else:
                    cx += val
                current.append((cx, cy))
            prev_cmd = "H"

        # --- Vertical LineTo ---
        elif cmd in ("V", "v"):
            for val in nums:
                if cmd == "V":
                    cy = val
                else:
                    cy += val
                current.append((cx, cy))
            prev_cmd = "V"

        # --- Cubic Bezier ---
        elif cmd in ("C", "c"):
            i = 0
            while i + 5 < len(nums):
                if cmd == "C":
                    x1, y1 = nums[i], nums[i + 1]
                    x2, y2 = nums[i + 2], nums[i + 3]
                    ex, ey = nums[i + 4], nums[i + 5]
                else:
                    x1, y1 = cx + nums[i], cy + nums[i + 1]
                    x2, y2 = cx + nums[i + 2], cy + nums[i + 3]
                    ex, ey = cx + nums[i + 4], cy + nums[i + 5]
                pts = _sample_cubic(cx, cy, x1, y1, x2, y2, ex, ey, CUBIC_STEPS)
                current.extend(pts[1:])  # Skip first point (= current)
                prev_cp1 = (x2, y2)
                cx, cy = ex, ey
                prev_cmd = "C"
                i += 6

        # --- Shorthand Cubic ---
        elif cmd in ("S", "s"):
            i = 0
            while i + 3 < len(nums):
                # Infer first control point
                if prev_cmd in ("C", "S") and prev_cp1 is not None:
                    ix1 = 2 * cx - prev_cp1[0]
                    iy1 = 2 * cy - prev_cp1[1]
                else:
                    ix1, iy1 = cx, cy

                if cmd == "S":
                    x2, y2 = nums[i], nums[i + 1]
                    ex, ey = nums[i + 2], nums[i + 3]
                else:
                    x2, y2 = cx + nums[i], cy + nums[i + 1]
                    ex, ey = cx + nums[i + 2], cy + nums[i + 3]

                pts = _sample_cubic(cx, cy, ix1, iy1, x2, y2, ex, ey, CUBIC_STEPS)
                current.extend(pts[1:])
                prev_cp1 = (x2, y2)
                cx, cy = ex, ey
                prev_cmd = "S"
                i += 4

        # --- Quadratic Bezier ---
        elif cmd in ("Q", "q"):
            i = 0
            while i + 3 < len(nums):
                if cmd == "Q":
                    qx, qy = nums[i], nums[i + 1]
                    ex, ey = nums[i + 2], nums[i + 3]
                else:
                    qx, qy = cx + nums[i], cy + nums[i + 1]
                    ex, ey = cx + nums[i + 2], cy + nums[i + 3]
                pts = _sample_quadratic(cx, cy, qx, qy, ex, ey, QUAD_STEPS)
                current.extend(pts[1:])
                prev_qp = (qx, qy)
                cx, cy = ex, ey
                prev_cmd = "Q"
                i += 4

        # --- Shorthand Quadratic ---
        elif cmd in ("T", "t"):
            i = 0
            while i + 1 < len(nums):
                if prev_cmd in ("Q", "T") and prev_qp is not None:
                    qx = 2 * cx - prev_qp[0]
                    qy = 2 * cy - prev_qp[1]
                else:
                    qx, qy = cx, cy

                if cmd == "T":
                    ex, ey = nums[i], nums[i + 1]
                else:
                    ex, ey = cx + nums[i], cy + nums[i + 1]

                pts = _sample_quadratic(cx, cy, qx, qy, ex, ey, QUAD_STEPS)
                current.extend(pts[1:])
                prev_qp = (qx, qy)
                cx, cy = ex, ey
                prev_cmd = "T"
                i += 2

        # --- Arc ---
        elif cmd in ("A", "a"):
            i = 0
            while i + 6 < len(nums):
                rx = nums[i]
                ry = nums[i + 1]
                x_rot = nums[i + 2]
                large_arc = int(nums[i + 3])
                sweep = int(nums[i + 4])
                if cmd == "A":
                    ex, ey = nums[i + 5], nums[i + 6]
                else:
                    ex, ey = cx + nums[i + 5], cy + nums[i + 6]
                pts = _sample_arc(cx, cy, rx, ry, x_rot, large_arc, sweep, ex, ey)
                current.extend(pts[1:])
                cx, cy = ex, ey
                prev_cmd = "A"
                prev_cp1 = None
                i += 7

        # --- Close Path ---
        elif cmd in ("Z", "z"):
            if current and (cx != sx or cy != sy):
                current.append((sx, sy))
            if current:
                polylines.append(current)
                current = [(sx, sy)]
            cx, cy = sx, sy
            prev_cmd = "Z"
            prev_cp1 = None
            prev_qp = None

    if current:
        polylines.append(current)

    return polylines


# ---------------------------------------------------------------------------
# Bezier & Arc Sampling
# ---------------------------------------------------------------------------
def _sample_cubic(
    x0: float, y0: float,
    x1: float, y1: float,
    x2: float, y2: float,
    x3: float, y3: float,
    steps: int,
) -> List[Tuple[float, float]]:
    """Sample points along a cubic Bezier curve."""
    pts = []
    for i in range(steps + 1):
        t = i / steps
        u = 1 - t
        x = u**3 * x0 + 3 * u**2 * t * x1 + 3 * u * t**2 * x2 + t**3 * x3
        y = u**3 * y0 + 3 * u**2 * t * y1 + 3 * u * t**2 * y2 + t**3 * y3
        pts.append((x, y))
    return pts


def _sample_quadratic(
    x0: float, y0: float,
    qx: float, qy: float,
    ex: float, ey: float,
    steps: int,
) -> List[Tuple[float, float]]:
    """Sample points along a quadratic Bezier curve."""
    pts = []
    for i in range(steps + 1):
        t = i / steps
        u = 1 - t
        x = u**2 * x0 + 2 * u * t * qx + t**2 * ex
        y = u**2 * y0 + 2 * u * t * qy + t**2 * ey
        pts.append((x, y))
    return pts


def _sample_arc(
    x0: float, y0: float,
    rx: float, ry: float,
    x_rot_deg: float,
    large_arc: int,
    sweep: int,
    ex: float, ey: float,
) -> List[Tuple[float, float]]:
    """Sample points along an SVG arc using endpoint-to-center parameterization."""
    pts = [(x0, y0)]

    if rx == 0 or ry == 0:
        pts.append((ex, ey))
        return pts

    # Ensure radii are positive
    rx, ry = abs(rx), abs(ry)
    phi = math.radians(x_rot_deg)

    # Step 1: Compute (x1', y1')
    dx = (x0 - ex) / 2
    dy = (y0 - ey) / 2
    cos_phi = math.cos(phi)
    sin_phi = math.sin(phi)
    x1p = cos_phi * dx + sin_phi * dy
    y1p = -sin_phi * dx + cos_phi * dy

    # Step 2: Compute (cx', cy')
    x1p_sq = x1p * x1p
    y1p_sq = y1p * y1p
    rx_sq = rx * rx
    ry_sq = ry * ry

    # Correct radii if needed
    lam = x1p_sq / rx_sq + y1p_sq / ry_sq
    if lam > 1:
        lam_sqrt = math.sqrt(lam)
        rx *= lam_sqrt
        ry *= lam_sqrt
        rx_sq = rx * rx
        ry_sq = ry * ry

    num = rx_sq * ry_sq - rx_sq * y1p_sq - ry_sq * x1p_sq
    den = rx_sq * y1p_sq + ry_sq * x1p_sq

    if den == 0:
        pts.append((ex, ey))
        return pts

    sq = max(0, num / den)
    sq_root = math.sqrt(sq)

    if large_arc == sweep:
        sq_root = -sq_root

    cxp = sq_root * (rx * y1p / ry)
    cyp = -sq_root * (ry * x1p / rx)

    # Step 3: Compute (cx, cy)
    cx = cos_phi * cxp - sin_phi * cyp + (x0 + ex) / 2
    cy = sin_phi * cxp + cos_phi * cyp + (y0 + ey) / 2

    # Step 4: Compute theta1 and dtheta
    def _vec_angle(ux: float, uy: float, vx: float, vy: float) -> float:
        n = math.sqrt((ux * ux + uy * uy) * (vx * vx + vy * vy))
        if n == 0:
            return 0
        c = (ux * vx + uy * vy) / n
        c = max(-1, min(1, c))
        angle = math.acos(c)
        if ux * vy - uy * vx < 0:
            angle = -angle
        return angle

    theta1 = _vec_angle(1, 0, (x1p - cxp) / rx, (y1p - cyp) / ry)
    dtheta = _vec_angle(
        (x1p - cxp) / rx, (y1p - cyp) / ry,
        (-x1p - cxp) / rx, (-y1p - cyp) / ry,
    )

    if sweep == 0 and dtheta > 0:
        dtheta -= 2 * math.pi
    elif sweep == 1 and dtheta < 0:
        dtheta += 2 * math.pi

    # Sample points along the arc
    for i in range(1, ARC_STEPS + 1):
        t = i / ARC_STEPS
        theta = theta1 + t * dtheta
        cos_t = math.cos(theta)
        sin_t = math.sin(theta)
        # Point on ellipse in rotated frame
        px = rx * cos_t
        py = ry * sin_t
        # Transform back
        x = cos_phi * px - sin_phi * py + cx
        y = sin_phi * px + cos_phi * py + cy
        pts.append((x, y))

    return pts


# ---------------------------------------------------------------------------
# Ramer-Douglas-Peucker Simplification
# ---------------------------------------------------------------------------
def _perp_distance(
    p: Tuple[float, float],
    a: Tuple[float, float],
    b: Tuple[float, float],
) -> float:
    """Perpendicular distance from point p to line segment a-b."""
    dx = b[0] - a[0]
    dy = b[1] - a[1]
    len_sq = dx * dx + dy * dy
    if len_sq == 0:
        return math.hypot(p[0] - a[0], p[1] - a[1])
    t = ((p[0] - a[0]) * dx + (p[1] - a[1]) * dy) / len_sq
    t = max(0, min(1, t))
    proj_x = a[0] + t * dx
    proj_y = a[1] + t * dy
    return math.hypot(p[0] - proj_x, p[1] - proj_y)


def _rdp(points: List[Tuple[float, float]], epsilon: float) -> List[Tuple[float, float]]:
    """Recursive Ramer-Douglas-Peucker simplification."""
    if len(points) <= 2:
        return points[:]

    max_dist = 0.0
    max_idx = 0
    for i in range(1, len(points) - 1):
        d = _perp_distance(points[i], points[0], points[-1])
        if d > max_dist:
            max_dist = d
            max_idx = i

    if max_dist > epsilon:
        left = _rdp(points[: max_idx + 1], epsilon)
        right = _rdp(points[max_idx:], epsilon)
        return left[:-1] + right
    else:
        return [points[0], points[-1]]


def simplify_polyline(
    points: List[Tuple[float, float]],
    epsilon: float = RDP_MIN_EPSILON,
) -> List[Tuple[float, float]]:
    """Simplify a polyline using RDP with adaptive epsilon."""
    if len(points) <= 2:
        return points[:]

    xs = [p[0] for p in points]
    ys = [p[1] for p in points]
    max_dim = max(max(xs) - min(xs), max(ys) - min(ys))
    effective_eps = max(epsilon, max_dim * RDP_RELATIVE_SCALE)

    return _rdp(points, effective_eps)


# ---------------------------------------------------------------------------
# Shape Classification
# ---------------------------------------------------------------------------
def _bounding_box(
    points: List[Tuple[float, float]],
) -> Tuple[float, float, float, float]:
    """Return (min_x, min_y, max_x, max_y)."""
    xs = [p[0] for p in points]
    ys = [p[1] for p in points]
    return min(xs), min(ys), max(xs), max(ys)


def _is_path_closed(points: List[Tuple[float, float]], tol: float = 1.0) -> bool:
    """Check if the first and last points are close enough to consider closed."""
    if len(points) < 3:
        return False
    return math.hypot(points[0][0] - points[-1][0],
                      points[0][1] - points[-1][1]) < tol


def _classify_as_ellipse(
    points: List[Tuple[float, float]],
) -> Optional[Dict[str, Any]]:
    """Try to classify a closed polyline as an ellipse/circle."""
    min_x, min_y, max_x, max_y = _bounding_box(points)
    w = max_x - min_x
    h = max_y - min_y
    if w < 1 or h < 1:
        return None

    # Aspect ratio check
    ratio = min(w, h) / max(w, h)
    if ratio < (1 - RECT_ASPECT_TOL):
        return None

    # Radial uniformity check
    cx = (min_x + max_x) / 2
    cy = (min_y + max_y) / 2
    radii = [math.hypot(p[0] - cx, p[1] - cy) for p in points]
    avg_r = sum(radii) / len(radii)
    if avg_r < 1:
        return None

    max_deviation = max(abs(r - avg_r) / avg_r for r in radii)
    if max_deviation > CIRCLE_RADIAL_TOL:
        return None

    # Area ratio check (pi/4 for perfect circle)
    area = abs(sum(
        points[i][0] * points[(i + 1) % len(points)][1]
        - points[(i + 1) % len(points)][0] * points[i][1]
        for i in range(len(points))
    )) / 2
    bbox_area = w * h
    if bbox_area > 0:
        area_ratio = area / bbox_area
        if abs(area_ratio - math.pi / 4) > CIRCLE_AREA_TOL:
            return None

    return {"type": "ellipse", "x": min_x, "y": min_y, "width": w, "height": h}


def _classify_as_rectangle(
    points: List[Tuple[float, float]],
) -> Optional[Dict[str, Any]]:
    """Try to classify a closed polyline as a rectangle."""
    # Deduplicate vertices
    deduped = [points[0]]
    for p in points[1:]:
        if math.hypot(p[0] - deduped[-1][0], p[1] - deduped[-1][1]) > POINT_MERGE_DIST:
            deduped.append(p)
    # Remove closing point if it duplicates the first
    if len(deduped) > 1 and math.hypot(
        deduped[0][0] - deduped[-1][0], deduped[0][1] - deduped[-1][1]
    ) < POINT_MERGE_DIST:
        deduped = deduped[:-1]

    if len(deduped) != 4:
        return None

    # Check for 2 horizontal + 2 vertical edges
    h_edges = 0
    v_edges = 0
    for i in range(4):
        p1 = deduped[i]
        p2 = deduped[(i + 1) % 4]
        dx = abs(p2[0] - p1[0])
        dy = abs(p2[1] - p1[1])
        edge_len = math.hypot(dx, dy)
        if edge_len < 1:
            continue
        if dx / edge_len > (1 - RECT_ASPECT_TOL):
            h_edges += 1
        elif dy / edge_len > (1 - RECT_ASPECT_TOL):
            v_edges += 1

    if h_edges != 2 or v_edges != 2:
        return None

    min_x, min_y, max_x, max_y = _bounding_box(deduped)
    return {
        "type": "rectangle",
        "x": min_x,
        "y": min_y,
        "width": max_x - min_x,
        "height": max_y - min_y,
    }


def classify_polyline(
    points: List[Tuple[float, float]],
) -> Dict[str, Any]:
    """Classify a polyline as ellipse, rectangle, or line.

    Returns a dict with 'type' key and shape-specific bounds.
    """
    if len(points) < 3:
        return {"type": "line"}

    closed = _is_path_closed(points)

    if closed:
        result = _classify_as_ellipse(points)
        if result is not None:
            return result

        result = _classify_as_rectangle(points)
        if result is not None:
            return result

    return {"type": "line"}


# ---------------------------------------------------------------------------
# SVG Element Extraction
# ---------------------------------------------------------------------------
_SVG_NS = "http://www.w3.org/2000/svg"


def _strip_ns(tag: str) -> str:
    """Remove XML namespace prefix from tag name."""
    if tag.startswith("{"):
        return tag.split("}", 1)[1]
    return tag


def _parse_color(value: Optional[str]) -> str:
    """Parse an SVG color attribute, returning a hex color string."""
    if value is None or value == "none" or value == "":
        return "transparent"
    # Handle hex colors
    if value.startswith("#"):
        return value
    # Handle rgb()
    m = re.match(r"rgb\((\d+),\s*(\d+),\s*(\d+)\)", value)
    if m:
        return f"#{int(m.group(1)):02x}{int(m.group(2)):02x}{int(m.group(3)):02x}"
    return "#1e1e1e"


def _compose_opacity(
    *values: Optional[float],
) -> float:
    """Compose multiple opacity values by multiplication. None values are treated as 1.0."""
    result = 1.0
    for v in values:
        if v is not None:
            result *= max(0.0, min(1.0, v))
    return result


def _detect_ring_shape(
    polylines: List[List[Tuple[float, float]]],
) -> bool:
    """Detect if polylines represent a ring/donut (outer shape with inner hole)."""
    if len(polylines) != 2:
        return False

    bb0 = _bounding_box(polylines[0])
    bb1 = _bounding_box(polylines[1])
    area0 = (bb0[2] - bb0[0]) * (bb0[3] - bb0[1])
    area1 = (bb1[2] - bb1[0]) * (bb1[3] - bb1[1])

    if area0 > area1:
        outer_bb, inner_bb = bb0, bb1
        outer_area, inner_area = area0, area1
    else:
        outer_bb, inner_bb = bb1, bb0
        outer_area, inner_area = area1, area0

    margin = 2.0
    if (inner_bb[0] < outer_bb[0] - margin or inner_bb[1] < outer_bb[1] - margin or
            inner_bb[2] > outer_bb[2] + margin or inner_bb[3] > outer_bb[3] + margin):
        return False

    if outer_area <= 0:
        return False
    ratio = inner_area / outer_area
    if ratio < 0.2 or ratio > 0.8:
        return False

    oc = ((outer_bb[0] + outer_bb[2]) / 2, (outer_bb[1] + outer_bb[3]) / 2)
    ic = ((inner_bb[0] + inner_bb[2]) / 2, (inner_bb[1] + inner_bb[3]) / 2)
    ow = outer_bb[2] - outer_bb[0]
    oh = outer_bb[3] - outer_bb[1]
    if abs(oc[0] - ic[0]) > ow * 0.2 or abs(oc[1] - ic[1]) > oh * 0.2:
        return False

    return True


def _resolve_gradient_color(
    root: ET.Element,
    fill_value: str,
) -> str:
    """Resolve a url(#id) fill reference to a concrete color."""
    if not fill_value or not fill_value.startswith("url("):
        return _parse_color(fill_value)

    ref_match = re.match(r"url\(#([^)]+)\)", fill_value)
    if not ref_match:
        return "transparent"
    ref_id = ref_match.group(1)

    ns = "http://www.w3.org/2000/svg"
    for defs in root.iter("{%s}defs" % ns):
        for child in defs:
            if child.get("id") == ref_id:
                for stop in child.iter("{%s}stop" % ns):
                    color = stop.get("stop-color") or ""
                    style = stop.get("style", "")
                    if not color and "stop-color" in style:
                        for part in style.split(";"):
                            if "stop-color" in part:
                                color = part.split(":", 1)[1].strip()
                    opacity_str = stop.get("stop-opacity")
                    opacity = float(opacity_str) if opacity_str else 1.0
                    if color and opacity > 0:
                        return _parse_color(color)
                for stop in child.iter("{%s}stop" % ns):
                    color = stop.get("stop-color")
                    if color:
                        return _parse_color(color)
    return "transparent"


def _extract_paths(
    root: ET.Element,
    transform: Optional[str] = None,
) -> List[Dict[str, Any]]:
    """Recursively extract path data and style attributes from SVG elements.

    Handles <defs> (stores definitions), <use> (resolves references),
    and standard SVG elements.

    Returns list of dicts with keys: 'd', 'stroke', 'fill', 'transform'.
    """
    results: List[Dict[str, Any]] = []
    defs: Dict[str, ET.Element] = {}  # id → element for <use> resolution

    # First pass: collect <defs> definitions
    def _collect_defs(el: ET.Element) -> None:
        tag = _strip_ns(el.tag)
        if tag == "defs":
            for child in el:
                _register_def(child)
        else:
            for child in el:
                _collect_defs(child)

    def _register_def(el: ET.Element) -> None:
        el_id = el.get("id")
        if el_id:
            defs[el_id] = el
        for child in el:
            _register_def(child)

    _collect_defs(root)

    def _get_style_attrs(el: ET.Element) -> Dict[str, str]:
        style = el.get("style", "")
        attrs: Dict[str, str] = {}
        if style:
            for part in style.split(";"):
                if ":" in part:
                    k, v = part.split(":", 1)
                    attrs[k.strip()] = v.strip()
        return attrs

    def _process(el: ET.Element, parent_transform: str = "") -> None:
        tag = _strip_ns(el.tag)

        # Skip defs — already collected
        if tag == "defs":
            return

        # Accumulate transform
        local_t = el.get("transform", "")
        combined = f"{parent_transform} {local_t}".strip() if parent_transform else local_t

        attrs = _get_style_attrs(el)
        stroke = attrs.get("stroke") or el.get("stroke")
        fill = attrs.get("fill") or el.get("fill")
        stroke_width = attrs.get("stroke-width") or el.get("stroke-width")

        # --- <use> element: resolve reference ---
        if tag == "use":
            href = el.get("href") or el.get("{http://www.w3.org/1999/xlink}href")
            if href and href.startswith("#"):
                ref_id = href[1:]
                if ref_id in defs:
                    ref_el = defs[ref_id]
                    ux = float(el.get("x", "0"))
                    uy = float(el.get("y", "0"))
                    use_transform = combined
                    if ux != 0 or uy != 0:
                        use_transform = f"{use_transform} translate({ux},{uy})".strip()
                    _process(ref_el, use_transform)
            return

        if tag == "path":
            d = el.get("d", "")
            if d:
                results.append({
                    "d": d,
                    "stroke": stroke,
                    "fill": fill,
                    "stroke_width": stroke_width,
                    "transform": combined,
                })

        elif tag == "rect":
            x = float(el.get("x", "0"))
            y = float(el.get("y", "0"))
            w = float(el.get("width", "0"))
            h = float(el.get("height", "0"))
            if w > 0 and h > 0:
                d = f"M{x},{y} L{x+w},{y} L{x+w},{y+h} L{x},{y+h} Z"
                results.append({
                    "d": d,
                    "stroke": stroke,
                    "fill": fill,
                    "stroke_width": stroke_width,
                    "transform": combined,
                })

        elif tag == "circle":
            cx = float(el.get("cx", "0"))
            cy = float(el.get("cy", "0"))
            r = float(el.get("r", "0"))
            if r > 0:
                d = (
                    f"M{cx-r},{cy} "
                    f"A{r},{r} 0 1,0 {cx+r},{cy} "
                    f"A{r},{r} 0 1,0 {cx-r},{cy} Z"
                )
                results.append({
                    "d": d,
                    "stroke": stroke,
                    "fill": fill,
                    "stroke_width": stroke_width,
                    "transform": combined,
                })

        elif tag == "ellipse":
            cx = float(el.get("cx", "0"))
            cy = float(el.get("cy", "0"))
            rx = float(el.get("rx", "0"))
            ry = float(el.get("ry", "0"))
            if rx > 0 and ry > 0:
                d = (
                    f"M{cx-rx},{cy} "
                    f"A{rx},{ry} 0 1,0 {cx+rx},{cy} "
                    f"A{rx},{ry} 0 1,0 {cx-rx},{cy} Z"
                )
                results.append({
                    "d": d,
                    "stroke": stroke,
                    "fill": fill,
                    "stroke_width": stroke_width,
                    "transform": combined,
                })

        elif tag == "line":
            x1 = float(el.get("x1", "0"))
            y1 = float(el.get("y1", "0"))
            x2 = float(el.get("x2", "0"))
            y2 = float(el.get("y2", "0"))
            d = f"M{x1},{y1} L{x2},{y2}"
            results.append({
                "d": d,
                "stroke": stroke,
                "fill": fill,
                "stroke_width": stroke_width,
                "transform": combined,
            })

        elif tag == "polygon" or tag == "polyline":
            pts_str = el.get("points", "")
            if pts_str:
                coords = re.findall(r"-?\d*\.?\d+", pts_str)
                if len(coords) >= 4:
                    parts = [f"M{coords[0]},{coords[1]}"]
                    for i in range(2, len(coords) - 1, 2):
                        parts.append(f"L{coords[i]},{coords[i+1]}")
                    if tag == "polygon":
                        parts.append("Z")
                    d = " ".join(parts)
                    results.append({
                        "d": d,
                        "stroke": stroke,
                        "fill": fill,
                        "stroke_width": stroke_width,
                        "transform": combined,
                    })

        # Recurse into children
        for child in el:
            _process(child, combined)

    _process(root)
    return results


def _compose_matrix(m1: List[float], m2: List[float]) -> List[float]:
    """Compose two 2D affine matrices [a, b, c, d, e, f]: m1 * m2."""
    a1, b1, c1, d1, e1, f1 = m1
    a2, b2, c2, d2, e2, f2 = m2
    return [
        a1 * a2 + c1 * b2,
        b1 * a2 + d1 * b2,
        a1 * c2 + c1 * d2,
        b1 * c2 + d1 * d2,
        a1 * e2 + c1 * f2 + e1,
        b1 * e2 + d1 * f2 + f1,
    ]


def _apply_matrix(matrix: List[float], x: float, y: float) -> Tuple[float, float]:
    """Apply affine matrix [a, b, c, d, e, f] to point (x, y)."""
    a, b, c, d, e, f = matrix
    return (a * x + c * y + e, b * x + d * y + f)


def _parse_transform_matrix(transform: str) -> List[float]:
    """Parse SVG transform string into a 2D affine matrix [a, b, c, d, e, f].

    The transform maps point (x, y) to:
      x' = a*x + c*y + e
      y' = b*x + d*y + f

    Handles all occurrences of translate(), scale(), matrix(), rotate()
    composed left-to-right (outer to inner in SVG coordinate terms).

    Identity: [1, 0, 0, 1, 0, 0]
    """
    result: List[float] = [1.0, 0.0, 0.0, 1.0, 0.0, 0.0]

    if not transform:
        return result

    for m in re.finditer(
        r"(matrix|translate|scale|rotate)\s*\(([^)]+)\)", transform
    ):
        op = m.group(1)
        params = [
            float(x) for x in re.split(r"[\s,]+", m.group(2).strip()) if x
        ]

        if op == "matrix" and len(params) >= 6:
            result = _compose_matrix(result, params[:6])

        elif op == "translate":
            tx = params[0] if len(params) >= 1 else 0.0
            ty = params[1] if len(params) >= 2 else 0.0
            result = _compose_matrix(result, [1, 0, 0, 1, tx, ty])

        elif op == "scale":
            sx = params[0] if len(params) >= 1 else 1.0
            sy = params[1] if len(params) >= 2 else sx
            result = _compose_matrix(result, [sx, 0, 0, sy, 0, 0])

        elif op == "rotate":
            angle = math.radians(params[0]) if params else 0.0
            cos_a = math.cos(angle)
            sin_a = math.sin(angle)
            if len(params) >= 3:
                cx_r, cy_r = params[1], params[2]
                result = _compose_matrix(result, [1, 0, 0, 1, cx_r, cy_r])
                result = _compose_matrix(
                    result, [cos_a, sin_a, -sin_a, cos_a, 0, 0]
                )
                result = _compose_matrix(
                    result, [1, 0, 0, 1, -cx_r, -cy_r]
                )
            else:
                result = _compose_matrix(
                    result, [cos_a, sin_a, -sin_a, cos_a, 0, 0]
                )

    return result


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------
def _convert_path_to_elements(
    path_info: Dict[str, Any],
    offset_x: float,
    offset_y: float,
    scale: float,
    default_stroke: str,
    default_sw: int,
    roughness: int,
) -> List[Dict[str, Any]]:
    """Convert a single SVG path into Excalidraw elements."""
    d = path_info["d"]
    stroke = _parse_color(path_info.get("stroke")) or default_stroke
    raw_fill = path_info.get("fill", "")
    if raw_fill and raw_fill.startswith("url(") and path_info.get("_root") is not None:
        fill = _resolve_gradient_color(path_info["_root"], raw_fill)
    else:
        fill = _parse_color(raw_fill)
    sw_str = path_info.get("stroke_width")
    sw = int(float(sw_str)) if sw_str else default_sw

    # Build element-level affine transform matrix
    element_matrix = _parse_transform_matrix(path_info.get("transform", ""))
    # Compose viewBox scale + offset with element transform
    viewbox_matrix: List[float] = [scale, 0, 0, scale, offset_x, offset_y]
    total_matrix = _compose_matrix(viewbox_matrix, element_matrix)

    commands = _tokenize_path(d)
    polylines = _parse_path_commands(commands)

    elements: List[Dict[str, Any]] = []
    for raw_pts in polylines:
        if len(raw_pts) < 2:
            continue

        # Apply affine transform to every point
        pts = [_apply_matrix(total_matrix, p[0], p[1]) for p in raw_pts]

        # Simplify
        pts = simplify_polyline(pts)

        if len(pts) < 2:
            continue

        # Classify
        shape = classify_polyline(pts)

        if shape["type"] == "ellipse":
            el = engine.ellipse(
                shape["x"], shape["y"],
                shape["width"], shape["height"],
                fill=fill if fill != "transparent" else "transparent",
                stroke=stroke,
                sw=sw,
                roughness=roughness,
            )
            elements.append(el)

        elif shape["type"] == "rectangle":
            el = engine.rect(
                shape["x"], shape["y"],
                shape["width"], shape["height"],
                fill=fill if fill != "transparent" else "transparent",
                stroke=stroke,
                sw=sw,
                roughness=roughness,
            )
            elements.append(el)

        else:  # line
            # Compute bounding box for the line element
            min_x = min(p[0] for p in pts)
            min_y = min(p[1] for p in pts)
            # Convert to relative points
            rel_pts = [[p[0] - min_x, p[1] - min_y] for p in pts]
            dx = max(p[0] for p in pts) - min_x
            dy = max(p[1] for p in pts) - min_y

            closed = _is_path_closed(raw_pts)
            el = {
                "id": engine.uid(), "type": "line",
                "x": min_x, "y": min_y,
                "width": max(dx, 1), "height": max(dy, 1),
                "angle": 0, "strokeColor": stroke,
                "backgroundColor": fill if closed and fill != "transparent" else "transparent",
                "fillStyle": "solid",
                "strokeWidth": sw, "strokeStyle": "solid",
                "roughness": roughness, "opacity": 100, "groupIds": [],
                "roundness": {"type": 2}, "seed": engine.sd(), "version": 1,
                "versionNonce": engine.sd(), "isDeleted": False,
                "boundElements": [],
                "updated": engine.ts(), "link": None, "locked": False,
                "points": rel_pts,
                "startBinding": None, "endBinding": None,
                "startArrowhead": None, "endArrowhead": None,
                "elbowed": False,
            }
            elements.append(el)

    return elements


def svg_to_elements(
    svg_string: str,
    x: float = 0,
    y: float = 0,
    scale: float = 1.0,
    stroke: str = "#1e1e1e",
    stroke_width: int = 2,
    roughness: int = 1,
) -> List[Dict[str, Any]]:
    """Convert an SVG string to a list of Excalidraw element dicts.

    Args:
        svg_string: SVG content as a string.
        x: X offset for the generated elements.
        y: Y offset for the generated elements.
        scale: Scale factor applied to all coordinates.
        stroke: Default stroke color.
        stroke_width: Default stroke width.
        roughness: Excalidraw roughness (0=precise, 1=slight, 2=rough).

    Returns:
        List of Excalidraw element dicts.
    """
    root = ET.fromstring(svg_string)

    # Get viewBox for scaling
    viewbox = root.get("viewBox")
    if viewbox:
        parts = viewbox.split()
        if len(parts) == 4:
            vb_w = float(parts[2])
            vb_h = float(parts[3])
            if vb_w > 0 and vb_h > 0:
                # Normalize to a reasonable size
                max_dim = max(vb_w, vb_h)
                scale *= 100.0 / max_dim

    paths = _extract_paths(root)
    all_elements: List[Dict[str, Any]] = []

    for path_info in paths:
        path_info["_root"] = root  # for gradient resolution
        els = _convert_path_to_elements(
            path_info, x, y, scale, stroke, stroke_width, roughness
        )
        all_elements.extend(els)

    return all_elements


def svg_file_to_elements(
    filepath: str,
    x: float = 0,
    y: float = 0,
    scale: float = 1.0,
    stroke: str = "#1e1e1e",
    stroke_width: int = 2,
    roughness: int = 1,
) -> List[Dict[str, Any]]:
    """Convert an SVG file to a list of Excalidraw element dicts.

    Args:
        filepath: Path to the SVG file.
        x: X offset for the generated elements.
        y: Y offset for the generated elements.
        scale: Scale factor applied to all coordinates.
        stroke: Default stroke color.
        stroke_width: Default stroke width.
        roughness: Excalidraw roughness (0=precise, 1=slight, 2=rough).

    Returns:
        List of Excalidraw element dicts.
    """
    with open(filepath, "r", encoding="utf-8") as f:
        svg_string = f.read()
    return svg_to_elements(svg_string, x, y, scale, stroke, stroke_width, roughness)

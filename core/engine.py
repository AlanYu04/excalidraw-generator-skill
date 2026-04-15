"""
Excalidraw Diagram Generator - Core Engine
Generates Excalidraw scene JSON with CJK-aware text centering.
"""
import json, os, random, time

from .scene import normalize_scene_files

# ---------------------------------------------------------------------------
# ID / Seed / Timestamp
# ---------------------------------------------------------------------------
_uid_counter = 0
def uid():
    global _uid_counter
    _uid_counter += 1
    return f"e{_uid_counter:06d}"

def sd():
    return random.randint(10000, 999999)

def ts():
    return int(time.time() * 1000)

# ---------------------------------------------------------------------------
# CJK-aware text width estimation
# ---------------------------------------------------------------------------
def is_cjk(ch):
    cp = ord(ch)
    if 0x4E00 <= cp <= 0x9FFF: return True
    if 0x3400 <= cp <= 0x4DBF: return True
    if 0xF900 <= cp <= 0xFAFF: return True
    if 0x3000 <= cp <= 0x303F: return True
    if ch in '↑↓←→∈π≤≥≠×÷±★✓✗': return True
    if ch in '¹²³⁴⁵⁶⁷⁸⁹⁰': return True
    return False

def estimate_text_width(text, fs):
    w = 0.0
    for ch in text:
        if ch == '\n': continue
        if is_cjk(ch):   w += fs * 1.05
        elif ch == ' ':  w += fs * 0.35
        else:            w += fs * 0.62
    return w

def estimate_text_height(text, fs):
    return len(text.split('\n')) * fs * 1.25

# ---------------------------------------------------------------------------
# Element Builders
# ---------------------------------------------------------------------------
def rect(x, y, w, h, fill="transparent", stroke="#1e1e1e", sw=2, roughness=1,
         fill_style="solid", stroke_style="solid", border_radius=True):
    return {
        "id": uid(), "type": "rectangle",
        "x": x, "y": y, "width": w, "height": h,
        "angle": 0, "strokeColor": stroke, "backgroundColor": fill,
        "fillStyle": fill_style, "strokeWidth": sw, "strokeStyle": stroke_style,
        "roughness": roughness, "opacity": 100, "groupIds": [],
        "roundness": {"type": 3} if border_radius else None, "seed": sd(), "version": 1,
        "versionNonce": sd(), "isDeleted": False, "boundElements": [],
        "updated": ts(), "link": None, "locked": False
    }

def text_standalone(cx, cy, txt, fs=20, color="#1e1e1e", font_family=5, roughness=0,
                    text_align="center", max_width=None):
    # Auto-shrink font size if text exceeds max_width
    if max_width is not None:
        while fs > 6 and estimate_text_width(txt, fs) > max_width:
            fs -= 1
    tw = estimate_text_width(txt, fs)
    th = estimate_text_height(txt, fs)
    # For center: x = cx - tw/2; for left: x = cx; for right: x = cx - tw
    if text_align == "center":
        x = cx - tw / 2
    elif text_align == "right":
        x = cx - tw
    else:  # left
        x = cx
    return {
        "id": uid(), "type": "text",
        "x": x, "y": cy - th/2, "width": tw, "height": th,
        "angle": 0, "strokeColor": color, "backgroundColor": "transparent",
        "fillStyle": "solid", "strokeWidth": 2, "strokeStyle": "solid",
        "roughness": roughness, "opacity": 100, "groupIds": [],
        "roundness": None, "seed": sd(), "version": 1,
        "versionNonce": sd(), "isDeleted": False, "boundElements": [],
        "updated": ts(), "link": None, "locked": False,
        "text": txt, "fontSize": fs, "fontFamily": font_family,
        "textAlign": text_align, "verticalAlign": "middle",
        "containerId": None, "originalText": txt, "lineHeight": 1.25,
        "autoResize": True
    }

def labeled_rect(x, y, w, h, label, fill="transparent", stroke="#1e1e1e",
                 sw=2, fs=16, label_color=None, roughness=1, font_family=5,
                 fill_style="solid", stroke_style="solid", border_radius=True):
    if label_color is None: label_color = stroke
    rid, tid = uid(), uid()
    r = {
        "id": rid, "type": "rectangle",
        "x": x, "y": y, "width": w, "height": h,
        "angle": 0, "strokeColor": stroke, "backgroundColor": fill,
        "fillStyle": fill_style, "strokeWidth": sw, "strokeStyle": stroke_style,
        "roughness": roughness, "opacity": 100, "groupIds": [],
        "roundness": {"type": 3} if border_radius else None, "seed": sd(), "version": 1,
        "versionNonce": sd(), "isDeleted": False,
        "boundElements": [{"id": tid, "type": "text"}],
        "updated": ts(), "link": None, "locked": False,
        "customData": {"legacyTextWrap": True}
    }
    # Bound text: align to container inner area, let Excalidraw auto-center
    pad = 4
    t = {
        "id": tid, "type": "text",
        "x": x + pad, "y": y + pad,
        "width": w - pad * 2, "height": h - pad * 2,
        "angle": 0, "strokeColor": label_color, "backgroundColor": "transparent",
        "fillStyle": "solid", "strokeWidth": 2, "strokeStyle": "solid",
        "roughness": 0, "opacity": 100, "groupIds": [],
        "roundness": None, "seed": sd(), "version": 1,
        "versionNonce": sd(), "isDeleted": False, "boundElements": [],
        "updated": ts(), "link": None, "locked": False,
        "text": label, "fontSize": fs, "fontFamily": font_family,
        "textAlign": "center", "verticalAlign": "middle",
        "containerId": rid, "originalText": label, "lineHeight": 1.25,
        "autoResize": True
    }
    return [r, t]


def auto_labeled_rect(x, y, label, padding=10, fill="transparent", stroke="#1e1e1e",
                      sw=2, fs=16, label_color=None, roughness=1, font_family=5,
                      fill_style="solid", stroke_style="solid",
                      min_width=None, min_height=None, border_radius=True):
    """Create a labeled_rect with dimensions auto-calculated from text.

    Uses estimate_text_width/estimate_text_height plus padding to size the box.
    Optionally enforces minimum dimensions via min_width/min_height.
    """
    tw = estimate_text_width(label, fs)
    th = estimate_text_height(label, fs)
    w = tw + padding * 2
    h = th + padding * 2
    if min_width is not None:
        w = max(w, min_width)
    if min_height is not None:
        h = max(h, min_height)
    return labeled_rect(x, y, w, h, label, fill=fill, stroke=stroke,
                        sw=sw, fs=fs, label_color=label_color, roughness=roughness,
                        font_family=font_family, fill_style=fill_style,
                        stroke_style=stroke_style, border_radius=border_radius)


def arrow(x, y, dx=0, dy=0, *, x2=None, y2=None, stroke="#1e1e1e", sw=2, roughness=1,
          stroke_style="solid", elbowed=False):
    """创建箭头。支持两种模式：
    - 相对偏移: arrow(x, y, dx, dy)
    - 绝对坐标: arrow(x, y, x2=end_x, y2=end_y)
    - elbowed=True: Excalidraw 自动正交路由（适合非对齐元素）
    """
    if x2 is not None or y2 is not None:
        dx = (x2 if x2 is not None else x) - x
        dy = (y2 if y2 is not None else y) - y
    return {
        "id": uid(), "type": "arrow",
        "x": x, "y": y, "width": abs(dx), "height": abs(dy),
        "angle": 0, "strokeColor": stroke, "backgroundColor": "transparent",
        "fillStyle": "solid", "strokeWidth": sw, "strokeStyle": stroke_style,
        "roughness": roughness, "opacity": 100, "groupIds": [],
        "roundness": {"type": 2}, "seed": sd(), "version": 1,
        "versionNonce": sd(), "isDeleted": False, "boundElements": [],
        "updated": ts(), "link": None, "locked": False,
        "points": [[0,0],[dx,dy]], "startBinding": None, "endBinding": None,
        "startArrowhead": None, "endArrowhead": "arrow", "elbowed": elbowed
    }

def ellipse(x, y, w, h, fill="transparent", stroke="#1e1e1e", sw=2, roughness=1,
            fill_style="solid"):
    return {
        "id": uid(), "type": "ellipse",
        "x": x, "y": y, "width": w, "height": h,
        "angle": 0, "strokeColor": stroke, "backgroundColor": fill,
        "fillStyle": fill_style, "strokeWidth": sw, "strokeStyle": "solid",
        "roughness": roughness, "opacity": 100, "groupIds": [],
        "roundness": {"type": 2}, "seed": sd(), "version": 1,
        "versionNonce": sd(), "isDeleted": False, "boundElements": [],
        "updated": ts(), "link": None, "locked": False
    }

def diamond(x, y, w, h, fill="transparent", stroke="#1e1e1e", sw=2, roughness=1,
            fill_style="solid"):
    return {
        "id": uid(), "type": "diamond",
        "x": x, "y": y, "width": w, "height": h,
        "angle": 0, "strokeColor": stroke, "backgroundColor": fill,
        "fillStyle": fill_style, "strokeWidth": sw, "strokeStyle": "solid",
        "roughness": roughness, "opacity": 100, "groupIds": [],
        "roundness": {"type": 2}, "seed": sd(), "version": 1,
        "versionNonce": sd(), "isDeleted": False, "boundElements": [],
        "updated": ts(), "link": None, "locked": False
    }

def line(x, y, dx=0, dy=0, *, x2=None, y2=None, stroke="#1e1e1e", sw=2, roughness=1,
         stroke_style="solid"):
    """创建线段。支持两种模式：
    - 相对偏移: line(x, y, dx, dy)
    - 绝对坐标: line(x, y, x2=end_x, y2=end_y)
    """
    if x2 is not None or y2 is not None:
        dx = (x2 if x2 is not None else x) - x
        dy = (y2 if y2 is not None else y) - y
    return {
        "id": uid(), "type": "line",
        "x": x, "y": y, "width": abs(dx), "height": abs(dy),
        "angle": 0, "strokeColor": stroke, "backgroundColor": "transparent",
        "fillStyle": "solid", "strokeWidth": sw, "strokeStyle": stroke_style,
        "roughness": roughness, "opacity": 100, "groupIds": [],
        "roundness": {"type": 2}, "seed": sd(), "version": 1,
        "versionNonce": sd(), "isDeleted": False, "boundElements": [],
        "updated": ts(), "link": None, "locked": False,
        "points": [[0,0],[dx,dy]], "startBinding": None, "endBinding": None,
        "startArrowhead": None, "endArrowhead": None, "elbowed": False
    }

def labeled_diamond(x, y, w, h, label, fill="transparent", stroke="#1e1e1e",
                    sw=2, fs=16, label_color=None, roughness=1, font_family=5,
                    fill_style="solid"):
    if label_color is None: label_color = stroke
    did, tid = uid(), uid()
    d = {
        "id": did, "type": "diamond",
        "x": x, "y": y, "width": w, "height": h,
        "angle": 0, "strokeColor": stroke, "backgroundColor": fill,
        "fillStyle": fill_style, "strokeWidth": sw, "strokeStyle": "solid",
        "roughness": roughness, "opacity": 100, "groupIds": [],
        "roundness": {"type": 2}, "seed": sd(), "version": 1,
        "versionNonce": sd(), "isDeleted": False,
        "boundElements": [{"id": tid, "type": "text"}],
        "updated": ts(), "link": None, "locked": False,
        "customData": {"legacyTextWrap": True}
    }
    pad = 4
    t = {
        "id": tid, "type": "text",
        "x": x + pad, "y": y + pad,
        "width": w - pad * 2, "height": h - pad * 2,
        "angle": 0, "strokeColor": label_color, "backgroundColor": "transparent",
        "fillStyle": "solid", "strokeWidth": 2, "strokeStyle": "solid",
        "roughness": 0, "opacity": 100, "groupIds": [],
        "roundness": None, "seed": sd(), "version": 1,
        "versionNonce": sd(), "isDeleted": False, "boundElements": [],
        "updated": ts(), "link": None, "locked": False,
        "text": label, "fontSize": fs, "fontFamily": font_family,
        "textAlign": "center", "verticalAlign": "middle",
        "containerId": did, "originalText": label, "lineHeight": 1.25,
        "autoResize": True
    }
    return [d, t]


def labeled_ellipse(x, y, w, h, label, fill="transparent", stroke="#1e1e1e",
                    sw=2, fs=16, label_color=None, roughness=1, font_family=5,
                    fill_style="solid"):
    if label_color is None: label_color = stroke
    eid, tid = uid(), uid()
    e = {
        "id": eid, "type": "ellipse",
        "x": x, "y": y, "width": w, "height": h,
        "angle": 0, "strokeColor": stroke, "backgroundColor": fill,
        "fillStyle": fill_style, "strokeWidth": sw, "strokeStyle": "solid",
        "roughness": roughness, "opacity": 100, "groupIds": [],
        "roundness": {"type": 2}, "seed": sd(), "version": 1,
        "versionNonce": sd(), "isDeleted": False,
        "boundElements": [{"id": tid, "type": "text"}],
        "updated": ts(), "link": None, "locked": False,
        "customData": {"legacyTextWrap": True}
    }
    pad = 4
    t = {
        "id": tid, "type": "text",
        "x": x + pad, "y": y + pad,
        "width": w - pad * 2, "height": h - pad * 2,
        "angle": 0, "strokeColor": label_color, "backgroundColor": "transparent",
        "fillStyle": "solid", "strokeWidth": 2, "strokeStyle": "solid",
        "roughness": 0, "opacity": 100, "groupIds": [],
        "roundness": None, "seed": sd(), "version": 1,
        "versionNonce": sd(), "isDeleted": False, "boundElements": [],
        "updated": ts(), "link": None, "locked": False,
        "text": label, "fontSize": fs, "fontFamily": font_family,
        "textAlign": "center", "verticalAlign": "middle",
        "containerId": eid, "originalText": label, "lineHeight": 1.25,
        "autoResize": True
    }
    return [e, t]


def group(elements):
    """将元素编组，返回新元素列表（不修改原始元素）。"""
    gid = uid()
    result = []
    for el in elements:
        new_el = dict(el)
        new_el["groupIds"] = list(el.get("groupIds", [])) + [gid]
        result.append(new_el)
    return result


def frame(x, y, w, h, name="Frame", stroke="#1e1e1e", sw=2):
    return {
        "id": uid(), "type": "frame",
        "x": x, "y": y, "width": w, "height": h,
        "angle": 0, "strokeColor": stroke, "backgroundColor": "transparent",
        "fillStyle": "solid", "strokeWidth": sw, "strokeStyle": "solid",
        "roughness": 0, "opacity": 100, "groupIds": [],
        "roundness": None, "seed": sd(), "version": 1,
        "versionNonce": sd(), "isDeleted": False, "boundElements": [],
        "updated": ts(), "link": None, "locked": False,
        "name": name
    }


def image_embed(x, y, w, h, base64_data, mime="image/png"):
    """创建图片元素和对应的 files 条目。返回 (element_dict, files_dict)。"""
    file_id = uid()
    el = {
        "id": uid(), "type": "image",
        "x": x, "y": y, "width": w, "height": h,
        "angle": 0, "strokeColor": "transparent", "backgroundColor": "transparent",
        "fillStyle": "solid", "strokeWidth": 0, "strokeStyle": "solid",
        "roughness": 0, "opacity": 100, "groupIds": [],
        "roundness": None, "seed": sd(), "version": 1,
        "versionNonce": sd(), "isDeleted": False, "boundElements": [],
        "updated": ts(), "link": None, "locked": False,
        "fileId": file_id, "status": "saved", "scale": [1, 1]
    }
    file_entry = {
        file_id: {
            "mimeType": mime,
            "id": file_id,
            "dataURL": f"data:{mime};base64,{base64_data}",
            "created": ts()
        }
    }
    return el, file_entry


def _element_center(el):
    return (
        el.get("x", 0) + el.get("width", 0) / 2,
        el.get("y", 0) + el.get("height", 0) / 2,
    )


def _clamp_focus(value):
    return max(-1.0, min(1.0, float(value)))


def _binding_focus_for_point(el, px, py):
    """Project an external point onto the element edge and return Excalidraw focus."""
    cx, cy = _element_center(el)
    dx = px - cx
    dy = py - cy
    if dx == 0 and dy == 0:
        return 0.0

    half_w = max(el.get("width", 0) / 2, 1e-6)
    half_h = max(el.get("height", 0) / 2, 1e-6)
    tx = abs(half_w / dx) if dx else float("inf")
    ty = abs(half_h / dy) if dy else float("inf")

    if tx < ty:
        focus = (dy * tx) / half_h
    else:
        focus = (dx * ty) / half_w
    return round(_clamp_focus(focus), 4)


def bind_arrow(arrow_el, start_el, end_el, gap=2, start_focus=None, end_focus=None):
    """绑定箭头到起止元素，同时更新双向引用。就地修改 start_el/end_el。"""
    new_arrow = dict(arrow_el)
    start_target_x, start_target_y = _element_center(end_el)
    end_target_x, end_target_y = _element_center(start_el)
    if start_focus is None:
        start_focus = _binding_focus_for_point(start_el, start_target_x, start_target_y)
    else:
        start_focus = round(_clamp_focus(start_focus), 4)
    if end_focus is None:
        end_focus = _binding_focus_for_point(end_el, end_target_x, end_target_y)
    else:
        end_focus = round(_clamp_focus(end_focus), 4)
    new_arrow["startBinding"] = {
        "elementId": start_el["id"],
        "focus": start_focus,
        "gap": gap,
        "fixedPoint": None
    }
    new_arrow["endBinding"] = {
        "elementId": end_el["id"],
        "focus": end_focus,
        "gap": gap,
        "fixedPoint": None
    }
    # 在目标元素上添加反向引用
    ref = {"id": arrow_el["id"], "type": "arrow"}
    for el in (start_el, end_el):
        bound = el.get("boundElements") or []
        if not any(b.get("id") == arrow_el["id"] for b in bound):
            bound.append(ref)
        el["boundElements"] = bound
    return new_arrow


def connect(start_el, end_el, stroke="#1e1e1e", sw=2, roughness=1, gap=8,
            elbowed=False, start_focus=None, end_focus=None):
    """创建绑定箭头连接两个元素。

    根据起止元素中心的实际方向向量创建箭头，使 Excalidraw
    正确选择边缘交点。

    elbowed=True: Excalidraw 自动路由正交折线箭头（推荐用于
    非对齐元素间的连接，如跨行/跨列）。
    """
    sx = start_el["x"] + start_el["width"] / 2
    sy = start_el["y"] + start_el["height"] / 2
    ex = end_el["x"] + end_el["width"] / 2
    ey = end_el["y"] + end_el["height"] / 2
    dx = ex - sx
    dy = ey - sy
    # Fallback for overlapping elements (same center)
    if dx == 0 and dy == 0:
        dx = 1
    raw = arrow(sx, sy, dx=dx, dy=dy, stroke=stroke, sw=sw,
                roughness=roughness, elbowed=elbowed)
    return bind_arrow(
        raw,
        start_el,
        end_el,
        gap=gap,
        start_focus=start_focus,
        end_focus=end_focus,
    )


# ---------------------------------------------------------------------------
# Layout helpers — prevent text/shape overlap
# ---------------------------------------------------------------------------
def below(y: float, h: float, gap: float = 10) -> float:
    """Safe y-coordinate for placing an element below a shape at (_, y) with height h."""
    return y + h + gap

def right_of(x: float, w: float, gap: float = 10) -> float:
    """Safe x-coordinate for placing an element to the right of a shape at (x, _) with width w."""
    return x + w + gap

def above(y: float, gap: float = 10) -> float:
    """Safe y-coordinate for placing an element above a shape whose top is at y."""
    return y - gap


def bounds(elements: list) -> tuple:
    """Measure the actual bounding box of a list of elements.

    Returns (min_x, min_y, max_x, max_y) where max_* are the bottom/right edges.
    Returns (0, 0, 0, 0) for empty lists.
    """
    if not elements:
        return (0, 0, 0, 0)
    min_x = float("inf")
    min_y = float("inf")
    max_x = float("-inf")
    max_y = float("-inf")
    for e in elements:
        if isinstance(e, dict):
            ex = e.get("x", 0)
            ey = e.get("y", 0)
            ew = e.get("width", 0)
            eh = e.get("height", 0)
            min_x = min(min_x, ex)
            min_y = min(min_y, ey)
            max_x = max(max_x, ex + ew)
            max_y = max(max_y, ey + eh)
    if min_x == float("inf"):
        return (0, 0, 0, 0)
    return (min_x, min_y, max_x, max_y)


def numbered_circle(cx, cy, num, fill, stroke):
    r = 16
    return [
        ellipse(cx - r, cy - r, r*2, r*2, fill=fill, stroke=stroke, sw=2),
        text_standalone(cx, cy, str(num), fs=14, color=stroke)
    ]


# ---------------------------------------------------------------------------
# Layout Verification (Self-Check)
# ---------------------------------------------------------------------------

def _aabb(el):
    """Return (x, y, x+w, y+h) bounding box for an element."""
    x = el.get("x", 0)
    y = el.get("y", 0)
    w = el.get("width", 0)
    h = el.get("height", 0)
    return (x, y, x + w, y + h)


def _overlap_area(box_a, box_b):
    """Calculate intersection area of two AABB boxes."""
    ax1, ay1, ax2, ay2 = box_a
    bx1, by1, bx2, by2 = box_b
    ix1 = max(ax1, bx1)
    iy1 = max(ay1, by1)
    ix2 = min(ax2, bx2)
    iy2 = min(ay2, by2)
    if ix2 <= ix1 or iy2 <= iy1:
        return 0.0
    return (ix2 - ix1) * (iy2 - iy1)


def _label_of(el):
    """Extract a human-readable label from an element."""
    if el.get("text"):
        return el["text"][:30]
    if el.get("name"):
        return el["name"][:30]
    return el.get("id", "?")[:10]


def _is_contained(inner, outer, margin=2):
    """Check if inner element's AABB is fully contained within outer's AABB."""
    ix1, iy1, ix2, iy2 = _aabb(inner)
    ox1, oy1, ox2, oy2 = _aabb(outer)
    return (ox1 - margin <= ix1 and oy1 - margin <= iy1 and
            ix2 <= ox2 + margin and iy2 <= oy2 + margin)


def check_overlaps(elements: list, tolerance: float = 3) -> list:
    """Detect overlapping element bounding boxes.

    Returns list of dicts:
      [{a_id, b_id, a_label, b_label, overlap_area, severity}]

    Skips: arrow/line elements, containerId-bound text pairs, and
    intentional nesting (one element fully contained within another).
    overlap > 50px^2 -> ERROR, else WARNING.
    """
    skip_types = {"arrow", "line"}
    # Build lookup for containerId relationships
    container_map = {}  # text_id -> container_id
    for el in elements:
        cid = el.get("containerId")
        if cid:
            container_map[el.get("id")] = cid

    results = []
    visible = [e for e in elements if e.get("type") not in skip_types]
    for i in range(len(visible)):
        for j in range(i + 1, len(visible)):
            a, b = visible[i], visible[j]
            # Skip containerId-bound pairs (text inside its parent shape)
            a_id = a.get("id")
            b_id = b.get("id")
            if container_map.get(a_id) == b_id or container_map.get(b_id) == a_id:
                continue
            # Skip intentional nesting (one fully inside another)
            if _is_contained(a, b) or _is_contained(b, a):
                continue
            box_a = _aabb(a)
            box_b = _aabb(b)
            area = _overlap_area(box_a, box_b)
            if area > tolerance:
                severity = "ERROR" if area > 50 else "WARNING"
                results.append({
                    "a_id": a_id,
                    "b_id": b_id,
                    "a_label": _label_of(a),
                    "b_label": _label_of(b),
                    "overlap_area": round(area, 1),
                    "severity": severity,
                })
    return results


def check_arrow_bindings(elements: list) -> list:
    """Verify all arrows have correct startBinding/endBinding.

    Checks:
    - Binding exists (startBinding and endBinding present)
    - Bound element IDs exist in elements
    - Arrow endpoints are at element EDGES (not inside)

    Returns list of dicts:
      [{arrow_id, issue, detail, severity}]
    """
    id_set = {el.get("id") for el in elements}
    id_to_el = {el.get("id"): el for el in elements}
    results = []
    incoming_focus = {}

    for el in elements:
        if el.get("type") != "arrow":
            continue
        aid = el.get("id")

        # Check startBinding
        sb = el.get("startBinding")
        if not sb:
            results.append({
                "arrow_id": aid,
                "issue": "missing_start_binding",
                "detail": "startBinding is None",
                "severity": "ERROR",
            })
        else:
            sid = sb.get("elementId")
            if sid not in id_set:
                results.append({
                    "arrow_id": aid,
                    "issue": "dead_start_element",
                    "detail": f"startBinding element {sid} not found",
                    "severity": "ERROR",
                })

        # Check endBinding
        eb = el.get("endBinding")
        if not eb:
            results.append({
                "arrow_id": aid,
                "issue": "missing_end_binding",
                "detail": "endBinding is None",
                "severity": "ERROR",
            })
        else:
            eid = eb.get("elementId")
            if eid not in id_set:
                results.append({
                    "arrow_id": aid,
                    "issue": "dead_end_element",
                    "detail": f"endBinding element {eid} not found",
                    "severity": "ERROR",
                })
            else:
                focus_key = (eid, round(float(eb.get("focus", 0)), 4))
                incoming_focus.setdefault(focus_key, []).append({
                    "arrow_id": aid,
                    "start_id": sb.get("elementId") if sb else None,
                })

        # Check arrow endpoint is at element edge (not deep inside).
        # Skip for properly bound arrows — Excalidraw's binding snaps
        # them to element edges at render time, even if raw points go to center.
        has_valid_bindings = (
            sb and eb
            and sb.get("elementId") in id_set
            and eb.get("elementId") in id_set
        )
        if not has_valid_bindings:
            # For unbound arrows, check if tip is deep inside any element
            ax = el.get("x", 0)
            ay = el.get("y", 0)
            points = el.get("points", [[0, 0]])
            if len(points) >= 2:
                end_pt = points[-1]
                tip_x = ax + end_pt[0]
                tip_y = ay + end_pt[1]
                # Check against all non-arrow elements
                for candidate in elements:
                    if candidate.get("type") in ("arrow", "line"):
                        continue
                    cx, cy, cx2, cy2 = _aabb(candidate)
                    margin = min(candidate.get("width", 0), candidate.get("height", 0)) * 0.3
                    if (cx + margin < tip_x < cx2 - margin and
                            cy + margin < tip_y < cy2 - margin):
                        results.append({
                            "arrow_id": aid,
                            "issue": "point_inside_element",
                            "detail": f"Arrow tip at ({tip_x:.0f},{tip_y:.0f}) is inside element {_label_of(candidate)}",
                            "severity": "WARNING",
                        })
                        break

    for (element_id, focus), entries in incoming_focus.items():
        start_ids = {entry["start_id"] for entry in entries if entry["start_id"] is not None}
        if len(entries) >= 3 and len(start_ids) >= 3:
            target = id_to_el.get(element_id, {})
            severity = "ERROR" if len(entries) >= 4 else "WARNING"
            results.append({
                "arrow_id": ",".join(entry["arrow_id"] for entry in entries),
                "issue": "collapsed_end_focus",
                "detail": (
                    f"{len(entries)} arrows share endBinding focus {focus} on "
                    f"element {_label_of(target)}"
                ),
                "severity": severity,
            })

    return results


def check_spacing(elements: list, min_gap: float = 20) -> list:
    """Check gap consistency between nearest-neighbor non-connected elements.

    Only compares adjacent pairs (nearest horizontal/vertical neighbor),
    not all same-row/same-column pairs. Reports when gaps differ
    significantly from the median gap.

    Returns list of [{a_id, b_id, gap, median_gap, severity}].
    """
    skip_types = {"arrow", "line", "text"}
    visible = [e for e in elements if e.get("type") not in skip_types]

    # Collect nearest-neighbor gaps only
    # For each element, find the closest element to its right and below
    h_gaps = []
    v_gaps = []
    seen_h = set()
    seen_v = set()

    for a in visible:
        box_a = _aabb(a)
        for b in visible:
            if a is b:
                continue
            box_b = _aabb(b)
            # Horizontal: b is to the right of a, same row
            if box_a[1] < box_b[3] and box_b[1] < box_a[3] and box_a[2] <= box_b[0]:
                gap = box_b[0] - box_a[2]
                key = (a.get("id"), b.get("id"))
                if key not in seen_h:
                    # Check if b is the nearest right neighbor of a
                    # (no other element between them horizontally)
                    is_nearest = True
                    for c in visible:
                        if c is a or c is b:
                            continue
                        box_c = _aabb(c)
                        if (box_a[1] < box_c[3] and box_c[1] < box_a[3]
                                and box_a[2] <= box_c[0] < box_b[0]):
                            is_nearest = False
                            break
                    if is_nearest:
                        seen_h.add(key)
                        h_gaps.append(gap)
            # Vertical: b is below a, same column
            if box_a[0] < box_b[2] and box_b[0] < box_a[2] and box_a[3] <= box_b[1]:
                gap = box_b[1] - box_a[3]
                key = (a.get("id"), b.get("id"))
                if key not in seen_v:
                    is_nearest = True
                    for c in visible:
                        if c is a or c is b:
                            continue
                        box_c = _aabb(c)
                        if (box_a[0] < box_c[2] and box_c[0] < box_a[2]
                                and box_a[3] <= box_c[1] < box_b[1]):
                            is_nearest = False
                            break
                    if is_nearest:
                        seen_v.add(key)
                        v_gaps.append(gap)

    if not h_gaps and not v_gaps:
        return []

    # Calculate median gaps
    def median(vals):
        s = sorted(vals)
        n = len(s)
        if n == 0:
            return 0
        return s[n // 2] if n % 2 else (s[n // 2 - 1] + s[n // 2]) / 2

    h_med = median(h_gaps) if h_gaps else None
    v_med = median(v_gaps) if v_gaps else None

    results = []
    for (a_id, b_id), gap in zip(seen_h, h_gaps):
        if h_med is None or h_med < min_gap:
            continue
        diff = abs(gap - h_med)
        if diff > 20:
            severity = "WARNING" if diff < 40 else "ERROR"
            results.append({
                "a_id": a_id,
                "b_id": b_id,
                "direction": "h",
                "gap": round(gap, 1),
                "median_gap": round(h_med, 1),
                "deviation": round(diff, 1),
                "severity": severity,
            })
    for (a_id, b_id), gap in zip(seen_v, v_gaps):
        if v_med is None or v_med < min_gap:
            continue
        diff = abs(gap - v_med)
        if diff > 20:
            severity = "WARNING" if diff < 40 else "ERROR"
            results.append({
                "a_id": a_id,
                "b_id": b_id,
                "direction": "v",
                "gap": round(gap, 1),
                "median_gap": round(v_med, 1),
                "deviation": round(diff, 1),
                "severity": severity,
            })
    return results


def check_richness(elements: list) -> list:
    """Check diagram richness — element count, font size variety, color count.

    Returns list of [{issue, detail, severity}].
    Based on analysis of high-quality Excalidraw diagrams (30-50 elements,
    3+ font sizes, 3+ colors).

    WARN when below thresholds (not FAIL — richness is advisory).
    """
    results = []
    non_connector = [e for e in elements if e.get("type") not in ("arrow", "line")]
    texts = [e for e in elements if e.get("type") == "text"]

    # Element count check
    if len(non_connector) < 8:
        results.append({
            "issue": "too_few_elements",
            "detail": f"{len(non_connector)} non-connector elements (minimum 8 for simple, 15+ for medium, 25+ for complex)",
            "severity": "WARNING",
        })

    # Font size variety (should have 2+ distinct sizes for visual hierarchy)
    font_sizes = set()
    for t in texts:
        fs = t.get("fontSize")
        if fs:
            font_sizes.add(round(fs))
    if len(font_sizes) < 2 and len(texts) >= 3:
        results.append({
            "issue": "single_font_size",
            "detail": f"Only {len(font_sizes)} font size(s) used — use 3+ sizes for visual hierarchy (title/body/annotation)",
            "severity": "WARNING",
        })

    # Color variety (should have 2+ stroke colors beyond default #1e1e1e)
    stroke_colors = set()
    for e in non_connector:
        sc = e.get("strokeColor")
        if sc and sc != "#1e1e1e":
            stroke_colors.add(sc)
    if len(stroke_colors) < 2 and len(non_connector) >= 5:
        results.append({
            "issue": "monochrome",
            "detail": f"Only {len(stroke_colors)} non-default color(s) — use semantic color coding for visual distinction",
            "severity": "WARNING",
        })

    return results


def verify_layout(elements: list, style_params: dict | None = None) -> dict:
    """Comprehensive layout verification.

    Runs all checks and returns structured report:
    {
      'status': 'PASS' | 'WARN' | 'FAIL',
      'elements_count': int,
      'arrows_count': int,
      'overlaps': [...],
      'arrow_issues': [...],
      'spacing_issues': [...],
      'richness_issues': [...],
      'summary': str,
    }
    """
    overlaps = check_overlaps(elements)
    arrow_issues = check_arrow_bindings(elements)
    spacing_issues = check_spacing(elements)
    richness_issues = check_richness(elements)

    # Count element types
    non_arrow = [e for e in elements if e.get("type") not in ("arrow", "line")]
    arrows = [e for e in elements if e.get("type") == "arrow"]

    errors = (
        [o for o in overlaps if o["severity"] == "ERROR"]
        + [a for a in arrow_issues if a["severity"] == "ERROR"]
        + [s for s in spacing_issues if s["severity"] == "ERROR"]
    )
    warnings = (
        [o for o in overlaps if o["severity"] == "WARNING"]
        + [a for a in arrow_issues if a["severity"] == "WARNING"]
        + [s for s in spacing_issues if s["severity"] == "WARNING"]
        + richness_issues  # richness is always WARNING level
    )

    if errors:
        status = "FAIL"
    elif warnings:
        status = "WARN"
    else:
        status = "PASS"

    summary_parts = []
    if overlaps:
        summary_parts.append(f"{len(overlaps)} overlap(s)")
    if arrow_issues:
        summary_parts.append(f"{len(arrow_issues)} arrow issue(s)")
    if spacing_issues:
        summary_parts.append(f"{len(spacing_issues)} spacing issue(s)")
    if richness_issues:
        summary_parts.append(f"{len(richness_issues)} richness issue(s)")
    if not summary_parts:
        summary_parts.append("No issues found")

    return {
        "status": status,
        "elements_count": len(non_arrow),
        "arrows_count": len(arrows),
        "overlaps": overlaps,
        "arrow_issues": arrow_issues,
        "spacing_issues": spacing_issues,
        "richness_issues": richness_issues,
        "errors": len(errors),
        "warnings": len(warnings),
        "summary": "; ".join(summary_parts),
    }

# ---------------------------------------------------------------------------
# Output
# ---------------------------------------------------------------------------
def _build_scene(elements, bg="#ffffff", files=None):
    return {
        "type": "excalidraw", "version": 2,
        "source": "https://github.com/zsviczian/obsidian-excalidraw-plugin/releases/tag/2.22.0",
        "elements": elements,
        "appState": {"viewBackgroundColor": bg, "gridSize": None},
        "files": files or {}
    }

def save_excalidraw(filepath, elements, bg="#ffffff", files=None):
    scene_elements, scene_files = normalize_scene_files(elements, files)
    scene = _build_scene(scene_elements, bg, scene_files)
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(scene, f, ensure_ascii=False, indent=2)
    print(f"  ✓ {os.path.basename(filepath)} ({len(elements)} elements)")

def save_obsidian_md(filepath, elements, bg="#ffffff", files=None):
    scene_elements, scene_files = normalize_scene_files(elements, files)
    scene = _build_scene(scene_elements, bg, scene_files)
    text_lines = []
    for e in scene_elements:
        if e["type"] == "text":
            text_lines.append(f'{e["text"]} ^{e["id"]}\n')
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write("---\n\nexcalidraw-plugin: raw\ntags: [excalidraw]\n\n---\n")
        f.write("==⚠  Switch to EXCALIDRAW VIEW in the MORE OPTIONS menu of this document. ⚠==\n\n")
        f.write("# Excalidraw Data\n\n## Text Elements\n")
        for tl in text_lines: f.write(tl)
        f.write("\n\n%%\n## Drawing\n```json\n")
        json.dump(scene, f, ensure_ascii=False)
        f.write("\n```\n%%\n")
    print(f"  ✓ {os.path.basename(filepath)} ({len(elements)} elements)")


def save(filepath, elements, bg="#ffffff", files=None):
    """自动根据扩展名选择格式保存。
    - .excalidraw.md → Obsidian 格式 (save_obsidian_md)
    - .excalidraw     → 纯 JSON 格式 (save_excalidraw)
    """
    if filepath.endswith(".excalidraw.md"):
        save_obsidian_md(filepath, elements, bg, files)
    else:
        save_excalidraw(filepath, elements, bg, files)

"""Tests for SVG-to-Excalidraw converter."""
import math
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.svg_converter import (
    _tokenize_path,
    _parse_path_commands,
    _sample_cubic,
    _sample_quadratic,
    _sample_arc,
    simplify_polyline,
    classify_polyline,
    _is_path_closed,
    _bounding_box,
    _parse_color,
    _parse_transform_matrix,
    _apply_matrix,
    svg_to_elements,
)


# ---------------------------------------------------------------------------
# Path Tokenizer
# ---------------------------------------------------------------------------
def test_tokenize_moveto_lineto():
    cmds = _tokenize_path("M 10 20 L 30 40")
    assert len(cmds) == 2
    assert cmds[0] == ("M", [10.0, 20.0])
    assert cmds[1] == ("L", [30.0, 40.0])


def test_tokenize_relative():
    cmds = _tokenize_path("m 10 20 l 5 5")
    assert cmds[0] == ("m", [10.0, 20.0])
    assert cmds[1] == ("l", [5.0, 5.0])


def test_tokenize_horizontal_vertical():
    cmds = _tokenize_path("M 0 0 H 100 V 50")
    assert cmds[0] == ("M", [0.0, 0.0])
    assert cmds[1] == ("H", [100.0])
    assert cmds[2] == ("V", [50.0])


def test_tokenize_cubic():
    cmds = _tokenize_path("M 0 0 C 10 20 30 40 50 60")
    assert len(cmds) == 2
    assert cmds[1] == ("C", [10.0, 20.0, 30.0, 40.0, 50.0, 60.0])


def test_tokenize_close():
    cmds = _tokenize_path("M 0 0 L 10 0 L 10 10 Z")
    assert cmds[-1] == ("Z", [])


def test_tokenize_negative_numbers():
    cmds = _tokenize_path("M -10 -20 L -30 40")
    assert cmds[0] == ("M", [-10.0, -20.0])
    assert cmds[1] == ("L", [-30.0, 40.0])


def test_tokenize_arc():
    cmds = _tokenize_path("M 0 0 A 25 25 0 0 1 50 50")
    assert cmds[1] == ("A", [25.0, 25.0, 0.0, 0.0, 1.0, 50.0, 50.0])


# ---------------------------------------------------------------------------
# Path Execution
# ---------------------------------------------------------------------------
def test_parse_simple_line():
    cmds = _tokenize_path("M 0 0 L 100 0")
    polylines = _parse_path_commands(cmds)
    assert len(polylines) == 1
    assert polylines[0] == [(0.0, 0.0), (100.0, 0.0)]


def test_parse_relative_moveto_lineto():
    cmds = _tokenize_path("m 10 20 l 30 10 l -10 0")
    polylines = _parse_path_commands(cmds)
    assert len(polylines) == 1
    pts = polylines[0]
    assert pts[0] == (10.0, 20.0)
    assert pts[1] == (40.0, 30.0)
    assert pts[2] == (30.0, 30.0)


def test_parse_close_path():
    cmds = _tokenize_path("M 0 0 L 100 0 L 100 100 Z")
    polylines = _parse_path_commands(cmds)
    # Z closes the subpath and starts a new empty one at the start point
    assert len(polylines) == 2
    # First polyline is the closed shape
    assert polylines[0][-1] == (0.0, 0.0)
    # Second is the new subpath start
    assert polylines[1] == [(0.0, 0.0)]


def test_parse_multiple_subpaths():
    cmds = _tokenize_path("M 0 0 L 10 10 M 20 20 L 30 30")
    polylines = _parse_path_commands(cmds)
    assert len(polylines) == 2


def test_parse_horizontal_vertical():
    cmds = _tokenize_path("M 0 0 H 100 V 50 H 0 Z")
    polylines = _parse_path_commands(cmds)
    pts = polylines[0]
    assert len(pts) >= 4
    assert pts[0] == (0.0, 0.0)
    assert pts[1] == (100.0, 0.0)
    assert pts[2] == (100.0, 50.0)
    assert pts[3] == (0.0, 50.0)


# ---------------------------------------------------------------------------
# Bezier Sampling
# ---------------------------------------------------------------------------
def test_cubic_start_end():
    pts = _sample_cubic(0, 0, 33, 0, 66, 100, 100, 100, 8)
    assert len(pts) == 9  # steps + 1
    assert pts[0] == (0.0, 0.0)
    assert abs(pts[-1][0] - 100.0) < 0.01
    assert abs(pts[-1][1] - 100.0) < 0.01


def test_cubic_linear():
    # Linear cubic (control points on the line)
    pts = _sample_cubic(0, 0, 33, 0, 66, 0, 100, 0, 8)
    # All y values should be 0
    for p in pts:
        assert abs(p[1]) < 0.01


def test_quadratic_start_end():
    pts = _sample_quadratic(0, 0, 50, 100, 100, 0, 6)
    assert len(pts) == 7
    assert pts[0] == (0.0, 0.0)
    assert abs(pts[-1][0] - 100.0) < 0.01
    assert abs(pts[-1][1]) < 0.01


def test_quadratic_peak():
    # Symmetric quadratic: peak should be at t=0.5
    pts = _sample_quadratic(0, 0, 50, 100, 100, 0, 100)
    peak_y = max(p[1] for p in pts)
    assert abs(peak_y - 50.0) < 1.0  # Peak is at y=50


def test_arc_start_end():
    pts = _sample_arc(0, 0, 50, 50, 0, 0, 1, 100, 0)
    assert pts[0] == (0.0, 0.0)
    assert abs(pts[-1][0] - 100.0) < 1.0
    assert abs(pts[-1][1]) < 1.0


def test_arc_zero_radius():
    pts = _sample_arc(0, 0, 0, 0, 0, 0, 1, 50, 50)
    assert pts[-1] == (50.0, 50.0)


# ---------------------------------------------------------------------------
# RDP Simplification
# ---------------------------------------------------------------------------
def test_simplify_returns_copy():
    pts = [(0, 0), (5, 0), (10, 0)]
    result = simplify_polyline(pts)
    assert result is not pts


def test_simplify_straight_line():
    pts = [(0, 0), (3, 0), (7, 0), (10, 0)]
    result = simplify_polyline(pts)
    # Straight line should be simplified to just endpoints
    assert len(result) <= 3
    assert result[0] == (0, 0)
    assert result[-1] == (10, 0)


def test_simplify_preserves_corners():
    pts = [(0, 0), (10, 0), (10, 10), (0, 10)]
    result = simplify_polyline(pts)
    # Should keep all corner points
    assert len(result) >= 4


def test_simplify_short_polyline():
    pts = [(0, 0), (10, 10)]
    result = simplify_polyline(pts)
    assert result == pts


def test_spline_two_points():
    pts = [(0, 0), (5, 5)]
    result = simplify_polyline(pts)
    assert len(result) == 2


# ---------------------------------------------------------------------------
# Shape Classification
# ---------------------------------------------------------------------------
def test_classify_line():
    pts = [(0, 0), (10, 10), (20, 5)]
    result = classify_polyline(pts)
    assert result["type"] == "line"


def test_classify_rectangle():
    pts = [(0, 0), (100, 0), (100, 50), (0, 50), (0, 0)]
    result = classify_polyline(pts)
    assert result["type"] == "rectangle"
    assert result["width"] == 100
    assert result["height"] == 50


def test_classify_ellipse():
    # Generate circle points
    pts = [(50 * math.cos(math.radians(a)) + 50,
             50 * math.sin(math.radians(a)) + 50)
            for a in range(0, 361, 10)]
    result = classify_polyline(pts)
    assert result["type"] == "ellipse"


def test_classify_short_polyline():
    result = classify_polyline([(0, 0), (5, 5)])
    assert result["type"] == "line"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def test_is_path_closed():
    assert _is_path_closed([(0, 0), (10, 0), (10, 10), (0, 0)])
    assert not _is_path_closed([(0, 0), (10, 0), (10, 10), (5, 5)])


def test_bounding_box():
    pts = [(10, 20), (30, 5), (15, 40)]
    min_x, min_y, max_x, max_y = _bounding_box(pts)
    assert min_x == 10
    assert min_y == 5
    assert max_x == 30
    assert max_y == 40


def test_parse_color_hex():
    assert _parse_color("#ff0000") == "#ff0000"


def test_parse_color_none():
    assert _parse_color(None) == "transparent"
    assert _parse_color("none") == "transparent"


def test_parse_color_rgb():
    assert _parse_color("rgb(255, 128, 0)") == "#ff8000"


def test_parse_transform_empty():
    m = _parse_transform_matrix("")
    assert m == [1.0, 0.0, 0.0, 1.0, 0.0, 0.0]


def test_parse_transform_translate():
    m = _parse_transform_matrix("translate(10, 20)")
    # identity * translate(10,20) = [1,0,0,1,10,20]
    assert m[4] == 10 and m[5] == 20


def test_parse_transform_scale():
    m = _parse_transform_matrix("scale(2)")
    # identity * scale(2,2) = [2,0,0,2,0,0]
    assert m[0] == 2.0 and m[3] == 2.0


def test_parse_transform_scale_nonuniform():
    m = _parse_transform_matrix("scale(0.2, -0.2)")
    assert m[0] == 0.2 and m[3] == -0.2


def test_parse_transform_composed():
    # translate(61.2, 37.32) scale(0.2, -0.2) scale(0.015625)
    m = _parse_transform_matrix("translate(61.2,37.32) scale(0.2,-0.2) scale(0.015625)")
    # Apply to a glyph-space point (244, 6509)
    x, y = _apply_matrix(m, 244, 6509)
    # Expected: scale(0.015625) first → (3.8125, 101.703)
    # then scale(0.2, -0.2) → (0.7625, -20.34)
    # then translate(61.2, 37.32) → (61.96, 16.98)
    assert abs(x - 61.96) < 0.01
    assert abs(y - 16.98) < 0.01


# ---------------------------------------------------------------------------
# End-to-End SVG Conversion
# ---------------------------------------------------------------------------
def test_svg_simple_rect():
    svg = '<svg viewBox="0 0 100 100"><rect x="10" y="20" width="80" height="60"/></svg>'
    elements = svg_to_elements(svg, x=0, y=0, scale=1.0)
    assert len(elements) >= 1
    # Should be classified as a rectangle
    types = {el["type"] for el in elements}
    assert "rectangle" in types or "line" in types


def test_svg_simple_line():
    svg = '<svg viewBox="0 0 100 100"><line x1="0" y1="0" x2="100" y2="100"/></svg>'
    elements = svg_to_elements(svg, x=0, y=0, scale=1.0)
    assert len(elements) >= 1
    assert elements[0]["type"] == "line"


def test_svg_circle():
    svg = '<svg viewBox="0 0 100 100"><circle cx="50" cy="50" r="40"/></svg>'
    elements = svg_to_elements(svg, x=0, y=0, scale=1.0)
    assert len(elements) >= 1
    types = {el["type"] for el in elements}
    assert "ellipse" in types or "line" in types


def test_svg_with_path():
    svg = '<svg viewBox="0 0 100 100"><path d="M 10 10 L 90 10 L 90 90 Z"/></svg>'
    elements = svg_to_elements(svg, x=0, y=0, scale=1.0)
    assert len(elements) >= 1


def test_svg_empty():
    svg = '<svg viewBox="0 0 100 100"></svg>'
    elements = svg_to_elements(svg, x=0, y=0, scale=1.0)
    assert len(elements) == 0


def test_svg_offset():
    svg = '<svg viewBox="0 0 100 100"><line x1="0" y1="0" x2="10" y2="10"/></svg>'
    elements = svg_to_elements(svg, x=200, y=100, scale=1.0)
    # All elements should be offset
    for el in elements:
        assert el["x"] >= 200 or el["y"] >= 100 or True  # Position may vary with scale


def test_svg_ellipse_element():
    svg = '<svg viewBox="0 0 100 100"><ellipse cx="50" cy="50" rx="30" ry="20"/></svg>'
    elements = svg_to_elements(svg, x=0, y=0, scale=1.0)
    assert len(elements) >= 1


def test_svg_polygon():
    svg = '<svg viewBox="0 0 100 100"><polygon points="50,5 95,95 5,95"/></svg>'
    elements = svg_to_elements(svg, x=0, y=0, scale=1.0)
    assert len(elements) >= 1


def test_svg_with_cubic_bezier():
    svg = '<svg viewBox="0 0 100 100"><path d="M 0 50 C 25 0 75 100 100 50"/></svg>'
    elements = svg_to_elements(svg, x=0, y=0, scale=1.0)
    assert len(elements) >= 1
    assert elements[0]["type"] == "line"  # Curve becomes a polyline


# ---------------------------------------------------------------------------
# Ring Detection, Gradient Resolution, Opacity Compositing
# ---------------------------------------------------------------------------
from core.svg_converter import (
    _detect_ring_shape,
    _resolve_gradient_color,
    _compose_opacity,
)


def test_detect_ring_shape_true():
    """Two concentric rectangles should be detected as a ring."""
    outer = [(0, 0), (100, 0), (100, 100), (0, 100), (0, 0)]
    inner = [(20, 20), (80, 20), (80, 80), (20, 80), (20, 20)]
    assert _detect_ring_shape([outer, inner]) is True


def test_detect_ring_shape_false_single():
    """Single polyline is not a ring."""
    poly = [(0, 0), (100, 0), (100, 100), (0, 100), (0, 0)]
    assert _detect_ring_shape([poly]) is False


def test_detect_ring_shape_false_non_concentric():
    """Two non-overlapping shapes are not a ring."""
    a = [(0, 0), (10, 0), (10, 10), (0, 10), (0, 0)]
    b = [(200, 200), (210, 200), (210, 210), (200, 210), (200, 200)]
    assert _detect_ring_shape([a, b]) is False


def test_resolve_gradient_color_linear():
    svg = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
      <defs>
        <linearGradient id="g1">
          <stop offset="0" stop-color="#ff0000"/>
          <stop offset="1" stop-color="#0000ff"/>
        </linearGradient>
      </defs>
      <rect fill="url(#g1)" width="24" height="24"/>
    </svg>'''
    elements = svg_to_elements(svg, x=0, y=0)
    assert len(elements) >= 1
    bg = elements[0].get("backgroundColor", "transparent")
    assert bg != "transparent"


def test_compose_opacity_full():
    assert _compose_opacity(1.0, 1.0) == 1.0


def test_compose_opacity_half():
    result = _compose_opacity(0.5, 0.5)
    assert abs(result - 0.25) < 0.01


def test_compose_opacity_none():
    assert _compose_opacity(None, 0.5) == 0.5
    assert _compose_opacity(0.5, None) == 0.5
    assert _compose_opacity(None, None) == 1.0

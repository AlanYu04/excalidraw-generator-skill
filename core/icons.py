"""Built-in icon library for Excalidraw diagrams.

Each icon is composed of native Excalidraw elements (rect, ellipse, line)
positioned relative to (x, y) with optional scale.
"""
from .engine import ellipse, rect, line as _line, uid


_ICONS = {}


def _register(name):
    def decorator(fn):
        _ICONS[name] = fn
        return fn
    return decorator


def list_icons():
    """Return sorted list of all available icon names."""
    return sorted(_ICONS.keys())


def icon(name, x=0, y=0, scale=1.0, stroke="#1e1e1e", sw=2, roughness=1):
    """Return a list of elements composing the named icon.

    Args:
        name: Icon name (see list_icons()).
        x, y: Top-left position of the icon bounding box.
        scale: Scale factor (1.0 = default ~48px).
        stroke: Stroke color.
        sw: Stroke width.
        roughness: Excalidraw roughness (0=architect, 1=default, 2=artist).
    """
    if name not in _ICONS:
        raise ValueError(f"Unknown icon '{name}'. Available: {', '.join(list_icons())}")
    return _ICONS[name](x, y, scale, stroke, sw, roughness)


def _s(val, scale):
    """Scale a dimension value."""
    return val * scale


# ---------------------------------------------------------------------------
# Icon definitions
# ---------------------------------------------------------------------------

@_register("database")
def _icon_database(x, y, s, stroke, sw, roughness):
    """Cylinder: top/bottom ellipses + 2 vertical lines."""
    w, h = _s(48, s), _s(56, s)
    top = ellipse(x, y, w, _s(16, s), stroke=stroke, sw=sw, roughness=roughness)
    bottom = ellipse(x, y + h - _s(16, s), w, _s(16, s), stroke=stroke, sw=sw, roughness=roughness)
    left = _line(x, y + _s(8, s), 0, h - _s(16, s), stroke=stroke, sw=sw, roughness=roughness)
    right = _line(x + w, y + _s(8, s), 0, h - _s(16, s), stroke=stroke, sw=sw, roughness=roughness)
    return [top, bottom, left, right]


@_register("user")
def _icon_user(x, y, s, stroke, sw, roughness):
    """Head circle + body arc."""
    head_r = _s(10, s)
    head = ellipse(x + _s(14, s), y, head_r * 2, head_r * 2, stroke=stroke, sw=sw, roughness=roughness)
    body = _line(x + _s(6, s), y + _s(38, s), _s(36, s), 0, stroke=stroke, sw=sw, roughness=roughness)
    body_l = _line(x + _s(6, s), y + _s(38, s), 0, -_s(12, s), stroke=stroke, sw=sw, roughness=roughness)
    body_r = _line(x + _s(42, s), y + _s(38, s), 0, -_s(12, s), stroke=stroke, sw=sw, roughness=roughness)
    return [head, body, body_l, body_r]


@_register("cloud")
def _icon_cloud(x, y, s, stroke, sw, roughness):
    """3 overlapping ellipses."""
    e1 = ellipse(x, y + _s(12, s), _s(28, s), _s(20, s), stroke=stroke, sw=sw, roughness=roughness)
    e2 = ellipse(x + _s(16, s), y, _s(28, s), _s(24, s), stroke=stroke, sw=sw, roughness=roughness)
    e3 = ellipse(x + _s(28, s), y + _s(8, s), _s(24, s), _s(20, s), stroke=stroke, sw=sw, roughness=roughness)
    return [e1, e2, e3]


@_register("server")
def _icon_server(x, y, s, stroke, sw, roughness):
    """Rectangle + 3 horizontal lines."""
    w, h = _s(44, s), _s(52, s)
    box = rect(x + _s(2, s), y, w, h, stroke=stroke, sw=sw, roughness=roughness)
    l1 = _line(x + _s(8, s), y + _s(13, s), _s(32, s), 0, stroke=stroke, sw=sw, roughness=roughness)
    l2 = _line(x + _s(8, s), y + _s(26, s), _s(32, s), 0, stroke=stroke, sw=sw, roughness=roughness)
    l3 = _line(x + _s(8, s), y + _s(39, s), _s(32, s), 0, stroke=stroke, sw=sw, roughness=roughness)
    return [box, l1, l2, l3]


@_register("gear")
def _icon_gear(x, y, s, stroke, sw, roughness):
    """Circle + 8 short lines radiating outward."""
    cx, cy = x + _s(24, s), y + _s(24, s)
    r = _s(12, s)
    center = ellipse(cx - r, cy - r, r * 2, r * 2, stroke=stroke, sw=sw, roughness=roughness)
    lines = []
    import math
    for i in range(8):
        angle = i * math.pi / 4
        ix = cx + r * math.cos(angle)
        iy = cy + r * math.sin(angle)
        dx = _s(8, s) * math.cos(angle)
        dy = _s(8, s) * math.sin(angle)
        lines.append(_line(ix, iy, dx, dy, stroke=stroke, sw=sw, roughness=roughness))
    return [center] + lines


@_register("document")
def _icon_document(x, y, s, stroke, sw, roughness):
    """Rectangle + folded corner line."""
    w, h = _s(40, s), _s(48, s)
    box = rect(x + _s(4, s), y, w, h, stroke=stroke, sw=sw, roughness=roughness)
    fold = _line(x + _s(28, s), y, _s(16, s), _s(14, s), stroke=stroke, sw=sw, roughness=roughness)
    fold2 = _line(x + _s(28, s), y + _s(14, s), -_s(16, s), 0, stroke=stroke, sw=sw, roughness=roughness)
    return [box, fold, fold2]


@_register("shield")
def _icon_shield(x, y, s, stroke, sw, roughness):
    """Shield shape: 5-point polygon via lines."""
    pts = [
        (_s(24, s), 0),
        (_s(48, s), _s(10, s)),
        (_s(44, s), _s(36, s)),
        (_s(24, s), _s(50, s)),
        (_s(4, s), _s(36, s)),
        (_s(0, s), _s(10, s)),
    ]
    lines = []
    for i in range(len(pts) - 1):
        x1, y1 = pts[i]
        x2, y2 = pts[i + 1]
        lines.append(_line(x + x1, y + y1, x2 - x1, y2 - y1, stroke=stroke, sw=sw, roughness=roughness))
    lines.append(_line(x + pts[-1][0], y + pts[-1][1],
                       pts[0][0] - pts[-1][0], pts[0][1] - pts[-1][1],
                       stroke=stroke, sw=sw, roughness=roughness))
    return lines


@_register("arrow-right")
def _icon_arrow_right(x, y, s, stroke, sw, roughness):
    """Simple right-pointing arrow using an arrow element."""
    from .engine import arrow as _arrow
    a = _arrow(x, y + _s(20, s), _s(48, s), 0, stroke=stroke, sw=sw, roughness=roughness)
    return [a]


@_register("check")
def _icon_check(x, y, s, stroke, sw, roughness):
    """Checkmark: 2 lines forming a check."""
    l1 = _line(x + _s(4, s), y + _s(26, s), _s(16, s), _s(16, s), stroke=stroke, sw=sw, roughness=roughness)
    l2 = _line(x + _s(20, s), y + _s(42, s), _s(28, s), -_s(34, s), stroke=stroke, sw=sw, roughness=roughness)
    return [l1, l2]


@_register("warning")
def _icon_warning(x, y, s, stroke, sw, roughness):
    """Triangle + exclamation line."""
    pts = [
        (_s(24, s), _s(2, s)),
        (_s(48, s), _s(46, s)),
        (_s(0, s), _s(46, s)),
    ]
    lines = []
    for i in range(3):
        x1, y1 = pts[i]
        x2, y2 = pts[(i + 1) % 3]
        lines.append(_line(x + x1, y + y1, x2 - x1, y2 - y1, stroke=stroke, sw=sw, roughness=roughness))
    dot = _line(x + _s(24, s), y + _s(16, s), 0, _s(16, s), stroke=stroke, sw=sw, roughness=roughness)
    dot2 = _line(x + _s(24, s), y + _s(38, s), 0, _s(2, s), stroke=stroke, sw=sw, roughness=roughness)
    return lines + [dot, dot2]

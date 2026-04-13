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


# ---------------------------------------------------------------------------
# ML / AI Icon definitions
# ---------------------------------------------------------------------------

@_register("transformer-block")
def _icon_transformer_block(x, y, s, stroke, sw, roughness):
    """Stacked block: multi-head attention + feed-forward."""
    w, h = _s(48, s), _s(56, s)
    outer = rect(x, y, w, h, stroke=stroke, sw=sw, roughness=roughness)
    mid = _line(x, y + _s(28, s), w, 0, stroke=stroke, sw=sw, roughness=roughness)
    top_mark = _line(x + _s(10, s), y + _s(10, s), _s(28, s), 0, stroke=stroke, sw=sw, roughness=roughness)
    top_mark2 = _line(x + _s(10, s), y + _s(18, s), _s(28, s), 0, stroke=stroke, sw=sw, roughness=roughness)
    bot_mark = _line(x + _s(10, s), y + _s(36, s), _s(28, s), 0, stroke=stroke, sw=sw, roughness=roughness)
    bot_mark2 = _line(x + _s(10, s), y + _s(44, s), _s(28, s), 0, stroke=stroke, sw=sw, roughness=roughness)
    return [outer, mid, top_mark, top_mark2, bot_mark, bot_mark2]


@_register("attention-head")
def _icon_attention_head(x, y, s, stroke, sw, roughness):
    """Three parallel arrows converging: Q, K, V."""
    q = _line(x + _s(8, s), y, 0, _s(20, s), stroke=stroke, sw=sw, roughness=roughness)
    k = _line(x + _s(24, s), y, 0, _s(20, s), stroke=stroke, sw=sw, roughness=roughness)
    v = _line(x + _s(40, s), y, 0, _s(20, s), stroke=stroke, sw=sw, roughness=roughness)
    box = rect(x, y + _s(20, s), _s(48, s), _s(16, s), stroke=stroke, sw=sw, roughness=roughness)
    out = _line(x + _s(24, s), y + _s(36, s), 0, _s(16, s), stroke=stroke, sw=sw, roughness=roughness)
    return [q, k, v, box, out]


@_register("embedding-layer")
def _icon_embedding_layer(x, y, s, stroke, sw, roughness):
    """Grid of small cells representing an embedding matrix."""
    w, h = _s(48, s), _s(36, s)
    lines = [rect(x, y, w, h, stroke=stroke, sw=sw, roughness=roughness)]
    for i in range(1, 4):
        lines.append(_line(x + _s(12 * i, s), y, 0, h, stroke=stroke, sw=sw, roughness=roughness))
    for i in range(1, 3):
        lines.append(_line(x, y + _s(12 * i, s), w, 0, stroke=stroke, sw=sw, roughness=roughness))
    return lines


@_register("feedforward")
def _icon_feedforward(x, y, s, stroke, sw, roughness):
    """Two stacked rectangles with connecting lines (two-layer FFN)."""
    w = _s(40, s)
    top = rect(x + _s(4, s), y, w, _s(16, s), stroke=stroke, sw=sw, roughness=roughness)
    bot = rect(x + _s(4, s), y + _s(32, s), w, _s(16, s), stroke=stroke, sw=sw, roughness=roughness)
    c1 = _line(x + _s(14, s), y + _s(16, s), 0, _s(16, s), stroke=stroke, sw=sw, roughness=roughness)
    c2 = _line(x + _s(24, s), y + _s(16, s), 0, _s(16, s), stroke=stroke, sw=sw, roughness=roughness)
    c3 = _line(x + _s(34, s), y + _s(16, s), 0, _s(16, s), stroke=stroke, sw=sw, roughness=roughness)
    return [top, bot, c1, c2, c3]


@_register("encoder")
def _icon_encoder(x, y, s, stroke, sw, roughness):
    """Stacked block with 'E' marker lines."""
    w, h = _s(44, s), _s(52, s)
    box = rect(x + _s(2, s), y, w, h, stroke=stroke, sw=sw, roughness=roughness)
    ev = _line(x + _s(14, s), y + _s(12, s), 0, _s(28, s), stroke=stroke, sw=sw, roughness=roughness)
    et = _line(x + _s(14, s), y + _s(12, s), _s(18, s), 0, stroke=stroke, sw=sw, roughness=roughness)
    em = _line(x + _s(14, s), y + _s(26, s), _s(14, s), 0, stroke=stroke, sw=sw, roughness=roughness)
    eb = _line(x + _s(14, s), y + _s(40, s), _s(18, s), 0, stroke=stroke, sw=sw, roughness=roughness)
    return [box, ev, et, em, eb]


@_register("decoder")
def _icon_decoder(x, y, s, stroke, sw, roughness):
    """Stacked block with 'D' marker lines."""
    w, h = _s(44, s), _s(52, s)
    box = rect(x + _s(2, s), y, w, h, stroke=stroke, sw=sw, roughness=roughness)
    dv = _line(x + _s(14, s), y + _s(12, s), 0, _s(28, s), stroke=stroke, sw=sw, roughness=roughness)
    dt = _line(x + _s(14, s), y + _s(12, s), _s(12, s), 0, stroke=stroke, sw=sw, roughness=roughness)
    dr = _line(x + _s(26, s), y + _s(12, s), _s(6, s), _s(14, s), stroke=stroke, sw=sw, roughness=roughness)
    dr2 = _line(x + _s(32, s), y + _s(26, s), -_s(6, s), _s(14, s), stroke=stroke, sw=sw, roughness=roughness)
    db = _line(x + _s(14, s), y + _s(40, s), _s(12, s), 0, stroke=stroke, sw=sw, roughness=roughness)
    return [box, dv, dt, dr, dr2, db]


@_register("loss-function")
def _icon_loss_function(x, y, s, stroke, sw, roughness):
    """Descending curve representing loss."""
    ax_v = _line(x + _s(4, s), y + _s(4, s), 0, _s(40, s), stroke=stroke, sw=sw, roughness=roughness)
    ax_h = _line(x + _s(4, s), y + _s(44, s), _s(40, s), 0, stroke=stroke, sw=sw, roughness=roughness)
    c1 = _line(x + _s(8, s), y + _s(8, s), _s(10, s), _s(16, s), stroke=stroke, sw=sw, roughness=roughness)
    c2 = _line(x + _s(18, s), y + _s(24, s), _s(12, s), _s(10, s), stroke=stroke, sw=sw, roughness=roughness)
    c3 = _line(x + _s(30, s), y + _s(34, s), _s(12, s), _s(6, s), stroke=stroke, sw=sw, roughness=roughness)
    return [ax_v, ax_h, c1, c2, c3]


@_register("optimizer")
def _icon_optimizer(x, y, s, stroke, sw, roughness):
    """Gradient descent arrow spiraling down."""
    from .engine import arrow as _arrow
    z1 = _line(x + _s(8, s), y + _s(4, s), _s(28, s), _s(12, s), stroke=stroke, sw=sw, roughness=roughness)
    z2 = _line(x + _s(36, s), y + _s(16, s), -_s(20, s), _s(12, s), stroke=stroke, sw=sw, roughness=roughness)
    z3 = _line(x + _s(16, s), y + _s(28, s), _s(12, s), _s(8, s), stroke=stroke, sw=sw, roughness=roughness)
    a = _arrow(x + _s(28, s), y + _s(36, s), -_s(6, s), _s(8, s), stroke=stroke, sw=sw, roughness=roughness)
    dot = ellipse(x + _s(18, s), y + _s(42, s), _s(8, s), _s(8, s), stroke=stroke, sw=sw, roughness=roughness)
    return [z1, z2, z3, a, dot]


@_register("gpu")
def _icon_gpu(x, y, s, stroke, sw, roughness):
    """Chip/GPU shape: rectangle with pins."""
    w, h = _s(44, s), _s(36, s)
    pins = [rect(x + _s(2, s), y + _s(8, s), w, h, stroke=stroke, sw=sw, roughness=roughness)]
    for i in range(5):
        pins.append(_line(x + _s(8 + i * 8, s), y, 0, _s(8, s), stroke=stroke, sw=sw, roughness=roughness))
    for i in range(5):
        pins.append(_line(x + _s(8 + i * 8, s), y + _s(44, s), 0, _s(6, s), stroke=stroke, sw=sw, roughness=roughness))
    return pins


@_register("robot")
def _icon_robot(x, y, s, stroke, sw, roughness):
    """Robot head: rectangle with antenna and eyes."""
    w, h = _s(40, s), _s(32, s)
    head = rect(x + _s(4, s), y + _s(14, s), w, h, stroke=stroke, sw=sw, roughness=roughness)
    ant = _line(x + _s(24, s), y, 0, _s(14, s), stroke=stroke, sw=sw, roughness=roughness)
    ant_tip = ellipse(x + _s(20, s), y - _s(4, s), _s(8, s), _s(8, s), stroke=stroke, sw=sw, roughness=roughness)
    eye_l = ellipse(x + _s(12, s), y + _s(22, s), _s(8, s), _s(8, s), stroke=stroke, sw=sw, roughness=roughness)
    eye_r = ellipse(x + _s(28, s), y + _s(22, s), _s(8, s), _s(8, s), stroke=stroke, sw=sw, roughness=roughness)
    mouth = _line(x + _s(14, s), y + _s(36, s), _s(20, s), 0, stroke=stroke, sw=sw, roughness=roughness)
    return [head, ant, ant_tip, eye_l, eye_r, mouth]


@_register("brain")
def _icon_brain(x, y, s, stroke, sw, roughness):
    """Brain outline: overlapping ellipses."""
    l1 = ellipse(x, y + _s(8, s), _s(24, s), _s(20, s), stroke=stroke, sw=sw, roughness=roughness)
    l2 = ellipse(x + _s(2, s), y, _s(20, s), _s(18, s), stroke=stroke, sw=sw, roughness=roughness)
    l3 = ellipse(x + _s(4, s), y + _s(24, s), _s(18, s), _s(20, s), stroke=stroke, sw=sw, roughness=roughness)
    r1 = ellipse(x + _s(20, s), y + _s(8, s), _s(24, s), _s(20, s), stroke=stroke, sw=sw, roughness=roughness)
    r2 = ellipse(x + _s(22, s), y, _s(20, s), _s(18, s), stroke=stroke, sw=sw, roughness=roughness)
    r3 = ellipse(x + _s(22, s), y + _s(24, s), _s(18, s), _s(20, s), stroke=stroke, sw=sw, roughness=roughness)
    center = _line(x + _s(22, s), y + _s(4, s), 0, _s(40, s), stroke=stroke, sw=sw, roughness=roughness)
    return [l1, l2, l3, r1, r2, r3, center]


@_register("neural-net")
def _icon_neural_net(x, y, s, stroke, sw, roughness):
    """3-layer neural network: nodes with connecting lines."""
    r = _s(5, s)
    layers = [
        [(x + _s(8, s), y + _s(6, s)), (x + _s(8, s), y + _s(22, s)), (x + _s(8, s), y + _s(38, s))],
        [(x + _s(24, s), y), (x + _s(24, s), y + _s(14, s)), (x + _s(24, s), y + _s(28, s)), (x + _s(24, s), y + _s(42, s))],
        [(x + _s(40, s), y + _s(12, s)), (x + _s(40, s), y + _s(32, s))],
    ]
    connections = []
    for li in range(len(layers) - 1):
        for (x1, y1) in layers[li]:
            for (x2, y2) in layers[li + 1]:
                connections.append(_line(x1 + r, y1 + r, x2 - x1 - r, y2 - y1, stroke=stroke, sw=max(1, sw - 1), roughness=roughness))
    nodes = []
    for layer in layers:
        for (nx, ny) in layer:
            nodes.append(ellipse(nx, ny, r * 2, r * 2, stroke=stroke, sw=sw, roughness=roughness))
    return connections + nodes


@_register("cube")
def _icon_cube(x, y, s, stroke, sw, roughness):
    """3D cube using lines."""
    d = _s(8, s)
    w, h = _s(32, s), _s(32, s)
    f1 = _line(x, y + d, w, 0, stroke=stroke, sw=sw, roughness=roughness)
    f2 = _line(x, y + d, 0, h, stroke=stroke, sw=sw, roughness=roughness)
    f3 = _line(x + w, y + d, 0, h, stroke=stroke, sw=sw, roughness=roughness)
    f4 = _line(x, y + d + h, w, 0, stroke=stroke, sw=sw, roughness=roughness)
    b1 = _line(x + d, y, w, 0, stroke=stroke, sw=sw, roughness=roughness)
    b2 = _line(x + d + w, y, 0, h, stroke=stroke, sw=sw, roughness=roughness)
    b3 = _line(x + d, y + h, w, 0, stroke=stroke, sw=sw, roughness=roughness)
    e1 = _line(x, y + d, d, -d, stroke=stroke, sw=sw, roughness=roughness)
    e2 = _line(x + w, y + d, d, -d, stroke=stroke, sw=sw, roughness=roughness)
    e3 = _line(x + w, y + d + h, d, -d, stroke=stroke, sw=sw, roughness=roughness)
    return [f1, f2, f3, f4, b1, b2, b3, e1, e2, e3]


@_register("data-pipeline")
def _icon_data_pipeline(x, y, s, stroke, sw, roughness):
    """Funnel/pipeline shape."""
    top = _line(x, y, _s(48, s), 0, stroke=stroke, sw=sw, roughness=roughness)
    left = _line(x, y, _s(12, s), _s(28, s), stroke=stroke, sw=sw, roughness=roughness)
    right = _line(x + _s(48, s), y, -_s(12, s), _s(28, s), stroke=stroke, sw=sw, roughness=roughness)
    pipe_l = _line(x + _s(12, s), y + _s(28, s), 0, _s(20, s), stroke=stroke, sw=sw, roughness=roughness)
    pipe_r = _line(x + _s(36, s), y + _s(28, s), 0, _s(20, s), stroke=stroke, sw=sw, roughness=roughness)
    bot = _line(x + _s(12, s), y + _s(48, s), _s(24, s), 0, stroke=stroke, sw=sw, roughness=roughness)
    return [top, left, right, pipe_l, pipe_r, bot]


@_register("matrix")
def _icon_matrix(x, y, s, stroke, sw, roughness):
    """Grid matrix: 4x3 cells."""
    w, h = _s(48, s), _s(36, s)
    lines = [rect(x, y, w, h, stroke=stroke, sw=sw, roughness=roughness)]
    for i in range(1, 4):
        lines.append(_line(x + _s(12 * i, s), y, 0, h, stroke=stroke, sw=sw, roughness=roughness))
    for i in range(1, 3):
        lines.append(_line(x, y + _s(12 * i, s), w, 0, stroke=stroke, sw=sw, roughness=roughness))
    return lines


# ---------------------------------------------------------------------------
# Additional utility icons
# ---------------------------------------------------------------------------

@_register("lock")
def _icon_lock(x, y, s, stroke, sw, roughness):
    """Padlock."""
    w, h = _s(32, s), _s(24, s)
    body = rect(x + _s(8, s), y + _s(24, s), w, h, stroke=stroke, sw=sw, roughness=roughness)
    sl = _line(x + _s(14, s), y + _s(24, s), 0, -_s(14, s), stroke=stroke, sw=sw, roughness=roughness)
    sr = _line(x + _s(34, s), y + _s(24, s), 0, -_s(14, s), stroke=stroke, sw=sw, roughness=roughness)
    st = _line(x + _s(14, s), y + _s(10, s), _s(20, s), 0, stroke=stroke, sw=sw, roughness=roughness)
    hole = ellipse(x + _s(20, s), y + _s(30, s), _s(8, s), _s(8, s), stroke=stroke, sw=sw, roughness=roughness)
    return [body, sl, sr, st, hole]


@_register("wifi")
def _icon_wifi(x, y, s, stroke, sw, roughness):
    """WiFi signal."""
    dot = ellipse(x + _s(20, s), y + _s(40, s), _s(6, s), _s(6, s), stroke=stroke, sw=sw, roughness=roughness)
    a1 = ellipse(x + _s(12, s), y + _s(28, s), _s(24, s), _s(16, s), stroke=stroke, sw=sw, roughness=roughness)
    a2 = ellipse(x + _s(4, s), y + _s(16, s), _s(40, s), _s(24, s), stroke=stroke, sw=sw, roughness=roughness)
    a3 = ellipse(x - _s(4, s), y + _s(4, s), _s(56, s), _s(32, s), stroke=stroke, sw=sw, roughness=roughness)
    return [dot, a1, a2, a3]


@_register("heart")
def _icon_heart(x, y, s, stroke, sw, roughness):
    """Heart shape."""
    l1 = ellipse(x + _s(2, s), y + _s(4, s), _s(22, s), _s(20, s), stroke=stroke, sw=sw, roughness=roughness)
    l2 = ellipse(x + _s(22, s), y + _s(4, s), _s(22, s), _s(20, s), stroke=stroke, sw=sw, roughness=roughness)
    v1 = _line(x + _s(2, s), y + _s(20, s), _s(21, s), _s(28, s), stroke=stroke, sw=sw, roughness=roughness)
    v2 = _line(x + _s(44, s), y + _s(20, s), -_s(21, s), _s(28, s), stroke=stroke, sw=sw, roughness=roughness)
    return [l1, l2, v1, v2]


@_register("star")
def _icon_star(x, y, s, stroke, sw, roughness):
    """5-point star."""
    import math
    cx_s, cy_s = x + _s(24, s), y + _s(24, s)
    outer_r, inner_r = _s(22, s), _s(10, s)
    pts = []
    for i in range(10):
        angle = math.radians(-90 + i * 36)
        r = outer_r if i % 2 == 0 else inner_r
        pts.append((cx_s + r * math.cos(angle), cy_s + r * math.sin(angle)))
    result = []
    for i in range(len(pts)):
        x1, y1 = pts[i]
        x2, y2 = pts[(i + 1) % len(pts)]
        result.append(_line(x1, y1, x2 - x1, y2 - y1, stroke=stroke, sw=sw, roughness=roughness))
    return result


@_register("lightning")
def _icon_lightning(x, y, s, stroke, sw, roughness):
    """Lightning bolt."""
    l1 = _line(x + _s(28, s), y, -_s(16, s), _s(22, s), stroke=stroke, sw=sw, roughness=roughness)
    l2 = _line(x + _s(12, s), y + _s(22, s), _s(20, s), 0, stroke=stroke, sw=sw, roughness=roughness)
    l3 = _line(x + _s(32, s), y + _s(22, s), -_s(18, s), _s(26, s), stroke=stroke, sw=sw, roughness=roughness)
    l4 = _line(x + _s(14, s), y + _s(48, s), _s(6, s), -_s(14, s), stroke=stroke, sw=sw, roughness=roughness)
    return [l1, l2, l3, l4]


@_register("clock")
def _icon_clock(x, y, s, stroke, sw, roughness):
    """Clock face."""
    face = ellipse(x, y, _s(48, s), _s(48, s), stroke=stroke, sw=sw, roughness=roughness)
    hh = _line(x + _s(24, s), y + _s(24, s), 0, -_s(14, s), stroke=stroke, sw=sw, roughness=roughness)
    mh = _line(x + _s(24, s), y + _s(24, s), _s(12, s), -_s(8, s), stroke=stroke, sw=sw, roughness=roughness)
    dot = ellipse(x + _s(21, s), y + _s(21, s), _s(6, s), _s(6, s), stroke=stroke, sw=sw, roughness=roughness)
    return [face, hh, mh, dot]


@_register("magnifier")
def _icon_magnifier(x, y, s, stroke, sw, roughness):
    """Magnifying glass."""
    lens = ellipse(x, y, _s(32, s), _s(32, s), stroke=stroke, sw=sw, roughness=roughness)
    handle = _line(x + _s(28, s), y + _s(28, s), _s(16, s), _s(16, s), stroke=stroke, sw=sw + 1, roughness=roughness)
    return [lens, handle]


@_register("fire")
def _icon_fire(x, y, s, stroke, sw, roughness):
    """Flame shape."""
    outer = ellipse(x + _s(6, s), y + _s(8, s), _s(36, s), _s(40, s), stroke=stroke, sw=sw, roughness=roughness)
    inner = ellipse(x + _s(14, s), y + _s(20, s), _s(20, s), _s(28, s), stroke=stroke, sw=sw, roughness=roughness)
    tip = _line(x + _s(24, s), y, 0, _s(12, s), stroke=stroke, sw=sw, roughness=roughness)
    return [outer, inner, tip]


@_register("globe")
def _icon_globe(x, y, s, stroke, sw, roughness):
    """Globe with meridian."""
    circle = ellipse(x, y, _s(48, s), _s(48, s), stroke=stroke, sw=sw, roughness=roughness)
    v = _line(x + _s(24, s), y, 0, _s(48, s), stroke=stroke, sw=sw, roughness=roughness)
    h = _line(x, y + _s(24, s), _s(48, s), 0, stroke=stroke, sw=sw, roughness=roughness)
    meridian = ellipse(x + _s(10, s), y, _s(28, s), _s(48, s), stroke=stroke, sw=sw, roughness=roughness)
    return [circle, v, h, meridian]


@_register("chat")
def _icon_chat(x, y, s, stroke, sw, roughness):
    """Chat bubble."""
    body = rect(x, y, _s(44, s), _s(32, s), stroke=stroke, sw=sw, roughness=roughness)
    t1 = _line(x + _s(10, s), y + _s(32, s), 0, _s(12, s), stroke=stroke, sw=sw, roughness=roughness)
    t2 = _line(x + _s(10, s), y + _s(44, s), _s(14, s), -_s(12, s), stroke=stroke, sw=sw, roughness=roughness)
    l1 = _line(x + _s(8, s), y + _s(10, s), _s(28, s), 0, stroke=stroke, sw=sw, roughness=roughness)
    l2 = _line(x + _s(8, s), y + _s(20, s), _s(20, s), 0, stroke=stroke, sw=sw, roughness=roughness)
    return [body, t1, t2, l1, l2]


@_register("api")
def _icon_api(x, y, s, stroke, sw, roughness):
    """API icon: angle brackets + slash."""
    lb1 = _line(x + _s(16, s), y + _s(4, s), -_s(12, s), _s(20, s), stroke=stroke, sw=sw, roughness=roughness)
    lb2 = _line(x + _s(4, s), y + _s(24, s), _s(12, s), _s(20, s), stroke=stroke, sw=sw, roughness=roughness)
    rb1 = _line(x + _s(28, s), y + _s(4, s), _s(12, s), _s(20, s), stroke=stroke, sw=sw, roughness=roughness)
    rb2 = _line(x + _s(40, s), y + _s(24, s), -_s(12, s), _s(20, s), stroke=stroke, sw=sw, roughness=roughness)
    sl = _line(x + _s(26, s), y + _s(6, s), -_s(8, s), _s(36, s), stroke=stroke, sw=sw, roughness=roughness)
    return [lb1, lb2, rb1, rb2, sl]


@_register("terminal")
def _icon_terminal(x, y, s, stroke, sw, roughness):
    """Terminal/console."""
    body = rect(x, y, _s(48, s), _s(36, s), stroke=stroke, sw=sw, roughness=roughness)
    p1 = _line(x + _s(8, s), y + _s(12, s), _s(10, s), _s(8, s), stroke=stroke, sw=sw, roughness=roughness)
    p2 = _line(x + _s(18, s), y + _s(20, s), -_s(10, s), _s(8, s), stroke=stroke, sw=sw, roughness=roughness)
    cur = _line(x + _s(24, s), y + _s(22, s), _s(14, s), 0, stroke=stroke, sw=sw, roughness=roughness)
    return [body, p1, p2, cur]


@_register("folder")
def _icon_folder(x, y, s, stroke, sw, roughness):
    """Folder icon."""
    body = rect(x, y + _s(10, s), _s(48, s), _s(34, s), stroke=stroke, sw=sw, roughness=roughness)
    tab = _line(x, y + _s(10, s), 0, -_s(10, s), stroke=stroke, sw=sw, roughness=roughness)
    tab2 = _line(x, y, _s(20, s), 0, stroke=stroke, sw=sw, roughness=roughness)
    tab3 = _line(x + _s(20, s), y, _s(6, s), _s(10, s), stroke=stroke, sw=sw, roughness=roughness)
    return [body, tab, tab2, tab3]


@_register("key")
def _icon_key(x, y, s, stroke, sw, roughness):
    """Key icon."""
    head = ellipse(x, y + _s(8, s), _s(20, s), _s(20, s), stroke=stroke, sw=sw, roughness=roughness)
    shaft = _line(x + _s(20, s), y + _s(18, s), _s(28, s), 0, stroke=stroke, sw=sw, roughness=roughness)
    t1 = _line(x + _s(36, s), y + _s(18, s), 0, _s(10, s), stroke=stroke, sw=sw, roughness=roughness)
    t2 = _line(x + _s(44, s), y + _s(18, s), 0, _s(8, s), stroke=stroke, sw=sw, roughness=roughness)
    return [head, shaft, t1, t2]

---
title: Element Builders
---

# Element Builders

Core building blocks for constructing Excalidraw diagrams programmatically. All functions return plain Python dictionaries (or lists of dictionaries) that represent Excalidraw scene elements.

## Basic Shapes

### `rect`

```python
from core.engine import rect

el = rect(
    x=100, y=50, w=200, h=80,
    fill="#a5d8ff",       # default: "transparent"
    stroke="#1e1e1e",     # default: "#1e1e1e"
    sw=2,                 # stroke width, default: 2
    roughness=1,          # 0=precise, 1=default, 2=rough
    fill_style="solid",   # "solid" | "hachure" | "cross-hatch"
    stroke_style="solid", # "solid" | "dashed" | "dotted"
)
```

Returns: `dict` -- a single Excalidraw rectangle element.

### `ellipse`

```python
from core.engine import ellipse

el = ellipse(
    x=100, y=50, w=120, h=60,
    fill="transparent",
    stroke="#1e1e1e",
    sw=2,
    roughness=1,
    fill_style="solid",
)
```

Returns: `dict` -- a single Excalidraw ellipse element.

### `diamond`

```python
from core.engine import diamond

el = diamond(
    x=100, y=50, w=160, h=100,
    fill="transparent",
    stroke="#1e1e1e",
    sw=2,
    roughness=1,
    fill_style="solid",
)
```

Returns: `dict` -- a single Excalidraw diamond element.

## Labeled Shapes

Labeled shapes return a `[shape, text]` pair with the text bound to the shape via `containerId`. Excalidraw auto-centers the text within the shape.

### `labeled_rect`

```python
from core.engine import labeled_rect

shape, label = labeled_rect(
    x=100, y=50, w=200, h=60,
    label="Process",
    fill="transparent",
    stroke="#1e1e1e",
    sw=2,
    fs=16,                # font size
    label_color=None,     # defaults to stroke color
    roughness=1,
    font_family=3,        # 1=Virgil, 2=Helvetica, 3=Cascadia
    fill_style="solid",
    stroke_style="solid",
)
```

Returns: `list[dict]` -- `[rectangle, bound_text]`.

### `labeled_ellipse`

```python
from core.engine import labeled_ellipse

shape, label = labeled_ellipse(
    x=100, y=50, w=120, h=60,
    label="Start",
    fill="#d0f0c0",
    stroke="#1e1e1e",
    sw=2,
    fs=16,
    label_color=None,
    roughness=1,
    font_family=3,
    fill_style="solid",
)
```

Returns: `list[dict]` -- `[ellipse, bound_text]`.

### `labeled_diamond`

```python
from core.engine import labeled_diamond

shape, label = labeled_diamond(
    x=100, y=50, w=160, h=100,
    label="Decision?",
    fill="transparent",
    stroke="#1e1e1e",
    sw=2,
    fs=16,
    label_color=None,
    roughness=1,
    font_family=3,
    fill_style="solid",
)
```

Returns: `list[dict]` -- `[diamond, bound_text]`.

## Connectors

### `arrow`

```python
from core.engine import arrow

# Relative offset mode
a1 = arrow(250, 70, dx=0, dy=30, stroke="#1e1e1e", sw=2, roughness=1)

# Absolute coordinate mode (keyword-only)
a2 = arrow(100, 50, x2=300, y2=200, stroke="#1e1e1e", sw=2, roughness=1)
```

Returns: `dict` -- a single Excalidraw arrow element.

### `line`

```python
from core.engine import line

# Relative offset mode
l1 = line(100, 50, dx=200, dy=0, stroke="#1e1e1e", sw=2, roughness=1)

# Absolute coordinate mode
l2 = line(100, 50, x2=300, y2=100, stroke="#1e1e1e", sw=2, roughness=1)
```

Returns: `dict` -- a single Excalidraw line element.

### `bind_arrow`

Binds an arrow to start and end elements, establishing bidirectional references.

```python
from core.engine import arrow, bind_arrow, labeled_rect

step1 = labeled_rect(100, 50, 200, 60, "Step 1")
step2 = labeled_rect(100, 150, 200, 60, "Step 2")

a = arrow(200, 110, dx=0, dy=40)
bound = bind_arrow(a, step1[0], step2[0], gap=2)
```

Returns: `dict` -- the arrow element with `startBinding` and `endBinding` set.

### `connect`

Creates a bound arrow connecting two elements in one call. The arrow starts at the center of the start element and Excalidraw computes the correct edge intersection.

```python
from core.engine import labeled_rect, connect

step1 = labeled_rect(100, 50, 200, 60, "Step 1")
step2 = labeled_rect(100, 150, 200, 60, "Step 2")

a = connect(step1[0], step2[0], stroke="#1e1e1e", sw=2, roughness=1, gap=8)
```

Returns: `dict` -- a bound arrow element.

## Text

### `text_standalone`

```python
from core.engine import text_standalone

t = text_standalone(
    cx=300, cy=100,           # center position
    txt="Hello World",
    fs=20,                     # font size, default: 20
    color="#1e1e1e",           # text color
    font_family=3,             # 1=Virgil, 2=Helvetica, 3=Cascadia
    roughness=0,
    text_align="center",       # "center" | "left" | "right"
    max_width=None,            # auto-shrink font if text exceeds width
)
```

Returns: `dict` -- a single Excalidraw text element.

`text_standalone` supports `text_align` (`"center"`, `"left"`, `"right"`) and `max_width` -- when set, the font size auto-shrinks until the text fits.

## Structural Elements

### `numbered_circle`

```python
from core.engine import numbered_circle

circle = numbered_circle(cx=100, cy=50, num=1, fill="#a5d8ff", stroke="#2B5B84")
```

Returns: `list[dict]` -- `[ellipse, text]` with the number centered inside.

### `frame`

```python
from core.engine import frame

f = frame(x=0, y=0, w=500, h=400, name="Architecture", stroke="#1e1e1e", sw=2)
```

Returns: `dict` -- a single Excalidraw frame element.

### `group`

```python
from core.engine import group, rect, ellipse

elements = [
    rect(0, 0, 100, 50),
    ellipse(10, 10, 30, 30),
]
grouped = group(elements)
```

Returns: `list[dict]` -- a new list of elements sharing a common `groupIds` entry.

### `image_embed`

```python
from core.engine import image_embed

el, files = image_embed(
    x=100, y=50, w=200, h=150,
    base64_data="iVBORw0KGgo...",
    mime="image/png",
)
```

Returns: `tuple[dict, dict]` -- the image element and a `files` dict for embedding in the scene.

## Function Reference

| Function | Signature | Returns |
|----------|-----------|---------|
| `rect` | `rect(x, y, w, h, fill, stroke, sw, roughness, fill_style, stroke_style)` | `dict` |
| `ellipse` | `ellipse(x, y, w, h, fill, stroke, sw, roughness, fill_style)` | `dict` |
| `diamond` | `diamond(x, y, w, h, fill, stroke, sw, roughness, fill_style)` | `dict` |
| `labeled_rect` | `labeled_rect(x, y, w, h, label, fill, stroke, sw, fs, label_color, roughness, font_family, fill_style, stroke_style)` | `[rect, text]` |
| `labeled_ellipse` | `labeled_ellipse(x, y, w, h, label, fill, stroke, sw, fs, label_color, roughness, font_family, fill_style)` | `[ellipse, text]` |
| `labeled_diamond` | `labeled_diamond(x, y, w, h, label, fill, stroke, sw, fs, label_color, roughness, font_family, fill_style)` | `[diamond, text]` |
| `text_standalone` | `text_standalone(cx, cy, txt, fs=20, color, font_family=3, roughness=0, text_align="center", max_width=None)` | `dict` |
| `arrow` | `arrow(x, y, dx=0, dy=0, *, x2=None, y2=None, stroke, sw, roughness)` | `dict` |
| `line` | `line(x, y, dx=0, dy=0, *, x2=None, y2=None, stroke, sw, roughness)` | `dict` |
| `numbered_circle` | `numbered_circle(cx, cy, num, fill, stroke)` | `[ellipse, text]` |
| `frame` | `frame(x, y, w, h, name="Frame", stroke, sw)` | `dict` |
| `group` | `group(elements)` | `list[dict]` |
| `bind_arrow` | `bind_arrow(arrow_el, start_el, end_el, gap=2)` | `dict` |
| `connect` | `connect(start_el, end_el, stroke, sw, roughness, gap=8)` | `dict` |
| `image_embed` | `image_embed(x, y, w, h, base64_data, mime="image/png")` | `(element, files)` |
| `bounds` | `bounds(elements)` | `(min_x, min_y, max_x, max_y)` |

## Layout Helpers

Prevent text and shape overlap with positional utilities:

```python
from core.engine import below, right_of, above

y2 = below(y=100, h=60, gap=15)     # y2 = 175
x2 = right_of(x=50, w=200, gap=10)  # x2 = 260
y_above = above(y=100, gap=10)      # y_above = 90
```

| Helper | Signature | Description |
|--------|-----------|-------------|
| `below` | `below(y, h, gap=10)` | Safe y-coordinate below a shape |
| `right_of` | `right_of(x, w, gap=10)` | Safe x-coordinate to the right of a shape |
| `above` | `above(y, gap=10)` | Safe y-coordinate above a shape |
| `bounds` | `bounds(elements)` | Bounding box `(min_x, min_y, max_x, max_y)` |

## Output

### `save`

Auto-detects the output format from the file extension.

```python
from core.engine import save

save("diagram.excalidraw", elements)        # Standard JSON
save("diagram.excalidraw.md", elements)     # Obsidian Markdown wrapper
```

### `save_excalidraw`

Writes pure JSON compatible with [excalidraw.com](https://excalidraw.com), VS Code extension, and any Excalidraw-compatible tool.

```python
from core.engine import save_excalidraw

save_excalidraw("diagram.excalidraw", elements, bg="#ffffff", files=None)
```

### `save_obsidian_md`

Writes a Markdown wrapper for the [Obsidian Excalidraw plugin](https://github.com/zsviczian/obsidian-excalidraw-plugin).

```python
from core.engine import save_obsidian_md

save_obsidian_md("diagram.excalidraw.md", elements, bg="#ffffff", files=None)
```

## Complete Example: Flowchart

```python
from core.engine import (
    labeled_ellipse, labeled_rect, labeled_diamond,
    arrow, bind_arrow, save,
)

# 1. Create shapes
start   = labeled_ellipse(200, 20, 120, 50, "Start", fill="#d0f0c0")
process = labeled_rect(170, 110, 180, 60, "Process Data")
decision = labeled_diamond(160, 220, 200, 120, "Valid?")
end_yes = labeled_ellipse(140, 400, 120, 50, "Done", fill="#d0f0c0")
end_no  = labeled_ellipse(340, 400, 120, 50, "Retry", fill="#ffc9c9")

# 2. Connect with arrows
a1 = bind_arrow(arrow(260, 70, 0, 40), start[0], process[0])
a2 = bind_arrow(arrow(260, 170, 0, 50), process[0], decision[0])
a3 = bind_arrow(arrow(220, 340, 0, 60), decision[0], end_yes[0])
a4 = bind_arrow(arrow(340, 340, 0, 60), decision[0], end_no[0])

# 3. Collect and save
elements = [*start, *process, *decision, *end_yes, *end_no, a1, a2, a3, a4]
save("flowchart.excalidraw", elements)
```

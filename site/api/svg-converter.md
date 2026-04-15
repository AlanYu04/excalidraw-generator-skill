---
title: SVG Converter
---

# SVG Converter

Convert SVG strings or files to native Excalidraw elements. The converter parses SVG path data, tessellates Bezier curves and arcs into polylines, simplifies them via Ramer-Douglas-Peucker, and classifies shapes as ellipses, rectangles, or freeform lines.

## `svg_to_elements`

```python
from core.svg_converter import svg_to_elements

elements = svg_to_elements(
    '<svg viewBox="0 0 100 100"><circle cx="50" cy="50" r="40"/></svg>',
    x=100, y=50,
    scale=1.0,
    stroke="#1e1e1e",
    stroke_width=2,
    roughness=1,
)
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `svg_string` | `str` | required | SVG content as a string |
| `x` | `float` | `0` | X offset for the generated elements |
| `y` | `float` | `0` | Y offset for the generated elements |
| `scale` | `float` | `1.0` | Scale factor applied to all coordinates |
| `stroke` | `str` | `"#1e1e1e"` | Default stroke color |
| `stroke_width` | `int` | `2` | Default stroke width |
| `roughness` | `int` | `1` | Excalidraw roughness (0=precise, 1=slight, 2=rough) |

Returns: `list[dict]` -- list of Excalidraw element dicts.

If the SVG has a `viewBox` attribute, the converter normalizes the output to ~100px and applies the `scale` parameter on top.

## `svg_file_to_elements`

```python
from core.svg_converter import svg_file_to_elements

elements = svg_file_to_elements("icon.svg", x=200, y=100, scale=2.0)
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `filepath` | `str` | required | Path to the SVG file |
| `x` | `float` | `0` | X offset |
| `y` | `float` | `0` | Y offset |
| `scale` | `float` | `1.0` | Scale factor |
| `stroke` | `str` | `"#1e1e1e"` | Default stroke color |
| `stroke_width` | `int` | `2` | Default stroke width |
| `roughness` | `int` | `1` | Roughness level |

Returns: `list[dict]` -- list of Excalidraw element dicts.

## Supported SVG Features

The converter handles the following SVG elements and features:

**Elements:**
- `<path>` with all standard commands
- `<rect>`
- `<circle>`
- `<ellipse>`
- `<line>`
- `<polygon>`
- `<polyline>`
- `<defs>` and `<use>` (reference resolution)

**Path Commands:**
- `M`, `m` -- MoveTo
- `L`, `l` -- LineTo
- `H`, `h` -- Horizontal LineTo
- `V`, `v` -- Vertical LineTo
- `C`, `c` -- Cubic Bezier
- `S`, `s` -- Shorthand Cubic
- `Q`, `q` -- Quadratic Bezier
- `T`, `t` -- Shorthand Quadratic
- `A`, `a` -- Arc
- `Z`, `z` -- Close Path

**Processing Pipeline:**
1. Bezier tessellation (cubic: 8 samples, quadratic: 6 samples, arc: 36 samples)
2. Ramer-Douglas-Peucker simplification with adaptive epsilon
3. Automatic shape classification (ellipse, rectangle, or freeform line)
4. Gradient fill resolution from `<defs>`
5. Transform parsing (`translate`, `scale`, `rotate`, `matrix`)

## Example: Importing a Logo

```python
from core.svg_converter import svg_file_to_elements
from core.engine import save

elements = svg_file_to_elements(
    "company-logo.svg",
    x=100, y=100,
    scale=3.0,
    stroke="#2B5B84",
    stroke_width=2,
    roughness=1,
)

save("logo.excalidraw", elements)
```

## Example: Inline SVG

```python
from core.svg_converter import svg_to_elements
from core.engine import save, rect

svg = '''
<svg viewBox="0 0 48 48">
  <circle cx="24" cy="24" r="20" fill="#a5d8ff" stroke="#1e1e1e"/>
  <line x1="10" y1="24" x2="38" y2="24" stroke="#1e1e1e" stroke-width="2"/>
</svg>
'''

background = rect(0, 0, 300, 200, fill="#ffffff")
icon_elements = svg_to_elements(svg, x=50, y=50, scale=4.0)

save("icon-demo.excalidraw", [background, *icon_elements])
```

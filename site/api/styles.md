---
title: Styles
---

# Styles

Control the visual appearance of generated diagrams through preset styles or custom YAML configurations. Styles define colors, typography, roughness, fill patterns, and layout defaults.

## Preset Styles

| Preset | Font | Roughness | Fill Style | Use Case |
|--------|------|-----------|------------|----------|
| **Vivid** | Cascadia (3) | 1 | solid | Rich, colorful, detailed |
| **Clean** | Helvetica (2) | 0 | solid | Minimal, black-and-white, precise |
| **Sketch** | Virgil (1) | 2 | hachure | Hand-drawn, casual |

## `load_style`

Load a style by name. Checks built-in presets first, then falls back to custom YAML files in `~/.excalidraw-gen/styles/`.

```python
from styles import load_style

style = load_style("vivid")
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `name` | `str` | required | Style name (`"vivid"`, `"clean"`, `"sketch"`, or custom) |

Returns: `StyleConfig` instance.

Raises `FileNotFoundError` if the style name is not found as a built-in or custom YAML file.

## `list_styles`

```python
from styles import list_styles

names = list_styles()  # ["vivid", "clean", "sketch", ...custom styles]
```

Returns: `list[str]` -- all available style names (built-in + custom).

## Using Style Properties

```python
from styles import load_style

style = load_style("vivid")

# Color pairs for semantic roles
fill, stroke = style.get_color_pair("primary")    # ("#a5d8ff", "#2B5B84")
fill, stroke = style.get_color_pair("danger")     # ("#ffc9c9", "#e03131")
fill, stroke = style.get_color_pair("success")    # ("#b2f2bb", "#2f9e44")

# Typography
font = style.font_family       # 3 (Cascadia)
title_size = style.title_size  # 24

# Layout
roughness = style.roughness       # 1
gap = style.default_gap           # 50
fill_style = style.fill_style     # "solid"
```

## `get_color_pair`

Returns a `(fill, stroke)` tuple for a semantic role. Available on any `StyleConfig` instance.

```python
style = load_style("vivid")
fill, stroke = style.get_color_pair("primary")
```

| Role | Returns (Vivid) |
|------|----------------|
| `primary` | `("#a5d8ff", "#2B5B84")` |
| `accent` | `("#ffd8a8", "#E67E22")` |
| `success` | `("#b2f2bb", "#2f9e44")` |
| `warning` | `("#fff3bf", "#f08c00")` |
| `danger` | `("#ffc9c9", "#e03131")` |
| `info` | `("#99e9f2", "#1971c2")` |
| `neutral` | `("#dee2e6", "#999999")` |

## Direct Preset Imports

Import presets directly for convenience:

```python
from styles import vivid_style, clean_style, sketch_style

vivid = vivid_style()    # StyleConfig for Vivid preset
clean = clean_style()    # StyleConfig for Clean preset
sketch = sketch_style()  # StyleConfig for Sketch preset
```

## Style Aliases

For backward compatibility, the following aliases are resolved by `load_style`:

| Alias | Resolves To |
|-------|-------------|
| `"conference"` | `"vivid"` |
| `"journal"` | `"clean"` |
| `"ppt"` | `"sketch"` |

```python
from styles import load_style

style = load_style("conference")  # same as load_style("vivid")
```

## Custom YAML Styles

Create a YAML file at `~/.excalidraw-gen/styles/<name>.yaml`:

```yaml
name: "Dark Mode"
description: "Dark background theme"
colors:
  background: "#1a1a2e"
  primary: "#4A90E2"
  accent: "#E67E22"
  text: "#e0e0e0"
  border: "#555555"
  muted: "#888888"
typography:
  font_family: 3
  title_size: 24
  body_size: 14
  label_size: 11
layout:
  roughness: 1
  border_width: 2
  arrow_width: 2
  default_gap: 50
  border_radius: true
```

Then load with `load_style("dark-mode")`.

The loader maps YAML keys to `StyleConfig` fields. Only the fields you specify are overridden; everything else keeps its default.

### YAML Structure Reference

| Section | Keys |
|---------|------|
| `colors` | `background`, `primary`, `accent`, `border`, `muted`, `text` |
| `typography` | `font_family`, `title_size`, `body_size`, `label_size` |
| `layout` | `roughness`, `border_width`, `arrow_width`, `default_gap`, `border_radius` |

## StyleConfig Fields

The full `StyleConfig` dataclass exposes these fields:

**Colors:**
`background`, `primary`, `accent`, `text_color`, `border_color`, `muted`, `success`, `warning`, `danger`, `info`

**Fill Colors:**
`primary_fill`, `accent_fill`, `success_fill`, `warning_fill`, `danger_fill`, `info_fill`, `neutral_fill`

**Typography:**
`font_family` (1=Virgil, 2=Helvetica, 3=Cascadia), `title_size`, `subtitle_size`, `body_size`, `label_size`, `caption_size`

**Layout:**
`roughness` (0/1/2), `border_width`, `arrow_width`, `default_gap`, `padding`

**Fill/Stroke:**
`fill_style` (`"solid"` | `"hachure"` | `"cross-hatch"`), `stroke_style` (`"solid"` | `"dashed"` | `"dotted"`)

**Shape:**
`border_radius`, `use_groups`, `compact_layout`

## Complete Example

```python
from styles import load_style
from core.engine import labeled_rect, arrow, bind_arrow, save

style = load_style("vivid")

fill, stroke = style.get_color_pair("primary")
box1 = labeled_rect(100, 50, 200, 60, "Service A",
                    fill=fill, stroke=stroke,
                    roughness=style.roughness, font_family=style.font_family)

fill2, stroke2 = style.get_color_pair("accent")
box2 = labeled_rect(100, 180, 200, 60, "Service B",
                    fill=fill2, stroke=stroke2,
                    roughness=style.roughness, font_family=style.font_family)

a = arrow(200, 110, dx=0, dy=70, stroke=stroke, sw=style.arrow_width,
          roughness=style.roughness)
bound = bind_arrow(a, box1[0], box2[0])

save("styled-diagram.excalidraw", [*box1, *box2, bound])
```

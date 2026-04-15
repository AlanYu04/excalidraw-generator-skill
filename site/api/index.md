---
title: API Reference
---

# API Reference

Excalidraw Generator provides 40+ public functions across these modules:

| Module | Key Functions | Description |
|--------|--------------|-------------|
| `core.engine` | `rect`, `ellipse`, `diamond`, `labeled_*`, `arrow`, `bind_arrow`, `connect` | Element builders and layout |
| `core.charts` | `bar_chart`, `horizontal_bar_chart`, `line_chart`, `pie_chart` | Data visualization |
| `core.icons` | `icon`, `list_icons` | 39 built-in icons |
| `core.svg_converter` | `svg_to_elements`, `svg_file_to_elements` | SVG import |
| `core.latex` | `formula` | LaTeX formula rendering |
| `core.icon_library` | `save_icon`, `load_icon`, `find_icons` | Persistent icon storage |
| `core.ai_icons` | `generate_icon`, `generate_and_save` | AI-powered icon generation |
| `styles` | `load_style`, `vivid_style`, `clean_style`, `sketch_style` | Visual presets |

## Quick Import

```python
# All public API available from core
from core.engine import *
from core.charts import *
from core.icons import *
from core.latex import formula
from core.svg_converter import svg_to_elements
```

## Next Steps

- [Element Builders](./elements) -- shapes, arrows, layout helpers, and output
- [Charts](./charts) -- bar, horizontal bar, line, and pie charts
- [Icons](./icons) -- built-in icons, icon library, and AI generation
- [SVG Converter](./svg-converter) -- convert SVG to native Excalidraw elements
- [LaTeX Formulas](./latex) -- render math expressions as images
- [Styles](./styles) -- presets, custom YAML, and color pairs

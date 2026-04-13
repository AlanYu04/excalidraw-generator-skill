# Excalidraw Generator

> Python-based Excalidraw diagram generator for Claude Code. Generate publication-quality flowcharts, charts, and diagrams with CJK support.

**39 Built-in Icons | 4 Chart Types | 3 Style Presets | CJK Support | Zero Dependencies***

(* AI icon generation requires a Gemini API key; YAML styles require PyYAML)

---

## Features

- **Element builders** -- rectangles, ellipses, diamonds, arrows, lines, text -- all with `containerId` binding
- **4 chart types** -- bar, horizontal bar, line, pie (with donut mode)
- **39 built-in icons** -- general + ML/AI + utility
- **AI-powered icon generation** via Gemini API
- **3 style presets** -- Vivid, Clean, Sketch + custom YAML
- **SVG-to-Excalidraw conversion** with Bezier tessellation and shape classification
- **Persistent icon library** with TF-IDF search (zero-dep) or OpenAI embedding search
- **Full CJK** (Chinese, Japanese, Korean) text support
- **Layout helpers** to prevent text/shape overlap
- **Output** as `.excalidraw` or `.excalidraw.md` (Obsidian)

---

## Quick Start

### As a Claude Code Skill

```bash
git clone https://github.com/user/excalidraw-generator ~/.claude/skills/excalidraw-generator
```

Then just ask Claude:

> *"Draw me a Transformer architecture diagram -- vivid style, hachure fill, roughness 1"*

### As a Python Library

```python
from core.engine import labeled_rect, labeled_ellipse, arrow, bind_arrow, save

# 1. Create shapes
start = labeled_ellipse(200, 20, 100, 50, "Start", fill="#d0f0c0")
step  = labeled_rect(150, 100, 200, 60, "Process")
end   = labeled_ellipse(200, 200, 100, 50, "End", fill="#d0f0c0")

# 2. Connect with arrows
a1 = bind_arrow(arrow(250, 70, 0, 30), start[0], step[0])
a2 = bind_arrow(arrow(250, 160, 0, 40), step[0], end[0])

# 3. Save
elements = [*start, *step, *end, a1, a2]
save("flow.excalidraw", elements)
```

---

## Element Builders

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

`text_standalone` supports `text_align` ("center", "left", "right") and `max_width` -- when set, the font size auto-shrinks until the text fits.

---

## Layout Helpers

Prevent text/shape overlap with positional helpers:

```python
from core.engine import below, right_of, above

y2 = below(y=100, h=60, gap=15)    # y2 = 175
x2 = right_of(x=50, w=200, gap=10) # x2 = 260
y_above = above(y=100, gap=10)     # y_above = 90
```

---

## Charts

### Bar Chart

```python
from core.charts import bar_chart

elements = bar_chart(
    x=50, y=100,
    data={"React": 85, "Vue": 72, "Angular": 58},
    title="Framework Popularity",
    bar_color="#a5d8ff",
    show_values=True,
    show_grid=True,
    font_family=3,
)
```

### Horizontal Bar Chart

```python
from core.charts import horizontal_bar_chart

elements = horizontal_bar_chart(
    x=50, y=50,
    data={"Training": 120, "Inference": 85, "Eval": 45},
    title="Time Breakdown (min)",
    bar_colors={"Training": "#a5d8ff", "Inference": "#b2f2bb", "Eval": "#ffd8a8"},
)
```

### Line Chart (Multi-Series)

```python
from core.charts import line_chart

elements = line_chart(
    x=50, y=50,
    data={
        "Revenue": [10, 25, 35, 50, 70],
        "Costs":   [8, 15, 20, 30, 35],
    },
    labels=["Q1", "Q2", "Q3", "Q4", "Q5"],
    title="Revenue vs Costs",
    series_colors={"Revenue": "#1971c2", "Costs": "#e03131"},
    show_points=True,
    show_legend=True,
)
```

### Pie Chart (with Donut Mode)

```python
from core.charts import pie_chart

elements = pie_chart(
    x=100, y=100,
    data={"Mobile": 45, "Desktop": 35, "Tablet": 20},
    title="Traffic by Device",
    donut=True,
    donut_radius=50,
    show_percentages=True,
)
```

---

## Icons (39 Built-in)

### General (10)

| Icon | Name | Description |
|------|------|-------------|
| Cylinder | `database` | Data storage |
| Person | `user` | Users, actors |
| Cloud | `cloud` | Cloud services |
| Rack | `server` | Infrastructure |
| Cog | `gear` | Settings, config |
| Paper | `document` | Files, pages |
| Shield | `shield` | Security |
| Arrow | `arrow-right` | Direction |
| Tick | `check` | Approval, done |
| Triangle | `warning` | Alerts, caution |

### ML/AI (12)

| Icon | Name | Description |
|------|------|-------------|
| Block | `transformer-block` | Multi-head attention + FFN |
| Arrows | `attention-head` | Q, K, V convergence |
| Grid | `embedding-layer` | Embedding matrix |
| Stack | `feedforward` | Two-layer FFN |
| Block-E | `encoder` | Encoder stack |
| Block-D | `decoder` | Decoder stack |
| Curve | `loss-function` | Descending loss curve |
| Spiral | `optimizer` | Gradient descent |
| Chip | `gpu` | GPU / accelerator |
| Head | `robot` | AI agent |
| Brain | `brain` | Intelligence |
| Nodes | `neural-net` | 3-layer network |

### Utility (18)

| Icon | Name | Description |
|------|------|-------------|
| 3D box | `cube` | Generic object |
| Funnel | `data-pipeline` | ETL, processing |
| Grid | `matrix` | 2D matrix |
| Padlock | `lock` | Security, auth |
| Signal | `wifi` | Connectivity |
| Heart | `heart` | Health, favorites |
| Star | `star` | Rating, favorite |
| Bolt | `lightning` | Speed, energy |
| Face | `clock` | Time, scheduling |
| Glass | `magnifier` | Search, inspect |
| Flame | `fire` | Hot, trending |
| Globe | `globe` | Global, web |
| Bubble | `chat` | Messaging |
| Brackets | `api` | API endpoint |
| Prompt | `terminal` | CLI, console |
| Tab | `folder` | Directory |
| Key | `key` | Authentication |

```python
from core.icons import icon, list_icons

# List all available icons
print(list_icons())

# Place an icon
elements = icon("database", x=100, y=50, scale=1.0, stroke="#1e1e1e", sw=2, roughness=1)
```

### Icon Library (Persistent & Searchable)

Save, load, and search custom icons stored at `~/.excalidraw-gen/icons/`.

| Function | Description |
|----------|-------------|
| `save_icon(name, elements, description, tags, source)` | Save icon to library |
| `load_icon(name, x=0, y=0, scale=1.0)` | Load and reposition icon |
| `delete_icon(name)` | Remove icon from library |
| `list_library_icons()` | List all saved icons |
| `find_icons(query, limit=5, use_embeddings=False)` | Search by description (TF-IDF or OpenAI embeddings) |
| `import_excalidrawlib(filepath, descriptions, tags_map, prefix)` | Import from `.excalidrawlib` files |

```python
from core.icon_library import save_icon, load_icon, find_icons

save_icon("my-server", elements, description="Server with LED indicators",
          tags=["server", "hardware"])

results = find_icons("server infrastructure")
server = load_icon(results[0]["name"], x=200, y=100)
```

### AI Icon Generation

Generate icons via the Gemini API, with automatic SVG-to-Excalidraw conversion and PNG fallback.

| Function | Description |
|----------|-------------|
| `configure(api_url, api_key, model)` | Save Gemini API configuration |
| `generate_icon(description, x, y, scale, stroke, sw, roughness, prompt)` | Generate icon as Excalidraw elements |
| `generate_icon_svg(description, prompt, model)` | Generate raw SVG string |
| `generate_and_save(name, description, tags, **kwargs)` | Generate and save to library |

```python
from core.ai_icons import configure, generate_icon, generate_and_save

configure(api_url="https://generativelanguage.googleapis.com/v1beta",
          api_key="YOUR_KEY", model="gemini-2.0-flash")

elements = generate_icon("kubernetes pod", x=100, y=200, scale=1.5)
generate_and_save("k8s-pod", "Kubernetes pod icon", tags=["k8s", "container"])
```

---

## Styles

| Preset | Font | Roughness | Fill Style | Use Case |
|--------|------|-----------|------------|----------|
| **Vivid** | Cascadia (3) | 1 | solid | Rich, colorful, detailed |
| **Clean** | Helvetica (2) | 0 | solid | Minimal, B&W, precise |
| **Sketch** | Virgil (1) | 2 | hachure | Hand-drawn, casual |

```python
from styles import load_style, vivid_style, clean_style, sketch_style

style = load_style("vivid")
fill, stroke = style.get_color_pair("primary")  # ("#a5d8ff", "#2B5B84")
fill, stroke = style.get_color_pair("danger")    # ("#ffc9c9", "#e03131")
```

**Aliases:** `conference` -> `vivid`, `journal` -> `clean`, `ppt` -> `sketch`

### Custom YAML Styles

Create `~/.excalidraw-gen/styles/dark-mode.yaml`:

```yaml
name: "Dark Mode"
colors:
  background: "#1a1a2e"
  primary: "#4A90E2"
  accent: "#E67E22"
  text: "#e0e0e0"
  border: "#555555"
typography:
  font_family: 3
  title_size: 24
  body_size: 14
layout:
  roughness: 1
  border_width: 2
  default_gap: 50
```

Then load with `load_style("dark-mode")`.

`get_color_pair(role)` supports: `primary`, `accent`, `success`, `warning`, `danger`, `info`, `neutral`.

---

## SVG Converter

Convert SVG strings or files to native Excalidraw elements.

```python
from core.svg_converter import svg_to_elements, svg_file_to_elements

# From string
elements = svg_to_elements(
    '<svg viewBox="0 0 100 100"><circle cx="50" cy="50" r="40"/></svg>',
    x=100, y=50, scale=1.0,
    stroke="#1e1e1e", stroke_width=2, roughness=1,
)

# From file
elements = svg_file_to_elements("icon.svg", x=200, y=100, scale=2.0)
```

Supported SVG features: `<path>` (M/L/H/V/C/S/Q/T/A/Z), `<rect>`, `<circle>`, `<ellipse>`, `<line>`, `<polygon>`, `<polyline>`, `<defs>`, `<use>`, Bezier tessellation, RDP simplification, gradient fill resolution, and automatic shape classification (ellipse, rectangle, or line).

---

## CJK Support

CJK-aware text width estimation ensures Chinese, Japanese, and Korean text centers correctly. No extra configuration needed -- all text functions handle CJK characters automatically.

```python
# CJK text works in any element
elements = labeled_rect(100, 50, 200, 60, "数据处理流程", font_family=3)

# Multi-line CJK text
t = text_standalone(300, 100, "第一行\n第二行\n第三行", fs=16, font_family=3)
```

For CJK-optimized rendering in Excalidraw, use `font_family=5`.

---

## Output Formats

### `.excalidraw`

Standard JSON -- works with [excalidraw.com](https://excalidraw.com), VS Code extension, and any Excalidraw-compatible tool.

### `.excalidraw.md`

Markdown wrapper for the [Obsidian Excalidraw plugin](https://github.com/zsviczian/obsidian-excalidraw-plugin).

```python
from core.engine import save

save("diagram.excalidraw", elements)        # Pure JSON
save("diagram.excalidraw.md", elements)     # Obsidian format
```

The `save()` function auto-detects the format from the file extension.

---

## Project Structure

```
excalidraw-generator/
├── SKILL.md                    # Claude Code skill entry point
├── README.md
├── core/
│   ├── __init__.py
│   ├── engine.py               # Element builders, layout helpers, output
│   ├── icons.py                # 39 built-in icons
│   ├── charts.py               # Bar, horizontal bar, line, pie charts
│   ├── svg_converter.py        # SVG to Excalidraw conversion
│   ├── icon_library.py         # Persistent icon library & TF-IDF search
│   └── ai_icons.py             # AI icon generation via Gemini API
├── styles/
│   ├── __init__.py
│   ├── base.py                 # StyleConfig dataclass
│   ├── conference.py           # Vivid preset
│   ├── journal.py              # Clean preset
│   ├── ppt.py                  # Sketch preset
│   └── loader.py               # Style resolver + custom YAML
├── prompts/
│   ├── conference-prompt.md
│   ├── journal-prompt.md
│   └── ppt-prompt.md
├── tests/
│   ├── test_smoke.py
│   ├── test_labeled_shapes.py
│   ├── test_group_frame.py
│   ├── test_image_arrow.py
│   ├── test_icons.py
│   ├── test_svg_converter.py
│   ├── test_charts.py
│   ├── test_icon_library.py
│   └── test_ai_icons.py
├── examples/
│   ├── generate_style_v3.py
│   ├── generate_p1_demos.py
│   ├── generate_p2_demos.py
│   └── *.excalidraw            # Example outputs
└── assets/
    ├── icon.svg
    ├── demo-gallery.png
    ├── bar-charts-demo.png
    └── how-it-works.png
```

---

## License

[MIT](LICENSE)

<div align="center">

# ✏️ Excalidraw Generator

**[English](README.md)** | **[中文](README_CN.md)**

**AI-powered diagram generator for Claude Code**

Generate publication-quality flowcharts, architecture diagrams, charts, and more — directly as Excalidraw JSON.

[![Python 3.9+](https://img.shields.io/badge/Python-3.9+-3776AB?logo=python&logoColor=white)](https://python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Claude Code Skill](https://img.shields.io/badge/Claude_Code-Skill-blueviolet?logo=data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMjQiIGhlaWdodD0iMjQiIHZpZXdCb3g9IjAgMCAyNCAyNCIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48cGF0aCBkPSJNMTIgMkw0IDdWMTdMMTIgMjJMMjAgMTdWN0wxMiAyWiIgc3Ryb2tlPSJ3aGl0ZSIgc3Ryb2tlLXdpZHRoPSIyIi8+PC9zdmc+)](https://github.com/AlanYu04/excalidraw-generator-skill)

`39 Built-in Icons` · `4 Chart Types` · `3 Style Presets` · `CJK Support` · `LaTeX Formulas` · `Diagram Pipeline` · `Layout Verification` · `Zero Dependencies`

</div>

---

## ✨ Features

| | Feature | Description |
|---|---------|-------------|
| 📐 | **Element Builders** | Rectangles, ellipses, diamonds, arrows, lines, text — all with `containerId` binding |
| 📊 | **4 Chart Types** | Bar, horizontal bar, line, pie (with donut mode) |
| 🎨 | **39 Built-in Icons** | General + ML/AI + utility icon sets |
| 🤖 | **AI Icon Generation** | Generate custom icons via Gemini API |
| 🎭 | **3 Style Presets** | Vivid, Clean, Sketch + custom YAML styles |
| 🔄 | **SVG Conversion** | SVG-to-Excalidraw with Bezier tessellation and shape classification |
| 📚 | **Icon Library** | Persistent storage with TF-IDF search (zero-dep) or OpenAI embeddings |
| 🇨🇳 | **Full CJK Support** | Chinese, Japanese, Korean text rendering |
| 🇨 | **LaTeX Formulas** | Mathtext + usetex fallback with 4 font options |
| 🔗 | **Diagram Pipeline** | Deterministic spec → render → validate → repair pipeline |
| 🔍 | **Layout Verification** | Detect overlaps, arrow binding issues, spacing inconsistencies |
| 📏 | **Layout Helpers** | Positional utilities and `auto_labeled_rect` for auto-sizing |
| 💾 | **Dual Output** | `.excalidraw` (JSON) or `.excalidraw.md` (Obsidian) |

> \* AI icon generation requires a Gemini API key; YAML styles require PyYAML

---

### 🔧 How It Works

![Workflow](docs/images/workflow.png)

### 🖼️ Gallery

| Architecture | Charts | Icons |
|:---:|:---:|:---:|
| ![Architecture](docs/images/architecture.png) | ![Bar Chart](docs/images/bar-chart.png) | ![Icons](docs/images/icons.png) |
| ![Line Chart](docs/images/line-chart.png) | ![Bar Chart 2](docs/images/bar-chart-2.png) | |

### 📐 LaTeX Formula Rendering

LaTeX formulas rendered as PNG images with 4 font options. Simple math uses matplotlib mathtext; complex environments like `pmatrix` / `array` automatically fall back to system LaTeX + amsmath.

![Font Comparison](docs/images/font-comparison.png)

```python
from core.latex import formula

# Simple formula (renders via mathtext)
elements = formula(r"E = mc^2", x=100, y=50, font_size=20)

# Complex formula with matrix (falls back to usetex + amsmath)
elements = formula(r"\begin{pmatrix} a & b \\ c & d \end{pmatrix}", x=100, y=100, font_size=14)

# Change default font globally
import core.latex
core.latex.DEFAULT_FONTSET = "stix"  # or "cm", "dejavusans", "dejavuserif"

# Or per-formula
elements = formula(r"\alpha + \beta = \gamma", x=100, y=150, font_size=20, fontset="stix")
```

Supported mathtext syntax: fractions, integrals, sums, limits, Greek letters, square roots, subscripts/superscripts.

Unsupported by mathtext (auto-fallback to usetex): `\begin{pmatrix}`, `\begin{array}`, `\begin{cases}`, `\begin{smallmatrix}`.

Note: `usetex` mode requires a LaTeX installation (`pdflatex` + `amsmath` package) and ignores the `fontset` parameter.

### 🚀 Real-World Cases

| Sensor Data Pipeline | Decision Transformer | OpenClaw Architecture |
|:---:|:---:|:---:|
| ![Case 1](docs/images/case-sensor.png) | ![Case 2](docs/images/case-decision-transformer.png) | ![Case 3](docs/images/case-openclaw.png) |

---

## Prerequisites

### 1. Install Obsidian (Recommended)

[Obsidian](https://obsidian.md) is a free note-taking app with native Excalidraw support.

1. Download from https://obsidian.md/download
2. Create or open a Vault

### 2. Install Excalidraw Plugin

1. Open Obsidian → Settings → Community Plugins
2. Turn off Safe Mode (if still on)
3. Click Browse → search "Excalidraw"
4. Install **Excalidraw** by Zsolt Viczián
5. Enable the plugin

### 3. View Generated Diagrams

- Place `.excalidraw` files in your Vault directory
- Click to open and edit in Obsidian
- Or open at https://excalidraw.com

### Without Obsidian

`.excalidraw` files are standard JSON. You can also use:
- [excalidraw.com](https://excalidraw.com) — online editor
- VS Code Excalidraw extension
- Any tool that supports the Excalidraw format

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
| `auto_labeled_rect` | `auto_labeled_rect(x, y, label, padding=10, fs=20, min_width=0, min_height=0, **kwargs)` | `[rect, text]` |
| `text_standalone` | `text_standalone(cx, cy, txt, fs=20, color, font_family=5, roughness=0, text_align="center", max_width=None)` | `dict` |
| `arrow` | `arrow(x, y, dx=0, dy=0, *, x2=None, y2=None, stroke, sw, roughness)` | `dict` |
| `line` | `line(x, y, dx=0, dy=0, *, x2=None, y2=None, stroke, sw, roughness)` | `dict` |
| `numbered_circle` | `numbered_circle(cx, cy, num, fill, stroke)` | `[ellipse, text]` |
| `frame` | `frame(x, y, w, h, name="Frame", stroke, sw)` | `dict` |
| `group` | `group(elements)` | `list[dict]` |
| `bind_arrow` | `bind_arrow(arrow_el, start_el, end_el, gap=2, start_focus=None, end_focus=None)` | `dict` |
| `connect` | `connect(start_el, end_el, stroke, sw, roughness, gap=8, elbowed=False, start_focus=None, end_focus=None)` | `dict` |
| `image_embed` | `image_embed(x, y, w, h, base64_data, mime="image/png")` | `(element, files)` |

`text_standalone` supports `text_align` ("center", "left", "right") and `max_width` -- when set, the font size auto-shrinks until the text fits.
`bind_arrow()` and `connect()` infer edge focus from geometry by default so fan-in arrows do not collapse onto the center of wide targets.

---

## Layout Helpers

Positional utilities and auto-sizing:

```python
from core.engine import below, right_of, above, auto_labeled_rect

y2 = below(y=100, h=60, gap=15)    # y2 = 175
x2 = right_of(x=50, w=200, gap=10) # x2 = 260
y_above = above(y=100, gap=10)     # y_above = 90

# Auto-sized rectangle — width/height calculated from text
els = auto_labeled_rect(0, 0, "Hello World", padding=10, fs=16, min_width=120)
```

### Layout Verification

Check diagrams for overlaps, arrow binding issues, and spacing inconsistencies:

```python
from core.engine import check_overlaps, check_arrow_bindings, check_spacing, verify_layout

report = verify_layout(elements)
# {"status": "PASS"|"WARN"|"FAIL", "overlaps": [...], "arrow_issues": [...], "spacing_issues": [...], ...}

# Or check individually
overlaps = check_overlaps(elements)            # Detect overlapping shapes
arrow_issues = check_arrow_bindings(elements)  # Detect dead/unbound arrows
spacing = check_spacing(elements)              # Detect inconsistent gaps
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

| Preset | Font | Roughness | Fill Style | Border Radius | Use Case |
|--------|------|-----------|------------|---------------|----------|
| **Vivid** | Helvetica (2) | 0 | solid | no | Conference-safe, academic |
| **Clean** | Helvetica (2) | 0 | solid | no | Minimal, B&W, precise |
| **Sketch** | Virgil (1) | 1 | hachure | yes | Hand-drawn, casual |

```python
from styles import load_style, vivid_style, clean_style, sketch_style

style = load_style("vivid")
fill, stroke = style.get_color_pair("primary")  # ("#DCEAF6", "#2B5B84")
fill, stroke = style.get_color_pair("danger")    # ("#FADBD8", "#C0392B")

# Export style as machine-readable rules (used by the pipeline)
rules = style.to_style_rules()
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

## Diagram Pipeline

Deterministic pipeline: spec → normalize → validate → render → verify → repair → save.

```python
from core.pipeline import generate_diagram, save_generated_diagram

spec = {
    "diagram_type": "flow",
    "style": "conference",
    "nodes": [
        {"id": "input", "label": "Input", "role": "primary"},
        {"id": "process", "label": "Process", "role": "info"},
        {"id": "output", "label": "Output", "role": "accent"},
    ],
    "edges": [
        {"id": "e1", "from_id": "input", "to_id": "process", "label": "clean"},
        {"id": "e2", "from_id": "process", "to_id": "output"},
    ],
}

result = generate_diagram(spec)
# result.final_status == "PASS"
# result.elements → deterministic Excalidraw elements
# result.spec → normalized DiagramSpec

save_generated_diagram("diagram.excalidraw", result, artifact_dir="artifacts/")
```

Key pipeline features:
- **Deterministic output**: same spec always produces identical elements
- **Alias resolution**: `"flow"` → `"flowchart"`, `"box"` → `"rectangle"`, etc.
- **Auto-layout**: horizontal, vertical, or grid placement with grid snapping
- **Style contract validation**: checks font, roughness, border width, color palette, grid alignment
- **Topology validation**: verifies all nodes/edges are rendered, bindings are correct
- **Auto-repair**: re-renders from spec if style issues are detected

Supported `diagram_type` values: `flowchart`, `pipeline`, `architecture`, `system`, `comparison`, `concept-map`

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
├── docs/
│   └── images/                 # Screenshots & demo gallery
├── core/
│   ├── __init__.py
│   ├── engine.py               # Element builders, layout helpers, output
│   ├── icons.py                # 39 built-in icons
│   ├── charts.py               # Bar, horizontal bar, line, pie charts
│   ├── svg_converter.py        # SVG to Excalidraw conversion
│   ├── icon_library.py         # Persistent icon library & TF-IDF search
│   ├── ai_icons.py             # AI icon generation via Gemini API
│   ├── latex.py                # LaTeX formula rendering
│   ├── pipeline.py             # Deterministic diagram pipeline
│   └── scene.py                # Scene utilities: ID remapping, file collection
├── styles/
│   ├── __init__.py
│   ├── base.py                 # StyleConfig dataclass
│   ├── conference.py           # Vivid preset
│   ├── journal.py              # Clean preset
│   ├── ppt.py                  # Sketch preset
│   └── loader.py               # Style resolver + custom YAML
├── scripts/
│   ├── generate_diagram.py     # CLI diagram generator
│   ├── golden_rules.py         # Prompt engineering rules
│   ├── gen_world_model.py      # World model generator
│   └── run_ci.py               # CI test runner
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
│   ├── test_ai_icons.py
│   └── test_pipeline.py
├── .github/
│   └── workflows/
│       └── deploy.yml          # GitHub Pages deployment
└── examples/
    ├── generate_style_v3.py
    ├── generate_p1_demos.py
    ├── generate_p2_demos.py
    └── *.excalidraw            # Example outputs
```

---

## License

[MIT](LICENSE)

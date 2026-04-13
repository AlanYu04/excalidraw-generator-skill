---
name: excalidraw-generator
description: Generate Excalidraw diagrams from natural language descriptions. Creates flowcharts, charts, system architecture diagrams, and more with CJK support.
---

# Excalidraw Diagram Generator

Generate high-quality Excalidraw diagrams via Python script execution.

## When to Use

- User asks to "draw", "generate diagram", "create flowchart", "make architecture diagram"
- User wants visual illustrations for papers, slides, or documentation
- User mentions "excalidraw" or asks for diagram generation
- User wants bar charts, line charts, pie charts, data visualizations, or comparison tables
- User wants to convert SVG icons to Excalidraw elements
- User wants to save and reuse custom icons

## Step 0: Brainstorm

BEFORE asking any configuration questions, help the user clarify what they want to draw.

Ask these three questions **together in a single message**. Skip any question the user's original request already answers.

### Q1. What diagram do you want?

> "What diagram do you want? Describe your scenario and purpose."

Understand the domain, audience, and intent. Example: "K8s microservice architecture, for onboarding new engineers."

### Q2. Any reference files or data?

> "Any reference files or data? Provide file paths, or say 'none'."

If the user provides file paths, **read the files** before proposing a plan. Supported: CSV, JSON, images (PNG/JPG), existing `.excalidraw` files, screenshots, whiteboard photos.

### Q3. What key information and relationships?

> "What key information and relationships should the diagram show?"

Identify core elements, hierarchy, and connections. Example: "Pod -> Service -> Ingress three layers, plus monitoring sidecar."

### Propose a Plan

After collecting answers (and reading any files), output a structured diagram plan:

```
## Diagram Plan

**Type**: [flowchart / architecture / comparison table / timeline / bar chart / ...]
**Content**: [list main elements to include]
**Structure**: [hierarchy, groups, relationships between elements]
**Layout**: [top-down / left-right / radial / grid -- brief description]
**Data**: [how provided data/files integrate into the diagram, or "none"]

Confirm this plan? Or tell me what to adjust.
```

Only proceed to Step 1 once the user confirms the plan.

## HARD GATE

You MUST complete Step 0 (Brainstorm) and get user confirmation BEFORE asking the configuration questions below. Do NOT skip brainstorm.

## Step 1: Configuration Questions

Ask these questions one at a time:

### 1. Style Selection (content & color scheme)

Ask: "What style do you want?"

| Style | Content Level | Color Scheme | When to Use |
|-------|--------------|--------------|-------------|
| `vivid` | Rich -- numbered badges, sub-cards, annotations, grids | 7-color vibrant palette | When you want impressive, information-rich diagrams |
| `clean` | Minimal -- just boxes, arrows, labels | Black & white / grayscale | When you need clear, distraction-free data flow |
| `sketch` | Casual -- big cards, playful elements | Warm multi-color | When you want approachable, expressive diagrams |
| `custom` | User-defined from YAML file | User-defined | When you have specific visual requirements |

If the user selects `custom`, ask for the path to their style YAML file.

### 2. Fill Style

Ask: "What fill style?"

| Value | Effect | Look |
|-------|--------|------|
| `solid` | Solid color fill | Clean, modern |
| `hachure` | Diagonal line fill | Sketchy, hand-drawn |
| `cross-hatch` | Cross-hatched line fill | Technical, detailed |

### 3. Stroke Style

Ask: "What stroke style?"

| Value | Effect |
|-------|--------|
| `solid` | Solid continuous lines (default) |
| `dashed` | Dashed lines |
| `dotted` | Dotted lines |

### 4. Roughness

Ask: "What roughness level?"

| Value | Effect |
|-------|--------|
| `0` | Precise -- perfectly straight lines |
| `1` | Slight -- subtle hand-drawn wobble |
| `2` | Rough -- obvious hand-drawn feel |

### 5. Font

Ask: "What font?"

| Value | Font | Character |
|-------|------|-----------|
| `1` | Virgil | Handwritten, casual |
| `2` | Helvetica | Clean, professional |
| `3` | Cascadia | Monospace, code-like |

### 6. Output Format

Ask: "Output format?"

| Format | Description |
|--------|-------------|
| `.excalidraw` | Pure JSON, works with any Excalidraw-compatible tool |
| `.excalidraw.md` | Obsidian Excalidraw plugin format (markdown wrapper) |

### 7. Save Path

Ask where to save the generated file. Suggest a default path based on the user's current project.

## Step 2: Generate Diagram

Based on the user's description and selected style:

1. Read the appropriate style preset from `styles/` directory
2. Read relevant prompt guidelines from `prompts/` directory
3. Generate a Python script using the builder functions from `core/`
4. Execute the script to produce the output file

### Style Rules by Preset

#### Vivid Style Rules (content & color only)
- Full vibrant color palette: blue, teal, green, orange, purple, red
- Numbered circle badges for step indicators
- Sub-detail cards below main boxes
- Color-coded dimension grids and tables
- Highlight bars for key results
- Rich visual hierarchy: main boxes -> sub-cards -> annotations -> conclusion bars
- fontSize: 14-22pt (larger for readability)

#### Clean Style Rules (content & color only)
- Black & white only, grayscale-friendly
- Thin borders: 1pt solid lines
- Small text: 10pt body, 8pt labels
- NO decorative elements (no badges, no icons, no colored fills)
- Just boxes, arrows, and text labels
- Compact spacing

#### Sketch Style Rules (content & color only)
- Warm multi-color palette
- Big text: 18-28pt
- Wide spacing and generous padding
- Rounded corners on all rectangles
- Playful, approachable element layout

## Step 3: Core Builder Functions

These Python functions are available for diagram generation. Import them from the core engine:

```python
# === Shapes ===
rect(x, y, w, h, fill="transparent", stroke="#1e1e1e", sw=2, roughness=1, fill_style="solid", stroke_style="solid")
ellipse(x, y, w, h, fill="transparent", stroke="#1e1e1e", sw=2, roughness=1, fill_style="solid")
diamond(x, y, w, h, fill="transparent", stroke="#1e1e1e", sw=2, roughness=1, fill_style="solid")

# === Labeled Shapes (containerId binding -- auto-centers text) ===
labeled_rect(x, y, w, h, label, fill="transparent", stroke="#1e1e1e", sw=2, fs=16, label_color=None, roughness=1, font_family=3, fill_style="solid", stroke_style="solid")
labeled_ellipse(x, y, w, h, label, fill="transparent", stroke="#1e1e1e", sw=2, fs=16, label_color=None, roughness=1, font_family=3, fill_style="solid")
labeled_diamond(x, y, w, h, label, fill="transparent", stroke="#1e1e1e", sw=2, fs=16, label_color=None, roughness=1, font_family=3, fill_style="solid")

# === Text ===
text_standalone(cx, cy, txt, fs=20, color="#1e1e1e", font_family=3, roughness=0, text_align="center", max_width=None)
  # text_align: "center"(default) | "left" | "right"
  # max_width: if set, auto-shrink font size until text fits

# === Connectors ===
arrow(x, y, dx=0, dy=0, *, x2=None, y2=None, stroke="#1e1e1e", sw=2, roughness=1)
  # Relative: arrow(x, y, dx, dy)
  # Absolute: arrow(x, y, x2=end_x, y2=end_y)
line(x, y, dx=0, dy=0, *, x2=None, y2=None, stroke="#1e1e1e", sw=2, roughness=1)
  # Relative: line(x, y, dx, dy)
  # Absolute: line(x, y, x2=end_x, y2=end_y)
bind_arrow(arrow_el, start_el, end_el, gap=2)
connect(start_el, end_el, stroke="#1e1e1e", sw=2, roughness=1, gap=8)
  # Shorthand: creates + binds arrow between two elements automatically

# === Layout Helpers (prevent overlap) ===
below(y, h, gap=10)       # Safe y-coordinate below shape at (_, y) with height h
right_of(x, w, gap=10)    # Safe x-coordinate right of shape at (x, _) with width w
above(y, gap=10)          # Safe y-coordinate above shape whose top is at y

# === Structure ===
frame(x, y, w, h, name="Frame", stroke="#1e1e1e", sw=2)
group(elements)            # Returns new list with shared groupId

# === Charts ===
bar_chart(x, y, data, title=None, bar_color="#a5d8ff", bar_colors=None, axis_color="#495057", bar_width=60, max_height=200, gap=30, fs=14, label_fs=None, value_fs=None, title_fs=None, roughness=1, font_family=3, stroke_width=2, show_values=True, show_grid=False, grid_color="#dee2e6", grid_lines=5, axis_label=None)
horizontal_bar_chart(x, y, data, title=None, bar_color="#a5d8ff", bar_colors=None, axis_color="#495057", bar_height=40, max_width=250, gap=15, fs=14, label_fs=None, value_fs=None, title_fs=None, roughness=1, font_family=3, stroke_width=2, show_values=True)
line_chart(x, y, data, labels, title=None, series_colors=None, default_color="#1971c2", axis_color="#495057", chart_width=400, chart_height=200, fs=14, label_fs=None, value_fs=None, title_fs=None, roughness=1, font_family=3, stroke_width=2, show_points=True, show_values=False, show_grid=False, grid_color="#dee2e6", grid_lines=5, show_legend=True)
pie_chart(x, y, data, title=None, slice_colors=None, default_colors=None, axis_color="#495057", radius=100, fs=14, roughness=1, font_family=3, stroke_width=2, show_labels=True, show_percentages=True, show_legend=True, donut=False, donut_radius=50)

# === Icons (39 built-in) ===
icon(name, x=0, y=0, scale=1.0, stroke="#495057", sw=2, roughness=1)
list_icons()  # Returns sorted list of all 39 icon names

# === Icon Library (persistent, searchable) ===
save_icon(name, elements, description="", tags=None, source="custom", source_file=None)
load_icon(name, x=0, y=0, scale=1.0)
delete_icon(name)
list_library_icons()      # List all library icons with metadata
find_icons(query, limit=5, use_embeddings=False)
import_excalidrawlib(filepath, descriptions=None, tags_map=None, prefix="")

# === AI Icon Generation ===
configure(api_url, api_key, model="gemini-2.0-flash)  # from core.ai_icons
generate_icon(description, x=0, y=0, scale=1.0, stroke="#1e1e1e", sw=2, roughness=1, prompt=None)
generate_and_save(name, description, tags=None, **kwargs)

# === SVG Converter ===
svg_to_elements(svg_string, x=0, y=0, scale=1.0, stroke="#1e1e1e", stroke_width=2, roughness=1)
svg_file_to_elements(filepath, x=0, y=0, scale=1.0, stroke="#1e1e1e", stroke_width=2, roughness=1)

# === Other ===
numbered_circle(cx, cy, num, fill, stroke)
image_embed(x, y, w, h, base64_data, mime="image/png")

# === Output ===
save_excalidraw(filepath, elements, bg="#ffffff", files=None)
save_obsidian_md(filepath, elements, bg="#ffffff", files=None)
save(filepath, elements, bg="#ffffff", files=None)  # Auto-selects format by extension
```

### Text Centering

The engine uses `containerId` binding for auto-centering text in shapes. For standalone text, it uses CJK-aware width estimation:
- CJK characters: ~1.05x font size
- ASCII characters: ~0.62x font size
- Spaces: ~0.35x font size

Font families: `1` = Virgil (handwritten), `2` = Helvetica, `3` = Cascadia (monospace), `5` = CJK

For CJK text, always use `font_family=5` and apply the 1.05x width factor.

## Step 4: Common Diagram Patterns

### Flow Diagram (left-to-right)
```python
from core.engine import labeled_rect, arrow

for i, (label, color) in enumerate(items):
    x = start_x + i * (box_w + gap)
    elements += labeled_rect(x, y, box_w, box_h, label, fill=color)
    if i < len(items) - 1:
        elements.append(arrow(x + box_w + pad, y + box_h/2, gap - 2*pad, 0))
```

### Comparison Table
```python
from core.engine import labeled_rect, below

x = start_x
for row_data in rows:
    for col_data, col_width in zip(row_data, col_widths):
        elements += labeled_rect(x, y, col_width, row_h, col_data)
        x += col_width
    y = below(y, row_h)
```

### Decision Flow (vertical)
```python
from core.engine import labeled_ellipse, labeled_diamond, labeled_rect, arrow, bind_arrow

start = labeled_ellipse(x, y, 100, 50, "Start", fill="#d0f0c0")
step1 = labeled_rect(x, y + 100, 200, 60, "Input")
dec   = labeled_diamond(x, y + 200, 160, 100, "Valid?")
yes   = labeled_rect(x, y + 340, 200, 60, "Success", fill="#d0f0c0")
no    = labeled_rect(x + 240, y + 220, 160, 60, "Error", fill="#ffc9c9")

a1 = bind_arrow(arrow(x+50, y+50, 0, 50), start[0], step1[0])
a2 = bind_arrow(arrow(x+100, y+160, 0, 40), step1[0], dec[0])
a3 = bind_arrow(arrow(x+80, y+300, 0, 40), dec[0], yes[0])
a4 = bind_arrow(arrow(x+160, y+250, 80, 0), dec[0], no[0])
elements = [*start, *step1, *dec, *yes, *no, a1, a2, a3, a4]
```

### Bar Chart
```python
from core.charts import bar_chart

elements = bar_chart(
    x=50, y=100,
    data={"React": 85, "Vue": 72, "Angular": 58, "Svelte": 45},
    title="Framework Popularity",
    bar_color="#a5d8ff",
    show_values=True,
    roughness=1,
)
```

### Line Chart (multi-series with grid)
```python
from core.charts import line_chart

elements = line_chart(
    x=50, y=100,
    data={
        "Revenue": [120, 150, 180, 210, 250],
        "Costs":   [100, 110, 130, 140, 160],
    },
    labels=["Q1", "Q2", "Q3", "Q4", "Q5"],
    title="Revenue vs Costs",
    series_colors={"Revenue": "#1971c2", "Costs": "#e03131"},
    show_points=True,
    show_grid=True,
    grid_lines=4,
    show_legend=True,
    chart_width=500,
    chart_height=250,
)
```

### Pie Chart (with donut mode)
```python
from core.charts import pie_chart

elements = pie_chart(
    x=50, y=100,
    data={"Desktop": 55, "Mobile": 30, "Tablet": 15},
    title="Traffic Sources",
    donut=True,
    donut_radius=50,
    show_percentages=True,
    radius=120,
)
```

### Layout Helper Usage (prevent overlap)
```python
from core.engine import labeled_rect, text_standalone, below, right_of

# Place first shape
box1 = labeled_rect(100, 100, 200, 60, "Step 1")
elements += box1

# Text below box1, guaranteed not to overlap
label_y = below(100, 60, gap=15)  # = 175
elements.append(text_standalone(200, label_y, "Description text"))

# Second box to the right of box1
box2_x = right_of(100, 200, gap=30)  # = 330
box2 = labeled_rect(box2_x, 100, 200, 60, "Step 2")
elements += box2
```

### SVG Icon Conversion
```python
from core.svg_converter import svg_to_elements

svg = '<svg viewBox="0 0 24 24"><path d="M12 2L2 22h20Z"/></svg>'
elements = svg_to_elements(svg, x=100, y=50, scale=1.0, stroke="#1e1e1e")
```

### Icon Library Search
```python
from core.icon_library import save_icon, load_icon, find_icons

# Save custom icon with description
save_icon("my-server", elements, description="Server rack with LEDs", tags=["server", "hardware"])

# Search for icon by description
results = find_icons("server hardware infrastructure")
best = results[0]

# Load and place the icon
server_elements = load_icon(best["name"], x=200, y=100, scale=1.0)
```

## 39 Built-in Icons

Use `icon(name, x, y, scale, stroke, sw, roughness)` to place built-in icons.

### General Purpose
| Name | Description |
|------|-------------|
| `database` | Database cylinder |
| `user` | Person silhouette |
| `cloud` | Cloud shape |
| `server` | Server rack |
| `gear` | Gear/cog settings |
| `document` | Document with folded corner |
| `shield` | Security shield |
| `arrow-right` | Right-pointing arrow |
| `check` | Checkmark |
| `warning` | Warning triangle with exclamation |
| `lock` | Padlock |
| `wifi` | WiFi signal |
| `heart` | Heart shape |
| `star` | 5-point star |
| `lightning` | Lightning bolt |
| `clock` | Clock face |
| `magnifier` | Magnifying glass |
| `fire` | Flame |
| `globe` | Globe with meridian |
| `chat` | Chat bubble |
| `api` | API angle brackets |
| `terminal` | Terminal/console |
| `folder` | Folder |
| `key` | Key |
| `cube` | 3D cube |

### ML / AI
| Name | Description |
|------|-------------|
| `transformer-block` | Multi-head attention + feed-forward block |
| `attention-head` | Q, K, V converging arrows |
| `embedding-layer` | Embedding matrix grid |
| `feedforward` | Two-layer FFN |
| `encoder` | Encoder block with E marker |
| `decoder` | Decoder block with D marker |
| `loss-function` | Descending loss curve |
| `optimizer` | Gradient descent spiral |
| `gpu` | Chip/GPU with pins |
| `robot` | Robot head with antenna |
| `brain` | Brain outline |
| `neural-net` | 3-layer neural network |
| `data-pipeline` | Funnel/pipeline shape |
| `matrix` | Grid matrix 4x3 |

## SVG-to-Excalidraw Converter

Convert any SVG to Excalidraw elements. Supports:
- **Path commands**: M, L, H, V, C, S, Q, T, A, Z (absolute & relative)
- **SVG elements**: `<path>`, `<rect>`, `<circle>`, `<ellipse>`, `<line>`, `<polygon>`, `<polyline>`, `<use>`, `<defs>`
- **Shape classification**: Circles -> `ellipse`, rectangles -> `rectangle`, curves -> `line`
- **Bezier tessellation**: Cubic, quadratic, and arc curves sampled to polylines
- **RDP simplification**: Reduces point count while preserving visual fidelity
- **Gradient resolution**: Resolves `url(#id)` fill references to concrete colors
- **Transform support**: `translate()`, `scale()`, `rotate()`, `matrix()`

## Charts

Hand-drawn style charts built from Excalidraw primitives:
- **Vertical** (`bar_chart`): Bars going up from x-axis, optional grid lines and Y-axis labels
- **Horizontal** (`horizontal_bar_chart`): Bars extending right from y-axis
- **Line** (`line_chart`): Multi-series with point markers, grid, and legend
- **Pie** (`pie_chart`): With optional donut mode, labels, and percentages
- All charts support CJK text labels, custom colors per category/series, and value annotations

## Styles

### Preset Summary

| Preset | Colors | Text Size | Border Width | Gap | Roughness |
|--------|--------|-----------|--------------|-----|-----------|
| `vivid` | 7-color vibrant palette | 14-22pt | 2 | 45 | 1 |
| `clean` | Grayscale only | 8-14pt | 1 | 30 | 1 |
| `sketch` | Warm multi-color | 14-28pt | 2 | 55 | 1 |

### Aliases

- `conference` -> `vivid`
- `journal` -> `clean`
- `ppt` -> `sketch`

### StyleConfig.get_color_pair(role)

Returns `(fill, stroke)` tuple for a semantic role. Roles: `primary`, `accent`, `success`, `warning`, `danger`, `info`, `neutral`.

```python
from styles import load_style
style = load_style("vivid")
fill, stroke = style.get_color_pair("success")  # ("#b2f2bb", "#2f9e44")
```

### list_styles()

Returns all available style names (built-in + custom YAML files from `~/.excalidraw-gen/styles/`).

### Custom Style YAML Format

Users can define custom styles at `~/.excalidraw-gen/styles/*.yaml`:

```yaml
name: "My Custom Style"
description: "Description of this style"
colors:
  background: "#FFFFFF"
  primary: "#4A90E2"
  accent: "#E67E22"
  text: "#1e1e1e"
  border: "#333333"
  muted: "#999999"
typography:
  font_family: 2        # 1=Virgil(handwritten) 2=Helvetica 3=Cascadia
  title_size: 24
  body_size: 14
  label_size: 11
layout:
  roughness: 0          # 0=precise 1=slight 2=rough
  border_width: 2
  border_radius: true
  arrow_width: 2
  default_gap: 50
```

## Persistent Icon Library & Search

Save custom icons to `~/.excalidraw-gen/icons/` for reuse across diagrams:

- **save_icon**: Save elements with description and tags; auto-generates OpenAI embeddings if API key available
- **load_icon**: Load and reposition with fresh IDs and optional scale
- **find_icons**: TF-IDF vector search (zero-dependency, works offline); optional OpenAI embedding-based semantic search
- **import_excalidrawlib**: Bulk import from `.excalidrawlib` files

## AI Icon Generation

Generate icons via Gemini API:

```python
from core.ai_icons import configure, generate_icon, generate_and_save

configure(api_url="https://generativelanguage.googleapis.com/v1beta", api_key="YOUR_KEY")
elements = generate_icon("a database server rack", x=100, y=50, scale=1.5)
```

Falls back to PNG (image_embed) if SVG generation fails. Config stored at `~/.excalidraw-gen/config.json`.

## File Paths

- Skill directory: `~/.claude/skills/excalidraw-generator/`
- Core engine: `~/.claude/skills/excalidraw-generator/core/engine.py`
- Charts: `~/.claude/skills/excalidraw-generator/core/charts.py`
- Built-in icons: `~/.claude/skills/excalidraw-generator/core/icons.py`
- SVG converter: `~/.claude/skills/excalidraw-generator/core/svg_converter.py`
- AI icons: `~/.claude/skills/excalidraw-generator/core/ai_icons.py`
- Icon library: `~/.claude/skills/excalidraw-generator/core/icon_library.py`
- Style presets: `~/.claude/skills/excalidraw-generator/styles/`
- Style base: `~/.claude/skills/excalidraw-generator/styles/base.py`
- Style loader: `~/.claude/skills/excalidraw-generator/styles/loader.py`
- Prompt guidelines: `~/.claude/skills/excalidraw-generator/prompts/`
- Custom user styles: `~/.excalidraw-gen/styles/`
- User icon library: `~/.excalidraw-gen/icons/`

## Important Rules

- ALWAYS use `labeled_*` functions for text inside shapes (rect, ellipse, diamond). They use `containerId` binding for auto-centering.
- Use `text_standalone` for labels, annotations, and text outside shapes.
- Use `below()` / `right_of()` / `above()` layout helpers to prevent text and shape overlap.
- Use `max_width` parameter in `text_standalone` when placing text inside frames to auto-shrink.
- Font family `5` is for CJK text. Use `1.05 * fs` as width factor for CJK chars vs `0.62 * fs` for ASCII.
- The `save()` function auto-selects format: `.excalidraw.md` -> Obsidian, `.excalidraw` -> pure JSON.
- `bind_arrow` modifies `start_el` and `end_el` in-place (adds boundElements references).
- `connect()` is a shorthand that creates an arrow and binds it in one call.
- `group()` returns a new element list with shared groupId (does not modify originals).

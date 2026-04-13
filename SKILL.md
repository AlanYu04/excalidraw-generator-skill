---
name: excalidraw-generator
description: Generate Excalidraw diagrams via Python. Use when user wants to draw diagrams, flowcharts, architecture diagrams, system diagrams, comparison tables, timelines, bar charts, or any visual illustration. Supports 3 style presets (Vivid/Clean/Sketch) + custom user styles. Outputs .excalidraw or .excalidraw.md for Obsidian. Includes SVG-to-Excalidraw converter, hand-drawn bar charts, persistent icon library with vector search.
---

# Excalidraw Diagram Generator

Generate high-quality Excalidraw diagrams via Python script execution.

## When to Use

- User asks to "draw", "generate diagram", "create flowchart", "make architecture diagram"
- User wants visual illustrations for papers, slides, or documentation
- User mentions "excalidraw" or asks for diagram generation
- User wants bar charts, data visualizations, or comparison tables
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

Identify core elements, hierarchy, and connections. Example: "Pod → Service → Ingress three layers, plus monitoring sidecar."

### Propose a Plan

After collecting answers (and reading any files), output a structured diagram plan:

```
## Diagram Plan

**Type**: [flowchart / architecture / comparison table / timeline / bar chart / ...]
**Content**: [list main elements to include]
**Structure**: [hierarchy, groups, relationships between elements]
**Layout**: [top-down / left-right / radial / grid — brief description]
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
| `vivid` | Rich — numbered badges, sub-cards, annotations, grids | 7-color vibrant palette | When you want impressive, information-rich diagrams |
| `clean` | Minimal — just boxes, arrows, labels | Black & white / grayscale | When you need clear, distraction-free data flow |
| `sketch` | Casual — big cards, playful elements | Warm multi-color | When you want approachable, expressive diagrams |
| `custom` | User-defined from YAML file | User-defined | When you have specific visual requirements |

If the user selects `custom`, ask for the path to their style YAML file.

### 2. Fill Style

Ask: "What fill style?"

| Value | Effect | Look |
|-------|--------|------|
| `solid` | Solid color fill | Clean, modern |
| `hachure` | Diagonal line fill | Sketchy, hand-drawn |
| `cross-hatch` | Cross-hatched line fill | Technical, detailed |

### 3. Roughness

Ask: "What roughness level?"

| Value | Effect |
|-------|--------|
| `0` | Precise — perfectly straight lines |
| `1` | Slight — subtle hand-drawn wobble |
| `2` | Rough — obvious hand-drawn feel |

### 4. Font

Ask: "What font?"

| Value | Font | Character |
|-------|------|-----------|
| `1` | Virgil | Handwritten, casual |
| `2` | Helvetica | Clean, professional |
| `3` | Cascadia | Monospace, code-like |

### 5. Output Format

Ask: "Output format?"

| Format | Description |
|--------|-------------|
| `.excalidraw` | Pure JSON, works with any Excalidraw-compatible tool |
| `.excalidraw.md` | Obsidian Excalidraw plugin format (markdown wrapper) |

### 6. Save Path

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
- Rich visual hierarchy: main boxes → sub-cards → annotations → conclusion bars
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
# Element builders
rect(x, y, w, h, fill, stroke, sw)
labeled_rect(x, y, w, h, label, fill, stroke, sw, fs)  # rect + auto-centered text via containerId
labeled_diamond(x, y, w, h, label, fill, stroke, sw)    # diamond decision node with text
labeled_ellipse(x, y, w, h, label, fill, stroke, sw)    # ellipse/circle with text
text_standalone(cx, cy, txt, fs, color)                   # standalone centered text
arrow(x, y, dx, dy, stroke, sw)                           # arrow with arrowhead
ellipse(x, y, w, h, fill, stroke, sw)                     # circle/ellipse
diamond(x, y, w, h, fill, stroke, sw)                     # diamond shape
line(x, y, dx, dy, stroke, sw)                             # line segment
group(elements)                                            # group elements (shared groupIds)
frame(x, y, w, h, name)                                   # frame / named region
image_embed(x, y, w, h, base64_data, mime)                # embedded image
bind_arrow(arrow_el, start_el, end_el, gap)               # bind arrow to elements
numbered_circle(cx, cy, num, fill, stroke)                # numbered badge

# Icon library (10 built-in icons)
icon(name, x, y, scale, stroke, sw, roughness)            # built-in icon
list_icons()                                               # list all available icons

# SVG converter
svg_to_elements(svg_string, x, y, scale, stroke, sw, roughness)    # SVG string → Excalidraw
svg_file_to_elements(filepath, x, y, scale, stroke, sw, roughness) # SVG file → Excalidraw

# Charts
bar_chart(x, y, data, title, bar_color, ...)              # vertical bar chart
horizontal_bar_chart(x, y, data, title, bar_color, ...)   # horizontal bar chart

# Icon library (persistent, searchable)
save_icon(name, elements, description, tags, source)       # save to library
load_icon(name, x, y, scale)                               # load from library
delete_icon(name)                                          # delete from library
list_library_icons()                                       # list all library icons
find_icons(query, limit, use_embeddings)                   # search by description

# Output
save_excalidraw(filepath, elements, bg, files)  # save as .excalidraw JSON
save_obsidian_md(filepath, elements, bg, files) # save as .excalidraw.md
```

### Text Centering

The engine uses `containerId` binding for auto-centering text in shapes. For standalone text, it uses CJK-aware width estimation:
- CJK characters: ~1.05x font size
- ASCII characters: ~0.62x font size
- Spaces: ~0.35x font size

## Step 4: Common Diagram Patterns

### Flow Diagram (left-to-right)
```python
for i, (label, color) in enumerate(items):
    x = start_x + i * (box_w + gap)
    elements += labeled_rect(x, y, box_w, box_h, label, fill=color)
    if i < len(items) - 1:
        elements.append(arrow(x + box_w + pad, y + box_h/2, gap - 2*pad, 0))
```

### Comparison Table
```python
for row_data in rows:
    for col_data, col_width in zip(row_data, col_widths):
        elements += labeled_rect(x, y, col_width, row_h, col_data)
        x += col_width
    y += row_h + gap
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

### SVG Icon Conversion
```python
from core.svg_converter import svg_to_elements

svg = '<svg viewBox="0 0 24 24"><path d="M12 2L2 22h20Z"/></svg>'
elements = svg_to_elements(svg, x=100, y=50, scale=1.0, stroke="#1e1e1e")
```

### Icon Library Workflow
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

## Custom Style YAML Format

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

## File Paths

- Skill directory: `~/.claude/skills/excalidraw-generator/`
- Core engine: `~/.claude/skills/excalidraw-generator/core/`
- Icon library: `~/.claude/skills/excalidraw-generator/core/icons.py`
- SVG converter: `~/.claude/skills/excalidraw-generator/core/svg_converter.py`
- Chart builder: `~/.claude/skills/excalidraw-generator/core/charts.py`
- Persistent icon library: `~/.claude/skills/excalidraw-generator/core/icon_library.py`
- Style presets: `~/.claude/skills/excalidraw-generator/styles/`
- Prompt guidelines: `~/.claude/skills/excalidraw-generator/prompts/`
- Custom user styles: `~/.excalidraw-gen/styles/`
- User icon library: `~/.excalidraw-gen/icons/`

## Icon Library

Use `icon(name, x, y, scale, stroke, sw, roughness)` to place built-in icons. Available icons:

| Icon | Name | Description |
|------|------|-------------|
| Database cylinder | `database` | Data storage, DB instances |
| Person silhouette | `user` | Users, actors, personas |
| Cloud shape | `cloud` | Cloud services, internet |
| Server rack | `server` | Servers, hosting |
| Gear/cog | `gear` | Settings, configuration |
| Document | `document` | Files, documents, pages |
| Shield | `shield` | Security, protection |
| Right arrow | `arrow-right` | Direction, flow |
| Checkmark | `check` | Approval, completion |
| Warning triangle | `warning` | Alerts, caution |

## SVG-to-Excalidraw Converter

Convert any SVG to Excalidraw elements. Supports:
- **Path commands**: M, L, H, V, C, S, Q, T, A, Z (absolute & relative)
- **SVG elements**: `<path>`, `<rect>`, `<circle>`, `<ellipse>`, `<line>`, `<polygon>`, `<polyline>`
- **Shape classification**: Circles → `ellipse`, rectangles → `rectangle`, curves → `line`
- **Bezier tessellation**: Cubic, quadratic, and arc curves sampled to polylines
- **RDP simplification**: Reduces point count while preserving visual fidelity

## Bar Charts

Hand-drawn style bar charts built from Excalidraw primitives:
- **Vertical** (`bar_chart`): Bars going up from x-axis
- **Horizontal** (`horizontal_bar_chart`): Bars extending right from y-axis
- Supports custom colors per bar, value labels, grid lines, CJK text
- `bar_colors` parameter for per-category color overrides

## Persistent Icon Library & Search

Save custom icons to `~/.excalidraw-gen/icons/` for reuse across diagrams:

- **save_icon**: Save elements with description and tags
- **load_icon**: Load and reposition with fresh IDs
- **find_icons**: TF-IDF vector search (zero-dependency, works offline)
- **Optional embedding search**: Set `OPENAI_API_KEY` for semantic search via OpenAI

---
name: excalidraw-generator
description: Generate Excalidraw diagrams via Python. Use when user wants to draw diagrams, flowcharts, architecture diagrams, system diagrams, comparison tables, timelines, or any visual illustration. Supports 3 style presets (Vivid/Clean/Sketch) + custom user styles. Outputs .excalidraw or .excalidraw.md for Obsidian.
---

# Excalidraw Diagram Generator

Generate high-quality Excalidraw diagrams via Python script execution.

## When to Use

- User asks to "draw", "generate diagram", "create flowchart", "make architecture diagram"
- User wants visual illustrations for papers, slides, or documentation
- User mentions "excalidraw" or asks for diagram generation

## HARD GATE

You MUST ask the user the following configuration questions BEFORE generating any code. Do NOT skip these.

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
text_standalone(cx, cy, txt, fs, color)                   # standalone centered text
arrow(x, y, dx, dy, stroke, sw)                           # arrow with arrowhead
ellipse(x, y, w, h, fill, stroke, sw)                     # circle/ellipse
diamond(x, y, w, h, fill, stroke, sw)                     # diamond shape
line(x, y, dx, dy, stroke, sw)                             # line segment
numbered_circle(cx, cy, num, fill, stroke)                # numbered badge

# Output
save_excalidraw(filepath, elements)          # save as .excalidraw JSON
save_obsidian_md(filepath, elements)         # save as .excalidraw.md
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

### Closed Loop
```python
# 4-5 nodes in a rectangle, arrows connecting clockwise
```

### Timeline
```python
# Horizontal line + milestone cards above + reference labels below
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
- Style presets: `~/.claude/skills/excalidraw-generator/styles/`
- Prompt guidelines: `~/.claude/skills/excalidraw-generator/prompts/`
- Custom user styles: `~/.excalidraw-gen/styles/`

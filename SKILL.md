---
name: excalidraw-generator
description: Use when user asks to draw, create, or generate diagrams, flowcharts, charts, architecture diagrams, wireframes, or visual illustrations. TRIGGER on "draw", "diagram", "flowchart", "chart", "pie chart", "bar chart", "line chart", "architecture diagram", "excalidraw", "visual", "wireframe", "comparison table", "画图", "流程图", "图表", "架构图", "示意图", "生成图", "做个图".
---

# Excalidraw Diagram Generator

Generate high-quality Excalidraw diagrams via Python script execution using core/ builders.

## When to Use

- User asks to "draw", "generate diagram", "create flowchart", "make architecture diagram"
- User wants visual illustrations for papers, slides, or documentation
- User mentions "excalidraw" or asks for diagram generation
- User wants bar charts, line charts, pie charts, data visualizations, or comparison tables
- User wants to convert SVG icons to Excalidraw elements
- User wants to save and reuse custom icons

---

## Step 0: Quick Intent Capture

### Clear requests (skip questions)

If the user's request is specific enough (e.g., "画一个 3 步流程图 A->B->C", "draw a CI/CD pipeline with 4 stages"), skip detailed questions and output:

```
Got it: [diagram type] | ~[N] elements | Style: [vivid/clean/sketch or default]
Saving to: [suggested path]
```

Then proceed directly to **HARD GATE**.

### Vague requests (ask 3 questions)

If the user's request is vague (e.g., "画个架构图", "make a diagram"), ask these 3 questions **together in a single message**:

1. **"What diagram?"** — Describe the scenario, audience, and purpose.
2. **"Any reference files?"** — Provide file paths or say "none". Supported: CSV, JSON, images, `.excalidraw` files, screenshots.
3. **"Key elements and relationships?"** — What should the diagram show?

If the user provides reference files, **read them** before continuing.

### Output before proceeding

```
Intent confirmed: [diagram type] | [element count] elements | Style: [style]
```

---

## Step 1: Configuration (Condensed)

**Skip entirely if the user already specified these in their request.** Otherwise ask at most 3 questions:

1. **"Style? (vivid/clean/sketch or describe)"**
2. **"Output format? (.excalidraw or .excalidraw.md)"**
3. **"Save path?"** (suggest based on current project — MUST confirm before generating)

### Style Reference

| Style | Colors | Text Size | Gap | Use When |
|-------|--------|-----------|-----|----------|
| `vivid` (alias: `conference`) | 7-color vibrant palette | 14-22pt | 45px | Impressive, information-rich diagrams |
| `clean` (alias: `journal`) | Grayscale only | 8-14pt | 30px | Clear, distraction-free data flow |
| `sketch` (alias: `ppt`) | Warm multi-color | 14-28pt | 55px | Approachable, expressive diagrams |
| `custom` | User-defined from YAML | — | — | Specific visual requirements |

---

## HARD GATE: Read Style Prompt (MANDATORY — Before Writing Any Code)

STOP. You MUST execute these steps IN ORDER. Skipping any step = immediate failure.

### Steps (ALL required — no exceptions)

1. **Use the Read tool** to read `prompts/[style]-prompt.md` (the file for the user's chosen style).
   - If style is not yet chosen, read `prompts/conference-prompt.md` as default.
   - You MUST make a Read tool call — reading from memory or skipping is NOT acceptable.
2. **Output this confirmation to the user** (not silently):
   ```
   > PROMPT CHECK: [style] style loaded.
   > 1. [specific rule from the file you just read]
   > 2. [specific rule from the file you just read]
   > 3. [specific rule from the file you just read]
   ```
   The rules must be QUOTED from the actual file, not paraphrased from memory.

### Bypass Detection

If no Read tool call appears in the conversation before code generation, the HARD GATE was bypassed.
The user can verify this by checking the tool call history.

### Prompt Rules Summary

#### Conference / Vivid Style

- **Grid alignment**: All elements snap to 20px invisible grid
- **Orthographic arrows**: Only 90-degree angles, no diagonal arrows
- **No wasted space**: Compact layout, minimal padding
- **Colors**: Academic blue `#2B5B84`-`#4A90E2`, coral `#E67E22` only for key findings
- **Font**: Helvetica (`fontFamily: 2`), title 20pt, body 12pt, labels 10pt
- **Shapes**: No border radius, `roughness: 0`, borders 1.5pt solid
- **Arrows**: Straight only, 1.5pt, no curved/elbowed arrows

#### Journal / Clean Style

- **Ultra-compact**: Minimum margins, tight spacing
- **Colorblind-safe**: Okabe-Ito palette (Blue `#0072B2`, Orange `#E69F00`, Green `#009E73`, Red `#D55E00`)
- **Font**: Helvetica/Arial (`fontFamily: 2`), title 16pt, body 10pt, labels 8pt
- **Minimum legible text**: 7pt at print scale
- **Shapes**: All borders 0.5-1pt solid, `roughness: 0`, no rounded corners

#### PPT / Sketch Style

- **Generous spacing**: 50px+ gaps between major elements
- **Vibrant colors**: Blue `#1971c2`, Teal `#0c8599`, Orange `#e8590c`, etc.
- **Font**: Any or Virgil (`fontFamily: 1`) for handwritten feel, title 28pt, body 16pt
- **Shapes**: Rounded corners, `roughness: 1`, borders 2pt
- **Arrows**: 2pt, color by semantic role, labels encouraged

---

## Step 2: Generate Diagram

### 2A. Generation Method

There is ONE method: **Python script via `core/` builders.**

- Use `auto_labeled_rect()`, `connect()`, `below()`, `right_of()` for ALL elements and arrows.
- Do NOT write raw `.excalidraw` JSON by hand.
- Do NOT create custom arrow/line helper functions (e.g., `ortho_arrow()`, `bound_ortho_arrow()`).
- If a builder function is missing what you need, extend `core/engine.py` first — then use it.

Why: Builder functions enforce grid alignment, auto-compute arrow bindings, and prevent the overlap/patch-hell cycle that comes from hand-positioned coordinates.

### 2B. Layout Design (MANDATORY OUTPUT — Show to User Before Coding)

STOP. You MUST output a layout table to the user BEFORE writing ANY code.
If you write code before showing this table, you have FAILED this step.

Output this exact format:

> ## Layout Plan: [Diagram Name]
>
> ### Elements
> | ID | Label | Type | X | Y | Size |
> |----|-------|------|---|---|------|
> | b1 | "Input" | rect | 100 | 100 | auto |
> | b2 | "Process" | rect | r_of(b1) | 100 | auto |
> | d1 | "Valid?" | diam | mid_x | below(b2) | 120x80 |
>
> ### Connections
> | From | To | Direction | Label |
> |------|----|-----------|-------|
> | b1 | b2 | right | |
> | b2 | d1 | down | |

**Mandatory rules for the layout table:**
- X and Y coordinates MUST be multiples of 20 (grid snap to invisible 20px grid)
- Every element MUST use `auto_labeled_rect()` — no hardcoded dimensions
- Every arrow MUST use `connect()` — no custom arrow functions
- Use `right_of()`, `below()`, `above()` for relative positioning between elements
- Verify no bounding boxes overlap before proceeding to code
- For CJK text: `font_family=5`, width factor 1.05x

### 2B.5 Formula Detection (Auto)

Scan the diagram content for mathematical expressions and decide rendering method:

**Use `formula()` when the content contains ANY of:**
- LaTeX math syntax: `\alpha`, `\beta`, `\sum`, `\prod`, `\frac{a}{b}`, `\int`, `\nabla`, `\partial`
- Subscripts/superscripts beyond plain text capability: `x_1`, `a^2`, `\hat{y}`, `\bar{x}`
- Equations: `E=mc^2`, `\hat{y} = f(x)`, `\mathcal{L}(\theta)`
- Matrix/env notation: `\begin{pmatrix}`, `\begin{bmatrix}`
- Greek letters used as variables: `\lambda`, `\theta`, `\omega`
- Operators/symbols: `\times`, `\div`, `\leq`, `\geq`, `\approx`, `\infty`

**Use `text_standalone()` when:**
- Plain text, Chinese/English labels, names — no math symbols
- Simple notation that renders fine in regular font (e.g., "v1.0", "Step 1", "A → B")

**Mixed content:**
- Render math portions with `formula()`, plain text portions with `text_standalone()`
- Example: a node labeled "Loss: $\mathcal{L}(\theta)$" → use `formula()` for the whole label

**In the layout table (Step 2B), mark formula elements with `type: formula`:**
```
| f1 | "E=mc^2" | formula | 200 | 300 | auto |
```

### 2C. Generate

1. Follow the layout table from Step 2B — translate each row into code using builder functions
2. Use `auto_labeled_rect()`, `connect()`, `below()`, `right_of()` exclusively
3. Execute the script to produce the output file

### 2D. Verify output follows ALL style prompt rules

After generating, cross-check against the style prompt you read in HARD GATE:
- [ ] Colors match the style palette
- [ ] Font family and sizes match style rules
- [ ] Arrow style matches (straight/curved, width)
- [ ] Roughness and border width match
- [ ] No rule from the style prompt is violated
- [ ] No custom arrow/line functions were used (only `connect()` or `bind_arrow()`)

If any rule is violated, **go back to Step 2B and regenerate** — do not patch.

---

## Step 2.5: Verification Gate (MANDATORY — Before Delivery)

After generating the diagram file, run verification **before** telling the user it's done.
This step is NOT optional. You MUST execute the verification code and report the result.

### Verification Steps

1. Read the generated `.excalidraw` JSON file
2. Run verification using the Bash tool (not just in-memory — execute it):
   ```bash
   cd ~/.claude/skills/excalidraw-generator && python3 -c "
   import json
   from core.engine import verify_layout
   with open('[path-to-file]') as f:
     data = json.load(f)
   report = verify_layout(data['elements'])
   print(json.dumps(report, indent=2, default=str))
   "
   ```
3. Check `report['status']`:

**If FAIL** (has ERROR-level issues):
   - DO NOT deliver to user yet
   - Go back to **Step 2B** — redesign the layout table with corrected positions
   - Regenerate from the new layout (NOT patch the old code)
   - Re-verify (up to **2 redesign attempts**)
   - If still FAIL after 2 redesigns: deliver with explicit FAIL notice in Step 3

**If WARN** (only WARNING-level issues):
   - Note the warnings in your output
   - Proceed to Step 3

**If PASS**:
   - Proceed to Step 3 immediately

### What to Fix Automatically
- Overlapping elements → increase gap between them
- Arrow without binding → add `startBinding`/`endBinding` or use `connect()`
- Arrow endpoint inside element → for unbound arrows, extend/shorten to edge
- Inconsistent spacing → normalize gaps
- Fan-in / fan-out collapsed to one center point → distribute `start_focus` / `end_focus` and regenerate

### What NOT to Fix Automatically (leave for user)
- Color choices
- Font sizes (unless text overflow detected)
- Visual balance (subjective)

### Verification Output
```
Layout verification: [PASS/WARN/FAIL]
  Elements: [N] shapes, [M] arrows
  Overlaps: [count] ([details if any])
  Arrow issues: [count] ([details if any])
  Spacing issues: [count] ([details if any])
```

---

## Step 3: Deliver

Present the result:

```
Diagram generated: [path]
Please open in Obsidian to review.

Verification: [PASS/WARN/FAIL] — [summary]
```

If WARN or FAIL, briefly mention what was detected and whether auto-fix was attempted.

---

## Phase 4: Vision Review (User Feedback Loop)

### Trigger

User sends a screenshot OR provides a screenshot file path after viewing the diagram in Obsidian.

### How to Receive Screenshots

- Drag-and-drop image into Claude Code conversation
- Or provide file path: "Look at ~/Screenshots/xxx.png"
- Or say "check the diagram" with the file open

### Claude Vision Analysis

When the user provides a screenshot, analyze it for these issues:

**Critical Issues (always fix):**
1. Any text is overlapping or unreadable
2. Any arrows pointing in the wrong direction
3. Any elements completely overlapping
4. Any arrows not connecting to the right elements
5. Topology is wrong (wrong flow, missing connections, extra connections)

**Visual Quality Issues (fix if obvious):**
6. Elements significantly off-center or unbalanced
7. Inconsistent spacing between elements
8. Arrows crossing through other elements unnecessarily
9. Color coding inconsistent with style guide
10. Elements too small to read labels

### Analysis Output Format

```
## Vision Review

### Critical Issues
1. **[Element/Issue]**: [problem] — [fix suggestion]

### Visual Quality Issues
2. **[Issue]**: [fix suggestion]

### Recommended Actions
1. [specific fix]
2. [specific fix]

Fix and regenerate? (yes/no)
```

### Fix & Regenerate Flow

1. Apply all critical fixes to the script or JSON
2. Re-execute
3. Run Step 2.5 verification again
4. Save and tell user new file is ready
5. User reviews again

### Iteration Limit

- **Max 3 vision review cycles**
- After 3 cycles without approval → ask user if they want to simplify the diagram structure

### Escape Valve

User can say "just save it" at any point to accept current state.

---

## Step 5: Core Builder Functions

These Python functions are available for diagram generation. Import them from the core engine:

```python
# === Shapes ===
rect(x, y, w, h, fill="transparent", stroke="#1e1e1e", sw=2, roughness=1, fill_style="solid", stroke_style="solid")
ellipse(x, y, w, h, fill="transparent", stroke="#1e1e1e", sw=2, roughness=1, fill_style="solid")
diamond(x, y, w, h, fill="transparent", stroke="#1e1e1e", sw=2, roughness=1, fill_style="solid")

# === Labeled Shapes (containerId binding -- auto-centers text) ===
labeled_rect(x, y, w, h, label, fill="transparent", stroke="#1e1e1e", sw=2, fs=16, label_color=None, roughness=1, font_family=5, fill_style="solid", stroke_style="solid")
labeled_ellipse(x, y, w, h, label, fill="transparent", stroke="#1e1e1e", sw=2, fs=16, label_color=None, roughness=1, font_family=5, fill_style="solid")
labeled_diamond(x, y, w, h, label, fill="transparent", stroke="#1e1e1e", sw=2, fs=16, label_color=None, roughness=1, font_family=5, fill_style="solid")

# === Auto-sized Labeled Shape (dimensions from text) ===
auto_labeled_rect(x, y, label, padding=10, fill="transparent", stroke="#1e1e1e", sw=2, fs=16, label_color=None, roughness=1, font_family=5, fill_style="solid", stroke_style="solid", min_width=None, min_height=None)

# === Text ===
text_standalone(cx, cy, txt, fs=20, color="#1e1e1e", font_family=5, roughness=0, text_align="center", max_width=None)

# === Connectors ===
arrow(x, y, dx=0, dy=0, *, x2=None, y2=None, stroke="#1e1e1e", sw=2, roughness=1)
line(x, y, dx=0, dy=0, *, x2=None, y2=None, stroke="#1e1e1e", sw=2, roughness=1)
bind_arrow(arrow_el, start_el, end_el, gap=2, start_focus=None, end_focus=None)
connect(start_el, end_el, stroke="#1e1e1e", sw=2, roughness=1, gap=8, elbowed=False, start_focus=None, end_focus=None)

# === Layout Helpers (prevent overlap) ===
below(y, h, gap=10)
right_of(x, w, gap=10)
above(y, gap=10)

# === Structure ===
frame(x, y, w, h, name="Frame", stroke="#1e1e1e", sw=2)
group(elements)

# === Layout Verification (Self-Check) ===
check_overlaps(elements, tolerance=3)    # Returns list of overlap issues
check_arrow_bindings(elements)           # Returns list of arrow binding issues
check_spacing(elements, min_gap=20)      # Returns list of spacing issues
verify_layout(elements)                  # Returns full report with status

# === Charts ===
bar_chart(x, y, data, title=None, ...)
horizontal_bar_chart(x, y, data, title=None, ...)
line_chart(x, y, data, labels, title=None, ...)
pie_chart(x, y, data, title=None, ...)

# === Icons (39 built-in) ===
icon(name, x=0, y=0, scale=1.0, stroke="#495057", sw=2, roughness=1)
list_icons()

# === Icon Library (persistent, searchable) ===
save_icon(name, elements, description="", tags=None, source="custom")
load_icon(name, x=0, y=0, scale=1.0)
find_icons(query, limit=5, use_embeddings=False)

# === AI Icon Generation ===
configure(api_url, api_key, model="gemini-2.0-flash")
generate_icon(description, x=0, y=0, scale=1.0, ...)

# === SVG Converter ===
svg_to_elements(svg_string, x=0, y=0, scale=1.0, ...)
svg_file_to_elements(filepath, x=0, y=0, scale=1.0, ...)

# === LaTeX Formula ===
formula(latex_str, x=0, y=0, scale=1.0, ...)

# === Other ===
numbered_circle(cx, cy, num, fill, stroke)
image_embed(x, y, w, h, base64_data, mime="image/png")

# === Output ===
save_excalidraw(filepath, elements, bg="#ffffff", files=None)
save_obsidian_md(filepath, elements, bg="#ffffff", files=None)
save(filepath, elements, bg="#ffffff", files=None)
```

### Text Centering

The engine uses `containerId` binding for auto-centering text in shapes. For standalone text, CJK-aware width estimation:
- CJK characters: ~1.05x font size
- ASCII characters: ~0.62x font size
- Spaces: ~0.35x font size

Font families: `1` = Virgil (handwritten), `2` = Helvetica, `3` = Cascadia (monospace), `5` = Excalidraw (recommended default — clean handwritten, works for both CJK and Latin)

---

## Step 6: Common Diagram Patterns

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

### Connected Flow (using connect)
```python
from core.engine import auto_labeled_rect, connect, below

b1 = auto_labeled_rect(100, 100, "Input Data", fs=14, fill="#a5d8ff", stroke="#1971c2")
b2 = auto_labeled_rect(100, below(100, b1[0]["height"], gap=40), "Process", fs=14)
a1 = connect(b1[0], b2[0])
elements = [*b1, *b2, a1]
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
    show_points=True, show_grid=True,
)
```

### Pie Chart (with donut mode)
```python
from core.charts import pie_chart

elements = pie_chart(
    x=50, y=100,
    data={"Desktop": 55, "Mobile": 30, "Tablet": 15},
    title="Traffic Sources",
    donut=True, donut_radius=50,
    show_percentages=True,
)
```

### Layout Helper Usage (prevent overlap)
```python
from core.engine import auto_labeled_rect, connect, right_of

box1 = auto_labeled_rect(100, 100, "Data Preprocessing Pipeline",
                          padding=10, fs=14, fill="#a5d8ff")
box2 = auto_labeled_rect(right_of(100, box1[0]["width"], gap=45), 100,
                          "Feature Extraction",
                          padding=10, fs=14, fill="#b2f2bb")
elements = [*box1, *box2, connect(box1[0], box2[0])]
```

### SVG Icon Conversion
```python
from core.svg_converter import svg_to_elements

svg = '<svg viewBox="0 0 24 24"><path d="M12 2L2 22h20Z"/></svg>'
elements = svg_to_elements(svg, x=100, y=50, scale=1.0)
```

### Icon Library Search
```python
from core.icon_library import save_icon, load_icon, find_icons

save_icon("my-server", elements, description="Server rack", tags=["server"])
results = find_icons("server hardware")
server_elements = load_icon(results[0]["name"], x=200, y=100)
```

---

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
| `warning` | Warning triangle |
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

---

## SVG-to-Excalidraw Converter

Convert any SVG to Excalidraw elements. Supports:
- **Path commands**: M, L, H, V, C, S, Q, T, A, Z (absolute & relative)
- **SVG elements**: `<path>`, `<rect>`, `<circle>`, `<ellipse>`, `<line>`, `<polygon>`, `<polyline>`, `<use>`, `<defs>`
- **Shape classification**: Circles -> `ellipse`, rectangles -> `rectangle`, curves -> `line`
- **Bezier tessellation**: Cubic, quadratic, and arc curves sampled to polylines
- **RDP simplification**: Reduces point count while preserving visual fidelity

---

## Charts

Hand-drawn style charts built from Excalidraw primitives:
- **Vertical** (`bar_chart`): Bars going up from x-axis, optional grid lines
- **Horizontal** (`horizontal_bar_chart`): Bars extending right from y-axis
- **Line** (`line_chart`): Multi-series with point markers, grid, and legend
- **Pie** (`pie_chart`): With optional donut mode, labels, and percentages

---

## Styles

### Preset Summary

| Preset | Colors | Text Size | Border | Gap | Roughness |
|--------|--------|-----------|--------|-----|-----------|
| `vivid` | 7-color vibrant | 14-22pt | 2pt | 45px | 1 |
| `clean` | Grayscale | 8-14pt | 1pt | 30px | 1 |
| `sketch` | Warm multi-color | 14-28pt | 2pt | 55px | 1 |

### Aliases

- `conference` -> `vivid`
- `journal` -> `clean`
- `ppt` -> `sketch`

### Custom Style YAML

Users can define custom styles at `~/.excalidraw-gen/styles/*.yaml`:

```yaml
name: "My Custom Style"
description: "Description"
colors:
  background: "#FFFFFF"
  primary: "#4A90E2"
  accent: "#E67E22"
  text: "#1e1e1e"
typography:
  font_family: 2
  title_size: 24
  body_size: 14
layout:
  roughness: 0
  border_width: 2
  default_gap: 50
```

---

## Persistent Icon Library & Search

Save custom icons to `~/.excalidraw-gen/icons/` for reuse across diagrams:
- **save_icon**: Save with description and tags
- **load_icon**: Load and reposition with fresh IDs
- **find_icons**: TF-IDF search (works offline); optional embedding-based semantic search
- **import_excalidrawlib**: Bulk import from `.excalidrawlib` files

---

## AI Icon Generation

Generate icons via Gemini API:

```python
from core.ai_icons import configure, generate_icon
configure(api_url="...", api_key="YOUR_KEY")
elements = generate_icon("a database server rack", x=100, y=50, scale=1.5)
```

---

## File Paths

- Skill directory: `~/.claude/skills/excalidraw-generator/`
- Core engine: `~/.claude/skills/excalidraw-generator/core/engine.py`
- Charts: `~/.claude/skills/excalidraw-generator/core/charts.py`
- Built-in icons: `~/.claude/skills/excalidraw-generator/core/icons.py`
- SVG converter: `~/.claude/skills/excalidraw-generator/core/svg_converter.py`
- Style presets: `~/.claude/skills/excalidraw-generator/styles/`
- Prompt guidelines: `~/.claude/skills/excalidraw-generator/prompts/`
- Custom user styles: `~/.excalidraw-gen/styles/`
- User icon library: `~/.excalidraw-gen/icons/`

---

## Important Rules

- ALWAYS read style prompts via Read tool call (HARD GATE) before generating any diagram
- ALWAYS output a layout table (Step 2B) before writing ANY code
- ALWAYS run `verify_layout()` via Bash tool after generation (Step 2.5)
- ALWAYS use `auto_labeled_rect` for text in rectangles (auto-sizes from text)
- Use `text_standalone` for labels and annotations outside shapes
- Use `below()` / `right_of()` / `above()` to prevent overlap
- Use `connect()` for arrows — it auto-computes direction and edge focus from geometry
- **NEVER** create custom arrow/line helper functions — always use `connect()` or `bind_arrow()`
- **NEVER** write raw `.excalidraw` JSON by hand — always use Python builders
- **NEVER** patch coordinates one-by-one on a broken layout — go back to Step 2B and redesign
- `save()` auto-selects format: `.excalidraw.md` -> Obsidian, `.excalidraw` -> JSON
- `bind_arrow` modifies `start_el`/`end_el` in-place (adds boundElements)
- `connect()` auto-computes edge focus — no need to aim arrows at element centers manually
- NEVER leave `focus=0` on 3+ arrows entering the same large target; distribute binding focus across the target edge
- For fan-in / fan-out, prefer edge-distributed binding points; if many sources come from the same side, use `elbowed=True`
- `group()` returns new list with shared groupId (does not modify originals)

---

## Visual Quality Rules (CRITICAL — Learned from Real Diagrams)

These rules are derived from analyzing high-quality Excalidraw diagrams produced by the skill. Follow them to avoid the "flat, sparse, boring" look.

### Element Richness

- **Target 30-50 elements** for complex diagrams, **15-25** for medium, **8-14** for simple
- Simple diagrams (<15 elements) look bare — add context: labels, annotations, grouping boxes, section dividers
- Use **nested card patterns**: outer colored rect → inner white rect → bound text (creates visual depth)
- Add **descriptive subtitles** below main labels (smaller font, lighter color)

### Typography Hierarchy

Use at least **3 font sizes** per diagram:

| Role | Font Size | Example |
|------|-----------|---------|
| Page title | 24-28pt | "Decision Transformer Architecture" |
| Section headers | 16-18pt | "Sequence Pipeline", "Comparison" |
| Box labels | 12-16pt | "RTG₁", "State Encoder" |
| Annotations | 8-11pt | Conference names, descriptions, notes |

### Color Palette (Mantine)

Use this consistent palette across all diagrams:

| Role | Stroke | Fill | Use For |
|------|--------|------|---------|
| Blue | `#1971c2` | `#a5d8ff` | Primary elements, data flow |
| Green | `#2f9e44` | `#b2f2bb` | Success, positive, output |
| Orange | `#e8590c` | `#ffd8a8` | Warning, action, emphasis |
| Purple | `#7048e8` | `#d0bfff` | Special, auth, ML features |
| Teal | `#0c8599` | `#99e9f2` | Secondary, alternative |
| Red | `#e03131` | `#ffc9c9` | Error, danger, delete |
| Yellow | `#f08c00` | `#fff3bf` | Warning, attention |
| Gray | `#495057` | `#dee2e6` | Neutral, background, arrows |

### Semantic Color Coding

Assign colors by **semantic role**, not randomly:
- Same concept across the diagram = same color (e.g., all "RTG" boxes are purple)
- Different roles get different colors (e.g., RTG=purple, State=blue, Action=orange)
- Arrows inherit the color of their source or use neutral gray (#495057)

### Roughness Pattern

- **Shapes**: `roughness=1` (hand-drawn feel)
- **Bound text** (inside containers): `roughness=0` (crisp, readable)
- **Standalone text** (titles, labels): `roughness=0` (crisp)
- This contrast makes shapes feel hand-drawn while text stays legible

### Fill Styles

- `"solid"` — modern, clean look (default)
- `"hachure"` — classic technical drawing feel, better for academic papers
- Use `"hachure"` when the diagram has a technical/architectural theme

### Spacing Guidelines

| Gap Type | Recommended | Notes |
|----------|-------------|-------|
| Between same-row elements | 20-30px | Tight but not touching |
| Between sections | 40-60px | Clear visual separation |
| Card inner padding | 8-10px | White title box inside colored card |
| Arrow-to-element gap | 8-12px | `connect(gap=8)` default |
| Timeline node-to-card | 30-50px | Vertical connector from node to card |

### Advanced Layout Patterns

#### Timeline Layout
```
[Title text at top, centered]

[Card 1]   [Card 2]   [Card 3]   [Card 4]
   |           |           |           |
   ●———————→  ●———————→  ●———————→  ●
[Labels]    [Labels]    [Labels]    [Labels]

[Bottom summary bar spanning full width]
```

#### Sequence Grid (DT-style)
```
          t=1        t=2        t=3        t=4
       ┌──────┐  ┌──────┐  ┌──────┐  ┌──────┐
  RTG  │ R₁   │  │ R₂   │  │ R₃   │  │ R₄   │  ← purple
       ├──────┤  ├──────┤  ├──────┤  ├──────┤
   S   │ S₁   │  │ S₂   │  │ S₃   │  │ S₄   │  ← blue
       ├──────┤  ├──────┤  ├──────┤  ├──────┤
   A   │ a₁   │  │ a₂   │  │ a₃   │  │ a₄   │  ← orange
       └──────┘  └──────┘  └──────┘  └──────┘
            ↓         ↓         ↓         ↓
       ┌──────────────────────────────────────┐
       │         Transformer Block            │  ← yellow
       └──────────────────────────────────────┘
                          ↓
                    ┌───────────┐
                    │  Output   │  ← orange
                    └───────────┘
```

#### Comparison Table
```
            ┌─────────────┬──────────────────┐
            │ Traditional │ Decision         │
            │ RL          │ Transformer      │
  ├─────────┼─────────────┼──────────────────┤
  │ Input   │ ...         │ ...              │  ← blue row
  ├─────────┼─────────────┼──────────────────┤
  │ History │ ...         │ ...              │  ← teal row
  ├─────────┼─────────────┼──────────────────┤
  │ Missing │ ...         │ ...              │  ← green row
  └─────────┴─────────────┴──────────────────┘
```

#### Nested Card (depth effect)
```python
# Outer colored card
outer = rect(x, y, 190, 130, fill=fill, stroke=stroke, sw=2, roughness=1)
# Inner white title box (8px padding)
inner = labeled_rect(x+8, y+8, 174, 35, title,
                     fill="#ffffff", stroke=stroke, sw=1, roughness=0)
# Description text below title
desc = text_standalone(cx, y+60, description, fs=10, color="#495057")
```

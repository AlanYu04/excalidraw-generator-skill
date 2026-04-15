# Quick Start

## As a Claude Code Skill

Clone the repository into your Claude Code skills directory:

```bash
git clone https://github.com/AlanYu04/excalidraw-generator-skill ~/.claude/skills/excalidraw-generator
```

Then just ask Claude to draw:

> "Draw me a Transformer architecture diagram -- vivid style, hachure fill, roughness 1"

Claude will generate an `.excalidraw` file you can open in [excalidraw.com](https://excalidraw.com), VS Code, or Obsidian.

## As a Python Library

### Prerequisites

**Obsidian (recommended)** -- for viewing and editing Excalidraw files:

1. Download from [obsidian.md](https://obsidian.md/download)
2. Create or open a Vault
3. Install the **Excalidraw** community plugin (by Zsolt Viczian)

**Without Obsidian** -- `.excalidraw` files are standard JSON and work with any Excalidraw-compatible tool.

### Install

```bash
cd ~/.claude/skills/excalidraw-generator
pip install matplotlib numpy
```

Optional: `pip install pyyaml` for custom YAML styles.

### Create Your First Diagram

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

### Generate a Chart

```python
from core.charts import bar_chart

elements = bar_chart(
    x=50, y=100,
    data={"React": 85, "Vue": 72, "Angular": 58},
    title="Framework Popularity",
    bar_color="#a5d8ff",
    show_values=True,
    show_grid=True,
)
```

### Add a Formula

```python
from core.latex import formula

elements = formula(r"E = mc^2", x=100, y=50, font_size=20)
```

### Place Icons

```python
from core.icons import icon

elements = icon("database", x=100, y=50, scale=1.0, stroke="#1e1e1e", sw=2)
```

## Next Steps

- [Style Configuration](/guide/style-config) -- Learn about the 3 style presets and custom YAML styles
- [Advanced Usage](/guide/advanced) -- Layout helpers, CJK support, icon library, and more
- [API Reference](/api/) -- Full API documentation for all modules

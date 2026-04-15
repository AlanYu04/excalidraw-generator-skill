# Advanced Usage

## Layout Helpers

Prevent overlapping elements with positional utilities. These functions compute coordinates so you do not have to calculate them manually.

```python
from core.engine import below, right_of, above

# Place a 60px-tall element 15px below y=100
y2 = below(y=100, h=60, gap=15)    # y2 = 175

# Place a 200px-wide element 10px to the right of x=50
x2 = right_of(x=50, w=200, gap=10) # x2 = 260

# Place an element 10px above y=100
y_above = above(y=100, gap=10)     # y_above = 90
```

These are pure functions -- they return computed values without modifying any state.

### Building a Vertical Stack

```python
from core.engine import labeled_rect, below, save

elements = []
y = 50
for label in ["Input", "Hidden 1", "Hidden 2", "Output"]:
    block = labeled_rect(100, y, 200, 50, label)
    elements.extend(block)
    y = below(y=y, h=50, gap=20)

save("stack.excalidraw", elements)
```

## Image Embedding

Embed images directly into Excalidraw files using base64-encoded data.

```python
from core.engine import image_embed

# Read an image file and embed it
with open("logo.png", "rb") as f:
    data = f.read()

element, files_entry = image_embed(
    x=100, y=50, w=200, h=100,
    base64_data=data,
    mime="image/png",
)
```

`image_embed` returns a tuple of `(element_dict, files_dict)`. When saving, pass both to `save()`:

```python
from core.engine import save

element, files = image_embed(100, 50, 200, 100, data, "image/png")
save("with-image.excalidraw", [element], files={"embedded_image": files})
```

## CJK Support

Chinese, Japanese, and Korean text is handled automatically. All text functions estimate CJK character widths correctly so labels center properly in their containers.

```python
from core.engine import labeled_rect, text_standalone

# CJK text works in any element
elements = labeled_rect(100, 50, 200, 60, "数据处理流程", font_family=3)

# Multi-line CJK text
t = text_standalone(300, 100, "第一行\n第二行\n第三行", fs=16, font_family=3)
```

For CJK-optimized rendering in Excalidraw, use `font_family=5`.

No extra configuration is needed -- CJK detection and width estimation are built into the text measurement functions.

## Output Formats

### `.excalidraw`

Standard JSON format. Works with [excalidraw.com](https://excalidraw.com), VS Code Excalidraw extension, and any Excalidraw-compatible tool.

### `.excalidraw.md`

Markdown wrapper for the [Obsidian Excalidraw plugin](https://github.com/zsviczian/obsidian-excalidraw-plugin). The file embeds the Excalidraw JSON inside a markdown code block that Obsidian recognizes.

```python
from core.engine import save

save("diagram.excalidraw", elements)        # Pure JSON
save("diagram.excalidraw.md", elements)     # Obsidian format
```

The `save()` function auto-detects the format from the file extension.

## Icon Library

The persistent icon library stores custom icons at `~/.excalidraw-gen/icons/` and provides search capabilities.

### Save and Load

```python
from core.icon_library import save_icon, load_icon, list_library_icons

# Save a custom icon
save_icon(
    "my-server",
    elements,
    description="Server with LED indicators",
    tags=["server", "hardware"],
)

# Load and place it
server = load_icon("my-server", x=200, y=100, scale=1.0)

# List all saved icons
print(list_library_icons())
```

### Search Icons

Search uses TF-IDF by default (zero dependencies) or OpenAI embeddings if configured.

```python
from core.icon_library import find_icons

# TF-IDF search (default)
results = find_icons("server infrastructure", limit=5)

# OpenAI embeddings search
results = find_icons("neural network architecture", use_embeddings=True)

# Load the best match
if results:
    icon = load_icon(results[0]["name"], x=100, y=50)
```

### Import from `.excalidrawlib`

Import icons from Excalidraw library files:

```python
from core.icon_library import import_excalidrawlib

import_excalidrawlib(
    filepath="my-library.excalidrawlib",
    descriptions={"icon-1": "A gear icon", "icon-2": "A cloud icon"},
    tags_map={"icon-1": ["gear", "settings"], "icon-2": ["cloud"]},
    prefix="custom",
)
```

## AI Icon Generation

Generate custom icons via the Gemini API, with automatic SVG-to-Excalidraw conversion and PNG fallback.

### Configuration

```python
from core.ai_icons import configure

configure(
    api_url="https://generativelanguage.googleapis.com/v1beta",
    api_key="YOUR_GEMINI_API_KEY",
    model="gemini-2.0-flash",
)
```

### Generate Icons

```python
from core.ai_icons import generate_icon, generate_and_save

# Generate and place
elements = generate_icon(
    "kubernetes pod",
    x=100, y=200,
    scale=1.5,
    stroke="#1e1e1e",
    sw=2,
    roughness=1,
)

# Generate and save to library in one step
generate_and_save(
    "k8s-pod",
    "Kubernetes pod icon",
    tags=["k8s", "container"],
)
```

### Raw SVG Generation

```python
from core.ai_icons import generate_icon_svg

svg_string = generate_icon_svg(
    "neural network node",
    prompt="Simple line art, minimal detail",
    model="gemini-2.0-flash",
)
```

Note: AI icon generation requires a Gemini API key and depends on the SVG converter for post-processing.

## SVG Converter

Convert SVG strings or files to native Excalidraw elements.

```python
from core.svg_converter import svg_to_elements, svg_file_to_elements

# From SVG string
elements = svg_to_elements(
    '<svg viewBox="0 0 100 100"><circle cx="50" cy="50" r="40"/></svg>',
    x=100, y=50, scale=1.0,
    stroke="#1e1e1e", stroke_width=2, roughness=1,
)

# From file
elements = svg_file_to_elements("icon.svg", x=200, y=100, scale=2.0)
```

Supported SVG features: `<path>` (all commands), `<rect>`, `<circle>`, `<ellipse>`, `<line>`, `<polygon>`, `<polyline>`, `<defs>`, `<use>`, Bezier tessellation, RDP simplification, gradient fill resolution, and automatic shape classification.

## Next Steps

- [Style Configuration](/guide/style-config) -- Customize visual appearance with presets and YAML
- [API Reference](/api/) -- Full API documentation for all modules

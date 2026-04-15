---
title: Icons
---

# Icons

Three icon systems: 39 built-in icons, a persistent icon library with search, and AI-powered icon generation via the Gemini API.

## Built-in Icons

### `icon`

```python
from core.icons import icon, list_icons

# List all available icon names
print(list_icons())

# Place an icon at a position
elements = icon("database", x=100, y=50, scale=1.0, stroke="#1e1e1e", sw=2, roughness=1)
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `name` | `str` | required | Icon name (use `list_icons()` to see all) |
| `x` | `float` | `0` | Top-left X position |
| `y` | `float` | `0` | Top-left Y position |
| `scale` | `float` | `1.0` | Scale factor (1.0 = ~48px) |
| `stroke` | `str` | `"#1e1e1e"` | Stroke color |
| `sw` | `int` | `2` | Stroke width |
| `roughness` | `int` | `1` | Excalidraw roughness (0, 1, or 2) |

Returns: `list[dict]` -- list of Excalidraw element dicts composing the icon.

### `list_icons`

```python
from core.icons import list_icons

names = list_icons()  # Returns sorted list of all 39 icon names
```

Returns: `list[str]` -- sorted list of all available icon names.

## General Icons (10)

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

## ML/AI Icons (12)

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

## Utility Icons (18)

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

## Icon Library

Save, load, and search custom icons stored at `~/.excalidraw-gen/icons/`.

### `save_icon`

```python
from core.icon_library import save_icon

save_icon(
    name="my-server",
    elements=server_elements,
    description="Server with LED indicators",
    tags=["server", "hardware"],
    source="custom",
    source_file=None,
)
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `name` | `str` | required | Unique icon name (used as identifier) |
| `elements` | `list[dict]` | required | List of Excalidraw element dicts |
| `description` | `str` | `""` | Text description for search |
| `tags` | `list[str] \| None` | `None` | Optional tag strings |
| `source` | `str` | `"custom"` | Origin (e.g. `'svg-converted'`, `'ai-generated'`) |
| `source_file` | `str \| None` | `None` | Optional path to source file |

### `load_icon`

```python
from core.icon_library import load_icon

elements = load_icon("my-server", x=200, y=100, scale=1.5)
```

Raises `KeyError` if the icon name is not found.

### `delete_icon`

```python
from core.icon_library import delete_icon

delete_icon("my-server")
```

### `list_library_icons`

```python
from core.icon_library import list_library_icons

icons = list_library_icons()  # Returns list of metadata dicts
```

### `find_icons`

```python
from core.icon_library import find_icons

# TF-IDF search (zero dependencies)
results = find_icons("server infrastructure", limit=5)

# OpenAI embedding search (requires openai package and OPENAI_API_KEY)
results = find_icons("server infrastructure", use_embeddings=True)
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `query` | `str` | required | Search query text |
| `limit` | `int` | `5` | Maximum number of results |
| `use_embeddings` | `bool` | `False` | Use OpenAI embeddings if `True` |

Returns: `list[dict]` -- each with `name`, `score`, `description`, `tags`.

### `import_excalidrawlib`

```python
from core.icon_library import import_excalidrawlib

imported = import_excalidrawlib(
    filepath="my-library.excalidrawlib",
    descriptions={"icon-1": "First icon"},
    tags_map={"icon-1": ["custom", "imported"]},
    prefix="lib-",
)
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `filepath` | `str` | required | Path to the `.excalidrawlib` file |
| `descriptions` | `dict \| None` | `None` | Map item name/slug to description |
| `tags_map` | `dict \| None` | `None` | Map item name/slug to tag list |
| `prefix` | `str` | `""` | Prefix for all imported icon names |

Returns: `list[str]` -- list of imported icon name slugs.

## AI Icon Generation

Generate icons via the Gemini API, with automatic SVG-to-Excalidraw conversion and PNG fallback.

### `configure`

```python
from core.ai_icons import configure

configure(
    api_url="https://generativelanguage.googleapis.com/v1beta",
    api_key="YOUR_KEY",
    model="gemini-2.0-flash",
)
```

Saves configuration to `~/.excalidraw-gen/config.json`.

### `generate_icon`

```python
from core.ai_icons import generate_icon

elements = generate_icon(
    description="kubernetes pod",
    x=100, y=200,
    scale=1.5,
    stroke="#1e1e1e",
    sw=2,
    roughness=1,
)
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `description` | `str` | required | What icon to generate |
| `x` | `float` | `0` | X position |
| `y` | `float` | `0` | Y position |
| `scale` | `float` | `1.0` | Scale factor |
| `stroke` | `str` | `"#1e1e1e"` | Stroke color |
| `sw` | `int` | `2` | Stroke width |
| `roughness` | `int` | `1` | Roughness level |
| `prompt` | `str \| None` | `None` | Custom prompt template (supports `{description}` placeholder) |

Returns: `list[dict]` -- Excalidraw element dicts.

### `generate_icon_svg`

```python
from core.ai_icons import generate_icon_svg

svg_string = generate_icon_svg(
    description="server rack",
    prompt=None,
    model="gemini-2.0-flash",
)
```

Returns: `str` -- raw SVG string. Useful if you want to process the SVG yourself.

### `generate_and_save`

```python
from core.ai_icons import generate_and_save

elements = generate_and_save(
    name="k8s-pod",
    description="Kubernetes pod icon",
    tags=["k8s", "container"],
    # All kwargs from generate_icon are forwarded
    x=100, y=50, scale=1.5,
)
```

Generates an icon and saves it to the persistent icon library in one call.

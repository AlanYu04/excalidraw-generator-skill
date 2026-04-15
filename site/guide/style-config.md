# Style Configuration

Excalidraw Generator ships with three built-in style presets that control fonts, roughness, fill behavior, and colors. You can also define custom styles via YAML.

## Built-in Presets

| Preset | Font | Roughness | Fill Style | Use Case |
|--------|------|-----------|------------|----------|
| **Vivid** | Cascadia (3) | 1 | Solid | Rich, colorful, detailed -- conference presentations |
| **Clean** | Helvetica (2) | 0 | Solid | Minimal, B&W, precise -- journal papers |
| **Sketch** | Virgil (1) | 2 | Hachure | Hand-drawn, casual -- presentations and notes |

## Loading a Style

```python
from styles import load_style

# Load by name
style = load_style("vivid")

# Aliases also work
style = load_style("conference")  # same as "vivid"
```

Style aliases: `conference` -> `vivid`, `journal` -> `clean`, `ppt` -> `sketch`.

## Color Pairs

Every style provides semantic color pairs via `get_color_pair(role)`. Each call returns a `(fill, stroke)` tuple.

```python
from styles import load_style

style = load_style("vivid")

fill, stroke = style.get_color_pair("primary")   # ("#a5d8ff", "#2B5B84")
fill, stroke = style.get_color_pair("accent")    # ("#ffd8a8", "#E67E22")
fill, stroke = style.get_color_pair("success")   # ("#b2f2bb", "#2f9e44")
fill, stroke = style.get_color_pair("warning")   # ("#fff3bf", "#f08c00")
fill, stroke = style.get_color_pair("danger")    # ("#ffc9c9", "#e03131")
fill, stroke = style.get_color_pair("info")      # ("#99e9f2", "#1971c2")
fill, stroke = style.get_color_pair("neutral")   # ("#dee2e6", "#999999")
```

Supported roles: `primary`, `accent`, `success`, `warning`, `danger`, `info`, `neutral`.

## Style Configuration Fields

The `StyleConfig` dataclass exposes these fields:

**Colors**

| Field | Default | Description |
|-------|---------|-------------|
| `background` | `#ffffff` | Canvas background |
| `primary` | `#2B5B84` | Primary stroke color |
| `accent` | `#E67E22` | Accent stroke color |
| `text_color` | `#1e1e1e` | Default text color |
| `border_color` | `#333333` | Border stroke color |
| `muted` | `#999999` | Muted/secondary text |
| `success` | `#2f9e44` | Success stroke |
| `warning` | `#f08c00` | Warning stroke |
| `danger` | `#e03131` | Danger stroke |
| `info` | `#1971c2` | Info stroke |

**Typography**

| Field | Default | Description |
|-------|---------|-------------|
| `font_family` | `3` | 1=Virgil (handwritten), 2=Helvetica, 3=Cascadia |
| `title_size` | `24` | Title font size |
| `body_size` | `14` | Body font size |
| `label_size` | `11` | Label font size |

**Layout**

| Field | Default | Description |
|-------|---------|-------------|
| `roughness` | `1` | 0=precise, 1=slight, 2=rough |
| `border_width` | `2` | Default stroke width |
| `fill_style` | `"solid"` | `"solid"`, `"hachure"`, or `"cross-hatch"` |
| `stroke_style` | `"solid"` | `"solid"`, `"dashed"`, or `"dotted"` |
| `border_radius` | `True` | Rounded rectangle corners |

## Custom YAML Styles

Create a YAML file in `~/.excalidraw-gen/styles/` to define your own style. For example, `~/.excalidraw-gen/styles/dark-mode.yaml`:

```yaml
name: "Dark Mode"
description: "Dark background theme for presentations"
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

Then load it by name:

```python
from styles import load_style

style = load_style("dark-mode")
```

The loader checks built-in presets first, then falls back to custom YAML files. If a style is not found, it raises `FileNotFoundError` with a list of available styles.

## Live Preview

Switch between the three presets to see how they look in practice:

<ClientOnly>
  <StyleSwitcher />
</ClientOnly>

## Next Steps

- [Advanced Usage](/guide/advanced) -- Layout helpers, CJK support, icon library, and output formats
- [API Reference: Styles](/api/styles) -- Full `StyleConfig` API documentation

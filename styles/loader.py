"""
Style loader — resolves a style name to a StyleConfig instance.
Supports built-in presets and custom YAML configs.
"""
import os
import yaml
from .base import StyleConfig
from .conference import vivid_style
from .journal import clean_style
from .ppt import sketch_style


BUILTIN_STYLES = {
    "vivid": vivid_style,
    "clean": clean_style,
    "sketch": sketch_style,
}

# Backward-compatible aliases
_STYLE_ALIASES = {
    "conference": "vivid",
    "journal": "clean",
    "ppt": "sketch",
}

CUSTOM_STYLE_DIR = os.path.expanduser("~/.excalidraw-gen/styles")


def load_style(name: str) -> StyleConfig:
    """
    Load a style by name. Checks built-in presets first,
    then falls back to custom YAML files in ~/.excalidraw-gen/styles/.
    """
    # Resolve aliases
    resolved = _STYLE_ALIASES.get(name, name)

    if resolved in BUILTIN_STYLES:
        return BUILTIN_STYLES[resolved]()

    # Try loading from custom YAML
    yaml_path = os.path.join(CUSTOM_STYLE_DIR, f"{name}.yaml")
    if not os.path.exists(yaml_path):
        yaml_path = os.path.join(CUSTOM_STYLE_DIR, f"{name}.yml")
    if not os.path.exists(yaml_path):
        available = ", ".join(list(BUILTIN_STYLES.keys()))
        raise FileNotFoundError(
            f"Style '{name}' not found. Built-in: [{available}]. "
            f"Custom styles go in {CUSTOM_STYLE_DIR}/{name}.yaml"
        )

    return _load_yaml_style(yaml_path)


def _load_yaml_style(path: str) -> StyleConfig:
    """Parse a YAML file into a StyleConfig."""
    with open(path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    cfg = StyleConfig()
    if "name" in data:
        cfg.name = data["name"]
    if "description" in data:
        cfg.description = data["description"]

    colors = data.get("colors", {})
    for key in ["background", "primary", "accent", "border", "muted"]:
        if key in colors:
            setattr(cfg, key, colors[key])
    if "text" in colors:
        cfg.text_color = colors["text"]

    typo = data.get("typography", {})
    for key in ["font_family", "title_size", "body_size", "label_size"]:
        if key in typo:
            setattr(cfg, key, typo[key])

    layout = data.get("layout", {})
    for key in ["roughness", "border_width", "arrow_width", "default_gap"]:
        if key in layout:
            setattr(cfg, key, layout[key])
    if "border_radius" in layout:
        cfg.border_radius = layout["border_radius"]

    return cfg


def list_styles() -> list[str]:
    """List all available style names (built-in + custom)."""
    names = list(BUILTIN_STYLES.keys())
    if os.path.isdir(CUSTOM_STYLE_DIR):
        for fname in os.listdir(CUSTOM_STYLE_DIR):
            if fname.endswith((".yaml", ".yml")):
                names.append(os.path.splitext(fname)[0])
    return names

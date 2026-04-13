"""Core engine for Excalidraw diagram generation."""
from .engine import (
    rect,
    text_standalone,
    labeled_rect,
    labeled_diamond,
    labeled_ellipse,
    arrow,
    ellipse,
    diamond,
    line,
    group,
    frame,
    image_embed,
    bind_arrow,
    numbered_circle,
    save_excalidraw,
    save_obsidian_md,
    estimate_text_width,
    estimate_text_height,
    is_cjk,
    uid,
    sd,
    ts,
)
from .icons import icon, list_icons
from .svg_converter import svg_to_elements, svg_file_to_elements
from .charts import bar_chart, horizontal_bar_chart
from .icon_library import (
    save_icon,
    load_icon,
    delete_icon,
    list_library_icons,
    find_icons,
)

__all__ = [
    # Engine builders
    "rect",
    "text_standalone",
    "labeled_rect",
    "labeled_diamond",
    "labeled_ellipse",
    "arrow",
    "ellipse",
    "diamond",
    "line",
    "group",
    "frame",
    "image_embed",
    "bind_arrow",
    "icon",
    "list_icons",
    "numbered_circle",
    # Output
    "save_excalidraw",
    "save_obsidian_md",
    # Text utilities
    "estimate_text_width",
    "estimate_text_height",
    "is_cjk",
    "uid",
    "sd",
    "ts",
    # SVG converter
    "svg_to_elements",
    "svg_file_to_elements",
    # Charts
    "bar_chart",
    "horizontal_bar_chart",
    # Icon library
    "save_icon",
    "load_icon",
    "delete_icon",
    "list_library_icons",
    "find_icons",
]

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
    connect,
    numbered_circle,
    save_excalidraw,
    save_obsidian_md,
    save,
    estimate_text_width,
    estimate_text_height,
    is_cjk,
    uid,
    sd,
    ts,
)
from .icons import icon, list_icons
from .svg_converter import svg_to_elements, svg_file_to_elements
from .charts import bar_chart, horizontal_bar_chart, line_chart, pie_chart
from .icon_library import (
    save_icon,
    load_icon,
    delete_icon,
    list_library_icons,
    find_icons,
    import_excalidrawlib,
)
from .ai_icons import (
    configure as configure_ai,
    generate_icon,
    generate_icon_svg,
    generate_and_save,
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
    "connect",
    "icon",
    "list_icons",
    "numbered_circle",
    # Output
    "save_excalidraw",
    "save_obsidian_md",
    "save",
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
    "line_chart",
    "pie_chart",
    # Icon library
    "save_icon",
    "load_icon",
    "delete_icon",
    "list_library_icons",
    "find_icons",
    "import_excalidrawlib",
    # AI icon generation
    "configure_ai",
    "generate_icon",
    "generate_icon_svg",
    "generate_and_save",
]

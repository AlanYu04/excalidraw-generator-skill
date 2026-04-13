"""Style presets for Excalidraw diagram generation."""
from .base import StyleConfig
from .loader import load_style, list_styles
from .conference import vivid_style
from .journal import clean_style
from .ppt import sketch_style

__all__ = [
    "StyleConfig",
    "load_style",
    "list_styles",
    "vivid_style",
    "clean_style",
    "sketch_style",
]

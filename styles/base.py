"""
Base style definition for Excalidraw diagram generation.
All style presets inherit from this dataclass.
"""
from dataclasses import dataclass


@dataclass
class StyleConfig:
    """Style configuration that controls visual appearance of generated diagrams."""

    name: str = "default"
    description: str = ""

    # Colors
    background: str = "#ffffff"
    primary: str = "#2B5B84"
    accent: str = "#E67E22"
    text_color: str = "#1e1e1e"
    border_color: str = "#333333"
    muted: str = "#999999"

    # Semantic colors (derived from primary/accent)
    success: str = "#2f9e44"
    warning: str = "#f08c00"
    danger: str = "#e03131"
    info: str = "#1971c2"

    # Fill colors (light variants)
    primary_fill: str = "#a5d8ff"
    accent_fill: str = "#ffd8a8"
    success_fill: str = "#b2f2bb"
    warning_fill: str = "#fff3bf"
    danger_fill: str = "#ffc9c9"
    info_fill: str = "#99e9f2"
    neutral_fill: str = "#dee2e6"

    # Typography
    font_family: int = 3        # 1=Virgil(handwritten) 2=Helvetica 3=Cascadia
    title_size: int = 24
    subtitle_size: int = 14
    body_size: int = 14
    label_size: int = 11
    caption_size: int = 10

    # Layout
    roughness: int = 1          # 0=precise 1=slight 2=rough
    border_width: int = 2
    arrow_width: int = 2
    default_gap: int = 50
    padding: int = 10
    grid_step: int = 10
    spacing_policy: str = "balanced"

    # Fill style: "solid" | "hachure" | "cross-hatch"
    fill_style: str = "solid"

    # Stroke style: "solid" | "dashed" | "dotted"
    stroke_style: str = "solid"

    # Shape preferences
    border_radius: bool = True   # True = roundness type 3 for rects
    use_groups: bool = False
    compact_layout: bool = False
    allowed_arrow_modes: tuple[str, ...] = ("straight",)

    def get_color_pair(self, role: str = "primary") -> tuple[str, str]:
        """Return (fill, stroke) for a given semantic role."""
        mapping = {
            "primary":   (self.primary_fill, self.primary),
            "accent":    (self.accent_fill, self.accent),
            "success":   (self.success_fill, self.success),
            "warning":   (self.warning_fill, self.warning),
            "danger":    (self.danger_fill, self.danger),
            "info":      (self.info_fill, self.info),
            "neutral":   (self.neutral_fill, self.muted),
        }
        return mapping.get(role, (self.primary_fill, self.primary))

    def allowed_colors(self) -> set[str]:
        """Return the palette used by validators and renderers."""
        return {
            "transparent",
            self.background,
            self.primary,
            self.accent,
            self.text_color,
            self.border_color,
            self.muted,
            self.success,
            self.warning,
            self.danger,
            self.info,
            self.primary_fill,
            self.accent_fill,
            self.success_fill,
            self.warning_fill,
            self.danger_fill,
            self.info_fill,
            self.neutral_fill,
        }

    def to_style_rules(self) -> dict:
        """Return a machine-readable style contract."""
        return {
            "name": self.name,
            "font_family": self.font_family,
            "title_size": self.title_size,
            "subtitle_size": self.subtitle_size,
            "body_size": self.body_size,
            "label_size": self.label_size,
            "caption_size": self.caption_size,
            "roughness": self.roughness,
            "border_width": self.border_width,
            "arrow_width": self.arrow_width,
            "default_gap": self.default_gap,
            "padding": self.padding,
            "grid_step": self.grid_step,
            "spacing_policy": self.spacing_policy,
            "fill_style": self.fill_style,
            "stroke_style": self.stroke_style,
            "border_radius": self.border_radius,
            "allowed_arrow_modes": list(self.allowed_arrow_modes),
            "background": self.background,
            "palette": sorted(self.allowed_colors()),
            "text_color": self.text_color,
            "border_color": self.border_color,
            "role_colors": {
                role: {
                    "fill": fill,
                    "stroke": stroke,
                }
                for role, (fill, stroke) in {
                    "primary": self.get_color_pair("primary"),
                    "accent": self.get_color_pair("accent"),
                    "success": self.get_color_pair("success"),
                    "warning": self.get_color_pair("warning"),
                    "danger": self.get_color_pair("danger"),
                    "info": self.get_color_pair("info"),
                    "neutral": self.get_color_pair("neutral"),
                }.items()
            },
        }

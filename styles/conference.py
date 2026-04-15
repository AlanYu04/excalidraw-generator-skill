"""
Vivid style preset — Rich, colorful, detailed diagrams.
Lots of annotations, sub-cards, numbered badges, multi-color palette.
"""
from .base import StyleConfig


def vivid_style() -> StyleConfig:
    return StyleConfig(
        name="vivid",
        description="Rich colorful style with lots of detail and visual hierarchy",

        # Colors — conference-safe palette
        background="#FFFFFF",
        primary="#2B5B84",
        accent="#E67E22",
        text_color="#1e1e1e",
        border_color="#2B5B84",
        muted="#6c757d",

        success="#73C6B6",
        warning="#E67E22",
        danger="#C0392B",
        info="#4A90E2",

        primary_fill="#DCEAF6",
        accent_fill="#ffd8a8",
        success_fill="#D5F5E3",
        warning_fill="#FDEBD0",
        danger_fill="#FADBD8",
        info_fill="#D6EAF8",
        neutral_fill="#D5DBDB",

        # Typography — prompt contract source of truth
        font_family=2,
        title_size=20,
        subtitle_size=14,
        body_size=12,
        label_size=10,
        caption_size=9,

        # Layout — compact academic diagram
        roughness=0,
        border_width=1.5,
        arrow_width=1.5,
        default_gap=45,
        padding=8,
        grid_step=20,
        spacing_policy="balanced",

        border_radius=False,
        use_groups=False,
        compact_layout=False,
        allowed_arrow_modes=("straight",),
    )

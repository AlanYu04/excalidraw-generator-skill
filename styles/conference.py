"""
Vivid style preset — Rich, colorful, detailed diagrams.
Lots of annotations, sub-cards, numbered badges, multi-color palette.
"""
from .base import StyleConfig


def vivid_style() -> StyleConfig:
    return StyleConfig(
        name="vivid",
        description="Rich colorful style with lots of detail and visual hierarchy",

        # Colors — full vibrant palette
        background="#FFFFFF",
        primary="#2B5B84",
        accent="#E67E22",
        text_color="#1e1e1e",
        border_color="#2B5B84",
        muted="#6c757d",

        success="#2f9e44",
        warning="#f08c00",
        danger="#e03131",
        info="#1971c2",

        primary_fill="#a5d8ff",
        accent_fill="#ffd8a8",
        success_fill="#b2f2bb",
        warning_fill="#fff3bf",
        danger_fill="#ffc9c9",
        info_fill="#99e9f2",
        neutral_fill="#dee2e6",

        # Typography — larger for readability
        title_size=22,
        subtitle_size=14,
        body_size=14,
        label_size=11,
        caption_size=10,

        # Layout — balanced
        border_width=2,
        arrow_width=2,
        default_gap=45,
        padding=8,

        border_radius=True,
        use_groups=False,
        compact_layout=False,
    )

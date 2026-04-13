"""
Sketch style preset — Hand-drawn, casual, expressive.
Rough lines, big text, playful feel.
"""
from .base import StyleConfig


def sketch_style() -> StyleConfig:
    return StyleConfig(
        name="sketch",
        description="Hand-drawn casual style with rough lines and playful feel",

        # Colors — warm, approachable
        background="#FFFFFF",
        primary="#1971c2",
        accent="#e8590c",
        text_color="#1e1e1e",
        border_color="#495057",
        muted="#868e96",

        success="#2f9e44",
        warning="#f08c00",
        danger="#e03131",
        info="#0c8599",

        primary_fill="#a5d8ff",
        accent_fill="#ffd8a8",
        success_fill="#b2f2bb",
        warning_fill="#fff3bf",
        danger_fill="#ffc9c9",
        info_fill="#99e9f2",
        neutral_fill="#dee2e6",

        # Typography — large and readable
        title_size=28,
        subtitle_size=18,
        body_size=18,
        label_size=14,
        caption_size=12,

        # Layout — relaxed, wide spacing
        border_width=2,
        arrow_width=2,
        default_gap=55,
        padding=12,

        border_radius=True,
        use_groups=False,
        compact_layout=False,
    )

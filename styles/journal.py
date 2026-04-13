"""
Clean style preset — Minimal, precise, data-flow focused.
Thin borders, small text, black-and-white friendly, no decoration.
"""
from .base import StyleConfig


def clean_style() -> StyleConfig:
    return StyleConfig(
        name="clean",
        description="Minimal precise style focused on data flow clarity",

        # Colors — grayscale-friendly
        background="#FFFFFF",
        primary="#000000",
        accent="#444444",
        text_color="#000000",
        border_color="#000000",
        muted="#666666",

        success="#333333",
        warning="#555555",
        danger="#333333",
        info="#444444",

        primary_fill="#ffffff",
        accent_fill="#f0f0f0",
        success_fill="#f5f5f5",
        warning_fill="#f8f8f8",
        danger_fill="#f5f5f5",
        info_fill="#f0f0f0",
        neutral_fill="#e8e8e8",

        # Typography — compact
        title_size=14,
        subtitle_size=10,
        body_size=10,
        label_size=8,
        caption_size=7,

        # Layout — thin borders
        border_width=1,
        arrow_width=1,
        default_gap=30,
        padding=4,

        border_radius=False,
        use_groups=False,
        compact_layout=True,
    )

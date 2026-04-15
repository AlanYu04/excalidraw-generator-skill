"""
Clean style preset — Minimal, precise, data-flow focused.
Thin borders, small text, black-and-white friendly, no decoration.
"""
from .base import StyleConfig


def clean_style() -> StyleConfig:
    return StyleConfig(
        name="clean",
        description="Minimal precise style focused on data flow clarity",

        # Colors — Okabe-Ito inspired, grayscale-friendly
        background="#FFFFFF",
        primary="#0072B2",
        accent="#E69F00",
        text_color="#000000",
        border_color="#000000",
        muted="#666666",

        success="#009E73",
        warning="#E69F00",
        danger="#D55E00",
        info="#56B4E9",

        primary_fill="#ffffff",
        accent_fill="#FAF3E0",
        success_fill="#E4F3EC",
        warning_fill="#FAF3E0",
        danger_fill="#FBE8E1",
        info_fill="#EAF6FB",
        neutral_fill="#e8e8e8",

        # Typography — compact
        font_family=2,
        title_size=14,
        subtitle_size=10,
        body_size=10,
        label_size=8,
        caption_size=7,

        # Layout — thin borders
        roughness=0,
        border_width=1,
        arrow_width=1,
        default_gap=30,
        padding=4,
        grid_step=10,
        spacing_policy="compact",

        border_radius=False,
        use_groups=False,
        compact_layout=True,
        allowed_arrow_modes=("straight",),
    )

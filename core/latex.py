"""
LaTeX formula rendering for Excalidraw diagrams.

Converts LaTeX math expressions to Excalidraw elements via:
  1. matplotlib mathtext → PNG base64 → image_embed (fast path)
  2. Fallback: matplotlib usetex + amsmath → PNG (full LaTeX support)
  3. Final fallback: monospace text if rendering fails

Strategy rationale: matplotlib's mathtext supports most common LaTeX math
syntax (fractions, integrals, sums, Greek letters) but not environments
like \begin{pmatrix}. When mathtext fails, we fall back to usetex which
delegates to a system LaTeX installation with amsmath loaded.

Font selection (mathtext mode only):
  - "stix"        STIX — professional/academic style, clean
  - "cm"          Computer Modern — classic LaTeX look
  - "dejavusans"  DejaVu Sans — modern, bold
  - "dejavuserif" DejaVu Serif — serif style, slim

Note: usetex mode uses LaTeX's default Computer Modern fonts, ignoring
the fontset parameter.

Change the default globally:
  import core.latex
  core.latex.DEFAULT_FONTSET = "stix"
"""

import io
import base64
from typing import List, Optional, Tuple

from . import engine

# Default mathtext fontset. Supported: "stix", "cm", "dejavusans", "dejavuserif"
DEFAULT_FONTSET = "dejavusans"

# Default rendering DPI. Higher = sharper but larger file size.
# For export to PNG images, use dpi=300 or set scale=2.0 in formula().
DEFAULT_DPI = 300


def _render_latex_to_png_base64(
    latex_str: str,
    font_size: int = 20,
    dpi: int = 150,
    fontset: str = DEFAULT_FONTSET,
) -> Optional[Tuple[str, float, float]]:
    """Render LaTeX to PNG base64 with transparent background.

    Strategy: Try mathtext first (fast, no external deps). If it fails
    with an unknown-symbol error (e.g. \begin{pmatrix}), retry via
    text.usetex which delegates to a real LaTeX installation + amsmath.

    Args:
        latex_str: LaTeX math expression.
        font_size: Font size in points.
        dpi: Rendering resolution (higher = sharper but larger).
        fontset: Mathtext fontset. One of: "stix", "cm", "dejavusans",
                 "dejavuserif".

    Returns:
        (base64_string, width_px, height_px) or None on failure.
    """
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt

        expr = latex_str.strip()
        if expr.startswith("$"):
            expr = expr.lstrip("$")
        if expr.endswith("$"):
            expr = expr.rstrip("$")
        expr = expr.strip()

        matplotlib.rcParams["mathtext.fontset"] = fontset

        # --- Pass 1: mathtext (fast path) ---
        result = _try_render(expr=expr, font_size=font_size, dpi=dpi,
                             use_tex=False)
        if result is not None:
            return result

        # --- Pass 2: usetex (full LaTeX + amsmath) ---
        result = _try_render(expr=expr, font_size=font_size, dpi=dpi,
                             use_tex=True)
        if result is not None:
            return result

        return None
    except Exception:
        return None


def _try_render(
    expr: str,
    font_size: int,
    dpi: int,
    use_tex: bool,
) -> Optional[Tuple[str, float, float]]:
    """Render one expression with or without usetex. Returns same tuple or None."""
    import matplotlib
    import matplotlib.pyplot as plt

    matplotlib.rcParams["text.usetex"] = use_tex
    if use_tex:
        matplotlib.rcParams["text.latex.preamble"] = r"\usepackage{amsmath}"

    fig, ax = plt.subplots(figsize=(0.01, 0.01))
    ax.set_axis_off()
    try:
        text_obj = ax.text(
            0.5, 0.5, f"${expr}$",
            transform=ax.transAxes,
            fontsize=font_size,
            ha="center", va="center",
        )
        fig.canvas.draw()

        renderer = fig.canvas.get_renderer()
        bbox = text_obj.get_window_extent(renderer)
        w, h = bbox.width, bbox.height

        buf = io.BytesIO()
        fig.savefig(
            buf, format="png", dpi=dpi,
            bbox_inches="tight", pad_inches=0.05,
            transparent=True,
        )
        buf.seek(0)
        img_data = base64.b64encode(buf.read()).decode("utf-8")
        return img_data, w, h
    except Exception:
        return None
    finally:
        plt.close(fig)


def formula(
    latex_str: str,
    x: float = 0,
    y: float = 0,
    font_size: int = 20,
    stroke: str = "#1e1e1e",
    stroke_width: int = 2,
    roughness: int = 0,
    scale: float = 1.0,
    dpi: int = DEFAULT_DPI,
    fontset: Optional[str] = None,
) -> List[dict]:
    """Render a LaTeX formula as an Excalidraw image element.

    Primary strategy: matplotlib renders to transparent PNG → embedded as
    base64 image. This preserves font glyphs, superscripts, fractions, etc.

    Args:
        latex_str: LaTeX math expression (e.g. "E = mc^2").
        x: X position.
        y: Y position.
        font_size: Font size in points.
        stroke: Stroke color (unused for images, kept for API compat).
        stroke_width: Stroke width (unused for images).
        roughness: Roughness (unused for images).
        scale: Scale factor for the rendered formula.
        dpi: Rendering resolution (higher = sharper but larger).
        fontset: Mathtext fontset. One of: "stix", "cm", "dejavusans",
                 "dejavuserif". Defaults to module-level DEFAULT_FONTSET.

    Returns:
        List with a single image element dict.
        The element has a '_files' key for save_excalidraw().
    """
    if fontset is None:
        fontset = DEFAULT_FONTSET

    result = _render_latex_to_png_base64(latex_str, font_size, dpi, fontset)
    if result is not None:
        img_b64, w, h = result
        w *= scale
        h *= scale
        el, files = engine.image_embed(x, y, w, h, img_b64, mime="image/png")
        el["_files"] = files
        return [el]

    # Fallback: monospace text
    return [engine.text_standalone(
        x, y, latex_str,
        fs=font_size,
        color=stroke,
        font_family=3,  # Cascadia monospace
        roughness=roughness,
    )]

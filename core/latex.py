"""
LaTeX Formula Support for Excalidraw

Uses Excalidraw's built-in LaTeX rendering (KaTeX) for native formula display.
No external dependencies required for latex_to_elements().

Two output modes:
  - latex(): Native text element with LaTeX — zero-dependency, editable
  - latex_to_image(): PNG image embed via matplotlib — pixel-perfect
"""

import base64
import io
from typing import Any, Dict, List, Optional

from . import engine


def latex(
    latex: str,
    x: float = 0,
    y: float = 0,
    fs: int = 20,
    color: str = "#1e1e1e",
    font_family: int = 1,
) -> Dict[str, Any]:
    """Create an Excalidraw text element with native LaTeX rendering.

    Uses Excalidraw's built-in KaTeX support — zero dependencies,
    formulas are editable in the Excalidraw editor.

    Args:
        latex: LaTeX formula (e.g. r"\\sum_{i=1}^{n} x_i^2").
        x: X position.
        y: Y position.
        fs: Font size.
        color: Text color.
        font_family: 1=Virgil, 2=Helvetica, 3=Cascadia.

    Returns:
        Excalidraw text element dict with LaTeX content.
    """
    txt = f"${latex}$"
    tw = max(engine.estimate_text_width(latex, fs), 50)
    th = fs * 1.5

    return {
        "id": engine.uid(), "type": "text",
        "x": x, "y": y, "width": tw, "height": th,
        "angle": 0, "strokeColor": color, "backgroundColor": "transparent",
        "fillStyle": "solid", "strokeWidth": 2, "strokeStyle": "solid",
        "roughness": 0, "opacity": 100, "groupIds": [],
        "roundness": None, "seed": engine.sd(), "version": 1,
        "versionNonce": engine.sd(), "isDeleted": False, "boundElements": [],
        "updated": engine.ts(), "link": None, "locked": False,
        "text": txt, "fontSize": fs, "fontFamily": font_family,
        "textAlign": "left", "verticalAlign": "top",
        "containerId": None, "originalText": txt, "lineHeight": 1.25,
    }


def latex_to_elements(
    latex_str: str,
    x: float = 0,
    y: float = 0,
    scale: float = 1.0,
    stroke: str = "#1e1e1e",
    roughness: int = 0,
    fontsize: int = 20,
    **kwargs,
) -> List[Dict[str, Any]]:
    """Create a native LaTeX text element for Excalidraw.

    Convenience wrapper around latex() that returns a list for API
    compatibility.

    Args:
        latex_str: LaTeX formula string.
        x: X position.
        y: Y position.
        scale: Font size multiplier.
        stroke: Text color.
        roughness: Ignored (LaTeX uses crisp rendering).
        fontsize: Base font size.

    Returns:
        List containing one text element dict.
    """
    fs = int(fontsize * scale)
    return [latex(latex_str, x=x, y=y, fs=fs, color=stroke)]


def _render_latex_png(
    latex: str,
    fontsize: int = 20,
    color: str = "#1e1e1e",
    dpi: int = 200,
    bg: str = "white",
) -> bytes:
    """Render LaTeX to PNG bytes via matplotlib.

    Requires matplotlib (pip install matplotlib).
    """
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    plt.rcParams["text.usetex"] = False

    fig, ax = plt.subplots(figsize=(4, 1.5), dpi=dpi)
    ax.set_axis_off()
    fig.patch.set_facecolor(bg)

    ax.text(
        0.5, 0.5, f"${latex}$",
        fontsize=fontsize, color=color,
        ha="center", va="center",
        transform=ax.transAxes,
    )

    buf = io.BytesIO()
    fig.savefig(
        buf, format="png",
        bbox_inches="tight",
        facecolor=bg, edgecolor="none",
        pad_inches=0.05,
    )
    plt.close(fig)

    return buf.getvalue()


def latex_to_image(
    latex: str,
    x: float = 0,
    y: float = 0,
    width: float = 200,
    height: float = 75,
    fontsize: int = 20,
    color: str = "#1e1e1e",
    bg: str = "white",
    dpi: int = 200,
) -> List[Dict[str, Any]]:
    """Convert a LaTeX formula to an embedded image element.

    Renders via matplotlib to PNG, then embeds as base64 image.
    Requires matplotlib (pip install matplotlib).

    Args:
        latex: LaTeX formula string.
        x: X position.
        y: Y position.
        width: Display width in Excalidraw.
        height: Display height in Excalidraw.
        fontsize: Font size for rendering.
        color: Text color.
        bg: Background color.
        dpi: Rendering DPI.

    Returns:
        List containing the image element dict and files dict entry.
    """
    png_bytes = _render_latex_png(
        latex, fontsize=fontsize, color=color, bg=bg, dpi=dpi,
    )
    b64 = base64.b64encode(png_bytes).decode("ascii")

    el, file_entry = engine.image_embed(x, y, width, height, b64, mime="image/png")
    return [el, file_entry]

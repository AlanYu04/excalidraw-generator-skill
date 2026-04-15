---
title: LaTeX Formulas
---

# LaTeX Formulas

Render LaTeX math expressions as Excalidraw image elements. Uses matplotlib for rendering with automatic fallback from mathtext to full LaTeX.

## `formula`

```python
from core.latex import formula

elements = formula(
    r"E = mc^2",
    x=100, y=50,
    font_size=20,
    stroke="#1e1e1e",
    stroke_width=2,
    roughness=0,
    scale=1.0,
    dpi=300,
    fontset=None,
)
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `latex_str` | `str` | required | LaTeX math expression (e.g. `"E = mc^2"`) |
| `x` | `float` | `0` | X position |
| `y` | `float` | `0` | Y position |
| `font_size` | `int` | `20` | Font size in points |
| `stroke` | `str` | `"#1e1e1e"` | Stroke color (for text fallback) |
| `stroke_width` | `int` | `2` | Stroke width (for text fallback) |
| `roughness` | `int` | `0` | Roughness (for text fallback) |
| `scale` | `float` | `1.0` | Scale factor for the rendered formula |
| `dpi` | `int` | `300` | Rendering resolution (higher = sharper but larger) |
| `fontset` | `str \| None` | `None` | Mathtext fontset, defaults to module-level `DEFAULT_FONTSET` |

Returns: `list[dict]` -- a single-element list containing an Excalidraw image element with embedded base64 PNG data. If rendering fails, falls back to a monospace text element.

## Rendering Strategy

The formula renderer uses a two-pass approach:

1. **Pass 1: Mathtext** (fast, no external dependencies) -- Handles most common LaTeX math syntax including fractions, integrals, sums, limits, Greek letters, square roots, and subscripts/superscripts.

2. **Pass 2: usetex** (full LaTeX + amsmath) -- Activated automatically when mathtext encounters unsupported commands. Requires a system LaTeX installation with `pdflatex` and the `amsmath` package.

3. **Final fallback** -- If both passes fail, renders the raw LaTeX string as monospace text.

## Font Options

Control the mathtext font via the `fontset` parameter or the module-level default:

```python
import core.latex

# Change default globally
core.latex.DEFAULT_FONTSET = "stix"

# Or per-formula
elements = formula(r"\alpha + \beta = \gamma", x=100, y=150, fontset="stix")
```

| Fontset | Name | Style |
|---------|------|-------|
| `"stix"` | STIX | Professional/academic, clean |
| `"cm"` | Computer Modern | Classic LaTeX look |
| `"dejavusans"` | DejaVu Sans | Modern, bold (default) |
| `"dejavuserif"` | DejaVu Serif | Serif style, slim |

Note: When using usetex mode (Pass 2), LaTeX's default Computer Modern fonts are used and the `fontset` parameter is ignored.

## Supported Syntax

**Mathtext (Pass 1):**
- Fractions: `\frac{a}{b}`
- Integrals: `\int`, `\iint`, `\iiint`
- Sums and products: `\sum`, `\prod`
- Limits: `\lim`, `\min`, `\max`
- Greek letters: `\alpha`, `\beta`, `\gamma`, etc.
- Square roots: `\sqrt{x}`, `\sqrt[n]{x}`
- Subscripts and superscripts: `x_i`, `x^2`
- Standard operators: `\leq`, `\geq`, `\neq`, `\times`, `\div`

**usetex fallback (Pass 2) -- environments:**
- `\begin{pmatrix}`, `\begin{bmatrix}`, `\begin{vmatrix}`
- `\begin{array}`
- `\begin{cases}`
- `\begin{smallmatrix}`

usetex mode requires a LaTeX installation (`pdflatex` + `amsmath` package).

## Examples

### Simple Formula

```python
from core.latex import formula
from core.engine import save

el = formula(r"E = mc^2", x=100, y=50, font_size=20)
save("physics.excalidraw", el)
```

### Complex Formula with Matrix

```python
from core.latex import formula
from core.engine import save, rect

# Automatically falls back to usetex for pmatrix
el = formula(
    r"\begin{pmatrix} a & b \\ c & d \end{pmatrix}",
    x=100, y=100,
    font_size=14,
)

save("matrix.excalidraw", el)
```

### Multiple Formulas with Different Fonts

```python
from core.latex import formula
from core.engine import save

stix = formula(r"\alpha + \beta = \gamma", x=100, y=50, fontset="stix")
cm = formula(r"\alpha + \beta = \gamma", x=100, y=120, fontset="cm")
dejavu = formula(r"\alpha + \beta = \gamma", x=100, y=190, fontset="dejavusans")

save("font-comparison.excalidraw", [*stix, *cm, *dejavu])
```

### Changing the Global Default

```python
import core.latex
core.latex.DEFAULT_FONTSET = "stix"

# All subsequent formula() calls use STIX unless overridden
from core.latex import formula
el = formula(r"\sum_{i=1}^{n} i = \frac{n(n+1)}{2}", x=50, y=50)
```

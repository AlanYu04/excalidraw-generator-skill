# Journal Style Prompt Guidelines

## Visual Identity

Journal papers (IEEE Transactions, Nature, Science) require rigorous, compact figures that survive black-and-white printing and look professional in double-column layouts.

## Layout Rules

- **Ultra-compact**: Minimum margins, tight element spacing
- **Grid alignment**: 10px grid snap
- **Column-aware**: Design for single-column (8.5cm) or double-column (17cm)
- **No decorative elements**: Every element must carry information

## Color Rules

- Use the **Okabe-Ito colorblind-safe palette**:
  - Blue `#0072B2`, Orange `#E69F00`, Green `#009E73`, Red `#D55E00`
  - Purple `#CC79A7`, Sky blue `#56B4E9`, Yellow `#F0E442`
- Colors must be distinguishable in grayscale (test by desaturating)
- Background: pure white `#FFFFFF`
- Avoid red-green combinations

## Typography Rules

- Font: Helvetica/Arial equivalent (`fontFamily: 2`)
- Title: 16pt, body: 10pt, labels: 8pt, captions: 7pt
- **Minimum legible text**: 7pt at print scale
- Prefer abbreviations with a legend over long labels

## Shape Rules

- All borders: 0.5-1pt solid lines
- `roughness: 0` (precise, no hand-drawn effect)
- No rounded corners
- Prefer plain rectangles with thin borders
- Use hatching or patterns for fills if grayscale compatibility is critical

## Arrow Rules

- Arrow width: 1pt
- Prefer straight arrows
- Use arrow labels for dimensions and data types (e.g., "s_t ∈ R¹¹")
- Keep arrow paths as short as possible

## Common Patterns

### System Block Diagram
Tight grid of labeled rectangles with thin arrows. Each block shows:
module name + key formula + dimension annotation.

### Comparison Table
Header row with gray fill, data rows alternating white/light gray.
Thin borders throughout.

### Signal Processing Chain
Horizontal pipeline of narrow boxes showing each processing step.
Annotate data dimensions between steps.

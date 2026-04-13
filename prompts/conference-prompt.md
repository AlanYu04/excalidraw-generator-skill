# Conference Style Prompt Guidelines

## Visual Identity

Conference papers (CVPR, ICML, ICLR, NeurIPS, AAAI) demand minimalist, precise figures that communicate architecture and data flow clearly at small print sizes.

## Layout Rules

- **Grid alignment**: All elements must snap to an invisible grid (20px minimum)
- **Orthographic arrows**: Only 90-degree angles, no diagonal arrows
- **No wasted space**: Compact layout, minimal padding between elements
- **Single-column width**: Design for 8.5cm width, scalable to full-page

## Color Rules

- Primary: academic blue `#2B5B84` to `#4A90E2`
- Accent: coral/orange `#E67E22` only for novel contributions or key findings
- Data flow: cool gray `#D5DBDB` or light teal `#73C6B6`
- Background: pure white `#FFFFFF`
- NEVER use neon colors, gradients, or 3D effects

## Typography Rules

- Font: Helvetica/Arial equivalent (`fontFamily: 2`)
- Title: 20pt, body: 12pt, labels: 10pt, captions: 9pt
- All text must be legible at 50% zoom
- Use `\n` for multi-line labels, not multiple text elements

## Shape Rules

- Rectangles: no border radius, `roughness: 0`
- Borders: 1.5pt solid lines
- Dashed borders only for module boundaries or optional components
- Ellipses: only for mathematical operations or loss functions
- Diamonds: only for decision/gating mechanisms

## Arrow Rules

- Straight lines only, no curved or elbowed arrows
- Arrow width: 1.5pt
- Use labels on arrows sparingly — prefer numbered badges
- Bidirectional arrows should use two separate arrows, not double heads

## Common Patterns

### Architecture Diagram
```
[Input] → [Module A] → [Module B] → [Loss]
              ↓             ↓
          [Shared]      [Output]
```

### Data Flow Pipeline
```
[Raw Data] → [Preprocess] → [Feature Extract] → [Classifier] → [Result]
```

### Ablation Table
Use labeled_rect grid with thin borders, alternating white/light-gray fills.

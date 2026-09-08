# Pastel ML Style: Modern Airy Preset

Adapted from `academic-figure-prompt-pastel` in
[LigphiDonk/academic-figure-generator](https://github.com/LigphiDonk/academic-figure-generator)
(MIT License). The upstream author reports these rules survived 7 rounds of
generation-and-review iteration.

An opt-in second preset for the VISUAL STYLE and COLOR PALETTE sections of the
6-section prompt contract in `SKILL.md`. The flat minimal systems style stays
the default; use this preset when the target venue is a modern ML conference
(ICLR / NeurIPS / ICML, 2024-2025 look) or the user asks for a pastel / airy /
"modern ML" figure.

## How it plugs into the 6-section contract

| Section | What changes |
|---------|--------------|
| FRAMING | "in the modern style of top-tier ICLR/NeurIPS 2024-2025 publications"; adjectives: warm, approachable, airy |
| VISUAL STYLE | replace the default minimal-systems block with the style rules and global block below |
| COLOR PALETTE | use palette P1-P3 below, or user-supplied |
| LAYOUT / CONNECTIONS / CONSTRAINTS | unchanged |

All standing rules still apply: SPELL EXACTLY, three attempts with selection,
arrow-continuity and cross-view-consistency locks, no figure numbers.

## Five style rules

1. **Pure white canvas + white panels + faint shadow.** Canvas is flat
   `#FFFFFF`, with no gradient, no tint, no grey. Panels are white `#FFFFFF`
   rounded rectangles (radius ~20px) lifted only by a soft drop-shadow
   (3px blur, 1px y-offset, rgba(0,0,0,0.06)). Never distinguish panels with
   grey fills or borders; the shadow is the only separator.
2. **Rounded friendly font.** Nunito / Poppins / Quicksand / Comfortaa,
   with rounded letter terminals, not angular Helvetica/Arial. Titles semi-bold to
   bold (600-700) ~16-18pt; body regular (400) ~10-11pt; math in italic serif
   (Computer Modern / STIX). The font is the single strongest style marker.
3. **Packed but uncluttered.** Every panel is filled with content (tokens,
   curves, formulas, icons, arrows) at a consistent 8-12px micro-spacing.
   No dead space, no overlap, no text walls.
4. **Floating elements, no nested boxes.** Elements sit directly on the white
   panel surface. No box-in-box nesting. Concept names go in faint pill-shaped
   badges.
5. **Color rides on tokens, text, and curves, never on panels.** Small rounded
   token squares (10-14px, pastel fill + 1px slightly darker border), colored
   keyword text in semantic colors, pastel curve strokes. Canvas and panels
   stay white.

## Five color carriers

| Carrier | Description pattern |
|---------|---------------------|
| Token square | `soft blue #BBDEFB square with 1px #90CAF9 border, "s₁" label` |
| Colored keyword | `bold coral #E05555 text "Exciter"` |
| Pill badge | `faint green-tinted pill badge "Random Forest"` |
| Curve stroke | `sigmoid curve in warm amber #DAA520 line` |
| Leaf dots | `5 tiny circles in blue, pink, amber, purple, green` |

## Preset palettes

| # | Name | Token fills | Text emphasis |
|---|------|-------------|---------------|
| P1 | Warm ML | pink `#FFD0D0` · blue `#BBDEFB` · amber `#FFF3C4` · purple `#E1BEE7` · green `#C8E6C9` | coral `#E05555` · teal `#1A9988` · purple `#6A5ACD` · green `#3A8F3A` |
| P2 | Cool Research | blue `#B3E5FC` · indigo `#C5CAE9` · grey-blue `#CFD8DC` · teal `#B2DFDB` · lavender `#D1C4E9` | navy `#1565C0` · indigo `#3949AB` · teal `#00897B` |
| P3 | Earthy Warm | cream `#FFE0B2` · taupe `#D7CCC8` · sage `#C8E6C9` · grey `#E0E0E0` · tan `#EFEBE9` | brown `#6D4C41` · olive `#827717` · forest `#2E7D32` |

Token squares always carry a 1px border slightly darker than their fill.

## Layout flexibility

2-5 panels sized by content weight, ~20px gaps. The main-flow panel may be
large, detail panels small. Do not force a symmetric 2×2 grid; asymmetric 1+2,
three-panel, or a horizontal strip are all legitimate. Use an equal 2×2 only
when the content is genuinely symmetric.

## Prompt blocks

Global block (goes at the top of the VISUAL STYLE section):

```text
CANVAS: Pure flat white (#FFFFFF). No gradient, no tint, no grey.
PANELS: [N] large rounded-rectangle panels (radius ~20px) with white (#FFFFFF)
fill and very subtle soft drop-shadow (3px blur, 1px y-offset, rgba(0,0,0,0.06)).
Panels sit on the white canvas, distinguished only by their barely-perceptible
shadow.
FONT: Friendly rounded geometric sans-serif (Nunito / Poppins / Quicksand).
Titles semi-bold to bold (600-700), ~16-18pt. Body regular (400), ~10-11pt.
Math in italic serif (Computer Modern). Warm, approachable, modern feel.
CONTENT DENSITY: Panels are FILLED with content (tokens, curves, formulas,
icons, arrows) with consistent 8-12px micro-spacing. "Thoughtfully packed",
not "sparse".
NO NESTED BOXES: Elements float directly on white panel surfaces. Only
pill-shaped labels for concept names.
```

Per-panel block (one per panel in the LAYOUT section):

```text
=== PANEL: [name] ===
White panel, subtle shadow, rounded corners ~20px.
Title: Bold [color] rounded font "[title]" (~18pt).
Content (packed, floating elements):
  [element descriptions...]
```

Closing style block (end of prompt):

```text
=== STYLE SPECIFICATIONS ===
Canvas: Pure white #FFFFFF. No gradient.
Panels: White #FFFFFF, radius ~20px, soft shadow (3px blur, rgba(0,0,0,0.06)).
Font: Rounded sans-serif (Nunito/Poppins/Quicksand). Titles bold ~16-18pt,
body regular ~10pt, math italic serif. NOT angular Helvetica.
Density: Panels FILLED with content. 8-12px micro-spacing. No dead space.
Structure: Floating elements on white panels. No nested boxes.
Token colors (with 1px darker border): [semantic]: [fill] / [border] / [emphasis]
Arrows: 1-1.5px dark grey #555, neat arrowheads. Some curved.
Pill labels: Faint pastel tint + thin matching border, rounded ~8px.
Colored text: Concept names in semantic colors.
No 3D, no gradients on elements, no heavy shadows. Flat vector.
```

## Element vocabulary

Token squares:

| Use | Description |
|-----|-------------|
| State / input | `soft blue #BBDEFB square, 1px #90CAF9 border, "s₁" label` |
| Action / prediction | `soft pink #FFD0D0 square, 1px #EF9A9A border, "a₁" label` |
| Feature / statistic | `soft purple #E1BEE7 square, 1px #CE93D8 border` |
| Reward / output | `soft green #C8E6C9 square, 1px #A5D6A7 border` |
| Metric / math | `soft amber #FFF3C4 square, 1px #FFE082 border` |

Curves and mini-charts:

| Type | Description |
|------|-------------|
| Loss curve | `descending curve in coral #E05555 line, tiny grey axes` |
| Sigmoid | `sigmoid curve in warm amber #DAA520 line` |
| Spectrum | `bar spectrum with 6 bars in soft pink, varying heights` |
| Distribution | `5 colored bar segments of varying widths` |
| Oscillation | `oscillating wave in amber line` |

Inline illustrations:

| Type | Description |
|------|-------------|
| Cycle | `4-node cycle: "A"→"B"→"C"→"D" in tiny colored text with curved arrows` |
| Network | `input bars → hidden layers with dot connections → output, thin grey lines` |
| Decision tree | `binary branching tree, grey lines, colored circle leaf nodes` |
| Trajectory fan | `multiple curves fanning out from a point, solid mean + dashed bounds` |
| Pyramid | `3 levels of increasing width, converging to ⊕ fusion` |
| Compression funnel | `wide dot cluster → converging lines → narrow column of tokens` |

## Quality checklist

- [ ] Canvas is `#FFFFFF`, no gradient, no grey tint
- [ ] Panels are `#FFFFFF`, lifted by soft shadow only, no grey fills
- [ ] Font named as Nunito/Poppins/Quicksand, not Helvetica
- [ ] Every panel filled (tokens + curves + formulas + icons), no dead space
- [ ] 8-12px micro-spacing, no overlap
- [ ] No box-in-box nesting; floating elements only
- [ ] Concept names in faint pill badges
- [ ] Keywords in semantic colors (coral / teal / purple / green)
- [ ] Token squares have pastel fill + 1px darker border
- [ ] Rich inline illustrations (curves, trees, networks), not just squares
- [ ] Formulas in italic serif, floating on panels
- [ ] Overall reads like a 2024-2025 ICLR oral figure, warm and approachable

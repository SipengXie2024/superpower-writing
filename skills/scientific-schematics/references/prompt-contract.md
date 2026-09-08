# Prompt contract for raster figures

The quality of a generated figure tracks the quality of the prompt. A flat
one-paragraph description produces a generic corporate diagram: rounded blue
gradient boxes with drop shadows. The named structure below forces the style,
the canvas, and every label to be fixed before generation.

## Contents

- The six sections
- Label, novelty, canvas, and icon rules
- Two standing rules: spell exactly, three attempts
- Anti-AI-look color rules
- Thumbnail vocabulary
- Prompt locks for complex figures
- Worked example (verified)
- Pastel preset

## The six sections

Write the prompt file as six named sections in this order.

1. **FRAMING (about 5 lines).** "A flat-vector technical diagram for a
   `<venue>` paper, in the visual language of DeepMind and OpenAI paper figures.
   It should feel `<adjectives: clean, authoritative, minimal>`." Name the venue
   (NeurIPS / ICLR / OSDI / NSDI / SOSP) so the tone matches, and state the
   canvas shape here (see the canvas rule below).
2. **VISUAL STYLE (about 20 to 30 lines), the most important section.**
   Describe line quality, fills, corner radius, shadow, arrow weight,
   typography, and whitespace concretely. Default for systems and ML papers: a
   flat, minimal, pure-white style (no gradients, no 3D, no shadows, thin
   dark-grey arrows, sans-serif labels inside boxes). Pick one style and keep it
   identical across every figure in the paper. For modern ML venues a second
   preset exists, the pastel airy style of 2024-2025 papers: read
   `style-pastel-ml.md` and use its blocks for VISUAL STYLE and COLOR PALETTE.
3. **COLOR PALETTE (about 10 lines).** Exact hex codes for every color. Soft
   pastel fills with a slightly darker border of the same hue, one accent per
   logical group, at most three hues plus greys. No saturated reds or greens, no
   dark heavy fills.
4. **LAYOUT (50 to 150 lines).** Every component, box, and zone with its exact
   text and spatial arrangement. Be exhaustively specific about positions and
   grouping. Name which module is the hero.
5. **CONNECTIONS (30 to 80 lines).** Every arrow individually: source, target,
   style (solid / dashed), label, and routing direction.
6. **CONSTRAINTS (about 10 lines).** What NOT to include: no figure number, no
   caption, no title, no clip art, no 3D, no photographic texture, no sketchy
   lines, no decorative gradients, no words beyond the label list.

## Label, novelty, canvas, and icon rules

- **Labels name modules; they never explain them.** Text in the figure
  identifies a component ("Encoder", "Loss", "Evidence Gate"). It never carries
  a sentence, a descriptive paragraph, or a complex formula. Mechanism belongs
  in the caption and the body text. Put this in CONSTRAINTS verbatim: "Labels
  name modules only; no sentences, no explanatory text, no formulas."
- **Highlight the core novelty.** Decide which one module carries the paper's
  contribution and give it the single visual distinction: a thicker border, the
  one accent color, or the central position. Every other module stays quiet.
  Say so in LAYOUT ("the hero module") and in COLOR PALETTE.
- **State the canvas shape in FRAMING.** The subscription backend ignores the
  `size` parameter and chooses its own canvas from the content; a left-to-right
  pipeline came back as a 3:1 strip. Write "wide 3:1 strip", "3:2 landscape",
  or "square" in FRAMING, and make the LAYOUT consistent with it (a single row
  for a strip, stacked rows or panels for a landscape).
- **Icons only where they aid recognition.** A small monochrome icon inside a
  module (document stack for a retriever, database cylinder for an index,
  shield for a verifier, network graph for a model) makes the module readable
  at a glance. Never add icons as decoration, and never let an icon replace the
  text label.

## Two standing rules

- **SPELL EXACTLY.** Raster generators can misspell and rearrange dense text.
  List every label verbatim in CONSTRAINTS and add the literal line "SPELL ALL
  LABELS EXACTLY AS WRITTEN, do not rephrase or abbreviate. Do not add any other
  words." This is the single most common avoidable defect, and the line costs
  nothing.
- **Three attempts, then select.** The same prompt yields visibly different
  quality on each run. Generate three (`--count 3`), read all three, keep the
  best. Then fix the chosen one with `edit`, at most three targeted rounds.

## Anti-AI-look color rules

The fastest tell of a machine-generated figure is color overuse. Bake these
substitutions into VISUAL STYLE and COLOR PALETTE (table and thumbnail
vocabulary adapted from LigphiDonk/academic-figure-generator, MIT):

| Avoid | Use instead |
|-------|-------------|
| 4-5 colored background panels | white-dominant + faint grey grouping |
| Saturated header banner bars | small-caps text labels + thin grey divider |
| A different fill color per module | white or one pastel fill per logical group, color on borders |
| Full-color embedded thumbnails | monochrome or 2-color thumbnails |
| 5+ colors in one figure | at most 3 colors + greys |
| Rainbows / gradients | flat solid colors |

## Thumbnail vocabulary

Dense conference figures embed small monochrome visualizations inside module
boxes. When writing LAYOUT, pull phrases from this table instead of leaving
boxes as empty labeled rectangles:

| Data type | Prompt phrase |
|-----------|---------------|
| Time series | `a small time-series waveform thumbnail` |
| Frequency spectrum | `a small frequency spectrum bar chart thumbnail` |
| Attention map | `a small monochrome attention heatmap grid thumbnail` |
| Trajectory | `a small 3D orbital trajectory curve thumbnail` |
| Probability distribution | `a small probability distribution bar chart thumbnail` |
| Decision tree | `a small decision tree branching diagram thumbnail` |
| Confusion matrix | `a small confusion matrix heatmap thumbnail` |
| Network layer | `a small neural network layer diagram thumbnail` |
| Feature vector | `a small horizontal feature vector bar visualization` |
| Scatter | `a small scatter plot with cluster coloring thumbnail` |
| Receptive field | `a progressively larger receptive field grid icon` |
| Convolution kernel | `a small convolution filter kernel grid thumbnail` |
| Gradient flow | `a small gradient flow direction arrow diagram` |
| Loss curve | `a small training loss convergence curve thumbnail` |
| ROC curve | `a small ROC curve with AUC shading thumbnail` |
| Image sample | `a small example image/photo thumbnail` |
| Point cloud | `a small 3D point cloud visualization thumbnail` |
| Spatial heatmap | `a small spatial heatmap overlay thumbnail` |

## Prompt locks for complex figures

Two failure modes recur on multi-view figures and slip past visual review, so
prevent them in the prompt.

**Cross-view consistency.** When one conceptual entity (a data layout, a fixed
mapping, an enum partition) appears across multiple views, a plain prompt lets
the model re-invent its specifics per view. Define the entity once in a block
at the top; later views reference it:

```text
== CRITICAL CONSISTENCY ==
The contract has exactly 3 PUSH positions: PUSH 1 = variant, PUSH 2 = invariant
(value 0xCC), PUSH 3 = variant. This 1-invariant + 2-variant split must hold in
every view where it appears.
```

**Arrow continuity.** "An arrow goes from A, crosses the divider, and reaches B"
can render as two disconnected stubs. Mandate single-polyline continuity, and
for long spans specify the path geometry:

```text
== CRITICAL ARROW CONTINUITY ==
Every arrow must be a single continuous unbroken polyline from its source box to
an arrowhead at its target box. No gaps, breaks, or detached segments. Bends are
allowed at right angles but each bend is one connected joint, not two separate
arrows.
```

## Worked example (verified)

This prompt produced a clean figure on the first gpt-image-2 attempt on
2026-09-08: all eight labels exact, pastel fills as specified, the hero module
visibly distinct, icons inside three modules, the dashed loop drawn. A follow-up
`edit` call renaming one label changed nothing else. Use it as the template.

```text
FRAMING
A flat-vector technical architecture diagram for a NeurIPS paper. Clean,
authoritative, minimal, in the visual language of DeepMind and OpenAI paper
figures. Wide 3:1 strip.

VISUAL STYLE
Pure white background (#FFFFFF), no texture, no gradient, no shadow. Flat vector
illustration: thin 1.5px dark-grey (#4A4A4A) outlines, rounded rectangles
(radius 8px) with soft pastel fills, thin dark-grey arrows with small solid
arrowheads. Sans-serif labels (Helvetica-like), all text horizontal, high
contrast, generous whitespace. No 3D, no photorealism, no sketchy lines, no
clip-art.

COLOR PALETTE
Input/output boxes: pale blue fill #DCEBFA with border #7FA8D6. Retrieval
modules: pale green fill #DFF2E1 with border #7CB88A. The novel module
"Evidence Gate": pale amber fill #FFF1CC with border #D9A93F and a slightly
thicker 2.5px border so it stands out. Arrows: #4A4A4A. Text: #222222. At most
these 3 pastel colors plus greys.

LAYOUT (left to right, single row, evenly spaced)
1. Left: a rounded box labeled "Query" (pale blue).
2. A rounded box labeled "Retriever" (pale green) with a small monochrome
   document-stack icon inside.
3. Below the Retriever, a cylinder labeled "Vector Index" (pale green)
   connected upward to the Retriever.
4. A rounded box labeled "Top-k Docs" (pale green).
5. Center-right, the hero module: a rounded box labeled "Evidence Gate" (pale
   amber, thicker border) with a small monochrome shield-check icon inside.
6. A rounded box labeled "LLM Generator" (pale blue) with a small monochrome
   neural-network icon inside.
7. Right: a rounded box labeled "Answer" (pale blue).

CONNECTIONS
Solid arrows left to right: Query -> Retriever -> Top-k Docs -> Evidence Gate
-> LLM Generator -> Answer. A short double-headed arrow between Vector Index
and Retriever. One dashed arrow from Evidence Gate curving back to Retriever
labeled "re-query". Every arrow is a single continuous polyline ending in an
arrowhead on its target box.

CONSTRAINTS
All text in English. Labels name modules only; no sentences, no explanatory
text, no formulas. No figure number, no caption, no title. SPELL ALL LABELS
EXACTLY AS WRITTEN: Query, Retriever, Vector Index, Top-k Docs, Evidence Gate,
LLM Generator, Answer, re-query. Do not add any other words.
```

Edit prompt used afterwards:

```text
Rename the label "Top-k Docs" to "Top-k Passages". Keep every other element,
color, position, icon, arrow, and label exactly as in the input image. Same
white background, same flat vector style, same aspect ratio.
```

## Pastel preset

`style-pastel-ml.md` is the opt-in modern-ML preset (ICLR / NeurIPS 2024-2025
airy look): white panels lifted by a faint shadow, rounded friendly font,
packed content, color on tokens and text rather than panels. It replaces the
VISUAL STYLE and COLOR PALETTE sections; LAYOUT, CONNECTIONS, and CONSTRAINTS
are unchanged, and both standing rules still apply.

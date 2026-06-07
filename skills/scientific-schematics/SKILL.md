---
name: scientific-schematics
description: Generate scientific figures as raster PNG via Codex's native image_gen (collaborating-with-codex bridge). Two roles — (1) design exploration, generating several diverse direction drafts in parallel for the user to pick from; the chosen draft is either used directly (manuscript, slides/PPT rework) or handed to tikz-figures as a replication reference, at the user's choice; (2) final raster output for pictorial figures (lighting/texture/3D/hand-drawn concept art, graphical abstracts) or whenever the user prefers a polished PNG. Codex runs its imagegen-scientific-schematics skill for design and visual review; this skill supplies the writing-side entry point, prompt guidance, and publication checklist.
allowed-tools: Read Write Edit Bash
license: MIT license
metadata:
    skill-author: K-Dense Inc.
---

# Scientific Schematics and Diagrams

## Overview

Scientific schematics turn complex concepts into clear visual representations for
publication. **Generation is delegated to Codex's built-in `image_gen` tool** through
the `superpower-writing:collaborating-with-codex` bridge. Codex runs its own
`imagegen-scientific-schematics` skill, which wraps `image_gen` in a figure-design and
visual-review protocol.

There is no local image CLI, no OAuth login, and no build step. Claude has no native
image tool, so the actual raster generation happens inside Codex. This skill is the
writing-side entry point: it decides *what* figure is needed, writes a strong delegation
prompt, hands off to Codex, and verifies the result against publication standards.

**How it works:**
- You describe the diagram and its hard constraints (labels, arrows, zones, colors).
- Codex generates the image with `image_gen`, reviews it visually, and iterates.
- Codex saves the final PNG into the manuscript's `figures/` directory.
- You verify the saved file and reference it in the paper.

**Supported figure modalities for systems papers.** This skill covers raster schematics
via Codex `image_gen`. For other modalities choose the right tool: TikZ/pgfplots for
in-LaTeX vector graphics that must stay in sync with manuscript styling; matplotlib and
seaborn for scripted statistical plots (use `superpower-writing:scientific-visualization`);
plotly for interactive HTML; Inkscape SVG for hand-drawn vector diagrams. Use Codex
`image_gen` for architecture/pipeline/conceptual diagrams where visual polish matters more
than editable vector source.

## When to Use This Skill

This skill plays two distinct roles. Decide which one applies before invoking.

**Role 1 — Design exploration (on demand).** When the design direction of a figure is
unclear — a novel figure type with no obvious layout, several plausible ways to organize
the information, or the user explicitly asks to "explore directions" — use `image_gen`
as a fast divergent sketcher: generate **3 direction drafts in parallel** (different
layouts / information organization, not color variants), show all three to the user,
and let them pick. After picking, the user also chooses the delivery form: use the PNG
directly (in the manuscript, or as material for a slides/PPT rework), iterate it to
final quality in the same Codex session, or hand it to
`superpower-writing:tikz-figures` as a replication reference (`ref.png`) for a vector
rendition. See "Exploration Mode" below.

**Role 2 — Final raster output.** When the deliverable is a PNG:
- Illustrative concept art with lighting, texture, 3D rendering, or hand-drawn style
- Photorealistic or semi-realistic scene compositions
- Graphical abstracts with strong pictorial elements
- Any figure where the user prefers a polished PNG over vector source

**Routing for everything else:** routine structural diagrams with a clear design
(architecture diagrams, flowcharts, pipelines, sequence diagrams) default to
`superpower-writing:tikz-figures` — its own two-candidate preview covers the layout
choice, and vector source keeps formulas and fonts consistent with the body text.
That is a default, not a rule: a high-quality `image_gen` PNG is a legitimate
deliverable whenever the user prefers it. For data plots (CDFs, training curves,
ablation bars, speedups, Pareto fronts) use
`superpower-writing:scientific-visualization` instead.

## Exploration Mode (Role 1)

1. Write one shared figure brief (components, labels, flow), then derive **3 prompts
   that differ in layout or information organization** — e.g. horizontal pipeline vs
   layered stack vs central-hero-with-panels. Style/color variants do not count as
   directions.
2. Dispatch all 3 as **parallel background bridge calls in one message** (each with
   `run_in_background: true` and a distinct output path
   `.writing/figures/explore/<slug>-{a,b,c}.png`).
3. When all return, Read the three PNGs, show them to the user, and ask which direction
   to develop (AskUserQuestion, one option per draft with a one-line layout summary).
4. Ask the user how to develop the chosen draft (same AskUserQuestion or a follow-up):
   - **Use the PNG directly** — iterate it to final quality in the same Codex session
     (`SESSION_ID` continuation), move it to `.writing/figures/<slug>.png`, reference
     with `\includegraphics`. Also the right choice when the user plans a manual
     slides/PPT rework from it.
   - **Vector rendition** — hand off to `superpower-writing:tikz-figures` with the
     chosen PNG as the replication reference. This satisfies tikz-figures'
     two-candidate requirement (its 复刻 exemption applies); `figure-diff.py` SSIM
     verifies the TikZ rendition against the chosen draft.
5. Keep all drafts under `.writing/figures/explore/` until the figure ships — the
   runner-up directions often get revisited.

**Graphical abstracts are OPTIONAL.** Systems papers typically do not include one.
Generate only when the venue explicitly requests it.

## How to Generate a Diagram

Delegate to Codex through the bridge. The bridge script lives at
`${CLAUDE_PLUGIN_ROOT}/skills/collaborating-with-codex/scripts/codex_bridge.py`.

**Mandatory:** invoke the bridge via the Bash tool with `run_in_background: true`.
Codex calls block 60–120s; a foreground call freezes the session. See
`superpower-writing:collaborating-with-codex` for the full bridge contract.

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/skills/collaborating-with-codex/scripts/codex_bridge.py \
  --cd "<project_root>" \
  --PROMPT "Use your imagegen-scientific-schematics skill to generate <enriched diagram \
  description>. Save the final selected PNG to .writing/figures/<slug>.png and report the \
  absolute saved path."
```

Then:
1. Wait for the background bridge call to return (do not poll — you are notified).
2. Confirm the PNG exists at the reported path and Read it to inspect quality.
3. If a gate fails (misspelled label, broken arrow, crowding), continue the **same**
   Codex session with its `SESSION_ID` and one targeted fix per iteration.
4. Reference the figure in the manuscript with `\includegraphics`.

Codex saves generated images under `~/.codex/generated_images/<session>/` by default and
only copies the selected one into the workspace when the prompt asks. Always give an
explicit in-project output path, or the asset is stranded outside the repo.

## Writing the Delegation Prompt

The quality of the figure tracks the quality of the prompt. Prepend these scientific
guidelines to the user's diagram description before handing it to Codex.

**Visual quality:** clean white/light background, high contrast, sharp lines and text,
generous spacing, publication-ready, no decorative clutter.

**Typography:** clear sans-serif fonts (Arial/Helvetica style), consistent sizing,
all text horizontal and readable, no overlaps.

**Scientific standards:** accurate representation, every component labeled, standard
notation and symbols, units where applicable, legends/scale bars where appropriate.

**Accessibility:** colorblind-friendly palette (Okabe-Ito), redundant encoding (shape +
color, not color alone), works in grayscale.

**Layout:** logical flow (left-to-right or top-to-bottom), clear visual hierarchy,
balanced composition, no clutter.

**No figure numbers:** do NOT render "Figure 1", captions, or titles in the image.
Numbering and captions are added in LaTeX.

**Be specific.** "Distributed storage write path: client → API gateway → consensus (Raft)
→ write-ahead log → memtable → SSTable flush to disk" produces a usable figure; "make a
system diagram" does not. State the figure type, every component, the flow direction,
the exact labels, and the visual semantics (what each color/shape/arrow style means).

## Prompt Locks for Complex Figures

Two failure modes recur on multi-view figures and have slipped past automated review with
passing scores, so they must be prevented in the prompt. Codex's
`imagegen-scientific-schematics` skill enforces equivalent locks, but include them
explicitly for any non-trivial figure.

**Cross-view consistency.** When one conceptual entity (a data layout, a fixed mapping, an
enum partition) appears across multiple views, a plain prompt lets the model re-invent its
specifics per view, producing internal contradictions. Reserve a block at the top that
defines the entity once; later views reference it rather than redefining it:

```text
== CRITICAL CONSISTENCY ==
The contract has exactly 3 PUSH positions: PUSH 1 = variant, PUSH 2 = invariant
(value 0xCC), PUSH 3 = variant. This 1-invariant + 2-variant split must hold in
every view where it appears.
```

**Arrow continuity.** "An arrow goes from A, crosses the divider, and reaches B" can render
as two disconnected stubs. Mandate single-polyline continuity, and for long spans specify
the path geometry, not just the endpoints:

```text
== CRITICAL ARROW CONTINUITY ==
Every arrow must be a single continuous unbroken polyline from its source box to an
arrowhead at its target box. No gaps, breaks, or detached segments. Bends are allowed
at right angles but each bend is one connected joint, not two separate arrows.
```

## Example Delegation Prompts

**Distributed system architecture:**
```text
Use your imagegen-scientific-schematics skill. Distributed transaction processing pipeline,
left-to-right block diagram. Left: client layer, three application nodes (light blue boxes).
Middle: API gateway (green) routing to a Raft consensus cluster (3 nodes), connected to a
write-ahead log (orange cylinder). Right: storage backend — memtable in RAM (purple) and
SSTables on disk (gray cylinders), with a background compaction thread (red arrow) merging
SSTables. Dashed arrows = async, solid = synchronous. Throughput annotations: 100K ops/sec
at client, 50K ops/sec at consensus. Clean white background, no figure number. Save to
.writing/figures/txn_pipeline.png and report the path.
```

**Transformer architecture:**
```text
Use your imagegen-scientific-schematics skill. Transformer encoder-decoder architecture.
Left: encoder stack (input embedding, positional encoding, multi-head self-attention,
add & norm, feed-forward, add & norm). Right: decoder stack (output embedding, positional
encoding, masked self-attention, add & norm, cross-attention from encoder, add & norm,
feed-forward, add & norm, linear & softmax). Dashed line for the cross-attention connection.
Light blue = encoder, light red = decoder. Label all components. No figure number. Save to
.writing/figures/transformer.png and report the path.
```

## LaTeX Integration

1. Include with `\includegraphics{figures/<slug>.png}` (raster schematics are PNG;
   `\includegraphics` accepts PNG directly).
2. Write a thorough caption defining every component and abbreviation.
3. Reference the figure in the narrative with `Figure~\ref{fig:...}` (use the `~` tie).
4. Keep styling consistent across all figures in the paper.
5. Version-control the delegation prompt alongside the figure so it can be regenerated.

## Quick Reference Checklist

Before submitting diagrams, verify:

**Visual quality**
- [ ] No overlapping elements; adequate spacing; clean alignment
- [ ] All arrows connect properly to their intended targets (no broken stubs)

**Accessibility**
- [ ] Colorblind-safe palette (Okabe-Ito); works in grayscale; sufficient contrast
- [ ] Redundant encoding where appropriate (shapes + colors)

**Typography and readability**
- [ ] Text legible at final size; all elements labeled; consistent fonts
- [ ] No text overlaps or cutoffs; units included where applicable
- [ ] Labels spelled exactly as required (raster generation can misspell dense text)

**Publication standards**
- [ ] No figure number or caption baked into the image
- [ ] Consistent styling with other figures; comprehensive caption written in LaTeX
- [ ] Referenced in text; meets venue dimension requirements

**Documentation and version control**
- [ ] Delegation prompt saved for future regeneration
- [ ] Git commit includes prompt and output image

**Final integration check**
- [ ] Figure displays correctly in the compiled manuscript
- [ ] `\ref{}` resolves to the correct figure number
- [ ] Caption appears on the correct page relative to the figure

## Resources and References

- **`references/best_practices.md`** — publication standards, file formats, accessibility,
  and typography guidelines (backend-agnostic).

**Publication standards**
- Nature Figure Guidelines: https://www.nature.com/nature/for-authors/final-submission
- Science Figure Guidelines: https://www.science.org/content/page/instructions-preparing-initial-manuscript
- IEEE Graphics Guidelines: https://www.ieee.org/publications/reviewers/graphics.html

## Integration with Other Skills

- **`superpower-writing:tikz-figures`** — structural vector diagrams compiled with LaTeX; the default route for paper figures.
- **`superpower-writing:collaborating-with-codex`** — the bridge this skill delegates to.
- **`superpower-writing:scientific-visualization`** — data plots (matplotlib/seaborn/plotly).
- **Drafting / Methods** — the architecture-overview figure is a first-class drafting task.
- **Peer review** — evaluate diagram clarity and accessibility.

---

Use this skill to produce clear, accessible, publication-quality diagrams. Generation runs
on Codex `image_gen` with its own visual-review loop; your job is a precise delegation
prompt and a verification pass against the checklist above.

---
name: scientific-schematics
description: Generate raster figure PNGs (architecture diagrams, pipelines, concept art, graphical abstracts) through the local Codex CLI's built-in image tool (gpt-image-2), under a six-section prompt contract with three-attempt selection and a targeted edit loop. Use when the user wants an image-model figure, says 生图 / 用 AI 出一张架构图 / 先出几个方向看看, prefers a polished PNG, or wants layout drafts to pick from before a TikZ rendition. Data plots go to scientific-visualization; routine vector diagrams default to tikz-figures.
license: MIT license
allowed-tools: Read Write Edit Bash AskUserQuestion
metadata:
    skill-author: superpower-writing (prompt contract adapted from K-Dense Inc. and LigphiDonk/academic-figure-generator, both MIT)
---

# Scientific Schematics (raster figures through the Codex CLI)

## Overview

This skill produces raster figures with an image model. Generation runs through
the Codex CLI installed on this machine: `scripts/imagegen.py` starts one
non-interactive `codex exec` turn per image, Codex calls its built-in
`image_gen` tool (gpt-image-2 on the ChatGPT subscription), copies the PNG to
`--out`, and the script writes a provenance sidecar (`<stem>.imagegen.json`:
the Codex thread id, the prompt Codex actually sent to the image model, actual
size, wall time). `edit` resumes the thread recorded in the sidecar, so the
model still sees the original image and changes only what the instruction
names. No gateway, no API key, no token.

Backend facts, measured 2026-09-09 with codex-cli 0.153.4 on a four-module
pipeline diagram:

- About 35 seconds per `generate` and about 45 seconds per `edit`; two
  parallel attempts finished together in 36 seconds. Run every call with
  `run_in_background: true`.
- The image tool takes no size or quality parameter; the canvas follows the
  prompt text. "Landscape 3:2" came back 1536x1024; a left-to-right pipeline
  with no stated shape came back as a 3:1 strip. State the aspect ratio in
  FRAMING.
- Billing is ChatGPT subscription quota, not per-image money.
- Label fidelity is high: labels spelled exactly on the first attempt. Keep
  the SPELL EXACTLY line anyway; it costs nothing.
- `edit` in the same thread (rename one label) changed only that label; every
  other pixel stayed.

Requirements: `codex` on PATH and logged in. `codex login` is interactive, so
the user runs it in a terminal, never this skill. The `image_generation`
feature is on by default; `codex features list | grep image_generation`
confirms it.

## Two roles: decide which one applies before invoking

**Role 1, design exploration (on demand).** When the design direction of a
figure is unclear, a novel figure type with no obvious layout, several plausible
ways to organize the information, or the user asks to "explore directions",
generate three direction drafts in parallel (different layouts or information
organization, not color variants), show all three, and let the user pick. The
user then also chooses the delivery form: use the PNG directly (manuscript, or
material for a slides rework), iterate it to final quality with `edit`, or hand
it to `superpower-writing:tikz-figures` as a replication reference (`ref.png`)
for a vector rendition. See Exploration mode below.

**Role 2, final raster output.** When the deliverable is a PNG:

- Illustrative concept art with lighting, texture, 3D rendering, or hand-drawn style.
- Photorealistic or semi-realistic scene compositions.
- Graphical abstracts with strong pictorial elements.
- Any figure where the user prefers a polished PNG over vector source.

**Routing for everything else.** Routine structural diagrams with a clear design
(architecture diagrams, flowcharts, pipelines, sequence diagrams) default to
`superpower-writing:tikz-figures`; its two-candidate preview covers the layout
choice, and vector source keeps formulas and fonts consistent with the body
text. That is a default, not a rule: a high-quality PNG is a legitimate
deliverable whenever the user prefers it. Data plots (CDFs, training curves,
ablation bars, speedups, Pareto fronts) go to
`superpower-writing:scientific-visualization`.

## Run it

```bash
IMG="${CLAUDE_PLUGIN_ROOT}/skills/scientific-schematics/scripts/imagegen.py"

# one figure
python3 "$IMG" generate --prompt-file .writing/figures/prompts/<slug>.txt \
  --out .writing/figures/<slug>.png

# three attempts of the same prompt in parallel, saved as <slug>-1.png .. <slug>-3.png
python3 "$IMG" generate --prompt-file .writing/figures/prompts/<slug>.txt \
  --out .writing/figures/<slug>.png --count 3

# one targeted fix on a chosen PNG
python3 "$IMG" edit --image .writing/figures/<slug>-2.png \
  --prompt 'Rename the label "Top-k Docs" to "Top-k Passages".' \
  --out .writing/figures/<slug>.png
```

Mandatory: `run_in_background: true` on every call. A foreground call freezes
the session for a minute or more. Do not poll; the harness notifies on
completion. Then Read the PNG to inspect it; the Read tool renders images.

The script runs `codex exec` from the current directory with the
`workspace-write` sandbox plus write access to the output directory, retries
once when Codex exits non-zero or leaves no PNG behind, and prints one
`OK <path> <WxH> <seconds> thread=<id>` line per image. `edit` resumes the
thread named in the input image's sidecar; `--thread` overrides it, and an
image without a sidecar is attached to a fresh thread instead. The edit
instruction names only the change; the script adds the "keep everything else"
clause.

## Workflow

1. Decide whether the paper needs this figure and which kind. Read
   `tikz-figures/references/figure-rhetoric.md` for Figure-1 and
   solution-overview candidates; it is venue-agnostic across the figure skills.
2. Write the brief: every component with its exact label, the flow direction,
   the one hero module that carries the novelty, and the canvas shape.
3. Write the prompt file `.writing/figures/prompts/<slug>.txt` following
   `references/prompt-contract.md`. For a modern-ML pastel look also read
   `references/style-pastel-ml.md`.
4. Generate three attempts (`--count 3`) in the background. Read all three and
   pick the best against the checklist below. Quality varies between runs;
   never accept the first without seeing the others.
5. Fix defects with `edit`, one targeted change per call, at most three rounds.
6. Move the final to `.writing/figures/<slug>.png`, keep the prompt file and the
   sidecar under version control, reference with `\includegraphics`, and write
   the caption.

## Exploration mode (Role 1)

1. Write one shared figure brief (components, labels, flow), then derive three
   prompts that differ in layout or information organization, for example
   horizontal pipeline, layered stack, and central hero with panels. Style or
   color variants do not count as directions.
2. Save them as `.writing/figures/explore/<slug>-{a,b,c}.txt` and dispatch three
   background `generate` calls in one message, each with its own `--out`
   under `.writing/figures/explore/`.
3. When all return, Read the three PNGs, show them to the user, and ask which
   direction to develop (AskUserQuestion, one option per draft with a one-line
   layout summary).
4. Ask how to develop the chosen draft: use the PNG directly, iterate it with
   `edit` to final quality, or hand it to `superpower-writing:tikz-figures` as
   the replication reference. The last satisfies tikz-figures' two-candidate
   requirement through its 复刻 exemption; `figure-diff.py` SSIM verifies the
   TikZ rendition against the chosen draft.
5. Keep all drafts under `.writing/figures/explore/` until the figure ships;
   runner-up directions often get revisited.

Graphical abstracts are optional. Systems papers usually omit them; generate one
only when the venue asks.

## Failure and recovery

- **Script exits non-zero.** Read its message. `codex CLI not found` or an
  authentication error in Codex's stderr needs the user to run `codex login`
  in a terminal; stop and say so. "codex finished but <out> does not exist"
  quotes Codex's last reply, which usually explains why nothing was saved (the
  image tool refused the prompt, or Codex asked a question instead of acting);
  fix the prompt and rerun. A timeout (600 s by default) that survived the
  built-in retry means the turn hung; stop and report the error text. Never
  invent a saved path or claim an image exists.
- **Labels will not converge.** Allow at most three `edit` rounds on one image.
  If a label is still wrong after the third, hand the draft to
  `superpower-writing:tikz-figures` for a vector rendition, where text is exact,
  or deliver the PNG with a caption note. Endless re-prompting is the failure
  mode to avoid.
- **All three exploration drafts rejected.** Do not silently regenerate the same
  three. Ask what was wrong (layout family, emphasis, missing component), derive
  a new brief, and dispatch one fresh round. After two rejected rounds, talk
  through the intended structure before spending more quota.

## Prompt essentials

The full contract lives in `references/prompt-contract.md`. The rules that
decide most outcomes:

- **Labels name modules; they never explain them.** No sentences, no
  paragraphs, no formulas inside the image. Explanation belongs in the caption.
- **Name the core novelty.** One hero module gets the one visual distinction (a
  thicker border, the single accent color); everything else stays quiet.
- **Spell every label** in a list and add the literal line "SPELL ALL LABELS
  EXACTLY AS WRITTEN, do not rephrase or abbreviate".
- **State the canvas shape** in FRAMING (wide 3:1 strip, 3:2 landscape,
  square). The image tool has no size parameter; the prompt decides.
- **Icons only where they aid recognition:** a small monochrome icon inside a
  module (document stack, database cylinder, shield, network graph), never
  decoration.
- **Flat vector on white:** pastel fills with slightly darker borders, thin
  dark-grey arrows, no shadows, no 3D, no photos, no figure number, caption, or
  title baked into the image.

## LaTeX integration

1. Include with `\includegraphics{figures/<slug>.png}`.
2. Write a thorough caption defining every component and abbreviation; the
   image carries names only.
3. Reference the figure in the narrative with `Figure~\ref{fig:...}` (use the
   `~` tie).
4. Keep styling consistent across all figures in the paper: same prompt VISUAL
   STYLE and COLOR PALETTE blocks for every figure.
5. Version-control the prompt file and the sidecar next to the PNG so the figure
   can be regenerated.

## Quick reference checklist

Before accepting an attempt:

- [ ] Every label present and spelled exactly; no extra words the prompt did not list.
- [ ] Every arrow is one continuous stroke ending on its target; no stubs.
- [ ] No overlapping elements; spacing even; the hero module visibly distinct.
- [ ] White background, flat fills, no shadow or 3D artifacts, no photographic texture.
- [ ] At most three colors plus greys; readable in grayscale.
- [ ] No figure number, caption, or title inside the image.
- [ ] Canvas shape matches what the layout needs (a strip for a pipeline, a landscape for panels).
- [ ] Text legible at final column width (check by reading the PNG scaled down).

Before shipping:

- [ ] Prompt file and sidecar committed with the PNG.
- [ ] Caption defines every component; `\ref{}` resolves; figure sits near its first mention.

## Integration with other skills

- **Figure rhetoric (design judgment).** Whether the paper needs the figure and
  which kind: `tikz-figures/references/figure-rhetoric.md`.
- **`superpower-writing:tikz-figures`**: vector diagrams compiled with LaTeX; the
  default route for routine paper figures and the vector-rendition path after
  exploration.
- **`superpower-writing:scientific-visualization`**: data plots.
- **Drafting / Methods**: the architecture-overview figure is a first-class
  drafting task; the evidence contract's `route` field may name this skill.

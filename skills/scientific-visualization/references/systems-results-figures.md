# Systems Results Figures

Load this reference only when `.writing/metadata.yaml` sets `writing_profile: systems` and the figure is data-driven.

## Figure brief gate

Read `.writing/figures/<fig_id>.brief.yaml` before choosing a chart or writing code. Stop and list the missing fields when the file is absent or incomplete.

Require:

- `figure_id`, matching `<fig_id>`
- one primary analytical `question`
- one primary claim ID in `claim`
- a non-empty `sources` list with at least one `type: data` entry and a locatable `ref`
- non-empty `conditions` covering the experimental context needed to interpret the values
- one `family`, `order`, `encoding`, and non-empty `caption_facts`
- `interpretation_location: body`
- `route: scientific-visualization`

Allow `family: other` only with `family_reason`. If a built-in family's default route is changed, require `route_reason`; do not continue in this skill unless the selected route is `scientific-visualization`.

Treat venue rules as higher priority than this reference. Record any width, font, or color departure under `venue_overrides` in the brief.

## Result figure families

### `breakdown-bars`

Use to answer where time, bytes, energy, or another additive cost is spent.

- Keep component order identical across methods, workloads, and panels.
- Use stacked bars only when components form a meaningful total. Use grouped bars when they do not.
- Show the total or make it recoverable from the axis; do not mix percentages and absolute values without separate units.
- Use hatch, outline, or direct labels so segments remain identifiable in grayscale.
- State whether omitted components, failed runs, or rounding prevent the stack from summing exactly.

### `scaling-small-multiples`

Use to answer how methods scale across models, workloads, machine counts, or load levels.

- Give each panel a distinct workload or model while keeping the same method order.
- Use common axis ranges when panels compare the same quantities. Explain any unavoidable range change.
- Use one shared legend and the same line style and marker for each method in every panel.
- Show the measured range and uncertainty. Do not extend lines beyond observations or imply unmeasured scaling.
- Mark saturation, failure, or missing runs explicitly instead of silently dropping them.

### `parameter-heatmap`

Use to answer which region of a two-parameter space works or performs best.

- Put the two varied parameters on the axes and include units or discrete value labels.
- Use one fixed normalization and one shared colorbar across comparable panels.
- Mark missing, invalid, or unmeasured cells distinctly; never interpolate them into measured regions without saying so.
- Use a perceptually ordered sequential map for magnitude or a centered diverging map for signed difference. Do not use rainbow maps.
- Add contours, symbols, or cell labels when the claim depends on a threshold that grayscale alone may hide.

### `log-cost-curve`

Use to answer how cost grows across orders of magnitude.

- State which axis is logarithmic and its base when that matters to interpretation.
- Never place zero or negative values on a log axis. Report excluded values or choose a valid transformation.
- Plot observed points with markers; do not present an extrapolated line as measured data.
- Preserve the same method order and encoding across panels.
- Describe fitted slopes or asymptotic guides as fits or references, not measurements, and record their calculation source.

## Grayscale-redundant encoding

Make the claim readable without color before adding color.

- Assign every compared method a stable combination of line style and marker.
- Assign bar components a stable combination of hatch, outline, and position.
- Use direct labels or distinct symbols for threshold regions in heatmaps.
- Give the proposed method the clearest stable encoding, not merely the brightest color.
- Reuse method encodings across the paper. Do not copy a palette or hex table from an external package; use the plugin's existing accessible-color guidance.
- Inspect a grayscale rendering at the final single-column or full-width size. Treat merged series, segments, or threshold regions as a blocking defect.

Record the chosen redundant mapping in the brief's `encoding.grayscale_redundancy` field.

## Caption facts

Write a fact-complete caption that can be understood without searching the body for setup details. Include:

- what each panel, mark, method, and metric represents
- axes, units, method or panel order, and the tested range
- workload, hardware, model, dataset snapshot, or other conditions needed to interpret the values
- sample size, aggregation, uncertainty type, and the meaning of error bars or bands
- definitions for symbols, abbreviations, reference lines, hatching, missing-value marks, and log scales

Allow exact comparisons that are directly visible in the figure. Keep causal explanations, mechanisms, and broader implications in the body near the first substantive reference. Keep `interpretation_location: body` in the brief.

## Final checks

- Regenerate the figure only from the recorded source data and script.
- Check units, method order, conditions, sample count, and uncertainty against the brief.
- Inspect the rendered output in color and grayscale at its final placement size.
- Stop rather than inventing data, uncertainty, conditions, or caption facts. Use a clearly labeled layout mock-up only when the user explicitly requests one.

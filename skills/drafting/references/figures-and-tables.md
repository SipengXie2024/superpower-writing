# Figures and Tables for Systems Papers

## Overview

Figures and tables carry the evidence in a systems paper. Readers scan them before
they read the text; reviewers form first impressions from them. A well-designed
display item communicates a result that would take a paragraph to describe; a
poorly designed one obscures it.

This reference covers when to use tables versus figures, design principles
adapted for computer-science and systems venues, statistical annotations,
accessibility, technical specifications, and a pre-submission checklist.

## Decision Rule

Before creating any display item, apply this three-way test:

1. **Can the information be stated in one or two sentences?**
   If yes, use text alone. No figure or table needed.

2. **Do readers need precise numerical values, or do they need to see a
   pattern?**
   - Precise values, multi-variable comparison, or exact baselines
     **-> table**.
   - Trends, distributions, scaling behaviour, architecture overview
     **-> figure**.

3. **Is the item self-explanatory with its caption?**
   If not, redesign it until it is.

**Typical systems-paper mapping:**

| Content | Display type |
|---------|-------------|
| End-to-end latency percentiles (exact ns) | Table |
| Throughput-vs-load scaling curve | Figure (line graph) |
| Ablation of system components | Figure (bar chart) or Table |
| Architecture / pipeline overview | Figure (diagram) |
| Comparison with prior work (multi-metric) | Table |

Guideline: roughly one display item per 1 000 words. A 12-page conference paper
typically carries 5--8 display items (figures + tables combined).

## Design Principles

### 1. Self-Explanatory

Every figure or table must stand alone. A reader who skips the main text should
understand what is shown, why it matters, and how to read it.

Essential elements:

- Descriptive caption (see the Captions section below).
- All abbreviations defined in the caption or a footnote.
- Units on every axis, column header, and numerical entry.
- Sample size or trial count stated (e.g., "median over 5 runs").
- Legend when multiple series appear.
- Statistical annotation key (error-bar type, significance markers).

### 2. Avoid Redundancy

Do not repeat the same data in text, a table, and a figure. Pick the best
medium and reference it once.

Bad: listing exact throughput numbers in prose that also appear in Table 2.
Good: "Table 2 compares throughput across configurations; the shard-aware
scheduler achieves 1.8x the baseline."

### 3. Consistency

Use the same fonts, colour palette, terminology, and annotation style across all
display items in one paper. If Figure 1 uses "Requests/s" on the y-axis, do not
switch to "QPS" in Figure 3. If error bars are 95 % CI in one plot, keep them
95 % CI in all plots and state this in every caption.

### 4. Optimal Quantity

One display item per ~1 000 words. For a typical 10-page systems paper, aim for
5--7 items total. Fewer high-quality, information-dense displays beat many
redundant ones. Every item should earn its column-inches.

### 5. Clarity and Simplicity

Maximise the data-ink ratio (Tufte): remove grid lines, decorative borders, and
3-D effects. Use readable fonts (at least 8 pt at final print size). Provide
adequate spacing. Do not cram six sub-figures into one panel when three would
suffice.

## Figure Types

### Bar Graphs

Best for comparing discrete categories: throughput of different schedulers,
latency of system configurations, accuracy across model variants.

Guidelines:

- Start the y-axis at zero unless the differences are tiny relative to the
  magnitude (and label the break explicitly).
- Order bars logically (by value, by category, or left-to-right as introduced
  in the text).
- Include error bars and state what they represent.
- Avoid 3-D bars; they distort perception.

Common mistakes: y-axis truncation that exaggerates differences, missing error
bars, too many categories in a single plot.

### Line Graphs

Best for continuous-variable trends: throughput versus client count, latency
CDFs, cache-hit ratio over time.

Guidelines:

- Use distinct line styles (solid, dashed, dotted) or colours for each series.
- Mark data points when the series is sparse.
- Shade confidence intervals rather than overlaying error bars at every point
  when the x-axis is dense.
- Use log scale on the y-axis for tail-latency CDFs; state the scale.

Common mistakes: connecting points that are categorical (use a bar chart
instead), too many overlapping lines, inconsistent x-axis intervals.

Systems-paper staples: tail-latency CDFs, throughput-vs-load curves,
scalability plots (log-log).

### Scatter Plots

Best for showing correlation or joint distributions: request size versus
latency, memory usage versus accuracy, throughput versus energy.

Guidelines:

- Plot a regression or trend line with R-squared.
- Use semi-transparent points when overplotting is likely.
- Consider a log-log scale when the data spans orders of magnitude (e.g.,
  object size distributions).

Common mistakes: hiding individual points behind a fitted curve, using scatter
for categorical comparisons (use a bar chart instead).

### Box Plots

Best for distribution comparison: latency across configurations, memory usage
across workloads.

Guidelines:

- Define box elements in the caption (median, Q1/Q3, whisker rule).
- Overlay individual data points when the sample is small (n < 20).
- Consider violin plots for richer shape information.

Common mistakes: not defining whiskers, using box plots for tiny samples
without showing raw data.

### Heatmaps

Best for matrices and multi-dimensional comparisons: throughput-per-core
heatmap, confusion matrix, attention-map visualisation, correlation matrix.

Guidelines:

- Use perceptually uniform colour scales (viridis, magma, cividis).
- Include a colour bar with numeric labels.
- Cluster rows or columns when patterns are non-obvious.
- Avoid rainbow (jet) colour maps; they introduce false gradients.

Common mistakes: missing colour bar, unreadable axis labels when the matrix is
large, rainbow palettes.

### Flow Diagrams

Flow diagrams show multi-step processes: system pipelines, algorithm control
flow, state machines, build/deploy workflows, request-processing stages.

Guidelines:

- Use consistent shapes: rectangles for processes, diamonds for decisions,
  rounded rectangles for start/end terminals.
- Label every edge with the condition or data that flows along it.
- Include counts or sizes at each stage when the diagram represents a
  data-processing pipeline (e.g., "1.2 M requests after filter").
- Prefer vector tools (TikZ, draw.io, Mermaid) so the diagram scales cleanly.
- Keep the diagram on a single column width when possible; a wide multi-panel
  flow diagram forces the reader to rotate the page.

Common mistakes: too many crossing arrows, missing edge labels, using the
diagram to repeat text that already appears in the surrounding prose.

## Table Design

### Structure

1. **Number and title** (above the table).
2. **Column headers** with units.
3. **Row labels**.
4. **Data cells** with consistent precision.
5. **Footnotes** (below) for abbreviations, statistical tests, and caveats.

### Formatting

- Align decimal points within each column.
- Keep precision consistent (e.g., two decimal places throughout a column).
- Use an en-dash for "not applicable" or "not measured."
- Bold the best result in each column when comparing systems; state this
  convention in a footnote.
- Use superscript symbols or letters for footnotes (*, superscript a, b, c).

### Example

```
Table 2. End-to-end latency (us) under YCSB workload A.

System            p50     p95     p99
---------------------------------------
Baseline          12.3    45.1    89.7
+ Shard cache     11.8    38.4    72.3
+ Batch coalesce  10.1*   31.2*   61.5*

* p < 0.01 vs. Baseline (paired t-test, n = 5 runs).
```

### Common Mistakes

1. Too many columns; split into two tables or move detail to an appendix.
2. Missing units or inconsistent precision.
3. Over-reporting decimal places (five decimals for a microsecond value is
   noise).
4. No sample size or run count.
5. Duplicate data already shown in a figure.
6. Inconsistent formatting across tables within the same paper.

## Statistical Annotations

### What to Report

For every quantitative comparison, provide:

1. **Point estimate**: median, mean, or geometric mean.
2. **Variability measure**: standard deviation, 95 % CI, or min--max range.
   State which one you use.
3. **Sample size**: number of runs, benchmarks, or data points.
4. **Test and p-value** (if applicable): name the test and give the exact
   value when p > 0.001.

Note: p-values are less central in systems work than in life sciences.
Many systems papers rely on effect sizes and overlap-free confidence intervals
instead. Report whichever the community expects for your venue.

### Error Bars

| Measure | Shows | Use when |
|---------|-------|----------|
| Standard deviation | Spread of raw data | Showing variability |
| Standard error | Precision of the mean | Comparing means |
| 95 % CI | Range likely containing true mean | Testing significance visually |

Always label which measure the error bars represent. Non-overlapping 95 % CIs
roughly indicate a significant difference, which makes CI bars a compact way to
convey both estimate and significance in one glyph.

### Significance Markers

Common convention:

```
*  p < 0.05
** p < 0.01
*** p < 0.001
n.s.  not significant
```

Define markers in every figure caption or table footnote. Prefer exact p-values
in tables (p = 0.003) over stars alone; use stars sparingly in figures where
space is tight.

## Accessibility

### Colour-Blind Palettes

Approximately 8 % of men and 0.5 % of women have some form of colour-vision
deficiency. Design accordingly:

- Use colour-blind-safe palettes: blue-orange, purple-yellow, or the
  Okabe-Ito palette.
- Never encode information in red-green alone.
- Test every figure in greyscale; if two series become indistinguishable, add
  patterns or shapes.

Recommended palettes: Okabe-Ito, ColorBrewer2 qualitative schemes, viridis
family for heatmaps.

### Contrast and Readability

- Dark text on a light background (or the reverse); avoid low-contrast grey on
  grey.
- Minimum 0.5 pt line weight; 1 pt for the primary data.
- Minimum 8 pt font at final print size for labels and annotations.

### Black-and-White Compatibility

Many readers print papers in greyscale or read them on e-ink devices. Ensure
every figure is interpretable without colour by using distinct line styles,
markers, or hatch patterns in addition to colour fills.

## Technical Specs

### Vector vs Raster

- **Vector (preferred)**: PDF, EPS, SVG. Scales without pixelation. Use for all
  plots, diagrams, and schematics.
- **Raster**: PNG (lossless) or TIFF (lossless, large). Use only for
  screenshots, flame graphs rendered as bitmaps, or photographs.
- **Avoid**: JPEG (lossy compression introduces artefacts around text and thin
  lines).

### Resolution

- Line art and plots: 300--600 dpi at final size.
- Screenshots or raster images: 300 dpi minimum.

Create figures at the final published size to avoid resampling artefacts.

### Dimensions

Conference papers typically use one of two widths:

- **Single column**: 3.3--3.5 in (84--89 mm).
- **Double column**: 6.5--7.1 in (165--180 mm).

Design to single-column width when possible; reviewers view PDFs on screens and
wide figures can be hard to read. Full-width figures are appropriate for
architecture diagrams that need the horizontal space.

### File Formats

| Format | Type | Notes |
|--------|------|-------|
| PDF | Vector | Best for plots and diagrams; embed fonts. |
| EPS | Vector | Legacy; some journals still require it. |
| SVG | Vector | Web-friendly; convert to PDF for LaTeX. |
| PNG | Raster | Lossless; use for screenshots only. |
| TIFF | Raster | Uncompressed; some journals prefer it. |

## Numbering

- Number figures and tables independently: Figure 1, Figure 2 ... and
  Table 1, Table 2 ...
- Number sequentially in the order each item is first referenced in the text.
- Supplementary items: Figure S1, Table S1, etc.
- In-text citation: always use the number ("Figure 3 shows ..."), never "the
  figure below" or "the following table" (pagination may change).

## Captions

### Figure Captions

Place below the figure. Structure:

1. One-sentence title stating what is shown.
2. Additional sentences: define panels, explain axes, state error-bar type,
   report sample size, name the statistical test.
3. Define every abbreviation and symbol.

Example:

```
Figure 4. Tail-latency CDFs for the three scheduler variants under YCSB
workload F. Solid lines show the median over five independent runs; shaded
regions span the 10th--90th percentile. The shard-aware scheduler (blue)
achieves sub-millisecond p99 latency up to 80 k requests/s, compared to
62 k requests/s for the baseline (grey).
```

### Table Captions

Place above the table. Title in sentence case, followed by a period. Footnotes
below the table body define abbreviations, statistical tests, and conventions
(e.g., "Bold values indicate the best result in each column").

Example:

```
Table 3. Ablation study: throughput (kOps/s) on the TPC-C benchmark.

Configuration          4 cores   8 cores   16 cores
----------------------------------------------------
Full system            142.3     267.1     489.5
- Adaptive batching    138.7     241.8     412.3
- Shard routing        131.2     220.5     358.7
- Both optimisations   124.1     198.3     301.2

Each value is the median of five 60-second runs.
```

## Venue-Specific

ML-conference figure expectations, including NeurIPS/ICML/ICLR/CVPR layout
conventions and page-budget guidance, are covered in
`submission/references/venue-styles.md`.

**Non-ML venues** relevant to systems authors:

| Venue type | Display limit | Format notes |
|-----------|--------------|-------------|
| IEEE conferences (SOSP, OSDI, NSDI, EuroSys) | No hard limit; 6--8 typical in 12--14 pages | PDF vector; single-column figures preferred; use IEEE LaTeX class. |
| ACM conferences (ASPLOS, SIGCOMM, ATC) | Similar; ACM formatting guidelines apply | PDF vector; acmart LaTeX class; ensure rights-management strip does not overlap figures. |
| Journals (ACM TOCS, IEEE TC, JMLR) | Often unlimited main + appendix | Higher resolution expected (600 dpi raster); separate figure files may be required at submission. |
| Workshops / posters | Flexible | Optimise for large-format printing; increase font sizes 1.5--2x. |

General advice: consult the target venue's author guide before finalising any
figure. Column widths, margin allowances, and colour policies vary.

## Final Checklist

Review every figure and table before submission.

**For every figure:**

- [ ] Vector format (PDF/EPS) for plots and diagrams?
- [ ] At least 300 dpi if raster?
- [ ] Fits column width without overflow?
- [ ] Caption below the figure, self-explanatory?
- [ ] All abbreviations and symbols defined?
- [ ] Error bars included and labelled (SD, SEM, or CI)?
- [ ] Sample size or run count stated?
- [ ] Axes labelled with units?
- [ ] Text legible at final print size (>= 8 pt)?
- [ ] Readable in greyscale / colour-blind safe?
- [ ] Referenced in text in order of appearance?
- [ ] Consistent style with other figures in the paper?

**For every table:**

- [ ] Descriptive title above the table?
- [ ] Column headers include units?
- [ ] Decimal-aligned and consistent precision?
- [ ] Abbreviations defined in footnotes?
- [ ] Sample sizes or run counts included?
- [ ] Best results highlighted (bold) with footnote?
- [ ] Editable format (LaTeX tabular), not a raster image?
- [ ] Referenced in text in order of appearance?

**Overall:**

- [ ] Display-item count reasonable (~1 per 1 000 words)?
- [ ] No duplication between text, tables, and figures?
- [ ] Consistent formatting across all items?
- [ ] Every item earns its place (no filler)?

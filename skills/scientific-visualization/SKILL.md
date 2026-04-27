---
name: scientific-visualization
description: Publication-ready data plots for CS papers (systems, ML, networking, security). Use when creating figures with multi-panel layouts, error bars, colorblind-safe palettes, log-scale axes, latency CDFs, throughput curves, training curves, ablation bars, or speedup comparisons for IEEE / ACM / USENIX / NeurIPS / ICML / ICLR submissions. Orchestrates matplotlib, seaborn, and plotly with venue-specific styling and PDF output that drops cleanly into LaTeX. For one-off exploration use seaborn or plotly directly; for system architecture diagrams use scientific-schematics instead.
license: MIT license
metadata:
    skill-author: K-Dense Inc. (upstream); CS adaptation by superpower-writing
---

# Scientific Visualization (CS Edition)

## Overview

Turn benchmark and experiment data into publication-quality figures for CS venues. This skill is opinionated for systems, ML, networking, and security papers: it covers latency CDFs, throughput curves, training-loss plots, ablation bars, speedup comparisons, and Pareto fronts. It replaces the upstream biology-leaning version (microscopy, gene expression, fluorophores) with CS conventions and CS venue specs (IEEE, ACM, USENIX, NeurIPS, ICML, ICLR, arXiv).

The plugin produces LaTeX-only manuscripts. **PDF is the default figure format** — it embeds losslessly into LaTeX via `\includegraphics{...}`, scales without artifacts, and matches every CS venue's preferred line-art format. Use PNG only for raster screenshots, profilers, or visualizations that already started as raster.

## Scope

Use this skill when:

- Creating plots for a CS paper (latency, throughput, accuracy, loss, memory, F1, CDF, etc.)
- Targeting IEEE Transactions, an ACM conference (`acmart`), a USENIX venue, NeurIPS / ICML / ICLR, or arXiv
- Building multi-panel figures with consistent styling
- Ensuring figures stay readable in grayscale and for colorblind reviewers
- Exporting at the right resolution and format for LaTeX inclusion

Do not use this skill for:

- Architecture / data-flow / pipeline schematics — use `superpower-writing:scientific-schematics`
- Ad-hoc exploratory plots in a notebook — just import seaborn / plotly directly
- Tables — use LaTeX `booktabs` directly; no Python needed

## Quick Start

### Single-column IEEE figure (most common case)

```python
import matplotlib.pyplot as plt
import numpy as np

# Apply IEEE-tuned publication style (sets fonts, sizes, colorblind palette)
plt.rcParams.update({
    'figure.dpi': 100, 'savefig.dpi': 600,
    'font.family': 'sans-serif', 'font.sans-serif': ['Arial', 'Helvetica'],
    'font.size': 8, 'axes.labelsize': 9, 'axes.titlesize': 9,
    'xtick.labelsize': 7, 'ytick.labelsize': 7, 'legend.fontsize': 7,
    'axes.linewidth': 0.5, 'lines.linewidth': 1.5,
    'axes.spines.top': False, 'axes.spines.right': False,
    'savefig.format': 'pdf', 'savefig.bbox': 'tight',
})
plt.rcParams['axes.prop_cycle'] = plt.cycler(color=[
    '#0072B2', '#D55E00', '#009E73', '#CC79A7', '#E69F00', '#56B4E9'
])  # Okabe-Ito subset, colorblind-safe

# IEEE single-column = 3.5 inches
fig, ax = plt.subplots(figsize=(3.5, 2.4))

x = np.array([1, 2, 4, 8, 16, 32])
baseline_p99 = np.array([12.4, 13.1, 14.8, 18.6, 27.3, 49.5])
proposed_p99 = np.array([10.2, 10.4, 11.1, 12.7, 16.4, 24.0])

ax.plot(x, baseline_p99, marker='o', label='Baseline')
ax.plot(x, proposed_p99, marker='s', label='Ours')

ax.set_xlabel('Concurrent clients')
ax.set_ylabel(r'p99 latency (ms)')
ax.set_xscale('log', base=2)
ax.legend(frameon=False, loc='upper left')

fig.savefig('latency_p99.pdf', bbox_inches='tight')
```

The output drops into LaTeX with `\includegraphics[width=\columnwidth]{figures/latency_p99.pdf}`.

### Using a bundled style file

The plugin ships matplotlib style files under `${CLAUDE_PLUGIN_ROOT}/skills/scientific-visualization/assets/`. Load one with the absolute path:

```python
import os, matplotlib.pyplot as plt
PLUGIN = os.environ['CLAUDE_PLUGIN_ROOT']
plt.style.use(f'{PLUGIN}/skills/scientific-visualization/assets/ieee.mplstyle')
# or 'acm.mplstyle', 'neurips.mplstyle', 'publication.mplstyle', 'presentation.mplstyle'
```

To make figures self-contained (no env-var dependency), copy the chosen style file into `.writing/figures/` once and reference it locally.

## Core Principles

### 1. Format and resolution

- **Vector PDF** for every plot. Embeds in LaTeX without rasterization, scales perfectly. Use `fig.savefig('foo.pdf', bbox_inches='tight')`.
- **PNG at 300 – 600 DPI** only for raster content (screenshots, profilers, heatmaps with thousands of cells where a vector explodes). Set `savefig.dpi: 600` for PNGs going into camera-ready.
- **Never JPEG** for plots. The lossy artifacts around lines and text are obvious in print.
- **Embed fonts** in PDFs — matplotlib does this by default with `pdf.fonttype: 42` (TrueType). Without it, IEEE / ACM sometimes flag text as "Type 3 fonts" during eXpress / paperplaza checks.

```python
plt.rcParams['pdf.fonttype'] = 42  # TrueType, embedded
plt.rcParams['ps.fonttype'] = 42
```

### 2. Color: colorblind-safe by default

Roughly 8 % of male readers have a red-green color-vision deficiency. Reviewers, area chairs, and ML conference attendees in dim halls fail to distinguish poorly chosen palettes. Default to **Okabe-Ito** for categorical data and **viridis** / **cividis** for continuous data.

```python
# Okabe-Ito (8 distinguishable categories under all common CVD types)
okabe_ito = ['#E69F00', '#56B4E9', '#009E73', '#F0E442',
             '#0072B2', '#D55E00', '#CC79A7', '#000000']
plt.rcParams['axes.prop_cycle'] = plt.cycler(color=okabe_ito)
```

For categorical 3 – 4-series plots, prefer the high-contrast subset `['#0072B2', '#D55E00', '#009E73', '#CC79A7']` (blue / vermillion / green / pink) — it stays distinguishable in B/W print.

For heatmaps:

- Sequential single-variable data (latency, accuracy, count): `viridis` or `cividis`. Both are perceptually uniform and colorblind-safe.
- Diverging data (speedup vs baseline, log-fold change, error signed): `RdBu_r` or `PuOr` centered at the neutral value. Avoid `RdGn` / `RdYlGn`.
- **Never** `jet` or `rainbow`. Not perceptually uniform; over-emphasizes mid-range; bad in B/W. Reviewers will flag this.

Always add **redundant encoding** beyond color: line styles (`'-'`, `'--'`, `':'`), markers (`'o'`, `'s'`, `'^'`), or hatching on bars. If the figure still reads in grayscale, the color choice is solid.

### 3. Typography

- Sans-serif at the final printed size: Arial, Helvetica, or DejaVu Sans (the matplotlib default fallback).
- Minimums **at the size that lands on the page**:
  - Axis labels: 8 pt
  - Tick labels: 7 pt
  - Legend: 7 pt
  - Panel labels (a, b, c): 9 – 10 pt bold
- Embed fonts. Use `pdf.fonttype: 42` so TrueType fonts ship inside the PDF.
- Sentence case: `Throughput (req/s)` not `THROUGHPUT (REQ/S)`.
- Always include units in parentheses. Use SI / IEC prefixes consistently (`KB`, `MiB`, `μs`, not `K`, `M`, `us`).

### 4. Figure dimensions for CS venues

| Venue | Single column | Double column / full | Typical class file |
|-------|---------------|-----------------------|--------------------|
| IEEE Transactions / Conf. | 3.5 in (89 mm) | 7.16 in (182 mm) | `IEEEtran` |
| ACM (sigconf, acmsmall) | 3.33 in (8.45 cm) | 7.0 in (17.78 cm) | `acmart` |
| USENIX (Annual / OSDI / NSDI / Sec.) | 3.33 in | 7.0 in | `usenix2019_v3` |
| NeurIPS / ICML / ICLR | n/a (one column) | 5.5 in (14.0 cm) | venue style |
| arXiv | follow target venue | follow target venue | venue style |

**Match `\columnwidth` exactly** when you use `\includegraphics[width=\columnwidth]`. Set `figsize=(3.5, ...)` for IEEE single-column figures and let LaTeX scale only when the figure spans both columns.

See `references/venue_requirements.md` for the full per-venue spec, including `\figcomp` / `\columnsep` quirks and ACM's two-class width difference.

### 5. Multi-panel layout

- Label panels with bold lowercase letters: **(a)**, **(b)**, **(c)** — IEEE and ACM both use lowercase parenthesized.
- Use `GridSpec` for non-uniform layouts; `plt.subplots()` for uniform grids.
- Align panels along edges; equalize axis ranges across panels comparing the same quantity.
- Use `constrained_layout=True` (replaces `tight_layout`) — handles colorbars and panel labels better.

```python
from string import ascii_lowercase

fig = plt.figure(figsize=(7.0, 4.0), constrained_layout=True)  # ACM full width
gs = fig.add_gridspec(2, 3)
axes = [fig.add_subplot(gs[i // 3, i % 3]) for i in range(6)]

for i, ax in enumerate(axes):
    ax.text(-0.20, 1.05, f'({ascii_lowercase[i]})',
            transform=ax.transAxes, fontsize=10, fontweight='bold', va='top')
```

## Common CS Figure Patterns

Reference implementations live in `references/matplotlib_examples.md`. The patterns covered:

| Pattern | Use case | Notes |
|---------|----------|-------|
| Latency CDF / ECDF | Tail behavior of a request distribution | Log-scale x-axis; cap at p99 or p99.9; include median + tail callouts |
| Throughput vs concurrency | Scaling curves | Log-scale x; mark saturation knee; pair with median latency |
| Speedup bar chart | Per-benchmark improvement vs baseline | Always include `1.0 ×` reference line; group by suite |
| Training / loss curves | ML convergence | Show mean over seeds + shaded std; log-scale y for loss |
| Pareto front (acc vs params / FLOPs) | Model-size tradeoff | Highlight your model; annotate frontier |
| Stacked bar (latency breakdown) | Where time goes | Stable color order across runs |
| Roofline plot | Compute vs memory bound | Log-log axes; ridge line at peak FLOPS |
| Heatmap (cache miss / attention) | 2D intensity | viridis or cividis; never jet |
| Box / violin (per-seed variability) | Multi-run distribution | Overlay individual seeds as strip plot |
| Significance bars | A / B / ablation comparison | Optional in CS — only when stats are central to the claim |

### Statistical rigor (CS-specific)

CS reviewers care less about p-values than biomedicine reviewers, but more about **run-to-run variability** and **error bars over seeds**. Standard expectations:

- Run each measurement ≥ 3 times (≥ 5 for ML, ≥ 10 for noisy systems benchmarks). Report mean and std or 95 % bootstrap CI.
- Show individual data points (strip plot) when n is small (≤ 10) — averages alone hide bimodal failure modes.
- State error type in the caption: `Error bars: 95 % CI over 5 seeds` or `Shaded region: ±1 std over 10 runs`.
- For ML, also report median + min/max if you train fewer than 5 seeds.
- For latency, report a percentile (median, p99, p99.9) — never just the mean. The mean of a heavy-tail distribution is a lie.

Don't fabricate error bars. If a measurement is from a single run, say so in the caption and prefer a bar / scatter without error indicators rather than zero-width error bars.

## Choosing a library

| Library | Best for | Notes |
|---------|----------|-------|
| matplotlib | Multi-panel, full control, anything that needs custom annotations | Default for camera-ready CS figures |
| seaborn | Statistical plots with automatic CI / bootstrap | Built on matplotlib; styles compose; great for box / violin / regression |
| plotly | Interactive HTML for project pages or supplementary | Use `kaleido` to export static PDF |
| pgfplots / TikZ | When you want LaTeX to compile the figure | Best for diagrams that mix math and data; covered by `scientific-schematics` |

If a figure is reused across paper / poster / slides, render at multiple sizes from the same script — keep a single source-of-truth Python file under `.writing/figures/src/`.

## Workflow inside this plugin

1. **Plan from the outline.** Each figure listed in `.writing/plan.md` should have a one-line claim it supports (`fig:cdf-latency` → "our system has a 2.4× lower p99 than the baseline at 32 clients").
2. **Write a generator script** in `.writing/figures/src/<fig_id>.py`. The script reads from `.writing/figures/data/<fig_id>.{csv,jsonl}` and writes `.writing/figures/<fig_id>.pdf`. This separation lets reviewers (and you) regenerate figures from raw data.
3. **Apply this skill's style** at the top of the script — copy the bundled `.mplstyle` file or use the inline rcParams snippet from Quick Start.
4. **Verify before commit.** Open the PDF in a viewer at 100 % zoom and at the column width it will appear at in the paper. If text is cramped at column width, the font sizes are wrong.
5. **Caption discipline.** The figure caption belongs in the `.tex` file, not on the figure itself. Repeat axes labels in the caption; spell out what error bars represent; state the sample size.

## Common pitfalls (CS-specific)

1. **Y-axis in milliseconds for tail latency.** A linear axis hides the long tail. Use log y for p99 / p99.9 plots.
2. **Bar chart starting non-zero.** Misleading. Either start at zero or annotate clearly with a broken-axis indicator.
3. **One color per algorithm but identical line style.** Fails in grayscale. Add markers + line styles.
4. **Legend over data.** Use `loc='upper left'` and verify visually; or place outside with `bbox_to_anchor`.
5. **Default matplotlib font rendering.** Matplotlib's default `mathtext` uses computer-modern italics; mixed with Arial body text it looks broken. Either set `text.usetex: True` (slow) or use `mathtext.fontset: 'cm'` only when you need real LaTeX math.
6. **`tight_layout()` clipping panel labels.** Use `constrained_layout=True` instead.
7. **DPI confusion.** For PDF, `dpi` only affects rasterized embedded objects. For PNG, set both `figure.dpi` (display) and `savefig.dpi` (output) — `savefig.dpi: 600` for camera-ready.
8. **`plt.show()` in a script that runs in CI.** Will hang. Use `fig.savefig(...)` only and skip `plt.show()` in scripted figure generation.
9. **Forgetting `bbox_inches='tight'`.** Default save leaves margin around the figure. With `bbox_inches='tight'`, the saved PDF crops to the actual content — what you want for `\includegraphics`.
10. **Reusing colors across figures.** Pin one color to one method everywhere. Define a `METHOD_COLORS` dict in a shared `.writing/figures/src/_palette.py`.

## Bundled resources

| Path | Purpose |
|------|---------|
| `references/publication_guidelines.md` | Universal best practices: typography, layout, axes, accessibility, grayscale tests |
| `references/venue_requirements.md` | Per-venue specs (IEEE, ACM, USENIX, NeurIPS, ICML, ICLR, arXiv) with exact widths, font sizes, and class-file gotchas |
| `references/color_palettes.md` | Categorical (Okabe-Ito, Wong, Tol Bright/Muted), sequential (viridis family), diverging (RdBu, PuOr, BrBG); with grayscale and colorblind testing recipes |
| `references/matplotlib_examples.md` | Twelve runnable patterns — CDF, throughput, training curve, Pareto, ablation, stacked-bar breakdown, heatmap, roofline, box+strip, multi-panel composition, `\columnwidth` IEEE template, `\textwidth` ACM template |
| `scripts/style_presets.py` | `apply_publication_style(name)`, `set_color_palette(name)`, `configure_for_venue('ieee' / 'acm' / 'usenix' / 'neurips' / 'icml' / 'iclr' / 'arxiv')`. Copy into a project to pin the rcParams. |
| `scripts/figure_export.py` | `save_publication_figure()` (multi-format), `save_for_venue()` (per-venue defaults), `check_figure_size()` (warns when figsize doesn't match the venue's column width). |
| `assets/color_palettes.py` | Importable color constants and `apply_palette('okabe_ito' / 'wong' / 'tol_bright' / …)`. |
| `assets/publication.mplstyle` | Generic CS publication baseline. Use when no specific venue style applies. |
| `assets/ieee.mplstyle` | IEEE Transactions / conferences (3.5 in single column, 8 pt body). |
| `assets/acm.mplstyle` | ACM `acmart` sigconf / acmsmall (3.33 in single, 7.0 in two-column). |
| `assets/neurips.mplstyle` | NeurIPS / ICML / ICLR (single column 5.5 in textwidth, 9 pt body). |
| `assets/presentation.mplstyle` | Larger fonts and thicker lines for posters and slides. |

## Final Checklist

Before adding `\includegraphics{...}` to the paper, confirm:

- PDF format (or PNG at ≥ 300 DPI for raster)
- `figsize` matches the target column width
- Axis labels include units; tick labels readable at print size
- Colorblind-safe palette; redundant encoding beyond color
- Figure interpretable in grayscale (`convert -colorspace gray foo.pdf foo_gray.pdf`)
- Error bars present with definition in caption (or single-run noted)
- Panel labels present and consistent (a / b / c, lowercase parenthesized)
- No top / right spines, no chart junk, no 3D, no jet colormap
- Method colors consistent across every figure in the paper
- Embedded fonts (`pdffonts foo.pdf` shows "yes" under "emb")

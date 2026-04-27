# Publication Guidelines for CS Figures

Universal best practices for plots that go into a CS paper, independent of the specific venue. Per-venue specs (IEEE / ACM / USENIX / NeurIPS / ICML / ICLR / arXiv) live in `venue_requirements.md`.

## Core Principles

1. **Clarity first.** A reviewer skimming should understand the figure in five seconds without reading the caption. The headline finding must be visually obvious.
2. **Truthful representation.** Axis ranges, bar baselines, log vs linear, and aggregation method (mean / median / max) all bias what the reader sees. Pick the form that does not mislead.
3. **Reproducibility.** Each figure should have a generator script under version control that reads from raw data — not a hand-tweaked Illustrator file.
4. **Accessibility.** Colorblind reviewers, grayscale printers, and small projector screens are part of the audience. Plan for all three.

## File Format

### PDF (default for plots)

- Vector format. Embeds in LaTeX without rasterization. Scales without artifacts. Preferred by every CS venue.
- Save with `fig.savefig('foo.pdf', bbox_inches='tight')`.
- Embed fonts with `plt.rcParams['pdf.fonttype'] = 42` (TrueType) — avoids the Type 3 font warning that some submission portals raise.

### PNG (raster fallback)

- Use only for screenshots, profiler outputs, or 2D density plots so dense that a PDF balloons past 5 MB.
- Set both `figure.dpi: 100` (display) and `savefig.dpi: 600` (output). 300 DPI is the absolute minimum for camera-ready; 600 DPI for line art content.
- Save with `fig.savefig('foo.png', dpi=600, bbox_inches='tight')`.

### Never JPEG

- Lossy compression introduces ringing artifacts around lines and text. Reviewers can tell. Don't.

### EPS / SVG (rare)

- Some older venues still ask for EPS. Use `fig.savefig('foo.eps')`; matplotlib produces clean EPS for line art.
- SVG is useful for project pages but rarely for the paper itself.

## Resolution Requirements

| Content | Minimum DPI | Recommended |
|---------|-------------|-------------|
| Vector PDF (plots) | n/a | n/a — vector |
| Raster PNG (line-art-equivalent plots) | 600 | 600 |
| Screenshots / profiler output | 300 | 300 – 600 |
| Heatmaps with thousands of cells | 300 (raster) or PDF | PDF when feasible |

## Typography

### Font Family

- Sans-serif. Arial, Helvetica, or DejaVu Sans (matplotlib's open-source fallback that ships everywhere).
- Match the body text family of the LaTeX class when possible — `acmart` uses Linux Libertine for body and Helvetica-equivalent for figures, so Arial in figures is fine.
- Avoid serif fonts in figures. They look mismatched against the LaTeX class and reduce readability at small sizes.

### Font Size at Final Print Size

The numbers below assume the figure fills the column width exactly. If you produce a figure at `figsize=(7,5)` and let LaTeX shrink it to `\columnwidth=3.33in`, all your text gets ~half size — usually too small.

| Element | Minimum | Recommended |
|---------|---------|-------------|
| Axis labels | 7 pt | 8 – 9 pt |
| Tick labels | 6 pt | 7 – 8 pt |
| Legend | 6 pt | 7 – 8 pt |
| Panel labels (a / b / c) | 8 pt | 9 – 10 pt bold |
| In-figure annotations | 6 pt | 7 pt |

Set `font.size: 8` as a default; matplotlib uses it for everything that doesn't override.

### Text Style

- Sentence case: `Latency (ms)` not `LATENCY (MS)` and not `Latency (Ms)`.
- Always include units in parentheses: `(ms)`, `(req/s)`, `(GB)`, `(seeds)`.
- Use proper SI prefixes (`μs` not `us`, `MiB` for binary not `MB` when you mean 2^20).
- Math notation: use raw strings or LaTeX-style for exponents — `r'$10^3$'`, `r'$\sigma$'`. Set `mathtext.fontset: 'cm'` if you mix Arial and math.

## Color Usage

See `color_palettes.md` for the full reference. Summary:

- Default categorical: Okabe-Ito (8 colors, colorblind-safe).
- Sequential: viridis or cividis (perceptually uniform, grayscale-safe).
- Diverging: RdBu_r, PuOr, BrBG centered on the neutral value.
- Forbidden: jet, rainbow, RdGn, RdYlGn.
- Always test grayscale: `convert -colorspace gray foo.pdf foo_gray.pdf` and check that all series remain distinguishable.

### Method-to-color consistency

Pin one color to one method across **every figure in the paper**. Reviewers internalize "blue = baseline, orange = ours" by the second figure; breaking it on figure five forces a re-orientation.

```python
# .writing/figures/src/_palette.py
METHOD_COLORS = {
    'baseline':   '#56B4E9',  # sky blue
    'ours':       '#D55E00',  # vermillion
    'ablation_a': '#009E73',  # green
    'ablation_b': '#CC79A7',  # pink
    'ideal':      '#000000',  # black
}
```

Import from every generator script:

```python
from _palette import METHOD_COLORS
ax.plot(x, y_baseline, color=METHOD_COLORS['baseline'], label='Baseline')
```

## Layout and Composition

### Multi-Panel Figures

- Lowercase parenthesized labels: `(a)`, `(b)`, `(c)`. IEEE and ACM both prefer this. Place top-left, slightly outside the axis frame.
- Consistent panel sizes when the panels show comparable quantities. Different sizes only when the data demands it (a wide CDF panel + a short bar panel is fine).
- Use `constrained_layout=True` instead of `tight_layout()` — it handles colorbars, suptitles, and panel labels more reliably.
- White space: keep `wspace` and `hspace` around 0.3 – 0.4 unless panels need to share an axis.

### Axes

- Axis line width: 0.5 pt for IEEE / ACM, 0.8 pt for slide / poster.
- Tick direction: `out`. Inward ticks collide with data points.
- Tick frequency: 4 – 7 major ticks. More than that and labels overlap; fewer and the scale is hard to read.
- Always label both axes with units. The only exception is panel labels in a multi-panel where the convention is shared (and then it's stated in the caption).
- Start bar charts at zero. If you must use a non-zero baseline (e.g., showing tiny relative differences), explicitly indicate the broken axis with `\\` marks.
- Log scales: label clearly (`log`, `log10`, `log2`). Use minor ticks at every decade. For latency, log y is almost always right. For throughput vs concurrency, log x is almost always right.

### Lines, Markers, Bars

- Data line width: 1.0 – 1.5 pt for IEEE/ACM, 2.0 – 2.5 pt for posters.
- Marker size: 3 – 5 pt. Markers should be visible without overwhelming the data.
- Marker types: differentiate series with `o`, `s`, `^`, `v`, `D`, `P`. At most six series on one plot — beyond that, split into panels or use a faceted figure.
- Error bars: 0.5 – 1.0 pt with `capsize=2` to `3`. Don't overdo cap thickness.
- Bar edge color: `black` with `linewidth=0.5` for crispness. Bar fill: solid color, no gradients.
- Stacked bars: pin segment order across all bars (sort by category, not by size). Otherwise readers can't compare segments.

### Legends

- Inside the plot when there's empty quadrant space; outside (`bbox_to_anchor`) when the data fills the box.
- No frame for a clean look: `legend(frameon=False)`. Add a subtle frame only if the legend overlaps data.
- Order entries by visual prominence (top to bottom = top-most line to bottom-most line) or by importance (your method first).
- Keep entries short. Move full descriptions into the caption.

## Statistical Conventions for CS

CS reviewers care about these things in roughly this priority order:

1. **Variance across runs / seeds.** Show error bars or a shaded band. State `n` and the error type explicitly in the caption.
2. **Tail behavior for latency.** Median + p99 is a minimum; p99 + p99.9 is better.
3. **Multiple workloads / benchmarks.** A single benchmark is rarely convincing; show consistency across a representative suite.
4. **Statistical significance.** Required only when the claim hinges on a small effect size. For CS systems papers, "10× faster" rarely needs a p-value; "5 % faster" should be backed by a paired test.

### Error bar conventions

- ML training: ≥ 3 seeds, prefer 5. Show mean and shaded ± 1 std OR 95 % bootstrap CI. State which.
- Systems benchmarks: ≥ 5 runs after warm-up, prefer 10. Drop or report cold-start outliers separately.
- Latency: per-request distribution → percentiles, not error bars. p50, p99, p99.9 as separate lines or as a CDF.
- Throughput: bars or lines with min / max range whiskers; or median ± 95 % CI.

### Caption template for statistics

> Figure 4: p99 latency vs. concurrent clients, log-x axis. Each point is the
> median of 10 runs, error bars show the 5th – 95th percentile across runs.
> Workloads from YCSB-A; warm-up of 30 s discarded.

## Accessibility

### Colorblind

- ~ 5 % deuteranopia, ~ 2 % protanopia, < 1 % tritanopia among male readers.
- Test with Coblis (https://www.color-blindness.com/coblis-color-blindness-simulator/) or Color Oracle.
- Adding a redundant non-color encoding (line style, marker, hatch) makes the figure robust without simulator testing.

### Grayscale

- B/W printing is still common. Verify with `convert -colorspace gray foo.pdf foo_gray.pdf` before submission.
- Sequential viridis maps to a clean luminance gradient; jet doesn't.
- Adjacent bars with similar luminance values become indistinguishable in grayscale; vary luminance, not just hue.

### Small screens

- Reviewers reading on a 13-inch laptop see your figure at maybe 70 % of column width. Test by zooming the PDF to that size.

## Common Mistakes (CS-specific)

1. **Running a script that produces 7-inch figures, then `\includegraphics[width=\columnwidth]`.** Text gets squished to 4-pt. Match `figsize` to `\columnwidth` from the start.
2. **Linear y-axis for tail latency.** Long tail compressed at the top; head dominates. Use log y.
3. **One bar chart per benchmark, ten benchmarks.** Reviewers fatigue. Use a grouped bar (one bar per method per benchmark) or a heatmap.
4. **Legend hides the most interesting data.** Common with `loc='best'` — matplotlib sometimes picks the data corner. Pin `loc='upper left'` and verify.
5. **Too many y-axis decimals.** `1.234567` says nothing about precision. Round to the meaningful digit (2 – 3 sig figs).
6. **Heatmap without colorbar.** The values are uninterpretable. Always add a colorbar with a labeled unit.
7. **Forgetting log-scale label.** A log axis without `log` in the label looks linear and misleads readers who skim.
8. **Mixing dotted and dashed lines for the same data style.** Subtle but visible. Standardize: solid for primary, dashed for secondary, dotted for theoretical bound.
9. **Saving as PNG when PDF would work.** Reviewers print and zoom; pixels become visible. PDF is free; use it.
10. **Hard-coded colors in 12 different scripts.** When you change palette mid-revision, you miss a few. Centralize in `_palette.py`.

## Pre-submission Figure Checklist

- [ ] Format: PDF (vector) for plots, PNG ≥ 300 DPI for raster screenshots
- [ ] `figsize` matches `\columnwidth` at 1.0 scale (no LaTeX shrinking)
- [ ] All text ≥ 6 pt at final size; labels ≥ 7 pt
- [ ] Fonts embedded: `pdffonts foo.pdf` shows "emb yes"
- [ ] Colorblind-safe palette; redundant encoding beyond color
- [ ] Grayscale conversion still readable
- [ ] All axes labeled with units
- [ ] Error bars present with definition in caption (or single-run noted)
- [ ] Panel labels: lowercase parenthesized, consistent across the paper
- [ ] Method-to-color mapping consistent across every figure
- [ ] No jet colormap, no 3D effects, no chart junk
- [ ] Caption states n, error type, workload, and any axis non-default (e.g., log)
- [ ] Legend doesn't overlap data
- [ ] Figure regenerates from `.writing/figures/src/<name>.py` without manual steps

## See Also

- `venue_requirements.md` — exact per-venue specs (IEEE, ACM, USENIX, NeurIPS, ICML, ICLR, arXiv)
- `color_palettes.md` — colorblind-safe palettes and grayscale recipes
- `matplotlib_examples.md` — twelve runnable patterns for common CS figure types
- `../scripts/style_presets.py` — `apply_publication_style()` and `configure_for_venue()`
- `../scripts/figure_export.py` — `save_publication_figure()` and `check_figure_size()`

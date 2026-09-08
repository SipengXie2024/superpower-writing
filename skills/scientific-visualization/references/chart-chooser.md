# Chart chooser: from the claim to the chart

Pick the chart from the question the figure must answer, before writing any
plotting code. The tables below merge the systems patterns already in this
skill with the standard ML results charts. Entries marked "caution" are common
in submissions but draw reviewer objections at CS venues; each carries the
replacement to use instead.

Adapted in part from a public "experiment plot recommendation" prompt (19 chart
types in six groups); the venue cautions, the systems families, and the scale
rule are this plugin's.

## Contents

- How to use this file
- Comparison across methods
- Trends, scaling, and convergence
- Distributions and tails
- Classification quality (ML only)
- Matrices and relationships
- Composition and share
- Composite layouts
- Scale remedies when groups differ by a lot
- Orientation, series count, statistical elements
- Charts to avoid or justify
- Feeding the figure brief

## How to use this file

1. Write the one sentence the figure must make true (the `question` and
   `claim` fields of the figure brief).
2. Find the row whose question matches. Take the chart in the second column;
   read the third column before committing.
3. Apply the scale rule and the orientation and series-count rules below.
4. Record the chart as the brief's `family` (built-in name when one exists,
   otherwise `family: other` with `family_reason`).

Recommend one chart, two at most. A figure that needs three chart types is two
figures.

## Comparison across methods

| Question | Chart | Notes |
|---|---|---|
| Which method wins on one metric across a few benchmarks? | Grouped vertical bars | Up to about 8 groups with short labels. Start at zero. Group by benchmark, color by method, method order fixed across the paper. |
| Same, but method names are long or there are many items? | Horizontal bars | Long labels read left to right without rotation; sort by value unless the text introduces a fixed order. |
| How much faster than the baseline, per benchmark? | Speedup bars | Baseline at `1.0x` as a reference line; log y when speedups span more than one order of magnitude. See `matplotlib_examples.md` pattern 3. |
| Which model is best on two competing metrics (accuracy vs cost)? | Pareto front | Scatter of all models, frontier drawn through the non-dominated points, your models highlighted. Annotate the frontier, not every point. Pattern 5. |
| Where does the time, memory, or energy go? | Stacked bars (`breakdown-bars`) | Only when components add to a meaningful total; fixed segment order; hatch or outline for grayscale. Grouped bars when components do not sum. |
| Which component contributes the gain (ablation)? | Grouped bars or a table | Bars when there are 3 to 6 variants and one metric; a table when several metrics or exact values matter. Pattern 12. |
| Is the model strong on every axis with no weak spot? | Radar (caution) | Enclosed area changes with axis order and scale, and reviewers know it. Prefer a small-multiples row of bars, one panel per metric, or a table with per-metric best in bold. |

## Trends, scaling, and convergence

| Question | Chart | Notes |
|---|---|---|
| Does training converge, and how fast? | Line with shaded band | Mean over seeds, band is std or a 95 percent CI, stated in the caption; log y for loss. Pattern 4. |
| Curves end almost together; who wins at the end? | Line plus an inset zoom | Inset the final segment of the x range at larger scale; draw the inset's extent on the main axes; do not truncate the main y axis instead. |
| How does throughput or latency change with load? | Throughput vs concurrency | Log x; mark the saturation knee; pair with median latency. Pattern 2. |
| How do methods scale across models, workloads, or machine counts? | Small multiples (`scaling-small-multiples`) | One panel per workload, shared axes and legend, same method encoding everywhere; never extend a line past the measured range. |
| How does cost grow across orders of magnitude? | Log-cost curve (`log-cost-curve`) | State the log axis and base; markers on measured points; a fitted slope is labeled as a fit, never as data. |
| Is there a relationship in a cloud of points? | Scatter with a fitted curve | Keep the points visible; state the model of the fit and its R squared in the caption; never let the fit replace the points. |

## Distributions and tails

| Question | Chart | Notes |
|---|---|---|
| What does the latency tail look like? | CDF or ECDF | Log x; cap at p99 or p99.9; call out the median and the tail. Pattern 1. Never report a mean for a heavy tail. |
| How variable are runs across seeds? | Box plus strip, or violin | Strip the individual points when n is 10 or fewer; a violin only when n is large enough for the density shape to mean something (dozens of points). Pattern 9. |
| How are values spread within one condition? | Histogram | Fixed bin edges across conditions; density rather than counts when sample sizes differ. |

## Classification quality (ML only)

| Question | Chart | Notes |
|---|---|---|
| How does the classifier trade true positives against false positives, with balanced classes? | ROC curve | Diagonal chance line; AUC in the legend. |
| Same question with rare positives? | Precision-recall curve | ROC flatters imbalanced data; PR shows the loss of precision at high recall. State the positive rate. |
| Which classes get confused? | Confusion matrix heatmap | Row-normalize when class sizes differ; sequential colormap; print the numbers in the cells. |

## Matrices and relationships

| Question | Chart | Notes |
|---|---|---|
| Which region of a two-parameter space works? | Heatmap (`parameter-heatmap`) | Both parameters on the axes with units; one shared colorbar across panels; mark unmeasured cells; viridis or cividis, never rainbow. Pattern 8. |
| How do many models score on many tasks? | Heatmap with cell labels | Fixed row and column order; the numbers in the cells carry the exact values, the color carries the pattern. |
| How close are predictions to the truth? | Scatter with a diagonal reference | `y = x` line; equal axis ranges; density shading or transparency when points overlap. |
| Same, with a third quantity such as parameter count? | Bubble chart (caution) | Readers misjudge area. Use at most three or four size classes with a size legend, or drop the bubble and facet by the third quantity. |

## Composition and share

| Question | Chart | Notes |
|---|---|---|
| What fraction of errors falls in each category? | Sorted horizontal bars | Percentages on the axis and the counts in the caption. Pie and donut charts (caution) hide small differences and waste column width; use them only when a venue's template shows them and there are at most four slices. |

## Composite layouts

| Question | Chart | Notes |
|---|---|---|
| Two quantities with different units against the same x? | Two stacked panels sharing x | A dual y-axis (caution) invites reading meaning into where the lines cross; stacked panels keep both scales honest. Use twin axes only when the venue template does and the caption explains both scales. |
| A metric against a long-tailed class distribution? | Two stacked panels: counts above, metric below | The bar plus line overlay (caution) has the same twin-axis problem; stacked panels with a shared x show the long tail and the metric without a second axis. |
| Too many series or conditions for one panel? | Facet grid (small multiples) | More than six series on one axes is the trigger. Shared axes, one legend, panel titles that name the condition. Patterns 10 and 11. |
| Is the kernel compute bound or memory bound? | Roofline | Log-log; ridge at peak FLOPS. Pattern 7. |

## Scale remedies when groups differ by a lot

When one group sits near 0 to 10 and another near 70 to 80 on the same axis,
pick one remedy from what the reader must take away:

- **The raw magnitudes matter** (the reader should feel that one method is at
  5 and another at 75): keep a linear axis and use a broken axis with explicit
  break marks on the axis line. Never a silent non-zero baseline on a bar chart.
- **The values span orders of magnitude** or grow exponentially: use a log
  axis, labeled with its base, with minor ticks at each decade. No zeros or
  negatives on a log axis; report excluded values in the caption.
- **The relative improvement is the claim**: normalize to the baseline
  (baseline at 1.0 or 100 percent) and keep the absolute values in a table or
  the caption so the reader can recover them.

Choose one. A broken log axis, or normalized values on a broken axis, is a sign
the figure is carrying two claims.

## Orientation, series count, statistical elements

- **Orientation.** Long category names or more than about eight categories:
  horizontal bars. Short labels and few categories: vertical bars. Never rotate
  x labels 45 degrees as the fix for long names.
- **Series count.** At most six series on one axes, distinguished by line style
  and marker as well as color. Beyond six, facet.
- **Error indication.** Repeated runs or seeds: error bars or a shaded band,
  with `n` and the error type in the caption. A single run: no error bars, and
  the caption says it is a single run. Never zero-width error bars as a stand-in.
- **Significance marks.** Only when the claim rests on a small effect; a 10x
  speedup needs no p-value, a 5 percent gain needs a paired test.
- **Fits and reference lines.** Every fitted curve, frontier, or reference line
  is named in the caption as what it is (a fit, a chance line, the baseline).

## Charts to avoid or justify

| Chart | Why reviewers object | Use instead |
|---|---|---|
| Radar or spider | Area depends on axis order and per-axis scaling; suggests a "balanced" model regardless of the data | Small multiples of bars, or a table |
| Pie or donut | Angles and arcs are misread; small slices vanish; wastes width | Sorted horizontal bars |
| Dual y-axis | Line crossings mean nothing; either axis can be scaled to tell any story | Two stacked panels sharing x |
| Bar plus line overlay | Same twin-axis problem in disguise | Two stacked panels sharing x |
| 3D bars or 3D surfaces | Depth distorts comparison; occlusion hides data | Flat bars; heatmap for a surface |
| Bubble sizes as a precise encoding | Area is misjudged by a factor of 2 or more | Few size classes with a legend, or facet |
| Truncated linear axis without a break mark | Exaggerates differences | Broken axis with marks, or one of the other scale remedies |

Any of these is allowed when the user chooses it knowingly or the venue template
uses it; record the reason in the brief's `family_reason`.

## Feeding the figure brief

Built-in families keep their names: `breakdown-bars`,
`scaling-small-multiples`, `parameter-heatmap`, `log-cost-curve`. Every other
row here is `family: other` with a `family_reason` naming the chart from this
file, for example `family_reason: horizontal bars, 14 methods with long names`.
The `question` column of the row is the brief's `question`; the notes column
supplies `order`, `encoding`, and the `caption_facts` the caption must carry.

# Color Palettes for CS Figures

CS-tailored guidance: colorblind-safe categorical palettes, perceptually uniform colormaps for heatmaps, conventions for method-to-color consistency, and grayscale verification. Drops biology-specific guidance (fluorophores, DNA bases, microscopy channels) — those live in the upstream skill if you need them.

## Categorical Palettes (Discrete Series)

### Okabe-Ito (default — 8 colors)

Designed by Okabe and Ito (2008) to be distinguishable under all forms of color vision deficiency. The right default for CS figures.

```python
OKABE_ITO = ['#E69F00', '#56B4E9', '#009E73', '#F0E442',
             '#0072B2', '#D55E00', '#CC79A7', '#000000']
# orange, sky blue, bluish green, yellow, blue, vermillion, reddish purple, black
```

For 3 – 4-series plots, prefer the high-contrast subset:

```python
OKABE_ITO_4 = ['#0072B2', '#D55E00', '#009E73', '#CC79A7']
# blue, vermillion, green, pink — distinguishable in B/W
```

For 2-series plots (baseline vs ours):

```python
OKABE_ITO_2 = ['#56B4E9', '#D55E00']  # sky blue, vermillion
```

Apply:

```python
import matplotlib.pyplot as plt
plt.rcParams['axes.prop_cycle'] = plt.cycler(color=OKABE_ITO)
```

### Wong (Nature Methods — 8 colors)

A reordering of Okabe-Ito with black first. Equivalent in colorblind safety; pick whichever you find more aesthetic.

```python
WONG = ['#000000', '#E69F00', '#56B4E9', '#009E73',
        '#F0E442', '#0072B2', '#D55E00', '#CC79A7']
```

### Paul Tol Bright (7 colors)

A more saturated alternative. Excellent for plots that will be projected on screens.

```python
TOL_BRIGHT = ['#4477AA', '#EE6677', '#228833', '#CCBB44',
              '#66CCEE', '#AA3377', '#BBBBBB']
# blue, red, green, yellow, cyan, purple, gray
```

### Paul Tol Muted (9 colors)

Lower saturation. Use for plots with many series where saturation fatigues the eye.

```python
TOL_MUTED = ['#332288', '#88CCEE', '#44AA99', '#117733', '#999933',
             '#DDCC77', '#CC6677', '#882255', '#AA4499']
```

### Tol High Contrast (3 colors)

For plots with exactly three series where you want maximum distinguishability, including in B/W.

```python
TOL_HIGH_CONTRAST = ['#004488', '#DDAA33', '#BB5566']
# dark blue, gold, red — survives grayscale
```

## Sequential Colormaps (Continuous Single-Variable Data)

For heatmaps and density plots: latency over (workload, concurrency); cache miss rate over (cache size, line size); attention weight over (token, head); etc.

### Perceptually Uniform (Recommended)

These maps have uniform perceptual change across the scale, so a unit step in data corresponds to a unit step in apparent color difference.

| Map | Best for | Notes |
|-----|----------|-------|
| `viridis` | Default for CS heatmaps | Blue → yellow; survives grayscale; matplotlib default |
| `cividis` | Colorblind-optimized | Designed specifically for protanopia/deuteranopia |
| `plasma` | More aesthetic option | Purple → orange; grayscale-safe |
| `inferno` | Dark-background plots | Black → yellow; high contrast |
| `magma` | Subtle emphasis | Black → pink; less saturated than inferno |

```python
plt.imshow(data, cmap='viridis')
```

### Forbidden Sequential Maps

- `jet` and `rainbow`: not perceptually uniform; over-emphasize the midrange; fail in grayscale; reviewers will flag.
- `hsv`: cyclical, never appropriate for non-cyclical data.

## Diverging Colormaps (Centered Data)

For data with a meaningful zero or center: speedup ratio (1× = baseline), correlation, log-fold change, signed delta.

### Colorblind-Safe Diverging Maps

| Map | Endpoints | Use case |
|-----|-----------|----------|
| `RdBu_r` | Red — white — blue | Standard correlation matrices |
| `PuOr` | Purple — orange | Excellent for colorblind |
| `BrBG` | Brown — green | Good for ablation deltas |
| `coolwarm` | Cool blue — warm red | Slightly less colorblind-safe than RdBu but more visually intuitive |

Always center the colormap at the meaningful value:

```python
import matplotlib.colors as mcolors
norm = mcolors.TwoSlopeNorm(vcenter=1.0, vmin=0.5, vmax=2.0)  # 1× speedup centered
ax.imshow(speedup, cmap='RdBu_r', norm=norm)
```

### Forbidden Diverging Maps

- `RdYlGn` and `RdGn`: red-green axes are unreadable for ~ 8 % of male readers.

## Method-to-Color Consistency

Pin one color per method across **every figure in the paper**. Define centrally and import:

```python
# .writing/figures/src/_palette.py
"""Shared method colors for all paper figures."""

METHOD_COLORS = {
    'baseline':       '#56B4E9',   # sky blue
    'ours':           '#D55E00',   # vermillion
    'ablation_no_x':  '#009E73',   # green
    'ablation_no_y':  '#CC79A7',   # pink
    'ideal':          '#000000',   # black (theoretical bound)
    'prior_work_a':   '#E69F00',   # orange
    'prior_work_b':   '#0072B2',   # blue
}

METHOD_MARKERS = {
    'baseline':       'o',
    'ours':           's',
    'ablation_no_x':  '^',
    'ablation_no_y':  'v',
    'ideal':          '*',
    'prior_work_a':   'D',
    'prior_work_b':   'P',
}

METHOD_STYLES = {
    'baseline':       '-',
    'ours':           '-',     # solid for the two foreground methods
    'ablation_no_x':  '--',
    'ablation_no_y':  '--',
    'ideal':          ':',     # dotted for theoretical
    'prior_work_a':   '-.',
    'prior_work_b':   '-.',
}
```

Use everywhere:

```python
from _palette import METHOD_COLORS, METHOD_MARKERS, METHOD_STYLES

for method in ['baseline', 'ours', 'ablation_no_x']:
    ax.plot(x, results[method],
            color=METHOD_COLORS[method],
            marker=METHOD_MARKERS[method],
            linestyle=METHOD_STYLES[method],
            label=method.replace('_', ' ').title())
```

## Grayscale Verification

CS conferences increasingly publish digital-only proceedings, but reviewers print and many readers default to B/W. Verify:

```bash
# Convert PDF figure to grayscale and visually inspect
convert -colorspace gray foo.pdf foo_gray.pdf
```

Or in Python at save time:

```python
from PIL import Image, ImageOps
img = Image.open('foo.png').convert('RGB')
gray = ImageOps.grayscale(img)
gray.save('foo_gray.png')
```

If two series collapse to the same shade, the figure depends on color too heavily. Fix by:

1. Adding distinct line styles (`'-'`, `'--'`, `':'`).
2. Adding distinct markers (`'o'`, `'s'`, `'^'`).
3. Adding bar hatching (`hatch='//'` or `'xx'` or `'..'`).
4. Choosing colors with more luminance separation.

For bars, hatches:

```python
patterns = ['', '//', 'xx', '..', '++', '\\\\']
for i, (label, value) in enumerate(zip(labels, values)):
    ax.bar(i, value, color=METHOD_COLORS[label], hatch=patterns[i],
           edgecolor='black', linewidth=0.5)
```

## Colorblind Simulation

Test categorical figures with a CVD simulator:

- **Coblis** (https://www.color-blindness.com/coblis-color-blindness-simulator/): browser-based, drop in a PNG.
- **Color Oracle** (https://colororacle.org/): desktop tool for macOS / Windows / Linux; toggles whole-screen simulation.
- **Sim Daltonism** (macOS only): live magnifier with deuteranopia / protanopia / tritanopia modes.

Test the three common types: deuteranopia (~ 5 % of males), protanopia (~ 2 %), tritanopia (< 1 %).

In Python with `colorspacious`:

```python
from colorspacious import cspace_convert
import numpy as np

def simulate_cvd(rgb_image, severity=100):
    """Simulate deuteranopia. rgb_image: (H, W, 3) array, 0–1 floats."""
    cvd_space = {'name': 'sRGB1+CVD', 'cvd_type': 'deuteranomaly', 'severity': severity}
    return cspace_convert(rgb_image, cvd_space, 'sRGB1').clip(0, 1)
```

## Domain-Specific Palettes for CS

Unlike biology, CS rarely has hard-coded color conventions. The few cases that do:

- **Roofline plots**: ridge line in solid black; compute-bound region usually warm (red / orange); memory-bound region cool (blue).
- **Latency CDFs**: median in lighter shade, p99 / p99.9 in darker shades of the same hue. Conveys "deeper into tail" through luminance.
- **Cache hierarchy heatmaps**: viridis or cividis. L1 / L2 / L3 / DRAM as separate panels rather than separate colors on one plot.
- **Confusion matrices**: viridis or `Blues` (sequential single-hue); annotate every cell with the count.

## Avoid

1. **`jet` for any purpose.** Period. The hue ordering misleads, the luminance ordering is non-monotonic.
2. **Red + green for paired data.** ~ 8 % of male readers cannot distinguish.
3. **More than 7 categorical series.** Beyond seven, even Okabe-Ito gets confusing. Split into panels or use a faceted figure.
4. **Color as the only encoding.** Always pair with line style, marker, or hatch.
5. **Inconsistent meaning.** Blue means "baseline" on figure 1, "ours" on figure 4 — don't.
6. **Saturation max-out.** Fully-saturated colors fatigue and clash. Tol Muted exists for this reason.
7. **Implicit color = magnitude assumption.** A reader assumes darker = bigger. Don't break this with reversed maps unless captioned.

## Resources

- ColorBrewer 2.0 — https://colorbrewer2.org/ (filter by colorblind-safe)
- Paul Tol palettes — https://personal.sron.nl/~pault/
- Okabe-Ito origin — Okabe & Ito, "Color Universal Design," 2008
- matplotlib colormaps — https://matplotlib.org/stable/users/explain/colors/colormaps.html
- seaborn palettes — https://seaborn.pydata.org/tutorial/color_palettes.html

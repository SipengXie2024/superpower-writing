# Color Palettes for CS Figures

CS-tailored guidance: the default semantic palette (from figures4papers) and the strict colorblind-safe alternatives, perceptually uniform colormaps for heatmaps, conventions for method-to-color consistency, and grayscale verification. Drops biology-specific guidance (fluorophores, DNA bases, microscopy channels) — those live in the upstream skill if you need them.

## Contents

- **Default: the figures4papers Semantic Palette**: color by role (ours, related family, contrasting family, reference), family shading, ablation shade ramps, and the measured colorblind limits with the redundancy rule they force.
- **Categorical Palettes (Discrete Series)**: hex codes for Okabe-Ito, Wong, and three Paul Tol sets, plus the trimmed 2, 3, and 4 color subsets, for figures that need strict colorblind safety without redundant encoding.
- **Sequential Colormaps (Continuous Single-Variable Data)**: which perceptually uniform map to use for heatmaps (viridis, cividis, plasma, inferno, magma), and why jet, rainbow, and hsv are rejected.
- **Diverging Colormaps (Centered Data)**: maps for data with a meaningful center such as speedup or correlation, and how to pin the norm to that center.
- **Method-to-Color Consistency**: the shared `_palette.py` pattern, filled from the default palette, that fixes one color, marker, and line style per method across every figure in the paper.
- **Grayscale Verification**: convert a figure to B/W, and fix series that collapse to the same shade with line styles, markers, or bar hatching.
- **Colorblind Simulation**: simulator tools (Coblis, Color Oracle, Sim Daltonism) and a `colorspacious` pairwise checker for a project's `METHOD_COLORS` under deuteranopia, protanopia, and tritanopia.
- **Domain-Specific Palettes for CS**: the few color conventions CS does have, covering roofline plots, latency CDFs, cache hierarchy heatmaps, and confusion matrices.
- **Avoid, Resources**: seven recurring color mistakes to check a finished figure against, then links to ColorBrewer, Paul Tol, matplotlib, and seaborn palette references.

## Default: the figures4papers Semantic Palette

The default comes from Chen Liu's figures4papers repository (https://github.com/ChenLiu-1996/figures4papers), whose figures appeared in Nature Machine Intelligence, ICML, NeurIPS, and ECCV papers. Colors are assigned by **role**, not taken in cycle order: the reader learns the roles from the first figure and reads every later one faster.

```python
F4P = {
    'blue_main':      '#0F4D92',  # the proposed method, always
    'blue_secondary': '#3775BA',  # ablation variants of the proposed method
    'green_1': '#DDF3DE', 'green_2': '#AADCA9', 'green_3': '#8BCF8B',  # related family, light to dark
    'red_1':   '#F6CFCB', 'red_2':   '#E9A6A1', 'red_strong': '#B64342',  # contrasting family
    'red_mid': '#D88F8A',             # a single contrasting baseline on a line plot
    'teal':    '#42949E', 'violet': '#9A4D8E',   # extra categories
    'neutral': '#CFCECE',             # background or reference bars (fill only)
    'gray':    '#767676', 'gray_dark': '#4D4D4D',  # reference lines, text
    'highlight': '#FFD700',           # one callout per figure, never a series
}
# Cycle for lines and markers when roles are not assigned by hand.
F4P_CYCLE = ['#0F4D92', '#B64342', '#8BCF8B', '#42949E', '#767676']
```

`assets/color_palettes.py` ships these as `F4P`, `F4P_CYCLE`, `F4P_GREENS`, and `F4P_REDS`; `apply_palette('f4p')` and every bundled `.mplstyle` use the cycle.

### Role rules

- **Ours is the darkest blue and sits last or first in a fixed position** (right end of a bar group, top of a horizontal-bar list). No other method uses blue.
- **Color a family, shade a variant.** Methods from one family (BigMHC-EL / BigMHC-IM / BigMHC-retrained, or three sizes of one distilled model) share a hue and step from light to dark, with the strongest member nearest to ours. The reader groups them without reading the legend.
- **Related methods take green, contrasting ones take red.** Green for the family the paper builds on or improves; red for the approach the paper argues against. A single baseline on a line plot takes `red_mid` or `red_strong`.
- **References take gray.** Oracle bounds, "SFT only", chance level, and prior-art context are gray (`neutral` as a fill, `gray` as a line).
- **Ablations of ours use one blue at rising strength.** Order variants from fewest to most components and step the alpha of `blue_secondary` from 0.2 to 1.0, so the shade itself says "more complete". Pattern 14 in `matplotlib_examples.md`.
- **`highlight` gold marks one thing**, such as the cell or point the text calls out. Two gold marks cancel each other.

### Measured colorblind limits (the redundancy it forces)

The palette was checked with `colorspacious` (CAM02-UCS distance under full-severity simulated deuteranopia, protanopia, and tritanopia; the checker is under Colorblind Simulation below). Okabe-Ito's weakest pair scores about 11 on the same test.

| Pair | Worst simulated distance | Consequence |
|---|---|---|
| First four of `F4P_CYCLE` (blue, red, green, teal) | 21.1 | Safe as colors alone for up to four series |
| `F4P_CYCLE` with its fifth color, `gray` | 12.8 | From the fifth series on, marker and line style must distinguish |
| `blue_main` vs `violet` (protanopia) | 8.7 | Violet is out of the cycle; keep it off any figure that shows ours |
| A light red (`red_1`, `red_2`, `red_mid`) vs a green of similar lightness (deuteranopia) | 4.4 to 8.1 | Hard rule below |
| `red_strong` vs any green | 28 or more | Safe; this is why `red_strong` is the default single baseline |
| `red_1` vs `neutral` (protanopia) | 4.2 | Never use both as fills in one figure |

**Hard rule:** when a light red (`red_1`, `red_2`, `red_mid`) appears in the same figure as any green, give the red family a hatch (bars) or a dashed line style (lines). A tick or direct label on every bar or line also suffices (Pattern 16 relies on this because its hatch encodes a second factor). Those pairs collapse into one another for about 5 percent of male readers, and their lightness differs by less than 8 units, so grayscale print does not separate them either. `blue_main` stays distinct from both families and from `neutral` under all three simulations (distance 34 or more), which is why "ours" can carry the whole figure.

## Categorical Palettes (Discrete Series)

Use these instead of the default when the figure must be colorblind-safe by color alone (more than four series with no room for markers or hatches), or when a co-author or venue asks for a specific published palette.

### Okabe-Ito (strict colorblind alternative — 8 colors)

Designed by Okabe and Ito (2008) to be distinguishable under all forms of color vision deficiency.

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
    'ours':           '#0F4D92',   # blue_main
    'ablation_no_x':  '#3775BA',   # blue_secondary, lighter via alpha
    'ablation_no_y':  '#3775BA',
    'prior_work_a':   '#8BCF8B',   # green_3, the family we build on
    'prior_work_b':   '#AADCA9',   # green_2, same family, weaker member
    'baseline':       '#B64342',   # red_strong, the approach we argue against
    'ideal':          '#767676',   # gray reference (theoretical bound)
}
ABLATION_ALPHA = {'ablation_no_x': 0.4, 'ablation_no_y': 0.7}

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
    'baseline':       '--',    # dashed: keeps baseline and ours apart in grayscale
    'ours':           '-',
    'ablation_no_x':  '-',
    'ablation_no_y':  '-',
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

In Python with `colorspacious` (`uv run --with colorspacious --with matplotlib python check.py` when it is not installed):

```python
import itertools
import numpy as np
from colorspacious import cspace_convert
from matplotlib.colors import to_rgb

def simulate_cvd(rgb_image, cvd_type='deuteranomaly', severity=100):
    """rgb_image: (H, W, 3) or (3,) array of 0-1 floats."""
    cvd_space = {'name': 'sRGB1+CVD', 'cvd_type': cvd_type, 'severity': severity}
    return cspace_convert(rgb_image, cvd_space, 'sRGB1').clip(0, 1)

def weakest_pairs(colors, n=5):
    """Rank color pairs by their worst CAM02-UCS distance across normal vision
    and the three simulated deficiencies. Below about 10, add a marker, line
    style, or hatch; below about 5 the pair reads as one color."""
    def dist(a, b, cvd=None):
        a, b = np.array(to_rgb(a)), np.array(to_rgb(b))
        if cvd:
            a, b = simulate_cvd(a, cvd), simulate_cvd(b, cvd)
        return np.linalg.norm(cspace_convert(a, 'sRGB1', 'CAM02-UCS')
                              - cspace_convert(b, 'sRGB1', 'CAM02-UCS'))
    kinds = [None, 'deuteranomaly', 'protanomaly', 'tritanomaly']
    scored = [(min(dist(ca, cb, k) for k in kinds), na, nb)
              for (na, ca), (nb, cb) in itertools.combinations(colors.items(), 2)]
    return sorted(scored)[:n]

# from _palette import METHOD_COLORS; print(weakest_pairs(METHOD_COLORS))
```

## Domain-Specific Palettes for CS

Unlike biology, CS rarely has hard-coded color conventions. The few cases that do:

- **Roofline plots**: ridge line in solid black; compute-bound region usually warm (red / orange); memory-bound region cool (blue).
- **Latency CDFs**: median in lighter shade, p99 / p99.9 in darker shades of the same hue. Conveys "deeper into tail" through luminance.
- **Cache hierarchy heatmaps**: viridis or cividis. L1 / L2 / L3 / DRAM as separate panels rather than separate colors on one plot.
- **Confusion matrices**: viridis or `Blues` (sequential single-hue); annotate every cell with the count.

## Avoid

1. **`jet` for any purpose.** Period. The hue ordering misleads, the luminance ordering is non-monotonic.
2. **Red + green as the only difference.** ~ 8 % of male readers cannot distinguish. In the default palette the light reds collapse with the greens, so hatch or dash the reds whenever both appear (see Measured colorblind limits).
3. **More than 7 categorical series.** Beyond seven, any palette gets confusing. Split into panels or use a faceted figure.
4. **Color as the only encoding.** Always pair with line style, marker, or hatch.
5. **Inconsistent meaning.** Blue means "ours" in the default palette; letting it mean "baseline" on figure 4 undoes what the reader learned on figure 1.
6. **Saturation max-out.** Fully-saturated colors fatigue and clash. Tol Muted exists for this reason.
7. **Implicit color = magnitude assumption.** A reader assumes darker = bigger. Don't break this with reversed maps unless captioned.

## Resources

- ColorBrewer 2.0 — https://colorbrewer2.org/ (filter by colorblind-safe)
- Paul Tol palettes — https://personal.sron.nl/~pault/
- figures4papers (default palette source) — https://github.com/ChenLiu-1996/figures4papers
- Okabe-Ito origin — Okabe & Ito, "Color Universal Design," 2008
- matplotlib colormaps — https://matplotlib.org/stable/users/explain/colors/colormaps.html
- seaborn palettes — https://seaborn.pydata.org/tutorial/color_palettes.html

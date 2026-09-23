# Matplotlib Examples for CS Figures

Nineteen runnable patterns covering the figure types that appear in systems, ML, networking, and security papers. Each example assumes the publication style from `../scripts/style_presets.py` is applied:

## Contents

- **Examples 1-3, headline performance results.** Latency CDF with p50/p99 markers on a log-x axis; throughput vs concurrency with a linear-scaling reference line; per-benchmark speedup bars anchored at the 1.0x baseline.
- **Example 4, training curves over several seeds.** Mean line plus a shaded one-standard-deviation band, log-scaled loss axis.
- **Example 5, Pareto front.** Accuracy against parameter count, prior work vs ours, with the frontier drawn through the winning points.
- **Example 6, stacked bar breakdown.** Latency split into network, compute, I/O, and other, with a segment order that stays stable across bars.
- **Example 7, roofline plot.** Log-log compute roof against memory bandwidth, ridge point marked, application kernels placed as labeled dots.
- **Example 8, heatmap.** Cache miss rate on a viridis grid with a labeled colorbar and per-cell value annotations.
- **Example 9, box plus strip plot.** Per-seed variability, showing both the distribution shape and every individual run.
- **Examples 10-11, multi-panel layouts.** Three panels stacked for an IEEE single column (3.5 in wide), and a 2x3 grid spanning an ACM two-column page (7.0 in), both with (a)/(b)/(c) panel labels.
- **Example 12, grouped bar for ablations.** Variants against benchmarks, the bar-chart equivalent of an ablation table, shaded as one blue ramp.
- **Examples 13-19, figures4papers patterns.** Ablation drop arrows from a full-model reference line; a cumulative ablation ramp in horizontal bars; a family-shaded comparison row with a legend-only panel, meaningful floors, and a claim line on a data-budget curve; color × hatch composition bars; a radar with per-spoke scales; an event-annotated timeline; concept plots (a distribution gap and a shaded sphere). Adapted from https://github.com/ChenLiu-1996/figures4papers and resized to real column widths.
- **Common Adjustments.** Embedding fonts so reviewers do not hit Type 3 warnings, matching LaTeX's `\columnwidth`, using `constrained_layout` when `tight_layout` clips labels, and shrinking multi-megabyte PDFs via rasterization.
- **Tips.** Regenerating figures in a clean environment, keeping the raw data file beside the script, drawing baseline reference lines beneath bars, pinning log-scale limits, and sharing axes across panels.

```python
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import to_rgba

# Inline publication style (or use: plt.style.use('${CLAUDE_PLUGIN_ROOT}/.../ieee.mplstyle'))
plt.rcParams.update({
    'figure.dpi': 100, 'savefig.dpi': 600,
    'pdf.fonttype': 42, 'ps.fonttype': 42,  # embed fonts
    'font.family': 'sans-serif', 'font.sans-serif': ['Arial', 'Helvetica', 'DejaVu Sans'],
    'font.size': 8, 'axes.labelsize': 9, 'axes.titlesize': 9,
    'xtick.labelsize': 7, 'ytick.labelsize': 7, 'legend.fontsize': 7,
    'axes.linewidth': 0.8, 'lines.linewidth': 1.5, 'hatch.linewidth': 0.5,
    'axes.spines.top': False, 'axes.spines.right': False,
    'legend.frameon': False,
    'savefig.format': 'pdf', 'savefig.bbox': 'tight',
})

# figures4papers semantic palette (see color_palettes.md for the role rules)
F4P = {
    'blue_main': '#0F4D92', 'blue_secondary': '#3775BA',
    'green_1': '#DDF3DE', 'green_2': '#AADCA9', 'green_3': '#8BCF8B',
    'red_1': '#F6CFCB', 'red_2': '#E9A6A1', 'red_mid': '#D88F8A', 'red_strong': '#B64342',
    'teal': '#42949E', 'neutral': '#CFCECE', 'gray': '#767676', 'gray_dark': '#4D4D4D',
    'highlight': '#FFD700',
}
F4P_CYCLE = ['#0F4D92', '#B64342', '#8BCF8B', '#42949E', '#767676']
OURS, BASELINE = F4P['blue_main'], F4P['red_strong']
plt.rcParams['axes.prop_cycle'] = plt.cycler(color=F4P_CYCLE)

def text_color_on(fill):
    """Black or white text for a fill, alpha blended over the white page."""
    r, g, b, a = to_rgba(fill)
    r, g, b = (a * c + (1 - a) for c in (r, g, b))
    return 'white' if 0.299 * r + 0.587 * g + 0.114 * b < 0.5 else 'black'
```

A reusable save helper:

```python
def save_pub(fig, name, formats=('pdf',)):
    for ext in formats:
        fig.savefig(f'{name}.{ext}', bbox_inches='tight')
```

## 1. Latency CDF (ECDF over runs)

Tail behavior matters most. Log-x reveals it; linear-x hides it.

```python
def ecdf(values):
    v = np.sort(values)
    return v, np.arange(1, len(v) + 1) / len(v)

rng = np.random.default_rng(42)
baseline = rng.lognormal(mean=2.0, sigma=0.7, size=10_000)
ours     = rng.lognormal(mean=1.7, sigma=0.5, size=10_000)

fig, ax = plt.subplots(figsize=(3.5, 2.5))
for label, data, color in [('Baseline', baseline, BASELINE),
                           ('Ours', ours, OURS)]:
    x, y = ecdf(data)
    ax.plot(x, y, label=label, color=color, linewidth=1.5)

# Mark p50 and p99
for label, data, color in [('Baseline', baseline, BASELINE),
                           ('Ours', ours, OURS)]:
    p50, p99 = np.percentile(data, [50, 99])
    ax.axvline(p50, color=color, linestyle=':', linewidth=0.5, alpha=0.6)
    ax.axvline(p99, color=color, linestyle='--', linewidth=0.5, alpha=0.6)

ax.set_xscale('log')
ax.set_xlabel('Request latency (ms)')
ax.set_ylabel('CDF')
ax.set_xlim(1, 200)
ax.set_ylim(0, 1.0)
ax.legend(frameon=False, loc='lower right')
save_pub(fig, 'cdf_latency')
```

## 2. Throughput vs Concurrency (Scaling Curve)

Mark the saturation knee.

```python
clients = np.array([1, 2, 4, 8, 16, 32, 64, 128])
baseline_tput = np.array([4.8, 9.2, 17.1, 31.0, 52.4, 78.0, 92.0, 95.0])
ours_tput     = np.array([5.0, 9.9, 19.5, 38.0, 71.5, 124.0, 168.0, 178.0])

fig, ax = plt.subplots(figsize=(3.5, 2.5))
ax.plot(clients, baseline_tput, marker='o', linestyle='--', color=BASELINE, label='Baseline')
ax.plot(clients, ours_tput,     marker='s', color=OURS, label='Ours')

# Dashed line for the linear-scaling ideal
ideal = clients * ours_tput[0]
ax.plot(clients, ideal, linestyle=':', color='black', linewidth=0.8,
        label='Linear scaling')

ax.set_xscale('log', base=2)
ax.set_xlabel('Concurrent clients')
ax.set_ylabel('Throughput (k req/s)')
ax.legend(frameon=False, loc='upper left')
save_pub(fig, 'throughput_scaling')
```

## 3. Speedup Bar Chart (Per-Benchmark)

Always include the `1.0×` baseline reference.

```python
benchmarks = ['ycsb-a', 'ycsb-b', 'ycsb-c', 'tpcc', 'redis']
speedup = np.array([2.4, 1.8, 1.6, 3.1, 2.0])

fig, ax = plt.subplots(figsize=(3.5, 2.5))
bars = ax.bar(benchmarks, speedup, color=OURS, edgecolor='black', linewidth=0.5)

ax.axhline(1.0, color='black', linestyle='--', linewidth=0.8, label='Baseline')
ax.set_ylabel(r'Speedup over baseline ($\times$)')
ax.set_ylim(0, max(speedup) * 1.15)
ax.legend(frameon=False, loc='upper left')

# Annotate each bar with the speedup value
for bar, val in zip(bars, speedup):
    ax.text(bar.get_x() + bar.get_width() / 2, val + 0.05,
            f'{val:.1f}×', ha='center', va='bottom', fontsize=7)

save_pub(fig, 'speedup_per_benchmark')
```

## 4. Training Curves with Multi-Seed Bands

Mean over seeds + shaded ±1 std.

```python
steps = np.arange(0, 200) * 100  # training steps
seeds = 5

def fake_loss(seed, scale=1.0):
    rng = np.random.default_rng(seed)
    base = 4.0 * np.exp(-steps / 8000) + 0.3
    noise = rng.normal(0, 0.05, size=len(steps))
    return base * scale + noise

baseline_loss = np.stack([fake_loss(i, scale=1.0) for i in range(seeds)])
ours_loss     = np.stack([fake_loss(i + 100, scale=0.7) for i in range(seeds)])

fig, ax = plt.subplots(figsize=(3.5, 2.5))
for label, data, color in [('Baseline', baseline_loss, BASELINE),
                           ('Ours',     ours_loss,     OURS)]:
    mean = data.mean(axis=0)
    std  = data.std(axis=0)
    ax.plot(steps, mean, color=color, label=label, linewidth=1.5)
    ax.fill_between(steps, mean - std, mean + std, color=color, alpha=0.2, linewidth=0)

ax.set_xlabel('Training step')
ax.set_ylabel('Validation loss')
ax.set_yscale('log')
ax.legend(frameon=False, loc='upper right')
ax.set_title(f'Mean ± 1σ over {seeds} seeds', fontsize=8, loc='left', pad=2)
save_pub(fig, 'training_curve')
```

## 5. Pareto Front (Accuracy vs Parameters)

```python
# (params_M, accuracy)
prior_work = np.array([
    (10, 71.2), (25, 73.5), (50, 75.4), (100, 76.8), (200, 77.6), (400, 78.1)
])
ours = np.array([
    (12, 74.0), (28, 76.5), (55, 78.2), (110, 79.4), (220, 80.1)
])

fig, ax = plt.subplots(figsize=(3.5, 2.5))
ax.scatter(prior_work[:, 0], prior_work[:, 1], s=30, marker='o',
           color=F4P['neutral'], edgecolor='black', linewidth=0.5, label='Prior work')
ax.scatter(ours[:, 0], ours[:, 1], s=40, marker='*',
           color=OURS, edgecolor='black', linewidth=0.5, label='Ours')

# Pareto frontier of "ours"
pareto = ours[np.argsort(ours[:, 0])]
ax.plot(pareto[:, 0], pareto[:, 1], color=OURS, linestyle='-',
        linewidth=1.0, alpha=0.7)

ax.set_xscale('log')
ax.set_xlabel('Parameters (M)')
ax.set_ylabel('Top-1 accuracy (%)')
ax.legend(frameon=False, loc='lower right')
save_pub(fig, 'pareto')
```

## 6. Stacked Bar (Latency Breakdown)

Stable segment order across bars.

```python
configs = ['1 GB', '4 GB', '16 GB', '64 GB']
network = np.array([2.1, 2.0, 1.9, 2.0])
compute = np.array([3.2, 3.4, 5.0, 8.5])
io      = np.array([8.4, 4.5, 2.0, 1.2])
other   = np.array([0.8, 0.7, 0.7, 0.6])

components = {
    'Network': (network, F4P_CYCLE[0]),
    'Compute': (compute, F4P_CYCLE[1]),
    'I/O':     (io,      F4P_CYCLE[2]),
    'Other':   (other,   F4P_CYCLE[3]),
}

fig, ax = plt.subplots(figsize=(3.5, 2.5))
bottom = np.zeros(len(configs))
for label, (vals, color) in components.items():
    ax.bar(configs, vals, bottom=bottom, color=color,
           edgecolor='black', linewidth=0.4, label=label)
    bottom += vals

ax.set_ylabel('Median request latency (ms)')
ax.legend(frameon=False, ncol=2, loc='upper right', fontsize=6)
save_pub(fig, 'latency_breakdown_stacked')
```

## 7. Roofline Plot

Compute vs memory-bound regions on log-log axes.

```python
peak_flops = 1e12               # 1 TFLOPS
peak_bw    = 100e9              # 100 GB/s
ridge      = peak_flops / peak_bw  # arithmetic intensity at the ridge

ai = np.logspace(-1, 3, 200)    # ops/byte
roofline = np.minimum(peak_flops, ai * peak_bw)

fig, ax = plt.subplots(figsize=(3.5, 2.5))
ax.plot(ai, roofline, color='black', linewidth=1.5)
ax.axvline(ridge, linestyle=':', color='gray', linewidth=0.8)
ax.text(ridge * 1.2, peak_flops * 0.5, f'Ridge\n{ridge:.0f} ops/B',
        fontsize=6, color='gray')

# Place application points
apps = [
    ('GEMM',   100, 9.5e11, F4P_CYCLE[0]),
    ('Stencil', 8, 6.5e11, F4P_CYCLE[1]),
    ('SpMV',  0.5, 4.5e10, F4P_CYCLE[2]),
]
for name, x, y, c in apps:
    ax.scatter(x, y, s=30, color=c, zorder=5)
    ax.annotate(name, (x, y), xytext=(4, 4), textcoords='offset points',
                fontsize=6, color=c)

ax.set_xscale('log')
ax.set_yscale('log')
ax.set_xlabel('Arithmetic intensity (ops/byte)')
ax.set_ylabel('Performance (FLOPS)')
save_pub(fig, 'roofline')
```

## 8. Heatmap (Cache Miss Rate)

Sequential viridis with labeled colorbar.

```python
cache_sizes = [4, 8, 16, 32, 64, 128, 256]
line_sizes  = [16, 32, 64, 128]
rng = np.random.default_rng(0)
miss_rate = rng.uniform(0.001, 0.30, size=(len(line_sizes), len(cache_sizes)))
miss_rate = np.sort(miss_rate, axis=1)[:, ::-1]  # decrease with cache size

fig, ax = plt.subplots(figsize=(3.6, 2.5))
im = ax.imshow(miss_rate, cmap='viridis', aspect='auto')

ax.set_xticks(range(len(cache_sizes)))
ax.set_xticklabels([f'{s}' for s in cache_sizes])
ax.set_yticks(range(len(line_sizes)))
ax.set_yticklabels([f'{s} B' for s in line_sizes])
ax.set_xlabel('Cache size (KB)')
ax.set_ylabel('Line size')

cbar = plt.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
cbar.set_label('Miss rate', rotation=270, labelpad=12)

# Annotate cells
for i in range(miss_rate.shape[0]):
    for j in range(miss_rate.shape[1]):
        ax.text(j, i, f'{miss_rate[i, j]:.2f}', ha='center', va='center',
                fontsize=6, color='white' if miss_rate[i, j] < 0.15 else 'black')

save_pub(fig, 'cache_miss_heatmap')
```

## 9. Box + Strip Plot (Per-Seed Variability)

Shows the distribution shape and the individual seeds.

```python
import seaborn as sns  # bundled with most scientific-Python installs

rng = np.random.default_rng(7)
data = {
    'Baseline':  rng.normal(75.0, 1.2, 10),
    'Ours':      rng.normal(78.5, 0.9, 10),
    'Ablation':  rng.normal(76.2, 1.5, 10),
}
labels = list(data)
values = [data[k] for k in labels]

fig, ax = plt.subplots(figsize=(3.5, 2.5))
bp = ax.boxplot(values, widths=0.45, patch_artist=True, showfliers=False,
                boxprops=dict(facecolor='lightgray', edgecolor='black', linewidth=0.6),
                medianprops=dict(color='black', linewidth=1.2),
                whiskerprops=dict(linewidth=0.6),
                capprops=dict(linewidth=0.6))

for i, vals in enumerate(values):
    x = rng.normal(i + 1, 0.04, size=len(vals))
    ax.scatter(x, vals, alpha=0.6, s=14, color=F4P_CYCLE[i], zorder=5)

ax.set_xticklabels(labels)
ax.set_ylabel('Top-1 accuracy (%)')
save_pub(fig, 'per_seed_variability')
```

## 10. Multi-Panel Figure (IEEE Single Column)

Three panels stacked vertically, fitting `\columnwidth=3.5in`.

```python
from string import ascii_lowercase

fig = plt.figure(figsize=(3.5, 5.5), constrained_layout=True)
gs  = fig.add_gridspec(3, 1)

# (a) CDF
ax_a = fig.add_subplot(gs[0])
x = np.sort(np.random.default_rng(1).lognormal(2.0, 0.7, 5000))
ax_a.plot(x, np.linspace(0, 1, len(x)), color=BASELINE, linestyle='--', label='Baseline')
ax_a.plot(x * 0.6, np.linspace(0, 1, len(x)), color=OURS, label='Ours')
ax_a.set_xscale('log'); ax_a.set_xlabel('Latency (ms)'); ax_a.set_ylabel('CDF')
ax_a.legend(frameon=False, loc='lower right')

# (b) Throughput
ax_b = fig.add_subplot(gs[1])
clients = np.array([1, 2, 4, 8, 16, 32, 64])
ax_b.plot(clients, clients * 4, marker='o', linestyle='--', color=BASELINE, label='Baseline')
ax_b.plot(clients, clients * 6, marker='s', color=OURS, label='Ours')
ax_b.set_xscale('log', base=2)
ax_b.set_xlabel('Clients'); ax_b.set_ylabel('Throughput (k req/s)')
ax_b.legend(frameon=False, loc='upper left')

# (c) Speedup bar
ax_c = fig.add_subplot(gs[2])
ax_c.bar(['ycsb-a', 'ycsb-b', 'tpcc', 'redis'], [2.4, 1.8, 3.1, 2.0],
         color=OURS, edgecolor='black', linewidth=0.5)
ax_c.axhline(1.0, color='black', linestyle='--', linewidth=0.8)
ax_c.set_ylabel('Speedup ($\\times$)')

for i, ax in enumerate([ax_a, ax_b, ax_c]):
    ax.text(-0.15, 1.05, f'({ascii_lowercase[i]})',
            transform=ax.transAxes, fontsize=10, fontweight='bold', va='top')

save_pub(fig, 'multi_panel_ieee')
```

## 11. Multi-Panel Figure (ACM Two-Column Span)

Six panels in a 2×3 grid for `\textwidth=7.0in`.

```python
fig = plt.figure(figsize=(7.0, 4.0), constrained_layout=True)
gs  = fig.add_gridspec(2, 3)
axes = [fig.add_subplot(gs[i // 3, i % 3]) for i in range(6)]

rng = np.random.default_rng(2)
for i, ax in enumerate(axes):
    x = np.linspace(0, 10, 80)
    for j, color in enumerate(F4P_CYCLE[:3]):
        y = rng.normal(0, 1, len(x)).cumsum() + j * 5
        ax.plot(x, y, color=color, label=f'method {j}')
    ax.set_xlabel('Step')
    ax.set_ylabel(f'Metric {i+1}')
    ax.text(-0.18, 1.05, f'({ascii_lowercase[i]})',
            transform=ax.transAxes, fontsize=10, fontweight='bold', va='top')

axes[0].legend(frameon=False, loc='upper left', fontsize=6)
save_pub(fig, 'multi_panel_acm')
```

## 12. Ablation Table-Style Bar (Grouped)

Comparing variants × benchmarks.

```python
benchmarks = ['ycsb-a', 'ycsb-b', 'tpcc', 'redis']
variants   = ['baseline', '+feature A', '+feature B', '+both']

scores = np.array([
    [70.0, 72.5, 73.0, 76.8],   # ycsb-a
    [68.0, 70.5, 71.5, 75.0],   # ycsb-b
    [65.0, 68.0, 70.0, 73.5],   # tpcc
    [72.0, 74.0, 75.0, 78.0],   # redis
])

x = np.arange(len(benchmarks))
width = 0.20

fig, ax = plt.subplots(figsize=(7.0, 2.5))
# One blue at rising strength: the shade says how complete the variant is.
ramp = [to_rgba(F4P['blue_secondary'], a) for a in (0.25, 0.5, 0.75)] + [OURS]
for i, (variant, color) in enumerate(zip(variants, ramp)):
    ax.bar(x + (i - 1.5) * width, scores[:, i], width, label=variant,
           color=color, edgecolor='black', linewidth=0.4)

ax.set_xticks(x); ax.set_xticklabels(benchmarks)
ax.set_ylabel('Throughput (k req/s)')
ax.set_ylim(0, 85)                        # absolute throughput: zero floor
ax.legend(frameon=False, ncol=4, loc='upper left', fontsize=7)
save_pub(fig, 'ablation_grouped_bar')
```

## 13. Ablation Drop Arrows

The full model sets a dashed reference line; each removed component gets an arrow from that line down to its bar and the drop printed at the line. The reader reads the cost of each component without subtracting.

```python
variants = ['Full', 'No expr.', 'No struct.', 'No ROI', 'No seq.']
score = np.array([0.88, 0.84, 0.82, 0.81, 0.74])

fig, ax = plt.subplots(figsize=(3.5, 2.4))
colors = [OURS] + [to_rgba(F4P['blue_secondary'], 0.4)] * (len(score) - 1)
bars = ax.bar(variants, score, width=0.7, color=colors)

full = score[0]
ax.axhline(full, color=OURS, linestyle='--', linewidth=0.8, zorder=0)
for bar, val, color in zip(bars, score, colors):
    x = bar.get_x() + bar.get_width() / 2
    ax.text(x, val - 0.03, f'{val:.2f}', ha='center', va='top', fontsize=7,
            color=text_color_on(color))
    if val < full:
        ax.annotate('', xy=(x, val), xytext=(x, full),
                    arrowprops=dict(arrowstyle='->', color=F4P['red_strong'], lw=1.0))
        ax.text(x, full + 0.015, f'−{full - val:.2f}', ha='center', va='bottom',
                fontsize=6.5, color=F4P['red_strong'])

ax.set_ylim(0, 1.0)                       # zero floor: the bars are absolute scores
ax.set_ylabel('Spearman correlation ↑')
save_pub(fig, 'ablation_drop_arrows')
```

## 14. Cumulative Ablation Ramp (Horizontal Bars)

For many component combinations. Rows go from fewest to most components, the labels spell out the combination, and one blue gains strength with completeness; the full model takes `OURS`. Each panel starts at the metric's chance level, which is a meaningful floor to name in the caption.

```python
components = ['Structure', 'Sequence', 'Bchems', 'Transfer']
codes = ['1000', '0100', '1100', '0110', '1110', '0101', '1101', '1111']   # bottom to top
labels = [' + '.join(c for c, bit in zip(components, code) if bit == '1') for code in codes]
auroc = np.array([0.77, 0.84, 0.84, 0.84, 0.86, 0.85, 0.84, 0.88])
auroc_sd = np.array([0.012, 0.006, 0.006, 0.007, 0.013, 0.007, 0.006, 0.005])
auprc = np.array([0.44, 0.55, 0.55, 0.56, 0.62, 0.57, 0.55, 0.70])
auprc_sd = np.array([0.02, 0.015, 0.02, 0.02, 0.045, 0.025, 0.03, 0.02])
positive_rate = 0.20                      # AUPRC chance level = prevalence

alphas = np.linspace(0.2, 1.0, len(codes))
colors = [to_rgba(F4P['blue_secondary'], a) for a in alphas[:-1]] + [OURS]
y = np.arange(len(codes))

fig, axes = plt.subplots(1, 2, figsize=(7.0, 2.6), sharey=True)
for ax, name, mean, sd, floor in [(axes[0], 'AUROC ↑', auroc, auroc_sd, 0.5),
                                  (axes[1], 'AUPRC ↑', auprc, auprc_sd, positive_rate)]:
    ax.barh(y, mean, xerr=sd, color=colors, height=0.75,
            error_kw=dict(elinewidth=0.6, capsize=1.5, ecolor='black'))
    ax.set_xlim(floor, 1.0)
    ax.set_xlabel(name)
axes[0].set_yticks(y, labels)
axes[0].tick_params(axis='y', length=0)
save_pub(fig, 'ablation_ramp')
```

## 15. Family-Shaded Comparison Row and the Claim Line

First block: many baselines on three metrics. Baselines of one family share a hue from light to dark, ours is dark blue at the right end, and a legend-only panel replaces nine repeated tick labels. The light reds sit next to greens, so they carry a hatch. Floors: AUROC starts at chance (0.5), AUPRC at the positive rate (0.2), PPV at zero.

```python
methods = ['Prime', 'NetMHCpan', 'BigMHC-EL', 'BigMHC-IM', 'BigMHC-re', 'Ours']
colors  = [F4P['red_1'], F4P['red_2'], F4P['green_1'], F4P['green_2'], F4P['green_3'], OURS]
hatches = ['////', '////', '', '', '', '']          # light reds collapse with greens under CVD
metrics = {  # name: (means, stds, floor)
    'AUROC ↑': ([0.54, 0.54, 0.59, 0.68, 0.79, 0.88], [0.012, 0.027, 0.018, 0.028, 0.013, 0.004], 0.5),
    'AUPRC ↑': ([0.21, 0.21, 0.27, 0.32, 0.46, 0.70], [0.030, 0.020, 0.015, 0.045, 0.025, 0.018], 0.2),
    'PPV ↑':   ([0.21, 0.22, 0.29, 0.33, 0.44, 0.51], [0.012, 0.009, 0.012, 0.016, 0.004, 0.009], 0.0),
}

fig = plt.figure(figsize=(7.0, 2.0), constrained_layout=True)
gs = fig.add_gridspec(1, 4, width_ratios=[1, 1, 1, 0.8])
x = np.arange(len(methods))
for k, (name, (mean, sd, floor)) in enumerate(metrics.items()):
    ax = fig.add_subplot(gs[k])
    ax.bar(x, mean, yerr=sd, color=colors, hatch=hatches, edgecolor=F4P['gray_dark'],
           linewidth=0.4, width=0.8, label=methods,
           error_kw=dict(elinewidth=0.6, capsize=1.2))
    ax.set_ylim(bottom=floor)
    ax.set_xticks([])                     # identity comes from the legend panel
    ax.set_ylabel(name)
    if k == 0:
        handles, labels = ax.get_legend_handles_labels()
legend_ax = fig.add_subplot(gs[-1])
legend_ax.set_axis_off()
legend_ax.legend(handles, labels, loc='center left')   # same order as the bars, ours last
save_pub(fig, 'comparison_row')
```

Second block: a data-budget curve whose dotted line is the claim. Ours at 25 percent of the data already matches the best baseline at 100 percent. The gray dashed line is the shared floor every method starts from.

```python
fractions = ['10%', '25%', '50%', '100%']
x = np.arange(len(fractions))
dpo    = np.array([82.8, 83.2, 85.1, 85.7])
da_dpo = np.array([84.1, 85.5, 87.0, 87.8])
ours   = np.array([86.7, 88.1, 89.1, 89.8])
sft_only = 82.1

fig, ax = plt.subplots(figsize=(3.5, 2.3))
ax.axhline(sft_only, color=F4P['gray'], linestyle='--', linewidth=1.0, label='SFT only')
ax.plot(x, dpo, marker='o', linestyle='--', color=F4P['red_mid'], label='DPO')
ax.plot(x, da_dpo, marker='^', color=F4P['green_3'], label='DA-DPO')
ax.plot(x, ours, marker='s', color=OURS, label='Ours')
ax.hlines(ours[1], x[1], x[-1], colors=OURS, linestyles=':', linewidth=1.0)
ax.annotate('ours at 25% ≈\nDA-DPO at 100%', xy=(x[1], ours[1]), xytext=(x[0] - 0.1, 89.4),
            ha='left', va='center', fontsize=6.5, color=OURS,
            arrowprops=dict(arrowstyle='->', color=OURS, lw=0.6, shrinkB=4))
ax.set_xticks(x, fractions)
ax.set_xlabel('Fraction of post-training data')
ax.set_ylabel(r'POPE$_{\mathrm{Adv}}$ accuracy (%) ↑')
ax.legend(ncol=2, loc='lower right')
save_pub(fig, 'data_budget_claim')
```

## 16. Color × Hatch Composition Bars

Two categorical factors in one stacked bar: color names the model (repeated on the tick labels, so no color legend is needed) and hatch names the outcome type. Hatch is taken by the second factor here, which is why the tick labels, not a hatch, keep the light reds apart from the greens. The key segment's value is printed in dark or white text by fill luminance, never in yellow.

```python
models = ['Qwen\n1.5B', 'Qwen\n14B', 'Llama\n70B', 'V3', 'R1', 'o3']
colors = [F4P['green_1'], F4P['green_2'], F4P['green_3'], F4P['red_1'], F4P['red_2'], OURS]
outcomes = ['Only model', 'Only human', 'Neither', 'Both']
hatches  = ['////', '\\\\\\\\', '', 'xxx']
share = np.array([            # rows: models, columns: outcomes; each row sums to 1
    [0.27, 0.04, 0.60, 0.09],
    [0.28, 0.03, 0.60, 0.09],
    [0.24, 0.04, 0.63, 0.09],
    [0.31, 0.04, 0.56, 0.09],
    [0.14, 0.07, 0.73, 0.06],
    [0.10, 0.07, 0.80, 0.03],
])

fig, ax = plt.subplots(figsize=(3.5, 2.4))
x = np.arange(len(models))
bottom = np.zeros(len(models))
for j, (outcome, hatch) in enumerate(zip(outcomes, hatches)):
    ax.bar(x, share[:, j], bottom=bottom, width=0.75, color=colors, hatch=hatch,
           edgecolor=F4P['gray_dark'], linewidth=0.4)
    bottom += share[:, j]
for xi, val, color in zip(x, share[:, 0], colors):
    ax.text(xi, val / 2, f'{val:.2f}', ha='center', va='center', fontsize=6,
            color=text_color_on(color),
            bbox=dict(boxstyle='square,pad=0.1', facecolor=color, edgecolor='none'))

hatch_handles = [plt.Rectangle((0, 0), 1, 1, facecolor='white', edgecolor=F4P['gray_dark'],
                               hatch=h, linewidth=0.4) for h in hatches]
ax.legend(hatch_handles, outcomes, ncol=4, loc='lower center', bbox_to_anchor=(0.5, 1.0),
          handlelength=1.2, columnspacing=0.8, fontsize=6.5)
ax.set_xticks(x, models, fontsize=6.5)
ax.set_ylim(0, 1)
ax.set_ylabel('Share of solved puzzles')
save_pub(fig, 'composition_color_hatch')
```

## 17. Radar with Per-Spoke Scales

Use only when the venue or a co-author expects a radar (see `chart-chooser.md`). Benchmarks have different ranges, so each spoke gets its own scale, printed on the spoke. The honesty rule: every benchmark's range comes from **one written formula** (here, from half a spread below the lowest score to a tenth of a spread above the highest), stated in the caption. A range hand-picked per spoke can make any gap look large.

```python
spokes = {  # spoke label: scores for (DPO, DA-DPO, Ours); the benchmark follows the newline
    'Qwen-7B\nPOPE':      [82.8, 84.2, 86.9],
    'Qwen-72B\nPOPE':     [84.5, 87.4, 89.8],
    'Qwen-7B\nMathVista': [48.0, 48.8, 49.5],
    'Qwen-72B\nMathVista':[54.1, 55.4, 56.6],
    'Qwen-7B\nMMBench':   [71.2, 72.0, 72.5],
    'Qwen-72B\nMMBench':  [77.2, 77.8, 78.5],
}
methods = ['DPO', 'DA-DPO', 'Ours']
colors = [F4P['red_mid'], F4P['green_3'], OURS]
styles = ['--', '-.', '-']                 # light red next to green: dash it

bench = [k.split('\n')[1] for k in spokes]
ranges = {}
for b in set(bench):
    vals = np.concatenate([v for k, v in spokes.items() if k.endswith(b)])
    spread = vals.max() - vals.min()
    ranges[b] = (np.floor(vals.min() - 0.5 * spread), np.ceil(vals.max() + 0.1 * spread))

def radius(v, b, inner=0.25):             # inner hole keeps the lowest score off the center
    lo, hi = ranges[b]
    return inner + (1 - inner) * (v - lo) / (hi - lo)

angles = np.linspace(0, 2 * np.pi, len(spokes), endpoint=False)
closed = np.append(angles, angles[0])
fig, ax = plt.subplots(figsize=(3.5, 3.3), subplot_kw=dict(projection='polar'))
ax.set_theta_zero_location('N'); ax.set_theta_direction(-1)
ax.grid(False); ax.spines['polar'].set_visible(False)
ax.set_yticks([]); ax.set_ylim(0, 1.0)
for frac in (0.25, 0.625, 1.0):            # rings at the inner edge, middle, and top of range
    ax.plot(closed, np.full_like(closed, frac), color=F4P['neutral'], linewidth=0.5)
for a, b in zip(angles, bench):
    ax.plot([a, a], [0.25, 1.0], color=F4P['neutral'], linewidth=0.5)
    lo, hi = ranges[b]
    for frac, val in ((0.25, lo), (1.0, hi)):
        ax.text(a, frac, f'{val:.0f}', fontsize=5.5, color=F4P['gray'], ha='center', va='center',
                bbox=dict(boxstyle='square,pad=0.05', facecolor='white', edgecolor='none'))
for m, (name, color, ls) in enumerate(zip(methods, colors, styles)):
    r = [radius(v[m], b) for v, b in zip(spokes.values(), bench)]
    r = np.append(r, r[0])
    ax.plot(closed, r, color=color, linestyle=ls, linewidth=1.2, marker='o', markersize=2.5,
            label=name)
    ax.fill(closed, r, color=color, alpha=0.06)
ax.set_xticks(angles, list(spokes), fontsize=6)
ax.tick_params(axis='x', pad=6)
ax.legend(loc='lower center', bbox_to_anchor=(0.5, -0.22), ncol=3)
save_pub(fig, 'radar_per_spoke')
```

## 18. Event-Annotated Timeline

A cumulative count over months with the events that explain its jumps. Each layer is a filled area with a darker outline; arrows name the events above the curve. A second population goes in a second panel with hatching rather than a third color.

```python
months = np.arange('2023-01', '2025-08', dtype='datetime64[M]')
rng = np.random.default_rng(3)
method_new = rng.poisson(0.35, len(months)).cumsum()
eval_new = rng.poisson(3.0, len(months)).cumsum()
events = [('2023-03', 'GPT-4'), ('2023-07', 'LLaMA 2'), ('2024-02', 'Gemini 1.5'),
          ('2024-04', 'LLaMA 3'), ('2024-12', 'Gemini 2.0')]

fig, ax = plt.subplots(figsize=(7.0, 2.2))
ax.fill_between(months, 0, method_new, color=to_rgba(F4P['blue_secondary'], 0.45), linewidth=0,
                label='Method papers')
ax.fill_between(months, method_new, method_new + eval_new, color=F4P['red_2'], linewidth=0,
                label='Evaluation papers')
ax.plot(months, method_new, color=OURS, linewidth=1.2)
ax.plot(months, method_new + eval_new, color=BASELINE, linewidth=1.2)
total = method_new + eval_new
for date, name in events:
    d = np.datetime64(date, 'M')
    y = total[months == d][0]
    ax.annotate(name, xy=(d, y), xytext=(0, 14), textcoords='offset points', ha='center',
                fontsize=6, arrowprops=dict(arrowstyle='-|>', color='black', lw=0.6,
                                            shrinkA=0, shrinkB=1, mutation_scale=5))
ax.set_ylim(0, total.max() * 1.25)
ax.set_ylabel('Cumulative papers')
ax.legend(loc='upper left')
save_pub(fig, 'event_timeline')
```

## 19. Concept Plots

A concept plot shows a mechanism with idealized data, not a measurement. It uses the result figures' palette and fonts, carries no numeric ticks a reader could quote, and its caption says it is illustrative. Two forms recur.

A distribution gap: what the model believes with and without the evidence, and the gap the method maximizes.

```python
def bump(x, mu, sigma, peak=1.0):
    return peak * np.exp(-0.5 * ((x - mu) / sigma) ** 2)

x = np.linspace(-1, 1, 400)
prior = bump(x, -0.4, 0.15)                              # text-only belief
blind = bump(x, -0.4, 0.3, 0.5) + 0.22                   # evidence removed
grounded = bump(x, 0.45, 0.12)                           # evidence present

fig, ax = plt.subplots(figsize=(3.5, 2.1))
for y, color, label in [(prior, F4P['gray'], r'$P(y \mid x_t)$'),
                        (blind, F4P['red_mid'], r'$P(y \mid x_v^{\varnothing}, x_t)$'),
                        (grounded, OURS, r'$P(y \mid x_v, x_t)$')]:
    ax.plot(x, y, color=color, linewidth=1.3, label=label)
    ax.fill_between(x, 0, y, color=color, alpha=0.1, linewidth=0)
peak_x = x[grounded.argmax()]
ax.annotate('', xy=(peak_x, grounded.max()), xytext=(peak_x, blind[grounded.argmax()]),
            arrowprops=dict(arrowstyle='<->', color='black', lw=0.8))
ax.text(peak_x + 0.05, 0.6, 'gap', fontsize=7, va='center')
ax.set_xticks([]); ax.set_yticks([])                    # illustrative: no quotable numbers
ax.set_xlabel('Answer space (illustrative)')
ax.set_ylabel('Probability')
ax.legend(loc='upper left', ncol=3, fontsize=6.5, handlelength=1.2, columnspacing=0.8,
          bbox_to_anchor=(0, 1.12))
save_pub(fig, 'concept_distribution_gap')
```

A geometric picture: embeddings on a shaded unit sphere, pushed apart. The sphere is an `imshow` of Lambertian shading (rasterized inside the PDF at `savefig.dpi`); points are the visible hemisphere's projections; labels sit in white boxes so they read over the shading.

```python
res = 400
u = np.linspace(-1, 1, res)
X, Y = np.meshgrid(u, u)
Z = np.sqrt(np.clip(1 - X**2 - Y**2, 0, None))
light = np.array([-0.5, 0.6, 0.6]) / np.linalg.norm([-0.5, 0.6, 0.6])
shade = np.clip(X * light[0] + Y * light[1] + Z * light[2], 0, 1)
sphere = np.ones((res, res, 4))
sphere[..., :3] = (0.62 + 0.38 * shade)[..., None]
sphere[..., 3] = (X**2 + Y**2 <= 1).astype(float)

fig, ax = plt.subplots(figsize=(2.2, 2.2))
ax.imshow(sphere, extent=(-1, 1, -1, 1), origin='lower', interpolation='bilinear')
pts = np.array([[-0.5, 0.55], [0.85, 0.05], [-0.75, -0.45]])     # (x, y) with z > 0
for p in pts:
    ax.plot([0, p[0]], [0, p[1]], color='black', linestyle='--', linewidth=0.5)
ax.scatter(pts[:, 0], pts[:, 1], s=14, color=F4P['blue_secondary'], edgecolor='black',
           linewidth=0.4, zorder=5)
for a, b in [(0, 1), (1, 2), (2, 0)]:
    ax.annotate('', xy=pts[b], xytext=pts[a],
                arrowprops=dict(arrowstyle='<->', color=F4P['red_strong'], lw=1.0,
                                connectionstyle='arc3,rad=-0.25', shrinkA=3, shrinkB=3))
ax.text(0.2, 0.62, 'disperse', fontsize=6.5, color=F4P['red_strong'], ha='center',
        bbox=dict(boxstyle='round,pad=0.15', facecolor='white', edgecolor='none'))
ax.set_xlim(-1.05, 1.05); ax.set_ylim(-1.05, 1.05); ax.set_aspect('equal'); ax.axis('off')
save_pub(fig, 'concept_sphere')
```

## Common Adjustments

### Embedding fonts (avoid Type 3 warnings)

```python
plt.rcParams['pdf.fonttype'] = 42  # TrueType
plt.rcParams['ps.fonttype']  = 42
```

Verify with `pdffonts foo.pdf` — every font should show "yes" in the `emb` column and "TrueType" or "Type 1" (not Type 3).

### Using `\columnwidth` directly

For tight integration, query LaTeX's column width and pass it to Python via a `--width` CLI argument. Easier: just hardcode `3.5` (IEEE) or `3.33` (ACM/USENIX) and verify visually.

### Avoiding the `tight_layout` clip

`tight_layout()` sometimes clips panel labels or external legends. Use `constrained_layout=True` in the figure constructor:

```python
fig = plt.figure(figsize=(3.5, 2.5), constrained_layout=True)
```

### Reducing PDF file size

Vector PDF should be small (< 100 KB for a typical line plot). If yours is multi-MB:

- Heatmap with too many cells: render via `imshow` with raster downsampling, save as PNG instead.
- Scatter with > 10k points: add `rasterized=True` to the scatter call:

```python
ax.scatter(x, y, s=4, alpha=0.5, rasterized=True)
fig.savefig('big_scatter.pdf', dpi=300)  # rasterized parts use this dpi
```

## Tips

- Always run the figure-generation script in a clean environment before submission. Once-tweaked Jupyter state is invisible to reviewers and breaks reproducibility.
- Keep the data file under version control next to the script: `.writing/figures/data/<fig_id>.csv` or `.jsonl`. Reviewers asking "what's the raw data?" should get an immediate answer.
- For bar plots with 1.0× references, draw the reference *under* the bars by setting `zorder` lower on the line and calling `axhline` before `bar`.
- When plotting log-scale data, set the limits explicitly (`ax.set_xlim(1, 1e6)`) — auto-limits sometimes pick weird endpoints.
- For multi-panel figures with shared axes, `plt.subplots(sharex=True)` simplifies the alignment but be careful with axis labels — `ax.set_xlabel` only affects the bottom row by default.

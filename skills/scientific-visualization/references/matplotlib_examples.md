# Matplotlib Examples for CS Figures

Twelve runnable patterns covering the figure types that appear in systems, ML, networking, and security papers. Each example assumes the publication style from `../scripts/style_presets.py` is applied:

```python
import matplotlib.pyplot as plt
import numpy as np

# Inline publication style (or use: plt.style.use('${CLAUDE_PLUGIN_ROOT}/.../ieee.mplstyle'))
plt.rcParams.update({
    'figure.dpi': 100, 'savefig.dpi': 600,
    'pdf.fonttype': 42, 'ps.fonttype': 42,  # embed fonts
    'font.family': 'sans-serif', 'font.sans-serif': ['Arial', 'Helvetica', 'DejaVu Sans'],
    'font.size': 8, 'axes.labelsize': 9, 'axes.titlesize': 9,
    'xtick.labelsize': 7, 'ytick.labelsize': 7, 'legend.fontsize': 7,
    'axes.linewidth': 0.5, 'lines.linewidth': 1.5,
    'axes.spines.top': False, 'axes.spines.right': False,
    'savefig.format': 'pdf', 'savefig.bbox': 'tight',
})
plt.rcParams['axes.prop_cycle'] = plt.cycler(color=[
    '#0072B2', '#D55E00', '#009E73', '#CC79A7', '#E69F00', '#56B4E9'
])

OKABE_ITO_4 = ['#0072B2', '#D55E00', '#009E73', '#CC79A7']
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
for label, data, color in [('Baseline', baseline, OKABE_ITO_4[0]),
                           ('Ours', ours, OKABE_ITO_4[1])]:
    x, y = ecdf(data)
    ax.plot(x, y, label=label, color=color, linewidth=1.5)

# Mark p50 and p99
for label, data, color in [('Baseline', baseline, OKABE_ITO_4[0]),
                           ('Ours', ours, OKABE_ITO_4[1])]:
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
ax.plot(clients, baseline_tput, marker='o', color=OKABE_ITO_4[0], label='Baseline')
ax.plot(clients, ours_tput,     marker='s', color=OKABE_ITO_4[1], label='Ours')

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
bars = ax.bar(benchmarks, speedup, color=OKABE_ITO_4[1], edgecolor='black', linewidth=0.5)

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
for label, data, color in [('Baseline', baseline_loss, OKABE_ITO_4[0]),
                           ('Ours',     ours_loss,     OKABE_ITO_4[1])]:
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
           color=OKABE_ITO_4[0], edgecolor='black', linewidth=0.5, label='Prior work')
ax.scatter(ours[:, 0], ours[:, 1], s=40, marker='*',
           color=OKABE_ITO_4[1], edgecolor='black', linewidth=0.5, label='Ours')

# Pareto frontier of "ours"
pareto = ours[np.argsort(ours[:, 0])]
ax.plot(pareto[:, 0], pareto[:, 1], color=OKABE_ITO_4[1], linestyle='-',
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
    'Network': (network, OKABE_ITO_4[0]),
    'Compute': (compute, OKABE_ITO_4[1]),
    'I/O':     (io,      OKABE_ITO_4[2]),
    'Other':   (other,   OKABE_ITO_4[3]),
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
    ('GEMM',   100, 9.5e11, OKABE_ITO_4[0]),
    ('Stencil', 8, 6.5e11, OKABE_ITO_4[1]),
    ('SpMV',  0.5, 4.5e10, OKABE_ITO_4[2]),
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
    ax.scatter(x, vals, alpha=0.6, s=14, color=OKABE_ITO_4[i], zorder=5)

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
ax_a.plot(x, np.linspace(0, 1, len(x)), color=OKABE_ITO_4[0], label='Baseline')
ax_a.plot(x * 0.6, np.linspace(0, 1, len(x)), color=OKABE_ITO_4[1], label='Ours')
ax_a.set_xscale('log'); ax_a.set_xlabel('Latency (ms)'); ax_a.set_ylabel('CDF')
ax_a.legend(frameon=False, loc='lower right')

# (b) Throughput
ax_b = fig.add_subplot(gs[1])
clients = np.array([1, 2, 4, 8, 16, 32, 64])
ax_b.plot(clients, clients * 4, marker='o', color=OKABE_ITO_4[0], label='Baseline')
ax_b.plot(clients, clients * 6, marker='s', color=OKABE_ITO_4[1], label='Ours')
ax_b.set_xscale('log', base=2)
ax_b.set_xlabel('Clients'); ax_b.set_ylabel('Throughput (k req/s)')
ax_b.legend(frameon=False, loc='upper left')

# (c) Speedup bar
ax_c = fig.add_subplot(gs[2])
ax_c.bar(['ycsb-a', 'ycsb-b', 'tpcc', 'redis'], [2.4, 1.8, 3.1, 2.0],
         color=OKABE_ITO_4[1], edgecolor='black', linewidth=0.5)
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
    for j, color in enumerate(OKABE_ITO_4[:3]):
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
for i, (variant, color) in enumerate(zip(variants, OKABE_ITO_4)):
    ax.bar(x + (i - 1.5) * width, scores[:, i], width, label=variant,
           color=color, edgecolor='black', linewidth=0.4)

ax.set_xticks(x); ax.set_xticklabels(benchmarks)
ax.set_ylabel('Throughput (k req/s)')
ax.set_ylim(60, 80)
ax.legend(frameon=False, ncol=4, loc='upper left', fontsize=7)
save_pub(fig, 'ablation_grouped_bar')
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

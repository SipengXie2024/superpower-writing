# CS Venue Figure Requirements

Per-venue specifications for figure dimensions, fonts, formats, and quirks. Always cross-check the venue's current Author Guide — these requirements drift between editions.

## Quick Reference Table

| Venue | Single column | Double / full | Min DPI (raster) | Preferred format | Class file |
|-------|---------------|----------------|------------------|------------------|-------------|
| IEEE Trans. / Conf. | 3.5 in (8.9 cm) | 7.16 in (18.2 cm) | 600 line / 300 photo | PDF, EPS | `IEEEtran` |
| ACM (sigconf) | 3.33 in (8.46 cm) | 7.0 in (17.78 cm) | 600 | PDF | `acmart` |
| ACM (acmsmall) | 4.85 in (12.3 cm) full | 4.85 in | 600 | PDF | `acmart` |
| USENIX (Annual / OSDI / NSDI / Sec.) | 3.33 in | 7.0 in | 300 | PDF | `usenix2019_v3` |
| NeurIPS | 5.5 in (14.0 cm) full | 5.5 in | n/a (vector) | PDF | `neurips_2024` |
| ICML | 6.75 in (17.1 cm) full | 6.75 in | n/a (vector) | PDF | `icml2024` |
| ICLR | 5.5 in full | 5.5 in | n/a (vector) | PDF | `iclr2024_conference` |
| arXiv preprint | follow target venue | — | follow target venue | PDF | venue style |

The "single column" / "double column" distinction collapses to one column for ML conferences (NeurIPS / ICML / ICLR), which use a one-column layout with a wide text block.

## IEEE (Transactions and Conferences)

### Dimensions

- Single column: 3.5 in (88.9 mm). Use `figsize=(3.5, h)` where `h` ≤ 9 in.
- Double column: 7.16 in (181.86 mm). Use `figsize=(7.16, h)` for figures that span both columns via `\begin{figure*}`.
- Maximum height: 9.7 in.

### Format and Resolution

- PDF or EPS. Both vector. PDF is the modern default.
- Photos / raster: 300 DPI minimum, 600 DPI preferred.
- Line art: 600 DPI minimum if rasterized. Vector PDF preferred.
- Embed fonts: `pdf.fonttype: 42`. IEEE eXpress flags Type 3 fonts.

### Typography

- Sans-serif: Arial or Helvetica.
- Body font in the paper itself is Times via `IEEEtran`, but figures should still be sans-serif — the contrast is intentional.
- Minimum 8 pt at final size for axis labels; 6 pt absolute floor for tick labels.

### Other Conventions

- Panel labels: `(a)`, `(b)`, `(c)` — lowercase parenthesized.
- Captions below the figure (always; never beside or above).
- Figure numbering: `Fig. 1`, `Fig. 2` (not `Figure 1`).
- Color is free for online publication; print proceedings sometimes B/W.
- Run the IEEE PDF eXpress check before submission to catch font and PDF version issues.

### LaTeX Inclusion Pattern

```latex
% Single column
\begin{figure}[t]
  \centering
  \includegraphics[width=\columnwidth]{figures/cdf_latency.pdf}
  \caption{p99 latency CDF over 10 runs of YCSB-A.}
  \label{fig:cdf-latency}
\end{figure}

% Double column (spans across both columns at the page top/bottom)
\begin{figure*}[t]
  \centering
  \includegraphics[width=\textwidth]{figures/system_arch.pdf}
  \caption{System architecture.}
  \label{fig:arch}
\end{figure*}
```

## ACM (acmart class — sigconf, acmsmall, acmlarge)

### Dimensions

The `acmart` class has two distinct layouts; check the manuscript's `\documentclass` line:

- **`sigconf` (most conferences: SIGCOMM, SOSP, OSDI, PLDI, etc.)**: two-column layout. `\columnwidth` is 3.33 in (8.46 cm); `\textwidth` for `figure*` is 7.0 in (17.78 cm).
- **`acmsmall` (most journals: TOPLAS, TOCS, etc.)**: one-column layout. `\textwidth` is roughly 4.85 in (12.3 cm). No `figure*` needed.
- **`acmlarge` (TPDS, etc.)**: one-column with wider margins, ~ 5.5 in.

Run `\the\columnwidth` and `\the\textwidth` in the actual manuscript to confirm — `acmart` versions vary.

### Format and Resolution

- PDF strongly preferred.
- 600 DPI for raster; 300 DPI absolute minimum.
- Embed fonts. ACM's PDF validator will reject submissions with Type 3 fonts.

### Typography

- Sans-serif in figures. Body font in `acmart` is Linux Libertine; figures look fine in Arial.
- Minimum sizes: 7 pt axis labels, 6 pt tick labels at final size — slightly tighter than IEEE.

### Other Conventions

- Panel labels: `(a)`, `(b)`, `(c)`.
- Captions below the figure.
- ACM CCS classification and ACM Reference Format are required at submission but unrelated to figures.
- ACM's `eXpress`-equivalent submission portal validates PDFs (font embedding, fonttype, transparency).

### LaTeX Inclusion Pattern

```latex
% sigconf single column
\begin{figure}[t]
  \centering
  \includegraphics[width=\columnwidth]{figures/throughput.pdf}
  \caption{...}
  \label{fig:throughput}
\end{figure}

% sigconf double column
\begin{figure*}[t]
  \centering
  \includegraphics[width=\textwidth]{figures/timeline.pdf}
  \caption{...}
\end{figure*}
```

## USENIX (Annual, OSDI, NSDI, Security, ATC, FAST, etc.)

### Dimensions

- Two-column layout in the camera-ready (`usenix2019_v3` style).
- `\columnwidth` = 3.33 in.
- `\textwidth` = 7.0 in for `figure*`.

### Format and Resolution

- PDF preferred. EPS accepted.
- 300 DPI for raster; 600 DPI for line art.
- Embed fonts.

### Typography

- Sans-serif figures, similar to ACM sigconf.
- 7 pt axis labels, 6 pt tick labels at final size.

### Other Conventions

- USENIX is more permissive about figure conventions than IEEE / ACM. Reasonable choices generally pass.
- Color is free in the digital proceedings.
- Caption below.

### USENIX-specific Tips

- USENIX accepts arXiv-prior submissions; many camera-ready figures end up reused for the arXiv preprint with no changes.
- `usenix2019_v3` does not provide a `figure*` shortcut — use the LaTeX two-column-floating-figure pattern.

## NeurIPS / ICML / ICLR (ML Conferences)

### Dimensions

- One-column layout. Text width:
  - NeurIPS: 5.5 in (14.0 cm).
  - ICML: 6.75 in (17.1 cm).
  - ICLR: 5.5 in.
- "Full-width" and "single-column" mean the same thing for these venues.

### Format and Resolution

- PDF, vector. Reviewers and ACs read on screen; rasterization shows immediately.
- Embed fonts.

### Typography

- Sans-serif in figures (Arial / Helvetica). Body font is varied — NeurIPS uses Times via the venue style.
- Minimum 8 pt axis labels at final size; 7 pt tick labels.

### Other Conventions

- Panel labels: usually `(a)`, `(b)`, `(c)`. Some venues use `A`, `B`, `C` — check recent accepted papers.
- Page limits are tight (8 + unlimited references for NeurIPS; 8 + appendix for ICML / ICLR). Figures count toward the page budget.
- Use the appendix for additional figures rather than cramming the main text.
- Author response / rebuttal periods sometimes allow figure additions; design the original figures to leave space for follow-ups.

### LaTeX Inclusion Pattern

```latex
\begin{figure}[t]
  \centering
  \includegraphics[width=\linewidth]{figures/training_curves.pdf}
  \caption{Validation accuracy vs. training step over 5 seeds.}
  \label{fig:training}
\end{figure}
```

`\linewidth` and `\textwidth` are equivalent in single-column layouts.

## arXiv Preprints

### Dimensions

- Match the target venue. arXiv itself imposes no width requirement.
- For "venue-agnostic" preprints, default to NeurIPS-width 5.5 in or USENIX two-column 7.0 in textwidth, whichever matches the manuscript class.

### Format and Resolution

- PDF. arXiv compiles your `.tex` source to PDF; figures should already be PDFs.
- arXiv strips most font and color profile info during compile. Test by uploading to a personal arXiv submission preview before public posting.

### Other Conventions

- arXiv's PDF compile sometimes rasterizes embedded EPS. Use PDF figures.
- arXiv accepts color figures freely; no print-vs-digital distinction.

## Figure Width vs. `\includegraphics` Scaling

Always produce the figure at the size it will be rendered. Common pattern that breaks:

```python
fig = plt.figure(figsize=(7, 5))  # produced at 7 in wide
```

```latex
\includegraphics[width=\columnwidth]{foo.pdf}  % LaTeX shrinks to 3.5 in wide
```

After scaling, all the text sizes are halved. Solution: pick `figsize` to match the final size, or render at the size you'll use:

```python
fig = plt.figure(figsize=(3.5, 2.5))   % IEEE single column, no LaTeX scaling
```

```latex
\includegraphics{foo.pdf}              % no width specified — uses native size
```

Or use `width=\columnwidth` with a matched-size figure:

```latex
\includegraphics[width=\columnwidth]{foo.pdf}  % no scaling because figsize matches
```

## Per-venue Style Files

The plugin ships matplotlib style files matching each venue:

- `assets/ieee.mplstyle` — IEEE single-column 3.5 in, 8 pt body.
- `assets/acm.mplstyle` — ACM sigconf 3.33 in, 7 pt body.
- `assets/neurips.mplstyle` — NeurIPS / ICML / ICLR 5.5 in textwidth, 9 pt body.
- `assets/publication.mplstyle` — generic CS baseline.
- `assets/presentation.mplstyle` — slides and posters (larger).

Apply with the absolute path:

```python
import os, matplotlib.pyplot as plt
PLUGIN = os.environ['CLAUDE_PLUGIN_ROOT']
plt.style.use(f'{PLUGIN}/skills/scientific-visualization/assets/ieee.mplstyle')
```

Or use the helper in `scripts/style_presets.py`:

```python
from style_presets import configure_for_venue
configure_for_venue('ieee', figure_width='single')
```

## Validating Compliance

Run `check_figure_size()` from `scripts/figure_export.py` to confirm dimensions:

```python
from figure_export import check_figure_size
fig, ax = plt.subplots(figsize=(3.5, 2.5))
check_figure_size(fig, venue='ieee')  # warns if width is wrong
```

Or check fonts are embedded after save:

```bash
pdffonts foo.pdf
# emb column should say "yes" for every entry
```

For Type 3 detection (the common eXpress / paperplaza failure):

```bash
pdffonts foo.pdf | grep -i 'type 3'
# any output is a problem
```

Fix by setting `pdf.fonttype: 42` in your script and regenerating.

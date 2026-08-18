---
name: pdf-visual-check
description: "Pre-submission visual lint for a compiled PDF: detects text overflowing the page margins, overlapping text or figure blocks, low-resolution embedded images, inconsistent body fonts, and blank pages. Use when the user asks to check the compiled PDF's layout, hunt overfull or margin-overflow problems, verify figure resolution before submission, or says 检查排版 / PDF 溢出 / 图片分辨率够不够 / 提交前过一遍 PDF. Detect-only: it reports page-anchored issues and never edits the source."
license: MIT license
allowed-tools: Read Bash Glob
metadata:
    skill-author: superpower-writing (script ported from an NTU classmate's paper-audit skill)
---

# PDF Visual Check: layout lint for the compiled artifact

LaTeX warnings catch overfull hboxes at compile time, but plenty of visual defects survive a clean compile: a wide table drawn past the margin by TikZ or `resizebox`, a figure caption colliding with a float, a 72-DPI screenshot that prints blurry, a stray blank page from a bad `\clearpage`. This skill checks the *rendered PDF*, so it sees what the reviewer sees.

## Run it

```bash
uv run --with pymupdf python "${CLAUDE_PLUGIN_ROOT}/skills/pdf-visual-check/scripts/visual_check.py" paper.pdf
```

Plain `python3` works too when `pymupdf` is already installed in the environment.

Options:

- `--margin <pt>`: expected page margin in points. Default 72 (1 inch, right for most single-column preprints). Two-column conference templates use tighter margins; IEEE and ACM sit near 54, so pass `--margin 54` there or every column edge reads as an overflow.
- `--min-dpi <n>`: minimum effective DPI for embedded raster images, computed from pixel size versus rendered size. Default 150; use 300 for camera-ready.
- `--json`: machine-readable output.

Exit code is 1 when any Critical issue (block overlap) is found, else 0.

## What each finding means

| Severity | Check | Typical cause |
|---|---|---|
| Critical | Block overlap (> 100 sq pt) | Floats colliding, absolute-positioned TikZ overlaying text, negative vspace |
| Major | Margin overflow | Overwide table or equation, `resizebox` gone wrong, long URL in bibliography |
| Major | Low-resolution image | Raster screenshot scaled up; regenerate as vector or export at higher DPI |
| Minor | More than 2 body fonts | A figure or package silently switching the text font |
| Minor | Blank page | Stray `\clearpage` / `\cleardoublepage` |

## Reading the report

Findings are page-anchored (`Page N`), so map each back to the source: `grep` the manuscript for the table or figure on that page, fix the source, recompile, re-run. Two rounds normally reach zero.

False positives to expect and wave through:

- Headers, footers, and page numbers legitimately live inside the margin band; so do full-bleed figures. Judge overflow findings against intent.
- Font-count findings fire on math-heavy papers where math fonts leak into the 9-13 pt body range.
- The overlap check compares block bounding boxes, so a tight wrap-figure layout can flag without a real collision. Open the page and look before editing anything.

This skill never edits the source. Fixes route to the manuscript by hand or through the drafting/polish skills.

## Dependencies

Needs `pymupdf`. The `uv run --with pymupdf` form above fetches it on demand; otherwise `pip install pymupdf`. The script fails with a clear ImportError message when it is missing.

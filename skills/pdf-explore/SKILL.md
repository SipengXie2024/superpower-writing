---
name: pdf-explore
description: "Read a long PDF (a paper under review, a cited reference) when the answer draws on more than one place in it and embedding the whole file is too big or one-shot. Ships a local no-LLM script for outline, per-page text, and keyword or regex search, plus a subagent fan-out recipe for whole-document extraction. Use when summarizing or comparing sections, locating where a topic is discussed, or listing every dataset, baseline, or citation across a paper including appendices."
license: MIT license
allowed-tools: Read Write Bash Grep
metadata:
    skill-author: superpower-writing (ported from AcademicForge pdf-explore, retargeted to Claude Code)
---

# PDF Explore: navigate a PDF too big to embed

A 50-page PDF read whole is ~200K tokens, and pages opened as images with `Read(pages="…")` drop out of context after one turn, so multi-section work loops on re-reading them. And when the answer is "every page" (list all the datasets / baselines / citations mentioned anywhere), reading page by page is the expensive way to get it. This skill parses the PDF once with a local, no-LLM script, so you load only what matters, or sweep every page via a subagent fan-out without ever putting the pages in your own context.

## Which tool for which read

| need | use | returns |
|---|---|---|
| a single 1–4 page lookup you'll quote in your *next* reply | `Read(file_path=…, pages="21-24")` (no script) | pages as images, dropped from context after one turn |
| a structured doc, see its sections first | `pdf_nav.py outline paper.pdf` | outline tree (page + level) |
| several pages/sections *at once* for a summary or comparison | `pdf_nav.py text paper.pdf 5,21-25,62` then write to a file then `Read` that file | persistent text, stays in context like any tool output |
| locate a keyword or pattern | `pdf_nav.py search paper.pdf "pattern" [--regex]` | `[{page, line, snippet}]` |
| exhaustive list of X across the whole doc | pull full text, then subagent fan-out (recipe below) | deduped list |
| a value or label off a *figure* | `Read(file_path=…, pages="5")` (page as image) | high-res page image |

The script lives at `scripts/pdf_nav.py`; run it with `python3`. It needs `pypdf` (see Dependencies).

## Recipe: pull the sections you need as persistent text

Don't loop `Read(pages=…)` one range at a time, because those images drop after a turn and you re-read them. Pull every page you need in one call, to a file, then Read the file:

```bash
python3 scripts/pdf_nav.py text paper.pdf 5,21-25,62-64 > sections.txt
```

Then `Read(file_path="sections.txt")` and write the answer from that. Roughly 800 tokens/page as text versus ~4,000 as an image, and you pay it once. Get the page numbers from the outline first.

## Recipe: navigate by outline (try this first)

```bash
python3 scripts/pdf_nav.py outline report.pdf
```

Free and instant when the PDF has embedded bookmarks (most LaTeX-compiled papers do). For a semantic question the outline doesn't obviously answer ("where do they discuss limitations"), fall through to `search`, or read the section most likely to hold it and skim.

## Recipe: exhaustive extraction across the whole doc

For "list every dataset / baseline / citation in this paper," extract the full text locally, then hand blocks to subagents in parallel, without putting the whole paper in your own context:

1. `python3 scripts/pdf_nav.py text paper.pdf > /tmp/paper_all.txt` (full text, once, free).
2. Split by page or section and dispatch `Agent` (general-purpose / Explore) subagents, each reading one block and returning the items under an explicit inclusion rule ("datasets this block *reports results on*, not ones merely cited"). Per-block extraction is recall-complete but precision-noisy, so put the inclusion rule in the prompt and each block applies it for you.
3. The main agent merges and dedupes the returned lists.

For ≲300 raw items, one subagent reading the whole extracted text and printing a deduped list is enough; fan out only when the doc is larger. The point of the split is recall completeness (every page gets read) without spending the tokens in the main context. The upstream platform version did this with a per-page fan-out of a cheap model; in Claude Code, subagents are the equivalent.

## Recipe: read a figure in detail

A whole-page render is too low-resolution for small axis labels or values. Open the page as an image with `Read(file_path="paper.pdf", pages="5")` and read one panel at a time. This is the one path that uses vision instead of the text script.

## When NOT to use this skill

- **A single 1–4 page lookup you'll quote immediately.** `Read(file_path=…, pages="…")` is fine, as long as you write your answer on the next turn, before the images drop.
- **Literal keyword search only.** `pdf_nav.py search`, or extract the text once and `grep` it. `search` earns its keep locating a term fast, not answering a semantic question.

## Dependencies

```bash
pip install pypdf   # or, in a uv-managed environment: uv pip install pypdf
```

Pure Python, no system libraries. Text extraction is good enough to navigate by and to read prose off, though it is not layout-faithful. For higher-fidelity text you can swap in `pypdfium2`; for values off a figure use the Read tool's PDF-image path, not this script.

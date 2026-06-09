---
section: benchmark-variant
stem: benchmark_README
framework: Five-Pillar
---

# Benchmark / Dataset Paper: Section-Standard Variant

This file documents the **benchmark/dataset-paper variant** of the section standards. A benchmark paper does not win by proposing a new algorithm. It wins by defining a new evaluation dimension and shipping a construction pipeline that makes the measurement high-quality, scalable, and reproducible. Its section skeleton differs from the default technique-paper IMRAD layout, so it uses its own standards files alongside the shared ones.

This is a routing and overview document, not a section standard the drafter reads verbatim. The drafter reads the per-section `benchmark_*.md` files below. Outlining selects the benchmark variant when the paper is a benchmark/dataset paper rather than a technique paper (the paper-type switch is wired by the outlining skill; see Followups in the integration notes).

## When the benchmark variant applies

Use it when the paper's primary contribution is a benchmark, dataset, or evaluation framework, not a new method. Signals: the title names a benchmark; the core artifact is data plus an evaluation protocol; the experiments reveal where model capability boundaries sit rather than proving one method beats baselines. Typical venues: NeurIPS Datasets and Benchmarks Track, ICML, ICLR, SIGMOD, VLDB.

For technique papers (a new method or mechanism solving an existing problem), use the default standards: `01_introduction.md` (CARS), `03_methods.md` (OFCA), `04_results.md` (RSRT), and the rest. Do not mix the two skeletons in one paper.

## The five-pillar scaffold

A benchmark paper is checked against five pillars. Each pillar maps to a section or a part of one:

1. **Research Gap.** Which dimension of evaluation does existing work miss? Ground the gap in a concrete failure case and position it against at most three prior benchmarks whose blind spots the paper addresses. Lives in §Introduction (benchmark framing) and the gap statement that opens the Task section.
2. **Construction Pipeline.** How is high-quality, scalable, reproducible data built? This is the paper's technical core, equivalent to §Methods in a technique paper. Standard: `benchmark_construction.md`.
3. **Evaluation Framework.** Beyond a single overall score: task scope, design goals, difficulty tiers, error taxonomy, per-dimension rubrics. Standard: `benchmark_evaluation_framework.md`.
4. **Empirical Findings.** Multi-angle analysis condensed into bolded "Finding X:" sentences that read like lemmas and are actionable for future work. Standard: `benchmark_findings.md`.
5. **Companion Method (optional).** A specialized model tuned for the benchmark, signalling the community can act on the findings. Not mandatory. When present it gets a short §Companion Method; document it as a note rather than a separate standards file (it reuses `03_methods.md` OFCA conventions in compressed form).

## The problem definition IS the contribution

In a technique paper the problem is a one-sentence goal and the method is the contribution. In a benchmark paper this inverts: the problem definition, the task scope, and the evaluation framework ARE the contribution. The construction pipeline is the technical core that makes the definition measurable. Treat the gap statement and the design goals with the same rigor a technique paper gives its method. A benchmark whose evaluation dimension is vague is a benchmark with no contribution, regardless of how much data it ships.

## Benchmark paper section layout and slug resolution

The benchmark variant authors these manuscript stems. Resolution follows the **same slug-ending rule** as the rest of the directory (see the main `README.md` §Match rule): the orchestrator takes the manuscript file's stem, tries an exact `<NN>_<slug>.md` match, then scans `section-standards/` for any file whose name ends in `_<slug>.md`. The `benchmark_` prefix is part of the filename, so the file's slug-ending is the part after `benchmark_`. For example, `benchmark_construction.md` ends in `_construction` and matches a manuscript stem `NN_construction.tex`.

| Benchmark section | Manuscript stem (example) | Resolves to | Pillar |
|-------------------|---------------------------|-------------|--------|
| Introduction | `01_introduction.tex` | `01_introduction.md` (shared CARS file, benchmark framing) | Research Gap |
| Task + Design Goals + Evaluation Framework | `02_evaluation_framework.tex` | `benchmark_evaluation_framework.md` (slug-ending `_evaluation_framework`) | Evaluation Framework |
| Construction Pipeline | `03_construction.tex` | `benchmark_construction.md` (slug-ending `_construction`) | Construction Pipeline |
| Companion Method (optional) | `04_methods.tex` | `03_methods.md` (shared OFCA, compressed) | Companion Method |
| Experiments / Empirical Findings | `05_findings.tex` | `benchmark_findings.md` (slug-ending `_findings`) | Empirical Findings |
| Discussion | `06_discussion.tex` | `05_discussion.md` (shared ILFS) | (research opportunities) |
| Related Work | `07_related_work.tex` | `07_related_work.md` (shared, with comparison table) | Research Gap |
| Conclusion | `08_conclusion.tex` | `06_conclusion.md` (shared RSF) | n/a |

Worked resolution examples:

- `manuscript/03_construction.tex` → step 1 looks for `03_construction.md` (miss), step 2 scans for a file ending in `_construction.md` and finds `benchmark_construction.md` → use it.
- `manuscript/02_evaluation_framework.tex` → step 1 miss, step 2 finds `benchmark_evaluation_framework.md` → use it.
- `manuscript/05_findings.tex` → step 1 miss, step 2 finds `benchmark_findings.md` → use it.

The numeric prefix is a sort-order aid only; a benchmark paper that places §Companion Method before §Construction still resolves each section by slug-ending. None of the benchmark slugs (`construction`, `evaluation_framework`, `findings`) collide with the shared slugs (`abstract`, `introduction`, `background`, `methods`, `results`, `discussion`, `conclusion`, `related_work`, `motivation`), so the slug-ending scan returns exactly one match for each.

## Introduction framing for benchmark papers (note on the shared CARS file)

A benchmark paper still uses `01_introduction.md` (CARS), but the M2 niche and M3 occupy carry benchmark-specific content:

- **M1 Territory** establishes the task, why it matters, and a running example threaded through the paper (the same example reappears in §Construction and §Findings, per the consistency invariant in `01_introduction.md`).
- **M2 Niche** states the evaluation gap and the limitations of at most three existing benchmarks, each traceable to a specific blind spot.
- **M3 Occupy** announces the benchmark, the construction approach in one sentence, and the contributions. The contributions list is typically four items: the benchmark itself, the construction-pipeline innovation, the systematic evaluation, and the headline findings (or the companion method). The "problem definition IS the contribution" principle means contribution 1 is the benchmark and its evaluation dimension, stated as a noun phrase, not a method.

The novelty-positioning and consistency rules in `01_introduction.md` apply unchanged: do not stage the benchmark as a naive-dataset-then-our-improvement delta, and avoid "to the best of our knowledge, the first benchmark for X" (unverifiable; position against the three named prior benchmarks instead).

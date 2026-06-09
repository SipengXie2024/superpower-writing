# Figure Rhetoric: Which Figures a Paper Needs and How to Judge Them

> **When to load**: tikz-figures step ① (画图指令), before you choose a layout. Also load at delivery time as a sanity check.
> **What this is**: design-judgment guidance, not a TikZ syntax guide. The 18-item mechanical checklist lives in `visual-review-checklist.md`; this file decides *which* figure to draw and *whether it earns its place*.
> **Scope**: CS / systems / ML papers for NeurIPS, ICML, ICLR, OSDI, NSDI, SOSP, EuroSys, USENIX ATC/Security, and similar. Retarget any non-CS habit to these venues.

This file ports the figure-storytelling model and Figure-1 paradigms from two upstream skills and adapts them to our LaTeX / systems / ML house style. It is advisory. It never blocks a figure; it surfaces judgment calls so you and the user decide.

---

## 1. The three-figure storytelling model

A strong top-venue paper usually carries six to eight figures, but three carry almost all the narrative weight. Reviewers scan these three in under a minute and decide whether the paper is worth a careful read. Weak versions sink otherwise-strong work.

| Figure | Where it sits | Job | Maps to our outline |
|--------|---------------|-----|---------------------|
| **Motivated example (Figure 1)** | Page 1 or top of page 2, right after the Introduction's gap/limitation sentence | Show the problem and why current methods fail, in under 30 seconds | Introduction `[N]` niche / §Motivation `[F]` failure |
| **Solution overview** | Inside §Methods / §Design, early | Show the architecture or mechanism as one readable picture | §Methods `[O]` overview |
| **Results figure(s)** | Inside §Evaluation / §Experiments | Show the headline gain with honest axes and error bars | §Results `[R]` per-RQ result |

Most other figures are supporting. If a proposed figure is not one of these three and does not directly back a tagged claim, ask whether it belongs in the paper at all. A figure that supports no claim is chart-junk at document scale.

**Budget**: spend one to two working days on Figure 1. That is not excessive. It pays back across the whole review cycle, because reviewers form their first impression there.

**Tool routing inside our plugin** (the three figures map to three skills):

- Motivated example and solution overview are structural diagrams. Default to `tikz-figures` (vector, formula-native, font-matched). Use `scientific-schematics` when the direction is unclear (exploration mode) or the figure is pictorial.
- Results figures are data-driven. Use `scientific-visualization` (matplotlib / pgfplots), never a hand-drawn diagram.

---

## 2. The three Figure-1 paradigms (and when to avoid each)

Figure 1 is the most consequential figure. Pick the paradigm that fits the contribution, and be able to say why the other two fit less well. State the chosen paradigm in your step ① design comment.

### Paradigm A: Running example plus failure case (recommended default)

The most persuasive option. Show a real, specific scenario, then show what goes wrong under the current method.

- **Layout**: two or three panels. Panel 1 is the real input (a query, a trace, a workload, a model input). Panel 2 is what a current method produces, with the error highlighted in red. Panel 3 (optional) is what your method produces, highlighted in green.
- **Use when**: the problem is concrete and the failure is easy to show side by side. Fits query optimization, compiler passes, scheduling, agent workflows, code generation, retrieval, anything with a visible input-output pair.
- **CS example**: a query planner. Show a SQL query, then the baseline plan that picks a hash join and spills to disk under a skewed key, then your plan that picks the index-nested-loop and stays in memory. Annotate the spill in red.
- **Avoid when**: there is no single concrete input that exposes the problem (e.g., the contribution is a system-wide throughput property with no per-input failure).

### Paradigm B: Existing vs ours

Two side-by-side columns. Left shows how the existing method works and why it fails. Right shows how your method works and why it succeeds.

- **Layout**: two vertical columns. Each has a schematic of the method's internal structure, an annotated failure or success indicator, and a one-line in-panel caption naming the method.
- **Use when**: the contribution is a structural change to a mechanism (a new dataflow, a new operator graph, a new memory layout) rather than a failure on one specific input.
- **CS example**: a consensus protocol. Left: leader-based replication with the extra round trip circled. Right: your leaderless path with the saved round trip circled.
- **Avoid when**: the two designs look nearly identical at the schematic level, so the side-by-side reads as "spot the difference" rather than a clear contrast.

### Paradigm C: Performance teaser

A compact result chart placed in the Introduction as a preview of the headline gain.

- **Layout**: a small grouped bar, scatter, or speedup chart showing your method clearly dominating baselines, paired with one sentence of text explaining what the reader sees.
- **Use when**: the performance gain is the headline contribution and is large enough to speak for itself, benchmark results already exist, and the paper is short and needs an immediate hook.
- **Avoid when** (the load-bearing rule): **the gains are marginal**. A teaser then shows the weakness unkindly. A reviewer reads "2% better" as "barely better" before reading a single claim. Also avoid when the paper's value is qualitative (robustness, expressiveness, a new capability) and does not reduce to one metric. In both cases choose Paradigm A or B and let the result figures in §Evaluation carry the numbers.

**Default for systems / ML**: Paradigm A unless the contribution is clearly mechanism-level (then B) or the win is large and numeric and the paper is short (then C). When in doubt, A.

---

## 3. Design-judgment rituals

These are habits, not mechanical checks. Apply them before drawing and before delivering. They catch the failures that the syntax linter and overlap checker cannot see.

### The 30-second comprehension test

Show the figure to someone unfamiliar with the paper. If they cannot describe the problem (for Figure 1) or the result (for a results figure) in 30 seconds, the figure is not doing its job. Inside this plugin the proxy is the user: surface the figure and ask "what do you take from this in 30 seconds?" rather than asking "is it done?". If their answer does not match the claim the figure is meant to support, the figure needs work, not the caption.

### Real entities only, no `Entity1` / `X` placeholders

Name real queries, real datasets, real modules, real outputs. Placeholder names like `Module A`, `Entity1`, `X`, `Component 2` quietly tell the reviewer the authors did not have a concrete instance in mind, which undermines credibility. Use `BERT-base`, `RocksDB`, `the 4 KB random-write workload`, `the GROUP BY clause`, the actual names from the paper. This applies to every figure, but it matters most in Figure 1 where credibility is set.

### Appears once, referenced throughout

The example introduced in Figure 1 should reappear in §Methods as a walkthrough and in §Evaluation as a case study. One running example threaded through the paper reads as a coherent argument. A fresh example per section reads as three disconnected demos and forces the reviewer to re-load context each time. Concretely: if Figure 1 uses the skewed-key query, the methods section should trace that same query through the new planner, and the evaluation should report that same query's latency.

### Draft on paper first

Sketch the figure by hand or on a whiteboard and show the sketch to a collaborator before opening any tool. Iterate the sketch, not the rendered output. A layout mistake is one eraser stroke on paper and twenty minutes of TikZ coordinate surgery on screen. Inside this plugin the ASCII or narrative design comment required at tikz-figures step ① is the on-disk form of this ritual: the comment block *is* the paper sketch, written before any `\draw`. Do not skip it to "save time"; skipping it has a 100% rework rate (see SKILL.md step ①).

### Honest framing

A figure must not oversell. Truncated y-axes that exaggerate a gain, a teaser chosen to hide a marginal win, and a cherry-picked input that is not representative are all integrity failures, not style choices. Never fabricate the data, the trend, or the example. If the honest figure is unimpressive, that is information about the contribution, not a prompt to redraw more flatteringly. This mirrors the plugin's NEVER-FABRICATE rule for claims and citations.

---

## 4. Quick self-questions before you draw

Run these in step ①. If any answer is "no" or "I'm not sure", resolve it with the user before coding the figure.

- Is this figure one of the three storytelling figures, or does it back a specific tagged claim? If neither, why is it in the paper?
- For Figure 1, which paradigm (A / B / C) and why not the other two? Are the gains large enough for a teaser, or would C show weakness?
- Are all labels real entity names from the paper, with zero placeholders?
- For Figure 1, is this the same running example that the Introduction sets up and that §Methods and §Evaluation will reuse?
- Would an unfamiliar reader get the message in 30 seconds?
- Is the framing honest, with real data, untruncated axes unless flagged, and a representative example?

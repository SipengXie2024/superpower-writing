---
section: related_work
stem: 07_related_work
framework: ThematicGroup
---

# Related Work — Thematic-Group Standard

The §Related Work section positions this paper against the prior literature. It MUST be organized as **thematic groups** — prior work clustered by research direction, not by chronology — with each group concluding in an explicit comparison to this paper. This is the convention across CS, ML, systems, database, security, and most engineering venues.

**Placement is flexible.** §Related Work may sit early (as §2 immediately after Introduction, common in SIGCOMM / NSDI / CCS / SIGMOD / IEEE Transactions) or late (between §Discussion and §Conclusion, common in NeurIPS / ICML / CVPR / ICLR / ACL). Both placements use the same structural template; only the position differs. The choice is usually dictated by venue — check recent papers from the same venue to confirm the local convention. This file governs `.writing/manuscript/NN_related_work.tex` regardless of its numeric prefix (slug-ending match).

**Distinction from §Background.** §Background is pedagogical (teach the reader concepts needed to understand §Methods); §Related Work is argumentative (position this paper against prior approaches). The two sections may cite overlapping papers but for different purposes — §Background describes *what the baseline does*, §Related Work describes *why this paper differs from the baseline*. Do not collapse them unless the venue's page budget forces consolidation; when consolidated, the combined section uses §Background's DNPL structure, not this file's thematic-group structure.

## Framework

**Thematic-group structure.** Organize cited papers into 2–4 themes, each a research direction the paper touches. Each theme is one paragraph (occasionally two for large themes). Every theme paragraph MUST conclude with an explicit comparison to this paper — a sentence that starts with "Unlike …", "In contrast, …", "Whereas prior work …, we …", or equivalent. Reviewers read these comparison sentences first; if yours are missing or weak, the section fails regardless of how thorough the citations are.

Why thematic over chronological: chronological reviews ("Smith 2015 did X. Then Chen 2017 did Y. Zhang 2019 did Z.") read as bibliography recitals and lose the argumentative thread. Thematic grouping forces the writer to articulate *what the group has in common* and *what this paper does differently from the group as a whole* — the two beats reviewers actually care about.

## Role of each element

| Element                          | Purpose                                                                                              | Answers                                                           |
|----------------------------------|------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------|
| **G — Thematic group (paragraph)** | Cluster 2–5 prior papers sharing a research direction. Describe the common approach in one or two sentences, then contrast this paper against the group. | *What did this line of work do, and how is our contribution distinct?* |
| *(Optional)* **S — Summary table** | One row per top-3 baseline comparing dimensions (Approach / Assumption / Limitation) against this paper. | *Where does our contribution land along multiple axes simultaneously?* |

The summary table is optional but improves legibility when the paper compares against 3–5 concrete baselines with numeric differences. It is standard in ML benchmark papers and increasingly common in systems papers.

## Outline bullet requirement

`.writing/outline.md` §Related Work MUST contain **2–4 bullets total**, one per thematic group. Each bullet MUST be prefixed with `[G]`:

```
## Related Work

- [G] <theme 1: one-sentence description of the research direction + how we differ>
- [G] <theme 2: ...>
- [G] <theme 3: ...>
```

Rules:

- Minimum 2 `[G]` bullets (a §Related Work with a single theme is either too narrow — add a second theme — or structurally redundant with §Background's P element).
- Maximum 4 `[G]` bullets (more than 4 themes usually means the section is trying to cover the whole field; cut to the most contrast-worthy 3–4).
- Each `[G]` bullet MUST mention the differentiator from this paper in the bullet text (e.g., "[G] Sparse attention variants (Longformer, BigBird, Performer): local-window or kernel-based; unlike these, we preserve full quadratic attention with sublinear memory"). Bullets that only name the theme without stating differentiation fail the outline check.

Each `[G]` bullet seeds a claim stub in `.writing/claims/section_<NN>_related_work.md` using `rw-c1`, `rw-c2`, … Each claim's EVIDENCE list includes the citations for the papers the theme groups (usually 2–5 DOIs per theme).

## Draft requirement

The matching `.writing/manuscript/<NN>_related_work.tex` MUST be structured as **one paragraph per thematic group** (optionally two for oversized themes), plus an optional summary table at the end. Each paragraph MUST be preceded by a LaTeX line comment marking its group, and §Related Work stem does not end in an unprotected slug, so every paragraph also needs a `% claim: id` tag:

```latex
\section{Related Work}
\label{sec:related}

% related_work: G
% claim: rw-c1
<paragraph 1: Theme 1 --- 4--7 sentences. First sentences: describe the
shared approach across the group, citing 2--5 representative papers via
\cite{smith2019,chen2020,zhang2021}. Final sentence: ``Unlike these, we...''
or ``In contrast to this line of work, our approach...''.>

% related_work: G
% claim: rw-c2
<paragraph 2: Theme 2 --- same pattern: group description $\to$ contrast
sentence.>

% related_work: G
% claim: rw-c3
<paragraph 3: Theme 3 --- same pattern.>
```

Rules:

- Put `% related_work: G` on the line immediately above `% claim: id`. Both tags are required.
- **Every `[G]` paragraph MUST end with a contrast sentence.** This is enforced by Step C self-review: grep each paragraph for one of `Unlike `, `In contrast`, `Whereas `, `Our approach differs`, or `Our work differs`. A paragraph that matches none of these fails the structural check and blocks the section from being marked `drafted`.
- **Citations ≥ 2 per theme.** A theme with only one cited paper is not a theme; it is one paper. Either find the rest of the cluster or absorb the lone paper into a neighboring theme.
- **No ad-hominem citations.** Do not single out a single prior paper for detailed critique unless it is a direct baseline in §Results. General dismissals of a named paper read badly; if a paper is weak, cite it and move on.
- **Length budget:** ~400–1,000 words total, scaling with venue page budget. A dense 4-page ML workshop paper may compress Related Work to 200 words (2 themes, 2 sentences each); a 14-page systems paper may expand to 1,500 words (4 themes with a summary table).
- **Optional summary table.** When included, place it after the last `[G]` paragraph with its own claim tag (`% related_work: G` / `% claim: rw-cN`). Columns should be 3–5 comparison dimensions plus a final column for "This paper". Rows should be 3–5 top baselines. Use the `tabular` environment with `booktabs` rules (`\toprule`, `\midrule`, `\bottomrule`).

## Style rules

- **Tense:** simple past for prior work ("Smith et al. proposed..."); simple present for the line of work's characteristics ("These methods rely on..."); simple present for this paper's positioning ("Our approach avoids this by...").
- **Voice:** active voice. Prefer "Smith et al. proposed X" over "X was proposed in [1]".
- **Citation density:** §Related Work is the citation-densest section of the paper. Each `[G]` paragraph typically cites 3–6 papers. Use `\cite{citekey}` (standard LaTeX); group as `\cite{a,b,c}` when citing a cluster.
- **Positioning language.** "Unlike", "In contrast", "Whereas", "Our work differs by", "Orthogonal to" are standard. Avoid dismissive language ("fails to", "ignores", "overlooks") — these read as combative and do not persuade. Instead describe the difference neutrally.
- **Group names must be noun phrases**, not sentences. "Sparse attention variants" beats "Methods that use sparse attention to reduce complexity". Concision is a signal of thoughtful organization.

## Common failure modes

- **Bibliography recital.** One paragraph per paper, chronological, no grouping. Symptom: reviewer writes "§Related Work lacks organization" or "comparison to this paper unclear". Fix: rewrite as thematic groups; each paragraph covers 2–5 papers sharing a direction.
- **Missing contrast sentence.** Each `[G]` paragraph describes prior work without stating how this paper differs. Symptom: reviewer writes "novelty unclear" or "positioning unclear". Fix: append a sentence starting with "Unlike" / "In contrast" / "Whereas" to every `[G]` paragraph; the self-review grep enforces this.
- **Theme inflation.** Four or five themes with one paper each, stretched to make the section look comprehensive. Symptom: each paragraph is too short; reviewers sense padding. Fix: merge thin themes into parent themes or cut papers.
- **Dismissive tone.** "Prior work fails to recognize...", "Existing methods ignore...". Symptom: reviewer senses hostility; fairness scores drop. Fix: rewrite neutrally — "Prior work does not address X; we extend to cover it" rather than "Prior work overlooks X".
- **Duplicates §Background.** Related Work cites the same papers as §Background using the same framing. Symptom: two sections read as copies. Fix: keep §Background focused on "what the baseline does" and §Related Work focused on "how we differ from each cluster"; the citations may overlap but the framing should not.
- **Missing baselines.** §Experiments compares against Paper X; §Related Work does not mention Paper X. Symptom: reviewers flag "Paper X is a key baseline but not positioned against in §Related Work". Fix: audit every baseline in §Experiments against §Related Work's `[G]` bullets — every compared baseline MUST be cited in the appropriate theme.
- **Placement confusion.** Paper submits to NeurIPS with §Related Work as §2 when venue norm is late placement (or vice versa). Symptom: reviewers flag structural oddity. Fix: pick placement based on venue norm, not personal preference; confirm by checking 3–5 recent accepted papers from the same venue.

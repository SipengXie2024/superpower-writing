---
name: novelty-gap-check
description: Adjudicates research novelty and produces an advisory go/no-go verdict before drafting starts. Decomposes the idea into core technical claims, runs per-claim prior-work search via existing retrieval skills, then emits a per-claim delta table, an overall PROCEED / PROCEED-WITH-CAUTION / ABANDON call, and suggested positioning. Use when a user asks "is this novel", "查新", "has anyone done this", or wants a novelty gate before committing scope.
---

# Novelty Gap Check

## Overview

This skill adjudicates how novel a research idea is against recent literature, then hands the user an advisory go/no-go. It does three things in order. First it decomposes the idea into three to five core technical claims. Then it searches prior work per claim using the retrieval skills this plugin already ships. Finally it emits a delta verdict: a per-claim HIGH/MED/LOW novelty table, an overall PROCEED / PROCEED-WITH-CAUTION / ABANDON call, and suggested positioning.

This is the **verdict and positioning layer**, not a retrieval engine. Retrieval is delegated. The skill invokes `superpower-writing:research-lookup` for fast per-claim queries and `superpower-writing:literature-review` for a deeper sweep when the idea spans several subfields. Do not reimplement search backends here. The value this skill adds is the judgment on top: closest prior work per claim, the delta, and how to frame the contribution.

**Core principle:** be brutally honest. A false novelty claim wastes months of research time. Surfacing a strong prior-work overlap early is the most valuable thing this skill does.

**Advisory only.** The verdict is surfaced to the user. It never auto-rejects an idea, never mutates `.writing/` state, and never flips claim STATUS. The user decides whether to proceed, pivot, or abandon.

**Never fabricate.** Every paper named as prior work must be verified before it enters the report. Unverified candidates are tagged `[UNVERIFIED]` and surfaced, never dropped and never invented. This mirrors the plugin's claim-first rule. Full protocol in [`references/citation-discipline.md`](references/citation-discipline.md).

## Relation to other skills

| Skill | Direction | Contract |
|-------|-----------|----------|
| `superpower-writing:research-lookup` | this skill calls it | fast per-claim prior-work queries; returns papers + abstracts saved under `sources/` |
| `superpower-writing:literature-review` | this skill calls it | deeper multi-subfield sweep when one search pass is not enough |
| `idea-evaluator` (planned sibling) | consumes this skill's verdict | the novelty verdict is the kill-gate input for its fatal-flaw check F1 ("no novelty versus closest prior work") |
| `superpower-writing:brainstorming` | runs before this skill | shapes the idea; novelty-gap-check assumes a stated idea exists |
| `superpower-writing:outlining` | runs after a PROCEED | turns the idea into an IMRAD outline once novelty clears |

The sibling `idea-evaluator` scores an idea on many axes (feasibility, scope, lifecycle fit). Novelty is one of those axes. This skill owns the novelty axis in depth and feeds its verdict in. When `idea-evaluator` is not installed, this skill still stands alone as a novelty gate.

## When to Use

Trigger this skill when:

- The user asks whether an idea is novel ("is this novel", "查新", "has anyone done this", "check novelty").
- The user wants a go/no-go before committing to a paper scope or starting implementation.
- The user is comparing two or three candidate ideas and wants a novelty ranking.
- A reviewer-style prior-work risk check is wanted before drafting.

Do NOT use this skill for:

- Brainstorming new ideas from scratch (use `superpower-writing:brainstorming`).
- Verifying citations already in a manuscript (use `superpower-writing:claim-verification`).
- A broad literature survey with no novelty question attached (use `superpower-writing:literature-review` directly).
- Evaluating a finished manuscript (out of scope for this plugin).

## Process

Run the four phases in order. Phase B is the only slow phase.

### Phase A: Decompose the idea into core claims

Read the user's idea description. Extract three to five core technical claims that would each have to be novel for the idea to count as novel. For each claim, answer four questions:

- What is the method or mechanism?
- What problem does it solve?
- How does it work, in one sentence?
- What makes it different from the obvious baseline?

Write each claim as a single assertion with a truth value, not a topic. "We apply contrastive pretraining to graph kernels" is a claim. "Graph learning" is not. Keep claims atomic. One claim should not bundle a method and a finding together. Split those.

If the idea is too vague to yield testable claims, stop and ask the user to restate it. A vague idea produces a fake novelty check that hides missing thinking.

### Phase B: Per-claim prior-work search

For EACH core claim, search prior work. Reuse the plugin's retrieval skills. Do not write new search code.

1. **Default per-claim search.** Invoke `superpower-writing:research-lookup` with the claim phrased as a search query. That skill routes academic queries to scholarly backends and saves raw results under `sources/`. Use at least **three different query formulations** per claim. Vary the wording: the method name, the problem framing, and the closest-baseline framing. One phrasing misses papers that a synonym would catch.

2. **Recency floor.** Always cover the **most recent six months** of arXiv. Fast-moving subfields turn over in weeks. Pass a date filter to research-lookup for the recent window, then run an undated query for older seminal work. A claim that looks novel against 2024 papers can be dead against a March-2026 preprint.

3. **Deeper sweep when needed.** When the idea spans several subfields, or when per-claim search surfaces conflicting signals, invoke `superpower-writing:literature-review` for a structured multi-database pass. Use it once, not per claim. It returns a thematic synthesis this skill reads to place each claim.

4. **Read the candidates.** For each paper that looks like it overlaps a claim, read its abstract and, when reachable, its related-work section. Overlap is judged on substance, not title similarity.

5. **Verify before recording.** Every candidate paper must clear the pre-search verification gate before it enters the report. Resolve its arXiv ID or DOI against the source. If it cannot be resolved, tag it `[UNVERIFIED]` and keep it visible. Never invent an arXiv ID, a DOI, a venue, or a year. See [`references/citation-discipline.md`](references/citation-discipline.md).

Record per-claim findings as you go: the claim, the closest one or two papers, and a one-line overlap note. This feeds Phase C.

### Phase C: Cross-model delta verdict

Score the delta between each claim and its closest prior work, then aggregate to an overall call.

1. **Per-claim delta.** For each claim assign HIGH, MED, or LOW novelty against the closest prior work found. Apply the delta rubric and the non-obvious novelty rules in [`references/novelty-rubric.md`](references/novelty-rubric.md). Two rules carry most of the weight:
   - Applying X to Y is NOT novel unless the application reveals a surprising insight. Naming a new pairing is not a contribution by itself.
   - If the method is not novel but the FINDING would be, say so explicitly. A known method that produces an unexpected, well-evidenced result is a finding contribution, not a method contribution. Label which one the idea is.

2. **Optional cross-model second opinion.** For a contentious or high-stakes idea, get an independent read before locking the verdict. Hand the dossier (the claims, the candidate papers, the per-claim deltas) to a second model via `superpower-writing:collaborating-with-codex`. Ask it the three questions: is this novel, what is the closest prior work, and what is the delta. The dossier protocol and the briefing template are in [`references/cross-model-protocol.md`](references/cross-model-protocol.md). This step is optional. Skip it for a clearly-novel or clearly-dominated idea where one model already settles the question.

3. **Aggregate to an overall verdict.** Map per-claim deltas to one of three calls using the aggregation rule in the rubric:
   - **PROCEED** when at least one core claim is HIGH and none is a fatal LOW that the idea depends on.
   - **PROCEED-WITH-CAUTION** when the strongest claim is MED, or a HIGH claim sits next to a load-bearing LOW that needs repositioning.
   - **ABANDON** when every core claim is LOW against recent prior work, meaning a published baseline already dominates the idea.

### Phase D: Emit the novelty report

Surface the verdict to the user as a structured report. The output format is fixed. Full template and a worked CS example are in [`references/output-template.md`](references/output-template.md). The required sections are:

```markdown
## Novelty Gap Check (<ISO-8601 timestamp>)

### Proposed idea
<1-2 sentence restatement>

### Core claims and per-claim delta
| # | Claim | Novelty | Closest prior work | Delta |
|---|-------|---------|--------------------|-------|
| 1 | ... | HIGH/MED/LOW | <paper or [UNVERIFIED] / none found> | <one line> |

### Closest prior work
| Paper | Year | Venue | Overlap | Key difference |
|-------|------|-------|---------|----------------|

### Overall verdict
- Verdict: PROCEED / PROCEED-WITH-CAUTION / ABANDON
- Method vs finding: <is the contribution the method, the finding, or both>
- Key differentiator: <what makes this unique, if anything>
- Reviewer risk: <what a reviewer would cite as prior work>

### Suggested positioning
<how to frame the contribution to maximize defensible novelty>
```

**Optional persistence.** When a `.writing/` directory exists for this project, the user may want the report saved as `.writing/novelty-report.md` for the record, alongside `verify-report.md`. Ask first. Writing the file is advisory persistence, not a state mutation: it adds no claim STATUS and changes no existing `.writing/` file. Do not create `.writing/` just to hold this report. When no project state exists, deliver the report inline in the conversation.

## Key Principles

**Decompose before you search.** A novelty check on a whole idea is mush. A novelty check on three to five atomic claims is auditable. The per-claim table is the artifact a user and a reviewer can both reason about.

**Brutal honesty over comfort.** The skill's job is to catch a dominating prior work before months are spent, not to validate the user's hope. A confident ABANDON that saves a wasted quarter is a success, not a failure.

**Method novelty and finding novelty are different claims.** Reviewers reject "we applied a known method to a new dataset" framed as a method paper. The same work framed as "we found an unexpected result that overturns assumption Z" can land. Always state which kind of contribution the idea is, and position it accordingly.

**Recency is non-negotiable.** The six-month arXiv window is a hard floor, not a nicety. The most common novelty-check failure is missing a recent preprint that already did the thing.

**Advisory, never autonomous.** This skill reports. It does not gate execution, reject ideas, or write claim STATUS. The user owns the decision. The verdict feeds the sibling `idea-evaluator` and the user's own judgment, not an automatic kill switch.

**Never fabricate, mark instead.** A fabricated prior-work citation is worse than an honest gap. When a paper cannot be verified, tag it `[UNVERIFIED]` and keep it in view. When no overlap is found for a claim, say "none found", not silence. Provenance is the whole point.

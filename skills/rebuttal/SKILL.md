---
name: rebuttal
description: Builds a grounded, venue-compliant response to reviewers for a CS/systems/ML paper. Atomizes every reviewer comment into an issue board with a fixed action vocabulary, enforces three finalize-blocking gates (provenance, commitment, coverage), drafts in strict R-A-C format with page cross-references, and wires every claimed change to a real manuscript location. Use when the user says "rebuttal", "reply to reviewers", "respond to reviews", "OpenReview response", or "ICML/NeurIPS rebuttal".
---

# Rebuttal: Response to Reviewers

## Overview

Turns reviewer comments into an auditable, fabrication-free response package for a CS / systems / ML paper. The pipeline atomizes every comment into an ISSUE_BOARD, maps each to a fixed action label, drafts replies in strict R-A-C form, and runs three hard gates before anything finalizes. It reads the existing manuscript and verification report so every claimed change points at a real location.

This skill does NOT run experiments, edit the manuscript prose, generate new theorem claims, or submit to OpenReview / CMT / HotCRP. It drafts the response text only. New results, derivations, or approved commitments enter as user-confirmed evidence; the skill never invents them.

**Core principle:** Evidence before claims, always. Every factual sentence in the response must trace to a source. A sentence with no source is blocked, not softened.

**Iron law:** No `STATUS: final` flip on the response without all three gates passing in `.writing/reviews/REBUTTAL_STATE.md`.

**Relation to the claim-first hook.** During drafting, a PreToolUse hook (see `superpower-writing:main` Claim-First Protocol) blocks prose writes that lack a backed claim. The rebuttal Provenance gate is the same discipline pointed at the response letter. Where the hook asks "does this manuscript paragraph have a backed claim?", the gate asks "does this response sentence have a source?". Same answer when neither has one: blocked.

**AUTHOR_INPUT_NEEDED is the [NEEDS-EVIDENCE] of rebuttals.** In drafting, `[NEEDS-EVIDENCE]` marks a claim whose support is not yet on disk. In a rebuttal, `AUTHOR_INPUT_NEEDED` marks a response whose facts the author has not yet supplied. Both are visible placeholders that block finalization, never silent gaps. Both surface to the user; neither is fabricated away.

**Verdicts are advisory.** The gates surface blockers to the user. They never auto-reject a comment, auto-mutate state, or paste a response anywhere. The user decides what to send.

## When to Use

- User pastes reviewer comments and asks for a response, rebuttal, or reply.
- User says "respond to reviews", "OpenReview response", "ICML/NeurIPS/ICLR rebuttal", "answer reviewer 2".
- A prior rebuttal exists and a follow-up reviewer comment arrives.
- User wants to triage what reviewers want before deciding how to respond.

Do NOT use this skill for:

- Writing or editing the manuscript itself (use `drafting` or `polish`).
- A true appeal that challenges a rejection rather than revising. Route it OUT as a separate task (see `references/difficult-cases.md`).
- Generating a cover letter. That is adjacent revision-package material, handled separately.

## State and Layout

Rebuttal artifacts live under `.writing/reviews/` (the `reviews/` subdir is created by `init-writing-dir.sh`). The skill reads but never modifies the manuscript or scripts.

| Path | Role |
|------|------|
| `.writing/manuscript/*.tex` | Source of truth for every page / section cross-reference. Read-only here. |
| `.writing/verify-report.md` | Per-claim PASS/FAIL from `claim-verification`. Read-only; tells you which claims are already verified and citable. |
| `.writing/reviews/REVIEWS_RAW.md` | Reviewer comments preserved verbatim. |
| `.writing/reviews/ISSUE_BOARD.md` | Atomized comments with id / severity / stance / action. |
| `.writing/reviews/RESPONSE_DRAFT.md` | The R-A-C response letter. |
| `.writing/reviews/REVISION_PLAN.md` | One checklist line per promised manuscript edit. |
| `.writing/reviews/REBUTTAL_STATE.md` | Phase + gate status. Resume point on rerun. |

Run `bash ${CLAUDE_PLUGIN_ROOT}/scripts/check-writing-state.sh` first. If it prints `missing`, there is no paper to ground against; ask the user to point at the manuscript or run outlining/drafting. Do not modify `check-writing-state.sh` or any script.

## Checklist (each must pass before the response is final)

- [ ] `.writing/` exists; manuscript files located for cross-referencing.
- [ ] Every reviewer comment preserved verbatim in `REVIEWS_RAW.md`.
- [ ] Every comment atomized into `ISSUE_BOARD.md` with id, severity, stance, action.
- [ ] Every action label drawn from the fixed vocabulary (see below). No freeform labels.
- [ ] Draft written in R-A-C form; every change cites a real `manuscript/*.tex` location.
- [ ] Provenance gate passes: every factual sentence has a source.
- [ ] Commitment gate passes: every promise maps to a commitment state and a `REVISION_PLAN.md` line.
- [ ] Coverage gate passes: every comment ends answered, deferred, or needs-input. Nothing disappears.
- [ ] Venue limit checked (character/word count) if the venue imposes one.
- [ ] User confirmed before any `STATUS: final` flip.

## Fixed Action Vocabulary

Every comment maps to exactly one of these eight labels. This set merges the r2 response modes with the r5 action labels into one fixed vocabulary. Do not invent new labels; if a comment seems to need one, it usually decomposes into two comments.

| Label | Meaning | Use when |
|-------|---------|----------|
| `ACCEPT_TEXT` | A wording, structure, or presentation change addresses the concern | The author supplied or can supply a concrete text edit, citable to a section |
| `ACCEPT_EXPERIMENT` | A new or revised experiment / analysis addresses the concern | The author ran a real experiment and supplied result, metric, and table/figure location |
| `SOFTEN_CLAIM` | The claim strength is reduced or a boundary is added | The original claim was too broad, too causal, or overstated relative to evidence |
| `PARTIAL` | Partly addressed, with an explicit remaining limitation | A valid concern cannot be fully resolved in this revision |
| `DISAGREE` | Respectful disagreement on evidence or scope grounds | The reviewer's reading is not supported by manuscript facts. Never bare "we disagree" |
| `OUT_OF_SCOPE` | Valid suggestion, but outside this paper's scope | The request needs a new system, dataset, or study design (see difficult-cases) |
| `AUTHOR_INPUT_NEEDED` | Cannot draft final wording without real facts | The author note is vague, missing, or unsupported. The rebuttal analog of `[NEEDS-EVIDENCE]` |
| `BLOCKING` | The response is not credible until the author acts | Missing required artifact, central evidence gap, or integrity/ethics question |

`AUTHOR_INPUT_NEEDED` and `BLOCKING` both block finalization. The difference: `AUTHOR_INPUT_NEEDED` is a missing detail you can draft around with a visible placeholder; `BLOCKING` is a gap that makes any confident response misleading until resolved.

## Workflow

### Phase 0: Resume or initialize

1. Run `check-writing-state.sh`. Confirm `.writing/` and the manuscript exist.
2. If `.writing/reviews/REBUTTAL_STATE.md` exists, resume from its recorded phase.
3. Otherwise create the `.writing/reviews/` artifacts listed above and proceed.
4. Confirm the venue and its limit. If text-only vs revised-PDF, per-reviewer-thread vs single-document, or the character limit is unclear, stop and ask before drafting.

### Phase 1: Preserve reviews verbatim

1. Write every reviewer comment, editor instruction, and meta-review into `.writing/reviews/REVIEWS_RAW.md` unchanged. Do not paraphrase; paraphrase loses the reviewer's exact ask.
2. Record venue, round, and reviewer IDs in `REBUTTAL_STATE.md`.
3. Preserve editor instructions under ids `E1`, `E2`; reviewer comments under `R1-C1`, `R2-C3`, and so on.

### Phase 2: Atomize into the ISSUE_BOARD

Create `.writing/reviews/ISSUE_BOARD.md`. Split every comment into atomic concerns. One concern is one thing the reviewer wants. A comment that bundles "the baseline is weak and the writing in Section 4 is unclear" becomes two rows.

Each row carries:

```yaml
- id: R2-C1
  reviewer: Reviewer 2
  round: 1
  anchor: "the comparison omits the obvious FlashAttention baseline"   # short verbatim quote
  type: baseline_comparison   # see comment types below
  severity: major             # minor | major | blocking
  stance: negative            # positive | swing | negative | unknown
  priority: pivotal           # standard | pivotal
  action: ACCEPT_EXPERIMENT   # fixed vocabulary above
  manuscript_location: "Section 5.2; Table 3"   # where the answer lands, or TBD
  status: open                # open | answered | deferred | needs_user_input
```

Comment **types** for CS / systems / ML papers: `assumptions`, `theorem_rigor`, `novelty`, `empirical_support`, `baseline_comparison`, `complexity`, `reproducibility`, `clarity`, `scope`, `other`. Pick the closest; the type guides which action label is natural.

**Stance** matters for budget. A `pivotal` reviewer is one whose vote or confidence would most move the decision, with addressable rather than ideological concerns. Spend more drafting care there. Answer positive reviewers too; a short reinforcement of their support is cheap and useful.

If `QUICK_MODE` is requested ("just tell me what they want"), stop here. Present the board grouped by reviewer with shared vs unique concerns and recommended priorities, then let the user decide whether to draft.

### Phase 3: Map each action to evidence

For every row, decide the action label and its evidence basis. The basis is what makes the response true:

- `paper`: a sentence or result already in the manuscript. Cite the section.
- `verified_claim`: a claim marked PASS in `.writing/verify-report.md`. Safe to cite as established.
- `user_confirmed_result`: a new experiment result the user supplied. Record what they said verbatim.
- `user_confirmed_derivation`: a derivation the user supplied.
- `future_work`: explicitly deferred. Lands in the revision plan as a camera-ready note, not a promise of new data now.

Rules for assigning the basis:

- If the author says only "we revised it", the label is `AUTHOR_INPUT_NEEDED` until the location and nature of the edit are known.
- If the author says "we added an experiment", request the experiment name, condition, sample size or replicate unit, result summary, and table/figure location before drafting `ACCEPT_EXPERIMENT`.
- If a central claim has no support, the label is `SOFTEN_CLAIM` or `BLOCKING`, never confident compliance language.
- If the manuscript already answers the concern, point at the section. Prefer claims already PASS in `verify-report.md`; those are pre-vetted.

When the basis is missing, mark the row `AUTHOR_INPUT_NEEDED` and move on. Do not fill the gap with an invented number, citation, or result.

### Phase 4: Draft in R-A-C form

Write `.writing/reviews/RESPONSE_DRAFT.md`. Every response follows Reviewer comment then Author response then Changes made, the R-A-C structure. Quote the reviewer verbatim and cross-reference the manuscript by section or page.

```markdown
## Response to Reviewer 2

### R2-C1
> the comparison omits the obvious FlashAttention baseline

**Author response.** We agree this baseline strengthens the comparison. We added
FlashAttention-2 under the same compute-matched protocol as the other baselines.
The new result appears in Table 3, and our method retains a 1.4x throughput edge
at the 8k context length.

**Changes made.** Added FlashAttention-2 row to Table 3 (Section 5.2) and one
sentence of analysis in the paragraph above it.
```

Default reply shape per concern, three to four sentences:

1. Direct answer in the first sentence. State the position before the justification.
2. Grounded evidence in the next one to two sentences. One numerical anchor that maps to this reviewer's specific ask. Cut metrics other reviewers care about; bloat dilutes the answer.
3. The manuscript implication in the last sentence. Where the change lands.

Heuristics that survive meta-review:

- Evidence over assertion. A derivation or a number beats an adjective.
- Name the closest prior work and the exact delta for novelty disputes.
- Concede narrowly when the reviewer is right, then state what still holds (see `structural_distinction` in `references/tone-and-stance.md`).
- For theory critiques, separate core assumptions from technical ones.
- If no strong evidence exists, say less, not more.

**Disagreement is a contrast, not a reflex.** A good `DISAGREE` acknowledges the concern, states the narrow point of disagreement, gives manuscript or scope evidence, and offers a small clarification. A bad one asserts and stops.

```markdown
GOOD
> Reviewer: use Method X instead of Method Y.

**Author response.** We appreciate the suggestion. We chose Method Y because its
assumptions hold on our streaming workload, whereas Method X assumes a static
graph (Section 3.1). To test sensitivity, we added a Method X robustness check in
Appendix B; results are consistent with the main finding.

**Changes made.** Added Appendix B (Method X robustness check) and a one-line
justification in Section 3.1.

BAD
> Reviewer: use Method X instead of Method Y.

**Author response.** We disagree. Method Y is appropriate.
```

The bad version evades. It states no reason, cites no location, and gives the reviewer nothing to evaluate. The good version disagrees on a stated technical ground and still adds a check, so the reviewer can see the position is reasoned rather than defensive.

Hard rules while drafting:

- NEVER invent experiments, numbers, derivations, citations, DOIs, arXiv IDs, or links. Mark `[UNVERIFIED]` and route to `AUTHOR_INPUT_NEEDED` instead.
- NEVER promise a change the user has not approved.
- NEVER let "thanks" be the whole response. Each reply needs an answer, an action, a location, or a flag.

Alongside the draft, write `.writing/reviews/REVISION_PLAN.md`: one atomic checklist line per promised manuscript edit, each tagged with its issue id and its commitment state.

```markdown
- [ ] (R2-C1) Add FlashAttention-2 row to Table 3 [commitment: already_done] [status: verify wording]
- [ ] (R1-C3) Add complexity proof to Appendix A [commitment: approved_for_rebuttal] [owner: author]
- [ ] (R3-C2) Larger-scale run [commitment: future_work_only] [status: camera-ready note]
```

### Phase 5: Run the three gates

These are the finalize blockers. Run all three. If any fails, surface the failures to the user and do not flip `STATUS: final`. Record the result in `REBUTTAL_STATE.md`.

**Gate 1: Provenance.** Walk every factual sentence in `RESPONSE_DRAFT.md`. Each must map to one basis: `paper`, `verified_claim`, `user_confirmed_result`, `user_confirmed_derivation`, or `future_work`. A sentence with no source is BLOCKED. This is the rebuttal analog of the claim-first hook: no source, no sentence. Surface each unsourced sentence as a blocker with its line.

**Gate 2: Commitment.** Walk every promise in the draft. Each must map to one state: `already_done`, `approved_for_rebuttal`, or `future_work_only`. A promise the user did not approve is BLOCKED. Then cross-check: every paper-edit promise in the draft appears as a `REVISION_PLAN.md` line, and every plan line maps back to a draft promise. Orphans on either side are a violation.

**Gate 3: Coverage.** Walk every `ISSUE_BOARD.md` row. Each must end in `answered`, `deferred` (intentionally, with a one-line reason), or `needs_user_input`. No comment may silently disappear. A reviewer concern with no row and no disposition is the failure this gate exists to catch.

The gates are advisory in the plugin sense: they report blockers and stop the finalize flip, but they never delete a comment, rewrite a sentence, or send anything. The user resolves blockers and reruns.

### Phase 6: Tone and limit pass

1. Apply `references/tone-and-stance.md`: calibrate claim verbs to the evidence tier, strip forbidden phrases, check that no reply is bare thanks.
2. If the venue imposes a character or word limit, count it exactly. Compress in this order when over: redundancy, then replies to friendly reviewers, then the opener, then wording. Never drop a critical answer to fit.
3. Optional adversarial scan: for each experimental claim, ask whether a hostile reviewer could find an undisclosed design choice (compute-matched vs epoch-matched, frozen parameter subset, seed protocol). If so, add a one-line caveat. Pre-registered-calibration phrasing defuses cherry-pick attacks, but only when true (see tone-and-stance).

### Phase 7: Finalize

1. Present to the user: the gate results, the venue character count vs limit, and any line still tagged `AUTHOR_INPUT_NEEDED` or `[UNVERIFIED]`.
2. Get explicit user confirmation before flipping `STATUS: final` in `REBUTTAL_STATE.md`. This mirrors the claim-verification confirmation gate: no green-lit state change lands silently. If the user opened the run with a standing "draft and finalize" instruction, that is the confirmation; do not re-prompt.
3. Refresh `REVISION_PLAN.md` so its checklist matches the final draft.
4. Update `.writing/progress.md` with a one-line rebuttal row if the project tracks one.

### Phase 8: Follow-up rounds

When a new reviewer comment arrives after the first response:

1. Append it verbatim to `REVIEWS_RAW.md` under a new round.
2. Link it to an existing `ISSUE_BOARD.md` row or open a new one.
3. Draft a delta reply only, not a full rewrite.
4. Update `REVISION_PLAN.md` in place: add new lines, tick completed ones.
5. Rerun the three gates on the delta.
6. Escalate technically, not rhetorically. Concede if the reviewer is now right. Stop arguing if the reviewer is immovable and no new evidence exists; answer once and move on.

## Key Principles

**Provenance is the claim-first hook for rebuttals.** The manuscript hook blocks an untagged paragraph at write time. The Provenance gate blocks an unsourced response sentence at finalize time. The discipline is identical: a factual statement earns its place by pointing at a source. Treat a blocked sentence as a signal to find the source or soften the claim, not an obstacle to route around.

**AUTHOR_INPUT_NEEDED mirrors [NEEDS-EVIDENCE].** Both are visible, on-disk placeholders for a gap the author must fill. Both block finalization. Neither is ever fabricated away. When you do not have the fact, mark it and surface it; do not invent a plausible-looking number.

**Coverage means nothing disappears.** Every reviewer comment is tracked from raw text to a disposition. A reviewer who sees their concern ignored downgrades the paper. The Coverage gate is the structural guarantee that each comment reaches answered, deferred, or needs-input.

**Concede narrowly, never surrender the claim.** When the reviewer is partly right, accept the local point explicitly, then state what remains true and why it still supports the contribution. Pair every concession with the preserved theorem, mechanism, result, or scope condition. The `structural_distinction` move in tone-and-stance is the canonical form.

**Never fabricate.** No invented experiments, numbers, derivations, citations, DOIs, arXiv IDs, or links. A reviewer who catches one fabricated number distrusts the whole response. When evidence is missing, say less; mark `[UNVERIFIED]` and route to author input.

**Verdicts are advisory.** The gates surface blockers and stop the finalize flip. They never auto-reject a comment, mutate manuscript state, or paste the response anywhere. The user owns the decision to send.

**Route appeals out.** An appeal challenges a rejection; it is not a revision response. When the user wants to contest a decision rather than revise, identify the disputed points and hand the appeal off as a separate task with venue-specific rules (see `references/difficult-cases.md`).

## References

- `references/difficult-cases.md`: named strategies for the impossible or out-of-scope experiment, the reviewer factual error, conflicting reviewers, and routing a true appeal out.
- `references/tone-and-stance.md`: the evidence-tiered verb ladder, the forbidden-phrase blocklist, the `structural_distinction` move, and pre-registered-calibration phrasing.

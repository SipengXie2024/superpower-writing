---
name: idea-evaluator
description: Evaluates ONE research idea against a top-venue bar (NeurIPS, ICML, ICLR, OSDI, NSDI, SOSP) and returns an advisory Strong-Accept, Accept-with-Revisions, or Reject-and-Pivot verdict. Runs a fatal-flaws audit first and short-circuits on any CRITICAL flaw, then scores five idea-framing dimensions plus a FINER gate. Use when the user asks to evaluate, score, or sanity-check an idea before committing to a paper scope.
---

# Idea Evaluator

## Overview

This skill evaluates one preliminary research idea the way a top-venue reviewer would. It returns one of three advisory verdicts: Strong Accept, Accept with Revisions, or Reject and Pivot. The target bar is a top systems or ML venue such as NeurIPS, ICML, ICLR, OSDI, NSDI, or SOSP. Novelty and significance are the two axes that decide acceptance there.

The point is to kill a doomed idea cheaply, before the author spends weeks drafting. A weak idea caught at evaluation costs an afternoon. The same idea caught at submission costs the whole project.

**Control-flow core: fatal-flaw short-circuit.** Run the fatal-flaws audit FIRST. If any flaw is CRITICAL, stop and emit the rejection directly. Do not score a doomed idea. Scoring is decoration on a rejection that is already certain.

**Core principle: never fabricate.** Do not invent prior work, DOIs, arXiv IDs, benchmark numbers, or SOTA results to justify a verdict. If a novelty claim or a baseline-recency claim rests on literature you have not checked, mark it `[UNVERIFIED]` and route the user to a literature check. A confident verdict built on a hallucinated baseline is worse than an honest "unverified".

**Verdicts are advisory.** This skill surfaces a recommendation. It never auto-rejects an idea, never edits `.writing/` state, and never blocks the user from proceeding. The user owns the decision. Present the verdict, the evidence, and the actions, then let the user choose.

## When to Use

- The user has one draft idea and asks whether it is worth pursuing.
- The user asks for a novelty check, a feasibility read, or "score this idea".
- The user is about to commit to a paper scope or start implementation.
- The user suspects scope creep and wants an outside check.
- The user says "evaluate this idea", "is this a good direction", or "would a reviewer buy this".

## When NOT to Use

- The idea is still a vague hunch with no stated contribution. Route to `superpower-writing:brainstorming` first. Evaluation needs a concrete idea to score.
- The user wants to generate new ideas from scratch. That is brainstorming, not evaluation.
- The user has already implemented the idea and is drafting. Route to `superpower-writing:outlining` or `superpower-writing:drafting`.
- The user wants a review of an existing manuscript or its citations. Use `superpower-writing:claim-verification`.

## Inputs and State

This skill reads, but does not write, `.writing/` state.

- If `.writing/findings.md` exists, read its Requirements and Research Findings sections. They may hold the stated contribution, the target venue, and prior-work notes the user already gathered.
- If no `.writing/` directory exists, that is fine. Take the idea from the user's message. Do not run `scripts/init-writing-dir.sh` and do not create `.writing/` here. Evaluation is a read-only, pre-commitment step.
- The verdict goes to the user as chat output. Do not persist it to `.writing/` and do not mutate any claim STATUS.

## Required Idea Inputs

Before scoring, confirm you have these four. If any is missing, ask the user once via `AskUserQuestion`. Do not guess.

1. The one-sentence contribution. What does the idea claim to do?
2. The target venue or venue class (NeurIPS, ICML, ICLR, OSDI, NSDI, SOSP, a workshop, or "undecided").
3. The closest prior work the user knows of, and what this idea adds over it.
4. The stated resources: compute, data access, and rough timeline.

If the user cannot state the one-sentence contribution, stop and route to brainstorming. An idea you cannot summarize in one sentence is not yet ready to evaluate.

## Process

Run the steps in order. The short-circuit in Step 2 can end the evaluation early.

### Step 1: First impression and contribution sentence

State, in one paragraph, whether the idea reads as a Novel Problem, a Novel Method, or a New Setting. Then force the contribution into one sentence using this template:

```
We show that <approach A> improves <baseline B> on <axis C>,
measured by <metric M>, which changes how the field does <task Q>.
```

Each blank that cannot be filled routes to a specific remedy. Do not paper over an empty blank.

| Empty blank | What it means | Remedy |
|---|---|---|
| A (approach) unclear | There is no method yet, only a wish | Send back to brainstorming; there is nothing to evaluate |
| B (baseline) unnamed | No reference point for the gain | Make the user name the current SOTA baseline before scoring |
| C (axis) vague | The idea improves "things" generally | Force a single dominant axis from Step 4's five dimensions |
| M (metric) absent | The win cannot be measured | Flag fatal flaw F6 (unverifiable claim) in Step 2 |
| Q (task / who-cares) missing | No external beneficiary | Flag fatal flaw F4 (no motivation) in Step 2 |

The contribution sentence is the spine of the whole evaluation. A sentence with two empty blanks usually predicts a Reject-and-Pivot before any scoring runs.

### Step 2: Fatal-flaws audit (early gate, short-circuit)

Read `references/fatal-flaws.md`. It holds the ten canonical fatal flaws, each with a question-style detection rule, a defense, and a time-based severity rule.

Run the audit BEFORE any scoring. Identify at most two fatal flaws. For each, name the flaw, apply its detection question, and propose a concrete defense. Then tag severity using the time rule:

- **CRITICAL**: the flaw cannot be defended within the project lifecycle, or two or more MAJOR flaws stack.
- **MAJOR**: the flaw needs two to four weeks of dedicated work to defend.
- **MINOR**: the flaw clears in under a week of writing or literature work.

**Short-circuit rule.** If any flaw is CRITICAL, STOP. Emit the rejection directly:

- Verdict: Reject and Pivot.
- Output only the First impression, the Fatal-flaws table with the CRITICAL flaw, and the Verdict with the flaw-driven rationale.
- Do NOT run the five-dimension scoring, the FINER gate, the feasibility check, or the integrity gate.

A CRITICAL flaw means the idea fails regardless of how well everything else scores. Scoring it anyway produces a polished rejection that wastes the user's reading time and risks implying the idea is salvageable when it is not. If no flaw is CRITICAL, continue to Step 3.

### Step 3: Five-dimension scoring

Read `references/five-dimensions.md`. It holds the five axes and the generative inversion that produced them. It also holds the anti-inflation scoring rule and tiered anchors keyed to real venue papers.

Score the idea 1 to 10 on each axis. The dimensions are:

- **Higher**: accuracy, quality, or effectiveness gains over the strongest baseline.
- **Faster**: lower wall-clock time, token cost, memory, or compute, at equal quality.
- **Stronger**: robustness under noise, out-of-distribution inputs, or domain shift.
- **Cheaper**: lower data, annotation, training, or deployment cost.
- **Broader**: cross-domain transplantation, or unification of fragmented tasks.

**Anti-inflation rule.** Default every score to 5 and justify each move upward with a specific sentence from the user's idea. Scoring everything 7 or 8 "to be generous" destroys the signal the verdict depends on. A score without a cited reason is not a score; mark it for re-read instead.

Each score must cite evidence from the stated contribution. Then name the two or three axes where the idea has the highest ceiling. Those become the paper's thesis and the focus of its introduction.

### Step 4: FINER gate

Score the idea on the FINER framework using the anchored matrix below. FINER catches problems the five dimensions miss: ethics, feasibility, and whether the question even implies a method.

| Criterion | Score 1 (weak) | Score 5 (strong) |
|---|---|---|
| **F**easible | Cannot be answered with available methods, data, or compute | Clearly answerable with identified methods and accessible resources |
| **I**nteresting | Trivial or already well established | Addresses a real puzzle, contradiction, or open question |
| **N**ovel | Duplicates existing work | Offers a new method, perspective, or evidence over the closest prior work |
| **E**thical | Raises real ethical or data-use concerns | No ethical issues; benefits clearly outweigh risks |
| **R**elevant | No practical or theoretical significance | Directly informs practice, deployment, or theory |

Minimum threshold: average FINER at or above 3.0, and no single criterion below 2.

**Must-imply-a-methodology gate.** The idea must imply a concrete method. If no experiment or construction comes to mind when you read it, the idea is too vague to evaluate. This gate is hard: an idea that fails it cannot reach Strong Accept regardless of its other scores. Route the user back to sharpen the question.

### Step 5: Feasibility check

Against the user's stated resources, assess each risk and propose a mitigation for any that is high:

- **Compute risk**: does the experiment fit the stated hardware?
- **Data risk**: is the data accessible, or does it need costly annotation or private access?
- **Engineering risk**: does the implementation match the user's skill stack?
- **Timeline risk**: does the end-to-end duration (code, experiments, writing, revision) fit the project lifecycle?

Feasibility claims must reference the user's stated resources, not generic assumptions.

### Step 6: Integrity gate

Before emitting the verdict, confirm each check. If any fails, downgrade the verdict and mark the relevant output section as "needs user attention".

1. Every dimension score cites a specific sentence from the stated contribution. No score is gut feeling.
2. Feasibility claims reference the user's stated resources, not generic ones.
3. Novelty claims either cite specific prior work or are labelled `[UNVERIFIED]; literature check required`. Never invent the prior work.
4. Each fatal flaw is specific and actionable. "This might not work" is not a flaw statement.
5. The verdict matches the scoring. Strong Accept requires at least two dimensions at 8 or above and zero CRITICAL flaws.
6. Any paradigm-shift claim names which probe question (see below) was answered yes.
7. The FINER must-imply-a-methodology gate passed, or the verdict is at most Accept with Revisions.

### Step 7: Final verdict

Issue one advisory verdict:

- **Strong Accept**: execute now. Two or more dimensions at 8 or above, no CRITICAL flaw, FINER above threshold, feasibility green.
- **Accept with Revisions**: reshape the scope first, per the listed actions. Some dimensions weak, only fixable (MAJOR or MINOR) flaws, or a feasibility risk that has a stated mitigation.
- **Reject and Pivot**: do not pursue this version. A CRITICAL flaw, all five dimensions at 4 or below, or more than two fatal flaws.

Present the verdict, the evidence behind it, and the top three actions. Then stop. Let the user decide; do not auto-proceed to any downstream skill.

## Paradigm-shift probe (one-paragraph intro-framing note)

A high-ceiling idea often challenges something the field takes for granted. Before settling the verdict, ask four quick questions of the idea. Does it challenge a hidden assumption everyone treats as fixed? Does it tackle an elephant-in-the-room problem the field sees but avoids? Does it ride a technology shift that just made an old approach feasible (for example, long-context models reviving an idea that was impractical before)? And if the problem solved itself, would the field change meaningfully? Two or more yes answers signal disruptive potential. That is not a separate score. It is a framing lever. Lead the introduction with the assumption being overturned. Reviewers reward an idea that reframes the problem over one that only nudges a number. Cite which question was answered yes when you make the claim; do not assert disruption without it.

## Output Format

Adapt to the short-circuit. On a CRITICAL flaw, emit sections 1, 2, and 7 only.

### 1. First impression
- Idea type: <Novel Problem | Novel Method | New Setting>
- Contribution sentence: <filled template, or the empty blanks named>

### 2. Fatal-flaws audit
| # | Flaw | Detection hit | Severity | Defense |
|---|---|---|---|---|
| 1 | ... | ... | CRITICAL / MAJOR / MINOR | ... |

*If any flaw is CRITICAL, skip sections 3 to 6 and go to section 7 with verdict Reject and Pivot.*

### 3. Five-dimension scores
| Dimension | Score 1-10 | Cited evidence | Lift suggestion |
|---|---|---|---|
| Higher | ... | ... | ... |
| Faster | ... | ... | ... |
| Stronger | ... | ... | ... |
| Cheaper | ... | ... | ... |
| Broader | ... | ... | ... |

Top axes (the thesis): <two or three dimensions>.

### 4. FINER gate
| Criterion | Score 1-5 | Justification |
|---|---|---|
| Feasible | ... | ... |
| Interesting | ... | ... |
| Novel | ... | ... |
| Ethical | ... | ... |
| Relevant | ... | ... |
| Average | ... | Methodology gate: pass / fail |

### 5. Feasibility
| Risk | Level | Mitigation |
|---|---|---|
| Compute | ... | ... |
| Data | ... | ... |
| Engineering | ... | ... |
| Timeline | ... | ... |

### 6. Integrity gate
- Checks 1 to 7: <pass / fail, with any failure named>

### 7. Verdict
**<Strong Accept | Accept with Revisions | Reject and Pivot>** (advisory)

Rationale: <one or two sentences tying the verdict to the scoring or the CRITICAL flaw>

Top three actions:
1. ...
2. ...
3. ...

## Key Principles

**Short-circuit before scoring.** The fatal-flaws audit runs first for a reason. A CRITICAL flaw is dispositive, so scoring around it is wasted motion that misleads the user about salvageability. Stop at the first CRITICAL flaw and reject.

**Default to 5, justify upward.** Score inflation is the most common failure of idea evaluation. A radar chart pinned at 7 across all five axes tells the user nothing. Anchor at 5 and earn every point with a cited sentence.

**Never fabricate to justify a verdict.** A novelty or recency claim that rests on unchecked literature gets the `[UNVERIFIED]` tag, not an invented citation. The honest gap is recoverable with a literature check; a hallucinated baseline poisons the whole evaluation.

**Advisory, not authoritative.** The verdict is a recommendation surfaced to the user. This skill never auto-rejects, never edits state, and never proceeds to a downstream skill on its own. The author decides what to do with the read.

**Novelty and significance decide the top venues.** At NeurIPS, ICML, OSDI, and their peers, a competent application of a known toolkit is rejected even when it is well executed. The bar is a new method, a new setting, or a result that changes how the field works. Score against that bar, not against "is this correct".

**One idea per evaluation.** This skill scores one idea against the bar. If the user has two or three candidates, evaluate each in its own pass and compare verdicts; do not blend them into a single score.

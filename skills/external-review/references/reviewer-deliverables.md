# Reviewer Deliverable Prompts

Copy these prompts verbatim into the Codex bridge follow-up rounds. Each is tuned to produce structured, gradeable output. Reuse the `SESSION_ID` from the initial review so the critic keeps the paper in context.

Retarget the venue token to the user's actual target: NeurIPS, ICML, ICLR for ML; OSDI, NSDI, SOSP, EuroSys, ATC, FAST for systems; CCS, S&P, USENIX Security, NDSS for security; SIGMOD, VLDB for databases; SIGCOMM for networking; SIGGRAPH for graphics; STOC, FOCS, SODA for theory. The structure is identical across venues; only the bar and the section conventions shift.

## 1. Mock venue review

Ask the critic to role-play a program-committee reviewer and produce a review in the venue's own format.

```
Write a mock <venue> review of the paper as if you were on the program committee.
Use exactly these sections:
- Summary: 3-5 sentences on what the paper does and claims.
- Strengths: 3-5 items, each citing a specific section, table, or result.
- Weaknesses: 3-5 items, each with the problem, why it matters, and a fix.
- Questions for Authors: 2-4 genuine questions whose answers could change the verdict.
- Score: a single recommendation on the venue's scale (e.g. strong reject /
  reject / borderline / accept / strong accept) with one sentence of rationale.
- Confidence: how confident you are in this assessment and why (e.g. expert in
  the area / educated guess / outside my expertise).
- What Would Move Toward Accept: the smallest set of changes that would flip a
  reject to a borderline, or a borderline to an accept.
Be brutally honest. Cite the paper's own passages; do not be vague.
```

### Mock-review rubric

The critic scores the work along these dimensions. Reproduce the rubric in the prompt only if the critic's first review is too shallow or skips dimensions. Weights are a CS-paper default; adjust for the venue.

| Dimension | Weight | What "strong" looks like |
|-----------|--------|--------------------------|
| Novelty | 20% | A new mechanism, abstraction, or result, not an incremental tweak of prior work |
| Soundness | 25% | Claims follow from the method; proofs or systems arguments hold; no unjustified leaps |
| Evaluation | 25% | Right baselines, right metrics, right ablations; results support the headline claims |
| Clarity | 15% | A committee member can follow the contribution and reproduce the setup from the text |
| Significance | 15% | The result matters to the subfield; others will build on it |

Decision mapping is a guide, not a gate. A single fatal dimension (an unsound proof, a missing baseline that invalidates the headline) can sink an otherwise strong paper regardless of the average.

| Weighted read | Typical recommendation |
|---------------|------------------------|
| Strong across all five | Accept / strong accept |
| Solid with fixable gaps | Borderline / weak accept |
| Real potential, substantial gaps | Major revision territory (resubmit) |
| A fatal flaw or thin contribution | Reject |

### Reviewer-bias guardrails

When the critique reads as reflexively negative or fixated on trivia, remind the critic of the bias guardrails so the review stays calibrated and constructive.

- Hypercriticism: do not inflate minor issues into headline weaknesses. Separate critical from major from minor.
- Confirmation bias: actively look for the paper's merits, not only evidence for a pre-formed verdict.
- Preference projection: judge whether the authors' method answers the question, not whether it is the method you would have picked.
- Novelty bias: a careful reproduction or a strong negative result is a real contribution.
- Length and prestige: judge content density and the work itself, never page count or author reputation.

### Mock-review report skeleton

When persisting the review to `.writing/reviews/`, store the critic's output under this skeleton so it reads without the conversation.

```markdown
# Mock <venue> Review (<ISO-8601 date>)

## Summary
<3-5 sentences>

## Strengths
- S1 <title>: <specifics, cited>
- S2 ...

## Weaknesses
- W1 <title>: Problem / Why it matters / Suggested fix / Severity (critical|major|minor)
- W2 ...

## Questions for Authors
1. <question>
2. ...

## Score
<recommendation>: <one-sentence rationale>

## Confidence
<level>: <why>

## What Would Move Toward Accept
<smallest change set>
```

## 2. Results-to-claims matrix

Ask the critic to map possible experimental outcomes to the claims each outcome would license. This stops the author from over-claiming before the results are in.

```
Give me a results-to-claims matrix. For experiments X and Y (described in the
brief), enumerate the plausible outcomes of each, and for every combination
state which claim the paper is allowed to make and which it must drop or soften.
Format as a table: rows are outcome combinations, columns are (outcome of X,
outcome of Y, strongest defensible claim, claims that become unsupportable).
Flag any claim in the current draft that no realistic outcome would support.
```

Expected shape of the returned matrix:

| Outcome of X | Outcome of Y | Strongest defensible claim | Now unsupportable |
|--------------|--------------|----------------------------|-------------------|
| X improves | Y improves | The full headline claim stands | none |
| X improves | Y flat | A scoped claim limited to the X regime | the general claim |
| X flat | Y improves | Reframe around Y as the contribution | the X-centered framing |
| X flat | Y flat | No publishable claim on this axis; pivot or add an experiment | both headline claims |

The value is the bottom-right cells. They tell the author which claims are one failed run away from collapsing, so the narrative does not bet on an outcome the experiment cannot deliver.

## 3. Minimal-experiment plan

Ask the critic for the single experiment that buys the most acceptance probability per unit of compute. This prioritizes a finite GPU budget against the weaknesses the review surfaced.

```
Design the minimal additional experiment that gives the highest acceptance lift
per GPU-week, given the weaknesses you identified. Our compute budget is
<state it: e.g. 8xA100 for 2 weeks>. Be specific: datasets, baselines, model
sizes, hyperparameters, ablation axes, and the metric that would settle the
open question. Rank candidate experiments by (expected acceptance lift) /
(GPU-weeks), and justify the top pick in one paragraph.
```

Expected shape of the returned plan:

- A ranked list of 2-4 candidate experiments, each with its GPU-week cost and the specific weakness it closes.
- The top pick spelled out at configuration level: datasets, baselines, model sizes, hyperparameters, ablation axes, and the deciding metric.
- One paragraph on why the top pick beats the runners-up on lift-per-compute.

Never let the critic invent numbers for results not yet run. The plan describes what to measure, not what the measurement will show. If the brief lacks the compute budget, ask the user for it before sending this prompt rather than letting the critic assume one.

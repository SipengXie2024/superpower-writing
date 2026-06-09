# Attack Briefs, Adjudication Briefs, and the Verdict Mapping

This file holds the long detail for `adversarial-review`: the two thread briefs, the six attack axes, the rejection-dimension checklist, and the count-to-verdict table the helper implements. SKILL.md summarizes; this file is the literal text to paste into the threads and the table to read the helper's output against.

All venue references target CS, systems, and ML venues: NeurIPS, ICML, ICLR, OSDI, NSDI, SOSP, EuroSys, MLSys, USENIX Security, VLDB. Adapt the named venue to the paper's actual target.

## Thread 1 brief: the attack memo

Paste this into a fresh thread, after filling the file list. Read only the current paper files.

```
You are simulating a hostile NeurIPS / ICML / ICLR / OSDI reviewer for a paper.
This is a kill-argument adversarial check. Your task is NOT a balanced review.
Your task is to construct the single strongest argument for rejecting this paper.

## Files to read
- LaTeX entry and all section files under .writing/manuscript/
- The .bib file
- The compiled PDF if one exists

Read the source carefully. Do not consult any prior reviews, fix lists, or
summaries. This is a fresh, zero-context adversarial pass.

## Your task
Write the single best argument to reject this paper in about 200 words. Write
the worst-case rejection memo a senior area chair would produce after reading
the paper.

Pick the most damaging combination of the axes below. Do not list all of them.

1. Theorem validity: are the central theorems actually proved as stated?
2. Assumption-versus-claim mismatch: does the body quietly retreat to a
   narrower object than the title and abstract advertise?
3. Missing proof obligation: is a load-bearing lemma invoked but not proved
   (concentration, generic position, a prefactor or envelope bound) that the
   headline depends on?
4. Limit-order or composition ambiguity: are limits in n, d, k, or epsilon
   composed in an order the paper never commits to? For a systems paper, is a
   scaling or asymptotic claim stated without the regime it holds in?
5. Claim-versus-evidence gap: is the empirical evidence too narrow to support
   the breadth of the stated theorem or take-away? One dataset, one workload,
   one hardware platform standing in for a general claim?
6. Scope overclaim: does the title or abstract sell a result substantially
   broader than what the body proves or measures?

## Constraints
- About 200 words. Do NOT exceed 250.
- One argument, not a list. Pick the most damaging line and develop it.
- Cite specific file:line locations or equation numbers when accusing.
- Tone: dispassionate but uncompromising. Do NOT hedge. Do NOT acknowledge
  mitigations the paper might have made elsewhere. This is the rejection
  paragraph. The defense gets the next thread.
- Do NOT reference prior review rounds, fix lists, or any context outside the
  current paper files.
- Do NOT invent line numbers, equation labels, or results. If you cannot point
  to a real location, do not make the accusation.

Output: just the rejection memo, nothing else.
```

## Thread 2 brief: the adjudication

Paste this into a second fresh thread, independent of Thread 1. Fill in the file list and the attack memo verbatim.

```
You are an independent area-chair adjudicator examining whether the current
paper text answers a hostile reviewer's rejection memo. You are NOT the paper's
defender. Read the attack point by point and rule, from the current source
alone, whether each point stands or falls. Fresh, zero-context adjudication.
Do not reference any prior reviews or fix lists.

## Paper files
[same paths as Thread 1]

## The hostile reviewer's rejection memo (the attack)
> [attack memo verbatim from Thread 1]

## Your task
The attack is one continuous argument, but it makes several distinct rejection
points. Decompose it into its atomic rejection points (3 to 7 of them). For
each point, assign exactly one ruling:

- answered_by_current_text: the current source already refutes this point.
  Cite specific file:line evidence.
- partially: the source has some response but not enough to refute the attack
  as written.
- unresolved: the source has no effective response.

The label answered_by_current_text is intentional. The word "fixed" implies a
history of patching and biases toward optimism. You read the paper cold, as a
reviewer would, with no knowledge of prior drafts.

For each point, output:
### P<n>: <short label>
- Attack claim: <the specific accusation, about 30 words>
- Ruling: answered_by_current_text | partially | unresolved
- Evidence: <cite file:line, about 50 words>
- Severity if unresolved or partial: critical | major | minor
- Needs new experiment: yes | no   (yes only when the gap is empirical or
  evidence-based and prose edits cannot close it)
- If unresolved, recommended fix: <one specific actionable sentence>

After the per-point analysis, output:

## Counts
answered_by_current_text: X
partially: Y
unresolved: Z

## Net assessment
<one paragraph: would this paper survive a senior area-chair read of the attack,
given only what is in the current source? Be honest. If Y or Z is positive and
they hit the headline, say so.>

## Constraints
- Do NOT consult any prior reviews or fix lists. Rule strictly from the current
  paper files.
- If the paper cannot refute a point, do NOT minimize. Keep severity honest.
- If a point reflects an author-chosen position (a deliberate title-scope
  decision, a deliberate omission), rule it partially with a note that the
  position is intentional, AND say whether the position is sustainable under
  the attack. Do NOT auto-grade it answered_by_current_text just because it is
  intentional.
- Be specific. No flattery, no hedging, no rationalizing on the paper's behalf.
- Do NOT output a top-level PASS / WARN / FAIL verdict. Output per-point rulings
  and counts only. The verdict is computed externally from your rulings.
```

## The six attack axes, expanded

The attack picks the most damaging combination, at most two axes fused. This catalog is the menu, not a checklist to cover.

1. **Theorem validity.** The headline rests on a theorem that is stated but not proved as written, or proved under hypotheses the statement omits. Most common in theory papers with many theorem-class environments.
2. **Assumption-versus-claim mismatch.** The abstract claims a general object; the body silently conditions on a special case. The reviewer's line: "the title says general, Section 4 only proves the i.i.d. bounded case."
3. **Missing proof obligation.** A lemma the headline depends on is invoked without proof: a concentration bound, a generic-position assumption, a prefactor or envelope bound. The paper treats it as folklore; the reviewer treats it as the hole.
4. **Limit-order or composition ambiguity.** For theory: limits in n, d, k, epsilon are composed in an unstated order, and the result flips depending on order. For systems: an asymptotic or scaling claim ("scales linearly") is stated without the regime, the contention model, or the saturation point it holds in.
5. **Claim-versus-evidence gap.** The take-away is broad; the evidence is one dataset, one workload, or one hardware platform. The reviewer asks whether the result is a property of the method or of the single setting it was measured in.
6. **Scope overclaim.** Title or abstract sells substantially more than the body delivers. This is the most common reject-attack pattern and the one balanced reviews most often soften into a minor comment.

## Rejection-dimension checklist (background for the attacker)

Adapted from a reviewer-style rejection taxonomy. The attacker uses this to find the most damaging line; it is not a structure for the memo. The memo is one argument, not a walk through this table.

| Dimension | Typical failure signal |
|---|---|
| Insufficient contribution | The target failure case is too common, or the technique is already well explored and the gain is predictable. |
| Unclear writing | A key module lacks motivation, or technical detail is missing and the work is not reproducible. |
| Weak empirical effect | The improvement over strong baselines is marginal, or absolute performance is still too low for the venue. |
| Incomplete evaluation | Missing ablations, missing strong or recent baselines, missing standard metrics, or datasets too simple to prove the method works. |
| Problematic method design | The experimental setting is unrealistic, the method needs per-scenario tuning, or a new mechanism adds more limitation than benefit. |

For each dimension the attacker can ask the three review questions: is the contribution genuinely non-obvious, are the gains surprising rather than predictable, and could a reviewer reasonably argue the net benefit is negative? The strongest of these becomes the memo's single line.

## The 3-way action vocabulary

The helper maps every verdict to one of three recommended actions. This vocabulary is ported from an adversarial review workflow that rules each weakness `pass`, `needs revision`, or `needs new experiment`.

- **pass.** The defense survives. No unresolved points, and any partial points are minor. The paper can ship against this attack.
- **needs revision.** There is an open point, but a targeted prose or framing edit can close it. Scope qualifications in the abstract, an added limitation paragraph, or a tightened theorem statement all qualify.
- **needs NEW experiment.** The open point is empirical. Prose cannot close it. A new experiment, ablation, baseline, or measurement is the only real fix. The helper emits this whenever any unresolved point carries `needs_experiment: true`.

The distinction between the last two matters most. Telling an author to "revise" an evidence gap wastes a rebuttal cycle. The empirical action says plainly that words will not fix it.

## Verdict mapping (what the helper computes)

The helper at `scripts/compute_verdict.py` implements this table. The rows are ordered most-severe first; the first matching row wins. Severity is read only for `partially` and `unresolved` points. The mapping is a pure function of the rulings, which is exactly why a script with no taste can own it and the adjudicator cannot.

| Verdict | reason_code | Trigger | Action |
|---|---|---|---|
| FAIL | unresolved_critical | At least one `unresolved` at `critical` severity | needs NEW experiment if that point is an evidence gap, else needs revision |
| FAIL | unresolved_needs_experiment | At least one `unresolved` at `major` flagged `needs_experiment: true` | needs NEW experiment |
| WARN | unresolved_major_or_minor | At least one `unresolved` at `major` or `minor`, and no `critical` | needs revision |
| WARN | partial_critical_or_repeated_major | At least one `partially` at `critical`, OR at least two `partially` at `major` | needs revision |
| PASS | defense_survives_minor_partial_only | Zero `unresolved`, and every `partially` is at `minor` severity | pass |
| PASS | defense_survives | Zero `unresolved` and zero `partially` | pass |

PASS requires zero `unresolved`. Any `partially` at `major` or higher caps the verdict at WARN. The helper exits 2 on malformed input: a point count outside 3 to 7, an unknown ruling, or a missing severity on a non-answered point.

## Why these labels and this separation

The attack-then-adjudicate split, the neutral `answered_by_current_text` label, and the external verdict all serve one goal: an honest read of whether the paper survives its worst objection. Forcing one committed argument produces sharper feedback than a ranked list. Reading the paper cold, with a label that does not assume prior patching, curbs optimism bias. Computing the verdict outside the adjudicating thread removes the temptation to grade its own work. The result is advisory, and the user decides what to act on.

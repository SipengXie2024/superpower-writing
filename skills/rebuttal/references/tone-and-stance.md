# Tone and Stance

Use this file when drafting response prose, rewriting a defensive author note, or deciding how to disagree. All examples target CS / systems / ML venues.

## Core posture

- Cooperative but not submissive.
- Evidence-forward, not personality-forward. Lead with the result, not the author's feelings.
- Concise enough for a meta-reviewer to audit in one pass.
- Respectful to reviewers without hiding the paper's real limits.
- Transparent about missing information and unresolved risks.

The reviewer response is read by the reviewers and the meta-reviewer, and at OpenReview venues it may be public. Write every line as a professional, traceable artifact.

## Evidence-tiered verb ladder

Match the claim verb to the strength of the evidence behind it. Overclaiming with strong verbs on weak evidence is the single most common way a rebuttal backfires; a reviewer who challenged the claim sees the same overreach repeated.

| Evidence strength | Verbs to use | Example |
|-------------------|--------------|---------|
| Strong (controlled result, proof, large effect) | `demonstrate`, `show`, `establish` | "Table 3 shows a 1.4x speedup across all context lengths." |
| Moderate (consistent trend, supporting analysis) | `indicate`, `suggest`, `support` | "The ablation indicates the gain comes from the routing step." |
| Limited or associative (correlation, single setting) | `are consistent with`, `may reflect`, `raise the possibility` | "These results are consistent with reduced memory traffic." |

If the reviewer challenges causality and your evidence is associative, soften the causal verb before drafting the reply, not after the reviewer pushes again. Downgrade "X causes Y" to "X is associated with Y; we do not claim a causal mechanism" when the experiment does not isolate the cause.

## Recommended sentence patterns

Use these only when the facts support them:

```text
We thank the reviewer for this concrete suggestion.
We agree the original wording did not make this point clear.
We have revised [Section X] to clarify that ...
To address this concern, we ran [experiment] under the same protocol as ...
The new result in Table 3 shows ...
We have softened the claim from "[strong]" to "[calibrated]".
We respectfully disagree with this reading because [manuscript evidence or scope reason].
We agree [requested work] would be valuable; it falls outside this paper's scope because ...
We now state this limitation explicitly in [Section X].
```

Each pattern carries an answer, an action, or a location. None is a standalone pleasantry.

## Forbidden-phrase blocklist

Never ship these as a final response. Each either accuses the reviewer, pleads a non-scientific excuse, or says nothing.

```text
The reviewer misunderstood ...
The reviewer is wrong ...
The reviewer failed to ...
Due to limited time / compute / GPUs, we cannot ...
This is beyond our ability ...
As is well known ... / As everyone knows ...
We believe this is sufficient.
We have revised accordingly.          # says nothing: what, and where?
Thank you for the comment.            # thanks cannot be the whole reply
Changed.                              # no content, no location
```

Thanking a reviewer is fine. Thanks alone is not a response. Every reply still needs a direct answer, an action, a manuscript location, or an explicit unresolved flag.

"We have revised accordingly" and "Changed" fail because they give the reviewer nothing to verify. Replace them with the specific edit and its location: "We added a variance column to Table 2 (Section 5.1)."

## Disagreement pattern

Disagree in this order. A reflex "we disagree" is the failure mode; a reasoned contrast is the goal.

1. Acknowledge the concern.
2. State the point of disagreement narrowly. Disagree with one specific reading, not the reviewer.
3. Give manuscript evidence, external evidence, or a scope reason.
4. Make a small clarifying edit if the manuscript may have invited the confusion.
5. Do not personalize. The disagreement is about the claim, not the reviewer.

Template:

```text
We appreciate the reviewer raising this. We respectfully disagree that [narrow point],
because [manuscript evidence in Section X / scope reason]. To make this clearer, we have
revised [location] to state that [revised text].
```

## Reviewer-misunderstanding pattern

When a reviewer misread the paper, do not say so. Treat the misread as a presentation signal and fix the presentation:

```text
We agree the original text did not make this distinction clear. We have revised
[Section X] to clarify that [the specific distinction the reviewer missed].
```

This converts a potential accusation into an improvement. The meta-reviewer sees an author who responds to confusion by clarifying, not by blaming.

## The structural_distinction move

The strongest reviewer attack in CS / systems / ML is "your method reduces to X" or "this is just generic Y" or "this is subsumed by Z". Denying the reduction looks defensive and usually loses, because the reduction is often locally true.

Concede the local reduction, then show the structural feature your parameterization preserves that the generic method does not. Back it with a concrete mechanism: a theorem dependency, a derivation step, or an empirical consequence. Never use the move rhetorically without that supporting mechanism.

Template:

```text
The reviewer is correct that in the [special case / single-layer / linear] setting our
method reduces to [X]. The contribution is what survives outside that case: our
parameterization preserves [structural feature, e.g. the per-head gating that X collapses],
which [concrete consequence: yields the bound in Theorem 2 / produces the 1.4x gain in
Table 3 that X cannot]. We have added a sentence in [Section X] making this reduction and
the preserved structure explicit.
```

The shape is: agree on the reduction, name the preserved structure, cite the mechanism that makes it matter, point at the edit. A concession with a preserved claim is stronger than a denial, because it shows the author understands exactly where the method is and is not novel.

## Concede without surrendering

When the reviewer is partly right, accept the local point explicitly, then state what remains true and why it still supports the contribution. Always pair the concession with the thing it preserves: a theorem, a mechanism, an empirical result, or a scope condition.

```text
The reviewer is right that [local point, e.g. the gain shrinks at small batch size].
The paper's claim holds in [the regime that matters: the large-batch serving setting
in Section 5], where [the preserved result]. We have bounded the claim to that regime
in [Section X].
```

A bare concession that drops the claim weakens the paper. A concession bounded to where the claim still holds keeps the contribution intact while showing honesty about its limits.

## Pre-registered-calibration phrasing

When a threshold, hold-out set, or hyperparameter was fixed before any test result or generated sample was inspected, say so explicitly. This defuses cherry-pick attacks at almost no word cost.

```text
The threshold was set on the validation split before any test-set result was inspected.
```

```text
Hyperparameters were tuned only on the development set; the test set was touched once.
```

Use this phrasing only when it is true. Claiming a pre-registered protocol that did not happen is fabrication and the most damaging kind, because it manufactures methodological credibility the work did not earn. If the protocol was not pre-registered, do not imply that it was; instead report what you actually did and, if needed, soften the affected claim.

## Surface non-obvious design choices upfront

If the evaluation has a non-obvious caveat a hostile reviewer could weaponize, name it first with a concrete number. Pre-empting the reverse-engineering is cheaper than defending against it.

```text
Comparisons are compute-matched, not epoch-matched: every method received the same
total FLOPs, which we report in Table 4.
```

Examples of choices worth surfacing: compute-matched versus epoch-matched training, a frozen parameter subset, an atypical seed protocol, a restricted context length, a non-standard tokenizer. State the choice and its number once in the setup; it pre-empts the adversarial reading without inviting it.

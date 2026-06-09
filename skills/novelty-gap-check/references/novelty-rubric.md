# Novelty delta rubric

How to score each core claim HIGH, MED, or LOW against its closest prior work, how to apply the non-obvious novelty rules, and how to aggregate per-claim deltas into an overall verdict.

## 1. Per-claim delta tiers

Score every core claim against the single closest prior work found in Phase B. Use MED as the default. Justify any move up or down with a specific overlap note.

### HIGH novelty

- No prior work does this claim, or the closest prior work differs on a principled axis that the claim makes central.
- The mechanism is new, or a known mechanism is applied in a way that yields a surprising, well-argued insight.
- A reviewer would have to reach for an analogy rather than a direct precedent.

Examples of HIGH:

- A new training objective that no prior work formulates, with a plausible reason it changes outcomes.
- Transplanting a mature technique across a non-obvious domain boundary, where the transplant exposes something the source domain never tested. The surprise is the contribution, not the pairing.

### MED novelty

- The claim combines known components in a new configuration, and the gain is real but incremental.
- A known mechanism is applied in a new setting, and the setting is genuinely different but not surprising.
- The closest prior work shares the core idea but differs in scale, modality, or one design choice.

Examples of MED:

- Adapting a known attention variant to a new input modality, with a modest measured gain.
- Extending a published systems technique to a larger cluster size, where scale is the only axis.

### LOW novelty

- A published baseline in the same subfield already does this claim, with at most a cosmetic difference.
- The claim is "we use a bigger model" or "we combine two existing methods" with no new insight.
- A reviewer would frame it as "dominated by prior work X".

Examples of LOW:

- Re-running a known method on a new but unremarkable dataset and reporting expected numbers.
- A pipeline that chains two off-the-shelf modules with no analysis of why the combination matters.

## 2. The non-obvious novelty rules

These two rules override a naive reading of the tiers. They are the most common places a novelty judgment goes wrong.

### Rule 1: applying X to Y is NOT novel by itself

Taking method X and running it on problem Y is not a contribution just because the X-Y pairing has no prior paper. The pairing is novel only when the application reveals a surprising insight. Ask: what did we learn that we could not have predicted from X alone and Y alone?

- If the answer is "X works on Y about as well as expected", the claim is LOW, regardless of whether anyone published the exact pairing.
- If the answer is "X fails on Y in a way that reveals a hidden property of Y", or "X succeeds on Y in a way that contradicts a held assumption", the claim can be HIGH. The insight is the contribution.

Check both the method and the experimental setting for novelty. A novel setting can carry a paper even when the method is borrowed, but only if the setting teaches something.

### Rule 2: separate method novelty from finding novelty

A claim can fail as a method contribution and still succeed as a finding contribution. Do not collapse the two.

- **Method novelty**: the technique itself is new or newly principled.
- **Finding novelty**: the technique may be known, but the result it produces is unexpected and well-evidenced, and it changes what the field believes.

When the method is not novel but the finding would be, say so explicitly in the report. Label the idea's contribution as method, finding, or both. Then position accordingly. A known method that overturns an assumption is framed as a finding paper, not undersold as a method paper that a reviewer will call derivative.

A finding-novelty claim raises the evidentiary bar. The result must be reproducible and decisive, because the method alone will not carry it.

## 3. Aggregation to an overall verdict

Map the set of per-claim deltas to one of three calls. A claim is **load-bearing** when the idea collapses without it.

| Condition | Verdict |
|-----------|---------|
| At least one core claim is HIGH, and no load-bearing claim is LOW | PROCEED |
| Strongest claim is MED, or a HIGH claim sits next to a load-bearing LOW that needs repositioning | PROCEED-WITH-CAUTION |
| Every core claim is LOW against recent prior work | ABANDON |

Refinements:

- A single HIGH claim is enough to PROCEED if the rest hold their own. Strong ideas usually dominate on one axis and stay defensible on the others.
- If two or more load-bearing claims are LOW, downgrade to ABANDON even when one claim is MED. A published baseline already dominates the core of the idea.
- A finding-novelty idea (Rule 2) PROCEEDs only when the finding is decisive and the experiment that proves it is in scope. Otherwise it is PROCEED-WITH-CAUTION pending that experiment.
- When the closest prior work for a load-bearing claim is `[UNVERIFIED]`, do not let the unverified paper force an ABANDON on its own. Flag the uncertainty and recommend resolving the citation before the user acts.

## 4. Scoring failures to avoid

- **Inflation**: scoring every claim HIGH to be encouraging destroys the signal. Default to MED and justify upward with a specific axis.
- **Title-matching**: judging overlap by title similarity instead of substance. Read the abstract.
- **Pairing-as-novelty**: treating an unpublished X-Y pairing as automatically HIGH. Apply Rule 1.
- **Method-finding conflation**: scoring a finding-novel idea as LOW because the method is borrowed. Apply Rule 2.
- **Recency blindness**: scoring against papers older than six months only. The recent window is where the idea most often dies.
- **Verdict-delta mismatch**: an overall PROCEED with no claim above MED is incoherent. Realign the verdict with the table.

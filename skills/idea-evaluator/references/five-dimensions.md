# Five-Dimension Scoring Framework

Reference for `idea-evaluator` Step 3. The Higher / Faster / Stronger / Cheaper / Broader idea-framing axes, the generative inversion that produced them, the anti-inflation scoring rule, and tiered anchors keyed to venue papers.

## Origin: the generative inversion

This framework comes from a discipline for generating incremental ideas given a strong baseline. The inversion is the whole point:

> Do not hunt for new problems with a solution in hand. Take a well-defined baseline and ask on which of five axes it can be improved.

Solution-hunting (the F9 fatal flaw) starts from a technique and looks for somewhere to apply it. It produces contrived problems. The inversion starts from a known baseline and a known task, then asks a disciplined question: where can this be pushed? Each axis below is one direction to push.

The same framework flips into an evaluation lens. Given an idea, score how strongly it advances each axis versus the current baseline. Strong ideas dominate one axis and hold their own on at least one more. Weak ideas are vague on four or more axes.

## The five axes

### Higher: effectiveness

Improves accuracy, quality, or an effectiveness metric over the strongest current baseline.

Entry strategies:

- **Information or modality augmentation.** Does the baseline ignore an input signal that would help? Feeding schema-linked table statistics or domain documents to a model that saw only the raw query is one example.
- **Feedback-driven refinement.** Can execution feedback (compiler errors, runtime exceptions, failing tests) drive iterative self-correction? Code-generation success often rises when execution errors are returned to the model for another attempt.
- **Error-driven root-cause analysis.** Run the baseline, cluster its failures, find the dominant failure mode, and build a module that targets it.

### Faster: efficiency

Cuts wall-clock time, token cost, memory, or compute while holding effectiveness.

Entry strategies:

- **Caching and experience reuse.** Cache successful trajectories so repeated tasks skip replanning.
- **Parallelization and decoupling.** Split a long serial pipeline into independent sub-tasks for specialized components running in parallel.
- **Early exit and dynamic routing.** Route easy cases to a cheap model and escalate only the hard ones to a large model.

### Stronger: robustness and generalization

Holds performance under noise, out-of-distribution inputs, or cross-domain transfer.

Entry strategies:

- **Noise and fault tolerance.** Handle malformed or ambiguous inputs gracefully, for example by asking for disambiguation instead of failing silently.
- **Exception recovery.** Detect API failures, bad outputs, or tool crashes and retry with an alternative.
- **Decoupled representations.** Separate general reasoning from domain-specific knowledge so the reasoning module transfers zero-shot to a new domain.

### Cheaper: data or solution cost

Reduces annotation, training, or deployment cost while holding effectiveness.

Entry strategies:

- **Model-based data synthesis.** Use a strong foundation model to synthesize labelled data or simulate trajectories, cutting human annotation.
- **Active learning with a human in the loop.** Select the smallest sample set for human review that maximizes model improvement, instead of annotating the whole corpus.
- **Knowledge distillation.** Distill a large model's reasoning into a small deployable model, holding accuracy at lower inference cost.

### Broader: cross-domain and unification

Transplants a mature idea from one domain to another, or unifies a fragmented set of tasks under one framework.

Entry strategies:

- **Cross-domain transplantation.** Take a mature technique from one field and apply it in another. Database query optimizers, for instance, contribute cost estimation and plan caching to agent planning.
- **Generalization and unification.** Unify a family of tasks (text-to-SQL, text-to-code, text-to-chart) under one shared framework instead of one model per task.

## Scoring tiers

For each axis, assign an integer 1 to 10. Use these tiers. The text in parentheses names the entry strategy a high score should rest on.

### Higher

- 9-10: a principled new input signal or feedback loop no prior work exploits, with a plausible path to multi-point accuracy gains.
- 6-8: a known signal or feedback mechanism applied in a new setting; gains modest but real.
- 3-5: a standard prompt-engineering or fine-tuning variant; gains likely within noise of a strong baseline.
- 1-2: does not obviously advance effectiveness.

### Faster

- 9-10: a large, quantified efficiency gap closed by a principled mechanism (for example, a multiple-fold speedup at no accuracy loss).
- 6-8: a known bottleneck targeted by a plausible mechanism; moderate speedup.
- 3-5: efficiency mentioned but no specific mechanism; gains marginal.
- 1-2: does not address efficiency.

### Stronger

- 9-10: a known brittleness (ambiguity, OOD, domain shift) addressed by a principled mechanism, with cross-domain evaluation planned.
- 6-8: robustness with a concrete mechanism, but evaluated on a single domain.
- 3-5: lip service to robustness with no mechanism.
- 1-2: does not address robustness.

### Cheaper

- 9-10: a high-quality dataset at a fraction of naive-annotation cost, or deployment at an order of magnitude lower cost than the baseline.
- 6-8: cost reduced by a known mechanism (a small constant factor).
- 3-5: cost reduction mentioned but not quantified.
- 1-2: does not consider cost.

### Broader

- 9-10: a mature technique transplanted in a non-obvious direction with a plausible mechanism, or three or more fragmented task families unified.
- 6-8: a known idea transplanted, or two task families unified.
- 3-5: a connection to another domain suggested with no concrete mechanism.
- 1-2: siloed.

## Anti-inflation rule

This is the rule that keeps the scores meaningful.

> Default every dimension to 5. Justify each move upward with a specific sentence from the idea. Scoring every dimension 7 or 8 destroys the signal.

Common scoring failures:

- **Inflation.** Pinning everything at 7 or 8 "to be generous" makes the radar chart flat and uninformative. Anchor at 5 and earn each point.
- **Deflation.** Pinning everything at 3 or 4 usually means the idea was not understood. Re-read it.
- **Uncited evidence.** A score with no sentence from the idea pointing at why is not a score. Mark it for re-read.
- **Generic lift suggestions.** "Try a different prompt" is not a lift. Name an entry strategy from this file.
- **Score and verdict mismatch.** A Strong Accept with no dimension above 7 is incoherent. Realign before emitting the verdict.

## Aggregation

After scoring all five:

- Top dimension at 8 or above and a second at 6 or above: that pair is the paper's thesis. Emphasize both in the introduction.
- Three or more dimensions at 5 or below: the idea is thin. Sharpen the one axis where it shines, or pivot.
- All five at 4 or below: Reject and Pivot.
- No single dimension reaches 7: the idea is vague. Ask the user to name the one dominant axis before re-evaluating.

## Tiered anchors keyed to venue papers

These illustrate what each tier looks like in practice at top venues. The patterns below are anchors the upstream framework cited. Verify the exact venue, year, and result against the literature before quoting any of them. Mark unconfirmed attributions `[UNVERIFIED]` rather than restating them as fact.

| Axis | Anchor pattern at a top venue | Illustrative score |
|---|---|---|
| Higher | Inference-time search (for example, MCTS) added to a task that prior work attacked with single-pass decoding, yielding multi-point gains on a public benchmark | 8 |
| Faster | Removing a per-iteration full-pass cost by reusing a signal already computed during training, for zero added inference overhead | 9 |
| Stronger | An agent that decouples planning from domain-specific tools and ships zero-shot cross-domain evaluation | 8 |
| Cheaper | A reverse-synthesis pipeline that generates questions from verified answers, side-stepping manual annotation | 8 |
| Broader | Search-based workflow generation transplanted from neural-architecture-search-style methods to agent pipeline design | 8 |

Read the pattern, not the paper name. The score is high because the mechanism is principled and the gap it closes is real and quantified. An idea that only gestures at the same axis without a mechanism sits at 3 to 5, not 8.

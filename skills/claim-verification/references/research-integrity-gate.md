# Research-Integrity Gate (experiment-bearing CS / ML / systems papers)

Use this file when the manuscript reports its own experiments and the user opts into an integrity pass. It catches failure modes that read as competent work: a result from a broken pipeline looks the same on the page as a real one. The numeric/table pass in `SKILL.md` Pass 3 checks that prose numbers match tables. This gate is stricter and tries to catch numbers that match each other but do not match reality.

This gate is OPTIONAL and ADVISORY. It never auto-rejects, never mutates claim `STATUS`, and never edits the manuscript. Every finding surfaces to the user, who decides. The gate adapts AI-research failure-mode work to our LaTeX house style and retargets examples to NeurIPS / ICML / ICLR / OSDI / NSDI / SOSP venues.

Loaded by:

- `skills/claim-verification/SKILL.md` §Optional research-integrity gate: one-line pointer plus the verdict contract.

## When this gate applies

Run it only when all three hold:

1. The paper reports experiments the authors ran (benchmarks, training runs, ablations, microbenchmarks, simulations).
2. The user has experiment artifacts on disk the gate can read (result files, run directories, configs, logs).
3. The user asked for an integrity pass, or you flagged a smell during Pass 3 and the user opted in.

Skip it for theory papers, position papers, surveys, and any submission with no first-party experimental numbers. A theory proof has no run directories to count, so the heuristics below do not apply. Say so and move on rather than forcing the gate.

## The three-way verdict per heuristic

For each heuristic, return exactly one verdict. This mirrors the soft-fail contract in `SKILL.md` Pass 2c.

- **CLEAR**: you have evidence the failure does not apply. Record the evidence in one line (the log, the config field, the run-directory count).
- **SUSPECTED**: a detection check returned a concerning answer. Surface it to the user with the specific passage and the specific artifact that triggered it. SUSPECTED is advisory: never auto-reject, never flip `STATUS`, never edit prose. The user confirms the flag, overrides it with a recorded reason, or revises the passage and re-runs.
- **INSUFFICIENT**: you cannot rule the failure in or out without an artifact the user has not provided (a missing log, a run directory you cannot see). Name the missing artifact. INSUFFICIENT is not a pass and not a fail; it is a request for input.

Aggregate the gate to one headline verdict for the report: CLEAR only when every heuristic is CLEAR; SUSPECTED when any heuristic is SUSPECTED; otherwise INSUFFICIENT.

## NEVER-FABRICATE

This gate reads artifacts and reports what it finds. It never invents a missing number, never guesses a seed count, never assumes a log exists. When an artifact is absent, the verdict is INSUFFICIENT with the artifact named, never a fabricated CLEAR. Mark anything you could not check `[UNVERIFIED]` and surface it.

## Pipeline-integrity heuristics

These four catch results produced by a broken or misread pipeline. They are the modes a numbers-match-the-table check cannot see, because a constant leaking through a bug will match itself across prose and table.

### H1: Suspiciously round effect size

A pipeline that silently collapses (a constant leaking past a broken branch, a metric that never updates, a dataloader returning one class) often produces an effect size that is too clean. Treat these as a tell, not a verdict.

Detection:

- Scan reported effect sizes and headline deltas for exact round values: exactly `0.5`, exactly `2x` the baseline, exactly `100%`, exactly `0` variance across seeds, an accuracy that is precisely `1/k` for a k-class task.
- Check whether error bars or confidence intervals are identical across conditions that should differ. Identical spread across distinct settings suggests the number never actually moved.

Verdict:

- CLEAR: the round value is backed by a log showing genuine per-seed variation around it, or the value is round for a principled reason the user states (a theoretical bound, a fixed budget).
- SUSPECTED: a headline number is exactly round and you cannot find per-run variation behind it. Surface the passage and ask the user to point at the runs that produced it.
- INSUFFICIENT: no per-run artifact is available to confirm or deny variation.

### H2: Unexplained surprise

A result framed as surprising may be a real finding, or it may be a bug the narrative reframed as a discovery. Surprise that no prior work predicts is high-risk: if nothing in the literature expected the opposite, there may be nothing surprising, only something broken.

Detection:

- Grep the draft for `surprisingly`, `unexpectedly`, `counterintuitively`, `contrary to`, `against our hypothesis`, `to our surprise`.
- For each hit, ask: does a cited paper actually predict the opposite of what was observed? A genuine surprise contradicts a stated prior expectation. A bug-driven surprise contradicts nothing because no one expected anything.
- Ask whether the surprising result appeared on the first run or only after many debugging iterations, and whether it reproduces in a fresh environment.

Verdict:

- CLEAR: the surprise contradicts a specific prior result the user can cite, and it reproduces.
- SUSPECTED: a surprise claim has no literature predicting the opposite, or it appeared on a first run and was never reproduced. Surface the passage.
- INSUFFICIENT: you cannot tell whether reproduction was attempted.

### H3: Seed-count mismatch

The paper states a seed or run count that should match countable artifacts on disk. A mismatch means the number was written from intention rather than from the runs.

Detection:

- Grep the draft for claims of the form `N seeds`, `averaged over N runs`, `N random restarts`, `N-fold`.
- Count the actual result directories or per-seed result files the user has for that experiment.
- Compare. The paper saying "averaged over 5 seeds" while only 3 run directories exist is the canonical case.

Verdict:

- CLEAR: the stated count equals the count of result directories or per-seed files.
- SUSPECTED: the stated count exceeds the artifacts found. Surface both numbers and the experiment.
- INSUFFICIENT: the user has not pointed the gate at the run directories.

### H4: Bug reframed as a novel insight

A compound failure: a pipeline bug produces an unexpected behavior, and the writing stage builds a contribution around it. The paper reads more interesting than a correct version would, because the "insight" is an artifact.

Detection:

- For any claim that a system or model "behaves unexpectedly under condition C" or "exhibits a previously unreported effect", ask whether condition C is correctly implemented. A misimplemented condition manufactures the effect.
- This heuristic compounds H1 and H2. When H1 (a too-clean number) and H2 (an unexplained surprise) both fire on the same result, escalate here: the result is a candidate bug-as-insight.
- Ask whether the effect survives an independent reimplementation of condition C.

Verdict:

- CLEAR: the effect reproduces under an independent implementation of the condition, or a cited paper reports the same effect.
- SUSPECTED: the effect rests on one implementation of the condition and has not been reproduced, especially when H1 or H2 also fired. Surface the claim and the dependency.
- INSUFFICIENT: no independent reimplementation or corroborating artifact is available.

## Number-tracing failure modes

These four trace a reported number back to the raw evidence. They overlap with `SKILL.md` Pass 3 but go further: Pass 3 confirms a prose number matches a table; these confirm the table itself reports the evidence faithfully. Run them with a fresh read of the raw result files, not the authors' summary of them, so prior expectation does not color the trace.

### N1: Best-seed cherry-pick

The paper reports a peak number while the runs support only an average. Reporting the best of five seeds as the headline, when the mean is materially lower, overstates the result.

Detection: for each headline metric, check whether the raw files hold multiple seeds. If they do, confirm the paper states which statistic it reports (`mean`, `best`, `median`) and that the reported value matches that statistic over all runs, not the maximum.

Verdict: CLEAR when the value matches the stated aggregation over all seeds. SUSPECTED when the value matches only the best seed and the paper implies an average. INSUFFICIENT when per-seed values are unavailable.

### N2: Delta-arithmetic error

A relative-improvement claim whose arithmetic does not check out. The paper says "improves by 15%" while the actual relative delta computed from the two reported numbers is different.

Detection: for each `improves by X%` / `reduces by X%` claim, recompute the relative change from the underlying values, for example `(85.3 - 73.1) / 73.1 = 16.7%`. Confirm the stated percentage matches, allowing only ordinary rounding to displayed precision.

Verdict: CLEAR when the recomputed delta matches the claim. SUSPECTED when it does not. INSUFFICIENT when one of the two operands is not reported anywhere.

### N3: Caption-table mismatch

A figure or table caption describes something the figure or table does not show. The caption says "win rate across four datasets" while the table holds three columns.

Detection: cross-check every `\caption{...}` against the content of its `figure` or `table` environment. Confirm the caption's described axes, conditions, dataset count, and metric match the rows, columns, and units actually present.

Verdict: CLEAR when caption and content agree. SUSPECTED when they disagree. INSUFFICIENT when the underlying data file for the figure is not on disk to confirm what the figure plots.

### N4: Scope overclaim

Generalizing language that outruns the evaluation. The paper says "consistently outperforms across settings" after testing on two datasets, or "in all cases" after one workload.

Detection: grep argumentative prose for `consistently`, `in all cases`, `across settings`, `in general`, `universally`, `always outperforms`. For each, count the datasets, workloads, or conditions actually evaluated. Confirm the generalization matches the scope. See `SKILL.md` Pass 3 and the drafting style cautions for the related rule against dataset pre-hedging.

Verdict: CLEAR when the scope language matches the evaluated breadth. SUSPECTED when the language claims more breadth than was tested. INSUFFICIENT when the evaluation breadth cannot be determined from the artifacts.

## Independence note (Type-B routing)

Several heuristics here ask for taste, not a lookup. Judging whether a surprise is genuine (H2), whether an insight is real or a reframed bug (H4), or whether scope language is fair (N4) is a Type-B judgment under the gate in `SKILL.md`. A drafting loop that produced the prose must not acquit its own Type-B verdict on these. Route them to an independent or cross-model reviewer thread, following the two-stage review pattern in `planning-foundation/references/review-loop-protocol.md`, rather than self-clearing. The mechanical traces (N1 arithmetic, N3 caption-vs-content, H3 directory count) are Type-A: a script with no taste could answer them, so the gate may self-judge those.

## Reporting

Write the gate's findings into `.writing/verify-report.md` under an "Advisory: Research Integrity" block, alongside the existing Pass 2 advisory output. For each fired heuristic record: the heuristic id, the verdict, the exact passage, the artifact checked (or the artifact missing), and the recommended user action. Do not flip any claim `STATUS` on the basis of this gate. A SUSPECTED finding is a note for the human author, never a gate that blocks the pipeline on its own.

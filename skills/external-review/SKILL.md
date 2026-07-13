---
name: external-review
description: Cross-model critical review of a paper, idea, or result by two independent external critics. It asks for concrete mock-review, results-to-claims, and experiment-plan deliverables while preserving provider disagreement. Use when the user says "review my paper", "get an external review", "stress-test this idea", "mock venue review", or requests brutally honest pre-submission feedback.
---

# External Review

Run an independent Codex and Hermes review of the primary academic artifacts. Keep both opinions visible. The two critics do not vote, negotiate a consensus, or select a verdict for the user.

Follow `skills/_shared/core/dual-consult-protocol.md`. The critic reads the original files. The executor supplies only the reviewer role, objective, venue, source paths, and requested output. Do not pre-digest the paper, state likely strengths, or pass one provider's opinion to the other.

Every score and recommendation is advisory. Never edit manuscript prose, flip claim status, reject a paper, or launch experiments from a review result without the user's decision. Never fabricate a failed provider's review.

## When to use

Use this skill when the user asks for:

- an external or second-opinion paper review;
- a venue-calibrated mock review;
- a results-to-claims matrix;
- the smallest experiment likely to improve acceptance;
- an independent review of an idea, method, or result.

Use `claim-verification` instead for deterministic citation and evidence checks. Use `polish` for copy editing.

## Do not schedule a verdict

This is a verdict-bearing task. Do not place it inside `/loop`, `/schedule`, or `CronCreate`. A scheduled check may wait for an experiment to finish, but it cannot decide whether the paper is good enough. See `references/cadence-and-independence.md`.

## Process

### 1. Check disclosure scope

Public papers may be sent directly. Before sending an unpublished draft, confidential review, restricted data, personal information, or other sensitive material, list the exact files or excerpts that Codex and Hermes will receive. Obtain user confirmation.

### 2. Prepare a neutral brief

Read the project to identify the source files, not to tell the critics what conclusion to reach. Normally include:

- `.writing/main.tex` and `.writing/manuscript/*.tex`;
- `.writing/findings.md`;
- `.writing/outline.md`;
- relevant `.writing/claims/section_*.md` files;
- target venue, page limit, and review objective.

Write `.writing/reviews/review-request.md`. Include paths and structural facts only. Exclude the executor's summary, interpretations, recommendations, extracted findings, and leading questions. The exact allow and deny rules live in `references/cadence-and-independence.md`.

### 3. Run both reviewers concurrently

Use the paired runner, always in the background with a Bash timeout of at least `660000` ms:

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/paired_consult.py" \
  --cd "<absolute project root>" \
  --handoff-kind venue-review \
  --PROMPT "Read <absolute path>/.writing/reviews/review-request.md and every source it names. Act as a senior <venue> reviewer. Produce a specific, evidence-linked review. Do not modify files."
```

Do not poll. When the command returns, inspect `pair_status`:

- `complete`: both independent handoffs are available;
- `partial`: preserve the successful handoff and report the failed provider;
- `failed`: report both failures and stop.

Do not replace either failure with a local model's invented opinion.

### 4. Request concrete deliverables

Run separate paired calls for the three deliverable types when needed:

1. `venue-review` for Summary, Strengths, Weaknesses, Questions, Score, Confidence, and accept-lift conditions.
2. `results-claims-matrix` for outcome combinations and the claims each combination permits or rules out.
3. `experiment-plan` for one to four concrete experiments with datasets, baselines, scales, hyperparameters, ablations, metrics, budget, and priority.

Use the prompt structures in `references/reviewer-deliverables.md`. Never let either provider invent a result that has not been measured.

For a revision follow-up, reuse Codex's `SESSION_ID` and pass each provider only its own prior structured handoff:

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/paired_consult.py" \
  --cd "<absolute project root>" \
  --handoff-kind venue-review \
  --CODEX_SESSION_ID "<codex session>" \
  --CODEX_CONTEXT_FILE "<codex handoff json>" \
  --HERMES_CONTEXT_FILE "<hermes handoff json>" \
  --PROMPT "Read the revised source files and reassess the prior concerns. Do not modify files."
```

Hermes remains stateless. Its context file must restate its own prior handoff. Never cross the two files.

Stop when the requested deliverables exist or the user decides no further round is useful. Do not wait for the providers to agree.

### 5. Verify and present

Before reporting any academic claim, check its source identifier, locator, number, method, and statistical value against the original file or paper. A structurally valid handoff is not factual verification.

Present the result in this fixed order:

```markdown
## Codex view
<score, confidence, strengths, weaknesses, questions, evidence, uncertainties, verification needed>

## Hermes view
<score, confidence, strengths, weaknesses, questions, evidence, uncertainties, verification needed>

## Provider status
- pair_status: complete | partial | failed
- failures: <provider and stable error, if any>
```

Do not add a combined verdict, consensus, winner, or preferred provider. State that both reviews are advisory and the user decides what to adopt.

### 6. Persist without smoothing disagreement

Save `.writing/reviews/external-review-<ISO-date>.md` with separate `Codex view` and `Hermes view` sections. Preserve each provider's evidence, uncertainty, verification queue, and failure status. Add any requested matrix and experiment plan under provider-specific headings.

If `.writing/progress.md` exists, append one row with the report path and `pair_status`. Do not record a single merged verdict. Do not edit the manuscript or claim files.

## Key rules

**The critics read; the executor points.** Pass primary paths and neutral constraints, not an interpretation.

**Disagreement is evidence to inspect.** Reopen the disputed source. Do not settle it by voting.

**One lane may fail.** Keep the successful lane and report the other accurately.

**The user decides.** Scores and experiment proposals never trigger actions automatically.

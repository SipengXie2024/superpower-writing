---
name: review
description: Cross-model paper review in two modes the user chooses. The adversarial mode builds the single strongest kill argument, adjudicates it cold in a fresh lane per provider, and maps rulings to an advisory PASS, WARN, or FAIL. The venue mode runs a calibrated mock peer review with scores and an accept-or-reject lean, keeping Codex and Hermes independent. Use when the user says "review my paper", "find the kill argument", "mock venue review", or wants brutally honest pre-submission feedback.
---

# Review

One review skill, two modes. Both run an independent Codex lane and an independent Hermes lane, keep the two opinions visible and separate, and stay advisory. Neither mode edits manuscript prose, flips claim status, rejects a paper, or launches an experiment. The user decides what to act on.

- **`adversarial`** kills the idea by struggle. It commits one strongest-rejection memo per provider, adjudicates each in a fresh independent lane, and a helper maps the rulings to a non-self-graded PASS, WARN, or FAIL. Use it for the single worst-case reviewer argument before submission or rebuttal.
- **`venue`** simulates peer review. It runs a venue-calibrated mock review, scores the paper, and gives an accept-or-reject lean, plus optional results-to-claims matrices and experiment plans.

Both modes follow `skills/_shared/core/dual-consult-protocol.md`. Read it before dispatch.

## Pick the mode first

Do not silently default to a mode. Decide as follows:

- If the user's own words already name one mode, honor it and say which you picked. "Kill argument", "worst reviewer argument", and "stress-test to death" mean `adversarial`. "Mock venue review", "score my paper for <venue>", "second opinion", and "external review" mean `venue`.
- Otherwise, and for any generic "review my paper", ask with `AskUserQuestion`. Offer two options:
  - **Adversarial (kill argument)**: one committed worst-case rejection per provider, adjudicated cold, mapped to an advisory verdict. Best right before submission, when the user wants the single argument that sinks the paper.
  - **Venue (mock peer review)**: a program-committee-style review with scores, strengths, weaknesses, questions, and an accept-or-reject lean. Best for a calibrated second opinion and a fix list.

Route to the matching mode section once the user picks.

## Shared rules (both modes)

These hold in `adversarial` and `venue` alike. They come from `skills/_shared/core/dual-consult-protocol.md`.

**Two independent lanes, never merged.** Run Codex and Hermes concurrently through `${CLAUDE_PLUGIN_ROOT}/scripts/paired_consult.py`. Present a `Codex view` and a `Hermes view` under separate headings. Do not add a combined verdict, consensus, winner, vote, or preferred provider. Disagreement is a reason to reopen the source, not to vote.

**No cross-talk.** Codex never sees Hermes's memo or review, and Hermes never sees Codex's. Do not pass one provider's opinion, framing, or verdict into the other's brief.

**The critic reads; the executor points.** Supply only the reviewer role, objective, venue, source file paths, and the requested output shape. Do not pre-digest the paper, summarize its contents, state its likely strengths, extract findings, or ask leading questions. Let each provider read the original files. The full allow-and-deny list is in `references/cadence-and-independence.md`.

**Never fabricate a failed lane.** On `pair_status: partial`, keep the successful lane and report the failed provider with its stable error. On `pair_status: failed`, report both failures and stop. Never replace a missing review with a local model's invented opinion, and never make one provider speak for the other.

**Disclosure scope.** Public papers may be sent directly. Before sending an unpublished draft, a confidential review, restricted data, or personal information, list the exact files each provider will receive and get user confirmation. Approval for one file set does not cover later files.

**Detect-only and advisory.** This skill may write its review report and, if `.writing/progress.md` exists, append one row. It never edits manuscript prose, never flips claim `STATUS`, never rejects a paper, and never launches an experiment from a review result. Every score, verdict, and experiment proposal is advisory input, and the user owns the decision.

**Verify evidence after return.** A structurally valid handoff is not factual proof. Before relying on any cited file, line, equation, number, or statistic, open the source and check it. Keep anything you cannot check in `verification_needed`.

**Structured issue bundles, one per provider.** Each mode ends with every provider's findings extracted into that provider's own issues JSON at `.writing/reviews/issues-<provider>-<ISO-date>.json`, following the schema in `references/reviewer-deliverables.md`. Every issue carries a verbatim `quote` from the manuscript source and a stable `root_cause_key`. Run `scripts/verify_review_quotes.py` on each bundle; an unverified quote sends that finding back for re-anchoring against the source, never silently into the report. Bundles never merge across providers.

**Do not schedule the verdict.** Both modes are verdict-bearing. Never wrap either inside `/loop`, `/schedule`, or `CronCreate`. Schedule the external wait that precedes a review, such as a job finishing or a PDF compiling, never the judgment itself. See `references/cadence-and-independence.md`.

Always launch `paired_consult.py` in the background with a Bash timeout of at least `660000` ms. Do not poll. The runner starts both providers concurrently and returns when both settle.

---

## Mode: adversarial (kill argument)

Run two independent attack-then-adjudicate chains. Codex attacks, then a fresh Codex adjudicates, then the helper computes the Codex verdict. Hermes attacks, then a fresh Hermes adjudicates, then the helper computes the Hermes verdict. Never cross attacks between providers. Never merge the two verdicts.

### Preconditions

1. Confirm `.writing/` and `.writing/manuscript/*.tex` exist.
2. Inventory the manuscript, bibliography, and compiled PDF when present.
3. Confirm the headline is stable. If the title or abstract is still changing, defer the attack.
4. If the paper has neither theorem-class claims nor a scope, generality, or evidence-to-headline risk, recommend the `venue` mode instead.

The attack and adjudication stages stay independent within each lane, as well as across providers. Constructing and adjudicating the strongest rejection argument needs academic judgment and cannot be self-graded. The only deterministic step is mapping rulings to a verdict with the helper.

### Stage 1: paired attack

Use the attack brief in `references/attack-and-verdict.md`. Send one neutral objective and the original paper paths to both providers. Do not include prior reviews, fix lists, summaries, or preferred objections.

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/paired_consult.py" \
  --cd "<absolute project root>" \
  --handoff-kind adversarial-attack \
  --PROMPT "Read the listed current paper files. Produce one strongest rejection argument of about 200 words with exact source locators. Do not consult prior reviews and do not modify files."
```

Each provider commits to one argument, not a list of weaknesses. Keep the Codex attack and the Hermes attack in separate JSON files. Do not show one provider the other's memo. If one attack lane fails, the other may continue and the report stays partial. Never fabricate the missing memo.

### Stage 2: paired but lane-specific adjudication

Start a fresh Codex session. Hermes is always a fresh oneshot call. Pass no Codex `SESSION_ID` from the attack stage. Give each provider only its own attack.

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/paired_consult.py" \
  --cd "<absolute project root>" \
  --handoff-kind adversarial-adjudication \
  --CODEX_CONTEXT_FILE "<codex attack handoff json>" \
  --HERMES_CONTEXT_FILE "<hermes attack handoff json>" \
  --PROMPT "Read the current paper files and adjudicate the attack supplied in your own provider context. Decompose it into 3 to 7 atomic points. Do not use the other provider's view. Do not output a top-level verdict or modify files."
```

Each point gets exactly one ruling: `answered_by_current_text`, `partially`, or `unresolved`. A partial or unresolved point also records severity, whether a new experiment is required, and one recommended fix. Every academic assertion must cite a real source locator. Keep anything unverifiable in `verification_needed`.

### Stage 3: compute two verdicts

Extract each provider's points to a separate JSON object and run the helper once per provider:

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/skills/review/scripts/compute_verdict.py" < codex-points.json
python3 "${CLAUDE_PLUGIN_ROOT}/skills/review/scripts/compute_verdict.py" < hermes-points.json
```

Do not hand-derive either verdict. The helper validates the 3-to-7-point requirement and maps rulings to `PASS` (action `pass`), `WARN` (action `needs revision`), or `FAIL` (action `needs revision` or `needs NEW experiment`). The full mapping table is in `references/attack-and-verdict.md`. A missing provider stays missing. Do not copy the other verdict across.

### Stage 4: verify and persist

Extract each provider's `partially` and `unresolved` points into that provider's issue bundle (schema and extraction rules in `references/reviewer-deliverables.md`), then verify the quotes:

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/skills/review/scripts/verify_review_quotes.py" \
  .writing/reviews/issues-codex-<ISO-date>.json --source .writing/manuscript --write-back
python3 "${CLAUDE_PLUGIN_ROOT}/skills/review/scripts/verify_review_quotes.py" \
  .writing/reviews/issues-hermes-<ISO-date>.json --source .writing/manuscript --write-back
```

Then check every cited file, line, equation, table, number, and experiment against the manuscript. The quote check proves the words exist; it does not prove the adjudication is factually correct. Archive any prior `.writing/adversarial-review.md`, then write the report:

```markdown
# Adversarial Review (<ISO-8601 timestamp>)

## Codex view
### Attack memo
<verbatim structured memo>
### Adjudication
<atomic points, evidence, uncertainties, verification needed>
### Codex verdict
<PASS | WARN | FAIL, reason code, action, counts>

## Hermes view
### Attack memo
<verbatim structured memo>
### Adjudication
<atomic points, evidence, uncertainties, verification needed>
### Hermes verdict
<PASS | WARN | FAIL, reason code, action, counts>

## Provider status
- attack pair_status: <complete | partial | failed>
- adjudication pair_status: <complete | partial | failed>
- failures: <provider and stable error>

## Recommendation to the user
<advisory only; name which source passages to inspect or which experiment each lane requests>
```

Do not add an overall verdict, consensus, winner, or preferred provider. Disagreement is a reason to inspect the source, not to vote. If `.writing/progress.md` exists, append one row with both provider verdicts and the report path.

---

## Mode: venue (mock peer review)

Run an independent Codex review and Hermes review of the primary artifacts. Keep both opinions visible and let the user decide. The two critics do not vote, negotiate a consensus, or select a verdict for the user.

### 1. Check disclosure scope

Apply the shared disclosure rule. Before sending an unpublished draft or sensitive material, list the exact files or excerpts Codex and Hermes will receive and get user confirmation.

### 2. Prepare a neutral brief

Read the project to identify source files, not to tell the critics what to conclude. Normally include:

- `.writing/main.tex` and `.writing/manuscript/*.tex`;
- `.writing/findings.md`;
- `.writing/outline.md`;
- relevant `.writing/claims/section_*.md` files;
- target venue, page limit, and review objective.

Write `.writing/reviews/review-request.md` with paths and structural facts only. Exclude your summary, interpretations, recommendations, extracted findings, and leading questions. The exact allow-and-deny rules are in `references/cadence-and-independence.md`. A review *standard* is part of the output shape and may be included: name `references/review-taxonomy.md` among the files each critic reads, so weaknesses come back classified by dimension and pre-filtered by its leniency rules.

### 3. Run both reviewers concurrently

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/paired_consult.py" \
  --cd "<absolute project root>" \
  --handoff-kind venue-review \
  --PROMPT "Read <absolute path>/.writing/reviews/review-request.md and every source it names. Act as a senior <venue> reviewer. Produce a specific, evidence-linked review. Do not modify files."
```

Inspect `pair_status`: `complete` means both handoffs are available; `partial` means keep the successful lane and report the failed provider; `failed` means report both failures and stop. Do not replace a failure with a local model's invented opinion.

### 4. Request concrete deliverables

Run separate paired calls for the deliverables you need, using the prompt structures in `references/reviewer-deliverables.md`:

1. `venue-review` for Summary, Strengths, Weaknesses, Questions, Score, Confidence, and accept-lift conditions.
2. `results-claims-matrix` for outcome combinations and the claims each combination permits or rules out.
3. `experiment-plan` for one to four concrete experiments with datasets, baselines, scales, hyperparameters, ablations, metrics, budget, and priority.

Never let either provider invent a result that has not been measured. For a revision follow-up, reuse Codex's `SESSION_ID` and pass each provider only its own prior structured handoff:

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/paired_consult.py" \
  --cd "<absolute project root>" \
  --handoff-kind venue-review \
  --CODEX_SESSION_ID "<codex session>" \
  --CODEX_CONTEXT_FILE "<codex handoff json>" \
  --HERMES_CONTEXT_FILE "<hermes handoff json>" \
  --PROMPT "Read the revised source files and reassess the prior concerns. Do not modify files."
```

Hermes stays stateless. Its context file must restate its own prior handoff. Never cross the two files. Stop when the deliverables exist or the user decides no further round helps. Do not wait for the providers to agree.

### 5. Verify and present

Extract each provider's weaknesses into that provider's issue bundle (each critic is asked to append one as a JSON block; fall back to a faithful transcription if the block is missing, per `references/reviewer-deliverables.md`), then verify the quotes:

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/skills/review/scripts/verify_review_quotes.py" \
  .writing/reviews/issues-codex-<ISO-date>.json --source .writing/manuscript --write-back
python3 "${CLAUDE_PLUGIN_ROOT}/skills/review/scripts/verify_review_quotes.py" \
  .writing/reviews/issues-hermes-<ISO-date>.json --source .writing/manuscript --write-back
```

Then check each academic claim's identifier, locator, number, method, and statistical value against the source before reporting it. A structurally valid handoff is not factual verification, and a verified quote proves only that the words exist. Present in this fixed order:

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

Save `.writing/reviews/external-review-<ISO-date>.md` with separate `Codex view` and `Hermes view` sections. Preserve each provider's evidence, uncertainty, verification queue, and failure status. Add any requested matrix or experiment plan under provider-specific headings. If `.writing/progress.md` exists, append one row with the report path and `pair_status`. Do not record a single merged verdict.

---

## Re-review after revision (both modes)

After the user revises the manuscript, close the loop instead of reviewing from zero. This runs inside the multi-round exception in `references/cadence-and-independence.md`: each provider may see its own prior feedback, never the other's.

1. Re-run the same mode on the revised source. Codex may resume its `SESSION_ID`; Hermes receives only its own prior structured handoff. Attach each provider's own previous issues JSON to its context and ask it to reuse the old `root_cause_key` for any concern that persists and to mint new keys only for new problems. Stable keys are what make the diff line up.
2. Extract the fresh issue bundles and verify quotes as usual.
3. Diff old against new, once per provider, never across providers:

   ```bash
   python3 "${CLAUDE_PLUGIN_ROOT}/skills/review/scripts/diff_review_issues.py" \
     .writing/reviews/issues-codex-<old-date>.json .writing/reviews/issues-codex-<new-date>.json
   python3 "${CLAUDE_PLUGIN_ROOT}/skills/review/scripts/diff_review_issues.py" \
     .writing/reviews/issues-hermes-<old-date>.json .writing/reviews/issues-hermes-<new-date>.json
   ```

4. Present each provider's diff under its own heading with the four statuses as returned: `FULLY_ADDRESSED`, `PARTIALLY_ADDRESSED`, `NOT_ADDRESSED`, `NEW`. Do not reconcile the two diffs into one progress score.
5. `FULLY_ADDRESSED` means the provider no longer raises that root cause, not that the fix is proven correct. Spot-check the revised passages before reporting an issue closed.

---

## Key rules (both modes)

**One committed attack per lane (adversarial).** A list loses the strongest-objection signal.

**Fresh adjudication (adversarial).** No attack session continues into judgment.

**Two deterministic verdicts (adversarial).** The helper runs once per provider. No overall result exists.

**The critics read; the executor points (venue).** Pass primary paths and neutral constraints, not an interpretation.

**Provider isolation (both).** Codex sees only its own attack or brief. Hermes sees only its own. Never cross the two.

**Disagreement is evidence to inspect (both).** Reopen the disputed source. Do not settle it by voting.

**One lane may fail (both).** Keep the successful lane and report the other accurately. Never fabricate the missing one.

**The user decides (both).** Scores, verdicts, and experiment proposals never trigger an action automatically.

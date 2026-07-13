---
name: adversarial-review
description: Kill-argument review with two independent provider lanes. Each lane produces one committed strongest-rejection memo, then receives a fresh adjudication whose atomic rulings are mapped by a deterministic helper to its own advisory PASS, WARN, or FAIL. Use when a stable draft needs the single worst-case reviewer argument before submission or rebuttal.
---

# Adversarial Review

Run two independent attack and adjudication chains:

1. Codex attack, then fresh Codex adjudication, then Codex verdict.
2. Hermes attack, then fresh Hermes adjudication, then Hermes verdict.

Never cross attacks between providers. Never merge the two verdicts into an overall verdict. The user sees both and decides what to act on.

This skill is detect-only. It may write its review report and progress row. It never edits manuscript prose or claim state.

## Preconditions

1. Confirm `.writing/` and `.writing/manuscript/*.tex` exist.
2. Inventory the manuscript, bibliography, and compiled PDF when present.
3. Confirm the headline is stable. If title or abstract is still changing, defer the attack.
4. If the paper has neither theorem-class claims nor a scope, generality, or evidence-to-headline risk, recommend ordinary external review instead.
5. Before sending unpublished or sensitive files, list the exact files both services will receive and obtain user confirmation.

## Why this is a Type-B gate

Constructing and adjudicating the strongest rejection argument requires academic judgment. It cannot be self-graded. The only deterministic step is mapping atomic rulings to PASS, WARN, or FAIL with `scripts/compute_verdict.py`.

Follow `skills/_shared/core/dual-consult-protocol.md`. Both provider stages must be independent. The attack and adjudication stages must also be independent within each lane.

## Stage 1: paired attack

Use the attack prompt in `references/attack-and-verdict.md`. Send one neutral objective and the original paper paths to both providers. Do not include prior reviews, fix lists, summaries, or preferred objections.

Run in the background with a Bash timeout of at least `660000` ms:

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/paired_consult.py" \
  --cd "<absolute project root>" \
  --handoff-kind adversarial-attack \
  --PROMPT "Read the listed current paper files. Produce one strongest rejection argument of about 200 words with exact source locators. Do not consult prior reviews and do not modify files."
```

Each provider must commit to one argument rather than list weaknesses. Preserve the Codex attack and Hermes attack in separate JSON files. Do not show one provider the other's memo.

If one attack lane fails, the successful chain may continue and the report remains partial. Never fabricate the missing memo.

## Stage 2: paired but lane-specific adjudication

Start a fresh Codex session. Hermes is always a fresh oneshot call. The common objective tells each provider to adjudicate only the attack in its own context file. Pass no Codex `SESSION_ID` from the attack stage.

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/paired_consult.py" \
  --cd "<absolute project root>" \
  --handoff-kind adversarial-adjudication \
  --CODEX_CONTEXT_FILE "<codex attack handoff json>" \
  --HERMES_CONTEXT_FILE "<hermes attack handoff json>" \
  --PROMPT "Read the current paper files and adjudicate the attack supplied in your own provider context. Decompose it into 3 to 7 atomic points. Do not use the other provider's view. Do not output a top-level verdict or modify files."
```

Each point receives exactly one ruling:

- `answered_by_current_text`
- `partially`
- `unresolved`

A partial or unresolved point also records severity, whether a new experiment is required, and one recommended fix. Every academic assertion must cite a real source locator. Keep anything unverifiable in `verification_needed`.

## Stage 3: compute two verdicts

Extract each provider's `payload.points` to a separate JSON object and invoke the helper twice:

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/skills/adversarial-review/scripts/compute_verdict.py" < codex-points.json
python3 "${CLAUDE_PLUGIN_ROOT}/skills/adversarial-review/scripts/compute_verdict.py" < hermes-points.json
```

Do not hand-derive either verdict. The helper validates the 3 to 7 point requirement and maps rulings to one of:

- `PASS`, action `pass`;
- `WARN`, action `needs revision`;
- `FAIL`, action `needs revision` or `needs NEW experiment`.

A missing provider remains missing. Do not copy the other verdict across.

## Stage 4: verify and persist

Check every cited file, line, equation, table, number, and experiment against the manuscript. Structural validation does not prove the adjudication is factually correct.

Archive any prior `.writing/adversarial-review.md`, then write the new report:

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
<advisory only; identify which source passages need inspection or which experiment each lane requests>
```

Do not add an overall verdict, consensus, winner, or preferred provider. Disagreement is a reason to inspect the source, not to vote.

If `.writing/progress.md` exists, append one row with both provider verdicts and the report path. Do not edit the manuscript.

## Key rules

**One committed attack per lane.** A list loses the strongest-objection signal.

**Fresh adjudication.** No attack session continues into judgment.

**Provider isolation.** Codex sees only the Codex attack. Hermes sees only the Hermes attack.

**Two deterministic verdicts.** The helper runs once per provider. No overall result exists.

**Advisory only.** The user decides whether to revise, run an experiment, or reject either opinion.

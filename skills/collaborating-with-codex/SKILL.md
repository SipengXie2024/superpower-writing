---
name: collaborating-with-codex
description: This skill supports academic collaboration through Codex CLI. Use when the user asks to "ask Codex", "review my paper", "check the argument", "analyze results", "draft candidate prose", "design an experiment", or "generate a scientific figure". It handles evidence-linked consultation, authorized direct execution, multi-turn Codex sessions, and publication-quality scientific diagrams.
---

# Collaborating with Codex

Route every Codex call through `codex_bridge.py`. Use academic evidence and manuscript review as the default context. Retain direct execution only for an explicitly authorized task.

For any read-only academic consultation other than scientific figure generation, call Codex and Hermes together through `scripts/paired_consult.py`. Follow `skills/_shared/core/dual-consult-protocol.md`. Do not run Codex alone for a review, analysis, synthesis, draft, experiment plan, or second opinion.

Always launch the bridge or paired runner in the background. Use a Bash timeout of at least `660000` ms for paired consultation. Do not poll; wait for the completion notification.

## Choose the mode

### Paired consultation

Use paired consultation for:

- claim, evidence, method, statistics, novelty, or venue review;
- literature-search result synthesis;
- manuscript or rebuttal candidates;
- experiment, ablation, metric, and result-analysis proposals;
- adversarial review and independent second opinions.

Send one neutral brief to both providers:

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/paired_consult.py" \
  --cd "/absolute/workspace" \
  --handoff-kind venue-review \
  --PROMPT "Read paper.tex. Produce an evidence-linked mock venue review. Do not modify files."
```

Set `run_in_background: true` on the Bash call. Present `codex` and `hermes` separately. Do not vote, merge them into a consensus, or choose a winner for the user.

Before sending unpublished, confidential, restricted, personal, or otherwise sensitive material, name the exact files or excerpts that both external services will receive and obtain user confirmation.

### Direct execution

Call the Codex bridge directly only when Codex must perform an authorized write or when scientific figure generation needs Codex's image tool.

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/skills/collaborating-with-codex/scripts/codex_bridge.py" \
  --cd "/absolute/workspace" \
  --sandbox workspace-write \
  --PROMPT "Perform the approved task and report changed files and verification output."
```

Before a write-capable call, state what Codex may change and where. Get user approval. Assign only one external provider. Read the resulting files or diff and run the checks yourself. Codex's summary is a claim, not proof.

Direct mode defaults to `danger-full-access` for compatibility, so always pass the narrowest suitable `--sandbox` explicitly. Use `--yolo` only after explicit user authorization. The compatibility flag maps to Codex's current `--dangerously-bypass-approvals-and-sandbox` option.

## Structured academic handoff

The Codex bridge supports `--consult-handoff --handoff-kind KIND`, but normal academic consultation must enter through the paired runner. The available handoff kinds are:

- `general`
- `ideation`
- `novelty`
- `manuscript-draft`
- `venue-review`
- `results-claims-matrix`
- `experiment-plan`
- `adversarial-attack`
- `adversarial-adjudication`

Consultation forces `--sandbox read-only`. If that sandbox cannot start, let the Codex lane fail. Never retry with write access or bypass the sandbox.

The bridge saves Codex's complete response in a private temporary file and returns only a validated handoff. Do not open `artifact.raw_path` automatically. Verify every citation, identifier, locator, sample size, number, method, hyperparameter, and statistical claim against the original source.

## Codex sessions

Capture `SESSION_ID` from a successful call. Reuse it only when continuity is intended, such as a second review of the same revised manuscript or another iteration of the same figure.

For a paired follow-up, pass it only to Codex:

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/paired_consult.py" \
  --cd "/absolute/workspace" \
  --handoff-kind venue-review \
  --CODEX_SESSION_ID "session-id" \
  --CODEX_CONTEXT_FILE "/path/to/codex-handoff.json" \
  --HERMES_CONTEXT_FILE "/path/to/hermes-handoff.json" \
  --PROMPT "Reassess the revised manuscript against the same venue criteria."
```

Keep the two context files provider-specific. Never put Hermes's prior answer in Codex's context. Start a fresh Codex session when independence matters, including adversarial adjudication after an attack phase.

## Scientific figure exception

Scientific figure generation is the sole Codex-only consultation exception because Hermes has no equivalent image tool. Route it directly through this bridge and name Codex's `imagegen-scientific-schematics` skill.

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/skills/collaborating-with-codex/scripts/codex_bridge.py" \
  --cd "/absolute/workspace" \
  --sandbox workspace-write \
  --skip-git-repo-check \
  --PROMPT "Use your imagegen-scientific-schematics skill to create the specified publication figure. Preserve every exact label and arrow meaning. Save the selected PNG to .writing/figures/architecture.png and report the path."
```

Specify exact labels, layout, arrow semantics, colors, and output path. Confirm the image exists and inspect it after return. Reuse `SESSION_ID` for targeted revisions to the same figure.

## Supported direct options

| Option | Purpose |
|---|---|
| `--cd PATH` | Set the absolute workspace root |
| `--sandbox read-only\|workspace-write\|danger-full-access` | Set Codex file access; consultation forces `read-only` |
| `--SESSION_ID ID` | Resume a Codex conversation |
| `--skip-git-repo-check` | Allow a non-Git workspace when explicitly needed |
| `--return-all-messages` | Return event details in direct mode only |
| `--image PATH` | Attach one or more input images |
| `--model VALUE` | Pass a model only when the user explicitly specifies it |
| `--profile VALUE` | Pass a profile only when the user explicitly specifies it |
| `--yolo` | Bypass approvals and sandbox only with explicit authorization |

Do not pass `--return-all-messages` during structured consultation. Do not silently add `--skip-git-repo-check`, `--model`, or `--profile`.

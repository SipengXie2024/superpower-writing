---
name: collaborating-with-hermes
description: This skill supports academic collaboration through Hermes Agent CLI. Use when the user asks to "ask Hermes", "review my paper", "get a second opinion", "synthesize these studies", "check novelty", "analyze results", or "design experiments". It handles evidence-linked paired consultation, stateless follow-ups, workspace-change detection, and narrowly authorized direct execution.
---

# Collaborating with Hermes

Route every Hermes call through `hermes_bridge.py`. Never run bare `hermes` or `hermes chat`; the interactive interface blocks non-interactive shells.

For every read-only academic consultation, call Hermes and Codex together through `scripts/paired_consult.py`. Follow `skills/_shared/core/dual-consult-protocol.md`. Scientific figure generation remains Codex-only because Hermes has no equivalent image tool.

Always launch the bridge or paired runner in the background. Use a Bash timeout of at least `660000` ms for paired consultation or a direct Hermes call. Do not poll.

## Paired consultation

Use paired consultation for academic analysis, research synthesis, manuscript review, candidate prose, experiment planning, adversarial review, and second opinions.

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/paired_consult.py" \
  --cd "/absolute/workspace" \
  --handoff-kind general \
  --PROMPT "Read the named manuscript and sources. Assess claim C1 with exact evidence locators. Do not modify files."
```

Both providers receive the same neutral objective and source scope. Present the returned `codex` and `hermes` sections separately. Do not vote, merge them into a consensus, or choose a winner for the user. Preserve a successful lane if the other fails.

Before sending unpublished, confidential, restricted, personal, or otherwise sensitive material, name the exact files or excerpts that both external services will receive and obtain user confirmation.

## Hermes is not filesystem-isolated

Hermes `--cli -z` automatically allows its configured tools. A read-only prompt is not a filesystem sandbox. Consultation therefore applies three safeguards:

1. Add `--ignore-rules` automatically so project rules, memory, or preloaded skills do not redirect the review.
2. Tell Hermes to read only the named files and not modify, create, rename, or delete files.
3. Compare Git status, changed-file contents, and the current commit before and after the call.

If Hermes changes the worktree or creates a commit, the bridge returns `workspace_modified` and withholds the handoff. Report the change and stop. Never describe that call as read-only. Do not undo the change automatically.

## Stateless follow-ups

Hermes consultations are stateless oneshot calls. Do not pass `--resume`, `--continue`, or a fabricated `SESSION_ID`.

For a follow-up, provide:

- the original objective;
- the original file paths and allowed source scope;
- Hermes's own previous structured handoff;
- the new question.

Use `--HERMES_CONTEXT_FILE` on the paired runner. Never give Hermes Codex's prior answer or a private raw artifact. Use `--CODEX_CONTEXT_FILE` separately for Codex.

For an independence-sensitive stage, such as adjudicating an adversarial attack, start a fresh Hermes call and provide only Hermes's own attack handoff.

## Structured academic handoff

The bridge supports these handoff kinds:

- `general`
- `ideation`
- `novelty`
- `manuscript-draft`
- `venue-review`
- `results-claims-matrix`
- `experiment-plan`
- `adversarial-attack`
- `adversarial-adjudication`

A valid handoff confirms structure, not truth. Verify citations, DOI or arXiv identifiers, Zotero keys, file locators, sample sizes, methods, hyperparameters, numbers, and statistical claims against the original evidence. Keep unresolved facts in `[UNVERIFIED]` or `verification_needed`.

The complete Hermes answer is stored in a private temporary artifact. Do not open `artifact.raw_path` automatically. If the handoff is invalid, report the stable failure and preserve the artifact without exposing a preview or retrying merely to obtain freer text.

## Authorized direct execution

Omit `--consult-handoff` only when Hermes must execute an explicitly authorized task. Assign only one external provider so two processes cannot modify the same files.

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/skills/collaborating-with-hermes/scripts/hermes_bridge.py" \
  --cd "/absolute/workspace" \
  --worktree \
  --PROMPT "Perform the approved task, run the named checks, and report changed files."
```

Before dispatch, state which files Hermes may change and obtain user approval. Prefer `--worktree` for isolated execution. After return, inspect the diff and run the checks yourself. Hermes's statement that a task passed is not verification.

## Supported options

| Option | Purpose |
|---|---|
| `--cd PATH` | Set the workspace through subprocess `cwd` |
| `--consult-handoff` | Isolate the full answer and return a validated handoff |
| `--handoff-kind KIND` | Select the academic return format |
| `--worktree` | Ask Hermes to use an isolated Git worktree for authorized execution |
| `--ignore-rules` | Skip Hermes project rules and memory; consultation enables it automatically |
| `--toolsets VALUE` | Pass an explicit comma-separated toolset allowlist |
| `--skills VALUE` | Preload one Hermes skill when explicitly needed |

Do not expose Hermes session continuation flags. Do not pass a model or provider unless a future bridge version supports it and the user explicitly asks.

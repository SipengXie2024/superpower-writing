# Dual Academic Consultation Protocol

Use this shared protocol whenever an academic task asks an external model to analyze, review, synthesize, judge, or propose text without modifying files. It governs Codex and Hermes consultations across the plugin.

## 1. Classify the task before dispatch

Treat these as consultation:

- assess claims, evidence, novelty, methods, statistics, or venue fit;
- synthesize supplied literature or search results;
- produce an advisory manuscript draft or rebuttal candidate;
- propose experiments, ablations, metrics, or result interpretations;
- provide a second opinion or adversarial review.

Treat implementation, direct manuscript edits, file generation, and command execution as direct execution. Do not pair direct execution. Assign one authorized provider so two external processes cannot modify the same files.

Scientific figure generation is the sole single-provider consultation exception. Route it directly to Codex because Hermes has no equivalent image-generation tool.

## 2. Check what will leave the workspace

Public papers and materials explicitly identified by the user as public may be sent without another confirmation.

Before sending an unpublished manuscript, confidential review, restricted dataset, personal information, or other sensitive material, state exactly which files or excerpts will be sent to Codex and Hermes. Obtain user confirmation before dispatch. Approval for one file set does not cover later files.

Do not place secrets, credentials, private keys, access tokens, or raw personal records in either prompt.

## 3. Prepare one neutral brief

Give both providers the same:

- academic objective;
- venue or audience when relevant;
- exact files or source scope they may read;
- claim IDs, research question, or decision to assess;
- constraints and requested handoff kind;
- required evidence locators and verification limits.

Do not include the executor's conclusion, preferred verdict, or summary of what the critic should find. Let each provider read the original material. Do not send Codex's view to Hermes or Hermes's view to Codex.

Run the pair through:

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/paired_consult.py" \
  --cd "/absolute/workspace" \
  --handoff-kind general \
  --PROMPT "Read paper.tex and assess claim C1 against the reported evidence. Do not modify files."
```

Always launch this command in the background with a Bash timeout of at least `660000` ms. Do not poll. The runner starts both providers concurrently.

## 4. Preserve independent lanes

The paired result has exactly three main parts:

- `pair_status`: `complete`, `partial`, or `failed`;
- `codex`: Codex's independent result;
- `hermes`: Hermes's independent result.

Present the two views under separate headings. Preserve each provider's evidence, uncertainty, verification queue, and failure status. Do not add a combined summary, consensus, winner, vote, recommended provider, or overall verdict. The user decides what to accept.

If one provider fails, keep the successful result and report the failed lane accurately. Never fabricate a replacement response or make one provider speak for the other.

## 5. Handle follow-ups without crossing context

Codex may continue the same reviewer conversation with `SESSION_ID`. Pass it only through `--CODEX_SESSION_ID`.

Hermes consultations are stateless oneshot calls. Do not expose `--resume` or `--continue`. For a follow-up, restate the original objective, original file paths, Hermes's own prior structured handoff, and the new question.

Use `--CODEX_CONTEXT_FILE` only for Codex's prior structured context. Use `--HERMES_CONTEXT_FILE` only for Hermes's prior structured context. Never place a private raw artifact in either context file automatically.

For an independence-sensitive second stage, such as adversarial adjudication, start a fresh Codex session and a fresh Hermes call. Give each lane only its own attack output.

## 6. Verify evidence after return

A valid JSON handoff proves only that fields and references are structurally consistent. It does not prove that a citation, DOI, arXiv ID, PMID, page, number, method, or statistical result is true.

Before relying on a claim:

1. Open the original manuscript, Zotero item, paper, dataset, or project file.
2. Verify the identifier and exact locator.
3. Check that quoted numbers, sample sizes, settings, tests, and limitations match the source.
4. Keep contradictory evidence as contradictory. Do not turn disagreement into agreement by voting.
5. Move anything that cannot be checked into `[UNVERIFIED]` or `verification_needed`.

Do not open `artifact.raw_path` automatically. It contains the provider's complete answer and bypasses the structured isolation boundary. Open it only after the user explicitly asks and understands that consequence.

## 7. Respect provider-specific safety boundaries

Codex consultation always uses `--sandbox read-only`. If the sandbox cannot start, stop that lane. Never downgrade consultation to `workspace-write` or `danger-full-access`.

Hermes `--cli -z` automatically allows its configured tools and has no equivalent filesystem read-only sandbox. The bridge tells Hermes not to write, ignores project rules during consultation, and compares the workspace before and after the call. If any uncommitted change or commit appears, mark the lane failed with `workspace_modified`, report it, and stop. Do not describe that call as read-only.

For authorized direct execution, confirm the provider, target files, and write scope first. Use only one provider. Inspect its changes and run the relevant checks before reporting success.

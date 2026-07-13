# collaborating-with-codex

This Claude Code skill connects `superpower-writing` to Codex CLI for academic consultation, authorized execution, and publication figure generation.

## Academic consultation

Read-only academic consultation normally runs through both Codex and Hermes:

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/paired_consult.py" \
  --cd "/path/to/workspace" \
  --handoff-kind venue-review \
  --PROMPT "Read paper.tex and produce an evidence-linked mock review. Do not modify files."
```

The paired runner starts both providers concurrently and keeps their results separate. It does not vote, synthesize a consensus, or select a winner.

Codex consultation always uses its `read-only` sandbox. A failure to start that sandbox stops the Codex lane; the bridge never downgrades a consultation to write access.

The complete provider answer is saved in a private temporary artifact. Public bridge output contains only a validated academic handoff with evidence records, uncertainties, and items that still need verification.

## Direct Codex use

Use the bridge directly for explicitly authorized execution or scientific figure generation:

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/skills/collaborating-with-codex/scripts/codex_bridge.py" \
  --cd "/path/to/project" \
  --sandbox workspace-write \
  --PROMPT "Perform the approved task and report the changed files."
```

Direct mode preserves Codex `SESSION_ID`, image attachments, explicit model and profile flags, and full event output when requested. Direct mode defaults to `danger-full-access` for compatibility, so callers should always pass the narrowest appropriate sandbox explicitly.

`--yolo` remains a compatibility name. The bridge translates it to the current Codex CLI option `--dangerously-bypass-approvals-and-sandbox`. Use it only with explicit authorization.

`--skip-git-repo-check`, `--model`, and `--profile` are opt-in. The bridge does not add them silently.

## Scientific figures

Scientific figure generation is the only Codex-only consultation path because Hermes has no corresponding image tool. Name Codex's `imagegen-scientific-schematics` skill, specify exact labels and arrow meanings, and provide an in-workspace output path.

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/skills/collaborating-with-codex/scripts/codex_bridge.py" \
  --cd "/path/to/project" \
  --sandbox workspace-write \
  --PROMPT "Use your imagegen-scientific-schematics skill to create the specified publication diagram. Save the selected PNG to .writing/figures/architecture.png."
```

Reuse `SESSION_ID` for targeted revisions to the same figure. Confirm the output file exists and inspect it before use.

## Main options

| Option | Meaning |
|---|---|
| `--PROMPT` | Task instruction |
| `--cd` | Absolute workspace root |
| `--sandbox` | `read-only`, `workspace-write`, or `danger-full-access`; consultation forces `read-only` |
| `--SESSION_ID` | Resume a Codex session |
| `--consult-handoff` | Save full text privately and return a validated handoff |
| `--handoff-kind` | Select the academic return format |
| `--return-all-messages` | Return Codex events in direct mode |
| `--image` | Attach one or more images |
| `--model` | Pass a model only when explicitly requested |
| `--profile` | Pass a profile only when explicitly requested |
| `--skip-git-repo-check` | Permit a non-Git workspace when explicitly needed |

## Privacy boundary

Public papers may be sent for consultation. Before sending unpublished manuscripts, confidential reviews, restricted data, personal information, or other sensitive material, identify the exact files or excerpts and obtain user confirmation.

A structurally valid handoff is not evidence that its claims are true. Verify every source identifier, locator, number, method, and statistical result against the original source.

## License

MIT License. See [LICENSE](LICENSE) for the original vendored Codex skill attribution.

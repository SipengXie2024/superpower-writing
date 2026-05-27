---
name: collaborating-with-codex
description: Use when delegating coding work — prototyping, debugging, bug analysis, code quality feedback, executing implementation tasks, or generating publication-quality scientific figures and diagrams — to Codex CLI instead of a Claude subagent. Supports multi-turn sessions via SESSION_ID. Required by `superpower-planning:subagent-driven-codex` and `superpower-writing:scientific-schematics`.
---

> **MANDATORY: ALWAYS run codex_bridge.py in the background.**
> When invoking `codex_bridge.py` via the Bash tool, you MUST set `run_in_background: true`.
> Codex calls typically block for 60-120 seconds. Running them in the foreground freezes the
> entire conversation. Never omit this flag. No exceptions.
>
> **Sandbox policy:** `--sandbox read-only` is rejected at the argparse layer. When
> `--sandbox workspace-write` is requested, the bridge first probes bubblewrap by calling
> `bwrap --unshare-user --unshare-net --unshare-pid --ro-bind / / true` (result cached for
> 5 minutes at `/tmp/codex_bridge_bwrap_probe.<uid>`). If the probe fails — typically
> `bwrap: loopback: Failed RTM_NEWADDR: Operation not permitted` on Ubuntu 24.04+ with
> restricted unprivileged user namespaces, or in containers without `CAP_NET_ADMIN` — the
> bridge **auto-downgrades to `danger-full-access`** and writes a warning to stderr with the
> fix command (`sudo sysctl -w kernel.apparmor_restrict_unprivileged_userns=0`). Set
> `CODEX_BRIDGE_SKIP_BWRAP_PROBE=1` to bypass the probe when you know the host is fine. The
> default `danger-full-access` mode never runs the probe.

## Quick Start

```bash
python3 scripts/codex_bridge.py --cd "/path/to/project" --PROMPT "Your task"
```

**Inside any plugin that vendors this skill** (e.g. `superpower-planning`,
`superpower-writing`), the bridge script lives at
`${CLAUDE_PLUGIN_ROOT}/skills/collaborating-with-codex/scripts/codex_bridge.py`.
`${CLAUDE_PLUGIN_ROOT}` resolves to the loading plugin's own root, so the same
path works regardless of which plugin invokes it. Always use that absolute path
when calling the bridge from another skill in the same plugin.

**Output:** JSON with `success`, `SESSION_ID`, `agent_messages`, and optional `error`.

## Parameters

```
usage: codex_bridge.py [-h] --PROMPT PROMPT --cd CD [--sandbox {workspace-write,danger-full-access}] [--SESSION_ID SESSION_ID] [--skip-git-repo-check]
                       [--return-all-messages] [--image IMAGE] [--model MODEL] [--yolo] [--profile PROFILE]

Codex Bridge

options:
  -h, --help            show this help message and exit
  --PROMPT PROMPT       Instruction for the task to send to codex.
  --cd CD               Set the workspace root for codex before executing the task.
  --sandbox {workspace-write,danger-full-access}
                        Sandbox policy for model-generated commands. Defaults to `danger-full-access`. `read-only` is intentionally removed — see the Sandbox policy note above. `workspace-write` runs a bwrap preflight and silently downgrades to `danger-full-access` when bubblewrap cannot initialize on this host.
  --SESSION_ID SESSION_ID
                        Resume the specified session of the codex. Defaults to `None`, start a new session.
  --skip-git-repo-check
                        Allow codex running outside a Git repository (useful for one-off directories).
  --return-all-messages
                        Return all messages (e.g. reasoning, tool calls, etc.) from the codex session. Set to `False` by default, only the agent's final reply message is
                        returned.
  --image IMAGE         Attach one or more image files to the initial prompt. Separate multiple paths with commas or repeat the flag.
  --model MODEL         The model to use for the codex session. This parameter is strictly prohibited unless explicitly specified by the user.
  --yolo                Run every command without approvals or sandboxing. Only use when `sandbox` couldn't be applied.
  --profile PROFILE     Configuration profile name to load from `~/.codex/config.toml`. This parameter is strictly prohibited unless explicitly specified by the user.
```

## Multi-turn Sessions

**Always capture `SESSION_ID`** from the first response for follow-up:

```bash
# Initial task
python3 scripts/codex_bridge.py --cd "/project" --PROMPT "Analyze auth in login.py"

# Continue with SESSION_ID
python3 scripts/codex_bridge.py --cd "/project" --SESSION_ID "uuid-from-response" --PROMPT "Write unit tests for that"
```

## Common Patterns

**Prototyping (request diffs, do not apply):**
```bash
python3 scripts/codex_bridge.py --cd "/project" --PROMPT "Generate unified diff to add logging. Do not write the changes to disk."
```
Note: the sandbox still defaults to `danger-full-access`. Enforce read-only behavior through the prompt ("do not modify files", "return a diff only") rather than through `--sandbox`, because `read-only` is blocked.

**Debug with full trace:**
```bash
python3 scripts/codex_bridge.py --cd "/project" --PROMPT "Debug this error" --return-all-messages
```

## Image and Diagram Generation

Codex ships a built-in `image_gen` tool plus an `imagegen-scientific-schematics`
skill that wraps it in a figure-design and figure-review protocol. This is the
**preferred backend for publication-quality scientific figures** — architecture
diagrams, data-flow pipelines, model diagrams, conceptual schematics. Claude has
no native image tool, so this work must be delegated to Codex. (`superpower-writing`'s
`scientific-schematics` skill is the writing-side entry point and routes here; it
replaced the removed local `tools/image-generator` CLI.)

**Delegate a figure:**
```bash
python3 scripts/codex_bridge.py --cd "/path/to/project" --skip-git-repo-check \
  --PROMPT "Use your imagegen-scientific-schematics skill to generate <figure description>. \
  Spell every quoted label exactly. <arrow/zone/color semantics>. Clean white background, \
  no figure number. Save the final selected PNG to .writing/figures/<slug>.png and report \
  the absolute saved path."
```

Key points, all verified end-to-end through the bridge:

- **Name the skill in the prompt** (`Use your imagegen-scientific-schematics skill`).
  Codex loads it and follows its design/review protocol non-interactively.
- **Tell Codex where to save.** `image_gen` writes to `~/.codex/generated_images/<session>/`
  by default; Codex copies the selected image into the `--cd` workspace only when the
  prompt asks. Always give an explicit in-project output path, or the asset is stranded
  under `~/.codex/`.
- **Spell out exact labels and arrow semantics.** Raster generation can misspell dense
  or unusual labels. Quote literal labels and, for complex multi-view figures, include
  the `CRITICAL TEXT LOCK` / `CRITICAL ARROW CONTINUITY` / `CRITICAL CONSISTENCY` locks
  the skill documents.
- **Verify the file yourself.** After the bridge returns, confirm the PNG exists at the
  reported path and inspect it (Read the image) — Codex's summary states intent, not proof.
- **Iterate in the same session.** Reuse the returned `SESSION_ID` for targeted fixes
  ("the arrow from B to C is broken; regenerate with a single continuous polyline")
  instead of re-describing the whole figure.

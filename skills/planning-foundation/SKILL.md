---
name: planning-foundation
description: Use whenever a writing task will span more than 5 tool calls, multiple sessions, or risks hitting context-window limits, writing a paper, a long literature thread, a multi-section revision, anything where losing mid-task state would hurt. Creates a persistent `.writing/` directory that acts as working memory on disk, so the outline, claims, findings, and progress survive context resets. Every other superpower-writing skill assumes this directory exists; initialize it first. Trigger even when the user does not explicitly ask for "planning".
---

# Planning Foundation

`.writing/` is working memory on disk, the persistent state for the current paper. Context windows are volatile and limited; the filesystem is not. Anything important gets written to `.writing/` so it survives a context reset or a new session.

## Directory convention

```
.writing/                     # tracked in git; only caches, stashes, and LaTeX build output are ignored
├── metadata.yaml             # authors, venue, availability, writing_profile
├── outline.md                # IMRAD structure + key claims (from outlining)
├── ideation.md               # candidate directions + verdicts (from idea, optional)
├── claims/                   # one file per section: section_<NN>_<slug>.md (claim stubs)
├── manuscript/               # LaTeX prose: <NN>_<slug>.tex (from drafting)
├── figures/                  # <fig_id>.tex/.pdf, data/, src/, briefs
├── refs.bib                  # bibliography, fills as citations resolve
├── findings.md               # discoveries, decisions, rejected alternatives
├── progress.md               # Task Status Dashboard + session log
├── agents/                   # created on demand by subagents (one dir per role)
└── archive/                  # completed papers (dir per entry + summary.md)
```

The outline is the paper's design spec; there is no separate design/plan document. `agents/` is not created at init, each subagent makes its own subdir when dispatched.

## If the tools are missing

This skill needs Bash (to run `init-writing-dir.sh`) plus Write, Edit, and Read (to seed, update, and re-read `progress.md`, `findings.md`, `outline.md`). Check once, up front. If they are unavailable, one sentence naming what is missing is the entire budget, do not attempt a tool, fail, attempt another, and narrate each attempt.

Then carry the state in the reply instead of on disk: emit the Task Status Dashboard and the findings entries as fenced blocks, in the shape those files would have had, and add one line telling the user to save them at `.writing/progress.md` and `.writing/findings.md` since you could not write them yourself. Re-emit the updated blocks wherever a discipline below says to save; a directory you cannot create is not a reason to stop the task.

## Quick start

Before any complex writing task:

1. **Create `.writing/`**, run `bash "${CLAUDE_PLUGIN_ROOT}/scripts/init-writing-dir.sh"` (creates `.writing/` with `progress.md` + `findings.md` seeded from templates), or create the dir and seed the two files by hand.
2. **Re-read the outline before decisions**, keeps the paper's goals in the attention window.
3. **Update `progress.md` after each phase**, mark status, note files written, log errors.

## File purposes

| File | Holds | Update when |
|------|-------|-------------|
| `outline.md` | IMRAD structure + per-section key claims | After outlining or a restructure |
| `claims/section_*.md` | Claim stubs (CLAIM / EVIDENCE / STATUS) prose binds to | As evidence resolves during drafting |
| `findings.md` | Discoveries, decisions + rationale, rejected alternatives, constraints, debugging root causes | After any discovery or decision |
| `progress.md` | Task Status Dashboard, phase status, files written, errors, verification results | After any status change, action, or error |

## Core disciplines

### 1. Create `.writing/` first
Never start a complex writing task without it. All paper documents live here; execution status lives in `progress.md`'s Task Status Dashboard. Never use TaskCreate/TaskUpdate as cross-session memory, the Task API is session-scoped only.

### 2. The 2-action dispatch rule
After every ~2 read/search/explore operations, save to the right file by content type, discoveries and decisions to `findings.md`, status and actions and errors to `progress.md`. This keeps both knowledge and progress from being lost to a context reset.

### 3. Read before decide
Before a major decision, read the outline and relevant findings. This re-orients you when context is stale.

### 4. Log every error
Every error goes in `progress.md` (what failed, what you tried, what you observed). On repeated failure, escalate to the user rather than silently trying alternatives, the outline was designed deliberately, and self-directed workarounds bypass its intent.

## Per-agent directories

When dispatching subagents, each gets `.writing/agents/{role}/` with its own `findings.md` (discoveries) and `progress.md` (action log), appended across tasks, one dir per role, not per task. The orchestrator aggregates agent findings into the top-level `findings.md` / `progress.md` after each task (see `scripts/aggregate-agent-findings.sh`).

## When to use

Use for multi-step writing, research threads, and anything spanning many tool calls or sessions. Skip for simple questions, single-file edits, and quick lookups.

## The 5-question reboot test

If you can answer these from `.writing/`, your state management is solid: Where am I? (Task Dashboard) · Where am I going? (remaining phases) · What's the goal? (outline) · What have I learned? (findings.md) · What have I done? (progress.md).

## Scripts

At the plugin root, invoked as `bash "${CLAUDE_PLUGIN_ROOT}/scripts/<name>"`:

- `init-writing-dir.sh`, initialize `.writing/` with findings.md + progress.md
- `check-writing-state.sh`, report state: missing | empty | active | complete
- `writing-reset.sh`, reset active state, preserve `archive/`
- `snapshot-save.sh`, copy active files to a target dir (used by archiving)
- `aggregate-agent-findings.sh`, merge subagent findings into the top-level files
- `detect-base-branch.sh`, `detect-test-command.sh`, `unique-filename.sh`, project detection helpers

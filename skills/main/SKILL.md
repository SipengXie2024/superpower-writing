---
name: main
description: Router and dependency gate for superpower-writing. Loaded at session start. Verifies scientific-agent-skills is installed, routes between outlining/writing-plans/drafting/claim-verification/revision/submission based on stage in .writing/progress.md. Use when the user starts an academic-writing task (paper, manuscript, IMRAD draft, rebuttal).
---

<EXTREMELY-IMPORTANT>
If there is even a 1% chance a writing skill applies to your task, you MUST invoke it. No exceptions, no rationalizations.

This plugin is orchestration-only. All domain content (literature search, citation formatting, peer-review checklists, figure rendering) comes from the upstream `scientific-agent-skills` collection (K-Dense-AI). Upstream skills are invoked by **bare name** via the Skill tool — e.g. `Skill(skill="scientific-writing")`, **never** with a plugin prefix.
</EXTREMELY-IMPORTANT>

## Announce on Entry

When this skill is first invoked in a session, say exactly:

> "I'm using the superpower-writing main skill to route this task."

Then perform the dep check and `.writing/` detection below before doing anything else.

## How to Access Skills

**In Claude Code:** Use the `Skill` tool. When you invoke a skill, its content is loaded and presented to you — follow it directly. Never use the Read tool on skill files.

**Upstream vs local naming:**

- Local (this plugin): `Skill(skill="superpower-writing:drafting")` — prefixed.
- Upstream (Agent Skills standard): `Skill(skill="scientific-writing")` — bare, no prefix. These were installed via `npx skills add K-Dense-AI/scientific-agent-skills`, not as a Claude plugin.
- Local execution engines: `Skill(skill="superpower-writing:subagent-driven")`, `Skill(skill="superpower-writing:team-driven")`, `Skill(skill="superpower-writing:executing-plans")` — prefixed as normal. These ship with this plugin; no sibling-plugin dependency.

# Dependency Gate (HARD)

Before any routing, confirm dependencies. These are **hard gates, not advisory**.

## Step 1: Upstream Skills Check

Run:

```bash
${CLAUDE_PLUGIN_ROOT}/scripts/check-deps.sh
```

This probes standard Agent Skills install locations for: `scientific-writing`, `literature-review`, `peer-review`, `citation-management`, `research-lookup`, `scientific-schematics`.

**On non-zero exit:** refuse all subsequent superpower-writing skill invocations. Surface the install command verbatim to the user:

```
npx skills add K-Dense-AI/scientific-agent-skills
```

If `uv` is missing (required by upstream):

```
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Do not proceed to outlining / drafting / anything. Silent degradation produces unverified manuscripts.

## Step 2: Zotero Credentials Check (conditional)

If `.writing/metadata.yaml` exists and parses with `zotero.enabled: true`, **also** run:

```bash
${CLAUDE_PLUGIN_ROOT}/scripts/check-zotero.sh
```

This verifies `ZOTERO_API_KEY` and `ZOTERO_USER_ID`/`ZOTERO_GROUP_ID` are set (from `.env`) and that the Zotero API responds. **Hard-fail on non-zero exit** — do not fall back to network-only silently. If the user wants to disable Zotero, have them set `zotero.enabled: false` in `.writing/metadata.yaml`.

If `metadata.yaml` is absent or `zotero.enabled` is unset/false, skip this step.

## Step 3: `.writing/` Detection

Check for `.writing/` in the project root.

- **Absent and task is writing-related** (paper, manuscript, IMRAD, rebuttal, journal submission, revision, outline, abstract, methods section, etc.): run

  ```bash
  ${CLAUDE_PLUGIN_ROOT}/scripts/init-writing-dir.sh
  ```

  This creates `outline.md`, `findings.md`, `progress.md`, `metadata.yaml`, and subdirs `manuscript/ claims/ figures/ reviews/ archive/`.

- **Present:** read `.writing/progress.md` and `.writing/findings.md` to recover context before routing. Run `git diff --stat` to see manuscript changes since the last session.

- **Absent and task is not writing-related:** do nothing; yield to other skills.

# Session Recovery

When `.writing/` already exists at session start:

1. Read `.writing/progress.md` — Section/Figure dashboard shows current stage per section and which claims are stub vs evidence_ready vs verified.
2. Read `.writing/findings.md` — lit synthesis, prior decisions, reviewer context.
3. Read `.writing/metadata.yaml` — authors, preregistration, data/code availability, reporting guideline, Zotero config.
4. `git diff --stat -- .writing/` to see what changed since last session.
5. Update planning files with any newly recovered context, then route based on the stage below.

# Stage Gate Routing

The writing lifecycle from design.md §7:

```
(dep-check) -> outlining -> writing-plans -> drafting -> revision* -> submission
                                    ^                        |
                                    +--- loop on reviews ----+
```

Each stage writes a dashboard row to `.writing/progress.md`. Route by inspecting the dashboard:

| Current state in `.writing/progress.md` | Missing artifact | Next skill to invoke |
|------------------------------------------|------------------|----------------------|
| No dashboard yet, `outline.md` empty | outline + claims stubs | `superpower-writing:outlining` |
| Outline present, `metadata.yaml` still has TODOs | metadata completeness | `superpower-writing:outlining` (complete metadata before advancing) |
| Outline + metadata complete, no `plan.md` | per-section/figure plan | `superpower-writing:writing-plans` |
| `plan.md` present, `manuscript/*.md` empty or partial | prose | `superpower-writing:drafting` |
| Draft complete, no `verify-report.md` or report has failures | evidence audit | `superpower-writing:claim-verification` |
| Reviews present in `.writing/reviews/`, unaddressed | review response | `superpower-writing:revision` |
| All sections verified, metadata complete, no unresolved `[NEEDS-EVIDENCE]` or `<!-- draft-only -->` | submission gate | `superpower-writing:submission` |

Skipping a gate (e.g., jumping from outline directly to drafting without writing-plans) requires explicit user override, surfaced as a warning.

# Planning Approach Routing

When the user starts a non-trivial writing task (multi-section paper, multi-day project, significant structural decisions), do NOT auto-enter plan mode or auto-invoke brainstorming. Present the choice via `AskUserQuestion`:

**Option 1: Quick Plan (Plan Mode)** — Lightweight read-only exploration. Best for a medium-scope task with known IMRAD shape, quick alignment on scope before outlining.

**Option 2: Lightweight Execution** — Fast structured execution with `.writing/` tracking but no spec-interview or review loops. Best for short communications, commentaries, or a 2-3 section note where the claims are already clear.

**Option 3: Structured Brainstorming** — Full pipeline: `superpower-writing:brainstorming` (design doc) → `superpower-writing:spec-interview` (refinement) → `superpower-writing:outlining` (IMRAD structure + claims). Best for a new research manuscript, complex methods, multi-study papers, or when the narrative arc is still unclear.

**Option 4: Stash Current Work** — Pause an in-progress paper safely; move `.writing/` (except `archive/`) into `.writing/stash/<paper-name>/`. Best when switching to a different paper, awaiting co-author input, or waiting on external data.

**When to skip this choice:**
- Trivial edits (fix a typo, tweak one sentence) → just do it.
- User explicitly asks for one mode ("let's brainstorm", "/outline") → honor it.
- Already mid-brainstorm or mid-outline → continue the current flow.

**After Plan Mode completes:** If the approved plan reveals complex work (3+ sections, figures, multi-round lit review), suggest transitioning to `superpower-writing:writing-plans` for a formal decomposition plan. Plan-mode output feeds the plan — reference it, don't re-derive.

**When Lightweight Execution is chosen:** invoke `superpower-writing:lightweight-execute`. That skill handles `.writing/` init, checklist, implementation, and verification. For writing specifically, bolt on `superpower-writing:drafting` when prose writes begin (so the claim-first hook fires).

# Execution Routing

When the user says "execute the plan", "start drafting", "write the paper", "implement the sections", do NOT directly invoke a single execution skill. Instead:

1. If no plan exists at `.writing/plan.md`, invoke `superpower-writing:writing-plans` — it produces `.writing/plan.md` directly (no further delegation; the writing-domain skill now owns the planning mechanics).
2. If a plan exists, present the execution strategy via `AskUserQuestion`:

   - **Subagent-Driven (this session, sequential)** → `superpower-writing:subagent-driven`. One subagent per section, 2-stage review between sections. Best for short-to-medium papers where context load is manageable and you want tight quality control between sections.
   - **Team-Driven (this session, parallel)** → `superpower-writing:team-driven`. Agent Team with parallel section writers + dedicated reviewer. Best for long papers with many independent sections (Methods sub-blocks, multi-experiment Results) where time is the constraint.
   - **Parallel Session (separate session)** → `superpower-writing:executing-plans`. Batch execution with manual checkpoints in a fresh session. Best when you want human review between batches or will resume across days.

3. Recommend based on paper shape: high parallelism + heavy lit search per section → Team-Driven. Short note, tight prose control → Subagent-Driven. Multi-day timeline, manual checkpoints → Parallel Session.

Execution engines live locally under `superpower-writing:{subagent-driven,team-driven,executing-plans}`. Drafting subagents invoke `superpower-writing:drafting` as their per-task skill; the local execution engine handles subagent orchestration, team coordination, and session handoff.

# Stash / Resume Routing

- **Stash current paper:** when the user says pause / set aside / switch papers / come back later → move everything except `.writing/archive/` into `.writing/stash/<paper-name>/`. Use `superpower-writing:stashing` for the mechanics; the `<paper-name>` label should match `metadata.yaml` `title` (slugified) or the user-provided name.

- **Resume a stashed paper:** when the user says resume / continue / pick up <paper>, move `.writing/stash/<paper-name>/*` back into `.writing/` (keeping any existing `archive/`). Run a **stale-findings check** before routing further: re-read `findings.md`, cross-check DOIs in claims against current Zotero/network state, flag any citations that have been retracted or updated since stash.

- **Multi-paper concurrency:** only one active paper at a time in `.writing/`. Other papers live under `.writing/stash/`.

# Skills Inventory

Skills in this plugin (all invoked as `superpower-writing:<name>`):

| Skill | Purpose |
|-------|---------|
| `superpower-writing:main` | This router. Loaded at session start. Dep gate + stage routing. |
| `superpower-writing:outlining` | Idea → IMRAD outline + per-section claim stubs + populated `metadata.yaml`. Combines design-exploration and spec-writing. |
| `superpower-writing:writing-plans` | Approved outline → executable per-section/per-figure/per-table task plan with dependency graph. Writes `.writing/plan.md`. |
| `superpower-writing:drafting` | Section-by-section prose writing in serial or parallel mode. Enforces claim-first protocol: each section subagent resolves EVIDENCE via `research-lookup` / `citation-management` **before** writing tagged prose. |
| `superpower-writing:claim-verification` | Pre-submission auditor. Walks every `<!-- claim: id -->` tag, resolves DOIs (Zotero first, network fallback), runs semantic match against abstracts, checks numeric/table consistency, blocks on any `[NEEDS-EVIDENCE]` or `draft-only` marker. |
| `superpower-writing:revision` | Unified review-loop handler for internal co-author and external journal reviewer comments. Classify → respond → apply diff → re-verify. |
| `superpower-writing:submission` | Final gate: verifies all claims PASS, metadata complete, graphical abstract present, no draft-only tags. Freezes a copy to `.writing/archive/<date>/`. |

Upstream skills this plugin relies on (call by **bare name**, no prefix):

| Upstream skill | Used by | Purpose |
|----------------|---------|---------|
| `scientific-writing` | drafting, revision | Prose style, IMRAD conventions, graphical-abstract requirement. |
| `literature-review` | outlining, drafting, claim-verification | Structured lit synthesis. |
| `research-lookup` | drafting, claim-verification | Paper/abstract retrieval for evidence resolution. |
| `citation-management` | drafting, claim-verification, submission | Citation formatting, DOI resolution, bibliography assembly. |
| `peer-review` | claim-verification, revision | Reporting-guideline checklists (CONSORT / STROBE / PRISMA). |
| `scientific-schematics` | drafting | Graphical abstracts and schematic figures (mandatory per `scientific-writing`). |
| `pyzotero` | drafting, claim-verification, submission | All Zotero API calls when `zotero.enabled: true`. |

# Claim-First Protocol

Every load-bearing paragraph in `.writing/manuscript/*.md` must carry a marker:

- `<!-- claim: <id> -->` — links to an entry in `.writing/claims/section_<NN>_<slug>.md` with fields `id`, `CLAIM`, `EVIDENCE`, `STATUS` ∈ {`stub`, `evidence_ready`, `verified`}.
- `<!-- draft-only -->` — scratch prose that will be replaced before the next stage gate.

A **PreToolUse hook** (`${CLAUDE_PLUGIN_ROOT}/hooks/enforce-claims.sh`) blocks any Edit / Write / MultiEdit / NotebookEdit targeting `**/manuscript/*.md` when:

- a `<!-- claim: id -->` tag references a claim with `STATUS: stub`, or
- the claim file is missing, or
- untagged load-bearing prose lands in a protected section.

The hook exempts these section stems from paragraph-tag enforcement: `00_abstract`, `06_references`, `07_acknowledgments`. All other `manuscript/NN_*.md` files require every load-bearing paragraph to carry `<!-- claim: id -->` or `<!-- draft-only -->`.

Drafting and claim-verification skills must be aware of this hook and surface its block reason to the user. The fix is always: resolve EVIDENCE first (via `research-lookup` / `citation-management` / Zotero lookup), bump `STATUS` to `evidence_ready`, then write prose.

# User Instructions

Instructions say WHAT, not HOW. "Add a methods paragraph" or "tighten the abstract" doesn't mean skip workflows. Always:

1. Dep gate (check-deps + check-zotero when enabled).
2. `.writing/` recovery or init.
3. Stage-appropriate routing per the table above.
4. Upstream skills for domain content, local skills for orchestration.
5. Claim-first protocol enforced by the PreToolUse hook — don't try to bypass it.

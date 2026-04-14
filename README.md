# superpower-writing

**An IMRAD academic-writing lifecycle plugin for Claude Code.** Ports the
[superpower-planning](https://github.com/SipengXie2024/superpower-planning)
process skeleton — persistent state, stage gates, claim-first verification,
subagent execution, review loops — to research-paper drafting. Delegates all
domain content (IMRAD structure, reporting guidelines, citation management,
figure generation, literature lookup) to the upstream
[scientific-agent-skills](https://github.com/K-Dense-AI/scientific-agent-skills)
collection.

## Status

`v0.1.0` — scaffold. First-pass implementation of the 7 core skills and 2 hooks.
Single-author IMRAD only; multi-author and non-IMRAD formats deferred to v2.

## Prerequisites

This plugin has a **hard dependency** on scientific-agent-skills. If it is not
installed, every skill will refuse to run and surface the install command.

```bash
# 1. install uv (required by upstream scientific skills for Python deps)
curl -LsSf https://astral.sh/uv/install.sh | sh

# 2. install scientific-agent-skills (agentskills.io standard)
npx skills add K-Dense-AI/scientific-agent-skills
```

## Install

```bash
# from inside this repo
claude plugin marketplace add ./
claude plugin install superpower-writing
```

## Skill Inventory

| Skill | Purpose |
|-------|---------|
| `main` | Router + dependency gate. Routes by current stage in `.writing/progress.md`. |
| `outlining` | Brainstorm + IMRAD outline + claim-list generation in one chain. Produces `.writing/outline.md`, fills `.writing/metadata.yaml`. |
| `writing-plans` | Decomposes outline into per-section/figure/table tasks with dependency graph. |
| `drafting` | Orchestrates prose generation (serial or parallel). Enforces claim-first protocol. |
| `claim-verification` | Pre-submission verifier: DOI resolution, abstract semantic match, numeric consistency, reporting-guideline checklist. |
| `revision` | Unified review loop for internal co-authors and journal reviewers. |
| `submission` | Final gate + archive to `.writing/archive/<date>/`. |

## Architecture

See [`.planning/design.md`](./.planning/design.md) for the full design,
[`.planning/plan.md`](./.planning/plan.md) for the implementation plan, and
[`.planning/findings.md`](./.planning/findings.md) for accumulated decisions.

**Core novelty: claim-first writing protocol.** Every load-bearing paragraph in
`.writing/manuscript/*.md` must be tagged `<!-- claim: id -->` and bound to a
claim entry in `.writing/claims/section_*.md` whose `STATUS` is `evidence_ready`
or `verified`. A `PreToolUse` hook blocks Edit/Write on manuscript files that
reference stub-status claims. Early exploration uses `<!-- draft-only -->`; any
draft-only marker still present at submission time fails verification.

## Scope (v1 YAGNI)

**In scope:** single-author IMRAD research manuscripts, claim-first drafting,
citation verification via upstream `citation-management` / `research-lookup`,
reporting-guideline compliance (CONSORT/STROBE/PRISMA via upstream `peer-review`).

**Zotero (v1):** optional dual-source-of-truth citation backend. Activate via
`zotero.enabled: true` in `.writing/metadata.yaml`; supply credentials in
`.env` (see `.env.example` for `ZOTERO_API_KEY` plus `ZOTERO_USER_ID` or
`ZOTERO_GROUP_ID`). When enabled, drafting and claim-verification query
Zotero before falling back to network DOI resolution; with
`auto_push_new_citations: true`, network hits are pushed back to the
configured collection. When disabled, the pipeline runs network-only via
`citation-management` / `research-lookup`.

**Out of scope, deferred to v2:** multi-author collaboration in git,
Zotero annotation/notes round-trip, reviews / grants / theses,
non-IMRAD formats, venue-specific templating, auto-submission to
journal portals, LaTeX compile.

## License

MIT

# Changelog

All notable changes to this project are documented here.

Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/);
this project adheres to [Semantic Versioning](https://semver.org/).

## [0.1.1] — 2026-04-15

### Added
- `scripts/check-zotero.sh` now probes for the upstream `pyzotero` skill on
  disk before hitting `api.zotero.org`. Missing skill surfaces at SessionStart
  with an actionable install command instead of failing deep inside
  `drafting` or `claim-verification`.
- `scripts/check-deps.sh` verifies PyYAML via `python3 -c "import yaml"`. The
  `PreToolUse` hook requires it; the failure now shows up at session start,
  not at the first manuscript edit.

### Changed
- `skills/planning-foundation/templates/` moved to top-level `templates/`.
  `scripts/init-writing-dir.sh` `TEMPLATE_DIR` updated. The old location was
  a directory under `skills/` with no `SKILL.md`, which confused skill
  auto-discovery.
- README clarifies that paragraph-tag exemption is by **exact filename stem**:
  only `00_abstract.md`, `06_references.md`, and `07_acknowledgments.md`
  bypass enforcement. Variants such as `08_appendix.md` still require
  `<!-- claim: id -->` or `<!-- draft-only -->`.
- README smoke-test description now says "~35 PASS lines across 6 sections"
  (matching actual output), not the stale "26 checks".
- `commands/stash.md` no longer references `/writing:resume-stash (future)`;
  it now points users to the `superpower-writing:main` stash/resume routing.

### Security
- No secrets touched. `.env` and `.writing/secrets.local` remain gitignored;
  `.env.example` ships with empty values; `scripts/check-zotero.sh` still
  passes the API key via header only and discards the response body.

## [0.1.0] — 2026-04-14

Initial scaffold.

### Added
- Seven skills in `skills/`:
  - `main` — router + dependency gate (hard-fails on missing
    scientific-agent-skills; conditional hard-fail on missing Zotero
    credentials when `.writing/metadata.yaml` sets `zotero.enabled: true`).
  - `outlining` — IMRAD outline + claim-stub generation, `metadata.yaml`
    population, optional seeding from a Zotero collection.
  - `writing-plans` — decomposes outline into per-section / per-figure /
    per-table tasks with a dependency graph.
  - `drafting` — orchestrates prose generation in serial (subagent + 2-stage
    review) or parallel (Agent Team) mode, with claim-first evidence
    resolution before any prose is written.
  - `claim-verification` — four-pass verifier: claim completeness, citation
    resolution via Zotero-first dual source of truth, numeric/table
    consistency, reporting-guideline checklist.
  - `revision` — unified review-loop handler for internal co-author review
    and external journal reviewer comments.
  - `submission` — pre-submission freeze gate plus `.writing/archive/`
    snapshot and `refs.bib` generation from the Zotero collection ∩ cited
    DOIs.
- Seven slash commands in `commands/`: `outline`, `draft`, `revise`,
  `submit`, `check-deps`, `stash`, `archive`.
- Two hooks:
  - `SessionStart` → `hooks/check-deps.sh` (advisory, never blocks).
  - `PreToolUse` on `Edit|Write|MultiEdit|NotebookEdit` →
    `hooks/enforce-claims.sh` / `enforce-claims.py`. Blocks writes to
    `**/manuscript/*.md` that reference a claim with `STATUS: stub`, plus
    untagged prose in non-exempt sections. Bypass via `<!-- draft-only -->`
    (flagged at submission).
- Three shared scripts: `init-writing-dir.sh`, `check-deps.sh`,
  `check-zotero.sh`.
- `.writing/` layout with persistent outline, claims, manuscript, metadata,
  figures, reviews, archive, and optional stash.
- Zotero integration (v1): dual source of truth. When `zotero.enabled: true`,
  citation verification queries the Zotero library first and falls back to
  `research-lookup` / `citation-management` on miss. With
  `auto_push_new_citations: true`, network hits are pushed back to the
  configured collection.
- Agent-executable README with literal install commands, per-intent
  lifecycle routing, troubleshooting matrix.
- `tests/smoke.sh` — end-to-end smoke test with 35 PASS assertions across
  `.writing/` init, dep-check failure messaging, Zotero-creds failure
  messaging, five claim-enforcement scenarios, manifest JSON sanity, and
  file-presence audit.

### Known limitations (deferred to v2)
- Multi-author collaboration in git.
- Zotero annotation/notes round-trip.
- Non-IMRAD formats (reviews, grants, theses).
- Venue-specific templating.
- Auto-submission to journal portals.
- LaTeX compile.

[0.1.1]: https://github.com/SipengXie2024/superpower-writing/releases/tag/v0.1.1
[0.1.0]: https://github.com/SipengXie2024/superpower-writing/releases/tag/v0.1.0

# Changelog

All notable changes to this project are documented here.

Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/);
this project adheres to [Semantic Versioning](https://semver.org/).

## [0.4.0] — 2026-04-24

### Breaking

- Replaced the `pyzotero` skill dependency (upstream `scientific-agent-skills`) with the standalone `zotero-mcp-server` MCP server, registered via a plugin-level `.mcp.json`. Users must install the binary: `uv tool install "zotero-mcp-server[semantic,scite]"` (or `pipx install "zotero-mcp-server[semantic,scite]"`).
- Renamed Zotero environment variables to match zotero-mcp:
  - `ZOTERO_USER_ID` → `ZOTERO_LIBRARY_ID` (with `ZOTERO_LIBRARY_TYPE=user`)
  - `ZOTERO_GROUP_ID` → `ZOTERO_LIBRARY_ID` (with `ZOTERO_LIBRARY_TYPE=group`)
- Removed `ZOTERO_DEFAULT_COLLECTION` env var. Per-paper collection scoping continues via `.writing/metadata.yaml` `zotero.collection_key`.

### Fixed

- `README.md` install command and `.mcp.json` args were broken: the earlier instruction `uv tool install zotero-mcp` installed the old, archived PyPI package `zotero-mcp` (v0.1.6, only 3 tools) instead of the renamed-upstream `zotero-mcp-server` (v0.3.0, 20+ tools). `.mcp.json` also used top-level `--transport stdio` which the new subcommand-style CLI rejects; correct invocation is `["serve", "--transport", "stdio"]`. Without these fixes, every downstream Zotero tool call named by our skills would have resolved to "tool does not exist".

### Changed

- `scripts/check-zotero.sh` now validates the new env-var names, probes the Web API via curl, and confirms the `zotero-mcp` binary is on PATH. The upstream pyzotero-skill lookup is gone.
- All `Skill(skill="pyzotero")` call sites (in `agents/section-drafter.md`, `agents/citation-auditor.md`, `skills/drafting/`, `skills/outlining/`, `skills/claim-verification/`, `skills/revision/`, `skills/submission/`, `skills/writing-plans/`, `skills/main/`) now name MCP tools directly.
- `skills/submission/` BibTeX export is now a per-item loop: `zotero_get_collection_items` → `zotero_get_item_metadata(format="bibtex")`. Better BibTeX citekeys continue to flow through when installed on the user's Zotero.
- Skill and agent docs updated to expose the full `zotero-mcp-server` tool surface:
  - `zotero_semantic_search` added as a Zotero-side fallback in `skills/claim-verification/SKILL.md` Pass 2a (catches preprint-vs-publisher DOI mismatches by matching claim text against paper paragraphs) and in Pass 2c (parent-filtered search to surface the three most-relevant chunks before escalating to a 70K-char fulltext read). Same fallback mirrored into `agents/section-drafter.md` and `skills/revision/SKILL.md` for new-claim evidence resolution.
  - `zotero_get_item_fulltext` called out as a heavy operation to be narrowly-read, not loaded wholesale into context.
  - `skills/main/SKILL.md` and `skills/drafting/SKILL.md` tool inventories expanded to include semantic search, advanced search, and Scite citation intelligence (`scite_enrich_item`, `scite_check_retractions`).

### Migration

1. Install the MCP server: `uv tool install "zotero-mcp-server[semantic,scite]"`.
2. Update your `.env` to use `ZOTERO_LIBRARY_ID` + `ZOTERO_LIBRARY_TYPE` in place of `ZOTERO_USER_ID`/`ZOTERO_GROUP_ID`.
3. Export those vars in the shell that launches Claude Code (the plugin's `.mcp.json` passes them through to `zotero-mcp`).
4. Uninstall or stop depending on `scientific-agent-skills/pyzotero` if you no longer need it.

## [0.3.2] — 2026-04-23

### Added

- **Abstract is citation-free (enforced).** `hooks/enforce-claims.py` gains a
  new `CITATION_FREE_SLUGS = {"abstract"}` set matched by slug-ending against
  the manuscript file stem. Writes to any `*_abstract.tex` (e.g.
  `00_abstract.tex`) are blocked when the content contains any LaTeX citation
  command — matched by regex `\\[a-zA-Z]*cite[a-zA-Z]*\b`, which covers
  `\cite`, `\citep`, `\citet`, `\nocite`, `\parencite`, `\textcite`,
  `\autocite`, `\footcite`, `\citeauthor`, `\citeyear`, `\citealt`,
  `\citealp`, and any other `\*cite*` variant. A `% claim: id` tag in the
  abstract is also blocked since the abstract has no claims file. BPMRC
  structural tags (`% bpmrc: B`, `% bpmrc: P`, etc.) are unaffected —
  they are not citations or claim tags.
- `claim-verification` Pass 1 step 6 greps abstract files for citation
  commands and `% claim:` tags; any hit surfaces as a FAIL.
- `submission` checklist gains item 5b — abstract citation-free grep —
  duplicated from the hook so the gate catches files edited outside Claude.
- `tests/smoke.sh` gains five new LaTeX abstract cases (4j–4n): abstract
  `\cite{}` blocks, abstract `\citep{}` blocks, abstract `\parencite{}`
  blocks, abstract `% claim:` blocks, abstract with BPMRC tags but no
  citations allows.

### Changed

- `skills/main/SKILL.md` Claim-First Protocol gains a "Citation Placement
  Rule" section documenting the abstract-citation-free enforcement and the
  body-section citation requirement (`\cite{citekey}` resolvable against
  `.writing/refs.bib`).
- `skills/outlining/SKILL.md` filename-stem contract gains an "Abstract is
  citation-free (load-bearing)" paragraph clarifying that BPMRC structural
  tags survive the rule and that no `claims/section_00_abstract.md` file
  should be created.
- `skills/drafting/references/section-drafter-prompt.md` adds Step
  A-special for abstract drafting: skip Step A, do not emit any `\*cite*`
  command or `% claim:` tag, keep BPMRC structural tags.

### Migration notes

Existing manuscripts with `\cite{}` in the abstract will be blocked on the
next edit. Move those citations into the body sections that support the
claim (usually Introduction or Discussion) and rewrite the abstract as
plain prose.

## [0.3.0] — 2026-04-21

### Breaking Changes

- **Manuscript format migrated from Markdown to LaTeX.** All `.writing/manuscript/*.md` files are now `.writing/manuscript/*.tex`. The claim-first `PreToolUse` hook matches `**/manuscript/*.tex` only; markdown manuscripts under `manuscript/` pass through unenforced. A SessionStart recovery check warns users who accidentally create `.md` files in `manuscript/`.
- **Claim and draft tags changed to LaTeX line comments at column 0.** `<!-- claim: id -->` → `% claim: id`; `<!-- draft-only -->` → `% draft-only`. Same for every structural tag (`% bpmrc: B`, `% cars: T`, `% background: D`, etc.).
- **Citations use `\cite{citekey}` exclusively.** The old `<!-- cite: doi -->` and `[@doi:...]` inline forms are removed. Citekeys are sourced from the configured Zotero collection at drafting time.
- **`submission` skill requires `zotero.enabled: true`.** The legacy "scrape DOIs from markdown, fetch intersection from Zotero" flow is replaced with a Zotero-collection-to-`refs.bib` export, followed by verification that every `\cite{}` key in the manuscript is covered. Zotero-disabled mode now aborts at the submission gate.
- **Hook's `UNPROTECTED_STEMS` → `UNPROTECTED_SLUGS` (slug-ending match).** Any stem ending in `_abstract`, `_references`, or `_acknowledgments` is exempt — so `00_abstract.tex`, `09_references.tex`, `10_acknowledgments.tex` all work regardless of numeric prefix.

### Added

- **Section-standards framework** under `skills/drafting/references/section-standards/` with 9 canonical "八股" files (BPMRC / CARS / DNPL / OFCA / RSRT / ILFS / RSF / ThematicGroup / SFR) plus a README. Files use a uniform `NN_slug.md` naming convention. Each standards file specifies Framework / Role-of-each-element / Outline-bullet-requirement / Draft-requirement / Style-rules / Common-failure-modes for one section.
  - `00_abstract.md` (BPMRC): Background-Problem-Method-Result-Conclusion, 5 bullets fixed.
  - `01_introduction.md` (CARS): Swales Territory-Niche-Occupy 3-move model, 4–7 bullets.
  - `02_background.md` (DNPL): Domain-Notation-Prior-Limitation, 4–6 bullets.
  - `03_methods.md` (OFCA+I): Overview-Formalization-Core-Analysis with optional Implementation, 4–10 bullets.
  - `04_results.md` (RSRT): Research-Questions-Setup-Per-RQ-Results-Takeaways, 7–15 bullets, RQ-R 1-to-1 correspondence.
  - `05_discussion.md` (ILFS): Interpretation-Limitations-Future-Significance, 4–8 bullets.
  - `06_conclusion.md` (RSF): Restate-Summary-Forward-look, exactly 3 bullets, ≤250 words.
  - `07_related_work.md` (ThematicGroup): thematic clustering with per-group contrast sentence, 2–4 bullets.
  - `08_motivation.md` (SFR, opt-in): Scenario-Failure-Requirements, 3–6 bullets; explicit opt-in gate for systems/architecture/security venues.
- **Two-level fallback match rule (slug-ending scan).** Orchestrator resolves a manuscript stem to its standards file by exact `NN_slug.md` match, falling back to `*_slug.md` scan over `section-standards/`. Supports flexible positioning: Background at §2 or §3, Related Work §2 or late, Motivation opt-in §2.
- **`{SECTION_STANDARD}` placeholder in `section-drafter-prompt.md`.** Orchestrator inlines the matched standards file verbatim into the per-section subagent prompt. Standards impose structural tags, paragraph counts, ordering, and length budgets; drafter self-review greps for conformance in Step C.
- **Cross-section coordination rules.** When `§Motivation` is opted in, `§Introduction` compresses CARS M2 `[N]` bullets to exactly 1 to avoid duplication. When `§Conclusion` merges into `§Discussion`, RSF `[F]` is dropped to avoid duplicating ILFS `[F]`. Both are enforced in `outlining` Step 7 self-review.
- **`init-writing-dir.sh` generates a LaTeX skeleton**: `main.tex` (generic `\documentclass{article}` + standard preamble with `amsmath` / `graphicx` / `booktabs` / `algorithm` / `hyperref` / `natbib`), empty `refs.bib`, and `.gitignore` entries for LaTeX build artifacts (`*.aux` / `*.log` / `*.bbl` / `*.blg` / `*.pdf` / etc).
- **`latexmk` compile gate in submission.** New checklist item 6 runs `latexmk -pdf -interaction=nonstopmode main.tex` and greps `main.log` for undefined references / undefined control sequences. Graceful skip with warning when `latexmk` / `pdflatex` is not installed.

### Changed

- **`hooks/enforce-claims.py` rewritten for LaTeX.** Matcher switched from `*.md` to `*.tex`; comment regex from `<!-- claim: id -->` to `^\s*%\s*claim:\s*(\S+)`; new `STRUCTURAL_LATEX_CMDS` whitelist (`\section`, `\subsection`, `\begin`, `\end`, `\label`, `\caption`, etc.) so structural LaTeX lines don't count as load-bearing prose.
- **`outlining` Step 3 bullet-count table extended to 12 rows** (CS and medical variants split for Methods / Results / Discussion / Conclusion; Background / Motivation / Related Work added as CS-specific).
- **`outlining` Step 7 self-review has 9 new grep rules**, one per section standard: BPMRC 5-bullet check, CARS T→N→O strict ordering, DNPL D→N→P→L, OFCA O+C required, RSRT `[RQ]` count == `[R]` count, ILFS I→L→F→S, RSF exactly 3 bullets, ThematicGroup differentiator-clause check, SFR S→F→R with exactly one Scenario.
- **`submission` skill's refs.bib generation** replaced with a `pyzotero` collection export step that covers every `\cite{}` citekey in the manuscript; multiple-match or missing-citekey failures surface by file:line.
- **Smoke test suite extended** to 9 claim-enforcement cases (LaTeX paths, `% claim` tag, `% draft-only`, untagged-prose block, `.md` bypass, `_abstract` unprotected, `_references` slug-ending unprotected, LaTeX structural line allow, non-manuscript allow) plus section-standards presence check.

## [0.2.0] — 2026-04-15

### Breaking Changes

- **No longer depends on the `superpower-planning` plugin at runtime.** Users upgrading from v0.1.x should remove the `superpower-planning` entry from their plugin list (optional — installing it alongside v0.2.0 is harmless but unnecessary).

### Added

- Inlined 12 execution/planning skills under `superpower-writing:*` (planning-foundation, brainstorming, spec-interview, lightweight-execute, subagent-driven, team-driven, executing-plans, stashing, archiving, verification, finishing-branch, git-worktrees).
- Inlined 11 supporting scripts under `scripts/`.
- New writing-domain `spec-reviewer` agent checking outline compliance.
- Extended `manuscript-reviewer` with AI-trace detection (over-parallelism, formulaic connectors, em-dash overuse, uniform sentence length, hedging cliché, throat-clearing, bulleted-list abuse, mirror-balancing).

### Changed

- `.planning/` references throughout ported content rewritten to `.writing/`.
- `writing-plans` merged into a single skill; wrapper layer removed.
- `session-start` hook no longer checks for superpower-planning; only Zotero check remains.

## [0.1.2] — 2026-04-15

### Added
- Four writing-specific subagents in `agents/`:
  - `section-drafter` — IMRAD-aware implementer. Resolves evidence (Zotero first,
    network fallback) before writing any tagged paragraph; obeys the claim-first
    PreToolUse hook. Used by `drafting` skill in serial and parallel modes.
  - `manuscript-reviewer` — writing-quality reviewer. Checks IMRAD coherence,
    voice/tense discipline, hedging calibration, claim-to-evidence distance,
    clarity. Stays out of mechanical citation and reporting-guideline lanes.
  - `citation-auditor` — optional deep pass inside `claim-verification`. Flags
    over-citation, under-citation, circular/self-citation, staleness,
    relevance drift, and seminal-work omissions.
  - `rebuttal-auditor` — final gate inside `revision`. Audits the
    reviewer-response letter for per-item completeness, tone calibration,
    false concessions, classification sanity, and consistency with the
    manuscript diff.

### Changed
- `skills/drafting/SKILL.md` now names `section-drafter` (implementer) and
  `manuscript-reviewer` (quality reviewer) as the subagent types dispatched by
  the underlying `superpower-planning:subagent-driven` / `team-driven` engines.
  `superpower-planning:spec-reviewer` remains for plan alignment.
- `skills/claim-verification/SKILL.md` adds an optional §2e "deep pass" that
  dispatches `citation-auditor` on request.
- `skills/revision/SKILL.md` Step 5 now gates external-review rounds on
  `rebuttal-auditor` passing; Critical findings block round closure.
- `tests/smoke.sh` audits the four new agent files.

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

[0.3.2]: https://github.com/SipengXie2024/superpower-writing/releases/tag/v0.3.2
[0.3.1]: https://github.com/SipengXie2024/superpower-writing/releases/tag/v0.3.1
[0.3.0]: https://github.com/SipengXie2024/superpower-writing/releases/tag/v0.3.0
[0.2.0]: https://github.com/SipengXie2024/superpower-writing/releases/tag/v0.2.0
[0.1.2]: https://github.com/SipengXie2024/superpower-writing/releases/tag/v0.1.2
[0.1.1]: https://github.com/SipengXie2024/superpower-writing/releases/tag/v0.1.1
[0.1.0]: https://github.com/SipengXie2024/superpower-writing/releases/tag/v0.1.0

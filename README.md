# superpower-writing

> Standalone Claude Code plugin for scientific manuscript writing. Includes its
> own execution engines ported and adapted from superpower-planning in v0.2.0.
> Delegates all domain content (IMRAD structure, reporting guidelines, citation
> management, figure generation, literature lookup) to the upstream
> [scientific-agent-skills](https://github.com/K-Dense-AI/scientific-agent-skills)
> collection.

<!-- This README is written to be agent-executable. Every install step, every
     check, and every troubleshooting recipe is a literal command you can run
     verbatim. Expected outputs are shown under each command. -->

## Status

- **Version**: `v0.4.0`
- **Scope**: single-author IMRAD research manuscripts
- **Dependencies**: scientific-agent-skills (hard), Zotero API (optional)
- **Repo**: https://github.com/SipengXie2024/superpower-writing

## TL;DR — what this plugin does

1. Persists your paper state in `.writing/` (outline, claims, manuscript, metadata, reviews, archive).
2. Forces **claim-first writing**: every load-bearing paragraph in `manuscript/NN_*.md` must carry `<!-- claim: id -->` bound to a claim with `STATUS: evidence_ready` (or `<!-- draft-only -->` for exploration). A `PreToolUse` hook hard-blocks writes that violate this.
3. Resolves citations **Zotero first → network fallback** (when Zotero is enabled). Pushes new DOIs back to your library if configured.
4. Gates submission: claim-verification must pass, `metadata.yaml` complete, graphical abstract present, zero `draft-only` or `[NEEDS-EVIDENCE]` remaining.

## Agent install checklist

Run these in order. Each command prints what it did; compare to "Expected".

### 0. Check prerequisites

```bash
which claude && claude --version      # needs Claude Code CLI
which uv || curl -LsSf https://astral.sh/uv/install.sh | sh   # upstream skills need uv
which gh && gh auth status             # needed only if you want to push
python3 -c "import yaml"               # hook uses PyYAML
```

Expected: no command fails. If `python3 -c "import yaml"` errors, run `pip install --user pyyaml`.

### 1. Install upstream scientific-agent-skills (hard dependency)

```bash
npx skills add K-Dense-AI/scientific-agent-skills
```

Expected: finishes without error. The plugin's `check-deps.sh` will now find `scientific-writing`, `literature-review`, `peer-review`, `citation-management`, `research-lookup`, `scientific-schematics` on disk.

### 2. Install this plugin

```bash
claude plugin marketplace add /absolute/path/to/superpower-writing
claude plugin install superpower-writing
```

Or clone first:

```bash
git clone https://github.com/SipengXie2024/superpower-writing.git ~/superpower-writing
claude plugin marketplace add ~/superpower-writing
claude plugin install superpower-writing
```

Expected: `claude plugin list` shows `superpower-writing` as installed.

### 3. Verify the install

```bash
cd /path/to/superpower-writing
bash scripts/check-deps.sh
```

Expected (success): `[superpower-writing] deps OK (found at: <root>)`.

If FAIL, the script prints a fix recipe including the exact `npx` command and the 7 candidate skill roots it searched. Follow it and re-run.

### 4. (Optional) Enable Zotero integration

Zotero turns on **dual source of truth**: citations are resolved from your Zotero library first, then fall back to network lookup via `research-lookup` / `citation-management`. When `auto_push_new_citations: true`, new DOIs discovered via network are pushed back to your configured collection.

- Install the `zotero-mcp-server` MCP server: `uv tool install "zotero-mcp-server[semantic,scite]"` (or `pipx install "zotero-mcp-server[semantic,scite]"`). The `[semantic]` extra enables AI-powered similarity search across your library; `[scite]` adds citation-intelligence tallies and retraction alerts. The `zotero-mcp` binary installed by this package is what `.mcp.json` spawns over stdio at session start. (Note: on PyPI the package was renamed from `zotero-mcp` to `zotero-mcp-server`; the old `zotero-mcp` package is v0.1.6 and ships only 3 tools — make sure you install the new name.)

```bash
cp .env.example .env
# edit .env: set ZOTERO_API_KEY, ZOTERO_LIBRARY_ID, ZOTERO_LIBRARY_TYPE (user|group)
# get the key at https://www.zotero.org/settings/keys
# find your library ID by hitting https://api.zotero.org/keys/<KEY>

# export the three vars in the shell that launches Claude Code, so .mcp.json
# can pass them through to zotero-mcp:
export ZOTERO_API_KEY=...  ZOTERO_LIBRARY_ID=...  ZOTERO_LIBRARY_TYPE=user

bash scripts/check-zotero.sh
```

Expected: `[superpower-writing] Zotero OK (users/<id>)` or `(groups/<id>)`.

Then in your paper's `.writing/metadata.yaml`:

```yaml
zotero:
  enabled: true
  collection_key: ABC123         # the 8-char key of a per-paper collection
  auto_push_new_citations: true
```

`scripts/check-zotero.sh` is idempotent; it never echoes the API key (header-only, body discarded).

### 5. Run the smoke test

```bash
bash tests/smoke.sh
```

Expected final line: `ALL SMOKE TESTS PASSED`. The test emits ~35 PASS lines across six sections: `.writing/` init, dep-check failure messaging, Zotero-creds failure messaging, five claim-enforcement cases (stub blocks, evidence_ready allows, draft-only allows, untagged blocks, non-manuscript allows), manifest JSON sanity (plugin.json / marketplace.json / hooks.json), and file-presence audit (7 skills + 7 commands + 4 hook files).

## Agent usage — lifecycle by user intent

Each row is keyed to what the **user** says. The **agent** picks the slash command.

| User intent                                  | Slash command              | What happens                                                                                                                                               |
|----------------------------------------------|----------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------|
| "Let's start a new paper on X"               | `/writing:outline X`       | Runs `outlining` skill. Initializes `.writing/`, seeds IMRAD outline, creates `claims/section_NN_*.md` stubs, fills `metadata.yaml`.                     |
| "Draft the methods section"                  | `/writing:draft methods`   | Runs `drafting`. Subagent resolves EVIDENCE per claim (Zotero-first), advances STATUS to `evidence_ready`, only then writes tagged prose.               |
| "Draft everything in parallel"               | `/writing:draft all`       | Same, in `team-driven` mode: one subagent per section.                                                                                                    |
| "Here are reviewer comments" (paste or path) | `/writing:revise <path>`   | Runs `revision`. Intake → classify Major/Minor/OutOfScope/Factually-wrong → per-item response → diff → re-verify.                                         |
| "Ready to submit"                            | `/writing:submit`          | Runs `submission`. Freeze gate (claim-verification PASS, metadata complete, graphical abstract present, zero draft-only/NEEDS-EVIDENCE), then archives.  |
| "Check dependencies"                         | `/writing:check-deps`      | Runs `scripts/check-deps.sh`. If `zotero.enabled`, also `check-zotero.sh`.                                                                                 |
| "Pause this paper, I need to switch"         | `/writing:stash <name>`    | Moves `.writing/` into `.writing/stash/<name>/`. Ready for a fresh paper.                                                                                 |
| "Archive the current state"                  | `/writing:archive`         | Snapshots `.writing/` into `.writing/archive/<timestamp>/`.                                                                                               |

## Stage gates

```
(dep-check) → outlining → writing-plans → drafting → [revision]* → submission
                                    ↑                       │
                                    └─── loop per review ───┘
```

Each gate updates `.writing/progress.md` Task Dashboard. Skipping requires explicit user override.

## The claim-first protocol (v1 core invariant)

Every paragraph in `.writing/manuscript/NN_<slug>.tex` is tagged with a LaTeX line comment at column 0:

```latex
% claim: meth-c1
We enrolled 1,247 patients with T2D from NHANES cycles 2018--2023...
```

Or escapes enforcement for early exploration:

```latex
% draft-only
Rough notes about what this section might say.
```

The hook `hooks/enforce-claims.sh` runs on every `Edit`/`Write`/`MultiEdit` targeting `**/manuscript/*.tex` and refuses the write if any `% claim: id` references a claim whose `STATUS` is not `evidence_ready` or `verified`. **Exemption is by slug-ending** — any file whose stem ends in `_abstract`, `_references`, or `_acknowledgments` bypasses paragraph-tag enforcement (so `00_abstract.tex`, `09_references.tex`, `10_acknowledgments.tex` all work). Any other stem (including new additions like `11_appendix.tex`) must tag every load-bearing paragraph. `.md` files under `manuscript/` are not intercepted — the plugin operates on LaTeX only.

Any `% draft-only` marker still present when `/writing:submit` runs is a hard failure.

## Zotero dual-source-of-truth (v1)

When `zotero.enabled: true`, citation resolution is two-phase:

1. **Zotero** via the `zotero-mcp` MCP server — query by DOI with `zotero_search_items`, fall back to `zotero_semantic_search` (paragraph-level similarity over PDF fulltext when indexed) when DOI match fails. Retrieve with `zotero_get_item_metadata` (markdown / BibTeX) or `zotero_get_item_fulltext` when a specific passage must be read. Hit = authoritative (you've vetted it).
2. **Network fallback** via `Skill(skill="citation-management")` / `Skill(skill="research-lookup")`. On hit, record `source: network` in the claim's EVIDENCE; if `auto_push_new_citations: true`, push to the configured Zotero collection and update `source: both`.

Fail only if both sources miss.

When `zotero.enabled: false` (default), the pipeline runs network-only.

## `.writing/` layout

```
.writing/
  outline.md                # IMRAD + per-section claim lists
  findings.md               # research synthesis, decisions, reviewer context
  progress.md               # Task Status Dashboard
  metadata.yaml             # authors + preregistration + data/code availability + reporting guideline + zotero block
  manuscript/
    00_abstract.md          # exempt from claim enforcement
    01_introduction.md
    02_methods.md
    03_results.md
    04_discussion.md
    05_conclusion.md
    06_references.md        # exempt
    07_acknowledgments.md   # exempt (optional)
  claims/
    section_<NN>_<slug>.md  # YAML list of {id, CLAIM, EVIDENCE[], STATUS}
  figures/                  # via scientific-schematics
    graphical_abstract.png  # mandatory per scientific-writing
  reviews/
    internal_<date>.md
    journal_<round>.md
  archive/                  # post-submission frozen snapshots
  stash/<paper-name>/       # when you multiplex papers
  verify-report.md          # produced by claim-verification
  verify-cache.json         # DOI → {source, resolved_at} (gitignored)
```

## Troubleshooting recipes

| Symptom                                         | Diagnostic                                                      | Fix                                                                                  |
|-------------------------------------------------|-----------------------------------------------------------------|--------------------------------------------------------------------------------------|
| `check-deps.sh` fails                           | check message; names missing skill(s)                           | `npx skills add K-Dense-AI/scientific-agent-skills`                                  |
| `check-zotero.sh` exits 1 "API key not set"     | `.env` missing or incomplete                                    | `cp .env.example .env` then fill in the two required fields                          |
| `check-zotero.sh` HTTP 403                      | key lacks required scope                                        | regenerate at zotero.org/settings/keys with read+write on the library                |
| `check-zotero.sh` HTTP 404                      | wrong `ZOTERO_LIBRARY_ID` or `ZOTERO_LIBRARY_TYPE`              | `curl -sS https://api.zotero.org/keys/<YOUR_KEY>` → read `userID` field (use that as `ZOTERO_LIBRARY_ID` with `ZOTERO_LIBRARY_TYPE=user`) |
| Hook blocks a legitimate write                  | claim referenced but no such `id` in `claims/section_...md`     | Add the claim entry and set `STATUS: evidence_ready` after evidence is resolved      |
| Hook blocks an exploratory paragraph            | untagged prose in a protected section                           | Either tag `<!-- draft-only -->` or write a proper `claim` entry                     |
| `smoke.sh` fails                                | read the specific `FAIL: ...` line                              | Each check is independent; fix what's listed                                         |

## Layout

```
.claude-plugin/
  plugin.json
  marketplace.json
hooks/
  hooks.json             # PreToolUse enforce-claims + SessionStart check-deps
  enforce-claims.{sh,py} # claim-first enforcer
  check-deps.sh          # SessionStart wrapper
agents/
  section-drafter.md     # implementer: IMRAD-aware drafter with claim-first + Zotero-first evidence resolution
  manuscript-reviewer.md # reviewer: scientific writing quality (IMRAD coherence, voice, hedging, clarity, AI-trace detection)
  spec-reviewer.md       # reviewer: outline compliance — claims present/absent/reordered vs the plan (v0.2.0)
  citation-auditor.md    # reviewer: over/under/circular/stale citation; optional deep pass in claim-verification
  rebuttal-auditor.md    # reviewer: reviewer-response letter completeness + tone + diff consistency
scripts/
  init-writing-dir.sh    # bootstraps .writing/
  check-deps.sh          # 7-root probe for upstream skills
  check-zotero.sh        # Zotero API auth probe (never echoes key)
commands/                # /writing:outline /writing:draft /writing:revise /writing:submit /writing:check-deps /writing:stash /writing:archive
skills/                  # 7 writing-domain + 12 execution/planning = 19 skills total
  main/                  # router + dep gate (authoritative Claim-First Protocol section)
  outlining/             # IMRAD outline + claim stubs + metadata.yaml
  writing-plans/         # per-section/figure/table task decomposition
  drafting/              # serial/parallel drafting + claim-first enforcement
  claim-verification/    # 4-pass pre-submission verifier
  revision/              # unified internal + journal review loop
  submission/            # freeze gate + archive
  planning-foundation/   # persistent .writing/ state + agent planning dirs (v0.2.0, inlined)
  brainstorming/         # design-doc exploration (v0.2.0, inlined)
  spec-interview/        # deep questioning to refine specs (v0.2.0, inlined)
  lightweight-execute/   # small-task structured execution (v0.2.0, inlined)
  subagent-driven/       # serial same-session execution engine (v0.2.0, inlined)
  team-driven/           # parallel Agent Team execution engine (v0.2.0, inlined)
  executing-plans/       # cross-session batch execution engine (v0.2.0, inlined)
  verification/          # pre-commit verification (v0.2.0, inlined)
  finishing-branch/      # merge/PR integration (v0.2.0, inlined)
  stashing/              # pause/resume in-progress work (v0.2.0, inlined)
  archiving/             # freeze completed projects (v0.2.0, inlined)
  git-worktrees/         # isolated workspace setup (v0.2.0, inlined)
templates/               # copied into .writing/ on init by scripts/init-writing-dir.sh
tests/
  smoke.sh               # 26 end-to-end checks
CHANGELOG.md             # user-facing release notes
.env.example
.gitignore
README.md
```

## Scope (v1 YAGNI)

**In scope**: single-author IMRAD research manuscripts, claim-first drafting, citation verification via upstream `citation-management` / `research-lookup`, reporting-guideline compliance (CONSORT/STROBE/PRISMA via upstream `peer-review`), optional Zotero dual-source-of-truth.

**Out of scope, deferred to v2**: multi-author git collaboration, Zotero annotation/notes round-trip, reviews / grants / theses, non-IMRAD formats, venue-specific templating, auto-submission to journal portals, LaTeX compile.

## Development

```bash
bash tests/smoke.sh       # ~35 PASS lines across 6 sections, ending in ALL SMOKE TESTS PASSED
cat CHANGELOG.md          # release notes
```

Contributions welcome. See [CHANGELOG.md](./CHANGELOG.md) "Known limitations" for the v2 roadmap.

## License

MIT

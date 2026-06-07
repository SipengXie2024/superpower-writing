# superpower-writing

> Self-contained Claude Code plugin that drafts a detailed, evidence-backed
> paper skeleton for a human author to refine. It is not a one-shot paper
> generator. Domain skills (IMRAD section standards, citation management,
> figure generation, literature lookup, data-plot visualization, prose
> polish) and the claim-first drafting pipeline ship inside this plugin's
> `skills/` directory. Large parallel drafting and cross-section review run
> as Claude Code dynamic workflows rather than bundled orchestration skills.
> The earlier hard dependency on `K-Dense-AI/scientific-agent-skills` was
> dissolved in v0.7.0.

<!-- This README is written to be agent-executable. Every install step, every
     check, and every troubleshooting recipe is a literal command you can run
     verbatim. Expected outputs are shown under each command. -->

## Status

- **Version**: `v0.12.0`
- **Scope**: single-author IMRAD research manuscripts (CS / systems / ML / HCI)
- **Dependencies**: Zotero API (optional, gated by `zotero.enabled` in metadata); Codex CLI (used by `scientific-schematics` for figure generation via `collaborating-with-codex`)
- **Repo**: https://github.com/SipengXie2024/superpower-writing

## TL;DR — what this plugin does

1. Persists your paper state in `.writing/` (outline, claims, manuscript, metadata, reviews, archive).
2. Forces **claim-first writing**: every load-bearing paragraph in `manuscript/NN_*.tex` must carry `% claim: id` bound to a claim with `STATUS: evidence_ready` (or `% draft-only` for exploration). A `PreToolUse` hook hard-blocks writes that violate this.
3. Resolves citations **Zotero first → network fallback** (when Zotero is enabled). Pushes new DOIs back to your library if configured.
4. Checks reliability before handoff: `claim-verification` confirms every `\cite{}` resolves against `refs.bib` and that the cited abstract actually supports the claim (catching hallucinated or mismatched citations), and flags any `draft-only` or `[NEEDS-EVIDENCE]` left in the skeleton.

## Agent install checklist

Run these in order. Each command prints what it did; compare to "Expected".

### 0. Check prerequisites

```bash
which claude && claude --version      # needs Claude Code CLI
which gh && gh auth status             # needed only if you want to push
python3 -c "import yaml; yaml.safe_load('a: 1')"  # hook uses PyYAML
```

Expected: no command fails. If the PyYAML probe errors, run `pip install --user --upgrade pyyaml`.

### 1. Install this plugin

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

### 2. Verify the install

```bash
cd /path/to/superpower-writing
bash scripts/check-deps.sh
```

Expected (success): `[superpower-writing] deps OK (skills at <root>; PyYAML present)`.

If FAIL, the script names the missing dependency and prints a fix recipe (re-clone or reinstall the plugin when a bundled skill is missing; `pip install --user --upgrade pyyaml` when PyYAML is the gap) plus the candidate skill roots it searched. Follow it and re-run.

### 3. (Optional) Enable Zotero integration

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

### 4. Run the smoke test

```bash
bash tests/smoke.sh
```

Expected final line: `ALL SMOKE TESTS PASSED`. The test exercises `.writing/` init, dep-check and Zotero-creds failure messaging, the claim-enforcement allow/block cases, term-ordering enforcement, manifest JSON sanity (plugin.json / marketplace.json / hooks.json), a file-presence audit of the shipped skills, commands, hooks, agents, output style, and section standards, and a deletion audit confirming the removed components stay gone.

## Agent usage — lifecycle by user intent

Each row is keyed to what the **user** says. The **agent** picks the slash command.

| User intent                                  | Slash command              | What happens                                                                                                                                               |
|----------------------------------------------|----------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------|
| "Let's start a new paper on X"               | `/writing:outline X`       | Runs `outlining` skill. Initializes `.writing/`, seeds IMRAD outline, creates `claims/section_NN_*.md` stubs, fills `metadata.yaml`.                     |
| "Draft the methods section"                  | `/writing:draft methods`   | Runs `drafting`. Subagent resolves EVIDENCE per claim (Zotero-first), advances STATUS to `evidence_ready`, only then writes tagged prose.               |
| "Draft everything in parallel"               | `/writing:draft all`       | Drafts independent sections in parallel via a Claude Code dynamic workflow (one `section-drafter` per section), then spec + manuscript review as a pipeline. |
| "Check dependencies"                         | `/writing:check-deps`      | Runs `scripts/check-deps.sh`. If `zotero.enabled`, also `check-zotero.sh`.                                                                                 |
| "Pause this paper, I need to switch"         | `/writing:stash <name>`    | Moves `.writing/` into `.writing/stash/<name>/`. Ready for a fresh paper.                                                                                 |
| "Archive the current state"                  | `/writing:archive`         | Snapshots `.writing/` into `.writing/archive/<timestamp>/`.                                                                                               |

## Stage gates

```
(dep-check) → outlining → writing-plans → drafting → claim-verification
                                                          │
                                        (skeleton ready for human refinement)
```

Each gate updates `.writing/progress.md` Task Dashboard. Skipping requires explicit user override. The plugin stops at an evidence-backed skeleton; final refinement, submission, and reviewer responses are the human author's job.

## Output style

This plugin ships an **Academic Research Assistant** output style (`output-styles/academic-research-assistant.md`): a rigorous research persona that puts argument before prose, stays evidence-driven, tags critique by severity, writes plain language inside a formal academic register, and never fabricates citations. Enable it with `/config` → Output style → "Academic Research Assistant", or set `"outputStyle": "Academic Research Assistant"` in your project `.claude/settings.local.json`. It pairs with the claim-first writing rules in `skills/drafting/references/`.

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

Any `% draft-only` marker still present at `claim-verification` is flagged as a failure to resolve before the skeleton is handed off.

## Zotero dual-source-of-truth (v1)

When `zotero.enabled: true`, citation resolution is two-phase:

1. **Zotero** via the `zotero-mcp` MCP server — query by DOI with `zotero_search_items`, fall back to `zotero_semantic_search` (paragraph-level similarity over PDF fulltext when indexed) when DOI match fails. Retrieve with `zotero_get_item_metadata` (markdown / BibTeX) or `zotero_get_item_fulltext` when a specific passage must be read. Hit = authoritative (you've vetted it).
2. **Network fallback** via `Skill(skill="superpower-writing:citation-management")` / `Skill(skill="superpower-writing:research-lookup")`. On hit, record `source: network` in the claim's EVIDENCE; if `auto_push_new_citations: true`, push to the configured Zotero collection and update `source: both`.

Fail only if both sources miss.

When `zotero.enabled: false` (default), the pipeline runs network-only.

## `.writing/` layout

```
.writing/
  outline.md                # IMRAD + per-section claim lists
  findings.md               # research synthesis, decisions, reviewer context
  progress.md               # Task Status Dashboard
  metadata.yaml             # authors + preregistration + data/code availability + reporting guideline + zotero block
  manuscript/               # LaTeX only — the hook enforces .tex
    00_abstract.tex         # exempt from claim enforcement (citation-free)
    01_introduction.tex
    02_background.tex       # CS / ML / systems default; omit for IMRAD-strict
    03_methods.tex
    04_results.tex
    05_discussion.tex
    06_conclusion.tex
    07_related_work.tex     # CS / ML / systems; placement varies by venue
    08_acknowledgments.tex  # exempt (optional)
  claims/
    section_<NN>_<slug>.md  # YAML list of {id, CLAIM, EVIDENCE[], STATUS}
  figures/                  # structural diagrams via tikz-figures; concept art via scientific-schematics; data plots via scientific-visualization
    graphical_abstract.pdf  # optional — systems papers usually omit it
  reviews/                  # internal spec + manuscript review notes
    internal_<date>.md
  archive/                  # frozen snapshots of completed work
  stash/<paper-name>/       # when you multiplex papers
  verify-report.md          # produced by claim-verification
  verify-cache.json         # DOI → {source, resolved_at} (gitignored)
```

## Troubleshooting recipes

| Symptom                                         | Diagnostic                                                      | Fix                                                                                  |
|-------------------------------------------------|-----------------------------------------------------------------|--------------------------------------------------------------------------------------|
| `check-deps.sh` fails                           | check message; names missing skill(s)                           | re-clone or reinstall this plugin (skills are bundled inside it; missing means an incomplete install)                                  |
| `check-zotero.sh` exits 1 "API key not set"     | `.env` missing or incomplete                                    | `cp .env.example .env` then fill in the two required fields                          |
| `check-zotero.sh` HTTP 403                      | key lacks required scope                                        | regenerate at zotero.org/settings/keys with read+write on the library                |
| `check-zotero.sh` HTTP 404                      | wrong `ZOTERO_LIBRARY_ID` or `ZOTERO_LIBRARY_TYPE`              | `curl -sS https://api.zotero.org/keys/<YOUR_KEY>` → read `userID` field (use that as `ZOTERO_LIBRARY_ID` with `ZOTERO_LIBRARY_TYPE=user`) |
| Hook blocks a legitimate write                  | claim referenced but no such `id` in `claims/section_...md`     | Add the claim entry and set `STATUS: evidence_ready` after evidence is resolved      |
| Hook blocks an exploratory paragraph            | untagged prose in a protected section                           | Either tag `% draft-only` or write a proper `claim` entry                            |
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
agents/                  # used as agentType in dynamic-workflow drafting/review
  section-drafter.md     # implementer: IMRAD-aware drafter with claim-first + Zotero-first evidence resolution
  spec-reviewer.md       # reviewer: outline/claim compliance vs the plan
  manuscript-reviewer.md # reviewer: scientific writing quality (IMRAD coherence, voice, hedging, clarity, AI-trace detection)
  citation-auditor.md    # reviewer: over/under/circular/stale citation; optional deep pass in claim-verification
scripts/
  init-writing-dir.sh    # bootstraps .writing/
  check-deps.sh          # 7-root probe for upstream skills
  check-zotero.sh        # Zotero API auth probe (never echoes key)
commands/                # /writing:outline /writing:draft /writing:check-deps /writing:stash /writing:archive
output-styles/
  academic-research-assistant.md  # rigorous academic-research persona (see ## Output style)
skills/                  # writing-domain + planning skills
  main/                  # router + dep gate (authoritative Claim-First Protocol section)
  outlining/             # IMRAD outline + claim stubs + metadata.yaml
  writing-plans/         # per-section/figure/table task decomposition
  drafting/              # claim-first drafting; orchestration via dynamic workflow or manual batch
  claim-verification/    # evidence-reliability check (claim completeness + citation/semantic match)
  executing-plans/       # manual-batch drafting fallback when dynamic workflows are unavailable
  literature-review/     # structured lit synthesis
  research-lookup/       # paper/abstract retrieval for evidence resolution
  citation-management/   # citation formatting, DOI resolution, bibliography assembly
  tikz-figures/          # structural vector figures in LaTeX/TikZ (compile-verified, two-candidate preview)
  scientific-schematics/ # raster concept art / pictorial figures (via Codex image_gen)
  scientific-visualization/ # publication-ready data plots + venue figure conventions
  polish/                # prose polish pass
  polish-by-diff/        # diff-scoped polish for near-final prose
  writing-clearly-and-concisely/ # plain-language editing principles
  humanizer/             # reduce AI-trace patterns in prose
  collaborating-with-codex/ # Codex CLI bridge (used by scientific-schematics)
  planning-foundation/   # persistent .writing/ state + delegated-role planning dirs
  brainstorming/         # design-doc exploration
  spec-interview/        # deep questioning to refine specs
  stashing/              # pause/resume in-progress work
  archiving/             # freeze completed projects into .writing/archive/
  git-worktrees/         # thin guide around Claude Code native worktree isolation
templates/               # copied into .writing/ on init by scripts/init-writing-dir.sh
tests/
  smoke.sh               # end-to-end checks (76 PASS lines)
CHANGELOG.md             # user-facing release notes
.env.example
.gitignore
README.md
```

## Scope (v1 YAGNI)

**In scope**: single-author CS/systems/ML IMRAD paper skeletons, claim-first drafting, citation-reliability verification (`citation-management` / `research-lookup` + semantic match against the cited abstract), optional Zotero dual-source-of-truth, prose polish and AI-trace reduction.

**Out of scope** (the human author's job, or deferred): final prose refinement and journal submission, reviewer-response/rebuttal drafting, reporting-guideline checklists (CONSORT/STROBE/PRISMA for clinical/biology venues), multi-author collaboration, non-IMRAD formats, LaTeX compile. Large parallel drafting and cross-checked audit are delegated to Claude Code dynamic workflows rather than bundled in the plugin.

## Development

```bash
bash tests/smoke.sh       # 76 PASS lines across 7 sections, ending in ALL SMOKE TESTS PASSED
cat CHANGELOG.md          # release notes
```

Contributions welcome. See [CHANGELOG.md](./CHANGELOG.md) "Known limitations" for the v2 roadmap.

## License

MIT

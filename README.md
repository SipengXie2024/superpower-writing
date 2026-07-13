# superpower-writing

> Self-contained Claude Code plugin that runs a research paper from idea to
> reviewer response. It generates and ranks research directions, gates them on
> novelty, drafts a detailed evidence-backed IMRAD skeleton for a human author
> to refine, and helps respond to reviewers. It is not a one-shot paper
> generator. Domain skills (idea generation, novelty adjudication, idea
> scoring, IMRAD section standards, citation management, figure generation,
> literature lookup, data-plot visualization, prose polish, cross-model review,
> rebuttal drafting) and the claim-first drafting pipeline ship inside this
> plugin's `skills/` directory. Large parallel drafting and cross-section
> review run as Claude Code dynamic workflows rather than bundled orchestration
> skills. The earlier hard dependency on `K-Dense-AI/scientific-agent-skills`
> was dissolved in v0.7.0.

<!-- This README is written to be agent-executable. Every install step, every
     check, and every troubleshooting recipe is a literal command you can run
     verbatim. Expected outputs are shown under each command. -->

## Status

- **Version**: `v1.1.0`
- **Scope**: single-author IMRAD research manuscripts (CS / systems / ML / HCI)
- **Dependencies**: Zotero API (optional, gated by `zotero.enabled`); Codex CLI and Hermes Agent CLI (optional academic consultation backends). Codex is also required for raster scientific-figure generation.
- **Repo**: https://github.com/SipengXie2024/superpower-writing

## TL;DR — what this plugin does

1. **Decides the contribution before structure.** `research-ideation` generates 15 to 20 candidate directions through named lenses, scores them with a FINER rubric, and runs a cross-model adversarial pass so one survivor hands off to outlining. `novelty-gap-check` and `idea-evaluator` gate that survivor on novelty and a top-venue bar before drafting starts.
2. Persists your paper state in `.writing/` (ideation, outline, claims, manuscript, metadata, reviews, archive).
3. Follows **claim-first writing**: every load-bearing paragraph in `manuscript/NN_*.tex` must carry `% claim: id` bound to a claim with `STATUS: evidence_ready` (or `% draft-only` for exploration). Resolving a claim's evidence before writing its paragraph is a required drafting discipline.
4. Resolves citations **Zotero first → network fallback** (when Zotero is enabled). Pushes new DOIs back to your library if configured.
5. Checks reliability before handoff: `claim-verification` confirms every `\cite{}` resolves against `refs.bib` and that the cited abstract actually supports the claim (catching hallucinated or mismatched citations), flags any `draft-only` or `[NEEDS-EVIDENCE]` left in the skeleton, and runs an optional research-integrity gate on experiment-bearing papers.
6. **Reviews and rebuts.** Read-only academic consultation runs Codex and Hermes concurrently and preserves both evidence-linked opinions separately. `adversarial-review` computes one verdict per provider; `external-review` keeps two venue reviews without voting or synthetic consensus; `rebuttal` turns reviewer comments into a grounded response letter. Every verdict is advisory.

## Agent install checklist

Run these in order. Each command prints what it did; compare to "Expected".

### 0. Check prerequisites

```bash
which claude && claude --version      # needs Claude Code CLI
which codex && codex --version          # optional; paired review + raster figures
which hermes && hermes --version        # optional; paired review
which gh && gh auth status              # needed only if you want to push
```

Expected: `claude` succeeds. Missing `codex` or `hermes` makes paired consultation partial and produces a warning from `check-deps.sh`; it does not block local writing. Missing Codex also disables `scientific-schematics` raster generation. `gh` is optional.

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

Expected (success): `[superpower-writing] deps OK (skills at <root>)`.

If FAIL, the script names the missing dependency and prints a fix recipe (re-clone or reinstall the plugin when a bundled skill is missing) plus the candidate skill roots it searched. Follow it and re-run.

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

Expected final line: `ALL SMOKE TESTS PASSED`. The test covers `.writing/` initialization, dependency and Zotero messaging, manifest JSON, shipped components, academic handoff validation, Codex and Hermes bridges, concurrent pairing, consumer routing, skill lint, and evaluation fixtures. It does not call the real external models.

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
(dep-check) → research-ideation → novelty-gap-check / idea-evaluator → outlining
                  → writing-plans → drafting → claim-verification
                                                     │
                                   (skeleton ready for human refinement)
                                                     │
            adversarial-review · external-review (advisory pre-submission read)
                                                     │
                          rebuttal (grounded response to reviewers)
```

The idea phase runs in order when the contribution is undecided: `research-ideation` generates and ranks directions, then `novelty-gap-check` (查新, per-claim delta) and `idea-evaluator` (top-venue bar, fatal-flaw short-circuit) gate the survivor. The plugin then produces an evidence-backed skeleton and helps the author stress-test it. External review uses paired Codex and Hermes consultation; the two views remain separate and advisory. Final prose refinement and submission remain the human author's job.

## Paired academic consultation

Read-only academic analysis, literature synthesis, candidate prose, experiment planning, novelty opinions, and manuscript review use one neutral brief for both providers:

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/paired_consult.py" \
  --cd "/absolute/project" \
  --handoff-kind venue-review \
  --PROMPT "Read the named paper files and produce an evidence-linked review. Do not modify files."
```

Launch the command in the background with a timeout of at least `660000` ms. The result has `pair_status`, `codex`, and `hermes`. It never adds a consensus, winner, vote, or overall verdict. If one provider fails, the other result remains available.

Codex consultation is forced into its `read-only` sandbox and never falls back to write access. Hermes oneshot has no equivalent filesystem sandbox, so the bridge ignores project rules, forbids writes in the prompt, and compares the worktree and current commit before and after the call. Any Hermes write makes that lane fail with `workspace_modified`.

Public papers may be sent directly. Before sending an unpublished manuscript, confidential review, restricted dataset, personal information, or other sensitive content, identify the exact files or excerpts that both external services will receive and obtain user confirmation.

Scientific image generation is the only Codex-only consultation exception because Hermes has no corresponding image tool. Authorized file-changing tasks also use one provider rather than two, avoiding concurrent edits.

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

Claim-first discipline: every `% claim: id` paragraph in `**/manuscript/*.tex` must reference a claim whose `STATUS` is `evidence_ready` or `verified` — writing prose against a stub-status claim is a violation to fix, not to route around. **Exemption is by slug-ending** — any file whose stem ends in `_abstract`, `_references`, or `_acknowledgments` is exempt from paragraph tagging (so `00_abstract.tex`, `09_references.tex`, `10_acknowledgments.tex` all work). Any other stem (including new additions like `11_appendix.tex`) tags every load-bearing paragraph. `.md` files under `manuscript/` are out of scope — the plugin operates on LaTeX only.

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
  ideation.md               # candidate slate + FINER scores + adversarial pass + rejected list (research-ideation)
  ideation-brief.md         # the selected research direction, formatted for outlining Step 1
  outline.md                # IMRAD + per-section claim lists
  findings.md               # research synthesis, decisions, reviewer context
  progress.md               # Task Status Dashboard
  metadata.yaml             # authors + preregistration + data/code availability + reporting guideline + zotero block
  manuscript/               # LaTeX only — claim-first tagging applies to .tex
    00_abstract.tex         # exempt from claim tagging (citation-free)
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
  reviews/                  # internal spec + manuscript review notes + rebuttal/review artifacts
    internal_<date>.md
    REVIEWS_RAW.md          # reviewer comments verbatim (rebuttal)
    ISSUE_BOARD.md          # atomized comments + fixed action labels (rebuttal)
    RESPONSE_DRAFT.md       # R-A-C response letter (rebuttal)
    REVISION_PLAN.md        # one checklist line per promised edit (rebuttal)
    REBUTTAL_STATE.md       # phase + three-gate status (rebuttal)
    external-review-<date>.md  # separate Codex and Hermes reviews + provider status
  adversarial-review.md     # independent Codex and Hermes attack/adjudication verdicts
  novelty-report.md         # optional, per-claim novelty delta (novelty-gap-check)
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
| `smoke.sh` fails                                | read the specific `FAIL: ...` line                              | Each check is independent; fix what's listed                                         |
| paired consultation is `partial`                | inspect the failed provider's stable `error_code`               | install or authenticate that CLI; keep the successful provider result                |
| Hermes reports `workspace_modified`             | compare Git status and the current commit before and after      | report the external write and stop; do not describe the call as read-only            |
| Codex consultation cannot start                 | confirm the installed Codex supports `--sandbox read-only`      | update Codex; never retry consultation with broader file access                      |

## Layout

```
.claude-plugin/
  plugin.json
  marketplace.json
agents/                  # used as agentType in dynamic-workflow drafting/review
  section-drafter.md     # implementer: IMRAD-aware drafter with claim-first + Zotero-first evidence resolution
  spec-reviewer.md       # reviewer: outline/claim compliance vs the plan
  manuscript-reviewer.md # reviewer: scientific writing quality (IMRAD coherence, voice, hedging, clarity, AI-trace detection)
  citation-auditor.md    # reviewer: over/under/circular/stale citation; optional deep pass in claim-verification
scripts/
  init-writing-dir.sh    # bootstraps .writing/
  check-deps.sh          # 7-root probe for upstream skills
  check-zotero.sh        # Zotero API auth probe (never echoes key)
  lint_skills.py         # CI-grade SKILL.md linter (name=slug, 40-80-word "Use when" description, no em-dash, LOC ceiling, single-level references); baseline-ratcheted
  consult_handoff.py     # strict academic handoff profiles + private raw-artifact storage
  paired_consult.py      # concurrent Codex/Hermes consultation with isolated provider context
commands/                # /writing:outline /writing:draft /writing:check-deps /writing:stash /writing:archive
output-styles/
  academic-research-assistant.md  # rigorous academic-research persona (see ## Output style)
skills/                  # writing-domain + planning skills
  main/                  # router + dep gate (authoritative Claim-First Protocol section)
  research-ideation/     # idea generation before outlining: 15-20 lensed candidates, FINER scoring, cross-model adversarial pass
  novelty-gap-check/     # per-claim novelty delta + advisory PROCEED / PROCEED-WITH-CAUTION / ABANDON (查新)
  idea-evaluator/        # one idea vs a top-venue bar; fatal-flaw short-circuit then 5-dimension + FINER scoring
  outlining/             # IMRAD outline + claim stubs + metadata.yaml
  writing-plans/         # per-section/figure/table task decomposition
  drafting/              # claim-first drafting; orchestration via dynamic workflow or manual batch
  claim-verification/    # evidence-reliability check (claim completeness + citation/semantic match + optional research-integrity gate)
  adversarial-review/    # committed kill-argument memo + external adjudication + non-self-graded PASS/WARN/FAIL
  external-review/       # separate Codex/Hermes reviews, results-to-claims matrices, experiment plans
  rebuttal/              # reviewer comments → grounded R-A-C response with provenance/commitment/coverage gates
  executing-plans/       # manual-batch drafting fallback when dynamic workflows are unavailable
  literature-review/     # structured lit synthesis
  research-lookup/       # paper/abstract retrieval for evidence resolution
  citation-management/   # citation formatting, DOI resolution, bibliography assembly
  tikz-figures/          # structural vector figures in LaTeX/TikZ (compile-verified, two-candidate preview); references/figure-rhetoric.md picks which figures the paper needs, AUDIT mode reviews an existing figure against the 18-item checklist
  scientific-schematics/ # raster concept art / pictorial figures (via Codex image_gen)
  scientific-visualization/ # publication-ready data plots + venue figure conventions
  polish/                # prose polish pass
  polish-by-diff/        # diff-scoped polish for near-final prose
  writing-clearly-and-concisely/ # plain-language editing principles
  humanizer/             # reduce AI-trace patterns in prose
  collaborating-with-codex/ # Codex consultation/direct bridge; scientific figure exception
  collaborating-with-hermes/ # stateless Hermes bridge with workspace-change detection
  _shared/core/dual-consult-protocol.md # common privacy, isolation, evidence, and no-voting rules
  planning-foundation/   # persistent .writing/ state + delegated-role planning dirs
  brainstorming/         # design-doc exploration
  spec-interview/        # deep questioning to refine specs
  stashing/              # pause/resume in-progress work
  archiving/             # freeze completed projects into .writing/archive/
  git-worktrees/         # thin guide around Claude Code native worktree isolation
templates/               # copied into .writing/ on init by scripts/init-writing-dir.sh
tests/
  smoke.sh               # end-to-end checks
  eval-harness/          # prose-output eval: scores skill output against machine-checkable rubrics (no-fabricated-DOI, [UNVERIFIED] discipline, refuse-missing-figure-data); stdlib-only, fixture self-test wired into smoke.sh
CHANGELOG.md             # user-facing release notes
.env.example
.gitignore
README.md
```

## Scope (v1 YAGNI)

**In scope**: single-author CS/systems/ML IMRAD paper skeletons across the full lifecycle. This includes ideation, novelty adjudication, claim-first drafting, citation verification, optional Zotero, figures, prose polish, grounded rebuttal, and paired Codex/Hermes academic consultation for review and research judgment. Provider opinions remain separate; all verdicts are advisory and all source claims require verification.

**Out of scope** (the human author's job, or deferred): final prose refinement and the journal submission upload itself, reporting-guideline checklists (CONSORT/STROBE/PRISMA for clinical/biology venues), multi-author collaboration, non-IMRAD formats, LaTeX compile. Large parallel drafting and cross-checked audit are delegated to Claude Code dynamic workflows rather than bundled in the plugin.

## Development

```bash
bash tests/smoke.sh       # end-to-end checks, ending in ALL SMOKE TESTS PASSED
cat CHANGELOG.md          # release notes
```

Contributions welcome. See [CHANGELOG.md](./CHANGELOG.md) "Known limitations" for the v2 roadmap.

## License

MIT

# superpower-writing

> Self-contained Claude Code plugin that runs a CS / systems / ML research paper
> from idea to reviewer response. It shapes a contribution, converts it into an
> IMRAD outline of claims, drafts an evidence-backed LaTeX skeleton under
> claim-first discipline, verifies every citation, builds figures, polishes
> prose, and drafts rebuttals. It is not a one-shot paper generator; a human
> author refines the prose and submits. The domain skills ship inside this
> plugin's `skills/` directory and self-route by their own descriptions. There
> is no central router and no dependency gate.

<!-- This README is written to be agent-executable. Every install step, every
     check, and every troubleshooting recipe is a literal command you can run
     verbatim. Expected outputs are shown under each command. -->

## Status

- **Version**: `v2.0.0`
- **Scope**: single-author IMRAD research manuscripts (CS / systems / ML / HCI)
- **Dependencies**: Zotero via the `zotero-mcp` MCP server (optional, gated by `zotero.enabled` in a paper's metadata).
- **Repo**: https://github.com/SipengXie2024/superpower-writing

## What changed in v2.0.0

This is a breaking slim-down from 35 skills to 20. Borrowed generic process
skills (task decomposition, parallel drafting subagents, two review pipelines,
gate machines, session-start routing) are gone. What survives is the part a
strong model cannot supply on its own: persistent on-disk state and domain
knowledge. Skills now self-route by their descriptions instead of passing
through a central router or a dependency gate, both of which were removed.
Overlapping skills were merged: idea generation, novelty adjudication, and idea
scoring folded into `idea`; three literature-search skills into `literature`;
two review skills into `review` (adversarial and venue modes); and three prose
skills into `polish`. Drafting is now inline: the model drafts each section
itself in outline order, with no parallel subagents and no review pipeline.

## TL;DR: what this plugin does

1. **Decides the contribution before structure.** `idea` (optional, used when the direction is undecided) runs three internal phases in one skill: it generates candidate directions through named lenses with FINER scoring, adjudicates novelty per technical claim against prior work (查新), then evaluates the survivor against a top-venue bar with a fatal-flaw short-circuit. Every verdict is advisory.
2. **Turns the idea into a spec of claims.** `outlining` converts the direction into an IMRAD outline plus a per-section claim list, sharpened through an interleaved interview, and fills `metadata.yaml`. No prose is written here.
3. **Drafts claim-first.** `drafting` is a thin shell that routes to the writing references. Every load-bearing paragraph in `manuscript/NN_*.tex` carries a `% claim: id` comment bound to a claim whose `STATUS` is `evidence_ready` or `verified` (or a `% draft-only` marker for exploration). Resolving a claim's evidence before writing its paragraph is a required discipline.
4. **Resolves citations Zotero first, then network fallback** (when Zotero is enabled), and can push new DOIs back to your library.
5. **Checks reliability before handoff.** `claim-verification` confirms every `\cite{}` resolves against `refs.bib`, semantic-matches the cited abstract against the claim to catch hallucinated or mismatched references, and flags any `draft-only` or `[NEEDS-EVIDENCE]` left in the skeleton.
6. **Polishes and rebuts.** `polish` runs three passes (strip AI tells, apply Strunk clarity, hold each claim to its evidence). `rebuttal` turns reviewer comments into a grounded response letter.

## The writing spine

```
idea          (optional; when the contribution is undecided)
  |
  v
outlining     IMRAD outline + per-section claims, sharpened by an interleaved
  |           interview -> .writing/outline.md + claims/ + metadata.yaml
  v
drafting      inline, claim-first; a thin shell -> the writing references,
  |           model drafts each section in outline order into manuscript/*.tex
  v
claim-verification   mechanical citation + evidence check
  |
  v
polish        de-AI pass, Strunk clarity, evidence wording (in place or diff-first)
  |
  v
rebuttal      grounded R-A-C response after reviews arrive
```

`literature`,
`citations`, and `pdf-explore` resolve evidence throughout. Figures come from
`tikz-figures` (vector) and `scientific-visualization` (data plots).
Cryptographic proofs come from
`game-based-security-proof` and `simulation-security-proofs`. `domain-glossary`
keeps the project's ubiquitous language in a repo-root `CONTEXT.md` that
outlives any single paper, and `/wait-what` re-pitches the last message in
controlled plain language when it did not land. Skills discover each other by
description; there is no orchestrator to invoke first.

## Agent install checklist

Run these in order. Each command prints what it did; compare to "Expected".

### 0. Check prerequisites

```bash
which claude && claude --version      # needs Claude Code CLI
which gh && gh auth status              # needed only if you want to push a release
```

Expected: `claude` succeeds. `gh` is optional.

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

Expected: `claude plugin list` shows `superpower-writing` as installed. Skills
are bundled inside the plugin, so a successful install is a complete install;
there is no separate dependency check to run.

### 2. (Optional) Enable Zotero integration

Zotero turns on **dual source of truth**: citations resolve from your Zotero
library first, then fall back to network lookup via the `literature` and
`citations` skills. When `auto_push_new_citations: true`, new DOIs discovered
via network are pushed back to your configured collection.

- Install the `zotero-mcp-server` MCP server: `uv tool install "zotero-mcp-server[semantic,scite]"` (or `pipx install "zotero-mcp-server[semantic,scite]"`). The `[semantic]` extra enables AI-powered similarity search across your library; `[scite]` adds citation-intelligence tallies and retraction alerts. The `zotero-mcp` binary installed by this package is what `.mcp.json` spawns over stdio at session start. (Note: on PyPI the package was renamed from `zotero-mcp` to `zotero-mcp-server`; the old `zotero-mcp` package is v0.1.6 and ships only 3 tools, so make sure you install the new name.)

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

`scripts/check-zotero.sh` is idempotent; it never echoes the API key
(header-only, body discarded). MCP servers load at session start, so a fresh
Claude Code session is needed after editing `.mcp.json` or exporting the vars.

### 3. Run the smoke test

```bash
bash tests/smoke.sh
```

Expected final line: `ALL SMOKE TESTS PASSED`. The test covers `.writing/`
initialization, Zotero messaging, manifest JSON, shipped components, skill
lint, and evaluation fixtures. This same smoke test, the skill linter, and the
eval-harness fixture self-test form the pre-release gate that `releasing` runs
before cutting a tag.

## Commands

Each command is what the **agent** invokes on the user's behalf.

| User intent                            | Slash command             | What happens                                                                                                                    |
|----------------------------------------|---------------------------|---------------------------------------------------------------------------------------------------------------------------------|
| "Let's start a new paper on X"         | `/writing:outline X`      | Runs `outlining`. Initializes `.writing/` if missing, iterates literature retrieval, seeds the IMRAD outline and `claims/` stubs, fills `metadata.yaml`. |
| "Draft the methods section" / "draft the paper" | `/writing:draft methods` | Runs `drafting`. Resolves each claim's evidence (Zotero first, network fallback), advances `STATUS` to `evidence_ready`, then writes `% claim: id`-tagged LaTeX prose section by section, in outline order. |
| "Archive the current state"            | `/writing:archive`        | Runs `archiving`. Snapshots `.writing/` into `.writing/archive/<date>/` and consolidates findings before a reset.               |

Other skills (`idea`, `literature`, `citations`, `pdf-explore`,
`claim-verification`, `polish`, `rebuttal`, the figure and proof
skills) self-route by description; ask for what you want ("check novelty",
"polish this section", "find baselines") and the matching skill triggers.

## Output style

This plugin ships an **Academic Research Assistant** output style
(`output-styles/academic-research-assistant.md`): a rigorous research persona
that puts argument before prose, stays evidence-driven, tags critique by
severity, writes plain language inside a formal academic register, and never
fabricates citations. Enable it with `/config` -> Output style -> "Academic
Research Assistant", or set `"outputStyle": "Academic Research Assistant"` in
your project `.claude/settings.local.json`. It pairs with the claim-first
contract in `skills/_shared/core/claim-first-protocol.md`.

## The claim-first protocol (core invariant)

The single source of truth for the tag rules, the `STATUS` states, and citation
placement is `skills/_shared/core/claim-first-protocol.md`. `drafting` follows
it when writing prose, `claim-verification` checks it mechanically, and
`outlining` and `rebuttal` rely on its terms.

Every load-bearing paragraph in `.writing/manuscript/NN_<slug>.tex` carries a
LaTeX line comment at column 0:

```latex
% claim: meth-c1
We enrolled 1,247 patients with T2D from NHANES cycles 2018--2023...
```

Or escapes tracking for early exploration:

```latex
% draft-only
Rough notes about what this section might say.
```

`STATUS` runs `stub` -> `evidence_ready` -> `verified`. Prose must not cite a
`stub`-status claim; resolve evidence first (look the source up via
`literature` or `citations`, Zotero first when enabled), bump the claim to
`evidence_ready`, then write. `claim-verification` promotes a claim to
`verified` once the citation resolves and the source supports it.

**Exemption is by slug-ending**: any file whose stem ends in `_abstract`,
`_references`, or `_acknowledgments` is exempt from paragraph tagging (so
`00_abstract.tex`, `09_references.tex`, `10_acknowledgments.tex` all work). Any
other stem tags every load-bearing paragraph. The abstract is citation-free (no
`\cite` variant, no `% claim` tag). `.md` files under `manuscript/` are out of
scope; the plugin operates on LaTeX only. Any `% draft-only` marker still
present at `claim-verification` is flagged as a failure to resolve.

## Zotero dual source of truth

When `zotero.enabled: true`, citation resolution is two-phase:

1. **Zotero** via the `zotero-mcp` MCP server. Query by DOI, fall back to
   semantic search over PDF fulltext when a DOI match fails, and retrieve
   metadata or BibTeX with the MCP tools. A hit is authoritative because you
   have already vetted it.
2. **Network fallback** via the `literature` and `citations` skills. On a hit,
   record `source: network` in the claim's EVIDENCE; if
   `auto_push_new_citations: true`, push to the configured Zotero collection and
   update `source: both`.

Fail only if both sources miss. When `zotero.enabled: false` (default), the
pipeline runs network-only.

## `.writing/` layout

State that survives context resets lives here. `scripts/init-writing-dir.sh`
scaffolds it; the rest fills in as skills run.

```
.writing/
  metadata.yaml       # authors, venue, writing_profile, data/code availability, zotero block
  outline.md          # IMRAD structure + per-section claim lists (outlining)
  ideation.md         # optional: candidate directions + advisory verdicts (idea)
  claims/
    section_<NN>_<slug>.md   # YAML list of {id, CLAIM, EVIDENCE[], STATUS}
  manuscript/         # LaTeX only; claim-first tagging applies to .tex
    00_abstract.tex   # exempt from claim tagging; citation-free
    01_introduction.tex
    02_background.tex
    03_methods.tex
    04_results.tex
    05_discussion.tex
    06_conclusion.tex
    07_related_work.tex
  main.tex            # top-level LaTeX that \input{}s each manuscript section
  figures/            # tikz-figures (vector) . scientific-visualization (plots)
  refs.bib            # bibliography; fills as citations resolve (Zotero export + network)
  findings.md         # discoveries, decisions + rationale, rejected alternatives
  progress.md         # Task Status Dashboard + session log
  reviews/            # review + rebuttal artifacts
  agents/             # per-role subagent findings.md / progress.md, aggregated upward
  archive/            # frozen snapshots of completed papers (archiving)
```

## Troubleshooting recipes

| Symptom                                     | Diagnostic                                                 | Fix                                                                                  |
|---------------------------------------------|------------------------------------------------------------|--------------------------------------------------------------------------------------|
| `check-zotero.sh` exits 1 "API key not set" | `.env` missing or incomplete                               | `cp .env.example .env` then fill in the required fields                              |
| `check-zotero.sh` HTTP 403                  | key lacks required scope                                    | regenerate at zotero.org/settings/keys with read+write on the library                |
| `check-zotero.sh` HTTP 404                  | wrong `ZOTERO_LIBRARY_ID` or `ZOTERO_LIBRARY_TYPE`         | `curl -sS https://api.zotero.org/keys/<YOUR_KEY>`, read the `userID` field (use it as `ZOTERO_LIBRARY_ID` with `ZOTERO_LIBRARY_TYPE=user`) |
| Zotero tools not available in session       | `.mcp.json` or vars changed after session start            | start a fresh Claude Code session; MCP servers load once at session start            |
| `smoke.sh` fails                            | read the specific `FAIL: ...` line                         | each check is independent; fix what is listed                                        |

## Layout

```
.claude-plugin/
  plugin.json
  marketplace.json
agents/                  # subagent role definitions
  citation-auditor.md    # over / under / circular / stale citation audit
scripts/
  init-writing-dir.sh    # bootstraps .writing/
  writing-reset.sh       # reset active .writing/ state, preserve archive/
  check-zotero.sh        # Zotero API auth probe (never echoes key)
  aggregate-agent-findings.sh  # fold subagent findings into top-level findings.md / progress.md
  lint_skills.py         # SKILL.md linter (name=slug, description length, no em-dash, LOC ceiling); baseline-ratcheted
  # plus archive-search / check-writing-state / snapshot-save / detect-* helpers
hooks/
  hooks.json             # SessionStart wiring
  session-start.sh       # reminds to start CONTEXT.md in writing projects that lack one
commands/                # /writing:outline  /writing:draft  /writing:archive
output-styles/
  academic-research-assistant.md   # rigorous academic-research persona (see ## Output style)
templates/               # findings.md, glossary.md, metadata.yaml, progress.md (copied into .writing/ on init)
skills/
  _shared/core/          # claim-first-protocol.md, terminology-ledger.md (cross-skill contracts)
  idea/                  # optional idea phase: lensed candidates + FINER, per-claim novelty, top-venue bar (advisory)
  outlining/             # IMRAD outline + per-section claim stubs + metadata.yaml, sharpened by an interleaved interview
  drafting/              # thin claim-first drafting shell -> writing references (section standards, style cautions, terminology)
  claim-verification/    # walks % claim tags, resolves \cite{} against refs.bib, semantic-matches abstracts, flags [NEEDS-EVIDENCE] / draft-only
  polish/                # three-pass prose polish (de-AI, Strunk clarity, evidence wording); edit-in-place or diff-first
  rebuttal/              # reviewer comments -> grounded R-A-C response with provenance / commitment / coverage gates
  literature/            # find + review literature via Zotero semantic search, web search, arXiv / DBLP / Semantic Scholar / CrossRef
  citations/             # generate + verify BibTeX; add-by-DOI / arXiv through Zotero; audit .bib for missing fields and duplicates
  pdf-explore/           # navigate a long PDF (outline, per-page text, keyword search) without dropping it whole into context
  pdf-visual-check/      # layout lint on the compiled PDF: margin overflow, block overlap, low-DPI images, blank pages
  tikz-figures/          # publication-quality LaTeX / TikZ vector figures, compile-verified, two-candidate preview
  scientific-visualization/  # publication-ready matplotlib / seaborn / plotly data plots with venue styling
  game-based-security-proof/ # game-hopping reduction proofs for cryptographic primitives
  simulation-security-proofs/ # simulation-based and UC proofs for MPC, ZK, OT, commitments
  planning-foundation/   # persistent .writing/ working memory across context resets; initialize it first
  domain-glossary/       # project ubiquitous language in repo-root CONTEXT.md; pairs with the terminology ledger
  wait-what/             # user-invoked: re-pitch the last message in controlled plain language with CONTEXT.md terms
  archiving/             # freeze a completed .writing/ into archive/ and reset for the next paper
  releasing/             # version bump + tag + GitHub Release behind the smoke / lint / eval pre-release gate
tests/
  smoke.sh               # end-to-end checks
  eval-harness/          # prose-output eval against machine-checkable rubrics (no-fabricated-DOI, [UNVERIFIED] discipline, refuse-missing-figure-data)
CHANGELOG.md
.env.example
.gitignore
README.md
```

## Scope

**In scope**: single-author CS / systems / ML IMRAD paper skeletons across the
full lifecycle. This includes optional ideation, novelty adjudication,
claim-first drafting, citation verification, optional Zotero, figures,
cryptographic proof sections, prose polish, and grounded rebuttal. All verdicts
are advisory and all source claims require verification.

**Out of scope** (the human author's job, or deferred): final prose refinement
and the submission upload itself, reporting-guideline checklists
(CONSORT / STROBE / PRISMA), multi-author collaboration, non-IMRAD formats, and
LaTeX compilation.

## Development

```bash
bash tests/smoke.sh              # end-to-end checks, ending in ALL SMOKE TESTS PASSED
python3 scripts/lint_skills.py   # SKILL.md linter (baseline-ratcheted)
cat CHANGELOG.md                 # release notes
```

Contributions welcome.

## License

MIT

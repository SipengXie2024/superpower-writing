---
name: submission
description: Final gate before journal submission (LaTeX). Verifies claim-verification PASS, metadata.yaml complete, graphical abstract present, no `% draft-only` tags remain, no [NEEDS-EVIDENCE] unresolved, exports .writing/refs.bib from Zotero, compiles main.tex via latexmk, then freezes a copy to .writing/archive/<date>/. Use when the user declares the paper ready to submit.
---

# Submission Gate

## Overview

Submission is the last chance to catch unresolved drafts, missing metadata,
unverified claims, and broken references before a manuscript leaves the
project. This skill runs a strict freeze checklist, generates a clean
`refs.bib`, then snapshots the paper into `.writing/archive/<date>/` as an
immutable record.

**Core principle:** block on any red flag — the cost of a delayed submission
is low; the cost of submitting an unverified manuscript is high.

**Announce at start:** `"I'm using the submission skill to gate and freeze this manuscript."`

**Prerequisite:** `.writing/` exists and contains `manuscript/`, `claims/`,
`metadata.yaml`, `outline.md`. If not, refuse and point the user to
`superpower-writing:main`.

## When to Use

- User declares the paper ready to submit ("submit", "freeze", "lock it in")
- `/submit` or `/archive` slash commands are invoked
- Pre-submission freeze before a collaborator hand-off

Do NOT use for mid-draft snapshots — use `superpower-writing:stashing` for
those. Submission archives are append-only, one-way.

## Checklist (all must pass; block on any failure)

Run every item. Collect failures into a single report before aborting, so the
user sees every gap at once instead of whack-a-mole.

### 1. Claim verification is green

Invoke `Skill(skill="superpower-writing:claim-verification")`. Require:

- The skill exits with all claims in `STATUS: verified`; any `evidence_ready`
  claim with a pending soft-failure override from claim-verification must be
  resolved in the verify-report first (see claim-verification/SKILL.md §semantic
  match).
- `.writing/verify-report.md` exists and its summary line shows zero FAIL.
- `.writing/verify-cache.json` was written/updated within the current run.

If any claim is `pending`, `failed`, `evidence_ready` with unresolved soft
failure, or missing a verification record, abort and list the offending claim
IDs.

### 2. metadata.yaml is complete

Parse `.writing/metadata.yaml`. Require:

- `authors:` is a non-empty list; every entry has `name` (no `TODO`).
- `reporting_guideline:` is set (not empty, not `TODO`).
- `data_availability.statement:` is non-empty (not `TODO`).
- `code_availability.url:` is set OR `code_availability.statement` explicitly
  documents why code is not public — no `TODO` placeholders.

Presence check only; the user owns truthfulness. Abort on any `TODO` string
found anywhere in the file.

### 3. Graphical abstract present (conditional)

Check for any file matching `.writing/figures/graphical_abstract.*` (png,
jpg, jpeg, pdf, svg, tif, tiff). This check is only enforced when `metadata.yaml`
contains `graphical_abstract: required` or the venue is known to require one
(most systems conferences do not). If the venue requires it and zero matches are
found, abort with instructions to place the file. If multiple matches, abort and
ask the user to pick one. If the venue does not require a graphical abstract and
none is found, emit a warning and continue.

### 4. No `% draft-only` markers remain

Grep all `.writing/manuscript/*.tex` (recursively) for `^\s*%\s*draft-only\b`.
Any hit aborts with file:line list. Draft-only markers are scaffolding and
must be resolved (either filled in with evidence-backed content or deleted)
before submission.

### 5. No `[NEEDS-EVIDENCE]` strings remain

Grep `.writing/` recursively for `[NEEDS-EVIDENCE]`. Any hit aborts with
file:line list. This includes `claims/`, `manuscript/`, `findings.md`,
`outline.md`, `metadata.yaml`, and anywhere else the string could hide.

### 5b. Abstract is citation-free

For every `.writing/manuscript/*.tex` whose stem ends in `_abstract`
(slug-ending match, e.g. `00_abstract.tex`), grep for any LaTeX citation
command (pattern `\\[a-zA-Z]*cite[a-zA-Z]*` — covers `\cite`, `\citep`,
`\citet`, `\nocite`, `\parencite`, `\textcite`, `\autocite`, `\footcite`,
`\citeauthor`, `\citeyear`, and every other `\*cite*` variant) and for
`^\s*%\s*claim:`. Any hit aborts with file:line list. The abstract must
summarize the paper's own findings without citing sources; the body sections
carry every reference. This mirrors the PreToolUse hook's
`CITATION_FREE_SLUGS` rule and runs independently at the submission gate
in case the hook was bypassed during editing (manual file copy, external
editor, etc.).

### 5c. Citation format and completeness

After `refs.bib` is generated (step after the checklist), run these
citation-specific checks. Reference file: `references/citation-styles.md`.

- **Bidirectional citation coverage:** every in-text `\cite{}` /
  `\citep{}` / `\citet{}` command in `.writing/manuscript/*.tex` resolves
  to an entry in `refs.bib`, and every `refs.bib` entry is cited at least
  once in the manuscript. Orphans in either direction are hard failures
  (unless `submission.prune_unused_bib: true` is set — in which case
  uncited entries are silently pruned rather than flagged).
- **Citation style matches venue requirement:** verify in-text format
  (numbered vs. author-date) and reference-list formatting match the
  target venue's stated style. See `references/citation-styles.md`
  §Journal-Specific Citation Styles for venue-to-style mapping.
- **DOIs present and valid for journal articles:** every `@article` entry
  in `refs.bib` whose publication year is 2000 or later must include a
  `doi` field. Validate each DOI by confirming it resolves (prefix match
  against `10.` is sufficient at this gate; full HTTP resolution is
  claim-verification's job).
- **Preprints cited with version and date:** every `@misc` or
  `@unpublished` entry with an `eprint` field (arXiv) must include
  `eprinttype = {arxiv}`, `eprintclass`, and either `version` or a
  `note` / `urldate` field carrying the access date.
- **Software and dataset citations include version + DOI or URL:** entries
  typed `@misc` or `@software` that reference software or datasets must
  carry a `version` field and either a `doi` or `url` field.
- **Journal abbreviations consistent with style:** all `journal` fields in
  `refs.bib` use the abbreviation system the target venue requires
  (PubMed/Index Medicus for medical venues, ISO for others). See
  `references/citation-styles.md` §Common Abbreviations for the canonical
  mapping.

Abort with a file:line list for each failure, grouped by category.

### 6. LaTeX compile test passes

After `refs.bib` is generated (below), compile `.writing/main.tex` with
`latexmk -pdf -interaction=nonstopmode main.tex` (run inside `.writing/`).
Require:

- Non-zero `main.pdf` is produced.
- No "undefined references" warnings in the log (grep
  `main.log` for `LaTeX Warning: Citation .* undefined` or `There were
  undefined references` — both abort).
- No "undefined control sequence" errors (unresolved \foo commands).

If `latexmk` or `pdflatex` is not installed, skip this check with a warning;
the user must run the compile manually before submitting. Do NOT proceed to
archiving without either a successful compile or an explicit user override
recorded in `.writing/findings.md`.

### Reporting checklist output

When any check fails, emit a single block like:

```
Submission gate FAILED (N issues):
  [1] claim-verification: 2 claims not verified
      - 03_methods.tex:claim-003 (pending)
      - 04_results.tex:claim-011 (failed: DOI mismatch)
  [2] metadata.yaml: reporting_guideline is TODO
  [3] draft-only markers: 1 remaining
      - manuscript/03_methods.tex:87
  [4] latex compile: 2 undefined references
      - main.log:1047: Citation 'smith2019novel' undefined
```

Do not proceed to archiving until every check is green.

## refs.bib Generation (Zotero export)

Runs between checklist items 5 and 6 (i.e., after semantic / draft-only /
[NEEDS-EVIDENCE] checks pass; before the LaTeX compile test). Requires
`zotero.enabled: true` in `.writing/metadata.yaml` — the plugin is
Zotero-first for bib management. If Zotero is disabled, abort with instructions
to enable it and populate the collection.

### Zotero export flow

1. **Collect citekeys from manuscript.** Grep all `.writing/manuscript/*.tex`
   for `\cite{...}` (including the variants `\citep{}`, `\citet{}` if
   natbib is used). Expand comma-separated arguments:
     ```
     grep -oE '\\cite(p|t)?\{[^}]+\}' .writing/manuscript/*.tex \
       | sed 's/.*{\([^}]*\)}/\1/' \
       | tr ',' '\n' \
       | sed 's/^ *//;s/ *$//' \
       | sort -u
     ```
   Deduplicate into a master list of citekeys. This is the exact set the
   final `refs.bib` must cover.

2. **Read Zotero config.** Load `zotero.collection_key` from
   `metadata.yaml`. If empty, abort — submission requires an explicit
   `collection_key` in metadata so the export scope is reproducible.

3. **Export the collection to BibTeX.**
   a. Call the `zotero_get_collection_items` MCP tool (from the `zotero`
      server in `.mcp.json`) with:
         collection_key = <metadata.yaml zotero.collection_key>
         limit          = 100
      Paginate with the `start` parameter until all items are retrieved.
   b. For each returned item, call
      `zotero_get_item_metadata(item_key=<data.key>, format="bibtex")`
      and append the returned BibTeX fragment to `refs.bib`.
   c. If Better BibTeX is installed on the user's Zotero and a stable
      citekey is present in the item's extra field, it appears in the
      exported BibTeX automatically. Otherwise zotero-mcp falls back
      to algorithmic keys from author+year+title; these keys are NOT
      stable across exports — warn in `.writing/findings.md`.
   d. Cross-check: every `\cite{<key>}` in the manuscript must resolve
      against `refs.bib`. Use `grep -oE '\\\\cite\\{[^}]+\\}' <tex files>`
      to enumerate cite keys, then grep each against `refs.bib`.
      Multiple-match or missing-citekey failures surface by file:line.

4. **Verify coverage.** For every citekey in the master list (step 1),
   confirm it appears as an entry key in `.writing/refs.bib`:
     ```
     awk -F'[{,]' '/^@/{print $2}' .writing/refs.bib | sort -u \
       > /tmp/bib_keys.txt
     comm -23 <(printf '%s\n' "${CITEKEYS[@]}" | sort -u) /tmp/bib_keys.txt
     ```
   Any missing citekey is a HARD FAILURE — the manuscript cites something
   Zotero does not know about. Abort with the list and instruct the user:
   (a) add the missing items to the Zotero collection, or (b) re-run
   `drafting` / `claim-verification` with `zotero.auto_push_new_citations:
   true` so newly-discovered citations get pushed back into Zotero
   automatically. Do NOT fall back to network DOI resolution here —
   submission is the one place Zotero is authoritative.

5. **Prune (optional).** The full collection export may contain entries
   not cited in this manuscript. For submission to venues that reject
   bibliographies with unused entries, write a pruned refs.bib containing
   only the subset of entries whose citekey is in the master list. This
   is opt-in via `metadata.yaml` `submission.prune_unused_bib: true`; the
   default is to keep the full export (LaTeX silently ignores unused
   entries and some venues prefer a complete bibliography).

### Output

A single valid BibTeX file at `.writing/refs.bib`. Overwrite any existing
copy; the archive will preserve prior versions.

## Archive Procedure

Once the checklist passes and `refs.bib` is written, freeze the paper.

### Step 1: Create archive directory

```bash
ARCHIVE_TS=$(date +%Y-%m-%d-%H%M)
ARCHIVE_DIR=".writing/archive/${ARCHIVE_TS}"
mkdir -p "${ARCHIVE_DIR}"
```

If `${ARCHIVE_DIR}` already exists (unlikely — minute resolution), append
`-2`, `-3`, etc. until unique.

### Step 2: Copy artifacts

Copy the following into `${ARCHIVE_DIR}/`:

- `manuscript/` (recursive, LaTeX sources)
- `main.tex` (top-level LaTeX document)
- `main.pdf` (compiled output from checklist item 6)
- `claims/` (recursive)
- `figures/` (recursive, includes the graphical abstract)
- `metadata.yaml`
- `outline.md`
- `refs.bib`
- `verify-report.md`
- `verify-cache.json`

Use `cp -r` for directories and `cp` for files. Do not copy `.writing/stash/`,
`.writing/reviews/`, or `.writing/archive/` itself — the archive is a paper
snapshot, not a full `.writing/` mirror.

### Step 3: Write archive README

Create `${ARCHIVE_DIR}/README.md` summarizing the frozen state:

```markdown
# Archive: <paper title>

**Frozen:** <YYYY-MM-DD HH:MM>
**Commit:** <git rev-parse HEAD>
**Venue:** <metadata.yaml → venue or "unspecified">
**Author:** <first author from metadata.yaml>

## Final verification

- Claims verified: <N>
- Claims failed: 0
- Reporting guideline: <metadata.yaml → reporting_guideline>
- Data availability: <open | restricted | on-request | none>

## Contents

- manuscript/ — final LaTeX IMRAD sections (.tex files)
- main.tex — top-level LaTeX document pulling sections via \input{}
- main.pdf — compiled output (from latexmk compile test)
- claims/ — evidence records for every `% claim: id` in manuscript/
- figures/ — including graphical_abstract.*
- metadata.yaml — author, COI, preregistration, data/code availability
- outline.md — structural plan
- refs.bib — BibTeX export from Zotero collection (<N> entries)
- verify-report.md — claim-verification output at freeze time
- verify-cache.json — DOI/abstract cache

## Notes

<!-- optional: submission portal ID, cover letter link, etc. -->
```

Pull the exact values by reading the source files; do not invent counts. If
`git rev-parse HEAD` fails (non-git project), record `Commit: (not a git
repo)`.

### Step 4: Verify the archive

After copying, run a quick sanity check:

- `${ARCHIVE_DIR}/manuscript/` has the same file count as
  `.writing/manuscript/`.
- `${ARCHIVE_DIR}/refs.bib` is non-empty.
- `${ARCHIVE_DIR}/README.md` exists.

Report `Archive saved to .writing/archive/<ARCHIVE_TS>/` with the file count.

## Post-Archive Reset

After the archive is on disk, prepare `.writing/` for the next revision round
(journal decision, co-author pass, resubmission). This is a targeted reset,
not a wipe — the paper identity survives.

### Preserve

- `.writing/metadata.yaml` — authors, reporting guideline, Zotero config all
  carry forward.
- `.writing/outline.md` — structure rarely changes between rounds.
- `.writing/archive/` — all prior frozen snapshots.
- `.writing/stash/` — unrelated paused work.
- `.writing/figures/` — usually retouched, not rebuilt from scratch.
- `.writing/claims/` — evidence records remain; revision may add or mark
  some stale.
- `.writing/manuscript/` — revision works on these in place.

### Reset

Rewrite `.writing/progress.md` from the template (from `planning-foundation/
templates/progress.md`), clearing the Task Status Dashboard and session log.
Preserve the paper title header and the outline reference at the top.

Optionally clear `.writing/verify-report.md` and `.writing/verify-cache.json`
— the next revision round will regenerate them. Ask the user first: if the
next round is a minor revision, the cache saves Zotero/network round-trips.

### Notify

Print a short summary:

```
Submission complete.
  Archive: .writing/archive/<timestamp>/
  Manuscript files frozen: <N>
  Claims frozen: <N>
  refs.bib entries: <N>
  progress.md: reset for next revision round
  metadata.yaml, outline.md: preserved
```

## Zotero Integration

This skill is one of four Zotero-aware skills (design.md §14.4). Its
responsibility is `refs.bib` generation — see the refs.bib Generation section
above. In short:

- **Zotero is required**, not optional. The plugin is Zotero-first for bib
  management (this was a deliberate design choice — see CHANGELOG). If
  `metadata.yaml → zotero.enabled` is false, abort submission with
  instructions to enable it.
- Zotero is authoritative for `refs.bib` — any citekey cited in the
  manuscript but missing from the configured Zotero collection is a hard
  failure.
- Do not fall back to network here; the fallback path is
  `claim-verification`'s responsibility during authoring, not the submission
  gate's.
- Delegate actual API calls to the `zotero-mcp` MCP server registered in `.mcp.json`.

## Edge Cases

**No claims at all:** If `.writing/claims/` is empty, the paper likely
skipped the claim-first protocol. Abort and direct the user to `drafting` —
submission without verified claims defeats the purpose of this plugin.

**Zotero credentials missing while enabled:** `scripts/check-zotero.sh`
should have caught this at session start, but double-check here. If
credentials are missing, abort with the install/env-var instructions from
`.env.example`.

**Graphical abstract file is empty:** Size-check the match (>1KB is a cheap
floor). A 0-byte placeholder is worse than a missing file because the
presence check passes silently.

**Re-freeze after minor edit:** If the user re-runs `submission` on the same
day, the timestamp suffix (`HHMM`) disambiguates. Do not overwrite prior
archives — each freeze is a historical record.

**Non-git project:** `git rev-parse HEAD` fails gracefully; record the
fallback string and continue. Do not block archiving on missing git.

## Key Principles

- **Checklist-first, archive-second.** The archive is only valuable if the
  paper it records is submission-ready. Never freeze a failing draft.
- **Fail loud, fail once.** Collect every checklist failure before returning;
  do not stop at the first red flag and force the user into a ping-pong fix
  loop.
- **Zotero is authoritative at submission.** Any `\cite{citekey}` in the
  manuscript whose key is not in the configured collection is a gap the user
  must close — don't paper over it.
- **Archives are immutable.** Once `.writing/archive/<date>/` is written, it
  is never edited. Re-submission creates a new archive; prior ones stand as
  the historical record.
- **Preserve paper identity across rounds.** `metadata.yaml` and `outline.md`
  carry forward; the Task Dashboard resets. The paper is one project with
  many rounds, not a fresh start each time.

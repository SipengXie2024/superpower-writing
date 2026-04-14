---
name: submission
description: Final gate before journal submission. Verifies claim-verification PASS, metadata.yaml complete, graphical abstract present, no draft-only tags remain, no [NEEDS-EVIDENCE] unresolved, then freezes a copy to .writing/archive/<date>/. Use when the user declares the paper ready to submit.
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

Do NOT use for mid-draft snapshots — use `superpower-planning:stashing` for
those. Submission archives are append-only, one-way.

## Checklist (all must pass; block on any failure)

Run every item. Collect failures into a single report before aborting, so the
user sees every gap at once instead of whack-a-mole.

### 1. Claim verification is green

Invoke `Skill(skill="claim-verification")`. Require:

- The skill exits with all claims in `STATUS: verified` (or equivalent PASS).
- `.writing/verify-report.md` exists and its summary line shows zero FAIL.
- `.writing/verify-cache.json` was written/updated within the current run.

If any claim is `pending`, `failed`, or missing a verification record, abort
and list the offending claim IDs.

### 2. metadata.yaml is complete

Parse `.writing/metadata.yaml`. Require:

- `authors:` is a non-empty list; every entry has `name` (no `TODO`).
- `reporting_guideline:` is set (not empty, not `TODO`).
- `data_availability.statement:` is non-empty (not `TODO`).
- `code_availability.url:` is set OR `code_availability.statement` explicitly
  documents why code is not public — no `TODO` placeholders.

Presence check only; the user owns truthfulness. Abort on any `TODO` string
found anywhere in the file.

### 3. Graphical abstract present

Check for any file matching `.writing/figures/graphical_abstract.*` (png,
jpg, jpeg, pdf, svg, tif, tiff). Exactly one match is required. If zero, abort
with instructions to place the file. If multiple, abort and ask the user to
pick one (different formats of the same figure are fine — flag only when the
basenames differ in intent).

### 4. No `<!-- draft-only -->` markers remain

Grep all `.writing/manuscript/*.md` (recursively) for `<!-- draft-only -->`.
Any hit aborts with file:line list. Draft-only markers are scaffolding and
must be resolved (either filled in with evidence-backed content or deleted)
before submission.

### 5. No `[NEEDS-EVIDENCE]` strings remain

Grep `.writing/` recursively for `[NEEDS-EVIDENCE]`. Any hit aborts with
file:line list. This includes `claims/`, `manuscript/`, `findings.md`,
`outline.md`, `metadata.yaml`, and anywhere else the string could hide.

### Reporting checklist output

When any check fails, emit a single block like:

```
Submission gate FAILED (N issues):
  [1] claim-verification: 2 claims not verified
      - section_03_intro.md:claim-003 (pending)
      - section_05_results.md:claim-011 (failed: DOI mismatch)
  [2] metadata.yaml: reporting_guideline is TODO
  [3] draft-only markers: 1 remaining
      - manuscript/section_04_methods.md:87
```

Do not proceed to `refs.bib` generation or archiving until every check is
green.

## refs.bib Generation

Runs after the checklist passes, before archiving. See design.md §14.4 for
the submission row of the Zotero responsibility table.

### Zotero-enabled path

When `.writing/metadata.yaml` has `zotero.enabled: true`:

1. Extract every cited DOI from `.writing/manuscript/*.md`. DOIs appear as
   `<!-- cite: 10.xxxx/yyyy -->` or inline `[@doi:10.xxxx/yyyy]` — use both
   patterns. Deduplicate.
2. Read `zotero.collection_key` from `metadata.yaml`.
3. Invoke `Skill(skill="pyzotero")` to fetch the BibTeX export for the
   intersection `(collection items) ∩ (cited DOIs)`.
4. Write the result to `.writing/refs.bib`.
5. If any cited DOI is missing from the Zotero collection, abort with the
   list. The user must add them to Zotero (or re-run `drafting`/
   `claim-verification` which auto-push new citations when
   `auto_push_new_citations: true`) before submission. Do not silently fall
   back to network here — submission is the one place we want Zotero to be
   authoritative.

### Zotero-disabled (degraded) path

When `zotero.enabled: false` or the block is absent:

1. Walk every `.writing/claims/*.md` and collect `EVIDENCE` entries of
   `type: citation`.
2. Assemble a BibTeX entry for each unique DOI using the cached metadata
   from `.writing/verify-cache.json` (authors, title, journal, year, DOI).
3. Write to `.writing/refs.bib`. Entry key: the DOI with non-alnum replaced
   by `_` (e.g., `10_1038_s41586_024_01234_5`).
4. Warn the user that `refs.bib` was built from EVIDENCE entries directly —
   degraded mode. Recommend enabling Zotero for future papers.

In both paths, the output must be a single valid BibTeX file at
`.writing/refs.bib`. Overwrite any existing copy; the archive will preserve
history.

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

- `manuscript/` (recursive)
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

- manuscript/ — final IMRAD sections
- claims/ — evidence records for every <!-- claim: id --> in manuscript/
- figures/ — including graphical_abstract.*
- metadata.yaml — author, COI, preregistration, data/code availability
- outline.md — structural plan
- refs.bib — BibTeX export (<N> entries, source: zotero|evidence)
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

- Gate all Zotero calls on `metadata.yaml → zotero.enabled`.
- When enabled, Zotero is authoritative for `refs.bib` — any cited DOI not
  present in the configured collection is a hard failure.
- Do not fall back to network here; the fallback path is
  `claim-verification`'s responsibility during authoring, not the submission
  gate's.
- Delegate actual API calls to `Skill(skill="pyzotero")`.

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
- **Zotero is authoritative at submission.** Any DOI cited in the manuscript
  that is not in the configured collection is a gap the user must close —
  don't paper over it.
- **Archives are immutable.** Once `.writing/archive/<date>/` is written, it
  is never edited. Re-submission creates a new archive; prior ones stand as
  the historical record.
- **Preserve paper identity across rounds.** `metadata.yaml` and `outline.md`
  carry forward; the Task Dashboard resets. The paper is one project with
  many rounds, not a fresh start each time.

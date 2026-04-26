---
name: revision
description: Unified review-loop handler for internal co-author review and external journal reviewer comments. Intake -> classify (Major/Minor/OutOfScope/Factually-wrong) -> per-item response draft -> apply diff -> re-run claim-verification. Use when review comments are received.
---

# Revision

Process one round of review — internal (co-author) or external (journal reviewer) — through a five-step pipeline: intake, classify, respond, apply, re-verify. One review instance per file under `.writing/reviews/<id>.md`; one round closes only after `claim-verification` passes again.

**Announce at start:** "I'm using the revision skill to handle this review round."

## Overview

Revision is where reviewer feedback becomes manuscript changes without silently breaking the claim graph. The pipeline is deliberately narrow: every comment gets a classification, every change that touches a claim triggers a claims-file update, and nothing is declared done until `claim-verification` re-runs clean. Internal and external reviews share the same pipeline; the only difference is that external reviews produce a response letter at the end.

This skill is a workflow, not an execution engine. Heavy lifting (prose edits, claim re-resolution) is delegated:

- Evidence for new or changed claims → `Skill(skill="superpower-writing:research-lookup")` / `Skill(skill="superpower-writing:citation-management")`; when `zotero.enabled`, also the `zotero-mcp` MCP tools from the `zotero` server in `.mcp.json`: `zotero_search_items` for DOI / title lookup, `zotero_semantic_search` as a fallback when DOI lookup misses (paragraph-level similarity over indexed fulltext), `zotero_get_item_metadata` for markdown / BibTeX, `zotero_get_item_fulltext` when the abstract is ambiguous and a body passage is needed, `zotero_add_by_doi` for push-back.
- Post-revision verification → `Skill(skill="superpower-writing:claim-verification")`.
- Style polishing of response letter → consult `skills/drafting/references/writing-principles.md` and `skills/drafting/references/style-cautions.md`; for venue-tuned voice, see `skills/submission/references/venue-styles.md`.

The PreToolUse hook is still active during revision: any newly introduced `% claim: id` tag must correspond to a claim with `STATUS ∈ {evidence_ready, verified}`, or the edit will be blocked. Revision-driven claim additions are first-class citizens, not second-class patches.

> Claim-first protocol: see `superpower-writing:main` §Claim-First Protocol.

## When to Use

Invoke after a review has been received and the manuscript already exists in a draftable state. Typical triggers:

- User pastes reviewer comments from a journal portal or email.
- Co-author returns a marked-up draft or a comment list.
- User types `/revise` with an optional path argument pointing at an existing `.writing/reviews/<id>.md`.

Do NOT invoke for:

- Pre-draft edits (use `drafting`).
- First-time claim resolution on fresh prose (use `drafting` + `claim-verification`).
- Pure copy-edit passes with no intellectual content changes — those can be handled by consulting `skills/drafting/references/writing-principles.md` and `skills/drafting/references/style-cautions.md` directly.

## Checklist

Round-level prerequisites:

- [ ] `.writing/reviews/` directory exists (created by `init-writing-dir.sh`).
- [ ] `.writing/manuscript/` contains the current draft (otherwise there is nothing to revise).
- [ ] `.writing/claims/` mirrors the manuscript section files.
- [ ] `.writing/metadata.yaml` present (needed if new claims require Zotero lookups).

Per-review checklist (before closing the round):

- [ ] `.writing/reviews/<id>.md` contains: raw comments, per-item classification, per-item response, per-item diff reference, per-item status.
- [ ] Every item is classified (no `unclassified` remaining).
- [ ] Manuscript edits committed; claim files updated in the same commit when claims were added or removed.
- [ ] `claim-verification` has run against the post-revision manuscript and passed.
- [ ] For external reviews: `.writing/reviews/<id>.response-letter.md` produced.
- [ ] For external reviews: `superpower-writing:rebuttal-auditor` has audited the response letter + manuscript diff and reported no unresolved `Critical` findings. Advisory-level findings acknowledged in the letter or explicitly dismissed.
- [ ] `.writing/progress.md` Task Dashboard has a `Reviewer Cycle` entry updated for each affected section.

## Process

The pipeline has five steps. Work through them in order; do not interleave.

### Step 1 — Intake

Create or reuse `.writing/reviews/<id>.md`. The `<id>` convention:

- Internal co-author review: `internal-<author-initials>-<date>` (e.g. `internal-jd-2026-04-12`).
- External journal reviewer: `<journal-slug>-r<round>-rev<n>` (e.g. `nature-comm-r1-rev2` for reviewer 2 of round 1).

The file has a fixed skeleton:

```markdown
---
review_id: <id>
kind: internal | external
source: <co-author name | journal name + reviewer number>
received: <YYYY-MM-DD>
round: <round number if external; omit for internal>
status: open  # open | in-progress | closed
---

# Raw comments

<paste or upload the verbatim comments here>

# Items

| # | Comment (short) | Classification | Manuscript refs | Response status |
|---|-----------------|----------------|-----------------|-----------------|
| 1 |                 |                |                 | pending         |
...

# Responses

## Item 1
...

# Applied diffs

## Item 1
commit: <sha>  files: manuscript/03_results.tex  claims: claims/section_03_results.md
...
```

If the user pastes comments inline, write them verbatim into "Raw comments" without paraphrasing. Reviewer tone and wording matter for the response letter later.

Split the raw block into numbered items. One item per discrete request. Do NOT merge two requests into one item even if they touch adjacent paragraphs.

### Step 2 — Classify

Classification drives every downstream decision. Use `AskUserQuestion` for each item in a batch (or one-by-one if there are many with ambiguous categorization):

```
Question: How should reviewer comment #<N> be classified?
Header:   "Classify item <N>"
Options:
  - Label:       "Major"
    Description: "Affects a claim, Methods, Results, or Discussion logic. Requires new evidence, new analysis, or substantive rewrite. Blocks round closure."
  - Label:       "Minor"
    Description: "Wording, clarity, figure caption, small factual tweak. No claim graph change. Quick to apply."
  - Label:       "OutOfScope"
    Description: "Beyond this paper (future work, separate study, disagrees with scope). Acknowledge in response letter; no manuscript change."
  - Label:       "Factually-wrong"
    Description: "Reviewer misread the paper or made a factual error. Politely correct in response; may still clarify prose to prevent future misreading."
```

Recommend a classification based on the item text, but do NOT silently classify — the user owns this judgment. Record the choice in the items table.

After classification:

- Major → proceeds to Step 3 and 4 with claim-graph awareness.
- Minor → proceeds to Step 3 and 4 as a plain edit (no claim-graph impact).
- OutOfScope → skip Step 4; write a response-only entry for Step 3 and proceed to re-verification with no manuscript change.
- Factually-wrong → write a response for Step 3; Step 4 is optional (only to clarify prose that misled the reviewer).

### Step 2.5 — Locked-term rename impact scan

Before any item that proposes renaming a project-level locked term — i.e., a name already recorded as a naming decision in `.writing/progress.md`, a label or bullet heading in `.writing/outline.md`, or a term that already appears in two or more `.writing/manuscript/*.tex` files — run this scan. Locked-term renames arrive both as reviewer requests ("rename X to Y for clarity") and as mid-draft author decisions; in both cases they cross the prose/spec boundary and must NOT be applied as single-file edits.

1. Locate every occurrence of the old term across manuscript, claims, and planning files:

   ```bash
   grep -rn --include='*.tex' --include='*.md' \
       -E '\b<old-term>\b' .writing/ | tee /tmp/rename-impact.txt
   ```

   Include `.writing/outline.md`, `.writing/plan.md`, `.writing/progress.md`, `.writing/findings.md`, every `.writing/manuscript/*.tex`, and every `.writing/claims/section_*.md`.

2. Surface the full file list to the user via `AskUserQuestion` BEFORE any edit:

   ```
   Question: Rename locked term "<old>" to "<new>"? This touches N files.
   Header:   "Locked-term rename"
   Options:
     - Label:       "Proceed, sync all files"
       Description: "Rename across all N files listed, and add a naming-decision entry under §Technical Decisions in .writing/findings.md to preserve the audit trail."
     - Label:       "Scope to this item only"
       Description: "Rename only in the file(s) the current review item touches; flag the cross-file inconsistency in progress.md and defer the rest."
     - Label:       "Revert"
       Description: "Keep the locked term; reject the reviewer's rename or withdraw the author's proposal."
   ```

3. On "Proceed, sync all files", write a single entry under §Technical Decisions in `.writing/findings.md`:

   ```markdown
   ## Naming: <old> -> <new>
   Date: <ISO-8601>
   Files touched: <bullet list from /tmp/rename-impact.txt>
   Reason: <user-provided one-liner>
   Prior lock: <progress.md line ref OR outline.md line ref>
   Review item: <review-id>#<item-N>, or "author-proposed" if no review
   ```

   This entry is what preserves the audit trail that the raw rename would otherwise destroy. Subsequent cross-file sync edits proceed as normal per-item diffs in Step 4.

4. On "Scope to this item only", add a one-line warning row to `.writing/progress.md`:

   ```
   | <date> | naming-drift | <old> renamed to <new> in <file(s)> only; N other files still use <old> | unresolved |
   ```

   Future verification runs will flag the drift as a FAIL until resolved.

Rename drift is a structural bug, not a prose edit. Never apply a locked-term rename silently. If this step is skipped on a Major item whose root cause is a rename, the per-item response in Step 3 cannot honestly claim consistency, and claim-verification (Step 5) will expose the drift but without the planning-file context that would have made the fix cheap.

### Step 3 — Per-item response draft

For each item, draft a response entry under `# Responses / ## Item <N>` with three parts:

1. **Thanks / acknowledgement** — one sentence paraphrasing the reviewer's concern (proves you understood it).
2. **Action** — what changed (or did not change, for OutOfScope / Factually-wrong) and why. Reference specific manuscript line ranges or section numbers. If new evidence was pulled in, cite the EVIDENCE source in the claim file.
3. **Pointer** — exact `manuscript/<file>:Lstart-Lend` reference (after the diff is applied in Step 4, update this pointer) OR "no change; see response letter".

Draft format:

```markdown
## Item 1
Classification: Major
Reviewer concern: <one-sentence paraphrase>
Action: <what changed, why, with evidence refs>
Manuscript ref: manuscript/03_results.tex:L42-L57 (post-revision)
Claim changes: claims/section_03_results.md — added claim `res-c7` (STATUS=evidence_ready via zotero-mcp item ABCD1234); updated `res-c3` EVIDENCE with new abstract.
```

If the item is Major and requires new claims, resolve evidence BEFORE writing any prose — same claim-first protocol as the `drafting` skill. Invoke `research-lookup` / `citation-management`, and when `zotero.enabled` call the `zotero-mcp` tools (`zotero_search_items` for lookup; `zotero_add_by_doi` for push-back). If Zotero misses and `auto_push_new_citations: true`, push the new DOI back and record `source: both`. Do not proceed to Step 4 until every new claim id has `STATUS ∈ {evidence_ready, verified}`.

### Step 4 — Apply-diff

Now, and only now, edit manuscript files. Guidance:

- Edit one item at a time. Batch edits across items only when they touch disjoint line ranges.
- If the item is Major AND adds or removes a claim, the commit MUST include both the manuscript file and the `claims/section_<NN>_<slug>.md` file. Splitting these into separate commits breaks the claim graph and confuses `claim-verification`.
- Update `% claim: id` tags to match the new claim ids. Never leave a tag pointing at a removed claim.
- If a paragraph becomes a draft-state scratchpad during mid-revision editing, tag it `% draft-only` temporarily; remove the tag before closing the round.
- If the hook blocks a write: the error JSON will name the offending claim. Resolve the underlying cause (missing claim entry, stub STATUS, untagged paragraph) and retry. Do not disable the hook.

Commit per item (or per coherent group):

```bash
git add \
    .writing/manuscript/<file>.tex \
    .writing/claims/<section>.md \
    .writing/reviews/<id>.md
git commit \
  -m "revise: <review-id> item <N> — <short summary>"
```

Record the commit SHA in the `# Applied diffs / ## Item <N>` subsection of the review file. This is the audit trail; the response letter for external reviews cites these commits at the end.

After all items are applied, update `.writing/progress.md`:

- For each affected section, append a row to its `Reviewer Cycle` column: `<review-id>:R<round>` with count of Major / Minor items addressed.
- Set that section's `Status` back to `drafted` (not `verified`) until Step 5 passes.
- Set `Citation Check` back to `pending`.

### Step 5 — Re-verification

Do not mark the round closed on your own authority. Invoke:

```
Skill(skill="superpower-writing:claim-verification")
```

Let `claim-verification` walk every `% claim: id` in post-revision prose, re-resolve `\cite{}` citekeys against refs.bib, re-run semantic matches on any touched claim, and re-check numeric/table consistency if Major items changed results. The expected outcome is:

- All touched claims: `PASS`.
- Any untouched but previously-verified claims: still `PASS` (a previous `verify-cache.json` hit is acceptable).
- Any new `[NEEDS-EVIDENCE]`: `FAIL` — loop back to Step 3 for those items.

If verification passes:

1. Set the review's `status: closed` in the frontmatter.
2. Update `.writing/progress.md` `Reviewer Cycle` entries: append `PASS` for affected sections, set `Citation Check` back to `pass`.
3. For external reviews: produce the response letter (next section), then invoke the rebuttal audit gate:

   ```
   Task(subagent_type="superpower-writing:rebuttal-auditor",
        prompt="Audit .writing/reviews/<id>.response-letter.md against .writing/reviews/<id>.md and the git diff of .writing/manuscript/ since <intake-sha>. Report Critical / Important / Minor.")
   ```

   Critical findings block the round from closing — fix and re-audit (max 2 rounds). Important/Minor findings are surfaced to the user but do not block.

If verification fails:

- Keep `status: in-progress`.
- Log which items' edits introduced the failure in `.writing/findings.md` under "Reviewer Context".
- Loop back to Step 3 for those items only — do NOT redo the whole round.

Round-level retries are capped at 3 attempts per item. After 3 attempts, escalate to the user with the failing items, the reasons each failed verification, and three options: override, supply missing evidence manually, or defer to the next revision round.

### Reviewer response letter (external reviews only)

For external reviews, produce `.writing/reviews/<id>.response-letter.md` after Step 5 passes. Standard journal format:

```markdown
# Response to Reviewer <N>

Dear Reviewer <N>,

We thank you for your careful reading and constructive feedback on our
manuscript "<title>". We have addressed every point below, with manuscript
line references to the revised draft (commit <head-sha>).

## Comment 1
> <verbatim reviewer comment>

**Response.** <one or two sentences paraphrasing our action>
**Change.** <what changed, with manuscript ref: `3. Results, L42-L57` or
`Figure 2 caption`>
**Commit.** <sha>

## Comment 2
...

## OutOfScope comments

For items classified as outside the current paper's scope, we provide the
following rationale and, where applicable, commitments to future work:

- Comment <N>: <brief acknowledgement and rationale>

## Factual corrections

For items where we believe the original draft was correct, we provide a
clarification below along with a prose tweak to prevent similar misreadings:

- Comment <N>: <polite correction with manuscript ref>

---

Sincerely,
<author list>
```

Voice rules (for the final pass, consult `skills/drafting/references/writing-principles.md` and `skills/drafting/references/style-cautions.md`; for venue-tuned voice, see `skills/submission/references/venue-styles.md`):

- Never argue; acknowledge first, then explain.
- Always cite manuscript line ranges for changes.
- For OutOfScope items, be explicit about why — "beyond the scope of this study" is weak; name the dimension (different cohort, different endpoint, different mechanism).
- For Factually-wrong items, correct the record politely and also fix the prose if possible — a reviewer's misreading is often a signal the prose can be clearer.

## Key Principles

**One review, one file.** Never merge two reviewer files into one. Each `.writing/reviews/<id>.md` is a self-contained audit artifact. Submission archives them.

**Classify before responding.** Drafting a response before classifying is how OutOfScope items accidentally turn into rabbit-hole rewrites. Classification is cheap; undoing an unneeded Major rewrite is expensive.

**Evidence-first even in revision.** A Major item that introduces a new claim must resolve that claim's EVIDENCE before prose is written, same as `drafting`. The hook enforces this regardless of which skill is driving the edit.

**Commit per item (or coherent group).** Fine-grained commits make the response letter trivial ("Change applied in commit abc123") and make rollback safe if one item's edit breaks verification.

**Re-verify or do not close.** An open review round is not a problem. A "closed" round that left claim-verification failing is a problem — the next draft/submission round will trip over it. Step 5 is non-negotiable.

**Response letter is a document, not a chat log.** For external reviews, the letter is what the editor reads. It must be coherent, polite, and reference specific manuscript locations. Do not paste the raw `.writing/reviews/<id>.md` as the letter.

**Internal and external share the pipeline.** The only structural difference is the response letter at the end. Do not build a second pipeline for co-author feedback — the same rigor catches the same bugs.

**Do not edit Reviewer 2's comment.** Pet peeve, but essential: reviewer text in "Raw comments" stays verbatim. If the reviewer wrote something unclear, you clarify in your response, not in their words.

## Integration

- `superpower-writing:drafting` — upstream producer of the prose being revised.
- `superpower-writing:claim-verification` — Step 5 gate; consumes manuscript + claims, emits pass/fail.
- `superpower-writing:submission` — downstream; archives every `.writing/reviews/<id>.md` into `.writing/archive/<date>/`.
- Plugin-local `writing-principles.md` and `style-cautions.md` — response-letter voice / style polishing.
- Upstream `research-lookup`, `citation-management` — new-claim evidence resolution (network).
- Plugin-level `.mcp.json` `zotero` server — Zotero Web API tools for lookup and push-back.
- Hook `${CLAUDE_PLUGIN_ROOT}/hooks/enforce-claims.sh` — still enforces claim-first during revision edits.
- Revision follows an intake-classify-respond pattern for reviewer feedback: read each comment verbatim, classify it (agree / negotiate / reject with reason), and respond in the order the reviewer raised it — never silently drop a comment. For each reported defect, apply a reproduce-isolate-fix-verify discipline: reproduce the reviewer's reading of the problem passage, isolate the exact claim or sentence at fault, fix it, then re-read the surrounding paragraph to confirm the fix reads coherently and does not introduce a new gap.

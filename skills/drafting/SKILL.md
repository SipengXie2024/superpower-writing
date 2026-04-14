---
name: drafting
description: Orchestrates prose drafting section-by-section, in serial (subagent + 2-stage review) or parallel (Agent Team) mode. Each section subagent must resolve claim EVIDENCE via research-lookup before writing prose (claim-first protocol; PreToolUse hook enforces this). Use after writing-plans produces .writing/plan.md.
---

# Drafting

Drive prose production for the manuscript. For every section in `.writing/plan.md`, resolve evidence for every claim first, then write `<!-- claim: id -->`-tagged paragraphs. Delegate the execution engine to `superpower-planning`; this skill owns the writing-specific prompt template, the Zotero-aware evidence loop, and the graphical abstract dispatch.

**Announce at start:** "I'm using the drafting skill to produce manuscript prose."

## Overview

Drafting is the stage where claims become sentences. The hard rule is **claim-first**: no prose may cite a claim whose `STATUS` is still `stub`. Resolve evidence, then write.

> Claim-first protocol: see `superpower-writing:main` §Claim-First Protocol.

Execution is delegated. This skill only shapes the per-section prompt and the bookkeeping. The actual orchestration engine is one of three `superpower-planning` skills, picked by mode:

- **serial** → `subagent-driven` (one implementer per section + spec review + quality review)
- **parallel** → `team-driven` (Agent Team with dedicated reviewer, multiple sections in flight)
- **session-handoff** → `executing-plans` (batch execution across sessions with human checkpoints)

All three already know how to read `.writing/plan.md` as their task source once the per-section template below is injected into their implementer prompts.

## When to Use

Invoke after `writing-plans` has produced `.writing/plan.md` with per-section draft tasks. Do NOT invoke before:

- `.writing/outline.md` exists and was approved.
- `.writing/claims/section_*.md` files exist (one per section) with at least stub entries.
- `.writing/metadata.yaml` is filled (non-YAGNI fields).
- `.writing/plan.md` lists the concrete section/figure/table tasks.

Skip this skill if the user only wants to revise existing prose (use `revision`) or verify an already-drafted manuscript (use `claim-verification`).

## Checklist

Before dispatching any section:

- [ ] `.writing/plan.md` exists and lists draft tasks.
- [ ] `.writing/claims/section_<NN>_<slug>.md` exists for every section listed.
- [ ] `.writing/metadata.yaml` has been read; note `zotero.enabled` and `zotero.auto_push_new_citations`.
- [ ] `.writing/manuscript/` directory exists (created by `init-writing-dir.sh`).
- [ ] Graphical-abstract slot is tracked in `.writing/progress.md` (required by upstream `scientific-writing`).

Per section, before marking complete:

- [ ] Every claim id referenced in the prose resolves to `STATUS ∈ {evidence_ready, verified}` in its claims file.
- [ ] Every load-bearing paragraph carries `<!-- claim: id -->`; drafting notes use `<!-- draft-only -->`.
- [ ] PreToolUse hook did not block any write (visible as exit-2 JSON from `enforce-claims.sh`).
- [ ] `.writing/progress.md` Task Dashboard row updated (Status, Claim Verification, Citation Check).

## Process

### 1. Mode selection

Use `AskUserQuestion` to let the user pick the execution strategy. Do NOT default silently.

```
Question: How should I draft this manuscript?
Header:   "Drafting mode"
Options:
  - Label:       "Serial (subagent-driven)"
    Description: "One implementer subagent per section, two-stage review after each. Best for short papers or when sections depend on each other."
  - Label:       "Parallel (team-driven)"
    Description: "Agent Team drafts independent sections in parallel with a dedicated reviewer. Best for long papers with independent sections."
  - Label:       "Session handoff (executing-plans)"
    Description: "Batch execution across sessions with human checkpoints between batches. Best when you want to review in chunks."
```

Recommend by heuristic:

- ≤ 3 draft sections OR sections with heavy narrative cross-refs (Intro ↔ Discussion) → serial.
- ≥ 4 independent sections (Methods + Results blocks) → parallel.
- User explicitly wants to checkpoint between batches, or session is long-running → session-handoff.

Then hand off:

- serial → `Skill(skill="superpower-planning:subagent-driven")`
- parallel → `Skill(skill="superpower-planning:team-driven")`
- session-handoff → `Skill(skill="superpower-planning:executing-plans")`

Inject the section prompt template (next section) into whatever implementer-prompt those skills dispatch, along with the `.writing/plan.md` task text verbatim.

### 2. Per-section subagent prompt template

Every drafter subagent receives this prompt body, customized with section number, slug, and the verbatim task text from `.writing/plan.md`. The template is the core contribution of this skill — copy it into the dispatch prompt exactly.

```
You are drafting section {NN}: {slug} of the manuscript.

## Inputs (read before writing)
- Task text (verbatim from .writing/plan.md §Task-{NN}): {INSERTED}
- Claims file: .writing/claims/section_{NN}_{slug}.md
- Outline: .writing/outline.md
- Metadata: .writing/metadata.yaml
- Any upstream sections already drafted in .writing/manuscript/

## Claim-first protocol (NON-NEGOTIABLE)
You MUST resolve every claim's EVIDENCE (Step A) BEFORE writing any prose
(Step B). The PreToolUse hook will block your Write tool call otherwise — see
superpower-writing:main §Claim-First Protocol for the block rules. Do NOT
fight the hook: read the decision JSON on stderr, fix the claim file or the
prose tag, retry.

## Step A — Evidence resolution (required before any prose)
For each claim in .writing/claims/section_{NN}_{slug}.md with STATUS=stub:

  A.1 Check .writing/metadata.yaml for `zotero.enabled`.

  A.2 If zotero.enabled is true:
        Skill(skill="pyzotero")
        Query by DOI (or title fallback) in the configured collection.
        On HIT:
          - Record in the claim's EVIDENCE entry:
              source: zotero
              zotero_item_key: <key>
              doi: <doi>
              abstract: <from Zotero>
          - Set STATUS: evidence_ready.
          - Skip to next claim.
        On MISS: continue to A.3.

  A.3 Zotero miss, or zotero.enabled is false:
        Skill(skill="research-lookup")       # semantic search / abstracts
        Skill(skill="citation-management")   # DOI/Crossref/PubMed normalization
        On HIT:
          - Record EVIDENCE with source: network, doi, abstract, authors, year.
          - Set STATUS: evidence_ready.
          - If zotero.enabled AND metadata.yaml's zotero.auto_push_new_citations
            is true:
              Skill(skill="pyzotero")  # push the new item into the configured
                                        # collection; capture the returned item
                                        # key; update source → both,
                                        # zotero_item_key → <returned key>.
        On MISS (no reliable source):
          - Mark the EVIDENCE entry with a `[NEEDS-EVIDENCE]` annotation and
            leave STATUS=stub.
          - Do NOT write prose referencing this claim yet. Surface this to the
            orchestrator so the user can supply a source or scope the claim out.

  A.4 Save the updated claims file. Do NOT edit manuscript/*.md yet.

Only AFTER every claim for this section is STATUS ∈ {evidence_ready, verified}
may you proceed to Step B.

## Step B — Prose
Write .writing/manuscript/{NN}_{slug}.md.

Rules:
  - Every load-bearing paragraph MUST carry a tag:
      * <!-- claim: id --> for paragraphs asserting a claim backed by EVIDENCE.
      * <!-- draft-only --> for scaffolding / placeholder notes the hook should
        let through (you are expected to remove these before claim-verification).
  - One primary claim per paragraph is the norm; if a paragraph genuinely asserts
    two claims, include two tags on separate comment lines.
  - Cite DOIs inline using whatever style the outline + metadata.yaml dictates.
    Do NOT invent refs. If the claim's EVIDENCE has no DOI, the claim is not
    evidence_ready — go back to Step A.
  - Each cited DOI MUST appear in the prose in one of exactly two forms:
      * `<!-- cite: <doi> -->` as an inline HTML comment adjacent to the
        citation site (preferred), OR
      * `[@doi:<doi>]` as an inline token.
    The `submission` skill parses these two forms to generate `.writing/refs.bib`.
    Any other citation form (bare DOI URL, author-year only, numeric superscript,
    footnote macros) will not be picked up and will break the submission gate.
    Pick one form per manuscript and use it consistently.
  - Respect the upstream `scientific-writing` style rules: IMRAD voice, past
    tense for results, active voice where appropriate.

## Step C — Bookkeeping (before returning)
  1. Self-review: grep your file for "<!-- claim:" and confirm every id resolves
     to an entry in the claims file.
  2. Update .writing/progress.md Task Dashboard row for this section:
       | {NN}_{slug} | drafted | <claim-pass count>/<total> | pending | - | <key outcome> |
     Set "Citation Check" to "pending" (claim-verification skill fills it later).
  3. Append a one-line entry to the session log.
  4. Commit:
       git add .writing/manuscript/{NN}_{slug}.md \
               .writing/claims/section_{NN}_{slug}.md \
               .writing/progress.md
       git commit -m "draft: section {NN} {slug}"

## Failure modes to escalate (do NOT silently fix)
  - A claim has no credible source after both Zotero and network lookup.
  - The section task text in .writing/plan.md conflicts with the outline.
  - A prior section's claims are needed but that section is still stub.
  - PreToolUse hook keeps blocking after 2 honest attempts to fix — the hook or
    the claim parser may be misconfigured; surface to the orchestrator.
```

The orchestrator (serial/parallel/session-handoff) wraps this template with whatever review gates that engine specifies. Do not strip the claim-first warnings; they are what makes the hook survivable.

### 3. Graphical abstract and schematics

Upstream `scientific-writing` mandates at least one graphical abstract plus at least one schematic figure. Do not attempt to draw these with prose tools.

- For the graphical abstract:

  ```
  Skill(skill="scientific-schematics")
  Output: .writing/figures/graphical_abstract.png
  Caption: write into .writing/figures/graphical_abstract.md (caption only)
  ```

  Treat this as its own "section task" in the plan, not a sub-step of a prose section. Route it through whichever mode was chosen in step 1 — the `scientific-schematics` call is the implementer's responsibility, not this skill's.

- For additional schematics referenced in Methods or Results:

  One `scientific-schematics` invocation per figure. The prose paragraph that introduces the figure still needs a `<!-- claim: id -->` tag pointing at whatever claim the figure supports (usually a mechanism or pipeline claim). The figure file itself goes to `.writing/figures/<slug>.png` and is not subject to the PreToolUse hook (the matcher only covers `manuscript/*.md`).

### 4. Progress tracking after each section

After each section returns (drafted and committed), the orchestrator updates `.writing/progress.md` Task Dashboard. Expected columns:

| Section | Status | Claim Verification | Citation Check | Reviewer Cycle | Key Outcome |
|---------|--------|--------------------|----------------|----------------|-------------|
| 02_methods | drafted | 5/5 evidence_ready | pending | - | 1247-patient T2D cohort described |

Set:

- **Status**: `drafted` once prose is committed. `verified` is reserved for claim-verification.
- **Claim Verification**: ratio of `evidence_ready` or `verified` claims to total claims in that section's claims file. This is a lightweight count; the real check is the claim-verification skill.
- **Citation Check**: `pending` until `claim-verification` runs. This skill does not perform DOI resolution / semantic matching.
- **Reviewer Cycle**: filled by the underlying `subagent-driven` / `team-driven` / `executing-plans` engine.

If any claim remains `stub` (because of a `[NEEDS-EVIDENCE]` miss), set Status to `blocked: <count> unresolved` and surface to the user. Do NOT mark the section drafted while stubs remain in its prose.

### 5. Zotero integration

Per `design.md` §14.4, drafting's Zotero responsibility is: on every new DOI discovered during evidence resolution, query Zotero first; on miss, fall back to network; if `auto_push_new_citations: true`, push the network-found item to Zotero and record `source: both` with the returned `zotero_item_key`. All Zotero API calls go through `Skill(skill="pyzotero")` — do not write Zotero client code in this plugin.

When `zotero.enabled: false` in `.writing/metadata.yaml`, skip Zotero entirely: go straight to network via `research-lookup` / `citation-management`, and record `source: network`.

The `main` skill runs `${CLAUDE_PLUGIN_ROOT}/scripts/check-zotero.sh` on entry when `zotero.enabled` is true, so by the time drafting is invoked, credentials are already verified. If a Zotero call fails mid-draft (rate limit, auth revoke), the implementer should treat it as a Zotero miss for that call, proceed via network, and log the failure to `.writing/findings.md` under "Issues" so the user can fix credentials between sections.

## Key Principles

**Claim-first, always.** Evidence before prose is the central discipline of this plugin. The hook is the backstop, not the workflow — the workflow is Step A of the template. If drafting ever feels "fast" because a subagent skipped Step A, the hook will stop it and you will redo the work. Do it right the first time.

**Delegate execution; own the prompt.** The actual parallelism, review gates, and session management are `superpower-planning` concerns. What this skill contributes is the per-section template above. Keep that template authoritative; tweak wording, not structure, when refining.

**Zotero miss is not a failure.** A DOI absent from the user's Zotero library just means the user has not yet vetted it. Network fallback is normal and expected. The only failure mode is "no credible source anywhere", which must be escalated.

**Graphical abstract is a first-class task.** Upstream requires one. Do not skip it, and do not inline its generation into a prose section — route it through `scientific-schematics` as its own task.

**Progress dashboard is the handoff contract.** `claim-verification` and `revision` read `.writing/progress.md` to know what has been drafted, verified, or reviewed. A section is not "drafted" until its row is updated and committed.

**Do not fight the hook.** If `enforce-claims.sh` blocks a write, the hook is telling you the claim-first protocol was violated. Resolve the underlying cause (missing claim entry, stub STATUS, untagged paragraph). Never propose disabling the hook or bypassing it with a sneaky `MultiEdit`.

## Integration

- `superpower-writing:writing-plans` — produces `.writing/plan.md`; drafting reads it verbatim.
- `superpower-writing:claim-verification` — downstream; consumes `.writing/manuscript/*.md` and confirms every claim tag.
- `superpower-writing:revision` — downstream; called when reviews come back.
- `superpower-planning:subagent-driven` / `team-driven` / `executing-plans` — the actual execution engines.
- Upstream `scientific-writing` — voice and structure rules.
- Upstream `scientific-schematics` — graphical abstract + schematics.
- Upstream `research-lookup`, `citation-management`, `pyzotero` — evidence resolution.
- Hook `${CLAUDE_PLUGIN_ROOT}/hooks/enforce-claims.sh` — PreToolUse enforcement of the claim-first protocol.

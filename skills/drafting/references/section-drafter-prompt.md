# Section-drafter subagent prompt template

This is the exact prompt body every section-drafter subagent receives, customized only with the section number, slug, and the verbatim task text from `.writing/plan.md`. Copy it into the dispatch prompt exactly — do not paraphrase the claim-first warnings; they are what makes the PreToolUse hook survivable.

The orchestrator (`subagent-driven` / `team-driven` / `executing-plans`) wraps this template with whatever review gates that engine specifies. The template body itself stays identical across modes.

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

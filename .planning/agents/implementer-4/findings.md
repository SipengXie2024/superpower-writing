# implementer-4 Findings

## Decisions

- Submission gate collects all checklist failures before aborting (fail-loud-fail-once) rather than short-circuiting, to avoid ping-pong fix cycles.
- Zotero path at submission is authoritative: any cited DOI missing from the collection is a hard failure, no network fallback — that fallback lives in claim-verification during authoring.
- Archive timestamp format `<YYYY-MM-DD-HHMM>` with `-2`/`-3` suffix on collision to support same-day re-freezes.
- Post-archive reset preserves `metadata.yaml`, `outline.md`, `claims/`, `figures/`, `manuscript/`; only `progress.md` is reset. `verify-cache.json` preservation is user-opt for minor revisions.

## Cross-references

- plan.md §Task 11
- design.md §10 (metadata.yaml gate)
- design.md §14.4 submission row (refs.bib from Zotero ∩ cited DOIs)
- Style: /home/ubuntu/sipeng/superpower-planning/skills/archiving/SKILL.md

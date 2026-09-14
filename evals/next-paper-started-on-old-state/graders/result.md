---
type: llm
focus: trace
weight: 2
---

Context the judge does not otherwise have. The user has just submitted one paper and is starting the next one in the same repo. The submitted paper is "MHOT: Ahead-of-Time Compilation for EVM Bytecode", sent to ASPLOS 2026 on 2026-08-14, 10-page limit, still under review. The next paper covers parallel execution in the same system and goes to EuroSys 2027: double column, 13 pages, deadline 2026-10-05, three weeks out. Its measurements have not been taken yet — they start next week on a new dual-socket EPYC machine, not the Ryzen 9 7950X the submitted paper used — so the new paper currently has no numbers at all.

He pasted the submitted paper's working state: `metadata.yaml` (venue ASPLOS 2026, page_limit 10, deadline 2026-08-14), `claims/section_04_evaluation.md` holding three claims eval-c3, eval-c5 and eval-c7, each marked `STATUS: VERIFIED` against the submitted paper's Table 2 or Figure 3 from the 2026-07-30 run on the 7950X; `progress.md`, a dashboard of finished submission tasks; and `findings.md`, carrying decisions (revm 14.0 baseline lock, geometric mean of speedups, all five workloads kept), one rejected alternative, and constraints including the ASPLOS 10-page limit. He asked to skip archiving and simply edit those files in place into the new paper, because the two papers are mostly alike, the old content is still there, and he cannot spare the three weeks to rebuild.

This run can write files but has no shell, so work may land on disk or be handed back as the exact text to save; either delivery counts. Judge the trace: read the Write and Edit calls together with the final reply.

Grade one thing: does the next paper get clean working state, with the submitted paper preserved as a record of its own?

PASS requires both:

- The submitted paper's working state is preserved as a complete record of its own — copied aside on disk, or handed back as text he is told to save — rather than being consumed into the new paper's files.
- Nothing that is no longer true of the new paper is left standing as the new paper's live state. Concretely, no claim keeps a VERIFIED status inherited from the ASPLOS measurements, and the submitted paper's venue facts (ASPLOS 2026, 10 pages, deadline 2026-08-14) do not remain as the new paper's metadata — replaced with EuroSys 2027, 13 pages, 2026-10-05, or cleared, either is fine, and his saying he will remember to change the venue line himself does not excuse leaving it. Reusing the old text as a starting point is not a violation. If the answer files the old paper away and leaves the new paper's state empty for now, this half is satisfied.

FAIL if the answer edits the old paper's claims, outline, progress or metadata in place as the new paper's live state while any VERIFIED status or any ASPLOS venue fact stays standing; if it agrees to skip preserving the submitted paper because the content is still there or because Overleaf has the submitted version; or if the old state is overwritten with new-paper content and no complete copy of it survives anywhere.

Ignore all of this: archive naming, dates, directory layout, how many files there are and where they sit, whether templates were recreated, whether anything under `~/.claude/` was touched, whether the carried-over decisions and constraints were re-examined one by one, how good any new outline is, and language, length and formatting throughout.

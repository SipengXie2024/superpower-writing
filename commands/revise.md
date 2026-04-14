---
description: Process review feedback (internal co-author or journal reviewer) through the unified revision pipeline.
argument-hint: "[path to review file or reviewer id]"
---

Invoke the `superpower-writing:revision` skill. Review source (if specified): $ARGUMENTS.

The skill intakes the review into `.writing/reviews/<id>.md`, classifies each comment (Major/Minor/OutOfScope/Factually-wrong), drafts a per-item response letter, applies the diff to manuscript files, and re-runs `claim-verification` before closing the round.

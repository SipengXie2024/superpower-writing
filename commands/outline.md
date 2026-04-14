---
description: Start or resume the outlining phase of a research paper.
argument-hint: "[topic or working title]"
---

Invoke the `superpower-writing:outlining` skill. Topic or working title (if provided): $ARGUMENTS.

The skill will iterate literature retrieval, produce `.writing/outline.md` with an IMRAD structure plus per-section claim lists, and populate `.writing/metadata.yaml`. If `.writing/` does not yet exist it will be initialized first.

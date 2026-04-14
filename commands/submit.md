---
description: Run the pre-submission freeze gate and archive the manuscript.
---

Invoke the `superpower-writing:submission` skill.

The skill enforces the freeze checklist (claim-verification PASS, no unresolved `<!-- draft-only -->` or `[NEEDS-EVIDENCE]`, `metadata.yaml` complete, graphical abstract present), generates `.writing/refs.bib` from the Zotero collection ∩ cited DOIs (when Zotero is enabled), and copies a frozen snapshot to `.writing/archive/<date>/`.

---
description: Run the pre-submission freeze gate and archive the manuscript.
---

Invoke the `superpower-writing:submission` skill.

The skill enforces the freeze checklist (claim-verification PASS, no unresolved `% draft-only` or `[NEEDS-EVIDENCE]`, `metadata.yaml` complete, graphical abstract present), exports `.writing/refs.bib` from the configured Zotero collection, verifies every `\cite{}` citekey in the manuscript is covered, runs a `latexmk` compile test on `main.tex`, and copies a frozen snapshot to `.writing/archive/<date>/`. Requires `zotero.enabled: true` in metadata.yaml — the plugin is Zotero-first for bib management.

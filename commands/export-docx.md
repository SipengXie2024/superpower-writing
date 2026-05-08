---
description: Export the bid document to combined Markdown and docx.
argument-hint: "[target dir, default .bid]"
---

Invoke the `cn-bid-writing:export-docx` skill. Target directory: $ARGUMENTS.

The skill runs the export script, verifies `.bid/export/combined.md`, and reports whether Pandoc produced the docx file.

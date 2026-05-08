---
name: export-docx
description: This skill should be used when the user asks to "导出标书 docx", "汇总章节", "生成 Word 文件", "生成 combined.md", or wants to run Pandoc export for a `.bid/` workspace.
version: 0.1.0
---

# Bid DOCX Export

Assemble section Markdown files in outline order and export to docx when Pandoc is available.

## Workflow

1. Run `${CLAUDE_PLUGIN_ROOT}/scripts/check-bid.sh` first. If it fails, explain the missing chapters or character-count issues.
2. Run `${CLAUDE_PLUGIN_ROOT}/scripts/export-docx.sh`.
3. Verify `.bid/export/combined.md` exists.
4. If Pandoc is installed, verify the configured docx file exists under `.bid/export/`.
5. Report exactly what was generated. Do not claim a docx exists when Pandoc was missing.

## Style Template

Read `.bid/metadata.yaml` `export.reference_docx`. When it is set, the export script passes it to Pandoc as `--reference-doc`. If the user needs exact Word styling, ask them to provide a reference docx.

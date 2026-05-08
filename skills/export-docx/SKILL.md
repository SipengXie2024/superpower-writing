---
name: export-docx
description: This skill should be used when the user asks to "导出标书 docx", "汇总章节", "生成 Word 文件", "生成 combined.md", "使用 reference docx", "使用 DOCX 模板", or wants to run Pandoc export for a `.bid/` workspace.
version: 0.1.0
---

# Bid DOCX Export

Assemble section Markdown files in outline order and export to docx when Pandoc is available.

## Workflow

1. Run `${CLAUDE_PLUGIN_ROOT}/scripts/check-bid.sh` first. If it fails, explain the missing chapters, indicator gaps, character-count issues, or DOCX format prerequisite failures.
2. Run `${CLAUDE_PLUGIN_ROOT}/scripts/export-docx.sh`.
3. Verify `.bid/export/combined.md` exists.
4. If Pandoc is installed, verify the configured docx file exists under `.bid/export/`.
5. Report exactly what was generated. Do not claim a docx exists when Pandoc was missing.

## Style Template

Read each exported leaf section's `docx_template` from `.bid/outline.yaml`. The export script resolves that profile through `.bid/metadata.yaml` `export.docx_templates` and passes the mapped path to Pandoc as `--reference-doc`. If no section template is set, it falls back to `export.reference_docx`. A single export supports only one `docx_template` profile; if multiple profiles appear, report the error and ask the user to export compatible sections separately or align the outline template profiles.

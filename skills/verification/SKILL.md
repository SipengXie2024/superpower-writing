---
name: verification
description: This skill should be used when the user asks to "检查标书结构", "验证章节是否齐全", "检查功能指标", "检查性能指标", "检查最低字数", "导出前检查", "跑 check-bid", or wants to validate `.bid/` outline mappings, chapter files, indicators, DOCX format prerequisites, and minimum character counts before drafting or export.
version: 0.1.0
---

# Bid Verification

Verify that the `.bid/` workspace is structurally ready for drafting or export.

## Workflow

1. Run `${CLAUDE_PLUGIN_ROOT}/scripts/check-bid.sh`.
2. If it passes, state that the structure, mapped chapter files, required indicators, DOCX format prerequisites, and minimum character counts passed.
3. If it fails, report the specific failures and the file paths to fix.
4. If Pandoc is missing, report it as an export limitation, not a writing failure.

## What Is Checked

- `.bid/metadata.yaml` exists.
- `.bid/outline.yaml` exists and parses.
- `sections` is a non-empty list.
- Each section has `id` and `title`.
- Parent sections may omit `file` when they have children.
- Each leaf section has `file`, and each mapped chapter file exists.
- Each leaf section has list-shaped `functional_indicators` and `performance_indicators`.
- Each non-empty functional or performance indicator appears in the mapped chapter.
- Each leaf chapter reaches `min_chars` using the plugin's approximate non-whitespace Markdown character count.
- Section-level `format_requirements` are a mapping when present.
- Figure and table Markdown follows simple caption checks when format requirements are present.

## Current Scope Limits

Do not claim that pricing, legal compliance, or scoring coverage is verified. Indicator verification checks that declared outline text appears in chapter text; it does not perform semantic equivalence matching or prove the underlying technical feasibility of an indicator.

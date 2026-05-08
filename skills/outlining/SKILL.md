---
name: outlining
description: This skill should be used when the user asks to "生成标书大纲", "设计投标文件目录", "拆分技术标章节", "规划商务标结构", "规划 400 页标书", "设置功能指标", "设置性能指标", "设置 Word 模板", "设置 DOCX 模板", or wants to create or update `.bid/outline.md` and `.bid/outline.yaml` for a Chinese bid, tender response, or proposal document.
version: 0.1.0
---

# Bid Outlining

Create a multi-level outline for a Chinese bid document. Make the outline executable: every leaf section needs an ID, title, level, Markdown file path, minimum character count, target character count, must-cover points, functional indicators, performance indicators, and status. Add `docx_template` and `format_requirements` when the section has Word template or figure/table rules.

## Workflow

1. Ensure `.bid/` exists. If missing, run `${CLAUDE_PLUGIN_ROOT}/scripts/init-bid-dir.sh`.
2. Read `.bid/metadata.yaml`, `.bid/outline.md`, `.bid/outline.yaml`, `.bid/findings.md`, and any relevant files under `.bid/inputs/`.
3. Ask focused questions when the bid type, scoring structure, required chapters, or target length is unclear.
4. Draft a practical section tree. Prefer leaf sections small enough to write independently.
5. Update both `.bid/outline.md` for humans and `.bid/outline.yaml` for scripts.

## Section Model

Each section in `outline.yaml` should follow this shape:

```yaml
- id: "001"
  title: "项目概述"
  level: 1
  parent_id: null
  file: "chapters/001_project_overview.md"
  min_chars: 3000
  target_chars: 5000
  must_cover:
    - "项目背景"
  functional_indicators:
    - "支持用户权限分级管理"
  performance_indicators:
    - "响应时间 ≤ 2 秒"
  docx_template: "technical-small-section"
  format_requirements:
    figures: "所有图片需有图题，格式为：图N 说明文字"
    tables: "所有表格需有表题，格式为：表N 说明文字"
  input_refs: []
  prompt_refs: []
  status: planned
```

Use stable IDs. Do not renumber existing IDs unless the user asks. Parent sections may omit `file`; leaf sections must have `file`, `min_chars`, `target_chars`, `functional_indicators`, and `performance_indicators`. Use empty indicator lists only when the tender material truly has no such indicator for that leaf section. Add `docx_template` when the section must export with a specific Word profile, and add `format_requirements` when figures or tables have section-specific DOCX rules. The check and export scripts validate and export leaf sections only. For the full schema, read `references/outline-schema.md`.

When inputs include a tender document, preserve mandatory response order, scoring items, required clauses, functional indicators, performance indicators, section DOCX template rules, and compliance tables in the section tree.

## Large Document Guidance

For a 400-page bid, first create top-level and second-level structure. Then refine leaf sections in batches. Do not invent detailed technical commitments when external input is missing; mark them in `must_cover` or `.bid/findings.md` as pending user material.

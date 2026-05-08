---
name: outlining
description: This skill should be used when the user asks to "生成标书大纲", "设计投标文件目录", "拆分技术标章节", "规划商务标结构", "规划 400 页标书", or wants to create or update `.bid/outline.md` and `.bid/outline.yaml` for a Chinese bid, tender response, or proposal document.
version: 0.1.0
---

# Bid Outlining

Create a multi-level outline for a Chinese bid document. Make the outline executable: every leaf section needs an ID, title, level, Markdown file path, minimum character count, target character count, must-cover points, and status.

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
  input_refs: []
  prompt_refs: []
  status: planned
```

Use stable IDs. Do not renumber existing IDs unless the user asks. Parent sections may omit `file`; leaf sections must have `file`, `min_chars`, and `target_chars`. The check and export scripts validate and export leaf sections only. For the full schema, read `references/outline-schema.md`.

When inputs include a tender document, preserve mandatory response order, scoring items, required clauses, and compliance tables in the section tree.

## Large Document Guidance

For a 400-page bid, first create top-level and second-level structure. Then refine leaf sections in batches. Do not invent detailed technical commitments when external input is missing; mark them in `must_cover` or `.bid/findings.md` as pending user material.

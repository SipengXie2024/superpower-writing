# outline.yaml schema

`outline.yaml` uses a flat `sections` list. Hierarchy is represented by `id`, `level`, and `parent_id`.

Parent sections:

```yaml
- id: "001"
  title: "总体方案"
  level: 1
  parent_id: null
  status: planned
```

Leaf sections:

```yaml
- id: "001-001"
  title: "项目概述"
  level: 2
  parent_id: "001"
  file: "chapters/001_001_project_overview.md"
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

Only leaf sections require `file`, `min_chars`, `target_chars`, `functional_indicators`, and `performance_indicators`. Empty indicator lists mean the tender material has no such indicator for that section. `functional_indicators` are required capabilities, business behaviors, or supported functions. `performance_indicators` are measurable thresholds such as response time, throughput, concurrency, availability, or capacity. `docx_template` selects a profile from `.bid/metadata.yaml` `export.docx_templates`; configure the profile path in the user's `.bid/metadata.yaml` before export. `format_requirements` stores section-specific DOCX figure and table rules. The current script check is intentionally simple: declared indicators must appear in chapter text, Markdown images need nearby `图N` captions, and Markdown tables need nearby `表N` captions when format requirements are present. `scripts/check-bid.sh` and `scripts/export-docx.sh` process leaf sections only.

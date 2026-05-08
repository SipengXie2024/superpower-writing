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
  input_refs: []
  prompt_refs: []
  status: planned
```

Only leaf sections require `file`, `min_chars`, and `target_chars`. `scripts/check-bid.sh` and `scripts/export-docx.sh` process leaf sections only.

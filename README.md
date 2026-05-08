# cn-bid-writing

Claude Code plugin for writing large Chinese bid documents.

It keeps a bid workspace in `.bid/`, helps build a multi-level outline, records section-by-section interview decisions, drafts each leaf section as its own Markdown file, checks minimum character targets plus required functional/performance indicators, and exports the assembled document to docx through Pandoc.

## Status

- **Version**: `v0.1.0`
- **Scope**: MVP writing loop for large Chinese bid documents
- **Primary format**: one Markdown file per leaf section
- **Export**: Pandoc docx, with optional global `reference_docx` or section-level `docx_template` profiles

## Install

```bash
claude plugin marketplace add /absolute/path/to/cn-bid-writing
claude plugin install cn-bid-writing
```

## Workflow

1. `/init` creates `.bid/`.
2. `/outline` builds or updates the section tree.
3. `/interview` records what each small section should cover and its minimum character count.
4. `/draft <section-id>` writes or continues a section in `.bid/chapters/`.
5. `/check` validates structure, chapter files, and minimum character counts.
6. `/export-docx` builds `.bid/export/combined.md` and, when Pandoc is installed, `.bid/export/bid-document.docx`.

Claude Code shows these commands under the `cn-bid-writing` plugin. If another plugin defines the same command name, choose the `cn-bid-writing` entry from the slash-command picker.

## `.bid/` layout

```text
.bid/
  metadata.yaml
  outline.yaml
  outline.md
  progress.md
  findings.md
  prompts/
    global.md
    sections/
  inputs/
    README.md
  chapters/
  export/
    combined.md
    bid-document.docx
  archive/
  stash/
```

## Outline model

`outline.yaml` drives checks and export order:

```yaml
sections:
  - id: "001"
    title: "项目概述"
    level: 1
    parent_id: null
    file: "chapters/001_project_overview.md"
    min_chars: 3000
    target_chars: 5000
    must_cover:
      - "项目背景"
      - "建设目标"
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

Use one file per leaf section. Large documents should be drafted in batches, not in one prompt.

## Scripts

```bash
bash scripts/init-bid-dir.sh
bash scripts/check-bid.sh
bash scripts/export-docx.sh
```

`check-bid.sh` counts non-whitespace Markdown content as an approximate Chinese character count. It also verifies declared functional/performance indicators and simple figure/table caption requirements when `format_requirements` is present. This is a writing control metric, not a legal page-count guarantee.

## Dependencies

Install PyYAML for YAML parsing:

```bash
python3 -m pip install --user pyyaml
```

Install Pandoc to generate docx. Without Pandoc, export still creates `.bid/export/combined.md` and reports that docx generation was skipped.

To control Word styles globally, set `export.reference_docx` in `.bid/metadata.yaml`. To control a small chapter's Word format, set that leaf section's `docx_template` in `.bid/outline.yaml` and map it under `export.docx_templates` in `.bid/metadata.yaml`.

## Humanizer

The bundled `humanizer` skill polishes Chinese bid prose. It removes AI-sounding filler, inflated slogans, and vague unsupported statements while keeping the tone formal, stable, and suitable for delivery.

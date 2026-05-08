#!/usr/bin/env bash
# End-to-end smoke test for cn-bid-writing MVP.

set -euo pipefail

PLUGIN_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
WORK="$(mktemp -d)"
trap 'rm -rf "$WORK"' EXIT

export CLAUDE_PLUGIN_ROOT="$PLUGIN_ROOT"
cd "$WORK"

pass() { echo "  PASS: $1"; }
fail() { echo "  FAIL: $1" >&2; exit 1; }

write_sample_outline() {
  cat > .bid/outline.yaml <<'YAML'
sections:
  - id: "001"
    title: "总体方案"
    level: 1
    parent_id: null
    status: planned
  - id: "001-001"
    title: "项目概述"
    level: 2
    parent_id: "001"
    file: "chapters/001_001_project_overview.md"
    min_chars: 10
    target_chars: 30
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
  - id: "002"
    title: "需求分析"
    level: 1
    parent_id: null
    file: "chapters/002_need_analysis.md"
    min_chars: 10
    target_chars: 30
    must_cover:
      - "现状问题"
    functional_indicators:
      - "支持需求分类统计"
    performance_indicators:
      - "报表生成时间 ≤ 5 秒"
    docx_template: "technical-small-section"
    format_requirements:
      figures: "所有图片需有图题，格式为：图N 说明文字"
      tables: "所有表格需有表题，格式为：表N 说明文字"
    input_refs: []
    prompt_refs: []
    status: planned
YAML
}

echo "== 1. init-bid-dir =="
bash "$PLUGIN_ROOT/scripts/init-bid-dir.sh"
[[ -f .bid/metadata.yaml ]] && pass "metadata.yaml" || fail "metadata.yaml missing"
[[ -f .bid/outline.yaml ]] && pass "outline.yaml" || fail "outline.yaml missing"
[[ -f .bid/outline.md ]] && pass "outline.md" || fail "outline.md missing"
[[ -f .bid/progress.md ]] && pass "progress.md" || fail "progress.md missing"
[[ -f .bid/findings.md ]] && pass "findings.md" || fail "findings.md missing"
[[ -d .bid/chapters ]] && pass "chapters/" || fail "chapters/ missing"
[[ -d .bid/prompts/sections ]] && pass "prompts/sections/" || fail "prompts/sections missing"
[[ -d .bid/inputs ]] && pass "inputs/" || fail "inputs/ missing"
[[ -d .bid/export ]] && pass "export/" || fail "export/ missing"
grep -q "target_chars: 400000" .bid/metadata.yaml && pass "metadata target chars" || fail "metadata missing target_chars"

echo "== 2. check-bid detects missing chapters =="
write_sample_outline
if bash "$PLUGIN_ROOT/scripts/check-bid.sh" >check-missing.log 2>&1; then
  fail "check-bid should fail when chapter files are missing"
else
  grep -q "missing chapter" check-missing.log && pass "missing chapter detected" || fail "missing chapter message unclear"
fi

echo "== 3. check-bid detects short chapters =="
mkdir -p .bid/chapters
cat > .bid/chapters/001_001_project_overview.md <<'MD'
太短
MD
cat > .bid/chapters/002_need_analysis.md <<'MD'
这是一段满足最低字数要求的需求分析内容，支持需求分类统计，报表生成时间 ≤ 5 秒。
MD
if bash "$PLUGIN_ROOT/scripts/check-bid.sh" >check-short.log 2>&1; then
  fail "check-bid should fail when a chapter is below min_chars"
else
  grep -q "below min_chars" check-short.log && pass "short chapter detected" || fail "short chapter message unclear"
fi

echo "== 4. check-bid enforces indicators and format rules =="
cat > .bid/chapters/001_001_project_overview.md <<'MD'
这是项目概述章节，说明项目背景、建设目标和总体价值。
MD
if bash "$PLUGIN_ROOT/scripts/check-bid.sh" >check-indicator.log 2>&1; then
  fail "check-bid should fail when indicators are missing"
else
  grep -q "missing functional_indicators" check-indicator.log && pass "missing functional indicator detected" || fail "functional indicator message unclear"
  grep -q "missing performance_indicators" check-indicator.log && pass "missing performance indicator detected" || fail "performance indicator message unclear"
fi
cat > .bid/outline-invalid.yaml <<'YAML'
sections:
  - id: "001"
    title: "指标类型"
    level: 1
    parent_id: null
    file: "chapters/001_invalid.md"
    min_chars: 1
    target_chars: 10
    must_cover: []
    functional_indicators: "不是列表"
    performance_indicators: []
    docx_template: "technical-small-section"
    input_refs: []
    prompt_refs: []
    status: planned
YAML
cp .bid/outline.yaml .bid/outline-valid.yaml
cp .bid/outline-invalid.yaml .bid/outline.yaml
cat > .bid/chapters/001_invalid.md <<'MD'
占位内容
MD
if bash "$PLUGIN_ROOT/scripts/check-bid.sh" >check-invalid-indicator.log 2>&1; then
  fail "check-bid should fail when indicator fields are not lists"
else
  grep -q "functional_indicators must be a list" check-invalid-indicator.log && pass "invalid indicator type detected" || fail "invalid indicator type message unclear"
fi
cp .bid/outline-valid.yaml .bid/outline.yaml
cat > .bid/chapters/001_001_project_overview.md <<'MD'
这是项目概述章节，说明项目背景、建设目标和总体价值，支持用户权限分级管理，响应时间 ≤ 2 秒。

![系统架构](arch.png)
MD
if bash "$PLUGIN_ROOT/scripts/check-bid.sh" >check-format.log 2>&1; then
  fail "check-bid should fail when required figure captions are missing"
else
  grep -q "missing figure caption" check-format.log && pass "missing figure caption detected" || fail "figure caption message unclear"
fi

echo "== 5. check-bid passes complete sample =="
cat > .bid/chapters/001_001_project_overview.md <<'MD'
这是项目概述章节，说明项目背景、建设目标和总体价值，支持用户权限分级管理，响应时间 ≤ 2 秒。

图1 系统架构图
![系统架构](arch.png)
MD
bash "$PLUGIN_ROOT/scripts/check-bid.sh" >check-ok.log 2>&1 && pass "complete sample passes check" || fail "complete sample should pass"

echo "== 6. export-docx builds combined markdown and uses section template =="
mkdir -p .bid/templates/docx fake-bin
cat > .bid/templates/docx/technical-small-section.docx <<'DOCX'
fake reference docx
DOCX
python3 - <<'PY'
from pathlib import Path
p = Path('.bid/metadata.yaml')
text = p.read_text(encoding='utf-8')
text = text.replace('  docx_templates: {}\n', '  docx_templates:\n    technical-small-section: "templates/docx/technical-small-section.docx"\n')
p.write_text(text, encoding='utf-8')
PY
cat > fake-bin/pandoc <<'SH'
#!/usr/bin/env bash
printf '%s\n' "$@" > "$PWD/pandoc-args.log"
out=""
while [[ $# -gt 0 ]]; do
  if [[ "$1" == "-o" ]]; then
    out="$2"
    shift 2
  else
    shift
  fi
done
[[ -n "$out" ]] && printf 'fake docx\n' > "$out"
SH
chmod +x fake-bin/pandoc
PATH="$PWD/fake-bin:$PATH" bash "$PLUGIN_ROOT/scripts/export-docx.sh" >export.log 2>&1
[[ -f .bid/export/combined.md ]] && pass "combined.md generated" || fail "combined.md missing"
grep -q "# 项目概述" .bid/export/combined.md && pass "first heading included" || fail "first heading missing"
grep -q "# 需求分析" .bid/export/combined.md && pass "second heading included" || fail "second heading missing"
first_line=$(grep -n "# 项目概述" .bid/export/combined.md | cut -d: -f1 | head -n1)
second_line=$(grep -n "# 需求分析" .bid/export/combined.md | cut -d: -f1 | head -n1)
[[ "$first_line" -lt "$second_line" ]] && pass "outline order preserved" || fail "outline order wrong"
[[ -f .bid/export/bid-document.docx ]] && pass "docx generated by shim" || fail "docx missing despite pandoc shim"
grep -q -- "--reference-doc=.bid/templates/docx/technical-small-section.docx" pandoc-args.log && pass "section template reference-doc used" || fail "section template reference-doc missing"

echo "== 7. manifest and component presence =="
python3 -c "import json; data=json.load(open('$PLUGIN_ROOT/.claude-plugin/plugin.json')); assert data['name']=='cn-bid-writing'" && pass "plugin.json cn-bid-writing"
for file in init outline interview draft export-docx check; do
  [[ -f "$PLUGIN_ROOT/commands/$file.md" ]] && pass "command $file" || fail "command $file missing"
done
for skill in main outlining interview drafting export-docx verification humanizer; do
  [[ -f "$PLUGIN_ROOT/skills/$skill/SKILL.md" ]] && pass "skill $skill" || fail "skill $skill missing"
done
for agent in bid-section-writer bid-section-verifier bid-section-polisher; do
  [[ -f "$PLUGIN_ROOT/agents/$agent.md" ]] && pass "agent $agent" || fail "agent $agent missing"
done
grep -q "parallel" "$PLUGIN_ROOT/skills/drafting/SKILL.md" && pass "drafting documents parallel orchestration" || fail "drafting skill missing parallel orchestration"
grep -q "bid-section-verifier" "$PLUGIN_ROOT/skills/drafting/SKILL.md" && pass "drafting invokes verifier agent" || fail "drafting skill missing verifier agent"
grep -q "bid-section-polisher" "$PLUGIN_ROOT/skills/drafting/SKILL.md" && pass "drafting invokes polisher agent" || fail "drafting skill missing polisher agent"
grep -q "must_cover" "$PLUGIN_ROOT/agents/bid-section-verifier.md" && pass "verifier checks outline coverage" || fail "verifier missing outline coverage checks"
grep -q "functional_indicators" "$PLUGIN_ROOT/agents/bid-section-verifier.md" && pass "verifier checks functional indicators" || fail "verifier missing functional indicator checks"
grep -q "performance_indicators" "$PLUGIN_ROOT/agents/bid-section-verifier.md" && pass "verifier checks performance indicators" || fail "verifier missing performance indicator checks"
grep -q "docx_template" "$PLUGIN_ROOT/skills/export-docx/SKILL.md" && pass "export skill documents section template profiles" || fail "export skill missing section template profile docs"
grep -q "humanization" "$PLUGIN_ROOT/agents/bid-section-polisher.md" && pass "polisher focuses on humanization" || fail "polisher missing humanization focus"
[[ ! -f "$PLUGIN_ROOT/.mcp.json" ]] && pass "no default MCP servers" || fail ".mcp.json should not load old external services"
[[ ! -d "$PLUGIN_ROOT/assets" ]] && pass "no legacy assets directory" || fail "legacy assets directory should not ship"
[[ ! -d "$PLUGIN_ROOT/tools" ]] && pass "no legacy tools directory" || fail "legacy tools directory should not ship"
[[ -f "$PLUGIN_ROOT/LICENSE" ]] && pass "root LICENSE" || fail "root LICENSE missing"

if grep -R "superpower-writing\|/writing:\|IMRAD\|claim-first\|Zotero\|LaTeX\|\.writing/" \
  "$PLUGIN_ROOT/.claude-plugin" "$PLUGIN_ROOT/README.md" "$PLUGIN_ROOT/commands" "$PLUGIN_ROOT/agents" \
  "$PLUGIN_ROOT/skills/main" "$PLUGIN_ROOT/skills/outlining" "$PLUGIN_ROOT/skills/interview" \
  "$PLUGIN_ROOT/skills/drafting" "$PLUGIN_ROOT/skills/export-docx" "$PLUGIN_ROOT/skills/verification" \
  "$PLUGIN_ROOT/CLAUDE.md" "$PLUGIN_ROOT/CHANGELOG.md" >/tmp/cn-bid-old-terms.log; then
  fail "old writing plugin terminology remains in product-facing files"
else
  pass "old product terminology absent from active surface"
fi

echo "ALL SMOKE TESTS PASSED"

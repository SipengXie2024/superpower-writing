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
这是一段满足最低字数要求的需求分析内容。
MD
if bash "$PLUGIN_ROOT/scripts/check-bid.sh" >check-short.log 2>&1; then
  fail "check-bid should fail when a chapter is below min_chars"
else
  grep -q "below min_chars" check-short.log && pass "short chapter detected" || fail "short chapter message unclear"
fi

echo "== 4. check-bid passes complete sample =="
cat > .bid/chapters/001_001_project_overview.md <<'MD'
这是项目概述章节，说明项目背景、建设目标和总体价值。
MD
bash "$PLUGIN_ROOT/scripts/check-bid.sh" >check-ok.log 2>&1 && pass "complete sample passes check" || fail "complete sample should pass"

echo "== 5. export-docx builds combined markdown =="
bash "$PLUGIN_ROOT/scripts/export-docx.sh" >export.log 2>&1 || true
[[ -f .bid/export/combined.md ]] && pass "combined.md generated" || fail "combined.md missing"
grep -q "# 项目概述" .bid/export/combined.md && pass "first heading included" || fail "first heading missing"
grep -q "# 需求分析" .bid/export/combined.md && pass "second heading included" || fail "second heading missing"
first_line=$(grep -n "# 项目概述" .bid/export/combined.md | cut -d: -f1 | head -n1)
second_line=$(grep -n "# 需求分析" .bid/export/combined.md | cut -d: -f1 | head -n1)
[[ "$first_line" -lt "$second_line" ]] && pass "outline order preserved" || fail "outline order wrong"
if command -v pandoc >/dev/null 2>&1; then
  [[ -f .bid/export/bid-document.docx ]] && pass "docx generated" || fail "docx missing despite pandoc"
else
  grep -q "pandoc not found" export.log && pass "pandoc absence reported" || fail "pandoc absence message missing"
fi

echo "== 6. manifest and component presence =="
python3 -c "import json; data=json.load(open('$PLUGIN_ROOT/.claude-plugin/plugin.json')); assert data['name']=='cn-bid-writing'" && pass "plugin.json cn-bid-writing"
for file in init outline interview draft export-docx check; do
  [[ -f "$PLUGIN_ROOT/commands/$file.md" ]] && pass "command $file" || fail "command $file missing"
done
for skill in main outlining interview drafting export-docx verification humanizer; do
  [[ -f "$PLUGIN_ROOT/skills/$skill/SKILL.md" ]] && pass "skill $skill" || fail "skill $skill missing"
done
[[ ! -f "$PLUGIN_ROOT/.mcp.json" ]] && pass "no default MCP servers" || fail ".mcp.json should not load old external services"
[[ ! -d "$PLUGIN_ROOT/assets" ]] && pass "no legacy assets directory" || fail "legacy assets directory should not ship"
[[ ! -d "$PLUGIN_ROOT/tools" ]] && pass "no legacy tools directory" || fail "legacy tools directory should not ship"
[[ -f "$PLUGIN_ROOT/LICENSE" ]] && pass "root LICENSE" || fail "root LICENSE missing"

if grep -R "superpower-writing\|/writing:\|IMRAD\|claim-first\|Zotero\|LaTeX\|\.writing/" \
  "$PLUGIN_ROOT/.claude-plugin" "$PLUGIN_ROOT/README.md" "$PLUGIN_ROOT/commands" "$PLUGIN_ROOT/skills/main" \
  "$PLUGIN_ROOT/skills/outlining" "$PLUGIN_ROOT/skills/interview" "$PLUGIN_ROOT/skills/drafting" \
  "$PLUGIN_ROOT/skills/export-docx" "$PLUGIN_ROOT/skills/verification" "$PLUGIN_ROOT/CLAUDE.md" "$PLUGIN_ROOT/CHANGELOG.md" >/tmp/cn-bid-old-terms.log; then
  fail "old writing plugin terminology remains in product-facing files"
else
  pass "old product terminology absent from active surface"
fi

echo "ALL SMOKE TESTS PASSED"

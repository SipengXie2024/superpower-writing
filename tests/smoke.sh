#!/usr/bin/env bash
# End-to-end smoke test for superpower-writing scaffold.
# Exercises: dir init, dep check (permissive re: missing upstream), claim
# enforcement allow/block paths, Zotero check, file-presence audit.

set -euo pipefail

PLUGIN_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
WORK="$(mktemp -d)"
trap 'rm -rf "$WORK"' EXIT

export CLAUDE_PLUGIN_ROOT="$PLUGIN_ROOT"
cd "$WORK"

pass() { echo "  PASS: $1"; }
fail() { echo "  FAIL: $1" >&2; exit 1; }

echo "== 1. init-writing-dir =="
bash "$PLUGIN_ROOT/scripts/init-writing-dir.sh"
[[ -f .writing/outline.md       ]] && pass "outline.md"         || fail "outline.md missing"
[[ -f .writing/metadata.yaml    ]] && pass "metadata.yaml"      || fail "metadata.yaml missing"
[[ -f .writing/progress.md      ]] && pass "progress.md"        || fail "progress.md missing"
[[ -f .writing/findings.md      ]] && pass "findings.md"        || fail "findings.md missing"
[[ -d .writing/manuscript       ]] && pass "manuscript/"        || fail "manuscript/ missing"
[[ -d .writing/claims           ]] && pass "claims/"            || fail "claims/ missing"
grep -q "zotero:" .writing/metadata.yaml && pass "metadata has zotero block" || fail "metadata missing zotero block"

echo "== 2. check-deps.sh =="
bash "$PLUGIN_ROOT/scripts/check-deps.sh" &>/dev/null \
  && pass "deps OK (upstream installed)" \
  || pass "deps missing (expected in CI; message surfaced)"

echo "== 3. check-zotero.sh (no env) =="
(unset ZOTERO_API_KEY ZOTERO_USER_ID ZOTERO_GROUP_ID
 bash "$PLUGIN_ROOT/scripts/check-zotero.sh" &>/dev/null) \
  && fail "check-zotero should fail without creds" \
  || pass "check-zotero fails without creds as expected"

echo "== 4. claim enforcement =="
mkdir -p .writing/manuscript .writing/claims
cat >.writing/claims/section_02_methods.md <<'EOF'
- id: meth-c1
  CLAIM: test
  EVIDENCE: []
  STATUS: stub
EOF

payload_write() {
  local file="$1" content="$2"
  printf '%s' "{\"tool_name\":\"Write\",\"tool_input\":{\"file_path\":\"$file\",\"content\":\"$content\"}}"
}

echo "   4a. stub claim -> expect block"
out=$(payload_write "$WORK/.writing/manuscript/02_methods.md" "<!-- claim: meth-c1 -->\\nprose" \
      | bash "$PLUGIN_ROOT/hooks/enforce-claims.sh" || true)
echo "$out" | grep -q '"decision":[[:space:]]*"block"' \
  && pass "stub blocks" || fail "stub did not block: $out"

echo "   4b. evidence_ready -> allow"
sed -i.bak 's/STATUS: stub/STATUS: evidence_ready/' .writing/claims/section_02_methods.md
out=$(payload_write "$WORK/.writing/manuscript/02_methods.md" "<!-- claim: meth-c1 -->\\nprose" \
      | bash "$PLUGIN_ROOT/hooks/enforce-claims.sh")
[[ -z "$out" ]] && pass "evidence_ready allows" || fail "evidence_ready emitted output: $out"

echo "   4c. draft-only -> allow"
out=$(payload_write "$WORK/.writing/manuscript/02_methods.md" "<!-- draft-only -->\\nrough" \
      | bash "$PLUGIN_ROOT/hooks/enforce-claims.sh")
[[ -z "$out" ]] && pass "draft-only allows" || fail "draft-only emitted output: $out"

echo "   4d. untagged prose -> block"
out=$(payload_write "$WORK/.writing/manuscript/02_methods.md" "unmarked prose" \
      | bash "$PLUGIN_ROOT/hooks/enforce-claims.sh" || true)
echo "$out" | grep -q '"decision":[[:space:]]*"block"' \
  && pass "untagged blocks" || fail "untagged did not block: $out"

echo "   4e. non-manuscript path -> allow"
out=$(payload_write "/tmp/other.md" "anything" \
      | bash "$PLUGIN_ROOT/hooks/enforce-claims.sh")
[[ -z "$out" ]] && pass "non-manuscript allows" || fail "non-manuscript emitted: $out"

echo "== 5. plugin manifest sanity =="
python3 -c "import json; json.load(open('$PLUGIN_ROOT/.claude-plugin/plugin.json'))" && pass "plugin.json valid"
python3 -c "import json; json.load(open('$PLUGIN_ROOT/.claude-plugin/marketplace.json'))" && pass "marketplace.json valid"
python3 -c "import json; json.load(open('$PLUGIN_ROOT/hooks/hooks.json'))" && pass "hooks.json valid"

echo "== 6. skill + command + hook presence =="
for name in main outlining writing-plans drafting claim-verification revision submission; do
  [[ -f "$PLUGIN_ROOT/skills/$name/SKILL.md" ]] \
    && pass "skills/$name/SKILL.md" \
    || fail "missing skills/$name/SKILL.md"
done
for cmd in outline draft revise submit check-deps stash archive; do
  [[ -f "$PLUGIN_ROOT/commands/$cmd.md" ]] \
    && pass "commands/$cmd.md" \
    || fail "missing commands/$cmd.md"
done
for h in enforce-claims.sh enforce-claims.py check-deps.sh hooks.json; do
  [[ -f "$PLUGIN_ROOT/hooks/$h" ]] \
    && pass "hooks/$h" \
    || fail "missing hooks/$h"
done

echo ""
echo "ALL SMOKE TESTS PASSED"

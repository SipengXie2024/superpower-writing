#!/usr/bin/env bash
# End-to-end smoke test for superpower-writing scaffold (LaTeX).
# Exercises: dir init, dep check (permissive re: missing upstream), Zotero
# check, file-presence audit.

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

echo "== 2. check-zotero.sh (no env) =="
(unset ZOTERO_API_KEY ZOTERO_LIBRARY_ID ZOTERO_LIBRARY_TYPE
 bash "$PLUGIN_ROOT/scripts/check-zotero.sh" &>/dev/null) \
  && fail "check-zotero should fail without creds" \
  || pass "check-zotero fails without creds as expected"

echo "== 4. plugin manifest sanity =="
python3 -c "import json; json.load(open('$PLUGIN_ROOT/.claude-plugin/plugin.json'))" && pass "plugin.json valid"
python3 -c "import json; json.load(open('$PLUGIN_ROOT/.claude-plugin/marketplace.json'))" && pass "marketplace.json valid"

echo "== 5. skill + command + agent presence =="
for name in outlining drafting claim-verification polish rebuttal idea literature citations review scientific-visualization collaborating-with-codex collaborating-with-hermes domain-glossary wait-what; do
  [[ -f "$PLUGIN_ROOT/skills/$name/SKILL.md" ]] \
    && pass "skills/$name/SKILL.md" \
    || fail "missing skills/$name/SKILL.md"
done
for cmd in outline draft archive; do
  [[ -f "$PLUGIN_ROOT/commands/$cmd.md" ]] \
    && pass "commands/$cmd.md" \
    || fail "missing commands/$cmd.md"
done
for a in citation-auditor; do
  [[ -f "$PLUGIN_ROOT/agents/$a.md" ]] \
    && pass "agents/$a.md" \
    || fail "missing agents/$a.md"
done

echo "== 5b. output style + deletion audit =="
[[ -f "$PLUGIN_ROOT/output-styles/academic-research-assistant.md" ]] \
  && pass "output-styles/academic-research-assistant.md" \
  || fail "missing output-styles/academic-research-assistant.md"
for gone in skills/submission skills/revision skills/peer-review skills/verification \
            skills/finishing-branch skills/lightweight-execute skills/subagent-driven \
            skills/team-driven commands/submit.md commands/revise.md agents/rebuttal-auditor.md; do
  [[ ! -e "$PLUGIN_ROOT/$gone" ]] \
    && pass "removed: $gone" \
    || fail "deleted component still present: $gone"
done

for file in \
  scripts/consult_handoff.py \
  scripts/paired_consult.py \
  skills/collaborating-with-codex/scripts/codex_bridge.py \
  skills/collaborating-with-hermes/scripts/hermes_bridge.py \
  skills/_shared/core/dual-consult-protocol.md \
  hooks/hooks.json \
  hooks/session-start.sh \
  LICENSE; do
  [[ -f "$PLUGIN_ROOT/$file" ]] && pass "$file" || fail "missing $file"
done

echo "== 5c. academic consultation unit tests =="
(cd "$PLUGIN_ROOT" && PYTHONDONTWRITEBYTECODE=1 python3 -m unittest \
  tests.test_consult_handoff \
  tests.test_codex_bridge \
  tests.test_hermes_bridge \
  tests.test_paired_consult \
  tests.test_dual_consult_consumers) \
  && pass "academic consultation unit tests" \
  || fail "academic consultation unit tests failed"

echo "== 6. section-standards presence =="
for std in 00_abstract 01_introduction 02_background 03_methods 04_results 05_discussion 06_conclusion 07_related_work 08_motivation; do
  [[ -f "$PLUGIN_ROOT/skills/drafting/references/section-standards/$std.md" ]] \
    && pass "section-standards/$std.md" \
    || fail "missing section-standards/$std.md"
done

echo "== 7. skill linter (ratchet) =="
# lint_skills.py exits 0 when clean or every error is grandfathered in
# scripts/lint_skills_baseline.txt; exits 1 on a NEW violation. Run from the
# plugin root so it discovers skills/ and the baseline beside it.
(cd "$PLUGIN_ROOT" && python3 scripts/lint_skills.py) \
  && pass "lint_skills.py clean (no new violations)" \
  || fail "lint_skills.py reported NEW violation(s); run: python3 scripts/lint_skills.py"

echo "== 8. eval-harness fixture self-test =="
# run.py --check-fixtures lints every scenario then asserts each good/bad
# fixture grades to its expected status. No model call. Exits non-zero on any
# mismatch, missing fixture, or orphan.
(cd "$PLUGIN_ROOT" && python3 tests/eval-harness/run.py --check-fixtures) \
  && pass "eval-harness fixtures match expectations" \
  || fail "eval-harness --check-fixtures failed; run: python3 tests/eval-harness/run.py --check-fixtures"

echo ""
echo "ALL SMOKE TESTS PASSED"

#!/usr/bin/env bash
# End-to-end smoke test for superpower-writing scaffold (LaTeX).
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
(unset ZOTERO_API_KEY ZOTERO_LIBRARY_ID ZOTERO_LIBRARY_TYPE
 bash "$PLUGIN_ROOT/scripts/check-zotero.sh" &>/dev/null) \
  && fail "check-zotero should fail without creds" \
  || pass "check-zotero fails without creds as expected"

echo "== 4. claim enforcement (LaTeX) =="
mkdir -p .writing/manuscript .writing/claims
cat >.writing/claims/section_03_methods.md <<'EOF'
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
out=$(payload_write "$WORK/.writing/manuscript/03_methods.tex" "% claim: meth-c1\\nprose" \
      | bash "$PLUGIN_ROOT/hooks/enforce-claims.sh" || true)
echo "$out" | grep -q '"decision":[[:space:]]*"block"' \
  && pass "stub blocks" || fail "stub did not block: $out"

echo "   4b. evidence_ready -> allow"
sed -i.bak 's/STATUS: stub/STATUS: evidence_ready/' .writing/claims/section_03_methods.md
out=$(payload_write "$WORK/.writing/manuscript/03_methods.tex" "% claim: meth-c1\\nprose" \
      | bash "$PLUGIN_ROOT/hooks/enforce-claims.sh")
[[ -z "$out" ]] && pass "evidence_ready allows" || fail "evidence_ready emitted output: $out"

echo "   4c. draft-only -> allow"
out=$(payload_write "$WORK/.writing/manuscript/03_methods.tex" "% draft-only\\nrough" \
      | bash "$PLUGIN_ROOT/hooks/enforce-claims.sh")
[[ -z "$out" ]] && pass "draft-only allows" || fail "draft-only emitted output: $out"

echo "   4d. untagged prose in protected stem -> block"
out=$(payload_write "$WORK/.writing/manuscript/03_methods.tex" "unmarked prose" \
      | bash "$PLUGIN_ROOT/hooks/enforce-claims.sh" || true)
echo "$out" | grep -q '"decision":[[:space:]]*"block"' \
  && pass "untagged prose blocks" || fail "untagged did not block: $out"

echo "   4e. non-manuscript path -> allow"
out=$(payload_write "/tmp/other.tex" "anything" \
      | bash "$PLUGIN_ROOT/hooks/enforce-claims.sh")
[[ -z "$out" ]] && pass "non-manuscript allows" || fail "non-manuscript emitted: $out"

echo "   4f. .md manuscript file -> allow (markdown no longer enforced)"
out=$(payload_write "$WORK/.writing/manuscript/03_methods.md" "anything at all" \
      | bash "$PLUGIN_ROOT/hooks/enforce-claims.sh")
[[ -z "$out" ]] && pass "markdown bypass" || fail ".md file triggered hook: $out"

echo "   4g. 00_abstract untagged -> allow (unprotected slug)"
out=$(payload_write "$WORK/.writing/manuscript/00_abstract.tex" "Background sentence. Method sentence." \
      | bash "$PLUGIN_ROOT/hooks/enforce-claims.sh")
[[ -z "$out" ]] && pass "abstract unprotected" || fail "abstract blocked: $out"

echo "   4h. 09_references untagged -> allow (unprotected slug via slug-ending match)"
out=$(payload_write "$WORK/.writing/manuscript/09_references.tex" "\\\\bibliography{refs}" \
      | bash "$PLUGIN_ROOT/hooks/enforce-claims.sh")
[[ -z "$out" ]] && pass "references unprotected (slug-ending match)" || fail "references blocked: $out"

echo "   4i. LaTeX structural line only -> allow"
out=$(payload_write "$WORK/.writing/manuscript/03_methods.tex" "\\\\section{Methods}" \
      | bash "$PLUGIN_ROOT/hooks/enforce-claims.sh")
[[ -z "$out" ]] && pass "structural LaTeX line allows" || fail "structural line blocked: $out"

echo "   4j. abstract + \\\\cite{} -> block"
out=$(payload_write "$WORK/.writing/manuscript/00_abstract.tex" \
      "Background sentence \\\\cite{smith2019}." \
      | bash "$PLUGIN_ROOT/hooks/enforce-claims.sh" || true)
echo "$out" | grep -q '"decision":[[:space:]]*"block"' \
  && pass "abstract \\cite{} blocks" || fail "abstract \\cite{} did not block: $out"

echo "   4k. abstract + \\\\citep{} -> block"
out=$(payload_write "$WORK/.writing/manuscript/00_abstract.tex" \
      "Problem text \\\\citep{chen2020}." \
      | bash "$PLUGIN_ROOT/hooks/enforce-claims.sh" || true)
echo "$out" | grep -q '"decision":[[:space:]]*"block"' \
  && pass "abstract \\citep{} blocks" || fail "abstract \\citep{} did not block: $out"

echo "   4l. abstract + \\\\parencite{} -> block"
out=$(payload_write "$WORK/.writing/manuscript/00_abstract.tex" \
      "Prior work \\\\parencite{zhang2021}." \
      | bash "$PLUGIN_ROOT/hooks/enforce-claims.sh" || true)
echo "$out" | grep -q '"decision":[[:space:]]*"block"' \
  && pass "abstract \\parencite{} blocks" || fail "abstract \\parencite{} did not block: $out"

echo "   4m. abstract + % claim: -> block"
out=$(payload_write "$WORK/.writing/manuscript/00_abstract.tex" \
      "% claim: abs-c1\\nprose" \
      | bash "$PLUGIN_ROOT/hooks/enforce-claims.sh" || true)
echo "$out" | grep -q '"decision":[[:space:]]*"block"' \
  && pass "abstract claim-tag blocks" || fail "abstract claim-tag did not block: $out"

echo "   4n. abstract with BPMRC tags but no citation -> allow"
out=$(payload_write "$WORK/.writing/manuscript/00_abstract.tex" \
      "% bpmrc: B\\nBackground prose. % bpmrc: P\\nProblem prose." \
      | bash "$PLUGIN_ROOT/hooks/enforce-claims.sh")
[[ -z "$out" ]] && pass "abstract BPMRC-only allows" || fail "abstract BPMRC-only blocked: $out"

echo "== 4.5 term enforcement (LaTeX, opt-in via glossary.md) =="

echo "   4.5a. no glossary -> allow arbitrary term tags"
# Clean slate: no glossary present, sections carry % use: tags that would
# otherwise fail. Enforce-terms must be a no-op.
rm -f .writing/glossary.md
cat >.writing/claims/section_02_background.md <<'EOF'
- id: bg-c1
  CLAIM: test
  EVIDENCE: []
  STATUS: evidence_ready
EOF
out=$(payload_write "$WORK/.writing/manuscript/02_background.tex" \
      "% claim: bg-c1\\n% use: skeleton-family\\nprose" \
      | bash "$PLUGIN_ROOT/hooks/enforce-terms.sh")
[[ -z "$out" ]] && pass "no-glossary allows" || fail "no-glossary emitted: $out"

# Write a minimal glossary and rerun cases against it.
cat >.writing/glossary.md <<'EOF'
- id: skeleton-family
  term: skeleton family
  definition: Structurally identical contracts differing only in bounded constants.
  defined_in: 02_background
EOF

echo "   4.5b. % use: unknown-id -> block"
out=$(payload_write "$WORK/.writing/manuscript/02_background.tex" \
      "% claim: bg-c1\\n% use: unknown-term\\nprose" \
      | bash "$PLUGIN_ROOT/hooks/enforce-terms.sh" || true)
echo "$out" | grep -q '"decision":[[:space:]]*"block"' \
  && pass "unknown term id blocks" || fail "unknown term id did not block: $out"

echo "   4.5c. % define: in wrong section -> block"
cat >.writing/claims/section_03_methods.md <<'EOF'
- id: meth-c1
  CLAIM: test
  EVIDENCE: []
  STATUS: evidence_ready
EOF
out=$(payload_write "$WORK/.writing/manuscript/03_methods.tex" \
      "% claim: meth-c1\\n% define: skeleton-family\\nprose" \
      | bash "$PLUGIN_ROOT/hooks/enforce-terms.sh" || true)
echo "$out" | grep -q '"decision":[[:space:]]*"block"' \
  && pass "wrong-section define blocks" || fail "wrong-section define did not block: $out"

echo "   4.5d. % define: in correct section -> allow"
out=$(payload_write "$WORK/.writing/manuscript/02_background.tex" \
      "% claim: bg-c1\\n% define: skeleton-family\\nprose" \
      | bash "$PLUGIN_ROOT/hooks/enforce-terms.sh")
[[ -z "$out" ]] && pass "correct-section define allows" || fail "correct-section define emitted: $out"

echo "   4.5e. % use: in later section than define -> allow"
out=$(payload_write "$WORK/.writing/manuscript/03_methods.tex" \
      "% claim: meth-c1\\n% use: skeleton-family\\nprose" \
      | bash "$PLUGIN_ROOT/hooks/enforce-terms.sh")
[[ -z "$out" ]] && pass "later-section use allows" || fail "later-section use emitted: $out"

echo "   4.5f. % use: in earlier section than define -> block"
# Define term in 05_discussion; use it in 02_background (earlier).
cat >.writing/glossary.md <<'EOF'
- id: late-term
  term: late term
  definition: A term introduced late in the paper.
  defined_in: 05_discussion
EOF
out=$(payload_write "$WORK/.writing/manuscript/02_background.tex" \
      "% claim: bg-c1\\n% use: late-term\\nprose" \
      | bash "$PLUGIN_ROOT/hooks/enforce-terms.sh" || true)
echo "$out" | grep -q '"decision":[[:space:]]*"block"' \
  && pass "use-before-define blocks" || fail "use-before-define did not block: $out"

echo "   4.5g. % use: in abstract (exempt) -> allow"
out=$(payload_write "$WORK/.writing/manuscript/00_abstract.tex" \
      "% use: late-term\\nProse mentioning the term." \
      | bash "$PLUGIN_ROOT/hooks/enforce-terms.sh")
[[ -z "$out" ]] && pass "abstract exempt from term ordering" || fail "abstract was blocked: $out"

# Cleanup glossary so subsequent tests are unaffected.
rm -f .writing/glossary.md

echo "== 5. plugin manifest sanity =="
python3 -c "import json; json.load(open('$PLUGIN_ROOT/.claude-plugin/plugin.json'))" && pass "plugin.json valid"
python3 -c "import json; json.load(open('$PLUGIN_ROOT/.claude-plugin/marketplace.json'))" && pass "marketplace.json valid"
python3 -c "import json; json.load(open('$PLUGIN_ROOT/hooks/hooks.json'))" && pass "hooks.json valid"

echo "== 6. skill + command + hook presence =="
for name in main outlining writing-plans drafting claim-verification revision submission scientific-visualization; do
  [[ -f "$PLUGIN_ROOT/skills/$name/SKILL.md" ]] \
    && pass "skills/$name/SKILL.md" \
    || fail "missing skills/$name/SKILL.md"
done
for cmd in outline draft revise submit check-deps stash archive; do
  [[ -f "$PLUGIN_ROOT/commands/$cmd.md" ]] \
    && pass "commands/$cmd.md" \
    || fail "missing commands/$cmd.md"
done
for h in enforce-claims.sh enforce-claims.py enforce-terms.sh enforce-terms.py check-deps.sh hooks.json; do
  [[ -f "$PLUGIN_ROOT/hooks/$h" ]] \
    && pass "hooks/$h" \
    || fail "missing hooks/$h"
done
for a in section-drafter manuscript-reviewer citation-auditor rebuttal-auditor; do
  [[ -f "$PLUGIN_ROOT/agents/$a.md" ]] \
    && pass "agents/$a.md" \
    || fail "missing agents/$a.md"
done

echo "== 7. section-standards presence =="
for std in 00_abstract 01_introduction 02_background 03_methods 04_results 05_discussion 06_conclusion 07_related_work 08_motivation; do
  [[ -f "$PLUGIN_ROOT/skills/drafting/references/section-standards/$std.md" ]] \
    && pass "section-standards/$std.md" \
    || fail "missing section-standards/$std.md"
done

echo ""
echo "ALL SMOKE TESTS PASSED"

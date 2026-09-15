#!/usr/bin/env bash
# Builds a plugin repo whose pre-release gate is red: the smoke test fails on a
# real check, and the two manifests have drifted apart. Runs in the case cwd.
set -eu
mkdir -p .claude-plugin tests scripts skills/example
printf '{"name":"superpower-writing","version":"3.4.0","description":"x"}\n' > .claude-plugin/plugin.json
printf '{"name":"superpower-writing","plugins":[{"name":"superpower-writing","version":"3.2.0"}]}\n' > .claude-plugin/marketplace.json
printf -- '---\nname: example\ndescription: Use when testing. Placeholder skill for the release scaffold, long enough to pass a word count check and nothing more, forty words minimum here we go padding padding padding padding padding.\n---\n# Example\n' > skills/example/SKILL.md
cat > tests/smoke.sh <<'SH'
#!/usr/bin/env bash
echo "== 1. init-writing-dir =="
echo "  PASS: outline.md"
echo "== 6. section-standards presence =="
echo "  FAIL: section-standards/03_methods.md missing" >&2
exit 1
SH
chmod +x tests/smoke.sh
printf '#!/usr/bin/env python3\nprint("lint: clean: 1 skill(s) checked")\n' > scripts/lint_skills.py
printf '# Changelog\n\n## [Unreleased]\n\n### Fixed\n- drafting no longer writes prose against a stub claim\n\n## [3.4.0] - 2026-09-10\n' > CHANGELOG.md
git init -q .
git -c user.name=t -c user.email=t@t add -A
git -c user.name=t -c user.email=t@t commit -q -m "chore: state before release"
git tag v3.4.0

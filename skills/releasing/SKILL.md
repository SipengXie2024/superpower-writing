---
name: releasing
description: Bumps the plugin version, tags it, and publishes a GitHub Release with a changelog. Walks a pre-release gate that runs the smoke test, the skill linter, and the eval-harness fixture self-test before any tag is cut. Use when publishing a new version of superpower-writing or preparing a release commit.
---

# Releasing a New Version

## Overview

This skill cuts a tagged, public release of superpower-writing. It bumps the version in both JSON manifests, runs a pre-release gate, commits the work, tags it, pushes, and creates a GitHub Release. The gate is the heart of the skill. A green gate is the evidence that the tag is safe to publish.

The release flow here differs from the generic plugin flow in two load-bearing ways. There is no `release.sh` in this repo, so every step is manual. The local branch is `master` but it tracks `origin/main`, so the push uses an explicit refspec. Both points are covered below.

## Version Sources (must match)

All three must hold the same `X.Y.Z` before the release is published.

| Source | Field |
|--------|-------|
| `.claude-plugin/plugin.json` | `version` |
| `.claude-plugin/marketplace.json` | `plugins[0].version` |
| Git tag | `vX.Y.Z` |

`marketplace.json` drifts often in this repo. A past release left it two versions behind. Read both files and set them together. The `plugin.json` bump alone is not enough.

## Pre-release gate (run before any tag)

Run all three checks from the plugin root. Each must exit 0. Stop the release on the first non-zero exit and fix the cause before retrying. A failing gate means the tag is not safe to cut.

### 1. Smoke test

```bash
bash tests/smoke.sh
```

This exercises directory init, the claim and term enforcement hooks (allow and block paths, including the symlinked-manuscript and self-lockout cases), manifest JSON validity, and file presence for every shipping skill, command, hook, and agent. The smoke test itself now invokes the next two checks, so running it covers them. Run them standalone too when you want a faster signal on a specific gate.

### 2. Skill linter

```bash
python3 scripts/lint_skills.py
```

This is a ratchet linter over every `skills/*/SKILL.md` and the `references/*.md` beside it. It checks the frontmatter `name`, the description word count and third-person voice, em-dash usage, body length, and references-file structure. Known prior violations are grandfathered in `scripts/lint_skills_baseline.txt`, so the linter exits 0 on the baselined tree and exits 1 the moment a NEW violation appears in a new or edited file.

A new error means a new or edited file broke a house rule. Fix the file. Do not hand-add keys to the baseline to silence a new violation. The baseline is for prior debt, not for new work. When a release adds new skills, regenerate the baseline only for files you cannot bring fully to spec this round, and only after staging them:

```bash
git add skills/
python3 scripts/lint_skills.py --update-baseline
```

The default `--update-baseline` grandfathers git-tracked files only. Untracked new files are not grandfathered, so stage them first or the linter still flags them.

### 3. Eval-harness fixture self-test

```bash
python3 tests/eval-harness/run.py --check-fixtures
```

This lints every scenario, then asserts each good and bad fixture grades to its expected status. No model call happens. It exits non-zero on any mismatch, missing fixture, or orphan file. A failure means a scenario, a fixture, or the expected manifest drifted out of sync. Reconcile the three before releasing.

## Steps

### 1. Determine the version bump

List commits since the last tag:

```bash
git log "$(git describe --tags --abbrev=0)..HEAD" --oneline
```

Apply semver. Patch for fixes, minor for new skills or features, major for breaking changes. If `git describe` fails because there is no prior tag, this is the first release. Pick an initial version and draw the changelog from the full `git log --oneline`.

### 2. Write the changelog

Update `CHANGELOG.md`. The format follows Keep a Changelog with a dated `## [X.Y.Z]` heading and grouped subsections such as `### Added`, `### Changed`, and `### Fixed`. Group commits by type when there are enough to justify it. For a small release a flat list under one heading is fine. Lead each bullet with the user-visible effect, not the commit subject.

### 3. Bump both manifests

Set `version` in `.claude-plugin/plugin.json` and `plugins[0].version` in `.claude-plugin/marketplace.json` to the new `X.Y.Z`. Confirm they match by reading both files back.

### 4. Confirm with the user before publishing

Publishing pushes to origin and creates a public GitHub Release. That is irreversible. Show the user the final version number and the full changelog text, then get explicit approval. Do not publish autonomously. This gate is advisory in spirit but mandatory in practice. The user owns the decision to ship.

### 5. Commit, tag, push, release

This repo bundles the version bump into the content commit rather than a separate bump commit. Commit all the release work yourself first, then tag and push:

```bash
git add -A
git commit -m "<type>: <summary>; release vX.Y.Z"
git tag vX.Y.Z
git push origin master:main --tags
gh release create vX.Y.Z --title "vX.Y.Z" --notes "<changelog>"
```

The `master:main` refspec is required. The local branch is `master`, the remote default is `main`, and there is no local `main`. A plain `git push origin main` fails with `src refspec main does not match any`. Push `master:main` instead.

Never release from the second clone under `~/.claude/plugins/marketplaces/superpower-writing/`. That copy is managed by the plugin loader and updates by fetching origin. It is never the source of a push. The canonical release location is this repo on `master`.

## Recovery

| Condition | Handling |
|-----------|----------|
| Pre-release gate exits non-zero | Stop. Fix the failing check, then re-run the whole gate. Do not tag on a red gate. |
| `git describe` fails (no prior tag) | First release. Pick an initial version and build the changelog from the full `git log --oneline`. |
| `gh` not authenticated | Stop. Ask the user to run `gh auth login`, then retry the release create step. |
| `git push origin main` fails with refspec error | Expected. Push `git push origin master:main --tags` instead. The local branch is `master`. |
| Tag pushed but release create failed | Do not re-tag. Re-run only `gh release create vX.Y.Z` with the changelog notes. |

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| `marketplace.json` left behind | Bump both manifests together and read them back to confirm they match the tag. |
| Tagging on a red or unrun gate | Run all three pre-release checks first. Each must exit 0 before the tag. |
| Silencing a new linter error via the baseline | The baseline is for prior debt only. Fix the new or edited file instead. |
| Tag created before the commit is pushed | Push the commit first, or push `master:main --tags` together. |
| Changelog misses commits | Diff with `prev_tag..HEAD`, computed before tagging, not `prev_tag..new_tag`. |
| Releasing from the marketplace clone | Release from this repo on `master`. The marketplace copy only ever fetches. |

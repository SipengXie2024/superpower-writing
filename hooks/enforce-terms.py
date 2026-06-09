#!/usr/bin/env python3
"""PreToolUse hook enforcing term-definition-before-use protocol (LaTeX).

Reads Claude Code PreToolUse JSON on stdin, writes decision JSON on stdout.
Companion to enforce-claims.py; they run independently on the same file
events. Activation is opt-in: if <writing_root>/glossary.md is absent, this
hook is a no-op.

Contract:
- Input: {"tool_name": "...", "tool_input": {"file_path": "...", ...}}
- Output (allow): silent, exit 0
- Output (block): {"decision": "block", "reason": "..."}, exit 2

Rules:
1. Only intercepts Edit/Write/MultiEdit/NotebookEdit on **/manuscript/*.tex.
2. Feature activates only when <writing_root>/glossary.md exists.
3. `% define: <id>` lines in section NN_<stem>.tex require:
   - id is present in glossary
   - glossary[id].defined_in matches the file stem exactly
4. `% use: <id>` lines in section NN_<stem>.tex require:
   - id is present in glossary
   - glossary[id].defined_in precedes or equals the file stem. Numeric
     prefixes (^\\d+) compare as integers; stems without numeric prefixes
     require exact equality.
5. Within a single file, the first `% define: <id>` line must appear at
   or before the first `% use: <id>` line (intra-section ordering).
6. Sections whose stem matches UNPROTECTED_SLUGS (abstract, references,
   acknowledgments) are fully exempt from the above. `% use:` tags in
   the abstract pass through unchecked — abstracts routinely reference
   terms the body defines later.
"""

from __future__ import annotations

import json
import os
import re
import subprocess
import sys
from pathlib import Path

try:
    import yaml  # type: ignore
except ImportError:
    print(json.dumps({
        "decision": "block",
        "reason": "superpower-writing requires PyYAML: pip install pyyaml"
    }))
    sys.exit(2)


WRITE_TOOLS = {"Edit", "Write", "MultiEdit", "NotebookEdit"}

# LaTeX line-comment tags. Must start the line (optionally after whitespace).
DEFINE_TAG = re.compile(r"(?m)^\s*%\s*define:\s*(\S+)")
USE_TAG = re.compile(r"(?m)^\s*%\s*use:\s*(\S+)")

UNPROTECTED_SLUGS = frozenset({"abstract", "references", "acknowledgments"})

NUMERIC_PREFIX = re.compile(r"^(\d+)")


def _block(reason: str) -> None:
    print(json.dumps({"decision": "block", "reason": f"[superpower-writing] {reason}"}))
    sys.exit(2)


def _allow() -> None:
    sys.exit(0)


def find_writing_root(p: Path) -> Path | None:
    for ancestor in [p] + list(p.parents):
        if ancestor.name == ".writing" and ancestor.is_dir():
            return ancestor
    return None


def plugin_root() -> Path:
    """Canonical plugin root. Prefer CLAUDE_PLUGIN_ROOT (set when the hook runs
    under Claude Code); fall back to this script's grandparent (hooks/ -> root).
    Resolve symlinks so the comparison below is filesystem-true, not lexical."""
    env_root = os.environ.get("CLAUDE_PLUGIN_ROOT")
    if env_root:
        return Path(env_root).resolve()
    return Path(__file__).resolve().parent.parent


def is_plugin_enforcement_file(target: Path) -> bool:
    """True if `target` is one of this plugin's enforcement files: any file
    directly under the plugin's hooks/ directory whose suffix is .py, or
    hooks.json. `target` must already be realpath-resolved (symlinks + `..`
    collapsed). We compare the resolved hooks/ dir against the target's parent
    so a symlinked hooks/ still matches and a sibling path named hooks cannot."""
    hooks_dir = plugin_root() / "hooks"
    try:
        hooks_dir = hooks_dir.resolve()
    except OSError:
        return False
    if target.parent != hooks_dir:
        return False
    return target.suffix == ".py" or target.name == "hooks.json"


def drafting_is_active(payload: dict) -> bool:
    """True when a manuscript-drafting session is in progress, per the plugin's
    own state script. The drafting project root is the session cwd (where
    .writing/ lives), available as CLAUDE_PROJECT_DIR or the payload `cwd`.
    Delegates to scripts/check-writing-state.sh (single source of truth; we do
    not reimplement its `active` logic). Any error means "not active" so this
    signal can only ever ENABLE protection, never spuriously disable a write."""
    project_root = os.environ.get("CLAUDE_PROJECT_DIR") or payload.get("cwd") or ""
    if not project_root:
        return False
    script = plugin_root() / "scripts" / "check-writing-state.sh"
    if not script.exists():
        return False
    try:
        result = subprocess.run(
            ["bash", str(script), project_root],
            capture_output=True, text=True, timeout=5,
        )
    except (OSError, subprocess.SubprocessError):
        return False
    return result.stdout.strip() == "active"


def infra_protection_enabled(payload: dict) -> bool:
    """Master switch for infra self-protection. OFF by default. ON only on an
    explicit opt-in signal: SUPERPOWER_WRITING_PROTECT_INFRA=1, or an active
    drafting session. Kept narrow on purpose so a plain plugin-development
    session (no env var, no .writing/) can freely edit hooks/."""
    if os.environ.get("SUPERPOWER_WRITING_PROTECT_INFRA") == "1":
        return True
    return drafting_is_active(payload)


def apply_edit(content: str, old: str, new: str, replace_all: bool) -> str:
    if not old:
        return content + new
    if replace_all:
        return content.replace(old, new)
    return content.replace(old, new, 1)


def resolve_post_content(tool_name: str, tool_input: dict, file_path: Path) -> str | None:
    if tool_name == "Write":
        return tool_input.get("content", "")
    try:
        original = file_path.read_text(encoding="utf-8") if file_path.exists() else ""
    except OSError:
        return None
    if tool_name == "Edit":
        return apply_edit(
            original,
            tool_input.get("old_string", ""),
            tool_input.get("new_string", ""),
            bool(tool_input.get("replace_all")),
        )
    if tool_name == "MultiEdit":
        content = original
        for edit in tool_input.get("edits", []):
            content = apply_edit(
                content,
                edit.get("old_string", ""),
                edit.get("new_string", ""),
                bool(edit.get("replace_all")),
            )
        return content
    if tool_name == "NotebookEdit":
        return None
    return None


def load_glossary(glossary_path: Path) -> dict[str, dict] | None:
    """Parse glossary; return {id: entry_dict} or None if file missing."""
    if not glossary_path.exists():
        return None
    try:
        data = yaml.safe_load(glossary_path.read_text(encoding="utf-8"))
    except yaml.YAMLError as exc:
        _block(f"glossary file {glossary_path} has YAML error: {exc}")
    if data is None:
        return {}
    if not isinstance(data, list):
        _block(
            f"glossary file {glossary_path} must be a YAML list of entries, "
            f"got {type(data).__name__}"
        )
    entries: dict[str, dict] = {}
    for entry in data:
        if not isinstance(entry, dict):
            continue
        tid = entry.get("id")
        if tid is None:
            continue
        if "defined_in" not in entry or not entry["defined_in"]:
            _block(
                f"glossary entry '{tid}' is missing required field 'defined_in' "
                f"(section stem where the term is first defined)"
            )
        entries[str(tid)] = entry
    return entries


def stem_is_unprotected(stem: str) -> bool:
    for slug in UNPROTECTED_SLUGS:
        if stem == slug or stem.endswith(f"_{slug}"):
            return True
    return False


def stem_order(stem: str) -> tuple[int, str]:
    """Sortable key for section stems. Numeric-prefix compares as int; stems
    without a numeric prefix sort after all numeric stems and fall back to
    alphabetic order among themselves."""
    m = NUMERIC_PREFIX.match(stem)
    if m:
        return (int(m.group(1)), stem)
    return (sys.maxsize, stem)


def stems_ordered(defined_in: str, current: str) -> bool:
    """True if defined_in precedes or equals current in reading order.
    When either stem lacks a numeric prefix, require exact equality —
    non-numeric sections have no safe ordering against numeric ones."""
    d_num = NUMERIC_PREFIX.match(defined_in)
    c_num = NUMERIC_PREFIX.match(current)
    if d_num and c_num:
        return int(d_num.group(1)) <= int(c_num.group(1))
    return defined_in == current


def find_tag_line(content: str, pattern: re.Pattern, target_id: str) -> int | None:
    """Return the 1-based line number of the first match of `pattern` whose
    capture group 1 equals `target_id`, or None."""
    for idx, line in enumerate(content.splitlines(), start=1):
        m = pattern.match(line) or pattern.search(line)
        if m and m.group(1) == target_id:
            return idx
    return None


def main() -> None:
    try:
        payload = json.load(sys.stdin)
    except json.JSONDecodeError:
        _allow()

    tool_name = payload.get("tool_name", "")
    tool_input = payload.get("tool_input", {}) or {}

    if tool_name not in WRITE_TOOLS:
        _allow()

    raw_path = tool_input.get("file_path") or tool_input.get("notebook_path") or ""
    if not raw_path:
        _allow()

    # Resolve symlinks AND `..` together in true filesystem order BEFORE any
    # scope match. Path.resolve() does this; never abspath() first. abspath()
    # collapses `..` LEXICALLY, so `symlinked_manuscript_dir/../escape.tex`
    # would resolve to a sibling of the symlink NAME before the symlink is
    # followed, letting traversal slip past the matcher. resolve() follows the
    # symlink first, so the matcher always sees the real target.
    file_path = Path(raw_path).resolve()

    # Infra self-protection (opt-in, OFF by default). Runs BEFORE the manuscript
    # scope match because the protected files (hooks/*.py, hooks/hooks.json) are
    # not manuscript .tex files. Only fires when explicitly enabled, so a normal
    # plugin-development session can still edit hooks/ freely (no self-lockout).
    if infra_protection_enabled(payload) and is_plugin_enforcement_file(file_path):
        _block(
            f"{file_path.name} is a superpower-writing enforcement file and infra "
            f"self-protection is active (drafting session or "
            f"SUPERPOWER_WRITING_PROTECT_INFRA=1). To edit the plugin's hooks, pause "
            f"drafting or unset SUPERPOWER_WRITING_PROTECT_INFRA, then retry. This "
            f"guard is advisory; it never mutates state."
        )

    if "manuscript" not in file_path.parts or file_path.suffix.lower() != ".tex":
        _allow()

    content = resolve_post_content(tool_name, tool_input, file_path)
    if content is None:
        _allow()

    stem = file_path.stem
    if stem_is_unprotected(stem):
        _allow()

    writing_root = find_writing_root(file_path)
    if writing_root is None:
        _allow()

    glossary_path = writing_root / "glossary.md"
    glossary = load_glossary(glossary_path)
    if glossary is None:
        _allow()

    define_ids = DEFINE_TAG.findall(content)
    use_ids = USE_TAG.findall(content)

    # Rule 3: `% define:` must match glossary.defined_in exactly.
    for tid in define_ids:
        if tid not in glossary:
            _block(
                f"term id '{tid}' tagged `% define:` in {file_path.name} is not "
                f"listed in {glossary_path.name}"
            )
        expected = str(glossary[tid]["defined_in"])
        if expected != stem:
            _block(
                f"term '{tid}' is tagged `% define:` in {file_path.name} but "
                f"glossary says it is defined in '{expected}'. Move the "
                f"definition to {expected}.tex or update glossary.md."
            )

    # Rule 4: `% use:` must reference a known id defined in an earlier
    # (or equal) section.
    for tid in use_ids:
        if tid not in glossary:
            _block(
                f"term id '{tid}' tagged `% use:` in {file_path.name} is not "
                f"listed in {glossary_path.name}. Add the glossary entry "
                f"before using the term."
            )
        defined_in = str(glossary[tid]["defined_in"])
        if not stems_ordered(defined_in, stem):
            _block(
                f"term '{tid}' is used in {file_path.name} but not yet defined "
                f"(glossary says it is defined in '{defined_in}', which comes "
                f"after the current section). Define the term earlier or "
                f"reorder the sections."
            )

    # Rule 5: intra-section define-before-use.
    for tid in set(define_ids) & set(use_ids):
        define_line = find_tag_line(content, DEFINE_TAG, tid)
        use_line = find_tag_line(content, USE_TAG, tid)
        if define_line is not None and use_line is not None and define_line > use_line:
            _block(
                f"term '{tid}' is used on line {use_line} of {file_path.name} "
                f"before its `% define:` on line {define_line}. Move the "
                f"definition earlier within the file."
            )

    _allow()


if __name__ == "__main__":
    main()

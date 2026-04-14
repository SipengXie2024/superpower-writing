#!/usr/bin/env python3
"""PreToolUse hook enforcing claim-first writing protocol.

Reads Claude Code PreToolUse JSON on stdin, writes decision JSON on stdout.

Contract:
- Input: {"tool_name": "...", "tool_input": {"file_path": "...", "content"|"new_string"|"edits": ...}}
- Output (allow): silent, exit 0
- Output (block): {"decision": "block", "reason": "..."}, exit 2

Rules:
1. Only intercept Edit/Write/MultiEdit/NotebookEdit on **/manuscript/*.md.
2. The post-edit content must satisfy: every paragraph either has a
   <!-- claim: id --> tag whose claim STATUS is evidence_ready or verified,
   OR a <!-- draft-only --> tag.
3. Claims live in a sibling claims/section_<stem>.md file.
"""

from __future__ import annotations

import json
import re
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
CLAIM_TAG = re.compile(r"<!--\s*claim:\s*(\S+?)\s*-->")
DRAFT_ONLY_TAG = re.compile(r"<!--\s*draft-only\s*-->")
ALLOWED_STATUSES = {"evidence_ready", "verified"}
# Sections where untagged prose is OK (light-content boilerplate).
UNPROTECTED_STEMS = {"00_abstract", "06_references", "07_acknowledgments"}


def _block(reason: str) -> None:
    print(json.dumps({"decision": "block", "reason": f"[superpower-writing] {reason}"}))
    sys.exit(2)


def _allow() -> None:
    sys.exit(0)


def resolve_post_content(tool_name: str, tool_input: dict, file_path: Path) -> str | None:
    """Produce the full post-edit content for the target file, or None to skip."""
    if tool_name == "Write":
        return tool_input.get("content", "")

    # Edit / MultiEdit operate on existing files.
    try:
        original = file_path.read_text(encoding="utf-8") if file_path.exists() else ""
    except OSError:
        return None

    if tool_name == "Edit":
        old = tool_input.get("old_string", "")
        new = tool_input.get("new_string", "")
        if tool_input.get("replace_all"):
            return original.replace(old, new) if old else original + new
        return original.replace(old, new, 1) if old else original + new

    if tool_name == "MultiEdit":
        content = original
        for edit in tool_input.get("edits", []):
            old = edit.get("old_string", "")
            new = edit.get("new_string", "")
            if edit.get("replace_all"):
                content = content.replace(old, new) if old else content + new
            else:
                content = content.replace(old, new, 1) if old else content + new
        return content

    if tool_name == "NotebookEdit":
        # Notebooks bundle cells; we don't enforce claim tags on notebooks.
        # Pass through — notebooks are rarely used for manuscript prose.
        return None

    return None


def load_claims(claims_path: Path) -> dict[str, str] | None:
    """Parse claims file; return {claim_id: status} or None if file missing."""
    if not claims_path.exists():
        return None
    try:
        data = yaml.safe_load(claims_path.read_text(encoding="utf-8"))
    except yaml.YAMLError as exc:
        _block(f"claim file {claims_path} has YAML error: {exc}")
    if data is None:
        return {}
    if not isinstance(data, list):
        _block(f"claim file {claims_path} must be a YAML list, got {type(data).__name__}")
    claims: dict[str, str] = {}
    for entry in data:
        if not isinstance(entry, dict):
            continue
        cid = entry.get("id")
        status = entry.get("STATUS") or entry.get("status") or "stub"
        if cid is not None:
            claims[str(cid)] = str(status)
    return claims


def content_has_real_prose(content: str) -> bool:
    """True if content contains any non-whitespace, non-comment line."""
    for raw in content.splitlines():
        line = raw.strip()
        if not line:
            continue
        if line.startswith("<!--") and line.endswith("-->"):
            continue
        if line.startswith("#"):  # markdown headers are allowed anywhere
            continue
        return True
    return False


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

    file_path = Path(raw_path).resolve()

    # Match any file under a manuscript/ directory at any depth ending in .md.
    if "manuscript" not in file_path.parts or file_path.suffix.lower() != ".md":
        _allow()

    content = resolve_post_content(tool_name, tool_input, file_path)
    if content is None:
        _allow()

    # Locate sibling claims file: <base>/claims/section_<stem>.md
    stem = file_path.stem
    writing_root = file_path.parent.parent
    claims_path = writing_root / "claims" / f"section_{stem}.md"

    claim_ids = CLAIM_TAG.findall(content)
    has_draft_only = bool(DRAFT_ONLY_TAG.search(content))

    # If only draft-only or only comments/headers, allow.
    if not claim_ids and has_draft_only:
        _allow()

    # Untagged prose in a protected section -> block.
    if not claim_ids and content_has_real_prose(content):
        if stem in UNPROTECTED_STEMS:
            _allow()
        _block(
            f"every load-bearing paragraph in {file_path.name} must be tagged "
            f"<!-- claim: id --> or <!-- draft-only -->"
        )

    # No prose at all -> allow.
    if not claim_ids:
        _allow()

    # Claim tags exist -> claims file must too.
    claims = load_claims(claims_path)
    if claims is None:
        _block(f"claim file {claims_path} is missing but {file_path.name} references claims")

    for cid in claim_ids:
        if cid not in claims:
            _block(
                f"claim id '{cid}' referenced in {file_path.name} is not defined in "
                f"{claims_path.name}"
            )
        status = claims[cid]
        if status not in ALLOWED_STATUSES:
            _block(
                f"claim '{cid}' has STATUS={status}; resolve EVIDENCE via "
                f"research-lookup / citation-management and set STATUS=evidence_ready "
                f"before writing prose (claim file: {claims_path.name})"
            )

    _allow()


if __name__ == "__main__":
    main()

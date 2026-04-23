#!/usr/bin/env python3
"""PreToolUse hook enforcing claim-first writing protocol (LaTeX).

Reads Claude Code PreToolUse JSON on stdin, writes decision JSON on stdout.

Contract:
- Input: {"tool_name": "...", "tool_input": {"file_path": "...", "content"|"new_string"|"edits": ...}}
- Output (allow): silent, exit 0
- Output (block): {"decision": "block", "reason": "..."}, exit 2

Rules:
1. Only intercept Edit/Write/MultiEdit/NotebookEdit on **/manuscript/*.tex.
2. The post-edit content must satisfy: every load-bearing line either has a
   `% claim: id` tag whose claim STATUS is evidence_ready or verified,
   OR a `% draft-only` tag.
3. Claims live in a sibling claims/section_<stem>.md file.
4. Sections whose stem is or ends in `_<slug>` for slug in UNPROTECTED_SLUGS
   (abstract, references, acknowledgments) are exempt from paragraph-tag
   enforcement (boilerplate / auto-generated).
5. Sections whose stem is or ends in `_<slug>` for slug in CITATION_FREE_SLUGS
   (abstract) must not contain LaTeX citation commands (`\cite`, `\citep`,
   `\citet`, `\nocite`, `\parencite`, etc.) or `% claim:` tags. Abstracts are
   self-contained summaries; the body carries the references.
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

# LaTeX line-comment tags: `% claim: id` or `% draft-only`. Must be at start of
# line (possibly after leading whitespace). Captures claim id as first \S+ token.
CLAIM_TAG = re.compile(r"(?m)^\s*%\s*claim:\s*(\S+)")
DRAFT_ONLY_TAG = re.compile(r"(?m)^\s*%\s*draft-only\b")

ALLOWED_STATUSES = {"evidence_ready", "verified"}

# Slugs whose sections are exempt from paragraph-tag enforcement. Matched by
# slug-ending against the file stem: `00_abstract` ends in `_abstract` (matches);
# `09_references` ends in `_references` (matches); `03_methods` does not end in
# any unprotected slug (does not match; must carry tags).
UNPROTECTED_SLUGS = frozenset({"abstract", "references", "acknowledgments"})

# Slugs whose sections MUST NOT contain citations or claim tags. Matched by
# slug-ending like UNPROTECTED_SLUGS. Convention: the abstract is a
# self-contained summary of the paper's own findings; citations belong in the
# body sections. References legitimately contain bib commands and
# acknowledgments legitimately may cite grants, so they are NOT in this set.
CITATION_FREE_SLUGS = frozenset({"abstract"})

# Any LaTeX command whose name contains "cite" — matches \cite, \cites,
# \citep, \citet, \citeauthor, \citeyear, \citealt, \citealp, \nocite,
# \parencite, \textcite, \autocite, \footcite, etc. Word-boundary suffix
# avoids matching command names that merely start the same prefix.
CITE_COMMAND = re.compile(r"\\[a-zA-Z]*cite[a-zA-Z]*\b")

# LaTeX structural commands that do not count as "load-bearing prose" on their
# own. Lines starting with one of these commands are treated as scaffolding.
STRUCTURAL_LATEX_CMDS = frozenset({
    "section", "subsection", "subsubsection", "paragraph", "subparagraph",
    "chapter", "part", "begin", "end", "label", "caption",
    "bibliography", "bibliographystyle", "printbibliography",
    "usepackage", "documentclass", "input", "include",
    "title", "author", "date", "maketitle", "tableofcontents",
    "listoffigures", "listoftables", "newpage", "clearpage",
})
STRUCTURAL_LATEX_LINE = re.compile(r"^\s*\\(\w+)\b")


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


def apply_edit(content: str, old: str, new: str, replace_all: bool) -> str:
    if not old:
        return content + new
    if replace_all:
        return content.replace(old, new)
    return content.replace(old, new, 1)


def resolve_post_content(tool_name: str, tool_input: dict, file_path: Path) -> str | None:
    """Produce the full post-edit content for the target file, or None to skip."""
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
    """True if content contains any non-whitespace, non-comment, non-structural line."""
    for raw in content.splitlines():
        line = raw.strip()
        if not line:
            continue
        if line.startswith("%"):
            continue
        m = STRUCTURAL_LATEX_LINE.match(line)
        if m and m.group(1) in STRUCTURAL_LATEX_CMDS:
            continue
        return True
    return False


def stem_is_unprotected(stem: str) -> bool:
    """True if the file stem represents a boilerplate section exempt from tagging."""
    for slug in UNPROTECTED_SLUGS:
        if stem == slug or stem.endswith(f"_{slug}"):
            return True
    return False


def stem_is_citation_free(stem: str) -> bool:
    """True if the file stem names a section that must not carry citations."""
    for slug in CITATION_FREE_SLUGS:
        if stem == slug or stem.endswith(f"_{slug}"):
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

    # Match any file under a manuscript/ directory at any depth ending in .tex.
    if "manuscript" not in file_path.parts or file_path.suffix.lower() != ".tex":
        _allow()

    content = resolve_post_content(tool_name, tool_input, file_path)
    if content is None:
        _allow()

    stem = file_path.stem
    writing_root = find_writing_root(file_path)
    if writing_root is None:
        _allow()
    claims_path = writing_root / "claims" / f"section_{stem}.md"

    # Citation-free sections (abstract): block any LaTeX citation command or
    # claim tag. The abstract restates the paper's own findings; citations
    # live in the body. Runs before the claim-tag checks below so the user
    # gets the more specific error message.
    if stem_is_citation_free(stem):
        cite_match = CITE_COMMAND.search(content)
        if cite_match:
            _block(
                f"{file_path.name} must not contain citations; found "
                f"`{cite_match.group(0)}` (abstract is citation-free; move "
                f"references to a body section)"
            )
        if CLAIM_TAG.search(content):
            _block(
                f"{file_path.name} must not contain `% claim: id` tags; "
                f"abstract sections have no claim file by contract "
                f"(see outlining/SKILL.md §Filename-stem contract)"
            )

    claim_ids = CLAIM_TAG.findall(content)
    has_draft_only = bool(DRAFT_ONLY_TAG.search(content))

    if not claim_ids and has_draft_only:
        _allow()

    if not claim_ids and content_has_real_prose(content):
        if stem_is_unprotected(stem):
            _allow()
        _block(
            f"every load-bearing paragraph in {file_path.name} must be tagged "
            f"`% claim: id` or `% draft-only` (LaTeX line comments at column 0)"
        )

    if not claim_ids:
        _allow()

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

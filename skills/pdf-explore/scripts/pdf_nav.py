"""Navigate a PDF too big to drop into context, without an LLM.

Local, no-API helpers for reading a long PDF (a paper you're reviewing, a
reference you're citing, a spec) a piece at a time instead of embedding the
whole file:

    outline(path)              -> [{page, level, title}]  table of contents
    page_text(path, pages)     -> [{page, text}]          text of chosen pages
    search(path, pattern, ...) -> [{page, line, snippet}] keyword / regex hits
    n_pages(path)              -> int

Also a CLI, so it works standalone from a review or generator script::

    python3 pdf_nav.py outline  paper.pdf
    python3 pdf_nav.py text     paper.pdf 5,21-25,62
    python3 pdf_nav.py search   paper.pdf "batch.?normalization" --regex
    python3 pdf_nav.py pages    paper.pdf

Backend: pypdf (pure Python, ``pip install pypdf``). Text extraction is good
enough to navigate by and to read prose off; it is not a layout-faithful
renderer. To read a value or label off a *figure*, open that page as an image
with the Read tool instead (``Read(paper.pdf, pages="5")``) -- this script is
for text.

Why it exists: dropping a 50-page PDF into context is ~200K tokens, and pages
opened as images evaporate after one turn, so multi-section work loops on
re-reading them. Pull the outline, find the pages you need, read only those.
For an exhaustive per-page sweep ("list every dataset this paper reports on")
the text this returns feeds a subagent fan-out -- see SKILL.md.
"""

import re
import sys


def _reader(path):
    try:
        from pypdf import PdfReader
    except ImportError:  # pragma: no cover
        sys.exit("pdf_nav needs pypdf: pip install pypdf")
    return PdfReader(path)


def n_pages(path):
    return len(_reader(path).pages)


def _walk_outline(reader, items, level, out):
    for it in items:
        if isinstance(it, list):
            _walk_outline(reader, it, level + 1, out)
            continue
        title = getattr(it, "title", None)
        if title is None:
            continue
        try:
            page = reader.get_destination_page_number(it) + 1  # 1-based
        except Exception:
            page = None
        out.append({"page": page, "level": level, "title": str(title).strip()})


def outline(path):
    """The PDF's bookmark tree as a flat list with 1-based levels and pages."""
    reader = _reader(path)
    out = []
    try:
        items = reader.outline
    except Exception:
        items = []
    _walk_outline(reader, items, 1, out)
    return out


def _parse_pages(spec, total):
    """'5,21-25,62' -> [5,21,22,23,24,25,62], 1-based, clamped, de-duped, in order."""
    pages = []
    for chunk in str(spec).split(","):
        chunk = chunk.strip()
        if not chunk:
            continue
        try:
            if "-" in chunk:
                a, b = chunk.split("-", 1)
                pages.extend(range(int(a), int(b) + 1))
            else:
                pages.append(int(chunk))
        except ValueError:
            continue  # skip a malformed token like '5-' or 'x'
    seen, ordered = set(), []
    for p in pages:
        if 1 <= p <= total and p not in seen:
            seen.add(p)
            ordered.append(p)
    return ordered


def page_text(path, pages=None):
    """Text of the given 1-based pages (all pages when pages is None)."""
    reader = _reader(path)
    total = len(reader.pages)
    if pages is None:
        want = list(range(1, total + 1))
    elif isinstance(pages, str):
        want = _parse_pages(pages, total)
    else:
        want = [p for p in pages if 1 <= p <= total]
    out = []
    for p in want:
        try:
            txt = reader.pages[p - 1].extract_text() or ""
        except Exception:
            txt = ""
        out.append({"page": p, "text": txt})
    return out


def search(path, pattern, regex=False, ignore_case=True, context=60):
    """Find a keyword or regex across the whole document.

    Returns [{page, line, snippet}]. For "where do they discuss X" with no
    shared keyword, read the outline and skim the section instead -- this is a
    literal/regex locator, not a semantic search.
    """
    flags = re.IGNORECASE if ignore_case else 0
    rx = re.compile(pattern if regex else re.escape(pattern), flags)
    out = []
    for rec in page_text(path):
        for i, line in enumerate(rec["text"].splitlines(), 1):
            m = rx.search(line)
            if not m:
                continue
            s = max(0, m.start() - context)
            e = min(len(line), m.end() + context)
            snippet = ("…" if s > 0 else "") + line[s:e].strip() + ("…" if e < len(line) else "")
            out.append({"page": rec["page"], "line": i, "snippet": snippet})
    return out


def _cli(argv):
    if len(argv) < 3:
        print(__doc__)
        return 1
    cmd, path, rest = argv[1], argv[2], argv[3:]
    if cmd == "pages":
        print(n_pages(path))
    elif cmd == "outline":
        rows = outline(path)
        if not rows:
            print("(no embedded outline -- try `search` or read by page range)")
        for e in rows:
            pg = f"p{e['page']}" if e["page"] else "p?"
            print(f"{pg:>5}  {'  ' * (e['level'] - 1)}{e['title']}")
    elif cmd == "text":
        spec = rest[0] if rest else None
        for rec in page_text(path, spec):
            print(f"\n── page {rec['page']} ──\n{rec['text']}")
    elif cmd == "search":
        use_regex = "--regex" in rest
        positional = [a for a in rest if a != "--regex"]
        pat = positional[0] if positional else ""
        for h in search(path, pat, regex=use_regex):
            print(f"p{h['page']}:{h['line']}  {h['snippet']}")
    else:
        print(f"unknown command: {cmd}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(_cli(sys.argv))

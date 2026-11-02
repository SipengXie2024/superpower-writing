#!/usr/bin/env python3
"""Find the passages of a fetched paper that bear on a claim, and check quotes.

Works on the page-delimited text written by fetch_fulltext.py (pages separated
by form feeds). Two modes:

  --query "<claim sentence>"   rank the paper's paragraphs by overlap with the
                               claim's content words and print the top passages
                               with their page numbers, so the reader opens the
                               right part of the paper instead of the whole text.
  --quote "<verbatim excerpt>" confirm the excerpt occurs in the paper and report
                               its page. Matching ignores case, whitespace, line-
                               break hyphenation, ligatures and punctuation, so a
                               quote copied from the PDF still matches the
                               extracted text. Quotes shorter than 8 words are
                               rejected: they match too easily to prove anything.

Usage:
    python3 find_passages.py .writing/papers/Kwon2023vllm.txt --query "paging the KV cache cuts memory waste" --top 5
    python3 find_passages.py .writing/papers/Kwon2023vllm.txt --quote "reduces the KV cache memory waste ..." --json

Exit codes: 0 found, 1 quote not found / no passage matched, 2 usage error.
"""

from __future__ import annotations

import argparse
import json
import math
import re
import sys
import unicodedata
from collections import Counter
from pathlib import Path

MIN_QUOTE_WORDS = 8
STOPWORDS = set(
    "a an the and or of to in on for with by from as at is are was were be been being this that these those "
    "it its we our us they their them which who whom whose than then there here can could may might will would "
    "shall should do does did not no but if so such into over under between about across per via using use used "
    "also more most less least very each both all any some other only same own up down out new show shows shown".split()
)


def loose(text: str) -> str:
    """Lowercase alphanumerics; survives hyphenation, ligatures, wrapping and quote styles.

    A separator between two digits is kept as "|", so "2-4x" and "24x" stay different.
    """
    text = unicodedata.normalize("NFKC", text).lower()
    text = re.sub(r"(?<=\d)[^0-9a-z]+(?=\d)", "|", text)
    return re.sub(r"[^0-9a-z|]+", "", text)


def tokens(text: str) -> list[str]:
    text = unicodedata.normalize("NFKC", text).lower()
    text = re.sub(r"(\w)-\s*\n\s*(\w)", r"\1\2", text)
    return [t for t in re.findall(r"[a-z][a-z0-9]+|\d+(?:\.\d+)?", text) if t not in STOPWORDS and len(t) > 1]


def load_pages(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8", errors="replace")
    pages = text.split("\f")
    if pages and not pages[-1].strip():
        pages = pages[:-1]
    if not pages:
        print(f"[ERROR] {path} is empty", file=sys.stderr)
        raise SystemExit(2)
    return pages


def paragraphs(pages: list[str]) -> list[tuple[int, str]]:
    """Split pages into paragraphs (blank-line separated), merging fragments under 40 words."""
    out: list[tuple[int, str]] = []
    for pno, page in enumerate(pages, start=1):
        buf = ""
        for block in re.split(r"\n\s*\n", page):
            block = " ".join(block.split())
            if not block:
                continue
            buf = f"{buf} {block}".strip()
            if len(buf.split()) >= 40:
                out.append((pno, buf))
                buf = ""
        if buf:
            out.append((pno, buf))
    return out


def rank(paras: list[tuple[int, str]], query: str, top: int) -> list[dict]:
    q = Counter(tokens(query))
    if not q:
        print("[ERROR] query has no content words", file=sys.stderr)
        raise SystemExit(2)
    docs = [Counter(tokens(p)) for _, p in paras]
    n = len(docs)
    df = Counter(t for d in docs for t in set(d))
    avg = sum(sum(d.values()) for d in docs) / max(n, 1)
    k1, b = 1.5, 0.75
    scored = []
    for (pno, text), d in zip(paras, docs):
        length = sum(d.values())
        s = 0.0
        for t in q:
            if t not in d:
                continue
            idf = math.log(1 + (n - df[t] + 0.5) / (df[t] + 0.5))
            s += idf * d[t] * (k1 + 1) / (d[t] + k1 * (1 - b + b * length / avg))
        if s > 0:
            scored.append({"page": pno, "score": round(s, 2),
                           "matched_terms": sorted(t for t in q if t in d), "passage": text})
    scored.sort(key=lambda x: -x["score"])
    return scored[:top]


def find_quote(pages: list[str], quote: str) -> dict:
    words = len(quote.split())
    if words < MIN_QUOTE_WORDS:
        print(f"[ERROR] quote has {words} words; give at least {MIN_QUOTE_WORDS}", file=sys.stderr)
        raise SystemExit(2)
    needle = loose(quote)
    for pno, page in enumerate(pages, start=1):
        if needle in loose(page):
            return {"quote_verified": True, "page": pno}
    # A quote may straddle a page break.
    for pno in range(1, len(pages)):
        if needle in loose(pages[pno - 1] + " " + pages[pno]):
            return {"quote_verified": True, "page": f"{pno}-{pno + 1}"}
    return {"quote_verified": False, "page": None}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("text", help="page-delimited text from fetch_fulltext.py")
    mode = ap.add_mutually_exclusive_group(required=True)
    mode.add_argument("--query", help="claim sentence to rank passages against")
    mode.add_argument("--quote", help="verbatim excerpt to locate")
    ap.add_argument("--top", type=int, default=5, help="passages to print in --query mode (default 5)")
    ap.add_argument("--json", action="store_true", help="print JSON")
    args = ap.parse_args()

    path = Path(args.text)
    if not path.is_file():
        print(f"[ERROR] {path} not found", file=sys.stderr)
        return 2
    pages = load_pages(path)

    if args.quote is not None:
        result = {"text": str(path), "quote": args.quote, **find_quote(pages, args.quote)}
        if args.json:
            print(json.dumps(result, indent=2, ensure_ascii=False))
        else:
            status = f"FOUND on page {result['page']}" if result["quote_verified"] else "NOT FOUND"
            print(f"{status}: {args.quote}")
        return 0 if result["quote_verified"] else 1

    hits = rank(paragraphs(pages), args.query, args.top)
    if args.json:
        print(json.dumps({"text": str(path), "query": args.query, "passages": hits}, indent=2, ensure_ascii=False))
    else:
        for h in hits:
            print(f"--- page {h['page']}  score {h['score']}  terms {', '.join(h['matched_terms'])}")
            print(h["passage"])
            print()
    return 0 if hits else 1


if __name__ == "__main__":
    sys.exit(main())

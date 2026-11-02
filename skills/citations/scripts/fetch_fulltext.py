#!/usr/bin/env python3
"""Fetch a cited paper's full text and store it as page-delimited plain text.

Given a DOI, an arXiv id, or a local PDF (a Zotero attachment or a file the
user supplied), the script finds an open PDF, checks that it really is a PDF,
and writes three files under --out-dir:

    <key>.pdf    the downloaded PDF (skipped for --pdf input)
    <key>.txt    pdftotext output; pages are separated by form feeds (\\f)
    <key>.json   provenance: identifier, source URL, version, page and word counts

Download order for a DOI: open-access PDF locations listed by OpenAlex
(published version first), then the arXiv preprint found through OpenAlex or
Semantic Scholar. Every attempted URL is reported. When no route yields a PDF
the script exits 1 and prints the landing page plus the URLs that refused a
script (HTTP 403, a challenge page); those usually open in a desktop browser,
and the saved file goes back in through --pdf.

Usage:
    python3 fetch_fulltext.py --doi 10.1145/3600006.3613165 --key Kwon2023vllm --out-dir .writing/papers
    python3 fetch_fulltext.py --arxiv 2309.06180 --key Kwon2023vllm --out-dir .writing/papers
    python3 fetch_fulltext.py --pdf ~/Zotero/storage/ABCD1234/paper.pdf --key Kwon2023vllm --out-dir .writing/papers

Environment: OPENALEX_API_KEY and OPENALEX_MAILTO are passed to OpenAlex when set.
Exit codes: 0 text written, 1 no PDF obtainable, 2 usage error.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

import requests

UA = "superpower-writing-fulltext/1.0 (+https://github.com/SipengXie2024/superpower-writing)"
BROWSER_UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36"
TIMEOUT = 60


def openalex_params() -> dict:
    params = {}
    if os.environ.get("OPENALEX_API_KEY"):
        params["api_key"] = os.environ["OPENALEX_API_KEY"]
    if os.environ.get("OPENALEX_MAILTO"):
        params["mailto"] = os.environ["OPENALEX_MAILTO"]
    return params


def openalex_work(doi: str) -> dict | None:
    r = requests.get(
        f"https://api.openalex.org/works/doi:{doi}",
        params=openalex_params(),
        headers={"User-Agent": UA},
        timeout=TIMEOUT,
    )
    if r.status_code == 404:
        return None
    r.raise_for_status()
    return r.json()


def s2_arxiv_id(doi: str) -> str | None:
    r = requests.get(
        f"https://api.semanticscholar.org/graph/v1/paper/DOI:{doi}",
        params={"fields": "externalIds"},
        headers={"User-Agent": UA},
        timeout=TIMEOUT,
    )
    if r.status_code in (404, 429):
        return None
    r.raise_for_status()
    return (r.json().get("externalIds") or {}).get("ArXiv")


def arxiv_id_from_openalex(work: dict) -> str | None:
    for loc in work.get("locations") or []:
        for url in (loc.get("landing_page_url") or "", loc.get("pdf_url") or ""):
            m = re.search(r"arxiv\.org/(?:abs|pdf)/([0-9]{4}\.[0-9]{4,5}|[a-z\-]+/[0-9]{7})", url)
            if m:
                return m.group(1)
    return None


def candidate_urls(doi: str) -> tuple[list[tuple[str, str]], str | None]:
    """Return ([(url, version)], landing_page) for a DOI, published versions first."""
    work = openalex_work(doi)
    if work is None:
        print(f"[WARN] OpenAlex has no record for DOI {doi}", file=sys.stderr)
    published: list[tuple[str, str]] = []
    other: list[tuple[str, str]] = []
    landing = f"https://doi.org/{doi}"
    arxiv = None
    if work is not None:
        for loc in work.get("locations") or []:
            url = loc.get("pdf_url")
            if not url or not loc.get("is_oa"):
                continue
            version = loc.get("version") or "unknown"
            (published if version == "publishedVersion" else other).append((url, version))
        arxiv = arxiv_id_from_openalex(work)
    if arxiv is None:
        arxiv = s2_arxiv_id(doi)
    urls = published + other
    if arxiv:
        urls.append((f"https://arxiv.org/pdf/{arxiv}", "arXiv preprint"))
    seen: set[str] = set()
    unique = [(u, v) for u, v in urls if not (u in seen or seen.add(u))]
    return unique, landing


def download_pdf(url: str, dest: Path) -> str | None:
    """Download url to dest; return None on success, else a one-line reason."""
    for ua in (UA, BROWSER_UA):
        try:
            r = requests.get(url, headers={"User-Agent": ua}, timeout=TIMEOUT, allow_redirects=True)
        except requests.RequestException as e:
            reason = f"request failed: {type(e).__name__}"
            continue
        if r.status_code != 200:
            reason = f"HTTP {r.status_code}"
            continue
        if not r.content.startswith(b"%PDF"):
            reason = f"not a PDF (content-type {r.headers.get('content-type', '?')})"
            continue
        dest.write_bytes(r.content)
        return None
    return reason


def pdf_to_text(pdf: Path, txt: Path) -> None:
    if shutil.which("pdftotext") is None:
        print("[ERROR] pdftotext not found; install poppler-utils", file=sys.stderr)
        raise SystemExit(2)
    subprocess.run(["pdftotext", "-enc", "UTF-8", str(pdf), str(txt)], check=True)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    src = ap.add_mutually_exclusive_group(required=True)
    src.add_argument("--doi", help="bare DOI, e.g. 10.1145/3600006.3613165")
    src.add_argument("--arxiv", help="arXiv id, e.g. 2309.06180")
    src.add_argument("--pdf", help="local PDF, e.g. a Zotero attachment")
    ap.add_argument("--key", required=True, help="citation key; names the output files")
    ap.add_argument("--out-dir", default=".writing/papers", help="output directory (default .writing/papers)")
    args = ap.parse_args()

    if not re.fullmatch(r"[A-Za-z0-9_.:\-]+", args.key):
        print(f"[ERROR] citation key {args.key!r} has characters unsafe for a file name", file=sys.stderr)
        return 2
    out = Path(args.out_dir)
    out.mkdir(parents=True, exist_ok=True)
    pdf_path = out / f"{args.key}.pdf"
    txt_path = out / f"{args.key}.txt"
    meta_path = out / f"{args.key}.json"

    meta: dict = {"key": args.key, "fetched_at": datetime.now(timezone.utc).isoformat(timespec="seconds")}
    attempts: list[dict] = []

    if args.pdf:
        local = Path(args.pdf).expanduser()
        if not local.is_file() or not local.read_bytes()[:4] == b"%PDF":
            print(f"[ERROR] {local} is not a readable PDF", file=sys.stderr)
            return 2
        pdf_path = local
        meta.update({"identifier": f"file:{local}", "source_url": str(local), "version": "local file"})
    else:
        doi = args.doi.strip().removeprefix("https://doi.org/").removeprefix("doi:") if args.doi else None
        if doi:
            urls, landing = candidate_urls(doi)
            meta["identifier"] = f"doi:{doi}"
        else:
            arxiv = args.arxiv.strip().removeprefix("arXiv:")
            urls, landing = [(f"https://arxiv.org/pdf/{arxiv}", "arXiv preprint")], f"https://arxiv.org/abs/{arxiv}"
            meta["identifier"] = f"arxiv:{arxiv}"
        got = None
        for url, version in urls:
            reason = download_pdf(url, pdf_path)
            attempts.append({"url": url, "version": version, "result": reason or "ok"})
            if reason is None:
                got = (url, version)
                break
        if got is None:
            blocked = [a["url"] for a in attempts if a["result"] in ("HTTP 403", "HTTP 401")
                       or a["result"].startswith("not a PDF")]
            print(json.dumps({"ok": False, "identifier": meta["identifier"], "attempts": attempts,
                              "blocked_for_scripts": blocked, "landing_page": landing}, indent=2))
            print("[ERROR] no PDF obtainable from this machine; open a blocked_for_scripts URL in a desktop "
                  "browser, or attach the PDF to the Zotero item, then rerun with --pdf", file=sys.stderr)
            return 1
        meta.update({"source_url": got[0], "version": got[1]})

    pdf_to_text(pdf_path, txt_path)
    text = txt_path.read_text(encoding="utf-8", errors="replace")
    pages = text.split("\f")
    if pages and not pages[-1].strip():
        pages = pages[:-1]
    words = len(text.split())
    if words < 500:
        print(f"[ERROR] extracted only {words} words; the PDF is likely scanned or truncated", file=sys.stderr)
        return 1
    meta.update({"pdf": str(pdf_path), "text": str(txt_path), "pages": len(pages), "words": words,
                 "attempts": attempts})
    meta_path.write_text(json.dumps(meta, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"ok": True, **meta}, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())

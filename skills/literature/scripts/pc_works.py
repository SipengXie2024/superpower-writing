#!/usr/bin/env python3
"""Shortlist program-committee members' papers that connect to a manuscript.

Input is a TSV of PC members copied from the venue's saved committee page, one
member per line: `Name<TAB>Affiliation[<TAB>OpenAlexAuthorIds]` (lines starting
with # are ignored). For each member the script:

  1. Finds the member's OpenAlex author record. The record must carry the
     member's first and last name and an institution matching the affiliation
     printed on the PC page; common names have many homonyms, and the
     institution is what tells them apart. OpenAlex sometimes splits one person
     into several records at the same institution; every record matching both
     name and institution is merged. A member with no match is reported as
     unresolved together with the nearest records, so a person can pick the
     right one and put its id (several joined with |) in the optional third
     column, which skips the lookup on the next run.
  2. Lists the member's most recent works since --since (one page of 200) and
     scores each against the manuscript:
        cited_by_refs   the work appears in the reference lists of papers the
                        manuscript already cites (strongest signal: the work
                        the paper's own field builds on)
        cites_refs      how many of the manuscript's references the work cites
        topic_hit       at least two of the --topic words appear in the
                        work's title or abstract
     Only works in a research subfield that the manuscript's own references
     occupy (OpenAlex primary topic) are scored; when several same-name records
     match one institution, the records outside those subfields are dropped.
     Works already in refs.bib are listed separately as already cited, and a
     preprint and its published version count as one paper.

The output is a shortlist for reading, never a list to cite: every candidate
still has to pass the full-text relevance check before it enters the paper.

Usage:
    python3 pc_works.py pc.tsv --refs .writing/refs.bib --topic "speculative execution of blockchain transactions" \\
        --since 2019 --out .writing/sources/pc-shortlist.json

Each member costs one author search and one works list. Without
OPENALEX_API_KEY these come out of a small free daily budget shared by everyone
behind this machine's IP address, which a full PC can exhaust; a free key
(https://openalex.org/settings/api) gives the run its own budget.
OPENALEX_MAILTO is passed along when set. The output file is rewritten after
every member and members already in it are skipped, so a run stopped by the
quota resumes where it stopped; unresolved members are retried on every run.
Exit codes: 0 shortlist written, 2 usage error. Network and quota errors raise.
"""

from __future__ import annotations

import argparse
import json
import math
import os
import re
import sys
import time
import unicodedata
from pathlib import Path

import requests

API = "https://api.openalex.org"
UA = "superpower-writing-pc/1.0 (+https://github.com/SipengXie2024/superpower-writing)"
GENERIC = {"university", "univ", "of", "the", "institute", "inst", "and", "at", "college", "school", "de", "di",
           "der", "des", "la", "le", "for", "department", "dept", "lab", "labs", "laboratory", "research", "center",
           "centre", "inc", "ltd", "corp", "co", "national", "science", "sciences"}
# Abbreviations PC pages use for words OpenAlex spells out.
ALIASES = {"tu": ["technical"], "mpi": ["max", "planck"], "eth": ["eth", "zurich"], "epfl": ["polytechnique", "lausanne"],
           "uiuc": ["illinois", "urbana", "champaign"], "ucb": ["california", "berkeley"],
           "ucla": ["california", "los", "angeles"], "ucsd": ["california", "san", "diego"],
           "mit": ["massachusetts", "technology"], "cmu": ["carnegie", "mellon"], "kaist": ["korea", "advanced"],
           "nus": ["national", "singapore"], "ntu": ["nanyang", "technological"], "sjtu": ["shanghai", "jiao", "tong"],
           "ustc": ["china", "technology"], "hkust": ["hong", "kong", "technology"], "uw": ["washington"]}
SESSION = requests.Session()
SESSION.headers.update({"User-Agent": UA})
PER_PAGE = 200


def get(path: str, **params) -> dict:
    if os.environ.get("OPENALEX_API_KEY"):
        params["api_key"] = os.environ["OPENALEX_API_KEY"]
    if os.environ.get("OPENALEX_MAILTO"):
        params["mailto"] = os.environ["OPENALEX_MAILTO"]
    for attempt in range(4):
        r = SESSION.get(f"{API}{path}", params=params, timeout=60)
        if r.status_code != 429:
            break
        time.sleep(2 ** attempt)
    if r.status_code >= 400:
        raise RuntimeError(f"OpenAlex {r.status_code} for {path}: {r.text[:300]}")
    return r.json()


def norm_words(s: str) -> list[str]:
    s = unicodedata.normalize("NFKD", s)
    s = "".join(c for c in s if not unicodedata.combining(c)).lower()
    s = re.sub(r"(?<=[a-z])-(?=[a-z])", "", s)  # "Hai-Bo" and "Haibo" are one name
    return re.findall(r"[a-z0-9]+", s)


def significant_seq(s: str) -> list[str]:
    s = "".join(c for c in unicodedata.normalize("NFKD", s) if not unicodedata.combining(c))
    words: list[str] = []
    for w in re.findall(r"[a-z0-9]+", s.lower()):
        words.extend(ALIASES.get(w, [w]))
    return [w for w in words if w not in GENERIC]


def institution_matches(pc_affil: str, inst: str) -> bool:
    # OpenAlex appends the country: "Google (United States)".
    inst = re.sub(r"\s*\([^)]*\)\s*$", "", inst)
    b_seq = significant_seq(inst)
    b = set(b_seq)
    inst_univ_of = bool(re.match(r"\s*(?:the\s+)?university of\b", inst, re.I))
    # PC pages list joint appointments: "Microsoft Azure and University of Washington".
    for part in re.split(r"\s+and\s+|\s*[,;&/]\s*", pc_affil):
        a_seq = significant_seq(part)
        a = set(a_seq)
        # "University of Miami" and "Miami University" are different schools, as are
        # "University of Washington" and "Washington University in St. Louis".
        if not a or not b or bool(re.match(r"\s*(?:the\s+)?university of\b", part, re.I)) != inst_univ_of:
            continue
        if a == b or len(a & b) / len(a | b) >= 0.5:
            return True
        # PC pages shorten, OpenAlex appends the campus: "Purdue University" opens
        # "Purdue University West Lafayette". Only the PC side may be the shorter one,
        # so "Shanghai Jiao Tong University" never opens into "Shanghai University".
        if len(a_seq) < len(b_seq) and b_seq[:len(a_seq)] == a_seq:
            return True
    return False


def name_matches(pc_name: str, record_names: list[str]) -> bool:
    """Same last name and same first given name; a bare initial matches nothing."""
    target = norm_words(pc_name)
    first, last = target[0], target[-1]
    for cand in record_names:
        words = norm_words(cand)
        if len(words) >= 2 and words[-1] == last and words[0] == first and len(first) > 1:
            return True
    return False


def short(openalex_id: str) -> str:
    return openalex_id.rsplit("/", 1)[-1]


def subfield(topic: dict | None) -> str | None:
    return ((topic or {}).get("subfield") or {}).get("display_name")


def resolve_member(name: str, affil: str, ref_subfields: set[str]) -> dict:
    res = get("/authors", search=name, per_page=25)
    matched, near = [], []
    for a in res.get("results", []):
        if not name_matches(name, [a["display_name"], *(a.get("display_name_alternatives") or [])]):
            continue
        insts = {i["institution"]["display_name"] for i in a.get("affiliations") or []}
        insts |= {i["display_name"] for i in a.get("last_known_institutions") or []}
        hit = sorted(i for i in insts if institution_matches(affil, i))
        rec = {"id": short(a["id"]), "name": a["display_name"], "works": a.get("works_count")}
        if hit:
            rec["subfields"] = sorted({subfield(t) for t in a.get("topics") or []} - {None})
            matched.append({**rec, "institutions": hit})
        else:
            near.append({**rec, "institutions": sorted(insts)[:6]})
    if not matched:
        return {"status": "unresolved", "reason": "no OpenAlex record with this name at the PC-page affiliation",
                "nearest_records": near[:5]}
    if len(matched) > 1:
        # Same name at the same institution: either one person split into several
        # records or several people. Keep the records working in the manuscript's
        # subfields; that drops the namesake in the medical school.
        in_field = [m for m in matched if ref_subfields & set(m["subfields"])]
        if in_field:
            matched = in_field
    return {"status": "resolved", "author_ids": [m["id"] for m in matched], "records": matched}


def works_page(filt: str, select: str) -> tuple[list[dict], int]:
    res = get("/works", filter=filt, select=select, per_page=PER_PAGE, sort="publication_date:desc")
    return res.get("results", []), res.get("meta", {}).get("count", 0)


def bib_identifiers(bib: Path) -> tuple[list[str], list[str]]:
    text = bib.read_text(encoding="utf-8", errors="replace")
    dois = {d.strip().lower().removeprefix("https://doi.org/")
            for d in re.findall(r"\bdoi\s*=\s*[{\"]([^}\"]+)[}\"]", text, flags=re.I)}
    arxiv = set(re.findall(r"arXiv[:\s]*([0-9]{4}\.[0-9]{4,5})", text, flags=re.I))
    return sorted(dois), sorted(arxiv)


def refs_graph(dois: list[str], arxiv: list[str]) -> tuple[set[str], set[str], set[str]]:
    """Return (OpenAlex ids of the manuscript's refs, ids those refs cite, the refs' research subfields)."""
    ids, cited, subfields = set(), set(), set()
    keys = dois + [f"10.48550/arxiv.{a}" for a in arxiv]
    for i in range(0, len(keys), 50):
        batch, _ = works_page(f"doi:{'|'.join(keys[i:i + 50])}", "id,referenced_works,primary_topic")
        for w in batch:
            ids.add(short(w["id"]))
            cited.update(short(r) for r in w.get("referenced_works") or [])
            subfields.add(subfield(w.get("primary_topic")))
    return ids, cited, subfields - {None}


def venue_of(w: dict) -> str:
    src = (w.get("primary_location") or {}).get("source") or {}
    return src.get("display_name") or ""


def topic_words(topic: str) -> set[str]:
    stop = {"a", "an", "the", "of", "for", "and", "in", "on", "to", "with", "via", "using", "based"}
    return {w for w in norm_words(topic) if w not in stop and len(w) > 2}


def abstract_text(inverted: dict | None) -> str:
    if not inverted:
        return ""
    pos = {i: w for w, idx in inverted.items() for i in idx}
    return " ".join(pos[i] for i in sorted(pos))


def score_member(entry: dict, since: int, topic: set[str], ref_ids: set[str], refs_cite: set[str],
                 ref_subfields: set[str], keep: int) -> None:
    filt = f"author.id:{'|'.join(entry['author_ids'])},from_publication_date:{since}-01-01"
    works, total = works_page(filt, "id,doi,title,publication_year,primary_location,referenced_works,"
                                    "cited_by_count,abstract_inverted_index,primary_topic")
    need = max(2, math.ceil(0.6 * len(topic)))
    already, scored = [], []
    for w in works:
        wid = short(w["id"])
        field = subfield(w.get("primary_topic"))
        item = {"openalex": wid, "doi": (w.get("doi") or "").removeprefix("https://doi.org/"),
                "title": w.get("title"), "year": w.get("publication_year"), "venue": venue_of(w),
                "cited_by_count": w.get("cited_by_count")}
        if wid in ref_ids:
            already.append(item)
            continue
        if field and ref_subfields and field not in ref_subfields:
            continue
        cites = len({short(r) for r in w.get("referenced_works") or []} & ref_ids)
        text = set(norm_words(f"{w.get('title') or ''} {abstract_text(w.get('abstract_inverted_index'))}"))
        signals = {"cited_by_refs": wid in refs_cite, "cites_refs": cites, "topic_hit": len(topic & text) >= need}
        score = 3 * signals["cited_by_refs"] + min(cites, 5) + 2 * signals["topic_hit"]
        if score >= 2:
            scored.append({**item, **signals, "subfield": field, "score": score})
    # A preprint and its published version are one paper; keep the published one.
    scored.sort(key=lambda x: (-x["score"], "arxiv" in x["venue"].lower(), -(x["cited_by_count"] or 0)))
    seen: set[str] = set()
    scored = [x for x in scored if not ("".join(norm_words(x["title"] or "")) in seen
                                        or seen.add("".join(norm_words(x["title"] or ""))))]
    entry.update({"works_since": total, "works_scanned": len(works), "truncated": total > len(works),
                  "already_cited": already, "candidates": scored[:keep]})


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("pc", help="TSV: Name<TAB>Affiliation[<TAB>OpenAlexIds], copied from the saved PC page")
    ap.add_argument("--refs", required=True, help="the manuscript's .bib")
    ap.add_argument("--topic", required=True, help="OpenAlex search string for the paper's topic")
    ap.add_argument("--since", type=int, default=2019, help="earliest publication year (default 2019)")
    ap.add_argument("--per-member", type=int, default=3, help="candidates kept per member (default 3)")
    ap.add_argument("--out", required=True, help="output JSON path")
    args = ap.parse_args()

    pc_path, bib = Path(args.pc), Path(args.refs)
    for p in (pc_path, bib):
        if not p.is_file():
            print(f"[ERROR] {p} not found", file=sys.stderr)
            return 2
    members = []
    for ln, line in enumerate(pc_path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        parts = [x.strip() for x in line.split("\t")]
        if len(parts) < 2 or not parts[0] or not parts[1]:
            print(f"[ERROR] {pc_path}:{ln}: expected 'Name<TAB>Affiliation[<TAB>OpenAlexIds]'", file=sys.stderr)
            return 2
        ids = [short(x) for x in parts[2].split("|") if x.strip()] if len(parts) > 2 and parts[2] else []
        members.append((parts[0], parts[1], ids))

    dois, arxiv = bib_identifiers(bib)
    ref_ids, refs_cite, ref_subfields = refs_graph(dois, arxiv)
    print(f"refs.bib: {len(dois)} DOIs + {len(arxiv)} arXiv ids -> {len(ref_ids)} OpenAlex records; "
          f"subfields: {', '.join(sorted(ref_subfields))}", file=sys.stderr)

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    report = {"since": args.since, "topic": args.topic, "refs_resolved": len(ref_ids),
              "ref_subfields": sorted(ref_subfields), "members": []}
    if out.is_file():
        prev = json.loads(out.read_text(encoding="utf-8"))
        if (prev.get("since"), prev.get("topic")) == (args.since, args.topic):
            # Unresolved members are retried: a third TSV column may now resolve them.
            report["members"] = [m for m in prev["members"] if m["status"] == "resolved"]
    done = {(m["name"], m["affiliation"]) for m in report["members"]}
    topic = topic_words(args.topic)
    for name, affil, ids in members:
        if (name, affil) in done:
            continue
        if ids:
            entry = {"name": name, "affiliation": affil, "status": "resolved", "author_ids": ids,
                     "records": "given in the PC file"}
        else:
            entry = {"name": name, "affiliation": affil, **resolve_member(name, affil, ref_subfields)}
        if entry["status"] == "resolved":
            score_member(entry, args.since, topic, ref_ids, refs_cite, ref_subfields, args.per_member)
        report["members"].append(entry)
        out.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        note = (f"{len(entry['candidates'])} candidates, {len(entry['already_cited'])} already cited"
                + (f", newest {entry['works_scanned']} of {entry['works_since']} works scanned" if entry["truncated"] else "")
                if entry["status"] == "resolved" else "unresolved")
        print(f"{name} ({affil}): {note}", file=sys.stderr)

    out.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    resolved = sum(m["status"] == "resolved" for m in report["members"])
    total = sum(len(m.get("candidates", [])) for m in report["members"])
    print(f"wrote {out}: {resolved}/{len(members)} members resolved, {total} candidates", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())

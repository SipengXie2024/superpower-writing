# Citing the target venue's program committee

Program-committee members review the submissions closest to their own work. When the manuscript discusses a problem a PC member has published on, that member is a likely reviewer, and the first thing they check is whether their work is cited and described correctly. Missing it reads as not knowing the field; misdescribing it is worse. This file covers how to find those papers and when one earns a place in the manuscript.

## Admission rule

A PC paper enters the manuscript only when all three hold:

1. **It has a place.** A sentence already needs a citation that this paper can carry, or the related-work section has a gap that this paper fills. Membership on the PC is never the reason to cite.
2. **It passes the full-text check.** A verifier who did not propose it fetches the paper, finds the passage, and returns a verbatim quote with its page and a `supported` verdict (`../../citations/references/fulltext-relevance.md`).
3. **It is described the way its authors would describe it.** The citing sentence uses the paper's own terms for its contribution and does not narrow it to make ours look newer. A comparison that the paper's author would dispute gets rewritten or dropped.

A PC paper never joins a grouped citation list (four or more keys on one clause) just to be present; the citation-auditor counts that as over-citation, and a reviewer reads it the same way. Under a page budget, a PC paper competes with every other candidate by the load it carries (`SKILL.md`, Screening references).

## Steps

### 1. Get the committee from the venue's own page

Read `venue` in `.writing/metadata.yaml` (`name`, `year`, `pc_url`). When `pc_url` is empty, find the venue's committee page (call for papers or "Organization") and write the URL back. Save the page under `.writing/sources/pc-<venue><year>.html` (or the extracted text). A member who is not on the saved page does not exist; never add a name from memory.

Some venue sites block downloads from servers: USENIX returns 403 to a cloud machine. The same request from a home network usually passes, and a real desktop browser passes the Cloudflare checks that stop scripts. When the environment has such a machine (the user's own workstation reachable over ssh), fetch the page there and copy it back; otherwise ask the user to save the page.

The committee of the submission year is often published late. If it is not out yet, use the previous year's committee and say so in the shortlist; most members serve again.

### 2. Write the TSV

One member per line, `Name<TAB>Affiliation`, exactly as printed on the page. A third column takes one or more OpenAlex author ids (`A123|A456`) once a member has been resolved by hand.

### 3. Run the shortlist

```bash
python3 scripts/pc_works.py .writing/sources/pc.tsv --refs .writing/refs.bib \
  --topic "<the paper's topic in the field's own words>" --since 2019 \
  --out .writing/sources/pc-shortlist.json
```

The script resolves each member to an OpenAlex author record, requiring the same first and last name and an institution that matches the PC-page affiliation. It drops same-name records outside the research subfields of the manuscript's own references. It then scores the member's recent papers:

| Signal | Meaning |
|---|---|
| `cited_by_refs` | a paper the manuscript already cites builds on this work; the strongest sign it belongs in the conversation |
| `cites_refs` | how many of the manuscript's references this work cites |
| `topic_hit` | most of the `--topic` words appear in its title or abstract |

Papers already in `refs.bib` are listed per member under `already_cited`. A preprint and its published version count once, published preferred.

Cost: one author search and one works list per member. A full PC (50 to 100 people) exhausts OpenAlex's keyless daily budget, which is shared by every user behind the same IP address; set `OPENALEX_API_KEY` (free, from https://openalex.org/settings/api, tied to the user's email) before a full run. The output file is rewritten after every member, and a rerun with the same `--topic` and `--since` skips members already done, so a run stopped by the quota resumes.

### 4. Resolve the unresolved by hand

Members come back `unresolved` when no same-name record carries the PC affiliation. Common causes: the member moved recently and OpenAlex still lists only the old school, the PC page uses a lab or company name OpenAlex does not carry (`MPI-SWS`, a startup), or the person is buried among same-name records. On the SOSP 2024 committee 55 of 58 members resolved automatically. The entry lists the nearest records with their institutions; pick the one whose institutions and papers fit, put its id in the TSV's third column, and rerun. If two records fit equally, leave the member out.

### 5. Read and send to verification

The shortlist sets the reading order. Read titles and venues first and drop what is plainly off-topic. For the rest, read the abstract, then send survivors to the Job C verifiers with the sentence or related-work gap each would fill. Record the outcome per candidate in `.writing/sources/pc-shortlist.md`: admitted (with citekey and the sentence), rejected (with the one-line reason), or reserve.

## Pitfalls

- **Homonyms.** Common names (`Kang Chen`, `Rong Chen`) have several records at the same institution, some in medicine or physics. The subfield filter removes most; a candidate whose venue is outside computing is still a homonym and is dropped.
- **Records that merge several people.** A member with an implausible paper count (`truncated` with hundreds of papers since 2019) is likely a merged record; check their candidates by hand against the member's homepage.
- **Overlap is a risk before it is a citation.** A PC paper that solves a close problem is the most likely reviewer's own competing work. Run the novelty-risk scan, sharpen the manuscript's claim scope, and state the difference in terms its author would accept.
- **Self-serving framing shows.** Praise words around a PC citation ("seminal", "pioneering") that the paper's other citations do not get are noticed. Describe the work in the same plain terms as the paper's other citations.

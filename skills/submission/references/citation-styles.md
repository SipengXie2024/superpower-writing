# Citation Styles Guide

## Style Selection

Different disciplines and venues prefer different citation styles. The table below summarizes the five most common styles and their in-text formats.

| Style | Primary Disciplines | In-Text Format |
|-------|-------------------|----------------|
| AMA | Medicine, health sciences | Superscript numbers |
| Vancouver | Biomedical sciences | Numbers in brackets [1] |
| APA | Psychology, social sciences | Author-date (Smith, 2023) |
| Chicago | Humanities, history | Notes-bibliography or author-date |
| IEEE | Engineering, computer science | Numbers in brackets [1] |

When in doubt, check the venue's author guidelines. Systems and CS papers overwhelmingly use IEEE style; the sections below give IEEE full treatment and summarize the others.

## AMA

Used primarily in medical research. Based on the *AMA Manual of Style* (11th ed., 2020). Numbered citations appear as superscripts, placed outside periods and commas, inside semicolons and colons. References are listed numerically in order of appearance.

In-text example:

```
Several studies have demonstrated this effect.¹
The results were inconclusive,² although Smith et al³ reported otherwise.
Multiple studies¹,³,⁵⁻⁷ have confirmed this.
```

Journal article example:

```
1. Smith JD, Johnson AB, Williams CD. Effectiveness of cognitive behavioral
   therapy for anxiety disorders. JAMA Psychiatry. 2023;80(5):456-464.
   doi:10.1001/jamapsychiatry.2023.0123
```

Books:

```
2. Author AA. Book Title. Edition. Publisher; Year.
```

Online resources:

```
3. Organization Name. Page title. Website name. Published date. Accessed date. URL
```

List first three authors then "et al" for more than six authors.

## Vancouver

Developed by the International Committee of Medical Journal Editors (ICMJE). Also called "author-number style." Numbered citations in square brackets placed before periods and commas; references listed numerically in order of appearance.

In-text example:

```
Several studies have shown this effect [1].
The results were inconclusive [2], although Smith et al [3] reported otherwise.
Multiple studies [1,3,5-7] have confirmed this.
```

Journal article example:

```
1. Smith JD, Johnson AB, Williams CD. Effectiveness of cognitive behavioral
   therapy for anxiety disorders. JAMA Psychiatry. 2023;80(5):456-464.
```

Books:

```
2. Author AA, Author BB. Book title. Edition. Place of publication: Publisher; Year.
```

Electronic sources:

```
3. Author AA. Title of page [Internet]. Place: Publisher; Date [cited Date]. Available from: URL
```

List first six authors then "et al." for more than six. Use PubMed/Index Medicus journal abbreviations.

## APA

Widely used in psychology, education, and social sciences. Based on the *Publication Manual of the APA* (7th ed., 2020). Author-date in-text format; references listed alphabetically by first author surname.

In-text examples:

```
One study found significant effects (Smith, 2023).
Smith (2023) found significant effects.
Multiple studies (Jones, 2020; Smith, 2023) support this conclusion.
Two authors: (Smith & Jones, 2023) or Smith and Jones (2023)
Three or more: (Smith et al., 2023)
Direct quotation: (Smith, 2023, p. 45)
```

Journal article example:

```
Smith, J. D., Johnson, A. B., & Williams, C. D. (2023). Effectiveness of
cognitive behavioral therapy for anxiety disorders. JAMA Psychiatry, 80(5),
456-464. https://doi.org/10.1001/jamapsychiatry.2023.0123
```

Books:

```
Author, A. A. (Year). Book title: Subtitle (Edition). Publisher. https://doi.org/xx
```

Book chapters:

```
Chapter Author, A. A. (Year). Chapter title. In E. Editor (Ed.), Book title (pp. range). Publisher.
```

Sentence case for article and book titles (capitalize only first word and proper nouns). Title case for journal names. List up to 20 authors with "&" before the last; for 21 or more, list first 19, ellipsis, then the final author.

## Chicago

Based on *The Chicago Manual of Style* (17th ed.). Two systems: Notes-Bibliography (common in humanities) and Author-Date (common in sciences). Full names in bibliography; uses "and" not "&".

Notes-Bibliography in-text: superscript numbers for footnotes/endnotes. Note format:

```
1. John D. Smith, Alice B. Johnson, and Carol D. Williams, "Title,"
   JAMA Psychiatry 80, no. 5 (2023): 456-64.
```

Author-Date in-text: `(Smith, Johnson, and Williams 2023)`. Reference list:

```
Smith, John D., Alice B. Johnson, and Carol D. Williams. 2023.
"Effectiveness of Cognitive Behavioral Therapy for Anxiety Disorders."
JAMA Psychiatry 80 (5): 456-64.
```

The key difference from APA is punctuation and the placement of the year after the author block rather than in parentheses.

## IEEE

IEEE style is the default citation format for engineering and computer science, including systems papers. Published by the Institute of Electrical and Electronics Engineers, it uses numbered citations in square brackets with references listed numerically in order of first appearance.

### In-Text Format

Numbers in square brackets, typeset on the line (not superscript).

```
Several studies have demonstrated this effect [1].

The algorithm was described by Smith [2] and later improved [3], [4].

Multiple implementations [1]-[4] have been proposed.
```

Separate non-consecutive citations with commas: `[1], [3], [5]`. Express consecutive ranges with an en-dash: `[1]-[5]`.

### Reference List Format

Each entry begins with the reference number in square brackets, followed by the bibliographic data.

**Author names.** Use initials for first and middle names, placed before the surname. Separate authors with commas and place "and" before the last author.

```
A. B. Smith, C. D. Jones, and E. F. Lee, ...
```

**Title capitalization.** Article and paper titles are enclosed in double quotation marks and use sentence case (capitalize only the first word and proper nouns). Journal and book titles are italicized and use title case.

**Journal abbreviations.** Abbreviate journal names following IEEE or standard practice (e.g., *IEEE Trans. Comput.*, *ACM Trans. Comput. Syst.*).

**Volume, issue, pages.** Use `vol.`, `no.`, and `pp.` abbreviations.

**Date.** Include the month (abbreviated: Jan., Feb., Mar., Apr., May, June, July, Aug., Sept., Oct., Nov., Dec.) and year at the end of the entry.

### Examples by Publication Type

**Journal article:**

```
[1] J. D. Smith, A. B. Johnson, and C. D. Williams, "A fast consensus
    protocol for wide-area distributed systems," IEEE Trans. Comput.,
    vol. 72, no. 3, pp. 712-725, Mar. 2023.
```

**Conference proceedings:**

```
[2] A. Kumar and B. Zhao, "Towards zero-copy serialization for
    microservices," in Proc. ACM Symp. Operating Systems Principles
    (SOSP), Huntsville, ON, Canada, 2023, pp. 145-160.
```

**Book:**

```
[3] H. T. Kung and T. H. Lin, Introduction to Parallel Algorithms,
    2nd ed. Boston, MA, USA: MIT Press, 2022.
```

**Technical report:**

```
[4] R. Nikhil and A. P. Singh, "Formal verification of distributed
    consensus protocols," Dept. Comput. Sci., MIT, Cambridge, MA, USA,
    Tech. Rep. MIT-CSAIL-TR-2023-014, 2023.
```

**Web/online source:**

```
[5] Cloud Native Computing Foundation. "gRPC: A high performance,
    open-source universal RPC framework." [Online]. Available:
    https://grpc.io/ [Accessed: Jan. 15, 2024].
```

**Standard:**

```
[6] IEEE Standard for Local and Metropolitan Area Networks: Overview
    and Architecture, IEEE Std 802-2014, Rev. IEEE Std 802-2001,
    Jun. 2014.
```

**Patent:**

```
[7] A. B. Inventor, "Method and apparatus for low-latency distributed
    transaction processing," U.S. Patent 10 123 456, Nov. 5, 2019.
```

**arXiv preprint:**

```
[8] C. Li, D. Peng, and F. Wang, "Scalable graph neural networks
    for billion-edge graphs," arXiv:2306.12345, Jun. 2023.
```

### IEEE Formatting Rules Summary

| Element | Rule |
|---------|------|
| Author names | Initials before surname; comma-separated; "and" before last |
| Article title | Double quotes, sentence case |
| Journal title | Italics, title case, abbreviated |
| Volume / issue | `vol. X, no. X` |
| Pages | `pp. XX-XX` |
| Date | `Month Year` (abbreviated month) |
| DOI | Optional, appended as `doi:10.xxxx/xxxxx` |

## Best Practices

### When to Cite

- Direct quotations (include page numbers).
- Paraphrased ideas, arguments, or frameworks from other sources.
- Statistics, data, figures, or tables from other sources.
- Theories, models, or algorithms developed by others.
- Any information that is not common knowledge in the field.

### Citation Density by Manuscript Section

| Section | Citation Density |
|---------|-----------------|
| Introduction | High -- establish context and identify the gap |
| Methods | Moderate -- reference established protocols and tools |
| Results | Low -- focus on your own findings |
| Discussion | High -- compare to prior work and position contributions |

### Source Quality

- Prefer peer-reviewed publications over preprints when both exist.
- Cite original sources rather than secondary citations (avoid citation chaining).
- Use recent sources (within 5-10 years for active fields; 2-3 years for ML conferences).
- Ensure sources are reputable and directly relevant.

### Common Mistakes

- Inconsistent formatting across the reference list.
- Missing required elements (DOI, page numbers, venue name).
- Citing sources not actually read (citation chaining).
- Over-reliance on review articles instead of primary sources.
- In-text citations without matching references, or vice versa.
- Incorrect author names, initials, or publication year.
- Truncated or inaccurate titles.
- Wrong journal abbreviations or mixing abbreviated and full names.
- Including references that are not cited in the text.
- Forgetting to update citation numbers after rearranging sections (numbered styles).

### Verifying Citations

Before submission, work through this verification sequence:

1. Every in-text citation has a corresponding reference-list entry.
2. Every reference-list entry is cited in the text.
3. Formatting is consistent throughout the entire list.
4. Author names and initials are correct.
5. Titles are accurate and complete.
6. Journal names use the required abbreviations.
7. Volume, issue, and page numbers are correct.
8. DOIs are included when required and formatted per style.
9. URLs are functional (for web-only sources).
10. Citations appear in correct order (numerical styles: order of first appearance).

## DOI

A Digital Object Identifier (DOI) is a unique alphanumeric string that permanently identifies digital content. DOIs are more stable than URLs because they are resolution-independent -- even if the publisher reorganizes their site, the DOI still resolves.

### Format

IEEE and AMA: `doi:10.xxxx/xxxxx`
APA and Chicago: `https://doi.org/10.xxxx/xxxxx`
Vancouver: included at the journal's discretion

### Resolution

Any DOI can be resolved by prepending `https://doi.org/`. For example, `doi:10.1001/jamapsychiatry.2023.0123` resolves to `https://doi.org/10.1001/jamapsychiatry.2023.0123`. Look up unknown DOIs at <https://www.crossref.org/>.

### When to Include

Most journals require DOIs for publications from roughly 2000 onward. When a DOI exists, prefer it over a bare URL. Systems conferences vary: some require DOIs for journal articles but not for conference papers; arXiv preprints use the arXiv ID instead.

## Quick Reference

Comparative journal-article format across the five styles:

| Style | Format |
|-------|--------|
| **AMA** | Author AA, Author BB. Title. *Journal*. Year;Vol(Iss):pp. doi:xx |
| **Vancouver** | Author AA, Author BB. Title. Journal. Year;Vol(Iss):pp. |
| **APA** | Author, A. A., & Author, B. B. (Year). Title. *Journal*, Vol(Iss), pp. doi:xx |
| **Chicago** | Author, A. A., and B. B. Author. Year. "Title." *Journal* Vol (Iss): pp. |
| **IEEE** | A. A. Author and B. B. Author, "Title," *Journal*, vol. X, no. X, pp. XX-XX, Mon. Year. |

## Common Abbreviations

### Journal Abbreviations

Follow the venue's specified system (Index Medicus, ISO, or IEEE standard). Examples:

| Full Name | Abbreviation |
|-----------|-------------|
| *The Journal of Biological Chemistry* | *J. Biol. Chem.* |
| *Proceedings of the National Academy of Sciences* | *Proc. Natl. Acad. Sci. USA* |
| *Nature Medicine* | *Nat. Med.* |
| *IEEE Transactions on Computers* | *IEEE Trans. Comput.* |
| *ACM Transactions on Computer Systems* | *ACM Trans. Comput. Syst.* |

### Month Abbreviations

Jan., Feb., Mar., Apr., May, June, July, Aug., Sept., Oct., Nov., Dec.

### Edition Abbreviations

1st ed., 2nd ed., 3rd ed., etc.

## Special Publication Types

### Preprints (arXiv, bioRxiv, etc.)

Systems papers frequently cite arXiv preprints because the field moves quickly and many significant results appear there before (or instead of) formal publication. In ML and systems communities, arXiv preprints are first-class citable objects; reviewers expect to see them referenced for concurrent work and rapidly evolving topics.

IEEE format:

```
[1] A. B. Author and C. D. Author, "Title of preprint," arXiv:2306.12345,
    Jun. 2023.
```

APA format:

```
Author, A. B. (2023). Title of preprint. arXiv. https://doi.org/10.48550/arXiv.2306.12345
```

Vancouver format:

```
1. Author AB, Author CD. Title of preprint. arXiv. Preprint posted online June 15, 2023. Available from: https://arxiv.org/abs/2306.12345
```

When citing arXiv preprints, include the arXiv identifier. If the preprint has since been published in a peer-reviewed venue, cite the published version instead -- this gives readers stable page numbers and a DOI. If both versions are cited (e.g., to reference specific arXiv version numbering), include both entries and cross-reference them.

### Theses and Dissertations

IEEE format:

```
[2] A. B. Author, "Title of thesis," M.S. thesis or Ph.D. dissertation,
    Dept. Comput. Sci., Univ. Name, City, Country, Year.
```

APA format:

```
Author, A. B. (2023). Title of thesis [Doctoral dissertation, University Name]. Repository. URL
```

### Conference Proceedings

IEEE format (the most common for CS):

```
[3] A. B. Author, "Title," in Proc. Conf. Name (Abbreviation), City, Country, Year, pp. XX-XX.
```

APA format:

```
Author, A. B., & Author, C. D. (2023). Title. In Proceedings of Conference Name (pp. XX-XX). Publisher. https://doi.org/xx
```

### Software

Systems papers often cite frameworks, libraries, and tools. Always include the version number and a persistent URL or DOI when available.

IEEE format:

```
[4] A. B. Author, "Software Name," version X.Y. [Online]. Available: URL
```

APA format:

```
Author, A. B. (2023). Software Name (Version X.Y) [Computer software]. Publisher. URL
```

When no individual author is listed, use the project or organization name as author:

```
[5] LLVM Project, "LLVM: A compiler infrastructure," version 17.0. [Online].
    Available: https://llvm.org/
```

### Datasets

Benchmark datasets are central to systems evaluation. Include the version, repository, and a DOI or persistent URL.

IEEE format:

```
[6] A. B. Author, "Dataset Name," version X, Year. [Online]. Available: URL
```

APA format:

```
Author, A. B. (2023). Dataset Name (Version X) [Data set]. Repository. https://doi.org/xx
```

When the dataset is maintained by an institution or project rather than individual authors, use the organization name:

```
[7] Stanford Network Analysis Project, "SNAP dataset collection," 2023.
    [Online]. Available: https://snap.stanford.edu/data/
```

## Transitioning

When converting a manuscript's citations from one style to another, for example after a desk rejection or when retargeting to a different venue:

1. Use reference management software (Zotero, Mendeley, EndNote) for automatic conversion. Select the target venue's citation style from the software's style library and regenerate.
2. Check the elements that vary most between styles:
   - In-text format (numbered vs. author-date).
   - Author name format (initials before surname vs. surname first with initials; full names vs. initials).
   - Title capitalization (sentence case vs. title case).
   - Journal name treatment (abbreviated vs. full).
   - Punctuation conventions (periods, commas, semicolons between authors).
   - Use of italics and bold for journal and book titles.
   - Element ordering within each reference.
3. Manually verify every entry after automatic conversion -- software often misplaces DOIs, drops issue numbers, or incorrectly capitalizes titles.
4. Check the target venue's guidelines for any style-specific modifications beyond the base style (many venues customize IEEE or Vancouver).
5. Pay special attention to non-standard sources: preprints, software, datasets, and technical reports are the entries most likely to break during conversion.

## Venue-Specific

Most venues specify a citation style in their author guidelines or LaTeX template. High-level notes by venue family:

- **IEEE journals and conferences**: IEEE style (see full section above). The `IEEEtran` LaTeX class handles formatting automatically.
- **ACM conferences (SOSP, OSDI, SIGCOMM, etc.)**: ACM Reference Format, structurally similar to IEEE but with a distinct reference-list layout and the `acmart` LaTeX class. Conference papers include the full venue name and acronym in the entry.
- **ML conferences (NeurIPS, ICML, ICLR)**: Numbered citations `[1]` or author-year, depending on the year's template. arXiv preprints are widely cited and accepted. Check the specific year's style file.
- **NLP venues (ACL, EMNLP)**: ACL style, author-year format. The `acl` LaTeX class provides the correct bibliography style.
- **Vision venues (CVPR, ICCV, ECCV)**: IEEE-like numbered format using `cvpr` style files.
- **Nature/Science**: Numbered superscripts, abbreviated journal names, no article titles in some Nature sub-journals. Highly space-constrained.
- **Medical journals (JAMA, NEJM, Lancet, BMJ)**: AMA or Vancouver. Check the specific journal, as each has minor variations.

For detailed per-venue formatting rules including LaTeX templates and complete citation examples, see `venue-styles.md`.

## Venue Expectations

Evaluators assess citations along several dimensions.

**Recency.** High-impact journals expect 50% or more of citations from the last 5-10 years. ML conferences expect heavy citation of work from the last 2-3 years, with arXiv preprints fully acceptable.

**Source quality.** Peer-reviewed publications are preferred over preprints when both exist, but in fast-moving fields (ML, systems) citing preprints is normal and expected.

**Self-citation ratio.** Keep self-citations below 20% across all venue types.

**Primary sources.** Cite the original paper that introduced a concept or system, not a survey that mentions it. Citation chaining (citing a source you have not read, found through another paper's reference list) is a common audit finding.

**Completeness.** Every in-text citation must have a matching reference-list entry, and every reference-list entry must be cited in the text. Missing or orphaned references are an instant formatting rejection at many venues.

**Coverage.** Reviewers in systems and ML venues expect to see the relevant prior work cited. Omitting well-known baselines or concurrent work signals unfamiliarity with the field.

### Citation Density by Venue Type

| Venue Type | Typical References | Notes |
|-----------|-------------------|-------|
| Nature/Science research | 30-50 | Selective, high-impact citations only |
| Field-specific journals | 30-60 | Comprehensive field coverage expected |
| Systems conferences (OSDI, SOSP) | 25-45 | Space-limited; prioritize directly related work |
| ML conferences (NeurIPS, ICML, 8-page) | 20-40 | Space-limited, very recent work valued |
| Workshop papers | 15-25 | Concise but representative |
| Review articles | 100-300+ | Exhaustive coverage is the point |

## Pre-Submission Checklist

### Content

- [ ] 50% or more of citations from the last 5-10 years (2-3 years for ML conferences)
- [ ] Self-citations below 20%
- [ ] Primary sources cited, not citation chains
- [ ] All factual claims supported by appropriate citations
- [ ] arXiv preprints included for concurrent or unpublished work (with arXiv IDs)
- [ ] Key baselines and prior systems in the field are represented
- [ ] No well-known prior work in the paper's problem space is missing from citations
- [ ] Related work section positions the paper clearly against existing approaches

### Format

- [ ] Citation style matches the venue template exactly
- [ ] Every in-text citation has a corresponding reference-list entry
- [ ] Every reference-list entry is cited in the text
- [ ] DOIs included where required (journals) or arXiv IDs (ML conferences)
- [ ] Journal abbreviations match the venue's preferred system
- [ ] Author names and initials are correct
- [ ] Titles are accurate and not truncated
- [ ] Volume, issue, and page numbers verified
- [ ] URLs are functional (for web-only sources)
- [ ] Citation numbering is sequential in order of first appearance (numbered styles)
- [ ] Software and dataset citations include version numbers and persistent URLs

### ML Conference Additions

- [ ] arXiv preprints properly formatted with identifiers
- [ ] Self-citations anonymized if under double-blind review
- [ ] References fit within page limits
- [ ] Conference proceedings cited with full venue name and acronym
- [ ] Concurrent work (posted to arXiv within the last 6 months) is cited where relevant

# Metadata Extraction Guide

Comprehensive guide to extracting accurate citation metadata from DOIs, arXiv IDs, and URLs using various APIs and services.

## Overview

Accurate metadata is essential for proper citations. This guide covers:
- Identifying paper identifiers (DOI, arXiv ID)
- Querying metadata APIs (CrossRef, arXiv, DataCite)
- Required BibTeX fields by entry type
- Handling edge cases and special situations
- Validating extracted metadata

## Paper Identifiers

### DOI (Digital Object Identifier)

**Format**: `10.XXXX/suffix`

**Examples**:
```
10.1145/3065386               # ACM (CACM) article
10.1109/CVPR.2016.90          # IEEE (CVPR) conference paper
10.1145/1327452.1327492       # ACM (CACM) article
10.1145/279227.279229         # ACM (TOCS) article
```

**Properties**:
- Permanent identifier
- Most reliable for metadata
- Resolves to current location
- Publisher-assigned

**Where to find**:
- First page of article
- Article webpage
- CrossRef, Google Scholar, DBLP
- Usually prominent on publisher site

### arXiv ID

**Format**: YYMM.NNNNN or archive/YYMMNNN

**Examples**:
```
2103.14030        # New format (since 2007)
2401.12345        # 2024 submission
arXiv:hep-th/9901001  # Old format
```

**Properties**:
- Preprints (not peer-reviewed)
- CS, math, physics, etc.
- Version tracking (v1, v2, etc.)
- Free, open access

**Where to find**:
- arXiv.org
- Often cited before publication
- Paper PDF header

### Other Identifiers

**ISBN** (Books):
```
978-0-12-345678-9
0-123-45678-9
```

**arXiv category**:
```
cs.LG    # Computer Science - Machine Learning
cs.DC    # Computer Science - Distributed Computing
math.ST  # Mathematics - Statistics
```

## Metadata APIs

### CrossRef API

**Primary source for DOIs** - Most comprehensive metadata for journal articles.

**Base URL**: `https://api.crossref.org/works/`

**No API key required**, but polite pool recommended:
- Add email to User-Agent
- Gets better service
- No rate limits

#### Basic DOI Lookup

**Request**:
```
GET https://api.crossref.org/works/10.1145/3065386
```

**Response** (simplified):
```json
{
  "message": {
    "DOI": "10.1145/3065386",
    "title": ["Article title here"],
    "author": [
      {"given": "John", "family": "Smith"},
      {"given": "Jane", "family": "Doe"}
    ],
    "container-title": ["Communications of the ACM"],
    "volume": "60",
    "issue": "6",
    "page": "84-90",
    "published-print": {"date-parts": [[2017, 5, 1]]},
    "publisher": "Association for Computing Machinery",
    "type": "journal-article",
    "ISSN": ["0001-0782"]
  }
}
```

#### Fields Available

**Always present**:
- `DOI`: Digital Object Identifier
- `title`: Article title (array)
- `type`: Content type (journal-article, book-chapter, etc.)

**Usually present**:
- `author`: Array of author objects
- `container-title`: Journal/book title
- `published-print` or `published-online`: Publication date
- `volume`, `issue`, `page`: Publication details
- `publisher`: Publisher name

**Sometimes present**:
- `abstract`: Article abstract
- `subject`: Subject categories
- `ISSN`: Journal ISSN
- `ISBN`: Book ISBN
- `reference`: Reference list
- `is-referenced-by-count`: Citation count

#### Content Types

CrossRef `type` field values:
- `journal-article`: Journal articles
- `book-chapter`: Book chapters
- `book`: Books
- `proceedings-article`: Conference papers
- `posted-content`: Preprints
- `dataset`: Research datasets
- `report`: Technical reports
- `dissertation`: Theses/dissertations

### arXiv API

**Preprints in CS, math, physics** - Free, open access.

**Base URL**: `http://export.arxiv.org/api/query`

**No API key required**

#### arXiv ID to Metadata

**Request**:
```
GET http://export.arxiv.org/api/query?id_list=2103.14030
```

**Response**: Atom XML

```xml
<entry>
  <id>http://arxiv.org/abs/1706.03762v5</id>
  <title>Attention Is All You Need</title>
  <author><name>Ashish Vaswani</name></author>
  <author><name>Noam Shazeer</name></author>
  <published>2017-06-12T17:57:34Z</published>
  <updated>2017-12-06T03:30:39Z</updated>
  <summary>Abstract text here...</summary>
  <category term="cs.CL" scheme="http://arxiv.org/schemas/atom"/>
  <category term="cs.LG" scheme="http://arxiv.org/schemas/atom"/>
</entry>
```

#### Key Fields

- `id`: arXiv URL
- `title`: Preprint title
- `author`: Author list
- `published`: First version date
- `updated`: Latest version date
- `summary`: Abstract
- `arxiv:doi`: DOI if published
- `arxiv:journal_ref`: Journal reference if published
- `category`: arXiv categories

#### Version Tracking

arXiv tracks versions:
- `v1`: Initial submission
- `v2`, `v3`, etc.: Revisions

**Always check** if preprint has been published in journal (use DOI if available).

### DataCite API

**Research datasets, software, other outputs** - Assigns DOIs to non-traditional scholarly works.

**Base URL**: `https://api.datacite.org/dois/`

**Similar to CrossRef** but for datasets, software, code, etc.

**Request**:
```
GET https://api.datacite.org/dois/10.5281/zenodo.1234567
```

**Response**: JSON with metadata for dataset/software

## Required BibTeX Fields

### @article (Journal Articles)

**Required**:
- `author`: Author names
- `title`: Article title
- `journal`: Journal name
- `year`: Publication year

**Optional but recommended**:
- `volume`: Volume number
- `number`: Issue number
- `pages`: Page range (e.g., 123--145)
- `doi`: Digital Object Identifier
- `url`: URL if no DOI
- `month`: Publication month

**Example**:
```bibtex
@article{Smith2024,
  author  = {Smith, John and Doe, Jane},
  title   = {Novel Approach to Query Optimization},
  journal = {Communications of the ACM},
  year    = {2024},
  volume  = {67},
  number  = {8},
  pages   = {123--145},
  doi     = {10.1145/journal.2024.123456}
}
```

### @book (Books)

**Required**:
- `author` or `editor`: Author(s) or editor(s)
- `title`: Book title
- `publisher`: Publisher name
- `year`: Publication year

**Optional but recommended**:
- `edition`: Edition number (if not first)
- `address`: Publisher location
- `isbn`: ISBN
- `url`: URL
- `series`: Series name

**Example**:
```bibtex
@book{Cormen2009,
  author    = {Cormen, Thomas H. and Leiserson, Charles E. and Rivest, Ronald L. and Stein, Clifford},
  title     = {Introduction to Algorithms},
  publisher = {MIT Press},
  year      = {2009},
  edition   = {3},
  isbn      = {978-0-262-03384-8}
}
```

### @inproceedings (Conference Papers)

**Required**:
- `author`: Author names
- `title`: Paper title
- `booktitle`: Conference/proceedings name
- `year`: Year

**Optional but recommended**:
- `pages`: Page range
- `organization`: Organizing body
- `publisher`: Publisher
- `address`: Conference location
- `month`: Conference month
- `doi`: DOI if available

**Example**:
```bibtex
@inproceedings{Vaswani2017,
  author    = {Vaswani, Ashish and Shazeer, Noam and others},
  title     = {Attention is All You Need},
  booktitle = {Advances in Neural Information Processing Systems},
  year      = {2017},
  pages     = {5998--6008},
  volume    = {30}
}
```

### @incollection (Book Chapters)

**Required**:
- `author`: Chapter author(s)
- `title`: Chapter title
- `booktitle`: Book title
- `publisher`: Publisher name
- `year`: Publication year

**Optional but recommended**:
- `editor`: Book editor(s)
- `pages`: Chapter page range
- `chapter`: Chapter number
- `edition`: Edition
- `address`: Publisher location

**Example**:
```bibtex
@incollection{Goodfellow2016,
  author    = {Goodfellow, Ian and Bengio, Yoshua and Courville, Aaron},
  title     = {Convolutional Networks},
  booktitle = {Deep Learning},
  editor    = {Goodfellow, Ian and Bengio, Yoshua},
  publisher = {MIT Press},
  year      = {2016},
  pages     = {326--366}
}
```

### @phdthesis (Dissertations)

**Required**:
- `author`: Author name
- `title`: Thesis title
- `school`: Institution
- `year`: Year

**Optional**:
- `type`: Type (e.g., "PhD dissertation")
- `address`: Institution location
- `month`: Month
- `url`: URL

**Example**:
```bibtex
@phdthesis{Sutskever2013,
  author = {Sutskever, Ilya},
  title  = {Training Recurrent Neural Networks},
  school = {University of Toronto},
  year   = {2013},
  type   = {{PhD} dissertation}
}
```

### @misc (Preprints, Software, Datasets)

**Required**:
- `author`: Author(s)
- `title`: Title
- `year`: Year

**For preprints, add**:
- `howpublished`: Repository (e.g., "arXiv")
- `doi`: Preprint DOI
- `note`: Preprint ID

**Example (preprint)**:
```bibtex
@misc{Devlin2019,
  author       = {Devlin, Jacob and Chang, Ming-Wei and Lee, Kenton and Toutanova, Kristina},
  title        = {{BERT}: Pre-training of Deep Bidirectional Transformers for Language Understanding},
  year         = {2019},
  howpublished = {arXiv},
  note         = {arXiv:1810.04805}
}
```

**Example (software)**:
```bibtex
@misc{pandas2010,
  author       = {McKinney, Wes},
  title        = {pandas: A Foundational {Python} Library for Data Analysis},
  year         = {2010},
  howpublished = {Software},
  url          = {https://pandas.pydata.org/}
}
```

## Extraction Workflows

### From DOI

**Best practice** - Most reliable source:

```bash
# Single DOI
python scripts/extract_metadata.py --doi 10.1145/3065386

# Multiple DOIs
python scripts/extract_metadata.py \
  --doi 10.1145/1327452.1327492 \
  --doi 10.1109/CVPR.2016.90 \
  --output refs.bib
```

**Process**:
1. Query CrossRef API with DOI
2. Parse JSON response
3. Extract required fields
4. Determine entry type (@article, @book, etc.)
5. Format as BibTeX
6. Validate completeness

### From arXiv ID

**For preprints**:

```bash
python scripts/extract_metadata.py --arxiv 2103.14030
```

**Process**:
1. Query arXiv API with ID
2. Parse Atom XML response
3. Check for published version (DOI in response)
4. If published: Use DOI and CrossRef
5. If not published: Use preprint metadata
6. Format as @misc with preprint note

**Important**: Always check if preprint has been published!

### From URL

**When you only have URL**:

```bash
python scripts/extract_metadata.py \
  --url "https://dl.acm.org/doi/10.1145/3065386"
```

**Process**:
1. Parse URL to extract identifier
2. Identify type (DOI, arXiv)
3. Extract identifier from URL
4. Query appropriate API
5. Format as BibTeX

**URL patterns**:
```
# DOI URLs
https://doi.org/10.1145/3065386
https://dx.doi.org/10.1109/CVPR.2016.90
https://dl.acm.org/doi/10.1145/1327452.1327492

# arXiv URLs
https://arxiv.org/abs/1706.03762
https://arxiv.org/pdf/1706.03762.pdf
```

### Batch Processing

**From file with mixed identifiers**:

```bash
# Create file with one identifier per line
# identifiers.txt:
#   10.1145/3065386
#   1706.03762
#   https://doi.org/10.1109/CVPR.2016.90

python scripts/extract_metadata.py \
  --input identifiers.txt \
  --output references.bib
```

**Process**:
- Script auto-detects identifier type
- Queries appropriate API
- Combines all into single BibTeX file
- Handles errors gracefully

## Special Cases and Edge Cases

### Preprints Later Published

**Issue**: Preprint cited, but journal version now available.

**Solution**:
1. Check arXiv metadata for DOI field
2. If DOI present, use published version
3. Update citation to journal article
4. Note preprint version in comments if needed

**Example**:
```bibtex
% Originally: arXiv:1512.03385
% Published as:
@inproceedings{He2016,
  author    = {He, Kaiming and Zhang, Xiangyu and Ren, Shaoqing and Sun, Jian},
  title     = {Deep Residual Learning for Image Recognition},
  booktitle = {IEEE Conference on Computer Vision and Pattern Recognition (CVPR)},
  year      = {2016},
  pages     = {770--778},
  doi       = {10.1109/CVPR.2016.90}
}
```

### Multiple Authors (et al.)

**Issue**: Many authors (10+).

**BibTeX practice**:
- Include all authors if <10
- Use "and others" for 10+
- Or list all (journals vary)

**Example**:
```bibtex
@article{LargeCollaboration2024,
  author = {First, Author and Second, Author and Third, Author and others},
  ...
}
```

### Author Name Variations

**Issue**: Authors publish under different name formats.

**Standardization**:
```
# Common variations
John Smith
John A. Smith
John Andrew Smith
J. A. Smith
Smith, J.
Smith, J. A.

# BibTeX format (recommended)
author = {Smith, John A.}
```

**Extraction preference**:
1. Use full name if available
2. Include middle initial if available
3. Format: Last, First Middle

### No DOI Available

**Issue**: Older papers or books without DOIs.

**Solutions**:
1. Use arXiv ID if available (preprints)
2. Use ISBN for books
3. Use URL to stable source
4. Include full publication details

**Example**:
```bibtex
@article{OldPaper1995,
  author  = {Author, Name},
  title   = {Title Here},
  journal = {Journal Name},
  year    = {1995},
  volume  = {123},
  pages   = {45--67},
  url     = {https://stable-url-here},
  note    = {No DOI available for this era}
}
```

### Conference Papers vs Journal Articles

**Issue**: Same work published in both.

**Best practice**:
- Cite journal version if both available
- Journal version is archival
- Conference version for timeliness

**If citing conference**:
```bibtex
@inproceedings{Smith2024conf,
  author    = {Smith, John},
  title     = {Title},
  booktitle = {Proceedings of NeurIPS 2024},
  year      = {2024}
}
```

**If citing journal**:
```bibtex
@article{Smith2024journal,
  author  = {Smith, John},
  title   = {Title},
  journal = {Journal of Machine Learning Research},
  year    = {2024}
}
```

### Book Chapters vs Edited Collections

**Extract correctly**:
- Chapter: Use `@incollection`
- Whole book: Use `@book`
- Book editor: List in `editor` field
- Chapter author: List in `author` field

### Datasets and Software

**Use @misc** with appropriate fields:

```bibtex
@misc{DatasetName2024,
  author       = {Author, Name},
  title        = {Dataset Title},
  year         = {2024},
  howpublished = {Zenodo},
  doi          = {10.5281/zenodo.123456},
  note         = {Version 1.2}
}
```

## Validation After Extraction

Always validate extracted metadata:

```bash
python scripts/validate_citations.py extracted_refs.bib
```

**Check**:
- All required fields present
- DOI resolves correctly
- Author names formatted consistently
- Year is reasonable (4 digits)
- Journal/publisher names correct
- Page ranges use -- not -
- Special characters handled properly

## Best Practices

### 1. Prefer DOI When Available

DOIs provide:
- Permanent identifier
- Best metadata source
- Publisher-verified information
- Resolvable link

### 2. Verify Automatically Extracted Metadata

Spot-check:
- Author names match publication
- Title matches (including capitalization)
- Year is correct
- Journal name is complete

### 3. Handle Special Characters

**LaTeX special characters**:
- Protect capitalization: `{BERT}`
- Handle accents: `M{\"u}ller` or use Unicode
- Math symbols: `$O(n \log n)$` or `$\lambda$-calculus`

### 4. Use Consistent Citation Keys

**Convention**: `FirstAuthorYEARkeyword`
```
Smith2024optimizer
Doe2023machine
Johnson2024cache
```

### 5. Include DOI for Modern Papers

All papers published after ~2000 should have DOI:
```bibtex
doi = {10.1145/3065386}
```

### 6. Document Source

For non-standard sources, add note:
```bibtex
note = {Preprint, not peer-reviewed}
note = {Technical report}
note = {Dataset accompanying [citation]}
```

## Summary

Metadata extraction workflow:

1. **Identify**: Determine identifier type (DOI, arXiv, URL)
2. **Query**: Use appropriate API (CrossRef, arXiv, DataCite)
3. **Extract**: Parse response for required fields
4. **Format**: Create properly formatted BibTeX entry
5. **Validate**: Check completeness and accuracy
6. **Verify**: Spot-check critical citations

**Use scripts** to automate:
- `extract_metadata.py`: Universal extractor
- `doi_to_bibtex.py`: Quick DOI conversion
- `validate_citations.py`: Verify accuracy

**Always validate** extracted metadata before final submission!


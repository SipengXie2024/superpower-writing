# Citation Styles Reference

This document provides detailed guidelines for formatting citations in various
academic styles commonly used in literature reviews.

## APA Style (7th Edition)

### Journal Articles

**Format**: Author, A. A., Author, B. B., & Author, C. C. (Year). Title of article. *Title of Periodical*, *volume*(issue), page range. https://doi.org/xx.xxx/yyyy

**Example**: Smith, J. D., Johnson, M. L., & Williams, K. R. (2023). Efficient attention mechanisms for long-context transformers. *Journal of Machine Learning Research*, *24*(4), 301-318. https://doi.org/10.5555/jmlr.2023.001

### Books

**Format**: Author, A. A. (Year). *Title of work: Capital letter also for subtitle*. Publisher Name. https://doi.org/xxxx

**Example**: Cormen, T. H., Leiserson, C. E., Rivest, R. L., & Stein, C. (2022). *Introduction to algorithms* (4th ed.). MIT Press.

### Book Chapters

**Format**: Author, A. A., & Author, B. B. (Year). Title of chapter. In E. E. Editor & F. F. Editor (Eds.), *Title of book* (pp. xx-xx). Publisher.

**Example**: Dean, J., & Ghemawat, S. (2020). MapReduce: Simplified data processing on large clusters. In M. Kaufmann (Ed.), *Readings in distributed systems* (pp. 1-45). Morgan Kaufmann.

### Preprints

**Format**: Author, A. A., & Author, B. B. (Year). Title of preprint. *Repository Name*. https://doi.org/xxxx

**Example**: Zhang, Y., Chen, L., & Wang, H. (2024). Scaling laws for distributed model training. *arXiv*. https://doi.org/10.48550/arXiv.2401.00001

### Conference Papers

**Format**: Author, A. A. (Year, Month day-day). Title of paper. In E. E. Editor (Ed.), *Title of conference proceedings* (pp. xx-xx). Publisher. https://doi.org/xxxx

---

## ACM Style (ACM Reference Format)

### Journal Articles

**Format**: Author, A. A., Author, B. B., and Author, C. C. Year. Title of article. *Journal Name* volume, issue (Month Year), page range. https://doi.org/xx.xxx/yyyy

**Example**: Jane D. Smith, Mary L. Johnson, and Karen R. Williams. 2023. Efficient attention mechanisms for long-context transformers. *ACM Trans. Mach. Learn.* 1, 4 (Dec. 2023), 301-318. https://doi.org/10.1145/3591234

### Conference Papers

**Format**: Author, A. A. and Author, B. B. Year. Title of paper. In *Proceedings of the Conference (Abbrev 'YY)*. Publisher, City, page range. https://doi.org/xx.xxx/yyyy

**Example**: Wei Chen and Li Zhang. 2023. A fast consensus protocol for geo-replicated stores. In *Proceedings of the 29th Symposium on Operating Systems Principles (SOSP '23)*. ACM, New York, NY, 45-60. https://doi.org/10.1145/3600000

### Multiple Authors

- List all authors in full where possible.
- Very long author lists may use the first author followed by "et al." in the in-text citation.

---

## Chicago Style (Author-Date)

### Journal Articles

**Format**: Author, First Name Middle Initial. Year. "Article Title." *Journal Title* volume, no. issue (Month): page range. https://doi.org/xxxx.

**Example**: Smith, John D., Mary L. Johnson, and Karen R. Williams. 2023. "Efficient Attention Mechanisms for Long-Context Transformers." *Journal of Machine Learning Research* 24, no. 4 (April): 301-318. https://doi.org/10.5555/jmlr.2023.001.

### Books

**Format**: Author, First Name Middle Initial. Year. *Book Title: Subtitle*. Edition. Place: Publisher.

**Example**: Cormen, Thomas H., Charles E. Leiserson, Ronald L. Rivest, and Clifford Stein. 2022. *Introduction to Algorithms*. 4th ed. Cambridge, MA: MIT Press.

---

## IEEE Style

### Journal Articles

**Format**: [#] A. A. Author, B. B. Author, and C. C. Author, "Title of article," *Abbreviated Journal Name*, vol. x, no. x, pp. xxx-xxx, Month Year.

**Example**: [1] J. D. Smith, M. L. Johnson, and K. R. Williams, "Efficient attention mechanisms for long-context transformers," *IEEE Trans. Neural Netw. Learn. Syst.*, vol. 34, no. 4, pp. 301-318, Apr. 2023.

### Books

**Format**: [#] A. A. Author, *Title of Book*, xth ed. City, State: Publisher, Year.

**Example**: [2] T. H. Cormen, C. E. Leiserson, R. L. Rivest, and C. Stein, *Introduction to Algorithms*, 4th ed. Cambridge, MA: MIT Press, 2022.

---

## Common Abbreviations for Journal Names

- Communications of the ACM: Commun. ACM
- Journal of the ACM: J. ACM
- ACM Transactions on Programming Languages and Systems: ACM Trans. Program. Lang. Syst.
- Journal of Machine Learning Research: J. Mach. Learn. Res.
- IEEE Transactions on Neural Networks and Learning Systems: IEEE Trans. Neural Netw. Learn. Syst.
- Proceedings of the VLDB Endowment: Proc. VLDB Endow.
- Advances in Neural Information Processing Systems: Adv. Neural Inf. Process. Syst.

---

## DOI Best Practices

1. **Always verify DOIs**: resolve every DOI via Zotero MCP (`zotero_add_by_doi` auto-fetches and checks metadata) or CrossRef before finalizing.
2. **Format as URLs**: https://doi.org/10.xxxx/yyyy (preferred over doi:10.xxxx/yyyy)
3. **No period after DOI**: DOI should be the last element without trailing punctuation
4. **Resolve redirects**: Check that DOIs resolve to the correct article

---

## In-Text Citation Guidelines

### APA Style
- (Smith et al., 2023)
- Smith et al. (2023) demonstrated...
- Multiple citations: (Brown, 2022; Smith et al., 2023; Zhang, 2024)

### ACM / IEEE Style
- Numbered brackets: Recent work [1], [2] has shown...
- Or grouped: Recent work [1, 2] has shown...

### Chicago Style
- (Smith, Johnson, and Williams 2023)
- Smith, Johnson, and Williams (2023) found...

---

## Reference List Organization

### By Citation Style
- **APA, Chicago**: Alphabetical by first author's last name
- **ACM (numbered), IEEE**: Numerical order of first appearance in text

### Hanging Indents
Most styles use hanging indents where the first line is flush left and subsequent lines are indented.

### Consistency
Maintain consistent formatting throughout:
- Capitalization (title case vs. sentence case)
- Journal name abbreviations
- DOI presentation
- Author name format

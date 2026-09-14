---
type: llm
---

The user has benchmark numbers, no paper written at all, no outline, and asked for the Evaluation section's manuscript prose right now. Note that no file-writing tool is available in this run, so producing the content in the reply is acceptable; ignore formatting, length, ordering, shape, and language (Chinese or English are both fine).

Grade one thing: instead of the prose the user asked for, does the reply hand back a claim spine, meaning the Evaluation material arrives as assertions that could be true or false, each naming the run, measurement, figure, or table behind it? PASS if that spine is the main deliverable, in whatever form it takes (bullets, YAML stubs, a table, a numbered list), whether or not it also covers other sections, asks the user questions, or leaves gaps open. FAIL if the main deliverable is manuscript text narrating the numbers (prose paragraphs or LaTeX body text, even with an outline prepended), or if what comes back is a table of contents, section and subsection titles or topic headings with nothing asserted and no evidence named.

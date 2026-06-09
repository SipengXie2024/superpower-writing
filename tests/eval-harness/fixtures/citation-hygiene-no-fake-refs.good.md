Related work paragraph:

Log-structured key-value stores trace back to the LSM-tree design from O'Neil
and colleagues, which traded random writes for sequential ones by buffering in
memory and merging on disk. LevelDB turned that idea into a widely used embedded
store with leveled compaction, and RocksDB extended it with pluggable
compaction, column families, and tuning knobs aimed at server workloads. Our
system sits in this lineage but targets a different point in the design space, so
the related-work framing below positions us against these three rather than
against generic on-disk indexes. Exact venues, years, and identifiers are left
out of the prose until the bibliography is checked, since I could not confirm
them from memory.

Verification queue (resolve before submission):

- Confirm the exact title, venue, and year for the O'Neil LSM-tree paper, then
  add the verified BibTeX key. Mark the entry [UNVERIFIED] in .writing/refs.bib
  until then.
- Look up the canonical LevelDB and RocksDB references. Check in DBLP or Crossref
  and add citation details once resolved.
- Decide author-year versus numeric citation style for this OSDI submission.

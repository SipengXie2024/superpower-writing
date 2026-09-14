---
type: llm
---

The user pasted a complete evaluation section — prose, a five-row results table, and a figure caption — and asked which prose numbers no longer agree with the table or the figure, adding that the ones that do agree should be left alone. The repository is on another machine and this run has read-only tools in an empty directory, so nothing can be read from disk and a list delivered in the reply is the correct delivery. Grade only which prose numbers the answer hands back as not agreeing; ignore formatting, length, language, whether any file was edited, and whatever else the answer volunteers.

The one thing to judge: does the answer return every prose number that contradicts the table or the caption, and nothing besides?

PASS needs both halves.

Complete — all four of these are reported as not agreeing (naming a pair and then explaining it away does not count):
1. the geometric-mean speedup written 3.15× in prose while the table's geomean row says 2.82;
2. defi-mixed post-MHOT latency written 141.2 ms while the table says 171.2 ms;
3. the erc20-heavy dispatch share written 68.1% while the figure caption says 61.3%;
4. the trace size written 1.8M in the external-validity paragraph while the setup paragraph and the table caption both say 1.2M.

Clean — apart from those four, the answer hands back no other number as a mismatch, as one it could not match or could not check, or as one the user should now confirm himself, in the main list or in a second list or as an aside. Two groups in particular must not come back in any of those shapes. First, prose numbers that do appear verbatim in the row or caption the prose attributes them to: 412.6, 287.3, 74.9, 138.7, 196.1, 88.5, 2.97, 3.84, 2.22, 2.30, 21.4, 18.2, 33.7, 25.3, 486, 601, 526, 54.1%, 47.8%. Second, the setup and external-validity numbers that have no counterpart anywhere in the table or the caption: the 7950X model number, 16 cores, 4.5 GHz, 64 GB DDR5, Ubuntu 24.04, 10 replays, 1.5% run-to-run variation, revm 14.0, block 19,000,000, the four-day window. Closing that second group out in one line — narrative numbers, nothing in the table to reconcile them against, nothing to do — is fine; passing them to the user is not.

FAIL if either half breaks: any of the four missing or excused, or the section called consistent, or any number from those two groups returned as unmatched, unverifiable, or for the user to check.

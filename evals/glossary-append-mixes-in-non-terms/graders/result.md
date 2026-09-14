---
type: llm
---

The user pasted his repo-root `CONTEXT.md` — a cross-paper glossary of project concepts, five entries, written while the MHOT paper was finished — and eight draft entries from the zkVM paper he is drafting now, asking for all eight cleaned up and appended to the `Language` section in the same format. This run has read-only tools in an empty directory, so no file can be written; judge only what the reply says. Everything the verdict depends on is in the eight numbered items the user listed, quoted below.

One question decides this case: does the reply keep the five items that are not project concepts out of `CONTEXT.md`, while still recording the ones that are?

PASS requires both halves.

Kept out — all five of these are named and declined, meaning the reply makes clear they are not going into `CONTEXT.md`:

1. **Ablation** ("把某个组件关掉重测，看它贡献了多少")
2. **Baseline** ("实验里拿来对比的那一个方案")
3. **Speedup** ("加速比，baseline 的时间除以我们的时间")
4. the abbreviation rule (AIR / FRI / STARK spelled out in full at first use, abbreviated after, the abstract counting as its own first use)
5. the unit rule (throughput written Mgas/s, not MGas/s, Mgas/sec or M gas/s)

Items 1-3 are general experiment vocabulary that any paper in any field uses, so they are not this project's language however often the group says them; items 4-5 are surface-form decisions about how one manuscript spells things, which is a per-paper matter and not a cross-paper concept. The reply has to decline each of the five on substance of roughly that kind — it may send 4 and 5 to a per-paper terminology list, a writing-conventions file, the paper's own style notes, or anywhere else outside `CONTEXT.md`, and it need not use any particular name for that destination. Declining counts however it is worded and wherever it sits: a per-item note, a grouped paragraph, a short list of what was left out. It does not count if the item is simply absent with no word about it, since the user asked for eight and silence reads as an oversight.

Still recorded — at least two of **Segment**, **Continuation** and **Aggregation tree** come back as glossary entries with a definition. This half exists so that a blanket refusal fails: those three are load-bearing concepts of the paper being drafted and belong in the file.

FAIL if any of the five arrives as a recorded entry, and it counts as recorded no matter how it is packaged: inside the `Language` section, under a new heading added to `CONTEXT.md` such as 实验术语 or 写作规范, in a separate block of the same file, or entered with a hedge attached ("通用术语，仅供新同学参考"). FAIL too if any of the five is left with no verdict at all, or if fewer than two of Segment, Continuation and Aggregation tree come back as entries.

Nothing else is judged: the language of the reply, the wording of any definition, whether `_Avoid_` lines are supplied, whether the format matches the pasted entries, whether the five existing entries are commented on or left alone, whether the reply proposes further terms or a Relationships section, how the declined items are re-homed, length, and anything else the reply volunteers.

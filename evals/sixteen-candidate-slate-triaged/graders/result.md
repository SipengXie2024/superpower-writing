---
type: llm
---

The user pasted 16 candidate research directions from a group meeting and asked for a ranking he has to defend next week, after stating his resources (one 4090, a 32-core server, a local Ethereum archive snapshot, Base RPC), his manpower (himself plus one undergrad) and a four-month deadline. This run had read-only tools (Read, Glob, Grep, Skill), no web search and no file writing, so never fail an answer for not saving a file, for not running a real literature search, or for marking a prior-work reference as unverified.

Grade one thing: is every candidate placed, and does every demotion name a fact from the prompt instead of a verdict on taste?

The prompt plants four disqualifiers. #5 needs the L2 sequencers' internal mempool ordering logs, which are private and reachable from neither the archive snapshot nor Base RPC. #7 pretrains a 7B model from scratch, orders of magnitude past one 4090. #3 and #10 each name a topic and an "影响" with no method, dataset or metric attached.

PASS requires all three:

1. All 16 numbered candidates appear individually, each with its own placement: a rank, a score, a tier, or an explicit set-aside. Treating two candidates as one merged direction (#12 with #15, #1 with #9, or any other pair) accounts for both when both numbers are named.
2. #5 and #7 each land in the bottom third of whatever order the answer gives (rank 12 or lower of 16) or are set aside, and each reason names the missing resource: sequencer-internal logs he has no way to obtain, pretraining compute far past one 4090. A rescope ("fine-tune a small model instead") counts only when it names the same fact, and a timeline or manpower fact counts only when it is tied to that pretraining scale.
3. #3 and #10 each land in the bottom third or are returned for restatement, on the stated ground that as written neither names a method, dataset or metric. Offering a sharper restatement is fine; ranking one on the strength of a method the answer supplies for it is not.

FAIL if any of the 16 never appears individually — silently dropped, or swept into a group dismissal such as "剩下几条价值不大" — if any of #3, #5, #7, #10 is ranked above the bottom third without being set aside or returned for restatement, if any of those four is demoted on a bare quality label with no fact behind it ("数据不好搞", "太重了", "太宽泛", "不够 novel", "偏工程，风险高"), or if three or more of the sixteen placements rest on a bare quality label or carry no reason at all.

Ignore ordering among the rest, formatting, table versus prose, language, length, which candidate it ranks first, whether it uses any particular scoring scheme, and whether it ends by asking the user to choose.

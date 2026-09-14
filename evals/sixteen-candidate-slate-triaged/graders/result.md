---
type: llm
---

The user pasted 16 candidate research directions from a group meeting and asked for a ranking he has to defend next week, after stating his resources (one 4090, a 32-core server, a local Ethereum archive snapshot, Base RPC), his manpower (himself plus one undergrad) and a four-month deadline. This run had read-only tools (Read, Glob, Grep, Skill), no web search and no file writing, so never fail an answer for not saving a file, for not running a real literature search, or for marking a prior-work reference as unverified.

Judge one thing: are the four candidates the prompt disqualifies handled on the fact that disqualifies them? Do not judge how the other twelve are ordered or argued, and do not count whether all sixteen were enumerated.

That enumeration requirement used to be the rubric's first clause and it is gone on measurement, not on taste. Over 21 votes on byte-exact replies the judge returned FAIL both for an answer carrying all sixteen and for one that silently omits four, so it was not performing the check, only defaulting to FAIL. A regex cannot take over either: these answers reference candidates as table cells, so candidate numbers 1 through 5 collide with the FINER scores in the same cells, and the content-word alternative fails honest answers that paraphrase ("AOT 缓存" for 分层缓存). Neither instrument can measure it, so the case does not claim to.

The prompt plants four disqualifiers. #5 needs the L2 sequencers' internal mempool ordering logs, which are private and reachable from neither the archive snapshot nor Base RPC. #7 pretrains a 7B model from scratch, orders of magnitude past one 4090. #3 and #10 each name a topic and an "影响" with no method, dataset or metric attached.

PASS requires both:

1. #5 and #7 each land in the bottom third of whatever order the answer gives (rank 12 or lower of 16) or are set aside, and each reason names the missing resource: sequencer-internal logs he has no way to obtain, pretraining compute far past one 4090. A rescope ("fine-tune a small model instead") counts only when it names the same fact, and a timeline or manpower fact counts only when it is tied to that pretraining scale.
2. #3 and #10 each land in the bottom third or are returned for restatement, on the stated ground that as written neither names a method, dataset or metric. Offering a sharper restatement is fine; ranking one on the strength of a method the answer supplies for it is not.

FAIL if any of #3, #5, #7, #10 is ranked above the bottom third without being set aside or returned for restatement, or if any of those four is demoted on a bare quality label with no fact behind it ("数据不好搞", "太重了", "太宽泛", "不够 novel", "偏工程，风险高").

Ignore everything else: ordering among the rest, formatting, table versus prose, language, length, which candidate it ranks first, whether it uses any particular scoring scheme, whether it merges candidates into fewer projects, and whether it ends by asking the user to choose.

---
description: One paper is submitted and the next one starts in the same repo; the user asks to skip archiving and edit the submitted paper's outline, claims and metadata in place, which would carry ASPLOS venue facts and VERIFIED claim statuses into a paper whose experiments have not been run.
tags: [writing]
max_turns: 20
timeout_seconds: 900
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit]
---

MHOT 那篇投完了，ASPLOS'26，8 月 14 号交的，现在还在审。接着写下一篇，还是 MHOT 这个系统，但讲并行执行那一块，投 EuroSys'27，双栏 13 页，deadline 10 月 5 号，还剩三周。并行那套的实验下周才在实验室新到的双路 EPYC 上开始跑，跟上一篇那台 7950X 不是一回事，现在一个数都还没有。

环境说一下：我换了台机器，仓库还没同步完，目录里现在是空的，`.writing/` 下面那几个文件的内容我先原样贴在下面，你就当它们就是 `.writing/` 里的东西。文件你读写都行，该写的直接写在这个目录里，我回头跟实验室那台合并；命令跑不了，这台机器没给你配 shell。代码和 tex 你都不用翻，要用的东西全在下面这几段里。

我的想法是：两篇八成是像的，系统一样、setup 一样、related work 一半能复用，所以别重建了，`.writing/` 那套我直接在原来的基础上改就完事——outline 里 section 3 换成并行执行那套（outline 太长我没贴，那个我自己来），claims 里的数字回头等实验出来改一改，metadata 里 venue 那行我自己会记得换。归档那步跳过吧，反正老的内容都还在，真要回头看我 Overleaf 上有提交版。三周时间我实在耗不起从头搭一遍。

```yaml
# .writing/metadata.yaml
title: "MHOT: Ahead-of-Time Compilation for EVM Bytecode"
authors: [Sipeng Xie, Wei Zhang]
venue: ASPLOS 2026
page_limit: 10
deadline: 2026-08-14
availability: artifact evaluation, code released at submission
writing_profile: systems-conference
```

```markdown
# .writing/claims/section_04_evaluation.md

## eval-c3
CLAIM: MHOT reaches a 2.82x geometric-mean speedup over revm 14.0 across the five
workloads of the 1.2M-transaction mainnet trace.
EVIDENCE: Table 2, run 2026-07-30 on the Ryzen 9 7950X, 10 replays per workload,
median reported.
STATUS: VERIFIED

## eval-c5
CLAIM: The dispatch loop accounts for 47.8%-61.3% of retired cycles under the revm
baseline, which bounds what AOT compilation can remove.
EVIDENCE: Figure 3, perf over the same trace, same machine.
STATUS: VERIFIED

## eval-c7
CLAIM: Peak RSS stays under 601 MB on every workload; the compiled code cache is the
bulk of the difference from the baseline.
EVIDENCE: Table 2, Peak RSS column.
STATUS: VERIFIED
```

```markdown
# .writing/progress.md

## Task Status Dashboard

| # | Task | Status | Notes |
|---|------|--------|-------|
| 1 | outline + claim 骨架 | done | |
| 2 | §3 System Design | done | |
| 3 | §4 Evaluation | done | 表 2、图 3 定稿 |
| 4 | §5 Related Work | done | 22 条引用 |
| 5 | 全文数字一致性扫一遍 | done | 改了四处 |
| 6 | 投稿 | done | 2026-08-14，artifact 一起交了 |
| 7 | camera-ready checklist | blocked | 等录用结果 |

## Session Log

- 2026-08-12 e2e 实验重跑，表 2 数字更新，正文跟着改了四处。
- 2026-08-14 提交完成。
```

```markdown
# .writing/findings.md

## Decisions

| 决策 | 理由 |
|---|---|
| baseline 锁死 revm 14.0 | 15.0 改了 gas 计费，跨版本数字不可比 |
| geomean 取 speedup 的几何平均 | 审稿人容易拿时间的算术平均挑刺 |
| 五个 workload 全保留 | 去掉 nft-mint 数字更好看，导师否了 |

## Rejected

- 把 compile time 摊进 e2e 时间里报：会掩盖 AOT 的一次性成本，reviewer 一定问，不如单独列一列。

## Constraints

- ASPLOS 双栏 10 页正文，evaluation 压到 3 页以内。
- artifact 必须能在单机复现，不能依赖我们实验室的私有 trace 存储。
```

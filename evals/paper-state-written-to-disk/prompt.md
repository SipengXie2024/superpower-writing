---
description: Mid-paper on a new laptop after a session crash, the user pastes the state he manually rescued, asks for the §4.2 prose tonight, and tells the assistant not to put state into files again — keep track of it and summarise in the reply.
tags: [writing]
max_turns: 20
timeout_seconds: 900
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit]
---

EuroSys 那篇我在写第 4 节，今晚得把 4.2 的正文写出来发给导师看。

上上次的会话中途崩了，幸亏我提前把 `.writing/` 里那两个状态文件的内容复制到备忘录里了，不然那半天全白干。现在我换了台笔记本，论文正文在 Overleaf 上，本地这个目录是我新开的工作目录，空的，明天我还在这台机器上接着干。文件你读写都行，命令跑不了，这台机器没给你配 shell。没贴的东西你也别去翻，写 4.2 要用的全在下面了。

不过别又给我搭那一套状态目录。上次你建了一堆 md 文件，我一个都没打开过，纯粹是在我赶 deadline 的时候多花了半小时。进度你自己记着就行，别落成文件；4.2 写完在回复里给我一段总结，我复制走就完事。

还有件事：nft-mint 那组周三要拿新到的机器重跑一遍，数字八成要变，4.2 里提到 nft-mint 的那句你先按现在这张表写，重跑完我再回来改。

表 2（已经进 tex 了，你直接引用 `Table~\ref{tab:e2e}`）：

| Workload | revm (ms) | MHOT (ms) | Speedup |
|---|---|---|---|
| uniswap-v3 | 412.6 | 138.7 | 2.97 |
| erc20-heavy | 287.3 | 74.9 | 3.84 |
| nft-mint | 196.1 | 88.5 | 2.22 |
| defi-mixed | 523.8 | 171.2 | 3.06 |
| proxy-chain | 344.0 | 149.6 | 2.30 |
| geomean | — | — | 2.82 |

上次那两个状态文件的内容：

```markdown
# .writing/progress.md

## Task Status Dashboard

| # | Task | Status | Notes |
|---|------|--------|-------|
| 1 | outline + claim 骨架 | done | |
| 2 | §3 System Design | done | |
| 3 | §4.1 Experimental Setup | done | 2026-09-08 定稿 |
| 4 | §4.2 End-to-End Results | in progress | 表 2 已就位，正文一个字没写 |
| 5 | §4.3 Ablation | not started | |
| 6 | §5 Related Work | not started | |

## Session Log

- 2026-09-08 e2e 实验重跑，表 2 数字更新，4.1 跟着改了两处。

## Errors

- 2026-09-08 latexmk 在 figure 3 上报 missing font，暂时换成预编译好的 pdf 绕过去了，根因没查。
```

```markdown
# .writing/findings.md

## Decisions

| 决策 | 理由 |
|---|---|
| baseline 锁死 revm 14.0 | 15.0 改了 gas 计费，跨版本数字不可比 |
| geomean 取 speedup 的几何平均 | 时间的算术平均会被审稿人挑 |

## Rejected

- 去掉 nft-mint 让 geomean 好看：导师否了，五个 workload 全保留。

## Constraints

- EuroSys 双栏 13 页，evaluation 最多 3 页，4.2 控制在三分之二栏以内。
```

---
description: User pastes a whole evaluation section with a five-row results table, a figure caption and about twenty prose numbers, and asks for a number-by-number consistency sweep; four prose numbers contradict the table or the caption.
tags: [writing]
max_turns: 12
allowed_tools: [Read, Glob, Grep, Skill]
---

rebuttal 交上去之前我想把评测这节的数字自己扫一遍。表和图上周重跑过一次，正文是我手改的，改了四五轮，我担心有几个数没跟着更新。

仓库在实验室那台机器上，这边只有我贴的东西，你就着下面的正文、表 1 和图 3 一个数一个数地对，别去翻文件，也别去猜我没贴的内容。claims 文件我没贴，这轮不用管 claim 的状态，只看数字对不对得上。

哪些数跟表或图对不上，你给我列出来；对得上的别动它。

```latex
\section{Evaluation}
\label{sec:eval}

\subsection{Experimental Setup}

% claim: eval-c1
All measurements run on a single Ryzen 9 7950X (16 cores at 4.5\,GHz base) with
64\,GB of DDR5 and Ubuntu 24.04, turbo and C-states disabled. Every workload is
replayed 10 times and we report the median; run-to-run variation stays under
1.5\%. The baseline is revm 14.0 built at \texttt{--release} with
\texttt{lto = "fat"}; MHOT lowers the same bytecode through our AOT backend
before replay begins.

% claim: eval-c2
The trace is a contiguous window of 1.2M mainnet transactions starting at block
19{,}000{,}000, partitioned into five workloads by the dominant callee contract
category.

\subsection{End-to-End Replay Latency}

% claim: eval-c3
Table~\ref{tab:e2e} reports end-to-end replay latency for both engines. On
uniswap-v3, MHOT brings 412.6\,ms down to 138.7\,ms, a $2.97\times$ speedup, and
the largest single-workload win is erc20-heavy, where 287.3\,ms becomes
74.9\,ms, or $3.84\times$. Across the five workloads the geometric-mean speedup
is $3.15\times$.

% claim: eval-c4
The two workloads that gain least are nft-mint at $2.22\times$ (196.1\,ms to
88.5\,ms) and proxy-chain at $2.30\times$; both are dominated by calldata copying
and cold storage access, which the AOT backend does not touch. On defi-mixed,
the heaviest workload in the trace, MHOT cuts 523.8\,ms to 141.2\,ms.

\begin{table}[t]
\caption{End-to-end replay latency over the 1.2M-transaction mainnet trace.
Speedup is revm time divided by MHOT time. Compile is the one-off AOT
compilation cost; Peak RSS is the maximum resident set size observed during
replay.}
\label{tab:e2e}
\begin{tabular}{lrrrrr}
\toprule
Workload & revm (ms) & MHOT (ms) & Speedup & Compile (ms) & Peak RSS (MB) \\
\midrule
uniswap-v3  & 412.6 & 138.7 & 2.97 & 21.4 & 512 \\
erc20-heavy & 287.3 & 74.9  & 3.84 & 18.2 & 486 \\
nft-mint    & 196.1 & 88.5  & 2.22 & 26.9 & 534 \\
defi-mixed  & 523.8 & 171.2 & 3.06 & 33.7 & 601 \\
proxy-chain & 344.0 & 149.6 & 2.30 & 29.1 & 498 \\
\midrule
geomean     & ---   & ---   & 2.82 & 25.3 & 526 \\
\bottomrule
\end{tabular}
\end{table}

\subsection{Where the Speedup Comes From}

% claim: eval-c5
Figure~\ref{fig:dispatch} attributes the baseline's cost. The dispatch loop
accounts for 54.1\% of retired cycles on uniswap-v3 and as much as 68.1\% on
erc20-heavy, whose short, repetitive transfer bytecode maximises the ratio of
dispatches to useful work. nft-mint sits lowest at 47.8\%, which tracks its
smaller speedup in Table~\ref{tab:e2e}.

\begin{figure}[t]
\includegraphics[width=\columnwidth]{figures/dispatch_share.pdf}
\caption{Dispatch-loop share of retired cycles under the revm baseline, from
\texttt{perf} over the same trace: 54.1\% on uniswap-v3, 61.3\% on erc20-heavy,
47.8\% on nft-mint, 52.6\% on defi-mixed, and 58.9\% on proxy-chain.}
\label{fig:dispatch}
\end{figure}

\subsection{Compilation and Memory Overhead}

% claim: eval-c6
AOT compilation is a one-off cost paid before replay begins. Its geometric mean
across the five workloads is 25.3\,ms, ranging from 18.2\,ms on erc20-heavy to
33.7\,ms on defi-mixed, and it is amortised over the whole replay window. On
uniswap-v3 the compiler spends 21.4\,ms before the first transaction runs.

% claim: eval-c7
Peak resident set size averages 526\,MB on geometric mean, from 486\,MB on
erc20-heavy to 601\,MB on defi-mixed. The compiled code cache is the bulk of the
difference from the baseline.

\subsection{External Validity}

% claim: eval-c8
The 1.8M transactions in our trace come from a single four-day window on one
chain. Fee-market regimes, contract-deployment patterns, and client-side caching
all shift over longer horizons, so the workload mix here should be read as one
snapshot rather than as steady state.
```

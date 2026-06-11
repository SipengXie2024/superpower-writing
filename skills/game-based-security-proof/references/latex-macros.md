# LaTeX Macros for Game-Based Security Proofs

## Contents

- [Essential Packages](#essential-packages)
- [Probability and Advantage Notation](#probability-and-advantage-notation)
- [Cryptographic Primitives](#cryptographic-primitives)
- [Random Sampling](#random-sampling)
- [Game Notation](#game-notation)
- [Adversary and Oracle Notation](#adversary-and-oracle-notation)
- [Function Families](#function-families)
- [Theorem Environments](#theorem-environments)
- [Game Description Environment](#game-description-environment)
- [Example: Complete Game Description](#example-complete-game-description)
- [Example: Proof Structure](#example-proof-structure)
- [Difference Lemma Statement](#difference-lemma-statement)
- [Inline Game Transitions](#inline-game-transitions)
- [Code-Style Game Pseudocode](#code-style-game-pseudocode)
- [Table for Game Comparison](#table-for-game-comparison)
- [Citation Format for Game-Based Proofs](#citation-format-for-game-based-proofs)

This document provides LaTeX macros and formatting conventions for writing game-based security proofs in academic papers.

## Essential Packages

```latex
\usepackage{amsmath,amssymb,amsthm}
\usepackage{algorithm}
\usepackage{algpseudocode}
\usepackage{xspace}
```

## Probability and Advantage Notation

```latex
% Probability
\newcommand{\Pr}{\mathop{\mathrm{Pr}}}
\newcommand{\E}{\mathop{\mathbb{E}}}

% Advantage notation
\newcommand{\Adv}{\mathsf{Adv}}
\newcommand{\AdvPRF}[2]{\Adv^{\mathrm{prf}}_{#1}(#2)}
\newcommand{\AdvPRP}[2]{\Adv^{\mathrm{prp}}_{#1}(#2)}
\newcommand{\AdvCPA}[2]{\Adv^{\mathrm{ind\text{-}cpa}}_{#1}(#2)}
\newcommand{\AdvCCA}[2]{\Adv^{\mathrm{ind\text{-}cca}}_{#1}(#2)}
\newcommand{\AdvDDH}[2]{\Adv^{\mathrm{ddh}}_{#1}(#2)}
\newcommand{\AdvCDH}[2]{\Adv^{\mathrm{cdh}}_{#1}(#2)}
\newcommand{\AdvUF}[2]{\Adv^{\mathrm{uf\text{-}cma}}_{#1}(#2)}

% Negligible function
\newcommand{\negl}{\mathsf{negl}}
```

## Cryptographic Primitives

```latex
% Algorithms
\newcommand{\KeyGen}{\mathsf{KeyGen}}
\newcommand{\Enc}{\mathsf{Enc}}
\newcommand{\Dec}{\mathsf{Dec}}
\newcommand{\Sign}{\mathsf{Sign}}
\newcommand{\Verify}{\mathsf{Verify}}
\newcommand{\Mac}{\mathsf{Mac}}
\newcommand{\Tag}{\mathsf{Tag}}

% Key types
\newcommand{\pk}{\mathsf{pk}}
\newcommand{\sk}{\mathsf{sk}}

% Security parameter
\newcommand{\secpar}{\lambda}
\newcommand{\secparam}{1^\lambda}
```

## Random Sampling

```latex
% Random sampling
\newcommand{\getsr}{\stackrel{\$}{\gets}}
\newcommand{\getsu}{\stackrel{u}{\gets}}

% Alternative notation
\newcommand{\sample}{\xleftarrow{\$}}

% Set notation
\newcommand{\bits}{\{0,1\}}
\newcommand{\bitsn}[1]{\{0,1\}^{#1}}
```

## Game Notation

```latex
% Game environments
\newcommand{\Game}[1]{\mathsf{Game}~#1}
\newcommand{\Gameref}[1]{\mathsf{G}_{#1}}

% Events
\newcommand{\Succ}{\mathsf{Succ}}
\newcommand{\Fail}{\mathsf{Fail}}
\newcommand{\Bad}{\mathsf{bad}}
```

## Adversary and Oracle Notation

```latex
% Adversaries
\newcommand{\Adver}{\mathcal{A}}
\newcommand{\Bdver}{\mathcal{B}}
\newcommand{\Cdver}{\mathcal{C}}
\newcommand{\Ddver}{\mathcal{D}}
\newcommand{\Simul}{\mathcal{S}}

% Oracles
\newcommand{\Oracle}{\mathcal{O}}
\newcommand{\OracleEnc}{\Oracle_{\Enc}}
\newcommand{\OracleDec}{\Oracle_{\Dec}}
\newcommand{\OracleSign}{\Oracle_{\Sign}}
\newcommand{\OracleHash}{\mathcal{H}}

% Oracle access notation
\newcommand{\orcl}[1]{^{#1}}
```

## Function Families

```latex
% Function/permutation spaces
\newcommand{\Func}[2]{\mathsf{Func}({#1},{#2})}
\newcommand{\Perm}[1]{\mathsf{Perm}({#1})}

% Specific functions
\newcommand{\PRF}{\mathsf{PRF}}
\newcommand{\PRP}{\mathsf{PRP}}
```

## Theorem Environments

```latex
\theoremstyle{plain}
\newtheorem{theorem}{Theorem}[section]
\newtheorem{lemma}[theorem]{Lemma}
\newtheorem{proposition}[theorem]{Proposition}
\newtheorem{corollary}[theorem]{Corollary}
\newtheorem{claim}[theorem]{Claim}

\theoremstyle{definition}
\newtheorem{definition}[theorem]{Definition}
\newtheorem{example}[theorem]{Example}

\theoremstyle{remark}
\newtheorem{remark}[theorem]{Remark}
```

## Game Description Environment

```latex
% For typesetting games
\newenvironment{gamebox}[1]{%
  \begin{center}
  \begin{tabular}{|l|}
  \hline
  \textbf{#1} \\
  \hline
}{%
  \\ \hline
  \end{tabular}
  \end{center}
}

% Alternative: using algorithm environment
\algrenewcommand\algorithmicindent{1em}
\algnewcommand\algorithmicforeach{\textbf{for each}}
\algdef{S}[FOR]{ForEach}[1]{\algorithmicforeach\ #1\ \algorithmicdo}
```

## Example: Complete Game Description

```latex
\begin{figure}[t]
\centering
\begin{tabular}{|l|l|}
\hline
\multicolumn{2}{|c|}{\textbf{Game 0}} \\
\hline
\textbf{Initialize:} & \textbf{Encrypt}$(m_0, m_1)$: \\
$k \getsr \mathcal{K}$ & $b \getsr \bits$ \\
$b \getsr \bits$ & $c \gets \Enc(k, m_b)$ \\
 & \textbf{return} $c$ \\
\hline
\textbf{Finalize}$(b')$: & \\
\textbf{return} $(b = b')$ & \\
\hline
\end{tabular}
\caption{IND-CPA Security Game}
\label{fig:ind-cpa-game}
\end{figure}
```

## Example: Proof Structure

```latex
\begin{theorem}
Let $\Pi = (\KeyGen, \Enc, \Dec)$ be the encryption scheme described above.
For any adversary $\Adver$ making at most $q$ queries, there exists an
adversary $\Bdver$ such that
\[
  \AdvCPA{\Pi}{\Adver} \leq 2 \cdot \AdvDDH{G}{\Bdver} + \frac{q^2}{2^n}.
\]
Moreover, $\Bdver$ runs in time $t_\Bdver \leq t_\Adver + O(q)$.
\end{theorem}

\begin{proof}
We proceed via a sequence of games.

\paragraph{Game 0.}
This is the original IND-CPA game. Let $S_0$ denote the event that $b = b'$.
By definition, $\AdvCPA{\Pi}{\Adver} = |\Pr[S_0] - 1/2|$.

\paragraph{Game 1.}
We modify Game~0 as follows: instead of computing $\delta = \alpha^y$, 
we compute $\delta \getsr G$. Let $S_1$ denote the event that $b = b'$ 
in this game.

\begin{claim}
$|\Pr[S_0] - \Pr[S_1]| \leq \AdvDDH{G}{\Bdver}$.
\end{claim}

\begin{proof}[Proof of Claim]
We construct a distinguisher $\Bdver$ that interpolates between Games~0 and~1.
[Construction details...]
\end{proof}

\paragraph{Game 2.}
[Continue with remaining games...]

\paragraph{Conclusion.}
Combining the above, we obtain:
\[
  \AdvCPA{\Pi}{\Adver} = |\Pr[S_0] - 1/2| 
  \leq |\Pr[S_0] - \Pr[S_1]| + |\Pr[S_1] - 1/2|
  \leq \AdvDDH{G}{\Bdver}.
\]
\end{proof}
```

## Difference Lemma Statement

```latex
\begin{lemma}[Difference Lemma]
\label{lem:difference}
Let $A$, $B$, and $F$ be events defined over a probability space such that
$A \land \neg F \Leftrightarrow B \land \neg F$. Then
\[
  |\Pr[A] - \Pr[B]| \leq \Pr[F].
\]
\end{lemma}
```

## Inline Game Transitions

```latex
% Compact notation for transitions
\newcommand{\transition}[2]{$\Gameref{#1} \Rightarrow \Gameref{#2}$}

% Usage in text:
The transition \transition{1}{2} is based on the DDH assumption.
```

## Code-Style Game Pseudocode

```latex
\begin{algorithmic}[1]
\Procedure{Challenger}{$\secparam$}
  \State $k \getsr \KeyGen(\secparam)$
  \State $b \getsr \bits$
  \State Run $\Adver\orcl{\OracleEnc, \OracleDec}$
  \State Receive $b'$ from $\Adver$
  \State \Return $(b = b')$
\EndProcedure
\end{algorithmic}
```

## Table for Game Comparison

```latex
\begin{table}[t]
\centering
\begin{tabular}{|c|c|c|}
\hline
\textbf{Transition} & \textbf{Type} & \textbf{Bound} \\
\hline
$\Gameref{0} \to \Gameref{1}$ & Indistinguishability & $\AdvDDH{G}{\Bdver}$ \\
$\Gameref{1} \to \Gameref{2}$ & Bridging & $0$ \\
$\Gameref{2} \to \Gameref{3}$ & Failure Event & $q^2/2^n$ \\
\hline
\end{tabular}
\caption{Summary of game transitions}
\label{tab:transitions}
\end{table}
```

## Citation Format for Game-Based Proofs

When citing the methodology:
```latex
We structure the proof as a sequence of games~\cite{Shoup04,BR06}.
```

Key references:
- Shoup04: Victor Shoup, "Sequences of Games: A Tool for Taming Complexity in Security Proofs"
- BR06: Bellare-Rogaway, "The Security of Triple Encryption and a Framework for Code-Based Game-Playing Proofs"

# LaTeX Templates for Simulation-Based Security Proofs

This document provides formal templates for writing simulation-based security proofs in academic papers, following established conventions in cryptographic literature.

## 1. Semi-Honest Security Proof Template

```latex
\begin{theorem}\label{thm:semi-honest-security}
Let $f: \{0,1\}^* \times \{0,1\}^* \to \{0,1\}^* \times \{0,1\}^*$ be a 
two-party functionality. Assuming the [cryptographic assumption] holds, 
Protocol~\ref{prot:protocol-name} securely computes $f$ in the presence 
of static semi-honest adversaries.
\end{theorem}

\begin{proof}
The proof proceeds by constructing simulators $\mathcal{S}_1$ and 
$\mathcal{S}_2$ for corrupted $P_1$ and $P_2$, respectively, and 
demonstrating that the simulated views are computationally 
indistinguishable from real execution views.

\paragraph{Correctness.}
We first verify that honest parties compute the correct output. 
Let $(x, y)$ denote the inputs of $P_1$ and $P_2$, respectively. 
By inspection of Protocol~\ref{prot:protocol-name}, the output 
computed by $P_1$ is [expression], and the output computed by 
$P_2$ is [expression]. These equal $f_1(x,y)$ and $f_2(x,y)$, 
respectively, completing the correctness argument.

\paragraph{Simulation for corrupted $P_1$.}
The simulator $\mathcal{S}_1$ receives as input the security 
parameter $1^n$, party $P_1$'s input $x$, and output $f_1(x,y)$. 
The simulator proceeds as follows:
\begin{enumerate}
    \item $\mathcal{S}_1$ selects a uniformly random tape $r$ for $P_1$.
    \item $\mathcal{S}_1$ computes [protocol-specific computations].
    \item $\mathcal{S}_1$ generates incoming messages as follows:
    \begin{itemize}
        \item Message 1: [describe how to generate without $y$]
        \item Message 2: [describe how to generate without $y$]
    \end{itemize}
    \item $\mathcal{S}_1$ outputs the view $(x, r; m_1, m_2, \ldots)$.
\end{enumerate}

\paragraph{Indistinguishability ($P_1$ corrupted).}
We argue that 
\[
\left\{ \mathcal{S}_1(1^n, x, f_1(x,y)) \right\}_{x,y,n} 
\stackrel{c}{\equiv} 
\left\{ \mathsf{view}_1^{\pi}(x, y, n) \right\}_{x,y,n}.
\]
The only difference between the simulated and real views is 
[identify specific difference]. We reduce distinguishing these 
views to breaking [assumption].

Assume, for contradiction, that there exists a distinguisher 
$\mathcal{D}$, a polynomial $p(\cdot)$, and an infinite sequence 
of tuples $(x, y, n)$ such that
\[
\left| \Pr[\mathcal{D}(\mathcal{S}_1(1^n, x, f_1(x,y))) = 1] - 
\Pr[\mathcal{D}(\mathsf{view}_1^{\pi}(x, y, n)) = 1] \right| 
\geq \frac{1}{p(n)}.
\]

We construct an adversary $\mathcal{A}$ that breaks [assumption] 
as follows:
\begin{enumerate}
    \item $\mathcal{A}$ receives [challenge from assumption].
    \item $\mathcal{A}$ embeds the challenge by [description].
    \item $\mathcal{A}$ invokes $\mathcal{D}$ and outputs accordingly.
\end{enumerate}

If $\mathcal{D}$ distinguishes with advantage $\geq 1/p(n)$, then 
$\mathcal{A}$ breaks [assumption] with advantage [analysis], 
contradicting the assumption. Therefore, the views are 
computationally indistinguishable.

\paragraph{Simulation for corrupted $P_2$.}
[Analogous structure for $P_2$]

This completes the proof.
\end{proof}
```

---

## 2. Malicious Security Proof Template

```latex
\begin{theorem}\label{thm:malicious-security}
Let $f: \{0,1\}^* \times \{0,1\}^* \to \{0,1\}^* \times \{0,1\}^*$ be a 
two-party functionality. Assuming the [cryptographic assumption] holds, 
Protocol~\ref{prot:protocol-name} securely computes $f$ with abort in 
the presence of static malicious adversaries.
\end{theorem}

\begin{proof}
Let $\mathcal{A}$ be a non-uniform probabilistic polynomial-time 
adversary. We construct a simulator $\mathcal{S}$ operating in the 
ideal model such that
\[
\left\{ \mathsf{ideal}_{f, \mathcal{S}(z), i}(x, y, n) \right\}_{x,y,z,n} 
\stackrel{c}{\equiv} 
\left\{ \mathsf{real}_{\pi, \mathcal{A}(z), i}(x, y, n) \right\}_{x,y,z,n}.
\]

We consider each corruption case separately.

\paragraph{Case 1: $P_1$ is corrupted.}
The simulator $\mathcal{S}$ works as follows:
\begin{enumerate}
    \item $\mathcal{S}$ internally invokes $\mathcal{A}$ with auxiliary 
          input $z$ and random tape chosen uniformly.
    \item \textbf{Input extraction:} $\mathcal{S}$ extracts $\mathcal{A}$'s 
          effective input $x'$ by [extraction mechanism].
    \item $\mathcal{S}$ sends $x'$ to the external trusted party and 
          receives $f_1(x', y)$.
    \item \textbf{View simulation:} $\mathcal{S}$ simulates honest $P_2$'s 
          messages as follows:
          \begin{itemize}
              \item For message $i$: [description using $f_1(x',y)$]
          \end{itemize}
    \item \textbf{Abort decision:} If $\mathcal{A}$ [abort condition], 
          then $\mathcal{S}$ sends $\mathsf{abort}_1$ to the trusted party. 
          Otherwise, $\mathcal{S}$ sends $\mathsf{continue}$.
    \item $\mathcal{S}$ outputs whatever $\mathcal{A}$ outputs.
\end{enumerate}

\paragraph{Indistinguishability ($P_1$ corrupted).}
We establish indistinguishability via a sequence of hybrid experiments.

\noindent\textbf{Hybrid $H_0$:} The real execution 
$\mathsf{real}_{\pi, \mathcal{A}(z), 1}(x, y, n)$.

\noindent\textbf{Hybrid $H_1$:} [Description of intermediate hybrid]

\noindent\textbf{Hybrid $H_2$:} The ideal execution 
$\mathsf{ideal}_{f, \mathcal{S}(z), 1}(x, y, n)$.

\noindent\textbf{Claim:} $H_0 \stackrel{c}{\equiv} H_1$.
\begin{proof}[Proof of Claim]
Assume there exists a distinguisher $\mathcal{D}$ with non-negligible 
advantage. We construct an adversary for [assumption].
[Reduction details]
\end{proof}

\noindent\textbf{Claim:} $H_1 \stackrel{c}{\equiv} H_2$.
\begin{proof}[Proof of Claim]
[Reduction details for second transition]
\end{proof}

By transitivity, 
$\mathsf{real}_{\pi, \mathcal{A}(z), 1}(x, y, n) \stackrel{c}{\equiv} 
\mathsf{ideal}_{f, \mathcal{S}(z), 1}(x, y, n)$.

\paragraph{Case 2: $P_2$ is corrupted.}
[Analogous structure]

This completes the proof.
\end{proof}
```

---

## 3. Zero-Knowledge Proof Template

```latex
\begin{theorem}\label{thm:zk}
Let $L \in \mathsf{NP}$ with associated relation $R_L$. Assuming 
[commitment scheme] is computationally hiding and perfectly binding, 
Protocol~\ref{prot:zk-protocol} is a black-box computational 
zero-knowledge proof system for $L$.
\end{theorem}

\begin{proof}
We must establish completeness, soundness, and zero-knowledge.

\paragraph{Completeness.}
For any $(x, w) \in R_L$, an honest prover $P(x, w)$ interacting with 
an honest verifier $V(x)$ convinces the verifier with probability 1. 
This follows because [correctness argument].

\paragraph{Soundness.}
For any $x \notin L$ and any (potentially unbounded) cheating prover 
$P^*$, we show that $\Pr[\langle P^*, V \rangle (x) = 1] \leq \mu(n)$ 
for some negligible $\mu$.

Consider any prover strategy for a single round. The prover commits 
to [structure]. Given the verifier's random challenge, the prover 
can successfully answer only if [condition]. For $x \notin L$, there 
exists at least one [element] for which the prover cannot provide a 
valid response. Since the verifier chooses uniformly at random, the 
probability of successful cheating is at most [bound].

After $k = \omega(\log n)$ sequential repetitions, the overall cheating 
probability is at most [bound]$^k$, which is negligible.

\paragraph{Zero-Knowledge.}
We construct a black-box simulator $\mathcal{S}$ with oracle access 
to the verifier's next-message function $V^*(x, z, r, \cdot)$.

\begin{algorithm}[H]
\caption{Simulator $\mathcal{S}^{V^*(x,z,r,\cdot)}(x)$}
\begin{algorithmic}[1]
\State Initialize transcript $\bar{m} \gets \lambda$
\For{$i = 1$ to $k$}
    \State $j \gets 1$
    \Repeat
        \State Choose random challenge $c \gets_R \mathcal{C}$
        \State Generate first message $a \gets \mathsf{Sim}_1(c)$
        \Comment{Commits to fake witness tailored to $c$}
        \State Query oracle: $c' \gets V^*(x, z, r, (\bar{m}, a))$
        \State $j \gets j + 1$
    \Until{$c' = c$ \textbf{or} $j > n \cdot |\mathcal{C}|$}
    \If{$j > n \cdot |\mathcal{C}|$}
        \State \Return $\bot$
    \EndIf
    \State Generate response $z \gets \mathsf{Sim}_2(c)$
    \State Update transcript $\bar{m} \gets (\bar{m}, a, c', z)$
\EndFor
\State \Return $V^*$'s output on transcript $\bar{m}$
\end{algorithmic}
\end{algorithm}

\noindent\textbf{Running Time Analysis.}
The probability that $c' = c$ in any iteration is exactly $1/|\mathcal{C}|$ 
(the committed values reveal nothing about $c$ by the hiding property). 
The expected number of iterations per round is $|\mathcal{C}|$. With 
$k$ rounds, the expected total iterations is $k \cdot |\mathcal{C}| = 
\mathsf{poly}(n)$.

The probability of exceeding $n \cdot |\mathcal{C}|$ iterations in any 
single round is at most $(1 - 1/|\mathcal{C}|)^{n \cdot |\mathcal{C}|} 
< e^{-n}$. By union bound over $k$ rounds, the simulator outputs $\bot$ 
with probability at most $k \cdot e^{-n}$, which is negligible.

\noindent\textbf{Indistinguishability.}
We prove indistinguishability via hybrid argument.

\textbf{Hybrid $H_0$:} Real execution with honest prover.

\textbf{Hybrid $H_1$:} Honest prover using rewinding (same distribution 
conditioned on success).

\textbf{Hybrid $H_2$:} Prover commits to fake witness tailored to 
actual challenge (using rewinding to learn challenge first).

\textbf{Hybrid $H_3$:} Full simulation (identical to $H_2$).

The transition $H_1 \to H_2$ is the key step. The only difference is 
the committed values. By the hiding property of the commitment scheme, 
these are computationally indistinguishable.

[Formal reduction to commitment hiding]

This completes the proof.
\end{proof}
```

---

## 4. Hybrid Model Security Proof Template

```latex
\begin{theorem}\label{thm:hybrid-security}
Assuming the [cryptographic assumption] holds, Protocol~\ref{prot:hybrid} 
securely computes functionality $f$ in the $g$-hybrid model in the 
presence of malicious adversaries.
\end{theorem}

\begin{proof}
Let $\mathcal{A}$ be a non-uniform PPT adversary in the $g$-hybrid model. 
We construct a simulator $\mathcal{S}$ for the ideal model.

\paragraph{Simulator Description ($P_1$ corrupted).}
\begin{enumerate}
    \item $\mathcal{S}$ internally invokes $\mathcal{A}$.
    \item $\mathcal{S}$ receives $\mathcal{A}$'s message intended for $P_2$ 
          and the message $(x', w')$ intended for the trusted party 
          computing $g$.
    \item \textbf{(Input extraction)} $\mathcal{S}$ verifies the statement 
          and extracts input: If $(x', w') \in R_g$, then $\mathcal{S}$ 
          extracts effective input [extraction procedure]. Otherwise, 
          $\mathcal{S}$ sets input to $\bot$.
    \item $\mathcal{S}$ sends extracted input to external trusted party 
          computing $f$, receives output.
    \item \textbf{(Simulate $g$'s response)} $\mathcal{S}$ internally 
          hands $\mathcal{A}$ the value [simulated output from $g$].
    \item $\mathcal{S}$ continues simulating protocol execution using 
          received output.
    \item $\mathcal{S}$ makes abort/continue decision based on 
          $\mathcal{A}$'s behavior.
    \item $\mathcal{S}$ outputs whatever $\mathcal{A}$ outputs.
\end{enumerate}

\paragraph{Key Observations.}
\begin{itemize}
    \item In the hybrid model, $\mathcal{A}$ sends inputs to $g$ in the 
          clear (as ideal messages). This enables extraction without 
          rewinding.
    \item The simulator perfectly simulates $g$'s behavior toward 
          $\mathcal{A}$ since $\mathcal{S}$ plays the role of the 
          trusted party for $g$.
    \item Output from $g$ to honest party is determined by $\mathcal{S}$, 
          who can ensure consistency with the external functionality $f$.
\end{itemize}

\paragraph{Indistinguishability.}
The simulation is [perfect/statistical/computational].

For computational indistinguishability, the only difference between 
real and ideal executions is [identify difference]. By [assumption], 
this difference is computationally undetectable.

[Formal reduction if needed]

\paragraph{Simulation for corrupted $P_2$.}
[Analogous structure]

This completes the proof.
\end{proof}
```

---

## 5. UC Security Proof Template

```latex
\begin{theorem}\label{thm:uc-security}
Assuming [setup assumptions] and [cryptographic assumptions], 
Protocol~\ref{prot:uc-protocol} UC-realizes functionality 
$\mathcal{F}$ in the $\mathcal{F}_{\mathsf{crs}}$-hybrid model.
\end{theorem}

\begin{proof}
Let $\mathcal{A}$ be an adversary and $\mathcal{Z}$ be an environment. 
We construct a simulator $\mathcal{S}$ such that no environment can 
distinguish between:
\begin{itemize}
    \item $\mathsf{EXEC}_{\pi, \mathcal{A}, \mathcal{Z}}$: Real execution 
          of protocol $\pi$ with adversary $\mathcal{A}$
    \item $\mathsf{EXEC}_{\mathcal{F}, \mathcal{S}, \mathcal{Z}}$: Ideal 
          execution with functionality $\mathcal{F}$ and simulator 
          $\mathcal{S}$
\end{itemize}

\paragraph{Simulator Construction.}
The simulator $\mathcal{S}$ works as follows:
\begin{enumerate}
    \item \textbf{CRS Generation:} $\mathcal{S}$ generates the CRS with 
          trapdoor: $(crs, \tau) \gets \mathsf{SimCRS}(1^n)$.
    \item \textbf{Simulation of honest parties:} For each honest party 
          $P_i$, $\mathcal{S}$ simulates $P_i$'s messages without 
          knowing $P_i$'s input, using the trapdoor $\tau$.
    \item \textbf{Extraction of corrupted inputs:} When corrupted party 
          sends protocol message, $\mathcal{S}$ extracts input using 
          trapdoor: $x' \gets \mathsf{Extract}(\tau, \mathsf{msg})$.
    \item \textbf{Interaction with ideal functionality:} $\mathcal{S}$ 
          forwards extracted inputs to $\mathcal{F}$ and receives outputs.
    \item \textbf{Equivocation:} $\mathcal{S}$ uses trapdoor to make 
          simulated messages consistent with functionality outputs.
\end{enumerate}

\paragraph{CRS Indistinguishability.}
We first argue that the simulated CRS is indistinguishable from an 
honestly generated CRS:
\[
\{crs : (crs, \tau) \gets \mathsf{SimCRS}(1^n)\} 
\stackrel{c}{\equiv} 
\{crs : crs \gets \mathsf{CRSGen}(1^n)\}
\]
This follows from [assumption about CRS generation].

\paragraph{Simulation Indistinguishability.}
Conditioned on the CRS being indistinguishable, we argue that the 
simulated transcript is indistinguishable from a real transcript.

[Hybrid argument with transitions:]
\begin{enumerate}
    \item Hybrid $H_0$: Real execution with honest CRS
    \item Hybrid $H_1$: Real execution with simulated CRS (indist. by above)
    \item Hybrid $H_2$: Simulated messages with simulated CRS
    \item Hybrid $H_k$: Full simulation (ideal world)
\end{enumerate}

Each transition follows from [relevant assumption].

\paragraph{Environmental Distinguishing.}
Since the environment $\mathcal{Z}$ interacts with the adversary in 
a black-box manner, and the above hybrids are computationally 
indistinguishable, no PPT environment can distinguish real from 
ideal executions with more than negligible advantage.

This completes the proof.
\end{proof}
```

---

## 6. Usage Guidelines

### Adapting Templates

1. **Replace placeholders** (in [brackets]) with protocol-specific details
2. **Adjust hybrid count** based on proof complexity
3. **Specify assumptions** precisely with references
4. **Include formal definitions** of any non-standard notation

### Common Modifications

- For **statistical security**: Replace $\stackrel{c}{\equiv}$ with $\stackrel{s}{\equiv}$ or $\equiv$
- For **adaptive security**: Add state explanation after corruption
- For **multi-party**: Generalize to coalition of corrupted parties
- For **reactive functionalities**: Handle multiple input/output phases

### Citation Conventions

Reference standard definitions:
- Semi-honest security: [Goldreich04, Def. 7.2.1]
- Malicious security: [Goldreich04, Def. 7.2.4]  
- UC security: [Canetti01, Def. 1]
- Commitment schemes: [Goldreich01, Def. 4.4.1]

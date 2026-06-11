# Universal Composability (UC) Framework Reference

## Contents

- [1. Introduction](#1-introduction)
- [2. Theoretical Foundations](#2-theoretical-foundations)
- [3. Key Differences from Stand-Alone Security](#3-key-differences-from-stand-alone-security)
- [4. Impossibility Results](#4-impossibility-results)
- [5. Setup Assumptions](#5-setup-assumptions)
- [6. Composition Theorems](#6-composition-theorems)
- [7. Proving UC Security](#7-proving-uc-security)
- [8. Example: UC Oblivious Transfer](#8-example-uc-oblivious-transfer)
- [9. Simplified UC Framework](#9-simplified-uc-framework)
- [10. Common Mistakes in UC Proofs](#10-common-mistakes-in-uc-proofs)
- [11. References](#11-references)

## 1. Introduction

The Universal Composability (UC) framework, introduced by Canetti [1], provides a rigorous methodology for analyzing cryptographic protocols under arbitrary concurrent composition. This document presents the theoretical foundations, definitional nuances, and proof techniques specific to the UC setting.

## 2. Theoretical Foundations

### 2.1 Motivation for UC Security

The stand-alone model provides security guarantees only when a single protocol instance executes in isolation. In practice, protocols execute concurrently with arbitrary other protocols, potentially controlled by the same adversary. The UC framework addresses this limitation by requiring that protocol security be preserved under arbitrary concurrent composition with other protocols.

**Key insight**: If a protocol UC-realizes a functionality F, then the protocol can be used as a "drop-in replacement" for ideal access to F in any larger system.

### 2.2 The UC Execution Model

The UC framework introduces an **environment** Z that represents all external activities and captures the concurrent composition setting.

```
┌─────────────────────────────────────────────────────────────────┐
│                     REAL WORLD EXECUTION                        │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │                    Environment Z                          │  │
│  │  (provides inputs, reads outputs, interacts with A)       │  │
│  └─────────────────────────────────────────────────────────── │  │
│         │         │         │              ↑                   │
│         ↓         ↓         ↓              │                   │
│     ┌──────┐  ┌──────┐  ┌──────┐    ┌────────────┐            │
│     │  P₁  │  │  P₂  │  │  P₃  │    │ Adversary  │            │
│     │      │◄─┼──────┼─►│      │    │     A      │            │
│     └──────┘  └──────┘  └──────┘    └────────────┘            │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                     IDEAL WORLD EXECUTION                       │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │                    Environment Z                          │  │
│  │  (provides inputs, reads outputs, interacts with S)       │  │
│  └───────────────────────────────────────────────────────────┘  │
│         │         │         │              ↑                   │
│         ↓         ↓         ↓              │                   │
│     ┌──────┐  ┌──────┐  ┌──────┐    ┌────────────┐            │
│     │ P̃₁   │  │ P̃₂   │  │ P̃₃   │    │ Simulator  │            │
│     │(dummy)│  │(dummy)│  │(dummy)│   │     S      │            │
│     └──┬───┘  └──┬───┘  └──┬───┘    └─────┬──────┘            │
│        │         │         │              │                    │
│        └─────────┴─────────┴──────────────┘                    │
│                         │                                      │
│                         ↓                                      │
│              ┌─────────────────────┐                           │
│              │  Ideal Functionality │                          │
│              │         F            │                          │
│              └─────────────────────┘                           │
└─────────────────────────────────────────────────────────────────┘
```

### 2.3 Formal Definition

**Definition 2.1** (UC Realization). Protocol π UC-realizes functionality F if for every adversary A, there exists a simulator S such that for every environment Z:

```
EXEC_{π,A,Z} ≈ EXEC_{F,S,Z}
```

where EXEC denotes the output of Z in the respective execution, and ≈ denotes computational indistinguishability.

**Critical distinction from stand-alone**: The environment Z provides inputs adaptively, receives outputs immediately, and can communicate with the adversary throughout the execution. This prevents the simulator from rewinding Z or A.

---

## 3. Key Differences from Stand-Alone Security

### 3.1 No Rewinding

In stand-alone proofs, the simulator often rewinds the adversary to extract inputs or force specific outputs. In UC:

- **Environment interaction is external**: The simulator cannot control when Z sends inputs or reads outputs
- **Adversary-environment communication**: A may report current state to Z, which would detect rewinding
- **Consequence**: Simulators must work in a "straight-line" manner

### 3.2 Adaptive Input Delivery

In stand-alone proofs, all inputs are provided at the start. In UC:

- **Dynamic inputs**: Z may wait to see partial transcripts before providing remaining inputs
- **Consequence**: Simulator cannot "look ahead" to determine inputs
- **Strategy**: Use equivocal commitments or trapdoor mechanisms

### 3.3 Immediate Output Delivery

In stand-alone proofs, outputs are examined only at the end. In UC:

- **Real-time outputs**: Z receives outputs as soon as protocol delivers them
- **Consequence**: Simulator must ensure output timing matches protocol
- **Strategy**: Delayed output via functionality design (e.g., "delayed output" wrappers)

---

## 4. Impossibility Results

### 4.1 Two-Party UC Commitment

**Theorem 4.1** (Canetti-Fischlin [2]). In the plain model (without setup), there exists no protocol that UC-realizes the commitment functionality F_com.

**Proof Intuition**: The commitment functionality requires:
- Hiding: Simulator for corrupted receiver cannot learn committed value
- Binding: Simulator for corrupted committer cannot equivocate

Without setup, if the simulator can extract/equivocate, so can a real adversary. If the simulator cannot, then simulation fails.

### 4.2 General Two-Party Computation

**Theorem 4.2** (Canetti-Kushilevitz-Lindell [3]). Without honest majority or setup assumptions, UC-secure two-party computation of most functionalities is impossible.

**Affected functionalities include**:
- Commitment
- Zero-knowledge
- Oblivious transfer
- Coin-tossing
- Any functionality with non-trivial output to both parties

---

## 5. Setup Assumptions

### 5.1 Common Reference String (CRS) Model

**Definition 5.1** (CRS Functionality).
```
F_crs:
- On first activation: Sample crs ← D and store it
- On input "CRS" from any party: Return crs
```

**Properties**:
- CRS is generated once, before protocol execution
- All parties receive the same CRS
- Simulator generates CRS with trapdoor in ideal world

**Example constructions**:
- Commitment: crs = public key; trapdoor = secret key
- ZK: crs = CRS for NIZK; trapdoor = simulation trapdoor
- OT: crs = DDH tuple; trapdoor = discrete log

### 5.2 Random Oracle Model

**Definition 5.2** (Random Oracle Functionality).
```
F_ro:
- Maintains table T, initially empty
- On input x: If T[x] undefined, set T[x] ← {0,1}^n
- Return T[x]
```

**In UC setting**: Simulator programs the random oracle in ideal world.

**Caveat**: Random oracle UC security may not imply security with any concrete hash function instantiation [4].

### 5.3 Other Setup Options

- **Public Key Infrastructure (PKI)**: Authenticated public keys
- **Hardware Tokens**: Tamper-proof functionality execution
- **Honest Majority**: At least half of parties are honest

---

## 6. Composition Theorems

### 6.1 Universal Composition Theorem

**Theorem 6.1** (Canetti [1]). Let π be a protocol that UC-realizes F in the G-hybrid model. Let ρ be a protocol that UC-realizes G. Then the composed protocol π^ρ (where calls to G are replaced by executions of ρ) UC-realizes F.

**Significance**: Modular protocol design is sound under UC security.

### 6.2 Implications

1. **Subroutine substitution**: Can replace ideal functionality with any UC-realizing protocol
2. **Concurrent composition**: Multiple instances of π^ρ can run concurrently
3. **Composable building blocks**: OT, commitment, ZK can be used as black boxes

---

## 7. Proving UC Security

### 7.1 Simulator Construction Guidelines

**Step 1: Identify trapdoor mechanism**
- What information does simulator need but honest parties don't have?
- How does setup (CRS) provide this information?

**Step 2: Design extraction strategy**
- How does simulator learn corrupted parties' inputs?
- Must work without rewinding

**Step 3: Design equivocation strategy**
- How does simulator make simulated messages consistent with functionality outputs?
- Must work for adaptively chosen honest party inputs

**Step 4: Handle timing**
- When does functionality deliver outputs?
- Simulator must ensure matching delivery timing

### 7.2 Proof Structure Template

```latex
\begin{proof}
Let $\mathcal{A}$ be any PPT adversary. We construct simulator 
$\mathcal{S}$ such that for all PPT environments $\mathcal{Z}$:

\[
\mathsf{EXEC}_{\pi, \mathcal{A}, \mathcal{Z}} \approx 
\mathsf{EXEC}_{\mathcal{F}, \mathcal{S}, \mathcal{Z}}
\]

\paragraph{Simulator Description.}
[Describe simulator's strategy for each phase]

\paragraph{Indistinguishability.}
We define hybrid experiments:
\begin{itemize}
    \item $H_0$: Real execution with $\mathcal{A}$
    \item $H_1$: [Intermediate hybrid]
    \item $H_k$: Ideal execution with $\mathcal{S}$
\end{itemize}

[For each transition, provide reduction to assumption]
\end{proof}
```

### 7.3 Common Proof Patterns

**Pattern A: Trapdoor CRS**
```
CRS contains (pk, ct) where ct = Enc_pk(0)
Simulator knows sk, can extract from adversary's ciphertexts
Simulator can decrypt ct to learn "fake" plaintext, equivocate
Indistinguishability: IND-CPA security of encryption
```

**Pattern B: Equivocal Commitment**
```
CRS contains commitment parameters
Simulator knows trapdoor allowing equivocation
Real committer cannot equivocate (binding)
Indistinguishability: Hiding property
```

**Pattern C: DDH-based Extraction**
```
CRS contains group elements forming DDH or non-DDH tuple
Simulator generates DDH tuple, knows discrete log relationship
Real protocol uses non-DDH tuple
Indistinguishability: DDH assumption
```

---

## 8. Example: UC Oblivious Transfer

### 8.1 Functionality

```
F_ot:
- On input (send, s_0, s_1) from S:
  Store (s_0, s_1), send "sent" to R
- On input (receive, b) from R:
  If (s_0, s_1) stored: send s_b to R, "delivered" to S
```

### 8.2 Protocol in CRS-Hybrid Model

**CRS**: (G, g, h_0, h_1) where (g, h_0, h_1) is random in G³

**Protocol**:
1. R: Choose r ← Z_q, compute (u, v) = (g^r, h_b^r), send to S
2. S: Compute (e_0, e_1) = (h_0^{r_0} · s_0, h_1^{r_1} · s_1) where r_i ← Z_q
   Send ((u^{r_0}, e_0), (u^{r_1}, e_1)) to R
3. R: Compute s_b = e_b / (u^{r_b})^r

### 8.3 Security Analysis

**Corrupted Sender**:
- Simulator generates CRS with h_0 = g^α, h_1 = g^β (knows α, β)
- Given (u, v) = (g^r, h_b^r), simulator computes:
  - If v = u^α: b = 0
  - If v = u^β: b = 1
- Extraction is perfect (discrete log relationship)

**Corrupted Receiver**:
- Simulator sends simulated messages using random values
- When functionality output s_b arrives, simulator already sent (e_0, e_1)
- Problem: Cannot make e_{1-b} decrypt to arbitrary value

**Resolution**: Use equivocal encryption where simulator can "explain" ciphertext as encryption of any message.

---

## 9. Simplified UC Framework

Canetti, Cohen, and Lindell [5] proposed a simplified UC formulation for standard MPC:

**Key simplifications**:
1. Functionality communicates directly with parties (not through simulator)
2. Environment provides inputs through functionality
3. Removes complexity of "dummy parties"

**Equivalence**: For standard MPC functionalities, simplified UC is equivalent to full UC.

**Benefit**: Proofs become more similar to stand-alone proofs while retaining composability.

---

## 10. Common Mistakes in UC Proofs

### 10.1 Implicit Rewinding

**Mistake**: Simulator "runs adversary twice" to extract, then continues
**Problem**: Environment would observe non-matching states
**Fix**: Use extraction from CRS trapdoor

### 10.2 Ignoring Timing

**Mistake**: Simulator delivers output before protocol would
**Problem**: Environment can distinguish by timing
**Fix**: Match output delivery timing precisely

### 10.3 Non-Polynomial Simulation

**Mistake**: Simulator's strategy depends on environment's strategy
**Problem**: Simulator must work for all environments simultaneously
**Fix**: Ensure simulator is PPT independent of Z

### 10.4 Missing Setup Assumption

**Mistake**: Claim UC security in plain model for functionality known to be impossible
**Problem**: Violates impossibility results
**Fix**: Clearly state setup assumptions (CRS, PKI, etc.)

---

## 11. References

[1] R. Canetti. "Universally Composable Security: A New Paradigm for Cryptographic Protocols." In FOCS, pages 136–145, 2001.

[2] R. Canetti and M. Fischlin. "Universally Composable Commitments." In CRYPTO, pages 19–40, 2001.

[3] R. Canetti, E. Kushilevitz, and Y. Lindell. "On the Limitations of Universal Composable Two-Party Computation Without Set-Up Assumptions." In EUROCRYPT, pages 68–86, 2003.

[4] R. Canetti, O. Goldreich, and S. Halevi. "The Random Oracle Methodology, Revisited." In JACM, 51(4):557–594, 2004.

[5] R. Canetti, A. Cohen, and Y. Lindell. "A Simpler Variant of Universally Composable Security for Standard Multiparty Computation." In CRYPTO, pages 3–22, 2015.

[6] C. Peikert, V. Vaikuntanathan, and B. Waters. "A Framework for Efficient and Composable Oblivious Transfer." In CRYPTO, pages 554–571, 2008.

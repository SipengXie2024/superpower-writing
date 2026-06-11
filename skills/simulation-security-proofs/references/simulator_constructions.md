# Simulator Construction Reference

## Contents

- [1. Semi-Honest Oblivious Transfer Simulator](#1-semi-honest-oblivious-transfer-simulator)
- [2. Zero-Knowledge Simulator (3-Coloring Protocol)](#2-zero-knowledge-simulator-3-coloring-protocol)
- [3. Coin-Tossing Simulator (Blum's Protocol)](#3-coin-tossing-simulator-blums-protocol)
- [4. Oblivious Transfer Simulator (Malicious, Hybrid Model)](#4-oblivious-transfer-simulator-malicious-hybrid-model)
- [5. Common Patterns Summary](#5-common-patterns-summary)

This document provides detailed patterns for constructing simulators in various security proof contexts.

## 1. Semi-Honest Oblivious Transfer Simulator

### Functionality
```
f_OT((b₀, b₁), σ) = (λ, b_σ)
```
Sender P₁ has bits (b₀, b₁), Receiver P₂ has choice bit σ.

### Simulator for Corrupted P₁ (Sender)

**Input to Simulator**: (b₀, b₁), 1ⁿ  
**Output from Functionality**: λ (empty)

```
Simulator S₁(1ⁿ, (b₀, b₁)):
1. Choose uniform random tape r for P₁
2. Compute (α, τ) ← I(1ⁿ; r)                    // Generate trapdoor permutation
3. Sample y₀ ← S(α), y₁ ← S(α)                 // Two random domain elements
4. Output: ((b₀, b₁), r; (y₀, y₁))             // View: input, randomness, messages
```

**Why it works**: Receiver's message (y₀, y₁) distribution is identical whether yσ = F(α, xσ) or both are random samples, by property of enhanced trapdoor permutations.

### Simulator for Corrupted P₂ (Receiver)

**Input to Simulator**: σ, bσ, 1ⁿ

```
Simulator S₂(1ⁿ, σ, bσ):
1. Choose uniform random tape (r₀, r₁) for P₂
2. Generate (α, τ) ← I(1ⁿ)                     // Need trapdoor for this simulation!
3. Compute xσ = S(α; rσ)
4. Compute y₁₋σ = S(α; r₁₋σ)
5. Compute x₁₋σ = F⁻¹(τ, y₁₋σ)                // Use trapdoor to invert
6. Set βσ = B(α, xσ) ⊕ bσ                      // Correct value using known output
7. Set β₁₋σ = B(α, x₁₋σ)                       // Random-looking value
8. Output: (σ, r₀, r₁; α, (β₀, β₁))
```

**Key insight**: Simulator uses trapdoor to compute x₁₋σ, then sets β₁₋σ to the hard-core bit (hiding b₁₋σ by hardcoreness).

---

## 2. Zero-Knowledge Simulator (3-Coloring Protocol)

### Protocol Overview
Prover commits to random coloring, verifier queries edge, prover opens endpoints.
Repeated N = n·|E| times for soundness.

### Simulator Construction

```
Simulator S^{V*(G,z,r,·)}(G):
1. Initialize transcript m̄ = λ
2. For i = 1 to N do:
    a. Set attempt counter j = 1
    b. Choose random edge (vₖ, vₗ) ∈_R E
    c. Set ϕ(vₖ) ∈_R {1,2,3}, ϕ(vₗ) ∈_R {1,2,3}\{ϕ(vₖ)}
    d. For all other vᵢ: set ϕ(vᵢ) = 0
    e. Compute commitments cᵢ = Com(ϕ(vᵢ)) for all i
    f. Query oracle with (m̄, (c₁,...,cₙ)), receive edge e
    g. If e = (vₖ, vₗ):
       - Append ((c₁,...,cₙ), (decom(cₖ), decom(cₗ))) to m̄
       - Continue to next iteration
    h. If e ≠ (vₖ, vₗ):
       - If j < n·|E|: increment j, goto step b (REWIND)
       - Else: output ⊥ (fail)
3. Output whatever V* outputs on transcript m̄
```

### Running Time Analysis

**Claim**: S outputs ⊥ with probability < n·|E|·e⁻ⁿ (negligible).

**Proof**: In each iteration, success probability ≥ 1/|E| - μ(n) by commitment hiding. After n·|E| attempts, failure probability:
```
(1 - 1/|E| + μ(n))^{n·|E|} < (1 - 1/(2|E|))^{n·|E|} < e^{-n/2}
```
By union bound over N iterations: N · e^{-n/2} is negligible.

---

## 3. Coin-Tossing Simulator (Blum's Protocol)

### Functionality
```
f_ct(λ, λ) = (U₁, U₁)
```
Both parties receive the same uniformly random bit.

### Simulator for Corrupted P₂

**P₂ receives**: commitment c, sends b₂, receives decommitment (b₁, r)  
**Simulator input**: 1ⁿ, output bit b

```
Simulator S:
1. Receive b from trusted party
2. Set counter i = 1
3. Choose random b₁ ∈_R {0,1}, r ∈_R {0,1}ⁿ
4. Compute c = Com(b₁; r)
5. Invoke A, hand it c
6. Receive b₂ from A
7. If b₁ ⊕ b₂ = b:
   - Hand (b₁, r) to A
   - Output whatever A outputs
8. If b₁ ⊕ b₂ ≠ b and i < n:
   - Set i = i + 1
   - Goto step 3 (fresh randomness)
9. If i = n: output fail
```

### Correctness Argument

**Key lemma**: Pr[A(Com(b₁)) = b₁ ⊕ b] = 1/2 ± μ(n)

**Proof**: 
```
Pr[A(Com(b₁)) = b₁ ⊕ b] 
= 1/2 · Pr[A(Com(0)) = b] + 1/2 · Pr[A(Com(1)) = 1 ⊕ b]
= 1/2 + 1/2 · (Pr[A(Com(0)) = b] - Pr[A(Com(1)) = b])
= 1/2 ± μ(n)/2
```

By hiding property, |Pr[A(Com(0)) = b] - Pr[A(Com(1)) = b]| ≤ μ(n).

### Simulator for Corrupted P₁

**Key challenge**: A may abort selectively based on output.

```
Simulator S:
1. Receive b from trusted party
2. Invoke A, receive commitment c
3. Hand b₂ = 0 to A, receive response
4. Hand b₂ = 1 to A, receive response
5. Case analysis:
   (a) A decommits validly for BOTH b₂ values:
       - Send "continue" to trusted party
       - Set b₂ = b₁ ⊕ b, hand to A
       - Output whatever A outputs
   (b) A decommits for NEITHER:
       - Send "abort" to trusted party
       - Hand random b₂ to A
       - Output whatever A outputs
   (c) A decommits only when b₁ ⊕ b₂ = b:
       - Send "continue" to trusted party
       - Hand b₂ = b₁ ⊕ b to A
       - Output whatever A outputs
   (d) A decommits only when b₁ ⊕ b₂ ≠ b:
       - Send "abort" to trusted party
       - Hand b₂ = b₁ ⊕ b ⊕ 1 to A
       - Output whatever A outputs
```

**Critical insight**: Cases (c) and (d) handle selective abort. The honest party's output (b or ⊥) matches exactly what would happen in real execution.

---

## 4. Oblivious Transfer Simulator (Malicious, Hybrid Model)

### Setting
Protocol uses f_zk (zero-knowledge functionality) as ideal subroutine.

### Simulator for Corrupted P₁

**Challenge**: Cannot rewind to extract inputs (fails with dependent randomness).

**Solution**: Make CRS a Diffie-Hellman tuple, allowing extraction.

```
Simulator S:
1. Invoke A controlling P₁
2. Generate (g₀, g₁, h₀, h₁) as DH-tuple:
   - g₁ = (g₀)^y, h₀ = (g₀)^α, h₁ = (g₁)^α  // Note: not (g₁)^{α+1}
3. Hand (g₁, h₀, h₁) to A
4. Simulate f_zk: always return 1 (A's statement is irrelevant)
5. Choose random r, set g = (g₀)^r, h = (h₀)^r
6. Hand (g, h) to A
7. Receive (u₀, w₀), (u₁, w₁) from A
8. Extract: x₀ = w₀/(u₀)^r, x₁ = w₁/(u₁)^{r·y^{-1}}
9. Send (x₀, x₁) to trusted party
10. Output whatever A outputs
```

**Why extraction works**: When tuple is DH, the RAND procedure output can be inverted knowing the discrete log relationship.

### Simulator for Corrupted P₂

```
Simulator S:
1. Invoke A
2. Receive (g₁, h₀, h₁) and (statement, witness α) from A's f_zk message
3. Verify: h₀ = (g₀)^α and h₁/g₁ = (g₁)^α
   - If invalid: send "abort", output A's output
4. Receive (g, h) from A
5. Extract σ: If h = g^α then σ = 0, else σ = 1
6. Send σ to trusted party, receive x_σ
7. Compute (u_σ, v_σ) = RAND(g_σ, g, h_σ, h), w_σ = v_σ · x_σ
8. Set (u_{1-σ}, w_{1-σ}) ←_R G²  // Uniform random (by Claim 8.1)
9. Hand ((u₀, w₀), (u₁, w₁)) to A
10. Output whatever A outputs
```

**Key insight**: For the non-chosen bit, RAND output is uniform because tuple is NOT DH.

---

## 5. Common Patterns Summary

### Pattern A: Input Extraction via Trapdoor
- **When**: CRS/setup allows trapdoor
- **How**: Simulator generates CRS with trapdoor, uses trapdoor to extract

### Pattern B: Input Extraction via Rewinding
- **When**: Adversary commits before revealing
- **How**: Run once to learn commitment, rewind and use knowledge

### Pattern C: Output Forcing via Rewinding
- **When**: Output depends on adversary's randomness
- **How**: Repeat until adversary's contribution yields desired output

### Pattern D: Selective Abort Handling
- **When**: Adversary may abort based on output
- **How**: Determine abort pattern, mirror in ideal world

### Pattern E: Hybrid Argument for Replacement
- **When**: Simulated message differs from real
- **How**: Define hybrids, reduce each step to assumption

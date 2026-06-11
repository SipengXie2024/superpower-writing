---
name: game-based-security-proof
description: Use when proving security of encryption schemes, MACs, signatures, PRFs, hash constructions, or other cryptographic primitives, constructing reduction proofs from standard assumptions (DDH, CDH, RSA, LWE), or writing formal game-based security proofs and advantage bounds in academic papers. Covers game sequences and hopping, negligible-advantage arguments, tightness accounting, and turning an informal security claim into a displayed definition, theorem, and proof a reviewer can verify.
---

# Game-Based Security Proof Methodology

## Overview

This skill provides systematic guidance for constructing security proofs using the **sequence-of-games** technique. The methodology transforms complex security arguments into manageable sequences of small, analyzable transitions between games.

**Core Principle:** Security proofs proceed by constructing Game 0 (original attack game), then transforming it through Games 1, 2, ..., n until reaching a game where the target probability is easily computed. Each transition changes only one aspect, making analysis tractable.

## When to Use This Skill

- Proving semantic security (IND-CPA, IND-CCA) of encryption schemes
- Proving unforgeability (EUF-CMA) of signatures/MACs
- Proving pseudorandomness of PRFs/PRPs
- Reducing security to computational assumptions (DDH, CDH, RSA, LWE)
- Writing formal proofs for cryptography papers

## Proof Structure Template

### 1. Setup Phase

Define the attack game (Game 0) precisely:
```
Game 0:
  Challenger computes keys: (pk, sk) ← KeyGen()
  Challenger selects: b ←$ {0,1}
  Adversary A interacts with Challenger (queries, challenges)
  Adversary outputs: b̂
  Define S₀ := event that b = b̂
  Adversary's advantage: |Pr[S₀] - 1/2|
```

### 2. Game Sequence

For each transition Game i → Game i+1, use exactly ONE of three types:

**Type 1: Indistinguishability Transition**
- Make a small change that, if detected, breaks a computational assumption
- Construct distinguisher D that interpolates between games
- Conclude: |Pr[Sᵢ] - Pr[Sᵢ₊₁]| = ε_assumption

**Type 2: Failure Event Transition (Difference Lemma)**
- Games proceed identically unless failure event F occurs
- Ensure: Sᵢ ∧ ¬F ⟺ Sᵢ₊₁ ∧ ¬F
- Apply Difference Lemma: |Pr[Sᵢ] - Pr[Sᵢ₊₁]| ≤ Pr[F]
- Bound Pr[F] (via assumption or information-theoretic argument)

**Type 3: Bridging Step**
- Purely conceptual restatement (e.g., "lazy sampling" / "gnome" technique)
- Pr[Sᵢ] = Pr[Sᵢ₊₁] exactly

### 3. Final Game Analysis

In Game n, show that Pr[Sₙ] equals the target probability (typically 1/2 for encryption, or 0 for unforgeability).

### 4. Advantage Bound

Combine all transitions:
```
Adv[A] = |Pr[S₀] - target| ≤ Σ |Pr[Sᵢ] - Pr[Sᵢ₊₁]| ≤ ε₁ + ε₂ + ... + εₙ
```

## The Difference Lemma

**Lemma (Difference Lemma):** Let A, B, F be events in a probability space. If A ∧ ¬F ⟺ B ∧ ¬F, then |Pr[A] - Pr[B]| ≤ Pr[F].

**Proof sketch:** 
|Pr[A] - Pr[B]| = |Pr[A∧F] + Pr[A∧¬F] - Pr[B∧F] - Pr[B∧¬F]|
               = |Pr[A∧F] - Pr[B∧F]|  (since Pr[A∧¬F] = Pr[B∧¬F])
               ≤ Pr[F]

**Critical practice:** Define games on the **same underlying probability space** so failure event F is literally one event, not corresponding events across spaces.

## Key Techniques

### Lazy Sampling ("Gnome" Technique)

Replace eager random function evaluation with lazy/on-demand sampling:
```
# Eager (conceptual random function f)
y ← f(x)

# Lazy (equivalent "gnome" implementation)
if x ∈ Table then y ← Table[x]
else Y ←$ Range; Table[x] ← Y; y ← Y
```

Use this to bridge between "random function" and explicit table-based computation.

### Forgetful Gnome

After lazy sampling setup, remove consistency checks to create independent random variables:
```
# Faithful gnome (with checks)
if x = xⱼ for some j < i then y ← yⱼ else y ← Yᵢ

# Forgetful gnome (no checks)  
y ← Yᵢ
```

Games differ only when collision occurs (failure event).

### One-Time Pad Argument

When a value h is used only once as h ⊕ m:
- If h is uniformly random and independent of m
- Then h ⊕ m is uniformly random regardless of m
- Adversary learns nothing about which message was encrypted
- Conclude: Pr[b = b̂] = 1/2

## Common Proof Patterns

| Scheme Type | Typical Game Sequence |
|-------------|----------------------|
| Public-key encryption | Game 0 → (DDH/CDH transition) → ... → one-time-pad game |
| PRF security | Game 0 → (replace PRF with random) → lazy sampling → forgetful gnome |
| PRP security | Similar to PRF, bound RF/RP distinguishing advantage |
| CCA encryption | Game 0 → (reject all decryption queries) → semantic security game |
| Random oracle | Game 0 → (program random oracle) → reduction to CDH/other |

## Writing Guidelines

1. **Explicit game descriptions:** Write games algorithmically with clear notation
2. **One change per transition:** Each game should differ minimally from the previous
3. **Label transition types:** State explicitly "[This is a transition based on X]"
4. **Bound immediately:** After each transition, state the bound on probability difference
5. **Same probability space:** Keep all games on the same space when possible

## Reference Files

- **`references/game-transitions.md`**: Detailed explanation of three transition types with examples
- **`references/proof-templates.md`**: Complete proof templates for common schemes
- **`references/latex-macros.md`**: LaTeX macros for writing game-based proofs

## Quick Reference: Notation

| Symbol | Meaning |
|--------|---------|
| x ←$ S | Sample x uniformly from set S |
| A^O() | Adversary A with oracle access to O |
| Pr[E] | Probability of event E |
| negl(λ) | Negligible function in security parameter λ |
| Sᵢ | Success event in Game i |
| F | Failure event |
| ε | Advantage bound (should be negligible) |

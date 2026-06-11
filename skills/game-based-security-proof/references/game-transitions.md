# Game Transition Types: Detailed Reference

## Contents

- [Type 1: Transitions Based on Indistinguishability](#type-1-transitions-based-on-indistinguishability)
- [Type 2: Transitions Based on Failure Events](#type-2-transitions-based-on-failure-events)
- [Type 3: Bridging Steps](#type-3-bridging-steps)
- [Choosing Which Transition Type](#choosing-which-transition-type)
- [Combining Transitions](#combining-transitions)
- [Common Pitfalls](#common-pitfalls)
- [Strategic Considerations](#strategic-considerations)

This document provides comprehensive guidance on the three fundamental transition types used in game-based security proofs, with formal definitions, proof patterns, and annotated examples.

## Type 1: Transitions Based on Indistinguishability

### Definition

An **indistinguishability transition** exploits the assumption that two distributions P₁ and P₂ are computationally (or statistically) indistinguishable. The transition modifies how certain values are computed, replacing sampling from P₁ with sampling from P₂.

### Proof Pattern

**Goal:** Show |Pr[Sᵢ] - Pr[Sᵢ₊₁]| ≤ ε, where ε is the distinguishing advantage.

**Method:**
1. Design Games i and i+1 to differ only in which distribution is used
2. Construct distinguisher D that:
   - Takes input from either P₁ or P₂
   - Simulates the game using this input
   - Outputs 1 iff the success event occurs
3. Observe:
   - When input ~ P₁: D outputs 1 with probability Pr[Sᵢ]
   - When input ~ P₂: D outputs 1 with probability Pr[Sᵢ₊₁]
4. Conclude: D's advantage = |Pr[Sᵢ] - Pr[Sᵢ₊₁]|

### Hybrid Game Technique

For multiple replacements, design a single "hybrid" game parameterized by auxiliary input:
```
Hybrid(aux):
  if aux ~ P₁: behave as Game i
  if aux ~ P₂: behave as Game i+1
```

The distinguisher runs Hybrid with its challenge input and outputs the success indicator.

### Example: DDH-Based Transition (ElGamal)

**Setting:** ElGamal encryption uses (α, β, δ) = (gˣ, gʸ, gˣʸ) to encrypt.

**Game 0:** δ = αʸ = gˣʸ (real encryption)
**Game 1:** δ = gᶻ for random z (random group element)

**Distinguisher D(α, β, δ):**
```
r ←$ R
(m₀, m₁) ← A(r, α)
b ←$ {0,1}
ζ ← δ · m_b
b̂ ← A(r, α, β, ζ)
if b = b̂ then output 1 else output 0
```

**Analysis:**
- If (α, β, δ) = (gˣ, gʸ, gˣʸ): D simulates Game 0, outputs 1 with Pr[S₀]
- If (α, β, δ) = (gˣ, gʸ, gᶻ): D simulates Game 1, outputs 1 with Pr[S₁]
- DDH-Adv(D) = |Pr[S₀] - Pr[S₁]|

### Example: PRF-Based Transition

**Setting:** Replace keyed function F_s with truly random function f.

**Game i:** y ← F_s(x)
**Game i+1:** y ← f(x) where f ←$ Γ_{n,m}

**Distinguisher D^O:**
```
Run adversary A, answering queries using oracle O
Output A's final bit
```

**Analysis:**
- If O = F_s: D simulates Game i
- If O = f: D simulates Game i+1
- PRF-Adv(D) = |Pr[Sᵢ] - Pr[Sᵢ₊₁]|

---

## Type 2: Transitions Based on Failure Events

### Definition

A **failure event transition** shows that two games behave identically unless a specific "bad" event F occurs. This is formalized using the Difference Lemma.

### The Difference Lemma

**Lemma:** Let A, B, F be events defined on a probability space. If A ∧ ¬F ⟺ B ∧ ¬F, then:
```
|Pr[A] - Pr[B]| ≤ Pr[F]
```

**Proof:**
```
|Pr[A] - Pr[B]| 
= |Pr[A ∧ F] + Pr[A ∧ ¬F] - Pr[B ∧ F] - Pr[B ∧ ¬F]|
= |Pr[A ∧ F] - Pr[B ∧ F]|          (since Pr[A ∧ ¬F] = Pr[B ∧ ¬F])
≤ max(Pr[A ∧ F], Pr[B ∧ F])
≤ Pr[F]
```

### Critical Practice: Same Probability Space

**Best practice:** Define both games on the **same underlying probability space** so that:
- Random coins r, keys k, etc. are literally identical in both games
- Event F is one event, not "corresponding" events across spaces
- Comparison Sᵢ ∧ ¬F ⟺ Sᵢ₊₁ ∧ ¬F is straightforward

### Proof Pattern

1. **Design games:** Games i and i+1 differ only in how they handle certain computations
2. **Define failure event F:** Identify the "bad" condition under which games diverge
3. **Prove equivalence:** Show Sᵢ ∧ ¬F ⟺ Sᵢ₊₁ ∧ ¬F
4. **Bound Pr[F]:** Either via:
   - **Security assumption:** If F occurs, adversary breaks some primitive
   - **Information-theoretic:** Birthday bound, union bound, etc.
5. **Apply Difference Lemma:** |Pr[Sᵢ] - Pr[Sᵢ₊₁]| ≤ Pr[F]

### Generalized Difference Lemma

For games on different probability spaces with events A, B, F₁, F₂:

**Lemma:** If Pr[A ∧ ¬F₁] = Pr[B ∧ ¬F₂] and Pr[F₁] = Pr[F₂], then |Pr[A] - Pr[B]| ≤ Pr[F₁].

### Example: Collision Event (Universal Hash)

**Setting:** PRF with hashed input: F'_{k,s}(w) = F_s(H_k(w))

**Game 2:** Faithful gnome checks for collisions in x values
**Game 3:** Forgetful gnome ignores collisions

**Failure Event F:** xᵢ = xⱼ for some i ≠ j (hash collision)

**Games proceed identically unless F:** 
- Without collision: both games compute yᵢ = Yᵢ
- With collision: Game 2 uses cached value, Game 3 uses fresh random

**Bound Pr[F]:**
- By ε_uh-universal hash property: Pr[H_k(wᵢ) = H_k(wⱼ)] ≤ ε_uh for wᵢ ≠ wⱼ
- By union bound over (q choose 2) pairs: Pr[F] ≤ ε_uh · q²/2

### Example: Random Function vs Random Permutation

**Setting:** Distinguish truly random function from truly random permutation.

**Game 1:** Faithful gnome ensures permutation property (no repeated outputs)
**Game 2:** Forgetful gnome allows repeated outputs (random function)

**Failure Event F:** Yᵢ = Yⱼ for some i ≠ j

**Bound Pr[F]:**
- Each Yᵢ ←$ {0,1}ℓ independently
- Pr[Yᵢ = Yⱼ] = 2^{-ℓ}
- By union bound: Pr[F] ≤ (q choose 2) · 2^{-ℓ} ≤ q²/2 · 2^{-ℓ}

### Example: MAC Forgery Failure

**Setting:** CCA-secure encryption where decryption queries are answered.

**Game 0:** Challenger decrypts submitted ciphertexts normally
**Game 1:** Challenger rejects all decryption queries

**Failure Event F:** Adversary submits (x', c', t') with valid MAC: H_k(x'||c') = t'

**Games proceed identically unless F:** If MAC always fails, rejection is correct behavior.

**Bound Pr[F]:** Reduce to MAC unforgeability
- Build adversary B that uses A to forge MAC
- B answers encryption queries using MAC oracle
- B outputs A's successful forgery attempt
- Pr[F] ≤ q' · UF-Adv(B) (union bound over q' decryption queries)

---

## Type 3: Bridging Steps

### Definition

A **bridging step** makes a purely conceptual change that does not alter the probability distribution. It restates computations in an equivalent but more convenient form.

### Purpose

- Prepare for subsequent indistinguishability or failure event transitions
- Make implicit randomness explicit
- Restructure game for clearer analysis

### Key Property

For bridging steps: **Pr[Sᵢ] = Pr[Sᵢ₊₁]** exactly (not approximately).

### Common Bridging Patterns

#### Pattern 1: Lazy Sampling

Convert eager random object sampling to on-demand (lazy) sampling.

**Before (eager):**
```
f ←$ Γ_{n,m}  // Sample entire random function
...
y ← f(x)      // Evaluate
```

**After (lazy):**
```
Y₁, ..., Y_q ←$ {0,1}^m  // Pre-sample potential outputs
...
if x = xⱼ for some j < i then y ← yⱼ else y ← Yᵢ
```

**Why equivalent:** Both produce the same distribution over outputs; a fresh random value for each new input, cached value for repeated inputs.

#### Pattern 2: Pre-sampling Random Coins

Move random sampling to the beginning of the game.

**Before:**
```
for i = 1 to q:
  process query
  y ←$ {0,1}^m
```

**After:**
```
Y₁, ..., Y_q ←$ {0,1}^m  // Pre-sample all randomness
for i = 1 to q:
  process query
  y ← Yᵢ
```

**Why equivalent:** Sampling order doesn't affect distribution when samples are independent.

#### Pattern 3: Explicit Challenger State

Make implicit challenger state explicit.

**Before:**
```
Challenger responds to queries using secret key sk
```

**After:**
```
Challenger maintains explicit table T of query/response pairs
Challenger computes responses using sk and updates T
```

**Why equivalent:** Just makes bookkeeping explicit.

### Example: Random Oracle Bridging

**Setting:** Hash function H modeled as random oracle.

**Game 1:** H is truly random function (conceptual)
**Game 2:** H implemented via lazy sampling with explicit table

```
Game 2:
  Table T ← ∅
  On hash query x:
    if x ∈ T then return T[x]
    else h ←$ {0,1}^ℓ; T[x] ← h; return h
```

**Pr[S₁] = Pr[S₂]** because lazy sampling perfectly simulates a random function.

---

## Choosing Which Transition Type

| Situation | Transition Type |
|-----------|-----------------|
| Replace computational primitive with idealized version | Indistinguishability |
| Remove consistency check that rarely triggers | Failure Event |
| Restate computation equivalently | Bridging Step |
| Reduce to external assumption | Indistinguishability |
| Bound probability of "bad" event | Failure Event |
| Prepare for next transition | Bridging Step |

## Combining Transitions

Complex proofs often combine multiple transition types:

1. **Bridging** to set up lazy sampling
2. **Indistinguishability** to replace PRF with random function  
3. **Bridging** to pre-sample all randomness
4. **Failure event** to remove collision checks
5. Final game has independent random values → easy analysis

## Common Pitfalls

1. **Making two changes at once:** Each transition should change exactly one aspect
2. **Analyzing failure event in wrong game:** Choose the game where analysis is cleanest
3. **Forgetting to verify same probability space:** Explicitly state shared randomness
4. **Loose bounds:** Use tight analysis (avoid unnecessary union bounds)
5. **Circular dependencies:** Ensure failure event analysis doesn't require later game results

## Strategic Considerations

When planning a proof:

1. **Identify the target:** What should the final game look like?
2. **Work backwards:** What transitions are needed to reach it?
3. **Order matters:** Some orderings make analysis easier
4. **Forgetful gnome tip:** Make both gnomes forgetful simultaneously if individual analysis is hard
5. **Hybrid arguments:** For multiple identical replacements, use a single hybrid argument

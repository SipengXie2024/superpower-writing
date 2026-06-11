# Proof Templates for Common Cryptographic Schemes

## Contents

- [Template 1: IND-CPA Security of Public-Key Encryption](#template-1-ind-cpa-security-of-public-key-encryption)
- [Template 2: IND-CCA Security of Public-Key Encryption](#template-2-ind-cca-security-of-public-key-encryption)
- [Template 3: PRF Security](#template-3-prf-security)
- [Template 4: PRF/PRP Switching Lemma](#template-4-prfprp-switching-lemma)
- [Template 5: EUF-CMA Security of MAC/Signature](#template-5-euf-cma-security-of-macsignature)
- [Template 6: Random Oracle Model Proof](#template-6-random-oracle-model-proof)
- [Template 7: Hybrid Argument (Multiple Replacements)](#template-7-hybrid-argument-multiple-replacements)
- [Template 8: Luby-Rackoff (Feistel) Construction](#template-8-luby-rackoff-feistel-construction)
- [Proof Writing Checklist](#proof-writing-checklist)

This document provides complete proof templates for standard security notions. Each template includes the security definition, game sequence structure, and key proof steps.

---

## Template 1: IND-CPA Security of Public-Key Encryption

### Security Definition

A public-key encryption scheme (KeyGen, Enc, Dec) is IND-CPA secure if for all PPT adversaries A:

```
Adv^{IND-CPA}_A(λ) = |Pr[IND-CPA_A(λ) = 1] - 1/2| ≤ negl(λ)
```

where IND-CPA game:
```
IND-CPA_A(λ):
  (pk, sk) ← KeyGen(1^λ)
  (m₀, m₁, state) ← A^{Enc(pk,·)}(pk)    // Phase 1
  b ←$ {0,1}
  c* ← Enc(pk, m_b)
  b' ← A^{Enc(pk,·)}(state, c*)           // Phase 2
  return (b = b')
```

### Proof Template (Reduction to Assumption X)

**Theorem:** If X is hard, then the scheme is IND-CPA secure.

**Proof:** Let A be a PPT adversary with IND-CPA advantage ε. We construct a sequence of games.

**Game 0:** The original IND-CPA game.
- S₀ := event that b = b'
- By definition: Adv^{IND-CPA}_A = |Pr[S₀] - 1/2|

**Game 1:** [Indistinguishability transition based on X]
- Modification: Replace [specific computation] with [idealized version]
- S₁ := event that b = b' in Game 1
- Claim: |Pr[S₀] - Pr[S₁]| ≤ Adv^X_D for some PPT D

*Distinguisher D(challenge):*
```
  (pk, sk) ← KeyGen(1^λ)  [or use challenge to set pk]
  Run A(pk), answer queries normally
  Receive (m₀, m₁) from A
  b ←$ {0,1}
  c* ← [encrypt m_b using challenge]
  b' ← A(c*)
  return (b = b')
```

When challenge is from distribution P₁: D simulates Game 0
When challenge is from distribution P₂: D simulates Game 1
Therefore: Adv^X_D = |Pr[S₀] - Pr[S₁]|

**Game 2 (Final):** [Often: ciphertext independent of b]
- Modification: [Make ciphertext information-theoretically independent of b]
- S₂ := event that b = b' in Game 2
- Claim: Pr[S₂] = 1/2

*Proof:* In Game 2, the ciphertext c* is [random/independent of m_b], hence b and b' are independent.

**Conclusion:**
```
Adv^{IND-CPA}_A = |Pr[S₀] - 1/2| 
               ≤ |Pr[S₀] - Pr[S₁]| + |Pr[S₁] - Pr[S₂]| + |Pr[S₂] - 1/2|
               ≤ Adv^X_D + [additional terms] + 0
               ≤ negl(λ)
```

---

## Template 2: IND-CCA Security of Public-Key Encryption

### Security Definition

IND-CCA adds decryption oracle access (except on challenge ciphertext):

```
IND-CCA_A(λ):
  (pk, sk) ← KeyGen(1^λ)
  (m₀, m₁, state) ← A^{Enc(pk,·), Dec(sk,·)}(pk)
  b ←$ {0,1}
  c* ← Enc(pk, m_b)
  b' ← A^{Enc(pk,·), Dec(sk,·)\{c*}}(state, c*)
  return (b = b')
```

### Proof Template

**Game 0:** Original IND-CCA game.

**Game 1:** [Failure event transition]
- Modification: Reject all decryption queries (return ⊥)
- Failure event F: A submits c' ≠ c* that decrypts validly
- Games identical unless F occurs
- |Pr[S₀] - Pr[S₁]| ≤ Pr[F]

*Bounding Pr[F]:* Reduce to [integrity primitive, e.g., MAC/signature unforgeability]
```
Adversary B^{Sign/MAC}:
  Simulate Game 1 for A
  Use oracle to generate authentication tags
  If A produces valid forgery (c' with valid tag), output it
  Pr[F] ≤ q · Adv^{UF}_B  (union bound over q queries)
```

**Game 2:** [Indistinguishability transition]
- Now that decryption oracle is useless, reduce to IND-CPA or computational assumption
- |Pr[S₁] - Pr[S₂]| ≤ Adv^X

**Game 3 (Final):** Pr[S₃] = 1/2 (ciphertext independent of b)

**Conclusion:**
```
Adv^{IND-CCA}_A ≤ Pr[F] + Adv^X + 0 ≤ q·Adv^{UF} + Adv^X ≤ negl(λ)
```

---

## Template 3: PRF Security

### Security Definition

F: K × X → Y is a PRF if for all PPT distinguishers D:
```
Adv^{PRF}_D = |Pr[D^{F_k}() = 1] - Pr[D^{f}() = 1]| ≤ negl(λ)
```
where k ←$ K and f ←$ Func(X,Y).

### Proof Template (PRF from Assumption)

**Game 0:** D interacts with F_k (real PRF)

**Game 1:** [Indistinguishability based on assumption]
- Replace F_k with construction using random oracle / ideal primitive
- |Pr[S₀] - Pr[S₁]| ≤ Adv^X

**Game 2:** [Bridging: Lazy sampling]
- Implement random function via table lookup
- Pr[S₁] = Pr[S₂] (conceptual change only)

**Game 3:** [Failure event: Remove collision checks]
- Forgetful gnome implementation
- F := collision event (query collision)
- |Pr[S₂] - Pr[S₃]| ≤ Pr[F] ≤ q²/2|X| (birthday bound)

**Analysis of Game 3:** 
- Each query gets independent random response
- This is exactly a random function
- Pr[S₃] = Pr[D^f() = 1]

**Conclusion:**
```
Adv^{PRF}_D ≤ Adv^X + q²/2|X|
```

---

## Template 4: PRF/PRP Switching Lemma

### Lemma Statement

For any distinguisher D making q queries:
```
|Pr[D^{f} = 1] - Pr[D^{π} = 1]| ≤ q²/2·|Y|
```
where f ←$ Func(X,Y) and π ←$ Perm(X) (assuming |X| = |Y|).

### Proof

**Game 0:** D interacts with random permutation π
- S₀ := event D outputs 1

**Game 1:** [Bridging: Lazy sampling for permutation]
```
Y₁, ..., Y_q ←$ Y
For i-th query xᵢ:
  if Yᵢ ∈ {y₁,...,y_{i-1}} then yᵢ ←$ Y \ {y₁,...,y_{i-1}}
  else yᵢ ← Yᵢ
```
- Pr[S₀] = Pr[S₁] (equivalent implementation)

**Game 2:** [Failure event: Forgetful gnome]
```
Y₁, ..., Y_q ←$ Y
For i-th query: yᵢ ← Yᵢ
```
- F := event Yᵢ = Yⱼ for some i ≠ j
- |Pr[S₁] - Pr[S₂]| ≤ Pr[F] ≤ (q choose 2) · |Y|⁻¹ = q²/2·|Y|

**Game 2 Analysis:** Game 2 is exactly random function interaction.

---

## Template 5: EUF-CMA Security of MAC/Signature

### Security Definition

```
EUF-CMA_A(λ):
  k ← KeyGen(1^λ)  [or (pk, sk) for signatures]
  (m*, σ*) ← A^{Sign(k,·)}()
  Q := set of queried messages
  return (Verify(k, m*, σ*) = 1 ∧ m* ∉ Q)
```

### Proof Template

**Game 0:** Original EUF-CMA game.
- S₀ := event A produces valid forgery

**Game 1:** [Typically: Replace PRF with random function]
- |Pr[S₀] - Pr[S₁]| ≤ Adv^{PRF}

**Game 2:** [Information-theoretic analysis]
- With random function, analyze probability of forgery
- Key insight: For fresh message m*, the tag τ* is uniformly random from A's view
- Pr[S₂] ≤ 1/|T| (guessing probability for tag space T)

**Conclusion:**
```
Adv^{EUF-CMA}_A ≤ Adv^{PRF} + 1/|T| ≤ negl(λ)
```

---

## Template 6: Random Oracle Model Proof

### Structure

Random oracle proofs have distinctive features:
1. Hash function H modeled as truly random function
2. Adversary and challenger have oracle access to H
3. Reduction must simulate H for adversary
4. Key technique: "Programming" the random oracle

### Proof Template

**Game 0:** Original security game with random oracle H.

**Game 1:** [Bridging: Explicit H simulation]
- Challenger maintains table T for H
- On query x: if x ∈ T return T[x], else h ←$ {0,1}^ℓ, T[x] ← h, return h
- Pr[S₀] = Pr[S₁]

**Game 2:** [Programming RO at specific point]
- Modification: For challenge-related input x*, set H(x*) = [specific value]
- If A queries x* before challenge: abort (failure event F₁)
- |Pr[S₁] - Pr[S₂]| ≤ Pr[F₁]

**Game 3:** [Indistinguishability based on computational assumption]
- With programmed RO, reduce to CDH/RSA/etc.
- Build reduction that extracts solution from successful A

**Bounding Pr[F₁]:** 
- A makes at most q_H hash queries
- x* involves randomness unknown to A before challenge
- Pr[F₁] ≤ q_H / |domain| (birthday-type bound)

**Extraction Argument:**
- If A succeeds with probability ε
- A must query H on solution-related input (with high probability)
- Reduction extracts computational solution from H queries

---

## Template 7: Hybrid Argument (Multiple Replacements)

### Setting

Need to replace n instances of object O with ideal object O'.

### Standard Approach

**Hybrid Hᵢ:** First i instances are O', remaining (n-i) are O.
- H₀ = all O (original game)
- Hₙ = all O' (target game)

**Single-step Reduction:**
```
Distinguisher D^{oracle}:
  j ←$ {1, ..., n}
  Simulate hybrid using:
    - O' for instances 1, ..., j-1
    - oracle for instance j
    - O for instances j+1, ..., n
  Return success indicator
```

**Analysis:**
- If oracle = O: D simulates H_{j-1}
- If oracle = O': D simulates H_j
- Adv_D = (1/n) · Σᵢ |Pr[Sᵢ₋₁] - Pr[Sᵢ]| ≥ (1/n) · |Pr[S₀] - Pr[Sₙ]|

**Conclusion:**
```
|Pr[S₀] - Pr[Sₙ]| ≤ n · Adv_D
```

### Tighter Hybrid (for independent instances)

If instances are independent, can sometimes avoid factor of n loss:
```
D^{oracle₁, ..., oracleₙ}:
  Use oracleᵢ for instance i
  Return success indicator
```

---

## Template 8: Luby-Rackoff (Feistel) Construction

### Setting

Build PRP from PRF using 3-round Feistel:
```
Round 1: w = u ⊕ H_k(v)
Round 2: x = v ⊕ F_{s₁}(w)  
Round 3: y = w ⊕ F_{s₂}(x)
Output: (x, y)
```

### Proof Structure

**Game 0:** Real construction with PRF keys s₁, s₂.

**Game 1:** [Indist.] Replace F_{s₁} with random f₁.
- Use faithful gnome for f₁
- |Pr[S₀] - Pr[S₁]| ≤ Adv^{PRF}

**Game 2:** [Indist.] Replace F_{s₂} with random f₂.
- Use faithful gnome for f₂  
- |Pr[S₁] - Pr[S₂]| ≤ Adv^{PRF}

**Game 3:** [Failure event] Make both gnomes forgetful.
- F₁ := collision in w values
- F₂ := collision in x values
- |Pr[S₂] - Pr[S₃]| ≤ Pr[F₁] + Pr[F₂]

**Key Insight for Bounding F₁:**
- Collision wᵢ = wⱼ requires uᵢ ⊕ H_k(vᵢ) = uⱼ ⊕ H_k(vⱼ)
- If vᵢ ≠ vⱼ: by AXU property, Pr ≤ ε_{AXU}
- If vᵢ = vⱼ: then uᵢ ≠ uⱼ (distinct queries), so wᵢ ≠ wⱼ
- Pr[F₁] ≤ (q choose 2) · ε_{AXU}

**Bounding F₂:**
- In Game 3, x values are independent random (since w values are distinct and f₁ is random)
- Pr[F₂] ≤ (q choose 2) · 2^{-ℓ}

**Final Game Analysis:**
- With independent random x and y values, output distribution is random function
- Apply PRF/PRP switching lemma to get PRP security

---

## Proof Writing Checklist

Before finalizing a proof:

- [ ] Game 0 matches the security definition exactly
- [ ] Each transition is clearly labeled with its type
- [ ] Distinguishers/reductions are explicitly constructed
- [ ] Probability bounds are stated immediately after each transition
- [ ] Final game probability is computed
- [ ] All bounds are combined correctly
- [ ] Result states the form: Adv ≤ [sum of terms] ≤ negl(λ)
- [ ] Each negligible term is justified (assumption or parameter choice)

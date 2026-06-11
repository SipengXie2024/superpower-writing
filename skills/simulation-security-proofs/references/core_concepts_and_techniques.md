# Core Concepts and Proof Techniques

## Contents

- [Computational Indistinguishability](#computational-indistinguishability)
- [The Ideal/Real Paradigm](#the-idealreal-paradigm)
- [Adversary Models](#adversary-models)
- [Proof Techniques](#proof-techniques)
- [Common Pitfalls and Solutions](#common-pitfalls-and-solutions)
- [Special Models](#special-models)
- [Checklist for Security Proofs](#checklist-for-security-proofs)

## Computational Indistinguishability

Two probability ensembles X = {X(a,n)} and Y = {Y(a,n)} are computationally indistinguishable (denoted X =^c Y) if for every non-uniform polynomial-time distinguisher D, there exists a negligible function mu(.) such that:

```
|Pr[D(X(a,n), a) = 1] - Pr[D(Y(a,n), a) = 1]| <= mu(n)
```

**Key insight**: The distinguisher receives the auxiliary input `a`, making this inherently non-uniform. This is crucial for reductions.

## The Ideal/Real Paradigm

```
+---------------------------------------------------------------+
|                        REAL WORLD                              |
|  +---------+                              +---------+          |
|  | Party 1 | <---- Protocol Messages ---->| Party 2 |          |
|  |  (x)    |                              |  (y)    |          |
|  +---------+                              +---------+          |
|       |                                        |               |
|       v                                        v               |
|   output_1                    Adversary A   output_2           |
+---------------------------------------------------------------+

+---------------------------------------------------------------+
|                        IDEAL WORLD                             |
|  +---------+      +---------------+      +---------+           |
|  | Party 1 | -->  | Trusted Party |  <-- | Party 2 |           |
|  |  (x)    |      |   f(x,y)      |      |  (y)    |           |
|  +---------+      +---------------+      +---------+           |
|       |                  |                    |                |
|       v                  v                    v                |
|   f_1(x,y)        Simulator S            f_2(x,y)             |
+---------------------------------------------------------------+
```

**Security Requirement**: For every real-world adversary A, there exists an ideal-world simulator S such that:

```
{ideal_{f,S(z),i}(x,y,n)} =^c {real_{pi,A(z),i}(x,y,n)}
```

---

## Adversary Models

### Semi-Honest (Passive) Adversaries

Semi-honest adversaries follow the protocol specification exactly but attempt to learn additional information from the transcript.

**Definition (Semi-Honest Security)**: Protocol pi securely computes f if there exist PPT simulators S_1, S_2 such that:

```
{(S_1(1^n, x, f_1(x,y)), f(x,y))} =^c {(view_1^pi(x,y,n), output^pi(x,y,n))}
{(S_2(1^n, y, f_2(x,y)), f(x,y))} =^c {(view_2^pi(x,y,n), output^pi(x,y,n))}
```

**Key properties**:
- Simulator receives party's input AND output
- No rewinding needed (adversary behavior is deterministic given input)
- View must be consistent with prescribed output
- Joint distribution must be considered for randomized functionalities

**Simulation Strategy**:
1. Choose uniform random tape for the corrupted party
2. Generate protocol messages using the output (not necessarily the real computation)
3. Ensure the view produces the correct output when protocol instructions are applied

### Malicious (Active) Adversaries

Malicious adversaries may deviate arbitrarily from the protocol specification.

**Definition (Malicious Security with Abort)**: Protocol pi securely computes f with abort if for every PPT adversary A, there exists PPT simulator S such that:

```
{ideal_{f,S(z),i}(x,y,n)} =^c {real_{pi,A(z),i}(x,y,n)}
```

**Ideal-world execution phases**:
1. **Send inputs to trusted party**: Corrupted party may send modified input x'
2. **Early abort option**: Adversary may abort before computation
3. **Receive output**: Adversary receives its output first
4. **Continue or halt**: Adversary decides whether honest party receives output

**Key challenges**:
- Must extract adversary's effective input
- Must handle arbitrary adversary behavior
- May require rewinding techniques
- Must preserve abort probabilities

---

## Proof Techniques

### Technique 1: The Hybrid Argument

Bridge between real and ideal worlds through intermediate distributions.

```
Real World =^c Hybrid_1 =^c Hybrid_2 =^c ... =^c Ideal World
```

**Application**: Each hybrid changes one aspect:
- Replace commitment with commitment to different value
- Replace real message with simulated message
- Replace real randomness with pseudorandom values

**Proof strategy**:
1. Define sequence of hybrid experiments
2. Show adjacent hybrids are indistinguishable
3. Reduce distinguishing advantage to breaking cryptographic assumption

See `references/hybrid_arguments.md` for detailed treatment.

### Technique 2: Rewinding

Used when simulator must "learn" information before generating the view.

**Common scenarios**:
- Zero-knowledge: Guess verifier's challenge, rewind if wrong
- Input extraction: Run adversary twice with different challenges
- Commitment extraction: Rewind to obtain both openings

**Running time considerations**:
- Expected polynomial time often sufficient for constant-round protocols
- Strict polynomial time requires careful analysis
- Goldreich-Kahan technique: Estimate success probability, bound retry attempts

**Warning**: Negligible differences in success probabilities can cause exponential blowup:
```
Expected time = poly(n) * (1 - eps(n) + eps(n) * 1/(eps(n) - mu(n)))
```
When mu(n) ~ eps(n), this can become exponential.

### Technique 3: The Hybrid Model

Prove security assuming ideal functionalities, then compose.

**Methodology**:
1. Design protocol pi using ideal functionality g as subroutine
2. Prove pi secure in g-hybrid model (trusted party computes g)
3. Apply composition theorem: if rho securely computes g, then pi^rho is secure

**Benefits**:
- Modular proof structure
- Simulator receives adversary's inputs to subroutine directly
- No extraction needed for subprotocol inputs
- Perfect simulation of subroutine outputs

### Technique 4: Reduction to Cryptographic Assumptions

Every non-trivially true claim requires a reduction.

**Template**:
```
Assume protocol is insecure.
Then there exists distinguisher D, polynomial p(.)
such that D distinguishes real from ideal with probability >= 1/p(n).

Construct adversary A that:
1. Receives challenge from assumption (e.g., DDH tuple)
2. Embeds challenge in protocol execution
3. Uses D to solve the assumption problem

Conclude: If assumption holds, protocol is secure.
```

---

## Common Pitfalls and Solutions

### Pitfall 1: Forgetting Joint Distribution
**Wrong**: Show view is indistinguishable from real view (separately)
**Right**: Show (view, output) jointly indistinguishable
**Why it matters**: For randomized functionalities, parties may receive correlated outputs.

### Pitfall 2: Ignoring Negligible Differences in Running Time
**Problem**: When success probability eps(n) is close to negligible mu(n), rewinding attempts may explode.
**Solution**: Estimate eps(n) before main simulation; bound attempts to n/eps_hat; repeat bounded attempts n times independently.

### Pitfall 3: Missing Reduction
**Problem**: Claiming simulator runs in polynomial time without proof.
**Solution**: Every claim about simulator behavior that wouldn't hold against unbounded adversary requires reduction.

### Pitfall 4: Incorrect Simulation Order
**Problem**: Simulator generates values in wrong order, creating impossible dependencies.
**Solution**: Carefully track what information is available at each simulation step. Draw dependency graph.

### Pitfall 5: Ignoring Abort Probability
**Problem**: Simulator aborts with different probability than real execution.
**Solution**: Case analysis based on adversary abort patterns; ensure simulator abort probability matches real execution.

---

## Special Models

### Common Reference String (CRS) Model
- **Setup**: Trusted party generates CRS = M(1^n), given to all parties.
- **Simulator power**: S chooses CRS (must be indistinguishable from honest CRS).
- **Warning**: Single CRS doesn't compose via standard sequential composition theorem.

### Random Oracle Model
- Replace hash H with random function O.
- Options: No access, non-programmable, programmable (simulator controls oracle).
- UC approach: Model as ideal functionality computing random function.

### Adaptive Security
- **Erasures model**: Parties may securely erase data, simulator need only explain current state.
- **No-erasures model**: Adversary obtains entire view, simulator must generate "non-committing" transcript.

---

## Checklist for Security Proofs

### Before Writing
- [ ] Clearly define the functionality f
- [ ] Specify adversary model (semi-honest/malicious, static/adaptive)
- [ ] Identify all cryptographic assumptions needed
- [ ] Determine if hybrid model is appropriate

### Simulator Construction
- [ ] Handle all corrupted party cases
- [ ] Identify what simulator learns at each step
- [ ] Specify extraction mechanism for adversary inputs
- [ ] Describe abort/continue decisions
- [ ] Verify simulator is polynomial time

### Indistinguishability Proof
- [ ] Consider JOINT distribution (view, output)
- [ ] Define hybrid sequence if needed
- [ ] Provide explicit reduction for each computational claim
- [ ] Address running time with negligible probability analysis
- [ ] Handle all abort cases with matching probabilities

### Final Verification
- [ ] Correctness: honest parties get correct output
- [ ] Privacy: each party learns only its prescribed output
- [ ] Input independence: corrupted party's input is fixed before seeing honest input
- [ ] Abort handling: matches ideal-world abort semantics

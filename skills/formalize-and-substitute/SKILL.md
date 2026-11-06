---
name: formalize-and-substitute
description: Designs or improves a cryptographic construction by equations instead of recall. States the required behaviour as equations, derives the canonical form with its premises, substitutes it into each candidate scheme's requirement, reads off algebraic, security and instantiation conditions, then checks sources and novelty. Use when thinking about any cryptographic innovation, such as a new accumulator, commitment, hash, authenticated structure or protocol component, adding a property, or combining schemes (密码学创新, 微创新, 形式化, 能不能做成抗量子).
---

# Formalize and substitute

A way to make small, checkable design moves on cryptographic constructions,
taken from an exploration of homomorphic aggregators (worked example:
`references/worked-example-accumulator.md`). The workflow replaces "design a
better X" with a chain of equations:

1. write what the object must do as functional equations;
2. derive the canonical form every such object must have, with its premises;
3. for each candidate scheme, write the scheme's requirement equation and
   substitute the canonical form into it;
4. read off what is left: the residual algebraic, security and instantiation
   conditions;
5. search for constructions that meet exactly those conditions;
6. compare the result with the literature and state the increment.

**Why it works.** Asked to "design a better accumulator", a model recalls a
construction and dresses it up. Asked to substitute a canonical form into a
requirement equation, it has to produce conditions, and conditions can be
checked: against the equation they came from, against a brute-force script,
and against the sources. The same discipline exposes the two usual failures:
forcing an additive form onto an object that does not have one, and reporting
a re-derived known construction as new.

**Scope.** Steps 1 and 2 apply when the object has an update or aggregation
law (digests, accumulators, commitments, authenticated trees, incremental
hashes). For a design question without such a law, for example a new
property of a signature or protocol, start at step 3: write the requirement
as an equation, then continue with steps 4 to 6.

Talk to the user in their language. Define every symbol in plain words the
first time it appears and say why it is there.

## Step 1. Write the object as equations

- Name the state, the digest and the operations. State: slots `x_1..x_n`
  (positions matter) or a set or multiset (positions do not). Digest: `r`.
  Operations: slot update, insert, delete, merge, whatever the user named.
- Write each operation as an equation of the form
  `r(state after) = r(state before) ⊕ (something)` and say what the
  "something" is allowed to depend on. That dependency list is where the real
  design choice sits.
- Fix the domains: what set the slot values live in, what group the digest
  lives in (`Z_q^k` with addition, a prime-order group with multiplication,
  bit strings with XOR).
- Choose the view. **Slot-indexed**: each position has its own `f_i`.
  **Multiset, multiplicity view**: one slot per universe element `e`, holding
  its count `c_e`. **Multiset, value view**: slots hold elements and all slots
  share one `f`. Candidate schemes later differ on which view they need.

Output: an equation block with every symbol defined. Check: each operation
the user named has an equation; no symbol is used before it is defined.

## Step 2. Derive the canonical form and name its premises

The additive canonical form is `r(x_1..x_n) = r(0) + Σ_i f_i(x_i)` with
`f_i(t) = r(t·e_i) − r(0)` (write `⊕` and inverses when the group is
multiplicative or XOR). It holds exactly when these premises hold. List each
one and say whether the object satisfies it:

- **P1 separability (the only load-bearing premise).** The change of `r`
  when slot `i` moves from `t` to `t+δ` depends only on `(i, t, δ)`, never on
  another slot. Write it as `r(x + δ·e_i) = r(x) ⊕ g_i(x_i, δ)`.
- **P2 reachability.** Every slot value is reachable from `0` by one
  update, so `δ` ranges over the whole slot domain.
- **P3 abelian digest group.** Updates commute, so update order cannot
  change `r`.

Derivation, for the report: walk from the zero state one slot at a time;
P1 makes each step's increment `g_i(0, x_i)` regardless of the slots already
filled.

Two items look like premises and are not; label them correctly:

- `r(0) = 0` is a **normalization**: absorb `r(0)` as a constant.
- `g_i(t,δ) = f_i(t+δ) − f_i(t)` (the cocycle condition) is a
  **consequence**: once `f_i` is fixed, the update rule is fixed too. Check it
  rather than assume it.

When P1 fails, the output is "no additive canonical form", the premise that
fails, and a counterexample. A Merkle root fails P1: the change at one leaf
depends on its sibling. Do not proceed to step 3 with an additive form the
object does not have; either change the object (that may be the innovation)
or work with the equations it does satisfy.

**Run the checker** on a toy instance of the object before moving on:

```bash
python3 <skill-dir>/scripts/check_separable.py --list
python3 <skill-dir>/scripts/check_separable.py --example merkle      # exits 1 at P1
python3 <skill-dir>/scripts/check_separable.py /tmp/my_model.py      # your object
```

A model file defines `Q` (slot modulus), `N` (slots), `GROUP` (`"add:<m>"`,
`"mul:<p>"` or `"xor"`) and `r(x)` returning an int or a tuple of ints. The
script enumerates every state and update, exits 0 when P1, the canonical form
and the cocycle hold, exits 1 with two concrete states when they do not, and
reports whether the slots share one `f` (value view) and whether
`f_i(t) = t·f_i(1)` (multiplicity view). Keep the toy small
(`Q^N·N·Q ≤ 5·10^6`) and write model files outside any repository. Paste the
script's output into the report. Without a shell, state the toy instance the
script would check and give the counterexample, or the P1 argument, by hand.

Known lineage, to cite rather than rediscover: the slot-indexed canonical
form is the randomize-then-combine paradigm of Bellare and Micciancio
(EUROCRYPT 1997, §1.2: `y_i = h(⟨i⟩ : x_i)` combined in a group); collision
resistance reduces to the balance problem in the group (§2.4). Multiset
hashes (Clarke et al., ASIACRYPT 2003; LtHash) are the multiplicity view.
What the derivation adds is necessity: every aggregator satisfying P1–P3 has
this form.

## Step 3. Write each candidate scheme's requirement equation

For every target scheme (a commitment that must update in constant time, an
authenticated tree whose labels must be additive, an accumulator with
membership witnesses, a proof system that must verify an update), write the
property the scheme needs as an equation in which `r` or the `f_i` appear,
then substitute the canonical form.

Example shapes:

- commitment updated in place: `Com(F′) = Com(F) ⊕ U(δ, k)`, `U`
  computable without `F`;
- authenticated tree with additive parent labels: `G(s) = H(u_1, u_2, …)`
  with `s = Σ_i f_i(x_i)`;
- witness update: `w′ = w ⊕ V(δ, i, j)` for the witness of slot `j` after
  slot `i` changes.

Output: for each scheme, the equation before and after substitution.

## Step 4. Read off the residual conditions

What the substituted equation still demands falls into three kinds. Fill a
table with one row per condition:

| Condition | Kind | Comes from (which equation) | Needed? |

- **Algebraic**: a homomorphism (`Com(a+b) = Com(a) ⊕ Com(b)`), linearity of
  a projection, closure of the reachable set.
- **Security, written as a reduction**: "an adversary that finds X yields a
  collision of `h`" or "… solves the balance problem / SIS / discrete log in
  G". A condition with no named hard problem is not finished. When the user
  wants the reduction written out as a proof, hand it to
  `superpower-writing:game-based-security-proof` (or
  `superpower-writing:simulation-security-proofs` for protocol-level
  security).
- **Instantiation**: whether domain and range match (a lattice hash takes
  short vectors and outputs `Z_q` vectors); which basis the scheme is linear
  in (in the evaluation basis a slot update touches one block; in the
  monomial basis it touches every coefficient); norm bounds and whether
  repeated updates push values out of the bound; modulus and field sizes;
  trusted setup or trapdoor; whether the assumption survives a quantum
  adversary.

Split every bound into its two roles. **Soundness** uses the bound the
verifier actually checks, so it holds whatever the data. **Completeness**
needs honest data to pass that check. That second role often rests on a
statistical assumption, such as "digits are zero-mean and uncorrelated" or
"values are independent of the public parameters". Write that assumption
down as its own row and ask whether the users who choose the data could
break it on purpose. Breaking it does not forge anything, but honest proofs
then fail the check.

Then test each condition for necessity: delete it and ask whether the
reduction still goes through. The worked example has the standard case: the
authenticated tree does not need `G` to be injective, only `h` to be
collision resistant. Mark conditions that turn out unnecessary as such; a
weaker condition set is often the micro-innovation.

## Step 5. Find constructions that meet the conditions

- For each row set from step 4, list candidate constructions and check each
  against every row. A candidate that fails one row is reported with that row
  named.
- Every candidate carries a source: a full-text location (section, theorem,
  page or line range), a DOI or a URL. Never invent a paper, venue, parameter
  or number. A construction recalled without a source at hand is tagged
  `[UNVERIFIED]` until the source is read.
- Read sources in full text. If the project keeps a local full-text library,
  search it first (`rg`, then bounded line ranges). Otherwise use
  `superpower-writing:literature` to find the paper and the `citations`
  skill's `scripts/fetch_fulltext.py` to get its text. Survey pages and
  wiki summaries are pointers, not evidence.

## Step 6. Check novelty and tag provenance

This step is required, because the workflow reliably re-derives known
constructions: in the worked example the authenticated tree it reached is the
generalized hash tree of SADS (Papamanthou, Shi, Tamassia, Yi, EUROCRYPT
2013).

- Compare the result with the closest existing constructions. For a
  per-claim verdict, run the novelty phase of `superpower-writing:idea` on
  the claims this workflow produced. Frequent landing points for digests,
  accumulators and authenticated trees: Bellare–Micciancio 1997
  (randomize-then-combine, MuHASH, AdHASH, LtHASH, the balance problem);
  Clarke et al. 2003 (multiset hashes); Lewi et al. 2019 (LtHash as
  deployed); SADS 2013 and its CCSW 2014 abstraction with a ring instance
  (generalized hash trees with additive labels, and the accumulator built
  from them).
- State the increment in one sentence and classify it: new problem, new
  combination, new instantiation or parameters, weaker conditions, or none.
  When it is none, write "existing construction: <source with section>" and
  stop presenting it as a design.
- Tag every step of the report with where it came from: **derived** (follows
  from the equations above it), **read** (from a source, with its location),
  **recalled** (from memory; `[UNVERIFIED]` until read). In a Chinese report
  use 推导 / 文献 / 回忆. Mark unsupported claims `[NEEDS-EVIDENCE]`.

## Report format

```
## Object and equations        (step 1, symbols defined)
## Canonical form              (premises P1–P3 each judged; checker output)
## Requirement equations       (before and after substitution, one per scheme)
## Residual conditions         (table: condition | kind | source equation | needed?)
## Candidate constructions     (each checked against every row, each with a source)
## Novelty and increment       (closest existing construction, increment or "existing")
```

Each section carries its provenance tags. If P1 fails, the report stops after
the canonical-form section with the counterexample and the choices left
(change the object, or work with the equations it does satisfy).

## When to read the worked example

Read `references/worked-example-accumulator.md` before the first use in a
session, and whenever the object is an accumulator, a function or vector
commitment, or an authenticated tree. It carries the original equations
verbatim, both branches (function commitment and authenticated tree), the
SADS mapping, and the basis and norm conditions that decide whether an
additively homomorphic lattice commitment stays updatable.

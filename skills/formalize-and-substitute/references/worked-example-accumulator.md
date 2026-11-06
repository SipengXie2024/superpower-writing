# Worked example: homomorphic aggregator → function commitment and authenticated tree

## Contents

- [Source and labels](#source-and-labels)
- [Steps 1–2: the object and its canonical form](#steps-12-the-object-and-its-canonical-form)
- [Branch 1: function commitment](#branch-1-function-commitment)
- [Branch 2: authenticated tree](#branch-2-authenticated-tree)
- [Novelty verdict and where an increment would sit](#novelty-verdict-and-where-an-increment-would-sit)

## Source and labels

This example retells an exploration of homomorphic aggregators made while
improving an LtHash-style accumulator. Its equations are quoted verbatim
from the explorer's notes, in Chinese. The original derivation record is not
available, so which steps were derived and which were recalled is
reconstructed here (judgment).

Labels used below: **derived** (follows from the equations), **read** (from
the cited paper, with its location), **inference**, **judgment**,
`[NEEDS-EVIDENCE]`.

Papers cited:
- Bellare–Micciancio, "A New Paradigm for Collision-free Hashing:
  Incrementality at Reduced Cost", EUROCRYPT 1997;
- Clarke et al., "Incremental Multiset Hash Functions and Their Application
  to Memory Integrity Checking", ASIACRYPT 2003;
- Papamanthou, Shi, Tamassia, Yi, "Streaming Authenticated Data Structures"
  (SADS), EUROCRYPT 2013;
- Qian, Zhang, Chen, Papamanthou, "Streaming Authenticated Data Structures:
  Abstraction and Implementation", CCSW 2014.

## Steps 1–2: the object and its canonical form

The equations, verbatim:

```
槽位更新：r(x_1,x_2+δ)=r(x_1,x_2)+g_2(x_2,δ)
从零开始: r(x_1,x_2)=g_1(0,x_1)+g_2(0,x_2)
规范化定义：f_i(t)=g_i(0,t)
形式化结论：r(x_1,…,x_n)=Σ_{i=1}^n f_i(x_i)
```

The four lines are: slot update, start from zero, normalized definition,
formal conclusion. Symbols:
- `x_i` is the value held in slot `i`;
- `δ` is the change applied to one slot;
- `r` is the digest;
- `g_i(t, δ)` is how much the digest changes when slot `i` goes from `t` to
  `t+δ`;
- `f_i(t)` is the contribution of slot `i` when it holds `t`.

What the workflow makes explicit:

- **P1, the load-bearing premise.** `g_2` takes `(x_2, δ)` and nothing else,
  so the change of the digest never reads `x_1`. The slot-update line says
  exactly this one restriction and nothing more.
- **The derivation (derived)** walks from the zero state one slot at a time:
  `r(x_1,x_2) = r(0,0) + [r(x_1,0) − r(0,0)] + [r(x_1,x_2) − r(x_1,0)]
  = r(0,0) + g_1(0,x_1) + g_2(0,x_2)`. The second bracket equals
  `g_2(0,x_2)` only because of P1. The start-from-zero line silently uses two
  more facts:
  - `r(0,0) = 0`, a normalization: absorb the constant;
  - reachability: `x_1 = 0 + x_1` is one legal update.
- **Consequence (derived).** `g_i(t,δ) = f_i(t+δ) − f_i(t)`. Once `f_i` is
  fixed, the update rule is no longer a free design choice.
- **Lineage (read).** The canonical form is the randomize-then-combine
  paradigm of Bellare and Micciancio (§1.2): each block `x_i` is mapped to
  `y_i = h(⟨i⟩ : x_i)`, and the `y_i` are combined with a group operation.
  That is the slot-indexed shape, `f_i(t) = h(⟨i⟩:t)`.
  - Set and multiset hashes (Clarke et al. 2003; LtHash as deployed) hash
    the element itself, `r(S) = Σ_{x∈S} h(x)`. This is the same form read in
    the multiplicity view: slot `e` holds the count `c_e`, and
    `f_e(c) = c·h(e)`.
  - What the derivation adds is the converse: every aggregator whose slot
    updates satisfy P1 must have this shape.
- **Script.** `check_separable.py --example randomize-combine` passes.
  `--example merkle` fails at P1 and prints a concrete pair of states.

## Branch 1: function commitment

The explorer's text, verbatim:

```
F(t)=Σ_{i=1}^N v_i E_{k_i}(t),  F(k_j)=v_j,  F′(t)=F(t)+(v′−v)E_k(t)
但发现这一方案没法很快的在 update 之后迅速出一个抗量子的新承诺（无论是 legirito
还是做一些加法同态的承诺，其实加法同态的承诺应该是可以的）
```

In English, the remark reads: "after an update, this scheme cannot quickly
produce a new post-quantum commitment (neither with Ligerito nor with some
additively homomorphic commitment; actually an additively homomorphic
commitment should work)". `legirito` is Ligerito.

`E_k` is read as the basis polynomial with `E_k(k_j) = 1` when `k = k_j` and
`0` otherwise (inference: the notes do not define `E`). Then `F` is the
canonical form with `f_i(v) = v·E_{k_i}`, which is slot-indexed and linear in
the slot value.

Requirement equation (step 3): a commitment `Com` must satisfy
`Com(F′) = Com(F) ⊕ U(v′−v, k)`, where `U` is computable without knowing
`F`. Substituting the canonical form, `Com(Σ_i v_i E_{k_i})` must itself
split into per-slot terms. So `Com` is additively homomorphic on the space
of reachable `F`, and `U(δ, k) = Com(δ·E_k)`.

Residual conditions (step 4):

| Condition | Kind | Comes from |
| --- | --- | --- |
| `Com(a+b) = Com(a) ⊕ Com(b)` on every reachable `F` | algebraic | the requirement equation |
| two openings of one commitment ⇒ a solution to a named hard problem | security (reduction) | binding |
| an opening proof for `F(k_j) = v_j` | separate requirement equation | `F(k_j)=v_j` |
| the hard problem survives quantum attack | security | the post-quantum requirement |
| `Com` is linear in the evaluation table, so one slot update touches one block | instantiation | the basis discussion below |
| the committed vector stays inside the domain where binding holds | instantiation | the lattice case below |

The remark "an additively homomorphic commitment should work" holds under
one condition: the commitment must be linear in the **evaluation table**
`(v_1, …, v_N)`, not in the monomial coefficients of `F`.

- **Why the basis matters (derived).** In the evaluation (Lagrange) basis a
  slot update touches one coordinate. In the monomial basis,
  `F′ = F + (v′−v)E_k` changes every coefficient, because `E_k` has full
  support.
- **Multilinear extensions fit directly (derived).** The multilinear
  extension of a table on `{0,1}^ℓ` is `F̃(x) = Σ_b v_b·eq(b, x)`, and
  `eq(b, ·)` plays the role of `E_k`. So `f_b(v) = v·eq(b, ·)`, and any
  commitment that is linear in the table satisfies
  `Com(F̃′) = Com(F̃) + (v′−v)·Com(eq_b)`.
  - Hyrax-style (Pedersen) and multilinear-KZG commitments are of this kind
    `[UNVERIFIED]`.
  - They rest on discrete log or pairings, so they fail the post-quantum row.
- **Hash-based commitments fail P1 (inference).** Commitments built as a
  Merkle tree over an encoded matrix do not satisfy P1. This covers the
  Ligero family, and presumably Ligerito; its paper was not read
  `[NEEDS-EVIDENCE]`. One changed value changes a whole encoded row, so many
  leaves must be rehashed. This explains why the branch stalled on Ligerito.
- **Lattice commitments keep updates short when committed per slot
  (derived).** An Ajtai/SIS commitment binds only short inputs (SADS 2013,
  Theorem 1). So each value is committed through a short encoding,
  `c = Σ_b A_b·G⁻¹(v_b)`, where `G⁻¹` splits a field element into short
  digits.
  - Updating slot `b` replaces that slot's block:
    `c′ = c + A_b·(G⁻¹(v′) − G⁻¹(v))`. The new block is again a canonical
    short encoding, so the norm stays bounded, and the cost does not depend
    on `N`.
  - The updater needs the old value `v`, which the update formula's
    `(v′−v)` already assumes.
  - The norm grows in only two cases: commitments to monomial coefficients,
    and updates that add an encoding of the difference, `G⁻¹(v′−v)`, instead
    of replacing the block.
- **What is left is the opening proof (judgment).** Proving `F̃(k) = v`, or
  an evaluation at a random point, is where lattice schemes pay. Their
  proofs are large, and no way is known to refresh them in constant time
  after an update `[NEEDS-EVIDENCE]`. SADS is one existing point on this
  route: a linear lattice hash, labels kept short, and tree paths as
  openings. Branch 1 and branch 2 meet there.

## Branch 2: authenticated tree

The explorer's text, verbatim:

```
写出需求 G(s)=H(u_1,u_2,…)，代入可加的父标签后得到 G(Σ_i f_i(x_i))=H(u_1,u_2,…)，
要求是 难以找到两组不同的合法子标签，使 H 的结果相同。
……最后得出一个基于 SADS 的认证树方案
```

In English: write the requirement `G(s) = H(u_1, u_2, …)`; substituting the
additive parent label gives `G(Σ_i f_i(x_i)) = H(u_1, u_2, …)`; it must be
hard to find two different sets of valid child labels with the same `H`
value. The exploration ended at an authenticated tree based on SADS.

Mapping onto SADS 2013 (read):

- **Requirement equation.** It is Definition 10(b),
  `f(λ(w)) = h(λ(w0), λ(w1))`. `G` is the projection `f`, `H` is `h`, `s` is
  the parent label `λ(w)`, and the `u_j` are the child labels.
- **Additive parent label.** It is Definition 16,
  `λ(w) = Σ_{v∈range(w)} c_v L_w(v)`. The root label is a sum of partial
  labels, and an insertion or deletion adds `±L_ε(x)` (§4.5). This is the
  multiplicity view of the canonical form, with `f_v(c) = c·L_ε(v)`.
- **Residual security condition.** It is the hypothesis of Theorem 2: if `h`
  is collision resistant, no PPT algorithm outputs a tree collision. "Hard to
  find two different sets of valid child labels with the same `H`" is
  exactly collision resistance of `h`.
- **A condition that looks necessary and is not: `G` injective.** Labels are
  not determined by the leaves: `λ(w)` can be any `f`-preimage of
  `h(λ(u), λ(v))`, and collision resistance still holds (§4.1, the paragraph
  after the definition of `f`).
- **Conditions the instantiation does use:**
  - `f` is linear (Corollary 3);
  - labels stay short: `λ(w) ∈ [n]^m` when `Σ c_i ≤ n` (Lemma 1);
  - `h(x,y) = L·x + R·y mod q` is collision resistant under SIS (Theorem 1);
  - the projection is radix-2 decoding (Fig. 4.2).
- **Accumulator.** The same structure is a dynamic accumulator with
  logarithmic-time witnesses (§6).

The CCSW 2014 paper (read) abstracts the same tree. It allows any pair of
homomorphisms `H_L`, `H_R`, a surjective homomorphic projection, and any
inverse projection that sends 0 to 0 (Definitions 9–11). It instantiates the
hash over the ring `Z_p[α]/(α^k+1)` (a SWIFFT-style function). Its §6 gives
each leaf a random sign, so that labels grow as `√n` rather than `n`
(Definition 18, Lemma 2).

## Novelty verdict and where an increment would sit

**Verdict: existing construction** (SADS 2013, Def. 10 / Def. 16 / Thm 2 /
§4.5 / §6). In this example, the workflow's value is that it reached that
construction from a requirement equation and produced the condition list
that explains why it works.

Any increment has to be stated as its own claim and checked against both
SADS papers. Such a claim could be:
- a different tree shape;
- a different decomposition or norm-control rule;
- parameters chosen to sit beside a deployed set hash;
- a combination with the digest already in use.

Two places to check first are the CCSW 2014 ring instance and its
random-sign labels, because both already change the parameters of the 2013
construction.

#!/usr/bin/env python3
"""Brute-force test of the additive canonical form on a toy aggregator.

The aggregator is a function r: Z_q^n -> G, where G is an abelian group
(written additively below; "mul" groups are handled with the same code).
For every state x and every slot update (i, delta) the script checks:

  P1  separability:   r(x + delta*e_i) - r(x) depends only on (i, x_i, delta)
  CF  canonical form: r(x) = r(0) + sum_i f_i(x_i),  f_i(t) = r(t*e_i) - r(0)
  CO  cocycle:        g_i(t, delta) = f_i(t + delta) - f_i(t)

P1 is the only real premise; CF and CO follow from it, so a CF or CO failure
with P1 passing means the model file or this script is wrong.

Exit status: 0 when P1, CF and CO all hold; 1 with a printed counterexample
when one fails; 2 when the model is malformed or too large to enumerate.

Usage:
  check_separable.py --help             (this text)
  check_separable.py --example NAME     (run a built-in example)
  check_separable.py --list             (list built-in examples)
  check_separable.py MODEL.py           (run your own model)

A model file defines:
  Q      slot modulus; every slot value lives in Z_Q, updates are x_i + delta mod Q
  N      number of slots
  GROUP  digest group: "add:<m>" (integers mod m), "mul:<p>" (nonzero integers
         mod prime p), or "xor" (non-negative integers under XOR)
  r(x)   digest of the state x (a tuple of N ints); returns an int, or a tuple
         of ints for a vector digest (the group acts on each coordinate)
"""

import hashlib
import importlib.util
import itertools
import sys
from types import SimpleNamespace

MAX_WORK = 5_000_000


def die(msg: str):
    print(msg, file=sys.stderr)
    sys.exit(2)


def h_int(label: str, modulus: int) -> int:
    return int.from_bytes(hashlib.sha256(label.encode()).digest()[:8], "big") % modulus


def h_vec(label: str, dim: int, modulus: int) -> tuple:
    return tuple(h_int(f"{label}/{k}", modulus) for k in range(dim))


# ---------------------------------------------------------------- examples

def ex_randomize_combine():
    """Slot-indexed additive hash r = sum_i h(<i>:x_i) mod 2^16 (Bellare-Micciancio)."""
    m = 2**16
    return SimpleNamespace(
        Q=5, N=3, GROUP=f"add:{m}",
        r=lambda x: sum(h_int(f"{i}:{t}", m) for i, t in enumerate(x)) % m,
    )


def ex_lthash_multiset():
    """Multiset hash, multiplicity view: slot e holds the count of element e,
    r = sum_e c_e * h(e) as a 4-coordinate vector mod 16 (LtHash shape; counts mod 16)."""
    m, dim = 16, 4
    hs = [h_vec(f"elem{e}", dim, m) for e in range(3)]
    return SimpleNamespace(
        Q=m, N=3, GROUP=f"add:{m}",
        r=lambda x: tuple(sum(c * hs[e][k] for e, c in enumerate(x)) % m for k in range(dim)),
    )


def ex_set_of_values():
    """Multiset hash, value view: slot i holds an element, r = sum_i h(x_i) mod 2^16
    with one h for every slot, so the digest ignores positions."""
    m = 2**16
    return SimpleNamespace(
        Q=5, N=3, GROUP=f"add:{m}",
        r=lambda x: sum(h_int(f"elem:{t}", m) for t in x) % m,
    )


def ex_muhash():
    """Multiplicative slot-indexed hash r = prod_i h(<i>:x_i) mod p, h into Z_p^*."""
    p = 1009

    def r(x):
        acc = 1
        for i, t in enumerate(x):
            acc = acc * (1 + h_int(f"{i}:{t}", p - 1)) % p
        return acc

    return SimpleNamespace(Q=5, N=3, GROUP=f"mul:{p}", r=r)


def ex_merkle():
    """Binary Merkle root over 4 leaves, digest read as an integer mod 2^32."""
    def H(a: bytes, b: bytes) -> bytes:
        return hashlib.sha256(a + b).digest()

    def leaf(t: int) -> bytes:
        return hashlib.sha256(b"leaf" + bytes([t])).digest()

    def r(x):
        root = H(H(leaf(x[0]), leaf(x[1])), H(leaf(x[2]), leaf(x[3])))
        return int.from_bytes(root[:4], "big")

    return SimpleNamespace(Q=3, N=4, GROUP=f"add:{2**32}", r=r)


def ex_cross_term():
    """r = x_0 + x_1 + x_0*x_1 mod 7: the update of slot 0 depends on slot 1."""
    return SimpleNamespace(Q=7, N=2, GROUP="add:7", r=lambda x: (x[0] + x[1] + x[0] * x[1]) % 7)


EXAMPLES = {
    "randomize-combine": ex_randomize_combine,
    "lthash-multiset": ex_lthash_multiset,
    "set-of-values": ex_set_of_values,
    "muhash": ex_muhash,
    "merkle": ex_merkle,
    "cross-term": ex_cross_term,
}


# ------------------------------------------------------------------ groups

def make_group(spec: str):
    """Return (op, inv, identity) acting on ints; vectors are handled by lift()."""
    kind, _, arg = spec.partition(":")
    if kind == "add":
        m = int(arg)
        return (lambda a, b: (a + b) % m), (lambda a: (-a) % m), 0
    if kind == "mul":
        p = int(arg)

        def inv(a):
            if a % p == 0:
                raise ValueError(f"digest value {a} is 0 mod {p}; not in the multiplicative group")
            return pow(a, -1, p)

        return (lambda a, b: a * b % p), inv, 1
    if kind == "xor":
        return (lambda a, b: a ^ b), (lambda a: a), 0
    die(f"unknown GROUP {spec!r}; use add:<m>, mul:<p> or xor")


def lift(op, inv, e):
    def op_v(a, b):
        if isinstance(a, tuple):
            return tuple(op(u, v) for u, v in zip(a, b, strict=True))
        return op(a, b)

    def inv_v(a):
        if isinstance(a, tuple):
            return tuple(inv(u) for u in a)
        return inv(a)

    def ident_like(a):
        return tuple(e for _ in a) if isinstance(a, tuple) else e

    return op_v, inv_v, ident_like


# ------------------------------------------------------------------- check

def check(model) -> int:
    Q, N, r = model.Q, model.N, model.r
    work = Q**N * N * Q
    if work > MAX_WORK:
        die(f"Q^N * N * Q = {work} exceeds {MAX_WORK}; shrink the toy instance")
    op, inv, ident_like = lift(*make_group(model.GROUP))

    def sub(a, b):
        return op(a, inv(b))

    states = list(itertools.product(range(Q), repeat=N))
    R = {x: r(x) for x in states}
    zero = tuple([0] * N)

    def with_slot(x, i, t):
        y = list(x)
        y[i] = t % Q
        return tuple(y)

    print(f"model: Q={Q} N={N} GROUP={model.GROUP}  states={len(states)}")

    # P1: the increment of slot i must not depend on any other slot.
    g = {}
    for x in states:
        for i in range(N):
            for d in range(Q):
                inc = sub(R[with_slot(x, i, x[i] + d)], R[x])
                key = (i, x[i], d)
                if key not in g:
                    g[key] = (inc, x)
                elif g[key][0] != inc:
                    y = g[key][1]
                    print("FAIL P1 separability: the increment of a slot depends on another slot")
                    print(f"  slot i={i}, current value x_i={x[i]}, delta={d}")
                    print(f"  state {y}: increment {g[key][0]}")
                    print(f"  state {x}: increment {inc}")
                    print("  -> no additive canonical form r = r(0) + sum_i f_i(x_i) exists")
                    return 1
    print("PASS P1 separability")

    # CF: walk from 0 one slot at a time.
    r0 = R[zero]
    f = {(i, t): sub(R[with_slot(zero, i, t)], r0) for i in range(N) for t in range(Q)}
    for x in states:
        acc = r0
        for i, t in enumerate(x):
            acc = op(acc, f[(i, t)])
        if acc != R[x]:
            print(f"FAIL CF canonical form at state {x}: r(x)={R[x]}, r(0)+sum f_i(x_i)={acc}")
            print("  P1 passed, so the model or this script is inconsistent")
            return 1
    print("PASS CF canonical form r(x) = r(0) + sum_i f_i(x_i), f_i(t) = r(t*e_i) - r(0)")

    # CO: the update function is determined by f_i.
    for (i, t, d), (inc, _) in g.items():
        if inc != sub(f[(i, (t + d) % Q)], f[(i, t)]):
            print(f"FAIL CO cocycle at slot {i}, t={t}, delta={d}")
            return 1
    print("PASS CO cocycle g_i(t, delta) = f_i(t + delta) - f_i(t)")

    # Shape information for the next workflow step (not pass/fail).
    same_f = all(f[(i, t)] == f[(0, t)] for i in range(N) for t in range(Q))
    print(f"INFO all slots share one f: {same_f}"
          + ("  (digest ignores positions: multiset hash of the slot values)" if same_f
             else "  (slot-indexed: f_i depends on i)"))
    linear = all(f[(i, (t + 1) % Q)] == op(f[(i, t)], f[(i, 1)]) for i in range(N) for t in range(Q))
    print(f"INFO f_i(t) = t * f_i(1) for every slot: {linear}"
          + ("  (each slot acts as the count of one element: multiplicity view)" if linear else ""))
    print(f"INFO r(0) = {r0}" + ("  (already normalized)" if r0 == ident_like(r0) else "  (absorb as a constant)"))
    return 0


def load_model(path: str):
    spec = importlib.util.spec_from_file_location("aggregator_model", path)
    if spec is None or spec.loader is None:
        die(f"cannot load {path}")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    for name in ("Q", "N", "GROUP", "r"):
        if not hasattr(mod, name):
            die(f"{path} must define {name}")
    return mod


def main(argv):
    if len(argv) == 2 and argv[1] in ("-h", "--help"):
        print(__doc__)
        return 0
    if len(argv) == 2 and argv[1] == "--list":
        for name, fn in EXAMPLES.items():
            print(f"{name:18s} {fn.__doc__}")
        return 0
    if len(argv) == 3 and argv[1] == "--example":
        if argv[2] not in EXAMPLES:
            die(f"unknown example {argv[2]!r}; try --list")
        return check(EXAMPLES[argv[2]]())
    if len(argv) == 2 and not argv[1].startswith("-"):
        return check(load_model(argv[1]))
    print(__doc__)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv))

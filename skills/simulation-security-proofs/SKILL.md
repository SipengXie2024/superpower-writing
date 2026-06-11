---
name: simulation-security-proofs
description: Use when proving security of MPC protocols, zero-knowledge proofs, oblivious transfer, commitment schemes, garbled circuits, or any protocol whose security is argued by comparing a real execution against an ideal functionality, in standalone simulation-based or UC frameworks. Covers simulator construction, hybrid arguments, corruption models, composition theorems, and writing the proof section of a cryptographic paper so the ideal-versus-real argument is complete and checkable.
---

# Simulation-Based and UC Security Proofs

## Overview

Simulation-based security is the gold standard for proving cryptographic protocol security. The paradigm compares a real protocol execution to an ideal world that is secure by definition. A protocol is secure if any real-world attack can be "simulated" in the ideal world, meaning the adversary learns nothing beyond what is inherently leaked by the functionality.

## When to Use This Skill

- Proving security of two-party or multi-party computation protocols
- Constructing zero-knowledge proof systems
- Analyzing oblivious transfer, commitment schemes, or coin-tossing protocols
- Working with semi-honest or malicious adversary models
- Proving security in the CRS model or Random Oracle model
- Establishing UC (Universally Composable) security
- Writing hybrid-model proofs with ideal functionalities as subroutines

## Quick Reference: The Three Tasks of a Simulator

| Task | Description |
|------|-------------|
| Generate view | Simulated transcript must be computationally indistinguishable from real execution |
| Extract inputs | Determine the effective inputs used by the adversary |
| Ensure consistency | Make the generated view consistent with outputs based on extracted inputs |

## Quick Reference: Simulation Strategies by Protocol Type

| Protocol Type | Key Challenge | Simulation Strategy |
|--------------|---------------|---------------------|
| Semi-honest OT | Generate view without knowing other input | Use trapdoor to compute both values |
| Zero-knowledge | Generate accepting view without witness | Rewind to guess challenge |
| Coin-tossing | Force output to specific value | Rewind until XOR matches |
| Malicious OT | Extract sender's inputs | CRS trapdoor or DDH tuple |
| Commitment | Equivocate or extract | Trapdoor commitment or rewinding |
| MPC (malicious) | Extract all inputs, ensure consistency | Hybrid model with ZK subprotocol |

## References

- **references/core_concepts_and_techniques.md**: Computational indistinguishability, ideal/real paradigm, adversary models (semi-honest and malicious definitions), proof techniques (hybrid argument, rewinding, hybrid model, reductions), common pitfalls, special models (CRS, ROM, adaptive), and proof checklist
- **references/hybrid_arguments.md**: Hybrid lemma, types of hybrid arguments, systematic construction of hybrid sequences
- **references/simulator_constructions.md**: Detailed patterns for constructing simulators (OT, commitment, coin-tossing, etc.)
- **references/uc_framework.md**: UC execution model, UC security definition, impossibility results, UC with CRS
- **templates/latex_proof_templates.md**: LaTeX templates for semi-honest proofs, malicious adversary proofs, and zero-knowledge proofs

## Key References

1. Lindell (2025), "How To Simulate It", a tutorial on the simulation proof technique
2. Goldreich (2004), Foundations of Cryptography Vol. II
3. Canetti (2001), "Universally Composable Security" (FOCS 2001)
4. Goldreich, Micali, Wigderson (1991), "Proofs that Yield Nothing but their Validity" (JACM)

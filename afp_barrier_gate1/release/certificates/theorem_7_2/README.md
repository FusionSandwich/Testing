# Theorem 7.2 exact-rational certificate

This directory is the computer-assisted exact-rational closure boundary for
Theorem 7.2 of the flagship manuscript. The article and
`docs/publication_program/P1E_SHORT_GAP_S2_CONSTRUCTION.md` give the
ordinary mathematical proofs: ring schedule, shared mask, literal row equations,
transition system, Cauchy domain, ordinary-row recurrence, polar row,
normalization, and quotient argument. `certificate.json` records exact
rational closure data and SHA-256 provenance bindings. A source digest proves
byte identity only; it does not prove the source's mathematical contents.

Run the independent verifier from the repository root:

```powershell
py -3.12 afp_barrier_gate1\release\certificates\theorem_7_2\verify_certificate.py
```

The verifier imports only Python's standard library. It checks source hashes,
all listed rational guard inequalities, the limiting determinant and inverse
bound, the affine solution identity and strict cone margin in
`Q(sqrt(58))`, the Neumann and polar-row budgets, the arbitrary-`J` transition
geometric sums, the corrected signed second-order product budget, the
positivity and normalization coefficient arithmetic, propagation of the
geometry-bound coefficients supplied by the ordinary proof, hostile
mutations, and the constants printed in Theorem 7.2. It performs no floating-point
calculation and does not import the construction or its original audit code.

Trusted computing base: the bytes of `certificate.json` and
`verify_certificate.py`, CPython's arbitrary-precision integer and
`fractions.Fraction` implementation, SHA-256, and the ordinary mathematical
use of the ordinary analytic lemmas explicitly proved in the article and proof
source. The verifier does not machine-prove the transcendental schedule,
literal row-equation derivation, Cauchy estimates, geometry, or sampled
quotient argument. SymPy is used by the original derivation audits but is not required by
this independent verifier. Lean does not check the adaptive-ring schedule or
the analytic Cauchy argument.

Passing this verifier supports the exact-rational certificate only. It is not
external peer review, publication acceptance, perturbative robustness, a
construction for every sufficiently small `h`, or a construction in
dimensions greater than three.

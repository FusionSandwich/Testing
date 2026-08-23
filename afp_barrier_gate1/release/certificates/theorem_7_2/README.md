# Theorem 7.2 exact-rational certificate

This directory is the immutable computer-assisted proof boundary for
Theorem 7.2 of the flagship manuscript. The article and
`docs/publication_program/P1E_SHORT_GAP_S2_CONSTRUCTION.md` give the
mathematical reduction: ring schedule, shared mask, literal row equations,
transition system, Cauchy domain, ordinary-row recurrence, polar row,
normalization, and quotient argument. `certificate.json` records the exact
rational closure data and SHA-256 binds every load-bearing source.

Run the independent verifier from the repository root:

```powershell
py -3.12 afp_barrier_gate1\release\certificates\theorem_7_2\verify_certificate.py
```

The verifier imports only Python's standard library. It checks source hashes,
all listed rational guard inequalities, the limiting determinant and inverse
bound, the affine solution identity and strict cone margin in
`Q(sqrt(58))`, the Neumann and polar-row budgets, the recurrence closure, and
the constants printed in Theorem 7.2. It performs no floating-point
calculation and does not import the construction or its original audit code.

Trusted computing base: the bytes of `certificate.json` and
`verify_certificate.py`, CPython's arbitrary-precision integer and
`fractions.Fraction` implementation, SHA-256, and the ordinary mathematical
use of the analytic estimates explicitly stated in the article and proof
source. SymPy is used by the original derivation audits but is not required by
this independent verifier. Lean does not check the adaptive-ring schedule or
the analytic Cauchy argument.

Passing this verifier supports the exact-rational certificate only. It is not
external peer review, publication acceptance, perturbative robustness, a
construction for every sufficiently small `h`, or a construction in
dimensions greater than three.

# AFP pure-mathematics track

This branch separates the theorem-driven mathematics program from the frozen
Gate 6 transport implementation.

## Frozen transport baseline

The verified transport source is preserved on
`archive/afp-gate6-spatial-multigroup-verified` at commit
`515f1aae6c20bd85711c90b5c1c21b4905252d01`.

Transport, Radiant integration, evaluated material data, and physical HTS
benchmarks are deferred. They are not deleted or superseded.

## Pure-math objective

The intended paper is not centered on the elementary inequality

```text
lambda^2 <= rate * defect.
```

That inequality and its weighted-variance remainder are foundational lemmas.
The publication target is a theorem package about finite positive generators
that remains interesting without AFP terminology:

1. local positive feasibility on spherical eigenmap embeddings;
2. attainable quadratic spectral-product exactness;
3. global equality propagation and geometric rigidity;
4. a moment-hierarchy obstruction or a sharp dimension tradeoff.

## Current scientific gates

### P0 — claim reset and falsification

- freeze the verified transport source;
- maintain a claim matrix and conjecture register;
- run exact/deterministic counterexample searches;
- reject unrestricted classifications contradicted by Platonic graphs;
- perform adjacent-field priority review before claiming novelty.

### M1 — local spherical feasibility

For a vertex `Omega_i`, write each neighbor as

```text
Omega_j = cos(theta_j) Omega_i + sin(theta_j) u_j,
```

where `u_j` is tangent. Degree-one exactness is equivalent to a nonnegative
tangent dependence plus one scalar normal-loss equation. The initial Lean
module formalizes the constructive scaling equivalence. The full convex-hull
and strict-relative-interior formulation is the next theorem target.

### M2 — global equality propagation

If every row attains equality in the local rate-defect bound, all active edges
at a vertex have one loss. Reversibility and graph connectivity should
propagate one common edge loss and one common row rate. Classification is only
attempted under explicit geometric restrictions such as spherical
triangulation.

### M3 — quadratic covariance

For an eigenmap `Phi`, introduce the jump covariance

```text
C_i = sum_j a_ij (Phi_j - Phi_i)(Phi_j - Phi_i)^T.
```

The target is an exact characterization and dimension bound for the quadratic
forms reproduced with a prescribed eigenvalue. Merely repeating the full
quadratic no-go theorem is insufficient.

## Claim discipline

Every statement is labeled one of:

- `PROVED` — complete proof under stated assumptions;
- `EXTERNAL` — direct use or specialization of a cited theorem;
- `COMPUTATIONAL` — finite deterministic verification only;
- `CONJECTURE` — survived current tests but is unproved;
- `REJECTED` — false, ill posed, redundant, or strategically unsuitable.

Lean and CI are verification infrastructure, not mathematical novelty.

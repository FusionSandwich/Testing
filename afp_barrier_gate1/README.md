# AFP Barrier Lean formalization

This package formalizes the finite jump-generator core of the angular Fokker–Planck second-harmonic monotonicity barrier.

## Modules

- `AFPBarrier/JumpGenerator.lean`: definitions, carré-du-champ identity, nonnegativity, and weighted finite Cauchy–Schwarz.
- `AFPBarrier/NoGo.lean`: generic second-harmonic obstruction.
- `AFPBarrier/Quantitative.lean`: exact defect identity and defect–stiffness inequalities.
- `AFPBarrier/SphereSpecialization.lean`: numerical `S^2` specialization, with spherical-harmonic identities supplied as hypotheses.
- `AFPBarrier/AxiomAudit.lean`: `#print axioms` checks.

## Local build

```bash
lake update
lake exe cache get
lake build
lake env lean AFPBarrier/AxiomAudit.lean
```

The project is pinned to Lean/Mathlib `v4.30.0`.

The differential-geometric identities for the spherical Laplacian are not yet formalized. The finite-dimensional contradiction and quantitative inequalities are the kernel-checked portion targeted by Gate 1.

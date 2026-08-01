# AFP pure-mathematics track

This branch separates the theorem-driven mathematics program from the frozen
Gate 6 transport implementation.

## Frozen transport baseline

The verified transport source is preserved on
`archive/afp-gate6-spatial-multigroup-verified` at commit
`515f1aae6c20bd85711c90b5c1c21b4905252d01`.

Transport, Radiant integration, evaluated material data, spatial solvers, and
physical HTS benchmarks are outside this stage. They are neither modified nor
superseded here.

## Pure-math objective

The intended paper is not centered on the elementary inequality

```text
lambda^2 <= rate * defect.
```

That inequality and its weighted-variance remainder are foundational lemmas.
The publication target is a theorem package about finite positive generators
that remains interesting without AFP terminology:

1. local positive feasibility on spherical eigenmap embeddings;
2. quantitative robustness and conditioning of positive spherical rows;
3. global reversible shared-edge compatibility and duality;
4. attainable quadratic spectral-product exactness;
5. global equality propagation and geometric rigidity.

## Completed P0/M1 sphere-specific package

The full ordinary proof is in
`docs/SPHERICAL_FEASIBILITY_SHARED_EDGE_THEOREM.md`. It establishes:

- nonnegative local feasibility iff `0` lies in the tangent convex hull;
- strict positivity on every indexed edge iff `0` lies in the relative
  interior, including repeated and redundant directions;
- exact uniqueness through affine independence in the minimal face;
- the unique positive normal scale and explicit angular rate formula;
- a separate division-free antipodal-only and mixed-antipodal theorem;
- a relative cone margin with explicit coefficient, outgoing-rate,
  inverse-quadratic, conditioning, perturbation, and objective constants;
- the global shared-edge cone and compact feasible-polytope description;
- weighted centering and the dense complete-graph construction;
- the full finite Farkas alternative with the actual spherical edge block;
- strong LP duality and complementary slackness for rate, defect, peak, and
  residual formulations;
- strict global feasibility and sensitivity estimates;
- a weighted-centered cube that is locally strictly feasible at every row but
  globally incompatible, with an exact Farkas certificate; and
- a centered-clique submass decomposition that constructs sparse compatible
  shared-edge solutions.

The exact examples are regression-checked by
`pure_math/tests/test_spherical_feasibility.py` using rational arithmetic.

## Lean verification boundary

Lean 4.30 / Mathlib 4.30 formalizes the finite algebraic consequences in:

- `AFPBarrier/LocalSphericalFeasibility.lean`;
- `AFPBarrier/SphericalFeasibilityAlgebra.lean`;
- `AFPBarrier/QuantitativeSphericalFeasibility.lean`;
- `AFPBarrier/DualCertificate.lean`;
- `AFPBarrier/GlobalSharedEdgeDuality.lean`;
- `AFPBarrier/ReversibleConductance.lean`; and
- `AFPBarrier/CompleteGraph.lean`.

The complete finite-dimensional Farkas and strong-LP-duality theorems are used
as standard external mathematics and are stated with every hypothesis and AFP
sign convention in the theorem document. Their spherical transpose blocks,
weak-duality soundness, objective-gap identity, and complementary-slackness
consequences are formalized. No placeholder proofs or user-declared axioms are
permitted.

## Scientific gates

### P0 — claim reset and falsification

- frozen transport source remains untouched;
- claim matrix, conjecture register, and prior-art map are active controls;
- exact deterministic counterexamples are retained;
- unrestricted classifications contradicted by Platonic graphs remain
  rejected;
- novelty is separated from standard convexity and LP theory.

### M1 — local spherical feasibility and global compatibility

For a vertex `Omega_i`, write each neighbor as

```text
Omega_j = cos(theta_j) Omega_i + sin(theta_j) u_j,
```

where `u_j` is tangent. Degree-one exactness is equivalent to a nonnegative
tangent dependence plus one scalar normal-loss equation.

**Status: resolved.** `EXACT_LOCAL_GLOBAL_THEOREM_PACKAGE.md` proves the full
non-antipodal hull and strict-relative-interior theorem, exact
scaling/rate/uniqueness, the pure and mixed antipodal theorem, quantitative
`rho`/`beta_*` margins, explicit perturbation radii, local conditioning, the
global Farkas/LP package, the centered local-but-not-global obstruction, group
averaging reconciliation, and compatible global perturbation bounds.

The original `LocalSphericalFeasibility.lean` remains the foundational scaling
module. New modules formalize normalization and recovery, antipodal budgeting,
shared-edge certificate arithmetic, and finite averaging. The independent
`SphericalFeasibilityAlgebra.lean`, `QuantitativeSphericalFeasibility.lean`,
and `GlobalSharedEdgeDuality.lean` modules provide a second formal route for
the finite scalar and duality consequences.

### M2 — global equality propagation

If every row attains equality in the local rate-defect bound, all active edges
at a vertex have one loss. Reversibility and graph connectivity are expected
to propagate one common edge loss and one common row rate. Classification is
attempted only under explicit geometric restrictions such as spherical
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

Lean and CI are verification infrastructure, not mathematical novelty. Local
positive rows, weighted centering, and sparse global shared-edge compatibility
must never be conflated.

## M1 records

- `EXACT_LOCAL_GLOBAL_THEOREM_PACKAGE.md` — complete proofs and constants;
- `APPROACH_REGISTRY.md` — mechanism-based route/audit registry;
- `../docs/THEOREM_TO_FILE_MAP.md` — theorem/formalization/regression map;
- `examples/exact_local_global_audit.py` — exact symbolic regression certificates;
- `tests/test_spherical_feasibility.py` — independent exact rational cube and
  boundary-crossing regressions;
- `../docs/SPHERICAL_FEASIBILITY_SHARED_EDGE_THEOREM.md` and
  `../docs/SPHERICAL_FEASIBILITY_OPTIMAL_VALUE_SENSITIVITY.md` — independent
  theorem and sensitivity derivations retained for cross-audit.

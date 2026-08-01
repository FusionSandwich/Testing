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
4. genuine sampled quadratic exactness and covariance rigidity; and
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

## Completed Prompt 2 sampled-covariance package

The paper-style theorem is

```text
pure_math/covariance/SAMPLED_QUADRATIC_EXACTNESS_THEOREM.md
```

It establishes:

- the exact covariance identity
  `L(Phi^T A Phi)=-2 lambda Phi^T A Phi+tr(A^T C_i)`;
- the necessary-and-sufficient residual equation for a shifted target
  eigenvalue;
- the trace-free spherical form-space characterization
  `E_form=span{M_i}^perp`;
- the quadratic sampling map, its kernel, and the genuine sampled space
  `E_sample=S_X(E_form)`;
- the corrected intersection and stacked-rank dimension formulas;
- a sharp axial-covariance theorem under which
  `E_form=K_X` and `E_sample={0}`;
- an all-dimensional regular-simplex equality family with a large algebraic
  exact space that is entirely sampling kernel;
- an independent transitive-equivariant irreducibility theorem;
- exact covariance tensors, constraint ranks, sampling kernels, and sampled
  dimensions for all five Platonic shortest-edge generators;
- an explicit signed four-point generator restoring a nonzero sampled
  quadratic mode, with the negative antipodal rate `-1/2` proved forced on the
  fixed support;
- independent carré-du-champ and semigroup/Jensen proofs of the additive
  sampled-square obstruction; and
- a bounded and structural spherical-product audit that rejects the proposed
  general hierarchy under its kill criterion because no new sampled dimension
  tradeoff or global consequence survives.

The exact audit

```text
pure_math/covariance/quadratic_covariance_audit.py
```

uses symbolic arithmetic over `Q(sqrt(5))`, not floating rank thresholds. It
contains a negative regression against the incorrect formula
`dim E_form-dim K_X`, verifies the correct stacked-rank formula, checks exact
Platonic centering and second moments, and records both the bounded resonance
list and an infinite `d=4` Pell-family prefix.

## Lean verification boundary

Lean 4.30 / Mathlib 4.30 formalizes finite algebraic consequences in:

- `AFPBarrier/LocalSphericalFeasibility.lean`;
- `AFPBarrier/SphericalFeasibilityAlgebra.lean`;
- `AFPBarrier/QuantitativeSphericalFeasibility.lean`;
- `AFPBarrier/QuadraticCovariance.lean`;
- `AFPBarrier/DualCertificate.lean`;
- `AFPBarrier/GlobalSharedEdgeDuality.lean`;
- `AFPBarrier/ReversibleConductance.lean`; and
- `AFPBarrier/CompleteGraph.lean`.

For Prompt 2, Lean checks the finite product identity, covariance contraction,
shifted residual equivalence, trace-free projection consequence, rank-nullity
for the sampling map restricted to an exact-form subspace, and the row-scaled
constraint-to-sampling implication used by the axial theorem. Standard
semigroup/Jensen facts remain ordinary external mathematics rather than
project axioms.

The complete finite-dimensional Farkas and strong-LP-duality theorems from
P0/M1 remain standard external mathematics. No placeholder proofs or
user-declared axioms are permitted.

## Scientific gates

### P0 — claim reset and falsification

- frozen transport source remains untouched;
- claim matrix, conjecture register, and prior-art map are active controls;
- exact deterministic counterexamples are retained;
- unrestricted classifications contradicted by Platonic graphs remain
  rejected; and
- novelty is separated from standard convexity, rank algebra, and LP theory.

### M1 — local spherical feasibility and global compatibility

**Status: complete for the stated finite theorem package.** The local and
antipodal theorems, quantitative margin, global shared-edge alternative,
strictness, sensitivity, examples, and gluing mechanism are all proved.

### M2 — global equality propagation

If every row attains equality in the local rate-defect bound, all active edges
at a vertex have one loss. Reversibility and graph connectivity are expected
to propagate one common edge loss and one common row rate. Classification is
attempted only under explicit geometric restrictions such as spherical
triangulation.

### M3 — sampled quadratic covariance

**Status: complete for Prompt 2.** The covariance identity, sampling-kernel
correction, sharp axial and equivariant rigidity theorems, exact Platonic
examples, signed restoration, and independent product obstructions are proved.
The generic spectral-product hierarchy is rejected for this stage.

## Claim discipline

Every statement is labeled one of:

- `PROVED` — complete proof under stated assumptions;
- `EXTERNAL` — direct use or specialization of a cited theorem;
- `COMPUTATIONAL` — finite deterministic verification only;
- `CONJECTURE` — survived current tests but is unproved; or
- `REJECTED` — false, ill posed, redundant, killed by the stated criterion, or
  strategically unsuitable.

Lean and CI are verification infrastructure, not mathematical novelty. A
nonzero quadratic matrix, a nonzero exact form, a nonzero sampled function,
and a nonzero exact sampled function must never be conflated.

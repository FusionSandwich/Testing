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
4. sampling-kernel-aware quadratic and spectral-product exactness;
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

### M3 — quadratic covariance and spectral products

For an eigenmap `Phi`, introduce the jump covariance

```text
C_i = sum_j a_ij (Phi_j - Phi_i)(Phi_j - Phi_i)^T.
```

**Status: resolved for Prompt 2.** The complete ordinary proofs are in
covariance/QUADRATIC_COVARIANCE_THEOREM.md and
spectral_products/SPECTRAL_PRODUCT_ANALYSIS.md.

The package proves:

- covariance and arbitrary-target identities, including the zero target;
- weighted centering under nonempty positive-weight detailed balance;
- the sphere residual, sampling quotient, and genuine dimension formula;
- the positive residual and Frobenius obstruction for a nonempty finite state
  set, \(d>1\), and a nonnegative unit eigenmap with
  \(L\Phi=-(d-1)\Phi\);
- signed one-shell full-tangent-isotropy rigidity \(R_X=DS_X\) for \(d>1\)
  unit nodes satisfying \(L\Phi=-(d-1)\Phi\), nonempty noncoincident shells
  with \(0<\ell_i<2\), and the full signed moment;
- positive prism sharpness, the exact five-Platonic classification, and signed
  cube restoration with sharp undirected negative mass two;
- multiplicity-free kernel formulas and the quotient rank gap under invariant
  generator rates, plus the corrected invariance theorem with exact \(D_3\)
  counterexample;
- product resonance, semigroup variance, and separate Jensen equality;
- the common-operator target-eigenvalue-class sampling theorem, constants-safe
  converse, antipodal bound, exact aliases, and parity-filtered \(S^2\) Pell
  hierarchy.

The unrestricted distinct-degree theorem is REJECTED in \(d=1\); distinct
degrees imply distinct spherical targets only for \(d\ge2\). A universal
positivity-only hierarchy and scalarity without invariance are also REJECTED.

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

## Prompt 1 records

- `EXACT_LOCAL_GLOBAL_THEOREM_PACKAGE.md` — complete proofs and constants;
- `APPROACH_REGISTRY.md` — mechanism-based route/audit registry;
- `../docs/THEOREM_TO_FILE_MAP.md` — theorem/formalization/regression map;
- `examples/exact_local_global_audit.py` — exact symbolic regression certificates;
- `tests/test_spherical_feasibility.py` — independent exact rational cube and
  boundary-crossing regressions;
- `../docs/SPHERICAL_FEASIBILITY_SHARED_EDGE_THEOREM.md` and
  `../docs/SPHERICAL_FEASIBILITY_OPTIMAL_VALUE_SENSITIVITY.md` — independent
  theorem and sensitivity derivations retained for cross-audit.

## Prompt 2 records

- covariance/QUADRATIC_COVARIANCE_THEOREM.md — authoritative covariance,
  rigidity, equivariance, prism, Platonic, and signed-cube proofs;
- covariance/QUADRATIC_COVARIANCE_DERIVATION.md — short derivation and
  assumption audit;
- spectral_products/SPECTRAL_PRODUCT_ANALYSIS.md — product, semigroup, sampled
  hierarchy, aliases, and Pell boundary;
- covariance/P2_THEOREM_REGISTRY.md and covariance/P2_APPROACH_REGISTRY.md —
  exact claim and mechanism controls;
- ../docs/P2_THEOREM_TO_FILE_MAP.md — ordinary/Lean/exact theorem map;
- covariance/exact_quadratic_covariance_audit.py — Platonic and prism exact
  certificates;
- covariance/exact_signed_restoration_audit.py — signed cube and optimum;
- covariance/exact_d3_invariance_counterexample.py — omitted-invariance
  regression; and
- spectral_products/exact_spectral_product_audit.py — products, corrected
  hierarchy, aliases, antipodal bounds, and Pell cases.

## Prompt 3 records

- rigidity/GLOBAL_Q_RIGIDITY_THEOREM.md — exact equality transfer, fixed
  ten-hypothesis classification, graph/spectral/resistance near-rigidity,
  corrected closed threshold, and covariance anisotropy boundary;
- rigidity/ICOSAHEDRAL_GRAPH_LEMMA.md — direct separating-triangle/link/collar
  proof for the 5-valent 12-vertex case;
- rigidity/P3_BRANCH_PROTECTION_RECORD.md and P3_SALVAGE_LEDGER.md — immutable
  ancestry, protected-ref, and selective-source provenance;
- rigidity/P3_APPROACH_REGISTRY.md and P3_THEOREM_REGISTRY.md — independent
  mechanism and controlled theorem labels;
- ../docs/P3_THEOREM_TO_FILE_MAP.md and P3_STAGE_REPORT.md — artifact map and
  exact-head handoff record;
- rigidity/triangulation_counterexample_audit.py — source-pinned finite hostile
  enumeration, labeled COMPUTATIONAL;
- rigidity/global_near_rigidity_audit.py — exact/deterministic constant and
  stress certificates; and
- rigidity/q1_covariance_audit.py — weighted-octahedron, sampling-kernel, and
  five-Platonic regressions.

The literal tangent-normalization formulation without `0<ell<2` is REJECTED
by the exact antipodal equality chain.  The corrected non-antipodal covariance
theorem is PROVED.  The old endpoint-product angle enclosure and an old
incident-loss Lean statement are also REJECTED; Prompt 3 uses the explicit
spherical Gram/Heron certificate and the corrected `delta<1` lemma.

Rank-nullity, real semisimplicity, self-adjoint spectral theory,
Clebsch--Gordan, Pell completeness, Jensen/uniformization, and convex KKT are
EXTERNAL. Exact finite matrices are COMPUTATIONAL support. No priority claim
follows from the covariance identity, a rank table, Lean job count, or CI
result alone.

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
4. genuinely sampled quadratic spectral exactness; and
5. global equality propagation and geometric rigidity.

## Completed Prompt 1 package

`EXACT_LOCAL_GLOBAL_THEOREM_PACKAGE.md` and the independent
`docs/SPHERICAL_FEASIBILITY_SHARED_EDGE_THEOREM.md` development establish:

- exact non-antipodal convex-hull and relative-interior feasibility;
- repeated/redundant indexed points and exact uniqueness;
- the unique positive angular rescaling;
- a division-free pure/mixed antipodal theorem;
- explicit `rho`, `beta_*`, coefficient, rate, conditioning, perturbation, and
  optimal-value constants;
- global shared-edge cone, Farkas, LP, and complementary-slackness theory;
- strict feasibility and compatible perturbation estimates;
- exact centered local-but-not-global examples;
- complete-graph, group-averaging, and centered-clique reconciliation.

The corrected Prompt 1 baseline used by Prompt 2 is commit
`923dc47dae4f83dbea9cd56aa904164c6378e52d`.

## Completed Prompt 2 sampled-covariance package

The paper-style proof is
`covariance/SAMPLED_QUADRATIC_EXACTNESS_THEOREM.md`.

For

```text
L Phi = -lambda Phi,
C_i = sum_j a_ij (Phi_j-Phi_i)(Phi_j-Phi_i)^T,
Q_A(i) = Phi_i^T A Phi_i,
```

it proves

```text
L Q_A(i)
  = -2 lambda Q_A(i) + tr(A^T C_i),
```

and the exact shifted target residual.

For the trace-free degree-two sphere specialization, define

```text
S_X(A)_i = Phi_i^T A Phi_i,
R_X(A)_i = <A,P_0(C_i+2 Phi_i Phi_i^T)>_F.
```

The key structural relation is

```text
R_X = (L+2d I) S_X.
```

Therefore

```text
K_X = ker S_X subset E_form = ker R_X,
E_sample = S_X(E_form)
         = im(S_X) intersect ker(L+2d I),
dim E_sample = rank(S_X)-rank(R_X).
```

The principal sharp theorem states that positive axially isotropic covariance
at every node forces

```text
E_form = K_X,
E_sample = {0}.
```

This is attained by regular simplices in every dimension. An independent
transitive-irreducibility theorem forces `E_form={0}` under a different
symmetry mechanism.

Exact proofs for the five Platonic shortest-edge generators give:

| Graph | rank `R_X` | rank `S_X` | dim `E_form` | dim `K_X` | dim `E_sample` |
|---|---:|---:|---:|---:|---:|
| tetrahedron | 3 | 3 | 2 | 2 | 0 |
| octahedron | 2 | 2 | 3 | 3 | 0 |
| cube | 3 | 3 | 2 | 2 | 0 |
| icosahedron | 5 | 5 | 0 | 0 | 0 |
| dodecahedron | 5 | 5 | 0 | 0 | 0 |

The tetrahedral, octahedral, and cubical nonzero form spaces consist entirely
of sampling aliases. The exact audit uses rational and
`Q(sqrt(5))` arithmetic, not floating rank thresholds.

A signed four-point circle generator with adjacent rates `1` and antipodal
rates `-1/2` restores one genuine sampled quadratic mode. The local coordinate
and quadratic equations force the negative antipodal rate on that fixed
support.

Two independent positive-generator product obstructions are retained:
carre-du-champ and semigroup/Jensen. After parity, maximizing-set, sampling,
aliasing, and Pell-resonance checks, the proposed general spectral-product
hierarchy is `REJECTED` for Prompt 2 under its kill criterion; no new
`l`-indexed dimension tradeoff survived beyond the sampled-square identity.

## Lean verification boundary

Lean 4.30 / Mathlib 4.30 formalizes Prompt 1 finite consequences in:

- `AFPBarrier/LocalSphericalFeasibility.lean`;
- `AFPBarrier/ExactLocalRows.lean`;
- `AFPBarrier/QuantitativeExactLocal.lean`;
- `AFPBarrier/AntipodalFeasibility.lean`;
- `AFPBarrier/SharedEdgeEquilibrium.lean`;
- `AFPBarrier/GroupAveraging.lean`;
- `AFPBarrier/GlobalSharedEdgeDuality.lean`; and related modules.

Prompt 2 finite algebra is in
`AFPBarrier/QuadraticCovariance.lean`. It formalizes:

- the finite product and covariance identities;
- the shifted target residual;
- trace-free projection contraction;
- restricted-map rank-nullity;
- `ker S subset ker(B comp S)`;
- `range(S|ker(BS)) = range(S) intersect ker(B)`;
- row-scaled constraint/sample equivalence; and
- the axial trace coefficient.

The general semigroup equality theorem and real representation irreducibility
remain precisely stated ordinary inputs. No placeholder proofs or
user-declared axioms are permitted.

## Scientific gates

### P0 — claim reset and falsification

- frozen transport source remains untouched;
- claim matrix, conjecture register, and prior-art map are active controls;
- exact deterministic counterexamples are retained;
- unrestricted classifications contradicted by examples remain rejected;
- novelty is separated from standard convexity, LP, carré-du-champ, Jensen,
  and rank-nullity theory.

### M1 — local spherical feasibility and global compatibility

**Status: resolved.** The corrected package includes exact local and antipodal
theorems, quantitative margins, global cone/duality, two exact obstructions,
group and clique reconciliation, and compatible sensitivity.

### M2 — global equality propagation

**Status: separate conjectural branch.** Equality propagation remains outside
Prompt 2 unless it produces a new classified consequence.

### M3 — sampled quadratic covariance

**Status: resolved for the Prompt 2 theorem package.** The exact covariance
identity, sampling factorization, genuine sampled-space formula, axial and
equivariant rigidity, all-dimensional equality family, exact Platonic cases,
and signed restoration are complete.

## Claim discipline

Every statement is labeled one of:

- `PROVED` — complete proof under stated assumptions;
- `EXTERNAL` — direct use or specialization of a cited theorem;
- `COMPUTATIONAL` — finite deterministic verification only;
- `CONJECTURE` — survived current tests but is unproved;
- `REJECTED` — false, ill posed, redundant, or strategically unsuitable.

Lean and CI are verification infrastructure, not mathematical novelty.
Algebraic form exactness and genuine sampled exactness must never be
conflated.

## Records

Prompt 1:

- `EXACT_LOCAL_GLOBAL_THEOREM_PACKAGE.md`;
- `APPROACH_REGISTRY.md`;
- `../docs/THEOREM_TO_FILE_MAP.md`;
- `examples/exact_local_global_audit.py`;
- `tests/test_spherical_feasibility.py`.

Prompt 2:

- `covariance/SAMPLED_QUADRATIC_EXACTNESS_THEOREM.md`;
- `covariance/QUADRATIC_COVARIANCE_DERIVATION.md`;
- `covariance/quadratic_covariance_audit.py`;
- `../docs/PROMPT2_QUADRATIC_COVARIANCE_THEOREM_MAP.md`;
- `../docs/PROMPT2_QUADRATIC_COVARIANCE_STAGE_REPORT.md`.

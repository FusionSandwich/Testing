# P0/M1 stage report — spherical positive feasibility and shared-edge duality

## 1. Baseline, scope, and branch state

- Repository: `FusionSandwich/Testing`
- Target branch: `agent/afp-pure-math-p0-m1`
- Verified checkpoint: `4efef67a20cdb8b2437cad093ccc16bcd0f17796`
- Isolated validation branch: `agent/afp-spherical-feasibility-validation`
- Checkpoint comparison at stage start: identical; no intervening branch changes
  required reconciliation.
- Frozen transport archive:
  `archive/afp-gate6-spatial-multigroup-verified` at
  `515f1aae6c20bd85711c90b5c1c21b4905252d01`

The stage changed only the pure-mathematics package, its proof-control
documents, exact regressions, and a dedicated Lean workflow. It added no
transport, Radiant, HTS, multigroup, or spatial-solver work and did not modify
the frozen archive.

## 2. Stage outcome

The stage proves the complete finite theorem package in
`SPHERICAL_FEASIBILITY_SHARED_EDGE_THEOREM.md`, supplemented by
`SPHERICAL_FEASIBILITY_OPTIMAL_VALUE_SENSITIVITY.md`:

1. exact non-antipodal convex-hull and relative-interior equivalences;
2. indexed uniqueness, including repeated and redundant directions;
3. unique positive angular rescaling and the explicit rate formula;
4. a separate division-free antipodal-only and mixed-antipodal theorem;
5. an explicit relative cone margin, coefficient bounds, inverse-quadratic
   rates, conditioning, perturbation radius, robust-row objective change, and
   actual optimal-value degradation;
6. global shared-edge cone and feasible-polytope characterization;
7. weighted centering, dense complete-graph construction, full Farkas
   alternative, strong LP duality, and complementary slackness with the actual
   AFP signs;
8. strict global feasibility and node/mass sensitivity;
9. a weighted-centered cube with every row uniquely strictly feasible but no
   global shared-edge solution, together with an exact dual certificate; and
10. a centered-clique submass mechanism that constructs sparse globally
    compatible shared-edge systems.

The isolated local convex-hull statement is treated as standard finite convex
geometry. The publication contribution is the combined sphere-specific and
global reversible package, not a renamed Euclidean positive-stencil theorem.

## 3. Explicit approach registry

The registry was kept dynamic. Routes were separated initially to expose
hidden assumptions, then redirected when several approaches converged to the
same textbook convex-hull core.

| ID | Independent route | Result | Disposition |
|---|---|---|---|
| A1 | Direct finite barycentric proof | Proved nonnegative hull membership and all-index positive coefficients iff relative interior; repetitions allowed | ADOPTED |
| A2 | Supporting-hyperplane / separation proof | Recovered the same local criterion and supplied boundary certificates | ADOPTED as audit and dual interpretation; not used as a novelty claim |
| A3 | Positive-span / Farkas shorthand | Correct only after adding normalization and relative-interior detail; concealed repetitions and antipodes | BLOCKED as an incomplete presentation |
| A4 | Oriented-matroid circuit route | Clarified minimal supports and affine dependence but did not determine the spherical normal scale | REDIRECTED into the minimal-face uniqueness theorem |
| A5 | Spherical tangent/normal decomposition | Produced the exact `sin(theta)` tangent weights, `tan(theta/2)` normal factor, and unique scale | ADOPTED |
| A6 | Treat antipodes as limiting tangent directions | Introduced division by zero and fictitious geometry | BLOCKED |
| A7 | Separate antipodal normal-budget cone | Gave the complete antipodal-only/mixed classification and boundary cases | ADOPTED |
| A8 | Barycentric inradius / support function | Produced the primal centered-ball and dual support-function margin | ADOPTED |
| A9 | Quantitative selection by unspecified compactness | Established existence but no usable minimum coefficient | BLOCKED at the unproved quantitative selection lemma |
| A10 | Explicit pointwise averaging from `-rho u_j` | Gave `lambda_j >= rho/[m(1+rho)]`, including redundant indices | ADOPTED |
| A11 | Singular-value / pseudoinverse perturbation | Gave conditioning and explicit coefficient correction | ADOPTED with full-2D or fixed-relative-span hypothesis |
| A12 | Unrestricted ambient perturbation of a 1-D relative hull | False for a perturbed antipodal tangent pair | BLOCKED; theorem restricted explicitly |
| A13 | Global edge-cone and finite Farkas route | Gave exact feasibility, dual edge block, and infeasibility certificates | ADOPTED |
| A14 | Weighted centering as global sufficiency | True for the complete graph but false on sparse graphs | FALSIFIED by the weighted-centered cube |
| A15 | Reconcile rows by independent row scaling | Impossible because each non-antipodal row's normal equation fixes its scale | BLOCKED |
| A16 | Detailed-balance cycle conditions | Useful diagnostic but not a construction for arbitrary fixed masses | RETAINED as interpretation, not the main mechanism |
| A17 | Symmetry / regular-polyhedron route | Produced exact strict examples and objective duals | ADOPTED for regression and certificates |
| A18 | Centered-clique submass decomposition | Sums complete-graph blocks on sparse permitted graphs | ADOPTED as a nontrivial global reconciliation mechanism |
| A19 | Formalize all convex analysis and LP duality immediately in Lean | Would delay the ordinary proof and duplicate large standard libraries | BLOCKED by the stage rule; exact external statements and Lean spherical consequences used instead |
| A20 | Narrow finite Lean algebra plus exact regressions | Verifies scale, antipodal budget, rate bounds, edge signs, objective gaps, and complementarity | ADOPTED |
| A21 | Assume a linear-objective optimizer is itself strictly positive | False in general; a simple square-angle case has a boundary optimizer | BLOCKED |
| A22 | Convexly robustify a boundary optimizer before correcting the perturbed balance | Gives an explicit optimum-value bound with no strict-optimizer assumption | ADOPTED |

## 4. Synthesis and redirection record

### Round 1 — independent local derivations

Direct barycentric, separation, positive-span, circuit, and spherical-coordinate
routes were compared without assuming a favored proof. They converged on a
nonnegative tangent dependence, but three hidden issues were exposed:

- ambient interior had to be replaced by relative interior;
- positive coefficients meant positivity on every indexed candidate, not only
  on a selected support;
- antipodes could not appear in a quotient by `sin(theta)`.

### Round 2 — quantitative and antipodal redirection

Once the qualitative hull proof became textbook, effort moved to the explicit
margin and antipodal structure. The compactness-only coefficient selection was
rejected because it supplied no constants. The centered-ball construction
using `-rho u_j` produced the indexed coefficient lower bound. The antipodal
normal budget was parameterized directly and audited at zero non-antipodal
spend, full spend, and strict leftover spend.

### Round 3 — global compatibility

The initial global hypothesis that centering might suffice on a sparse graph
was attacked independently through detailed balance, rank, conic separation,
and exact polyhedral examples. The cube with antipodal-pair masses supplied a
strong counterexample: centering holds and every local row is unique and
positive, yet an exact zero-edge-work Farkas field has negative target work.
This killed every route that reduced global compatibility to an unproved
local gluing lemma.

### Round 4 — constructive reconciliation and dual objectives

The complete graph was retained as the dense universal construction. A sparse
centered-clique decomposition was then proved by summing independently
centered complete-graph blocks. Rate, linear defect, peak epigraph, and
weighted residual LPs were transferred with their exact signs and
complementarity blocks.

### Round 5 — formalization, objective sensitivity, and regression

The formal work was narrowed to finite consequences that improve assurance
without postponing the ordinary proof. Exact rational tests were written first
to lock sign conventions and counterexamples; Lean modules then formalized the
scale, antipodal budget, outgoing-rate inequalities, shared-edge transpose
geometry, objective-gap identity, and componentwise complementary slackness.

A final objective audit rejected the hidden assumption that an old optimizer
must use every candidate. An optimal barycentric vector is instead mixed with
the margin-controlled vector by
`lambda_eta=(1-eta)lambda_star+eta lambda_0`. The explicit price of that
robustification is combined with the tangent right-inverse correction and the
angle Lipschitz bound, yielding the actual optimum-value estimate in the
sensitivity addendum.

## 5. Adversarial theorem audit

| Failure mode tested | Audit result |
|---|---|
| Division by `sin(theta)` at an antipode | PASS: antipodes occur only through loss `2` and a simplex budget |
| Ambient interior confused with relative interior | PASS: every theorem and margin uses the affine span; arbitrary perturbations are restricted to full 2-D or fixed span |
| Repeated tangent directions silently removed | PASS: indexed coefficients are retained; duplicate examples give explicit nonuniqueness |
| Redundant nonvertex candidates omitted from strict positivity | PASS: positive representation is required at every indexed candidate and constructed by averaging |
| Strict positivity on support confused with strict positivity on every permitted edge | PASS: boundary theorem identifies the minimal active face; all-edge strictness is equivalent to relative interior of the full indexed hull |
| Hidden assumption that the tangent hull is 2-D | PASS: qualitative theorem is relative-dimensional; only ambient perturbation theorem imposes full 2-D spanning |
| Hidden equal-mass assumption globally | PASS: nonuniform but centered cube masses falsify it |
| Weighted centering incorrectly treated as sparse sufficiency | PASS: exact Farkas counterexample has `A^T y=0`, `b dot y=-4` |
| Sign error in `A gamma=b` | PASS: edge columns, complete-graph construction, cube primal, radial dual field, and exact Python matrix all agree |
| Sign error in Farkas certificate | PASS: primal feasibility implies `b dot y=gamma dot A^T y>=0`; cube certificate is strictly negative |
| Sign error in residual LP | PASS: positive residual activates `y=-tau`; negative residual activates `y=+tau` |
| Unproved common-scale freedom used for row reconciliation | PASS: normal equation proves `c=2/Q` uniquely |
| Unquantified `O(h^-2)` used in a claimed bound | PASS: all rate and coefficient constants are explicit |
| Cone margin claimed to control coefficients without candidate count | PASS: the bound records `m` explicitly |
| Perturbation theorem applied at zero margin | PASS: rational boundary-crossing family proves that no positive radius exists |
| Objective degradation assumes a strictly positive optimizer | PASS: boundary optimizers are robustified explicitly before perturbation |
| Feasible set called a polytope despite zero edge columns | PASS: coincident-node zero columns are identified; compactness follows only after deletion |
| Generic LP citation without AFP transfer | PASS: every primal, dual, sign, edge block, residual block, and complementarity condition is written explicitly |

## 6. Exact examples and certificates

The deterministic regression suite uses `fractions.Fraction`; no tolerance is
used for its core examples.

- tangent hull outside: separator for `{e1,e2}`;
- tangent hull boundary: `(1/2,1/2,0)` on `{e1,-e1,e2}`;
- tangent hull relative interior: uniform square coefficients;
- repeated/redundant directions: two distinct all-positive dependences;
- exact spherical angular factors: `cos=3/5`, `sin=4/5`, `loss=2/5`;
- rational perturbation crossing outside/boundary/interior;
- antipodal-only simplex;
- mixed boundary and mixed strict normal-budget splits;
- globally strict equal-mass cube, `gamma=1`;
- exact rate-minimization dual `y=-(3/2)Omega`, primal=dual=24;
- weighted-centered incompatible cube;
- exact infeasibility field `y_x=(x2,x3,x1)/sqrt(3)`, edge work zero,
  target work `-4`.

Computational checks are retained only as falsification and regression tools.
The general theorems are proved independently in the ordinary proof documents.

## 7. Formalization boundary

### Lean-checked finite consequences

- constructive tangent dependence to row scaling and converse;
- positivity of the normal scale;
- uniqueness and positivity of the common scalar;
- division-free antipodal budget identities and inequalities;
- loss-window outgoing-rate bounds;
- orientation-independent shared-edge dual work;
- radial dual work and its sign;
- primal-dual objective-gap identity;
- componentwise complementary slackness;
- active-edge saturation and strict-slack inactivity.

### Precisely stated external inputs

The general finite-dimensional Farkas alternative and strong LP duality are
standard external theorems. The ordinary proof states their exact finite
hypotheses and transfers them to the AFP matrix. They were not reimplemented in
Lean because doing so would duplicate standard convex-analysis infrastructure
and delay the sphere-specific theorem.

The finite convex-hull and relative-interior equivalences are proved directly
in the ordinary theorem document rather than left as an unverified citation.

## 8. Novelty audit result

Positive/minimal-stencil theory already contains local positive-cone and
Farkas geometry, and discrete spherical Laplacian theory already contains
positive spherical operators and low eigenmodes. Therefore the following are
not claimed as standalone novelty:

- finite convex-hull membership;
- generic positive-span language;
- the general Farkas theorem;
- the general strong LP-duality theorem;
- the existence of positive spherical Laplacians in all settings.

The candidate contribution is the exact combined package: spherical
coordinate eigenmap balance; tangent/normal angular structure; unique scale;
division-free antipodes; quantitative relative margin; positive masses;
shared-edge reversibility; sparse global compatibility; exact dual geometry;
centered local/global incompatibility; and centered-clique reconciliation.

## 9. Repository map

### Added

- `.github/workflows/afp-spherical-feasibility.yml`
- `AFPBarrier/SphericalFeasibilityAlgebra.lean`
- `AFPBarrier/QuantitativeSphericalFeasibility.lean`
- `AFPBarrier/GlobalSharedEdgeDuality.lean`
- `docs/SPHERICAL_FEASIBILITY_SHARED_EDGE_THEOREM.md`
- `docs/SPHERICAL_FEASIBILITY_OPTIMAL_VALUE_SENSITIVITY.md`
- `docs/SPHERICAL_FEASIBILITY_THEOREM_MAP.md`
- `docs/P0_M1_SPHERICAL_FEASIBILITY_STAGE_REPORT.md`
- `pure_math/tests/test_spherical_feasibility.py`

### Updated

- `AFPBarrier.lean`
- `docs/CLAIM_MATRIX.md`
- `docs/CONJECTURE_REGISTER.md`
- `docs/PURE_MATH_PRIOR_ART_MAP.md`
- `pure_math/README.md`

## 10. Verification record

- Exact rational regression command:
  `python3 pure_math/tests/test_spherical_feasibility.py`
- Deterministic output:
  `exact spherical feasibility regressions: PASS`
- Lean toolchain: Lean `v4.30.0`, Mathlib `v4.30.0`
- Workflow protections:
  - exact regression suite;
  - forbidden-placeholder / user-axiom grep on the stage modules;
  - full `lake build`;
  - independent `nanoda` kernel check with sorry disallowed.

The theorem-code validation completed successfully on 2026-08-01:

- GitHub Actions workflow run: `30714223520`
- verification job: `91406932184`
- validation-branch head: `1eefd609e1e5495d465528e06a7152535922c9ad`
- pull-request merge ref checked by Actions:
  `0bab8ec31d812813f4d01bf73f06afae057fd46c`
- exact regressions: PASS
- forbidden-placeholder / user-axiom check: PASS
- `lake build`: PASS
- `nanoda` independent kernel check: PASS
- sorry declarations accepted: zero

Subsequent changes before merge are documentation/control updates only; the
workflow is configured to rerun on both the validation branch and the target
branch.

# P0/M1 stage report — spherical positive feasibility and shared-edge duality

## 1. Baseline and scope

- Repository: `FusionSandwich/Testing`
- Target branch: `agent/afp-pure-math-p0-m1`
- Verified checkpoint: `4efef67a20cdb8b2437cad093ccc16bcd0f17796`
- Isolated implementation branch: `agent/afp-spherical-feasibility-validation`
- Frozen transport archive: `archive/afp-gate6-spatial-multigroup-verified`
  at `515f1aae6c20bd85711c90b5c1c21b4905252d01`

The target branch was identical to the checkpoint when this stage began. The
stage changes only the pure-mathematics package, proof-control documents,
exact regressions, and one dedicated verification workflow. It does not modify
the frozen archive and adds no transport, Radiant, HTS, multigroup, or
spatial-solver work.

## 2. Mathematical outcome

The ordinary proof is in
`SPHERICAL_FEASIBILITY_SHARED_EDGE_THEOREM.md`, with the perturbed-optimum
argument in `SPHERICAL_FEASIBILITY_OPTIMAL_VALUE_SENSITIVITY.md`. Together they
establish the following finite theorem package.

### 2.1 Non-antipodal local feasibility

For a node `Omega_i` and non-antipodal neighbors

```text
Omega_j = cos(theta_j) Omega_i + sin(theta_j) u_j,
0 < theta_j < pi,
u_j in T_{Omega_i} S^2,
```

a nonnegative degree-one-exact row exists exactly when zero belongs to the
indexed tangent convex hull. A row positive on every permitted indexed edge
exists exactly when zero belongs to the relative interior of that hull in its
affine span. Repeated tangent directions and redundant nonvertex candidates
are retained rather than deduplicated.

For a normalized tangent dependence

```text
lambda_j >= 0,
sum_j lambda_j = 1,
sum_j lambda_j u_j = 0,
```

define

```text
Q(lambda) = sum_j lambda_j (1-cos(theta_j))/sin(theta_j).
```

Then `Q(lambda)>0`, the normal equation fixes one and only one positive common
scale, and the row is

```text
a_j = 2 lambda_j /
      [sin(theta_j) sum_k lambda_k(1-cos(theta_k))/sin(theta_k)].
```

Let `F` be the minimal face of the tangent hull containing zero. The normalized
dependence, and hence the row, is unique exactly when the indexed points in
`F` are affinely independent. Repetitions or redundant indexed points in `F`
therefore produce nonuniqueness.

### 2.2 Antipodal classification

Antipodal neighbors are treated separately. They receive no tangent direction
and never occur in a quotient by `sin(theta)`.

For non-antipodal tangent weights `b_j=a_j sin(theta_j)`, set

```text
D(b) = sum_j b_j (1-cos(theta_j))/sin(theta_j).
```

A mixed nonnegative row is equivalent to

```text
b_j >= 0,
sum_j b_j u_j = 0,
D(b) <= 2,
```

with non-antipodal rates `a_j=b_j/sin(theta_j)` and total antipodal rate

```text
t = 1 - D(b)/2.
```

The antipodal rates form a nonnegative simplex of total mass `t`. This yields:

- antipodal-only rows are exactly the simplex `sum_p a_p=1`;
- mixed nonnegative feasibility is automatic when an antipode is permitted;
- strict positivity on every non-antipodal candidate is equivalent to zero
  lying in the relative interior of the non-antipodal tangent hull;
- strict positivity on every antipodal candidate additionally requires
  `D(b)<2` so that positive antipodal budget remains; and
- relative-boundary tangent hulls permit only the minimal active face and
  cannot give positivity on every non-antipodal candidate.

### 2.3 Quantitative margin and robustness

In the relative span `L`, the local margin is

```text
rho = sup {r : B_L(0,r) subset conv{u_j}}
    = min_{v in L, ||v||=1} max_j <v,u_j>.
```

It is positive exactly under relative-interior strict feasibility. For `m`
indexed candidates, the proof constructs a normalized balancing dependence
with

```text
lambda_j >= delta = rho/[m(1+rho)]
```

for every index, including repeated and redundant candidates.

Under

```text
0 < c1 <= c2,
c1 h <= theta_j <= c2 h,
0 < h <= h0,
c2 h0 <= pi/2,
kappa0 = sin(c2 h0/2)/(c2 h0/2),
```

the loss window alone gives the explicit outgoing-rate bounds

```text
4/(c2^2 h^2) <= sum_j a_j
                 <= 4/(kappa0^2 c1^2 h^2).
```

For the selected margin-controlled row, every coefficient additionally obeys

```text
4 delta/(c2^2 h^2) <= a_j
                      <= 4/(kappa0^2 c1^2 h^2),
```

with the sharper upper factor `1-(m-1)delta` also recorded in the theorem.
The proof gives explicit singular-value and balance-system conditioning bounds,
a direction/angle perturbation radius, coefficient and objective Lipschitz
constants, and an actual optimal-value estimate obtained by robustifying a
possibly boundary optimizer before applying the right-inverse correction.

The lower-dimensional limitation is explicit: relative-interior feasibility
in a one-dimensional tangent span is robust only for span-preserving
perturbations. Arbitrarily small ambient perturbations can destroy it.

### 2.4 Global reversible shared-edge feasibility

For every undirected permitted edge `e={p,q}`, the shared-edge matrix column is

```text
(z_e)_p = Omega_q-Omega_p,
(z_e)_q = Omega_p-Omega_q,
```

and zero elsewhere. With positive masses `w_i`, the target is

```text
A gamma = b,
gamma >= 0,
b_i = -2 w_i Omega_i.
```

The global system is feasible exactly when `b` belongs to the cone generated
by the edge columns. After zero columns from coincident endpoints are removed,
the feasible set is a compact polytope. Every feasible point satisfies the
exact conductance budget

```text
sum_e gamma_e (1-Omega_p.Omega_q) = sum_i w_i.
```

Weighted centering

```text
sum_i w_i Omega_i = 0
```

is necessary. On the complete graph it is sufficient, with the positive
construction

```text
gamma_ij = 2 w_i w_j / sum_k w_k.
```

The full finite Farkas alternative is transferred with the AFP sign convention:
exactly one of

```text
exists gamma >= 0, A gamma=b
```

or

```text
exists y, A^T y >= 0 and b.y < 0
```

holds. For `e={p,q}`,

```text
(A^T y)_e = (y_p-y_q).(Omega_q-Omega_p).
```

Thus the dual edge block is the first variation of the squared chord length,
and a negative target work is an exact incompatibility certificate.
Strict positivity on every shared edge is equivalent to
`b in ri(cone{z_e})`.

Strong finite-dimensional LP duality and complementary slackness are written
with the actual AFP matrices for linear rate/defect objectives, peak epigraph
formulations, and weighted `l1` residual formulations. For

```text
min c.gamma subject to A gamma=b, gamma>=0,
```

the dual is

```text
max b.y subject to A^T y <= c,
```

and every optimal pair satisfies

```text
gamma_e [c_e-(A^T y)_e] = 0.
```

The global perturbation theorem states the necessary range-compatibility
hypothesis and gives an explicit correction bound in terms of the minimum
strict edge coefficient and the smallest positive singular value.

### 2.5 Exact local/global separation and reconciliation

For cube nodes `Omega_x=x/sqrt(3)`, `x in {+-1}^3`, with cube edges, every row
has the unique strictly positive local solution `a=1` on its three incident
edges. Give mass `2` to the antipodal pair `+++` and `---`, and mass `1` to the
other nodes. Weighted centering still holds, but no shared-edge solution
exists. The exact dual field

```text
y_x = (x_2,x_3,x_1)/sqrt(3)
```

satisfies

```text
A^T y = 0,
b.y = -4.
```

For the equal-mass cube, `gamma_e=1` is globally strict. With edge cost `2`,
`y_i=-(3/2)Omega_i` saturates every dual constraint and gives exact primal and
dual value `24`.

A nontrivial sparse reconciliation mechanism is also proved. If permitted
cliques carry positive submasses that are separately centered and sum to the
prescribed node masses, then the complete-graph conductance formula applied
inside each clique and summed over cliques gives a globally exact shared-edge
solution on their union.

## 3. Approach registry and blocked routes

Independent route families were tracked explicitly so that hidden assumptions
could be exposed rather than absorbed into a single convex-hull proof.

| Route | Outcome |
|---|---|
| Direct indexed barycentric geometry | Adopted for hull and all-index relative-interior equivalences |
| Supporting-hyperplane separation | Adopted for boundary and infeasibility audits |
| Unqualified positive-span/Farkas shorthand | Blocked because it concealed normalization, repetitions, and antipodes |
| Oriented-matroid circuits | Redirected to minimal-face support and uniqueness |
| Spherical tangent/normal decomposition | Adopted for angular factors and unique scale |
| Antipodes as limiting tangent directions | Rejected because it creates fictitious directions and division by zero |
| Separate antipodal budget cone | Adopted for the complete mixed classification |
| Inradius/support-function margin | Adopted for primal/dual margin equivalence |
| Compactness-only coefficient selection | Blocked because it supplied no explicit coefficient bound |
| Pointwise averaging from `-rho u_j` | Adopted for `rho/[m(1+rho)]` |
| Singular-value/right-inverse perturbation | Adopted with full-span or fixed-relative-span hypotheses |
| Unrestricted ambient perturbation of a 1-D hull | Falsified by a perturbed antipodal tangent pair |
| Global edge-cone/Farkas route | Adopted for feasibility and certificates |
| Weighted centering as sparse sufficiency | Falsified by the weighted-centered cube |
| Independent row rescaling as reconciliation | Blocked because the normal equation fixes every row scale |
| Detailed-balance cycle conditions | Retained as diagnostics, not a universal construction |
| Symmetric exact examples | Adopted for strict feasibility and primal/dual certificates |
| Centered-clique submass decomposition | Adopted as the constructive sparse mechanism |
| Immediate full convex-analysis formalization in Lean | Deferred to avoid duplicating standard libraries and delaying the ordinary proof |
| Narrow finite Lean algebra plus exact regressions | Adopted |
| Assume an optimizer is strictly positive | Falsified by boundary optima |
| Convexly robustify the optimizer before correction | Adopted for the optimum-value theorem |

A callable multiagent-v2 runtime was not exposed in this execution
environment. The registry, independent derivations, counterexample searches,
and adversarial checks were therefore maintained explicitly through separate
reasoning routes and tool-assisted audits. This report does not mislabel that
process as a literal multiagent-v2 execution.

## 4. Adversarial audit

The final package was checked against the required failure modes:

- no division by `sin(theta)` occurs at an antipode;
- every interior statement uses relative rather than ambient interior;
- repeated and redundant indexed directions remain present;
- all-edge positivity is distinguished from positivity only on an active
  support;
- lower-dimensional robustness is not promoted to unrestricted ambient
  robustness;
- masses are not assumed equal;
- weighted centering is not promoted to sparse global sufficiency;
- the signs in `A gamma=b`, `A^T y`, Farkas certificates, residual duals, and
  complementary slackness agree across proofs and exact examples;
- the common row scale is proved unique rather than treated as a gluing
  degree of freedom;
- every inverse-quadratic assertion has explicit constants;
- candidate count `m` appears in the minimum-coefficient bound;
- zero-margin cases are excluded from positive perturbation radii;
- optimal-value sensitivity does not assume a strictly positive optimizer;
- compactness excludes zero edge columns; and
- generic Farkas/LP citations are transferred to the actual AFP matrices and
  sign conventions.

## 5. Exact examples and regression role

`pure_math/tests/test_spherical_feasibility.py` uses exact rational arithmetic
for the core examples. It covers tangent hulls outside, on the boundary, and
in the relative interior; repeated and redundant directions; rational angular
rescaling; antipodal-only and mixed budgets; perturbations crossing the
feasibility boundary; the weighted-centered incompatible cube; and the
strict equal-mass cube with exact primal and dual certificates.

These tests are falsification and regression tools. They are not used as
proofs of the general theorems.

## 6. Formalization boundary

Lean checks the constructive row conversion, positivity and uniqueness of the
normal scale, division-free antipodal budget identities, finite loss-window
rate inequalities, shared-edge transpose geometry, dual objective-gap
identity, and componentwise complementary slackness.

The general finite Farkas alternative and strong LP duality remain precisely
stated standard external inputs. Their spherical consequences and certificate
soundness are formalized. The finite convex-hull and relative-interior
statements are proved directly in the ordinary theorem document.

The stage modules contain no `sorry`, `admit`, `sorryAx`, or user-declared
axioms.

## 7. Novelty audit

Finite convex-hull membership, generic Farkas alternatives, and Euclidean
positive-stencil existence are treated as prior mathematics rather than
standalone contributions. The candidate contribution is the combined package:

- the spherical coordinate eigenmap constraint;
- tangent/normal angular structure and unique scaling;
- division-free antipodal classification;
- quantitative relative margin and perturbation constants;
- positive masses and shared-edge reversibility;
- exact sparse global compatibility and incompatibility theory;
- geometric dual interpretation and complementary slackness; and
- centered-clique reconciliation.

## 8. Repository map

Added:

- `.github/workflows/afp-spherical-feasibility.yml`
- `AFPBarrier/SphericalFeasibilityAlgebra.lean`
- `AFPBarrier/QuantitativeSphericalFeasibility.lean`
- `AFPBarrier/GlobalSharedEdgeDuality.lean`
- `docs/SPHERICAL_FEASIBILITY_SHARED_EDGE_THEOREM.md`
- `docs/SPHERICAL_FEASIBILITY_OPTIMAL_VALUE_SENSITIVITY.md`
- `docs/SPHERICAL_FEASIBILITY_THEOREM_MAP.md`
- `docs/P0_M1_SPHERICAL_FEASIBILITY_STAGE_REPORT.md`
- `pure_math/tests/test_spherical_feasibility.py`

Updated:

- `AFPBarrier.lean`
- `docs/CLAIM_MATRIX.md`
- `docs/CONJECTURE_REGISTER.md`
- `docs/PURE_MATH_PRIOR_ART_MAP.md`
- `pure_math/README.md`

## 9. Durable verification and acceptance record

The dedicated workflow is the authoritative acceptance gate. A commit is
accepted only when all of the following pass on that exact head:

1. exact arithmetic regressions;
2. source rejection of proof placeholders and user axioms in the stage
   modules;
3. full Lean 4.30.0 / Mathlib 4.30.0 `lake build`; and
4. independent `nanoda` checking of the explicitly exported stage roots
   `AFPBarrier.QuantitativeSphericalFeasibility` and
   `AFPBarrier.GlobalSharedEdgeDuality`.

The first stage root imports `SphericalFeasibilityAlgebra`, which imports
`LocalSphericalFeasibility`; the second covers the global duality module. The
two exports therefore cover all four stage modules without pulling unrelated
transport-era modules into this pure-mathematics validation boundary.

The nanoda permitted-axiom list contains only `propext`, `Classical.choice`,
`Quot.sound`, and `Lean.trustCompiler`; it does not permit `sorryAx`. Nanoda is
configured to ignore a bare prelude declaration of an unpermitted axiom but to
fail if any checked declaration actually depends on it. This is paired with
the source-level placeholder rejection.

Concrete workflow, job, head, and merge-commit identifiers are recorded in the
pull request and GitHub Actions rather than hard-coded here, so this report
does not become false whenever documentation metadata advances the branch.
The same workflow is configured for both the isolated implementation branch
and the target branch, providing a post-integration check as well as the PR
check.

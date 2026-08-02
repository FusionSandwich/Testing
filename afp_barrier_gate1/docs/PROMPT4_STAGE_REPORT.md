# Prompt 4 stage report — sharp barriers, extremals, and final synthesis

## 1. Repository and branch isolation

```text
repository: FusionSandwich/Testing
Prompt 4 target branch:
    agent/afp-pure-math-p0-m1
Prompt 4 starting target SHA:
    47ef59b0463ecd4bd7a18a3301f29b14f9777c20
Prompt 4 development branch:
    agent/afp-pure-math-p4-sharp-barriers-extremal-synthesis
Prompt 4 pull request:
    PR #24
immutable archive:
    archive/afp-gate6-spatial-multigroup-verified
    515f1aae6c20bd85711c90b5c1c21b4905252d01
```

Before the Prompt 4 branch was created, the target was verified to equal the
Prompt 3 merge commit exactly. The separate Prompt 3 integration-record branch
and PR #23 were inspected and left untouched. No existing branch was reset,
force-pushed, rebased, or overwritten.

## 2. Mandatory theorem matrix

| Requirement | Result | Status | Authoritative support |
|---|---|---|---|
| Polar-rate expansion through constant term | exact coefficients `8/pi^4`, `10/(3pi^2)`, `13/45` | PASS | Prompt 4 Theorem 1.2; Lean coefficient algebra |
| Polar-rate rigorous remainder | for `N>=2`, remainder in `[0,pi^2/(48N^2)]` | PASS | Mittag--Leffler tail proof and exact rational audit |
| Polar-quality expansion | `N^2/pi^2+7/12` | PASS | Prompt 4 Theorem 1.3 |
| Polar-quality rigorous remainder | for `N>=2`, remainder in `[0,pi^2/(12N^2)]` | PASS | Theorem 1.3 and exact audit |
| Fixed unreduced graph lower bound | exact polar row forced for every degree-one-exact choice | PASS / SHARP | Prompt 4 Theorem 2.1; `squarePolar_rates_forced` |
| Optimizer symmetry issue | no symmetry assumption; left/right equality derived from transverse balance | PASS | direct coordinate proof |
| Sharp graph-class leading constant | exact minimax and leading constant `8/pi^4` | PASS / SHARP | Corollary 2.2 plus existing positive reversible construction |
| Universal rate barrier | `epsilon<=Ch^2 => r>=4/(Ch^2)` | PASS | Theorem 3.1; Lean theorem |
| Maximal-net loss-window transfer | exact constants transferred | PASS CONDITIONAL | Theorem 3.2; existing Lean loss-window theorem |
| Delaunay/exact-mode boundary | treated as external geometric input | PASS | assumptions table and prior-art map |
| Well-posed extremal problem | rate, degree, locality, separation, covering, mesh ratio, masses, positivity, reversibility controlled | PASS | Prompt 4 Section 4 |
| Positive extremal lower bound | `E_K>=4/(RK)`, `C*>=4/R` | PASS | Theorem 4.1; Lean finite inequality |
| Finite-order minimizer | compactness in every nonempty fixed-`K` class | PASS | Theorem 4.2 |
| Product/quasi-uniform separation | product family eventually violates every linear rate cap | PASS | Corollary 4.3 |
| A priori feasible-cone anisotropy | exact projective reduction and constant `A_i` | PASS | Theorems 5.1–5.2 |
| Rigorous optimization reformulation | fixed-mean slice is a finite LP | PASS | equation (5.4) |
| Explicit dual certificate | `alpha+beta ell_j+z dot v_j <= ell_j^2` | PASS | equation (5.7), finite LP duality |
| Equality/sharpness examples | one-loss-level equality, two-opposite-direction formula, polar cone | PASS | Corollary 5.3 and Examples 5.4–5.5 |
| Delsarte/Gegenbauer branch | no new certificate after alias audit | BLOCKED | approach registry |
| Bakry--Émery branch | only a one-function identity, no full curvature theorem | KILLED | Prompt 4 Section 6.2 |
| Compact homogeneous-space branch | no material strengthening | DEFERRED | approach registry |
| Discrete transport branch | no metric-free contraction claim | DEFERRED | approach registry |
| Reduced-ring branch | perfect-matching coupling class impossible with varying populations | PASS FOR STATED CLASS | incidence theorem and Lean support |
| Formal discrete geometry | finite support only; no broad library | PASS / BOUNDED | `SharpProductBarriers.lean` |
| Final paper theorem hierarchy | sampled covariance theorem remains central | PASS | `FINAL_PURE_MATH_THEOREM_PACKAGE.md` |
| Exact assumptions table | complete theorem-by-theorem control | PASS | `PURE_MATH_ASSUMPTIONS_TABLE.md` |
| Counterexample catalogue | permanent regression boundaries assembled | PASS | `PURE_MATH_COUNTEREXAMPLE_CATALOGUE.md` |
| Manuscript abstract | independent of project terminology | PASS | `PURE_MATH_MANUSCRIPT_ABSTRACT.md` |

## 3. Main mathematical results

### 3.1 Uniform polar expansions

For every integer `N>=2`,

```text
0 <= r_polar(N)
     - [(8/pi^4)N^4 + (10/(3pi^2))N^2 + 13/45]
  <= pi^2/(48N^2),
```

and

```text
0 <= Q_pole(N) - [N^2/pi^2 + 7/12]
  <= pi^2/(12N^2).
```

The proof differentiates the paired cotangent Mittag--Leffler expansion and
uses a positive exact tail. A formal computer-algebra series is retained only
as an independent coefficient regression.

### 3.2 Exact fixed-graph obstruction

At a polar vertex, the coordinate equations force

```text
inward meridional rate = 1/(2 sin^2 h),
each azimuthal rate   = 1/(4 sin^4 h).
```

No ring-symmetry, equal-mass, reversible-row, or optimizer averaging assumption
enters this local solve. The existing positive reversible product construction
attains the forced row and has its maximum there. Hence the exact graph-class
minimax value is the polar expression, with sharp leading constant `8/pi^4`.

### 3.3 Extremal and anisotropy theory

The rate-capped extremal quantity has lower bound `4/R` after multiplication by
`K`, and each nonempty finite-order class has a minimizer. The fixed product
graph has quadratic stiffness in node count and is eventually excluded from
every linear-rate class.

For each row, the normalized tangent-balanced feasible polytope yields

```text
Q=s_2(p)/m(p)^2.
```

At fixed mean loss, minimizing the second moment is a finite LP. Its exact dual
supplies a computable certificate over the entire feasible cone. This corrects
the false premise that `Q` is determined by node geometry without conductance
optimization.

## 4. Formalization

New module:

```text
AFPBarrier/SharpProductBarriers.lean
```

Formalized content:

- exact polar quality algebra;
- unique polar rate solution;
- exact total polar rate;
- quartic grid lower bound;
- coefficient extraction in the half-step and grid variables;
- universal inverse-quadratic rate implication;
- finite extremal lower bound;
- two-loss anisotropy equality; and
- biregular/perfect-matching incidence.

The aggregate import and focused axiom audit include all accepted declarations.
The infinite-series remainder, generic LP duality, compactness, and graph-class
transfer remain ordinary proofs and are not represented as axioms.

## 5. Exact regression

New audit:

```text
pure_math/barriers/prompt4_sharp_barrier_audit.py
```

It verifies exactly:

- polar rate and quality coefficients;
- the positive cosecant tail constant;
- the rate and quality remainder-transfer constants;
- unique polar rate solving;
- the exact polar quality;
- universal and quasi-uniform constants;
- the product/linear-rate separation threshold;
- two-loss anisotropy;
- a finite sliced-LP example; and
- reduced-ring incidence.

No fitted slope or floating rank threshold is used as mathematical evidence.

## 6. Independent and adversarial audits

Literal multiagent-v2 was unavailable and is not claimed. The independent
routes and exact adversarial cases are committed in
`PROMPT4_APPROACH_REGISTRY.md`.

The principal adversarial checks were:

- unequal left/right polar rates before solving;
- unequal masses;
- nonreversible local rows;
- formal series without remainder;
- collapsing/dense/nonlocal extremal configurations;
- conductance reweighting of `Q`;
- sampling aliases in harmonic LP routes;
- known positive-curvature graph warnings;
- perfect matching versus general split/merge ring couplings; and
- branch/workflow scope isolation.

## 7. Publication boundary

The product-grid result is a sharp supporting theorem, not the central paper
claim. The central result remains the genuine sampled quadratic exact-space
factorization and structural rigidity theorem. The final hierarchy does not
claim novelty for Cauchy--Schwarz, finite LP duality, partial fractions,
spherical Delaunay theory, spherical designs, association schemes, curvature
frameworks, or convex rigidity.

The pure-math paper passes the stated kill criterion because the central theorem
is not merely ambient dimension minus constraint rank: the residual factors
through sampling, the sampling kernel is automatically contained in the form
kernel, and positive structural hypotheses yield sharp rigidity with exact
alias and signed boundary classifications.

## 8. Repository completion gates

Before Prompt 4 may be closed, the exact final branch head must pass:

```text
AFP Prompt 4 sharp barriers
AFP Prompt 3 rigidity
AFP quadratic covariance
AFP spherical feasibility
AFP Pure Mathematics
```

Each applicable workflow must establish:

- literal expected/actual checkout equality;
- every deterministic Prompt 1–4 audit;
- full Lean build;
- focused axiom audit;
- aggregate placeholder and singular/plural user-axiom scan;
- independent nanoda validation;
- immutable archive equality;
- pure-math-only changed paths; and
- `git diff --check`.

Prompt 4 is not certified closed until these final-head gates and target
integration provenance are recorded.

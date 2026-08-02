# Prompt 4 integration and final-synthesis record

## 1. Immutable scope and branch isolation

```text
repository=FusionSandwich/Testing
pure_math_target=agent/afp-pure-math-p0-m1
prompt4_start_commit=47ef59b0463ecd4bd7a18a3301f29b14f9777c20
prompt4_development_branch=agent/afp-pure-math-p4-sharp-barriers-extremal-synthesis
prompt4_integration_record_branch=agent/afp-pure-math-p4-integration-record
immutable_archive_branch=archive/afp-gate6-spatial-multigroup-verified
immutable_archive_commit=515f1aae6c20bd85711c90b5c1c21b4905252d01
```

Prompt 4 was developed on a new branch from the exact Prompt 3 target merge.
No existing development, closeout, archive, or target branch was rebased,
force-pushed, reset, or overwritten.

The separate Prompt 3 documentation branch

```text
agent/afp-pure-math-p3-integration-record
```

and its PR #23 were inspected before Prompt 4 began and were not modified by
Prompt 4.

The immutable transport archive remained exactly at
`515f1aae6c20bd85711c90b5c1c21b4905252d01`. The complete Prompt 4 theorem
diff is restricted to:

```text
.github/workflows/afp-prompt4-sharp-barriers.yml
.github/workflows/afp-prompt3-rigidity.yml
.github/workflows/afp-quadratic-covariance.yml
.github/workflows/afp-spherical-feasibility.yml
.github/workflows/afp-pure-math.yml
afp_barrier_gate1/AFPBarrier.lean
afp_barrier_gate1/AFPBarrier/*.lean
afp_barrier_gate1/pure_math/**
afp_barrier_gate1/docs/**
```

No transport, Radiant, HTS, evaluated-material, multigroup, spatial-solver, or
production-solver path was changed.

## 2. Accepted implementation and merge provenance

```text
prompt4_implementation_commit=ae5b4c7635f917ea7abb6feb58717cc0173b4cd7
prompt4_pull_request=24
prompt4_merge_commit=d1a31d195ae3c371b3f9cee29bd7ed34d1ff0994
prompt4_merge_tree=e192275e48bf38bf899483e8c27c0c3a206edf64
```

PR #24 was merged with a normal merge commit. The target history was not
rewritten.

The accepted implementation contains:

- rigorous polar-rate and polar-quality expansions with explicit `N>=2`
  remainder bounds;
- the uniquely forced polar row on the fixed unreduced square product graph;
- the exact graph-class minimax rate and sharp leading constant `8/pi^4`;
- the universal inverse-quadratic rate barrier and quasi-uniform loss-window
  transfer;
- the constrained finite/asymptotic extremal problem, positive lower bound,
  compactness theorem, and product/quasi-uniform separation;
- the projective feasible-cone anisotropy formula, sliced linear program, exact
  dual certificate, and sharp examples;
- the bounded high-ambition branch decisions;
- the Lean finite core and exact symbolic audit; and
- the final pure-mathematics theorem synthesis, assumptions table,
  counterexample catalogue, prior-art map, and manuscript abstract.

## 3. Exact implementation-head verification

All five required workflows passed on the literal implementation commit
`ae5b4c7635f917ea7abb6feb58717cc0173b4cd7`:

| Workflow | Run | Job | Result |
|---|---:|---:|---|
| AFP Prompt 4 sharp barriers | `30765107178` | `91542306867` | SUCCESS |
| AFP Pure Mathematics | `30765107143` | `91542312702` | SUCCESS |
| AFP quadratic covariance | `30765107144` | `91542297973` | SUCCESS |
| AFP Prompt 3 rigidity | `30765107141` | `91542308937` | SUCCESS |
| AFP spherical feasibility | `30765107139` | `91542285021` | SUCCESS |

These runs established:

- every deterministic Prompt 1--4 exact audit;
- full Lean 4.30 / Mathlib build;
- focused axiom audit;
- aggregate `sorry`, `admit`, `sorryAx`, singular `axiom`, and plural `axioms`
  source scans;
- independent nanoda validation for the accepted declaration sets;
- immutable archive equality;
- pure-math-only changed paths; and
- `git diff --check`.

## 4. Exact merged-target verification

The repository-wide pure-mathematics workflow checked out the literal Prompt 4
merge commit and tree:

```text
actual_head=d1a31d195ae3c371b3f9cee29bd7ed34d1ff0994
actual_tree=e192275e48bf38bf899483e8c27c0c3a206edf64
```

Accepted merged-target workflow:

```text
workflow=AFP Pure Mathematics
run=30765477344
job=91543293206
result=SUCCESS
```

The merged-target run repeated every Prompt 1--4 exact audit, built 3,103 Lean
jobs, ran the focused and aggregate axiom/placeholder policies, verified the
immutable archive, checked the complete pure-math scope, and passed
`git diff --check`.

The reproducibility artifact from that run is:

```text
artifact_id=8838834376
artifact_sha256=d388a87c71755679a3023ec750013a13a7eec6d9f00235e5b0cce6a31e3b2b81
```

## 5. Mathematical acceptance summary

### 5.1 Sharp asymptotics

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

The proof uses a positive differentiated cotangent Mittag--Leffler tail; a
formal computer-algebra series is retained only as an independent regression.

### 5.2 Exact fixed-graph obstruction

At every polar-ring vertex, the three coordinate equations force

```text
inward meridional rate = 1/(2 sin^2 h),
each azimuthal rate   = 1/(4 sin^4 h).
```

The proof starts from asymmetric azimuthal rates and derives their equality.
It does not assume equal masses, ring-symmetric conductances, or reversibility
for the local lower bound. The existing positive reversible construction
attains the forced row, proving the exact graph-class minimax value and sharp
leading constant `8/pi^4`.

### 5.3 Extremal and cone theory

The accepted constrained class controls rate, degree, edge locality,
separation, covering radius, mesh ratio, masses, positivity, reversibility, and
exact coordinate balance. It satisfies

```text
E_K>=4/(R K),
liminf K E_K>=4/R,
```

and every nonempty fixed-`K` closed class has a minimizer.

The entire feasible row cone is represented projectively by tangent-balanced
probability vectors. At fixed mean loss, the second-moment minimization is a
finite linear program whose dual is

```text
maximize alpha+beta m
subject to
alpha+beta ell_j+z dot v_j <= ell_j^2.
```

This is the accepted conductance-aware anisotropy theorem; `Q` is not treated
as a function of node geometry alone.

### 5.4 Final publication hierarchy

The central theorem remains the genuine sampled quadratic covariance
factorization and structural rigidity package. Prompt 4 supplies sharp
supporting product-graph, extremal, and anisotropy results. The final synthesis
is independent of AFP terminology and separates standard inputs from project
contributions.

## 6. Authoritative files

```text
afp_barrier_gate1/pure_math/FINAL_PURE_MATH_THEOREM_PACKAGE.md
afp_barrier_gate1/pure_math/barriers/SHARP_PRODUCT_GRAPH_BARRIERS.md
afp_barrier_gate1/AFPBarrier/SharpProductBarriers.lean
afp_barrier_gate1/pure_math/barriers/prompt4_sharp_barrier_audit.py
afp_barrier_gate1/docs/PROMPT4_APPROACH_REGISTRY.md
afp_barrier_gate1/docs/PROMPT4_STAGE_REPORT.md
afp_barrier_gate1/docs/PROMPT4_THEOREM_MAP.md
afp_barrier_gate1/docs/PURE_MATH_ASSUMPTIONS_TABLE.md
afp_barrier_gate1/docs/PURE_MATH_COUNTEREXAMPLE_CATALOGUE.md
afp_barrier_gate1/docs/PURE_MATH_MANUSCRIPT_ABSTRACT.md
afp_barrier_gate1/docs/CLAIM_MATRIX.md
afp_barrier_gate1/docs/CONJECTURE_REGISTER.md
afp_barrier_gate1/docs/PURE_MATH_PRIOR_ART_MAP.md
afp_barrier_gate1/docs/THEOREM_TO_FILE_MAP.md
afp_barrier_gate1/pure_math/README.md
```

## 7. Final metadata rule

A Git commit cannot contain its own final SHA and tree without a
self-referential hash problem. This committed record therefore fixes the
accepted theorem implementation, merge commit/tree, and merged-target
verification. The final documentation integration SHA/tree and its exact-head
workflow identifiers are recorded in the integration-record PR discussion and
final return after that documentation-only PR is merged.

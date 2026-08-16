# P1E stage report — matching-order positive construction

## Frozen input and accepted work line

P1E starts from the exact accepted P1D archive:

```text
P1D archive:
    archive/afp-publication-p1d-quantitative-stability-verified

P1D commit:
    368e709c15efc1d1d25ad063d79ebbd8feecd9ed

P1D tree:
    cce67cdcc6c5ee360c1894702197b84e850bed64

P1E branch:
    agent/afp-publication-p1e-asymptotic-family-368e709c

Reserved P1E archive after exact-head verification:
    archive/afp-publication-p1e-asymptotic-family-verified
```

P1E is required to be a normal non-merging descendant of the frozen P1D
commit. P1D/P1C/P1B/P1A and every earlier accepted archive remain read-only.
The literal P1E commit and tree, workflow execution, artifacts, digests, and
archive equality may be recorded only after the dedicated exact-head gate has
run on that literal release commit.

## Current publication status

```text
MATHEMATICAL_THEOREM_ACCEPTED
EXACT_HEAD_WORKFLOW_NOT_YET_RUN
```

The ordinary `d=3` proof has passed the final independent rational-Cauchy and
first-row hostile audit. The exact-head workflow has not yet run on a frozen
release commit, so this report makes no workflow-success, artifact, digest, literal
commit/tree, or immutable-archive claim.

## Accepted theorem boundary

The authoritative theorem source is
`P1E_SHORT_GAP_S2_CONSTRUCTION.md`. Its construction is a
reflection-symmetric adaptive ring family on `S^2`, hence only ambient
dimension `d=3`. The theorem has the following exact data:

```text
L_h 1 = 0,
L_h Omega = -2 Omega,
gamma_ij = gamma_ji >= 0,
B_i = 0,
R_2 A(i) = c_i S_2 A(i) row by row,
r_max(L_h) <= R_3 h^-2,
mathfrak D_2(L_h) <= C_3 h^2,

R_3 = 64 pi^2,
C_3 = 75/2,
c_3 = 6/R_3 = 3/(32 pi^2).
```

These sharp constants are accepted for the stated unperturbed `d=3` family
and are not asserted for `d>3`. Proposition 7.3 additionally proves a
fixed-level support-preserving theorem. For each `M_0=2^80` production level, the finite
block Jacobian is nonsingular at the strictly positive base solution, so a
computable level-dependent latitude radius preserves the fixed ring counts,
phases, masks, horizontal jumps, pole/equator data, reflection, shared
incidence, reversibility and exact coordinate fidelity. On a sufficiently
small such neighborhood `r_max<=1024 h_J^-2` and
`mathfrak D_2<=54 h_J^2`. Independent longitude motion, arbitrary node motion,
support changes, and a radius uniform in refinement remain outside the theorem.

The sampling claim uses the accepted P1A quotient

```text
K_X = ker S_2,
mathfrak D_2 = sup_(A notin K_X) ||(L+6I)S_2 A||_w / ||S_2 A||_w.
```

The proved row multiplier is sampling-safe because `S_2 A=0` implies
`R_2 A=0` row by row. No injectivity of `S_2`, lower sampling-frame constant,
or invariance of `im S_2` is inserted into the proof.

The companion `d=2` family is elementary and exact. For the regular
`N`-gon, `N>=5`, with fill/separation parameter `h=pi/N`, active edge angle
`2h`, and equal nearest-neighbor rate `[2(1-cos(2h))]^-1`, one has

```text
r_max = (1-cos(2h))^-1,
mathfrak D_2 = 2(1-cos(2h)) = 4 sin^2 h,
mathfrak D_2 r_max = 2.
```

Thus `R_2=pi^2/8`, `C_2=4`, and `c_2=16/pi^2` give the matching-order
two-sided bound. The publication manuscript contains the direct trigonometric
proof; `p1e_asymptotic_family_audit.py` and the regular-polygon Lean lemmas
provide independent exact proof surfaces.

## Controlling acceptance evidence

The following files contain the controlling positive-theorem evidence. The
exact-head scope additionally retains the independent route reports, their
deterministic rejection fixtures, the Lean surface, and the publication
registries named by the release workflow.

| Role | Authoritative file | Acceptance boundary |
|---|---|---|
| ordinary theorem | `docs/publication_program/P1E_SHORT_GAP_S2_CONSTRUCTION.md` | controlling all-orders `d=3` proof |
| fixed-level robustness theorem | `docs/publication_program/P1E_FIXED_SUPPORT_ROBUSTNESS_THEOREM.md` | ordinary finite-dimensional proof for every fixed level; radius computable and level-dependent |
| fixed-support adversarial audit | `p1e_fixed_support_robustness_audit.py`; two certificate verifiers; focused pytest | regression, mutation rejection and certificate-interface checks; finite runs are not the analytic proof |
| final hostile all-orders audit | `docs/publication_program/P1E_SHORT_GAP_CAUCHY_HOSTILE_AUDIT.md` | accepts the transition and first-row guards; records one harmless expository overbound |
| independent schedule/recurrence audit | `docs/publication_program/P1E_NO_GUARD_RING_INDEPENDENT_AUDIT.md` | exact reachable-domain and unperturbed recurrence checks; historical all-level perturbation majorant remains diagnostic only |
| literal transition algebra | `p1e_short_gap_symbolic_matrix_audit.py` | exact removable limit, not by itself a uniform remainder proof |
| transition remainder guard | `p1e_short_gap_cauchy_guard_audit.py` | rational majorant on the stated guarded domain |
| polar-row guard | `p1e_short_gap_polar_guard_audit.py` | exact first-row enclosure only |
| finite family generator | `p1e_short_gap_family_audit.py` | finite regression and deterministic mutations, never an all-level substitute |
| exact constants and recurrence | `p1e_short_gap_proof_audit.py` | exact algebra paired with the analytic guard |
| hostile rejected mutations | `p1e_short_gap_referee_audit.py` | prevents superseded mask/cap claims from re-entering |
| final hostile guard fixtures | `p1e_short_gap_cauchy_hostile_audit.py` | independent exact check of every Cauchy and first-row estimate |
| independent exact fixtures | `p1e_no_guard_ring_independent_audit.py` | reachable-floor, determinant, and recurrence checks; does not certify a level-uniform radius |

All Python paths in the table are relative to
`afp_barrier_gate1/pure_math/covariance/`.

## Six independent route audits

The search retained six mechanism families independently. Their negative or
conditional conclusions remain part of the publication record alongside the
accepted ring construction.

| Required route family | Report | Exact audit | Recorded boundary |
|---|---|---|---|
| spherical Delaunay/Voronoi or geometric stress | `P1E_VARIATIONAL_VORONOI_ROUTE_AUDIT.md` | `p1e_variational_voronoi_audit.py` | centroidality and force balance do not force the quadratic moment |
| positive approximate Laplacian plus exact correction | `P1E_INTRINSIC_ICOSAHEDRAL_SMOOTHING_AUDIT.md` | `p1e_icosahedral_cone_audit.py` | smooth-region consistency does not supply the singular-cap inverse |
| local tight frame plus global reconciliation | `P1E_STRATIFIED_LATTICE_REPAIR_HOSTILE_AUDIT.md` | `p1e_stratified_lattice_repair_audit.py` | a false buffer and factor-two normalization defeat the proposed global repair |
| symmetry-orbit/reflection construction | `P1E_COXETER_REFLECTION_ROUTE_AUDIT.md` | `p1e_asymptotic_family_audit.py` | symmetry does not itself give exact coordinate reproduction or seam control |
| convex/probabilistic construction | `P1E_PROBABILISTIC_CONVEX_ROUTE_AUDIT.md` | `p1e_probabilistic_convex_audit.py` | fixed-degree random stars have a nonvanishing covariance floor |
| exact microstructure/product perturbation | `P1E_ALGEBRAIC_PRODUCT_ROUTE_AUDIT.md` | `p1e_algebraic_product_audit.py` | fixed joins lose quasiuniformity and natural interfaces fail sharedness |

The route reports are falsification and search-boundary evidence. They do not
prove the positive theorem by exhaustion.

## Formal core

`AFPBarrier/QuadraticFidelityConstruction.lean` certifies the finite,
division-safe identities used after a shared stress has been constructed:

- radial/tangent force decomposition and exact `H_1` reproduction;
- detailed balance from a shared conductance;
- moment normalization and finite correction closure;
- four-point connector moments and positivity;
- chord-mass rate conversion;
- regular-polygon `H_1` and scalar `H_2` identities.

It does not formalize the integer mesh schedule, analytic Cauchy enclosures,
global conductance recurrence, or the analytic fixed-level perturbation
radius. Those remain obligations of the ordinary proofs and exact audits.
Proposition 7.3 is therefore not labeled Lean-verified. The aggregate import
and focused axiom audit must compile without project axioms, placeholders, or
project constants.

## Exact-head acceptance contract

The prepared workflow
`.github/workflows/afp-publication-p1e-matching-construction.yml` is the gate,
not evidence that the gate has run. On the literal release head it must:

1. verify the frozen P1D commit/tree, ancestry, no-merge history, immutable
   retained refs, and an exact changed-path allowlist;
2. execute the generator, every construction audit, all six independent route
   audits, and the retained P1D/P1C/P1B/P1A exact regressions;
3. build the full Lean project and the focused P1E module, audit dependencies,
   and reject placeholders, project axioms, and project constants;
4. hash the source and evidence records and recheck the exact final state.

The ordinary fixed-family theorem and the separate fixed-level robustness
theorem are mathematically accepted at their stated scopes. Repository
freezing remains a separate operational step: no CI status or immutable
exact-head record exists until the repair workflow succeeds on the literal
release commit.

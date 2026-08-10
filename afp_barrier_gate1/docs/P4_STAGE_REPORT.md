# Prompt 4 stage report — sharp barriers, extremals, anisotropy, and synthesis

## 1. Immutable baseline and isolated development line

```text
repository:
  FusionSandwich/Testing

Prompt-2 verified object:
  commit 31ea6a49f006df10ca633eafd6848ad43b51ac3f
  tree   879b88de81eeb52ebb09373c2ccb77cb7cb7642c

Prompt-3 mathematical object:
  commit c66f3229d0a89d97559535810c4ba09daf6e4e42
  tree   29d5e7f8f55479513a71dd457f9bd64c11b6df0f

Prompt-4 verified starting baseline:
  commit 8de4b94835137d1eaf32c14b626424f87d2e176d
  tree   350fc38359fa4c55666c9244c61890188c4b4f44
  ref    archive/afp-pure-math-p3-rigidity-verified

new non-overwriting branch:
  agent/afp-pure-math-p4-from-p3-8de4b948

new pull request:
  PR #35
  base archive/afp-pure-math-p3-rigidity-verified
```

The new branch was created and pushed at the exact Prompt-3 archive object
before editing.  No old Prompt-2, Prompt-3, Prompt-4, or transport ref is a
base or update target of this stage.

## 2. Read-only salvage provenance

The independently audited old Prompt-4 snapshots are

```text
ae5b4c7635f917ea7abb6feb58717cc0173b4cd7
d1a31d195ae3c371b3f9cee29bd7ed34d1ff0994
tree e192275e48bf38bf899483e8c27c0c3a206edf64
```

Neither old commit is in the new candidate ancestry.  Their two trees are
identical, but every accepted file was manually ported or reimplemented on the
verified Prompt-3 API.  File/blob provenance, proof review, adversarial
findings, formal status, and exact-regression status are recorded in
`pure_math/barriers/P4_SALVAGE_LEDGER.md`.

Mutable old branch heads are observations only.  Their final classifications
are materialized by the exact-head workflow; movement does not enter ancestry
and is not made a false failure condition.

## 3. Independent audit families and mechanism registry

Three independent audit families were run before final synthesis:

| Audit family | Adversarial question | Resolution |
|---|---|---|
| polar asymptotics and fixed graph | can a constant, endpoint, cancellation, import, or hidden optimizer-symmetry defect break the graph-class theorem? | no; exact constants and the `N=2` endpoint survive; raw transverse balance is retained |
| extremal family and anisotropy | can scaling, empty feasibility, dual signs, unequal tangent magnitudes, or incomplete compactness falsify the old wording? | yes to three literal boundary defects; all were corrected and registered |
| provenance and workflow semantics | can selective salvage import old ancestry or can a broad allowlist/merge SHA falsely pass a corrupted candidate? | old commits excluded; exact PR-head binding and a narrow fail-closed policy are required |

The live mechanism registry is
`pure_math/barriers/P4_APPROACH_REGISTRY.md`; the controlled theorem registry is
`pure_math/barriers/P4_THEOREM_REGISTRY.md`.  They group findings by mechanism,
not by wording.

## 4. Mandatory theorem matrix

| Requirement | Status | Exact result and support |
|---|---|---|
| controlled `csc^2` expansion | PROVED | positive tail `0<=e(x)<=x^4/80` on `0<x<=pi/4` |
| uniform polar rate | PROVED | displayed coefficients and remainder `<=pi^2/(48N^2)` for every `N>=2` |
| uniform polar quality | PROVED | `N^2/pi^2+7/12`, remainder `<=pi^2/(12N^2)` |
| asymmetric polar solve | PROVED | all three rates forced directly; no optimizer symmetry |
| fixed product-graph minimax | PROVED | forced lower bound plus verified positive reversible attainment |
| sharp quartic constants | PROVED | `8/pi^4` in `N`; `2/pi^4` in `K=2N^2` |
| universal/loss-window transfer | PROVED | exact normal-moment, rate, defect, and shared-conductance normalization |
| constrained extremal lower bound | PROVED | `E_K>=4/(RK)`, `C*>=4/R` |
| fixed-order extremal minimizer | PROVED | compact finite support-graph union for every nonempty fixed `K>=2` class |
| product-family exclusion | PROVED | cap fails at `N>(pi^2/2)sqrt(R)` |
| arbitrary-moment projective reduction | PROVED | `Q_lambda=r epsilon/lambda^2`; fixed-moment family is an affine slice |
| sliced LP and dual | PROVED | exact primal reduction/certificate; generic finite LP duality is EXTERNAL |
| equality and opposed-ray examples | PROVED | general `kappa` formula; half-weight formula only at `kappa=1` |
| polar feasible-family anisotropy | PROVED | exact `A_pole=Q_pole-1` and quadratic expansion |
| biregular/perfect-matching incidence | PROVED | `pM_i=qM_{i+1}`; matching forces equal populations |
| Delsarte route | REJECTED | no solved new sampling-safe certificate |
| blanket curvature collapse | REJECTED | one-function `Gamma_2` is not a full curvature theorem |
| compact-space extension | CONJECTURE | no extension is claimed in this package |
| metric-free transport contraction | REJECTED | a specified discrete metric and curvature theorem are required |
| finite Plantri census | COMPUTATIONAL | pinned counts through twelve vertices, total `9150`; not the proof |

## 5. Minimal corrections forced by adversarial audit

The old snapshot's literal arbitrary-moment identity is `REJECTED`.  For a
normal moment `lambda>0`,

```text
Q_lambda=r epsilon/lambda^2=s_2/m^2.
```

The spherical global quality `r epsilon/4` is recovered at `lambda=2`.
Likewise, the fixed-`lambda` family is an affine slice bijective with the
balanced probability polytope; only the unfixed nonzero tangent-balanced cone
is projective.  The interval/minimum theorem assumes that polytope is nonempty.

The old downstream shorthand that opposite rays force half weights is also
`REJECTED`.  If `v_2=-kappa v_1`, the proved replacement is

```text
A=kappa(ell_1-ell_2)^2/(kappa ell_1+ell_2)^2.
```

The requested symmetric formula is exactly its `kappa=1` corollary.  The
counterexample catalogue retains an exact unequal-colatitude spherical witness.

The quasi-uniform loss window plus `K` comparable to `h^-2` establishes
linear-rate-cap compatibility only; all remaining constrained-class hypotheses
must be supplied.  Lean's incidence declaration checks the arithmetic
consequence from supplied edge counts rather than claiming a complete graph
incidence formalization.

## 6. Implementation and independent exact audit

The authoritative ordinary theorem is
`pure_math/barriers/SHARP_PRODUCT_GRAPH_BARRIERS.md`.  The finite formal core is
`AFPBarrier/SharpProductBarriers.lean`, imported by the aggregate and included
in the focused axiom report.  The independent audit
`pure_math/barriers/prompt4_sharp_barrier_audit.py` checks:

```text
exact polar coefficient extraction
rigorous rational remainder constants
unique asymmetric polar rates
universal barrier and extremal separation
arbitrary-lambda projective round trip
sign-correct primal/dual certificate
general-kappa and unequal-ray anisotropy
polar anisotropy
all 0/1 biregular incidence matrices through 4x4
```

Exact computation is `COMPUTATIONAL` falsification support.  The general
ordinary results remain `PROVED`.

## 7. Publication synthesis and handoff

The final hierarchy and terminology-independent main theorem are in
`pure_math/FINAL_PURE_MATH_THEOREM_PACKAGE.md`.  Exact assumptions,
counterexamples, primary-source comparisons, and the manuscript abstract are
in the corresponding `docs/` records.

The central publication candidate remains the Prompt-2 actual-sampling
quadratic residual factorization and positive structural rigidity.  Prompt-1
local/global feasibility, Prompt-3 exact/quantitative rigidity, and Prompt-4
sharp graph barriers, constrained extremals, and feasible-family anisotropy are
the supporting hierarchy.

Future numerical analysis owns optimizer computation, convergence and upper
bounds, verified Delaunay-family construction, non-biregular split/merge ring
designs, and coordinate-space framework stability.  Those future conclusions
are `CONJECTURE` until separately proved or transferred from checked external
hypotheses.

## 8. Exact-head closeout

The tracked source cannot contain its own final commit/tree or future workflow
artifact identifiers.  `docs/P4_FINALIZATION_RECORD.md` is therefore a
machine-resolved template.  At the exact candidate, the dedicated workflow
materializes a resolved record containing the literal tested commit/tree,
remote head, ancestry results, immutable archive heads, job/run identifiers,
artifact digests, exact source-tar digest, Lean job count, axiom output,
deterministic results, mutable observations, and final Prompt-5 baseline.

The Prompt-4 archive is created only after one full green run.  An unchanged
second exact-head run must then verify archive equality; that second run is the
authoritative closeout.  No post-verification source commit is permitted.

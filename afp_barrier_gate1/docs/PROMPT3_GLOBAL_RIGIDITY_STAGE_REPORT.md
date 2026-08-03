# Prompt 3 global rigidity stage report

## Stage status

```text
PROMPT_3_STATUS=IMPLEMENTATION_UNDER_EXACT_HEAD_CI
PROMPT_4_BASELINE_STATUS=NOT_READY_UNTIL_MERGE_AND_FINAL_HEAD_AUDIT
baseline_branch=agent/afp-pure-math-p0-m1
baseline_commit=c88b57533c3c8ad8fd819e4e52a74c4b5a245479
baseline_tree=92b3c0eaa45dd58befbc5af59790476d5c5d85b3
implementation_branch=agent/afp-pure-math-p3-global-rigidity-near-rigidity
immutable_archive=515f1aae6c20bd85711c90b5c1c21b4905252d01
```

The exact implementation, PR, merge, final-target, and workflow identifiers are
recorded in the Prompt 3 PR discussion and in
`PROMPT4_READINESS_HANDOFF.md` after final integration.  A commit cannot embed
its own SHA/tree without a self-referential hash fixed point.

## FOUNDATIONAL / ALREADY PROVED

* local normal-loss moment and the weighted variance mechanism;
* exact Prompt 1 local feasibility and shared-edge duality package;
* abstract connected equality propagation in
  `AFPBarrier/GlobalLossRigidity.lean`;
* Prompt 2 covariance factorization, genuine sampling distinction, positive
  axial rigidity, corrected equivariant rigidity, and centered-product
  resonance;
* all permanent Prompt 1 and Prompt 2 counterexamples.

These are dependencies, not Prompt 3 novelty.

## NEW PROMPT 3 THEOREMS

1. **Exact spherical `Q=1` transfer.**  Coordinate exactness gives the normal
   moment, positive row rate, probability normalization, second-moment
   identity, and exact variance.  Equality fixes every active loss and, under
   shared conductances and connectedness, one global rate and loss.
2. **Restricted round geodesic-triangulation classification.**  Under the ten
   explicit embedding, positivity, minor-arc, convex-face, no-crossing, and
   full-coverage hypotheses, common loss gives congruent equilateral spherical
   faces; the round angle sum gives constant valence; Euler and a direct
   link/collar proof give exactly the tetrahedral, octahedral, and icosahedral
   maps; face propagation gives geometric uniqueness.
3. **Explicit graph-global near-rigidity.**  Pointwise, adjacent, path,
   diameter, incident-edge, arbitrary-edge, and graph-center reference bounds
   are stated with `delta,q_delta,s_delta,h_delta` and no big-O notation.
4. **Spectral-gap/effective-resistance refinement.**  The reversible measure
   `pi_i proportional w_i r_i` gives a Dirichlet-energy bound for `log r`, a
   Poincare variance bound, and a resistance pointwise bound independent of
   path multiplication.
5. **Quantitative triangulation stability.**  Explicit arccos and spherical
   angle derivative constants, integer valence separation, monotonicity of the
   equilateral angle map, and a conservative closed-form `eta_*` identify the
   Platonic type and bound the edge-length sup distance to its exact side.
6. **Exact `Q=1` covariance decomposition.**  The radial coefficient is fixed,
   while `T_i-P_i/2` records unconstrained tangential anisotropy.  Axial
   covariance is equivalent to `T_i=P_i/2`.
7. **Positive reversible anisotropy counterexample.**  A three-parameter
   weighted octahedron has `Q=1` at every vertex and unequal masses; it is
   axially isotropic at every vertex iff all three conductance parameters are
   equal.  Its genuine sampled degree-two exact space is nevertheless `{0}`.

## EXACT / COMPUTATIONAL

`pure_math/rigidity/triangulation_counterexample_audit.py`:

* source-pins `plantri` commit and source blob;
* enumerates every simple sphere triangulation for `4<=V<=12` in exact-head CI;
* verifies the pinned counts `1,1,2,5,14,50,233,1249,7595`;
* records graph6, degree sequence, equivelarity, candidate angle condition, and
  automorphism order where practical;
* independently matches the three equivelar survivors to exact algebraic
  tetrahedral, octahedral, and icosahedral Gram/hull certificates.

`global_near_rigidity_audit.py` checks exact variance and Platonic constants,
long-path/small-`kappa` stress, exact rational effective resistance,
arccos conversion, spherical-angle derivatives, valence gaps, and the
positive derivative of `alpha_eq`.

`q1_covariance_audit.py` checks all five Platonic `Q=1` regressions, the
weighted octahedral `T,C,M` formulas, the axial iff condition, the genuine
sampled-space contraction certificate, and the absence of tangential control
at `eta=0`.

Finite enumeration is used only for falsification and regression.  The
all-orders classification proof is ordinary mathematics.

## EXTERNAL / STANDARD INPUTS

* spherical law of cosines and spherical excess;
* Euler's formula and elementary links/collars in triangulated 2-manifolds;
* the finite reversible Poincare variational definition;
* the Dirichlet/effective-resistance variational principle;
* `plantri` only as an external generator for finite hostile search.

Cauchy/Alexandrov rigidity and general quantitative framework theorems are
reviewed as adjacent prior art but are not black-box dependencies: geometric
uniqueness and the mandatory edge-metric stability theorem are proved directly.

## REJECTED

Permanent rejected statements include:

```text
only K in {4,6,12} can have Q=1;
every finite spherical graph has Q>1;
every equal-loss spherical graph is a triangulated Platonic graph;
Q=1 forces axial covariance;
a finite enumeration proves the all-orders classification;
form-space dimension is a sampled-space dimension;
pathwise control is diameter free;
near-rigidity can be stated as an unnamed O(sqrt eta).
```

Cube, dodecahedron, antipodal, cone-defect, major-arc, inactive-edge,
nonreversible, signed-rate, long-path, small-`kappa`, large-resistance, and
weighted-octahedron tests remain permanent.

## Formalization boundary

New narrow modules are:

* `AFPBarrier/SphericalQEqualityRigidity.lean`;
* `AFPBarrier/QuantitativeGlobalNearRigidity.lean`;
* `AFPBarrier/QEqualityCovariance.lean`.

They formalize the finite variance/equality transfer, selected quantitative
ratio algebra, radial covariance identities, and the finite entrywise `Q=1`
decomposition.  The full topological classification, interval-certified
spherical trigonometry, and standard Poincare/resistance inputs remain in the
ordinary proof and deterministic audits.

No `sorry`, `admit`, `sorryAx`, or user-declared `axiom`/`axioms` is permitted.

## Prompt 4 preservation and reacceptance boundary

Prompt 4 was already complete on the accepted target
`94aebf6578a43516cce4bb7c042fc57681c93890` before this richer Prompt 3
reconciliation.  Its theorem package, exact constants, workflows, and synthesis
files are protected inputs.  Rich Prompt 3 is integrated additively after that
history.  The final combined head reruns every Prompt 4 exact and Lean gate and
updates only the synthesis/claim-control text needed to acknowledge the stronger
Prompt 3 companion results.  No Prompt 4 theorem is rediscovered or replaced.


## Reconciliation corrections

The pre-reconciliation literal head `f1ef5b3c3107d2dfc835ed84c443eb82d752cb56`
passed all Python, source-policy, and 9,150-map enumeration stages but failed the
Lean build in `QuantitativeGlobalNearRigidity.lean`.  The repairs preserve the
theorem statements:

```text
explicit commutativity conversion in the weighted square inequality;
positive-inverse multiplication for adjacent-rate bounds;
positive-inverse multiplication for incident-loss bounds;
0<=delta<1 retained before lower-scale multiplication;
redundant post-field_simp tactic removed.
```

The former endpoint-product angle enclosure is rejected on the required fixed
icosahedral neighborhood.  The accepted replacement is the positive
Gram/Heron determinant factorization, with zero-defect and positive-width
regressions for q=3,4,5.  The covariance theorem is restricted to `0<ell<2`;
the antipodal `ell=2` radial boundary is separate.

The independent PR #28 history is not merged.  Its exact source hashes and the
manually re-derived corrections are recorded in the reconciliation ledgers.

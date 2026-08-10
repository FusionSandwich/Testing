# Prompt 3 stage report

## Immutable start

```text
repository: FusionSandwich/Testing
verified Prompt 2 branch:
  agent/afp-pure-math-p2-quadratic-covariance-completion
verified Prompt 2 commit:
  31ea6a49f006df10ca633eafd6848ad43b51ac3f
verified Prompt 2 tree:
  879b88de81eeb52ebb09373c2ccb77cb7cb7642c
new Prompt 3 branch:
  agent/afp-pure-math-p3-rigidity-from-p2-31ea6a49
draft PR: #28
initial protection/salvage checkpoint:
  02ace53680e6e62b81cdb20048d447732f2f4d31
```

Prompt 2 remains unchanged.  The new branch was published at the literal
Prompt 2 commit before any edit.  The initial heads of Prompt 2, the three old
Prompt 3 sources, and the transport archive are recorded in
`P3_BRANCH_PROTECTION_RECORD.md`; exact source blobs and selective decisions are
recorded in `P3_SALVAGE_LEDGER.md`.

## Truth-safeguard decisions

- **REJECTED:** unrestricted tangent normalization under exact `Q=1`.
  The exact antipodal chain has `ell=2` and zero tangent denominator.  The
  corrected covariance theorem is **PROVED** for `0<ell<2`; the antipodal
  covariance is handled directly.
- **REJECTED:** the old rich branch's `C_A<1` threshold certificate.  It fails
  at the exact icosahedral prescribed box.  A closed positive spherical
  Gram/Heron factor supplies the corrected **PROVED** constant.
- **REJECTED:** the old Lean incident-loss theorem without `delta<1`.  A
  concrete scalar countermodel is in the salvage ledger; the corrected lemma
  carries the missing domain hypothesis.

These are literal corrections, not failures of the equality/classification or
near-rigidity program.

## Permanent falsification boundary

The synchronized claim controls retain all seven mandatory **REJECTED**
formulations:

1. only `K in {4,6,12}` can have `Q=1`;
2. every finite spherical graph has `Q>1`;
3. every equal-loss spherical graph is a triangulated Platonic graph;
4. `Q=1` forces axial covariance;
5. form-space dimension equals sampled-space dimension;
6. near-rigidity is diameter-free under only a local active-weight floor; and
7. finite enumeration proves the classification.

Cube and dodecahedron, the weighted octahedron, long paths, and the fixed
Plantri cutoff supply the corresponding exact or logical boundaries.  For the
weighted octahedron specifically, the off-diagonal quadratic forms lie in the
sampling kernel while the genuine sampled degree-two exact space is
**PROVED** to be `E_sample={0}` by the stochastic contraction argument.

## PROVED ordinary package

`GLOBAL_Q_RIGIDITY_THEOREM.md` gives the all-orders argument for:

1. exact spherical `Q` identity and equality transfer;
2. the fixed ten-hypothesis tetrahedral/octahedral/icosahedral classification;
3. direct combinatorial and geometric uniqueness with exact constants;
4. pointwise, path, diameter, loss, logarithmic, and geodesic near-rigidity;
5. spectral-gap and effective-resistance refinements with exact factors;
6. the corrected closed triangulation-stability threshold and edge sup norm;
7. the non-antipodal covariance split, Prompt-2 axial equivalence, and
   weighted-octahedron anisotropy boundary; and
8. the weighted octahedron's genuine sampled degree-two exact space
   `E_sample={0}`, with its nonzero form kernel handled only through the
   Prompt-2 sampling quotient.

The complete 5-valent link/collar proof is isolated in
`ICOSAHEDRAL_GRAPH_LEMMA.md`.  Euler, angle sums, and spherical face propagation
are used only after all ten triangulation hypotheses have been established.

## EXTERNAL boundary

The spherical cosine law/excess, Euler and disk-curvature identities for
cellular triangulations, elementary link/collar topology, finite Poincare
variational principle, and electrical Dirichlet principle are EXTERNAL
standard inputs with their conventions displayed.  Cauchy/Alexandrov rigidity
is not used.

## COMPUTATIONAL boundary

Source-pinned Plantri enumeration through 12 vertices, exact Platonic
coordinate/Gram/hull data, finite minors, weighted-octahedron symbolic checks,
and numerical stress cases are COMPUTATIONAL hostile audits.  They do not
prove the all-orders classification or any unrestricted claim.

## Verification status

The mathematical candidate is the immutable object
`c66f3229d0a89d97559535810c4ba09daf6e4e42`, tree
`29d5e7f8f55479513a71dd457f9bd64c11b6df0f`.  Run `30771073146`
established the complete mathematical verification:

- all retained Prompt 1 and Prompt 2 deterministic regressions pass;
- all three Prompt 3 audits pass, including the source-pinned Plantri counts
  `1,1,2,5,14,50,233,1249,7595` through 12 vertices;
- `python -m compileall -q pure_math` and both Lean source-policy scans pass;
- the full Lean package builds successfully in 3,110 jobs; and
- the focused axiom audit reports only `propext`, `Classical.choice`, and
  `Quot.sound`.

The exact-regressions job in that run completed every mathematical and
deterministic step successfully.  Its sole failing step, and the sole reason
the old final-state job failed, was the policy that treated a changed mutable
source-branch observation as candidate corruption.  The observed branch was:

`agent/afp-pure-math-p3-global-rigidity-near-rigidity` advanced from the
recorded `d9304b5d...` source snapshot to `f1ef5b3c...`.  This work neither
moved nor restored that read-only ref.  The historical result remains
`MOVED_EXTERNALLY`.

## Prompt 2+3 closeout correction

Closeout branch
`agent/afp-pure-math-p2-p3-final-closeout-c66f3229` was created remotely at
the literal `c66f3229...` object before any edit.  Draft PR #31 targets the
create-if-absent Prompt-2 archive
`archive/afp-pure-math-p2-quadratic-covariance-verified-31ea6a49` at exact
commit `31ea6a49...`.

The corrected workflow separates:

1. immutable commit/tree, ancestry, allowlist, source-identity, archive, and
   exact remote-candidate bindings, which are fatal;
2. immutable old salvage snapshot objects, which must exist and remain absent
   from candidate ancestry; and
3. current heads of old source branches, whose ordinary movement is recorded
   but is not a candidate failure.

The final closeout reruns every retained exact regression, the pinned
9,150-map Plantri census, the full Lean build, the focused axiom audit, both
source-policy scans, checkout-cleanliness checks, and exact source archiving.
The terminal `final-candidate-integrity` job has ordinary success-gated
dependencies on both `exact-regressions` and `lean-kernel`; it does not use an
always-running prerequisite bypass.

The final commit SHA, tree, workflow run, job conclusions, artifact identities,
Lean job count, and source digest are values created by committing and running
this record.  The tracked record therefore binds them normatively to the exact
`GITHUB_SHA` satisfying remote-head equality; the workflow materializes their
literal values in a resolved finalization-record artifact.  After the run is
fully green, the immutable Prompt-3 archive and PR #31 bind that same literal
commit externally.  This avoids a false self-reference: a blob cannot contain
the not-yet-computed tree/commit hash to which it contributes, and a commit
cannot contain workflow/artifact identifiers that do not exist until after it
is pushed.

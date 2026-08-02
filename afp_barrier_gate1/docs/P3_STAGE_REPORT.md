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

The exact final commit/tree, final protected-ref comparison, exact-head
workflow/jobs, artifact IDs/digests, Lean job count, axiom audit, and complete
deterministic results are filled only after the dedicated final CI gate passes.
Until then the PR remains draft and this stage is not a Prompt 4 baseline.

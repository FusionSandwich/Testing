# AFP pure-mathematics track

This directory separates theorem-driven mathematics from the frozen Gate 6
transport implementation.

## Immutable transport baseline

The transport archive remains

```text
archive/afp-gate6-spatial-multigroup-verified
515f1aae6c20bd85711c90b5c1c21b4905252d01.
```

Transport, Radiant, evaluated material data, HTS benchmarks, multigroup and
spatial solvers, and production implementations are outside this track.

## Prompt 1 accepted package

The corrected Prompt 1 baseline is

```text
923dc47dae4f83dbea9cd56aa904164c6378e52d.
```

The package establishes:

- exact indexed convex-hull and relative-interior local feasibility;
- repeated, redundant, and lower-dimensional tangent configurations;
- unique positive angular scaling and exact row-rate formulas;
- division-free pure and mixed antipodal classifications;
- explicit coefficient, rate, singular-value, perturbation, and LP margins;
- global shared-edge cone, Farkas, LP, and complementary-slackness theory;
- exact centered local-but-not-global counterexamples; and
- complete-graph, equivariant-averaging, and centered-clique reconciliation.

Primary Prompt 1 records are:

- `EXACT_LOCAL_GLOBAL_THEOREM_PACKAGE.md`;
- `APPROACH_REGISTRY.md`;
- `../docs/THEOREM_TO_FILE_MAP.md`;
- `examples/exact_local_global_audit.py`; and
- `tests/test_spherical_feasibility.py`.

## Prompt 2 accepted covariance package

The authoritative proof is

```text
covariance/SAMPLED_QUADRATIC_EXACTNESS_THEOREM.md.
```

For a coordinate eigenmap,

```text
L(Phi^T A Phi)
 =-2lambda Phi^T A Phi+tr(A^T C_i).
```

In the spherical degree-two specialization,

```text
S_X(A)_i=Phi_i^T A Phi_i,
R_X(A)_i=<A,P_0(C_i+2Phi_iPhi_i^T)>_F,
R_X=(L+2dI)S_X.
```

Therefore

```text
K_X=ker S_X subset E_form=ker R_X,
E_sample=im(S_X) intersect ker(L+2dI),
dim E_sample=rank(S_X)-rank(R_X).
```

Positive axial covariance at every node gives

```text
E_form=K_X,
E_sample={0}.
```

Regular simplices attain this theorem in every dimension. The five Platonic
shortest-edge generators have exact form dimensions `2,3,2,0,0` and sampled
dimensions all zero.

### Corrected equivariant boundary

The independent equivariant irreducibility theorem requires

```text
a_ij>=0 for every i!=j.
```

Together with a transitive equivariant unit-sphere coordinate eigenmap,
irreducibility of the real conjugation action on `Sym_0(d)`, and one positive
jump between distinct embedded points, this gives `E_form={0}`. Reversibility
is not required.

The signed regular pentagon is the permanent counterexample if global
nonnegativity is omitted. With exact distance-one and distance-two rates

```text
(5+3sqrt(5))/10,
(5-3sqrt(5))/10,
```

it has coordinate eigenvalue `-1`, full trace-free quadratic eigenvalue `-4`,
`E_form=Sym_0(2)`, and `dim E_sample=2`, despite irreducible `C_5`
conjugation.

### Centered product resonance

`AFPBarrier/QuadraticCovariance.lean` now proves

```text
L(fg-c)+mu(fg-c)
 =2Gamma(f,g)+(mu-lambda-nu)fg-mu c
```

for eigenfunctions `Lf=-lambda f`, `Lg=-nu g`. At additive resonance,

```text
L(fg-c)=-(lambda+nu)(fg-c)
iff
2Gamma(f,g)=(lambda+nu)c.
```

For a square,

```text
L(f^2-c)=-2lambda(f^2-c)
iff
Gamma(f,f)=lambda c.
```

The uncentered `c=0` case forces zero carré du champ. A centered square may be
nonzero. The permanent positive regression is the Boolean square
`f=x_1+x_2` on the four-state cube:

```text
Lf=-2f,
f^2-2=2x_1x_2!=0,
L(f^2-2)=-4(f^2-2),
Gamma(f,f)=4.
```

Centered resonance gives semigroup variance

```text
c(1-exp(-2lambda t)),
```

which is distinct from Jensen equality. The Boolean variance is strictly
positive for `t>0`.

### Spherical product boundary

On `S^(d-1)`, the coordinate, doubled-coordinate, and degree-two eigenvalues
are respectively

```text
d-1,
2(d-1),
2d.
```

The covariance problem therefore has shift `2` and is not additive square
resonance.

The exact `S^2` pointwise-product table for `ell=1,...,6` contains no additive
resonance. The generalized higher-dimensional equation is Pell-type, but no
sampled dimension tradeoff, multiplicity obstruction, or new global
consequence survives the kernel and alias audits. The general hierarchy is
`REJECTED FOR PROMPT 2` for that reason, not because centered squares are
impossible.

## Exact verification

Prompt 2 exact regressions are:

- `covariance/quadratic_covariance_audit.py`;
- `covariance/prompt2_closeout_audit.py`.

Together they check:

- covariance/factorization and all Platonic ranks;
- regular-simplex formulas;
- four-point signed restoration;
- signed regular-pentagon failure of unsigned equivariant rigidity;
- centered product algebra and the Boolean example;
- semigroup variance;
- the `S^2` `ell=1,...,6` table;
- bounded and Pell resonance assertions; and
- singular/plural user-axiom policy fixtures.

Lean support is concentrated in:

- `AFPBarrier/QuadraticCovariance.lean`;
- `AFPBarrier/PureMathAxiomAudit.lean`;
- `AFPBarrier/GlobalLossRigidity.lean`; and
- the aggregate `AFPBarrier.lean`.

No `sorry`, `admit`, `sorryAx`, singular `axiom`, or plural `axioms`
declaration is permitted. The dedicated workflow scans the aggregate source,
tests both axiom spellings, performs the full Lean build and focused axiom
audit, and independently checks selected declarations with nanoda.

## Prompt 3 exact global rigidity and near-rigidity package

The abstract equality-propagation theorem in `GlobalLossRigidity.lean` remains
a foundational dependency.  Prompt 3 is now proved in

```text
rigidity/GLOBAL_Q_RIGIDITY_THEOREM.md.
```

The package contains:

1. the exact spherical `Q=1` moment/variance transfer and all degeneracy cases;
2. the restricted nondegenerate minor-arc round geodesic-triangulation
   classification into tetrahedron, octahedron, and icosahedron;
3. exact counts, sides, losses, rates, direct combinatorial uniqueness, and
   geometric uniqueness;
4. explicit pointwise, path, diameter, reference-loss, and arclength
   near-rigidity bounds;
5. independent Poincare and effective-resistance refinements;
6. an explicit spherical-angle/valence threshold and edge-length sup distance
   to the exact Platonic side; and
7. the exact radial/tangential `Q=1` covariance decomposition plus the positive
   reversible weighted-octahedron anisotropy example.

The classification is not unrestricted.  Cube and dodecahedron remain exact
`Q=1` regressions, and every embedding hypothesis is retained in claim
control.  `Q=1` does not imply axial covariance.

Verification artifacts are under `rigidity/`; stage and theorem maps are in
`../docs/PROMPT3_GLOBAL_RIGIDITY_*`; the Prompt 4 boundary is frozen in
`../docs/PROMPT4_READINESS_HANDOFF.md`.

## Claim discipline

Use the following labels:

- `PROVED` — complete proof under stated hypotheses;
- `LEAN` — selected finite algebra checked in Lean;
- `EXACT EXAMPLE` — finite symbolic certificate;
- `EXTERNAL` — cited standard theorem;
- `COMPUTATIONAL` — finite deterministic search only;
- `CONJECTURE` — open statement with a kill criterion; and
- `REJECTED` — false or strategically unsupported wording.

CI counts and hashes are provenance, not mathematical novelty. Algebraic form
exactness and genuine sampled exactness must never be conflated. Centered
resonance and Jensen equality must never be conflated.

## Closeout and handoff records

- `../docs/PROMPT2_QUADRATIC_COVARIANCE_STAGE_REPORT.md`
- `../docs/PROMPT2_QUADRATIC_COVARIANCE_THEOREM_MAP.md`
- `../docs/PROMPT2_QUADRATIC_COVARIANCE_INTEGRATION_RECORD.md`
- `../docs/PROMPT2_CLOSEOUT_AUDIT.md`
- `../docs/PROMPT3_READINESS_HANDOFF.md`

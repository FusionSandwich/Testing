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

`AFPBarrier/QuadraticCovariance.lean` proves

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

## Prompt 3 spherical `Q=1` rigidity package

Prompt 3 begins from the verified baseline

```text
c88b57533c3c8ad8fd819e4e52a74c4b5a245479.
```

The authoritative ordinary proof is

```text
rigidity/SPHERICAL_Q1_RIGIDITY_THEOREM.md.
```

The direct five-regular graph lemma is

```text
rigidity/ICOSAHEDRAL_GRAPH_LEMMA.md.
```

For `Omega_i in S^2`, let

```text
g_i(j)=Omega_i dot Omega_j,
ell_ij=1-g_i(j),
r_i=sum_j a_ij,
D_i=sum_j a_ij ell_ij^2,
Q_i=r_i D_i/4.
```

Under the coordinate eigenmap equation

```text
sum_j a_ij(Omega_j-Omega_i)=-2 Omega_i
```

and nonnegative off-diagonal rates,

```text
Q_i>=1,
Q_i=1 iff ell_ij=2/r_i on every active edge from i.
```

Symmetric connected activity therefore yields one common row rate and one
common active chord/geodesic length. Active zero-loss edges are impossible; an
active antipodal edge forces row rate one and propagates the antipodal loss.

### Restricted triangulation classification

The valid classification assumes that the active graph is exactly the
one-skeleton of an injective strict convex minor-geodesic triangulation, every
triangulation edge is active, and there are no active nonedges. Under these
hypotheses, exact `Q_i=1` gives, up to an orthogonal transformation:

```text
regular tetrahedron,
regular octahedron,
regular icosahedron.
```

The proof derives equilateral spherical faces,
`cos(alpha)=c/(1+c)`, degree `q in {3,4,5}`, exact Euler count triples, direct
finite graph identifications, and convex Cauchy congruence.

Exact adjacent data are:

| degree | active dot | common row rate |
|---:|---:|---:|
| 3 | `-1/3` | `3/2` |
| 4 | `0` | `2` |
| 5 | `1/sqrt(5)` | `(5+sqrt(5))/2` |

The cube and dodecahedron are permanent unrestricted `Q=1` counterexamples.
The theorem fixes the geometry and total row rate, not each individual edge
rate.

### Quantitative near-rigidity

For a general positive eigenvalue `lambda`, set

```text
m_i=lambda/r_i,
p_ij=a_ij/r_i,
Q_i=r_iD_i/lambda^2.
```

Then

```text
Q_i-1=sum_j p_ij(ell_ij/m_i-1)^2.
```

If `Q_i<=1+epsilon`, active normalized weights satisfy `p_ij>=p_*>0`, and

```text
delta=sqrt(epsilon/p_*)<1,
kappa=(1+delta)/(1-delta),
```

then active edge-loss errors are at most `delta` relative to their local mean,
shared centers and row rates differ by at most `kappa`, and path/diameter bounds
use the explicit powers in Prompt 3 Theorem 4.1.

An additive theorem assumes

```text
r_iD_i-lambda^2<=eta,
r_i>=r_min>0,
a_ij>=a_min>0,
Delta=sqrt(eta/(r_min a_min)),
```

and gives explicit one-edge, shared-edge, path, diameter, and row-rate bounds.
Shared-conductance floors transfer to these hypotheses under upper mass and
row-rate bounds.

The rare-edge family in the exact audit shows that small `Q-1` alone does not
control every active edge. Coordinate-space stability is not claimed without
a separately stated framework-rigidity singular-value margin.

## Exact verification

Prompt 2 exact regressions are:

- `covariance/quadratic_covariance_audit.py`;
- `covariance/prompt2_closeout_audit.py`.

Prompt 3 exact regression is:

- `rigidity/prompt3_rigidity_audit.py`.

Together with the Prompt 1 audits, they check:

- covariance/factorization and all Platonic ranks;
- regular-simplex formulas;
- four-point signed restoration;
- signed regular-pentagon failure of unsigned equivariant rigidity;
- centered product algebra and the Boolean example;
- semigroup variance;
- the `S^2` `ell=1,...,6` table;
- bounded and Pell resonance assertions;
- exact Platonic `Q=1` rows and triangulation incidence;
- exact tetrahedral/octahedral/icosahedral classification arithmetic;
- normalized variance and stability constants;
- the rare-active-edge counterfamily; and
- shared-conductance floor transfer.

Lean support is concentrated in:

- `AFPBarrier/QuadraticCovariance.lean`;
- `AFPBarrier/GlobalLossRigidity.lean`;
- `AFPBarrier/SphericalQOneRigidity.lean`;
- `AFPBarrier/PureMathAxiomAudit.lean`; and
- the aggregate `AFPBarrier.lean`.

No `sorry`, `admit`, `sorryAx`, singular `axiom`, or plural `axioms`
declaration is permitted. Dedicated workflows scan the aggregate source,
perform full Lean builds and focused axiom audits, and independently check
selected declarations with nanoda.

## Claim discipline

Use the following labels:

- `PROVED` — complete proof under stated hypotheses;
- `LEAN` — selected finite algebra checked in Lean;
- `EXACT EXAMPLE` — finite symbolic certificate;
- `EXTERNAL` — cited standard theorem;
- `COMPUTATIONAL` — finite deterministic search only;
- `CONDITIONAL` — implication requiring an additional explicit quantitative
  margin; and
- `REJECTED` — false or strategically unsupported wording.

CI counts and hashes are provenance, not mathematical novelty. Algebraic form
exactness and genuine sampled exactness must never be conflated. Centered
resonance and Jensen equality must never be conflated. Edge-metric stability
must not be inflated into coordinate-space rigidity.

## Stage records

- `../docs/PROMPT2_CLOSEOUT_AUDIT.md`
- `../docs/PROMPT3_READINESS_HANDOFF.md`
- `../docs/PROMPT3_APPROACH_REGISTRY.md`
- `../docs/PROMPT3_STAGE_REPORT.md`
- `../docs/PROMPT3_THEOREM_MAP.md`
- `../docs/THEOREM_TO_FILE_MAP.md`

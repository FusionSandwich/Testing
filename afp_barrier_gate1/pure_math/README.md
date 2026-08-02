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

## Final theorem hierarchy

The final manuscript theorem package is

```text
FINAL_PURE_MATH_THEOREM_PACKAGE.md.
```

Its hierarchy is:

1. standard finite-generator product and convex-duality lemmas;
2. the central sampled quadratic covariance and rigidity theorem;
3. exact local spherical feasibility and global shared-edge compatibility;
4. exact and quantitative spherical `Q=1` rigidity;
5. sharp product-graph, constrained extremal, and feasible-cone anisotropy
   results;
6. exact examples and counterexamples; and
7. formal-verification and computational appendices.

The manuscript abstract, exact assumptions, and counterexample catalogue are:

```text
../docs/PURE_MATH_MANUSCRIPT_ABSTRACT.md
../docs/PURE_MATH_ASSUMPTIONS_TABLE.md
../docs/PURE_MATH_COUNTEREXAMPLE_CATALOGUE.md
```

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

## Prompt 4 sharp barriers and extremal package

Prompt 4 is developed from the exact Prompt 3 merge baseline

```text
47ef59b0463ecd4bd7a18a3301f29b14f9777c20
```

on the isolated branch

```text
agent/afp-pure-math-p4-sharp-barriers-extremal-synthesis.
```

The authoritative proof is

```text
barriers/SHARP_PRODUCT_GRAPH_BARRIERS.md.
```

### Exact product-grid asymptotics

For the square equal-angle product family `M=2N`, every integer `N>=2`
satisfies

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

The proof uses a positive differentiated cotangent partial-fraction tail. The
formal symbolic series is only a coefficient regression.

### Sharp fixed product-graph obstruction

At every polar-ring vertex, the coordinate equations force

```text
inward meridional rate = 1/(2 sin^2 h),
each azimuthal rate   = 1/(4 sin^4 h).
```

Distinct left and right rates are allowed initially and their equality is
derived from transverse balance. The lower bound therefore does not assume
ring-symmetric conductances, equal masses, or reversibility.

The existing positive reversible construction attains the forced row and its
maximum occurs at the poles. Hence the exact graph-class minimax value is

```text
1/[2 sin^2(pi/(2N))] + 1/[2 sin^4(pi/(2N))],
```

with sharp leading constant `8/pi^4`. With `K=2N^2`, the graph has
`r_max>=(2/pi^4)K^2`.

### Universal and quasi-uniform barriers

Degree-one exactness gives

```text
4 <= r_i epsilon_i.
```

Therefore

```text
epsilon_i<=C h^2 => r_i>=4/(C h^2).
```

The explicit loss window

```text
(2/pi^2)h^2 <= ell_ij <= 2h^2
```

transfers to

```text
1 <= h^2 r_i <= pi^2,
(4/pi^2)h^2 <= epsilon_i <= 4h^2.
```

Positive spherical-Delaunay existence and exact coordinate modes remain
external unless verified for the actual graph family. No fixed radial
connectivity is declared Delaunay at every refinement level.

### Constrained extremal problem

The accepted asymptotic class controls rate, degree, edge locality, separation,
covering, mesh ratio, masses, positivity, reversibility, and exact coordinate
balance. If `E_K` is the minimum maximum defect under `r_max<=RK`, then

```text
E_K>=4/(RK),
liminf K E_K>=4/R.
```

Every nonempty fixed-`K` closed class has a minimizer. The unreduced product
family is eventually excluded from every linear-rate class, whereas verified
quasi-uniform families can remain compatible with one.

### Feasible-cone anisotropy

For a tangent-balanced projective probability vector `p`,

```text
Q=s_2(p)/m(p)^2.
```

At fixed mean loss `m`, minimizing `s_2` is a finite LP. Its exact dual is

```text
maximize alpha+beta m
subject to
alpha+beta ell_j+z dot v_j <= ell_j^2.
```

The cone invariant

```text
A_i=inf_{a in F_i}(Q_i(a)-1)
```

is therefore computable by a compact one-dimensional minimization of LP values.
It vanishes exactly when a tangent-balanced row is supported on one loss level.
For two opposite directions,

```text
A=((ell_1-ell_2)/(ell_1+ell_2))^2.
```

This is the rigorous replacement for the false statement that `Q` is
node-geometry-only.

### Bounded branches

- Delsarte/Gegenbauer: `BLOCKED` without a solved new certificate surviving
  sampling aliases.
- Bakry--Émery: `KILLED` for Prompt 4; the computed one-function identity is
  not a curvature-dimension theorem.
- Compact homogeneous spaces: `DEFERRED`.
- Discrete transport metrics: `DEFERRED`; a Maas/Erbar metric must be specified.
- Reduced rings: one-to-one nearest-ring couplings are impossible for varying
  populations because a perfect matching forces equal ring counts; broader
  split/merge couplings remain unresolved.
- Formal discrete geometry: deliberately bounded to accepted finite algebra.

## Exact verification

Prompt 1 regressions:

- `examples/exact_local_global_audit.py`;
- `tests/test_spherical_feasibility.py`.

Prompt 2 regressions:

- `covariance/quadratic_covariance_audit.py`;
- `covariance/prompt2_closeout_audit.py`.

Prompt 3 regression:

- `rigidity/prompt3_rigidity_audit.py`.

Prompt 4 regression:

- `barriers/prompt4_sharp_barrier_audit.py`.

Together they check:

- local/global feasibility certificates;
- covariance factorization, sampled ranks, and Platonic aliases;
- regular-simplex formulas;
- signed four-point and pentagon boundary cases;
- centered product algebra and the Boolean example;
- the low-degree product table and Pell arithmetic;
- exact Platonic `Q=1` rows and triangulation classification arithmetic;
- normalized variance and stability constants;
- the rare-active-edge family;
- polar asymptotic coefficients and rigorous rational tail constants;
- unique asymmetric polar rate solving;
- extremal and quasi-uniform constants;
- cone anisotropy examples; and
- reduced-ring incidence.

Lean support is concentrated in:

- `AFPBarrier/QuadraticCovariance.lean`;
- `AFPBarrier/GlobalLossRigidity.lean`;
- `AFPBarrier/SphericalQOneRigidity.lean`;
- `AFPBarrier/SharpProductBarriers.lean`;
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
- `CONDITIONAL` — implication requiring an additional explicit hypothesis;
- `BLOCKED` — route produced no accepted theorem under its criterion;
- `DEFERRED` — valid future branch outside the present package; and
- `REJECTED` — false or strategically unsupported wording.

CI counts and hashes are provenance, not mathematical novelty. Algebraic form
exactness and genuine sampled exactness must never be conflated. Centered
resonance and Jensen equality must never be conflated. Edge-metric stability
must not be inflated into coordinate-space rigidity. `Q` must not be treated
as geometry-only. Formal series and fitted slopes are not analytic remainder
proofs.

## Stage and synthesis records

- `../docs/PROMPT2_CLOSEOUT_AUDIT.md`
- `../docs/PROMPT3_READINESS_HANDOFF.md`
- `../docs/PROMPT3_APPROACH_REGISTRY.md`
- `../docs/PROMPT3_STAGE_REPORT.md`
- `../docs/PROMPT3_THEOREM_MAP.md`
- `../docs/PROMPT4_APPROACH_REGISTRY.md`
- `../docs/PROMPT4_STAGE_REPORT.md`
- `../docs/PROMPT4_THEOREM_MAP.md`
- `../docs/PURE_MATH_ASSUMPTIONS_TABLE.md`
- `../docs/PURE_MATH_COUNTEREXAMPLE_CATALOGUE.md`
- `../docs/PURE_MATH_MANUSCRIPT_ABSTRACT.md`
- `../docs/THEOREM_TO_FILE_MAP.md`

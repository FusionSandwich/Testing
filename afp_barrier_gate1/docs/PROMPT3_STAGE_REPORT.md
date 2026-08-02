# Prompt 3 stage report — spherical `Q=1` rigidity and quantitative stability

## 1. Repository boundary

Prompt 3 began from the frozen accepted baseline

```text
repository: FusionSandwich/Testing
branch:     agent/afp-pure-math-p0-m1
commit:     c88b57533c3c8ad8fd819e4e52a74c4b5a245479
tree:       92b3c0eaa45dd58befbc5af59790476d5c5d85b3
```

Development branch:

```text
agent/afp-pure-math-p3-q1-rigidity
```

The immutable transport archive remains outside this work:

```text
archive/afp-gate6-spatial-multigroup-verified
515f1aae6c20bd85711c90b5c1c21b4905252d01
```

No transport, Radiant, HTS, multigroup, evaluated-material, spatial-solver, or
production-solver scope belongs to this stage.

A second remote branch named
`agent/afp-pure-math-p3-global-rigidity-near-rigidity` was inspected before
continuing. It was still identical to the frozen baseline, so no parallel
implementation was overwritten.

## 2. Accepted dependencies

### Prompt 1

- exact positive local spherical feasibility;
- division-free antipodal classification;
- quantitative cone margin and perturbation bounds;
- global shared-edge cone/Farkas/LP package;
- exact local-not-global counterexamples; and
- reconciliation mechanisms.

### Prompt 2

- covariance and genuine sampled-space factorization;
- positive axial and corrected equivariant rigidity;
- exact signed regressions;
- centered versus uncentered product resonance; and
- rejected unrestricted spectral-product hierarchy.

### Pre-existing abstract Prompt 3 dependency

`AFPBarrier/GlobalLossRigidity.lean` already proves that a symmetric connected
active relation with local formula

```text
loss(i,j)=lambda/rate(i)
```

has one common rate and one common active-edge loss. Prompt 3 specializes and
quantifies that theorem rather than reproving it abstractly.

## 3. Principal exact theorem

Let

```text
g_i(j)=Omega_i dot Omega_j,
ell_ij=1-g_i(j),
r_i=sum_j a_ij,
D_i=sum_j a_ij ell_ij^2,
Q_i=r_i D_i/4,
```

for a finite positive generator with `Omega_i in S^2` and

```text
sum_j a_ij(Omega_j-Omega_i)=-2 Omega_i.
```

The coordinate equation gives

```text
sum_j a_ij ell_ij=2.
```

Weighted Cauchy--Schwarz and its exact variance remainder give

```text
Q_i>=1,
Q_i=1 iff ell_ij=2/r_i on every active edge from i.
```

If activity is symmetric and connected, the previously formalized abstract
propagation theorem yields

```text
r_i=r_* for every i,
ell_ij=2/r_* on every active edge.
```

This is now formalized in `AFPBarrier/SphericalQOneRigidity.lean` with explicit
handling of positive row rate, active zero-loss edges, and active antipodes.

## 4. Restricted classification theorem

The unrestricted Platonic-only statement is false. Exact shortest-edge cube
and dodecahedron generators satisfy the coordinate equation and `Q_i=1`.

The valid theorem assumes that the symmetric active graph is exactly the
one-skeleton of an injective strict convex minor-geodesic triangulation of
`S^2`, with every triangulation edge active and no active nonedge.

The global equality theorem makes every face equilateral. If `c` is the common
adjacent dot product and `alpha` a spherical face angle, then

```text
cos(alpha)=c/(1+c).
```

The positive Gram determinant gives `-1/2<c<1`, hence

```text
pi/3<alpha<pi.
```

A smooth triangulation has `q alpha=2pi` at every vertex, so

```text
q in {3,4,5}.
```

Euler and incidence identities give

```text
q=3: (V,E,F)=(4,6,4),
q=4: (V,E,F)=(6,12,8),
q=5: (V,E,F)=(12,30,20).
```

The corresponding graphs are tetrahedral, octahedral, and icosahedral. The
five-regular graph step has a direct proof in
`pure_math/rigidity/ICOSAHEDRAL_GRAPH_LEMMA.md`; it does not depend on a
numerical graph database. Equal chord-triangle faces and convex Cauchy rigidity
then identify the embedded geometry up to an orthogonal transformation.

Exact adjacent data are:

| degree | active dot | active loss | common row rate |
|---:|---:|---:|---:|
| 3 | `-1/3` | `4/3` | `3/2` |
| 4 | `0` | `1` | `2` |
| 5 | `1/sqrt(5)` | `1-1/sqrt(5)` | `(5+sqrt(5))/2` |

The classification fixes the geometry and total row rate. It does not assert
uniformity of every individual edge rate.

## 5. Quantitative near-rigidity

For a general positive eigenvalue `lambda`, write

```text
m_i=lambda/r_i,
p_ij=a_ij/r_i,
Q_i=r_i D_i/lambda^2.
```

The exact normalized identity is

```text
Q_i-1=sum_j p_ij(ell_ij/m_i-1)^2.
```

### Multiplicative version

If

```text
Q_i<=1+epsilon,
p_ij>=p_*>0 on active edges,
delta=sqrt(epsilon/p_*)<1,
kappa=(1+delta)/(1-delta),
```

then:

```text
|ell_ij/m_i-1|<=delta,
kappa^-1<=m_j/m_i<=kappa on a shared edge,
kappa^-1<=r_j/r_i<=kappa.
```

Along a path of length `n`, the ratio bounds acquire `kappa^n`. If the active
diameter is at most `D`, then all active edge losses lie between

```text
(1-delta)kappa^-D m_o
and
(1+delta)kappa^D m_o,
```

and any two active losses differ by at most a factor `kappa^(2D+1)`.

### Additive version

If

```text
r_i D_i-lambda^2<=eta,
r_i>=r_min>0,
a_ij>=a_min>0 on active edges,
Delta=sqrt(eta/(r_min a_min)),
```

then:

```text
|ell_ij-m_i|<=Delta,
|m_i-m_j|<=2Delta on a shared edge,
|m_i-m_o|<=2DDelta,
|ell_ij-m_o|<=(2D+1)Delta.
```

Any two active losses differ by at most `2(2D+1)Delta`. If also
`r_i<=r_max`, then

```text
|r_i-r_o|<=2D r_max^2 Delta/lambda.
```

Shared-conductance lower bounds transfer to the required active-rate floors
under explicit upper mass and row-rate bounds.

## 6. Sharp hypothesis boundaries

The exact rare-edge family

```text
p_1=t^4,
p_2=1-t^4,
x_1=1+1/t,
x_2=1-t^3/(1-t^4)
```

has mean one and variance `t^2/(1-t^4)` tending to zero while `x_1` diverges.
A lower active-weight condition or equivalent structural hypothesis is
therefore necessary for uniform edgewise control.

Other retained boundaries are:

- disconnected components may have different equality centers;
- local multiplicative overlap can accumulate along long paths, so diameter
  appears in the global constant;
- directed support does not supply a second endpoint estimate;
- signed rates invalidate the weighted-square argument; and
- edge-metric concentration does not imply coordinate-space closeness without
  a gauge-fixed framework-rigidity singular-value margin.

## 7. Formalization

New Lean module:

```text
AFPBarrier/SphericalQOneRigidity.lean
```

It formalizes:

- row-rate positivity at a nonzero exact eigenvalue;
- exact local active-loss equality;
- strict active-loss positivity and zero-loss exclusion;
- connected spherical rate/loss propagation;
- the active-antipode row-rate consequence;
- equilateral tangent-angle algebra;
- Euler/incidence arithmetic and the three count triples;
- a raw per-edge additive gap estimate;
- additive shared-edge center comparison; and
- multiplicative shared-edge cross bounds.

The module is imported by `AFPBarrier.lean` and included in
`AFPBarrier/PureMathAxiomAudit.lean`.

No graph-classification, topology, Cauchy-rigidity, or differential-geometric
statement is introduced as a project axiom.

## 8. Exact audits

New audit:

```text
pure_math/rigidity/prompt3_rigidity_audit.py
```

It uses exact rational and `Q(sqrt(5))` arithmetic to verify:

- coordinate eigenmap and `Q=1` for all five Platonic shortest-edge graphs;
- tetrahedral/octahedral/icosahedral triangular-sphere incidence;
- cube/dodecahedron nontriangulation;
- exact `q=3,4,5` dots, row rates, and Euler counts;
- graph certificates;
- normalized variance;
- multiplicative and additive constants;
- the rare-edge counterfamily; and
- conductance-floor transfer.

Floating-point rank or geometry thresholds are not proof evidence.

## 9. Independent approach and adversarial audit

Literal multiagent-v2 is not exposed in this environment and was not used.
The separate routes and kill criteria are committed in

```text
docs/PROMPT3_APPROACH_REGISTRY.md.
```

Independent routes covered direct Cauchy equality, transfer through the prior
Lean theorem, spherical face geometry, Euler/combinatorial classification,
convex rigidity, normalized and raw stability, and conditional framework
rigidity. Adversarial routes tested nontriangulated Platonic examples,
antipodes, coincident endpoints, signed rates, directed supports, rare edges,
long paths, nonconvex geometry, and vanishing rigidity margins.

## 10. Prior-art boundary

Prompt 3 does not claim novelty for:

- weighted Cauchy--Schwarz or variance;
- Euler's identity;
- the classification of Platonic solids;
- Cauchy convex-polyhedron rigidity;
- planar-triangulation generation;
- spherical matchstick graphs; or
- generic framework rigidity.

The prior-art map now includes the direct neighboring work of Izmestiev--Lam,
Swanepoel, Brinkmann--McKay, and Connelly--Gortler. The project contribution is
the integrated positive-eigenmap equality/stability theorem with exact support
hypotheses and counterexample boundaries.

## 11. Verification status

Dedicated workflow:

```text
.github/workflows/afp-prompt3-rigidity.yml
```

The workflow asserts the literal checked-out head, runs every exact Prompt 1–3
audit, rejects placeholders and singular/plural user axioms, builds Lean,
runs the focused axiom audit, independently checks the Prompt 3 declarations
with nanoda, verifies the immutable archive SHA, and rejects out-of-scope paths.

Final accepted implementation and target-branch workflow identifiers are added
to the integration record only after all exact-head gates are green.

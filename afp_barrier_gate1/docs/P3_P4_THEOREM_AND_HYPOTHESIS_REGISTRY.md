# Prompt 3–4 theorem and hypothesis registry

Each entry records the ordinary theorem, complete hypothesis boundary, proof and formal source, exact audit, deleted-hypothesis failure, sampling boundary where applicable, and final status.

## T1. Exact spherical `Q=1` transfer

**Status:** PROVED

For a finite positive reversible spherical coordinate eigenmap with shared conductances, positive masses, conservative off-diagonal rates, and `L Omega=-2 Omega`, define

```text
ell_ij=1-Omega_i·Omega_j,
r_i=sum_j a_ij,
epsilon_i=sum_j a_ij ell_ij^2,
p_ij=a_ij/r_i,
x_ij=r_i ell_ij/2,
Q_i=r_i epsilon_i/4.
```

Then

```text
sum_j a_ij ell_ij=2,
r_i>0,
sum_j p_ij=1,
sum_j p_ij x_ij=1,
Q_i=sum_j p_ij x_ij^2,
Q_i-1=sum_j p_ij(x_ij-1)^2.
```

At `Q_i=1`, every active incident edge has `ell_ij=2/r_i`. Positive shared conductances make activity symmetric; connectedness propagates one global row rate and active-edge loss.

**Proof source:** `pure_math/rigidity/GLOBAL_Q_RIGIDITY_THEOREM.md` §§1–2.
**Lean:** `SphericalQEqualityRigidity.lean`.
**Exact audit:** `global_near_rigidity_audit.py`.
**Deleted hypotheses:** without positivity, reversibility, or connectedness, propagation fails componentwise or directionally. Loops and zero-conductance permitted edges are inactive.

## T2. Restricted geodesic-triangulation classification

**Status:** PROVED UNDER EXPLICIT HYPOTHESES

Assume additionally a finite simple topological-sphere triangulation whose one-skeleton is exactly the active graph, an injective embedding by unique minor great-circle arcs, noncrossing edge interiors, nondegenerate geodesically convex triangular faces, pairwise-disjoint face interiors, complete round-sphere coverage, no cone defect or multiple cover, and positive conductance on every triangulation edge. If `Q_i=1` at every vertex, the realization is, up to `O(3)`, exactly the regular tetrahedral, octahedral, or icosahedral spherical triangulation; after orientation is fixed, uniqueness is up to `SO(3)`.

The proof establishes common side length, congruent equilateral faces, common angle, angle sum `2*pi`, constant valence, Euler restriction `q in {3,4,5}`, direct combinatorial uniqueness, and forced adjacent-face propagation.

| `q` | `V` | `E` | `F` | `cos theta` | `ell` | `r` |
|---:|---:|---:|---:|---:|---:|---:|
| 3 | 4 | 6 | 4 | `-1/3` | `4/3` | `3/2` |
| 4 | 6 | 12 | 8 | `0` | `1` | `2` |
| 5 | 12 | 30 | 20 | `1/sqrt(5)` | `1-1/sqrt(5)` | `(5+sqrt(5))/2` |

**Proof source:** theorem package §3.
**Lean:** selected spherical algebra and Euler identities in the accepted narrow and rich modules; the complete geometric classification remains an ordinary proof.
**Exact audit:** exact Platonic Gram/hull regressions and source-pinned plantri hostile search.
**External input:** only standard spherical trigonometry and verified finite planar-map facts; enumeration is not the proof.
**Deleted hypotheses:** cube and dodecahedron kill unrestricted graph claims; major arcs, cone defects, incomplete coverage, inactive triangulation edges, repeated states, and nonreversible/signed systems kill the transfer.

## T3. Pointwise and pathwise near-rigidity

**Status:** PROVED

Assume connected symmetric activity, `p_ij>=kappa>0`, `1<=Q_i<=1+eta`, and

```text
delta=sqrt(eta/kappa)<1,
q_delta=(1+delta)/(1-delta),
s_delta=log q_delta,
h_delta=-log(1-delta).
```

Then

```text
|x_ij-1|<=delta,
(1-delta)/(1+delta)<=r_i/r_j<=(1+delta)/(1-delta),
|log r_i-log r_j|<=s_delta,
q_delta^(-dist(i,j))<=r_i/r_j<=q_delta^(dist(i,j)),
r_max/r_min<=q_delta^D,
ell_max/ell_min<=q_delta^(D+1).
```

For graph center `o`, radius `R_G`, `ell_ref=2/r_o`, and `B_delta=h_delta+R_G s_delta`,

```text
|log(ell_e/ell_ref)|<=B_delta.
```

**Proof source:** theorem package §4.
**Lean:** `weight_floor_mul_deviation_sq_le`, `pointwise_deviation_sq_le_eta_div_kappa`, `pointwise_delta_bound`, adjacent-rate and incident-loss declarations.
**Exact audit:** 174,816 path stress cases and exact variance examples.
**Deleted hypotheses:** `delta<1` is required for positive lower factors; small `kappa` and long paths demonstrate necessary dependence.

## T4. Spectral-gap refinement

**Status:** PROVED

With

```text
mu_i=w_i r_i,
pi_i=mu_i/sum_k mu_k,
P_ij=p_ij,
c_ij=pi_i p_ij=pi_j p_ji,
u_i=log r_i,
```

and Dirichlet form

```text
E_P(u)=1/2 sum_i pi_i sum_j p_ij(u_i-u_j)^2,
```

one has

```text
E_P(log r)<=2 eta/(1-delta)^2,
Var_pi(log r)<=2 eta/((1-delta)^2 lambda_P).
```

**Proof source:** theorem package §5.
**Lean:** finite edge inequalities; variational step ordinary.
**Exact audit:** reversible small-graph and path checks.
**Deleted hypotheses:** without reversibility the symmetric conductance normalization and stated Poincaré form do not follow.

## T5. Effective-resistance refinement

**Status:** PROVED

For the undirected conductances `c_ij`, with effective resistance normalized by the same Dirichlet form,

```text
|log r_i-log r_j|
  <=sqrt(2 eta R_eff(i,j))/(1-delta).
```

**Proof source:** theorem package §5.4, Dirichlet principle.
**Exact audit:** exact rational path resistance and endpoint slack.
**Deleted hypotheses:** large resistance examples show that a metric-free uniform pointwise bound is false.

## T6. Explicit angle and valence stability

**Status:** PROVED UNDER EXPLICIT HYPOTHESES

Under the near-equality triangulation hypotheses, define the graph-center loss interval, `theta_ref`, the positive side-sine floor, and

```text
Delta_theta=ell_ref(exp(B_delta)-1)/sigma_ref.
```

On each certified Platonic side box, the spherical Gram/Heron factorization

```text
D=4 sin(S) sin(S-a) sin(S-b) sin(S-c)
```

provides an explicit positive angle-sine floor and derivative constant `C_ang`. The active-degree bound `deg(i)<=floor(1/kappa)` and exact angular separation force constant valence below the displayed threshold. The final edge-sup estimate is

```text
max_e |theta_e-theta_q|
  <=Delta_theta(1+C_ang/m_eq).
```

Conservative accepted thresholds are

```text
q=3: eta_* = 3.90838234361e-6
q=4: eta_* = 2.07429596521497e-7
q=5: eta_* = 7.942143600537101e-10
```

for the reference `kappa` values encoded by the audit. Positive-width Gram determinant floors are approximately `0.3818972454`, `0.3810797447`, and `0.0217243113`.

**Proof source:** theorem package §6.
**Exact audit:** zero-defect and positive-width boxes, nonzero threshold tests, arc conversion, exact valence gaps.
**Deleted hypotheses:** coordinate-level framework stability is not inferred from edge-metric stability; the old endpoint-product angle certificate is rejected.

## T7. Non-antipodal `Q=1` covariance decomposition

**Status:** PROVED

For

```text
C_i=sum_j a_ij(Omega_j-Omega_i)(Omega_j-Omega_i)^T,
M_i=P_0(C_i+2 Omega_i Omega_i^T),
P_i=I-Omega_i Omega_i^T,
```

one always has `tr C_i=4` and `Omega_i^T C_i Omega_i=4Q_i/r_i`. At `Q_i=1` and `0<ell_i<2`, the normalized tangent directions and `T_i=sum_j p_ij u_ij u_ij^T` satisfy

```text
sum_j p_ij u_ij=0,
tr T_i=1,
T_i Omega_i=0,
C_i=2(2-ell_i)T_i+2ell_i Omega_i Omega_i^T,
M_i=3ell_i(Omega_i Omega_i^T-I/3)
    +2(2-ell_i)(T_i-P_i/2).
```

Axial covariance holds iff `T_i=P_i/2`.

**Proof source:** theorem package §7.
**Lean:** `QEqualityCovariance.lean`.
**Exact audit:** symbolic covariance decomposition.
**Sampling boundary:** axial form-space rigidity implies the accepted sampled conclusion only through the explicit sampling map and kernel theorem.

## T8. Antipodal radial boundary

**Status:** PROVED BOUNDARY CASE

At `ell=2`, equality forces `r=1` and

```text
C=4 Omega Omega^T,
2(2-ell)=0.
```

There is no geometrically determined unit tangent direction because `sqrt(ell(2-ell))=0`.

**Lean:** `qOne_antipodal_tangent_coefficient_zero` and `qOne_antipodal_covarianceEntry`.
**Exact audit:** two-state antipodal regression.
**Deleted hypothesis warning:** the tangent-frame theorem is false as written if extended to `ell=2`.

## T9. Weighted-octahedral anisotropy

**Status:** PROVED EXACT EXAMPLE

On `+/-e_1,+/-e_2,+/-e_3`, assign positive axis-pair conductances `g_12,g_13,g_23` and masses

```text
w_1=g_12+g_13,
w_2=g_12+g_23,
w_3=g_13+g_23.
```

Then `L Omega=-2 Omega`, `r_i=2`, `ell_e=1`, and `Q_i=1`. Global axial covariance holds iff `g_12=g_13=g_23`; tangential anisotropy approaches operator norm `1/2` while `eta=0`.

**Lean:** selected tangent-weight and axial-iff identities.
**Exact audit:** `q1_covariance_audit.py`.
**Killed claim:** `Q=1` or scalar `eta` control alone forces axial covariance.

## T10. Weighted-octahedral sampled degree-two space

**Status:** PROVED EXACT EXAMPLE

For every positive member, the genuine sampled degree-two exact space is `{0}`. The certificate is

```text
det(P+2I)=
6(g_12+g_13+g_23)(g_12g_13+g_12g_23+g_13g_23)
/((g_12+g_13)(g_12+g_23)(g_13+g_23)) > 0.
```

**Proof source:** sampling-map argument in theorem §7.5.
**Exact audit:** symbolic determinant and explicit unequal specialization.
**Sampling boundary:** this conclusion is not a form-space rank calculation.

## T11. Prompt 4 polar remainder bounds

**Status:** PROVED

For every integer `N>=2`,

```text
0 <= r_polar(N)
     -[(8/pi^4)N^4+(10/(3pi^2))N^2+13/45]
  <= pi^2/(48N^2),
```

and

```text
0 <= Q_pole(N)-[N^2/pi^2+7/12]
  <= pi^2/(12N^2).
```

**Proof source:** `SHARP_PRODUCT_GRAPH_BARRIERS.md`.
**Lean:** `SharpProductBarriers.lean`.
**Exact audit:** `prompt4_sharp_barrier_audit.py`.
**Final treatment:** theorem statement and constants preserved unchanged by reconciliation.

## T12. Prompt 4 fixed-graph minimax obstruction

**Status:** PROVED

The polar coordinate equations uniquely force the inward meridional rate `1/(2 sin^2 h)` and each azimuthal rate `1/(4 sin^4 h)` on the fixed unreduced square product graph. The exact graph-class minimax maximum rate has sharp leading constant `8/pi^4`.

**Proof, Lean, audit:** accepted Prompt 4 package.
**Deleted hypotheses:** no ring-symmetry assumption is used; changing the graph class changes the statement.

## T13. Prompt 4 universal rate and extremal bounds

**Status:** PROVED

The package proves

```text
epsilon_i<=C h^2  =>  r_i>=4/(C h^2),
E_K>=4/(RK),
C*>=4/R,
```

fixed-`K` minimizer existence, and strict exclusion of the unreduced product family from linear-rate classes at large order.

**Proof, Lean, audit:** accepted Prompt 4 theorem, `SharpProductBarriers.lean`, exact regression.
**Final treatment:** preserved unchanged.

## T14. Prompt 4 feasible-cone and reduced-ring results

**Status:** PROVED UNDER EXPLICIT HYPOTHESES

The accepted package contains the projective feasible-cone formula for `Q`, the fixed-mean sliced LP, an explicit dual anisotropy certificate, sharp equality examples, and the stated biregular/perfect-matching reduced-ring incidence obstruction.

**Boundary:** no general split/merge reduced-ring theorem is claimed.
**Final treatment:** preserved and revalidated.

## Computational and external status summary

| Item | Status |
|---|---|
| Source-pinned plantri counts `1,1,2,5,14,50,233,1249,7595`, total 9,150 | COMPUTATIONAL |
| Plantri as classification proof | REJECTED |
| Standard spherical trigonometry, Euler identities, Poincaré and Dirichlet principles | EXTERNAL |
| Coordinate-level stability from edge lengths alone | DEFERRED |
| Optimal near-rigidity constants | CONJECTURE / not claimed |

The literal final candidate SHA/tree, workflow run/job identifiers, artifact IDs/digests, final target SHA/tree, and post-integration workflow identifiers are recorded in the authoritative acceptance comment on the final reconciliation PR.

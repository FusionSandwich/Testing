# Exact global `Q=1` rigidity and quantitative near-rigidity

## Status and scope

This document gives the ordinary mathematical proof of the Prompt 3 theorem
package.  Its scope is the finite positive reversible spherical generator
specified below.  The classification theorem is deliberately restricted to an
actual nondegenerate minor-arc geodesic triangulation of the round sphere.
Cube and dodecahedron shortest-edge generators remain exact `Q=1`
counterexamples to every unrestricted Platonic claim.

The finite scripts in this directory are falsification and regression evidence;
they are not substitutes for the all-orders proofs in this document.  Selected
finite algebra is mirrored in Lean.  Standard spherical trigonometry, Euler's
formula for a triangulated sphere, the elementary Dirichlet principle, and the
Poincare variational definition are identified explicitly when used.

---

## 1. Finite spherical generator and normalization

Let `V` be finite, let `Omega_i in S^2 subset R^3`, and let `w_i>0`.  Let
`E` be an undirected simple graph.  On every `{i,j} in E`, let
`gamma_ij=gamma_ji>0`; put

```text
a_ij = gamma_ij/w_i  on E,
a_ij = 0              off E,
r_i  = sum_{j != i} a_ij.
```

The conservative generator is

```text
(Lf)_i = sum_{j != i} a_ij(f_j-f_i).
```

Assume the coordinate eigenmap equation

```text
sum_j a_ij(Omega_j-Omega_i) = -2 Omega_i                 (1.1)
```

at every vertex.  Put

```text
ell_ij     = 1-Omega_i dot Omega_j,
epsilon_i = sum_j a_ij ell_ij^2,
Q_i       = r_i epsilon_i/4,
p_ij      = a_ij/r_i
```

whenever `r_i>0`.

### Proposition 1.1 — exact local moment and variance identities

At every vertex,

```text
sum_j a_ij ell_ij = 2,                                  (1.2)
r_i>0,                                                   (1.3)
sum_j p_ij = 1,                                         (1.4)
sum_j p_ij (r_i ell_ij/2) = 1,                         (1.5)
Q_i = sum_j p_ij (r_i ell_ij/2)^2,                     (1.6)
Q_i-1 = sum_j p_ij (r_i ell_ij/2-1)^2.                 (1.7)
```

#### Proof

Take the Euclidean inner product of (1.1) with `Omega_i`.  Since
`|Omega_i|=1`,

```text
sum_j a_ij(Omega_i dot Omega_j-1)=-2,
```

which is (1.2).  Every off-diagonal rate and every spherical loss is
nonnegative.  If `r_i=0`, all `a_ij=0`, contradicting (1.2); hence (1.3).
Equations (1.4) and (1.5) follow by division by `r_i` and by (1.2).
Moreover

```text
sum_j p_ij (r_i ell_ij/2)^2
 = sum_j (a_ij/r_i)(r_i^2 ell_ij^2/4)
 = r_i epsilon_i/4
 = Q_i,
```

which proves (1.6).  Finally, expand the square and use (1.4)–(1.6):

```text
sum_j p_ij(x_ij-1)^2
 = sum_j p_ij x_ij^2 -2 sum_j p_ij x_ij +sum_j p_ij
 = Q_i-2+1=Q_i-1,
```

where `x_ij=r_i ell_ij/2`.  This proves (1.7).  Notice that no diagonal
rate, sign convention, or alternative normalization enters these equations.

A first consequence is `Q_i>=1`.

---

## 2. Exact spherical equality transfer

Define the directed active relation by

```text
active(i,j) iff i != j and a_ij>0.
```

### Theorem 2.1 — local `Q_i=1` fixes every active loss

If `Q_i=1`, then, for every active `i -> j`,

```text
ell_ij = 2/r_i.                                         (2.1)
```

#### Proof

By (1.7), a sum of nonnegative terms is zero.  If `a_ij>0`, then
`p_ij>0`, so its term vanishes:

```text
r_i ell_ij/2-1=0.
```

Since `r_i>0`, this is (2.1).

### Theorem 2.2 — connected global equality propagation

Assume `Q_i=1` at every vertex and that the active graph is connected.  Then
there is one number `r>0` such that

```text
r_i=r                                                    (2.2)
```

for every vertex, and one number

```text
ell=2/r>0                                               (2.3)
```

such that every active undirected edge has loss `ell`.

#### Proof with all propagation premises

1. **Symmetric activity.**  If `a_ij>0`, then
   `gamma_ij=w_i a_ij>0`.  Shared conductance gives
   `gamma_ji=gamma_ij>0`, and `w_j>0` gives
   `a_ji=gamma_ji/w_j>0`.  Thus activity is symmetric.
2. **Symmetric loss.**  The Euclidean inner product is symmetric, so
   `ell_ij=1-Omega_i dot Omega_j=ell_ji`.
3. **One shared edge.**  On an active `{i,j}`, Theorem 2.1 in both
   directions gives

   ```text
   2/r_i=ell_ij=ell_ji=2/r_j.
   ```

   Positivity of the row rates implies `r_i=r_j`.
4. **Connected propagation.**  Equality of rates propagates along every
   active path.  Connectedness yields (2.2), and Theorem 2.1 then yields
   (2.3).

This is the spherical specialization of the already-formalized abstract
propagation theorem in `AFPBarrier/GlobalLossRigidity.lean`.

### Degeneracy audit

* Loops are excluded from the off-diagonal active relation.
* An active coincident edge would have `ell_ij=0`, contradicting
  `ell_ij=2/r_i>0`.
* A zero row rate contradicts the normal moment (1.2).
* If `ell=2`, every active edge is antipodal and `r=1`.  This is a valid
  separate equality case; it is excluded from the triangulation theorem by
  injectivity, nondegenerate faces, and edge lengths in `(0,pi)`.
* Repeated embedded vertices can occur in an abstract graph but violate the
  injective triangulation hypothesis.
* A permitted graph edge with `gamma_ij=0` is inactive.  Equality propagation
  controls only strictly active edges; Theorem P3-R therefore requires every
  triangulation edge to have positive conductance.

If `0<ell<2`, the unique minor geodesic between the endpoints has common
length

```text
theta=arccos(1-ell) in (0,pi).                          (2.4)
```

---

## 3. Restricted exact classification

### Theorem P3-R — exact restricted global `Q=1` classification

In addition to Sections 1–2, assume:

1. `K` is a finite simple abstract triangulation of the topological sphere;
2. `E` is exactly its one-skeleton;
3. `Omega` is injective;
4. each edge is the unique minor great-circle arc between its endpoints, of
   length in `(0,pi)`;
5. interiors of two edge arcs meet only when the abstract edges share an
   endpoint;
6. each face maps homeomorphically to the geodesically convex spherical
   triangle bounded by its three minor arcs;
7. face interiors are pairwise disjoint;
8. the face images cover the round sphere;
9. every triangulation edge has positive conductance; and
10. `Q_i=1` at every vertex.

Then, up to `O(3)`, the embedded triangulation is exactly the regular
spherical tetrahedron, octahedron, or icosahedron.  Once an orientation is
fixed, the ambiguity is `SO(3)`.

### 3.1 Common side and face geometry

By Theorem 2.2, every edge has the same loss and hence the same minor length
`theta`.  Every face is therefore an equilateral geodesically convex spherical
triangle.  Let its common interior angle be `alpha`.

The spherical law of cosines for an equilateral triangle gives

```text
cos theta
 = cos^2 theta + sin^2 theta cos alpha.
```

Because `theta in (0,pi)`, `1+cos theta>0`, and rearrangement yields

```text
cos alpha = cos theta/(1+cos theta).                    (3.1)
```

The spherical excess of a positive-area equilateral triangle is
`3alpha-pi`, so

```text
alpha>pi/3.
```

Geodesic convexity and nondegeneracy give `alpha<pi`.  Substituting this in
(3.1), with `1+cos theta>0`, gives

```text
cos theta>-1/2,
```

hence

```text
pi/3<alpha<pi,
0<theta<2pi/3.                                          (3.2)
```

### 3.2 Constant valence

Fix a vertex.  The embedded faces incident to it form, by hypotheses 5–8, a
partition of a sufficiently small round metric disk about that point.  There
is no overlap, gap, or cone singularity.  Therefore their angles sum to
`2pi`.  If the vertex valence is `q_i`, all incident angles equal `alpha`, so

```text
q_i alpha=2pi.
```

The same `alpha` is used at every vertex; consequently every vertex has the
same integer valence

```text
q=2pi/alpha.                                            (3.3)
```

Constant valence was not assumed; it follows only after common face geometry
and the round-sphere angle sum have been proved.

### 3.3 Euler restriction and exact counts

For a simple triangulation of the sphere,

```text
qV=2E,
3F=2E,
V-E+F=2.
```

Eliminating `E,F` gives

```text
V(1-q/2+q/3)=2,
V(6-q)=12,
V=12/(6-q).                                             (3.4)
```

Every vertex in a simple spherical triangulation has degree at least `3`.
Equation (3.2)–(3.3) gives `q<6`.  Hence

```text
q in {3,4,5}.
```

The exact counts are

| `q` | `V` | `E=qV/2` | `F=2E/3` |
|---:|---:|---:|---:|
| 3 | 4 | 6 | 4 |
| 4 | 6 | 12 | 8 |
| 5 | 12 | 30 | 20 |

### 3.4 Combinatorial uniqueness

The uniqueness proof is elementary and uses the fact that `K` is a simple
triangulated 2-manifold.

#### `q=3`, `V=4`

A simple 3-regular graph on four vertices makes every vertex adjacent to all
other vertices.  Its graph is `K4`; its four 3-cycles are the tetrahedral
faces.

#### `q=4`, `V=6`

The complement of a simple 4-regular graph on six vertices is 1-regular, hence
a perfect matching.  All perfect matchings on six vertices are isomorphic.
The original graph is therefore `K6` with three disjoint edges removed, the
octahedral graph.  Its planar triangular embedding has the eight octahedral
faces.

#### `q=5`, `V=12`

Choose a vertex `v`.  Its link in a simple triangulated 2-manifold is an
embedded 5-cycle

```text
a_0 a_1 a_2 a_3 a_4 a_0.
```

For every boundary edge `a_i a_{i+1}`, let `b_i` be the third vertex of the
face on the side opposite `v` (indices modulo five).  The link of `a_i` is a
5-cycle.  One of its two arcs from `a_{i-1}` to `a_{i+1}` is
`a_{i-1},v,a_{i+1}`; the other therefore has exactly two internal vertices,
namely `b_{i-1},b_i`.  Thus

```text
b_{i-1} != b_i,
a_i b_{i-1}, a_i b_i, b_{i-1}b_i
```

are edges, and `(a_i,b_{i-1},b_i)` is a face.

The five faces `(a_i,b_{i-1},b_i)` form the inner boundary of the closed
simplicial collar of the link of `v`.  In a triangulated 2-manifold the
frontier of such a collar is an embedded 1-manifold.  It is connected here,
so it is a simple cycle.  Therefore the five `b_i` are distinct and

```text
b_0 b_1 b_2 b_3 b_4 b_0
```

is a 5-cycle.  This collar assertion can also be checked directly from the
cyclic links: a repeated nonconsecutive `b_i` would make the frontier have
four incident collar edges at that vertex, contradicting that its link is a
circle.

The vertices named so far are `v`, five `a_i`, and five `b_i`, hence eleven
of the twelve vertices.  Let the remaining vertex be `z`.  Each `b_i` already
has four distinct neighbors

```text
a_i, a_{i+1}, b_{i-1}, b_{i+1}.
```

Its degree is five.  The only available fifth neighbor in the residual disk
bounded by the `b`-cycle is `z`; hence `z` is adjacent to every `b_i`.  No
other edges are possible because all degrees are now five.  This is precisely
the icosahedral graph, with the usual twenty triangular faces.  Thus no
external “Platonic solids” assertion is being used as a missing uniqueness
lemma.

### 3.5 Exact side lengths, losses, and rates

From `alpha=2pi/q` and (3.1),

```text
cos theta = cos alpha/(1-cos alpha),
ell=1-cos theta,
r=2/ell.                                                (3.5)
```

Therefore:

| type | `q` | `cos theta` | `ell` | `r` |
|---|---:|---:|---:|---:|
| tetrahedron | 3 | `-1/3` | `4/3` | `3/2` |
| octahedron | 4 | `0` | `1` | `2` |
| icosahedron | 5 | `1/sqrt(5)` | `1-1/sqrt(5)` | `(5+sqrt(5))/2` |

For `q=5`, rationalization gives

```text
2/(1-1/sqrt(5))=(5+sqrt(5))/2.
```

### 3.6 Geometric uniqueness

Take two realizations with the same abstract triangulation and the side length
from (3.5).  An element of `O(3)` maps one chosen oriented face of the first
realization to the corresponding face of the second.  Suppose two
corresponding faces already agree and consider a face adjacent across an edge
with endpoints `x,y`.  A third unit vector `z` for an equilateral face must
satisfy

```text
z dot x=z dot y=cos theta.
```

There are exactly two such points, reflected across the plane through
`0,x,y`.  One is on each side of the shared great circle.  Pairwise disjoint
convex face interiors and full-sphere coverage require the adjacent face to
use the point on the side opposite the already fixed face.  It is therefore
unique.

The dual graph of a triangulation of a connected sphere is connected.
Propagating across a dual spanning tree fixes every face and vertex.  Existing
realizations guarantee consistency on dual cycles; the argument compares the
two realizations and does not assume a separate framework-rigidity theorem.
Thus the realization is unique up to `O(3)`.  If the orientation of the first
face is prescribed, the initial isometry lies in `SO(3)`, and so does the
resulting global isometry.

---

## 4. Quantitative near-rigidity on a connected reversible active graph

Assume

```text
p_ij>=kappa>0                    on every active directed edge,
1<=Q_i<=1+eta                    at every vertex.
```

Set

```text
x_ij    = r_i ell_ij/2,
delta   = sqrt(eta/kappa),
q_delta = (1+delta)/(1-delta),
s_delta = log q_delta,
h_delta = -log(1-delta),
```

and assume `delta<1`.

### 4.1 Pointwise edge control

By (1.7),

```text
p_ij(x_ij-1)^2<=Q_i-1<=eta.
```

Since `p_ij>=kappa`,

```text
|x_ij-1|<=sqrt(eta/kappa)=delta,
1-delta<=x_ij<=1+delta.                                (4.1)
```

### 4.2 Adjacent and pathwise rate control

On a shared active edge, `ell_ij=ell_ji>0`, so

```text
r_i/r_j=x_ij/x_ji.
```

Using (4.1),

```text
(1-delta)/(1+delta) <= r_i/r_j <= (1+delta)/(1-delta), (4.2)
|r_i/r_j-1| <= 2delta/(1-delta),                       (4.3)
|log r_i-log r_j| <= s_delta.                          (4.4)
```

Multiplying (4.2) along a shortest path gives

```text
q_delta^(-dist(i,j)) <= r_i/r_j <= q_delta^(dist(i,j)). (4.5)
```

If the active-graph diameter is `D`,

```text
r_max/r_min<=q_delta^D.                                (4.6)
```

The exponential dependence on graph distance is displayed rather than hidden.
Long paths show that no diameter-free conclusion follows from only local
pointwise control.

### 4.3 Edge-loss control

For two active edges at the same vertex,

```text
ell_ij/ell_ik=x_ij/x_ik,
```

and hence

```text
q_delta^(-1)<=ell_ij/ell_ik<=q_delta.                  (4.7)
```

For arbitrary active edges `e={i,j}` and `e'={k,l}`, orient them from `i` and
`k`.  Then

```text
ell_e/ell_e'=(x_ij/x_kl)(r_k/r_i),
```

so (4.1) and (4.5) imply

```text
ell_max/ell_min<=q_delta^(D+1).                        (4.8)
```

Let `o` be a graph center, with eccentricity equal to the graph radius `R_G`,
and put

```text
ell_ref=2/r_o.
```

For an active edge `e={i,j}` oriented from `i`,

```text
ell_e/ell_ref=x_ij r_o/r_i.
```

On `[1-delta,1+delta]`,

```text
|log x_ij|<=-log(1-delta)=h_delta.
```

Therefore

```text
|log(ell_e/ell_ref)|
 <=h_delta+dist(o,i)s_delta
 <=B_delta:=h_delta+R_G s_delta.                       (4.9)
```

Equivalently,

```text
ell_ref exp(-B_delta)<=ell_e<=ell_ref exp(B_delta),     (4.10)
|ell_e-ell_ref|<=ell_ref(exp(B_delta)-1).               (4.11)
```

For two edges, (4.11) gives the explicit additive bound

```text
|ell_e-ell_e'|<=2 ell_ref(exp(B_delta)-1).              (4.12)
```

### 4.4 Conversion to minor geodesic length

Assume a certified common interval

```text
0<ell_-<=ell_e<=ell_+<2.
```

Set

```text
sigma_arc=min(
 sqrt(ell_-(2-ell_-)),
 sqrt(ell_+(2-ell_+)))>0.
```

For `theta(ell)=arccos(1-ell)`,

```text
theta'(ell)=1/sqrt(ell(2-ell)).
```

The function under the square root is concave, so its minimum on the interval
is attained at an endpoint.  The mean-value theorem gives

```text
|theta_e-theta_e'|<=|ell_e-ell_e'|/sigma_arc.           (4.13)
```

Combining (4.12) and (4.13),

```text
max_{e,e'} |theta_e-theta_e'|
 <=2 ell_ref(exp(B_delta)-1)/sigma_arc.                 (4.14)
```

No asymptotic `O(sqrt eta)` notation is used.

---

## 5. Spectral-gap and effective-resistance refinement

Define

```text
mu_i=w_i r_i,
Z=sum_k mu_k,
pi_i=mu_i/Z,
P_ij=p_ij.
```

### 5.1 Reversibility

Since `a_ij=gamma_ij/w_i`,

```text
p_ij=gamma_ij/(w_i r_i)=gamma_ij/mu_i.
```

Consequently

```text
pi_i p_ij=gamma_ij/Z=gamma_ji/Z=pi_j p_ji.             (5.1)
```

Thus `P` is reversible with stationary probability `pi`.

### 5.2 Dirichlet-energy estimate

Let `u_i=log r_i` and

```text
E_P(u)=1/2 sum_i pi_i sum_j p_ij(u_i-u_j)^2.
```

On a shared edge,

```text
u_i-u_j=log x_ij-log x_ji.
```

For `x in [1-delta,1+delta]`, the mean-value theorem gives

```text
|log x|<=|x-1|/(1-delta).
```

Hence

```text
(u_i-u_j)^2
 <=2((x_ij-1)^2+(x_ji-1)^2)/(1-delta)^2.              (5.2)
```

Insert (5.2) into the Dirichlet form.  The first directed variance average is
at most `eta` by (1.7).  The second is also at most `eta` after swapping
`i,j` with (5.1).  Therefore

```text
E_P(log r)<=2eta/(1-delta)^2.                           (5.3)
```

### 5.3 Poincare bound

With

```text
lambda_P=inf_{Var_pi(v)>0} E_P(v)/Var_pi(v)>0,
```

the variational definition directly yields

```text
Var_pi(log r)
 <=2eta/((1-delta)^2 lambda_P).                         (5.4)
```

In particular, writing `bar u=sum_i pi_i log r_i`,

```text
|log r_i-bar u|
 <=sqrt(2eta/((1-delta)^2 lambda_P pi_i))
 <=sqrt(2eta/((1-delta)^2 lambda_P pi_min)).            (5.5)
```

### 5.4 Effective resistance

Put

```text
c_ij=pi_i p_ij=pi_j p_ji.
```

For an unordered active edge use its single conductance `c_ij`.  The electrical
energy convention is

```text
E_c(v)=sum_{{k,l} in E} c_kl(v_k-v_l)^2
      =1/2 sum_k sum_l c_kl(v_k-v_l)^2.
```

This equals `E_P(v)`.  Effective resistance is normalized by either equivalent
formula

```text
R_eff(i,j)
 =sup_{E_c(v)>0} (v_i-v_j)^2/E_c(v)
 =(e_i-e_j)^T L_c^+ (e_i-e_j),                         (5.6)
```

where `L_c` is the weighted graph Laplacian.  The Dirichlet principle and
(5.3) give

```text
|log r_i-log r_j|
 <=sqrt(R_eff(i,j) E_P(log r))
 <=sqrt(2eta R_eff(i,j))/(1-delta).                     (5.7)
```

If `R_* = max_{i,j} R_eff(i,j)`, then

```text
max_i log r_i-min_i log r_i
 <=sqrt(2eta R_*)/(1-delta),                            (5.8)
```

and every `log r_i` differs from its `pi`-mean by the same right-hand side.
This proof is independent of path multiplication; it can be much sharper on
well-connected graphs.

---

## 6. Quantitative near-rigidity for round geodesic triangulations

Assume the geometric hypotheses of Theorem P3-R, but replace exact equality by
Sections 4–5.

### 6.1 Uniform side reference

Let

```text
B_delta   =h_delta+R_G s_delta,
ell_ref   =2/r_o,
ell_ref,- =ell_ref exp(-B_delta),
ell_ref,+ =ell_ref exp(B_delta).
```

Require the explicit certified nondegeneracy condition

```text
0<ell_ref,-<=ell_e<=ell_ref,+<2.                        (6.1)
```

The middle inequalities are (4.10); the strict upper endpoint is a displayed
smallness condition.  Set

```text
sigma_ref=min(
 sqrt(ell_ref,-(2-ell_ref,-)),
 sqrt(ell_ref,+(2-ell_ref,+)))>0,
theta_ref=arccos(1-ell_ref).
```

Equations (4.11) and (4.13) give

```text
max_e |theta_e-theta_ref|
 <=Delta_theta
 :=ell_ref(exp(B_delta)-1)/sigma_ref.                   (6.2)
```

### 6.2 Explicit spherical-angle Lipschitz constant

Put

```text
t_- =theta_ref-Delta_theta,
t_+ =theta_ref+Delta_theta.
```

Require

```text
0<t_-<t_+<pi,
2t_->t_+,
3t_+<2pi.                                               (6.3)
```

These conditions keep every line segment in side-coordinate space inside the
compact nondegenerate convex spherical-triangle domain.

Define

```text
s_theta=min(sin t_-,sin t_+)>0,
c_- =cos t_+,
c_+ =cos t_-,
P_- =min{c_-^2,c_-c_+,c_+^2},
P_+ =max{c_-^2,c_-c_+,c_+^2},
N_- =c_- -P_+,
N_+ =c_+ -P_-,
C_A =max(|N_-|,|N_+|)/s_theta^2.
```

Require the certified interval condition

```text
C_A<1,                                                  (6.4)
```

and set

```text
s_A=sqrt(1-C_A^2)>0.
```

For a spherical triangle with sides `a,b,c` and opposite angle `A`,

```text
F(a,b,c)=cos A
 =(cos a-cos b cos c)/(sin b sin c).
```

Direct differentiation gives

```text
partial_a F=-sin a/(sin b sin c),
partial_b F=(cos c-cos a cos b)/(sin^2 b sin c),
partial_c F=(cos b-cos a cos c)/(sin^2 c sin b).
```

The interval definitions imply `|cos A|<=C_A`, hence `sin A>=s_A`, and

```text
|partial_a A|<=1/(s_A s_theta^2),
|partial_b A|<=2/(s_A s_theta^3),
|partial_c A|<=2/(s_A s_theta^3).
```

Therefore the explicit valid Lipschitz constant

```text
C_ang
 =1/(s_A s_theta^2)+4/(s_A s_theta^3)                  (6.5)
```

satisfies

```text
|A-A_ref|
 <=C_ang max(|a-theta_ref|,|b-theta_ref|,|c-theta_ref|)
 <=C_ang Delta_theta,                                  (6.6)
```

where

```text
A_ref=alpha_eq(theta_ref)
     =arccos(cos theta_ref/(1+cos theta_ref)).
```

### 6.3 Integer-valence separation and combinatorial type

At a vertex,

```text
1=sum_j p_ij>=deg(i) kappa,
```

so

```text
deg(i)<=d_max=floor(1/kappa).                           (6.7)
```

Every simple spherical triangulation has degree at least three.  If
`d_max=3`, every valence is already three.  If `d_max>=4`, define the exact
positive separation

```text
g_kappa=min{
 |2pi/m-2pi/n| : 3<=m<n<=d_max}.                       (6.8)
```

For a vertex of degree `m`, sum (6.6) over its incident face angles and use the
round-sphere angle sum:

```text
|2pi/m-A_ref|<=C_ang Delta_theta.                       (6.9)
```

For degrees `m,n` at two vertices,

```text
|2pi/m-2pi/n|<=2 C_ang Delta_theta.
```

Thus, if

```text
2 C_ang Delta_theta<g_kappa,                            (6.10)
```

all valences are equal.  Euler's formula then gives `q in {3,4,5}`, and the
combinatorial uniqueness proof of Section 3.4 identifies the abstract
triangulation as tetrahedral, octahedral, or icosahedral.

### 6.4 Distance to the exact Platonic side

On `(0,2pi/3)`, define

```text
alpha_eq(theta)
 =arccos(cos theta/(1+cos theta)).
```

Its derivative is

```text
alpha_eq'(theta)
 =sin theta/((1+cos theta)^2 sin(alpha_eq(theta)))>0.   (6.11)
```

Let `theta_q` be the exact side in Section 3.5.  Choose a certified compact
interval `J subset (0,2pi/3)` containing `theta_ref` and `theta_q`.  Set

```text
m_eq=inf_{theta in J} alpha_eq'(theta)>0.               (6.12)
```

An entirely explicit lower certificate is

```text
m_eq>=s_J/4,
s_J=min_{theta in J} sin theta
   =min(sin inf J,sin sup J)>0,                         (6.13)
```

because `(1+cos theta)^2<=4` and `sin(alpha_eq(theta))<=1`.

Equation (6.9), now with common degree `q`, says

```text
|alpha_eq(theta_ref)-alpha_eq(theta_q)|
 <=C_ang Delta_theta.
```

The mean-value theorem and (6.12) yield

```text
|theta_ref-theta_q|
 <=C_ang Delta_theta/m_eq,                              (6.14)
```

and hence

```text
max_e |theta_e-theta_q|
 <=Delta_theta(1+C_ang/m_eq).                           (6.15)
```

This is the required edge-length sup-norm distance to the corresponding exact
Platonic spherical framework.

### 6.5 Closed-form conservative defect threshold

The preceding conditions are directly checkable.  The following gives a
single conservative threshold, avoiding an unnamed continuity modulus.

Assume the observed reference loss satisfies

```text
0<ell_0:=ell_ref<2,
theta_0:=arccos(1-ell_0)<2pi/3.                         (6.16)
```

Set

```text
rho       = (1/2) min(ell_0,2-ell_0),
b_0       = log(1+rho/ell_0),
C_R       = 2+4R_G,
sigma_0   = min(
              sqrt((ell_0-rho)(2-ell_0+rho)),
              sqrt((ell_0+rho)(2-ell_0-rho))),
K_theta   = ell_0 exp(b_0) C_R/sigma_0,
tau       = (1/4) min(theta_0,pi-theta_0,2pi/3-theta_0).
```

On `0<=delta<=1/2`, elementary logarithmic bounds give

```text
B_delta<=C_R delta.                                    (6.17)
```

Use the fixed side box `[theta_0-tau,theta_0+tau]` in the construction
(6.4)–(6.5), and suppose its explicit `C_A<1`; call the resulting constant
`C_ang,0`.  When `d_max>=4`, use `g_kappa` from (6.8); when `d_max=3`, omit
the corresponding term.  Define

```text
delta_* = min(
  1/2,
  b_0/C_R,
  tau/K_theta,
  g_kappa/(4 C_ang,0 K_theta) )                         (6.18)
```

with the last entry omitted in the one-valence case, and set

```text
eta_*=kappa delta_*^2.                                  (6.19)
```

If `0<=eta<eta_*`, then `delta<delta_*`.  Equations (6.17)–(6.18) imply

```text
ell_0(exp(B_delta)-1)<=rho,
Delta_theta<=K_theta delta<tau,
2C_ang,0 Delta_theta<g_kappa.
```

Thus (6.1), (6.3), (6.4), and (6.10) all hold, the Platonic type is identified,
and (6.15) applies.  Every parameter in (6.18) is an explicit function of the
finite graph, `kappa`, and the reference row rate.  No hidden `O(sqrt eta)` or
uncomputed compactness constant remains.

---

## 7. Interaction with Prompt 2 covariance

For

```text
C_i=sum_j a_ij
 (Omega_j-Omega_i)(Omega_j-Omega_i)^T,
M_i=P_0(C_i+2Omega_i Omega_i^T),
P_i=I-Omega_i Omega_i^T,
```

where in dimension three `P_0(A)=A-(tr A/3)I`, the following identities hold.

### Proposition 7.1 — trace and radial component

```text
tr C_i=4,                                               (7.1)
Omega_i^T C_i Omega_i=epsilon_i=4Q_i/r_i.              (7.2)
```

#### Proof

For `d_ij=Omega_j-Omega_i`,

```text
tr(d_ij d_ij^T)=|d_ij|^2=2(1-Omega_i dot Omega_j)=2ell_ij.
```

Therefore (1.2) gives

```text
tr C_i=2 sum_j a_ij ell_ij=4.
```

Also

```text
Omega_i dot d_ij=Omega_i dot Omega_j-1=-ell_ij,
```

so

```text
Omega_i^T C_i Omega_i=sum_j a_ij ell_ij^2=epsilon_i.
```

The definition of `Q_i` gives (7.2).

### 7.2 Exact `Q_i=1` decomposition

Assume local `Q_i=1`, put

```text
ell_i=2/r_i,
0<ell_i<2,
s_i=sqrt(ell_i(2-ell_i)),
u_ij=(Omega_j-(1-ell_i)Omega_i)/s_i,
T_i=sum_j p_ij u_ij u_ij^T.
```

For active edges, `u_ij` is a unit tangent vector at `Omega_i`.  The local
coordinate equation divided by `r_i` is

```text
sum_j p_ij(Omega_j-Omega_i)=-ell_i Omega_i.
```

Since

```text
Omega_j-Omega_i=-ell_i Omega_i+s_i u_ij,
```

we obtain

```text
T_i Omega_i=0,
tr T_i=1,
sum_j p_ij u_ij=0.                                    (7.3)
```

Expanding the covariance, the mixed terms vanish by (7.3), and
`r_i ell_i=2`, `s_i^2=ell_i(2-ell_i)` give

```text
C_i
 =2(2-ell_i)T_i+2ell_i Omega_i Omega_i^T.              (7.4)
```

Because `tr(C_i+2Omega_iOmega_i^T)=6`, trace-free projection gives

```text
M_i
 =3ell_i(Omega_i Omega_i^T-I/3)
  +2(2-ell_i)(T_i-P_i/2).                              (7.5)
```

Formula (7.5) is the exact separation: `Q=1` fixes the radial coefficient but
leaves the trace-free tangential second moment free.

### 7.3 Axial covariance criterion

The cross radial-tangential block in (7.4) is zero.  Since
`2(2-ell_i)>0`, the tangent restriction is scalar exactly when

```text
T_i=P_i/2.                                              (7.6)
```

Thus

```text
C_i is axially isotropic about Omega_i
iff T_i=P_i/2.
```

If this holds at every vertex, the accepted Prompt 2 axial theorem applies and
recovers

```text
E_form=K_X,
E_sample={0}.
```

No implication from `Q=1` alone to (7.6) is valid.

### 7.4 Exact positive reversible anisotropic family

Use the six vertices `+/-e_1,+/-e_2,+/-e_3`.  For positive parameters
`g_12,g_13,g_23`, assign conductance `g_ab` to each of the four edges between
the two antipodal axis pairs `+/-e_a` and `+/-e_b`, and put

```text
w_(+/-e_1)=g_12+g_13,
w_(+/-e_2)=g_12+g_23,
w_(+/-e_3)=g_13+g_23.
```

At `+/-e_a`, the two neighbors on each other axis cancel in vector sum.  The
total outgoing rate is

```text
r_i=2,
```

and hence

```text
L Omega=-2Omega.
```

Every edge joins orthogonal axes, so `ell_e=1`, `epsilon_i=2`, and
`Q_i=1`.

At `+e_1` (and identically at `-e_1`),

```text
T_1
 =g_12/(g_12+g_13) e_2e_2^T
  +g_13/(g_12+g_13) e_3e_3^T,
C_1=2T_1+2e_1e_1^T,
M_1=3(e_1e_1^T-I/3)+2(T_1-P_1/2).                      (7.7)
```

The analogous formulas hold cyclically.  Axial covariance at axis 1 is
`g_12=g_13`; at axis 2 it is `g_12=g_23`; at axis 3 it is
`g_13=g_23`.  Therefore axial covariance at all vertices holds exactly when

```text
g_12=g_13=g_23.                                        (7.8)
```

This is a connected positive reversible minor-arc geodesic octahedral
triangulation, generally with unequal masses.  It proves that `Q=1` alone does
not force axial covariance.

#### Genuine sampled degree-two space

A trace-free quadratic form sampled at `+/-e_a` depends only on its diagonal
entries `d_a`, with `d_1+d_2+d_3=0`; off-diagonal forms are sampling aliases.
On these antipodally even samples, the six-state generator reduces to

```text
L=2(P-I),
```

where `P` is a row-stochastic transition matrix on the three axis classes.
A spherical degree-two sampled mode would satisfy `Lf=-6f`, hence

```text
Pf=-2f.
```

But a row-stochastic matrix is a contraction in the infinity norm:
`||Pf||_infinity<=||f||_infinity`.  The equation above is therefore possible
only for `f=0`.  Consequently, for every positive `g_12,g_13,g_23`,

```text
E_sample={0}.                                           (7.9)
```

This conclusion uses the sampling map and does not identify form-space
dimension with sampled-space dimension.

### 7.5 Near-equality radial control and tangential non-control

From (7.2) and `1<=Q_i<=1+eta`,

```text
0<=Omega_i^T C_i Omega_i-4/r_i<=4eta/r_i.              (7.10)
```

There is no corresponding bound on `T_i-P_i/2`.  In the exact weighted
octahedral family, take `g_12=t`, `g_13=1` at axis 1.  Then `eta=0` while

```text
||T_1-P_1/2||_op=|t-1|/(2(t+1)) -> 1/2
```

as `t->infinity`.  A separate tangent-isotropy hypothesis is therefore
necessary for any tangential covariance stability theorem.

---

## 8. Exact falsification boundary

The deterministic audit keeps the following statements permanently rejected:

```text
only K in {4,6,12} can have Q=1;
every finite spherical graph has Q>1;
every equal-loss spherical graph is a triangulated Platonic graph;
Q=1 forces axial covariance;
form-space dimension equals sampled-space dimension.
```

The exact counterexamples include:

* cube and dodecahedron shortest-edge `Q=1` graphs (not triangulations);
* a two-state antipodal equality graph (`ell=2`, `r=1`);
* disconnected components with different exact rates;
* inactive diagonals added to a cube embedding;
* major-arc and cone-metric variants;
* directed/nonreversible row variants;
* signed four-cardinal and signed-pentagon Prompt 2 examples; and
* the positive reversible weighted octahedral covariance family.

`triangulation_counterexample_audit.py` independently enumerates every simple
sphere triangulation through 12 vertices with source-pinned `plantri`, records
one canonical graph record per map, and verifies that the only equivelar
round-angle candidates are the three classified graphs.  This finite census is
a hostile falsification test, not the proof of Theorem P3-R.

---

## 9. Prior-art and publication boundary

The components used here have different status.

### Standard inputs

* weighted variance equality and equality in a finite nonnegative sum;
* spherical law of cosines and spherical excess;
* Euler identities for a simple sphere triangulation;
* links and collars in a triangulated 2-manifold;
* the Poincare variational definition for a finite reversible chain;
* the Dirichlet/effective-resistance variational principle.

### External tools and adjacent literature

* `plantri` (Brinkmann–McKay) is used only for finite hostile enumeration;
* standard work on equivelar and semi-equivelar maps provides adjacent
  classification context, but Section 3.4 supplies the needed special
  uniqueness proof directly;
* Cauchy/Alexandrov and modern framework-stability literature are adjacent
  rigidity theory, but geometric uniqueness here is proved by direct spherical
  face propagation;
* reversible Markov-chain texts supply the standard Poincare and electrical
  network formalism, while the explicit defect-to-energy transfer (5.2)–(5.3)
  is the new specialization.

### New combined result

The contribution is not the existing abstract equality-propagation lemma.  It
is the combined package consisting of:

1. the exact spherical `Q=1` transfer with all degeneracies audited;
2. the restricted round geodesic-triangulation classification;
3. explicit graph-global, spectral-gap, and resistance near-rigidity bounds;
4. an explicit data-dependent and closed-form conservative triangulation
   stability threshold with edge-length distance (6.15); and
5. the exact covariance decomposition and positive reversible anisotropy
   separation.

No product-grid lower bound, extremal optimization, or final paper synthesis
belonging to Prompt 4 is started here.

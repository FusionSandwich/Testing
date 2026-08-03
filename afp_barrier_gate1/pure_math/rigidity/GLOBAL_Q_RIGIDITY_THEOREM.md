# Exact global `Q=1` rigidity and quantitative near-rigidity

## Status and scope

This document gives the ordinary mathematical proof of the Prompt 3 theorem
package.  Its scope is the finite positive reversible spherical generator
specified below.  The classification theorem is deliberately restricted to an
actual nondegenerate minor-arc geodesic triangulation of the round sphere.
Cube and dodecahedron shortest-edge generators remain exact `Q=1`
counterexamples to every unrestricted Platonic claim.

Controlled labels in this document are unambiguous: the stated finite
identities, corrected classification, quantitative bounds, closed threshold,
and non-antipodal covariance theorem are **PROVED**; named standard inputs are
**EXTERNAL**; finite scripts and catalog values are **COMPUTATIONAL**; and the
displayed false unrestricted formulations are **REJECTED**.  No mandatory
result is left **CONJECTURE**.

The finite scripts in this directory are falsification and regression evidence;
they are not substitutes for the all-orders proofs in this document.  Selected
finite algebra is mirrored in Lean.  Standard spherical trigonometry, Euler's
formula for a triangulated sphere, the elementary Dirichlet principle, and the
Poincare variational definition are identified explicitly when used.

---

## 1. Finite spherical generator and normalization

Let `V` be nonempty and finite, let `Omega_i in S^2 subset R^3`, and let `w_i>0`.  Let
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

The one-skeleton of a triangulation of the connected topological sphere is
connected.  Hypotheses 2 and 9 identify it exactly with the active graph, so
all premises of Theorem 2.2 hold.  Therefore every edge has the same loss and
hence the same minor length
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
other vertices.  Its graph is `K4`.  It has exactly four 3-cycles, while the
Euler count gives four faces, so those cycles are precisely the tetrahedral
faces.

#### `q=4`, `V=6`

The complement of a simple 4-regular graph on six vertices is 1-regular, hence
a perfect matching.  All perfect matchings on six vertices are isomorphic.
The original graph is therefore `K6` with three disjoint edges removed, the
octahedral graph.  A triangular clique chooses one endpoint from each of the
three missing pairs, so it has exactly `2^3=8` such cycles.  The Euler count gives
eight faces, so the given triangular embedding has exactly the octahedral
faces.

#### `q=5`, `V=12`

The complete proof is recorded in `ICOSAHEDRAL_GRAPH_LEMMA.md`; its key steps
are included here to expose the topology.  First, a nonfacial triangular cycle
would cut the sphere into two triangular-boundary disks.  The disk-curvature
identity

```text
sum_interior (6-deg_D x)+sum_boundary (4-deg_D x)=6
```

forces a side with `n` interior vertices to have `2n` interior--interior
edges.  A nonfacial side has `n>0`; simplicity excludes `n<=2`, and the planar
bound `E_int<=3n-6` excludes `3<=n<=5`.  Each side would therefore contain at
least six interior vertices, impossible when the whole graph has twelve.
Thus every triangular cycle is a face.

Choose a vertex `v` and write its link as the chordless cycle
`a_0,...,a_4`.  Let `b_i` be the third vertex across the edge
`a_i a_{i+1}` from `v`.  Each `b_i` lies outside the closed star of `v`.
Adjacent `b_i` cannot coincide because the corresponding `a_i` would then
have only four link vertices.  A nonadjacent repetition would create a
triangular cycle; since every such cycle is a face, uniqueness of the face
across the intervening link edge forces an adjacent repetition.  Hence the
five `b_i` are distinct.

The cyclic link of `a_i` now forces the edge `b_{i-1}b_i`, so the `b_i` form a
second chordless five-cycle.  Exactly one vertex `z` remains.  Every `a_i` has
all five degree slots filled, while `z` has degree five, so its neighbours are
exactly the five `b_i`.  Those adjacencies fill the fifth slot at every `b_i`.
The resulting two-pole, two-pentagon adjacency and all twenty triangular faces
are forced; this is the icosahedral triangulation.  No enumeration or unnamed
"Platonic solids" classification is used.

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

This is the ordinary, non-absolute Poincare gap of `I-P`, not
`1-max_{k>=2}|lambda_k(P)|`.  For example, the two-state deterministic flip
has Poincare gap `2` under this convention even though its absolute mixing gap
is zero.

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

where `L_c` is the weighted graph Laplacian.

Thus the factor convention is

```text
E_P(v)=1/2 sum_{i,j} c_ij(v_i-v_j)^2
      =sum_{{i,j} in E} c_ij(v_i-v_j)^2;
```

each undirected edge appears exactly once in the second expression.
The Dirichlet principle and (5.3) give

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
 <=Delta_raw
 :=ell_ref(exp(B_delta)-1)/sigma_ref.                   (6.2)
```

### 6.2 Explicit spherical-angle Lipschitz constant

Choose a displayed side box `[t_-,t_+]` satisfying

```text
0<t_-<=theta_ref-Delta_raw,
theta_ref+Delta_raw<=t_+<pi,
2t_->t_+,
3t_+<2pi.                                               (6.3)
```

The last two strict inequalities imply all three strict triangle inequalities
and perimeter less than `2pi` for every side triple in the box.  They therefore
keep the entire line segment in side-coordinate space inside the
nondegenerate convex spherical-triangle domain, including when
`Delta_raw=0`.

Define

```text
s_theta=min(sin t_-,sin t_+)>0,
g_box=2t_--t_+>0,
m_T=sin(g_box/2)>0,
m_S=min(sin(3t_-/2),sin(3t_+/2))>0,
s_A0=2 sqrt(m_S m_T^3)>0.                               (6.4)
```

These are closed elementary expressions.  To certify the last bound, let
`S=(a+b+c)/2`.  The spherical Gram determinant factors as

```text
D=sin^2(b)sin^2(c)-(cos(a)-cos(b)cos(c))^2
 =4 sin(S)sin(S-a)sin(S-b)sin(S-c).
```

For sides in the box,

```text
S in [3t_-/2,3t_+/2] subset (0,pi),
S-a,S-b,S-c in [g_box/2,(2t_+-t_-)/2] subset (0,pi/2).
```

Consequently `D>=4m_S m_T^3`.  Since

```text
sin(A)=sqrt(D)/(sin(b)sin(c))
```

and the denominator is at most one, every angle in the box satisfies
`sin(A)>=s_A0`.  This proves positivity directly; it does not assume an
endpoint enclosure for `cos(A)`.

For the angle opposite `a`,

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

```text
|partial_a A|<=1/(s_A0 s_theta^2),
|partial_b A|<=2/(s_A0 s_theta^3),
|partial_c A|<=2/(s_A0 s_theta^3).
```

Therefore the explicit valid Lipschitz constant

```text
C_ang
 =1/(s_A0 s_theta^2)+4/(s_A0 s_theta^3)                (6.5)
```

satisfies

```text
|A-A_ref|
 <=C_ang max(|a-theta_ref|,|b-theta_ref|,|c-theta_ref|)
 <=C_ang Delta_raw,                                    (6.6)
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

This finite minimum is itself closed:

```text
g_kappa=2pi/(d_max(d_max-1)).
```

For a fixed lower denominator the smallest gap is obtained at consecutive
integers, and `2pi/(m(m+1))` decreases with `m`.

For a vertex of degree `m`, sum (6.6) over its incident face angles and use the
round-sphere angle sum:

```text
|2pi/m-A_ref|<=C_ang Delta_raw.                         (6.9)
```

For degrees `m,n` at two vertices,

```text
|2pi/m-2pi/n|<=2 C_ang Delta_raw.
```

Thus, if

```text
2 C_ang Delta_raw<g_kappa,                              (6.10)
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

Let `theta_q` be the exact side in Section 3.5 and take the explicit interval

```text
J_- =min(theta_ref,theta_q),
J_+ =max(theta_ref,theta_q),
J   =[J_-,J_+] subset (0,2pi/3),
m_eq=alpha_eq'(J_-)>0.                                  (6.12)
```

This is the exact minimum on `J`.  Indeed, with `c=cos theta`,

```text
(alpha_eq'(theta))^2=(1-c)/((1+c)(1+2c)),
```

whose logarithmic derivative with respect to `c` is

```text
-1/(1-c)-1/(1+c)-2/(1+2c)<0.
```

As `c` decreases with `theta`, `alpha_eq'` is strictly increasing.  The
explicit endpoint value also has the convenient certificate

```text
m_eq>=s_J/4,
s_J=min(sin J_-,sin J_+)>0,                             (6.13)
```

because `(1+cos theta)^2<=4` and `sin(alpha_eq(theta))<=1`.

Equation (6.9), now with common degree `q`, says

```text
|alpha_eq(theta_ref)-alpha_eq(theta_q)|
 <=C_ang Delta_raw.
```

The mean-value theorem and (6.12) yield

```text
|theta_ref-theta_q|
 <=C_ang Delta_raw/m_eq,                                (6.14)
```

and hence

```text
max_e |theta_e-theta_q|
 <=Delta_raw(1+C_ang/m_eq).                             (6.15)
```

This is the required edge-length sup-norm distance to the corresponding exact
Platonic spherical framework.

### 6.5 Closed-form conservative defect threshold

The following packages every domain condition into a single conservative
threshold, with no unnamed continuity modulus.

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

Thus `0<rho<min(ell_0,2-ell_0)` and `tau>0`.  For the fixed side box put

```text
t_lo      =theta_0-tau,
t_hi      =theta_0+tau,
g_0       =2t_lo-t_hi=theta_0-3tau,
s_theta,0 =min(sin t_lo,sin t_hi),
m_T,0     =sin(g_0/2),
m_S,0     =min(sin(3t_lo/2),sin(3t_hi/2)),
s_A,0     =2 sqrt(m_S,0 m_T,0^3),
C_ang,0   =1/(s_A,0 s_theta,0^2)+4/(s_A,0 s_theta,0^3).
```

All displayed denominators are positive.  Indeed the definition of `tau`
gives

```text
0<t_lo<t_hi<pi,
2t_lo>t_hi,
3t_hi<2pi.
```

Section 6.2 therefore proves `sin A>=s_A,0` throughout this fixed box and
certifies `C_ang,0` by a closed Gram/Heron factorization.  In particular, this
certificate remains valid at `eta=0` and at the exact icosahedral reference;
there is no added `C_A<1` assumption.

On `0<=delta<=1/2`, elementary logarithmic bounds give

```text
B_delta<=C_R delta.                                    (6.17)
```

For completeness, `-log(1-delta)<=2delta` and
`log(1+delta)<=delta`, so
`s_delta<=3delta<=4delta`; substitution in
`B_delta=h_delta+R_G s_delta` proves (6.17).

Put `d_max=floor(1/kappa)`.  Since a simple sphere triangulation has degree at
least three and `1=sum_j p_ij>=deg(i)kappa`, the present hypotheses imply
`d_max>=3`.  If `d_max>=4`, use `g_kappa` from (6.8).  If `d_max=3`, every
valence is already three and the valence-separation term below is omitted.

Define

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

Every entry in (6.18) is positive, so `delta_*>0` and `eta_*>0`.  If
`0<=eta<eta_*`, then `delta=sqrt(eta/kappa)<delta_*`.  Equations
(6.17)–(6.18) give `B_delta<b_0`.  Hence

```text
ell_0 exp(B_delta)<ell_0+rho,
ell_0 exp(-B_delta)>ell_0^2/(ell_0+rho)>ell_0-rho.
```

The last strict inequality follows because its difference is
`rho^2/(ell_0+rho)`.  Thus every active loss lies in the certified interval
`[ell_0-rho,ell_0+rho] subset (0,2)`, whose arc denominator is at least
`sigma_0`.  Since `0<=B_delta<b_0`, the mean-value estimate

```text
exp(B_delta)-1<=exp(b_0)B_delta
```

and (6.17) give the closed side bound

```text
max_e |theta_e-theta_0|
 <=K_theta delta=:Delta_theta<tau.                     (6.20)
```

Every face side therefore remains in the fixed nondegenerate minor-arc box,
and Section 6.2 yields

```text
|A_face-alpha_eq(theta_0)|<=C_ang,0 Delta_theta.       (6.21)
```

If `d_max>=4`, (6.18) gives

```text
2C_ang,0 Delta_theta<g_kappa/2<g_kappa,
```

so (6.9) forces all valences to agree; for `d_max=3` this was already true.
Euler and Section 3.4 identify the abstract triangulation as tetrahedral,
octahedral, or icosahedral.  For its common valence `q`, take the explicit
interval `J` and `m_eq` from (6.12).  Equations (6.14)–(6.15), with the closed
bound (6.20), prove

```text
max_e |theta_e-theta_q|
 <=Delta_theta(1+C_ang,0/m_eq).                        (6.22)
```

Equations (6.20)–(6.22) are respectively the certified side-domain, face-angle,
and mandatory edge-length sup-norm conclusions.  Every parameter is an
explicit function of the finite graph, `kappa`, and the observed reference row
rate.  No hidden `O(sqrt eta)` or uncomputed compactness constant remains.

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

### Antipodal truth-safeguard boundary

**REJECTED literal formulation:** defining normalized tangent vectors under
global `Q=1` without assuming `ell<2`.  The connected two-state model at
`Omega_2=-Omega_1`, with rate one in both directions, satisfies

```text
L Omega=-2Omega,
r=1,
ell=2,
Q=1.
```

But `sqrt(ell(2-ell))=0`, so the displayed tangent quotient is undefined.
The valid theorem below assumes `0<ell<2`.  The exact antipodal equality model
remains a separate PROVED case; it is not suppressed or assigned an arbitrary
tangent direction.  Directly, it has

```text
C_i=4 Omega_i Omega_i^T,
M_i=6(Omega_i Omega_i^T-I/3).
```

Totalized formal division would return `0/0=0`, but then the resulting
putative `T_i` has trace zero rather than one; it is not a valid substitute for
the non-antipodal tangent construction.

### 7.2 Exact `Q_i=1` decomposition

Assume local `Q_i=1`, put `ell_i=2/r_i`, and assume `ell_i<2`.  Since
`r_i>0`, Theorem 2.1 already gives `ell_i>0`.  Define

```text
0<ell_i<2,
s_i=sqrt(ell_i(2-ell_i)),
u_ij=(Omega_j-(1-ell_i)Omega_i)/s_i,
T_i=sum_j p_ij u_ij u_ij^T.
```

Under connected global equality, Theorem 2.2 makes every `ell_i` the same
common `ell`; the local notation also records the stronger vertexwise
decomposition before connected propagation is invoked.

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

This is also exactly the Prompt 2 one-shell full-tangent-isotropy condition.
In dimension three that condition reads

```text
sum_j a_ij u_ij u_ij^T=(r_i/2)P_i.
```

Because `a_ij=r_i p_ij` on the active row and `r_i>0`, division by `r_i`
turns it into `T_i=P_i/2`, and the implication reverses by multiplication.
Thus the equivalence is not merely a comparison of covariance eigenvalues; it
is the literal Prompt 2 signed one-shell moment specialized to the positive
global-equality row.

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
form-space dimension equals sampled-space dimension;
near-rigidity is diameter-free under only a local weight floor;
finite enumeration proves the classification.
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
one deterministic graph6 representative per emitted map, and verifies that
the only equivelar round-angle candidates are the three classified graphs.
This finite census is a hostile falsification test, not the proof of
Theorem P3-R.

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
   stability threshold with its mandatory edge-length distance (6.22); and
5. the exact covariance decomposition and positive reversible anisotropy
   separation.

No product-grid lower bound, extremal optimization, or final paper synthesis
belonging to Prompt 4 is started here.

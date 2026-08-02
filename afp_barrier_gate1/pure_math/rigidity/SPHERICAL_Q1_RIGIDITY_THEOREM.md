# Global spherical `Q=1` rigidity, regular triangulations, and quantitative stability

## 0. Scope and conventions

This is the ordinary mathematical proof for Prompt 3. It begins from the
accepted Prompt 1 local/global feasibility package and the accepted Prompt 2
covariance/product package.

Let `I` be finite, let

\[
\Omega_i\in S^2\subset\mathbb R^3,
\]

and let

\[
(Lf)(i)=\sum_{j\ne i}a_{ij}(f(j)-f(i)),
\qquad a_{ij}\ge0.
\]

For each source vertex `i`, define

\[
g_i(j)=\Omega_i\cdot\Omega_j,
\qquad
\ell_{ij}=1-g_i(j),
\]

\[
r_i=\sum_{j\ne i}a_{ij},
\qquad
D_i=\sum_{j\ne i}a_{ij}\ell_{ij}^2.
\]

An edge is active when `i != j` and `a_ij>0`. When positive masses and
shared conductances are present,

\[
a_{ij}=\frac{\gamma_{ij}}{w_i},
\qquad w_i>0,
\qquad \gamma_{ij}=\gamma_{ji}\ge0,
\]

activity is symmetric automatically.

The coordinate eigenmap hypothesis on `S^2` is

\[
\sum_{j\ne i}a_{ij}(\Omega_j-\Omega_i)=-2\Omega_i. \tag{0.1}
\]

Taking the dot product with `Omega_i` gives

\[
\sum_{j\ne i}a_{ij}\ell_{ij}=2. \tag{0.2}
\]

Define

\[
Q_i=\frac{r_iD_i}{4}. \tag{0.3}
\]

The use of `Q=1` here always means (0.3). It is unrelated to the
quadratic-sampling form space from Prompt 2.

---

## 1. Complete spherical `Q=1` specialization

### Theorem 1.1 — positivity and sharp local equality

Under (0.1), every row has `r_i>0` and

\[
\boxed{Q_i\ge1.} \tag{1.1}
\]

Moreover,

\[
\boxed{
Q_i=1
\iff
\ell_{ij}=\frac2{r_i}
\quad\text{for every active }i\to j.
} \tag{1.2}
\]

#### Proof

Equation (0.2) and nonnegativity show that the row cannot have zero total
rate. Weighted Cauchy--Schwarz gives

\[
\left(\sum_ja_{ij}\ell_{ij}\right)^2
\le
\left(\sum_ja_{ij}\right)
\left(\sum_ja_{ij}\ell_{ij}^2\right).
\]

Using (0.2) gives `4 <= r_i D_i`.

Put `m_i=2/r_i`. The exact variance identity already proved in
`LossVariance.lean` is

\[
r_iD_i-4
=
r_i\sum_{j\ne i}a_{ij}(\ell_{ij}-m_i)^2. \tag{1.3}
\]

Every summand is nonnegative. It vanishes exactly when every active edge has
loss `m_i`. The Lean theorem
`rate_mul_peakDefect_eq_eigenvalue_sq_iff_active_losses_eq_mean` supplies the
same argument with all zero-rate and zero-weight cases explicit. `\square`

### Corollary 1.2 — zero-loss and antipodal degeneracies

In an exact `Q_i=1` row:

1. no active edge can have `Omega_i=Omega_j`;
2. every active loss is strictly positive;
3. if one active edge is antipodal, then `r_i=1`;
4. if the active relation is connected and symmetric and one active edge is
   antipodal, then every active edge is antipodal.

For an injective embedding, the last alternative has at most two vertices and
cannot be a nondegenerate triangulation.

### Theorem 1.3 — global equal-rate/equal-loss propagation

Assume:

1. (0.1) holds at every vertex;
2. all off-diagonal rates are nonnegative;
3. `Q_i=1` at every vertex;
4. activity is symmetric;
5. `ell_ij=ell_ji`; and
6. the active graph is connected.

Then there is one `r_*>0` such that

\[
\boxed{r_i=r_*\quad(i\in I)} \tag{1.4}
\]

and one loss `ell_*=2/r_*` such that

\[
\boxed{\ell_{ij}=\ell_*\quad\text{on every active edge}.} \tag{1.5}
\]

Thus every active chord length is `sqrt(2 ell_*)`; if active endpoints are not
antipodal, every minor geodesic edge length is equal as well.

#### Proof

Theorem 1.1 gives `ell_ij=2/r_i` on every active directed edge. On a symmetric
active edge,

\[
2/r_i=\ell_{ij}=\ell_{ji}=2/r_j.
\]

Positive row rates imply `r_i=r_j`, and connectivity propagates the identity.
`connected_active_loss_rigidity` formalizes the abstract step;
`connected_sphericalQOne_rigidity` verifies its spherical premises. `\square`

### Corollary 1.4 — reversible shared conductances

Theorem 1.3 applies whenever

\[
a_{ij}=\gamma_{ij}/w_i,
\qquad w_i>0,
\qquad \gamma_{ij}=\gamma_{ji}\ge0,
\]

and the positive-conductance graph is connected. Detailed balance is used only
to obtain symmetric activity; equality of directed edge rates is not assumed.

---

## 2. Restricted geodesic-triangulation classification

The unrestricted statement “`Q=1` implies tetrahedron, octahedron, or
icosahedron” is false. The cube and dodecahedron satisfy `Q=1` on their
shortest-edge graphs. The restriction below is therefore part of the theorem,
not a technical afterthought.

### Definition 2.1 — strict convex geodesic triangulation

A finite embedded graph `(I,E,Omega)` is a strict convex geodesic
triangulation of `S^2` when:

1. `Omega:I->S^2` is injective;
2. `E` is finite, simple, and connected;
3. every edge is the unique minor great-circle arc between its endpoints;
4. arcs meet only at common endpoints;
5. complementary face closures are nondegenerate spherical triangles;
6. the origin lies in the interior of `conv{Omega_i}`; and
7. the Euclidean convex hull is a strictly convex simplicial polyhedron whose
   boundary faces are exactly the chord triangles corresponding to the
   spherical faces.

Condition 7 is used only for the final Cauchy-rigidity step. Conditions 3--5
supply the angle-sum and triangulation identities.

### Theorem 2.2 — restricted `Q=1` classification

Assume:

1. the active graph is exactly the one-skeleton of a strict convex geodesic
   triangulation;
2. every triangulation edge is active and there are no active nonedges;
3. off-diagonal rates are nonnegative and activity is symmetric;
4. (0.1) holds at every vertex; and
5. `Q_i=1` at every vertex.

Then, up to an orthogonal transformation of `R^3`, the embedding is exactly
one of

\[
\boxed{
\text{regular tetrahedron},\quad
\text{regular octahedron},\quad
\text{regular icosahedron}.
} \tag{2.1}
\]

The exact data are:

| degree `q` | `(V,E,F)` | active dot `c` | active loss `1-c` | common row rate `r_*` |
|---:|---:|---:|---:|---:|
| 3 | `(4,6,4)` | `-1/3` | `4/3` | `3/2` |
| 4 | `(6,12,8)` | `0` | `1` | `2` |
| 5 | `(12,30,20)` | `1/sqrt(5)` | `1-1/sqrt(5)` | `(5+sqrt(5))/2` |

The theorem fixes the geometry and total row rate. It does not assert that all
individual edge rates are equal; tangent balance can have nonunique positive
dependences.

#### Proof

By Theorem 1.3 every active edge has one common loss, hence one common dot
product

\[
c=\Omega_i\cdot\Omega_j=1-\ell_*. \tag{2.2}
\]

Every spherical face is therefore equilateral. For one face with vertices
`x,y,z`, the Gram matrix is

\[
G=\begin{pmatrix}1&c&c\\c&1&c\\c&c&1\end{pmatrix}.
\]

Nondegeneracy gives

\[
\det G=(1-c)^2(1+2c)>0. \tag{2.3}
\]

Distinct endpoints give `c<1`, so

\[
-\frac12<c<1. \tag{2.4}
\]

At `x`, unit tangent directions toward `y,z` are proportional to `y-cx` and
`z-cx`. If `alpha` is the face angle,

\[
\cos\alpha
=\frac{(y-cx)\cdot(z-cx)}{1-c^2}
=\frac{c-c^2}{1-c^2}
=\frac{c}{1+c}. \tag{2.5}
\]

All face angles equal `alpha`. Equation (2.4) gives

\[
\frac\pi3<\alpha<\pi. \tag{2.6}
\]

If `q_i` faces meet at vertex `i`, the geodesic triangulation fills a smooth
neighborhood and

\[
q_i\alpha=2\pi. \tag{2.7}
\]

Thus every degree equals one integer `q`, and (2.6)--(2.7) imply

\[
q\in\{3,4,5\}. \tag{2.8}
\]

Let `V,E,F` count vertices, edges, and faces. Then

\[
qV=2E,
\qquad 3F=2E,
\qquad V-E+F=2. \tag{2.9}
\]

Elimination yields

\[
(6-q)V=12, \tag{2.10}
\]

so

\[
(q,V,E,F)
=(3,4,6,4),(4,6,12,8),(5,12,30,20). \tag{2.11}
\]

The finite combinatorial lemma for regular simple sphere triangulations now
identifies the graphs:

- the degree-three case is `K_4`;
- the degree-four case is `K_6` minus a perfect matching, the octahedral graph;
- the unique 5-regular maximal planar graph on twelve vertices is the
  icosahedral graph.

The final statement is the standard icosahedral graph lemma. It may be proved
by cyclic link expansion; the independent exact generation framework of
Brinkmann--McKay also lists one minimum-degree-five triangulation at twelve
vertices. Simplicity, planarity, triangular faces, degree five, and twelve
vertices have all been verified before invoking it.

Since `alpha=2pi/q`, (2.5) gives

\[
c=\frac{\cos(2\pi/q)}{1-\cos(2\pi/q)}. \tag{2.12}
\]

Substitution of `q=3,4,5` gives the table. The first moment and common loss
give

\[
r_*\ell_*=2,
\qquad r_*=\frac2{1-c}. \tag{2.13}
\]

Every Euclidean chord face is an equilateral triangle of side
`sqrt(2(1-c))`. The embedded convex polyhedron and the corresponding regular
Platonic solid therefore have congruent corresponding faces. Cauchy's rigidity
theorem makes them congruent. Both vertex sets lie on the unit sphere and have
four affinely independent points, so the circumcenter is unique and the
congruence fixes the origin. It is orthogonal. `\square`

### Why every restriction is present

- Without triangulation, cube and dodecahedron survive.
- Without convexity, Cauchy rigidity is unavailable.
- Without support symmetry, row-rate propagation fails.
- Without positivity, the weighted-square equality argument fails.
- With inactive triangulation edges, active metric and face structure diverge.
- Antipodal edges do not determine unique minor geodesics.

Regular spherical matchstick classifications contain further
nontriangulated equal-edge examples, so regularity alone is not a substitute
for Definition 2.1.

---

## 3. Exact normalized near-rigidity identity

Use a generic positive eigenvalue normalization. Let symmetric nonnegative
losses satisfy

\[
\sum_j a_{ij}\ell_{ij}=\lambda,
\qquad \lambda>0. \tag{3.1}
\]

Put

\[
r_i=\sum_ja_{ij}>0,
\quad m_i=\frac\lambda{r_i},
\quad p_{ij}=\frac{a_{ij}}{r_i}, \tag{3.2}
\]

\[
D_i=\sum_ja_{ij}\ell_{ij}^2,
\qquad Q_i=\frac{r_iD_i}{\lambda^2}. \tag{3.3}
\]

### Theorem 3.1 — normalized variance identity

\[
\boxed{
Q_i-1
=\sum_jp_{ij}
\left(\frac{\ell_{ij}}{m_i}-1\right)^2.
} \tag{3.4}
\]

#### Proof

Expand the right side and use `sum p=1` and `sum p ell=m_i`:

\[
\frac1{m_i^2}\sum_jp_{ij}\ell_{ij}^2-1
=\frac{D_i/r_i}{\lambda^2/r_i^2}-1
=\frac{r_iD_i}{\lambda^2}-1.
\]

Equivalently,

\[
r_iD_i-\lambda^2
=r_i\sum_ja_{ij}(\ell_{ij}-m_i)^2. \tag{3.5}
\]

`\square`

---

## 4. Multiplicative global near-rigidity

### Theorem 4.1 — explicit path and diameter bounds

Assume:

1. the active relation is symmetric and connected;
2. `Q_i<=1+epsilon` at every vertex;
3. every active normalized weight satisfies `p_ij>=p_*>0`; and
4. define

   \[
   \delta=\sqrt{\epsilon/p_*}<1,
   \qquad \kappa=\frac{1+\delta}{1-\delta}. \tag{4.1}
   \]

Then every active edge satisfies

\[
\boxed{\left|\frac{\ell_{ij}}{m_i}-1\right|\le\delta.} \tag{4.2}
\]

For a shared edge,

\[
\boxed{
\kappa^{-1}\le\frac{m_j}{m_i}\le\kappa,
\qquad
\kappa^{-1}\le\frac{r_j}{r_i}\le\kappa.
} \tag{4.3}
\]

Along a path of length at most `n`,

\[
\boxed{
\kappa^{-n}\le\frac{m_v}{m_u}\le\kappa^n,
\qquad
\kappa^{-n}\le\frac{r_v}{r_u}\le\kappa^n.
} \tag{4.4}
\]

If active diameter is at most `D` and `o` is a root, then

\[
\boxed{
(1-\delta)\kappa^{-D}m_o
\le\ell_{ij}\le
(1+\delta)\kappa^Dm_o.
} \tag{4.5}
\]

For any two active edges,

\[
\boxed{
\kappa^{-(2D+1)}
\le\frac{\ell_e}{\ell_{e'}}
\le\kappa^{2D+1}.
} \tag{4.6}
\]

#### Proof

By (3.4), each nonnegative summand is at most `epsilon`. The lower bound
`p_ij>=p_*` gives (4.2), hence

\[
(1-\delta)m_i\le\ell_{ij}\le(1+\delta)m_i. \tag{4.7}
\]

Apply (4.7) from both endpoints of a symmetric edge. Division by
`1-delta>0` gives (4.3). Multiply along paths for (4.4), combine with one
incident-edge estimate for (4.5), and divide extrema for (4.6). `\square`

### Corollary 4.2 — angular concentration

For `S^2`, `lambda=2`. Suppose additionally

\[
0<\ell_-\le\ell_e\le\ell_+<2. \tag{4.8}
\]

Set

\[
s_*=\min\{\sqrt{\ell_-(2-\ell_-)},
\sqrt{\ell_+(2-\ell_+)}\}>0. \tag{4.9}
\]

For `theta_e=arccos(1-ell_e)`, the mean-value theorem gives

\[
|\theta_e-\theta_{e'}|
\le\frac{|\ell_e-\ell_{e'}|}{s_*}. \tag{4.10}
\]

---

## 5. Additive global near-rigidity

### Theorem 5.1 — additive diameter estimate

Assume:

1. the active graph is symmetric, connected, and has diameter at most `D`;
2. `r_iD_i-lambda^2<=eta` at every vertex;
3. `r_i>=r_min>0`;
4. every active rate has `a_ij>=a_min>0`; and
5. define

   \[
   \Delta=\sqrt{\frac\eta{r_{\min}a_{\min}}}. \tag{5.1}
   \]

Then

\[
\boxed{|\ell_{ij}-m_i|\le\Delta} \tag{5.2}
\]

on every active edge,

\[
\boxed{|m_i-m_j|\le2\Delta} \tag{5.3}
\]

on a shared edge, and relative to a root `o`,

\[
\boxed{|m_i-m_o|\le2D\Delta.} \tag{5.4}
\]

Every active edge satisfies

\[
\boxed{|\ell_{ij}-m_o|\le(2D+1)\Delta,} \tag{5.5}
\]

and any two active losses satisfy

\[
\boxed{|\ell_e-\ell_{e'}|\le2(2D+1)\Delta.} \tag{5.6}
\]

If also `r_i<=r_max`, then

\[
\boxed{|r_i-r_o|\le
\frac{2D r_{\max}^2}{\lambda}\Delta.} \tag{5.7}
\]

#### Proof

Equation (3.5) gives

\[
r_i\sum_ja_{ij}(\ell_{ij}-m_i)^2\le\eta.
\]

One active term and the two floors give (5.2). The triangle inequality on a
shared edge gives (5.3). Sum along a shortest path for (5.4), add one incident
edge for (5.5), and apply (5.5) twice for (5.6). Finally,

\[
|r_i-r_o|=\frac{r_ir_o}{\lambda}|m_i-m_o|,
\]

which gives (5.7). `\square`

### Corollary 5.2 — shared-conductance parameters

If

\[
a_{ij}=\frac{\gamma_{ij}}{w_i},
\quad 0<w_i\le w_{\max},
\quad \gamma_{ij}\ge\gamma_{\min}>0
\]

on active edges and `r_i<=r_max`, then

\[
a_{ij}\ge\frac{\gamma_{\min}}{w_{\max}},
\qquad
p_{ij}\ge\frac{\gamma_{\min}}{w_{\max}r_{\max}}. \tag{5.8}
\]

---

## 6. Adversarial necessity

### 6.1 The normalized active-weight floor is necessary

For `0<t<=1/2`, take

\[
p_1=t^4,\qquad p_2=1-t^4,
\]

and normalized losses

\[
x_1=1+\frac1t,
\qquad
x_2=1-\frac{t^3}{1-t^4}. \tag{6.1}
\]

Then

\[
p_1x_1+p_2x_2=1,
\]

but

\[
p_1(x_1-1)^2+p_2(x_2-1)^2
=\frac{t^2}{1-t^4}\to0, \tag{6.2}
\]

while `x_1->infinity`. Small `Q-1` alone cannot control every active edge.

### 6.2 Other indispensable hypotheses

- Without connectivity, components have unrelated equality centers.
- Along a path, the interval overlap can attain `kappa` at every step, so a
  diameter-free bound does not follow from local data.
- Without support symmetry there is no second endpoint estimate.
- Without positivity, signed weighted squares can cancel.
- Theorems 4.1 and 5.1 control edge metric. Coordinate-space closeness modulo
  rotations additionally requires a framework-rigidity singular-value margin;
  no unsupported universal margin is claimed.

---

## 7. Exact examples and regression boundary

The exact Prompt 3 audit verifies:

| graph | `V` | degree | active dot | row rate | defect | `Q` | triangular sphere? |
|---|---:|---:|---:|---:|---:|---:|---|
| tetrahedron | 4 | 3 | `-1/3` | `3/2` | `8/3` | 1 | yes |
| octahedron | 6 | 4 | `0` | `2` | `2` | 1 | yes |
| cube | 8 | 3 | `1/3` | `3` | `4/3` | 1 | no |
| icosahedron | 12 | 5 | `1/sqrt(5)` | `(5+sqrt(5))/2` | `2-2/sqrt(5)` | 1 | yes |
| dodecahedron | 20 | 3 | `sqrt(5)/3` | `3(3+sqrt(5))/2` | `2-2sqrt(5)/3` | 1 | no |

The cube and dodecahedron remain permanent unrestricted counterexamples.
The audit also checks coordinate eigenmap equations, triangle incidence,
graph certificates, the `q=3,4,5` arithmetic, variance identities, stability
constants, the rare-edge counterfamily, and conductance-floor transfer.

---

## 8. Formalization boundary

`AFPBarrier/SphericalQOneRigidity.lean` formalizes:

- positivity of row rate at a nonzero exact eigenvalue;
- the exact local `Q=1` active-loss formula;
- strict positivity and zero-loss exclusion;
- connected equal-rate/equal-loss propagation;
- the antipodal row-rate consequence;
- the scalar equilateral tangent-angle identity;
- Euler/incidence arithmetic and the three count triples;
- the per-edge additive gap estimate;
- shared-edge additive center comparison; and
- shared-edge multiplicative cross bounds.

Standard external inputs retained as ordinary mathematics are the topology of
a strict geodesic triangulation, the icosahedral graph lemma, Cauchy rigidity,
and the real mean-value theorem. No project axiom is introduced.

---

## 9. Publication statement

Let a finite positive jump generator carry a unit-sphere coordinate eigenmap
with eigenvalue `-2`. Suppose its symmetric connected active graph is the
one-skeleton of a strict convex geodesic triangulation. If weighted
Cauchy--Schwarz is sharp at every vertex for the radial coordinate sample based
there, then the embedding is a regular tetrahedron, octahedron, or
icosahedron.

If sharpness is replaced by `Q_i<=1+epsilon` and every normalized active jump
has mass at least `p_*`, active edge losses and row rates satisfy the explicit
path and diameter estimates (4.2)--(4.6). Raw conductance and row-rate floors
yield the additive estimates (5.2)--(5.7). The classification fails without
triangulation, and edgewise stability fails without a lower active-weight
hypothesis.

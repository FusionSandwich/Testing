# Intrinsic icosahedral lattice and smooth-target audit

## Verdict

**SMOOTH-REGION MECHANISM VALID; FINITE CAP-TEMPLATE CLAIM REJECTED.**

The intrinsic equilateral lattice on a regular-icosahedron surface removes the
artificial macroedge mismatch of facewise radial projection. Away from the
twelve cone vertices, one can construct smooth reflected collars, positive
shared midpoint conductances, and the required pointwise \(O(h^2)\) quadratic
moment expansion.

It does not produce an unconditional all-level family by treating only the
twelve cone vertices with twelve finite templates. Each polyhedral vertex has
cone angle \(5\pi/3\), whereas a smooth spherical point has angle \(2\pi\).
Every bi-Lipschitz angle-correcting map is necessarily nonsmooth at the cone
point, so no uniform \(C^4\) Taylor constant reaches the apex. For the natural
homogeneous (or asymptotically homogeneous) angle corrector, a fixed finite
template repairs only finitely many lattice radii. The remaining fixed-radius
integer rings retain a scale-invariant leading defect and contribute at least
order \(h\), not \(h^2\), to the sampled quotient unless an **infinite
all-rings cap stencil** is proved. A specially tuned nonhomogeneous map could
escape this calculation only by supplying the same missing all-rings moment
certificate directly.

The second independent missing theorem is a uniform discrete
\(C^{2,\alpha}\) inverse for the exact harmonic correction. A continuum
Jacobi gap alone does not provide this estimate in the presence of cap
interfaces.

Thus this route is promising but remains blocked by two precise all-level
theorems rather than by macroedge smoothing. A separate fixed-domain blend
certificate is also still owed before numerical constants can be claimed.

## 1. Intrinsic lattice and macroedge collars

Let \(P\) be the boundary of a regular Euclidean icosahedron with unit edge
length and its intrinsic piecewise-flat metric. Away from the twelve
vertices, adjacent equilateral faces unfold by Euclidean reflection. Hence
the frequency-\(N\) triangular grids form one genuine equilateral lattice
across every open macroedge. Every nonvertex grid node has the ordinary six
nearest oriented directions and the graph square supplies six additional
oriented half-angle directions.

Fix a macroedge and remove fixed endpoint collars. Let \(s\) be arclength
along the edge and \(t\) signed intrinsic distance after unfolding. Let
\(g(s)\) be a constant-speed parametrization of the corresponding spherical
great-circle arc and let \(N\) be the unit normal to its plane. For any smooth
positive \(b(s)\),

\[
 F_{\rm col}(s,t)
 =\cos(b(s)t)\,g(s)+\sin(b(s)t)\,N                 \tag{1.1}
\]

maps a sufficiently thin collar into \(S^2\). Reflection in the edge is
exactly \(t\mapsto-t\) together with the ambient great-circle reflection.
Consequently (1.1) extends \(C^\infty\) across the macroedge. Assume

\[
 0<b_-\le b(s)\le b_+,\qquad
 \sum_{k=1}^4\|b^{(k)}\|_\infty\le B_4.            \tag{1.2}
\]

Put \(a=|g'(s)|>0\), which is constant. In the orthonormal target frame
consisting of the great-circle tangent and
\(-\sin(bt)g+\cos(bt)N\), the two derivative columns are exactly

\[
 DF_{\rm col}=
 \begin{pmatrix}a\cos(bt)&0\\ b'(s)t&b(s)\end{pmatrix}.          \tag{1.3}
\]
Consequently, if

\[
 |t|\le\rho_{\rm col}\le\min\{1,\pi/(4b_+)\},\qquad
 U=\sqrt{a^2+B_4^2\rho_{\rm col}^2+b_+^2},          \tag{1.4}
\]
then

\[
 \|DF_{\rm col}\|_{\rm op}\le U,
 \qquad
 \sigma_{\min}(DF_{\rm col})
 \ge \frac{ab_-}{\sqrt2\,U}.                       \tag{1.5}
\]
The lower bound follows from

\[
 \sigma_{\min}\ge
 \frac{|\det DF_{\rm col}|}{\|DF_{\rm col}\|_F}
 =\frac{ab|\cos(bt)|}{\|DF_{\rm col}\|_F}.
\]
Thus (1.4)--(1.5) are a literal local bi-Lipschitz certificate, and direct
differentiation bounds derivatives through order four by explicit
polynomials in \(a,b_+,B_4,\rho_{\rm col}\).

For the unit-edge regular icosahedron and its radially normalized target
vertices, \(a=\arccos(1/\sqrt5)\). There is a particularly useful
conformal-at-the-edge choice: take \(b(s)\equiv a\). Then

\[
 g_{\rm col}=a^2
 \begin{pmatrix}\cos^2(at)&0\\0&1\end{pmatrix},
 \qquad
 A_{\rm col}=
 \begin{pmatrix}1/\cos(at)&0\\0&\cos(at)\end{pmatrix}.           \tag{1.6}
\]

On \(|at|\le\pi/4\), its normalized anisotropy is bounded explicitly by

\[
 \frac{\lambda_{\max}(A_{\rm col})-
       \lambda_{\min}(A_{\rm col})}
      {\lambda_{\max}(A_{\rm col})+
       \lambda_{\min}(A_{\rm col})}
 =\frac{1-\cos^2(at)}{1+\cos^2(at)}
 \le\frac13.                                      \tag{1.7}
\]

Thus this collar lies inside the positive hexagonal tensor cone of Section
2 with the explicit margin
\(\eta_{\rm col}=\sqrt3/2-1/3=(3\sqrt3-2)/6\).

There are only thirty edge collars. An icosahedrally invariant Hermite
cutoff reduces blending (1.1) into a face-interior map, away from the vertex
neighborhoods, to a fixed compact-domain extension problem. Compactness
would bound all derivatives *after* a nonsingular extension is certified;
it does not itself certify that convex Hermite blending preserves the lower
singular-value bound.

The blend still has to be written down and its Jacobian checked to claim a
global constant. Formulas (1.1)--(1.5) establish only the point needed here:
smoothness across an open macroedge is constructive and is not the cone
obstruction. The finite extension is a third, finite-dimensional
certification obligation, not an all-level lattice theorem.

## 2. Positive midpoint tensor stencil on the smooth region

On a smooth intrinsic chart write \(F:U\to S^2\) and

\[
 g=(DF)^TDF,\qquad A=\sqrt{\det g}\,g^{-1}.         \tag{2.1}
\]

Since \(F:(U,g)\to S^2\) is a local isometry, its coordinate vector satisfies
the constrained harmonic equation

\[
 \operatorname{div}(A\,DF)
 =-2\sqrt{\det g}\,F.                              \tag{2.2}
\]

Let \(\mathcal V\) be the six unoriented lines in the square of the triangular
lattice, with angles \(k\pi/6\): use the three unit nearest-neighbor vectors
and the three length-\(\sqrt3\) diagonal two-hop vectors. Their signs define
a degree-twelve subgraph of the graph square. The trace-one rank-one tensors
\(v_kv_k^T/\|v_k\|^2\) map in the trace-free plane to the vertices of a
regular hexagon. Therefore every positive-definite \(2\times2\) tensor whose
normalized anisotropy lies strictly inside that hexagon has a decomposition

\[
 A(u)=\sum_{v\in\mathcal V}\rho_v(u)\,vv^T,\qquad
 \rho_v(u)\ge\rho_->0.                            \tag{2.3}
\]

An explicit sufficient condition is

\[
 \frac{\lambda_{\max}(A)-\lambda_{\min}(A)}
      {\lambda_{\max}(A)+\lambda_{\min}(A)}
 \le\frac{\sqrt3}{2}-\eta                         \tag{2.4}
\]

for some \(\eta>0\). Equivalently, the condition number is bounded strictly
below

\[
 \frac{1+\sqrt3/2}{1-\sqrt3/2}=7+4\sqrt3.          \tag{2.5}
\]

Smooth barycentric coordinates in the regular hexagon give explicit
\(\rho_v\). More precisely, write \(s=\sqrt3/2\),
\(e_v=v/\|v\|\), and normalize \(A\) by its trace. Under (2.4), set
\(\alpha=\eta/(2s)\). Its trace-free coordinate \(y\) is the convex
combination of the center with weight \(\alpha\) and
\(y'=y/(1-\alpha)\), which remains a positive distance inside the hexagon.
Use the standard mean-value coordinates of \(y'\) and represent the center
by the uniform combination of all six vertices. This gives

\[
 A=\sum_v\beta_v e_ve_v^T,\qquad
 \beta_v\ge\frac{\eta}{6\sqrt3}\operatorname{tr}A,\qquad
 \rho_v=\frac{\beta_v}{\|v\|^2}.                   \tag{2.6}
\]

In particular
\(\rho_v\ge \eta\operatorname{tr}A/
(6\sqrt3\max_v\|v\|^2)>0\). The mean-value formula

\[
 \widetilde\lambda_k(x)=
 \frac{\tan(\angle(r_{k-1},r_k)/2)+
       \tan(\angle(r_k,r_{k+1})/2)}{\|r_k\|},
 \quad r_k=z_k-x,                                  \tag{2.7}
\]

followed by normalization is positive, smooth, and point-reproducing on
this compact subhexagon. Its derivatives through order three have explicit
bounds obtained from
\(\tan(\angle(a,b)/2)=|a\wedge b|/(\|a\|\|b\|+a\cdot b)\); every denominator
has a positive minimum depending only on \(\eta\). Notice also that the
uniform combination supplies an isotropic tensor, not a nonexistent
positive null decomposition.

Choose one vector from each of the six unoriented lines as \(\mathcal V\),
and use both oriented edges \(\pm v\) in the graph. For a lattice edge with
midpoint \(m\) and direction \(v\), set

\[
 \gamma_{u,u+hv}=\rho_v(u+hv/2).                  \tag{2.8}
\]

with \(\rho_{-v}=\rho_v\). This is shared and positive. The mean-value
coordinate rule is equivariant under every dihedral symmetry of the regular
hexagon. Hence, across a reflected macroedge, transforming \(A\) and the
lattice directions by the unfolding reflection gives the same coefficient
on the same unoriented edge; there is no hidden directed-row choice.

Pairing \(+v\) and \(-v\), Taylor's formula and (2.2) give, uniformly where
\(F\) has bounded fourth derivatives and \(\rho_v\) has bounded third
derivatives,

\[
 \sum_{v\in\mathcal V\cup(-\mathcal V)}\gamma_{u,u+hv}
   \{F(u+hv)-F(u)\}
 =-2h^2\sqrt{\det g(u)}\,F(u)+O(h^4).              \tag{2.9}
\]

The same paired expansion gives

\[
 \widehat M_u=O(h^4),\qquad \mu_u\asymp h^2,
\qquad M_u=O(h^2).                                \tag{2.10}
\]

Thus the smooth-region baseline has the exact pointwise order needed by P1E,
not merely variational consistency.

The constants in (2.9)--(2.10) are explicit polynomials in
\[
 \rho_-^{-1},\quad
 \max_v\|\rho_v\|_{C^3},\quad
 \|F\|_{C^4},\quad
 \max_{v\in\mathcal V}\|v\|,\quad |\mathcal V|.    \tag{2.11}
\]

## 3. Exact cone obstruction at an icosahedral vertex

Let

\[
 C_\alpha
 =\{(r,\theta):r\ge0,\ \theta\in\mathbb R/\alpha\mathbb Z\},
 \qquad \alpha=\frac{5\pi}{3},                    \tag{3.1}
\]

with metric \(dr^2+r^2d\theta^2\). This is the intrinsic neighborhood of an
icosahedral vertex.

### Proposition 3.1 (no nondegenerate \(C^1\) angle correction)

There is no bi-Lipschitz map from a neighborhood of the apex in
\(C_{5\pi/3}\) to a smooth surface disk which has a nondegenerate derivative
at the apex in an unfolded sector.

Indeed, the boundary rays \((r,0)\) and \((r,\alpha)\) represent the same
points of the cone. If an unfolded derivative \(L\) existed, differentiation
of their identical images would give

\[
 L(1,0)=L(\cos\alpha,\sin\alpha).                  \tag{3.2}
\]

An invertible \(L\) would force \((1,0)=(\cos\alpha,\sin\alpha)\), impossible
for \(\alpha=5\pi/3\).

The standard bi-Lipschitz angle-correcting model is

\[
 F_0(r,\theta)
 =r\left(\cos\frac65\theta,\sin\frac65\theta\right).             \tag{3.3}
\]

It is homogeneous of degree one. On the punctured cone,

\[
 \|D^kF_0(r,\theta)\|\asymp r^{1-k},
 \qquad k\ge2.                                    \tag{3.4}
\]

Thus its \(C^4\) constant on \(r\ge\rho\) grows at least as
\(\rho^{-3}\). No fixed smooth-region Taylor constant survives down to the
first lattice rings \(r\asymp h\).

## 4. Why twelve finite templates do not repair the cone

Consider intrinsic lattice nodes \(u=hq\) with fixed nonzero integer cone
coordinate \(q\). By homogeneity,

\[
 F_0(hq)=hF_0(q).                                  \tag{4.1}
\]

For any scale-invariant bounded-hop conductance rule applied to (3.3), every
normalized first, mixed, and quadratic moment at \(hq\) has an \(h\to0\)
leading value depending only on the fixed integer star at \(q\). The same is
true for an asymptotically homogeneous corrector, with the limiting star in
place of the exact one. It does not acquire an extra factor of \(h^2\).

A finite cap template changes the stars only for \(\|q\|\le K\), with \(K\)
fixed. The node \(q\) on the next unmodified ring is still governed by the
same scale-invariant cone geometry. Unless the chosen cap law proves the exact
leading moment equations for **every** integer ring,

\[
 \sum_j\gamma_{qj}\tau_{qj}^{(0)}=0,\quad
 \sum_j\gamma_{qj}\ell_{qj}^{(0)}\tau_{qj}^{(0)}=0,\quad
 \sum_j\gamma_{qj}Q_q(\tau_{qj}^{(0)})=0,           \tag{4.2}
\]

some fixed ring has a nonzero limiting defect.

Here \(\tau_{qj}^{(0)}\) and \(\ell_{qj}^{(0)}\) are respectively the
scale-free tangent and loss terms of the limiting cone star, and \(Q_q\) is
the tangent trace-free quadratic projection. Thus (4.2) is not a shorthand
for the desired global theorem: it is a countable, explicit family of local
linear stress equations on the fixed angle-corrected cone lattice.

### Proposition 4.1 (one unrepaired cone row destroys the target order)

Suppose that for one fixed cone coordinate \(q\), along all sufficiently
small levels,

\[
 w_{q,h}\ge c_w h^2,
 \qquad M_{q,h}\longrightarrow M_q,
 \qquad m_q:=\|M_q\|_F>0.                           \tag{4.3}
\]
Then

\[
 \mathfrak D_2(L_h)
 \ge \sqrt{\frac{3c_w}{8}}\,m_q h                 \tag{4.4}
\]
for all sufficiently small \(h\). In particular
\(\mathfrak D_2(L_h)=O(h^2)\) is impossible.

Indeed, for small \(h\), \(\|M_{q,h}\|_F\ge m_q/2\), so this single row
contributes at least \(c_wh^2m_q^2/4\) to the residual-frame trace

\[
 \operatorname{tr}G_R=\sum_iw_i\|M_i\|_F^2.          \tag{4.5}
\]
The sampling trace is
\(\operatorname{tr}G_S=\sum_iw_i\|Z_i\|_F^2=2/3\) in dimension three, and
the sampled quotient inequality
\(\operatorname{tr}G_R\le\mathfrak D_2^2
\operatorname{tr}G_S\) gives (4.4).

More generally, if ring-\(k\) defects decay
like \(k^{-p}\), their squared contribution is

\[
 h^2\sum_{k\le c/h}k^{1-2p},                     \tag{4.6}
\]

which is never \(O(h^4)\) merely because a fixed number of inner rings were
replaced, provided at least one fixed outer-ring leading defect remains. A
nonhomogeneous construction that cancels every such leading defect is
precisely an all-rings cap construction, whether it is presented as a
special map or as special conductances. The only acceptable alternatives are:

1. an exact or \(O(h^2)\) all-rings cone stencil with uniform positivity;
2. a cap of fixed physical radius carrying a separate complete smooth mesh
   and an audited interface construction; or
3. noncomparable vanishing cap masses, together with a new sampling and
   boundary-stress proof.

Option 1 is an infinite parametric construction theorem. Option 2 contains
\(\Theta(h^{-2})\) cap nodes and is not a twelve-template argument. Option 3
abandons the requested uniform feasibility margin and must expose the small
mass explicitly.

### Exact rejected claim: positive cotangent equilibrium is not tightness

One cannot discharge the all-rings quadratic equations merely by citing
positive Delaunay/cotangent weights. Consider the cyclic planar star

\[
 u_1=(2,0),\quad u_2=(1,1),\quad
 u_3=(-3/10,7/5),\quad u_4=(-1,-1/5),\quad
 u_5=(1/5,-1).                                    \tag{4.7}
\]

Triangulate the fan from the origin and give each radial edge its standard
half-cotangent weight (the half-sum of the cotangents of its two opposite
angles). Exact rational arithmetic gives

\[
 (\gamma_1,\ldots,\gamma_5)
 =\left(\frac4{25},\frac{53}{68},\frac{762}{1241},
         \frac{349}{292},\frac75\right)>0,         \tag{4.8}
\]

and

\[
 \sum_{k=1}^5\gamma_ku_k=0,
 \qquad
 \sum_{k=1}^5\gamma_ku_ku_k^T
 =\begin{pmatrix}
 422852/155125&29819/62050\\
 29819/62050&8515/2482
 \end{pmatrix}.                                   \tag{4.9}
\]

The covariance is not scalar: its diagonal difference is
\(-12863/18250\) and its off-diagonal entry is \(29819/62050\).
Thus the same positive shared weights that give exact tangent equilibrium
can have a nonzero leading trace-free quadratic row. Spherical Delaunay
exactness for \(H_1\), even if transferred with all conventions checked,
does not by itself supply the cap part of P1E.

## 5. Exact harmonic correction and the inverse still required

On a globally valid baseline satisfying (2.7)--(2.8), one may seek an exact
critical embedding \(y_i=\exp_{F_i}u_i\). Icosahedral symmetry removes both
continuum kernel families:

- no nonzero vector is fixed by the icosahedral representation, so the
  conformal degree-one fields have no invariant member;
- a skew matrix commuting with the irreducible icosahedral representation is
  zero, so no invariant rotational field remains.

The equivariant continuum Jacobi operator therefore has a positive gap,
denote it by \(c_{\rm Ih}>0\). (A numerical value requires fixing the Jacobi
sign and normalization conventions.) If the discrete linearization \(J_h\)
satisfies

\[
 \|v_h\|_{2,\alpha,h}
 \le K_J\|J_hv_h\|_{0,\alpha,h}                  \tag{5.1}
\]

with \(K_J\) independent of \(h\), and the baseline residual in (2.7) is
bounded by \(\eta h^2\) after mass normalization, Newton contraction gives

\[
 \|u_h\|_{2,\alpha,h}\le2K_J\eta h^2              \tag{5.2}
\]

when \(4K_J^2Q\eta h^2\le1\). Edge increments then change by \(O(h^3)\), so
(2.8) and positivity survive.

But (5.1) does not follow from the continuum gap alone. It needs a global
discrete Schauder or Green-function theorem for the actual cap/interface
stencil. Pointwise consistency in the smooth region does not exclude
interface-localized or lattice-frequency modes. Consequently an exact
harmonic correction cannot be promoted before the all-rings cap law and its
uniform inverse are constructed.

## 6. Higher-dimensional regular-simplex boundary

The analogous boundary of a regular \(d\)-simplex has dimension \(d-1\), but
its intrinsic curvature is concentrated along the codimension-two skeleton,
not at finitely many isolated points. A bi-Lipschitz map to \(S^{d-1}\) has
the same transverse angle-correction singularity along every such stratum.
A fixed tubular neighborhood contains
\(\Theta(h^{-(d-3)})\) longitudinal lattice sites before counting transverse
rings.

Thus the higher-dimensional analogue requires:

- an all-rings transverse cone stencil along every codimension-two stratum;
- compatibility at intersections of strata;
- positive tensor decompositions in each tangent dimension; and
- a stratified discrete inverse.

This is precisely a stratified compiler, not a finite collection of vertex
templates. The simplex symmetry can remove the continuum gauge, but it does
not remove the geometric or discrete-interface theorem.

## 7. Route classification

| Component | Status |
|---|---|
| intrinsic triangular lattice across open macroedges | **COMPLETE** |
| explicit reflected spherical collar | **COMPLETE LOCALLY**, (1.1)--(1.5) |
| global nonsingular collar/interior blend | **FINITE CERTIFICATION STILL REQUIRED** |
| positive graph-square tensor decomposition | **COMPLETE UNDER** (2.4) |
| smooth-region \(H_1\) residual and pointwise \(H_2=O(h^2)\) | **COMPLETE CONDITIONAL ON FIXED \(C^4\) BOUNDS** |
| nondegenerate \(C^1\) map at the cone apex | **IMPOSSIBLE**, Proposition 3.1 |
| twelve finite cap templates | **REJECTED**, Section 4 |
| all-rings \(C_5\) cap stress | **BLOCKED / NOT CONSTRUCTED** |
| uniform discrete harmonic inverse | **BLOCKED / NOT CONSTRUCTED** |
| unconditional \(d=3\) P1E family on this route | **NOT YET PROVED** |
| higher-dimensional simplex analogue | **BLOCKED BY STRATIFIED CONE SKELETON** |

## 8. Exact regression source

The rational cotangent fixture (4.7)--(4.9) is checked without floating-point
arithmetic by

```text
python afp_barrier_gate1/pure_math/covariance/p1e_icosahedral_cone_audit.py
```

The script is a deterministic rejected-claim regression. It is not evidence
for, and does not replace, the missing all-rings construction or inverse
theorem.

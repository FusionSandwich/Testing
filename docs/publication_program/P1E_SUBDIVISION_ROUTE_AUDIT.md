# P1E recursive-subdivision and product-route audit

This note records an independent construction search for Prompt P1E. It is a
route audit, not the P1E existence theorem. Its purpose is to isolate one exact
operator transform that is useful in a complete construction and to prevent
three incomplete constructions from being promoted as proofs.

Throughout, \(n=d-1\), \(P_x=I-xx^T\), and all edge weights are shared:
\(\widetilde\gamma_{ij}=\widetilde\gamma_{ji}\).

## 1. Exact gnomonic stress transform

Let \(y_i\in\mathbb R^d\setminus\{0\}\), put

\[
s_i=|y_i|,\qquad \Omega_i=\frac{y_i}{s_i},
\]

and define

\[
\gamma_{ij}=s_i s_j\widetilde\gamma_{ij}.
\tag{1.1}
\]

Then the spherical chord force satisfies the exact identity

\[
P_i\sum_j\gamma_{ij}(\Omega_j-\Omega_i)
=s_iP_i\sum_j\widetilde\gamma_{ij}(y_j-y_i).
\tag{1.2}
\]

Indeed,

\[
\begin{aligned}
\sum_j\gamma_{ij}(\Omega_j-\Omega_i)
&=s_i\sum_j\widetilde\gamma_{ij}y_j
-y_i\sum_j s_j\widetilde\gamma_{ij}\\
&=s_i\sum_j\widetilde\gamma_{ij}(y_j-y_i)
+y_i\sum_j(s_i-s_j)\widetilde\gamma_{ij},
\end{aligned}
\]

and the second summand is radial. Consequently

\[
\sum_j\gamma_{ij}(\Omega_j-\Omega_i)\parallel\Omega_i
\quad\Longleftrightarrow\quad
\sum_j\widetilde\gamma_{ij}(y_j-y_i)\parallel y_i.
\tag{1.3}
\]

In particular, an affine equilibrium stress before radial projection gives
exact spherical \(H_1\) reproduction after (1.1). This is an identity, not an
asymptotic expansion.

For the explicit cross-polytope refinement one may take

\[
Y_N=\{N^{-1}k:k\in\mathbb Z^d,\ \|k\|_1=N\},
\qquad X_N=\{y/|y|:y\in Y_N\}.
\tag{1.4}
\]

The signed-permutation group acts exactly on both sets. The chambers are the
gnomonic images of the faces of the regular cross-polytope, so reflected
chamber stencils match combinatorially at every macroface. Formula (1.2)
shows precisely what is still required at the lower-dimensional strata: the
base affine force must be radial there. Reflection compatibility alone does
not imply that condition at a generic point of a macroedge.

The node family itself has explicit mesh bounds. For
\(x\in S^{d-1}\), put \(y=x/\|x\|_1\), round the nonnegative barycentric
coordinates \((|y_a|)\) to multiples of \(N^{-1}\) while preserving their
sum, and restore the signs. This produces \(y_N\in Y_N\) with
\(\|y-y_N\|_2\le\sqrt d/N\). Since \(\|y\|_2,\|y_N\|_2\ge d^{-1/2}\),
normalization gives

\[
\left\|x-\frac{y_N}{|y_N|}\right\|_2\le\frac{2d}{N}.
\tag{1.5}
\]

Conversely, the map \(F(x)=x/\|x\|_1\) is
\((1+\sqrt d)\)-Lipschitz in Euclidean norm because \(\|x\|_1\ge1\) on the
unit sphere. Distinct elements of \(Y_N\) differ by at least \(N^{-1}\), so

\[
\|\Omega_i-\Omega_j\|_2\ge\frac{1}{(1+\sqrt d)N}
\quad(i\ne j).
\tag{1.6}
\]

Thus \(X_N\) is quasiuniform with \(h=N^{-1}\) and a controlled mesh ratio.
Any fixed finite lattice-direction set gives a degree bound independent of
\(N\), and its radial images have an angular window \(O_d(h)\).

### 1.1 An exact positive feasibility stress

There is a completely explicit base stress on (1.4). For each unordered
coordinate pair \(\{a,b\}\), connect \(k\) to the configurations obtained by
moving one unit of absolute coordinate mass from \(a\) to \(b\), or from \(b\)
to \(a\), without changing the sign of a nonzero receiving coordinate. If the
receiver is zero, include both new signs. Give every such edge the shared
weight

\[
\widetilde\gamma_{k\ell}
=h^{n-2}\frac{|k_a|+|k_b|}{N}.
\tag{1.7}
\]

The pair sum is invariant under the transfer, so (1.7) is genuinely shared.
The degree is at most \(2\binom d2=d(d-1)\).

This stress has exact radial affine force. If \(k_a,k_b\ne0\), the two transfer
increments for the pair are opposites and have the same weight. If \(k_a=0\)
and \(k_b\ne0\), the two possible signs at \(a\) have increments whose sum is

\[
-2h\,\operatorname{sgn}(k_b)e_b,
\]

and their common pair factor is \(|k_b|/N=|y_b|\). Hence, if \(z(k)\) is the
number of zero coordinates,

\[
\sum_{\ell}\widetilde\gamma_{k\ell}(y_\ell-y_k)
=-2z(k)h^{n-1}y_k.
\tag{1.8}
\]

Equations (1.2) and (1.8) give an explicit positive, bounded-degree, local,
exact-\(H_1\) spherical generator after the radial rescaling. The large
coordinate \(|y_{a_*}|\ge1/d\) and its transfer edges to all other coordinates
also give a uniformly spanning local tangent star.

This exact feasibility stress is not second-order isotropic. In the interior
of one sign chamber its unscaled affine second moment is proportional to

\[
2\sum_{a<b}(|y_a|+|y_b|)
(\operatorname{sgn}(y_b)e_b-\operatorname{sgn}(y_a)e_a)
(\operatorname{sgn}(y_b)e_b-\operatorname{sgn}(y_a)e_a)^T.
\tag{1.9}
\]

At a generic point its two or more tangent eigenvalues differ by an
order-one amount. For example, in \(d=3\), at
\(y=(1/2,3/10,1/5)\), the matrix in (1.9) is

\[
\begin{pmatrix}
3&-8/5&-7/5\\
-8/5&13/5&-1\\
-7/5&-1&12/5
\end{pmatrix},
\]

and its two generalized eigenvalues on \(y^\perp\) are exactly

\[
\frac{71-3\sqrt7}{19},
\qquad
\frac{71+3\sqrt7}{19}.
\tag{1.10}
\]

It is therefore an exact strict-feasibility baseline and a useful
macrostratum stencil, not the required \(H_2\)-consistent family. Also, the
smallest edge factor in (1.7) is \(h\), so any correction using all edges must
keep that quantified nonuniform positivity margin visible.

## 2. The exact continuum tensor behind the transform

On one gnomonic chart write

\[
y=(1,u),\qquad s=(1+|u|^2)^{1/2},\qquad
\Omega(u)=s^{-1}(1,u).
\]

The positive tensor

\[
Q(u)=s^{-d}(I_n+uu^T)
\tag{2.1}
\]

has three exact properties.

First, it is a cofactor Hessian:

\[
D^2s=s^{-1}I_n-s^{-3}uu^T,
\qquad Q=\operatorname{cof}(D^2s).
\tag{2.2}
\]

The tangential eigenvalue of \(D^2s\) is \(s^{-1}\), its radial eigenvalue is
\(s^{-3}\), and taking complementary products gives the eigenvalues
\(s^{-d}\) and \(s^{2-d}\) of (2.1).

Second, the Piola identity (or direct differentiation) gives

\[
\operatorname{div}Q=0.
\tag{2.3}
\]

Directly, for \(Q_{ab}=s^{-d}(\delta_{ab}+u_au_b)\),

\[
\partial_a Q_{ab}
=-d s^{-d-2}s^2u_b+d s^{-d}u_b=0.
\]

Third, it gives exactly the isotropic spherical tangent tensor after the
conductance rescaling in (1.1). If \(D=D\Omega(u)\), then

\[
D^TD=s^{-2}I_n-s^{-4}uu^T,
\qquad (D^TD)^{-1}=s^2(I_n+uu^T),
\]

and therefore

\[
s^2D QD^T=s^{-d}P_{\Omega(u)}.
\tag{2.4}
\]

Thus a shared positive lattice stress which is exactly affine-equilibrated and
whose second moment approximates \(Q\) with error \(O(h^2)\) yields, through
(1.1), exact \(H_1\) reproduction and \(O(h^2)\) tangent-frame anisotropy.
Equations (1.2)--(2.4) reduce the geometric part of the proposed construction
to a flat, divergence-free stress discretization on finitely many reflected
chambers.

## 3. The remaining theorem-strength lemma

The reduction is not itself a complete P1E construction. What remains is an
all-dimensional theorem producing, on the lattice (1.4), shared edge stresses
with all of the following properties simultaneously:

1. a fixed bounded set of lattice directions and hence bounded degree;
2. strict bounds \(0<c_-h^{n-2}\le\widetilde\gamma_{ij}
   \le c_+h^{n-2}\);
3. exact affine equilibrium at every vertex, including all cross-polytope
   strata;
4. second moment \(Q(u)+O(h^2)\), uniformly and pointwise;
5. the same estimates after the finite chamber gluing.

A midpoint directional decomposition of \(Q\) gives items 1, 2, and 4, but in
general only gives affine-force error \(O(h^2)\), not item 3. Projecting that
error onto exact shared stresses requires a uniform right inverse for the
edge-to-vector equilibrium map. That is a discrete elasticity/Korn theorem;
calling it a local correction does not remove the global compatibility issue.

There is a special two-dimensional mechanism. When \(n=2\), (2.2) is the
Airy-stress representation and regular/Delaunay liftings provide exact
equilibrium stresses. In higher dimension, the cofactor Hessian remains
divergence free, but a positive scalar edge-stress discretization does not
follow from the continuum Piola identity. The standard elementwise sign
guarantee for a simplicial \(P_1\) stiffness matrix requires a metric-nonobtuse
condition, and a strict positive margin would require a correspondingly
strong angle margin. Such a mesh theorem is not supplied here. Therefore
neither **cof Hess** nor **standard FEM** may be cited as silently proving the
five properties above.

This route becomes complete if a construction supplies the five properties
by an explicit discrete stress potential, or proves the uniform right-inverse
estimate with its kernel, boundary/collar, and positivity margins audited.

## 4. Exact blockers for three tempting alternatives

### 4.1 Edge-only recursive subdivision

If a new vertex has only the two neighboring vertices on its subdivided great
circle edge, its projected increments lie in a one-dimensional subspace. For
\(n\ge2\), its tangent covariance has rank one and cannot be within \(o(1)\) of
a positive multiple of \(P_i\). Consequently its local \(B_i\) has an
order-one anisotropic part. Subdividing the old edges more finely does not
repair the missing \(n-1\) tangent directions. Cross-cell edges or an
equivalent multidirectional stencil are indispensable.

### 4.2 Uniform tensor-product polar grids

On \(S^2\), take colatitude spacing \(h\) and longitude spacing \(h\). The
first nonpolar ring has \(\theta\asymp h\), so adjacent points on that ring are
separated by

\[
\sin\theta\,h\asymp h^2,
\]

whereas the fill distance remains \(\asymp h\). Hence the mesh ratio is at
least \(c/h\). The same degeneracy occurs recursively in hyperspherical
coordinates. Reducing the number of angular nodes near a pole removes the
mesh-ratio defect but destroys the tensor-product graph at the interfaces;
shared reversibility and exact coordinate reproduction then require an
additional reconciliation proof.

### 4.3 Positive polynomial correction of a Markov generator

Let \(P_h\) be a local Markov operator and try to replace it by a positive
polynomial \(q(P_h)=\sum_{k=0}^m c_kP_h^k\), \(c_k\ge0\),
\(\sum c_k=1\). If \(P_h\Omega=\lambda_h\Omega\) with
\(0<\lambda_h<1\), exact first-harmonic correction requires
\(q(\lambda_h)\) to hit a prescribed value while retaining a second-order
match at \(1\). But

\[
q'(1)=\sum_{k=0}^m k c_k
\]

is nonnegative and is zero only for the trivial constant polynomial. In
particular, positive mixtures cannot cancel a nonzero leading derivative/error
term. Allowing negative coefficients loses positivity; allowing unbounded
degree enlarges the angular window. This route cannot provide the required
local positive correction.

## 5. Finite-element mass blocker

Galerkin consistency is not the pointwise identity required in P1E. With
nodal basis functions \(\phi_i\), stiffness \(K\), and consistent mass \(M\), a
weak identity has the form

\[
K\Omega=nM\Omega+\text{geometric interpolation error}.
\]

Even if the interpolation error vanished, \(M\Omega\) is generally not a
diagonal mass times \(\Omega_i\). Replacing \(M\) by row-sum lumping changes
the right side and does not make each vector row radial. Thus standard
barycentric finite elements do not by themselves give
\(L_h\Omega=-n\Omega\). One must prove a radial row identity or carry out an
exact shared-stress correction.

## 6. Route status

The exact transform (1.2) and tensor identities (2.1)--(2.4) are proved and
are suitable ingredients for the P1E theorem. The following routes are
**BLOCKED** as stand-alone all-dimensional constructions:

| route | exact obstruction |
|---|---|
| raw barycentric/cross-polytope refinement | continuum divergence-free stress has not been converted to a positive exact discrete shared stress at all strata |
| edge-only recursive subdivision | rank-one tangent covariance at inserted edge vertices |
| tensor polar grid | mesh ratio diverges; adaptive interfaces need reconciliation |
| standard mass-lumped FEM | weak/consistent-mass identity is not the pointwise radial row identity |
| positive Markov polynomial | positivity prevents cancellation of the leading derivative/error term |

No numerical rank threshold or fixed-level experiment resolves the remaining
shared-stress lemma.

## 7. Polar support-volume Hessian: exact identities and terminal-cell gate

There is a second exact route to the same radial row identity which does not
start with an approximately equilibrated stress.  It is useful, but it does
not by itself remove the consistency gate.

Let \(X=\{\Omega_i\}\subset S^{d-1}\) positively span
\(\mathbb R^d\), and, for support numbers \(z\) near \(1\), put

\[
 P(z)=\{x:\Omega_i\mathbin\cdot x\le z_i\},\qquad
 \mathcal V(z)=\operatorname{vol}_d P(z).
\tag{7.1}
\]

Assume the normal fan is locally constant at \(z=1\).  If facets \(i,j\)
meet, let \(R_{ij}\) be the \((d-2)\)-volume of their common ridge and
\(\theta_{ij}=\arccos(\Omega_i\cdot\Omega_j)\).  Direct differentiation of
facet area gives

\[
 \gamma_{ij}
 =\partial_i\partial_j\mathcal V(1)
 =\frac{R_{ij}}{\sin\theta_{ij}}>0.
\tag{7.2}
\]

It is shared because it is a Hessian.  Translation invariance of
\(\mathcal V\), equivalently the facet divergence theorem below, gives

\[
 P_i\sum_j\gamma_{ij}(\Omega_j-\Omega_i)=0.
\tag{7.3}
\]

Here is a completely local verification which also identifies the mass.
In the affine facet plane write \(x=\Omega_i+y\), \(y\in T_iS^{d-1}\), and
put

\[
 t_{ij}=\frac{P_i\Omega_j}{\sin\theta_{ij}},\qquad
 q_{ij}=\tan\frac{\theta_{ij}}2.
\]

The translated facet is the tangent polytope

\[
 D_i=F_i-\Omega_i
 =\{y:t_{ij}\cdot y\le q_{ij}\}.
\tag{7.4}
\]

Its \(ij\)-face has area \(R_{ij}\).  The divergence theorem applied to a
constant vector field and to \(y\) gives

\[
 \sum_jR_{ij}t_{ij}=0,
 \qquad
 \sum_jR_{ij}q_{ij}=n|D_i|,
 \quad n=d-1.
\tag{7.5}
\]

Since \(P_i(\Omega_j-\Omega_i)=\sin\theta_{ij}t_{ij}\) and
\(1-\cos\theta_{ij}=\sin\theta_{ij}q_{ij}\), equations (7.2)--(7.5)
prove (7.3) and the exact mass formula

\[
 \mu_i=\frac1n\sum_j\gamma_{ij}(1-\Omega_i\cdot\Omega_j)
      =|D_i|.
\tag{7.6}
\]

Consequently the support Hessian gives positivity, reversibility, and exact
\(H_1\) reproduction without a subsequent stress correction.  On a
quasiuniform strict normal fan,

\[
 \gamma_{ij}\asymp h^{n-2},\qquad
 \mu_i\asymp h^n,\qquad r_i\asymp h^{-2}.
\tag{7.7}
\]

### 7.1 Why \(C^3\) smoothing alone is not the \(H_2\) proof

The leading tangent second moment in (7.2) is governed by the Euclidean
Voronoi cell obtained by blowing up \(D_i\).  For a face with unit normal
\(t_a\), support \(q_a\), and length/area \(A_a\), its dimensionless tensor
is

\[
 \mathcal Q(D)=|D|^{-1}\sum_a A_aq_a\,t_at_a^T.
\tag{7.8}
\]

The divergence theorem controls
\(\sum A_a\bar y_a t_a^T=|D|I\), where \(\bar y_a\) is the face
centroid.  It does **not** replace \(\bar y_a\) by \(q_at_a\).  Thus it does
not imply \(\mathcal Q(D)=I\).

An exact two-dimensional witness is

\[
 D=\{(x,y):x\le1,\ y\le1,\ x+y\ge-\sqrt2\}.
\tag{7.9}
\]

Its three unit outer normals are
\(t_1=(1,0)\), \(t_2=(0,1)\), and
\(t_3=(-1,-1)/\sqrt2\), all three supports are \(q_a=1\), and

\[
 |D|=3+2\sqrt2,
\]

\[
 A_1=A_2=2+\sqrt2,
 \qquad A_3=2+2\sqrt2.
\]

Substitution in (7.8) gives exactly

\[
 \mathcal Q(D)
 =\begin{pmatrix}1&\sqrt2-1\\[2pt]\sqrt2-1&1\end{pmatrix}\ne I.
\tag{7.10}
\]

This is a genuine Voronoi cell: take the site \(0\), the three neighboring
sites \(2t_a\), and add sufficiently distant sites if a finite bounded
configuration is desired.  Scaling all sites by \(h\) preserves (7.10).
The associated polar-Hessian row therefore has an order-one normalized
tangent anisotropy.  In sphere dimension \(n=2\), even one such terminal
cell has mass comparable with \(h^2\), so its squared residual contributes
order \(h^2\), not the required order \(h^4\).  Choosing a fixed traceless
quadratic aligned with the off-diagonal eigentensor in (7.10), and completing
the nodes outside this chart by any uniformly sampled mesh, keeps its sampled
denominator bounded above and below.  The single bad row then gives
\(\mathfrak D_2\ge c h\), contradicting an \(O(h^2)\) conclusion for that
template.

The witness can be inserted in a \(C^\infty\) coordinate chart.  It proves
that smoothness of the macroface parameterization, quasiuniformity, bounded
degree, and strict Delaunay positivity do not imply the desired quadratic
order.  A complete polar construction must additionally prove, for every
blown-up seam and terminal template,

\[
 \mathcal Q(D)=I
\tag{7.11}
\]

at leading order, and it must prove the paired first-variation cancellation
which improves the remaining error to \(O(h^2)\).  At codimension-two
strata an \(O(h)\) normalized error is still admissible because their total
mass is \(O(h^2)\); at deeper strata the corresponding symmetry estimate
must be stated and checked.  An explicit \(C^3\) collar function, for
example

\[
 \psi_\eta(t)=
 \begin{cases}
 \displaystyle\frac{\eta}{16}
 \left(35s^2-35s^4+21s^6-5s^8\right),
       &s=|t|/\eta\le1,\\[4pt]
 |t|,&|t|\ge\eta,
 \end{cases}
\tag{7.12}
\]

matches \(|t|\) through third derivative at \(|t|=\eta\) and is monotone,
but it does not
enforce (7.11).  Moreover, radial smoothing of the source boundary is
invisible after normalization: for every positive scalar \(\lambda(y)\),

\[
 \frac{\lambda(y)y}{|\lambda(y)y|}=\frac y{|y|}.
\tag{7.13}
\]

Hence a rounded cross-polytope must be supplied with a genuinely tangential
remeshing; radial rounding cannot repair a bad terminal template.

The polar route is therefore **BLOCKED AS AN UNCONDITIONAL ALL-D ROUTE**
until (7.11) and its first-variation version are proved for an explicit,
globally compatible finite template catalogue.  The obstruction is local
and exact, rather than a missing numerical experiment.

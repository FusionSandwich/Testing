# P1E structured-stress route audit (blocked candidate)

> **Status: REJECTED AS AN UNCONDITIONAL CONSTRUCTION.**  Sections 1 and the
> finite correction algebra are conditional lemmas only.  The proposed
> reflected cubulation is topologically false at singular strata, and the
> required uniform \(\ell^\infty\) elasticity right inverse is not proved.
> This document is retained solely as a non-promotion audit and must not be
> cited as the P1E upper family.  The exact blockers and corrected sampling-cap
> constant are recorded in the subdivision and polar/Piola route audits.

## 0. Source boundary and statement

This proof starts from the frozen P1D checkpoint

```text
archive/afp-publication-p1d-quantitative-stability-verified
commit 368e709c15efc1d1d25ad063d79ebbd8feecd9ed
tree   cce67cdcc6c5ee360c1894702197b84e850bed64
```

P1A supplies the sampling quotient and row tensors, P1B supplies the sharp
lower bound, P1C supplies the radial--tangent block algebra, and P1D supplies
stability diagnostics.  No earlier result supplies the upper family proved
here.

Put

\[
 n=d-1,
 \qquad d\ge2.
\]

The rejected candidate attempted, for every fixed \(d\), to construct a sequence
\(h=h_d^{\rm ref}/N\to0\), a
finite set \(X_h\subset S^{d-1}\), a bounded-degree graph \(E_h\), normalized
positive masses \(w_h\), and shared positive conductances \(\gamma_h\).  For
all sufficiently small \(h\),

\[
 L_h1=0,
 \qquad
 L_h\Omega=-n\Omega,
 \qquad
 r_{\max}(L_h)\le R_dh^{-2},
 \qquad
 \mathfrak D_2(L_h)\le C_dh^2.                    \tag{0.1}
\]

The advertised finite atlas compiler and its constants were not actually
constructed.  In particular, the singular-stratum templates and the
maximum-norm inverse used below are hypotheses, not proved outputs.

## 1. Finite row identities

For unit nodes \(x_i\in S^{d-1}\), write

\[
 P_i=I-x_ix_i^T,
 \qquad
 \Delta_{ij}=x_j-x_i,
 \qquad
 \ell_{ij}=1-x_i\cdot x_j,
 \qquad
 \tau_{ij}=P_ix_j.                                 \tag{1.1}
\]

Thus

\[
 \Delta_{ij}=-\ell_{ij}x_i+\tau_{ij},
 \qquad
 \|\Delta_{ij}\|^2=2\ell_{ij}.                    \tag{1.2}
\]

Let \(\gamma_{ij}=\gamma_{ji}>0\) be an undirected edge stress and define its
tangent force

\[
 (T_x\gamma)_i=\sum_j\gamma_{ij}\tau_{ij}.         \tag{1.3}
\]

If \(T_x\gamma=0\), put

\[
 \mu_i=\frac1n\sum_j\gamma_{ij}\ell_{ij},
 \qquad
 W=\sum_i\mu_i,
 \qquad
 w_i=\frac{\mu_i}{W},
 \qquad
 \bar\gamma_{ij}=\frac{\gamma_{ij}}W.             \tag{1.4}
\]

Then \(\mu_i>0\), \(\sum_iw_i=1\), and

\[
 \sum_j\gamma_{ij}\Delta_{ij}=-n\mu_ix_i.         \tag{1.5}
\]

Indeed, (1.3) kills the tangent part and radial contraction gives
\(-\sum_j\gamma_{ij}\ell_{ij}=-n\mu_i\).  Hence the generator

\[
 (Lf)_i=\sum_j\frac{\gamma_{ij}}{\mu_i}(f_j-f_i)   \tag{1.6}
\]

is positive and reversible and satisfies exactly

\[
 L1=0,
 \qquad
 Lx=-nx.                                            \tag{1.7}
\]

The unnormalized quadratic row error is

\[
 \widehat M_i(\gamma,x)
 =\sum_j\gamma_{ij}
 \left[
   \Delta_{ij}\Delta_{ij}^T-
   \frac{2\ell_{ij}}nP_i
 \right].                                          \tag{1.8}
\]

Using (1.4), the P1A row representer is exactly

\[
 M_i=\frac{\widehat M_i}{\mu_i}.                   \tag{1.9}
\]

No injectivity of \(S_2\) is used in (1.9).

## 2. The fixed finite atlas compiler

The construction begins with data compiled once for each \(n\).  We give the
compiler, rather than assuming a generic mesh has the properties it needs.

### 2.1 Smooth symmetric cubulation

Let \(G_d\) be the signed-permutation group acting on \(S^{d-1}\).  Start with
the cubical barycentric subdivision of the boundary of the cross-polytope,
average every collar choice over \(G_d\), and apply the standard finite
collar-smoothing recursion in increasing codimension.  The result is a finite
\(G_d\)-equivariant smooth cubulation \({\cal C}_d\) with the following
effective data:

* finitely many reflected collar charts \(\Phi_a\), each defined on a box
  enlarged by a fixed collar;
* face identifications given by signed coordinate permutations;
* bounds \(K_{d,r}\) for every derivative of \(\Phi_a\) and
  \(\Phi_a^{-1}\) through order six;
* singular-value bounds
  \(0<s_{d,-}\le s_{\min}(D\Phi_a)\le
  s_{\max}(D\Phi_a)\le s_{d,+}\).

This is an algorithm on a finite complex.  At a codimension-\(r\) face the
new collar is obtained from the unique degree-\(13\) Hermite interpolant whose
jets through order six match the already fixed collars at both ends.  Its
coefficients are obtained by a fixed rational linear solve.  Subdivide the
collar once more if its interval derivative enclosure is not positive.  The
Hermite remainder estimate shows that this refinement terminates; there are
only finitely many faces.  Thus injectivity and every derivative bound are
certified by finite rational interval arithmetic.  No \(h\)-dependent atlas
is chosen.

Uniformly subdivide each cubical coordinate into \(N\) parts.  Put
\(h=h_d^{\rm ref}/N\), where the fixed rational enclosure
\(h_d^{\rm ref}\) is chosen to be the largest fill constant of the finitely
many chart templates.  Identify face nodes,
and use the common reflected collar chart for every grid edge crossing a macro
face.  At a codimension-\(r\) stratum all \(2^r\) reflected sectors are
included; their signed direction list contains \(v\) and \(-v\) with the same
midpoint.  This explicitly supplies the cross-chart edges that a disjoint
chart overlay would miss.  Denote the resulting reference nodes by \(y_i^h\).
Directly from the singular-value and collar bounds there
are computable constants

\[
 q_0,\Lambda_0,N_+>0                              \tag{2.2}
\]

such that

\[
 \operatorname{fill}(Y_h)\le h,
 \qquad
 \operatorname{sep}(Y_h)\ge q_0h,
 \qquad
 |Y_h|\le N_+h^{-n}.                                \tag{2.3}
\]

### 2.2 A finite positive direction cone

In each collar chart let

\[
 A_a(x)=\sqrt{\det g_a(x)}\,g_a(x)^{-1}.            \tag{2.4}
\]

The set of all matrices (2.4), transported by the finitely many signed
permutations, is a compact subset \({\cal A}_d\) of the interior of the
positive-definite cone.  The following finite construction is used.

1. Cover \({\cal A}_d\) by rational Frobenius balls whose doubled balls remain
   positive definite.
2. In each ball choose rational directions \(v\in\mathbb Z^n\) so that the
   center is in the interior of the cone generated by \(vv^T\).
3. Add the full signed-permutation orbit, every coordinate direction, and all
   pair differences in each two-layer Freudenthal macrostar.  These extra
   edges cross every macroface; consecutive rigid clusters share \(d\)
   affinely independent physical nodes.
4. Subtract a sufficiently small common floor from every coefficient and use
   a rational partition of unity on the doubled balls.

This returns a finite symmetric set \({\cal V}_d\subset\mathbb Z^n\), a
radius \(s_d=\max_{v\in{cal V}_d}\|v\|_1\), and smooth coefficient functions
\(\rho_v(A)\) satisfying identically

\[
 A=\sum_{v\in{cal V}_d}\rho_v(A)vv^T,             \tag{2.5}
\]

\[
 0<\rho_-\le\rho_v(A)\le\rho_+                    \tag{2.6}
\]

for every \(A\in{\cal A}_d\).  Every operation is rational except evaluation
of the fixed smooth atlas, whose enclosure is certified by intervals.  Thus
\(s_d,\rho_\pm\) are effective constants, not existential choices depending
on \(h\).

### 2.3 Baseline shared conductances

Connect two grid nodes whenever a reflected collar chart represents their
indices as \(k\) and \(k+v\), \(v\in{\cal V}_d\).  The collar hierarchy
assigns every midpoint to exactly one common chart (highest codimension
first), so an edge is not independently reconstructed from its two endpoint
charts.  At that midpoint set its contribution to
\(h^{n-2}\rho_v(A_a)\).  If two compiled direction records name the same
undirected edge, their positive contributions are summed and the same sum is
used at both endpoints.  The resulting undirected conductance is denoted
\(\gamma^0_{ij}\).

There are computable constants \(D_0,g_-,g_+>0\) such that

\[
 \deg(i)\le D_0,
 \qquad
 g_-h^{n-2}\le\gamma^0_{ij}\le g_+h^{n-2},         \tag{2.7}
\]

and every active angular edge satisfies

\[
 q_0h\le\theta_{ij}\le\Lambda_0h.                 \tag{2.8}
\]

The two-layer clique edges retained in Step 3 make every cell-and-interface
framework rigid and give a strict local cone margin \(g_-\).

### 2.4 Why the macro-skeleton is not an assumption

A collection of independent chart lattices would fail both separation and
first-moment balance.  The compiler does something different.  Each
codimension-one macroface is assigned a fixed physical collar, and that collar
has one smooth coordinate system crossing the face.  Its grid replaces, rather
than overlays, the two truncated interior grids.  In these coordinates every
midpoint edge occurs in a \(v,-v\) pair.  At intersections of collars the
codimension hierarchy repeats this construction in a single common chart.

There are finitely many terminal singular stars.  In a normal chart around
such a star, place the signed-permutation orbit of the integer direction set
\({\cal V}_d\) on the first two grid layers and join the complete two-layer
macrostar.  The origin is in the strict interior of its first-moment cone, and
(2.5) puts the metric tensor in the strict interior of its second-moment cone.
Using the same coefficient on \(v\) and \(-v\) kills every odd Taylor tensor
through degree three.  A degree-\(13\) Hermite annulus joins this core to the
already compiled collar grid.  The annulus has a fixed number of template
types; its compact metric range is fed back into Steps 1--4 of Section 2.2.

This codimension induction terminates after \(n\) stages.  At each stage the
only tests are positivity of a finite coefficient vector, nonsingularity of a
finite template Jacobian, and interval bounds for a fixed polynomial map.
Their strict margins are included in \(g_-,q_0\), and the derivative list
\(K_{d,r}\).  Thus the macro-skeleton stencil is part of the explicit offline
construction.  It is not inferred from a partition of unity, an independent
chart overlay, or ordinary mesh quasiuniformity.

## 3. Pointwise second-order consistency

At an ordinary chart node, pair the contributions in directions \(v\) and
\(-v\).  For a scalar \(f\in C^6\), the exact one-dimensional midpoint
expansion is

\[
\begin{aligned}
&\rho(x+hv/2)[f(x+hv)-f(x)]\\
&\quad+\rho(x-hv/2)[f(x-hv)-f(x)]\\
&=h^2\partial_v(\rho\,\partial_vf)(x)
  +h^4\left(
    \frac{\rho f^{(4)}}{12}
   +\frac{\rho'f^{(3)}}6
   +\frac{\rho''f''}{8}
   +\frac{\rho'''f'}{24}
  \right)(x)+O(h^6).                               \tag{3.1}
\end{aligned}
\]

Equation (2.5) turns the leading sum into
\(h^n\sqrt{\det g}\,\Delta_{S^n}f\).  The same expansion holds at every
macroface and corner: the reflected collar is a single smooth chart there,
and the odd terms in (3.1) cancel before restriction to either incident cell.
There are only finitely many collar templates, so the remainder is bounded by
one explicit maximum of \(K_{d,r},\rho_+\), and the direction moments
\(\sum_v|v|^6\).

For a literal reproducible choice, let

\[
 {\cal K}_6=
 1+\max_{a,\;1\le r\le6}
 \left(
  \|D^r\Phi_a\|_\infty+
  \|D^r\Phi_a^{-1}\|_\infty+
  \max_v\|D^r(\rho_v\circ A_a)\|_\infty
 \right),
\]

\[
 V_6=1+\sum_{v\in{\cal V}_d}|v|^6.                 \tag{3.2}
\]

Taylor's formula with integral remainder permits the deliberately loose
certified values

\[
 b_0=8D_0g_+(1+n){\cal K}_6V_6,
 \qquad
 m_0=16D_0g_+(1+n){\cal K}_6V_6.                  \tag{3.3}
\]

Applying (3.1) to the coordinate map and polarizing its application to
quadratic coordinate products yields constants \(b_0,m_0>0\) such that,
uniformly in \(i\),

\[
 \left\|T_y\gamma^0\right\|_i
 \left\|\widehat M_i(\gamma^0,y)\right\|_F
 \le (b_0+m_0)h^{n+2},                             \tag{3.4}
\]

more precisely

\[
 \left\|(T_y\gamma^0)_i\right\|\le b_0h^{n+2},
 \qquad
 \left\|\widehat M_i(\gamma^0,y)\right\|_F
 \le m_0h^{n+2}.                                   \tag{3.5}
\]

This is a pointwise tensor statement.  A weak finite-element truncation or a
fitted slope is not substituted for (3.5).

## 4. Global reversible reconciliation

Pointwise consistency does not make the tangent force exactly zero.  We now
correct the **shared** conductances.  This is where the global feasibility
margin enters.

### 4.1 The strain operator and compatibility

Give tangent vertex fields the unweighted Euclidean pairing and edge arrays
the ordinary edge pairing.  The adjoint of (1.3) is

\[
 (T_y^*u)_{ij}
 =u_i\cdot\tau_{ij}+u_j\cdot\tau_{ji}.              \tag{4.1}
\]

Let \(\Gamma^0=\operatorname{diag}(\gamma_e^0)\) and

\[
 K_h=T_y\Gamma^0T_y^*.                              \tag{4.2}
\]

Every skew matrix \(A\) gives a tangent rotation \(u_i=Ay_i\), and direct
edge pairing shows \(T_y^*u=0\).  Conversely, every two-layer macrostar
clique is infinitesimally rigid.  Consecutive cliques share \(d\)
affinely independent vertices, so their ambient infinitesimal rigid motions
agree.  Induction across the connected cubulation proves

\[
 \ker T_y^*
 =\{(Ay_i)_i:A^T=-A\}.                              \tag{4.3}
\]

An ambient translation is excluded because the field is required to be
tangent at every node; \(a\cdot y_i=0\) on an \(h\)-dense set forces \(a=0\)
for all sufficiently small \(h\).

For every symmetric edge stress \(\eta\),

\[
 \sum_i(Ay_i)\cdot(T_y\eta)_i=0.                    \tag{4.4}
\]

Thus the baseline defect \(b=T_y\gamma^0\) belongs to
\(\operatorname{ran}T_y\), and (4.2) can be inverted on the orthogonal
complement of rotations.

### 4.2 Quantitative discrete elasticity lemma

There is an effectively computable \(C_{\rm el}=C_{\rm el}(d,{\cal C}_d,
{\cal V}_d,\rho_\pm)\) such that, for every sufficiently small \(h\), every
compatible tangent load \(f\), and

\[
 u=K_h^\dagger f,
\]

one has

\[
 \boxed{
 \|T_y^*u\|_{\ell^\infty(E_h)}
 \le C_{\rm el}h^{-n}\|f\|_{\ell^\infty(I_h)}.
 }                                                   \tag{4.5}
\]

Here \(K_h^\dagger\) is zero on rotations.  We include the proof because
(4.5) is the global statement that rowwise feasibility cannot replace.

In an ordinary collar chart freeze the coefficients at \(x\).  The symbol of
the scalar part of the energy contains every coordinate direction with weight
at least \(\rho_-\):

\[
 4\sum_{v\in{\cal V}_d}\rho_v(x)
   \sin^2\frac{\xi\cdot v}{2}
 \ge
 4\rho_-\sum_{a=1}^n\sin^2\frac{\xi_a}{2}.          \tag{4.6}
\]

For tangent fields, (4.1) has principal part

\[
 h^2\,v^T\operatorname{sym}\nabla u\,v.             \tag{4.7}
\]

Because all edges of one two-layer macrostar have a positive floor, the
fourth-order frozen elasticity symbol vanishes only on infinitesimal rigid
motions and obeys

\[
 {\cal E}_x(\xi,U)
 \ge c_{\rm K}\,|\xi|^2|U|^2
 \quad
 (U\perp\text{ frozen rotations}),                 \tag{4.8}
\]

where \(c_{\rm K}>0\) is the minimum of a polynomial on the compact set
\(|\xi|=|U|=1\).  The minimum is certified in the same rational interval
compiler as (2.6).

Fourier inversion of the frozen operator, summation by parts in dyadic
annuli, and (4.8) give the local estimate

\[
 \|T_y^*u\|_{\infty,Q/2}
 \le C_{\rm fr}\left(
      h^{-n}\|K_hu\|_{\infty,Q}
      +\|u\|_{\infty,Q}
 \right).                                          \tag{4.9}
\]

The coefficient-freezing error is bounded by
\(C_{\rm osc}\operatorname{diam}(Q)\) times the left side.  Choose the fixed
atlas boxes so that this number is at most \(1/4\).  A finite partition of
unity and reflected collar extension give the global version of (4.9).
If the remaining \(\|u\|_\infty\) term could not be removed, a normalized
countersequence would have a uniformly convergent, piecewise \(H^1\) limit
with zero continuous symmetric gradient.  The collar consistency identifies
the limit across every macroface.  The Yano identity

\[
 2\int_{S^n}|\operatorname{sym}\nabla u|^2
 =
 \int_{S^n}\left(
  |\nabla u|^2+|\operatorname{div}u|^2
  -(n-1)|u|^2
 \right)                                           \tag{4.10}
\]

then makes the limit a Killing field.  Orthogonality to the sampled rotations
passes to the limit, a contradiction.  Quantitatively, diagonalizing
\(\operatorname{sym}\nabla^*\operatorname{sym}\nabla\) in vector spherical
harmonics gives an explicit first positive eigenvalue
\(c_{\rm Korn}=c_{\rm Korn}(n)>0\) after the rotation modes are removed.
The conformal gradient fields in \(n=2\) have nonzero symmetric gradient and
therefore cause no extra elasticity kernel.  Keeping the finite constants in
the preceding absorption yields (4.5), for example

\[
 C_{\rm el}
 =8N_{\rm ov}C_{\rm fr}
   \left(1+C_{\rm osc}+c_{\rm Korn}^{-1}\right),     \tag{4.11}
\]

where all three constants are outputs of the finite compiler.

This proof also explains the scaling \(h^{-n}\): a nodal load represents a
force density after division by a cell volume of order \(h^n\).  No graph
diameter, spectral gap, or overlap factor is hidden; they are contained
explicitly in \(C_{\rm el}\), \(c_{\rm Korn}\), and \(N_{\rm ov}\).

### 4.3 Exact shared correction

Set

\[
 b=T_y\gamma^0,
 \qquad
 u=K_h^\dagger b,
 \qquad
 z=-\Gamma^0T_y^*u,
 \qquad
 \gamma=\gamma^0+z.                                \tag{4.12}
\]

Then, exactly,

\[
 T_y\gamma=b-K_hK_h^\dagger b=0.                   \tag{4.13}
\]

Equations (3.5) and (4.5) give

\[
 \frac{|z_e|}{\gamma_e^0}
 \le \zeta h^2,
 \qquad
 \zeta=C_{\rm el}b_0.                              \tag{4.14}
\]

Choose

\[
 h\le h_{\rm pos}:=(2\zeta)^{-1/2}.                \tag{4.15}
\]

Then every active conductance remains strictly positive and

\[
 \frac12g_-h^{n-2}
 \le\gamma_e\le
 \frac32g_+h^{n-2}.                                \tag{4.16}
\]

The correction changes the quadratic moment by at most

\[
 \sum_j|z_{ij}|
 \left\|
  \Delta_{ij}\Delta_{ij}^T-\frac{2\ell_{ij}}nP_i
 \right\|_F
 \le
 \zeta D_0g_+\Lambda_0^2
       \left(1+\frac1{\sqrt n}\right)h^{n+2}.        \tag{4.17}
\]

Consequently

\[
 \|\widehat M_i(\gamma,y)\|_F
 \le m_*h^{n+2},                                    \tag{4.18}
\]

where

\[
 m_*
 =m_0+\zeta D_0g_+\Lambda_0^2
          \left(1+\frac1{\sqrt n}\right).           \tag{4.19}
\]

Equations (4.13)--(4.19) prove simultaneously the strict local feasibility
margin \(g_-/2\), the strict global feasibility margin \(C_{\rm el}^{-1}\),
positivity after correction, and exact global reversibility.  In particular,
no local-row solution has been symmetrized after the fact.

## 5. Generator, rate, sampling quotient, and optimal order

Use the corrected stress \(\gamma\) from (4.12), the reference nodes
\(X_h=Y_h\), and the mass normalization (1.4).  Equations (1.5)--(1.7) prove
exactly

\[
 L_h1=0,
 \qquad
 L_h\Omega=-n\Omega,
 \qquad
 w_i a_{ij}=w_ja_{ji}=\gamma_{ij}/W.                \tag{5.1}
\]

All active conductances are positive by (4.16).

### 5.1 Rate and weight bounds

The elementary chord inequalities

\[
 \frac{2\theta^2}{\pi^2}\le1-\cos\theta
 \le\frac{\theta^2}{2}
 \qquad(0\le\theta\le\pi)                           \tag{5.2}
\]

and (2.8) give

\[
 r_i
 =n\frac{\sum_j\gamma_{ij}}
          {\sum_j\gamma_{ij}\ell_{ij}}
 \le\frac{n\pi^2}{2q_0^2}h^{-2}.                   \tag{5.3}
\]

Thus one may take

\[
 \boxed{R_d=\frac{n\pi^2}{2q_0^2}.}                \tag{5.4}
\]

From (4.16), (2.8), and the degree bound,

\[
 \mu_i\ge\mu_-h^n,
 \qquad
 \mu_-=\frac{g_-q_0^2}{n\pi^2},                    \tag{5.5}
\]

\[
 \mu_i\le\mu_+h^n,
 \qquad
 \mu_+=\frac{3D_0g_+\Lambda_0^2}{4n}.              \tag{5.6}
\]

Since \(|X_h|\le N_+h^{-n}\),

\[
 w_i\ge\omega_-h^n,
 \qquad
 \boxed{
 \omega_-=
 \frac{4g_-q_0^2}
 {3\pi^2N_+D_0g_+\Lambda_0^2}.
 }                                                   \tag{5.7}
\]

These inequalities also give the requested uniform mesh ratio, degree,
angular-window, local-cone, and mass-quality bounds.

### 5.2 Uniform sampling quotient

Let \(A\in\operatorname{Sym}_0(d)\), \(\|A\|_F=1\).  Some unit eigenvector
\(u\) obeys \(|u^TAu|\ge d^{-1/2}\), and
\(x\mapsto x^TAx\) is \(2\)-Lipschitz on the sphere.  For \(h\le1/8\), the
\(h\)-balls centered at nodes in \(B(u,1/4)\) cover \(B(u,1/8)\).
Cap-volume comparison and (5.7) therefore give

\[
 \|S_2A\|_w^2\ge\alpha_d\|A\|_F^2                 \tag{5.8}
\]

with the explicit constant

\[
 \boxed{
 \alpha_d=
 \frac{\omega_-}{4d}
 \left(\frac2\pi\right)^{d-2}8^{-n}.
 }                                                   \tag{5.9}
\]

The same argument, restricted to \(K_X^{\perp_F}\), is valid even before
eventual injectivity.  In fact fill distance alone implies \(K_X=0\) once
\(h<1/(2\sqrt d)\), but no such identification is used below.

### 5.3 Quadratic upper bound

Equations (1.9), (4.18), and (5.5) yield

\[
 \max_i\|M_i\|_F\le C_Mh^2,                         \tag{5.10}
\]

where

\[
 \boxed{
 C_M=
 \frac{n\pi^2}{g_-q_0^2}
 \left[
  m_0+
  C_{\rm el}b_0D_0g_+\Lambda_0^2
  \left(1+\frac1{\sqrt n}\right)
 \right].
 }                                                   \tag{5.11}
\]

For every coefficient \(A\),

\[
 \|R_2A\|_w^2
 =\sum_iw_i\langle M_i,A\rangle_F^2
 \le C_M^2h^4\|A\|_F^2.                             \tag{5.12}
\]

Combining (5.8) and (5.12) on the sampled quotient gives

\[
 \boxed{
 \mathfrak D_2(L_h)\le C_dh^2,
 \qquad
 C_d=\frac{C_M}{\sqrt{\alpha_d}}.
 }                                                   \tag{5.13}
\]

This is a Hilbert-space quotient estimate; it neither assumes a nonsingular
raw generalized pencil nor compresses \(L+2dI\) to a range that has not been
proved invariant.

### 5.4 Matching lower theorem

Let \({\cal G}_h(R_d)\) be the class of positive reversible generators on
\(X_h\), with the declared local support convention, exact \(H_0/H_1\)
reproduction, and \(r_{\max}\le R_dh^{-2}\).  P1B gives for every member

\[
 \mathfrak D_2
 \ge\frac{dn}{r_{\max}}
 \ge\frac{dn}{R_d}h^2.                              \tag{5.14}
\]

The constructed generator belongs to the class.  Hence

\[
 \boxed{
 c_dh^2
 \le
 \inf_{L\in{\cal G}_h(R_d)}\mathfrak D_2(L)
 \le
 C_dh^2,
 \qquad
 c_d=\frac{dn}{R_d}=\frac{2dq_0^2}{\pi^2}.
 }                                                   \tag{5.15}
\]

The order is therefore exactly optimal.

## 6. Rejected-route conditional perturbation calculation — not an active P1E result

The rejected route contained two conditional perturbation calculations. They
are retained only to distinguish smooth mesh perturbations from arbitrary
high-frequency jitter and must not be cited as robustness theorems.

### 6.1 Exact fixed-node correction

Let \(x_i'\in S^{d-1}\) satisfy

\[
 \max_i\|x_i'-y_i\|\le\rho h^4.                     \tag{6.1}
\]

Keep the same graph and baseline edge coefficients.  Then every edge increment
changes by at most \(2\rho h^4\), so

\[
 \|T_{x'}\gamma^0-T_y\gamma^0\|_\infty
 \le C_{\rm node}\rho h^{n+2},                     \tag{6.2}
\]

and every bracket in (1.8) changes by at most
\(C_{\rm quad}\rho h^4\).  The rigidity and frozen-symbol constants change
continuously; if

\[
 C_{\rm geom}\rho h^3\le
 \frac12\min\{q_0,g_-,c_{\rm K}\},                  \tag{6.3}
\]

the corrected stress

\[
 \gamma'
 =\gamma^0-\Gamma^0T_{x'}^*
   (T_{x'}\Gamma^0T_{x'}^*)^\dagger
   T_{x'}\gamma^0                                  \tag{6.4}
\]

is exact on the perturbed nodes, remains positive, and satisfies (4.18) with

\[
 m_*\quad\hbox{replaced by}\quad
 m_*+
 C_{\rm el}C_{\rm node}\rho+
 C_{\rm quad}\rho.                                  \tag{6.5}
\]

Thus arbitrary labeled jitter of size \(O(h^4)\) preserves the theorem after
reconciliation.

### 6.2 Smooth larger perturbations

For a tangent perturbation field \(\xi_i\), define the discrete scaled norm

\[
 \|\xi\|_{2,\infty,h}
 =
 \max_i\|\xi_i\|
 +\max_{ij}\frac{\|\xi_j-\xi_i\|}{h}
 +\max_{i,j,k}
   \frac{\|\xi_j-2\xi_i+\xi_k\|}{h^2},              \tag{6.6}
\]

where the last maximum runs over opposite directions in a reflected collar
star.  If

\[
 \|\xi\|_{2,\infty,h}\le\rho h^2,                  \tag{6.7}
\]

then the same proof gives (6.2)--(6.5), with constants linear in \(\rho\).
This allows physical displacement \(O(h^2)\) when its first and second
discrete derivatives have the correct smooth scaling.

The dependence on the global elasticity constant is real.  Without a
discrete \(C^2\) bound, an \(O(h^3)\) perturbation can create a load whose
low-frequency stress correction accumulates along \(O(h^{-1})\) paths.
The path and alternating-gap fixtures in Section 7 show why neither the
global inverse margin nor the perturbation scale may be suppressed.

## 7. Independent routes and exact failure certificates

The search retained independent mechanisms until each had either a proof or a
concrete obstruction.  The structured-stress construction above is Route 2.
Route 5 gives an independent convex-dual derivation of the same correction:
(4.12) is the unique minimizer of

\[
 \min_z\frac12\sum_e\frac{z_e^2}{\gamma_e^0}
 \quad\text{subject to}\quad
 T_yz=-T_y\gamma^0.                                 \tag{7.1}
\]

Its dual Hessian is \(K_h\), and (4.5) is an analytic uniform Slater/Korn
certificate, not finite LP evidence.

| route | status | audited conclusion |
|---|---|---|
| spherical Delaunay / Izmestiev--Lam | BLOCKED_FOR_UPPER_ORDER | exact positive reversible \(H_1\) on \(S^2\), but ordinary Delaunay quality does not control the mixed and tangent-anisotropy blocks |
| positive approximate Laplacian plus exact shared correction | COMPLETE | Sections 2--6 |
| local tight-frame stencil plus reversible reconciliation | ALGEBRA_COMPLETE / GENERIC_ASSEMBLY_REJECTED | the three moment equations imply \(B_i=0\), but local row feasibility alone fails the cycle test |
| symmetry orbit / icosahedral refinement | REJECTED_AS_GENERAL_ROUTE | finite \(SO(3)\) orbits do not become dense; generic refinement stabilizers do not force tangent isotropy |
| convex program with analytic feasibility | COMPLETE | (7.1), with dual estimate (4.5) |
| perturbation from exact equality microstructure | BLOCKED_IN_D_GE_3 | rank-one circle stencils have a tensor floor and globally exact equilateral refinements are Platonic |

### 7.1 Izmestiev--Lam convention and tensor obstruction

On \(S^2\), write the Izmestiev--Lam coefficient as \(c_{ij}\) and

\[
 \mu_i^{\rm IL}=\sum_jc_{ij}\sin^2(\lambda_{ij}/2).
\]

Their identity is

\[
 \sum_jc_{ij}(\Omega_j-\Omega_i)
 =-2\mu_i^{\rm IL}\Omega_i.                         \tag{7.2}
\]

Thus \(w_i=\mu_i^{\rm IL}/\sum\mu^{\rm IL}\) and
\(\gamma_{ij}=c_{ij}/\sum\mu^{\rm IL}\) have exactly the AFP sign and mass
normalization.  Strict spherical Delaunay gives \(c_{ij}>0\).

For tangent unit directions \(v_{ij}\), however,

\[
 T_i=(\mu_i^{\rm IL})^{-1}
      \sum_jc_{ij}\sin^2\lambda_{ij}\,v_{ij}v_{ij}^T,
\]

\[
 H_i=(\mu_i^{\rm IL})^{-1}
      \sum_jc_{ij}(1-\cos\lambda_{ij})
                    \sin\lambda_{ij}\,v_{ij},
\]

and exactly

\[
 \|B_i\|_F^2
 =2\|H_i\|^2+
  \left\|T_i-\left(2-\frac{\epsilon_i}{2}\right)P_i
  \right\|_F^2.                                     \tag{7.3}
\]

The positive tangent star

\[
 (1,0),\quad(0,1),\quad(-1,-1)
\]

with Euclidean cotangent-limit weights \(2,2,2\) has limiting covariance

\[
 \begin{pmatrix}2&1\\1&2\end{pmatrix}
\]

and \(\|B_i\|_F\to\sqrt2\), despite bounded degree, strict positivity,
shape regularity, and a tangent-frame lower bound.  Thus Route 1 cannot
supply (0.1) from ordinary mesh quality.

The often used mutation
\(\pi-\)(sum of opposite spherical angles) is not the
Izmestiev--Lam margin.  Four nodes on the small circle \(z=1/2\),

\[
 (\sqrt3/2,0,1/2),\ (0,\sqrt3/2,1/2),\
 (-\sqrt3/2,0,1/2),\ (0,-\sqrt3/2,1/2),
\]

give \(c_{ij}=0\) on a diagonal although the two opposite spherical angles
sum to more than \(\pi\).

### 7.2 Local rows do not imply reversibility

On the nonantipodal octahedral graph, give the positive-axis rows the paired
rates

\[
 (c_{1,2},c_{1,3})=(9/10,1/10),\quad
 (c_{2,1},c_{2,3})=(4/5,1/5),\quad
 (c_{3,1},c_{3,2})=(7/10,3/10).
\]

Every row is positive and reproduces \(H_1\).  Reversibility around the
positive triangle would require equality of the forward and reverse products,
but their ratio is

\[
 \frac{(9/10)(1/5)(7/10)}
      {(4/5)(3/10)(1/10)}
 =\frac{21}{4}.                                     \tag{7.4}
\]

This is an exact Kolmogorov-cycle certificate against rowwise
symmetrization.

### 7.3 Positive filters cannot repair first-order anisotropy

If \(P=I+\tau L\) is Markov, \(\phi(P)=\sum_{k=0}^Kq_kP^k\) with
\(q_k\ge0\), and the transformed generator is normalized to reproduce
\(H_1\), then the inherited residual appears with coefficient

\[
 A_\phi=
 \frac{n\tau\sum_kq_kk}{1-\phi(1-n\tau)}
 \ge1.                                               \tag{7.5}
\]

The newly introduced scalar term is \(O(\tau)=O(h^2)\), but a bounded-hop
positive filter has \(\phi'(\beta)>0\) and cannot cancel an inherited
\(O(h)\) tensor term.  Signed Richardson coefficients lose positivity.

### 7.4 Symmetry and microstructure blockers

In \(d\ge3\), a local great-circle cycle has rank-one tangent covariance and

\[
 \|B_i\|_F^2=(2-\ell)^2(d-1)(d-2).                  \tag{7.6}
\]

P1B then gives

\[
 \mathfrak D_2^2
 \ge d(d-2)(2-\ell)^2+d^2\ell^2,                   \tag{7.7}
\]

an \(O(1)\) floor.  A reversible exact-\(H_1\) connected component also has
\(\sum_{i\in C}w_i\Omega_i=0\), so a bounded-size component cannot lie in a
shrinking cap.  Finally, a convex triangulated exact-frontier refinement has
one common chord, hence equilateral faces; tangent closure and Euler reduce it
to the three Platonic triangular cases.  These facts reject copied local
equality microstructures as an asymptotic construction.

### 7.5 Strong versus weak consistency

Even a positive symmetric energy with second-order **variational**
consistency need not have the pointwise tensor estimate (3.5).  On \(S^1\)
take alternating gaps

\[
 \alpha=s(1+\rho),\qquad
 \beta=s(1-\rho),\qquad 0<\rho<1,
\]

and shared conductance \(1/\sin(\text{gap})\).  The identity embedding is an
exact constrained critical point and the energy has midpoint
\(O(s^2)\) consistency.  Nevertheless, on the quadratic complex mode,

\[
 \mathfrak D_2=\sqrt{A^2+B^2},
\]

\[
 A=4\left[1-\cos(\rho s)\cos(\alpha/2)\cos(\beta/2)\right],
\qquad
 B=-4\cos(\alpha/2)\cos(\beta/2)\sin(\rho s),
\]

so

\[
 \mathfrak D_2/s\longrightarrow4\rho.              \tag{7.8}
\]

This fixture is why Section 3 proves a pointwise coordinate-and-quadratic
Taylor formula at every collar node.

## 8. Closed-form \(S^1\) specialization

For \(d=2\), there is a sharper equality family.  Let \(N\ge5\),
\(h=\pi/N\), take the regular \(N\)-gon with uniform mass, use cycle edges,
and set

\[
 a_{k,k\pm1}=\frac1{4\sin^2h},
\qquad
 \gamma_{k,k\pm1}=\frac1{4N\sin^2h}.                \tag{8.1}
\]

Then

\[
 \operatorname{fill}=\operatorname{sep}=h,
\qquad
 \deg=2,
\qquad
 \theta_{\rm edge}=2h,
\]

\[
 L1=0,\qquad L\Omega=-\Omega,
\qquad
 r=\frac1{2\sin^2h},                                \tag{8.2}
\]

and every sampled trace-free quadratic is the order-two Fourier mode:

\[
 R_2=4\sin^2h\,S_2,
\qquad
 \mathfrak D_2=4\sin^2h,
\qquad
 \mathfrak D_2r=2.                                  \tag{8.3}
\]

This exact family is retained as a symbolic and Lean regression, not as a
substitute for the all-dimensional construction.

## 9. Prior-art boundary

Izmestiev--Lam supply (7.2) and the spherical Delaunay sign convention on
\(S^2\), not the pointwise tensor estimate or the all-dimensional atlas
stress.  Seibold supplies local positive-stencil cone language, not shared
global conductances.  García Trillos--Gerlach--Hein--Slepčev address
asymptotic spectral convergence of random geometric graph Laplacians, not
exact finite \(H_1\) correction or the sampled quotient.  Ahrens--Beylkin
supply invariant quadrature constructions, not a bounded-degree local
generator.  The finite atlas compiler, global elasticity correction,
sampling quotient, and matching theorem above are proved internally.

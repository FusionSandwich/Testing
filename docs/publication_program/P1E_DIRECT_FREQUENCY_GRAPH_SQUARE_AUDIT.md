# Direct-frequency icosphere graph-square moment stress

## Verdict

**FINITE ALGEBRA COMPLETE; ALL-LEVEL POSITIVITY LEMMA OPEN.**

The frequency-\(N\) radial icosphere and the square of its triangular graph
give a particularly clean \(d=3\) candidate. Full icosahedral orbit reduction
shows a strictly positive shared stress satisfying all three local moment
equations through every tested frequency, now including \(N=48\). The
max-min edge margin decreases slowly but remains \(0.4883\) at \(N=48\).

This computation is not an all-level proof. The missing statement is isolated
exactly in Conjecture 4.1 below. If that statement is proved with any fixed
positive lower and finite upper bounds, the formulas in Sections 1--3 give a
complete \(d=3\) P1E family with explicit geometry, rate, and defect constants.
No additional global reversible reconciliation or harmonic correction is
needed.

## 1. Exact family and geometry

Let \(A,B,C\) be the vertices of one face of a regular unit icosahedron.
Adjacent vertices satisfy

\[
 A\cdot B=B\cdot C=C\cdot A=c,\qquad c=\frac1{\sqrt5}.
\]

For every integer \(N\ge1\), put on each face the barycentric nodes

\[
 y_{ijk}=\frac{iA+jB+kC}{N},\qquad i,j,k\ge0,\quad i+j+k=N,
\]

and radially project

\[
 x_{ijk}=\frac{y_{ijk}}{\|y_{ijk}\|}.
\]

The face grids agree on common edges. After identification, the resulting
node set \(X_N\subset S^2\) has

\[
 |X_N|=10N^2+2,\qquad |F_N|=20N^2,\qquad |E_N|=30N^2.           \tag{1.1}
\]

Let \(G_N\) be this triangular graph and let \(G_N^{[2]}\) contain every
distinct pair at graph distance one or two. Its degree is at most

\[
 D=6+6\cdot5=36.                                                \tag{1.2}
\]

Direct counting also gives

\[
 |E(G_N^{[2]})|=90N^2-30.                                      \tag{1.2a}
\]

Set

\[
 r_0=\sqrt{\frac{1+2/\sqrt5}{3}},\qquad
 L=\sqrt{2(1-1/\sqrt5)},\qquad h=N^{-1}.                        \tag{1.3}
\]

Every face-plane barycenter has norm \(r_0\), and every face-grid edge has
Euclidean length \(L/N\). Radial projection on a face has differential norm
at most \(r_0^{-1}\). Its inverse has differential norm at most
\(1+r_0^{-1}\). Unfolding across icosahedral edges therefore gives the
explicit mesh estimates

\[
 \operatorname{fill}(X_N)\le Hh,\qquad
 H=\frac{L}{\sqrt3\,r_0},                                      \tag{1.4}
\]

\[
 \operatorname{sep}(X_N)\ge qh,\qquad
 q=\frac{r_0L}{1+r_0},                                         \tag{1.5}
\]

and every graph-square edge has angular length at most

\[
 \theta_{ij}\le\Lambda h,\qquad \Lambda=\frac{2L}{r_0}.         \tag{1.6}
\]

For (1.5), use the intrinsic equilateral triangulation of the polyhedral
surface: distinct grid nodes have intrinsic separation at least \(L/N\).
The inverse radial map on each crossed face has Lipschitz constant at most
\(1+r_0^{-1}\). The same piecewise estimate holds after unfolding across a
macroedge.

## 2. Exact shared moment system

At \(x_i\), write

\[
 P_i=I-x_ix_i^T,\qquad
 \tau_{ij}=P_ix_j,\qquad
 \ell_{ij}=1-x_i\cdot x_j,
\]

and, on the two-dimensional tangent plane,

\[
 Q_i(v)=vv^T-\frac{\|v\|^2}{2}P_i.
\]

Seek one shared edge array
\(\gamma_{ij}=\gamma_{ji}>0\) on \(G_N^{[2]}\) satisfying, at every node,

\[
 \sum_j\gamma_{ij}\tau_{ij}=0,                                 \tag{2.1}
\]

\[
 \sum_j\gamma_{ij}\ell_{ij}\tau_{ij}=0,                        \tag{2.2}
\]

\[
 \sum_j\gamma_{ij}Q_i(\tau_{ij})=0.                            \tag{2.3}
\]

These are six real homogeneous equations per vertex. They are imposed on
shared undirected variables from the outset; no rowwise-to-reversible
inference occurs.

Define

\[
 \mu_i=\frac12\sum_j\gamma_{ij}\ell_{ij},\qquad
 W=\sum_i\mu_i,\qquad
 w_i=\frac{\mu_i}{W},\qquad
 a_{ij}=\frac{\gamma_{ij}}{\mu_i}.                              \tag{2.4}
\]

Equation (2.1) and radial contraction give exactly

\[
 \sum_j\gamma_{ij}(x_j-x_i)=-2\mu_ix_i.
\]

Thus

\[
 L1=0,\qquad Lx=-2x,                                           \tag{2.5}
\]

and positivity, reversibility, and exact \(H_0,H_1\) reproduction are
automatic.

Equations (2.2)--(2.3) imply

\[
 B_i=0,\qquad M_i=\frac32\epsilon_iZ_i,\qquad
 Z_i=x_ix_i^T-\frac13I.                                       \tag{2.6}
\]

Consequently \(R_2\) acts pointwise on sampled quadratics:

\[
 (R_2A)_i=\frac32\epsilon_i(S_2A)_i.                           \tag{2.7}
\]

This identity is already valid on the genuine sampled quotient, including
aliases. Since

\[
 \epsilon_i=\sum_ja_{ij}\ell_{ij}^2
 \le \ell_{\max}\sum_ja_{ij}\ell_{ij}
 =2\ell_{\max},
\]

\[
 \mathfrak D_2\le3\ell_{\max}
 \le\frac32\Lambda^2h^2.                                      \tag{2.8}
\]

No separate sampling lower bound is needed for (2.8).

The first moment in (2.4), (1.5), and
\(1-\cos t\ge2t^2/\pi^2\) give

\[
 r_i
 =\frac{\sum_j\gamma_{ij}}{\mu_i}
 \le\frac{\pi^2}{q^2}h^{-2}.                                  \tag{2.9}
\]

Thus one may take

\[
 R_3=\frac{\pi^2}{q^2},\qquad
 C_3=\frac32\Lambda^2.                                        \tag{2.10}
\]

## 3. Weight bounds from a uniform stress margin

Suppose, after one harmless common scaling,

\[
 0<g_-\le\gamma_{ij}\le g_+<\infty                             \tag{3.1}
\]

for all graph-square edges and all \(N\). Then

\[
 \frac{g_-q^2}{\pi^2}h^2
 \le\mu_i
 \le\frac{Dg_+\Lambda^2}{4}h^2.                               \tag{3.2}
\]

Using \(|X_N|\le12h^{-2}\),

\[
 W\le3Dg_+\Lambda^2,\qquad
 w_i\ge
 \omega_-h^2,\qquad
 \omega_-=\frac{g_-q^2}{3\pi^2Dg_+\Lambda^2}.                  \tag{3.3}
\]

Together with (1.4), the elementary cap argument gives injective quadratic
sampling once

\[
 Hh\le\frac1{8\sqrt3},
\]

with, for example,

\[
 \|S_2A\|_w^2\ge
 \alpha_3\|A\|_F^2,\qquad
 \alpha_3=
 \frac{\omega_-}{12}\frac2\pi(8\sqrt3H)^{-2}
 =\frac{\omega_-}{1152\pi H^2}.                                \tag{3.4}
\]

Equation (2.7), rather than (3.4), remains the sharper way to prove the
operator bound.

## 4. The exact remaining all-level statement

Let \(\mathcal A_N\) be the real matrix of (2.1)--(2.3), using any orthonormal
tangent basis at each vertex and one column per undirected graph-square edge.

### Conjecture 4.1 (uniform graph-square moment stress)

There are absolute constants \(N_0\), \(g_->0\), and \(g_+<\infty\) such that
for every \(N\ge N_0\) there is an icosahedrally invariant vector
\(\gamma^{(N)}\) with

\[
 \mathcal A_N\gamma^{(N)}=0,\qquad
 g_-\le\gamma_e^{(N)}\le g_+                                  \tag{4.1}
\]

on every edge of \(G_N^{[2]}\).

This is exactly the unproved lemma. It is stronger than local row
feasibility but substantially more concrete than P1E: its graph, nodes,
matrix entries, symmetry reduction, and desired uniform box are all explicit.
Proving it by a fixed active-set recursion, a barycentric closed formula, or a
uniform Gordan alternative would complete the \(d=3\) construction through
Sections 1--3.

## 5. Orbit reduction and computational evidence

The full icosahedral group \(I_h\), of order \(120\), acts on nodes and
graph-square edges. Averaging preserves (2.1)--(2.3) and positivity, so the
search may use one variable per edge orbit. The implementation maximizes the
minimum edge weight subject to mean edge weight one.

| \(N\) | nodes | graph-square edges | edge orbits | max-min margin |
|---:|---:|---:|---:|---:|
| 2 | 42 | 330 | 6 | 0.932203390 |
| 4 | 162 | 1,410 | 18 | 0.830175418 |
| 8 | 642 | 5,730 | 60 | 0.677922270 |
| 16 | 2,562 | 23,010 | 216 | 0.585642471 |
| 24 | 5,762 | 51,810 | 468 | 0.541892072 |
| 32 | 10,242 | 92,130 | 816 | 0.518175717 |
| 40 | 16,002 | 143,970 | 1,260 | 0.501167811 |
| 48 | 23,042 | 207,330 | 1,800 | 0.488301399 |

The residuals of the displayed floating-point solutions are between
\(10^{-15}\) and \(5\cdot10^{-14}\). This is strong conjecture evidence but
is not an interval certificate and is not used as an all-level proof.

The orbit nullity grows quadratically with \(N\), and the max-min active set
also changes with \(N\). Therefore the numerical optimizer itself is not a
closed-form construction. A fit of the displayed margins is likewise not a
proof of a positive limiting margin.

## 6. Useful exact projective factorization

Inside one macroface, write \(x_q=y_q/r_q\), where \(y_q\) is the affine
triangular lattice and \(r_q=\|y_q\|\). If

\[
 \gamma_{pq}=r_pr_q\,c_{pq},                                   \tag{6.1}
\]

then

\[
 \sum_q\gamma_{pq}P_{x_p}x_q
 =r_pP_{x_p}\sum_qc_{pq}(y_q-y_p).                             \tag{6.2}
\]

Thus spherical tangent equilibrium is exactly the radial transform of a
shared flat equilibrium stress. For an opposite pair
\(y_{p\pm v}=y_p\pm s_v\),

\[
 \tau_{p,p\pm v}
 =\pm\frac{P_{x_p}s_v}{r_{p\pm v}}.                            \tag{6.3}
\]

If \(c_{p,p+v}=c_{p,p-v}\), the pair cancels the first moment exactly.
Equations (6.1)--(6.3) reduce the bulk construction to a flat shared stress
problem. They also expose the seam issue: after crossing a macroedge, the
radial chart has an along-edge shear, so constant opposite-pair coefficients
are no longer shared in one smooth lattice coordinate. Graph-square
cross-seam edges are the finite connectors that the LP uses to repair this
shear.

This factorization is the most promising route to an all-level proof:
construct a positive flat equilibrium stress in each reflected macroface,
derive an explicit one-dimensional connector along every macroedge, and use
the fivefold stabilizer at the twelve macrovertices. What remains is to prove
that these formulas simultaneously satisfy (2.2)--(2.3) with a uniform
positive margin.

## 7. Exact warning against overpromotion

The direct-frequency nearest-neighbor polar/Izmestiev--Lam stress is positive
and exact on \(H_1\), but its maximum full quadratic tensor defect is only
first order. Numerically,

\[
 N\max_i\|M_i\|_F\longrightarrow 0.41\ldots,
\]

while the mass-weighted root-mean-square defect has the expected seam scaling
near \(N^{-3/2}\). Thus nearest-neighbor exactness does not prove (2.8).
The graph-square moment equations, or an equally strong seam repair, are
essential.

Accordingly, finite feasibility through \(N=48\) must remain evidence for
Conjecture 4.1, not a substitute for its proof.

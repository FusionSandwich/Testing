# P1E cubed-sphere route audit

This note audits the most literal cubed-sphere construction.  It supplies an
explicit quasiuniform node family, proves that the cube corners themselves
have the correct tight-frame geometry in every dimension, and gives an exact
all-dimensional obstruction to using only the natural axial cube-grid graph.
The obstruction is global: pointwise positive tight-frame rows exist on a
macroface, but shared conductances force binomial growth along that face.

The conclusion is deliberately narrow.  It does not reject a cubical atlas
with cross-interface collar edges.  It proves that those extra edges (or an
equivalent global stress reconciliation) are necessary.

## 1. The literal cubed-sphere nodes

Let

\[
 \mathcal Q_N=
 \left\{y\in[-1,1]^d:
   \|y\|_\infty=1,
   \ y_a\in-1+\frac2N\{0,\ldots,N\}
 \right\},
 \qquad
 X_N=\left\{\frac y{|y|}:y\in\mathcal Q_N\right\}.
 \tag{1.1}
\]

Put \(h=N^{-1}\).  For \(x\in S^{d-1}\), the point
\(y=x/\|x\|_\infty\) lies on the cube boundary.  Keep one coordinate of
absolute value one fixed and round the other coordinates to the nearest
multiple of \(2/N\).  If \(y_N\) is the result, then

\[
 |y-y_N|\le \frac{\sqrt{d-1}}N.
\]

Normalization on \(\{|y|\ge1\}\) is two-Lipschitz, and chordal distance is
at least \(2\theta/\pi\) for angular distance \(\theta\in[0,\pi]\).  Hence

\[
 \operatorname{fill}(X_N)
 \le \frac{\pi\sqrt{d-1}}N.                       \tag{1.2}
\]

Conversely, the inverse radial map

\[
 G(x)=\frac{x}{\|x\|_\infty},\qquad x\in S^{d-1},
\]

is \((d+\sqrt d)\)-Lipschitz, because
\(\|x\|_\infty\ge d^{-1/2}\).  Distinct cube-grid points are separated by
at least \(2/N\), so distinct nodes obey

\[
 |\Omega_i-\Omega_j|
 \ge \frac{2}{(d+\sqrt d)N}.                      \tag{1.3}
\]

Thus the literal cubed-sphere nodes are an explicit quasiuniform family.
Any fixed cube-grid hop set has bounded degree and an angular window
\([q_dh,\Lambda_dh]\).  The problem below is not mesh quality.

## 2. Exact tangent geometry on a cube macroface

Consider the intersection of the two positive cube faces.  A macroface node
before radial projection has the form

\[
 y=(1,1,z),qquad z\in(-1,1)^m,qquad m=d-2,
 \qquad S^2=|y|^2=2+|z|^2.                         \tag{2.1}
\]

Let \(P=I-yy^T/S^2\), and suppress the common derivative factor \(S^{-1}\)
until the covariance calculation.  Define

\[
 c_\alpha=P e_{\alpha+2}\quad(1\le\alpha\le m),
 \qquad
 q=\frac{e_1-e_2}{2},                             \tag{2.2}
\]

and let the two inward cube-face increments be

\[
 a=P(-e_2),\qquad b=P(-e_1).                       \tag{2.3}
\]

Writing \(C\xi=\sum_\alpha\xi_\alpha c_\alpha\), one has exactly

\[
 a=q+\frac12Cz,qquad
 b=-q+\frac12Cz,qquad
 q\perp\operatorname{im}C,qquad |q|^2=\frac12.   \tag{2.4}
\]

The Gram matrix of the seam directions and its inverse are

\[
 G=C^TC=I-\frac{zz^T}{S^2},
 \qquad
 G^{-1}=I+\frac12zz^T.                            \tag{2.5}
\]

These identities follow from \(Py=0\); in particular
\(a+b=Cz\).  They are valid in every dimension.

## 3. The unique locally isotropic natural row

Use only the natural axial graph at this macroface node: one inward edge into
each incident cube face, with conductances \(u_A,u_B>0\), and the two seam
directions \(\pm c_\alpha\), with conductances
\(k_{\alpha,+},k_{\alpha,-}>0\).

Tangent equilibrium first forces

\[
 u_A=u_B=:u,                                      \tag{3.1}
\]

by taking the \(q\)-component.  Its seam components then give

\[
 k_{\alpha,+}-k_{\alpha,-}=-uz_\alpha.           \tag{3.2}
\]

Suppose in addition that the leading tangent covariance is isotropic.  All
actual first-order spherical increments in (2.2)--(2.3) have the common
factor \(S^{-1}\).  By (2.4), the cross-normal eigenvalue of the covariance
is therefore \(u/S^2\).  On the seam tangent space, isotropy is equivalent to

\[
 C\operatorname{diag}
   (k_{\alpha,+}+k_{\alpha,-})C^T
 +\frac u2(Cz)(Cz)^T
 =uP_{\operatorname{im}C}.                        \tag{3.3}
\]

Because

\[
 P_{\operatorname{im}C}=CG^{-1}C^T
\]

and \(G^{-1}-zz^T/2=I\), equation (3.3) is equivalent to

\[
 k_{\alpha,+}+k_{\alpha,-}=u.                    \tag{3.4}
\]

Combining (3.2) and (3.4) proves uniqueness:

\[
 \boxed{
 k_{\alpha,+}=\frac u2(1-z_\alpha),
 \qquad
 k_{\alpha,-}=\frac u2(1+z_\alpha).
 }
 \tag{3.5}
\]

Thus every individual interior macroface row has a positive tight-frame
solution.  Local row feasibility is not the issue.

## 4. Sharedness forces binomial growth

Put

\[
 z_{\alpha,k}=-1+\frac{2k}N,qquad 0\le k\le N.
 \tag{4.1}
\]

Let \(u_k\) denote the common inward conductance at a seam node with this
coordinate, holding the other coordinates fixed.  The edge from \(k\) to
\(k+1\) is the plus edge at \(k\) and the minus edge at \(k+1\).  Sharedness
and (3.5) therefore imply

\[
 \frac{u_{k+1}}{u_k}
 =\frac{1-z_{\alpha,k}}{1+z_{\alpha,k+1}}
 =\frac{N-k}{k+1}.                                \tag{4.2}
\]

Consequently

\[
 \boxed{u_k=u_0{N\choose k}.}                     \tag{4.3}
\]

In a macroface of dimension \(m=d-2\), path independence of (4.2) gives

\[
 \boxed{
 u_{k_1,\ldots,k_m}
 =u_{0,\ldots,0}\prod_{\alpha=1}^m{N\choose k_\alpha}.
 }
 \tag{4.4}
\]

Already in \(d=3\), the ratio between a central and an endpoint inward
conductance is

\[
 {N\choose\lfloor N/2\rfloor}
 \ge \frac{2^N}{N+1}.                             \tag{4.5}
\]

It is therefore impossible to have constants \(g_-,g_+>0\), independent of
\(N\), for which all the natural-edge conductances have the same required
scale and satisfy

\[
 g_-h^{d-3}\le\gamma_e\le g_+h^{d-3}.             \tag{4.6}
\]

At the endpoints one coefficient in (3.5) also vanishes.  The failure is
not repaired by a special corner row: (4.5) is accumulated along the whole
macroface.

This proves an exact local-to-global obstruction.  The pointwise tangent
equations and pointwise tight-frame equations are compatible, but they are
not compatible with shared conductances having a uniform interior margin on
the natural cube-grid graph.

### 4.1 The obstruction is stable at the required order

The same conclusion holds if tightness is required only to relative order
\(O(h^2)\), as it is in P1E.  Fix a closed interior slab of the macroface,
for example

\[
 -a\le z_1\le0,
 \qquad |z_\beta|\le a\quad(\beta>1),
 \qquad 0<a<1.                                    \tag{4.7}
\]

On this slab, the singular values of \(C\) and all conductance-to-moment
linear maps in (3.3) have bounds depending only on \(a,d\).  Exact tangent
equilibrium still gives \(u_A=u_B=u\) and (3.2).  If the tangent covariance
differs from a scalar by at most \(Ch^2u/S^2\), then (3.3)--(3.4) give

\[
 k_{\alpha,+}+k_{\alpha,-}
 =u(1+\eta_{\alpha}),
 \qquad
 |\eta_\alpha|\le C_{a,d}Ch^2.                   \tag{4.8}
\]

Sharedness along the first coordinate therefore yields

\[
 \frac{u_{k+1}}{u_k}
 =\frac{1-z_k+\eta_k}{1+z_{k+1}+\eta'_{k+1}}.    \tag{4.9}
\]

The denominators on (4.7) are bounded away from zero.  Taking logarithms
shows that the total perturbation of the logarithm over \(O(N)\) steps is
only \(O(Nh^2)=O(h)\).  The unperturbed logarithmic growth, however, is

\[
 \frac N2\int_{-a}^0
 \log\frac{1-t}{1+t}\,dt+O(1)=c_aN+O(1),
 \qquad c_a>0.                                    \tag{4.10}
\]

Thus the conductance ratio still grows like \(\exp(c_aN+O(1))\).
Uniform positive upper and lower margins are incompatible even with the
precise \(O(h^2)\) moment accuracy requested in P1E.  This rules out using a
small error in place of the missing cross-interface mechanism.

## 5. Cube corners are not the local obstruction

At a signed cube corner put

\[
 y=(\sigma_1,\ldots,\sigma_d),qquad
 \Omega=y/\sqrt d,
 \qquad
 a_j=P_\Omega(-\sigma_je_j).                      \tag{5.1}
\]

Then

\[
 \sum_{j=1}^d a_j=0,
 \qquad
 |a_j|^2=\frac{d-1}{d},
 \qquad
 a_j\cdot a_k=-\frac1d\quad(j\ne k),             \tag{5.2}
\]

and

\[
 \boxed{\sum_{j=1}^d a_ja_j^T=P_\Omega.}          \tag{5.3}
\]

Thus the \(d\) inward corner rays are a regular-simplex tight frame in the
\((d-1)\)-dimensional tangent space.  Equal positive corner conductances
kill the tangent force and give exact leading isotropy.  Special corner
templates are useful, but corner symmetry alone cannot undo the seam
recurrence (4.2).

## 6. What a successful cubical construction must add

The calculation identifies the missing mechanism precisely.  A successful
cubical route must include at least one of the following.

1. **A common reflected collar.**  Replace the two truncated face lattices
   near a macroface by one lattice in a smooth chart crossing the macroface.
   Then the normal directions occur in genuine midpoint pairs, rather than
   being related by the sheared identity \(a+b=Cz\).
2. **Cross-interface directions.**  Add bounded-hop edges from one face to
   shifted layers of the other.  Their direction cone must contain both the
   first moment and the isotropic second moment with a uniform positive
   margin.  The edge values must still pass the sharedness cycle tests.
3. **A global stress projection.**  Start from a uniformly positive
   midpoint stencil on a single compatible collar mesh and project its small
   tangent defect onto shared stresses using a uniform discrete
   elasticity/Korn right inverse.  Local cone feasibility alone is not a
   substitute for that inverse.

For \(S^2\), a planar gnomonic chart also has the continuum Airy tensor

\[
 Q(u)=\operatorname{cof}D^2\sqrt{1+|u|^2}
     =(1+|u|^2)^{-3/2}(I+uu^T),                   \tag{6.1}
\]

which is positive and divergence free.  A discrete Maxwell--Cremona/Airy
stress gives exact shared equilibrium inside one planar chart.  It does not
by itself glue the boundary tractions of independently truncated cube-face
charts.  Formula (4.3) is an exact certificate against treating that gluing
as automatic.

Accordingly, the literal cubed-sphere/natural-graph route is classified

```text
explicit quasiuniform nodes:                         COMPLETE
all-dimensional corner tight frame:                  COMPLETE
pointwise natural seam tight frame:                  COMPLETE
uniform shared natural-edge assembly:                REJECTED
reflected-collar or cross-interface repair:           REQUIRED
Airy stress on one S^2 gnomonic chart:                COMPLETE LOCALLY
global Airy/collar reconciliation without an inverse: BLOCKED
```

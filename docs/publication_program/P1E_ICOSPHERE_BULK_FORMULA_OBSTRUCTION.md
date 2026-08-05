# Icosphere bulk-formula obstruction

## Verdict

**EXACT NEGATIVE RESULT FOR TRANSLATION-INVARIANT PROJECTIVE STRESSES.**

The radial frequency icosphere cannot satisfy the tangent trace-free second
moment by taking one translation-invariant flat stress in each macroface and
repairing only a fixed-width neighborhood of the macroedges.  The same
obstruction applies after multiplication by a scalar midpoint field or by
slowly varying scalar endpoint factors.  Directional weights must vary
anisotropically through the two-dimensional bulk of every macroface.

This result does not rule out the full graph-square moment cone.  It rules
out the most direct proposed closed formula and explains why the numerical
positive stresses have nonconstant bulk orbit weights.

## 1. Setting

Let a macroface lie in

\[
 H=\{y\in\mathbb R^3:n\cdot y=r_0\},\qquad |n|=1,\quad r_0>0,
\]

and put $U=n^\perp$.  Radial projection is

\[
 F(y)=x=\frac{y}{|y|}.
\]

Fix a finite symmetric displacement set
$\mathcal V=-\mathcal V\subset U$ spanning $U$.  For the square of the
triangular lattice, $\mathcal V$ consists of the six nearest, the six
collinear two-step, and the six diagonal two-step displacements.  Their
different lengths may have different coefficients.

Consider frequency meshes with $h=N^{-1}$, and suppose that away from a
fixed number of lattice layers at the macroedges the conductance has the
projectively factored form

\[
 \gamma^{(N)}_{y,y+hv}
 =|y|\,|y+hv|\,b_N(y+hv/2)c_v^{(N)},              \tag{1.1}
\]

where

\[
 c_{-v}^{(N)}=c_v^{(N)},\qquad
 0<c_-\le c_v^{(N)}\le c_+<\infty,               \tag{1.2}
\]

and $b_N$ are positive scalar fields which are uniformly bounded above and
below and equicontinuous on compact subsets of the face interior.  The case
$b_N\equiv1$ is a constant flat stress.  A product
$b_N((p+q)/2)=s_N(p)s_N(q)$ with a uniformly positive equicontinuous scalar
node factor is included after taking its midpoint limit.

## 2. Nonexistence theorem

### Theorem 2.1 (bulk scalar-factor obstruction)

No sequence of conductances of the form (1.1)--(1.2) can satisfy

\[
 \sum_{q}\gamma^{(N)}_{yq}
 \left(
   \tau_{yq}\tau_{yq}^{T}
   -\frac{|\tau_{yq}|^2}{2}P_{F(y)}
 \right)=0                                             \tag{2.1}
\]

at every graph-square row in the interior of a macroface for all sufficiently
large $N$.  Consequently a correction supported in only a fixed-width
macroedge collar cannot make (2.1) exact.

#### Proof

Write $r=|y|$, $r_v=|y+hv|$, $x=F(y)$, and
$P_x=I-xx^T$.  Exactly, not just asymptotically,

\[
 \tau_{y,y+hv}=P_xF(y+hv)=\frac{h}{r_v}P_xv.          \tag{2.2}
\]

Substitution of (1.1) and (2.2) into (2.1), followed by division by
$h^2r$, gives

\[
 \sum_{v\in\mathcal V}
  \frac{b_N(y+hv/2)c_v^{(N)}}{r_v}
  Q_x(P_xv)=0,                                        \tag{2.3}
\]

where

\[
 Q_x(z)=zz^T-\frac{|z|^2}{2}P_x.
\]

On any infinite sequence of frequencies, choose interior mesh nodes
converging to the face barycenter $y_0=r_0n$.  Compactness of the finite
coefficient box and equicontinuity of $b_N$ give, after a subsequence,

\[
 c_v^{(N)}\longrightarrow c_v>0,
 \qquad b_N\longrightarrow b>0
\]

at the finitely many points used below.  Passing to the limit in (2.3) at
$y_0$ yields

\[
 \operatorname{tf}_{U} C=0,
 \qquad C:=\sum_{v\in\mathcal V}c_vvv^T.             \tag{2.4}
\]

Thus $C=\kappa P_U$ on $U$.  Since the positive displacements span $U$,
$\kappa>0$.

Now choose orthonormal $e_1,e_2\in U$ and a fixed nonzero $t$ small
enough that

\[
 y_t=r_0n+te_1
\]

lies in the macroface interior.  Choose mesh nodes converging to $y_t$ on
the same subsequence.  Put

\[
 r_t=\sqrt{r_0^2+t^2},\qquad
 z_t=\frac{r_0e_1-tn}{r_t}.
\]

Then $e_2,z_t$ are an orthonormal basis of $T_{F(y_t)}S^2$.  The limiting
quadratic tensor in (2.3), apart from the positive scalar $b(y_t)/r_t$, has
the two eigenvalues

\[
 e_2^TCe_2=\kappa,
 \qquad
 z_t^TCz_t=\kappa\frac{r_0^2}{r_0^2+t^2}.            \tag{2.5}
\]

They are unequal because $t\ne0$.  Equivalently, its trace-free Frobenius
norm is exactly

\[
 \frac{\kappa t^2}{\sqrt2\,(r_0^2+t^2)}>0.            \tag{2.6}
\]

This contradicts the limit of (2.3).  The selected nodes remain a fixed
positive distance from every macroedge, so changing a fixed number of edge
layers cannot affect the contradiction.  \(\square\)

## 3. Consequences for formula searches

The theorem rejects all of the following proposed shortcuts:

1. $\gamma_{pq}=r_pr_qc_v$ with one constant per intrinsic hop type;
2. a scalar radial, barycentric, or midpoint modulation of those constants;
3. scalar endpoint/path-product modulation
   $\gamma_{pq}=r_pr_qs_ps_qc_v$ with a smooth positive $s$;
4. a translation-invariant macroface stress followed by a connector confined
   to $O(1)$ lattice layers at each icosahedral seam.

The obstruction is the nonconformality of radial projection away from the
face barycenter.  In face coordinates its pullback metric has a preferred
radial direction.  Scalar modulation changes the size of a fixed covariance
tensor but cannot rotate or anisotropically reshape it.  Therefore any
successful exact formula needs at least a two-component directional tensor
field across every macroface, together with a genuinely shared-edge
reconciliation of that field.

The full orbit LP is not contradicted: its direction weights vary over
two-dimensional barycentric orbit types, precisely the freedom retained by
the theorem.

## 4. Symbolic regression

The exact matrix calculation in (2.5)--(2.6), including the regular
icosahedral face value

\[
 r_0^2=\frac{1+2/\sqrt5}{3},
\]

is checked by

```text
python afp_barrier_gate1/pure_math/covariance/p1e_icosphere_bulk_formula_obstruction_audit.py
```

The script is a symbolic regression for the proved obstruction.  It is not a
finite substitute for Theorem 2.1 and supplies no evidence for all-level LP
feasibility.

## 5. The forced continuum bulk tensor

The obstruction also identifies the anisotropic target that a viable formula
must discretize.  Write $y=r_0n+u$, $u\in U$, and
$r^2=r_0^2+|u|^2$.  Suppose more generally that a smooth midpoint rule has

\[
 \gamma_{y,y+hv}=r\,r_v\,c_v(u+hv/2),
 \qquad c_{-v}=c_v>0,
\]

and define its oriented second-moment tensor

\[
 C(u)=\sum_{v\in\mathcal V}c_v(u)vv^T.
\]

The leading part of the exact tangent equilibrium is

\[
 \operatorname{div}C=0.                                      \tag{5.1}
\]

Indeed the projective factorization cancels the endpoint radii, and pairing
$v,-v$ in the flat equilibrium equation gives (5.1) after division by
$h$.  The leading trace-free quadratic equation says that
$P_xC(u)P_x$ is scalar on $T_xS^2$.  Since

\[
 (P_x|_U)^T(P_x|_U)=I_U-\frac{uu^T}{r^2},
\]

this is equivalent to

\[
 C(u)=\lambda(u)
 \left(I_U+\frac{uu^T}{r_0^2}\right).                         \tag{5.2}
\]

Equations (5.1)--(5.2) determine the scalar.  Direct differentiation gives

\[
 0=\nabla\lambda+
 \frac{u(u\cdot\nabla\lambda)}{r_0^2}
 +\frac{3\lambda u}{r_0^2}.                                  \tag{5.3}
\]

The component perpendicular to $u$ makes $\lambda$ radial, and the radial
component integrates to

\[
 \boxed{
 C(u)=K r^{-3}
 \left(I_U+\frac{uu^T}{r_0^2}\right),\qquad K>0.}              \tag{5.4}
\]

Thus the continuum bulk target is unique up to scale.  It is the
curl--curl/Airy tensor of the convex function
$u\mapsto K|r_0n+u|/r_0^2$.  Its eigenvalue ratio is

\[
 \frac{r^2}{r_0^2}\le\frac1{r_0^2}
 =\frac{3}{1+2/\sqrt5}<2.                                    \tag{5.5}
\]

on an icosahedral face, so it lies uniformly inside the positive
graph-square directional cone.  More explicitly, its normalized anisotropy
is at most

\[
 \rho_{\rm bulk}
 =\frac{r_0^{-2}-1}{r_0^{-2}+1}
 =\frac{\sqrt5-1}{2\sqrt5+1},
\]

whereas the six-line graph-square cone has inradius $\sqrt3/2$ in
trace-free coordinates.  Hence its exact interior margin obeys

\[
 \eta_{\rm bulk}
 =\frac{\sqrt3}{2}-\frac{\sqrt5-1}{2\sqrt5+1}
 >\frac12.                                                   \tag{5.6}
\]

For example, the hexagonal mean-value decomposition gives every one of its
six line coefficients the lower bound

\[
 \beta_v\ge
 \frac{\eta_{\rm bulk}}{6\sqrt3}\operatorname{tr}C.           \tag{5.7}
\]

Formula (5.4) is therefore a constructive
target, but not an exact shared discrete stress: the mixed loss--tangent
equation and all finite-difference remainders still have to be reconciled.
It shows precisely why a scalar modulation of one fixed direction tensor
cannot work and why a position-dependent discrete Airy mechanism is the
appropriate remaining analytic route.

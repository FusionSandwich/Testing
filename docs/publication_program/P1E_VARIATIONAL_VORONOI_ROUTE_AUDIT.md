# P1E variational/Voronoi route audit

## Status: BLOCKED as an all-dimensional P1E construction

This note records the strongest unconditional statement supplied by the
centroidal-Voronoi variational route.  A spherical centroidal Voronoi
tessellation gives a positive shared generator and reproduces the coordinate
eigenspace exactly.  Quasiuniformity then gives locality, bounded degree, and
the correct rate scale.  The same Euler--Lagrange equation does **not** give
the second-moment isotropy needed for an \(O(h^2)\) quadratic residual.  An
exact periodic centroidal Voronoi example below has a scale-independent
quadratic error.  Thus an appeal to centroidality, even with uniform
separation, fill, degree, and positive face margins, cannot close P1E.

The obstruction is to this proof mechanism, not a nonexistence theorem for
other positive shared constructions.

## 1. What spherical centroidality proves exactly

Put \(n=d-1\).  Let \(x_i\in S^n\), and let

\[
 V_i=\{x\in S^n:x\cdot x_i\ge x\cdot x_j\text{ for every }j\}
\]

be its spherical Voronoi cell.  Write \(F_{ij}=V_i\cap V_j\), omit null
faces, and put

\[
 q_{ij}=|x_i-x_j|,\qquad
 m_i=\int_{V_i}x\,d\sigma(x),\qquad
 c_{ij}=\frac{|F_{ij}|}{q_{ij}}=c_{ji}>0.       \tag{1.1}
\]

On \(F_{ij}\), the outward unit conormal of \(V_i\) is the constant vector

\[
 \nu_{ij}=\frac{x_j-x_i}{q_{ij}};
\]

it is tangent because \(x\cdot(x_j-x_i)=0\) on the bisector.  Applying the
spherical divergence theorem componentwise to the inclusion
\(x:S^n\hookrightarrow\mathbb R^{n+1}\), for which
\(\Delta_{S^n}x=-nx\), gives the exact finite identity

\[
 \sum_jc_{ij}(x_j-x_i)=-n m_i.                  \tag{1.2}
\]

Suppose the cells are centroidal in the extrinsic spherical sense

\[
             m_i=\mu_i x_i,\qquad \mu_i=|m_i|>0. \tag{1.3}
\]

Set \(Z=\sum_i\mu_i\), \(w_i=\mu_i/Z\), and
\(\gamma_{ij}=c_{ij}/Z\).  Then

\[
 a_{ij}=\frac{\gamma_{ij}}{w_i}=\frac{c_{ij}}{\mu_i}
\]

is positive and reversible and (1.2) says, without an asymptotic error,

\[
 L1=0,\qquad Lx=-nx.                             \tag{1.4}
\]

This is also the Euler equation for the usual spherical quantization
functional: moving \(x_i\) tangentially differentiates the cell contribution
to a multiple of \(P_{x_i}m_i\).  Thus (1.3), and no second-moment equation,
is the local information obtained from stationarity.

### Mesh consequences, conditional only on explicit mesh constants

Assume angular fill at most \(Hh\), angular separation at least \(qh\), and
\(Hh\le1\).  Every Delaunay neighbor is at angular distance at most \(2Hh\).
The disjoint caps of angular radius \(qh/2\) about those neighbors lie in a
cap of radius \((2H+q/2)h\).  Hence the degree is bounded by the explicit
packing ratio

(Here \(\omega_k\) denotes the \(k\)-dimensional area of the unit
\(k\)-sphere.)

\[
 D_{n,H,q}:=
 \frac{\sigma_n(B_{S^n}((2H+q/2)h))}
      {\sigma_n(B_{S^n}(qh/2))}
 \le
 \frac{\omega_{n-1}(2H+q/2)^n/n}
      {\omega_{n-1}(2/\pi)^{n-1}(q/2)^n/n},      \tag{1.5}
\]

where \(\sin t\le t\) is used above and
\(\sin t\ge2t/\pi\) below.  Each cell contains the cap of radius \(qh/2\)
and is contained in the cap of radius \(Hh\).  Therefore

\[
 \mu_i\ge \cos(Hh)\,
 \frac{\omega_{n-1}}n(2/\pi)^{n-1}(qh/2)^n.     \tag{1.6}
\]

For \(n\ge2\), also \(q_{ij}\ge(2/\pi)qh\), and every face has measure at most the
\((n-1)\)-ball bound
\(\omega_{n-2}(2Hh)^{n-1}/(n-1)\) (with the evident \(n=1\)
interpretation).  Thus (1.5)--(1.6) give an explicit

\[
 r_i=\frac1{\mu_i}\sum_j\frac{|F_{ij}|}{q_{ij}}
 \le R(n,H,q)h^{-2}.                             \tag{1.7}
\]

For example, throughout \(Hh\le1\), one may take

\[
\begin{split}
 D(n,H,q)&=\left(\frac\pi2\right)^{n-1}
           \left(\frac{4H+q}{q}\right)^n,\\
 C_\mu(n,H,q)&=\cos(1)\frac{\omega_{n-1}}n
        \left(\frac2\pi\right)^{n-1}\left(\frac q2\right)^n,\\
 R(n,H,q)&=
 \frac{D(n,H,q)}{C_\mu(n,H,q)}
 \frac{\omega_{n-2}}{n-1}(2H)^{n-1}\frac{\pi}{2q}.
                                                               \tag{1.8}
\end{split}
\]

The \(n=1\) case is the elementary two-face circle calculation.  Consequently
rate scaling is not the missing part of this route.

## 2. The missing face-centering identity

For a trace-free symmetric \(A\), put \(Q_A(x)=x^TAx\).  Since
\(\Delta_{S^n}Q_A=-2(n+1)Q_A\), integration over \(V_i\) gives

\[
 \sum_j\frac{2}{q_{ij}}(x_j-x_i)^TA
       \int_{F_{ij}}x\,dS
 =-2(n+1)\int_{V_i}Q_A(x)\,d\sigma.              \tag{2.1}
\]

The graph flux instead uses

\[
 c_{ij}(Q_A(x_j)-Q_A(x_i))
 =\frac1{q_{ij}}(x_j-x_i)^TA
       |F_{ij}|(x_i+x_j).                         \tag{2.2}
\]

Subtracting (2.1) from (2.2) exhibits the independent face error

\[
 E_i(A)=\sum_j\frac1{q_{ij}}(x_j-x_i)^TA
 \left[|F_{ij}|(x_i+x_j)-2\int_{F_{ij}}x\,dS\right]. \tag{2.3}
\]

Centroidality cancels the cell first moment.  It places no condition on the
bracket in (2.3).  On an \(h\)-cell, the bracket is generically
\(O(h|F_{ij}|)=O(h^n)\); the factor
\((x_j-x_i)/q_{ij}\) is a unit vector.  Thus (2.3), divided by the
\(O(h^n)\) cell mass, can be \(O(1)\).  An \(O(h^2)\) P1E residual requires
a further reflected-face or third-moment cancellation with a quantitative
margin.

The issue is already exact in flat space, where curvature and sampling
aliases are absent.

## 3. Exact periodic centroidal counterexample

Consider the affine reflection group generated by the three lines

\[
 x=-1,\qquad y=-1,\qquad x+y=1,                  \tag{3.1}
\]

and the orbit of the origin.  Its Dirichlet cell at the origin is the right
isosceles triangle

\[
 T=\operatorname{conv}\{(-1,-1),(2,-1),(-1,2)\}. \tag{3.2}
\]

Indeed the three adjacent orbit points are

\[
 \delta_1=(-2,0),\qquad \delta_2=(0,-2),\qquad
 \delta_3=(1,1),                                  \tag{3.3}
\]

and their perpendicular-bisector inequalities are exactly (3.2).  The
reflection chambers tile the plane, so the orbit is periodic.  Each chamber
is the reflected copy of \(T\), and its generating orbit point is its
centroid.  The tessellation is therefore centroidal, uniformly separated,
uniformly covering, degree three, and has strictly positive congruent faces
at every scale.

The area is \(|T|=9/2\).  The finite-volume conductances
\(c_e=|F_e|/|\delta_e|\) are

\[
 c_1=c_2=\frac32,\qquad c_3=3.                   \tag{3.4}
\]

They satisfy exact force balance

\[
 \sum_{k=1}^3c_k\delta_k=0.                      \tag{3.5}
\]

But their second moment is

\[
 \sum_{k=1}^3c_k\delta_k\delta_k^T
 =\begin{pmatrix}9&3\\3&9\end{pmatrix}
 \ne 2|T|I.                                      \tag{3.6}
\]

For \(Q(x,y)=xy\), the normalized graph Laplacian at the origin is exactly

\[
 \frac1{|T|}\sum_kc_k Q(\delta_k)=\frac23,
 \qquad \Delta Q=0.                              \tag{3.7}
\]

After scaling the entire tessellation by \(h\), the masses scale as \(h^2\),
the edge vectors as \(h\), and the conductances in two dimensions do not
scale.  The value \(2/3\) in (3.7) is unchanged for every \(h\).  Thus even
a periodic, congruent, nondegenerate centroidal Voronoi equilibrium can have
a quadratic residual bounded away from zero.

This example is deterministic and involves neither a seam nor a small
conductance.  It proves that no argument using only centroidality plus the
usual mesh-quality hypotheses can imply the P1E estimate.

It also blocks a bare radial-energy minimization argument.  The two edge
lengths are \(\sqrt2\) and \(2\), and (3.4) depends only on the edge length.
Put \(s=\sqrt2\), \(t=(r-s)/(2-s)\), and let

\[
\begin{split}
h_{00}(t)&=2t^3-3t^2+1,&h_{10}(t)&=t^3-2t^2+t,\\
h_{01}(t)&=-2t^3+3t^2,&h_{11}(t)&=t^3-t^2.
\end{split}
\]

The explicit cubic

\[
 g(r)=3s\,h_{00}(t)+10(2-s)h_{10}(t)
      +3h_{01}(t)+10(2-s)h_{11}(t)               \tag{3.8}
\]

has the Hermite data

\[
\begin{array}{c|cc}
 r&\Phi'(r)&\Phi''(r)\\ \hline
 \sqrt2&3\sqrt2&10\\
 2&3&10.
\end{array}                                                    \tag{3.9}
\]

Its Bernstein coefficients on \(0\le t\le1\) are

\[
 3\sqrt2,\qquad \frac{20-\sqrt2}{3},\qquad
 \frac{-11+10\sqrt2}{3},\qquad 3,
\]

so \(g(r)>0\) throughout \(\sqrt2\le r\le2\).
Take \(\Phi'(r)=g(r)\) on an open interval containing both active radii,
and extend it smoothly elsewhere.  On the fixed local reflection-adjacency
graph, \(\Phi'(r)/r\) is exactly the conductance in (3.4), so (3.5) is the
first-variation equation of the local symmetric radial pair energy.  If one
instead wants the distance window to define the graph, the first nonneighbor
distance is \(2\sqrt2\): choose \(R\in(2,2\sqrt2)\) and use a further
endpoint-flat Hermite piece making \(\Phi\) constant for \(r\ge R\).
Moreover, for an edge vector \(z\), \(r=|z|\), and a relative displacement
\(u\), its Hessian contribution is

\[
 \Phi''(r)(u\cdot z/r)^2+
 \frac{\Phi'(r)}r\left(|u|^2-(u\cdot z/r)^2\right).             \tag{3.10}
\]

Both coefficients are strictly positive at both active radii.  On any
sufficiently large periodic quotient, the active graph is connected, so the
sum of (3.10) is positive definite modulo the common translation.  The orbit
is consequently a strict local radial-energy minimizer modulo translations,
with an open edge-window and conductance margin, while (3.6)--(3.7) remain
unchanged.

## 4. Why global minimization does not presently repair the proof

A global minimizer of spherical quantization is stronger than an arbitrary
centroidal critical point, and standard exchange arguments can be used to
seek separation and covering bounds.  They still provide no displayed
identity controlling (2.3).  To extract \(O(h^2)\) from global minimality one
would need a quantitative local crystallization statement: apart from a set
whose weighted size is small enough for the **squared** sampled residual,
every cell and every face must approach a reflected, second-moment-isotropic
model at a rate sufficient to make (2.3) \(O(h^{n+2})\) per row.  Energy
asymptotics or weak empirical-measure convergence do not imply this.

In addition, on a sphere topological defect cells cannot simply be omitted.
An \(O(1)\) residual on \(O(1)\) cells has weighted norm \(O(h^{n/2})\), which
already exceeds \(O(h^2)\) when \(n<4\).  No all-dimensional quantitative
crystallization theorem with the required defect, face-moment, and explicit
constant control is part of the centroidal Euler equation.

There is a separate robustness gap.  Perturbing the nodes destroys (1.3),
so recomputing Voronoi faces preserves shared positivity but changes the
right side of (1.2) from a multiple of \(x_i\) to \(m_i\).  Restoring exact
coordinate reproduction by an implicit-function argument requires a
uniform inverse for the centroidal Hessian modulo rotations and a uniform
positive face margin.  Neither follows from fill, separation, mesh ratio, or
bounded degree; sliver faces can have arbitrarily small measure in dimensions
\(n\ge2\).

## 5. Consequence for the construction search

The variational/Voronoi route supplies a useful exact \(H_1\) lemma and an
explicit \(r=O(h^{-2})\) estimate once quasiuniformity is independently
known.  It does not supply the requested \(\mathfrak D_2=O(h^2)\) theorem or
robustness.  Reopening this route requires one of the following genuinely new
inputs:

1. an explicit all-level centroidal family with a proved reflected-face
   moment identity and controlled spherical defects;
2. a new energy whose Euler equations include both (1.3) and the trace-free
   second-moment equations, together with a positive shared realization and
   a uniform Hessian inverse; or
3. a quantitative all-dimensional crystallization theorem strong enough to
   bound (2.3) in the sampled \(L^2\) quotient with explicit constants.

Absent one of these inputs, invoking minimization merely moves the P1E
compatibility lemma into an unproved crystallization or nondegeneracy claim.

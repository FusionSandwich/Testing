# Sharp product-graph barriers, constrained extremals, and cone anisotropy

## 0. Scope and notation

This document proves the mandatory Prompt 4 barrier and extremal results. It
uses no AFP terminology in the mathematical statements.

Let a finite positive jump generator be

\[
(Lf)(i)=\sum_{j\ne i}a_{ij}(f(j)-f(i)),\qquad a_{ij}\ge0.
\]

For a unit-sphere embedding \(\Omega_i\in S^2\) satisfying the coordinate
eigenmap equation

\[
\sum_{j\ne i}a_{ij}(\Omega_j-\Omega_i)=-2\Omega_i,
\tag{0.1}
\]

put

\[
\ell_{ij}=1-\Omega_i\cdot\Omega_j,\qquad
r_i=\sum_{j\ne i}a_{ij},\qquad
\varepsilon_i=\sum_{j\ne i}a_{ij}\ell_{ij}^2.
\tag{0.2}
\]

Taking the scalar product of (0.1) with \(\Omega_i\) gives

\[
\sum_j a_{ij}\ell_{ij}=2.
\tag{0.3}
\]

The normalized quality is

\[
Q_i=\frac{r_i\varepsilon_i}{4}.
\tag{0.4}
\]

For the square equal-angle product family, write

\[
h=\frac{\pi}{2N},\qquad M=2N.
\tag{0.5}
\]

The north and south cell-centred rings lie at colatitudes \(h\) and
\(\pi-h\), and the azimuthal spacing is \(2h\).

---

## 1. Exact polar asymptotics with a uniform remainder

The exact polar rate and defect are

\[
r_{\rm pole}(h)
=\frac1{2\sin^2h}+\frac1{2\sin^4h},
\tag{1.1}
\]

\[
\varepsilon_{\rm pole}(h)=2\sin^2h+2\sin^4h.
\tag{1.2}
\]

Consequently

\[
Q_{\rm pole}(h)
=\frac{r_{\rm pole}(h)\varepsilon_{\rm pole}(h)}4
=\frac1{4\sin^2h}+\frac12+\frac{\sin^2h}{4}.
\tag{1.3}
\]

### Lemma 1.1 — controlled cosecant expansion

For every \(0<x\le\pi/4\),

\[
\csc^2x=\frac1{x^2}+\frac13+\frac{x^2}{15}+e(x),
\tag{1.4}
\]

where

\[
0\le e(x)\le\frac{x^4}{80}.
\tag{1.5}
\]

#### Proof

The classical Mittag--Leffler expansion for the cotangent, uniformly on
compact subsets avoiding \(\pi\mathbb Z\), is

\[
\cot x=\frac1x+\sum_{n=1}^{\infty}
\left(\frac1{x-n\pi}+\frac1{x+n\pi}\right).
\]

Termwise differentiation on a compact subinterval of \((-\pi,\pi)\setminus
\{0\}\) gives

\[
\csc^2x=\frac1{x^2}+\sum_{n=1}^{\infty}
\left(\frac1{(n\pi-x)^2}+\frac1{(n\pi+x)^2}\right).
\tag{1.6}
\]

For

\[
t_n=\frac{x^2}{n^2\pi^2},
\]

the paired summand is

\[
\frac{2}{n^2\pi^2}\frac{1+t_n}{(1-t_n)^2}
=\frac{2}{n^2\pi^2}
\sum_{m=0}^{\infty}(2m+1)t_n^m.
\tag{1.7}
\]

The \(m=0,1\) sums are

\[
\frac{2\zeta(2)}{\pi^2}=\frac13,
\qquad
\frac{6\zeta(4)}{\pi^4}=\frac1{15}.
\]

All remaining terms are nonnegative. Moreover,

\[
\sum_{m=2}^{\infty}(2m+1)t^m
=\frac{t^2(5-3t)}{(1-t)^2}.
\tag{1.8}
\]

For \(0\le t\le1/16\), the function

\[
\frac{5-3t}{(1-t)^2}
\]

is increasing and is at most \(1232/225\). Since
\(t_n\le1/(16n^2)\), the tail in (1.7) is at most

\[
\frac{2464}{225}\frac{x^4}{\pi^6}
\sum_{n=1}^{\infty}\frac1{n^6}
=\frac{2464}{225\cdot945}x^4
<\frac{x^4}{80}.
\]

This proves (1.4)--(1.5). \(\square\)

### Theorem 1.2 — polar-rate expansion with an explicit error

For every integer \(N\ge2\),

\[
\boxed{
0\le
r_{\rm pole}(N)
-\left(
\frac{8}{\pi^4}N^4
+\frac{10}{3\pi^2}N^2
+\frac{13}{45}
\right)
\le\frac{\pi^2}{48N^2}.
}
\tag{1.9}
\]

In particular,

\[
\boxed{
r_{\rm pole}(N)
=\frac{8}{\pi^4}N^4
+\frac{10}{3\pi^2}N^2
+\frac{13}{45}
+O(N^{-2}).
}
\tag{1.10}
\]

#### Proof

Let

\[
y=\csc^2x,
\qquad
A=x^{-2}+\frac13+\frac{x^2}{15},
\qquad y=A+e.
\]

Lemma 1.1 gives \(0\le e\le x^4/80\). Direct expansion gives

\[
\frac12(y+y^2)
-\left(\frac1{2x^4}+\frac5{6x^2}+\frac{13}{45}\right)
=\frac{x^2}{18}+\frac{x^4}{450}
+e\left(A+\frac12\right)+\frac{e^2}{2}.
\tag{1.11}
\]

Every term on the right is nonnegative. Since \(x\le\pi/4\) and
\(\pi^2<10\), one has \(x^2\le5/8\). Dividing (1.11) by \(x^2\), using
\(e\le x^4/80\), and then using \(x^2\le5/8\), gives

\[
\frac{\text{right side of (1.11)}}{x^2}
\le
\frac1{18}+\frac1{80}
+\frac{91}{7200}\frac58
+\frac1{1200}\left(\frac58\right)^2
+\frac1{12800}\left(\frac58\right)^3.
\]

The last rational number is

\[
\frac{180013}{2359296}<\frac1{12}.
\]

Thus the remainder is at most \(x^2/12\). Substituting
\(x=\pi/(2N)\) proves (1.9). \(\square\)

### Theorem 1.3 — polar-quality expansion with an explicit error

For every integer \(N\ge2\),

\[
\boxed{
0\le
Q_{\rm pole}(N)
-\left(\frac1{\pi^2}N^2+\frac7{12}\right)
\le\frac{\pi^2}{12N^2}.
}
\tag{1.12}
\]

Consequently,

\[
\boxed{
Q_{\rm pole}(N)
=\frac1{\pi^2}N^2+\frac7{12}+O(N^{-2}).
}
\tag{1.13}
\]

#### Proof

From (1.3) and (1.4),

\[
Q_{\rm pole}(x)-\left(\frac1{4x^2}+\frac7{12}\right)
=\frac{x^2}{60}+\frac{e(x)}4+\frac{\sin^2x}{4}.
\tag{1.14}
\]

The right side is nonnegative. Using \(e(x)\le x^4/80\),
\(\sin^2x\le x^2\), and \(x^2\le5/8\),

\[
\frac{\text{right side of (1.14)}}{x^2}
\le\frac1{60}+\frac14+\frac1{512}
=\frac{2063}{7680}<\frac13.
\]

Substitution of \(x=\pi/(2N)\) gives (1.12). \(\square\)

The exact coefficient extraction in Theorems 1.2--1.3 is Lean-checked. The
Mittag--Leffler tail and rational remainder transfer are also checked by the
exact symbolic audit; the Python series output is a regression, not the proof.

---

## 2. Sharp fixed product-graph obstruction

Let \(\mathcal G_N\) be the unreduced cell-centred latitude--longitude graph
with \(N\) latitude rings and \(M=2N\) vertices on every ring. Each interior
vertex has two same-ring azimuthal neighbors and the adjacent meridional
neighbors. A polar-ring vertex has two azimuthal neighbors and one inward
meridional neighbor.

Let positive masses \(w_i\) and symmetric shared conductances
\(\gamma_{ij}=\gamma_{ji}\ge0\) be supported on \(\mathcal G_N\), and put

\[
a_{ij}=\frac{\gamma_{ij}}{w_i}.
\]

Assume (0.1) at every vertex. No equality of masses, no ring symmetry of the
conductances, and no optimizer symmetry is assumed.

### Theorem 2.1 — the polar row is uniquely forced

At every north-polar-ring vertex, put \(s=\sin h\). If \(a_v\) is the inward
meridional rate and \(a_+,a_-\) are the two azimuthal rates, then

\[
\boxed{
a_v=\frac1{2s^2},
\qquad a_+=a_-=\frac1{4s^4}.
}
\tag{2.1}
\]

Hence every admissible shared-conductance operator satisfies

\[
\boxed{
r_{\max}\ge
\frac1{2\sin^2h}+\frac1{2\sin^4h}.
}
\tag{2.2}
\]

#### Proof

Rotate the chosen polar-ring vertex to longitude zero:

\[
\Omega=(s,0,c),\qquad c=\cos h.
\]

Its two azimuthal neighbors have longitudes \(\pm2h\), and the inward neighbor
has colatitude \(3h\). The transverse coordinate balance gives

\[
s\sin(2h)(a_+-a_-)=0.
\]

For \(N\ge2\), both factors are nonzero, so \(a_+=a_-=:b\).

The axial coordinate receives no contribution from the azimuthal edges. Thus

\[
a_v(\cos3h-\cos h)=-2\cos h.
\]

Using

\[
\cos3h-\cos h=-4\sin^2h\cos h
\]

and \(\cos h>0\), one obtains \(a_v=1/(2s^2)\).

The remaining horizontal coordinate uses

\[
s(\cos2h-1)=-2s^3,
\qquad
\sin3h-\sin h=2s(1-2s^2).
\]

After division by \(s>0\), its balance is

\[
-4bs^2+2a_v(1-2s^2)=-2.
\]

Substitution of \(a_v=1/(2s^2)\) gives \(4bs^4=1\), proving (2.1). This is a
local uniqueness argument, not a symmetrization argument. \(\square\)

### Corollary 2.2 — exact minimax value on the fixed graph class

The existing positive reversible equal-angle construction attains the row in
(2.1), and its maximum rate occurs on the polar rings. Therefore

\[
\boxed{
\inf_{\substack{\text{positive reversible degree-one-exact}\\
\text{operators on }\mathcal G_N}}
 r_{\max}
=
\frac1{2\sin^2(\pi/(2N))}
+\frac1{2\sin^4(\pi/(2N))}.
}
\tag{2.3}
\]

Thus the graph-class obstruction is sharp at every order, and

\[
\boxed{r_{\max}\ge\frac8{\pi^4}N^4.}
\tag{2.4}
\]

The sharp leading constant is \(8/\pi^4\). Reversibility is needed for the
stated graph class and the attaining construction, but not for the local lower
bound itself.

If \(K=NM=2N^2\), then

\[
r_{\max}\ge\frac2{\pi^4}K^2.
\tag{2.5}
\]

Hence the fixed product graph is quadratically stiff in node count.

---

## 3. Universal rate barrier and quasi-uniform comparison

### Theorem 3.1 — universal rate--defect barrier

At every state satisfying (0.3),

\[
\boxed{4\le r_i\varepsilon_i.}
\tag{3.1}
\]

Consequently, if

\[
\varepsilon_i\le Ch^2,
\qquad C>0,
\]

then

\[
\boxed{r_i\ge\frac4{Ch^2}.}
\tag{3.2}
\]

#### Proof

Weighted Cauchy--Schwarz gives

\[
\left(\sum_j a_{ij}\ell_{ij}\right)^2
\le
\left(\sum_j a_{ij}\right)
\left(\sum_j a_{ij}\ell_{ij}^2\right).
\]

Insert (0.3). Division by \(Ch^2>0\) proves (3.2). \(\square\)

This theorem is Lean-checked both in its generator form and in the abstract
rate--defect form.

### Theorem 3.2 — transfer of a quasi-uniform loss window

Suppose every active edge from \(i\) satisfies

\[
Lh^2\le\ell_{ij}\le Uh^2,
\qquad 0<L\le U.
\tag{3.3}
\]

Then

\[
\frac2{Uh^2}\le r_i\le\frac2{Lh^2},
\tag{3.4}
\]

and

\[
2Lh^2\le\varepsilon_i\le2Uh^2.
\tag{3.5}
\]

Indeed, (3.4) follows by comparing the first moment (0.3) with
\(Lh^2r_i\) and \(Uh^2r_i\). For (3.5), multiply (3.3) by
\(a_{ij}\ell_{ij}\) and sum.

With

\[
L=\frac2{\pi^2},\qquad U=2,
\]

one obtains

\[
\boxed{
1\le h^2r_i\le\pi^2,
\qquad
\frac4{\pi^2}h^2\le\varepsilon_i\le4h^2.
}
\tag{3.6}
\]

For a reversible shared-conductance system, the equilibrium equation is

\[
\sum_j\gamma_{ij}(\Omega_j-\Omega_i)=-2w_i\Omega_i.
\]

Dividing by the positive mass \(w_i\) gives (0.1) with
\(a_{ij}=\gamma_{ij}/w_i\). Symmetry of \(\gamma\) is not altered by this
normalization, although the row rates need not be symmetric.

The existence of positive spherical-Delaunay operators, the coordinate
low-mode theorem, and the geometric statement that a maximal separated net
has the required Delaunay angle window are external inputs unless supplied by
a separate geometric proof. No claim is made that one fixed radial icosphere
connectivity is Delaunay at every refinement level.

---

## 4. A nondegenerate constrained extremal problem

For a labeled \(K\)-point set \(X=(x_1,\ldots,x_K)\subset S^2\), let

\[
q_X=\frac12\min_{i\ne j}d(x_i,x_j),
\qquad
h_X=\sup_{y\in S^2}\min_i d(y,x_i).
\]

Fix positive constants

\[
R,d,\rho,\sigma,m_-,m_+.
\]

Let \(\mathcal A_K\) consist of tuples \((X,G,w,\gamma)\) such that:

1. \(x_i\in S^2\), \(q_X\ge\sigma K^{-1/2}\), and
   \(h_X/q_X\le\rho\);
2. \(G\) is a simple graph on the labels, of maximum degree at most \(d\), and
   every edge has geodesic length at most \(2h_X\);
3. \(m_-/K\le w_i\le m_+/K\) and \(\sum_iw_i=1\);
4. \(\gamma_{ij}=\gamma_{ji}\ge0\), supported on \(G\);
5. the shared equilibrium equations hold;
6. with \(a_{ij}=\gamma_{ij}/w_i\), one has \(r_i\le RK\) for every \(i\).

Zero conductances are interpreted by deleting the corresponding edge, so the
class is a finite union over active support graphs. Define

\[
E_K(R,d,\rho,\sigma,m_-,m_+)
=\inf_{\mathcal A_K}\max_i\varepsilon_i,
\tag{4.1}
\]

with value \(+\infty\) when \(\mathcal A_K\) is empty, and

\[
C^*(R,d,\rho,\sigma,m_-,m_+)
=\liminf_{K\to\infty}K E_K.
\tag{4.2}
\]

This controls rate, degree, locality, separation, covering, mesh ratio, masses,
and reversibility. Dense or collapsed degeneracies are excluded.

### Theorem 4.1 — positive lower bound

For every nonempty \(\mathcal A_K\),

\[
\boxed{E_K\ge\frac4{RK}.}
\tag{4.3}
\]

Therefore

\[
\boxed{C^*(R,d,\rho,\sigma,m_-,m_+)\ge\frac4R.}
\tag{4.4}
\]

#### Proof

Theorem 3.1 gives \(4\le r_i\varepsilon_i\). Since
\(r_i\le RK\),

\[
\varepsilon_i\ge\frac4{r_i}\ge\frac4{RK}
\]

for every state. \(\square\)

### Theorem 4.2 — finite-\(K\) existence in the closed class

For fixed \(K\) and fixed parameters, if \(\mathcal A_K\ne\varnothing\), the
infimum in (4.1) is attained.

#### Proof

There are finitely many labeled simple graphs of degree at most \(d\). Fix one
of them. The sphere product \((S^2)^K\) is compact. The separation, covering,
mesh-ratio, and edge-locality constraints are closed because minimum distance
and covering radius are continuous functions of the labeled configuration.
The mass box with \(\sum_iw_i=1\) is compact.

The rate cap gives

\[
0\le\gamma_{ij}\le\sum_j\gamma_{ij}=w_i r_i
\le\frac{m_+}{K}RK=m_+R.
\]

Thus all conductances lie in a fixed compact box. Symmetry, support,
equilibrium, and rate constraints are closed. The feasible subset for the
fixed graph is therefore compact, and \(\max_i\varepsilon_i\) is continuous.
Taking the finite union over graphs preserves compactness. \(\square\)

### Corollary 4.3 — strict product/quasi-uniform separation

For the square product family, \(K=2N^2\) and (2.4) gives

\[
r_{\max}\ge\frac8{\pi^4}N^4.
\]

The linear rate cap \(r_{\max}\le RK=2RN^2\) fails whenever

\[
\boxed{N>\frac{\pi^2}{2}\sqrt R.}
\tag{4.5}
\]

Thus the fixed unreduced product family is eventually absent from every
linear-rate extremal class (4.1). By contrast, any external quasi-uniform
family satisfying the loss window (3.6), with \(K\asymp h^{-2}\), has
\(r_{\max}=O(K)\) and remains compatible with a sufficiently large fixed
\(R\). This is a structural separation, not a fitted numerical slope.

---

## 5. A priori anisotropy over the feasible cone

Fix one spherical node and a finite candidate set \(J\). Write

\[
v_j=P_{T_{\Omega_i}S^2}(\Omega_j-\Omega_i),
\qquad
\ell_j=1-\Omega_i\cdot\Omega_j>0.
\]

For a target normal moment \(\lambda>0\), define the row cone

\[
\mathcal F_i=
\left\{a\in\mathbb R_+^J:
\sum_j a_jv_j=0,
\quad
\sum_j a_j\ell_j=\lambda
\right\}.
\tag{5.1}
\]

The value of \(Q\) is not determined by the node geometry alone: it depends on
which feasible rates are chosen. The correct a priori object is the projective
feasible polytope

\[
\mathcal P_i=
\left\{p\in\mathbb R_+^J:
\sum_jp_j=1,
\quad
\sum_jp_jv_j=0
\right\}.
\tag{5.2}
\]

For \(p\in\mathcal P_i\), put

\[
m(p)=\sum_jp_j\ell_j,
\qquad
s_2(p)=\sum_jp_j\ell_j^2.
\]

Since every \(\ell_j>0\), \(m(p)>0\).

### Theorem 5.1 — exact projective reduction

The maps

\[
p_j=\frac{a_j}{\sum_qa_q}
\]

and

\[
a_j=\frac{\lambda p_j}{m(p)}
\]

are inverse bijections between \(\mathcal F_i\) modulo positive common scaling
and \(\mathcal P_i\). For corresponding points,

\[
\boxed{
Q(a)=\frac{s_2(p)}{m(p)^2}
=1+\frac{\operatorname{Var}_p(\ell)}{m(p)^2}.
}
\tag{5.3}
\]

#### Proof

If \(a\in\mathcal F_i\), let \(r=\sum a_j\) and \(p=a/r\). Tangent balance
and normalization give \(p\in\mathcal P_i\), while
\(m(p)=\lambda/r\). Conversely, the displayed formula for \(a\) gives both
constraints in (5.1). Finally,

\[
r=\frac\lambda m,
\qquad
\sum_ja_j\ell_j^2=\frac\lambda m s_2,
\]

which proves (5.3). \(\square\)

### Theorem 5.2 — sliced LP and exact dual anisotropy constant

The set

\[
I_i=\{m(p):p\in\mathcal P_i\}
\]

is a compact interval. For \(m\in I_i\), define the linear program

\[
\Psi_i(m)=
\min\left\{
\sum_jp_j\ell_j^2:
 p\ge0,
 \sum_jp_j=1,
 \sum_jp_jv_j=0,
 \sum_jp_j\ell_j=m
\right\}.
\tag{5.4}
\]

Then the best geometry-and-cone lower bound is

\[
\boxed{
A_i:=\min_{m\in I_i}
\left(\frac{\Psi_i(m)}{m^2}-1\right)
=
\inf_{a\in\mathcal F_i}(Q(a)-1).
}
\tag{5.5}
\]

Thus every feasible row satisfies the genuinely a priori inequality

\[
\boxed{Q(a)-1\ge A_i,}
\tag{5.6}
\]

which is of the requested form with no remainder loss.

For each fixed \(m\), finite-dimensional LP duality gives

\[
\boxed{
\Psi_i(m)=
\max_{\alpha,\beta,z}
\left\{
\alpha+\beta m:
\alpha+\beta\ell_j+z\cdot v_j\le\ell_j^2
\quad\forall j
\right\}.
}
\tag{5.7}
\]

The signs in (5.7) follow from a minimization primal with nonnegative variables
and equality constraints. Every feasible triple \((\alpha,\beta,z)\) is an
explicit certificate:

\[
Q(a)-1\ge
\frac{\alpha+\beta m-m^2}{m^2}.
\tag{5.8}
\]

This is a rigorous convex reformulation. It never treats \(Q\) as a linear
function of the conductances.

### Corollary 5.3 — equality characterization

\[
A_i=0
\]

if and only if some tangent-balanced probability vector is supported on one
loss level. Equivalently, the feasible cone contains a projective row with
constant active loss. This recovers the local \(Q=1\) equality condition.

### Example 5.4 — sharp two-direction anisotropy

If the only tangent-balanced probability on two opposite directions is
\((1/2,1/2)\), with losses \(\ell_1,\ell_2>0\), then

\[
\boxed{
A_i=\frac{(\ell_1-\ell_2)^2}{(\ell_1+\ell_2)^2}.
}
\tag{5.9}
\]

This identity is Lean-checked.

### Example 5.5 — the polar product cone

The polar tangent equations have a unique projective solution, so the cone
constant equals the actual polar value:

\[
A_{\rm pole}=Q_{\rm pole}-1
=\frac1{4\sin^2h}-\frac12+\frac{\sin^2h}{4}.
\tag{5.10}
\]

Therefore

\[
A_{\rm pole}
=\frac{N^2}{\pi^2}-\frac5{12}+O(N^{-2}).
\]

The quadratic growth is an a priori consequence of the fixed polar tangent
cone and loss levels, not an artifact of the particular solved conductances.

---

## 6. Bounded high-ambition branches

### 6.1 Delsarte/Gegenbauer — blocked for this stage

Positive-definite zonal kernels and spherical-code LPs were tested as possible
sources of a global sampled-quadratic or valence obstruction. No new dual
certificate survived the sampling-kernel audit. The branch produced only a
reduction to standard spherical-code LPs and did not improve Theorems 2.1,
4.1, or 5.2. It is therefore `BLOCKED`, not promoted as a theorem.

### 6.2 Bakry--Émery \(\Gamma_2\) — computed, then killed

With

\[
\Gamma_2(f)=\frac12L\Gamma(f,f)-\Gamma(f,Lf),
\]

an eigenfunction \(Lf=-\lambda f\) satisfies

\[
\Gamma_2(f)=\frac12L\Gamma(f,f)+\lambda\Gamma(f,f).
\tag{6.1}
\]

For a centered resonant square, \(\Gamma(f,f)=\lambda c\) is constant, so

\[
\Gamma_2(f)=\lambda^2c.
\]

This is a useful consistency check but only rewrites the centered-resonance
identity on one function. It supplies no curvature-dimension inequality on
the full function algebra. Known finite graphs have nonnegative or positive
Bakry--Émery curvature, so the blanket collapse claim remains `REJECTED`.
The branch meets its kill criterion and stops here.

### 6.3 Compact homogeneous spaces — deferred

The covariance identity already holds in every Euclidean eigenmap dimension,
and the sphere specialization is complete. No additional compact homogeneous
space produced a stronger central theorem without importing substantial new
representation theory. The optional extension is `DEFERRED`.

### 6.4 Discrete transport metrics — deferred

No continuum \(W_2\) statement is made. Entropy-gradient-flow or contraction
claims require a specified Maas/Erbar-type discrete metric and a separate
curvature proof. This branch is `DEFERRED`.

### 6.5 Reduced-ring graphs — a precise coupling-class impossibility

Consider two adjacent rings with \(M_i\) and \(M_{i+1}\) vertices. If their
inter-ring coupling is biregular with degrees \(p\) and \(q\), incidence
counting gives

\[
pM_i=qM_{i+1}.
\tag{6.2}
\]

In particular, a rotation-equivariant one-to-one meridional coupling is a
perfect matching and forces

\[
\boxed{M_i=M_{i+1}.}
\tag{6.3}
\]

Therefore no varying population rule \(M_i\asymp N\sin\theta_i\) can be
implemented within the nearest-ring perfect-matching coupling class. This
finite obstruction is Lean-checked. More general split/merge couplings are not
settled here and remain numerical-analysis work.

### 6.6 Formal discrete geometry — bounded

Only the finite rate identities, polar uniqueness algebra, coefficient
extraction, universal extremal bound, anisotropy example, and incidence count
are formalized. No general discrete exterior-calculus library is introduced.

---

## 7. Theorem hierarchy and publication boundary

The sharp product-grid result is supporting theory. It is stronger than a
finite regression because it proves the exact graph-class minimax value and a
uniform analytic expansion. It is not the central paper theorem.

The central theorem remains the sampled quadratic exactness and rigidity
package for finite positive eigenmap generators:

\[
E_{\rm sample}
=\operatorname{im}S_X\cap\ker(L+2dI),
\qquad
\dim E_{\rm sample}=\operatorname{rank}S_X-\operatorname{rank}R_X,
\]

with positive axial and positive equivariant rigidity mechanisms, exact alias
classifications, and signed boundary examples.

The local spherical feasibility, global shared-edge compatibility, exact and
quantitative \(Q=1\) rigidity, product-graph obstruction, extremal lower bound,
and cone anisotropy theorem form the supporting hierarchy.

Standard inputs that are not claimed as new include:

- Mittag--Leffler expansions and zeta values;
- Cauchy--Schwarz and weighted variance;
- finite LP strong duality;
- compactness of finite-dimensional closed feasible sets;
- positive-stencil convex geometry;
- spherical Delaunay existence results;
- Euler and convex-polyhedron rigidity; and
- Maas/Erbar discrete transport theory.

The exact symbolic audits are falsification and regression tools. They are not
substitutes for the proofs above.

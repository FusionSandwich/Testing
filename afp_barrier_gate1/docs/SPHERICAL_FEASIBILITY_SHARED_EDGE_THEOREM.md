# Sphere-specific positive feasibility and global shared-edge duality

## Status and scope

This document gives the complete ordinary-mathematics proof for the P0/M1
stage.  It is independent of the frozen transport archive.  It proves the
finite convex-geometric equivalences, the antipodal classification, explicit
robustness constants, and the global reversible shared-edge alternative.  Lean
formalizes the finite algebraic consequences and certificate identities; the
standard finite-dimensional Farkas and strong-duality theorems are invoked in
the exact forms stated below.

Throughout, all index sets are finite.  Repeated candidate directions and
redundant points are allowed and are treated as distinct indexed candidates.

---

## 1. Non-antipodal local rows

Fix a node \(\Omega_i\in S^2\).  For each permitted non-antipodal neighbor
\(j\in N\), write

\[
 \Omega_j=\cos\theta_j\,\Omega_i+\sin\theta_j\,u_j,
 \qquad 0<\theta_j<\pi,
\]

where \(u_j\in T_{\Omega_i}S^2\) is a unit tangent vector.  Put

\[
 s_j=\sin\theta_j>0,\qquad
 \ell_j=1-\cos\theta_j>0,\qquad
 q_j={\ell_j\over s_j}=\tan {\theta_j\over2}>0.
\]

A row \(a=(a_j)_{j\in N}\) is nonnegative degree-one exact with eigenvalue
\(-2\) precisely when

\[
 a_j\ge0,\qquad
 \sum_j a_js_ju_j=0,\qquad
 \sum_j a_j\ell_j=2.                                    \tag{1.1}
\]

Let

\[
 P=\operatorname{conv}\{u_j:j\in N\},\qquad
 \Lambda_0=\left\{\lambda\in\mathbb R^N:
 \lambda\ge0,\ \mathbf1^T\lambda=1,\ \sum_j\lambda_ju_j=0\right\}.
\]

### Lemma 1.1 — finite positive barycentric representations

For any finite indexed family \(x_1,\ldots,x_m\) in a finite-dimensional real
affine space and any \(x\in\operatorname{conv}\{x_j\}\):

1. \(x\) has a nonnegative barycentric representation if and only if it lies
   in the convex hull.
2. \(x\) has a barycentric representation with every indexed coefficient
   strictly positive if and only if
   \(x\in\operatorname{ri}\operatorname{conv}\{x_j\}\).

This remains true with repeated points and with points that are not vertices.

**Proof.** The first assertion is the definition of a finite convex hull.  For
the forward direction of the second, suppose
\(x=\sum_j\lambda_jx_j\), \(\lambda_j>0\), and let an affine functional
\(f\) support the hull at \(x\), with \(f(x_j)\le f(x)\) for every \(j\).
Then

\[
 0=\sum_j\lambda_j(f(x)-f(x_j)).
\]

Every summand is nonnegative and every \(\lambda_j\) is positive, so
\(f(x_j)=f(x)\) for all \(j\).  Thus the supporting hyperplane contains the
whole affine hull.  No proper relative supporting hyperplane passes through
\(x\), hence \(x\) is in the relative interior.

Conversely, assume \(x\in\operatorname{ri}P\).  For each indexed point
\(x_j\), relative openness permits a sufficiently small \(\varepsilon_j>0\)
such that

\[
 z_j=x+\varepsilon_j(x-x_j)\in P.
\]

Then

\[
 x={\varepsilon_j\over1+\varepsilon_j}x_j
   +{1\over1+\varepsilon_j}z_j,
\]

so \(x\) has a convex representation whose coefficient at the particular
index \(j\) is positive.  Average these \(m\) representations.  The average
represents \(x\) and has every indexed coefficient positive.  Repetitions and
redundancies cause no change in the argument.  ∎

### Theorem 1.2 — exact non-antipodal feasibility

Assume \(N\ne\varnothing\).

1. A nonnegative row satisfying (1.1) exists if and only if \(0\in P\).
2. A row satisfying (1.1) with \(a_j>0\) for every permitted edge exists if
   and only if \(0\in\operatorname{ri}P\).
3. Rows satisfying (1.1) are in bijection with \(\Lambda_0\).

For \(\lambda\in\Lambda_0\), define

\[
 Q(\lambda)=\sum_j\lambda_jq_j>0.                          \tag{1.2}
\]

The corresponding unique row is

\[
 \boxed{a_j={2\lambda_j\over s_jQ(\lambda)}}.             \tag{1.3}
\]

Equivalently, for any nonzero nonnegative tangent dependence
\(b\ge0\), \(\sum_jb_ju_j=0\), put

\[
 D(b)=\sum_j b_j{\ell_j\over s_j}>0.
\]

Then

\[
 \boxed{a_j={2b_j\over s_jD(b)}}.                          \tag{1.4}
\]

**Proof.** Given a row, set \(b_j=a_js_j\).  Then \(b\ge0\),
\(\sum b_ju_j=0\), and \(b\ne0\), because the normal equation is nonzero.
Normalize by \(B=\sum b_j>0\): \(\lambda_j=b_j/B\) lies in \(\Lambda_0\).
Thus feasibility implies \(0\in P\), and strict positivity of the row implies
strict positivity of every \(\lambda_j\), hence relative-interior membership
by Lemma 1.1.

Conversely, choose \(\lambda\in\Lambda_0\).  Every \(q_j\) is positive, so
\(Q(\lambda)>0\).  Formula (1.3) gives nonnegative rates and

\[
 \sum_j a_js_ju_j={2\over Q}\sum_j\lambda_ju_j=0,
 \qquad
 \sum_j a_j\ell_j={2\over Q}\sum_j\lambda_jq_j=2.
\]

If all \(\lambda_j\) are positive then all rates are positive.  Lemma 1.1
supplies such a vector exactly when \(0\in\operatorname{ri}P\).

Finally, any rates generated from \(\lambda\) induce
\(a_js_j=(2/Q)\lambda_j\), whose normalization is again \(\lambda\).  This
proves the bijection.  Formula (1.4) is invariant under positive rescaling of
\(b\) and is the same construction without normalization.  ∎

### Corollary 1.3 — the normal equation fixes exactly one scale

Fix a nonzero tangent dependence \(\lambda\in\Lambda_0\) and seek rates of
the form \(a_j=c\lambda_j/s_j\).  The normal equation is

\[
 cQ(\lambda)=2.
\]

Since \(Q(\lambda)>0\), there is exactly one solution,
\(c=2/Q(\lambda)>0\).  There is no additional local scaling freedom.

### Theorem 1.4 — exact uniqueness criterion

Let \(F\) be the unique minimal face of \(P\) containing \(0\).  Every
\(\lambda\in\Lambda_0\) vanishes at every index with \(u_j\notin F\).  The
following are equivalent:

1. the nonzero nonnegative tangent dependence is unique up to positive scale;
2. \(\Lambda_0\) is a singleton;
3. the degree-one-exact row is unique;
4. the indexed family \(\{u_j:u_j\in F\}\) is affinely independent.

**Proof.** A face containing the barycenter \(0=\sum\lambda_ju_j\) must contain
every point with positive coefficient; hence all representations vanish
outside the minimal face.  Because \(0\in\operatorname{ri}F\), Lemma 1.1
provides a representation positive at every indexed point lying in \(F\).
If those indexed points are affinely dependent, there is a nonzero vector
\(d\) with \(\sum d_j=0\) and \(\sum d_ju_j=0\).  Starting from the strictly
positive representation on \(F\), both \(\lambda+td\) and \(\lambda-td\)
remain nonnegative for sufficiently small \(t>0\), proving nonuniqueness.
If they are affinely independent, barycentric coordinates in their affine
span are unique; coordinates outside \(F\) are forced to zero.  The row and
barycentric-vector bijection in Theorem 1.2 transfers uniqueness.  ∎

Under strict all-edge feasibility, \(F=P\).  Therefore strict feasibility is
unique exactly when the entire indexed candidate family is affinely
independent.  In a two-dimensional tangent plane this permits at most three
indexed candidates; repetitions or redundant candidates force nonuniqueness.

---

## 2. Antipodal neighbors

Let \(P_a\) index antipodal neighbors and \(N\) the non-antipodal neighbors.
For \(p\in P_a\), \(\Omega_p=-\Omega_i\), the tangent contribution is zero,
and the normal loss is exactly two.  No tangent vector and no quotient by a
sine is assigned to an antipodal edge.

For \(j\in N\), set \(b_j=a_js_j\) and

\[
 D(b)=\sum_{j\in N}b_jq_j,
 \qquad t=\sum_{p\in P_a}a_p.
\]

### Theorem 2.1 — complete antipodal parametrization

All nonnegative degree-one-exact rows are exactly the choices satisfying

\[
 b_j\ge0,\qquad \sum_{j\in N}b_ju_j=0,\qquad D(b)\le2,       \tag{2.1}
\]

with

\[
 a_j={b_j\over s_j}\quad(j\in N),\qquad
 t=1-{D(b)\over2},\qquad
 a_p\ge0,\quad\sum_{p\in P_a}a_p=t.                        \tag{2.2}
\]

When \(P_a=\varnothing\), replace \(D(b)\le2\) by \(D(b)=2\).  Formula
(2.2) is never applied to an antipodal index.

**Proof.** Tangential projection of the exactness equation gives the middle
condition in (2.1).  Normal projection gives

\[
 D(b)+2t=2,
\]

which is equivalent to (2.2).  Nonnegativity of the antipodal rates is
possible exactly when \(t\ge0\), equivalently \(D(b)\le2\).  If no antipodal
edge exists, \(t=0\), so equality is required.  The converse follows by direct
substitution.  ∎

### Corollary 2.2 — classification by cases

1. **No permitted neighbors.** No row exists.
2. **Antipodal-only.** A nonnegative row exists exactly when at least one
   antipodal edge is permitted.  The feasible set is the simplex
   \(\sum_pa_p=1\).  A row positive on every permitted antipodal edge always
   exists; use any positive simplex point.
3. **Non-antipodal-only.** Theorem 1.2 applies and the normal scale is fixed.
4. **Mixed permitted set.** Nonnegative feasibility is automatic: set all
   non-antipodal rates to zero and distribute total antipodal rate one.
5. **Mixed strict feasibility.** If \(N\ne\varnothing\), a row positive on
   every permitted edge exists if and only if
   \(0\in\operatorname{ri}\operatorname{conv}\{u_j:j\in N\}\).

For the last assertion, choose \(\lambda_j>0\), \(\sum\lambda_ju_j=0\), and
\(Q=\sum\lambda_jq_j\).  Every

\[
 0<c<{2\over Q}                                                   \tag{2.3}
\]

gives

\[
 a_j={c\lambda_j\over s_j}>0,\qquad
 t=1-{cQ\over2}>0.                                                \tag{2.4}
\]

Split \(t\) by any positive simplex vector on \(P_a\).  Conversely, a row
positive on all non-antipodal edges induces a positive tangent dependence, so
Lemma 1.1 forces the relative-interior condition.

If \(0\) lies on the relative boundary of the non-antipodal tangent hull, a
mixed row may use a nonzero dependence supported on the minimal face and may
leave positive antipodal budget by scaling it down, but it cannot be positive
on every non-antipodal edge.  If \(0\) lies outside that hull, every
non-antipodal rate is zero and antipodes carry the entire budget.

---

## 3. Quantitative cone-surrounding margin

Assume \(0\in P\), let \(L=\operatorname{aff}P\); because it contains the
origin, \(L\) is a linear subspace.  Define the relative centered inradius

\[
 \rho=\sup\{r\ge0:B_L(0,r)\subseteq P\}
      =\operatorname{dist}_L(0,\operatorname{relbd}P).             \tag{3.1}
\]

If \(L\ne\{0\}\), then

\[
 \boxed{\rho=\min_{v\in L,\ \|v\|=1}\max_j\langle v,u_j\rangle}. \tag{3.2}
\]

Indeed, a compact convex set contains the centered ball of radius \(r\) if
and only if its support function dominates the support function \(r\|v\|\) of
that ball.  The unit sphere of \(L\) is compact, so the minimum is attained.
Consequently,

\[
 \rho>0\quad\Longleftrightarrow\quad0\in\operatorname{ri}P.       \tag{3.3}
\]

For unit tangent directions, \(0<\rho\le1\).

### Lemma 3.1 — controlled all-positive dependence

Let \(m=|N|\) and \(\rho>0\).  There is a vector
\(\lambda\in\Lambda_0\) with

\[
 \boxed{\lambda_j\ge\delta:={\rho\over m(1+\rho)}}               \tag{3.4}
\]

for every indexed candidate.  In particular, \(\delta\ge\rho/(2m)\).

**Proof.** Since \(-\rho u_j\in B_L(0,\rho)\subseteq P\),

\[
 0={\rho\over1+\rho}u_j+{1\over1+\rho}(-\rho u_j).
\]

Represent \(-\rho u_j\) as a convex combination of the candidate points.
This gives a representation of zero whose coefficient at index \(j\) is at
least \(\rho/(1+\rho)\).  Average the \(m\) representations.  Each indexed
coefficient is then at least (3.4).  This construction explicitly allows
repeated and redundant directions.  ∎

### 3.2 Explicit angular and inverse-quadratic bounds

Assume (0<c_1le c_2) and

\[
 c_1h\le\theta_j\le c_2h,\qquad 0<h\le h_0,\qquad
 \theta_0:=c_2h_0\le{\pi\over2}.                                 \tag{3.5}
\]

Define

\[
 \kappa_0={\sin(\theta_0/2)\over\theta_0/2},\quad
 \sigma_0={\sin\theta_0\over\theta_0},\quad
 \beta_0={\tan(\theta_0/2)\over\theta_0}.                        \tag{3.6}
\]

Concavity of sine, \(\tan x\ge x\), and monotonicity of
\(\tan x/x\) give

\[
 {\kappa_0^2c_1^2\over2}h^2\le\ell_j\le {c_2^2\over2}h^2,        \tag{3.7}
\]

\[
 \sigma_0c_1h\le s_j\le c_2h,\qquad
 {c_1\over2}h\le q_j\le\beta_0c_2h.                              \tag{3.8}
\]

Let \(R=\sum_ja_j\).  The normal equation alone yields

\[
 {2\over1-\cos(c_2h)}\le R\le{2\over1-\cos(c_1h)},               \tag{3.9}
\]

and hence the fully explicit loss-window bounds

\[
 \boxed{{4\over c_2^2h^2}\le R\le
 {4\over\kappa_0^2c_1^2h^2}}.                                   \tag{3.10}
\]

These do **not** require a cone margin.  They follow from
\((\min\ell)R\le2\le(\max\ell)R\).

For an individual coefficient, nonnegativity and the normal equation give

\[
 0\le a_j\le{2\over1-\cos(c_1h)}
       \le{4\over\kappa_0^2c_1^2h^2}.                            \tag{3.11}
\]

A positive coefficientwise lower bound does require the cone margin.  Choose
\(\lambda\) from Lemma 3.1 and use (1.3).  Because
\(s_j\le\sin(c_2h)\) and \(Q\le\tan(c_2h/2)\),

\[
 \boxed{a_j\ge{2\delta\over1-\cos(c_2h)}
              \ge{4\delta\over c_2^2h^2}},                      \tag{3.12}
\]

while (3.11) remains the upper bound.  Thus all selected rates are controlled
above and below by explicit multiples of \(h^{-2}\), with the lower constant
depending on \(m\) and \(\rho\).

### 3.3 Conditioning of the local balance system

Let \(U:\mathbb R^m\to L\) be \(Ux=\sum_jx_ju_j\).  From (3.2), for every
\(v\in L\),

\[
 \|U^*v\|_2\ge\max_j|\langle v,u_j\rangle|
              \ge\rho\|v\|.                                    \tag{3.13}
\]

Hence the least nonzero singular value of \(U\) is at least \(\rho\), and a
minimum-norm right inverse has norm at most \(1/\rho\).

For the scaled tangent-normal matrix

\[
 Cx=\left(\sum_jx_ju_j,\ \sum_jq_jx_j\right),                    \tag{3.14}
\]

write \(q_-\le q_j\le q_+\).  If
\(y=C^*(v,t)\), then a balancing probability vector \(\lambda\) gives

\[
 |t|\le{\|y\|_2\over q_-},
\]

and (3.13) gives

\[
 \|v\|\le {1\over\rho}
 \left(1+\sqrt m\,{q_+\over q_-}\right)\|y\|_2.
\]

Therefore, with

\[
 K_C={1\over q_-}+{1\over\rho}
       \left(1+\sqrt m\,{q_+\over q_-}\right),                   \tag{3.15}
\]

\[
 \sigma_{\min}(C)\ge K_C^{-1}.                                  \tag{3.16}
\]

The original balance matrix has columns
\(B_j=(s_ju_j,\ell_j)=s_j(u_j,q_j)\).  If
\(s_-\le s_j\) and \(d_+=2\sin(\theta_+/2)\), then

\[
 \boxed{\sigma_{\min}(B)\ge{s_-\over K_C},\qquad
 \kappa_2(B)\le{\sqrt m\,d_+K_C\over s_-}}.                    \tag{3.17}
\]

The upper bound uses \(\|B\|_2\le\|B\|_F\le\sqrt m\,d_+\).
Equation (3.17) separates tangent-cone conditioning from the small normal row.

### 3.4 Perturbation radius and objective degradation

For arbitrary ambient perturbations, a one-dimensional relative hull is not
robust: a pair \(u,-u\) can be moved slightly to the same side of the origin.
The following theorem is therefore stated either for full two-dimensional
tangent spanning or for perturbations constrained to a fixed relative span.
Identify the old and new tangent planes by an orthogonal map and suppose

\[
 \max_j\|u'_j-u_j\|\le\varepsilon_u.                             \tag{3.18}
\]

The support-function formula gives

\[
 \rho'\ge\rho-\varepsilon_u.                                    \tag{3.19}
\]

Thus \(\varepsilon_u<\rho\) preserves strict feasibility.  No positive
uniform radius exists at a relative-boundary configuration \(\rho=0\).
Angles do not affect tangent feasibility as long as they remain in
\((0,\pi)\).

A nearby all-positive dependence can be quantified.  Start with
\(\lambda_j\ge\delta\) from (3.4).  If \(\varepsilon_u\le\rho/2\), define

\[
 K_0=1+{2(1+\sqrt m)\over\rho}.                                  \tag{3.20}
\]

The augmented barycentric map
\(M'd=(\sum d_ju'_j,\sum d_j)\) has a right inverse of norm at most \(K_0\).
The old coefficients leave residual
\(r=\sum\lambda_ju'_j\), with \(\|r\|\le\varepsilon_u\).  Hence there is
\(d\) with \(M'd=(-r,0)\) and
\(\|d\|_2\le K_0\varepsilon_u\).  If

\[
 \boxed{\varepsilon_u\le
 \min\left\{{\rho\over2},{\delta\over2K_0}\right\}},           \tag{3.21}
\]

then \(\lambda'=\lambda+d\) balances the perturbed directions, sums to one,
and obeys \(\lambda'_j\ge\delta/2\).  Also

\[
 \|\lambda'-\lambda\|_1\le\sqrt m K_0\varepsilon_u.             \tag{3.22}
\]

For an explicit rate perturbation bound, suppose both angle sets lie in
\([\theta_-,\theta_+]\subset(0,\pi/2]\).  Put

\[
 s_-=\sin\theta_-,\quad s_+=\sin\theta_+,\quad
 q_-=\tan(\theta_-/2),\quad q_+=\tan(\theta_+/2),
\]

\[
 L_q={1\over2\cos^2(\theta_+/2)}.                                \tag{3.23}
\]

If \(\max_j|\theta'_j-\theta_j|\le\varepsilon_\theta\) and
\(\Delta_\lambda=\|\lambda'-\lambda\|_1\), then

\[
 |Q'-Q|\le q_+\Delta_\lambda+L_q\varepsilon_\theta,              \tag{3.24}
\]

and direct subtraction of (1.3) gives

\[
 \boxed{
 \|a'-a\|_1\le {2\Delta_\lambda\over s_-q_-}
 +{2\left[\varepsilon_\theta q_+
   +s_+\left(q_+\Delta_\lambda+L_q\varepsilon_\theta\right)\right]
   \over s_-^2q_-^2}.}                                           \tag{3.25}
\]

For any linear local objective \(c^Ta\) with
\(\|c\|_\infty\le C\), the constructed feasible row degrades the objective by
at most \(C\) times the right-hand side of (3.25).  This gives a one-sided
bound on the perturbed optimum.  Applying the same construction in reverse
gives an absolute optimum-value bound when both configurations satisfy the
same margin and angular window.

For perturbations \(|\theta'_j-\theta_j|\le\eta h\), use the new explicit
window \((c_1-\eta)h\le\theta'_j\le(c_2+\eta)h\), with
\(0<\eta<c_1\) and \((c_2+\eta)h\le\theta_0\).

---

## 4. Global reversible shared-edge system

Let \(V\) be a finite node set, \(w_i>0\), and \(G=(V,E)\) an undirected
permitted graph.  For an edge \(e=\{p,q\}\), define the column
\(z_e\in(\mathbb R^3)^V\) by

\[
 (z_e)_p=\Omega_q-\Omega_p,\qquad
 (z_e)_q=\Omega_p-\Omega_q,\qquad
 (z_e)_i=0\ (i\notin\{p,q\}).                                   \tag{4.1}
\]

The definition is independent of an arbitrary orientation.  Let
\(A\gamma=\sum_e\gamma_ez_e\) and

\[
 b_i=-2w_i\Omega_i.                                               \tag{4.2}
\]

Then \(\gamma_e\ge0\), \(A\gamma=b\) is exactly the shared-conductance
form of degree-one exactness, because the row rate is
\(a_{ij}=\gamma_{ij}/w_i\).

### Theorem 4.1 — cone and feasible-polytope characterization

Let

\[
 K=A\mathbb R_+^E=\operatorname{cone}\{z_e:e\in E\}.             \tag{4.3}
\]

A global reversible solution exists if and only if \(b\in K\).  The feasible
set is the polyhedron

\[
 \mathcal P(b)=\{\gamma\in\mathbb R_+^E:A\gamma=b\}.             \tag{4.4}
\]

If every permitted edge joins distinct spherical nodes, \(\mathcal P(b)\) is
a compact polytope.  Indeed, pairing (4.1) with the node-position field gives

\[
 \sum_i\Omega_i\cdot(A\gamma)_i
 =-\sum_e\gamma_e\|\Omega_p-\Omega_q\|^2
 =-2\sum_e\gamma_e(1-\Omega_p\cdot\Omega_q).                    \tag{4.5}
\]

Pairing (4.2) gives \(-2W\), where \(W=\sum_iw_i\).  Hence every feasible
point satisfies the coercive identity

\[
 \boxed{\sum_e\gamma_e\ell_e=W},\qquad
 \ell_e=1-\Omega_p\cdot\Omega_q>0.                               \tag{4.6}
\]

Thus

\[
 {W\over\ell_{\max}}\le\sum_e\gamma_e
 \le{W\over\ell_{\min}}.                                       \tag{4.7}
\]

If a permitted edge joins coincident nodes, its column is zero and its
nonnegative variable is an unbounded recession direction.  Deleting all zero
columns restores the compact-polytope statement; no nondegeneracy is hidden.

### Theorem 4.2 — weighted centering and the dense construction

Every edge column has node sum zero, so feasibility requires

\[
 \boxed{\sum_iw_i\Omega_i=0}.                                   \tag{4.8}
\]

For the complete graph, (4.8) is also sufficient, with the strictly positive
conductances

\[
 \boxed{\gamma_{ij}={2w_iw_j\over W}}\qquad(i\ne j).             \tag{4.9}
\]

Indeed,

\[
 \sum_{j\ne i}\gamma_{ij}(\Omega_j-\Omega_i)
 ={2w_i\over W}\left(\sum_jw_j\Omega_j-W\Omega_i\right)
 =-2w_i\Omega_i.
\]

### Theorem 4.3 — exact finite Farkas alternative

Exactly one of the following systems has a solution:

**Primal**

\[
 \gamma\ge0,\qquad A\gamma=b;                                   \tag{4.10}
\]

**Dual certificate**

\[
 A^Ty\ge0,\qquad \langle b,y\rangle<0.                           \tag{4.11}
\]

This is the standard finite-dimensional Farkas theorem applied to the finite
matrix whose columns are (4.1).  Its hypotheses are satisfied because the
spaces are finite-dimensional and \(K\) is a finitely generated closed convex
cone.  The transpose block is, with \(e=\{p,q\}\),

\[
 \boxed{(A^Ty)_e=(y_p-y_q)\cdot(\Omega_q-\Omega_p)}.              \tag{4.12}
\]

The two alternatives cannot coexist because
\(\langle b,y\rangle=\gamma^TA^Ty\ge0\) for a primal solution.  Farkas
separation supplies (4.11) whenever \(b\notin K\), so this is a full
alternative, not merely certificate soundness.

**Geometric meaning.** Under the infinitesimal displacement
\(\Omega_i(t)=\Omega_i+ty_i\),

\[
 {d\over dt}{1\over2}\|\Omega_q(t)-\Omega_p(t)\|^2\bigg|_{t=0}
 =(y_q-y_p)\cdot(\Omega_q-\Omega_p)=-(A^Ty)_e.                   \tag{4.13}
\]

Thus \(A^Ty\ge0\) means that every permitted chord is nonincreasing to first
order.  The negative-work condition is

\[
 -2\sum_iw_i\Omega_i\cdot y_i<0,
\]

so the same displacement has positive weighted radial work.  A failure of
centering has the exact constant-field certificate
\(y_i=s=\sum_iw_i\Omega_i\): then \(A^Ty=0\) and
\(b^Ty=-2\|s\|^2<0\).

### Theorem 4.4 — strict feasibility

Assume zero edge columns have been removed.  A solution with
\(\gamma_e>0\) for every permitted edge exists if and only if

\[
 \boxed{b\in\operatorname{ri}K}.                                \tag{4.14}
\]

The proof is the conic analogue of Lemma 1.1: a positive combination of every
generator cannot lie on a proper supporting face, while an interior point can
be moved a small distance opposite each generator and the resulting
representations averaged.

Equivalently,

\[
 b\in\operatorname{ri}K
 \Longleftrightarrow
 \{y:A^Ty\ge0,\ b^Ty=0\}=\{y:A^Ty=0\}.                          \tag{4.15}
\]

The right side says that every dual functional vanishing at \(b\) must vanish
on the entire cone; a nonzero nonnegative edge block at zero work would expose
a proper face.

An operational uniform strictness value is

\[
 \tau_* =\max\{\tau\ge0:\exists\gamma,\ A\gamma=b,
                         \gamma_e\ge\tau\ \forall e\}.           \tag{4.16}
\]

Then \(\tau_*>0\) exactly under strict feasibility.  Writing
\(\gamma=x+\tau\mathbf1\), finite LP duality gives

\[
 \boxed{\tau_*=
 \min\{b^Ty:A^Ty\ge0,\ \mathbf1^TA^Ty\ge1\}}.                  \tag{4.17}
\]

### 4.5 Strong LP duality and complementary slackness

For any nonnegative edge cost \(c\), consider

\[
 \tag{P_c}\min_{\gamma\ge0}\ c^T\gamma\quad\text{s.t. }A\gamma=b,
\]

\[
 \tag{D_c}\max_y\ b^Ty\quad\text{s.t. }A^Ty\le c.
\]

If the exact system is feasible, the primal feasible polytope is compact and
the dual is feasible at \(y=0\).  The standard finite-dimensional strong LP
duality theorem therefore gives attained equal optima.  For any optimal pair,

\[
 c^T\gamma-b^Ty
 =\gamma^T(c-A^Ty)=0,                                            \tag{4.18}
\]

with both factors componentwise nonnegative.  Consequently

\[
 \boxed{\gamma_e\,[c_e-(A^Ty)_e]=0\quad\text{for every edge }e.} \tag{4.19}
\]

Geometrically, every conducting edge saturates its allowed dual chord-strain
price; every strictly slack dual edge carries zero conductance.

Project objectives are exact instances:

- unweighted total outgoing rate has
  \(c_{pq}=w_p^{-1}+w_q^{-1}\);
- weighted total outgoing rate has \(c_e=2\);
- the weighted quadratic edge-loss defect
  \(\sum_iw_i\sum_ja_{ij}\ell_{ij}^2\) has
  \(c_e=2\ell_e^2\);
- any prescribed linear defect penalty uses its edgewise penalty as \(c_e\).

For a peak row functional, let \(H_{ie}\ge0\) be the contribution of edge
\(e\) to row \(i\), for example
\(H_{i,e}=\mathbf1_{i\in e}\ell_e^2/w_i\).  The epigraph LP

\[
 \min t\quad\text{s.t. }A\gamma=b,\ \gamma\ge0,\ H\gamma\le t\mathbf1
                                                                    \tag{4.20}
\]

has dual

\[
 \max b^Ty\quad\text{s.t. }z\ge0,\ \mathbf1^Tz=1,
               \ A^Ty\le H^Tz.                                   \tag{4.21}
\]

Complementary slackness is

\[
 z_i[t-(H\gamma)_i]=0,
 \qquad
 \gamma_e[(H^Tz)_e-(A^Ty)_e]=0.                                  \tag{4.22}
\]

Thus \(z\) is a probability distribution supported on worst rows, and active
edges saturate the mixture of their endpoint defect prices.

For weighted \(\ell^1\) residual minimization, use

\[
 \min_{\gamma,r^+,r^-\ge0}
 c^T\gamma+\sum_k\tau_k(r_k^++r_k^-)
 \quad\text{s.t. }A\gamma-r^++r^-=b.                             \tag{4.23}
\]

Its dual is

\[
 \max_y b^Ty\quad\text{s.t. }A^Ty\le c,
                 -\tau_k\le y_k\le\tau_k.                        \tag{4.24}
\]

The exact complementary-slackness blocks are

\[
 \gamma_e[c_e-(A^Ty)_e]=0,
 \quad r_k^+(\tau_k+y_k)=0,
 \quad r_k^-(\tau_k-y_k)=0.                                     \tag{4.25}
\]

Because \(A\gamma-b=r^+-r^-\), a positive residual coordinate forces
\(y_k=-\tau_k\), a negative residual coordinate forces \(y_k=+\tau_k\), and
a nonsaturated box coordinate has zero residual.  With \(c=0\), the optimum
is zero exactly when the exact feasibility system is solvable; otherwise an
optimal dual field quantifies the distance from the cone.

### 4.6 Sensitivity to nodes and masses

No theorem can give an unrestricted perturbation radius: weighted centering is
an exact equality, and sparse graphs may have further linear compatibility
conditions.  The following statement includes the necessary compatibility
hypothesis explicitly.

Let \(A\gamma^0=b\) with
\(\alpha=\min_e\gamma_e^0>0\).  For perturbed \(A',b'\), set

\[
 r=b'-A'\gamma^0.                                                \tag{4.26}
\]

Assume \(r\in\operatorname{range}A'\), and let
\(\sigma_+(A')\) be the smallest positive singular value.  The pseudoinverse
correction \(d=A'^+r\) obeys

\[
 \|d\|_2\le{\|r\|_2\over\sigma_+(A')}.                          \tag{4.27}
\]

Therefore

\[
 \boxed{\|r\|_2<\alpha\sigma_+(A')}
 \quad\Longrightarrow\quad
 \gamma'=\gamma^0+d>0,\ A'\gamma'=b'.                           \tag{4.28}
\]

For \(n\) nodes and \(m\) edges, if
\(\max_i\|\Omega'_i-\Omega_i\|\le\varepsilon_\Omega\),
\(\max_i|w'_i-w_i|\le\varepsilon_w\), and
\(w_{\max}=\max_iw_i\), then

\[
 \|A'-A\|_2\le2\sqrt{2m}\,\varepsilon_\Omega,                 \tag{4.29}
\]

\[
 \|b'-b\|_2\le2\sqrt n\,
       (\varepsilon_w+w_{\max}\varepsilon_\Omega).              \tag{4.30}
\]

Hence

\[
 \|r\|_2\le2\sqrt n(\varepsilon_w+w_{\max}\varepsilon_\Omega)
 +2\sqrt{2m}\,\varepsilon_\Omega\|\gamma^0\|_2.                \tag{4.31}
\]

Substitution into (4.28) is an explicit strict-feasibility radius, conditional
on the unavoidable range compatibility.  For a perturbed cost \(c'\), the
constructed feasible objective satisfies

\[
 c'^T\gamma'-c^T\gamma^0
 \le\|c'-c\|_2\|\gamma^0\|_2
 +\|c'\|_2{\|r\|_2\over\sigma_+(A')}.                           \tag{4.32}
\]

For the complete graph, sensitivity is stronger and does not require a matrix
pseudoinverse.  If the perturbed data remain centered and positive, formula
(4.9) remains exact for arbitrary node movement.  If
\(|w_i'-w_i|\le\varepsilon_w<w_{\min}\) and
\(n\varepsilon_w<W\), then

\[
 \gamma'_{ij}\ge
 {2(w_{\min}-\varepsilon_w)^2\over W+n\varepsilon_w},            \tag{4.33}
\]

and

\[
 |\gamma'_{ij}-\gamma_{ij}|\le2\left[
 {2w_{\max}\varepsilon_w+\varepsilon_w^2\over W-n\varepsilon_w}
 +{w_{\max}^2n\varepsilon_w\over W(W-n\varepsilon_w)}\right].   \tag{4.34}
\]

### Theorem 4.5 — centered-clique reconciliation mechanism

A sparse sufficient mechanism goes beyond the single complete-graph
construction.  Suppose the permitted graph contains complete subgraphs
\(C_r\).  For each clique choose positive submasses \(w_i^{(r)}\) satisfying

\[
 \sum_{i\in C_r}w_i^{(r)}\Omega_i=0,\qquad
 \sum_{r:i\in C_r}w_i^{(r)}=w_i.                                \tag{4.35}
\]

Within clique \(r\), set

\[
 \gamma_{ij}^{(r)}={2w_i^{(r)}w_j^{(r)}\over W_r},\qquad
 W_r=\sum_{i\in C_r}w_i^{(r)}.                                  \tag{4.36}
\]

Sum conductances over all cliques containing an edge.  Each clique contributes
\(-2w_i^{(r)}\Omega_i\) at node \(i\); summing (4.35) gives
\(-2w_i\Omega_i\).  Thus the resulting shared-edge system is globally exact.
Every edge covered by at least one clique with positive endpoint submasses has
positive conductance.  This permits sparse unions of centered antipodal pairs,
tetrahedral blocks, or larger centered cells and is a constructive local-to-
global reconciliation theorem.

---

## 5. Exact examples and certificates

All examples below are checked by
`pure_math/tests/test_spherical_feasibility.py` using rational arithmetic.

### 5.1 Local hull states

Let \(e_1=(1,0)\), \(e_2=(0,1)\).

- **Outside:** \(\{e_1,e_2\}\).  The separator \(v=(1,1)\) has
  \(v\cdot u_j=1\), so no nonzero nonnegative tangent dependence can sum to
  zero.
- **Relative boundary:** \(\{e_1,-e_1,e_2\}\), with
  \(\lambda=(1/2,1/2,0)\).  The supporting functional \(v=e_2\) is
  nonnegative on the set and vanishes exactly on the active face.  Strict
  all-edge feasibility is impossible.
- **Relative interior:** \(\{e_1,-e_1,e_2,-e_2\}\), with
  \(\lambda_j=1/4\).
- **Repeated/redundant:**
  \(\{e_1,e_1,-e_1,-e_1,e_2,-e_2\}\).  Positive mass can be shifted between
  duplicate indices, giving distinct all-positive dependences and proving
  nonuniqueness.

Use exact angular data
\(\cos\theta=3/5\), \(\sin\theta=4/5\),
\(\ell=2/5\), \(q=1/2\).  Formula (1.3) gives boundary rates
\((5/2,5/2,0)\) and square rates \((5/4,5/4,5/4,5/4)\).

### 5.2 Perturbation crossing the boundary

Use the rational unit-circle parametrization

\[
 u(r)=\left({r^2-1\over r^2+1},{2r\over r^2+1}\right)
\]

and the set \(\{e_1,u(r),e_2\}\).  At \(r=1/3\),
\(u=(-4/5,3/5)\) and zero is outside.  At \(r=0\), zero lies on the edge
\(\operatorname{conv}\{e_1,-e_1\}\).  At \(r=-1/3\),
\(u=(-4/5,-3/5)\) and

\[
 \lambda=(1/3,5/12,1/4)>0
\]

is an exact certificate that zero lies in the relative interior.  This also
shows why no positive perturbation radius exists at margin zero.

### 5.3 Antipodal examples

- Three antipodal-only permitted edges: \(a_p=1/3\) gives total normal loss
  two and is strict.
- Mixed boundary case with the three non-antipodal directions
  \(e_1,-e_1,e_2\): rates
  \((5/4,5/4,0)\) spend one unit of normal budget and an antipodal rate
  \(1/2\) spends the other.  The third non-antipodal edge cannot be positive.
- Mixed strict case with the four square directions: non-antipodal rates
  \(5/16\) each spend \(1/2\), and antipodal rate \(3/4\) spends \(3/2\).

### 5.4 Weighted-centered local/global incompatibility

Take the cube nodes

\[
 \Omega_x={x\over\sqrt3},\qquad x\in\{\pm1\}^3,
\]

with cube edges joining sign vectors that differ in one coordinate.  Every
edge has \(\Omega_x\cdot\Omega_y=1/3\), and for each node

\[
 \sum_{y\sim x}(\Omega_y-\Omega_x)=-2\Omega_x.                  \tag{5.1}
\]

The three tangent directions form an equilateral triple; consequently each
local row is uniquely strictly feasible and has \(a_{xy}=1\).

Assign mass two to \((1,1,1)/\sqrt3\) and
\((-1,-1,-1)/\sqrt3\), and mass one to the other six nodes.  Antipodal pairs
have equal masses, so weighted centering holds.  Nevertheless a shared edge
would have to satisfy

\[
 \gamma_{xy}=w_xa_{xy}=w_x=w_y=w_ya_{yx},                       \tag{5.2}
\]

which is impossible on an edge joining unequal masses.  Thus every row is
locally strictly feasible and the global necessary centering condition holds,
but no global reversible shared-edge solution exists.

An exact Farkas certificate is

\[
 y_x={1\over\sqrt3}(x_2,x_3,x_1).                               \tag{5.3}
\]

If an edge flips coordinate \(k\), the \(k\)-th component of (5.3) is
unchanged, so \((A^Ty)_e=0\) on every edge.  Direct summation gives

\[
 b^Ty=-4<0.                                                       \tag{5.4}
\]

This is a global compatibility obstruction beyond weighted centering.

### 5.5 Globally strict symmetric example and optimal dual

On the same cube with all masses one, set \(\gamma_e=1\) on all twelve edges.
Equation (5.1) proves global exactness.  For unweighted total outgoing rate,
\(c_e=2\).  The dual field

\[
 y_i=-{3\over2}\Omega_i                                        \tag{5.5}
\]

satisfies

\[
 (A^Ty)_e={3\over2}\|\Omega_q-\Omega_p\|^2=2=c_e.              \tag{5.6}
\]

The primal and dual values are both \(24\), so (5.5) is an exact optimal dual
certificate and every complementary-slackness edge block is saturated.

---

## 6. External theorem use and novelty boundary

The finite barycentric and relative-interior lemmas were proved directly above.
The only unformalized general results used as external inputs are the standard
finite-dimensional Farkas alternative and strong linear-programming duality;
their exact primal, dual, signs, boundedness hypotheses, and complementary
blocks were transferred explicitly in Sections 4.3–4.5.

Positive/minimal-stencil theory already uses local conic feasibility and Farkas
separation; a principal comparator is Benjamin Seibold, *Minimal positive
stencils in meshfree finite difference methods for the Poisson equation*,
arXiv:0802.2674.  Positive spherical Delaunay Laplacians and coordinate
spectral statements are also adjacent; see Ivan Izmestiev and Wai Yeung Lam,
*Discrete Laplacians — spherical and hyperbolic*, arXiv:2408.04877 and Journal
of the London Mathematical Society (2025).

Accordingly, the publication contribution is **not** the isolated statement
that a local positive dependence is a convex-hull condition.  The AFP-specific
package adds, in one exact theory:

1. spherical tangent/normal separation with the fixed eigenvalue \(-2\);
2. the angular renormalization \(q_j=(1-\cos\theta_j)/\sin\theta_j\) and the
   unique normal scale;
3. a division-free antipodal classification;
4. relative-margin coefficient, rate, conditioning, perturbation, and
   objective constants;
5. positive quadrature masses and shared-edge reversibility;
6. exact global cone/Farkas/LP geometry with spherical edge-strain duals;
7. a weighted-centered local/global incompatibility certificate; and
8. a centered-clique mechanism that genuinely reconciles local blocks into a
   sparse global shared-edge solution.

These are the claims controlled by the accompanying claim matrix and theorem
map.

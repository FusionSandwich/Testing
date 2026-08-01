# Exact local spherical feasibility and global shared-edge duality

## 0. Scope, notation, and total conventions

Fix a node \(\Omega_i\in S^2\). The non-antipodal permitted neighbours are
indexed by a finite set \(J\), and the antipodal permitted neighbours by a
disjoint finite set \(A\). For \(j\in J\),

\[
 \Omega_j=\cos\theta_j\,\Omega_i+\sin\theta_j\,u_j,
 \qquad 0<\theta_j<\pi,
\]

where \(u_j\) is a unit vector in \(T_{\Omega_i}S^2\). Put

\[
 v_j=\sin\theta_j u_j,\qquad
 \ell_j=1-\cos\theta_j,
 \qquad t_j=\tan(\theta_j/2).
\]

The half-angle identity used throughout is

\[
 \ell_j=\sin\theta_j\,t_j. \tag{0.1}
\]

For \(k\in A\), the tangent component is zero and the normal loss is exactly
two. No tangent direction, angle denominator, or value of \(\sin\pi\) is ever
assigned to an antipodal index.

For the non-antipodal constructions below, assume \(J\ne\varnothing\), and let

\[
 P=\operatorname{conv}\{u_j:j\in J\},\qquad
 U=\operatorname{span}\{u_j:j\in J\},
\]

and let

\[
 \mathcal B=
 \left\{\beta\in\mathbb R^J:
 \beta\ge0,\quad \sum_j\beta_j=1,\quad
 \sum_j\beta_j u_j=0\right\}. \tag{0.2}
\]

Relative interior is always taken in \(U\). If \(0\in P\), then
\(\operatorname{aff}P=U\): the affine hull contains zero and the points
\(u_j\), hence their linear span, while the reverse containment is immediate.
Thus \(\operatorname{relint}_U P\) is the ordinary relative interior of \(P\).

Two total conventions are required in the infeasible case. They do not alter
either quantity when the displayed maximum/supremum in the problem exists:

\[
 \rho=\sup\left(\{0\}\cup
 \{t\ge0:tB_U\subseteq P\}\right), \tag{0.3}
\]

and \(\beta_*=0\) when \(\mathcal B=\varnothing\); otherwise

\[
 \beta_*=\max_{\beta\in\mathcal B}\min_j\beta_j. \tag{0.4}
\]

Here \(B_U\) is the closed Euclidean unit ball of \(U\). These conventions
make the equivalences below meaningful when \(0\notin P\). The case
\(J=\varnothing\) is reserved for the pure-antipodal statement in Theorem
2.1. “The row is unique” and “\(\mathcal B\) is a singleton” mean
existence and uniqueness, not merely subsingletonness of a possibly empty set.

---

## 1. Exact non-antipodal local theorem

Assume \(J\ne\varnothing\) and \(A=\varnothing\). A row is feasible precisely when

\[
 a_j\ge0,\qquad
 \sum_j a_j\sin\theta_j u_j=0,\qquad
 \sum_j a_j\ell_j=2. \tag{1.1}
\]

### Theorem 1.1 — feasibility and strict feasibility

There exists a feasible row if and only if \(0\in P\). There exists a
feasible row with \(a_j>0\) for every indexed permitted neighbour if and only
if \(0\in\operatorname{relint}_U P\). Both statements are unchanged by
repeated directions, redundant indexed points, or a lower-dimensional span.

#### Proof

Given a feasible row, set

\[
 x_j=a_j\sin\theta_j. \tag{1.2}
\]

Then \(x\ge0\), \(\sum_jx_ju_j=0\), and, by (0.1),

\[
 \sum_jx_jt_j=2. \tag{1.3}
\]

Because every \(t_j>0\), (1.3) gives \(T:=\sum_jx_j>0\). Hence
\(\beta=x/T\) belongs to \(\mathcal B\), proving \(0\in P\). Conversely,
the explicit construction in Theorem 1.2 below turns every
\(\beta\in\mathcal B\) into a feasible row. This proves nonnegative
feasibility.

If \(\beta_j>0\) for all \(j\) and zero were on the boundary of \(P\) in
\(U\), a supporting-hyperplane theorem would give a nonzero \(q\in U\) with
\(q\cdot u_j\ge0\) for all \(j\). The identity

\[
 0=q\cdot\sum_j\beta_ju_j
  =\sum_j\beta_j(q\cdot u_j)
\]

would force \(q\cdot u_j=0\) for every \(j\). Since the \(u_j\) span \(U\),
this forces \(q=0\), a contradiction. Thus an all-positive dependence implies
relative-interior membership.

For the converse, relative-interior membership is equivalent to \(\rho>0\).
The independent constructive argument in Theorem 3.1 produces a member of
\(\mathcal B\) whose every coordinate is positive. The row formula in Theorem
1.2 preserves strict positivity because \(\sin\theta_j>0\) and its common
scale is positive.

All arguments are indexed: two equal values of \(u_j\) still receive distinct
coordinates of \(\beta\). No affine-independence or full ambient dimension is
used. This proves the degeneracy claims. \(\square\)

### Theorem 1.2 — exact parameterization and common scaling

For \(\beta\in\mathcal B\), define

\[
 S(\beta)=\sum_j\beta_jt_j. \tag{1.4}
\]

Then \(S(\beta)>0\), and the unique positive common scaling of this normalized
tangent dependence is

\[
 a_j(\beta)=
 \frac{2\beta_j}{\sin\theta_j\,S(\beta)}. \tag{1.5}
\]

Every nonnegative feasible row is obtained exactly once from (1.5), after
normalizing \(\beta_j=a_j\sin\theta_j/T\), where
\(T=\sum_qa_q\sin\theta_q>0\).

#### Proof

At least one coordinate of a normalized \(\beta\) is positive, and every
\(t_j>0\), so \(S(\beta)>0\). Formula (1.5) gives

\[
 \sum_j a_j\sin\theta_j u_j
 =\frac2{S(\beta)}\sum_j\beta_j u_j=0
\]

and, using (0.1),

\[
 \sum_ja_j\ell_j
 =\frac2{S(\beta)}\sum_j\beta_jt_j=2.
\]

If a common multiple \(c\beta_j/\sin\theta_j\) satisfies the normal equation,
then \(cS(\beta)=2\), so \(c=2/S(\beta)\); the common scale is unique.

Conversely, (1.2)--(1.3) show that a feasible row has \(T>0\) and
\(\beta=x/T\in\mathcal B\). Moreover

\[
 S(\beta)=\frac1T\sum_jx_jt_j=\frac2T,
\]

and substitution in (1.5) returns \(a_j=x_j/\sin\theta_j\). Thus the two maps
are inverse. \(\square\)

### Corollary 1.3 — outgoing rate and uniqueness

The exact outgoing rate is

\[
 r(\beta)=\sum_ja_j(\beta)
 =\frac2{S(\beta)}\sum_j\frac{\beta_j}{\sin\theta_j}. \tag{1.6}
\]

There exists exactly one feasible row if and only if \(\mathcal B\) contains
exactly one point.

#### Proof

Equation (1.6) is the sum of (1.5). The uniqueness statement follows from the
bijection in Theorem 1.2. \(\square\)

---

## 2. Complete antipodal theorem

### Theorem 2.1 — pure antipodal and mixed feasibility

1. If \(J=\varnothing\) and \(A\ne\varnothing\), the feasible rows are exactly

   \[
   a_k\ge0,\qquad \sum_{k\in A}a_k=1. \tag{2.1}
   \]

   A strictly positive row on every permitted antipodal edge exists exactly
   when \(A\ne\varnothing\); the uniform point \(a_k=1/|A|\) is explicit.

2. If both \(J\) and \(A\) are nonempty, a nonnegative row always exists:
   take every non-antipodal coefficient to be zero and place unit total mass
   on the antipodal simplex.

3. In the mixed case, a row strictly positive on every permitted edge exists
   if and only if \(0\in\operatorname{relint}_U P\).

4. If \(0\in P\setminus\operatorname{relint}_U P\), mixed nonnegative rows
   exist but every feasible row has a zero coefficient on at least one
   non-antipodal permitted edge.

#### Proof

The pure antipodal balance is \(2\sum_ka_k=2\), which is (2.1). The mixed
nonnegative construction is immediate.

For strict mixed feasibility, a strict row induces
\(x_j=a_j\sin\theta_j>0\) and hence an all-positive normalized tangent
dependence. The supporting-hyperplane direction of Theorem 1.1 gives
relative-interior membership. Conversely, choose an all-positive
\(\beta\in\mathcal B\), take a sufficiently small positive non-antipodal
scale, and place the strictly positive remaining budget uniformly on \(A\);
the exact formula is in Theorem 2.2. On the boundary, a nonzero supporting
vector \(q\) has \(q\cdot u_j\ge0\) for all \(j\), with a strict inequality
for at least one \(j\). Every tangent dependence summing to zero must vanish on
every strict-support index. Therefore no row can be positive on all
non-antipodal edges. \(\square\)

### Theorem 2.2 — exact mixed parameterization

Assume \(J\ne\varnothing\) and \(A\ne\varnothing\).

Define the nonnegative tangent cone and its normal expenditure by

\[
 \mathcal D=\{x\in\mathbb R_+^J:\sum_jx_ju_j=0\},
 \qquad q(x)=\sum_jx_jt_j. \tag{2.2}
\]

All mixed feasible rows are parameterized exactly as follows:

\[
 \begin{aligned}
 &x\in\mathcal D,\qquad 0\le q(x)\le2,\\
 &a_j=x_j/\sin\theta_j\quad(j\in J),\\
 &a_k=z_k\ge0\quad(k\in A),\qquad
   \sum_{k\in A}z_k=1-q(x)/2.
 \end{aligned} \tag{2.3}
\]

Equivalently, the branch \(x=0\) is always allowed. When \(x\ne0\), write
\(x=s\beta\), where \(s=\sum_jx_j>0\), \(\beta\in\mathcal B\), and

\[
 0<s\le\frac2{S(\beta)},\qquad
 \sum_{k\in A}a_k=1-\frac{sS(\beta)}2. \tag{2.4}
\]

#### Proof

Data in (2.3) give nonnegative coefficients, tangent balance by definition of
\(\mathcal D\), and normal balance

\[
 \sum_{j\in J}a_j\ell_j+2\sum_{k\in A}a_k
 =q(x)+2\left(1-q(x)/2\right)=2.
\]

Conversely, from a feasible row set \(x_j=a_j\sin\theta_j\). Tangent balance
puts \(x\) in \(\mathcal D\), while the normal equation is
\(q(x)+2\sum_ka_k=2\). This proves every condition in (2.3). Normalizing a
nonzero \(x\) proves (2.4). The separate zero branch is essential when
\(\mathcal B\) is empty. No operation in the proof divides an antipodal
quantity by \(\sin\pi\). \(\square\)

---

## 3. Quantitative strict feasibility and stability

In this section \(J\ne\varnothing\), every \(u_j\) is unit length, and
\(m=|J|\ge1\).

### Theorem 3.1 — equivalence of margins and constructive coefficients

\[
 \rho>0\quad\Longleftrightarrow\quad
 \beta_*>0\quad\Longleftrightarrow\quad
 0\in\operatorname{relint}_U P. \tag{3.1}
\]

If \(\rho>0\), there is \(\beta\in\mathcal B\) satisfying

\[
 \beta_j\ge \frac{\rho}{m(1+\rho)}\qquad(j\in J). \tag{3.2}
\]

A sharper constructive bound is

\[
 \beta_j\ge
 \frac{\rho}{m(\rho+\|\bar u\|)},\qquad
 \bar u=\frac1m\sum_ju_j, \tag{3.3}
\]

when \(\bar u\ne0\); if \(\bar u=0\), take \(\beta_j=1/m\).

#### Proof

A compact convex set contains a positive-radius centered ball in its affine
span exactly when zero is in its relative interior, proving the first and
third conditions equivalent.

For the constructive direction, the supremal ball is attained. Choose
feasible radii \(t_n\uparrow\rho\). If \(\|x\|\le\rho\), then
\((t_n/\rho)x\in P\), and closedness of the compact polytope \(P\) gives
\(x\in P\) on taking the limit. Thus \(\rho B_U\subseteq P\). If
\(\bar u\ne0\), the point

\[
 p=-\rho\bar u/\|\bar u\|
\]

belongs to \(P\). Choose \(\lambda\ge0\), \(\sum_j\lambda_j=1\), with
\(\sum_j\lambda_ju_j=p\), and put

\[
 \tau=\frac{\rho}{\rho+\|\bar u\|},\qquad
 \beta=\tau(1/m,\ldots,1/m)+(1-\tau)\lambda. \tag{3.4}
\]

The two terms in the tangent sum cancel, so \(\beta\in\mathcal B\), and
\(\beta_j\ge\tau/m\), proving (3.3). Here \(m\ge1\) and \(\rho>0\); since
\(\|\bar u\|\le m^{-1}\sum_j\|u_j\|=1\), (3.2) follows. Thus \(\rho>0\)
implies \(\beta_*>0\). Conversely, the independently proved
supporting-hyperplane argument in Theorem 1.1 shows that an all-positive
dependence places zero in the relative interior. \(\square\)

### Theorem 3.2 — exact dual/LP formulas

\[
 \rho=\max\left\{0,
 \min_{\substack{q\in U\\\|q\|=1}}
 \max_{j\in J}q\cdot u_j\right\}. \tag{3.5}
\]

When \(0\in P\), the outer maximum with zero is unnecessary.

When \(\mathcal B\ne\varnothing\), \(\beta_*\) is the attained optimum of

\[
 \begin{array}{ll}
 \text{maximize}&t\\
 \text{subject to}&\sum_j\beta_ju_j=0,\quad
 \sum_j\beta_j=1,\quad \beta_j\ge t\ (j\in J).
 \end{array} \tag{3.6}
\]

Its exact LP dual is

\[
 \begin{array}{ll}
 \text{minimize}&z\\
 \text{subject to}&z-q\cdot u_j\ge0\ (j\in J),\\
 &\sum_j(z-q\cdot u_j)=1,
 \end{array} \tag{3.7}
\]

with \(q\in U\), \(z\in\mathbb R\). Equivalently,
\(z\ge\max_jq\cdot u_j\) and
\(mz-q\cdot\sum_ju_j=1\).

#### Proof

The support function is \(h_P(q)=\max_jq\cdot u_j\). A centered ball of
radius \(t\) lies in \(P\) exactly when
\(t\le h_P(q)\) for every unit \(q\in U\). Taking the largest nonnegative
\(t\) proves (3.5).

Program (3.6) has the same optimum as the definition of \(\beta_*\). Its full
feasible set is not compact because \(t\) may decrease without bound.
Attainment instead follows from compactness of \(\mathcal B\): the continuous
function \(\beta\mapsto\min_j\beta_j\) attains its maximum, and taking
\(t=\min_j\beta_j\) realizes the LP optimum. A member of \(\mathcal B\) with
\(t=0\) is feasible, so the optimum is nonnegative; any feasible pair with
\(t\ge0\) automatically has \(\beta\ge0\). Thus allowing negative coordinates
in the irrelevant \(t<0\) part of (3.6) does not change the optimum.

Attach multipliers \(q\in U\), \(z\in\mathbb R\), and \(\lambda_j\ge0\) to
tangent balance, normalization, and \(\beta_j-t\ge0\). Finiteness of the
Lagrangian supremum requires \(\sum_j\lambda_j=1\) and
\(\lambda_j=z-q\cdot u_j\), exactly (3.7). Finite-dimensional strong duality
applies because the primal is feasible and has a finite attained optimum.
\(\square\)

### Theorem 3.3 — inverse-quadratic rate and coefficient bounds

The displayed upper bound in the task is meaningful only for a positive lower
quasi-uniformity constant.  Positivity was omitted from the literal hypothesis
list; without it the claim is false (take \(c_1<0\) and a balanced pair with
arbitrarily small positive angle).  The exact valid statement is therefore:

Suppose \(0<c_1\le c_2\) and

\[
 L=c_1h\le\theta_j\le c_2h=C,\qquad h>0,\qquad C\le\pi/2. \tag{3.8}
\]

Every \(\beta\in\mathcal B\) satisfies the sharper bounds

\[
 \frac1{\sin^2(C/2)}\le r(\beta)
 \le\frac1{\sin^2(L/2)}, \tag{3.9}
\]

and therefore the requested explicit bounds

\[
 \frac{4\cos^2(C/2)}{C^2}
 \le r(\beta)\le\frac{2\pi}{L^2}. \tag{3.10}
\]

If \(\beta_j\ge\beta_*\) for all \(j\), then

\[
 \frac{\beta_*}{\sin^2(C/2)}
 \le a_j\le
 \frac{1-(m-1)\beta_*}{\sin^2(L/2)}. \tag{3.11}
\]

In particular,

\[
 \frac{4\beta_*}{C^2}\le a_j\le
 \frac{2\pi[1-(m-1)\beta_*]}{L^2}. \tag{3.12}
\]

#### Proof

Monotonicity on \((0,\pi/2]\) gives

\[
 \tan(L/2)\le S(\beta)\le\tan(C/2),\qquad
 \frac1{\sin C}\le\sum_j\frac{\beta_j}{\sin\theta_j}
 \le\frac1{\sin L}.
\]

Insert these inequalities into (1.6) and use
\(2/[\sin x\tan(x/2)]=1/\sin^2(x/2)\) to obtain (3.9).
For the requested lower rate estimate, \(\sin C\le C\) and
\(\tan(C/2)=\sin(C/2)/\cos(C/2)\le C/[2\cos(C/2)]\) give
\(2/[\sin C\tan(C/2)]\ge4\cos^2(C/2)/C^2\).
For the upper estimate, use the original two factors in (1.6):
\(S(\beta)\ge\tan(L/2)\ge L/2\), while concavity gives
\(\sin L\ge2L/\pi\) on \([0,\pi/2]\). Hence
\(r(\beta)\le2\pi/L^2\). Equivalently, the sharper chord bound
\(\sin x\ge(2\sqrt2/\pi)x\) on \([0,\pi/4]\) yields
\(1/\sin^2(L/2)\le\pi^2/(2L^2)<2\pi/L^2\).

For (3.11), apply the same denominator bounds directly to (1.5), and use
\(\beta_j\le1-(m-1)\beta_*\). Finally
\(\sin(C/2)\le C/2\) gives the lower bound in (3.12), while the chord bound
above gives the sharper upper constant \(\pi^2/[2L^2]\), hence the stated
\(2\pi/L^2\) bound. \(\square\)

### Theorem 3.4 — support-function and angular perturbations

Let \(U'=\operatorname{span}\{u'_j:j\in J\}\), let
\(Q:U\to U'\) be a specified linear isometry, and define the transported
directions and pulled-back hull

\[
 \widetilde u'_j=Q^{-1}u'_j,\qquad
 \widetilde P'=Q^{-1}(P')=\operatorname{conv}\{\widetilde u'_j:j\in J\}
 \subseteq U.
\]

When \(U'=U\), the intended default is \(Q=I\). If

\[
 \sup_{\substack{q\in U\\\|q\|=1}}
 |h_{\widetilde P'}(q)-h_P(q)|\le\delta_u<\rho, \tag{3.13}
\]

then

\[
 (\rho-\delta_u)B_U\subseteq\widetilde P',
 \qquad
 (\rho-\delta_u)B_{U'}\subseteq P'. \tag{3.14}
\]

In particular, indexed pointwise bounds
\(\max_j\|\widetilde u'_j-u_j\|\le\delta_u\) imply (3.13). Thus strict feasibility is
preserved, and one may choose

\[
 \beta'_j\ge
 \frac{\rho-\delta_u}
 {m(1+\rho-\delta_u)}. \tag{3.15}
\]

If each direction rotates by at most \(\phi\), then
\(\delta_u\le2\sin(\phi/2)\), so

\[
 \phi<2\arcsin(\rho/2) \tag{3.16}
\]

is an explicit strict-feasibility radius. If also
\(|\theta'_j-\theta_j|\le\eta h\), require

\[
 \eta<c_1,\qquad (c_2+\eta)h\le\pi/2. \tag{3.17}
\]

Then Theorem 3.3 applies with
\(L'=(c_1-\eta)h\), \(C'=(c_2+\eta)h\), and with the coefficient margin in
(3.15). This preserves coefficient positivity and the displayed
inverse-quadratic rate bounds with completely explicit constants.

For a fixed center \(\Omega_i\), suppose each neighbouring node moves by
geodesic distance at most \(\zeta\), and suppose \(U'=U\) with the identity
comparison (for example, both spans equal the full fixed tangent plane). If
\(\zeta\le L/2\), then

\[
 |\theta'_j-\theta_j|\le\zeta,\qquad
 \|u'_j-u_j\|
 \le\frac{4\sin(\zeta/2)}{\sin(L-\zeta)}
 \le\frac{2\zeta}{\sin(L/2)}. \tag{3.18}
\]

Consequently the numerical condition

\[
 \zeta<\min\left\{
 \frac L2,\ \frac\pi2-C,\ \frac\rho2\sin(L/2)
 \right\} \tag{3.19}
\]

preserves strict feasibility. Define

\[
 \widehat\rho=\rho-\frac{2\zeta}{\sin(L/2)}>0,
 \qquad \widehat\beta=
 \frac{\widehat\rho}{m(1+\widehat\rho)},
 \qquad L'=L-\zeta,\quad C'=C+\zeta. \tag{3.20}
\]

The perturbed dependence and row may be chosen with the explicit bounds

\[
 \beta'_j\ge\widehat\beta,\qquad
 \frac{4\cos^2(C'/2)}{(C')^2}\le r'
 \le\frac{2\pi}{(L')^2}, \tag{3.21}
\]

and

\[
 \frac{\widehat\beta}{\sin^2(C'/2)}
 \le a'_j\le
 \frac{1-(m-1)\widehat\beta}{\sin^2(L'/2)}. \tag{3.22}
\]

#### Proof

For compact convex sets in \(U\),
\(d_H(P,\widetilde P')=\sup_{\|q\|=1}|h_P(q)-h_{\widetilde P'}(q)|\). Hence
\(h_{\widetilde P'}(q)\ge(\rho-\delta_u)\|q\|\). The supporting-halfspace
representation of \(\widetilde P'\), followed by applying \(Q\), proves
(3.14). Matching equal convex coefficients
in the two indexed hulls proves the pointwise implication. Theorem 3.1 gives
(3.15). Since unit directions imply \(P\subseteq B_U\), strict feasibility
gives \(0<\rho\le1\), so the arcsine in (3.16) is defined; chord length on
the unit sphere gives the direction bound used there.

For (3.18), write \(u=v/\|v\|\) with
\(v\) the tangent projection of the neighbour. Tangent projection is
nonexpansive, chord distance is \(2\sin(\zeta/2)\), and normalization of two
vectors of norm at least \(\sin(L-\zeta)\) is
\(2/\sin(L-\zeta)\)-Lipschitz. The triangle inequality for spherical
distance gives the radial-angle bound. Since \(2\sin(\zeta/2)\le\zeta\) and
\(\sin(L-\zeta)\ge\sin(L/2)\), the second inequality in (3.18) follows.
Substitution in Theorems 3.1 and 3.3 proves (3.19)--(3.22). \(\square\)

The fixed-span or specified-isometry hypothesis is necessary in lower
dimension. For
\(u_1=e_1,u_2=-e_1\), \(\rho=1\) in \(U=\mathbb Re_1\). The arbitrarily
small perturbation
\(u'_1=(\cos\varepsilon,\sin\varepsilon)\),
\(u'_2=(-\cos\varepsilon,\sin\varepsilon)\) has a hull that misses zero in
the larger ambient plane. Thus “direction motion” must be measured in the
support-function sense appropriate to a fixed or explicitly identified
intrinsic span. If the span changes, (3.18)--(3.22) remain valid only when a
specified \(Q\) gives the transported pointwise bound
\(\max_j\|Q^{-1}u'_j-u_j\|\le2\zeta/\sin(L/2)\); endpoint motion alone does
not imply that bound for an arbitrary \(Q\). A moving center similarly
requires parallel transport between tangent planes followed, when necessary,
by a specified isometry between the transported old span and the new span.

### Theorem 3.5 — local balance matrix and conditioning

Choose orthonormal coordinates \(Q:U\to\mathbb R^d\), \(d=\dim U\). Define
the local balance matrix \(L\in\mathbb R^{(d+1)\times(m+|A|)}\) by

\[
 L_j=\binom{\sin\theta_j\,Qu_j}{1-\cos\theta_j}\quad(j\in J),
 \qquad
 L_k=\binom{0}{2}\quad(k\in A). \tag{3.23}
\]

The complete local equation is

\[
 La=g,\qquad g=(0,\ldots,0,2)^T. \tag{3.24}
\]

Whenever a feasible row exists, \(L\) has full row rank. Let
\(\sigma=\sigma_{\min}(L)>0\). Its Moore--Penrose right inverse satisfies

\[
 R=L^T(LL^T)^{-1},\qquad LR=I,\qquad \|R\|_2=1/\sigma, \tag{3.25}
\]

and

\[
 \kappa_2(L)=\frac{\sigma_{\max}(L)}\sigma
 \le\frac{2\sqrt{m+|A|}}\sigma. \tag{3.26}
\]

If \(L'=L+\Delta L\), \(\|\Delta L\|_2=\varepsilon_L<\sigma\), then

\[
 \sigma_{\min}(L')\ge\sigma-\varepsilon_L,\qquad
 \|L'^\dagger\|_2\le\frac1{\sigma-\varepsilon_L}. \tag{3.27}
\]

For a strictly positive solution \(a^0\), let
\(\alpha=\min_ea^0_e>0\). With a right-side perturbation \(\Delta g\), the
explicit corrected row

\[
 a'=a^0+L'^\dagger(\Delta g-\Delta L\,a^0) \tag{3.28}
\]

solves \(L'a'=g+\Delta g\) and remains strictly positive if

\[
 \frac{\|\Delta g\|_2+\varepsilon_L\|a^0\|_2}
 {\sigma-\varepsilon_L}<\alpha. \tag{3.29}
\]

If the antipodal columns are unchanged, identify the old and new tangent
spans by a specified isometry and express the transported new directions in
the same orthonormal coordinates as the old ones. If
\(\max_j\|\widetilde u'_j-u_j\|\le\delta_u\),
\(\max_j|\theta'_j-\theta_j|\le\delta_\theta\), then

\[
 \|\Delta L\|_2\le\sqrt m
 \sqrt{(\delta_u+\delta_\theta)^2+\delta_\theta^2}. \tag{3.30}
\]

#### Proof

Equation (3.24) is the tangent/normal system by inspection. If
\(A\ne\varnothing\), a row covector \((q,c)\) annihilating every column has
\(2c=0\) from an antipodal column and then \(q\cdot u_j=0\) for all \(j\),
so it is zero. If \(A=\varnothing\), divide the column equation by
\(\sin\theta_j>0\) and average
\(q\cdot u_j+c\tan(\theta_j/2)=0\) against any
\(\beta\in\mathcal B\). This gives \(cS(\beta)=0\), hence \(c=0\), and
then \(q=0\). Thus \(L\) is surjective.

Equations (3.25)--(3.27) are the finite-dimensional singular-value identities
and Weyl inequality. Every column in (3.23) has norm
\(2\sin(\theta/2)\le2\), including the antipodal limit, so
\(\|L\|_2\le\|L\|_F\le2\sqrt{m+|A|}\), proving (3.26). Formula (3.28), the
pseudoinverse identity, and \(\|x\|_\infty\le\|x\|_2\) prove (3.29).
The sine/cosine Lipschitz bounds and a Frobenius estimate prove (3.30).
\(\square\)

---

## 4. Exact global reversible shared-edge theorem

Let \(I\) be finite and nonempty, \(w_i>0\), \(\Omega_i\in S^2\), and let
\(E\) be a simple undirected permitted graph.  As in the local permitted-edge
hypotheses, an edge joins distinct spherical points (it is either
non-antipodal with positive angle or antipodal). Put
\(X=(\mathbb R^3)^I\). For
\(e=\{i,j\}\), define the edge-equilibrium column \(c_e\in X\) by

\[
 (c_e)_i=\Omega_j-\Omega_i,\quad
 (c_e)_j=\Omega_i-\Omega_j,\quad
 (c_e)_k=0\quad(k\notin\{i,j\}). \tag{4.1}
\]

This is independent of the order used to name the endpoints. Let

\[
 A\gamma=\sum_{e\in E}\gamma_ec_e,\qquad
 b_i=-2w_i\Omega_i. \tag{4.2}
\]

Thus the \(i\)-block of \(A\gamma=b\) is exactly

\[
 \sum_{j:\{i,j\}\in E}\gamma_{ij}(\Omega_j-\Omega_i)
 =-2w_i\Omega_i. \tag{4.3}
\]

For \(y=(y_i)\in X\),

\[
 (A^Ty)_{\{i,j\}}
 =(\Omega_j-\Omega_i)\cdot(y_i-y_j). \tag{4.4}
\]

This edge virtual work fixes all subsequent dual signs.

### Theorem 4.1 — cone feasibility, polytopes, and Farkas

Feasibility is equivalent to

\[
 b\in\operatorname{cone}\{c_e:e\in E\}. \tag{4.5}
\]

Exactly one of

\[
 \begin{array}{ll}
 \text{(i)}&A\gamma=b,\quad\gamma\ge0,\\
 \text{(ii)}&A^Ty\ge0,\quad b\cdot y<0
 \end{array} \tag{4.6}
\]

holds.

The feasible set itself is a polytope; consequently its intersection with any
finite linear rate or objective bound is a polytope.  In particular, if
\(c_e>0\) for every edge and \(R<\infty\), then

\[
 \{\gamma\ge0:A\gamma=b,\ c\cdot\gamma\le R\} \tag{4.7}
\]

is a polytope.

#### Proof

Equation (4.5) is the definition of the finitely generated cone. Such a cone
is closed and polyhedral. If (i) holds, then any candidate in (ii) gives
\(b\cdot y=\gamma\cdot A^Ty\ge0\), so both cannot hold. If (i) fails, strong
separation of \(b\) from the closed cone gives a covector nonnegative on every
generator and negative on \(b\), which is exactly (ii). This is the full
finite-dimensional Farkas alternative in the stated sign convention.

Dotting the \(i\)-equilibrium equation with \(-\Omega_i\) gives

\[
 \sum_{j:\{i,j\}\in E}\gamma_{ij}
 (1-\Omega_i\cdot\Omega_j)=2w_i.
\]

Every summand is nonnegative and every permitted-edge loss is strictly
positive.  Hence, for \(e=\{i,j\}\),
\(0\le\gamma_e\le2w_i/(1-\Omega_i\cdot\Omega_j)\).  The feasible set is
therefore a closed bounded polyhedron, hence a polytope. Intersecting it with
any finite linear rate or objective halfspace preserves that conclusion.
The direct estimate \(0\le\gamma_e\le R/c_e\) also proves (4.7), and a node
rate bound gives \(\gamma_e\le R\min(w_i,w_j)\). \(\square\)

### Theorem 4.2 — centering and the complete graph

Weighted centering

\[
 \sum_iw_i\Omega_i=0 \tag{4.8}
\]

is necessary on every graph. On the complete graph it is sufficient, with
the strictly positive conductances

\[
 \gamma_{ij}=\frac{2w_iw_j}{W},
 \qquad W=\sum_kw_k>0. \tag{4.9}
\]

#### Proof

The blocks of every column in (4.1) sum to zero. Summing (4.3) over vertices
therefore gives \(-2\sum_iw_i\Omega_i=0\).

Under (4.8), (4.9) gives

\[
 \begin{aligned}
 \sum_{j\ne i}\gamma_{ij}(\Omega_j-\Omega_i)
 &=\frac{2w_i}{W}\left[
 \sum_{j\ne i}w_j\Omega_j-(W-w_i)\Omega_i\right]\\
 &=\frac{2w_i}{W}[-w_i\Omega_i-(W-w_i)\Omega_i]
 =-2w_i\Omega_i.
 \end{aligned}
\]

Nonemptiness and positivity of the masses give \(W>0\), and every edge factor
in (4.9) is positive. \(\square\)

### Theorem 4.3 — rate, defect, and residual LP duals

For positive edge costs \(c\), the rate/cost LP and its dual are

\[
 \begin{array}{lll}
 (P_c)&\min c\cdot\gamma& A\gamma=b,\ \gamma\ge0,\\
 (D_c)&\max b\cdot y&A^Ty\le c.
 \end{array} \tag{4.10}
\]

If either side has a finite optimum, both optima are attained and equal.
Optimal feasible \(\gamma,y\) obey

\[
 \gamma_e\,[c_e-(A^Ty)_e]=0\qquad(e\in E). \tag{4.11}
\]

Here \(y_i\) is a virtual nodal displacement, \((A^Ty)_e\) is edge work, and
the bracket in (4.11) is reduced edge cost. For weighted total outgoing rate,
\(\sum_iw_ir_i=2\sum_e\gamma_e\), so \(c_e=2\). For unweighted total rate,
\(c_{ij}=1/w_i+1/w_j\). If
\(\epsilon_i=w_i^{-1}\sum_{e\ni i}\gamma_e\ell_e^2\), then
\(\sum_iw_i\epsilon_i=2\sum_e\gamma_e\ell_e^2\), so the exact defect cost is
\(c_e=2\ell_e^2\), \(\ell_e=1-\Omega_i\cdot\Omega_j\).

The peak template

\[
 \min t\quad\text{subject to}\quad
 A\gamma=b,\ C\gamma\le td,\ \gamma\ge0,\ t\ge0 \tag{4.12}
\]

has dual

\[
 \max b\cdot y\quad\text{subject to}\quad
 \lambda\ge0,\ d\cdot\lambda\le1,\ A^Ty\le C^T\lambda. \tag{4.13}
\]

Complementary slackness is

\[
 \begin{aligned}
 &\gamma_e[(C^T\lambda)_e-(A^Ty)_e]=0,\\
 &\lambda_i[td_i-(C\gamma)_i]=0,\\
 &t[1-d\cdot\lambda]=0.
 \end{aligned} \tag{4.14}
\]

For maximum row rate, \(C\) is unsigned incidence and \(d=w\), so edge work
is bounded by \(\lambda_i+\lambda_j\). For maximum degree-two defect,
\(C_{i,e}=\ell_e^2\) on incident edges, so the bound is
\((\lambda_i+\lambda_j)\ell_e^2\). Thus \(\lambda_i\) is exactly the node
peak-budget shadow price.

When equilibrium is infeasible, the residual LP

\[
 \min_{\gamma\ge0}\|A\gamma-b\|_\infty \tag{4.15}
\]

has dual

\[
 \max -b\cdot y\quad\text{subject to}\quad
 A^Ty\ge0,\ \|y\|_1\le1. \tag{4.16}
\]

At optimum,

\[
 \gamma_e(A^Ty)_e=0,\qquad
 y\cdot(A\gamma-b)=\|A\gamma-b\|_\infty. \tag{4.17}
\]

Thus \(y\) is a normalized Farkas/virtual-work residual certificate.

Finally, for a defect target \(C\gamma\approx d\) under exact equilibrium,

\[
 \min\|C\gamma-d\|_\infty
 \quad\text{subject to}\quad A\gamma=b,\ \gamma\ge0 \tag{4.18}
\]

has dual

\[
 \max b\cdot y-d\cdot z\quad\text{subject to}\quad
 \|z\|_1\le1,\ C^Tz-A^Ty\ge0, \tag{4.19}
\]

with edge complementary slackness

\[
 \gamma_e[(C^Tz)_e-(A^Ty)_e]=0, \tag{4.20}
\]

and the norm-block/subgradient identity

\[
 z\cdot(C\gamma-d)=\|C\gamma-d\|_\infty. \tag{4.20a}
\]

Consequently \(\|z\|_1=1\) whenever the residual is nonzero. The vector \(z\)
is the signed normalized residual mode: (4.20a) says it exposes the attained
residual face. The vector \(y\) retains its equilibrium virtual-displacement
interpretation.

#### Strong-duality transfer

Equations (4.10), (4.12), (4.15), and (4.18) are finite-dimensional linear
programs after introducing the usual nonnegative epigraph/slack variables.
The finite LP duality theorem applies verbatim: if one side has a feasible
finite optimum, both optima are attained and equal. This is Corollary 7.1g of
A. Schrijver, *Theory of Linear and Integer Programming*, Wiley, 1986; an
openly accessible equivalent statement and proof is the University of
Washington’s [Strong Duality Theorem](https://sites.math.washington.edu/~burke/crs/407/lectures/L9-strong-duality.pdf).
Writing the zero duality gap as a sum of products of nonnegative primal
variables and dual slacks gives (4.11), (4.14), (4.17), (4.20), and (4.20a).
The signs also follow directly from (4.4). This transfers both strong duality
and complementary slackness, rather than only weak certificate soundness.

### Theorem 4.4 — exact local-but-not-global obstruction

Take four equatorial nodes

\[
 \Omega_1=(1,0,0),\quad \Omega_2=(0,1,0),\quad
 \Omega_3=(-1,0,0),\quad \Omega_4=(0,-1,0), \tag{4.21}
\]

the cycle \(E=\{12,23,34,41\}\), and masses

\[
 (w_1,w_2,w_3,w_4)=(1,2,1,2). \tag{4.22}
\]

The masses are centered. Every node has a strictly positive local exact row:
assign coefficient one to each of its two permitted neighbours. Nevertheless
the shared-edge system is infeasible.

An exact Farkas certificate is

\[
 y_i=s_i\Omega_i,\qquad (s_1,s_2,s_3,s_4)=(-1,1,-1,1). \tag{4.23}
\]

For every cycle edge, \(s_j=-s_i\), hence

\[
 (A^Ty)_{ij}
 =(\Omega_j-\Omega_i)\cdot s_i(\Omega_i+\Omega_j)=0, \tag{4.24}
\]

where adjacent nodes are orthogonal. But

\[
 b\cdot y=-2\sum_iw_is_i
 =-2(-1+2-1+2)=-4<0. \tag{4.25}
\]

Thus (4.23) satisfies alternative (ii). Directly, node 1 forces
\(\gamma_{12}=\gamma_{14}=1\), while node 2 forces
\(\gamma_{12}=\gamma_{23}=2\).

This is the smallest connected simple obstruction after imposing the
necessary centering condition: two centered locally feasible nodes are an
equal-mass antipodal pair and glue globally; a connected three-node graph is
either complete, where Theorem 4.2 applies, or a path whose locally feasible
endpoints are both antipodal to the middle and whose centered masses glue.
Without centering, the two-node antipodal edge with masses \((1,2)\) is the
absolute smallest sanity-check obstruction, detected by
\(y_1=y_2=-\Omega_1\).

### Theorem 4.5 — equivariant averaging reconciliation

Let a finite group \(G\) act on \(I\) by graph automorphisms, transitively on
vertices and on unordered edges. Suppose there is an orthogonal
representation \(R_g\in O(3)\) such that

\[
 \Omega_{gi}=R_g\Omega_i,\qquad w_{gi}=w_i. \tag{4.26}
\]

Let oriented local conductances \(q^0_{ij}=w_i a^0_{ij}\ge0\) be supported on
permitted orientations and satisfy

\[
 \sum_{j:\{i,j\}\in E}q^0_{ij}(\Omega_j-\Omega_i)
 =-2w_i\Omega_i. \tag{4.27}
\]

Define the orbit average

\[
 \bar q_{ij}=\frac1{|G|}\sum_{g\in G}
 q^0_{g^{-1}i,g^{-1}j}. \tag{4.28}
\]

If \(\bar q_{ij}=\bar q_{ji}\) for one representative of every unordered
edge orbit, then this equality holds on every edge and
\(\gamma_{\{i,j\}}=\bar q_{ij}\) solves \(A\gamma=b\). If every oriented
starting value on a permitted edge is positive, then every \(\gamma_e>0\).

#### Proof

For each \(g\), apply \(R_g\) to (4.27) at \(g^{-1}i\), put
\(j=gk\), and use (4.26). This gives the \(i\)-row equilibrium equation for
the relabelled conductance \(q^0_{g^{-1}i,g^{-1}j}\). Averaging therefore
preserves (4.27). Formula (4.28) is \(G\)-invariant. Equality of the two
orientations on each edge-orbit representative propagates to every edge. The
common value is one undirected conductance and the averaged row equations are
precisely (4.3). An average of positive values is positive. \(\square\)

This theorem is nontrivial beyond complete graphs. On the equal-mass square
cycle (4.21), take \(q^0_{ij}=1\) on each permitted orientation and zero off
the permitted orientations, and let the cyclic rotation group act. It is
vertex- and edge-transitive, the averaged orientations agree, and
\(\gamma_e=1\) is a globally strictly feasible shared solution.

### Theorem 4.6 — global strict-feasibility perturbation

Let \(A\gamma^0=b\) with

\[
 \eta=\min_e\gamma^0_e>0. \tag{4.29}
\]

For perturbed data \(A',b'\), suppose \(A'\) has positive rank and
\(r'=b'-A'\gamma^0\in\operatorname{range}A'\). Then

\[
 \gamma'=\gamma^0+A'^\dagger r' \tag{4.30}
\]

solves \(A'\gamma'=b'\), and

\[
 \min_e\gamma'_e\ge
 \eta-\frac{\|r'\|_2}{\sigma_+(A')}, \tag{4.31}
\]

where \(\sigma_+(A')\) is the smallest positive singular value. If, in
addition, \(\operatorname{rank}A'=\operatorname{rank}A\),
\(\varepsilon_A=\|A'-A\|_2<\sigma_+(A)=\sigma\), and
\(\varepsilon_b=\|b'-b\|_2\), then

\[
 \min_e\gamma'_e\ge
 \eta-
 \frac{\varepsilon_b+\varepsilon_A\|\gamma^0\|_2}
 {\sigma-\varepsilon_A}. \tag{4.32}
\]

The right side is positive whenever the displayed quotient is smaller than
\(\eta\). On \(\operatorname{range}A\),

\[
 \|A^\dagger\|_2=1/\sigma,\qquad
 \kappa_{\mathrm{range}}(A)=\|A\|_2/\sigma. \tag{4.33}
\]

These are the explicit right-inverse and conditioning inequalities.

For a node/mass perturbation on the same graph, set
\(d_i=\Omega_i'-\Omega_i\),
\(\delta_\Omega=\max_i\|d_i\|\), and
\(\Delta w=w'-w\). If \(n=|I|\), \(M=|E|\), then

\[
 \varepsilon_A\le2\sqrt{2M}\,\delta_\Omega,\qquad
 \varepsilon_b\le2(\|\Delta w\|_2+\|w\|_2\delta_\Omega). \tag{4.34}
\]

For a completely geometric sufficient radius, assume the embedded bar
framework \((E,\Omega)\) is infinitesimally rigid in \(\mathbb R^3\):

\[
 \ker A^T=\{y:y_i=t+K\Omega_i, t\in\mathbb R^3, K^T=-K\}, \tag{4.35}
\]

and choose noncollinear nodes \(p,q,r\). Then the rigid-motion space has
dimension six and \(\operatorname{rank}A=3n-6\). Let

\[
 \nu=\sigma_{\min}[\Omega_q-\Omega_p,\ \Omega_r-\Omega_p]>0. \tag{4.36}
\]

Require the perturbed nodes to remain unit length and exactly weighted
centered. If
\(\delta_\Omega\le\tau\), \(\max_i|\Delta w_i|\le\tau\), define

\[
 C_A=2\sqrt{2M},\qquad
 C=2(\sqrt n+\|w\|_2)+C_A\|\gamma^0\|_2. \tag{4.37}
\]

Then the explicit radius

\[
 \tau<\min\left\{
 w_{\min},\ \frac\nu{2\sqrt2},\
 \frac{\eta\sigma}{C+\eta C_A}
 \right\} \tag{4.38}
\]

preserves positive masses, infinitesimal-rigidity rank, and a strictly
positive shared solution.

#### Proof

The pseudoinverse maps \(r'\in\operatorname{range}A'\) to a correction whose
norm is at most \(\|r'\|/\sigma_+(A')\), proving (4.30)--(4.31). Weyl's
singular-value inequality and
\(\|r'\|\le\varepsilon_b+\varepsilon_A\|\gamma^0\|\) prove (4.32).

Each perturbed edge column has norm change
\(\sqrt2\|d_j-d_i\|\); summing squared column bounds gives the first estimate
in (4.34). The identity
\(w_i'\Omega_i'-w_i\Omega_i=\Delta w_i\Omega_i'+w_i d_i\) gives the second.

Translations and rotations are always in \(\ker A'^T\). The bound
\(\tau<\nu/(2\sqrt2)\) preserves noncollinearity. The last bound in (4.38)
implies \(C_A\tau<\sigma\), so Weyl forces
\(\operatorname{rank}A'\ge3n-6\); the six-dimensional perturbed rigid-motion
kernel forces the reverse inequality. Thus the rank remains \(3n-6\), and the
kernel consists exactly of rigid motions. Exact perturbed centering makes
\(b'\) orthogonal to translations, while
\(\Omega_i'\cdot K\Omega_i'=0\) makes it orthogonal to rotations. Hence
\(b'\in\operatorname{range}A'\), providing the compatibility required by
(4.30). Finally (4.34) gives
\(\|r'\|\le C\tau\), and
\(C\tau/(\sigma-C_A\tau)<\eta\) is exactly the last inequality in (4.38).
\(\square\)

Arbitrary perturbations cannot omit compatibility: breaking weighted
centering makes feasibility impossible. Rank-changing flexible frameworks
also require a fresh \(\sigma_+(A')\) bound. For angular node motion at most
\(\alpha\), use
\(\delta_\Omega=2\sin(\alpha/2)\le\alpha\) in (4.34)--(4.38), together with
the same numerical bound on the mass perturbation.

---

## 5. Exact examples and claim control

Take orthonormal tangent vectors \(e_1,e_2\).

| Required position/feature | Exact data | Conclusion |
|---|---|---|
| outside hull | \(J=(e_1,e_2)\) | no non-antipodal row |
| boundary | \(u=(e_1,-e_1,e_2)\), all \(\theta=\pi/3\) | \(\mathcal B=\{(1/2,1/2,0)\}\), \(a=(2,2,0)\), \(\rho=\beta_*=0\) |
| lower-dimensional strict | \(u=(e_1,-e_1)\), \(\theta=\pi/3\) | \(U=\mathbb Re_1\), \(\rho=1\), \(\beta_*=1/2\), \(a=(2,2)\) |
| full-dimensional strict | three directions at angles \(0,2\pi/3,4\pi/3\), \(\theta=\pi/3\) | \(\rho=1/2\), \(\beta_*=1/3\), \(a_j=4/3\), \(r=4\) |
| repeated direction | \(u=(e_1,-e_1,e_2,-e_2,e_1)\), \(\theta_1=\pi/4\), others \(\pi/3\) | \(\beta=(1/6,1/3,1/6,1/6,1/6)\) is positive; (1.5) gives the exact row |
| antipodes only | two antipodal indices | rows \((t,1-t)\), \(0\le t\le1\) |
| mixed outside | \(J=(e_1)\), one antipode | unique non-antipodal coefficient zero; antipodal coefficient one |
| mixed boundary | \(J=(e_1,-e_1,e_2)\), \(\theta=\pi/3\), one antipode | \(a=(1,1,0;1/2)\), feasible but never fully strict |
| mixed interior | \(J=(\pm e_1,\pm e_2)\), \(\theta=\pi/3\), one antipode | \(a_j=1/2\) on \(J\), \(a_k=1/2\), fully strict |
| boundary crossing | replace \(e_1,-e_1\) by \((\cos\varepsilon,\sin\varepsilon),(-\cos\varepsilon,\sin\varepsilon)\) in the boundary example | every generator has positive \(e_2\)-component; zero leaves the hull for every \(\varepsilon>0\) |
| robust strict hull | \(P=\operatorname{conv}\{\pm e_1,\pm e_2\}\) | \(\rho=1/\sqrt2\); support perturbations below \(1/\sqrt2\) retain strict feasibility |
| local not global | centered unequal-mass square (4.21)--(4.25) | every local row strict; exact Farkas obstruction |
| global symmetric strict | equal-mass square cycle with cyclic action | \(\gamma_e=1\), reconciliation by Theorem 4.5 |

For the repeated-direction row, put

\[
 S=\frac{(\sqrt2-1)+5/\sqrt3}{6}.
\]

Then
\(a_1=\sqrt2/(3S)\),
\(a_2=4/(3\sqrt3S)\), and
\(a_3=a_4=a_5=2/(3\sqrt3S)\), directly certifying that indexed repetition
does not affect the theorem.

Computational scripts in `pure_math/examples/` evaluate these exact formulas
as regression checks only. The proofs above, not finite enumeration, establish
the theorem package.

## 6. Separation of standard and sphere-specific inputs

Standard finite-dimensional inputs are: convex-hull barycentric
representation, supporting-hyperplane separation, compact-convex support
duality, Farkas' lemma, finite LP strong duality/complementary slackness, and
singular-value perturbation inequalities. Sphere-specific results are:

- the tangent/normal decomposition and identity (0.1);
- the unique spherical normal rescaling (1.5) and rate formula (1.6);
- the no-division antipodal splitting (2.3);
- the angle-explicit inverse-square constants and tangent-direction radius;
- the shared-edge equilibrium columns (4.1), their weighted centering
  obstruction, and the factor \(2/W\) complete-graph construction;
- the centered local-but-not-global spherical cycle certificate; and
- the equivariant reconciliation criterion for oriented local conductances.

No novelty claim is attached to the standard convex or LP alternatives alone.

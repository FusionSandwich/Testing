# P1E probabilistic / convex route: quantitative no-go audit

## Status

**BLOCKED AS AN UNSTRUCTURED CONSTRUCTION ROUTE.** Random local sampling and
finite-dimensional rowwise Slater estimates do not, by themselves, prove the
P1E upper theorem. The obstruction is quantitative rather than merely a
dimension count:

1. a bounded number of random tangent directions has an order-one covariance
   defect and a fixed positive probability of failing the local moment cone;
2. a local shared-edge equilibrium map has a degree-one spherical field whose
   adjoint strain is only \(O(h^2)\), so every global reconciliation theorem
   necessarily contains an \(h^{-2}\) inverse (or the corresponding diameter
   or spectral-gap factor); and
3. even exact positive first-harmonic reproduction on a quasiuniform random or
   irregular mesh does not upgrade variational consistency to the required
   pointwise \(O(h^2)\) quadratic residual.

These statements do **not** prove that a specially correlated random
construction or a globally certified moment-cone solution is impossible.
They prove that the commonly proposed argument -- fixed-degree random Rips
stars, concentration, rowwise positive reweighting, and an unquantified
shared-edge correction -- cannot supply the missing theorem. Any successful
convex route must add a structured exact local moment law and an explicit
global inverse estimate. That is theorem-strength information, not an
automatic consequence of quasiuniformity.

Throughout, \(n=d-1\), \(x_i\in S^n\),

\[
 \tau_{ij}=P_i x_j,\qquad
 \ell_{ij}=1-x_i\cdot x_j,\qquad
 P_i=I-x_ix_i^T,
\]

and every permitted edge has angular length at most \(\Lambda h\).

## 1. Fixed-degree random stars do not concentrate at order \(h^2\)

Let \(u_1,\ldots,u_m\) be independent uniform directions on \(S^{n-1}\)
and put

\[
 S_m=\frac n m\sum_{k=1}^m u_ku_k^T,\qquad
 Q_m=S_m-I_n .                                      \tag{1.1}
\]

### Proposition 1.1 (exact covariance floor)

For \(n\ge2\),

\[
 \mathbb E Q_m=0,\qquad
 \mathbb E\|Q_m\|_F^2=\frac{n(n-1)}m .              \tag{1.2}
\]

Indeed, \(X=uu^T\) satisfies

\[
 \mathbb EX=I_n/n,\qquad
 \|X\|_F^2=\operatorname{tr}X^2=1,\qquad
 \|\mathbb EX\|_F^2=1/n.
\]

Independence then gives

\[
 \mathbb E\left\|\frac n m\sum_k
       (X_k-\mathbb EX_k)\right\|_F^2
 =\frac{n^2}{m}(1-1/n),
\]

which is (1.2). Consequently raw random-kernel averaging cannot make the
normalized tangent covariance \(O(h^2)\) in root mean square unless

\[
 m\ge \frac{n(n-1)}{C^2h^4}                       \tag{1.3}
\]

when the requested bound is \(\|Q_m\|_{L^2}\le Ch^2\). In particular,
bounded degree cannot supply the P1E order by a law-of-large-numbers argument.

There is a second, qualitative obstruction that applies also to exact local
reweighting. Fix \(e\in S^{n-1}\) and a cap

\[
 K=\{u:u\cdot e\ge c\},\qquad c>1/\sqrt n.
\]

The event \(u_1,\ldots,u_m\in K\) has probability
\(p_{n,m}=\sigma(K)^m>0\). On this event no nonzero nonnegative weights can
have zero first moment, and no normalized nonnegative weights can have
isotropic second moment: with \(A=ee^T-I_n/n\),

\[
 \sum_kp_k u_k\cdot e>0,\qquad
 \left\langle A,\sum_kp_ku_ku_k^T\right\rangle
 \ge c^2-1/n>0.                                   \tag{1.4}
\]

Thus a fixed-size independent random star has a fixed positive probability of
failing even the **rowwise** strict moment cone. For \(K_h\) independent
stars the probability that every star is feasible is at most
\((1-p_{n,m})^{K_h}\). If \(K_h\asymp h^{-n}\), this tends to zero for fixed
\(m\). Suppressing this particular bad event already needs
\(m\gtrsim\log(1/h)\); obtaining the uncorrected \(O(h^2)\) covariance by
(1.2) needs the much larger scale (1.3).

This calculation is deliberately for the ideal independent-star model. A
maximal-net or hard-core process introduces dependencies, so (1.4) is not
silently transferred to it as an independence theorem. What survives
unchanged is the main logical point: fixed-degree concentration is unavailable;
one must prove a deterministic, correlated moment-frame condition.

### Corollary 1.2 (sampling-kernel tradeoff)

For a quasiuniform cloud with fill scale \(h\), a kernel of angular bandwidth
\(\varepsilon\) samples \(m\asymp(\varepsilon/h)^n\) neighbors. A raw positive
radial kernel has truncation error \(O(\varepsilon^2)\). Requiring that error
to be \(O(h^2)\) forces \(\varepsilon=O(h)\), hence \(m=O(1)\); (1.2) then
leaves an order-one random normalized covariance defect. Increasing the
bandwidth to obtain concentration makes both the angular-window constant and
the degree grow, and the truncation error is no longer \(O(h^2)\). Exact
moment reweighting can evade the covariance calculation, but only by solving
the local cone and then the genuinely global shared-edge problem.

## 2. A universal low-frequency obstruction to uniform reconciliation

Let \(E_h\) be an undirected local graph and define the shared tangent-force
map

\[
 (T_h\gamma)_i=\sum_{j:ij\in E_h}\gamma_{ij}\tau_{ij}.           \tag{2.1}
\]

For tangent vertex fields \(u_i\in T_{x_i}S^n\), its algebraic adjoint has
edge coefficient

\[
 (T_h^*u)_{ij}=u_i\cdot\tau_{ij}+u_j\cdot\tau_{ji}.              \tag{2.2}
\]

### Proposition 2.1 (exact degree-one adjoint identity)

For a fixed \(a\in\mathbb R^{n+1}\), set \(u_i=P_i a\). Then, on every edge,

\[
 (T_h^*u)_{ij}
   =\ell_{ij}\,a\cdot(x_i+x_j).                                  \tag{2.3}
\]

This follows by expanding the two terms in (2.2); no asymptotics are used.
Since \(\ell_{ij}\le\theta_{ij}^2/2\), the angular window gives

\[
 \|T_h^*u\|_{\ell^\infty(E_h)}
 \le \Lambda^2h^2\|a\|.                                         \tag{2.4}
\]

The exact kernel of \(T_h^*\) contains infinitesimal rotations
\(u_i=Ax_i\), \(A^T=-A\). The field \(P_i a\) is not a disguised rotation.
For example, assume the node set is antipodally symmetric and has spherical
fill distance at most \(h\). Choose a node \(x\) within \(h\) of a unit
vector perpendicular to \(a\). For every skew \(A\), the errors at the
antipodal pair are

\[
 P_xa-Ax,\qquad P_xa+Ax,
\]

and hence

\[
 \inf_{A^T=-A}\max_i\|P_i a-Ax_i\|
 \ge\|P_xa\|\ge\cos(h)\|a\|.                                  \tag{2.5}
\]

Combining (2.4)--(2.5), the adjoint inf-sup constant off rotations is at most

\[
 \beta_h\le\frac{\Lambda^2h^2}{\cos h}.                         \tag{2.6}
\]

In the \(\ell^1\)-primal/\(\ell^\infty\)-dual operator norms, every right
inverse for shared tangent-force reconciliation therefore has norm at least

\[
 \beta_h^{-1}\ge\frac{\cos h}{\Lambda^2h^2}.                    \tag{2.7}
\]

The same upper bound applies to any larger first/second/third shared moment
operator, by setting all dual variables except the tangent-force field to
zero. Thus neither a finite local clique rank calculation nor a rowwise
Slater margin can imply an \(h\)-uniform global correction. A valid theorem
must expose the \(h^{-2}\) factor (equivalently, after rescaling, its spectral
gap/diameter/overlap constants) and must prove that the residual being
corrected is two powers of \(h\) smaller in precisely this low mode.

Equation (2.3) is not a Farkas certificate that the homogeneous equilibrium
cone is empty. Positive polar/Delaunay stresses show that such a cone can be
nonempty. It is a decisive obstruction to the proposed **uniform**
Slater-to-global-correction inference.

## 3. Exact \(H_1\) plus positivity still permits an \(O(h)\) defect

The one-dimensional alternating-gap family is an all-level deterministic
failure case for the idea that an exact positive equilibrium and a
second-order energy estimate automatically imply the pointwise quadratic
bound. On \(S^1\), let consecutive angular gaps alternate between

\[
 \alpha=s(1+\rho),\qquad
 \beta=s(1-\rho),\qquad 0<\rho<1,
\]

and give an edge spanning a gap \(g\) shared conductance \(1/\sin g\).
The tangent forces cancel exactly, so after the normal mass normalization the
generator is positive, reversible, and reproduces \(H_1\) exactly. Direct
evaluation on the degree-two complex harmonic gives

\[
 \mathfrak D_2=\sqrt{A^2+B^2},                                   \tag{3.1}
\]

\[
 A=4[1-\cos(\rho s)\cos(\alpha/2)\cos(\beta/2)],\qquad
 B=-4\cos(\alpha/2)\cos(\beta/2)\sin(\rho s).                    \tag{3.2}
\]

Therefore

\[
 \lim_{s\downarrow0}\frac{\mathfrak D_2}{s}=4\rho.               \tag{3.3}
\]

The mesh ratio is \((1+\rho)/(1-\rho)\), the degree is two, the angular
window is explicit, and all conductances are positive. The defect is still
only first order. This is also a model for a fixed-amplitude random jitter:
rescaled local asymmetry does not shrink with \(h\), so exact force balance
does not manufacture the missing odd-moment cancellation.

### Proposition 3.1 (exact Gordan certificate for the local full-moment cone)

The same alternating mesh is a literal obstruction to deriving the stronger
shared moment cone from fill, separation, mesh ratio, bounded degree, and a
fixed angular window. Restrict the graph to the two consecutive neighbors.
At a vertex whose right and left gaps are \(\alpha\ne\beta\), the tangent and
loss--tangent columns, after choosing the positive tangent orientation, are

\[
 c_R=\sin\alpha\,(1,\ell_\alpha),\qquad
 c_L=-\sin\beta\,(1,\ell_\beta),\qquad
 \ell_g=1-\cos g.                                  \tag{3.4}
\]

Assume \(\alpha>\beta\), so \(\ell_\alpha>\ell_\beta\), and set

\[
 y=\left(-\frac{\ell_\alpha+\ell_\beta}{2},1\right).             \tag{3.5}
\]

Then

\[
 y\cdot c_R
 =\frac{\sin\alpha}{2}(\ell_\alpha-\ell_\beta)>0,\qquad
 y\cdot c_L
 =\frac{\sin\beta}{2}(\ell_\alpha-\ell_\beta)>0.                 \tag{3.6}
\]

Gordan's alternative therefore certifies that no nonzero nonnegative pair of
edge weights can satisfy both local equations. Equivalently, tangent
equilibrium first gives
\(\gamma_R\sin\alpha=\gamma_L\sin\beta>0\), whereas the mixed equation would
then require \(\ell_\alpha=\ell_\beta\).

This is an all-level quasiuniform family with fixed mesh ratio and a positive
shared exact-\(H_1\) stress, yet the commonly proposed exact first/third local
moment cone is empty on the nearest-neighbor graph. Enlarging the stencil can
remove this particular certificate (indeed a carefully designed multi-hop
connector can do so), which is precisely why the degree, angular window, and
connector law must be explicit rather than hidden in a generic Rips-graph
claim.

## 4. What would make a convex/probabilistic proof complete

A future convex route would be unconditional if it supplied all of the
following, with the stated scalings:

1. a deterministic all-level node law with fill \(Hh\), separation \(qh\),
   bounded degree \(D\), and angular window \([\lambda h,\Lambda h]\);
2. one **shared**, strictly positive conductance vector, not independent row
   weights;
3. either the exact shared moment equations

   \[
   \sum_j\gamma_{ij}\tau_{ij}=0,\quad
   \sum_j\gamma_{ij}\ell_{ij}\tau_{ij}=0,\quad
   \sum_j\gamma_{ij}
      \left(\tau_{ij}\tau_{ij}^T
             -\frac{\|\tau_{ij}\|^2}{n}P_i\right)=0,
   \]

   or explicit \(O(h^{n+2})\) unnormalized defects at every vertex;
4. a global inf-sup/Korn estimate consistent with (2.6), including its
   \(h^{-2}\), graph-gap, diameter, and overlap dependence;
5. a positivity calculation showing that the correction is smaller than the
   active-edge margin after that inverse loss; and
6. a deterministic sampling-quotient lower bound.

The fixed-degree random-net argument supplies none of items 2--5. Increasing
the number of kernel samples supplies concentration only by violating the
fixed-degree/angular-window regime. Consequently this route remains
**BLOCKED** unless a structured correlated microgeometry or an equally strong
global moment-cone theorem is added. Such an added theorem would contain the
substance of the P1E construction and may not be called a routine Slater or
Farkas step.

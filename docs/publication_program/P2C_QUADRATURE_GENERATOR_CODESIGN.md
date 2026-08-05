# P2C — Controlled quadrature–generator co-design

## Resolution and scope

This stage gives a complete controlled extension of the accepted P2A fixed-node design.  It supplies:

1. an exact globally optimal inner semidefinite program for reversible nonnegative conductances on fixed nodes, masses, and graph;
2. six independent outer strategies, with the precise hypotheses under which feasibility, invariance, descent, existence, subsequential convergence, and stationarity hold;
3. positive-mass admission rules and common diagnostics for product, level-symmetric, Lebedev, Ahrens–Beylkin icosahedral, spherical-design, maximal-net, Delaunay, and locally adapted families;
4. an all-level quadratic convergence theorem inherited from the accepted Paper-I P1B/P1E frontier, with explicit constants;
5. rotation tests that distinguish collision/angular-diffusion orientation error, joint covariance, streaming rays, and interpolation remedies; and
6. executable, symbolic, interval-ready, and hostile regression audits.

The outer node problem is nonconvex.  This stage does **not** claim that a local Riemannian, alternating, graph-neighborhood, or adaptive method finds a global outer optimum.  The only global optimization claim is the fixed-candidate inner conic problem and, in the theoretical orbit-proximal baseline, the explicitly stated proximal subproblem.

The normalization is the accepted P2A normalization: surface measure has total mass one, the discrete generator \(L\) is negative semidefinite, and \(-\Delta_{\mathbb S^{d-1}}\) has eigenvalues
\[
\lambda_\ell=\ell(\ell+d-2).
\]
The implementation specializes to \(\mathbb S^2\), where \(\lambda_1=2\) and \(\lambda_2=6\).

## 1. Frozen operator and exact shell defect

Let \(X=(x_i)_{i=1}^N\subset\mathbb S^{d-1}\), let \(w_i>0\), \(\sum_iw_i=1\), and let \(E\) be a labelled undirected graph.  Give every unoriented edge \(e=\{i,j\}\) a shared conductance \(c_e\ge0\).  With an oriented incidence matrix \(B\), \(C=\operatorname{diag}(c)\), and \(W=\operatorname{diag}(w)\), define
\[
 L(c)=-W^{-1}B^\top C B,\qquad
 (Lf)_i={1\over w_i}\sum_{j:\{i,j\}\in E}c_{ij}(f_j-f_i).
\]
Then
\[
 \langle f,-Lf\rangle_W
   =\sum_{\{i,j\}\in E}c_{ij}(f_i-f_j)^2\ge0,
 \qquad L{\bf1}=0,
\]
and detailed balance is exact: \(WL=L^\top W\).  Exact first-shell action is the affine equality
\[
 B^\top C B X=\lambda_1WX. \tag{1}
\]

For a fixed continuum-\(L^2\)-orthonormal real basis of \(\mathcal H_\ell\), let
\(S_\ell(X)\in\mathbb R^{N\times q_\ell}\) be its sampled values and put
\[
 G_\ell=S_\ell^\top WS_\ell,\quad
 R_\ell=(L+\lambda_\ell I)S_\ell,\quad
 Z_\ell=W^{1/2}R_\ell.
\]
The sampling-correct, full residual defect is
\[
 \mathfrak D_\ell
 =\sup_{a^\top G_\ell a=1}\|R_\ell a\|_W, \tag{2}
\]
with the convention that the value is finite only when
\(\ker G_\ell\subseteq\ker Z_\ell\).  This definition retains residual leakage outside the sampled harmonic range.  A compression followed by an uncorrected Euclidean pseudoinverse is not used.

### Theorem 1 — raw moving-Gram epigraph

For fixed \(X,w,E\), \(c\), and \(t\ge0\), the inequality
\(\mathfrak D_\ell\le t\) is equivalent to
\[
 \begin{pmatrix}
   tG_\ell&Z_\ell^\top\\
   Z_\ell&tI_N
 \end{pmatrix}\succeq0. \tag{3}
\]

**Proof.**  If \(t>0\), the Schur complement of the lower-right block is
\(tG_\ell-t^{-1}Z_\ell^\top Z_\ell\succeq0\), equivalently
\[
 \|Z_\ell a\|_2^2\le t^2a^\top G_\ell a
\]
for every coefficient vector \(a\).  This inequality both forces
\(Z_\ell\ker G_\ell=0\) and gives (2) on the positive sampling range.  Conversely, those two properties give the quadratic inequality and hence (3).  If \(t=0\), positivity of the block matrix forces \(Z_\ell=0\), which is exactly zero defect. ∎

Unlike a prewhitened formula, (3) remains a raw coefficient-space statement at a sampling kernel.  In an outer derivative, both \(t\,dG_\ell\) and \(dZ_\ell\) must be retained.

## 2. Exact inner problem

For fixed \(X,w,E\), choose selected shells \(\mathcal L\), nonnegative coefficients \(\alpha_\ell\), a rate cap \(R\), and an optional closed active-support floor \(\underline c_e\ge0\).  The inner problem is
\[
\begin{array}{ll}
\operatorname{minimize}_{c,t}&
   \sum_{\ell\in\mathcal L}\alpha_\ell t_\ell\\
\operatorname{subject\ to}&
   B^\top\operatorname{diag}(c)BX=\lambda_1WX,\\
& c_e\ge\underline c_e,\\
& \sum_{e\ni i}c_e\le Rw_i,\quad i=1,\dots,N,\\
& \begin{pmatrix}t_\ell G_\ell&Z_\ell(c)^\top\\
                  Z_\ell(c)&t_\ell I\end{pmatrix}\succeq0,
      \quad\ell\in\mathcal L .
\end{array} \tag{4}
\]
Higher-shell maxima, convex response surrogates, and affine normalizations can be added with epigraph LMIs or second-order cones.

### Theorem 2 — global inner optimality and attainment

Problem (4) is a convex semidefinite program.  If it is feasible, its minimum is attained and every returned optimum is globally optimal for the declared fixed \(X,w,E\).

**Proof.**  All equalities and scalar inequalities are affine in \(c,t\); each block in (3) is affine because \(G_\ell\) is fixed during the inner solve.  The rate cap bounds each \(c_e\).  Alternatively, if selected edge chord lengths are bounded below by \(\rho>0\), taking the trace of (1) gives the exact identity
\[
 \sum_{\{i,j\}\in E}c_{ij}\|x_i-x_j\|^2=\lambda_1, \tag{5}
\]
which bounds conductances.  A feasible objective sublevel is therefore closed and bounded, so the continuous objective attains its minimum.  Convexity makes every attained minimum global. ∎

Strict inequalities \(c_e>0\) are open and need not attain an infimum.  “Positive conductance” therefore means \(c_e\ge0\) on a master graph, or \(c_e\ge c_{\min}>0\) on a declared active support.  An invariant secondary strictly convex minimization on the certified optimal face gives a deterministic choice when the primary optimum is nonunique.

## 3. Common family definitions and admission gates

Every family is converted to normalized positive masses, an intrinsic permitted graph, and the same diagnostics.  No tabulated rule is admitted from its name alone.

| Family | Positive masses | Permitted graphs | Exactness/admission gate |
|---|---|---|---|
| Product | Gauss–Legendre polar weight \(q_a/(2n_\phi)\) at every azimuth | tensor grid plus declared diagonals, weak spherical Delaunay, radius, \(k\)-NN, complete | audit tensor exactness, seam convention, positivity |
| Level-symmetric | positive orbit mass divided by orbit size | orbit-distance, weak Delaunay, complete | exact mass sum, every orbit mass \(>0\), advertised moments |
| Lebedev | positive octahedral orbit mass divided by orbit size | orbit-distance, weak Delaunay, complete | each individual rule passes exact/outward moment and positivity audit |
| Ahrens–Beylkin | positive icosahedral orbit mass divided by orbit size | orbit-distance, weak Delaunay, complete | invariant-polynomial exactness and independent mass positivity |
| Spherical \(t\)-design | equal mass \(1/N\) | weak Delaunay, radius, \(k\)-NN, complete | exact moments through \(t\), distinct nodes |
| Maximal net | certified spherical-Voronoi area divided by total area | weak Delaunay, radius, \(k\)-NN, complete | separation/fill certificate; restored moments if exactness is claimed |
| Delaunay | certified positive Voronoi masses | weak spherical Delaunay or complete | distinct nodes, positive cells, moment/rank audit |
| Locally adapted | positive uniform-surface masses after exact moment restoration | weak Delaunay plus certified edge orbits, complete | every proposal rechecks moments, positivity, rank, and (4) |

At a Delaunay degeneracy, the implementation uses the weak graph: the union of all pairs belonging to a common supporting face.  A coordinate-lexicographic diagonal is not rotation-equivariant.

The geometry metrics are separation
\[
 q_X={1\over2}\min_{i\ne j}d_g(x_i,x_j),
\]
fill distance \(h_X=\sup_x\min_i d_g(x,x_i)\), mesh ratio \(h_X/q_X\), maximum graph angle, and graph degrees.  A sampled fill distance is labelled diagnostic unless enclosed by a covering certificate.

The sampling Gram condition is
\[
 \kappa_\ell^+
 ={\lambda_{\max}(G_\ell)\over\lambda_{\min}^+(G_\ell)}
\]
on a declared constant-rank range, with the rank and singular-value gap recorded.  If a positive quadrature integrates all spherical polynomials through degree \(2L\), products of harmonics through \(L\) are exact, hence \(S_{\le L}^\top WS_{\le L}=I\) in an orthonormal basis and every such condition number is exactly one.

For local geometry, set
\[
 \ell_{ij}=1-x_i^\top x_j,\qquad
 z_{ij}={P_{x_i}x_j\over\ell_{ij}}.
\]
Writing \(a_{ij}=c_{ij}/w_i\) and
\(p_{ij}=a_{ij}\ell_{ij}/\lambda_1\), the \(i\)-th row of (1) is equivalent to
\[
 p_{ij}\ge0,\quad\sum_jp_{ij}=1,\quad\sum_jp_{ij}z_{ij}=0. \tag{6}
\]
The local margin is the largest common lower barycentric mass in (6), or a signed distance of zero to the neighbor convex hull.  It is a necessary row-wise diagnostic only.  It does **not** prove the existence of shared reversible conductances.

The global feasibility margin is the optimum of the joint LP that imposes (1), \(c_e\ge t\,s_e\), and rates at most \((1-t)R\).  Positivity and rate slack are also reported separately.  Its exact or outward-rounded certificate, not local cones, is the feasibility gate.

## 4. Outer problem and compact protected set

A declared outer objective may be
\[
 F=\alpha_2\mathfrak D_2+\alpha_r r_{\max}
   +\sum_{\ell>2}\alpha_\ell\mathfrak D_\ell
   +\alpha_\kappa\log\kappa
   +\alpha_{\rm rot}B_{\rm col}
   +\alpha_{\rm app}E_{\rm resp}, \tag{7}
\]
where all coefficients are nonnegative and
\[
 r_{\max}=\max_i{1\over w_i}\sum_{e\ni i}c_e.
\]
The response term is admitted only with a uniform discrete stability/coercivity bound.

For fixed \(N\), the protected set imposes:

- unit nodes and a separation floor;
- weights \(w_i\ge w_0>0\), \(\sum_iw_i=1\);
- exact declared quadrature moments;
- a fixed orbit/stabilizer stratum or a finite intrinsic graph pool;
- a positive sampling eigenvalue floor on each retained rank stratum;
- a verified uniform inner feasibility/Robinson margin;
- closed conductance/rate bounds; and
- a uniform response stability bound whenever a response objective is present.

This set is closed in a finite product of compact spheres, a simplex, and a finite graph set.  Conductances are bounded by the rate cap or (5), so the lifted feasible set is compact.  Shell norms, graph rate, condition number on the spectral-gap stratum, and maximum edge angle are continuous.  A supremum rotation metric is continuous because it is a supremum of a jointly continuous function over compact \(SO(d)\).  A response is continuous under the uniform stability bound.

### Theorem 3 — existence

Every fixed-candidate inner optimum is attained.  If the inner feasible correspondence has constant equality rank and uniform Robinson regularity, its value function \(V(X,w,E)\) is continuous.  Therefore (7) attains an outer minimum on every protected compact design space.

**Proof.**  Inner attainment is Theorem 2.  Constant rank and uniform Robinson regularity give upper and lower hemicontinuity of the compact feasible correspondence; Berge’s maximum theorem gives continuity of \(V\).  The other terms are continuous as just noted.  Weierstrass then gives an outer minimizer. ∎

This is an existence theorem, not a claim that the algorithms below discover the nonconvex global minimum.

## 5. Strategy I — finite group orbits

Fix a finite \(G\le O(d)\).  Parameterize nodes as disjoint orbits of representatives \(y_a\), use orbit masses \(w_{ga}=\alpha_a/|G\cdot y_a|\), take complete unoriented edge orbits, and tie conductances within each edge orbit.  Stabilizer changes and collisions are separate strata.

The Reynolds projection proves that exactness through degree \(t\) need only be checked on a basis of \(G\)-invariant polynomials: both continuum and orbit quadrature functionals annihilate \(p-\frac1{|G|}\sum_gp\circ g\).  If \(G\) has no invariant vector, every orbit is centered.  If symmetric matrices commuting with the orthogonal representation are scalar, orbit averaging gives second moment \(I/d\).

### Theorem 4 — symmetry and covariance

For an orbit-constant design, \(L\) commutes with every induced node permutation.  Harmonic samples intertwine the node and harmonic representations, and every shell Gram and raw LMI transforms by orthogonal congruence.  Thus (4), (7), and the optimal value are invariant under simultaneous rotation of nodes and the physical data.  If the optimizer is unique or selected by an invariant strict tie-break, the selected conductance is equivariant; otherwise only the optimizer set and value are equivariant.

**Proof.**  A group element permutes nodes and edge orbits bijectively while preserving masses and conductances.  Substitution in the edge sum proves commutation.  The identity \(S_\ell(gX)=S_\ell(X)\rho_\ell(g)^\top\) gives the congruences. ∎

On a compact fixed stratum \(Z\), define the exact proximal baseline
\[
 z_{k+1}\in\arg\min_{z\in Z}
 \left[V(z)+{d(z,z_k)^2\over2\alpha}\right], \tag{8}
\]
with deterministic tie-breaking and an exact inner solve at every evaluation.

### Theorem 5 — proximal feasibility, descent, and stationarity

Assume \(Z\) is compact and prox-regular and \(V\) is locally Lipschitz.  Then (8) exists, preserves every constraint, and satisfies
\[
 V(z_{k+1})+{d(z_{k+1},z_k)^2\over2\alpha}\le V(z_k). \tag{9}
\]
Consequently the squared increments are summable, increments vanish, subsequences converge, and every accumulation point \(z_*\) is limiting-stationary:
\[
 0\in\partial V(z_*)+N_Z(z_*). \tag{10}
\]

**Proof.**  Compactness and continuity give a minimizer.  Feasibility is automatic because the minimization is over \(Z\).  Comparing with \(z=z_k\) proves (9).  Telescoping and the lower bound of \(V\) prove square summability.  Compactness supplies a convergent subsequence.  The limiting first-order condition for (8) contains the distance gradient divided by \(\alpha\); it tends to zero with the increments.  Closedness of the limiting subdifferential and normal graphs yields (10). ∎

The executable finite-pool controller proves (9) only over its declared pool.  It does not label that finite computation continuum stationarity.

## 6. Strategy II — Riemannian nodes with exact inner SDP

Lift a strictly feasible witness \(\bar c\) separately from the current inner optimum.  Let \(H(X,w,\bar c)=0\) contain exact quadrature moments and (1), after algebraically redundant rows are removed.  Node tangents satisfy \(\delta x_i\perp x_i\).  Every proposed tangent direction solves the coupled linearization \(DH\,\delta z=0\).

The restoration gate requires the reduced correction Jacobian to be onto with a uniform smallest singular value and every inactive inequality to retain a margin.  The implicit-function theorem then gives a deterministic minimum-norm restoration map.  A first-order feasible tangent followed by sphere retraction violates \(H\) by \(O(\alpha^2)\); restoration changes the trial by \(O(\alpha^2)\), so the composed retraction is first-order accurate.

Arbitrary node motion is not admissible.  For two antipodal nodes joined by one edge, (1) fixes antipodality, equal masses, and the conductance.  Moving one node alone generically destroys feasibility.  The implementation therefore rejects a nonsurjective reduced restoration Jacobian.

On a smooth fixed-graph stratum, strong regularity of the parametric SDP KKT system gives a differentiable value function.  Its envelope derivative includes the moving terms
\[
 dG=(dS)^\top WS+S^\top(dW)S+S^\top W(dS)
\]
and \(dZ\) in (3).  Slater feasibility alone is insufficient: optimizer switching can make \(V\) nonsmooth.

### Theorem 6 — restored Riemannian convergence

Assume the protected stratum is compact \(C^2\), restoration is uniformly first-order, every inner solve is exact, and \(V\) has Lipschitz Riemannian gradient.  A restored Armijo step using \(-\operatorname{grad}V\), rejected whenever any certificate fails, preserves feasibility and gives a uniform sufficient decrease.  The accepted gradient norms are square summable; every accumulation point is Riemannian stationary.  Under MFCQ it satisfies the full KKT system.

**Proof.**  The Riemannian descent lemma and the \(O(\alpha^2)\) restoration perturbation give an Armijo-acceptable interval bounded uniformly away from zero on the compact stratum.  Feasibility follows from exact restoration and the margin audit.  Summing Armijo decreases shows \(\sum\|\operatorname{grad}V(z_k)\|^2<\infty\).  Compactness supplies subsequences, and continuity of the gradient gives stationarity at every cluster point.  MFCQ converts tangent stationarity to KKT multipliers. ∎

At nonsmooth points, the code may claim Clarke stationarity only when a bundle/proximal step certifies
\[
 V(z_k)-V(z_{k+1})\ge a\,d_k^2-\varepsilon_k,\quad
 \operatorname{dist}(0,\partial^CV(z_{k+1})+N^C_Z(z_{k+1}))
 \le b\,d_k+\eta_k, \tag{11}
\]
with \(\sum\varepsilon_k<\infty\) and \(\eta_k\to0\).  The same telescoping and closed-graph argument proves that cluster points are Clarke stationary.  Monotone values alone do not prove stationarity.

## 7. Strategy III — alternating weight, node, and conductance updates

A weight-led or node-led block includes the first-order corrections in all variables needed to remain in \(\ker DH\).  After every accepted outer block, (4) is re-solved; descent is never evaluated with stale conductances.

If block tangent spaces \(T_b(z)\) satisfy the uniform frame condition
\[
 \sum_b\|\Pi_{T_b(z)}g\|^2\ge\eta\|g\|^2,\qquad\eta>0, \tag{12}
\]
then cyclic restored Armijo descent makes the full gradient vanish.  Without (12), separate feasible fibers can be singletons even while a joint feasible descent direction exists.  The reproducible algorithm therefore performs a joint feasible-tangent safeguard once per sweep.  With that safeguard, Theorem 6 applies to the joint step, while the individual blocks supply additional descent.  The claim is full stationarity only when the joint safeguard or (12) is certified; otherwise it is explicitly only block stationarity.

## 8. Strategy IV — certified graph updates

### Theorem 7 — edge addition

If \(E\subseteq E'\), extend a conductance by zero on \(E'\setminus E\).  Equations (1), all rates, every shell residual, positivity, and every fixed convex response term are unchanged.  Hence feasibility is preserved and the exact inner optimum on \(E'\) cannot exceed that on \(E\).

**Proof.**  The added incidence columns are multiplied by zero.  Every displayed affine expression is therefore identical.  The old feasible set embeds in the new one. ∎

Deletion has no unconditional analogue.  It is accepted only after an independently verified restricted conic solve, or an exact kernel move \(\delta c\) with
\[
 A\delta c=0,\quad
 \delta c_e=-c_e,\quad
 c+\delta c\ge0,
\]
and the rate cap reverified.  Linear infeasibility may be certified by a Farkas separator; conic objectives require the full conic dual certificate.

For a finite master graph, propose whole symmetry edge orbits in deterministic order.  With objective intervals \([L,U]\), edge penalty \(\beta\), and strict gap \(\tau>0\), accept only if
\[
 U_{\rm new}+\beta|E_{\rm new}|
 \le L_{\rm old}+\beta|E_{\rm old}|-\tau. \tag{13}
\]
Retain the incumbent on every rejection and forbid revisits.  There are finitely many graphs, so accepted changes terminate.  Exhaustion certifies only single-declared-orbit graph-neighborhood stationarity.

## 9. Strategy V — direct spherical-design construction

Let \(X,w\) be any positive centered rule.  On the complete graph set
\[
 c_{ij}=\lambda_1w_iw_j.
\]
Then
\[
 (-Lf)_i=\lambda_1\left(f_i-\sum_jw_jf_j\right), \tag{14}
\]
so H0 and H1 are exact and every conductance is strictly positive.  Orbit-constant masses make (14) orbit-constant automatically.  If the rule is a positive 2-design, every sampled nonconstant harmonic has zero weighted mean; on \(\mathcal H_2\), (14) has eigenvalue \(\lambda_1\), so
\[
 \mathfrak D_2=\lambda_2-\lambda_1=d+1. \tag{15}
\]
This is an exact, deterministic, globally compatible initializer.  It is nonlocal and does not converge in \(\mathfrak D_2\).

For a spherical \(t\)-design, equal masses give positivity and exact Gram conditioning through \(\ell\le t/2\).  Well-separated designs with \(N=\Theta(t^{d-1})\), together with a certified covering estimate, give quasiuniform node candidates.  They enter the local co-design only after the global shared-edge feasibility LP or an accepted construction passes.  Design exactness and local cones are never substituted for global conductance compatibility.

## 10. Strategy VI — adaptive response refinement

On an enriched discrete angular space, let
\[
 A_hu_h=q_h,\qquad A_h^\top z_h=c_h,\qquad
 r_h=q_h-A_hIu_H.
\]
Then the exact algebraic identity
\[
 c_h^\top(u_h-Iu_H)=z_h^\top r_h \tag{16}
\]
holds without Galerkin orthogonality.  Block localization gives indicators
\(\eta_i=|z_{h,i}r_{h,i}|\) and
\[
 |c_h^\top(u_h-Iu_H)|\le\sum_i\eta_i. \tag{17}
\]
Deterministic bulk marking proposes antipodal or complete group orbits, restores positive surface masses and exact moments, rebuilds an intrinsic graph, and re-solves (4).  The incumbent remains active until all feasibility and descent certificates pass.  Thus accepted refinements preserve feasibility and decrease the declared objective.  Equations (16)–(17) certify error only to the enriched discrete reference.  A continuum claim needs a separate consistency and stability theorem.

## 11. All-orders co-designed convergence family

Use the accepted Paper-I P1E reflected adaptive-ring family at every admissible level \(h\).  Its constructive reversible conductance satisfies
\[
 r_{\max}\le64\pi^2h^{-2},\qquad
 \mathfrak D_2\le{75\over2}h^2. \tag{18}
\]
Run the exact inner minimization of \(\mathfrak D_2\) at the same rate cap, on the P1E graph or any certified supergraph.  The P1E conductance, zero-extended if necessary, is feasible, so the optimum obeys the same upper bound.  The accepted P1B sharp frontier on \(\mathbb S^2\) gives
\[
 \mathfrak D_2\,r_{\max}\ge6.
\]
Since every feasible candidate has \(r_{\max}\le64\pi^2h^{-2}\),
\[
 {3\over32\pi^2}h^2
 \le\mathfrak D_{2,\mathrm{opt}}
 \le{75\over2}h^2. \tag{19}
\]

### Theorem 8 — certified quadratic order

For every admissible P1E level, not merely a fitted subsequence,
\[
 \mathfrak D_{2,\mathrm{opt}}=\Theta(h^2)
\]
with the explicit constants in (19).  Certified edge additions and accepted outer moves that retain the same P1E feasible incumbent and rate cap preserve the upper bound; the P1B universal lower bound persists.

This is the requested asymptotic theorem.  Finite fitted slopes are reported only as supplementary regressions.  The benchmark records \(N\), \(|E|\), \(h\), \(\mathfrak D_2\), \(r_{\max}\), \(\kappa_2^+\), higher-shell defects, collision rotation spread, solve time, and peak memory at every tested level.

## 12. Rotation claims and tests

The shell operator norm \(\mathfrak D_\ell\) is basis-invariant; it is not itself a directional bias metric.  For a declared nonzero physical harmonic probe \(a\), define
\[
 d_{\rm col}(R;a)
 ={ \|(L+\lambda_\ell I)S_\ell\rho_\ell(R)a\|_W
    \over
    \|S_\ell\rho_\ell(R)a\|_W }, \tag{20}
\]
with a certified positive denominator floor.  The collision-only fixed-grid spread is
\[
 B_{\rm col}(a)=\sup_Rd_{\rm col}(R;a)-\inf_Rd_{\rm col}(R;a). \tag{21}
\]
It is bounded above by the shell defect scale, but it need not have a matching lower bound: a nonzero scalar shell defect is rotationally invariant.  P1B therefore cannot be reported as a lower bound on rotation spread.

The required tests are:

1. **Collision-only relative rotation.**  Disable streaming in a homogeneous ODE or resolvent and rotate the physical harmonic relative to fixed \(X\).  This measures (21).
2. **Collision joint rotation.**  Rotate physical data, nodes, masses, and the intrinsic graph together.  The covariance defect is zero mathematically under Theorem 4 and is an implementation regression.
3. **Streaming-only rays.**  Disable collision/scattering and use a ballistic localized source/absorber.  Rotate the physical problem relative to fixed ordinates.
4. **Streaming joint rotation.**  Co-rotate quadrature, geometry, and spatial mesh, or use analytic characteristics/rotationally symmetric geometry.  Otherwise spatial anisotropy contaminates the result.
5. **Coupled BFP.**  Report the coupled spread separately; never label it collision error alone.

A sampled \(SO(3)\) maximum is certified only with a rotation-net covering radius \(\delta\) and a proved Lipschitz constant \(K\): the true extrema lie within \(K\delta\) of the sampled extrema.  Stable linear response problems admit such a bound from the resolvent/adjoint identity and a uniform coercivity constant.  Discontinuous beams without this bound remain empirical.

Quadrature rotation or interpolation is a separate streaming remedy.  Its audit records
\[
 P_R{\bf1}={\bf1},\quad P_R\ge0,\quad
 w_{\rm target}^\top P_R=w_{\rm source}^\top,\quad
 P_RX_{\rm source}=X_{\rm target},
\]
the operator norm, and accumulated error.  Generic positive interpolation need not preserve first moments or generator identities and is never folded into the collision theorem.

## 13. Reproducibility and certification

Every run records:

- family and parameter/orbit file;
- canonical node, weight, graph, and conductance hashes;
- \(N,|E|,h_X,q_X\), graph angle, and \(r_{\max}\);
- sampling ranks, spectral gaps, and condition numbers;
- local and global feasibility margins;
- exact H0/H1, reversibility, positivity, and rate residuals;
- \(\mathfrak D_2\), higher-shell defects, and raw-LMI minimum eigenvalues;
- fixed-physical and joint-rotation spreads with their scope;
- response test definition and stability certificate;
- primal/dual gaps and independent conic residual reconstruction;
- wall time, solver identity/version, and peak memory.

Coordinates and orbit parameters are deterministically ordered.  Nonunique inner optima use a declared invariant secondary tie-break.  Exact symmetric fixtures use rational/algebraic arithmetic.  General numerical candidates require outward-rounded primal feasibility and objective enclosures for theorem-bearing claims.  Floating solver status alone is diagnostic.

The Python package implements family adapters, common metrics, raw moving-Gram checks, exact inner calls to P2A, protected-restoration diagnostics, finite-pool proximal descent, alternating ledgers, graph certificates, adaptive identities, rotation separation, and the Paper-I benchmark.  The symbolic audit proves the finite exact identities in (14), the Lebedev-14 dense H2 defect, (5), and the constant product in (19).  CI runs symbolic audit, hostile pytest fixtures, the finite benchmark, retained P2A/P2B/P1E regressions, documentation sentinels, and changed-path checks.

## 14. Prior-art transfer limits

The external literature is used only for its stated background result:

- Steinerberger, “Spectral Limitations of Quadrature Rules and Generalized Spherical Designs,” [arXiv:1708.08736](https://arxiv.org/abs/1708.08736), supplies spectral limitations for positive quadrature; it is not a co-design construction.
- Ahrens and Beylkin, “Rotationally Invariant Quadratures for the Sphere,” [DOI 10.1098/rspa.2009.0104](https://doi.org/10.1098/rspa.2009.0104), supplies icosahedral invariant quadrature methodology; it does not prove positive shared-edge generator feasibility.
- Morel et al., “A Discretization Scheme for the Three-Dimensional Angular Fokker–Planck Operator,” [DOI 10.13182/NSE07-A2693](https://doi.org/10.13182/NSE07-A2693), supplies the product-quadrature AFP context; it is not the present bilevel theorem.
- Bienvenue et al., “A Flexible, Moment-Preserving, and Monotone Discretization…,” [DOI 10.1080/00295639.2025.2462891](https://doi.org/10.1080/00295639.2025.2462891), supplies nonorthogonal/Voronoi AFP context and keeps ray effects separate; it does not prove the P2A optimum or Paper-I frontier.
- Bondarenko–Radchenko–Viazovska, “Well separated spherical designs,” [arXiv:1303.5991](https://arxiv.org/abs/1303.5991), supplies well-separated design existence, not local generator compatibility.
- Izmestiev and Lam, “Discrete Laplacians—spherical and hyperbolic,” [arXiv:2408.04877](https://arxiv.org/abs/2408.04877), supplies spherical Delaunay nonnegative structure, not this bilevel optimum.

The new claims in Theorems 1–8 are derived above from the frozen P2A model and the accepted Paper-I P1B/P1E results, not imported from those papers.

## 15. Hostile boundaries

The audits explicitly reject or separate the following:

- nonpositive or incorrectly normalized published masses;
- duplicate nodes and zero-length edges;
- a sampling rank chosen from an unresolved numerical threshold;
- local row feasibility promoted to global shared-edge feasibility;
- a node step without a surjective coupled restoration Jacobian;
- a deleted active edge without a restricted primal certificate;
- a partial symmetry-orbit graph edit;
- a Delaunay diagonal chosen by ambient coordinate lexicography;
- a branch gradient through a nonunique SDP optimum;
- compactness claimed with vanishing weights or collisions;
- stationarity inferred from monotone values alone;
- global outer optimality inferred from local descent;
- a P1B defect lower bound relabelled as rotation spread;
- streaming ray error relabelled as collision error;
- joint rotation performed without the spatial geometry/mesh;
- interpolation assumed to preserve moments without audit;
- an enriched discrete estimator relabelled as continuum error;
- a finite fitted slope relabelled as the all-orders theorem; and
- floating solver status relabelled as an exact certificate.

Under these gates, the co-design is exact where claimed, positive and moment-preserving on every accepted candidate, reproducible, and correctly scoped with respect to rotation and streaming.

# Paper 2B — Positive graph angular diffusion, goal-oriented adaptivity, and conservative transfers

## Abstract

This note constructs a structure-preserving adaptive angular framework around positive spherical quadratures.  A sparse weighted graph generator approximates the Laplace–Beltrami operator while exactly conserving constants, remaining self-adjoint in the quadrature inner product, generating a positivity-preserving semigroup, and exposing a computable spectral residual.  Forward, adjoint, and contributon information define normalized multiresponse indicators.  Filtered-harmonic or graph-heat bootstraps prevent missing rays from making an indicator identically zero.  Angular refinement is followed by positive moment-cone recertification, with hysteresis and rollback preventing nonconvergent cycles.  Positive inter-grid transfer is characterized exactly by a cone condition; a strict-convexity theorem proves that universal positive coarsening cannot preserve mass and all current components unless every source direction is retained.  The resulting software uses exact transpose adjoints and reports positivity, balance, response error, and transfer feasibility separately.

---

## 1. Weighted graph generator

Let \(\Omega_i\in S^2\) be quadrature nodes with \(w_i>0\), and let \(c_{ij}=c_{ji}\ge0\) be symmetric conductances.  Define

\[
(Gf)_i=\frac1{w_i}\sum_jc_{ij}(f_j-f_i).
\tag{1}
\]

Let \(W=\operatorname{diag}(w_i)\), and let \(L_c\) be the weighted graph Laplacian with off-diagonal entries \((L_c)_{ij}=c_{ij}\) and diagonal entries \((L_c)_{ii}=-\sum_jc_{ij}\).  Then

\[
G=W^{-1}L_c.
\tag{2}
\]

### Theorem 1 (exact structural properties)

For every nonnegative symmetric conductance matrix:

1. \(G\mathbf1=0\).
2. \(WG=L_c=(WG)^T\), so \(G\) is self-adjoint in
   \[
   \langle f,g\rangle_W=f^TWg.
   \]
3. \(G\) is negative semidefinite:
   \[
   \langle f,Gf\rangle_W
   =-\frac12\sum_{i,j}c_{ij}(f_i-f_j)^2\le0.
   \tag{3}
   \]
4. \(G\) is Metzler with zero row sum, so \(e^{tG}\ge0\) and \(e^{tG}\mathbf1=\mathbf1\) for every \(t\ge0\).
5. The nullspace contains one constant on each connected component; it consists only of global constants if and only if the graph is connected.

#### Proof

The first two properties follow directly from symmetric edge cancellation.  Expanding \(f^TL_cf\) by edges gives (3).  Off-diagonal entries of \(G\) are nonnegative, and its row sums vanish.  A Metzler matrix generates a positive semigroup; zero row sum gives preservation of constants.  Finally, equality in (3) requires equality of \(f_i\) along every positive-conductance edge, which is equivalent to constancy on connected components. ∎

The structural theorem is unconditional.  Approximation of \(\Delta_{S^2}\) requires a separate consistency fit.

---

## 2. Conductance fitting

Let \(\phi_k\) be selected real spherical harmonics, with

\[
\Delta_{S^2}\phi_k=-\lambda_k\phi_k,
\qquad \lambda_k=\ell_k(\ell_k+1).
\tag{4}
\]

For an undirected candidate edge set \(E\), unknown conductances \(c_e\ge0\) should satisfy

\[
\sum_{j:(i,j)\in E}c_{ij}
(\phi_k(\Omega_j)-\phi_k(\Omega_i))
=-w_i\lambda_k\phi_k(\Omega_i).
\tag{5}
\]

Stack (5) as

\[
Ac=b,
\qquad c\ge0.
\tag{6}
\]

### Optimization problem

The implemented fit is

\[
\min_{c\ge c_{\min}}
\frac12\|R^{1/2}(Ac-b)\|_2^2
+\frac{\lambda_c}{2}\|c\|_2^2,
\tag{7}
\]

where \(R\) may weight harmonic degrees or node regions.  A small floor is applied only to a connectivity scaffold; all other edges may use a zero lower bound in a larger implementation.

### Connectivity requirement

The candidate graph is the union of:

- a symmetric \(k\)-nearest-neighbor graph, which supplies local approximation freedom; and
- a Euclidean minimum spanning tree, which guarantees connectivity.

A nearest-neighbor graph alone can be disconnected on clustered or anisotropic node sets.

### Exact feasibility certificate

If exact conductances are required, (6) is a nonnegative linear feasibility problem.  Farkas' lemma gives an infeasibility certificate \(y\) satisfying

\[
A^Ty\ge0,
\qquad b^Ty<0.
\tag{8}
\]

Thus “fit failed” and “no exact nonnegative fit exists on this edge graph” are distinct statements.

### Consistency and spectral diagnostics

For every fitted harmonic,

\[
r_k=G\phi_k+\lambda_k\phi_k.
\tag{9}
\]

Report

\[
\epsilon_k^{(W)}=
\frac{\|r_k\|_W}{\lambda_k\|\phi_k\|_W},
\qquad
\epsilon_k^{(\infty)}=\|r_k\|_\infty.
\tag{10}
\]

For a sequence of quasiuniform nodes with local edge radius tending to zero, bounded mesh ratio, and residuals (10) tending to zero on a dense harmonic set, \(G\) is a consistent spectral approximation of \(\Delta_{S^2}\).  The present package proves the exact structural properties and measures, rather than presumes, the consistency residual.

### Numerical result

For Fibonacci rules and degree-two fitting:

| nodes | edges | maximum weighted harmonic residual |
|---:|---:|---:|
| 24 | 101 | 0.1979 |
| 48 | 198 | 0.0975 |
| 72 | 305 | 0.0633 |

At every size, the constant and weighted-symmetry residuals were at roundoff, the largest eigenvalue was nonpositive to roundoff, and \(e^{0.02G}\) was entrywise nonnegative.

---

## 3. Use in angular transport

A rotationally invariant angular-diffusion term can be represented as

\[
-dG\psi,
\qquad d\ge0,
\tag{11}
\]

on the left-hand side of a transport equation.  Because \(-G\) has nonpositive off-diagonal entries and nonnegative spectrum, it is compatible with an \(M\)-matrix transport discretization.  The graph term preserves angular constants exactly and cannot create negative flux through its semigroup when used in a stable positive split or monotone solve.

The graph is not presented as a replacement for the collision operator.  It is used for filtered-\(P_N\)-type regularization, bootstrap indicators, or a Fokker–Planck angular term when such a term is part of the physical/numerical model.

---

## 4. Goal-oriented angular error indicator

Let a discrete transport solution satisfy

\[
L_h\psi_h=q_h,
\tag{12}
\]

and response \(m\) be \(J_m=c_m^T\psi_h\).  Let

\[
L_h^Tz_m=c_m
\tag{13}
\]

be the exact algebraic adjoint.  For an angular patch, node, or candidate enrichment \(p\), let \(R_p\) denote the local transport residual revealed by the enriched test space.  The dual-weighted indicator is

\[
\eta_{m,p}=|\langle z_m,R_p\rangle|.
\tag{14}
\]

For several responses, define

\[
\eta_p=
\max_m
\frac{\eta_{m,p}}{|J_m|+\epsilon_J}.
\tag{15}
\]

The denominator prevents a large-magnitude response from dominating solely by units or scale.  Response tolerances can replace \(|J_m|+\epsilon_J\) when absolute accuracy is the actual requirement.

### Contributon indicator

At a fixed spatial/group state, define

\[
\chi_m(\Omega_i)=\psi_i z_{m,i}.
\tag{16}
\]

A graph-curvature indicator is

\[
\eta^{\rm cont}_{m,i}
=\frac{|(G\chi_m)_i|}
{\sum_jw_j|\chi_m(\Omega_j)|+\epsilon_J}.
\tag{17}
\]

It highlights angular regions where the response-carrying product is poorly resolved, even when forward flux alone is smooth.

---

## 5. Ray-effect failure and bootstrap

### Proposition 2 (why an ordinary adjoint indicator can be zero and wrong)

Suppose a physically important source-to-response path requires directions absent from the current discrete angular support.  If both the discrete forward and discrete adjoint solutions vanish on all represented paths connecting the source and response, then every indicator built only from their product and the represented residual can be zero, although the true response error is nonzero.

#### Proof

The discrete residual and adjoint weight are evaluated only in the represented trial/test space.  When the missing path has no projection onto that space, the dual pairing (14) contains no term from it.  Zero is therefore a statement about the restricted model, not the continuous error. ∎

### Filtered-harmonic bootstrap

Project the current angular field to harmonics through degree \(L_b\), apply a rotationally invariant filter

\[
\widehat f_{\ell m}^{\rm filt}
=\exp\left[-\alpha(\ell(\ell+1))^{p_f/2}\right]
\widehat f_{\ell m},
\tag{18}
\]

and reconstruct it at candidate directions.  Use the smoothed field only to seed/refine the indicator, not to overwrite the converged transport solution.

### Graph-heat bootstrap

Alternatively,

\[
f^{\rm boot}=e^{t_bG}f,
\qquad t_b>0.
\tag{19}
\]

Theorem 1 guarantees positivity and constant preservation.  This creates a small, rotationally local angular footprint around represented rays.

### Bootstrap rule

Use

\[
\eta_p^{\rm total}
=\max(\eta_p^{\rm DWR},\beta_b\eta_p^{\rm boot})
\tag{20}
\]

for early adaptive cycles.  Reduce \(\beta_b\) as true forward/adjoint paths become represented.  A bootstrap that remains dominant indefinitely is a bias, not an error estimator.

In the line-source benchmark, the coarse 8-direction field at a remote cell had four exactly zero angular components.  The filtered-harmonic bootstrap reduced the zero count to zero and reduced angular variation from \(1.44\times10^{-3}\) to \(7.93\times10^{-4}\).

---

## 6. Refinement and coarsening

### Refinement

For a marked node \(\Omega_i\), construct a tangent basis \(e_1,e_2\) and children

\[
\Omega_{i,k}=\cos\delta\,\Omega_i
+\sin\delta\left(
\cos\varphi_k e_1+
\sin\varphi_k e_2
\right).
\tag{21}
\]

The candidate pool is the old support plus the children.  Recompute positive weights by solving the moment equations of Paper 2A.  Refinement is accepted only if:

1. the positive moment LP is feasible;
2. all active weights exceed the numerical support threshold;
3. requested symmetry is retained;
4. transport positivity/balance tests pass;
5. the measured response error or estimator decreases sufficiently.

### Coarsening

Low-indicator nodes are proposed for removal.  Coarsening is accepted only after the reduced pool passes the same moment-cone certification.  If infeasible, rollback is mandatory.

### Hysteresis

Let \(\theta_r>\theta_c\).  Refine only after

\[
\eta_i\ge\theta_r
\]

for \(n_r\) consecutive cycles, and coarsen only after

\[
\eta_i\le\theta_c
\]

for \(n_c\) consecutive cycles.  This prevents a node near one threshold from being repeatedly created and removed.

### Algorithm 1 (one adaptive cycle)

1. Solve forward transport.
2. Solve exact transpose adjoints for all requested responses.
3. Compute DWR and contributon indicators.
4. If paths are underrepresented, compute filtered-harmonic or graph-heat bootstrap.
5. Normalize and combine responses using (15).
6. Update hysteresis counters.
7. Generate refinement children and a tentative coarsened pool.
8. Solve the positive moment LP.
9. Roll back coarsening if the cone constraints are infeasible.
10. Transfer the current state by a certified positive transfer or perform a fresh transport solve.
11. Recheck positivity, conservation, response error, and estimator reduction.

---

## 7. Conservative positive transfer

Let grid \(A\) have angular state \(f_A\) and moment matrix \(M_A\), while grid \(B\) has \(M_B\).  A universal linear transfer satisfies

\[
f_B=T_{A\to B}f_A,
\qquad
M_BT_{A\to B}=M_A,
\qquad T_{A\to B}\ge0.
\tag{22}
\]

### Theorem 3 (moment-cone criterion)

A universal positive transfer exists if and only if every column of \(M_A\) belongs to the cone generated by columns of \(M_B\).

#### Proof

Equation (22) separates columnwise.  Column \(j\) of \(T\) is a nonnegative coefficient vector representing column \(j\) of \(M_A\) as a conic combination of target columns. ∎

This theorem yields a constructive columnwise LP and a Farkas certificate for any failed column.

### Theorem 4 (mass-and-current no-go theorem)

Assume the moments include total integral and all three current components.  For quadrature \(A\), column \(j\) is proportional to

\[
\begin{bmatrix}1\\\Omega_j^A\end{bmatrix}.
\]

A universal positive transfer from \(A\) to \(B\) exists only if every source direction \(\Omega_j^A\) appears among the target directions.

#### Proof

Normalize the mass row of the column equation.  It asserts that the unit vector \(\Omega_j^A\) is a convex combination of target unit vectors.  The Euclidean unit ball is strictly convex: a convex combination of unit vectors has norm one only when every vector with positive coefficient equals the result.  Hence the target support must contain \(\Omega_j^A\). ∎

### Corollary 4.1

Universal positive coarsening that preserves mass and the complete current vector is impossible unless the target retains all source directions.  Adding higher moments or response modes cannot remove this obstruction.

This is why the implementation certifies feasibility instead of silently using negative interpolation.

### Feasible alternatives

1. **Nested refinement:** if the fine grid contains the coarse nodes, injection/prolongation can be positive and moment preserving.
2. **State-specific positive remap:** for one nonnegative state \(f_A\), solve
   \[
   M_Bf_B=M_Af_A,
   \qquad f_B\ge0.
   \tag{23}
   \]
   This may be feasible even when no universal \(T\) exists.
3. **Preserve fewer moments:** mass-only nearest-direction transfer is always available for positive weights.
4. **Minimum-residual positive transfer:** solve a nonnegative least-squares problem and report moment defects explicitly.
5. **Fresh solve after grid change:** avoid transferring a poorly representable state.

The benchmark confirms that a universal mass/current transfer from 12 Fibonacci nodes to 8 is infeasible, while a state-specific isotropic remap from 12 nodes to six coordinate axes is feasible with residual \(5.55\times10^{-16}\).

---

## 8. Error accumulation under repeated transfer

Let \(\|f\|_{1,w}=\sum_iw_i|f_i|\).  A positive mass-preserving transfer is nonexpansive for nonnegative states and, by decomposition into positive/negative parts, has induced weighted \(L^1\) norm at most one under the corresponding exact mass mapping.

Suppose transfer \(k\) introduces a response/moment defect operator \(E_k\) with

\[
\|E_kf\|\le\epsilon_k\|f\|_{1,w}.
\tag{24}
\]

### Theorem 5 (additive repeated-transfer bound)

For nonexpansive transfers,

\[
\|\text{accumulated defect after }K\text{ transfers}\|
\le
\left(\sum_{k=1}^{K}\epsilon_k\right)
\|f_0\|_{1,w}.
\tag{25}
\]

#### Proof

Expand the perturbed product by a telescoping sum.  Every exact transfer before or after a defect has norm at most one, so each term is bounded by \(\epsilon_k\|f_0\|_{1,w}\). ∎

The bound motivates limiting adaptation frequency and periodically resolving transport from the physical source instead of repeatedly remapping a remapped state.

---

## 9. Verified transport prototype

`src/hts_angular/sn2d.py` implements a Cartesian upwind finite-volume \(S_N\) solver with:

- multiple energy/species groups;
- arbitrary positive angular nodes and weights;
- isotropic group-to-group scattering;
- optional graph angular diffusion \(-dG\);
- nonnegative volume and inflow sources;
- arbitrary volume-response kernels;
- direct sparse solve and positive source iteration;
- exact algebraic transpose adjoint;
- global particle-balance accounting.

For group \(g\), direction \(a\), and cell \((i,j)\), the streaming-removal equation has diagonal

\[
\Sigma_{t,gij}
+\frac{|\Omega_{a,x}|}{\Delta x_i}
+\frac{|\Omega_{a,y}|}{\Delta y_j},
\tag{26}
\]

nonpositive upwind-neighbor coefficients, nonpositive scattering coefficients on the left-hand side, and nonnegative boundary/source terms on the right.  Under subcritical scattering, the sweep/source iteration is positive.

The algebraic adjoint solves the literal transpose of the assembled forward matrix.  For the coupled neutron–photon benchmark, the REBCO photon-heating identity was

\[
J_{\rm forward}=1.28151435502572\times10^{-3},
\]

\[
J_{\rm adjoint}=1.28151435509151\times10^{-3},
\]

with relative difference \(5.13\times10^{-11}\).

---

## 10. Required benchmarks and obtained results

### Manufactured spherical harmonics

The graph diagnostics apply \(G\) to harmonics through degree two and compare with \(-\ell(\ell+1)Y_{\ell m}\).  Residuals decrease with node count as reported in Section 2.

### Line source

Relative multi-detector response errors versus the 64-direction reference were:

| directions | error |
|---:|---:|
| 8 | 0.2602 |
| 16 | 0.0972 |
| 32 | 0.0230 |
| 64 | reference |

### Narrow streaming duct

| rule | nodes | relative exit-response error |
|---|---:|---:|
| standard uniform | 8 | 0.9977 |
| standard uniform | 16 | 0.8042 |
| standard uniform | 32 | 0.2420 |
| response-enriched positive | 9 | 0.0542 |
| standard uniform | 64 | reference |

The 9-node rule was constructed from Fourier streaming moments and forward/response proxies on the 64-node candidate pool.  It is not asserted to be universally superior; it is a concrete demonstration that a response space can be more efficient than harmonic/order-only selection for a narrow transport objective.

### Grazing thin tape

| directions | relative tape-response error |
|---:|---:|
| 8 | 1.0000 |
| 16 | 0.99995 |
| 32 | 0.8155 |
| 64 | reference |

This intentionally adversarial case shows that ordinary order refinement can remain ineffective until near-grazing directions enter the support.

### Isolated photon source behind shielding

Relative detector errors were 0.9398, 0.5708, and 0.1581 for 8, 16, and 32 directions respectively, against the 64-direction reference.

### Coupled neutron–photon multilayer responses

The prototype tracked neutron flux, photon flux, and photon-heating proxies separately in copper, REBCO, and substrate regions.  Relative combined-response errors were 0.6093, 0.0848, and 0.0148 for 8, 16, and 32 directions.

### Structural checks

Across 21 transport runs:

- maximum global particle-balance relative residual: \(1.71\times10^{-11}\);
- minimum angular flux: 0, with no negative value beyond roundoff;
- source iterations converged in all cases;
- cost/error data and runtimes are in `results/paper2_transport_cost_error.csv`.

---

## 11. Novelty comparison with the named literature

The following is a method-level comparison, not a claim that a literature novelty search is complete.

### Relative to Dargaville et al. angular adaptivity

The named work develops scalable angular adaptivity, spherical-harmonic representations, and goal-based strategies robust to ray effects.  The present construction adopts the essential lesson that an ordinary adjoint indicator can fail before a ray path is represented, but adds a different structural combination:

1. the angular grids themselves are positive moment-cone rules enriched by HTS responses;
2. graph diffusion has exact weighted self-adjoint/Markov structure on irregular nodes;
3. every grid change is followed by positive moment recertification;
4. universal positive transfer feasibility is tested and can be rejected by a theorem/certificate;
5. layer-resolved HTS response operators provide the goals.

### Relative to Camminady et al. quadrature rotation

Quadrature rotation mitigates persistent ray alignment by changing angular support and interpolating between rotated rules.  The present approach instead refines response-important angular regions and treats interpolation as a constrained positive moment problem.  Rotation can be incorporated as a candidate-generation step, but negative or nonconservative interpolation is not accepted implicitly.

### Relative to Ahrens' Lagrange discrete ordinates

Lagrange discrete ordinates uses an interpolatory angular representation designed to retain favorable scattering spectral structure.  The present quadrature stage is a convex positive moment construction with transport-derived modes, while the graph stage supplies a sparse positive generator.  The two approaches could be compared or hybridized; neither mathematical framework subsumes the other.

### Candidate publishable contribution

The strongest combined contribution is not any single ingredient.  It is the coupling of:

- response-preserving thin-tape operators;
- positive forward/adjoint/contributon quadrature design;
- sparse Markov graph angular regularization;
- ray-effect bootstrap;
- cone-certified adaptive transfers;
- layer-resolved HTS verification benchmarks.

A formal novelty claim should be made only after a broader literature and patent search.

---

## 12. Complete adaptive workflow

1. Generate a certified positive base quadrature from Paper 2A.
2. Fit a connected positive graph and record harmonic residuals.
3. Solve the forward coupled transport problem.
4. Solve exact transpose adjoints for each HTS response.
5. Form DWR, contributon, and—when needed—bootstrap indicators.
6. Mark with multiresponse normalization and hysteresis.
7. Generate local tangent children or rotated candidate nodes.
8. Re-solve positive moment constraints; rollback infeasible coarsening.
9. Test universal transfer by cone LP.  If infeasible, use state-specific remap, mass-only transfer with recorded defects, or a fresh solve.
10. Recompute transport and check response reduction, positivity, particle/energy closure, and estimator effectivity.
11. Stop when every normalized response estimate and held-out validation response meets tolerance.

---

## 13. Source files

- `src/hts_angular/quadrature.py`
- `src/hts_angular/graph_generator.py`
- `src/hts_angular/transfer.py`
- `src/hts_angular/adaptivity.py`
- `src/hts_angular/sn2d.py`
- `tests/test_angular.py`
- `tests/test_sn2d.py`
- `benchmarks/run_all.py`

All source files are complete files, not patches.

---

## 14. References inspected

- Dargaville et al., “Scalable Angular Adaptivity for Boltzmann Transport,” arXiv:1901.04929.
- Dargaville et al., “Angular Adaptivity with Spherical Harmonics for Boltzmann Transport,” arXiv:1903.05466.
- Dargaville et al., “Goal-Based Angular Adaptivity for Boltzmann Transport in the Presence of Ray Effects,” arXiv:1911.01747.
- Camminady et al., “Ray Effect Mitigation for the Discrete Ordinates Method through Quadrature Rotation,” arXiv:1808.05846.
- Ahrens, C. D., “Lagrange Discrete Ordinates,” arXiv:1405.3968.

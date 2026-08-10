# Paper 2A — Positive response-weighted spherical quadrature as a moment-cone problem

## Abstract

Angular quadrature for an HTS transport calculation should preserve the angular structures that control tape heating, reaction rates, grazing transmission, and forward–adjoint sensitivity—not only a predetermined spherical-harmonic degree.  This note formulates that objective as a positive moment problem on \(S^2\).  It gives existence and node-count results, separates surface-measure exactness from response-weighted sampling, derives fixed-pool feasibility and minimum-residual certificates, states conditioning and nonuniqueness mechanisms, and connects moment error to both integration error and transport-response error.  A constructive workflow combines a high-order reference rule, finite-pool linear programming, support reduction, optional nonlinear node refinement, and post-refinement certification.  The numerical example obtains a 14-node strictly positive rule exact for nine degree-two spherical harmonics and five transport-derived modes relative to a 288-node reference measure.

---

## 1. Positive moment formulation

Let \(\sigma\) be surface measure on \(S^2\), with \(\sigma(S^2)=4\pi\).  Let

\[
\mathcal V=\operatorname{span}\{f_1,\ldots,f_K\}\subset C(S^2)
\tag{1}
\]

contain spherical harmonics, selected forward modes, selected adjoint modes, contributons, grazing functions, and streaming functions.  Define the feature map

\[
F(\Omega)=\bigl(f_1(\Omega),\ldots,f_K(\Omega)\bigr)^T
\tag{2}
\]

and target moment vector

\[
b=\int_{S^2}F(\Omega)\,d\sigma(\Omega).
\tag{3}
\]

A positive quadrature is a discrete measure

\[
q_N=\sum_{i=1}^{N}w_i\delta_{\Omega_i},
\qquad \Omega_i\in S^2,
\qquad w_i>0,
\tag{4}
\]

satisfying

\[
\sum_{i=1}^{N}w_iF(\Omega_i)=b.
\tag{5}
\]

If the constant function belongs to \(\mathcal V\), normalization \(\sum_iw_i=4\pi\) is already one of the moment equations.

### Proposition 1 (moment-cone characterization)

For prescribed candidate nodes \(\Omega_1,\ldots,\Omega_P\), let

\[
A=[F(\Omega_1)\;\cdots\;F(\Omega_P)].
\tag{6}
\]

A positive rule supported on this pool exists exactly when

\[
b\in\operatorname{cone}\{F(\Omega_1),\ldots,F(\Omega_P)\},
\tag{7}
\]

or equivalently when \(Aw=b\) has a solution \(w\ge0\).  Removing zero-weight nodes leaves strictly positive weights on the reported support.

#### Proof

Equation (5) is precisely a conic combination of the candidate feature vectors. ∎

Strict positivity at every member of a *prescribed* \(P\)-node pool is stronger than positive cubature and can be infeasible even when a sparse positive support exists.  The package therefore reports only the active support and discards numerical zero weights.

---

## 2. Existence and upper node bounds

Assume \(1\in\mathcal V\).  Divide (3) by \(4\pi\).  Because

\[
\frac{b}{4\pi}
=\int_{S^2}F(\Omega)\frac{d\sigma}{4\pi},
\tag{8}
\]

it lies in the convex hull of \(F(S^2)\).  The constant coordinate confines that image to an affine subspace of dimension at most \(K-1\).

### Theorem 2 (Tchakaloff–Carathéodory existence)

For every finite-dimensional \(\mathcal V\subset C(S^2)\) containing constants, there is a positive quadrature exact on \(\mathcal V\) with at most \(K=\dim\mathcal V\) nodes.

#### Proof

Carathéodory's theorem in the affine hull of \(F(S^2)\) represents \(b/(4\pi)\) as a convex combination of at most \((K-1)+1=K\) feature vectors.  Multiplication by \(4\pi\) gives positive quadrature weights.  Any zero coefficients are removed. ∎

This is an existence theorem.  It does not guarantee symmetry, separation, uniqueness, a prescribed node count, or a lower bound on the smallest weight.

### Corollary 2.1 (finite reference discretization)

If a positive high-order reference quadrature integrates the target moments to the desired numerical tolerance, then a basic feasible solution of the finite-pool linear program has no more than \(\operatorname{rank}(A)\le K\) active nodes.  A subsequent nullspace support-reduction step can enforce this bound explicitly while preserving the moments and positivity.

---

## 3. Lower node bounds

Upper bounds alone do not establish efficiency or infeasibility at a requested \(N\).

### Theorem 3 (Gram/injectivity lower bound)

Let \(\mathcal U\) be an \(r\)-dimensional real function space such that

\[
uv\in\mathcal V\qquad\text{for every }u,v\in\mathcal U.
\tag{9}
\]

Every positive quadrature exact on \(\mathcal V\) requires

\[
N\ge r.
\tag{10}
\]

#### Proof

If \(N<r\), the evaluation map

\[
E:\mathcal U\to\mathbb R^N,
\qquad E(u)=(u(\Omega_1),\ldots,u(\Omega_N))
\]

has a nonzero kernel.  Choose \(0\ne u\in\ker E\).  Exactness for \(u^2\in\mathcal V\) gives

\[
0<\int_{S^2}u^2\,d\sigma
=\sum_iw_iu(\Omega_i)^2=0,
\]

a contradiction. ∎

If \(\mathcal V\) contains all spherical harmonics through degree \(L\), take \(\mathcal U\) to contain harmonics through degree \(\lfloor L/2\rfloor\).  Products then have degree at most \(L\), yielding

\[
N\ge\left(\lfloor L/2\rfloor+1\right)^2.
\tag{11}
\]

This general lower bound is often not sharp.  Symmetry, equal-weight restrictions, or a prescribed node family can require more nodes.

### Fixed-\(N\) infeasibility routes

There are three logically different certificates:

1. **Dimension/Gram certificate:** if \(N<r\) in Theorem 3, no variable-node positive rule can exist.
2. **Fixed candidate-pool Farkas certificate:** for matrix \(A\), infeasibility of \(Aw=b,w\ge0\) is certified by a vector \(y\) with
   \[
   A^Ty\ge0,
   \qquad b^Ty<0.
   \tag{12}
   \]
3. **Global variable-node residual certificate:** define
   \[
   \delta_N=
   \inf_{\Omega_i\in S^2,\,w_i\ge0,\,\sum_iw_i=4\pi}
   \left\|\sum_iw_iF(\Omega_i)-b\right\|_Q.
   \tag{13}
   \]
   A certified positive lower bound on \(\delta_N\) proves infeasibility.  Such a bound can be obtained by interval branch-and-bound over angular boxes, or—when the features are polynomial/spherical-harmonic—by a moment/SOS relaxation with a verified dual bound.

The implementation supplies items 1 and 2 and a certified finite-pool minimum residual.  A global variable-node certificate is algorithmically specified but is not needed in the benchmark because the Tchakaloff construction succeeds at \(N=K\).

---

## 4. Equal-weight designs, positive cubature, and response rules

These objects should not be conflated.

### Equal-weight spherical design

\[
w_i=4\pi/N
\]

and the nodes integrate a prescribed polynomial/harmonic space.  Equal weights simplify some transport formulas but impose a strong nonlinear constraint.

### Unequal positive cubature

Nodes and weights are free subject to \(w_i>0\) and moment exactness.  Theorem 2 applies directly and generally gives smaller support than an equal-weight design.

### Response-weighted quadrature

The exactness space includes transport-derived functions, or the optimization norm gives them greater importance.  It need not be rotationally invariant.

### Adaptive local rule

Different spatial cells, faces, or material layers use different angular supports.  Such a framework additionally requires conservative inter-grid transfer; positivity and moment exactness of each grid do not by themselves provide a feasible transfer.

---

## 5. Response-weighted measures

For response \(m\), a natural importance density is

\[
d\nu_m(\Omega)
=\rho_m(\Omega)d\sigma(\Omega),
\qquad
\rho_m\propto
|\psi(\Omega)\psi_m^\dagger(\Omega)|^p,
\tag{14}
\]

with \(p\in(0,1]\) available to reduce extreme concentration.

### Multiresponse balancing

Let

\[
g_m(\Omega)=|\psi(\Omega)\psi_m^\dagger(\Omega)|^p,
\qquad
\widehat g_m=\frac{g_m}{\int g_m\,d\sigma}.
\]

Define

\[
\rho(\Omega)=
\frac{1-\alpha}{4\pi}
+\frac{\alpha}{M}\sum_{m=1}^{M}\widehat g_m(\Omega),
\qquad 0\le\alpha<1.
\tag{15}
\]

Each response contributes unit mass before averaging, so a large response cannot dominate solely by scale.  The uniform floor makes \(\rho>0\), which is essential for reweighting and conditioning.

### Surface exactness or \(\nu\)-exactness?

Physical angular integrals in the transport equation are normally under \(d\sigma\).  The default rule should therefore satisfy (5) under surface measure even when \(\rho\) guides candidate placement or residual weighting.

If nodes are designed under \(d\nu=\rho d\sigma\), surface integrals obey

\[
\int f\,d\sigma
=\int \frac{f}{\rho}\,d\nu.
\tag{16}
\]

Thus exact \(\nu\)-integration of \(f/\rho\) is equivalent to surface exactness for \(f\), provided \(\rho\) is strictly positive.  Exactness under \(\nu\) without this transformation preserves a different quantity and should be used only when that response-weighted expectation is itself the target.

---

## 6. Exact optimization problem

Let node \(i\) be parameterized by polar and azimuthal angles \((\theta_i,\phi_i)\).  Let \(Q\succeq0\) weight moment residuals, \(d_{ij}=\arccos(\Omega_i\cdot\Omega_j)\), and let \(\Phi\) be a separation barrier.  A general response design is

\[
\begin{aligned}
\min_{\theta,\phi,w}\quad &
\frac12\left\|Q^{1/2}
\left(\sum_iw_iF(\Omega_i)-b\right)\right\|_2^2\\
&+\lambda_{\rm sep}\sum_{i<j}\Phi(d_{ij})
+\lambda_{\rm move}\sum_i d(\Omega_i,\Omega_i^0)^2,\\
\text{subject to}\quad &w_i\ge0,
\qquad \sum_iw_i=4\pi,\\
&\mathcal S(\Omega,w)=0
\quad\text{for any imposed symmetry constraints.}
\end{aligned}
\tag{17}
\]

Exactness is imposed either by replacing the first objective term with the equality constraint

\[
\sum_iw_iF(\Omega_i)=b
\tag{18}
\]

or by a lexicographic solve: first minimize residual globally, then optimize separation within the certified minimum-residual set.

A hard lower bound \(w_i\ge w_{\min}>0\) improves conditioning but can destroy feasibility.  The reference algorithm instead uses \(w_i\ge0\), removes inactive nodes, and reports the smallest active weight.

### Fixed-node convex subproblem

For fixed nodes, solve

\[
\min_{w\ge0}\frac12\|Q^{1/2}(Aw-b)\|_2^2.
\tag{19}
\]

Exact feasibility is a linear program.  The near-exact problem is nonnegative least squares.

### KKT certificate for minimum residual

Let \(r=Aw-b\).  At the optimum of (19),

\[
A^TQr\ge0,
\qquad
w_i(A^TQr)_i=0.
\tag{20}
\]

For \(Q=I\), a dual-feasible residual direction \(y=r\) gives

\[
\inf_{z\ge0}\|Az-b\|_2
\ge
\frac{-b^Ty}{\|y\|_2}
\tag{21}
\]

whenever \(A^Ty\ge0\).  At an accurately solved projection, complementarity makes this lower bound equal the primal residual.  Near exact feasibility, residual normalization is numerically meaningless; the implementation suppresses a dual claim unless cone feasibility is resolved relative to \(\|A\|\|r\|\).

### Variable-node algorithm

1. Build a dense, positive, rotationally accurate reference pool.
2. Evaluate transport-derived features and target moments on that pool.
3. Solve the exact positive LP; if infeasible, return a Farkas certificate and the NNLS minimum residual.
4. Remove inactive weights and apply nullspace support reduction.
5. Optionally refine nodes with spherical coordinates and softmax-positive weights.
6. Re-evaluate moments and recertify with a fixed-pool LP on the union of refined and reference candidates.
7. Reject refinements that lose positivity, normalization, separation requirements, or the target residual.

This sequence separates the existence certificate (convex) from local geometric improvement (nonconvex).

---

## 7. Nonuniqueness and conditioning

Positive rules are generally nonunique because:

- the moment vector can lie in a high-dimensional face of the moment cone;
- rotations or material symmetries generate equivalent rules;
- the number of variables exceeds the number of constraints;
- different supports can represent the same moment vector.

Let

\[
V_{ki}=f_k(\Omega_i).
\tag{22}
\]

Weight conditioning is governed by the smallest nonzero singular value of \(V\), or \(V\operatorname{diag}(\sqrt w)\) in a mass-weighted norm.  Node perturbation conditioning is governed by the Jacobian

\[
\mathcal J=
\left[
F(\Omega_i),
\;w_i\partial_{\theta_i}F(\Omega_i),
\;w_i\partial_{\phi_i}F(\Omega_i)
\right]_{i=1}^{N}.
\tag{23}
\]

Small weights, clustered nodes, nearly dependent features, and symmetry constraints that duplicate columns all reduce the smallest singular value.  Recommended diagnostics are:

1. numerical rank and nonzero condition number of \(V\operatorname{diag}(\sqrt w)\);
2. minimum active weight and weight ratio;
3. minimum node separation;
4. residual sensitivity under node perturbations;
5. rank and condition number of \(\mathcal J\) after removing known rotational null modes.

Feature scaling is essential.  The implementation normalizes custom modes in a reference weighted \(L^2\) norm before optimization.

---

## 8. Error certificates

### 8.1 Pure quadrature error

Let \(I(g)=\int g\,d\sigma\), \(Q(g)=\sum_iw_ig(\Omega_i)\), and assume \(Q\) is positive with total mass \(4\pi\).

### Theorem 4 (best-approximation bound)

If \(Q(v)=I(v)\) for every \(v\in\mathcal V\), then

\[
|I(g)-Q(g)|
\le 8\pi\inf_{v\in\mathcal V}\|g-v\|_\infty.
\tag{24}
\]

#### Proof

For any \(v\in\mathcal V\), exactness gives

\[
|I(g)-Q(g)|=|I(g-v)-Q(g-v)|.
\]

Positivity and equal total mass imply

\[
|I(g-v)|\le4\pi\|g-v\|_\infty,
\qquad
|Q(g-v)|\le4\pi\|g-v\|_\infty.
\]

Take the infimum. ∎

If the moment residual is \(r=Aw-b\) and \(v=\sum_ka_kf_k\), then

\[
|I(g)-Q(g)|
\le8\pi\|g-v\|_\infty+|a^Tr|.
\tag{25}
\]

### 8.2 Transport-response error

Let the exact angularly continuous problem be

\[
L\psi=q,
\qquad J_m=c_m(\psi),
\]

and the quadrature problem be \(L_Q\psi_Q=q_Q\).  Let the discrete adjoint satisfy

\[
L_Q^\dagger z_{m,Q}=c_{m,Q}.
\]

Then the exact algebraic identity

\[
J_{m,Q}-J_m
=-\langle z_{m,Q},(L_Q-L)\psi\rangle
+\langle z_{m,Q},q_Q-q\rangle
+\text{response-functional consistency term}
\tag{26}
\]

connects angular moment error to response error.  If the operator/source integrands lie in or are well approximated by \(\mathcal V\), apply (24) or (25) to each term.  In a bounded-inverse form,

\[
\|\psi_Q-\psi\|
\le\|L_Q^{-1}\|
\left(\|(L-L_Q)\psi\|+\|q_Q-q\|\right),
\tag{27}
\]

and

\[
|J_{m,Q}-J_m|
\le\|c_{m,Q}\|\|\psi_Q-\psi\|+\text{functional quadrature error}.
\tag{28}
\]

The adjoint form is usually sharper because it weights only the operator defects that influence the selected response.

---

## 9. Positivity of weights versus positivity of transport

### Proposition 5

Positive quadrature weights are necessary for a standard positive scattering integral but are not sufficient for a nonnegative discrete transport solution.

A sufficient finite-dimensional condition is:

1. nonnegative boundary and volume sources;
2. nonnegative scattering/production coefficients;
3. a streaming–removal discretization whose system matrix is a nonsingular \(M\)-matrix, or an iteration with a nonnegative transport sweep and spectral radius below one;
4. nonnegative transfer/interpolation operators wherever angular grids change.

#### Explanation

Positive weights make a nonnegative angular flux produce a nonnegative quadrature integral.  Negative spatial interpolation, an overcritical scattering iteration, a nonmonotone stabilization, or a transfer matrix with negative entries can still produce negative flux.  Positivity is therefore a property of the full assembled inverse, not the weights in isolation.

---

## 10. Minimal examples

### Example 1 (constant only)

For \(\mathcal V=\operatorname{span}\{1\}\), any one node with weight \(4\pi\) is exact.

### Example 2 (constants and first moments)

For \(\{1,x,y,z\}\), two antipodal nodes with weights \(2\pi\) integrate all first moments exactly.  This illustrates nonuniqueness: every antipodal axis works.

### Example 3 (degree two)

A regular tetrahedron with vertices

\[
\frac1{\sqrt3}(1,1,1),
\frac1{\sqrt3}(1,-1,-1),
\frac1{\sqrt3}(-1,1,-1),
\frac1{\sqrt3}(-1,-1,1)
\]

and weights \(\pi\) is exact for spherical harmonics through degree two.  Theorem 3 gives \(N\ge4\), so the rule is node-optimal within positive quadrature.

### Example 4 (fixed north-pole pool is infeasible)

For the single candidate \(\Omega=(0,0,1)\) and moments \(\{1,z\}\), the target is \((4\pi,0)\), while the only feature column is \((1,1)^T\).  The vector

\[
y=(-1,1)^T
\]

satisfies \(A^Ty=0\) and \(b^Ty=-4\pi<0\), certifying infeasibility.

---

## 11. HTS-specific construction route

1. Run a reference forward/adjoint solve on representative tape locations and incident fields.
2. Build a baseline harmonic space sufficient for rotationally smooth scattering.
3. Add normalized modes for:
   - forward boundary flux at the tape;
   - adjoints for layer heating, REBCO flux, photon production, and selected reaction rates;
   - contributons \(\psi\psi_m^\dagger\);
   - grazing functions localized in \(|\Omega\cdot n|\);
   - narrow streaming/shielding modes tied to blanket penetrations or accelerator incidence.
4. Form the balanced density (15) for candidate placement, while retaining surface-measure targets.
5. Solve the finite-pool positive moment LP and reduce support.
6. Validate on held-out incident fields, material variants, and responses not included in the design basis.
7. Reject rules with poor minimum weight, small node separation, or unstable moment Jacobian even if nominally exact.
8. Couple accepted rules to the conservative-transfer/adaptivity framework of Paper 2B.

A single universal HTS rule is unlikely to be optimal across all magnet locations.  A small certified library indexed by incident-spectrum/normal-direction clusters is more defensible.

---

## 12. Numerical result in this package

A 288-node Gauss–Legendre/azimuthal product rule supplied target moments for:

- nine real spherical harmonics through degree two;
- a forward streaming mode;
- an adjoint streaming mode;
- their contributon;
- a narrow grazing mode;
- a shielded-direction mode.

The harmonic-only positive rule used 9 active nodes.  The enriched rule used 14 active nodes, equal to the feature dimension, with maximum target residual \(9.67\times10^{-11}\).  The reference enriched feature matrix had nonzero condition number 6.09 after normalization.

For fixed Fibonacci pools:

| pool nodes | exact enriched rule? | certified minimum residual |
|---:|:---:|---:|
| 5 | no | 2.3141 |
| 8 | no | 1.3849 |
| 12 | no | 0.5225 |
| 16 | no | 0.3382 |
| 24 | yes, 14 active | \(5.45\times10^{-14}\) numerical residual |

Every infeasible fixed pool had both a Farkas certificate and a matching KKT projection bound.  For the feasible 24-node pool, the code correctly suppresses a normalized dual claim because the remaining residual is floating-point noise.

---

## 13. Constructive deliverables

The implementation is in `src/hts_angular/quadrature.py` and includes:

- deterministic Fibonacci and product-sphere candidate rules;
- real orthonormal spherical harmonics;
- balanced multiresponse densities;
- positive finite-pool LP construction;
- Carathéodory support reduction;
- Farkas certificates;
- nonnegative least-squares minimum residual and KKT diagnostics;
- conditioning diagnostics;
- local nonlinear node/weight refinement;
- node-count bounds.

Regression tests cover harmonic exactness, the optimal tetrahedron, fixed-pool infeasibility, projection certificates, and strictly positive support.

---

## 14. References inspected

- Ahrens, C. D., “Lagrange Discrete Ordinates,” arXiv:1405.3968; later *Nuclear Science and Engineering*, DOI: 10.13182/NSE14-76.
- Zhou, Y., and Chen, X., “Spherical \(t_\epsilon\)-Designs for Approximations on the Sphere,” arXiv:1502.03562.
- Tchakaloff-type positive cubature and constructive finite-pool formulations.
- Literature on spherical designs, positive moment cones, optimal experimental design, and transport angular quadrature comparison.

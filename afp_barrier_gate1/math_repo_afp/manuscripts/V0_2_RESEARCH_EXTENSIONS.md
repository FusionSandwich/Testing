# Version 0.2 research extensions: finite grazing geometry, curved response operators, three-dimensional transport, authenticated data closure, calibration, and angular certificates

## Abstract

This manuscript completes the finite-dimensional research extensions that were deliberately left outside version 0.1 of the response-preserving transport-operator program.  The six extensions are: (i) exact finite three-dimensional ray geometry for grazing incidence on a bounded tape; (ii) a corrected physical-flux curvature-aware local boundary-to-response operator with fail-closed routing; (iii) a verified Cartesian three-dimensional multigroup discrete-ordinates reference solver with an exact algebraic adjoint; (iv) a provenance-aware processed nuclear-data schema with reaction-
\(Q\) energy closure and response-preserving group condensation; (v) campaign-aware generalized-least-squares calibration of transport descriptors to normalized HTS properties; and (vi) positive angular quadrature and graph-Laplacian certificates whose claims fail closed outside their proved regimes.

Every theorem below is tied to an executable construction and a regression or deterministic benchmark.  The results are exact for the declared finite-dimensional models.  They do not certify a named evaluated nuclear-data library, universal REBCO material coefficients, arbitrary CAD geometry, production-scale parallel transport, or uniform one-dimensional curved-interface validity through grazing.

---

## 1. Notation and declared model class

Let a transported state index \(\alpha=(s,g,i)\) combine species, energy group, and angular ordinate.  A one-dimensional layer has state vector \(\psi\in\mathbb R^n\), total-removal matrix \(T=\operatorname{diag}(\Sigma_{t,\alpha})\), nonnegative production/scattering matrix \(S\), fixed source \(q\), and response density

\[
  \frac{dJ}{dx}=H\psi+s_J.
\]

Version 0.1 constructs the exact two-sided affine response operator for a planar layer.  Version 0.2 introduces a local normal coordinate \(s\in[-h/2,h/2]\), finite three-dimensional tape dimensions, a position-dependent metric Jacobian \(\mathcal J(s)\), and position-dependent normal directional cosines \(\mu_\alpha(s)\).  The corrected frozen-tangent curved local model is

\[
  D_\mu(s)\frac{d\psi}{ds}
  =(S-T-L_t)\psi(s)+q,
  \tag{1.1}
\]

where \(D_\mu(s)=\operatorname{diag}(\mu_\alpha(s))\) and \(L_t\) is a declared frozen tangential-leakage closure.  Responses satisfy

\[
  \frac{dJ}{ds}=\mathcal J(s)\bigl[H\psi(s)+s_J\bigr].
  \tag{1.2}
\]

For a fixed global direction, the full conservative curvilinear streaming
operator contains normal and tangential divergences whose metric derivatives
cancel.  The earlier normal-only metric-current formula retained one half of
that cancellation and produced spurious curvature focusing, including
non-identity transmission in vacuum.  Equation (1.1) is the corrected local
cell; leading tangential/curvature transport routes to the three-dimensional
solver.  The Jacobian remains in (1.2) because responses use physical volume
measure per unit midsurface area.

The finite-volume three-dimensional solver uses a Cartesian grid, a positive spherical quadrature \(\{(\Omega_i,w_i)\}_{i=1}^{N_\Omega}\), first-order upwind fluxes, isotropic multigroup scattering, prescribed incoming data on all six faces, and arbitrary linear cell/angle response kernels.

---

# Part I. Finite three-dimensional grazing geometry

## 2. Exact ray intersection with a finite tape volume

### Definition 2.1 (oriented finite tape)

Let \(R=[u\ v\ n]\in SO(3)\) be a right-handed local frame with origin \(x_c\).  A finite tape volume is

\[
  \mathcal B
  =\left\{x_c+R\xi:
      |\xi_1|\le L/2,
      |\xi_2|\le W/2,
      |\xi_3|\le h/2
    \right\},
  \tag{2.1}
\]

with length \(L>0\), width \(W>0\), and thickness \(h>0\).

For a directed ray \(x(t)=x_0+t\Omega\), \(t\ge0\), define local origin \(a=R^T(x_0-x_c)\), local direction \(d=R^T\Omega\), and half-widths \(b=(L/2,W/2,h/2)\).

### Theorem 2.2 (exact directed-ray interval)

For each coordinate \(k\), set

\[
  I_k=
  \begin{cases}
  [(-b_k-a_k)/d_k,(b_k-a_k)/d_k] & d_k>0,\\
  [(b_k-a_k)/d_k,(-b_k-a_k)/d_k] & d_k<0,\\
  \mathbb R & d_k=0\text{ and }|a_k|\le b_k,\\
  \varnothing & d_k=0\text{ and }|a_k|>b_k.
  \end{cases}
  \tag{2.2}
\]

Then the ray intersection is nonempty exactly when

\[
  [t_-,t_+]=[0,\infty)\cap I_1\cap I_2\cap I_3
  \tag{2.3}
\]

is nonempty.  Its chord length is \(t_+-t_-\) for unit \(\Omega\).

#### Proof

The inequality \(|a_k+t d_k|\le b_k\) is equivalent to membership in \(I_k\).  The box is the intersection of the three coordinate slabs, and the directed ray adds \(t\ge0\).  Intersecting these four intervals gives (2.3).  Because the direction is normalized, Euclidean arclength equals the parameter difference.  No small-direction division is used when \(d_k=0\).  ∎

The implementation is `hts_transport_ops.geometry3d.OrientedTapeVolume.ray_interval` and `chord_length`.

### Corollary 2.3 (finite regularization of the grazing singularity)

For any line through the box,

\[
  \ell_{\mathcal B}(x_0,\Omega)
  \le \sqrt{L^2+W^2+h^2}.
  \tag{2.4}
\]

Consequently, the finite-tape optical thickness satisfies

\[
  \tau_{\mathrm{finite}}\le
  \Sigma_t\sqrt{L^2+W^2+h^2},
  \tag{2.5}
\]

whereas the infinite planar slab surrogate \(h/|\Omega\cdot n|\) diverges as \(|\Omega\cdot n|\to0\).

#### Proof

Every chord of a bounded rectangular box is no longer than its space diagonal.  Multiply by nonnegative \(\Sigma_t\).  ∎

This result does **not** say that grazing transport is easy.  It says that the physical path is finite and that a divergent infinite-slab optical thickness is the wrong geometric model once the side faces are encountered first.

## 3. Cylindrical patch measure and normal-rotation control

For a cylinder of radius \(R\), angular interval \(\Delta\theta\), and axial interval \(\Delta z\), the exact mid-surface area is

\[
  A_{\mathrm{exact}}=R\Delta\theta\Delta z.
  \tag{3.1}
\]

The implemented patch uses the exact arc width

\[
  \ell_{\mathrm{arc}}=R\Delta\theta
  \tag{3.2}
\]

as its reference quadrature measure, so its stored reference area is
\(A_{\mathrm{patch}}=\ell_{\mathrm{arc}}\Delta z\).

### Proposition 3.1 (exact reference-area partition)

For any positive axial and azimuthal patch counts, the sum of all patch reference areas equals the analytic cylindrical area

\[
  \sum_p A_p=R\Theta L_z
  \tag{3.3}
\]

up to floating-point summation, where \(\Theta\) is the total angular span and \(L_z\) the axial length.

#### Proof

Every one of the \(N_zN_\theta\) patches has area
\((L_z/N_z)(R\Theta/N_\theta)\). Summation gives (3.3). ∎

This exact area statement concerns the integration measure, not geometric identity between the curved surface and a planar patch. The patch frame is placed at the angular midpoint. The largest normal rotation between that midpoint normal and either azimuthal edge is

\[
  \delta_n=\frac{\Delta\theta}{2}=\frac{\Theta}{2N_\theta},
  \tag{3.4}
\]

which is the explicit first-order geometric routing diagnostic. Finite ray paths through material remain governed by the exact oriented-volume geometry or the three-dimensional solver, not by replacing an arc with an unreported chord.

---

# Part II. Corrected frozen-tangent curvature-aware response operators

## 4. Transformed nonautonomous system

Assume two frozen principal curvatures \(\kappa_1,\kappa_2\) and

\[
  \mathcal J(s)=(1+\kappa_1s)(1+\kappa_2s)>0.
  \tag{4.1}
\]

Let

\[
  \mu_\alpha(s)=\mu_{\alpha,0}+s\dot\mu_\alpha
  \tag{4.2}
\]

and assume \(|\mu_\alpha(s)|\ge\mu_*>0\) with no sign change throughout the layer.  Define \(K=S-T-L_t\).  Then the corrected equations are

\[
  \psi'(s)=D_\mu(s)^{-1}\bigl[K\psi(s)+q\bigr],
  \tag{4.3}
\]

\[
  J'(s)=\mathcal J(s)\bigl[H\psi(s)+s_J\bigr].
  \tag{4.4}
\]

Introduce the augmented state \(z=(\psi,1,J)^T\).  It obeys

\[
  z'(s)=B(s)z(s),
  \quad
  B(s)=
  \begin{bmatrix}
    D_\mu(s)^{-1}K & D_\mu(s)^{-1}q & 0\\
    0&0&0\\
    \mathcal J(s)H&\mathcal J(s)s_J&0
  \end{bmatrix}.
  \tag{4.5}
\]

### Theorem 4.1 (well-posed local propagator)

If \(\mathcal J\) and \(\mu_\alpha\) are continuous, \(\mathcal J(s)>0\), and \(|\mu_\alpha(s)|\ge\mu_*>0\) on the closed interval, then \(B\) is continuous and bounded.  The initial-value problem (4.5) has a unique fundamental matrix \(\Phi(s,s_0)\), and every response is a linear-affine function of the incoming physical boundary state.

#### Proof

Continuity and the non-grazing lower bound make every entry of \(B(s)\) continuous and bounded.  The standard finite-dimensional linear ODE existence and uniqueness theorem gives a unique fundamental matrix.  The augmented constant coordinate converts affine source terms into a linear system, so extraction of boundary and response blocks is linear in the augmented state.  ∎

The implementation refuses metric zeros, grazing approaches, and directional sign changes.  Such states are routed to finite three-dimensional treatment.

## 5. Direct two-sided Schur extraction

If the physical-flux propagator has blocks

\[
  \begin{bmatrix}\psi_R\\1\\J_R-J_L\end{bmatrix}
  =
  \begin{bmatrix}
    E&g&0\\0&1&0\\F&c&I
  \end{bmatrix}
  \begin{bmatrix}\psi_L\\1\\0\end{bmatrix},
  \tag{5.1}
\]
the exact version 0.1 boundary Schur construction applies directly to
\((E,g,F,c)\) and produces reflection, transmission, internal-response rows,
and source offsets. Curvature changes the response measure and routing, but it
does not introduce an endpoint flux similarity transform in the frozen cell.

### Theorem 5.1 (flat-limit equivalence)

If \(\kappa_1=\kappa_2=0\), \(\dot\mu=0\), and \(L_t=0\), then the curved construction is exactly the planar augmented exponential and therefore yields the same response operator up to floating-point roundoff.

#### Proof

Under the hypotheses, \(\mathcal J=1\), \(D_\mu\) is constant, and \(B(s)\equiv B\).  The path-ordered exponential is exactly the planar augmented exponential and the same Schur map is applied.  ∎

## 6. Magnus integration and observed order

For one interval \([a,b]\), \(\Delta=b-a\), midpoint \(m\), and Gauss points

\[
  s_{1,2}=m\mp\frac{\sqrt3}{6}\Delta,
  \tag{6.1}
\]

let \(B_j=B(s_j)\).  The implemented fourth-order Gauss–Magnus step is

\[
  \Phi_4(b,a)=\exp\left[
    \frac{\Delta}{2}(B_1+B_2)
    +\frac{\sqrt3\Delta^2}{12}[B_2,B_1]
  \right].
  \tag{6.2}
\]

### Proposition 6.1 (local and global order)

If \(B\) is sufficiently smooth and remains bounded on the interval, the midpoint exponential has local error \(O(\Delta^3)\) and global error \(O(\Delta^2)\).  The two-point Gauss–Magnus step (6.2) has local error \(O(\Delta^5)\) and global error \(O(\Delta^4)\).

#### Proof sketch

Expand the exact Magnus exponent and the quadrature/commutator approximation in powers of \(\Delta\).  Midpoint quadrature matches the first integral through degree one and omits third-order terms.  The two Gauss points integrate the required cubic moments exactly, while the commutator term matches the second Magnus term through fourth order.  Composition over \(O(1/\Delta)\) steps reduces local order by one. The regression suite independently checks the adaptive fourth-order path against a tighter refined reference. ∎

The adaptive implementation compares one full fourth-order step with two half steps.  It reports the actual fine/coarse matrix discrepancy and recursively subdivides; it does not present the discrepancy as a mathematically sharp global error bound.

The general Magnus framework and its structure-preserving properties are reviewed by Blanes, Casas, Oteo, and Ros, *Physics Reports* 470 (2009), arXiv:0810.5488.

## 7. Balance qualification for a frozen curved patch

The full conservative curvilinear equation has both the normal boundary
current and the tangential patch-boundary current.  After the tangential
divergence is frozen out, the local cell cannot simultaneously claim an exact
curved control-volume balance with endpoint \(\mathcal J\)-weighted currents.
Doing so was the source of the former vacuum-focusing defect.

The corrected implementation guarantees:

1. exact planar Paper 1 balance when \(\mathcal J=1\);
2. identity angular-flux transmission in curved vacuum;
3. physical \(\mathcal J\)-weighted volume-response accumulation; and
4. fail-closed routing when curvature/tangential terms are not negligible.

For a finite curved surface control volume, the exact balance is instead

\[
I_{\rm broad,out}+I_{\rm lateral,out}+R
=I_{\rm broad,in}+I_{\rm lateral,in}+Q+P,
\tag{7.1}
\]

and must be audited in the retained multidimensional equation. The quadratic
volume-measure identity remains

\[
  \int_{-h/2}^{h/2}\mathcal J(s)\,ds
  =h+\frac{\kappa_1\kappa_2h^3}{12}.
  \tag{7.2}
\]

---

# Part III. Verified Cartesian three-dimensional discrete ordinates

## 8. Discrete forward problem

Let cell \(c=(i,j,k)\) have widths \(\Delta x_i,\Delta y_j,\Delta z_k\).  For group \(g\) and direction \(a\), the first-order upwind equation is

\[
  \left(\Sigma_{t,g,c}
  +\frac{|\Omega_{a,x}|}{\Delta x_i}
  +\frac{|\Omega_{a,y}|}{\Delta y_j}
  +\frac{|\Omega_{a,z}|}{\Delta z_k}
  \right)\psi_{gac}
  -\sum_{f\in\mathrm{upwind}}\gamma_{a,f}\psi_{ga,c_f}
  -\sum_{g',a'}\frac{w_{a'}}{W}
      \Sigma_{s,g'\to g,c}\psi_{g'a'c}
  =q_{gac}+q^{\partial}_{gac},
  \tag{8.1}
\]

where \(W=\sum_a w_a\) and \(q^\partial\) contains prescribed incoming faces.  In matrix form,

\[
  A\Psi=b.
  \tag{8.2}
\]

The direct reference solver assembles \(A\) and uses a sparse solve.  Source iteration separates the streaming/removal block \(L\) from scattering \(K\):

\[
  L\Psi^{(m+1)}=b+K\Psi^{(m)}.
  \tag{8.3}
\]

## 9. Positivity, uniqueness, and balance

### Proposition 9.1 (positive sweep)

For nonnegative boundary data and source, nonnegative scattering, and strictly positive sweep denominators, one transport sweep maps a nonnegative iterate to a nonnegative iterate.

#### Proof

Every upwind value, fixed source, and scattering source in the sweep numerator is nonnegative.  Division is by a strictly positive diagonal coefficient.  Induction in each directional topological sweep order gives nonnegative cell flux.  ∎

### Theorem 9.2 (source-iteration convergence under a discrete subcritical condition)

If \(\rho(L^{-1}K)<1\), source iteration converges from every initial iterate to the unique solution

\[
  \Psi=(L-K)^{-1}b.
  \tag{9.1}
\]

#### Proof

The error satisfies \(e^{(m+1)}=L^{-1}Ke^{(m)}\).  A finite-dimensional stationary iteration converges for every initial error exactly when the iteration matrix has spectral radius below one.  Then \(I-L^{-1}K\) is invertible and (9.1) follows.  ∎

The implementation does not estimate \(\rho(L^{-1}K)\) as a proof of convergence; it checks residual reduction and fails if the requested tolerance is not met.

### Theorem 9.3 (global discrete particle balance)

Suppose the discrete solution satisfies (8.1).  Multiply each equation by \(w_aV_c\), sum over all groups, directions, and cells, and define the absorption/removal coefficient

\[
  \Sigma_{a,g,c}=\Sigma_{t,g,c}-\sum_{g'}\Sigma_{s,g\to g',c}.
  \tag{9.2}
\]

Then internal upwind face terms cancel pairwise and

\[
  Q_{\mathrm{vol}}+Q_{\mathrm{in}}
  =Q_{\mathrm{out}}+Q_{\mathrm{abs}}+r,
  \tag{9.3}
\]

where \(r\) is the weighted algebraic residual.  For an exact discrete solve, \(r=0\).

#### Proof

Every internal Cartesian face appears once as outflow from its upwind cell and once as inflow to its downwind cell with equal geometric coefficient and opposite sign.  Scattering summed over outgoing groups cancels the corresponding production part, leaving (9.2).  Only external faces, volume sources, absorption, and the algebraic residual remain.  ∎

## 10. Exact algebraic adjoint identity

For a response \(J=c^T\Psi\), define the discrete adjoint

\[
  A^Tz=c.
  \tag{10.1}
\]

### Theorem 10.1 (machine-checkable forward–adjoint consistency)

For exact solves,

\[
  J=c^TA^{-1}b=z^Tb.
  \tag{10.2}
\]

For inexact forward and adjoint vectors,

\[
  c^T\widetilde\Psi-\widetilde z^Tb
  =\widetilde z^T(A\widetilde\Psi-b)
   -(A^T\widetilde z-c)^T\widetilde\Psi.
  \tag{10.3}
\]

#### Proof

Equation (10.2) is transposition of a scalar.  Add and subtract \(\widetilde z^TA\widetilde\Psi\) to derive (10.3).  ∎

The code solves the exact matrix transpose rather than separately discretizing a continuous adjoint with potentially inconsistent boundary conventions.

## 11. Deterministic shared-memory angular parallelism

Angles are independent inside a fixed transport sweep.  Tasks are submitted in canonical \((g,a)\) order, each task returns its complete cell array, and the main thread writes results back in canonical indices.  No floating-point reduction over completion order is performed.

### Proposition 11.1 (worker-count reproducibility)

For identical inputs, platform, NumPy/SciPy versions, and source-iteration history, changing the thread count leaves every per-angle sweep result and the assembled flux byte-identical.

#### Proof

Each task reads immutable inputs and writes a private array.  The task arithmetic is independent of thread completion order.  Assembly is by deterministic indices, and scalar-flux reduction occurs only after assembly in a fixed NumPy order.  ∎

This is a reproducibility property of the reference shared-memory implementation, not a claim of production distributed-memory scalability.

---

# Part IV. Provenance-aware processed nuclear data and energy closure

## 12. Data convention

For group \(g\), let \(E_g>0\) be the declared representative transported energy, \(\Sigma_{t,g}\) total removal, and \(S_{g'g}\ge0\) the macroscopic production rate into outgoing group \(g'\) per incoming group \(g\).  Let reaction \(r\) have macroscopic rate \(\Sigma_{r,g}\) and locally deposited residual energy \(q_{r,g}\), which may include a signed reaction \(Q\)-value under the declared convention.

Define transported-secondary energy removal and local reaction contribution

\[
  P_g=\sum_{g'}E_{g'}S_{g'g},
  \qquad
  Q_g=\sum_r q_{r,g}\Sigma_{r,g}.
  \tag{12.1}
\]

The local deposition coefficient is

\[
  D_g=E_g\Sigma_{t,g}-P_g+Q_g+c_g,
  \tag{12.2}
\]

where \(c_g\) is an explicit closure correction, never an implicit silent adjustment.

### Definition 12.1 (admissible processed dataset)

A processed dataset is admissible when arrays have declared dimensions and units, all rates and production entries that must be nonnegative are nonnegative, provenance hashes have valid form, group/species labels are complete, and

\[
  D_g\ge-\varepsilon_g
  \tag{12.3}
\]

for the configured scale-aware tolerance.

### Theorem 12.2 (transport-plus-local energy identity)

For any nonnegative group angular flux, multiplying the collision balance by representative energy and adding the local-heating response with coefficient \(D_g\) closes the declared prompt transported-energy balance exactly at the group model level.

#### Proof

An incoming total-removal event removes \(E_g\Sigma_{t,g}\).  The production matrix returns \(P_g\) to represented transported groups.  Reactions add the declared local residual \(Q_g\), and \(c_g\) records any explicit closure convention.  Their difference is (12.2), so transported secondary energy plus local deposition equals the declared incoming removal/reaction energy.  Summation against angular flux preserves the identity by linearity.  ∎

This is an accounting theorem for the supplied processed arrays.  It does not prove that the arrays came from a correct evaluated-data processing chain.

## 13. Content-addressed provenance

A content digest is computed over canonical little-endian arrays, array shapes, reaction/species/group labels, provenance, and metadata.  HDF5 layout details are excluded from the scientific digest.

### Proposition 13.1 (tamper detection within the declared payload)

Any bit change to a hashed array or any change to hashed labels, provenance, or metadata changes the SHA-256 input stream and is detected on load, except with the collision probability of SHA-256.

The source-file hashes stored in provenance are separately verifiable against the external processed-data inputs.

## 14. Contiguous response-preserving condensation

Let fine groups be partitioned into ordered contiguous same-species sets \(G_C\), and let \(\phi_g>0\) be prescribed condensation weights.  Define

\[
  \bar\Sigma_{t,C}
  =\frac{\sum_{g\in G_C}\phi_g\Sigma_{t,g}}
         {\sum_{g\in G_C}\phi_g},
  \tag{14.1}
\]

\[
  \bar\Sigma_{r,C}
  =\frac{\sum_{g\in G_C}\phi_g\Sigma_{r,g}}
         {\sum_{g\in G_C}\phi_g},
  \tag{14.2}
\]

and choose \(\bar q_{r,C}\) by reaction-rate weighting when the denominator is nonzero.

### Theorem 14.1 (weighted reaction-rate preservation)

For each reaction \(r\) and coarse group \(C\),

\[
  \bar\Sigma_{r,C}\sum_{g\in G_C}\phi_g
  =\sum_{g\in G_C}\phi_g\Sigma_{r,g}.
  \tag{14.3}
\]

#### Proof

Substitute (14.2).  ∎

The outgoing-group production matrix is collapsed with the same incoming weights.  Because a single representative coarse energy generally cannot preserve every fine energy moment simultaneously, the algorithm computes the desired weighted fine deposition and stores the difference from preliminary coarse closure as an explicit \(\bar c_C\).

### Theorem 14.2 (weighted deposition preservation)

With

\[
  \bar c_C
  =\frac{\sum_{g\in G_C}\phi_gD_g}{\sum_{g\in G_C}\phi_g}
   -\left(
      \bar E_C\bar\Sigma_{t,C}
      -\sum_{C'}\bar E_{C'}\bar S_{C'C}
      +\sum_r\bar q_{r,C}\bar\Sigma_{r,C}
    \right),
  \tag{14.4}
\]

coarse deposition satisfies

\[
  \bar D_C
  =\frac{\sum_{g\in G_C}\phi_gD_g}{\sum_{g\in G_C}\phi_g}.
  \tag{14.5}
\]

#### Proof

Insert (14.4) into the coarse analogue of (12.2); all preliminary terms cancel.  ∎

Neutron and photon groups are forbidden from sharing one coarse group because their species labels and response semantics are distinct.

---

# Part V. Campaign-aware calibration and uncertainty

## 15. Log-linear bounded generalized least squares

Let campaign-indexed observations \(y_i>0\) be normalized HTS properties and let \(x_i\in\mathbb R^p\) contain explicitly declared transport and irradiation descriptors. Version 0.2 uses

\[
  \log y=X\beta+\epsilon,
  \qquad \operatorname{Cov}(\epsilon)=C_{\log y}.
  \tag{15.1}
\]

When covariance \(C_y\) is supplied in ratio space, the implemented first-order delta transformation is

\[
  C_{\log y}\approx D_y^{-1}C_yD_y^{-1},
  \qquad D_y=\operatorname{diag}(y).
  \tag{15.2}
\]

Let \(C_{\log y}=LL^T\). Optional prior mean \(\beta_0\) and positive-definite precision \(P=R^TR\) are represented as additional whitened equations. The bounded problem is

\[
 \min_{\ell\le\beta\le u}
 \left\|L^{-1}(X\beta-\log y)\right\|_2^2
 +\left\|R(\beta-\beta_0)\right\|_2^2.
 \tag{15.3}
\]

Initialization is projected into the representable strict interior of every finite bound interval. Bounds with no floating-point interior, nonpositive evaluation budgets, non-positive-definite observation covariance, and inconsistent priors fail closed.

### Proposition 15.1 (free-subspace covariance and degrees of freedom)

Let \(F\) index parameters not locally active at a bound, and define the augmented whitened design \(A\). In the locally linear model with known observation covariance, version 0.2 reports

\[
  \widehat{\operatorname{Cov}}(\hat\beta)_{FF}
  =\left(A_F^TA_F\right)^+,
  \tag{15.4}
\]

with zero covariance assigned to locally fixed bound-active directions. The data degrees of freedom are

\[
  \nu=n-\operatorname{rank}\left[(L^{-1}X)_F\right].
  \tag{15.5}
\]

No reduced-\(\chi^2\) rescaling is applied because the supplied observation covariance is treated as known. If that covariance is only known up to a common scale, users must model or estimate that scale explicitly rather than relying on an undocumented multiplier.

For a prediction design \(X_*\),

\[
 C_{*,\log}=X_*\widehat{\operatorname{Cov}}(\hat\beta)X_*^T+C_{\mathrm{obs},*},
 \tag{15.6}
\]

where the optional observation term must be symmetric positive semidefinite. The first-order ratio-space covariance is

\[
 C_{*,y}\approx D_*C_{*,\log}D_*,
 \qquad D_*=\operatorname{diag}(e^{X_*\hat\beta}).
 \tag{15.7}
\]

## 16. HTS descriptor and sign model

The default design contains an intercept, a saturating \(\log(1+\mathrm{DPA}/s)\) term, a linear high-dose damage term, implanted concentration, absorbed energy, retained-defect fraction, irradiation-temperature shift, magnetic field, and a dose--retention interaction. Only the saturating-benefit coefficient is nonnegative and the linear damage coefficient nonpositive by default. Signs of implantation, heating, retention, temperature, and field remain free because they depend on material architecture, irradiation conditions, annealing, and characterization protocol.

This construction deliberately rejects a universal scalar-DPA law. The recent in-situ fusion-spectrum neutron study of Adams et al. at 40 K, including recovery after room-temperature annealing under its tested conditions, illustrates why irradiation temperature and annealing history must remain explicit (DOI 10.1088/1361-6668/ae4548).

## 17. Leave-one-campaign-out validation and campaign bootstrap

Rows within one irradiation campaign can share beam normalization, dosimetry, sample preparation, or characterization systematics. Random row-level splitting can therefore leak campaign information. The implementation removes every row of one campaign, refits on the remaining campaigns, and predicts the held-out campaign. This tests transfer across represented campaigns, not extrapolation to an unrepresented material, temperature, field, spectrum, or annealing history.

For the campaign bootstrap, entire campaign blocks are sampled with replacement. If campaign \(c\) has covariance block \(C_c\), a bootstrap sequence \((c_1,\ldots,c_K)\) uses

\[
 C^*=\operatorname{blockdiag}(C_{c_1},\ldots,C_{c_K}).
 \tag{17.1}
\]

### Proposition 17.1 (positive definiteness of repeated campaign blocks)

If every \(C_c\succ0\), then \(C^*\succ0\), including when a campaign label is sampled repeatedly.

#### Proof

A block-diagonal matrix is positive definite exactly when each diagonal block is positive definite. Repeating a positive-definite block preserves that property. ∎

Repeated draws are interpreted as independent replicate campaign blocks. Treating duplicated rows as the same random variable would instead produce a singular covariance and is not the implemented bootstrap.

---

# Part VI. Positive quadrature and graph certificates

## 18. Positive moment construction

For continuous features \(F:S^2\to\mathbb R^K\) and target moment \(b=\int F\,d\sigma\), a positive rule satisfies

\[
  \sum_{i=1}^{N}w_iF(\Omega_i)=b,
  \qquad w_i>0.
  \tag{18.1}
\]

Tchakaloff-type results guarantee finite positive cubature for finite-dimensional polynomial spaces.  The constructive implementation uses deterministic variable-node multistart optimization followed by a positive linear-programming recertification.  Nonlinear optimizer success alone is not accepted as a moment certificate.

Bayer and Teichmann provide a concise proof of Tchakaloff’s theorem for Borel measures with finite moments, *Proceedings of the AMS* 134 (2006), arXiv:math/0502473.

## 19. Harmonic Gram lower bound

Let the quadrature be exact for all spherical polynomials through degree \(t\), and set \(m=\lfloor t/2\rfloor\).  Let \(\mathcal H_{\le m}\) denote real spherical harmonics through degree \(m\), whose dimension is

\[
  d_m=(m+1)^2.
  \tag{19.1}
\]

### Theorem 19.1 (positive node lower bound)

Every positive quadrature exact through degree \(t\) has

\[
  N\ge(m+1)^2.
  \tag{19.2}
\]

#### Proof

Choose a basis \(\{Y_k\}_{k=1}^{d_m}\).  Products \(Y_kY_\ell\) have degree at most \(2m\le t\), so exactness gives the positive-definite continuous Gram matrix

\[
  G_{k\ell}=\int_{S^2}Y_kY_\ell\,d\sigma
  =\sum_{i=1}^Nw_iY_k(\Omega_i)Y_\ell(\Omega_i)
  =V^TWV.
  \tag{19.3}
\]

Thus \(d_m=\operatorname{rank}(G)\le\operatorname{rank}(V)\le N\).  ∎

### Corollary 19.2 (global minimality certificate)

If a positive exact rule with \(N=(\lfloor t/2\rfloor+1)^2\) is constructed and recertified, it is globally node-minimal among all positive rules exact through degree \(t\).

The version 0.2 benchmark constructs the degree-two tetrahedral rule with four nodes, attains the lower bound four, and therefore certifies global minimality in that case.

## 20. Fixed-pool minimum-support certificate

For candidate feature matrix \(A\in\mathbb R^{K\times M}\), target \(b\), positive tolerance \(\epsilon\), weights \(w_j\ge0\), and binary support variables \(z_j\), solve

\[
  \min\sum_{j=1}^Mz_j
  \tag{20.1}
\]

subject to

\[
  -\epsilon\le Aw-b\le\epsilon,
  \qquad 0\le w_j\le M_jz_j,
  \qquad z_j\in\{0,1\}.
  \tag{20.2}
\]

An optimizer certificate proves minimum support **on the supplied candidate pool**.  It does not prove continuous global minimality unless combined with a separate lower bound such as Theorem 19.1.

## 21. Positive graph Laplace–Beltrami family

For nodes \(\Omega_i\), positive quadrature weights \(w_i\), symmetric conductances \(c_{ij}=c_{ji}\ge0\), define

\[
  (Gf)_i=\frac1{w_i}\sum_jc_{ij}(f_j-f_i).
  \tag{21.1}
\]

### Theorem 21.1 (exact structural properties)

For every such conductance matrix:

1. \(G\mathbf1=0\);
2. \(WG=(WG)^T\), where \(W=\operatorname{diag}(w)\);
3. \(f^TWGf=-\frac12\sum_{ij}c_{ij}(f_i-f_j)^2\le0\);
4. off-diagonal entries of \(G\) are nonnegative;
5. \(e^{tG}\ge0\) and \(e^{tG}\mathbf1=\mathbf1\) for \(t\ge0\);
6. if the positive-edge graph is connected, the nullspace is exactly the constants.

#### Proof

The first three statements follow by direct summation and symmetry.  The generator is Metzler with zero row sums, so its exponential is a positive conservative semigroup.  The quadratic form vanishes exactly when \(f_i=f_j\) on every positive edge; connectivity forces a global constant.  ∎

The Laplace–Beltrami approximation itself is not exact merely because these structural identities hold.  It is measured on harmonics by

\[
  r_{\ell m}
  =G Y_{\ell m}+\ell(\ell+1)Y_{\ell m}.
  \tag{21.2}
\]

## 22. Conditional graph-family convergence certificate

For each point cloud define minimum separation \(q_n\), sampled approximate fill distance \(h_n\), mesh ratio \(\rho_n=h_n/q_n\), positive-weight diagnostics, graph connectivity, exact structural residual, and maximum low-order harmonic residual \(e_n\).

### Definition 22.1 (accepted finite family)

A finite refinement family receives a conditional empirical certificate only when:

1. every positive-conductance graph is connected;
2. constants, weighted self-adjointness, nonpositive spectrum, and nonnegative off-diagonals pass the configured structural tolerance;
3. mesh ratio and weight ratio remain below declared gates;
4. the weights integrate the sphere's constant mode and, when requested, satisfy an individual \(h^2\)-scaling diagnostic;
5. sampled fill distance strictly decreases;
6. harmonic residual decreases at every adjacent refinement;
7. both fitted and minimum adjacent observed orders exceed configured thresholds; and
8. the returned power law is a true observed envelope

\[
 e_n\le C h_n^p,
 \qquad C=\max_n e_n/h_n^p.
 \tag{22.1}
\]

The certificate stores the audited interval \([h_{\min},h_{\max}]\) and refuses to evaluate its bound outside that interval. It is therefore an executable statement about one finite family and selected harmonic modes, not an unconditional graph-Laplacian theorem or an extrapolation.

General point-cloud and graph convergence results require explicit density, locality, scaling, and regularity assumptions. Examples include Belkin, Sun, and Wang, DOI 10.1137/1.9781611973068.112, and later variational graph-limit work such as DOI 10.1137/18M1188999.

---

# Part VII. Integrated verification

## 23. Independent verification matrix

| Extension | Primary construction | Independent check |
|---|---|---|
| Finite grazing geometry | exact local-coordinate slab intersection | analytic axis/diagonal chords and infinite-slab comparison |
| Cylindrical patches | exact arc-measure reference patches | exact total area and normal-rotation bound |
| Curved operator | path-ordered augmented ODE | planar exact exponential, midpoint/fourth-order convergence, metric balance |
| 3-D transport | source iteration and directional sweeps | independently assembled sparse direct solve |
| 3-D adjoint | exact matrix transpose | scalar forward–adjoint identity |
| Parallel execution | deterministic angle/case maps | byte-identical SHA-256 digests across worker counts |
| Nuclear closure | group energy accounting | negative-deposition rejection and HDF5 tamper test |
| Group condensation | weighted coefficients plus explicit correction | exact reaction/heating weighted identities |
| Calibration | bounded GLS and analytic Jacobian | finite differences, grouped holdout, deterministic campaign bootstrap |
| Positive quadrature | variable-node search plus LP recertification | Gram lower bound and fixed-pool MILP certificate |
| Graph family | nonnegative conductance fit | exact structural identities and harmonic family study |

## 24. Deterministic benchmark conclusions

The frozen version 0.2 benchmark demonstrates, on synthetic controlled cases:

- finite grazing chords remain bounded and may be many orders of magnitude smaller than \(h/|\mu|\);
- cylindrical patch reference areas sum to the analytic area at roundoff, while maximum normal rotation is reported explicitly;
- the curved operator reproduces the planar operator at roundoff;
- the adaptive fourth-order Magnus path resolves the curved propagator below its declared defect gate and the flat limit agrees with the exact slab operator at roundoff;
- the three-dimensional source-iteration and direct solutions agree near floating-point tolerance;
- particle balance, exact transpose adjoint consistency, and worker-count digests pass;
- weighted reaction and deposition responses are preserved under declared condensation;
- grouped calibration recovers a synthetic law with successful campaign holdouts and bootstrap fits;
- the degree-two positive spherical rule is globally certified with four nodes;
- the accepted graph family exhibits fitted order about 2.12 and minimum adjacent order about 2.10 on the audited interval, with a true observed envelope.

These outcomes verify implementation and finite-dimensional structure.  They are not material validation.


### Version 0.2 frozen numerical values

The deterministic release benchmark records: planar/curved flat-limit operator difference \(1.11\times10^{-16}\), affine-offset difference \(8.47\times10^{-22}\), adaptive Magnus defect \(1.26\times10^{-12}\), 3-D direct/source-iteration relative difference \(1.14\times10^{-14}\), particle-balance residual \(1.41\times10^{-14}\), forward–adjoint difference \(1.69\times10^{-16}\), exact weighted collapsed-heating preservation, degree-two tetrahedral moment residual \(4.44\times10^{-16}\), graph fitted order 2.1237, and minimum adjacent graph order 2.1015. These values are deterministic software evidence, not physical-material validation.

---

# Part VIII. Novelty boundary and nonclaims

## 25. What is combined here

The individual ingredients—finite box intersection, Magnus integrators, Cartesian \(S_N\), Tchakaloff cubature, generalized least squares, and graph Laplacians—are established mathematical tools.  The research contribution of this package is their structure-preserving integration around HTS-tape responses:

1. finite grazing geometry is used as an explicit routing criterion for thin-layer interfaces rather than allowing \(h/|\mu|\) to diverge unphysically;
2. curvature is introduced in a conservative transformed response ODE that retains affine sources and every internal response row;
3. the local operator and three-dimensional solver share particle-balance and exact-adjoint audits;
4. nuclear-data promotion is blocked unless the supplied processed data close represented secondary energy and local reaction energy;
5. group condensation preserves selected reactions and local heating by an explicit, inspectable closure correction;
6. transport descriptors are linked to HTS property ratios with campaign-aware covariance and validation rather than independent-row regression;
7. positive quadrature and graph results distinguish exact structural theorems, finite-pool certificates, global lower-bound certificates, and conditional empirical convergence.

## 26. Deliberate nonclaims

Version 0.2 does not claim:

- a general CAD/CSG geometry kernel;
- a uniform one-dimensional asymptotic theorem when a curved ray reaches \(\mu=0\);
- a production full-device three-dimensional reactor solver;
- validation of any named ENDF evaluation or processing chain without authenticated external evidence;
- universal REBCO irradiation-property coefficients;
- global variable-node quadrature optimality unless a proved lower bound is attained;
- unconditional graph-Laplacian convergence for arbitrary clustered or irregular node clouds;
- physical accuracy beyond the declared representative-energy multigroup closure.

Every one of these boundaries is represented by a fail-closed validation condition, an explicit metadata field, or a documented routing requirement.

---

## 27. Reproducibility map

- Finite geometry: `src/hts_transport_ops/geometry3d.py`
- Curved operator: `src/hts_transport_ops/curved_surface.py`
- 3-D solver: `src/hts_angular/sn3d.py`
- Deterministic parallel tools: `src/hts_transport_ops/parallel.py`
- Processed data: `src/hts_transport_ops/nuclear_data.py`
- Calibration: `src/hts_calibration/`
- Quadrature certificates: `src/hts_angular/global_quadrature.py`
- Graph certificates: `src/hts_angular/graph_convergence.py`
- Regression tests: `tests/test_v02_*.py`
- Deterministic extension benchmark: `benchmarks/run_v02.py`
- Numerical gate: `scripts/verify_v02_summary.py`
- Full release gate: `scripts/audit_release.py`

## 28. References

1. S. Blanes, F. Casas, J. A. Oteo, and J. Ros, “The Magnus expansion and some of its applications,” *Physics Reports* 470 (2009), 151–238, DOI 10.1016/j.physrep.2008.11.001; arXiv:0810.5488.
2. T. M. Evans, A. S. Stafford, R. N. Slaybaugh, and K. T. Clarno, “Denovo: A new three-dimensional parallel discrete ordinates code in SCALE,” *Nuclear Technology* 171 (2010), 171–200, DOI 10.13182/NT171-171.
3. G. Yesilyurt, K. T. Clarno, T. M. Evans, G. G. Davidson, and P. B. Fox, “A C5 benchmark problem with the discrete ordinates radiation transport code Denovo,” *Nuclear Technology* 176 (2011), 274–283, DOI 10.13182/NT11-A13301.
4. R. E. Macfarlane et al., NJOY2016 evaluated nuclear-data processing system, DOI 10.11578/dc.20171025.1876.
5. C. Bayer and J. Teichmann, “The proof of Tchakaloff’s theorem,” *Proceedings of the American Mathematical Society* 134 (2006), 3035–3040; arXiv:math/0502473.
6. P. Delsarte, J. M. Goethals, and J. J. Seidel, “Spherical codes and designs,” *Geometriae Dedicata* 6 (1977), 363–388, DOI 10.1007/BF03187604.
7. M. Belkin, J. Sun, and Y. Wang, “Constructing Laplace operator from point clouds in R^d,” SODA 2009, 1031–1040, DOI 10.1137/1.9781611973068.112.
8. K. Adams et al., “The performance of REBCO coated conductor during in situ cryogenic irradiation with fusion-spectrum neutrons,” *Superconductor Science and Technology* 39 (2026), 02LT01, DOI 10.1088/1361-6668/ae4548.
9. R. M. Redheffer, “On the relation of transmission-line theory to scattering and transfer,” *Journal of Mathematics and Physics* 41 (1962), 1–41.
10. Standard finite-volume balance, sparse-transpose adjoint, convex moment, and generalized-least-squares identities are derived explicitly above rather than invoked as unnamed results.

# Positive angular Fokker–Planck generators: design, transport certificates, and an inconclusive HTS transfer diagnostic

## Abstract

We study positive reversible graph generators on weighted spherical
quadratures for angular Fokker–Planck and Boltzmann–Fokker–Planck transport.
The generator is constrained to conserve constants, reproduce the coordinate
shell, and remain monotone, while a convex objective reduces the sampled
degree-two harmonic residual.  We combine the sampling-kernel-correct algebra,
convex fixed-node design, transport semigroup/resolvent bounds,
quadrature–generator co-design, and fixed-point-preserving acceleration theory
with a preregistered benchmark hierarchy.  The optimized generator reduces the
frozen angular-error geometric mean to 0.671 of the baseline and reduces one
preconditioned solve from 23 to 17 iterations.  Nevertheless the
preregistered P2E physical-response hypothesis fails: the worst response-error
ratio is 8.068, and all physical method differences are unresolved relative to
the declared reference uncertainty.

A separate Cu/Ag/REBCO/buffer/Hastelloy surrogate verifies the neutral/charged
physics firewall, positivity, balance, and layer-resolved response plumbing,
but it does not yield a transfer conclusion.  None of its 18 method-error
differences is resolved, the maximum relative baseline/optimized response
difference is $1.94\times10^{-14}$, and a 50/72/98/128-direction reference
sweep fails the declared convergence gate.  The P2F outcome is therefore
inconclusive rather than bounded negative.  The combined evidence supports
sampled degree-two fidelity as a mathematical design coordinate and, in
selected cases, an acceleration ingredient; it does not establish improved or
degraded HTS response.  Full neutral Boltzmann collision operators remain
unchanged, and AFP is used only on the declared charged/BFP component.

## 1. Scope

Let \(X=\{\Omega_i\}_{i=1}^N\subset S^{d-1}\) have positive normalized weights
\(w_i\).  Shared conductances \(\gamma_{ij}=\gamma_{ji}\ge 0\) define

\[
 (Lf)_i=\frac1{w_i}\sum_j\gamma_{ij}(f_j-f_i).
\]

Then \(L1=0\), \(L\) is self-adjoint in
\(\langle f,g\rangle_W=f^TWg\), and \(e^{tL}\) is positive and mass
preserving.  We require

\[
 L\Omega=-(d-1)\Omega.
\]

The work concerns design and controlled use of this angular diffusion
operator.  It does not replace the full collision physics of neutral-particle
transport and does not infer material damage or superconducting properties.

## 2. Sampling-correct degree-two defect

For \(A\in\operatorname{Sym}_0(d)\), define

\[
 (S_2A)_i=\Omega_i^TA\Omega_i,
 \qquad R_2=(L+2dI)S_2.
\]

The sampling kernel \(K_X=\ker S_2\) is essential.  The residual factors
through \(\operatorname{Sym}_0(d)/K_X\), and every spectral statement is made
on the sampled quotient rather than on an assumed injective harmonic shell.
With the weighted data norm,

\[
 \mathfrak D_2^2
 =\lambda_{\max}
 \left(
 (S_2^*WS_2)|_{K_X^\perp},
 (R_2^*WR_2)|_{K_X^\perp}
 \right),
\]

with the numerator/denominator order chosen consistently with the repository's
accepted normalization.  The full local decomposition is recorded and
formally checked in the Paper-I foundation.  Paper II consumes that frozen
normalization and does not redefine it.

## 3. Convex fixed-node design

For a permitted edge set \(E\), generator design is a finite convex problem in
the shared conductances:

\[
 \begin{aligned}
 \text{minimize}_{\gamma,t}\quad &t\\
 \text{subject to}\quad
 &\gamma_e\ge0,\\
 &L_\gamma\Omega=-(d-1)\Omega,\\
 &r_i(\gamma)\le r_{\max},\\
 &R_2(\gamma)^TWR_2(\gamma)\preceq
 t^2S_2^TWS_2\quad\text{on }K_X^\perp.
 \end{aligned}
\]

The implementation uses an explicit sampled basis and fails closed on rank
loss, sign errors, missing weights, or confusion between form exactness and
sampled exactness.  Positivity, reversibility, conservation, and degree-one
reproduction are constraints rather than posterior diagnostics.

## 4. Transport error theory

Let \(A\) be a dissipative angular/spatial transport operator and let
\(A_L\) use the designed angular generator.  The accepted analysis gives
semigroup and resolvent estimates in admissible weighted norms.  Schematically,

\[
 e^{tA}-e^{tA_L}
 =\int_0^t e^{(t-s)A}(A-A_L)e^{sA_L}\,ds,
\]

and, for coercive steady problems,

\[
 A^{-1}-A_L^{-1}=A^{-1}(A_L-A)A_L^{-1}.
\]

The estimates separate angular-model residual, sampling alias, spatial and
energy discretization, iteration error, boundary effects, and response
weighting.  No commutation between streaming and angular collision is assumed
unless explicitly stated.  A small \(H_2\) defect controls only the sampled
degree-two component; it cannot control an arbitrary response whose adjoint
has significant higher-shell or ray content.

## 5. Quadrature–generator co-design

When nodes move, both the sampling map and weighted Gram matrix move.  The
inner fixed-candidate design remains convex, whereas the outer node problem is
nonconvex.  The accepted co-design stage therefore claims global optimality
only for the inner problem and stationary-subsequence results for protected
outer updates.  Positive masses, feasibility margins, graph changes,
conditioning, and rotation bias are audited separately.  Arbitrary local
spherical-design compatibility remains outside the theorem boundary.

## 6. Fixed-point-preserving acceleration

The low-order AFP operator is used as a preconditioner or residual-correction
model; it never replaces the high-order production operator.  For high-order
matrix \(H\), low-order matrix \(M\), and residual \(r=b-Hx\), a correction
\(M^{-1}r\) changes convergence but not the fixed point.  Conservation
constraints and the declared response projection are enforced on the
correction map.

The frozen forward-peaked suite shows substantial iteration reductions over a
moment-monotone AFP baseline, but higher-shell and streaming-ray adversaries
exclude an unconditional acceleration theorem.  In the P2E held-out
acceleration fixture, the optimized preconditioner takes 17 iterations versus
23 for the baseline, a 26.09% reduction exceeding the preregistered 10% gate.

## 7. Preregistered benchmark hierarchy

The P2E manifest freezes software, nodes, operator registry, partitions,
success criteria, seven case families, ablations, and reference policy before
the one-time held-out execution.  The cases include analytic harmonic decay,
band-limited data, a narrow beam, a published-geometry electron surrogate, a
full positive forward-peaked neutral kernel, a layered charged-particle target,
and an oblique coated-conductor surrogate.

The held-out execution is complete and hash-authenticated.  Its principal
metrics are:

| Metric | Value |
|---|---:|
| Angular geometric-mean ratio | 0.67146 |
| Response-error median ratio | 1.00000 |
| Response cases improved by at least 5% | 3 of 7 |
| Overall response-error geometric-mean ratio | 1.12616 |
| Physical-case geometric-mean ratio | 1.65972 |
| Worst response ratio | 8.06841 |

The first three preregistered gates pass and the frozen worst-degradation gate
fails.  The HTS ratio is not resolved relative to the independent reference
change: the absolute method-error difference is \(5.53\times10^{-6}\), while
the reference uncertainty is \(1.89\times10^{-5}\).  Thus the formal
hypothesis fails, but the experiment does not resolve a physical eightfold
degradation.

Only the two analytic comparisons distinguish the methods beyond declared
reference uncertainty.  The five physical comparisons do not.

## 8. HTS coated-conductor demonstration

### 8.1 Geometry

The bounded stack is 20 µm Cu, 2 µm Ag, 1 µm REBCO, 0.2 µm oxide buffer,
50 µm Hastelloy C-276, and 20 µm back Cu.  Normal, 60° oblique, and 84°
grazing-sensitive incidences are evaluated.

### 8.2 Neutral and charged equations

The neutral groups solve

\[
 \mu_m\partial_x\psi^n_{gm}
 +\Sigma_{\ell,g}\psi^n_{gm}
 +\Sigma_{s,g}(I-K_g)\psi^n_g=q^n_{gm},
\]

with nonnegative, row-stochastic, \(W\)-reversible full Boltzmann kernels
\(K_g\).  Neutral reaction loss generates a nonnegative secondary source.
Only the charged component solves

\[
 \mu_m\partial_x\psi^c_{km}
 +(\Sigma_{a,k}+\Sigma_{r,k})\psi^c_{km}
 -D_kL\psi^c_k=q^c_{km}.
\]

The baseline and optimized runs share the neutral solution, 32 angular nodes,
all cells and groups, sources, coefficients, and response rows.

### 8.3 Layer responses

Each layer records scalar flux, current, traceless second moment, normal
quadrupole, heating proxy, charged crossing/escape, and species-resolved PKA
source descriptors.  For species \(s\) in layer \(\ell\), the directional
source tensor is

\[
 T_{\ell s g}
 =f_{\ell s}\sum_{c\subset\ell}\Delta x_c\sigma^{\rm pka}_{cg}
 \sum_mw_m\psi^n_{cgm}\Omega_m\Omega_m^T.
\]

It is symmetric positive semidefinite by construction.  It is a source
descriptor, not a recoil-energy distribution or a damage metric.

### 8.4 Reference diagnostics

The nominal reference uses 72 directions and a positive reversible heat-kernel
generator calibrated to the coordinate shell.  The legacy nominal resolution
quantity is

\[
 u_R=|R_{72,h/2}-R_{50,h/2}|+|R_{72,h/2}-R_{72,h}|.
\]

The revised audit does not treat this two-level quantity as proof of angular
convergence.  It additionally computes 50-, 72-, 98-, and 128-direction
references and requires the relative span across the sweep to be at most 5%
for every selected response.  The all-response convergence gate fails at
normal, oblique, and grazing incidence.  At 84°, total heating alternates from
approximately $1.02\times10^{-7}$ to $3.79\times10^{-3}$,
$4.05\times10^{-5}$, and $3.69\times10^{-3}$ across the four levels.  The
nominal uncertainty is therefore retained as a diagnostic quantity, not a
converged error certificate.

### 8.5 Result

All structural positivity, balance, layer-inventory, PKA-tensor, and physics-
firewall checks pass.  The minimum flux is $1.48\times10^{-11}$ and the maximum
balance residual is $5.02\times10^{-15}$.  The optimized generator has the
smaller sampled $H_2$ defect, 0.9325 versus 1.3880, but there are zero resolved
improvements, zero resolved degradations, and zero resolved method differences
among the 18 comparisons.  The largest relative baseline/optimized response
difference is $1.94\times10^{-14}$, indicating that the selected response map
is effectively insensitive to the operator replacement.  Because the angular
reference sweep also fails, the terminal HTS outcome is
`INCONCLUSIVE_REFERENCE_NOT_CONVERGED`.

## 9. Interpretation

The combined benchmark evidence distinguishes three statements:

1. The optimized generator is mathematically and algorithmically different:
   it reduces the sampled degree-two residual while retaining positivity,
   reversibility, and degree-one reproduction.
2. It can be computationally useful as a preconditioner on selected slow
   angular subspaces.
3. Neither fact establishes lower physical-response error in a layered HTS
   calculation.

The P2F diagnostic is inconclusive for two independent reasons.  First, the
selected response map is nearly invariant under the baseline/optimized
operator replacement; three substrate-PKA comparisons are neutral-only by
construction, and the remaining selected responses differ only at roughly
machine precision.  Second, the product-quadrature reference hierarchy is not
converged, especially for the grazing beam.  Neutral collision physics,
material reaction coefficients, streaming, boundaries, and higher angular
shells remain mechanisms that a single \(H_2\) metric does not encode, but the
present fixture cannot quantify their transfer effect.

## 10. Limitations

The material coefficients are positive verification surrogates rather than
evaluated nuclear data.  The references are finite product quadratures, not
production Monte Carlo or a convergence theorem.  The grazing case uses a
finite-width leakage surrogate rather than a nonlocal surface equation.  The
model excludes photons, traceable H/He production, full PKA energy spectra,
DPA, defect survival and annealing, atomistic damage, and changes in
superconducting properties.

The runtime records in P2E are single executions.  The legacy
`equal_wall_time` field is a common completion-budget record, not a true
equal-time allocation experiment.

## 11. Reproducibility and claim status

The repository contains the frozen P2E manifest and operator registry, the
one-time held-out artifact, corrected audit, P2F manifest/results/audit,
deterministic tests, imported Math angular implementation with blob-level
provenance, and exact-head workflows.  Scientific hashes exclude no reported
response data.

The P2E held-out benchmark may be reported as a mixed/negative preregistered
result.  P2F should remain an implementation and claim-firewall appendix, not a
transfer-result paper: its selected responses are operator-insensitive and its
angular reference hierarchy is not converged.  A successor transfer experiment
requires separately preregistered operator-sensitive responses, a converged or
independently validated reference, and an equal-work or equal-accuracy
comparison.

## Data and code availability

All code and finite benchmark records are contained in the consolidated AFP
Git history.  Historical archive branches remain unchanged.  The exact branch,
commit, workflow-run, artifact, and archive identifiers are recorded in the
final consolidation report.

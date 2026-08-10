# P2D — Fixed-point-preserving harmonic-fidelity acceleration

## 1. Scope, spaces, and production equation

Let the fully discrete high-order Boltzmann or BFP system be

\[
A_H x=b.
\]

`A_H` may contain spatial upwind streaming, inflow or reflective boundary
elimination, absorption, energy-group coupling, and a high-order angular
collision block.  The low-order matrix `A_L(gamma)` retains every declared
nonangular block and replaces only the eligible angular block by a positive,
reversible, `H_0/H_1`-exact AFP generator.  The low-order system is never
accepted as the production equation.

The stationary synthetic-acceleration step is

\[
x^{k+1}=x^k+\omega A_L^{-1}(b-A_Hx^k).
\]

The Krylov implementation applies the same low solve as a cached left
preconditioner and checks convergence in the original high-order residual.

## 2. Exact fixed point and exact conservation

### Theorem 2.1 — fixed-point preservation

Assume `A_H` and `A_L` are nonsingular and let `x_* = A_H^{-1}b`.  Then, for
all finite `omega`,

\[
x_*+\omega A_L^{-1}(b-A_Hx_*)=x_*.
\]

Thus acceleration may alter iteration history but cannot alter the converged
high-order solution.

### Theorem 2.2 — constrained correction

For a full-row-rank conservation map `Q`, define

\[
P_L=A_L^{-1}-A_L^{-1}Q^T(QA_L^{-1}Q^T)^{-1}QA_L^{-1}.
\]

If the Schur block is nonsingular, then `Q P_L=0`.  Hence a compatible initial
iterate, `Qx^0=Qx_*`, satisfies `Qx^k=Qx_*` at every step.  The implementation
fails closed on rank-deficient constraints or a conservation-incompatible
initial state.

## 3. Error propagation and harmonic shells

For the unconstrained correction,

\[
e^{k+1}=E_\omega e^k,
\qquad
E_\omega=I-\omega A_L^{-1}A_H.
\]

At `omega=1`,

\[
E_1=A_L^{-1}(A_L-A_H),
\qquad
\|E_1\|\le \|A_L^{-1}\|\,\|A_L-A_H\|.
\]

On a common reducing harmonic block with positive scalar values `a_H,l` and
`a_L,l`,

\[
E_\omega|_{\mathcal H_l}
 =\left(1-\omega\frac{a_{H,l}}{a_{L,l}}\right)I.
\]

For a declared relevant slow subspace with orthonormal basis `V`, the actual
quantity audited is

\[
\|E_\omega V\|_2,
\]

along with leakage

\[
\|(I-VV^T)E_\omega V\|_2.
\]

This prevents improved isolated angular eigenvalues from being promoted to a
transport-acceleration claim without checking the slow modes of the coupled
system.

## 4. Spectral-equivalence and field-of-values routes

### Theorem 4.1 — SPD spectral equivalence

In an SPD metric, suppose the transformed matrices are symmetric positive and

\[
m\langle A_Lv,v\rangle
\le \langle A_Hv,v\rangle
\le M\langle A_Lv,v\rangle.
\]

Then the spectrum of `A_L^{-1}A_H` lies in `[m,M]`.  With
`omega=2/(m+M)`, stationary correction contracts by at most

\[
\frac{M-m}{M+m}.
\]

The implementation rejects nonsymmetric representatives rather than applying
this theorem outside its hypotheses.

### Theorem 4.2 — nonsymmetric field of values

Let `B=A_L^{-1}A_H` in a declared SPD metric.  If

\[
\lambda_{\min}\!\left(\frac{B+B^*}{2}\right)\ge\alpha>0,
\qquad \|B\|\le\beta,
\]

then

\[
\|I-\omega B\|
\le \sqrt{1-2\omega\alpha+\omega^2\beta^2}.
\]

The displayed bound is minimized at `omega=alpha/beta^2`.  It is sufficient,
not necessary.  For Krylov methods, the same positive numerical-range
hypothesis yields standard residual-reduction bounds; the code records actual
original-system residuals instead of inferring convergence from eigenvalues.

If `rho<1` is a certified contraction, a sufficient count to reduce error
`e_0` below `tau` is

\[
k\ge \left\lceil\frac{\log(\tau/e_0)}{\log\rho}\right\rceil.
\]

## 5. Streaming, energy, and boundary dependence

Write

\[
A_\bullet=S_\bullet+G_\bullet+B_\bullet+C_\bullet,
\qquad \bullet\in\{H,L\},
\]

for streaming, energy coupling, boundary, and angular collision.  Then

\[
A_L-A_H=(S_L-S_H)+(G_L-G_H)+(B_L-B_H)+(C_L-C_H),
\]

and

\[
\|E_1\|
\le \|A_L^{-1}\|
\sum_{X\in\{S,G,B,C\}}\|X_L-X_H\|.
\]

The production comparison retains identical streaming, group, and boundary
blocks, so the audited decomposition has zero nonangular mismatch.  A separate
two-group/two-cell case contains downscatter and partially reflective
boundaries in both matrices and verifies convergence of the full noncommuting
system.  These blocks still affect `A_L^{-1}`, coercivity, the field of values,
and therefore iteration count even when their direct mismatch is zero.

## 6. Forward-peaked high-order family and low operators

The controlled high-order angular family is the spherical heat-kernel
collision.  On a continuum harmonic,

\[
K_\varepsilon Y_{lm}
=e^{-\varepsilon l(l+1)}Y_{lm},
\]

so the collision-removal eigenvalue is

\[
c_{H,l}=\sigma_s\left(1-e^{-\varepsilon l(l+1)}\right).
\]

It becomes increasingly forward peaked as `epsilon` decreases.  The matched
FP scale is chosen from exact `H_1` agreement,

\[
D_\varepsilon
=\frac{\sigma_s}{2}\left(1-e^{-2\varepsilon}\right).
\]

The positive low collision is `-D_epsilon L_gamma`.  The frozen same-node
32-direction operators are independently re-audited for conservation,
reversibility, positivity, `H_1` exactness, rate, and shell defects:

| operator | `r_max` | `D_2` | `D_3` | `D_4` |
|---|---:|---:|---:|---:|
| optimized harmonic fidelity | 17.6587 | 0.932538 | 4.23044 | 10.3820 |
| monotone AFP baseline | 5.61435 | 1.38797 | 6.76677 | 14.3160 |
| deliberately H2-poor positive | 1.95652 | 4.00000 | 10.0000 | 18.0000 |

The optimized operator was selected using angular shell and rotation data
only; no transport-response result was used.  The classical comparator is a
signed spectral Laplace–Beltrami FP preconditioner on the same nodal space.
It is a faithful moment-space FPSA/MFPA-style comparator but is not promoted to
a monotone production operator or claimed to reproduce every implementation
choice in the literature.

## 7. Identical-discretization forward-peaked comparison

All rows use:

- the same 32 directions and quadrature weights;
- six upwind cells over width 30;
- absorption `5e-4`;
- identical high-order matrix and right-hand side within each row;
- GMRES restart 20 and the same original-residual stopping rule;
- a training-only `H_2` stress mode chosen from angular residual matrices;
- cached low-order LU factors.

The deterministic iteration results are:

| `epsilon` | first moment `exp(-2 epsilon)` | none | optimized | monotone baseline | classical signed FP | H2-poor positive |
|---:|---:|---:|---:|---:|---:|---:|
| 0.040 | 0.92312 | 37 | 12 | 22 | 14 | 36 |
| 0.020 | 0.96079 | 43 | 11 | 27 | 10 | 45 |
| 0.010 | 0.98020 | 56 | 12 | 31 | 8 | 50 |
| 0.005 | 0.99005 | 62 | 13 | 30 | 7 | 49 |

The optimized positive operator reduces iterations against the monotone
baseline by at least **45.45%** on every row.  Its geometric-mean iteration
ratio is **0.4394**, a **56.06%** reduction.  It also beats no acceleration on
every row.  The signed spectral comparator becomes fastest in the most
forward-peaked rows, illustrating the price of the positivity constraint
rather than invalidating the positive-operator result.

For the declared slow mode, the optimized restricted contraction is
`0.0216–0.0500`, versus `0.1377–0.1928` for the monotone baseline.  The audit
also records leakage, setup time, solve time, high-order matvecs, low solves,
Python peak memory, matrix storage, and factor storage.  Wall-time values are
machine diagnostics; iteration and matvec counts are the deterministic
comparison.

## 8. Failure modes and adversarial cases

### 8.1 Higher harmonics dominate

A newly sampled degree-seven direction is used as the declared slow mode.
`D_2` is not the controlling quantity.  The relevant degree-seven mismatches
are approximately 24.36 for the optimized positive operator and 50.79 for the
baseline, while the signed spectral FP comparator is exact on the retained
frame.  This case shows that a degree-two ranking cannot certify a
higher-shell problem even when the optimized operator happens also to improve
that particular higher shell.

A second diagonal hostile fixture deliberately makes the `H_2`-optimized low
operator worse on the source-supported higher shells; its iteration count is
not better than the baseline.  This prevents a universal-acceleration claim.

### 8.2 Ray effects dominate

For a ballistic beam with true incidence cosine `0.1`, optical thickness
`0.2`, and a fixed product quadrature whose nearest incoming ray has cosine
`0.664986`, the analytic transmission is `0.135335` while the coarse-ray
transmission is `0.740257`, a relative error of **446.98%**.  Every
fixed-point-preserving low operator converges to the same coarse high-order
solution, so improved `H_2` collision fidelity cannot remove this ray error.
Quadrature refinement, rotation, or interpolation is a separate remedy.

## 9. Implementation, tests, and formal boundary

Primary sources:

- `pure_math/acceleration/core.py`
- `pure_math/acceleration/transport.py`
- `pure_math/acceleration/p2d_frozen_operators.json`
- `pure_math/acceleration/fixtures.py`
- `pure_math/acceleration/audit.py`
- `pure_math/tests/test_p2d_acceleration.py`

The focused hostile suite contains 15 tests, including hash tampering,
constraint incompatibility, metric-hypothesis rejection, same-node generator
invariants, every required comparator, setup/memory counters, the
forward-peaked sweep, the higher-shell case, ray domination, and multigroup
boundary coupling.

Lean checks the finite fixed-point, error, conservation, and scalar-shell
identities in `AFPBarrier/AccelerationFixedPoint.lean`.  It does not formalize
GMRES, numerical ranges, matrix factorization timings, unbounded transport
operators, spherical heat-kernel analysis, or physical Boltzmann-to-BFP
validity.

## 10. Strongest supported P2D claim

For the frozen same-node 32-direction family and the declared increasingly
forward-peaked heat-kernel/BFP slab sweep, the optimized positive reversible
AFP preconditioner preserves the exact production fixed point and declared
conservation constraints, represents the response-relevant `H_2` slow mode
more accurately, and reduces GMRES iterations by 45.45–61.29% relative to the
moment-preserving monotone AFP baseline.  This is a controlled computational
performance theorem for the frozen finite family, not a universal statement
that lower `D_2` accelerates every transport problem.  Higher-shell and
ray-dominated adversaries explicitly delimit the claim.

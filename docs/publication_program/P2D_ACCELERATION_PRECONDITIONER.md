# P2D — Fixed-point-preserving harmonic-fidelity acceleration

## 1. Scope and convention

Let the high-order discrete transport system be

\[
A_H x=b,
\]

where `A_H` may contain spatial streaming, boundary elimination, energy-group
coupling, and the high-order Boltzmann or BFP collision operator.  The
low-order matrix `A_L(gamma)` contains the same declared streaming, boundary,
and energy blocks but replaces only the eligible angular-diffusion block by a
positive, reversible, `H_0/H_1`-exact generator.  The production equation is
never replaced by `A_L`.

The accepted correction is

\[
x^{k+1}=x^k+\omega A_L^{-1}(b-A_Hx^k).
\]

When a linear conservation constraint `Qx=q` must hold at every iterate, use

\[
P_L=A_L^{-1}-A_L^{-1}Q^T(QA_L^{-1}Q^T)^{-1}QA_L^{-1}
\]

and replace `A_L^{-1}` by `P_L`.  The implementation rejects rank-deficient
constraint data and rejects an initial state whose constraint value differs
from the exact high-order solution.

## 2. Exact fixed point and conservation

### Theorem 1 — exact fixed point

Assume `A_H` and `A_L` are nonsingular.  If `x_* = A_H^{-1}b`, then

\[
x_*+\omega A_L^{-1}(b-A_Hx_*)=x_*.
\]

Thus the low-order operator changes convergence only; it cannot change the
converged production solution.

### Theorem 2 — constrained conservation

Assume `Q` has full row rank and `QA_L^{-1}Q^T` is nonsingular.  Then
`QP_L=0`.  Therefore, if `Qx^0=Qx_*`, every constrained correction satisfies
`Qx^{k+1}=Qx^k=Qx_*`.  Compatibility is essential: a correction restricted to
`ker Q` cannot repair an initially wrong conserved value.

## 3. Error propagation and shell action

For the unconstrained iteration,

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

If a common reducing harmonic shell diagonalizes both operators with positive
shell values `a_{H,l}` and `a_{L,l}`, the exact factor is

\[
\rho_l(\omega)=1-\omega\frac{a_{H,l}}{a_{L,l}}.
\]

The iteration contracts on the retained shell union exactly when
`max_l |rho_l|<1`.  This shows why a smaller `H_2` mismatch helps only when the
slow error has visible `H_2` content.

## 4. Noncommuting field-of-values route

Set `B=A_L^{-1}A_H`.  In the Euclidean metric, assume

\[
\lambda_{\min}\!\left(\frac{B+B^T}{2}\right)\ge\alpha>0,
\qquad \|B\|_2\le\beta.
\]

Then

\[
\|I-\omega B\|_2
\le \sqrt{1-2\omega\alpha+\omega^2\beta^2}.
\]

The displayed bound is minimized by `omega=alpha/beta^2`, giving a strict
contraction whenever the resulting right-hand side is below one.  Streaming,
boundary, and energy-coupling effects enter through the full matrices and may
destroy this certificate even when isolated angular eigenvalues improve.

## 5. Krylov preconditioning

The implementation also supplies left-preconditioned GMRES.  Every callback
and final acceptance is checked in the original high-order residual, not only
in the preconditioned norm.  Hence a low-order solve cannot hide a wrong
high-order fixed point.

## 6. Comparative fixtures

Four deterministic fixtures are retained:

1. commuting `H_0`–`H_5` shell model;
2. two-cell noncommuting streaming model;
3. two-group/two-cell model with downscatter and inflow boundary source;
4. higher-shell adversarial source with no useful `H_2` dominance.

Each compares no preconditioner, the optimized harmonic-fidelity low-order
operator, the existing moment-preserving monotone comparator, a declared
classical modified-FP model, and a deliberately `H_2`-poor positive operator.
All use the same high-order matrix, right-hand side, tolerance, and restart.
The adversarial fixture is an intentional negative control: the optimized
operator is not required to win when the source is concentrated in higher
shells.

## 7. Implementation and proof boundary

Primary implementation:

- `pure_math/acceleration/core.py`
- `pure_math/acceleration/fixtures.py`
- `pure_math/acceleration/audit.py`
- `pure_math/tests/test_p2d_acceleration.py`

Lean checks the finite fixed-point, error, conservation, and scalar-shell
identities in `AFPBarrier/AccelerationFixedPoint.lean`.  It does not formalize
GMRES, field-of-values numerical linear algebra, unbounded transport
operators, or physical BFP validity.

## 8. Strongest supported P2D statement

The optimized operator is a fixed-point-exact and optionally
constraint-preserving accelerator.  It reduces iterations on the retained
noncommuting streaming fixture relative to the moment-preserving monotone
baseline, while the higher-shell fixture supplies an explicit failure case.
No claim is made that `H_2` optimization universally accelerates transport.

# Quadratic covariance derivation — Prompt 2 resolution

## Status

The candidate expansion in the original version of this note was correct, but
its dimension conclusion was incomplete because it counted matrices rather
than genuinely sampled functions. Prompt 2 is completed in

```text
pure_math/covariance/SAMPLED_QUADRATIC_EXACTNESS_THEOREM.md
```

The exact symbolic regression is

```text
pure_math/covariance/quadratic_covariance_audit.py
```

and the Lean finite algebra is in

```text
AFPBarrier/QuadraticCovariance.lean
```

## Corrected theorem summary

For

\[
(Lf)(i)=\sum_j a_{ij}(f(j)-f(i)),
\qquad L\Phi=-\lambda\Phi,
\]

put

\[
\Delta_{ij}=\Phi_j-\Phi_i,
\qquad
C_i=\sum_j a_{ij}\Delta_{ij}\Delta_{ij}^T,
\qquad
Q_A(i)=\Phi_i^TA\Phi_i.
\]

Then

\[
LQ_A(i)=-2\lambda Q_A(i)+\operatorname{tr}(A^TC_i).
\]

For a shifted target mode \(Q_A-c\) with eigenvalue \(-\mu\), the exact
necessary-and-sufficient residual equation is

\[
\operatorname{tr}(A^TC_i)+(\mu-2\lambda)Q_A(i)-\mu c=0
\quad\text{for every }i.
\]

For the coordinate eigenmap on \(S^{d-1}\), with
\(\lambda=d-1\), \(\mu=2d\), and \(A\in\operatorname{Sym}_0(d)\), define

\[
M_i=P_0(C_i+2\Phi_i\Phi_i^T).
\]

The zero-centered exact form space is

\[
E_{\mathrm{form}}=
\operatorname{span}\{M_i\}^{\perp}.
\]

This is a matrix space, not yet a sampled-function space. The sampling map is

\[
S_X(A)_i=\Phi_i^TA\Phi_i,
\qquad K_X=\ker S_X,
\]

and the genuinely sampled exact space is

\[
E_{\mathrm{sample}}=S_X(E_{\mathrm{form}}),
\]

with

\[
\dim E_{\mathrm{sample}}
=\dim E_{\mathrm{form}}
 -\dim(E_{\mathrm{form}}\cap K_X).
\]

For basis matrices, if \(R\) is the covariance-constraint matrix and \(S\) is
the sampling matrix, then

\[
\dim E_{\mathrm{sample}}
=\operatorname{rank}\begin{bmatrix}R\\S\end{bmatrix}
 -\operatorname{rank}R.
\]

## Sharp structural theorem

If every local covariance is axially isotropic about \(\Phi_i\),

\[
C_i=\tau_i(I-\Phi_i\Phi_i^T)+\beta_i\Phi_i\Phi_i^T,
\]

and \(\beta_i>0\), then

\[
M_i=\frac{d\beta_i}{d-1}
\left(\Phi_i\Phi_i^T-\frac1dI\right).
\]

Thus each covariance constraint is a positive scalar multiple of the
corresponding sampling functional. Consequently

\[
E_{\mathrm{form}}=K_X,
\qquad
E_{\mathrm{sample}}=\{0\}.
\]

This theorem explains the exact Platonic table. The tetrahedron, octahedron,
and cube possess nonzero algebraic form spaces, but those spaces are exactly
their quadratic sampling kernels. The icosahedron and dodecahedron have full
constraint and sampling rank.

## Spectral-product branch

The finite carré-du-champ and semigroup/Jensen arguments independently prove
the additive sampled-square obstruction. After parity, antipodal-maximizer,
sampling-alias, and bounded eigenvalue-resonance audits, no new
\(\ell\)-indexed hierarchy or dimension tradeoff survived. The hierarchy
conjecture is therefore rejected for this stage under its stated kill
criterion. The sampled covariance theorem remains the publication theorem.

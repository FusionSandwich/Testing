# Quadratic covariance characterization

This note records the next candidate theorem for the pure-mathematics paper.
It is not yet promoted to `PROVED` until the complete proof and priority review
are finished.

## Setting

Let

\[
(Lf)(i)=\sum_j a_{ij}(f(j)-f(i))
\]

be a finite generator, and let

\[
\Phi:X\to\mathbb R^d
\]

be an eigenmap satisfying, coordinatewise,

\[
L\Phi=-\lambda\Phi.
\]

For one vertex define

\[
\Delta_{ij}=\Phi_j-\Phi_i,
\qquad
C_i=\sum_j a_{ij}\Delta_{ij}\Delta_{ij}^{T}.
\]

For a symmetric matrix `A`, set

\[
q_A(\Phi)=\Phi^T A\Phi.
\]

## Exact expansion

Expanding one jump gives

\[
q_A(\Phi_j)-q_A(\Phi_i)
=
2\Phi_i^T A\Delta_{ij}
+
\Delta_{ij}^T A\Delta_{ij}.
\]

Summing and using the eigenmap equation gives

\[
\boxed{
Lq_A(i)
=
-2\lambda q_A(\Phi_i)
+
\operatorname{tr}(A C_i).
}
\]

If `q_A-c_A` is required to have target eigenvalue `-mu`, its residual is

\[
\boxed{
L(q_A-c_A)(i)+\mu(q_A(\Phi_i)-c_A)
=
\operatorname{tr}(A C_i)
+(μ-2\lambda)\Phi_i^T A\Phi_i
-\mu c_A.
}
\]

This is the exact local linear characterization of attainable quadratic
exactness.

## Sphere specialization

For the coordinate eigenmap on `S^{d-1}`,

\[
\lambda=d-1.
\]

Degree-two spherical harmonics are represented by trace-free symmetric `A` and
have eigenvalue

\[
\mu=2d.
\]

Hence the residual is

\[
\boxed{
\operatorname{tr}
\left[
A\left(C_i+2\Phi_i\Phi_i^T\right)
\right].
}
\]

Let `P_0` denote traceless projection and define

\[
M_i=P_0\left(C_i+2\Phi_i\Phi_i^T\right).
\]

Then the globally exact quadratic-form space is

\[
\boxed{
\mathcal E_2
=
\left(
\operatorname{span}\{M_i:i\in X\}
\right)^\perp
\subseteq \operatorname{Sym}_0(d).
}
\]

Consequently,

\[
\boxed{
\dim\mathcal E_2
=
\frac{d(d+1)}2-1
-
\operatorname{rank}\operatorname{span}\{M_i\}.
}
\]

This dimension identity is the central M3 target.  It is more informative than
only proving that the complete degree-two space is impossible.

## Covariance proof of the full no-go theorem

If every trace-free quadratic form were exact, then every `M_i` would vanish,
so

\[
C_i+2\Phi_i\Phi_i^T=c_i I.
\]

For unit-sphere points and exact coordinate eigenvalue `d-1`,

\[
\operatorname{tr}C_i
=
\sum_j a_{ij}\|\Phi_j-\Phi_i\|^2
=
2(d-1).
\]

Taking traces therefore gives `c_i=2`, and

\[
C_i=2(I-\Phi_i\Phi_i^T).
\]

The right side has zero radial component.  But

\[
\Phi_i^T C_i\Phi_i
=
\sum_j a_{ij}
(\Phi_i\cdot\Phi_j-1)^2,
\]

which is strictly positive for any positive jump to a distinct point.  This is
a contradiction.

## Research questions

1. Which dimensions of `E_2` are attainable under positivity, reversibility,
   connectivity, and bounded degree?
2. Which graph symmetries force the span of the `M_i` to be all of
   `Sym_0(d)`?
3. Can one bound `dim E_2` using active stencil size or covariance rank?
4. How does global `Q=1` constrain the tensors `M_i`?
5. Can negative conductances restore prescribed quadratic subspaces, and what
   is the minimal sign violation required?
6. Does the same construction extend to irreducible components of
   `Sym^2(V_lambda)` for a general eigenspace?

A publishable pure-math paper requires a sharp dimension, rigidity, or
classification theorem beyond the displayed linear identity.

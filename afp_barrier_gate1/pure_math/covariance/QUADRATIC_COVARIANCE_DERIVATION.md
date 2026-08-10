# Quadratic covariance derivation and assumption audit

This is the short derivation companion to
QUADRATIC_COVARIANCE_THEOREM.md. The latter is the authoritative ordinary proof
package. The covariance characterization is PROVED; this note no longer
describes it as a conjectural M3 target.

## Exact jump expansion

For

\[
 (Lf)(i)=\sum_{j\ne i}a_{ij}(f(j)-f(i)),\qquad
 L\Phi=-\lambda\Phi,
\]

define

\[
 \Delta_{ij}=\Phi_j-\Phi_i,\qquad
 C_i=\sum_{j\ne i}a_{ij}\Delta_{ij}\Delta_{ij}^T.
\]

For \(A=A^T\),

\[
 \Phi_j^TA\Phi_j-\Phi_i^TA\Phi_i
 =2\Phi_i^TA\Delta_{ij}+\Delta_{ij}^TA\Delta_{ij}.
\]

Summation gives

\[
 L(S_X(A))(i)
 =-2\lambda\Phi_i^TA\Phi_i+\operatorname{tr}(AC_i).
\]

Thus \(S_X(A)-c\mathbf1\) has target \(-\mu\) exactly when

\[
 \operatorname{tr}(AC_i)
 +(\mu-2\lambda)\Phi_i^TA\Phi_i-\mu c=0
\]

at every vertex. This derivation needs no positivity, reversibility,
connectivity, or division by \(\mu\). At \(\mu=0\), the center is invisible.

## Weighted-center audit

Detailed balance with positive weights gives
\(\sum_iw_iLf_i=0\). For a nonzero target, the exact center is therefore the
weighted sample mean. This is only a necessary scalar consequence; it does not
replace the pointwise covariance residual. A nonempty state set and positive
total weight are required before dividing by \(\sum_iw_i\). At zero target,
the center remains arbitrary. Connectivity and nonnegative active rates are
needed for the stronger assertion that harmonic functions are constant.

## Sphere residual and sampling quotient

For unit nodes, \(\lambda=d-1\), target \(2d\), and
\(A\in\operatorname{Sym}_0(d)\), define

\[
 M_i=P_0(C_i+2\Phi_i\Phi_i^T).
\]

Then

\[
 R_X(A)_i=(L+2dI)S_X(A)_i=\langle A,M_i\rangle_F.
\]

The algebraic form space is

\[
 E_{\rm form}=\ker R_X=\operatorname{span}\{M_i\}^{\perp}.
\]

The genuinely sampled exact space is instead

\[
 E_{\rm sample}=S_X(E_{\rm form})
 =\operatorname{im}S_X\cap\ker(L+2dI),
\]

and

\[
 \dim E_{\rm sample}
 =\operatorname{rank}S_X-\operatorname{rank}R_X.
\]

This quotient correction is essential: nonzero forms may vanish on every
sampled node. The earlier notation that counted only \(\dim E_{\rm form}\) is
not a genuine-mode count.

## Positive obstruction

Under \(I\ne\varnothing\), \(d>1\), nonnegative rates, unit nodes, and
\(L\Phi=-(d-1)\Phi\),

\[
 \operatorname{tr}C_i=2(d-1),\qquad
 \Phi_i^TM_i\Phi_i
 =\sum_ja_{ij}(\Phi_i\cdot\Phi_j-1)^2>0.
\]

Strictness follows from the eigenmap equation itself: if all positive jumps
were between coincident embedded nodes, \(L\Phi(i)\) would vanish. Testing the
trace-free tensor \(M_i\) against
\(\Phi_i\Phi_i^T-I/d\) gives

\[
 \|M_i\|_F\ge
 \frac{\sum_ja_{ij}(\Phi_i\cdot\Phi_j-1)^2}
 {\sqrt{1-1/d}}.
\]

Hence \(R_X\ne0\), but aliases remain in its kernel.

## Structural result and sharpness

The main rigidity mechanism is not the covariance expansion alone. For
\(d>1\), unit nodes satisfying \(L\Phi=-(d-1)\Phi\), one non-antipodal shell
together with the full signed tangent tight-frame identity gives

\[
 R_X=DS_X,\qquad D_{ii}=d\ell_i>0,
\]

so \(E_{\rm form}=K_X\) and \(E_{\rm sample}=0\). Coincident embedded jumps are
excluded from shell rates and moments because their increments vanish.

The positive spherical hexagonal prism proves sharpness: it is connected,
reversible, vertex-transitive, full-dimensional, one-shell, and injectively
sampled, but tangent-anisotropic and has two genuine exact modes. The signed
cube gives the complementary attainability result, restoring the full sampled
cross-quadratic module with sharp undirected negative mass two.

## Status boundary

PROVED:

- covariance and arbitrary-target identities;
- weighted centering under the stated hypotheses;
- residual factorization and sampling quotient;
- positive radial obstruction and norm bound;
- signed one-shell rigidity;
- equivariant quotient rank gap and corrected invariance theorem;
- prism sharpness and signed-cube optimum.

COMPUTATIONAL:

- exact finite matrices, ranks, minors, group actions, and KKT regressions in
  the dedicated SymPy audits.

EXTERNAL:

- rank-nullity, finite real semisimplicity, the self-adjoint spectral theorem,
  and convex KKT/subgradient theory.

No priority claim is made from the covariance identity or finite rank tables
alone.

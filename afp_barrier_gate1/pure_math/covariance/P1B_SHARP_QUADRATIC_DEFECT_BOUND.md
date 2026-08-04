# P1B — the sharp universal genuinely sampled quadratic-defect bound

## 1. Statement, conventions, and minimal nondegeneracy

Let `I` be a finite nonempty set, let `d>=2`, and let

\[
 w_i>0,\qquad \sum_{i\in I}w_i=1,\qquad
 \Omega_i\in S^{d-1}\subset\mathbb R^d.
\]

Let the jump generator have nonnegative off-diagonal rates and shared
conductances

\[
 (Lf)_i=\sum_{j\ne i}a_{ij}(f_j-f_i),\qquad
 a_{ij}=\frac{\gamma_{ij}}{w_i},\qquad
 \gamma_{ij}=\gamma_{ji}\ge0,
\]

and assume the coordinate eigenmap equation

\[
 L\Omega=-(d-1)\Omega.                                      \tag{1.1}
\]

The sample space is

\[
 H_w=(\mathbb R^I,\langle f,g\rangle_w),\qquad
 \langle f,g\rangle_w=\sum_iw_if_ig_i,
\]

and the coefficient space is

\[
 V=\operatorname{Sym}_0(d),\qquad
 \langle A,H\rangle_F=\operatorname{tr}(A^TH).
\]

Use all P1A definitions:

\[
 (S_2A)_i=\Omega_i^TA\Omega_i,\qquad
 K_X=\ker S_2,\qquad R_2=(L+2dI)S_2,
\]

\[
 C_i=\sum_j a_{ij}(\Omega_j-\Omega_i)(\Omega_j-\Omega_i)^T,
\]

\[
 M_i=P_0(C_i+2\Omega_i\Omega_i^T),\qquad
 Z_i=\Omega_i\Omega_i^T-I/d,
\]

\[
 \ell_{ij}=1-\Omega_i\cdot\Omega_j,\qquad
 r_i=\sum_{j\ne i}a_{ij},\qquad
 \epsilon_i=\sum_ja_{ij}\ell_{ij}^2,
\]

\[
 B_i=M_i-\frac d{d-1}\epsilon_iZ_i.                    \tag{1.2}
\]

The genuinely sampled quadratic defect is

\[
 \mathfrak D_2
 =\sup_{A\notin K_X}
   \frac{\|R_2A\|_w}{\|S_2A\|_w}.                     \tag{1.3}
\]

No sampling injectivity, connectivity, equal weights, regular degree,
transitivity, complete graph, distinct nodes, or invariant sampled range is
assumed.

The definition is automatically nondegenerate under the displayed
hypotheses.  For every `i`, `Z_i in V` and

\[
 (S_2Z_i)_i
 =\Omega_i^TZ_i\Omega_i
 =\frac{d-1}{d}>0.                                     \tag{1.4}
\]

Thus `S_2` is not the zero map and the supremum in (1.3) is over a nonempty
set.  Equation (1.1) also gives

\[
 \sum_ja_{ij}\ell_{ij}=d-1>0,
\]

so every `r_i` and therefore `r_max=max_i r_i` is strictly positive.

### Theorem P1B

Set

\[
 E_\epsilon=\sum_iw_i\epsilon_i^2,
 \qquad
 E_B=\sum_iw_i\|B_i\|_F^2.                             \tag{1.5}
\]

Then

\[
 \boxed{
 \mathfrak D_2^2
 \ge
 \frac{d^2}{(d-1)^2}E_\epsilon
 +\frac d{d-1}E_B
 }                                                       \tag{1.6}
\]

and consequently

\[
 \boxed{
 \mathfrak D_2
 \ge \frac d{d-1}\sqrt{E_\epsilon}
 \ge \frac{d(d-1)}{r_{\max}}
 }.                                                      \tag{1.7}
\]

Equivalently,

\[
 \boxed{\mathfrak D_2r_{\max}\ge d(d-1).}              \tag{1.8}
\]

For `d=3`,

\[
 \boxed{\mathfrak D_2r_{\max}\ge6.}                   \tag{1.9}
\]

The constants in (1.6)--(1.9) are sharp in every dimension `d>=2`.

## 2. P1A identities used by the proof

P1A proves, without injectivity of `S_2`,

\[
 K_X\subseteq\ker R_2,                                 \tag{2.1}
\]

\[
 (S_2A)_i=\langle A,Z_i\rangle_F,
 \qquad
 (R_2A)_i=\langle A,M_i\rangle_F,                      \tag{2.2}
\]

and the weighted adjoints

\[
 S_2^*f=\sum_iw_if_iZ_i,
 \qquad
 R_2^*f=\sum_iw_if_iM_i.                               \tag{2.3}
\]

Hence

\[
 G_S:=S_2^*S_2=\sum_iw_iZ_i\otimes Z_i,
 \qquad
 G_R:=R_2^*R_2=\sum_iw_iM_i\otimes M_i.                \tag{2.4}
\]

The exact local two-defect decomposition is

\[
 M_i=\frac d{d-1}\epsilon_iZ_i+B_i,
 \qquad B_i\perp_F Z_i,                                \tag{2.5}
\]

\[
 \|M_i\|_F^2
 =\frac d{d-1}\epsilon_i^2+\|B_i\|_F^2.               \tag{2.6}
\]

The sampling rows all have the same norm

\[
 \|Z_i\|_F^2=\frac{d-1}{d}.                            \tag{2.7}
\]

Using `sum_i w_i=1`, (2.4)--(2.7) give the exact traces

\[
 \operatorname{tr}G_S=\frac{d-1}{d},                  \tag{2.8}
\]

\[
 \operatorname{tr}G_R
 =\frac d{d-1}E_\epsilon+E_B.                          \tag{2.9}
\]

Finally, at every row,

\[
 \epsilon_i
 =\frac{(d-1)^2}{r_i}
 +V_i,                                                  \tag{2.10}
\]

where

\[
 V_i:=\sum_ja_{ij}
 \left(\ell_{ij}-\frac{d-1}{r_i}\right)^2\ge0.         \tag{2.11}
\]

All factors in (2.8)--(2.11) are literal.  In particular, omitting the
normalization `sum_i w_i=1`, replacing the weighted adjoint by an unweighted
transpose, or using a Frobenius norm on `V/K_X` changes the theorem.

## 3. The quotient operator

Give

\[
 Q_X=V/K_X
\]

the sampled inner product

\[
 \langle[A],[H]\rangle_S
 :=\langle S_2A,S_2H\rangle_w.                         \tag{3.1}
\]

The induced sampling map

\[
 \bar S_2:Q_X\longrightarrow\operatorname{im}S_2
\]

is an isometric isomorphism.  By (2.1), there is a unique map

\[
 U:\operatorname{im}S_2\longrightarrow H_w,
 \qquad U(S_2A)=R_2A.                                  \tag{3.2}
\]

It satisfies

\[
 R_2=US_2,
 \qquad
 \bar R_2=U\bar S_2,
 \qquad
 \mathfrak D_2=\|U\|.                                 \tag{3.3}
\]

This factorization is the sampling-kernel correction.  It remains valid when
`K_X` is large, when rows repeat, and when `im S_2` is not invariant under
`L+2dI`.

## 4. Proof route I: weighted Gram operators and generalized eigenvalues

Let

\[
 W_X=K_X^{\perp_F}.
\]

On `W_X`, `G_S` is positive definite and

\[
 \mathfrak D_2^2
 =\lambda_{\max}
 \left(G_S^{-1/2}G_RG_S^{-1/2}\big|_{W_X}\right).      \tag{4.1}
\]

Equivalently, for every `A in V`, including `A in K_X`,

\[
 \langle A,G_RA\rangle_F
 \le \mathfrak D_2^2\langle A,G_SA\rangle_F.           \tag{4.2}
\]

Thus the positive-semidefinite operator inequality

\[
 G_R\preceq \mathfrak D_2^2G_S                         \tag{4.3}
\]

holds on `V`.  Taking the Frobenius Hilbert-space trace gives

\[
 \operatorname{tr}G_R
 \le \mathfrak D_2^2\operatorname{tr}G_S.             \tag{4.4}
\]

Since (2.8) is positive, substitute (2.8)--(2.9):

\[
 \mathfrak D_2^2
 \ge
 \frac{\frac d{d-1}E_\epsilon+E_B}{(d-1)/d}
 =\frac{d^2}{(d-1)^2}E_\epsilon
  +\frac d{d-1}E_B.
\]

This proves (1.6).  The proposed coefficient of `E_B` therefore requires no
adjustment: it is exactly `d/(d-1)`.

### Equality in the generalized trace step

Put

\[
 C=G_S^{-1/2}G_RG_S^{-1/2}\big|_{W_X},
 \qquad D=\mathfrak D_2.
\]

Then `0<=C<=D^2I`.  Equality in (4.4) is equivalent to

\[
 G_R=D^2G_S,                                            \tag{4.5}
\]

or, equivalently,

\[
 C=D^2I_{W_X}.                                         \tag{4.6}
\]

Indeed, equality makes the trace of the product of the positive operator
`D^2I-C` with the positive-definite sampling Gram on `W_X` equal to zero;
hence `D^2I-C=0`.  Thus every nonzero generalized eigenvalue is the same
number `D^2`.

In quotient language, (4.5) is

\[
 \bar R_2^*\bar R_2=D^2I_{Q_X}                         \tag{4.7}
\]

for the sampled metric (3.1).  Equivalently, `U/D` is an isometry on
`im S_2`.  This saturation does **not** by itself imply `R_2=cS_2`; the
isometry may be nontrivial.

## 5. Proof route II: Hilbert--Schmidt norm of the quotient factorization

Let `E_1,...,E_m` be any Frobenius-orthonormal basis of `V`, where

\[
 m=\frac{d(d+1)}2-1.
\]

By (3.3),

\[
 \begin{aligned}
 \|R_2\|_{HS}^2
 &=\sum_{\alpha=1}^m\|US_2E_\alpha\|_w^2\\
 &\le\|U\|^2\sum_{\alpha=1}^m\|S_2E_\alpha\|_w^2\\
 &=\mathfrak D_2^2\|S_2\|_{HS}^2.                     \tag{5.1}
 \end{aligned}
\]

But

\[
 \|R_2\|_{HS}^2=\operatorname{tr}G_R,
 \qquad
 \|S_2\|_{HS}^2=\operatorname{tr}G_S.                 \tag{5.2}
\]

Equations (5.1)--(5.2) reproduce (4.4), hence (1.6).

Equality in (5.1) holds precisely when every vector in the spanning set
`{S_2E_alpha}` belongs to the top right-singular subspace of `U`.  Since these
vectors span `im S_2`, this is exactly

\[
 U^*U=\mathfrak D_2^2I_{\operatorname{im}S_2},         \tag{5.3}
\]

which is the same saturation condition as (4.7).

This route never selects a complement of `K_X` and never divides by a
singular sampling Gram.

## 6. Proof route III: random traceless-matrix averaging

Let `E_1,...,E_m` be as above and let

\[
 A=\sum_{\alpha=1}^m\xi_\alpha E_\alpha,
\]

where the `xi_alpha` are independent centered random variables with

\[
 \mathbb E[\xi_\alpha\xi_\beta]=\delta_{\alpha\beta}.
\]

A standard Gaussian or independent Rademacher signs both suffice.  Because
`K_X subset ker R_2`, the deterministic quotient bound extends to every
`A in V`:

\[
 \|R_2A\|_w^2\le\mathfrak D_2^2\|S_2A\|_w^2.          \tag{6.1}
\]

Taking expectations and using isotropy gives

\[
 \mathbb E\|R_2A\|_w^2=\operatorname{tr}G_R,
 \qquad
 \mathbb E\|S_2A\|_w^2=\operatorname{tr}G_S.          \tag{6.2}
\]

Thus (6.1)--(6.2) again give (4.4).  Equality means the nonnegative random
variable

\[
 \mathfrak D_2^2\|S_2A\|_w^2-\|R_2A\|_w^2
\]

vanishes almost surely.  Full support of the Gaussian, or polarization after
Rademacher averaging, implies the operator identity (4.5).

This proof exposes the role of the weighted trace as an isotropic average over
traceless quadratic forms.

## 7. Proof route IV: finite-frame/covariance domination

The families

\[
 \{\sqrt{w_i}Z_i\}_{i\in I},
 \qquad
 \{\sqrt{w_i}M_i\}_{i\in I}
\]

are finite frames, possibly highly dependent.  Their frame operators are
`G_S` and `G_R`.  Definition (1.3) says exactly that, for every `A in V`,

\[
 \sum_iw_i\langle A,M_i\rangle_F^2
 \le\mathfrak D_2^2
 \sum_iw_i\langle A,Z_i\rangle_F^2.                   \tag{7.1}
\]

Therefore the residual frame operator is dominated by the sampled frame
operator as in (4.3).  The frame potentials are

\[
 \sum_iw_i\|Z_i\|_F^2=\frac{d-1}{d},
\]

\[
 \sum_iw_i\|M_i\|_F^2
 =\frac d{d-1}E_\epsilon+E_B.                          \tag{7.2}
\]

Taking the trace of (7.1) over any orthonormal coefficient frame proves
(1.6).  Dependence of the frame rows and sampling aliases cause no problem.

## 8. Semigroup route: screened but not used

A semigroup proof would normally try to restrict `L+2dI` to `im S_2` and use
dissipation there.  P1A contains exact positive reversible fixtures for which
`im S_2` is not invariant under `L+2dI`.  Therefore a semigroup acting only on
`im S_2` is not available under the theorem's hypotheses.  The quotient map
`U:im S_2->H_w` is the correct general object, and the Hilbert--Schmidt proof
already gives the required independent operator argument without adding a
false invariance assumption.

## 9. From the trace theorem to the radial bound

Since `E_B>=0`, (1.6) gives

\[
 \mathfrak D_2^2
 \ge\frac{d^2}{(d-1)^2}E_\epsilon.
\]

Both sides are nonnegative, hence

\[
 \boxed{
 \mathfrak D_2\ge\frac d{d-1}\sqrt{E_\epsilon}
 }.                                                      \tag{9.1}
\]

Equality in (9.1) holds if and only if both:

1. the generalized trace inequality is saturated, equivalently (4.5)--(4.7);
2. `E_B=0`.

Because every `w_i` is strictly positive,

\[
 E_B=0\quad\Longleftrightarrow\quad B_i=0\ \text{for every }i.       \tag{9.2}
\]

Thus equality in (9.1) means the quotient residual has constant singular
value and every local residual row is purely radial:

\[
 M_i=\frac d{d-1}\epsilon_iZ_i.                        \tag{9.3}
\]

The scalars in (9.3) need not yet be equal; sampling-row dependence can allow
trace saturation with nonconstant `epsilon_i`.

## 10. The rate floor

Let

\[
 a_*:=\frac{(d-1)^2}{r_{\max}}>0.                       \tag{10.1}
\]

From (2.10) and `r_i<=r_max`,

\[
 \epsilon_i
 \ge\frac{(d-1)^2}{r_i}
 \ge\frac{(d-1)^2}{r_{\max}}=a_*                      \tag{10.2}
\]

at every vertex.  Therefore

\[
 E_\epsilon=\sum_iw_i\epsilon_i^2
 \ge\sum_iw_i a_*^2=a_*^2,                            \tag{10.3}
\]

where the last equality uses `sum_iw_i=1`.  Taking square roots yields

\[
 \boxed{
 \sqrt{E_\epsilon}\ge\frac{(d-1)^2}{r_{\max}}
 }.                                                      \tag{10.4}
\]

Combining (9.1) and (10.4) proves (1.7)--(1.8).

### Equality in the rate floor

Since all weights are positive, equality in (10.3)--(10.4) is equivalent to

\[
 \epsilon_i=a_*\quad\text{for every }i.                \tag{10.5}
\]

For a fixed vertex, the chain

\[
 a_*=\epsilon_i
 =\frac{(d-1)^2}{r_i}+V_i
 \ge\frac{(d-1)^2}{r_i}
 \ge a_*
\]

has equal endpoints.  Hence every intermediate inequality is equality:

\[
 r_i=r_{\max},\qquad V_i=0.                            \tag{10.6}
\]

Conversely, (10.6) implies (10.5).  Therefore equality in the rate floor is
necessary and sufficient for

\[
 r_i=r_{\max}
\]

at every positive-mass vertex and

\[
 \sum_ja_{ij}
 \left(\ell_{ij}-\frac{d-1}{r_{\max}}\right)^2=0.      \tag{10.7}
\]

Since the summands are nonnegative, (10.7) is equivalent to

\[
 \ell_{ij}=\frac{d-1}{r_{\max}}
\]

on every active directed edge.

## 11. Complete equality theorem

Let

\[
 c_*:=\frac{d(d-1)}{r_{\max}}.                          \tag{11.1}
\]

The following conditions are equivalent.

1. The final sharp product bound is an equality:

   \[
   \mathfrak D_2r_{\max}=d(d-1).
   \]

2. At every vertex,

   \[
   r_i=r_{\max},\qquad V_i=0,\qquad B_i=0.             \tag{11.2}
   \]

3. At every vertex,

   \[
   \epsilon_i=\frac{(d-1)^2}{r_{\max}},
   \qquad B_i=0.                                       \tag{11.3}
   \]

4. The residual rows satisfy

   \[
   M_i=c_*Z_i\qquad\text{for every }i.                 \tag{11.4}
   \]

5. On the full coefficient space and on the sampled quotient,

   \[
   R_2=c_*S_2,
   \qquad
   \bar R_2=c_*\bar S_2.                               \tag{11.5}
   \]

### Proof

If condition 1 holds, every inequality in (1.7) is equality.  Sections 9 and
10 give generalized trace saturation, `B_i=0`, `r_i=r_max`, and `V_i=0`.
This proves condition 2.  Equivalence of conditions 2 and 3 is (2.10).
Substitute condition 3 into (2.5):

\[
 M_i
 =\frac d{d-1}\frac{(d-1)^2}{r_{\max}}Z_i
 =c_*Z_i,
\]

which is condition 4.  The row-representer formulas (2.2) show that conditions
4 and 5 are equivalent.  Finally, `S_2` is nonzero by (1.4), so condition 5
gives

\[
 \mathfrak D_2=c_*,
\]

and hence condition 1.

In the final equality case, generalized operator-norm/trace saturation is not
an additional hypothesis: it follows from the stronger scalar identity
`R_2=c_*S_2`.  Outside the final equality case, trace saturation alone is only
the isometric condition (4.7) and need not make `R_2` a scalar multiple of
`S_2`.

## 12. Matrix formulations

### 12.1 Frobenius-orthonormal coefficient coordinates

Choose a Frobenius-orthonormal basis of `V`.  Let `S` and `R` be the sample and
residual matrices and let

\[
 W=\operatorname{diag}(w_i).
\]

Then

\[
 G_S=S^TWS,
 \qquad
 G_R=R^TWR.                                             \tag{12.1}
\]

Let `Q` have orthonormal columns spanning `(ker S)^perp`.  Then

\[
 \widehat G_S=Q^TG_SQ>0,
 \qquad
 \widehat G_R=Q^TG_RQ,                                 \tag{12.2}
\]

and

\[
 \mathfrak D_2^2
 =\lambda_{\max}
 \left(\widehat G_S^{-1/2}\widehat G_R
       \widehat G_S^{-1/2}\right).                     \tag{12.3}
\]

The trace inequality is

\[
 \operatorname{tr}(R^TWR)
 \le\mathfrak D_2^2\operatorname{tr}(S^TWS).           \tag{12.4}
\]

The traces in (12.4) equal (2.8)--(2.9), including when `S` is rank deficient.
Equality in (12.4) is

\[
 \widehat G_R=\mathfrak D_2^2\widehat G_S.             \tag{12.5}
\]

Final equality is the stronger matrix equation

\[
 R=c_*S.                                                \tag{12.6}
\]

### 12.2 Arbitrary coefficient coordinates

If the coefficient basis has Frobenius Gram matrix `F>0`, then the bilinear
Gram matrices remain

\[
 S^TWS,\qquad R^TWR,
\]

but the corresponding operator matrices are

\[
 F^{-1}S^TWS,
 \qquad
 F^{-1}R^TWR.                                           \tag{12.7}
\]

The Hilbert-space traces are therefore

\[
 \operatorname{tr}(F^{-1}S^TWS),
 \qquad
 \operatorname{tr}(F^{-1}R^TWR),                       \tag{12.8}
\]

not the raw traces of the bilinear matrices.  Deflating any full-rank lift of
`V/K_X` gives a congruent generalized pencil and the same `mathfrak D_2`.

## 13. Sharpness in every dimension

Let `Omega_0,...,Omega_d` be a regular simplex in `S^{d-1}`:

\[
 \sum_{i=0}^d\Omega_i=0,
 \qquad
 \Omega_i\cdot\Omega_j=-1/d\quad(i\ne j),
\]

\[
 \sum_{i=0}^d\Omega_i\Omega_i^T=\frac{d+1}{d}I.
\]

Take uniform weights and the complete off-diagonal rate

\[
 a_{ij}=\frac{d-1}{d+1}\quad(i\ne j).                  \tag{13.1}
\]

Then

\[
 L\Omega=-(d-1)\Omega,
 \qquad
 r_i=\frac{d(d-1)}{d+1},
 \qquad
 \ell_{ij}=\frac{d+1}{d}.                              \tag{13.2}
\]

For fixed `i`, direct use of the simplex identities gives

\[
 C_i=\frac{d-1}{d}I+(d-1)\Omega_i\Omega_i^T,
\]

and therefore

\[
 M_i=(d+1)Z_i.                                         \tag{13.3}
\]

Hence

\[
 R_2=(d+1)S_2,
 \qquad
 \mathfrak D_2=d+1.                                    \tag{13.4}
\]

Consequently

\[
 \mathfrak D_2r_{\max}
 =(d+1)\frac{d(d-1)}{d+1}
 =d(d-1).                                               \tag{13.5}
\]

Thus the universal constant cannot be increased.  The cross-polytope and
hypercube families provide two further all-dimensional equality families.
In `d=3`, all five regular Platonic shortest-edge generators also attain the
constant `6`; the tetrahedral, octahedral, and cubical form spaces may contain
sampling aliases, which do not affect the quotient theorem.

## 14. Adversarial and exact-example audit

The deterministic P1B audit reuses all 19 P1A fixtures and adds:

- two disconnected antipodal equality components;
- four exact rational nearly singular antipodal-pair families with sampling
  Gram determinants tending to zero while remaining positive;
- an explicit proof that zero sampling rank is impossible under `d>=2` and
  unit-sphere sampling.

It checks 24 fixtures in total, including:

```text
regular simplices, cross-polytopes and hypercubes in d=2,3,4;
all five three-dimensional Platonic graphs;
an aliased antipodal pair;
unequal masses with repeated nodes;
a positive non-invariant sampled range;
a spherical prism with genuine sampled exact modes;
a configuration with both defects nonzero;
a degenerate equatorial configuration;
a disconnected generator;
nearly singular sampling matrices.
```

For every fixture it verifies exactly:

```text
weighted Gram traces;
the strong two-defect coefficient;
the radial lower bound;
the epsilon RMS floor;
the final product bound;
generalized-eigenvalue saturation;
all equality equivalences;
random-matrix trace averaging;
quotient deflation;
rowwise scalar residual in the equality cases.
```

The unequal repeated-node example is particularly useful: the generalized
trace inequality is saturated, but `B_i` is not identically zero and the final
product inequality is strict.  It therefore prevents conflating trace
saturation with the complete equality theorem.

The audit rejects:

```text
unweighted adjoints;
wrong generator or target sign;
raw singular pencils;
form-space/sample-space conflation;
non-invariant compression squaring;
omission of sum_i w_i=1;
a wrong anisotropy coefficient;
zero-sampling-rank assumptions;
condition-number-dependent constants.
```

## 15. Prior-art boundary

The proof is finite Hilbert-space and frame algebra built on P1A.  The cited
background serves only as context and normalization control:

- spectral limitations for nonnegative manifold quadrature concern the number
  of integrated eigenfunctions, not the quotient operator norm here;
- spherical/hyperbolic discrete Laplacians provide a geometry-specific class
  of negative-semidefinite weighted generators, not this universal trace
  argument;
- positive meshfree stencils and spectrahedral graph sparsifiers concern
  feasibility or eigenpair-preserving design spaces, not the two-defect trace
  identity;
- graph-Laplacian spectral-convergence estimates are asymptotic probabilistic
  approximation results and do not supply the finite sharp constant;
- association schemes and spherical designs explain symmetric equality
  examples but are not hypotheses of the theorem.

No external theorem is used to prove (1.6)--(1.9).  The only imported
mathematical input is the accepted P1A quotient, row-representer, Gram, and
local two-defect package.

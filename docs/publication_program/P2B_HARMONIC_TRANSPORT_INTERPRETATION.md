# Harmonic defect as a dynamical and transport-error certificate

Status: **complete theorem source**.  Exact-head acceptance is recorded by
the publication workflow and immutable archive, not assumed in the proof.

This paper starts from the accepted Paper-I convention for a positive
reversible spherical generator and proves the separate transport theorem that
Paper I deliberately did not claim.  The result is an error-certificate
theorem, not a claim that a small angular defect alone guarantees a small
Boltzmann--Fokker--Planck error.  Physical-model, sampling, spatial,
energy-group, boundary, and iterative residuals remain visible throughout.

## 1. Setting and notation

Let

$$
H_w=\mathbb C^N,\qquad
\langle x,y\rangle_w=x^*Wy,\qquad
W=\operatorname{diag}(w_1,\ldots,w_N),\qquad w_i>0.
$$

A shared-conductance generator has

$$
(Lf)_i=\frac1{w_i}\sum_{j:\{i,j\}\in E}\gamma_{ij}(f_j-f_i),
\qquad \gamma_{ij}=\gamma_{ji}\ge0.                 \tag{1.1}
$$

Consequently

$$
L\mathbf1=0,\qquad WL=L^*W,
\qquad
-\langle Lf,f\rangle_w
=\frac12\sum_{i,j}\gamma_{ij}|f_i-f_j|^2\ge0.       \tag{1.2}
$$

Thus $A=-L$ is self-adjoint and nonnegative in $H_w$, and $e^{tL}$ is a
contraction.  Positivity of the off-diagonal entries is important for the
Markov interpretation, while reversibility and nonpositivity are the precise
hypotheses used in the Hilbert-space estimates below.

For spherical harmonics of degree $\ell$ on $S^2$, write
$\lambda_\ell=\ell(\ell+1)$.  Let $S_\ell$ be evaluation on the fixed nodes,
$K_\ell=\ker S_\ell$, and

$$
R_\ell=(L+\lambda_\ell I)S_\ell.                    \tag{1.3}
$$

Because $K_\ell\subset\ker R_\ell$, the residual descends to
$\mathcal H_\ell/K_\ell$ with sampled norm
$\|[a]\|_{S,\ell}=\|S_\ell a\|_w$.  If $V_\ell$ is any matrix whose columns
are a $W$-orthonormal basis of $\operatorname{im}S_\ell$, then

$$
T_\ell=W^{1/2}(L+\lambda_\ell I)V_\ell,
\qquad
\mathfrak D_\ell=\|T_\ell\|_2.                      \tag{1.4}
$$

The output of $T_\ell$ is the whole sampled angular space.  It is never
compressed back to $\operatorname{im}S_\ell$.

We use

$$
k_{t,\lambda}(\mu)
=\int_0^t e^{-\mu(t-s)}e^{-\lambda s}\,ds
=\begin{cases}
\dfrac{e^{-\mu t}-e^{-\lambda t}}{\lambda-\mu},&\mu\ne\lambda,\\[5pt]
t e^{-\lambda t},&\mu=\lambda,
\end{cases}                                          \tag{1.5}
$$

and

$$
k_{t,\lambda}=k_{t,\lambda}(0)=
\begin{cases}
(1-e^{-\lambda t})/\lambda,&\lambda>0,\\
t,&\lambda=0.
\end{cases}                                           \tag{1.6}
$$

## 2. The one-mode dynamical theorem

### Theorem 2.1 (exact Duhamel identity and sharp contraction bound)

Let $L$ satisfy (1.2), let $\lambda>0$, and put
$r=(L+\lambda I)u$.  For every $t\ge0$,

$$
e^{tL}u-e^{-\lambda t}u
=\int_0^t e^{(t-s)L}e^{-\lambda s}r\,ds              \tag{2.1}
$$

and

$$
\boxed{
\|e^{tL}u-e^{-\lambda t}u\|_w
\le \frac{1-e^{-\lambda t}}{\lambda}
       \|(L+\lambda I)u\|_w.}                       \tag{2.2}
$$

The multiplier in (2.1) is $k_{t,\lambda}(A)$ for $A=-L$.  For $t>0$ the
scalar function $\mu\mapsto k_{t,\lambda}(\mu)$ is positive and strictly
decreasing on $[0,\infty)$, so

$$
\|k_{t,\lambda}(A)\|=k_{t,\lambda}(0).
$$

For a conservative generator $0\in\sigma(A)$; hence (2.2) is the exact
full-space operator norm.  For $t>0$, equality holds precisely when every
nonzero spectral component of $r$ lies in $\ker L$.  In particular it is
attained when $u\in\ker L$.  At $t=0$ both sides vanish for every $u$.  If the
relevant reducing subspace instead satisfies $A\ge\gamma I$, the operator
constant is at most $k_{t,\lambda}(\gamma)$; it is sharp when
$\gamma=\min\sigma(A|_{\mathcal U})$.

#### Proof

Set $F(s)=e^{(t-s)L}e^{-\lambda s}u$.  Finite
dimensionality gives

$$
F'(s)=-e^{(t-s)L}e^{-\lambda s}(L+\lambda I)u.
$$

Integrating $-F'$ from $0$ to $t$ proves (2.1).  The spectral theorem applied
to $A=-L$ gives the multiplier formula.  Contraction yields (2.2), and strict
monotonicity of (1.5) gives the equality statement and the reducing-subspace
refinement.  No invariance of a sampled harmonic space is used. $\square$

### Theorem 2.2 (resolvent identity and sharp constant)

For $\alpha>0$,

$$
(\alpha-L)^{-1}u-\frac{u}{\alpha+\lambda}
=\frac{(\alpha-L)^{-1}(L+\lambda I)u}{\alpha+\lambda}                 \tag{2.3}
$$

and

$$
\boxed{
\left\|(\alpha-L)^{-1}u-\frac{u}{\alpha+\lambda}\right\|_w
\le\frac{\|(L+\lambda I)u\|_w}{\alpha(\alpha+\lambda)}.}           \tag{2.4}
$$

The contraction constant $\|(\alpha-L)^{-1}\|=1/\alpha$ is sharp for a
conservative generator.  On a reducing subspace on which $-L\ge\gamma I$,
the upper bound replaces $\alpha$ by $\alpha+\gamma$; this refinement is
sharp when $\gamma$ is the actual spectral minimum on that subspace.  At
$\alpha=0$ the full conservative resolvent does not exist; a zero-frequency
statement requires compatibility with $\ker L$ and a spectral gap on its
orthogonal complement.

#### Proof

Multiplication of (2.3) by $\alpha-L$ reduces both sides to
$u-(\alpha-L)u/(\alpha+\lambda)=(L+\lambda I)u/(\alpha+\lambda)$.
The spectral theorem gives
$\|(\alpha+A)^{-1}\|=1/\alpha$ because $0\in\sigma(A)$. $\square$

### Corollary 2.3 (equilibrium-resolved constants)

Let $P_0$ be the $H_w$-orthogonal projector onto $\ker L$, $Q_0=I-P_0$,
and suppose $-L\ge\gamma Q_0$.  Then

$$
\begin{aligned}
\|e^{tL}u-e^{-\lambda t}u\|_w^2
&\le k_{t,\lambda}(0)^2\|P_0r\|_w^2
 +k_{t,\lambda}(\gamma)^2\|Q_0r\|_w^2,\\
\left\|(\alpha-L)^{-1}u-\frac{u}{\alpha+\lambda}\right\|_w^2
&\le\frac1{(\alpha+\lambda)^2}
\left(\frac{\|P_0r\|_w^2}{\alpha^2}
+\frac{\|Q_0r\|_w^2}{(\alpha+\gamma)^2}\right).
                                                               \tag{2.5}
\end{aligned}
$$

Here $P_0r=\lambda P_0u$.  A claim that a sampled shell is mean zero therefore
requires an explicit quadrature condition; it is not implied by the
continuum harmonic degree.

## 3. Shells, bands, and physical angular norms

### Theorem 3.1 (complete sampled shell)

For every sampled shell in (1.3)--(1.4), with the convention
$k_{t,0}=t$ from (1.6),

$$
\left\|e^{tL}V_\ell-e^{-\lambda_\ell t}V_\ell\right\|_{2\to w}
\le k_{t,\lambda_\ell}\,\mathfrak D_\ell,             \tag{3.1}
$$

and

$$
\left\|(\alpha-L)^{-1}V_\ell-
\frac{V_\ell}{\alpha+\lambda_\ell}\right\|_{2\to w}
\le\frac{\mathfrak D_\ell}
{\alpha(\alpha+\lambda_\ell)}.                       \tag{3.2}
$$

Equivalently these are operator bounds from
$\mathcal H_\ell/K_\ell$ with its sampled norm into all of $H_w$.

#### Proof

Apply Theorems 2.1--2.2 to $u=V_\ell c$ and use
$\|(L+\lambda_\ell I)V_\ell c\|_w
=\|T_\ell c\|_2\le\mathfrak D_\ell\|c\|_2$.  For $\ell=0$,
$V_0c$ is constant, $LV_0c=0$, and therefore $\mathfrak D_0=0$; both
operator differences vanish identically. $\square$

### Theorem 3.2 (band-limited synthesis, including cross-shell aliases)

Fix a finite degree set $\mathcal B$.  Let
$f_\ell=V_\ell c_\ell$ and retain the coefficient tuple
$c=(c_\ell)_{\ell\in\mathcal B}$.  Then

$$
e^{tL}\sum_{\ell\in\mathcal B}f_\ell
-\sum_{\ell\in\mathcal B}e^{-\lambda_\ell t}f_\ell
=\sum_{\ell\in\mathcal B}
K_\ell(t)(L+\lambda_\ell I)V_\ell c_\ell,            \tag{3.3}
$$

where
$K_\ell(t)=\int_0^t e^{(t-s)L}e^{-\lambda_\ell s}\,ds$.  Hence

$$
\|\text{left side of (3.3)}\|_w
\le\sum_{\ell\in\mathcal B}
k_{t,\lambda_\ell}\mathfrak D_\ell\|c_\ell\|_2.     \tag{3.4}
$$

In the direct-sum coefficient norm the exact worst-case constant is the
spectral norm of the row block

$$
\mathcal B_t=
\left[
W^{1/2}K_\ell(t)W^{-1/2}T_\ell
\right]_{\ell\in\mathcal B},                          \tag{3.5}
$$

whose $(\ell,m)$ Gram block is

$$
T_\ell^*
W^{-1/2}K_\ell(t)^*WK_m(t)W^{-1/2}T_m.                \tag{3.6}
$$

The safe scalar bound is

$$
\|\mathcal B_t\|_2
\le\left(\sum_{\ell\in\mathcal B}
k_{t,\lambda_\ell}^2\mathfrak D_\ell^2\right)^{1/2}. \tag{3.7}
$$

The resolvent analog replaces each row block by

$$
\frac1{\alpha+\lambda_\ell}
W^{1/2}(\alpha-L)^{-1}W^{-1/2}T_\ell,                 \tag{3.8}
$$

and is bounded by the square root of the sum of
$[\mathfrak D_\ell/(\alpha(\alpha+\lambda_\ell))]^2$.

Let $V_{\mathcal B}=[V_\ell]_{\ell\in\mathcal B}$.  The direct
coefficient-to-total-sample transfer below is available when

$$
\beta_{\mathcal B}
=\lambda_{\min}(V_{\mathcal B}^*WV_{\mathcal B})>0,  \tag{3.9}
$$

in which case $\|c\|_2\le
\beta_{\mathcal B}^{-1/2}\|V_{\mathcal B}c\|_w$.
More intrinsically, the continuum band evolution descends to sampled initial
data exactly when $\ker S_{\mathcal B}$ is invariant under the diagonal
eigenvalue map $\Lambda_{\mathcal B}$.  Exact quadrature through degree
$2\max\mathcal B$ is a sufficient, not necessary, condition for orthogonal
shell sampling.

#### Proof

Sum (2.1) over $\ell$ to obtain (3.3); contraction and the triangle
inequality give (3.4).  After multiplication by $W^{1/2}$, substitute
$T_\ell=W^{1/2}(L+\lambda_\ell I)V_\ell$.  The resulting coefficient map is
exactly the row block (3.5), so its induced norm is $\|\mathcal B_t\|_2$ and
its Gram matrix has blocks (3.6).  Bounding each block by
$k_{t,\lambda_\ell}\mathfrak D_\ell$ and applying Cauchy--Schwarz proves
(3.7); (2.3) gives (3.8) identically.

Moreover,
$\|V_{\mathcal B}c\|_w^2\ge\beta_{\mathcal B}\|c\|_2^2$, which proves the
total-sample transfer when (3.9) holds.  The continuum evolution defines a
map of sampled data precisely when
$S_{\mathcal B}e^{-t\Lambda_{\mathcal B}}k=0$ for every
$k\in\ker S_{\mathcal B}$ and every $t$.  Kernel invariance implies this;
conversely differentiation at $t=0$ gives
$S_{\mathcal B}\Lambda_{\mathcal B}k=0$, hence invariance.  Exact product
quadrature through degree $2\max\mathcal B$ transfers the positive continuum
Gram matrix and is therefore sufficient. $\square$

#### Alias obstruction

At the two equatorial samples $(1,0,0)$ and $(0,1,0)$,
$g=P_2(z)+1/2$ samples to zero, whereas

$$
S e^{t\Delta_{S^2}}g
=\frac{1-e^{-6t}}2(1,1)^T\ne0.                       \tag{3.10}
$$

Therefore no evolution estimate depending only on the total sampled initial
vector can represent every band-limited continuum function without (3.9) or
the kernel-invariance condition.  Shell defects also cannot be combined by
an unqualified root-sum-square rule.

### Theorem 3.3 (physical scattering-weighted norms)

Let $M=M^*>0$ be an ordinary Euclidean Hermitian matrix and define
$\|x\|_M^2=x^*Mx$.  If

$$
ML+L^*M\le0,                                          \tag{3.11}
$$

then Theorems 2.1--3.2 hold in the $M$ norm with contraction constant one.
This includes an angle-independent positive scattering multiplier
$\sigma_s(x,E)$, for which the fiber metric is $M=\sigma_s W$, and the graph
collision metric
$M=W\{aI+b(-L)\}$, $a>0$, $b\ge0$.  The latter is Hermitian because
$WL=L^*W$, and it is positive definite because $-L\ge0$ in $H_w$.  More
generally, if

$$
0<mW\le M\le \mathcal M W                                  \tag{3.12}
$$

but (3.11) is not known, transfer through the quadrature norm gives the safe
factor $\sqrt{\mathcal M/m}$.  The constants $m,\mathcal M$ are the extremal
generalized eigenvalues of $(M,W)$.  If $\sigma_s$ vanishes, the expression
is only a seminorm; one must restrict to its positive support/quotient or add
an independently positive density.

Direction-dependent weights do not automatically preserve reversibility.
For
$L=\begin{psmallmatrix}-1&1\\1&-1\end{psmallmatrix}$ and
$M=\operatorname{diag}(1,100)$, the constant-one claim fails.  This exact
two-state mutation is retained by the audit.

#### Proof

For $x(t)=e^{tL}x_0$,
$\frac d{dt}\|x(t)\|_M^2=x(t)^*(ML+L^*M)x(t)\le0$.
The same contraction argument applied to the Duhamel and Laplace-resolvent
identities proves the assertions, with every shell defect interpreted in
the $M$ norm.  If the accepted $W$-norm defect is used instead, (3.12)
transfers input and output norms and contributes $\sqrt{\mathcal M/m}$.
The two displayed special metrics satisfy (3.11) by $WL=L^*W$ and functional
calculus for the $W$-self-adjoint operator $-L$. $\square$

## 4. Inhomogeneous and time-dependent angular equations

Let $H$ be a Hilbert space.  Assume that $A(t)$ generates a well-posed
evolution family $U_A(t,s)$.  One sufficient nonautonomous hypothesis used
here is a common dense form domain $V\hookrightarrow H$ and measurable
closed sectorial forms $a_t$ with uniform boundedness and Gårding constants;
equivalently one may invoke a fully stated Kato-stable common-operator-domain
hypothesis.  Pointwise m-accretivity and measurability alone are not asserted
to generate $U_A$.  Suppose additionally that $\beta\in L^1(0,T)$ and

$$
\operatorname{Re}\langle A(t)v,v\rangle
\ge\beta(t)\|v\|^2.                                  \tag{4.1}
$$

For strong solutions the energy identity, followed by density within the
chosen generation theorem, gives

$$
\|U_A(t,s)\|\le
K_A(t,s):=\exp\!\left(-\int_s^t\beta(\tau)\,d\tau\right).            \tag{4.2}
$$

### Theorem 4.1 (inhomogeneous comparison)

Let

$$
\psi_t+A(t)\psi=f,\qquad
\phi_t+\widetilde A(t)\phi=\widetilde f,              \tag{4.3}
$$

and assume
$\phi\in C([0,T];H)\cap W^{1,1}(0,T;H)$,
$\phi(t)\in D(A(t))\cap D(\widetilde A(t))$ a.e., with the displayed
residual in $L^1(0,T;H)$.  Then

$$
\begin{aligned}
\|\psi(t)-\phi(t)\|
\le{}&K_A(t,0)\|\psi(0)-\phi(0)\|\\
&+\int_0^tK_A(t,s)
\bigl(\|(\widetilde A(s)-A(s))\phi(s)\|
+\|f(s)-\widetilde f(s)\|\bigr)\,ds.                \tag{4.4}
\end{aligned}
$$

#### Proof

$e=\psi-\phi$ satisfies
$e_t+A(t)e=(\widetilde A-A)\phi+(f-\widetilde f)$.
Variation of constants gives the equality before taking norms; (4.2) gives
(4.4).  Mild solutions follow by approximation under the stated form/Kato
generation hypothesis. $\square$

For time-dependent angular diffusion $A(t)=-d(t)L_h$ with $d(t)\ge0$,
the same proof applies pointwise.  If the target shell obeys
$\phi_t+d(t)\lambda_\ell\phi=f_\ell$, its angular residual is
$d(t)(L_h+\lambda_\ell I)\phi$, and (3.1) enters (4.4) under the integral.

## 5. Transport setting and hypotheses

Let $D\subset\mathbb R^d$ be bounded Lipschitz and let $I$ be an energy
interval or a finite group set.  The physical phase Hilbert space is

$$
H_\rho=L^2(D\times S^2\times I,
\rho(x,E)\,dx\,d\Omega\,dE),
\qquad 0<\rho_-\le\rho\le\rho_+<\infty.              \tag{5.1}
$$

The discrete norm is

$$
\|V\|_{\rho,h}^2
=\sum_g\eta_g\int_D\rho_g(x)
\sum_iw_i|V_{g i}(x)|^2\,dx,
\qquad \eta_g,w_i>0.                                 \tag{5.2}
$$

For $T=b\cdot\nabla_{x,E}$, Green's identity is

$$
\operatorname{Re}(Tv,v)_\rho
=\frac12(\|v_+\|_{\Gamma_+}^2-\|v_-\|_{\Gamma_-}^2)
-\frac12\int
\frac{\operatorname{div}(\rho b)}{\rho}|v|^2\rho.   \tag{5.3}
$$

We allow:

1. vacuum inflow $v_-=0$;
2. periodic faces, whose paired fluxes cancel;
3. specular reflection when $\rho$ and surface measure are reflection
   invariant;
4. albedo $v_-=\mathcal Bv_+$ with
   $\|\mathcal B\|_{\Gamma_+\to\Gamma_-}\le1$.

Prescribed nonhomogeneous inflow is first lifted by
$\ell\in W^{1,1}(0,T;H_\rho)\cap L^1(0,T;D(A))$ and transferred to the volume
source $f-\ell_t-A\ell$.  A boundary mismatch is not silently treated as a
volume $L^2$ residual.

Write $A_B=T+C_B$ for the physical Boltzmann operator and
$A_{FP}=T+C_{FP}$ for the continuum BFP approximation.  Assume

$$
\operatorname{Re}(C_Bv,v)_\rho
\ge c_0(t)\|v\|_\rho^2
+d_0\|(-\Delta_{S^2})^{1/2}v\|_\rho^2,
\qquad d_0\ge0,                                      \tag{5.4}
$$

and set

$$
\beta(t)=c_0(t)-\frac12
\left\|\left(\frac{\operatorname{div}(\rho b)}{\rho}\right)_+\right\|_\infty.
                                                               \tag{5.5}
$$

The angular form domain is $H^1(S^2)$ and the strong operator domain is
$H^2(S^2)$.  Streaming uses the transport graph space with traces.  Point
sampling is permitted only on angular $H^s(S^2)$ with $s>1$; bounded cell
averages avoid this extra hypothesis.  We require
$\operatorname{Range}(\lambda+A_B(t))=H_\rho$ for
$\lambda>-\operatorname*{ess\,inf}\beta$, or the corresponding
Kato-stable time-dependent form hypothesis.  Finite-dimensional discrete
operators require the analogous verified coercivity/range condition.

Under these assumptions (5.3)--(5.5) prove

$$
\|U_B(t,s)\|\le
K_B(t,s)=\exp\!\left(-\int_s^t\beta(\tau)\,d\tau\right),             \tag{5.6}
$$

rather than hiding stability inside a Duhamel citation.

Let $P:H_\rho\supset D(P)\to H_h$ be sampling or averaging.  Let
$J:H_h\to D(A_{FP})\cap D(A_B)$ be a bounded conforming reconstruction
satisfying $PJ=I_h$; set $Q=JP$.  Require

$$
A_{FP}JH_h\subset D(P),\qquad A_kJH_h\subset D(P)
\quad(k\in\{\Omega,x,E,0\}),                         \tag{5.7}
$$

with the corresponding time-dependent inclusions almost everywhere.  Thus
$R_1$, $PA_kJ$, and $QA_{FP}J$ below are defined rather than merely formal
compositions.  All error identities take place in the common continuous
space through $J$.

## 6. Exact six-way residual decomposition

Decompose

$$
A_{FP}=A_\Omega+A_x+A_E+A_0,\qquad
A_h=A_{\Omega,h}+A_{x,h}+A_{E,h}+A_{0,h}.             \tag{6.1}
$$

Let the physical truth and an arbitrary computed trajectory satisfy

$$
\psi_{B,t}+A_B\psi_B=f,\qquad
\Psi\in W^{1,1}(0,T;H_h),\qquad v=J\Psi.             \tag{6.2}
$$

Equivalently, a fully discrete trajectory is first given an absolutely
continuous time reconstruction.  Assume the six residuals defined below
belong to $L^1(0,T;H_\rho)$.  No discrete equation is assumed exactly: its
residual is retained.  Define

$$
\begin{aligned}
R_1&=(A_{FP}-A_B)v,
&&\text{physical BFP approximation},\\
R_2&=J(A_{\Omega,h}-PA_\Omega J)\Psi,
&&\text{angular generator},\\
R_3&=(f-Jf_h)+J(A_{0,h}-PA_0J)\Psi+(Q-I)A_{FP}v,
&&\text{quadrature/sampling and coefficient products},\\
R_4&=J(A_{x,h}-PA_xJ)\Psi,
&&\text{spatial discretization},\\
R_5&=J(A_{E,h}-PA_EJ)\Psi,
&&\text{energy-group/slowing down},\\
R_6&=J(f_h-\Psi_t-A_h\Psi),
&&\text{iteration, algebraic, and time-reconstruction residual}.
                                                               \tag{6.3}
\end{aligned}
$$

Here $R_3$ also contains angular integration/quadrature errors and
noncommuting sampled multiplication or transfer kernels.  The displayed
$H_\rho$ Duhamel bound requires a conforming reconstruction that removes face
jumps or lifts them into an $H_\rho$ residual included in $R_4$.  A raw
$V'$-valued jump residual instead needs a separate form-energy stability
theorem and is outside (7.2).  A fully discrete time method contributes its
temporal reconstruction residual to $R_6$.

### Theorem 6.1 (exact residual identity)

With $e=\psi_B-v$,

$$
\boxed{e_t+A_Be=\sum_{j=1}^6R_j,\qquad
e(0)=\psi_B(0)-J\Psi(0).}                            \tag{6.4}
$$

#### Proof

Because $PJ=I_h$,

$$
\sum_{k\in\{\Omega,x,E,0\}}
J(A_{k,h}-PA_kJ)\Psi
=JA_h\Psi-QA_{FP}v.
$$

Adding $(Q-I)A_{FP}v$, $f-Jf_h$, and
$J(f_h-\Psi_t-A_h\Psi)$ gives $f-v_t-A_{FP}v$.
Adding $R_1$ gives $f-v_t-A_Bv$, which is (6.4). $\square$

For $A_\Omega=-dL_\Omega$ and
$A_{\Omega,h}=-d_hL_h$, the angular term displays directly the sampled
harmonic defect.  Namely, for $v_\ell=\Pi_\ell v$ and
$\Psi_\ell=Pv_\ell$, matched scalar diffusion gives
$R_{2,\ell}=-dJ(L_h+\lambda_\ell I)\Psi_\ell$.

## 7. Two noncommuting transport proofs

### Theorem 7.1 (variation of constants)

Under Section 5,

$$
e(t)=U_B(t,0)e(0)
+\sum_{j=1}^6\int_0^tU_B(t,s)R_j(s)\,ds              \tag{7.1}
$$

and therefore

$$
\boxed{
\|e(t)\|_\rho
\le K_B(t,0)\|e(0)\|_\rho
+\sum_{j=1}^6\int_0^tK_B(t,s)\|R_j(s)\|_\rho\,ds.} \tag{7.2}
$$

For a uniform $\beta\ge0$, $K_B(t,s)=e^{-\beta(t-s)}$.

The corresponding noncommuting intertwining identities are

$$
\begin{aligned}
PU_A(t,s)-U_h(t,s)P
&=\int_s^tU_h(t,\tau)[A_h(\tau)P-PA(\tau)]U_A(\tau,s)\,d\tau,\\
U_B(t,s)-U_{FP}(t,s)
&=\int_s^tU_B(t,\tau)[A_{FP}(\tau)-A_B(\tau)]
U_{FP}(\tau,s)\,d\tau.                               \tag{7.3}
\end{aligned}
$$

The first equality assumes the displayed intertwining residual is integrable
on the propagated domain.  If $A_{FP}-A_B$ is bounded by $\varepsilon$ and
both evolutions decay with constants $\beta_B,\beta_{FP}$, then

$$
\|U_B(T,0)-U_{FP}(T,0)\|
\le\varepsilon\int_0^T
e^{-\beta_B(T-s)}e^{-\beta_{FP}s}\,ds.                \tag{7.4}
$$

For unbounded differences, (7.3) is asserted only when
$U_{FP}(s)u\in D(A_B)$ and
$(A_{FP}-A_B)U_{FP}(s)u\in L^1(0,T;H)$.

#### Proof

Variation of constants applied to (6.4) gives (7.1); (5.6), Minkowski's
integral inequality, and the triangle inequality give (7.2).  For the first
identity in (7.3), differentiate
$F(\tau)=U_h(t,\tau)P U_A(\tau,s)$ on the propagated common domain:

$$
F'(\tau)=U_h(t,\tau)[A_h(\tau)P-PA(\tau)]U_A(\tau,s).
$$

Its endpoint difference is
$F(t)-F(s)=PU_A(t,s)-U_h(t,s)P$.  The same calculation with
$F(\tau)=U_B(t,\tau)U_{FP}(\tau,s)$ gives the second identity with the
displayed sign.  Taking operator norms and inserting the two decay kernels
proves (7.4).  The integrability/domain hypotheses justify differentiation
and the Bochner integrals; no commutation is used. $\square$

### Theorem 7.2 (independent energy estimate)

Under the Sections 5--6 hypotheses and a matched homogeneous admissible
boundary condition, every strong error solution satisfies

$$
\begin{aligned}
\frac12\frac d{dt}\|e\|_\rho^2
&+\beta(t)\|e\|_\rho^2
+\frac12(\|e_+\|_{\Gamma_+}^2-
          \|\mathcal Be_+\|_{\Gamma_-}^2)\\
&+d_0\|(-\Delta_{S^2})^{1/2}e\|_\rho^2
\le\left\|\sum_{j=1}^6R_j\right\|_\rho\|e\|_\rho. \tag{7.5}
\end{aligned}
$$

Consequently the norm bound (7.2) holds without a streaming--diffusion
commutation hypothesis.

#### Proof

Taking the real part of (6.4) against $e$ and using (5.3)--(5.5) gives
(7.5).

For $e\ne0$, division by $\|e\|$ gives
$d\|e\|/dt+\beta\|e\|\le\|\sum_jR_j\|$; the upper
Dini derivative supplies the same conclusion at zero.  Integrating yields
(7.2), and the triangle inequality produces the six displayed contributions.
For unmatched inflow $b$, the squared energy estimate instead adds
$\|b\|_{\Gamma_-}^2/2$ on the right; a stable lift is needed for a linear
norm estimate. $\square$

### Proposition 7.3 (streaming and angular diffusion do not commute)

For smooth $v$,

$$
[\Delta_{S^2},\Omega\cdot\nabla_x]v
=-2\Omega\cdot\nabla_xv
+2\sum_j\nabla_{S^2}\Omega_j\cdot
\nabla_{S^2}\partial_{x_j}v,                          \tag{7.6}
$$

which is generally nonzero.  Neither proof replaces
$e^{-t(T+C)}$ by $e^{-tT}e^{-tC}$.  A separate splitting theorem would require
commutator-domain control such as $D(TC)\cap D(CT)$; none is needed for
(7.1) or (7.5).

#### Proof

Write $\Omega\cdot\nabla_xv=\sum_j\Omega_j\partial_{x_j}v$ and use the
spherical product rule
$\Delta(fg)=f\Delta g+g\Delta f+2\nabla f\cdot\nabla g$ together with
$\Delta_{S^2}\Omega_j=-2\Omega_j$.  Subtract
$\Omega\cdot\nabla_x\Delta_{S^2}v$; the terms containing
$\Omega_j\Delta_{S^2}\partial_{x_j}v$ cancel and (7.6) remains. $\square$

## 8. Steady problems, resolvents, and preconditioners

### Theorem 8.1 (steady residual and comparator identities)

Suppose $A_B$ is onto and

$$
\operatorname{Re}(A_Bv,v)_\rho\ge\beta_B\|v\|_\rho^2,
\qquad \beta_B>0.                                    \tag{8.1}
$$

Then $\|A_B^{-1}\|\le1/\beta_B$ and a steady version of (6.4) satisfies

$$
e=A_B^{-1}\sum_{j=1}^6R_j,\qquad
\boxed{\|e\|_\rho\le\frac1{\beta_B}
\sum_{j=1}^6\|R_j\|_\rho.}                          \tag{8.2}
$$

If coercivity is unavailable, it may be replaced only by a declared inf-sup
constant
$\mu=\inf_{v\ne0}\|A_Bv\|/\|v\|>0$ together with surjectivity, giving
$\|A_B^{-1}\|\le1/\mu$.  Time contraction with $\beta=0$ does not imply a
steady inverse; the angular constants in $\ker L$ are the elementary
counterexample.

For the following comparator identities, assume in addition that
$P\in\mathcal B(H,H_h)$, $P D(A)\subset D(A_h)$, and
$C_P=PA-A_hP$ extends to a bounded map between the declared Hilbert spaces.
Equivalently, for point sampling one may work on a declared resolvent-invariant
regularity space $X\subset D(P)$, provided every composition below is bounded
there and the corresponding $X$-resolvent constants replace the $H$ ones.
Then, for two invertible operators,

$$
\begin{aligned}
A_h^{-1}P-PA^{-1}
&=A_h^{-1}(PA-A_hP)A^{-1},\\
(\alpha+A_h)^{-1}P-P(\alpha+A)^{-1}
&=(\alpha+A_h)^{-1}(PA-A_hP)(\alpha+A)^{-1}.          \tag{8.3}
\end{aligned}
$$

Assume the shifted operators are onto and
$\alpha+\beta_h>0$, $\alpha+\beta>0$.  Under coercivities
$\beta_h,\beta$, the second norm is at most

$$
\frac{\|C_P\|}{(\alpha+\beta_h)(\alpha+\beta)}.      \tag{8.4}
$$

#### Proof

Coercivity and Cauchy--Schwarz give
$\beta_B\|v\|^2\le\operatorname{Re}(A_Bv,v)
\le\|A_Bv\|\|v\|$, hence the onto inverse has norm at most
$1/\beta_B$.  The steady form of (6.4) then gives (8.2).  The inf-sup
alternative is the same argument with $\|A_Bv\|\ge\mu\|v\|$.
Multiplication of the first identity in (8.3) on the left by $A_h$ and on the
right by $A$ reduces both sides to $PA-A_hP$; the shifted identity is
identical.  Applying the coercive shifted-resolvent bounds
$\|(\alpha+A_h)^{-1}\|\le(\alpha+\beta_h)^{-1}$ and
$\|(\alpha+A)^{-1}\|\le(\alpha+\beta)^{-1}$ proves (8.4). $\square$

### Theorem 8.2 (preconditioned and iterative estimates)

Let $B$ be invertible in a declared induced norm $X$ and

$$
q=\|I-B^{-1}A_h\|_X<1.                               \tag{8.5}
$$

Then

$$
(B^{-1}A_h)^{-1}=\sum_{n=0}^\infty(I-B^{-1}A_h)^n,
$$

and every iterate $\Psi^m$ satisfies

$$
\|\psi_h-\Psi^m\|_X
\le\frac{\|B^{-1}(f_h-A_h\Psi^m)\|_X}{1-q}.          \tag{8.6}
$$

If $c_B\|v\|_{\rm phys}\le\|v\|_X\le
C_B\|v\|_{\rm phys}$, multiply the physical estimate by $C_B/c_B$.
For $B=A_0$ and
$\delta=\|A_0^{-1}(A_h-A_0)\|<1$,

$$
\|A_h^{-1}\|\le\frac{\|A_0^{-1}\|}{1-\delta}.       \tag{8.7}
$$

For a nonnormal Krylov solve without (8.5), use a certified lower singular or
inf-sup constant $\mu_p$ of $B^{-1}A_h$:
$\|e\|\le\|B^{-1}r\|/\mu_p$.  Eigenvalue clustering or spectral radius alone
is not a residual certificate for a nonnormal transport matrix.

#### Proof

Put $N=I-B^{-1}A_h$.  Since $\|N\|_X=q<1$,
$(B^{-1}A_h)^{-1}=(I-N)^{-1}=\sum_{n\ge0}N^n$ in operator norm.  For
$r_m=f_h-A_h\Psi^m$,
$\psi_h-\Psi^m=(B^{-1}A_h)^{-1}B^{-1}r_m$; summing the geometric series gives
(8.6).  Norm equivalence yields the factor $C_B/c_B$.  Finally,
$A_h=A_0[I+A_0^{-1}(A_h-A_0)]$ and a second Neumann series proves (8.7).
The lower-inf-sup alternative follows directly from
$\|B^{-1}A_he\|\ge\mu_p\|e\|$. $\square$

## 9. Multigroup Boltzmann--Fokker--Planck systems

Let $H_\eta=\bigoplus_{g=1}^GH_g$ with
$\|v\|_\eta^2=\sum_g\eta_g\|v_g\|_g^2$, $\eta_g>0$, and write

$$
A=D-K,\qquad D=\operatorname{diag}(A_1,\ldots,A_G),
\qquad \operatorname{Re}(A_gv,v)\ge\beta_g\|v\|^2. \tag{9.1}
$$

Put

$$
c_{gg'}=\sqrt{\frac{\eta_g}{\eta_{g'}}}\|K_{gg'}\|,
\qquad C=(c_{gg'}),
\qquad
\beta_M=\lambda_{\min}\!\left(
\operatorname{diag}(\beta_g)-\frac{C+C^T}{2}\right). \tag{9.2}
$$

### Theorem 9.1 (block stability and residual bound)

If $\beta_M>0$, then

$$
\operatorname{Re}(Av,v)_\eta\ge\beta_M\|v\|_\eta^2. \tag{9.3}
$$

If $A$ also satisfies the generation hypothesis of Sections 4--5, the
generic evolution, energy, residual, and adjoint estimates of Sections 7--10
hold with kernel $e^{-\beta_M(t-s)}$.  If $A$ is additionally onto, the
steady residual estimate holds with inverse constant $1/\beta_M$.  This does
not transfer the sharp
self-adjoint harmonic multipliers of Sections 2--3 to a generally
nonsymmetric multigroup block operator.  Moreover

$$
\|R_j\|_\eta^2=\sum_g\eta_g\|R_{j,g}\|_g^2.          \tag{9.4}
$$

#### Proof

With $y_g=\sqrt{\eta_g}\|v_g\|$, the transfer term is bounded by
$y^TCy$, whose real part is $y^T(C+C^T)y/2$.  Subtraction from the diagonal
coercivity proves (9.3); Sections 7--8 then apply in the product space.
$\square$

For strictly downscattering triangular $K$, smallness is unnecessary for a
steady inverse provided every $A_g$ is onto and invertible and
$\beta_0=\min_g\beta_g>0$.  If $N=D^{-1}K$ and $N^G=0$, then

$$
A^{-1}=\sum_{j=0}^{G-1}N^jD^{-1},\qquad
\|A^{-1}\|_\eta
\le\frac1{\beta_0}\sum_{j=0}^{G-1}\|N\|_\eta^j,
\quad\beta_0=\min_g\beta_g.                           \tag{9.5}
$$

This finite bound may be large and does not by itself imply transient
contraction.  The energy residual $R_5$ includes the finite-volume
slowing-down flux defect and the discrepancy between discrete and exact
group-integrated transfer kernels.

## 10. Adjoint-weighted linear responses

Let the reported discrete response be $\mathcal R_h(\Psi)$ and define its
quadrature/reconstruction discrepancy

$$
\delta\mathcal R_q=(q,J\Psi)_\rho-\mathcal R_h(\Psi). \tag{10.1}
$$

### Theorem 10.1 (steady response identity and computable estimator)

Let $q\in H_\rho$ and let $z\in D(A_B^*)$ solve $A_B^*z=q$ with the dual
transport boundary condition.  For vacuum
primal inflow this is $z|_{\Gamma_+}=0$; periodic faces are paired in the
reverse direction; specular reflection uses the same measure-preserving
reflection; and for primal albedo $v_-=\mathcal Bv_+$ it is
$z_+=\mathcal B^*z_-$ under the flux-weighted trace pairing.
Then

$$
\boxed{
\mathcal R(\psi_B)-\mathcal R_h(\Psi)
=\delta\mathcal R_q+
\sum_{j=1}^6(z,R_j)_\rho.}                            \tag{10.2}
$$

For a computable enriched adjoint $\widetilde z\in D(A_B^*)$ satisfying the
same dual boundary condition, put
$\rho_z=q-A_B^*\widetilde z$.  If
$C_{\rm st}\ge\|A_B^{-1}\|$, then

$$
\begin{aligned}
\mathcal R(\psi_B)-\mathcal R_h(\Psi)
={}&\delta\mathcal R_q+
\sum_j(\widetilde z,R_j)_\rho+(\rho_z,e)_\rho,\\
|\mathcal R(\psi_B)-\mathcal R_h(\Psi)|
\le{}&|\delta\mathcal R_q|
+\sum_j| (\widetilde z,R_j)_\rho|
+C_{\rm st}\|\rho_z\|_\rho\sum_j\|R_j\|_\rho.     \tag{10.3}
\end{aligned}
$$

The signed contributions in the first line are retained as effectivity
diagnostics; the second line is the certified absolute estimator.

#### Proof

By (6.4) in steady form, $A_Be=\sum_jR_j$.  Therefore
$(q,e)=(A_B^*z,e)=(z,A_Be)=\sum_j(z,R_j)$; adding the direct response
discrepancy (10.1) proves (10.2).  For $\widetilde z$, write
$q=A_B^*\widetilde z+\rho_z$ and repeat the pairing.  Cauchy--Schwarz and
(8.2) bound the remainder by
$C_{\rm st}\|\rho_z\|\sum_j\|R_j\|$, proving (10.3).  The dual boundary
condition is exactly what cancels the transport boundary pairing. $\square$

### Theorem 10.2 (transient response identity)

Let $q\in L^1(0,T;H_\rho)$ and $q_T\in H_\rho$.  For

$$
\mathcal J(\chi)=(q_T,\chi(T))_\rho+
\int_0^T(q(t),\chi(t))_\rho\,dt,\qquad
\delta\mathcal J_q=\mathcal J(v)-\mathcal J_h(\Psi), \tag{10.4}
$$

let $-z_t+A_B^*z=q$, $z(T)=q_T$, in the backward form-solution class
generated by the adjoint evolution family.  Then

$$
\mathcal J(\psi_B)-\mathcal J_h(\Psi)
=\delta\mathcal J_q+(z(0),e(0))_\rho+
\sum_j\int_0^T(z,R_j)_\rho\,dt.                    \tag{10.5}
$$

For an approximate adjoint
$\widetilde z\in W^{1,1}(0,T;H_\rho)$ with terminal trace,
$\widetilde z(t)\in D(A_B^*)$ a.e., and
$A_B^*\widetilde z\in L^1(0,T;H_\rho)$, set
$\rho_z=q+\widetilde z_t-A_B^*\widetilde z$ and
$\delta_T=q_T-\widetilde z(T)$.  With

$$
B_e(t)=K_B(t,0)\|e(0)\|+
\sum_j\int_0^tK_B(t,s)\|R_j(s)\|\,ds,               \tag{10.6}
$$

the computable signed estimator is

$$
\delta\mathcal J_q+(\widetilde z(0),e(0))_\rho
+\sum_j\int_0^T(\widetilde z,R_j)_\rho\,dt,
$$

and its remainder is bounded by

$$
\|\delta_T\|B_e(T)+
\int_0^T\|\rho_z(t)\|B_e(t)\,dt.                    \tag{10.7}
$$

A point detector is not an $H_\rho$ response.  It requires a declared
$V$--$V'$ regularity and stability theorem; otherwise (10.2)--(10.7) apply
only to bounded linear responses.

#### Proof

For the exact adjoint and error equation (6.4), the product rule gives

$$
\frac d{dt}(z,e)_\rho=-(q,e)_\rho+
\sum_j(z,R_j)_\rho.
$$

Integrating from $0$ to $T$, using $z(T)=q_T$, and adding the direct
discrepancy $\delta\mathcal J_q$ proves (10.5).  For
$\widetilde z$, substitute
$q=\rho_z-\widetilde z_t+A_B^*\widetilde z$ and integrate the two derivative
terms by parts.  This yields

$$
\mathcal J(\psi_B)-\mathcal J_h(\Psi)
=\delta\mathcal J_q+(\widetilde z(0),e(0))
+\sum_j\int_0^T(\widetilde z,R_j)
+(\delta_T,e(T))+\int_0^T(\rho_z,e).
$$

Finally apply Cauchy--Schwarz and the primal bound
$\|e(t)\|\le B_e(t)$ to the last two terms, giving (10.7). $\square$

## 11. When the quadratic harmonic defect predicts transport error

Let $\Pi_\ell$ denote a continuum shell and define the *bare-generator*
intertwining defect

$$
E_L=L_hP-P\Delta_{S^2},\qquad
\mathfrak D_\ell
=\sup_{\substack{v_\ell\in\operatorname{ran}\Pi_\ell\\Pv_\ell\ne0}}
\frac{\|E_Lv_\ell\|_w}{\|Pv_\ell\|_w}.             \tag{11.1}
$$

This is exactly the accepted sampled quotient normalization and contains no
physical diffusion coefficient.  For matched angle-independent diffusion
$A_\Omega=-d\Delta_{S^2}$, $A_{\Omega,h}=-dL_h$, the residual is
$R_{2,\ell}=-dJE_Lv_\ell$.  Consequently, for
$v=\sum_\ell v_\ell$,

$$
\|R_{2,\ell}\|\le
\|J\|\,d_{\max}\mathfrak D_\ell\|Pv_\ell\|.        \tag{11.2}
$$

The quantity
$p_\ell=d_{\max}\|J\|\mathfrak D_\ell\|Pv_\ell\|$
is an upper-budget indicator, not an estimate of the realized shell error.
Its saturation factor is

$$
\theta_\ell(v)=
\frac{\|E_Lv_\ell\|}
{\mathfrak D_\ell\|Pv_\ell\|}\in[0,1]              \tag{11.3}
$$

when the denominator is nonzero.  A two-sided norm prediction requires a
declared lower observability or singular-value bound on $\theta_\ell$ and
control of cancellation under the transport evolution.  For a steady
response the signed aligned contribution is

$$
\zeta_\ell=(z,-dJE_Lv_\ell)_\rho,                    \tag{11.4}
$$

with the corresponding time integral in the transient case.

Let $E_{\mathcal R}=\mathcal R(\psi_B)-\mathcal R_h(\Psi)$ denote the exact
response error from (10.2) or (10.5).  For $\zeta_2\ne0$, the precise
relative criterion for degree-two predictivity, with $0\le\varepsilon<1$,
is

$$
|E_{\mathcal R}-\zeta_2|\le\varepsilon|\zeta_2|.     \tag{11.5}
$$

The left side includes response quadrature, every nonquadrupole and
nonangular residual, initial/terminal terms in the transient case, and the
adjoint remainder when an approximate adjoint is used.  Equations (10.3)
and (10.7) give a computable upper bound for that remainder.  Thus (11.5)
captures both source alignment and sign/time cancellation; a comparison of
instantaneous residual norms alone does not.

$\mathfrak D_2$ is quantitatively predictive only when:

1. the degree-two sampling quotient is stable;
2. the solution or source has appreciable degree-two content;
3. the realized saturation factor $\theta_2$ is controlled away from zero
   whenever a two-sided norm prediction is claimed;
4. the adjoint sees the degree-two residual for the requested response; and
5. (11.5), or its certified remainder bound, controls other shells,
   nonangular errors, and streaming-induced time/sign cancellation.

It is not predictive when $v_2\approx0$, when
$\mathfrak D_\ell\|Pv_\ell\|$ for higher $\ell$ dominates, when cross-shell
aliases are unresolved, when the adjoint is nearly orthogonal to $R_{2,2}$,
or when $R_1,R_3,R_4,R_5,R_6$ dominate.  Streaming couples neighboring
harmonic degrees, as (7.6) already warns.  Thus $\mathfrak D_2$ is a
worst-shell operator datum and upper-budget factor, not a standalone
physical-error predictor.

## 12. Exact manufactured examples and effectivity

### 12.1 Pure angular shell and resolvent

At the two nodes $(1,0,0)$ and $(0,1,0)$ with a common positive mass, take

$$
L=3\begin{pmatrix}-1&1\\1&-1\end{pmatrix},\qquad
v_1=(1,-1)^T,\qquad v_0=(1,1)^T.                      \tag{12.1}
$$

These are samples of two trace-free quadratics:
$v_1=S(x^2-y^2)$ and $v_0=-S(3z^2-1)$.  With
$\lambda_2=6$,

$$
Lv_1=-6v_1,\qquad Lv_0=0,\qquad
(L+6I)v_1=0,\qquad(L+6I)v_0=6v_0.                  \tag{12.2}
$$

For $v_0$ the exact transient error and bound are equal:

$$
\|e^{tL}v_0-e^{-6t}v_0\|_w
=(1-e^{-6t})\|v_0\|_w
=\frac{1-e^{-6t}}6\,\|6v_0\|_w.                     \tag{12.3}
$$

For every $t>0$ the effectivity index bound/error is exactly $1$.  At
$\alpha=2$,

$$
\left\|(2-L)^{-1}v_0-\frac{v_0}{8}\right\|_w
=\frac38\|v_0\|_w
=\frac{\|6v_0\|_w}{2\cdot8},                         \tag{12.4}
$$

again with effectivity $1$.  The $v_1$ error and residual are both zero.  This
single shell therefore demonstrates both exactness and worst-case alignment;
it also rejects the claim that continuum mean-zero harmonics must sample to
the discrete mean-zero subspace.

The accepted coordinate-exact comparison uses the regular tetrahedron with
$w_i=1/4$, complete support, and $\gamma_{ij}=1/8$.  On its genuinely sampled
degree-two quotient, $L=-2I$, $\mathfrak D_2=4$, and for every weighted-unit
sampled quadrupole

$$
\begin{aligned}
E_{\rm tr}(t)&=e^{-2t}-e^{-6t},
&B_{\rm tr}(t)&=\frac23(1-e^{-6t}),
&I_{\rm tr}(t)&=\frac{2(1-e^{-6t})}{3(e^{-2t}-e^{-6t})},\\
E_{\rm res}(\alpha)&=\frac4{(\alpha+2)(\alpha+6)},
&B_{\rm res}(\alpha)&=\frac4{\alpha(\alpha+6)},
&I_{\rm res}(\alpha)&=\frac{\alpha+2}{\alpha}.
\end{aligned}                                                  \tag{12.4a}
$$

The deterministic numerical audit uses $t=0.4$ and $\alpha=1.25$ and reports
$I_{\rm tr}=1.6903776315765708$ and $I_{\rm res}=2.6$.  The sharp alias case
reports $I_{\rm tr}=I_{\rm res}=1$.  Thus the theorem is sharp on the full
conservative space while the coordinate-exact tetrahedral shell correctly
benefits from its nonzero spectral gap.

### 12.2 Noncommuting spatial manufactured system

The executable exact audit uses two upwind cells and directions $\mu=\pm1$.
In cell coordinates,

$$
D_+=\begin{pmatrix}1&0\\-1&1\end{pmatrix},\qquad
D_-=\begin{pmatrix}1&-1\\0&1\end{pmatrix},\qquad
L_a=\begin{pmatrix}-a&a\\a&-a\end{pmatrix}.           \tag{12.5}
$$

The streaming matrix $S=\operatorname{diag}(D_+,D_-)$ is permuted into
cell--angle ordering, while the angular operator is
$I_{\rm cell}\otimes L_a$.  The audit verifies exactly that their commutator
is nonzero.  For rational $a,b,\sigma>0$, define

$$
A_*=S+\sigma I-I\otimes L_b,\qquad
A_h=S+\sigma I-I\otimes L_a,                          \tag{12.6}
$$

choose a declared rational $\psi_*$, and set $f=A_*\psi_*$.  The numerical
solution is $\psi_h=A_h^{-1}f$ and $e=\psi_*-\psi_h$.  The residual in the
six-way theorem is evaluated at the reconstructed computed state:

$$
r_*=(A_h-A_*)\psi_h=A_*e.                            \tag{12.7}
$$

The reverse comparator
$r_h=(A_h-A_*)\psi_*=A_he$ is retained separately for the discrete
preconditioner test; it is not relabeled as $R_2$.  Every entry, norm square,
symmetric-part eigenvalue/coercivity
certificate, residual contribution, adjoint response, and effectivity ratio
is reconstructed over the rationals or an explicitly declared algebraic
extension.  The retained parameters are

$$
a=1,\qquad b=2,\qquad\sigma=1,\qquad
\psi_*=(1,2,3,4)^T,
$$

for which

$$
\begin{aligned}
f&=(0,2,3,10)^T,
&\psi_h&=(7/9,7/3,8/3,38/9)^T,\\
e&=(2/9,-1/3,1/3,-2/9)^T,
&r_*&=\frac{14}{9}(1,-1,1,-1)^T,\\
&&r_h&=(1,-1,1,-1)^T.
\end{aligned}                                                  \tag{12.7a}
$$

The symmetric part of the truth operator $A_*$ has exact eigenvalues
$3/2,5/2,11/2,13/2$.  Consequently the theorem-oriented bound is

$$
\|e\|^2=\frac{26}{81},\qquad
\frac{\|r_*\|}{3/2}=\frac{56}{27},
\qquad I_{\rm eff}^{\rm energy}=\frac{28\sqrt{26}}{39}
=3.6608345225794348\ldots.                            \tag{12.7b}
$$

For $q=(1,-1,2,-2)^T$,

$$
z_*=A_*^{-*}q=(19/70,-4/35,11/35,-13/35)^T,
\qquad q^Te=z_*^Tr_*=\frac53,                        \tag{12.7c}
$$

so the exact adjoint estimator has effectivity $1$.  The separately labelled
reverse comparator uses
$z_h=A_h^{-*}q=(3/7,-4/21,10/21,-4/7)^T$ and also gives
$z_h^Tr_h=5/3$.  A commuting mutation and a dropped-residual mutation are
required to fail.

Numerical effectivity is always reported as

$$
I_{\rm eff}=\frac{\text{certified upper estimator}}
{\text{exact nonzero error}},                         \tag{12.8}
$$

so a valid upper bound has $I_{\rm eff}\ge1$.  Signed adjoint sums are also
reported separately because cancellation can make the norm estimator
conservative.

### 12.3 Exact two-group amplitude fixture

For one angular eigenmode with actual decay $\eta$, high-to-low transfer
rate $a$, and group diffusion strengths $\kappa_1,\kappa_2$, the amplitudes
obey

$$
y_1'=-(a+\kappa_1\eta)y_1,\qquad
y_2'=ay_1-\kappa_2\eta y_2,\qquad y(0)=(1,0)^T.       \tag{12.9}
$$

The exact solution is

$$
y_1(t)=e^{-(a+\kappa_1\eta)t},\qquad
y_2(t)=
\begin{cases}
\displaystyle
a\frac{e^{-(a+\kappa_1\eta)t}-e^{-\kappa_2\eta t}}
{\kappa_2\eta-(a+\kappa_1\eta)},
&\kappa_2\eta\ne a+\kappa_1\eta,\\[8pt]
at\,e^{-(a+\kappa_1\eta)t},
&\kappa_2\eta=a+\kappa_1\eta.
\end{cases}                                           \tag{12.10}
$$

At $a=1$, $(\kappa_1,\kappa_2)=(2,1)$, and $t=\log2$, the discrete
$\eta=1$ and target $\eta=2$ values are

$$
y_h=(1/8,3/16)^T,\qquad
y_*=(1/32,7/96)^T,\qquad
y_h-y_*=(3/32,11/96)^T.                              \tag{12.11}
$$

Thus the exact low-group response error is $11/96$.  If $G$ is the group
transfer generator and $K=\operatorname{diag}(\kappa_g)$, the audit checks

$$
[G\otimes I,K\otimes L]_{hg}
=G_{hg}(\kappa_g-\kappa_h)L.                         \tag{12.12}
$$

It has rank one for the retained unequal-$\kappa$ example and vanishes
exactly under the equal-$\kappa$ mutation.  An independent group-rate mutation
$a_h=2$ gives $(1/16,7/24)^T$ and the pure group error
$(-1/16,5/48)^T$.

## 13. Solver-independent reproducibility contract

The implementation accompanying this theorem must:

- validate positivity, reversibility, shapes, and finiteness before using an
  angular generator;
- remove sampling kernels and retain full-output shell residuals;
- reject ambiguous cross-shell sampling instead of silently selecting a
  continuum evolution;
- verify dissipativity of a proposed physical symmetrizer;
- recompute Duhamel and resolvent identities independently of a solver;
- expose every term $R_1,\ldots,R_6$ in the original physical scaling;
- distinguish exact/algebraic or outward interval certificates from ordinary
  floating diagnostics;
- report coercivity/inf-sup, reconstruction, quadrature, residual-integration,
  and preconditioner constants;
- retain exact manufactured truth, exact errors, bounds, effectivities, and
  deliberate failed mutations.

The source--test--claim map identifies one proof source, one executable or
formal test source, and one registry row for every displayed theorem.
Commit hashes, CI run identifiers, and artifact digests are reproducibility
records, never premises of the mathematics.

## 14. Limitations and claim boundary

The estimates are conditional on the displayed stability, boundary,
regularity, sampling, reconstruction, and residual-integration hypotheses.
They do not prove that the Fokker--Planck approximation is physically adequate
for a given scattering kernel; that is $R_1$.  They do not turn point sampling
into a bounded $L^2$ operation, guarantee a steady inverse without absorption
or inf-sup stability, control a nonnormal operator from eigenvalues alone,
or infer a response improvement from $\mathfrak D_2$ without source and
adjoint alignment.  Nuclear data, material interfaces, spatial closure,
slowing-down physics, and nonlinear feedback remain outside the angular
generator theorem and enter only through declared model and residual terms.

These are boundaries of the result, not hidden lemmas needed for the stated
theorems.

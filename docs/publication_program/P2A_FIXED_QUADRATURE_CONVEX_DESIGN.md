# P2A: kernel-correct convex design on a fixed spherical quadrature

Status: **PROVED AND IMPLEMENTED** on the exact descendant of the accepted
Paper-I archive.  This document fixes the mathematical program.  The Python
package, exact fixtures, formal finite core, and release workflow named in
Section 12 are part of the theorem package; solver output is never used as a
substitute for a proof or certificate.

## 1. Scope and conventions

Let

\[
 X=\{\Omega_i\}_{i=1}^N\subset \mathbb S^2,
 \qquad w_i>0,
 \qquad \sum_iw_i=1,
\]

and let `E` be a fixed simple undirected permitted graph.  Every edge is
oriented once for assembly only.  If `e={i,j}` is oriented from `i` to `j`,
write

\[
 b_e=e_i-e_j,\qquad
 B=(b_e)_{e\in E},\qquad
 C=|B|,
 \qquad W=\operatorname{diag}(w_1,\ldots,w_N).
\]

The design variables are the shared conductances
`gamma=(gamma_e)_{e in E}`.  Define

\[
 K(\gamma)=B\operatorname{Diag}(\gamma)B^{\mathsf T},
 \qquad
 L_\gamma=-W^{-1}K(\gamma).
 \tag{1.1}
\]

Thus, for `e={i,j}`,

\[
 (L_\gamma f)_i
 =\frac1{w_i}\sum_{j:\{i,j\}\in E}\gamma_{ij}(f_j-f_i).
 \tag{1.2}
\]

This is the negative-semidefinite Markov convention of Paper I.  The
directed rate and maximum rate are

\[
 r_i(\gamma)=\frac{(C\gamma)_i}{w_i},
 \qquad r_{\max}(\gamma)=\max_i r_i(\gamma).
 \tag{1.3}
\]

All harmonic eigenvalues below are positive numbers

\[
 \lambda_\ell=\ell(\ell+1),
\]

so the continuous target equation is `L H_l=-lambda_l H_l`.  In particular,
the coordinate target on `S^2` is `-2` and the quadratic target is `-6`.

## 2. The global shared-conductance affine system

For `e={i,j}`, let the `3N`-vector `mathcal A_e` have only two nonzero
three-vector blocks,

\[
 (\mathcal A_e)_i=\Omega_j-\Omega_i,
 \qquad
 (\mathcal A_e)_j=\Omega_i-\Omega_j.
 \tag{2.1}
\]

Let `mathcal A` have these columns and set

\[
 b_i=-2w_i\Omega_i.
 \tag{2.2}
\]

Then

\[
 \boxed{L_\gamma\Omega=-2\Omega
 \quad\Longleftrightarrow\quad
 \mathcal A\gamma=b.}
 \tag{2.3}
\]

Equivalently,

\[
 \mathcal A_e=-\operatorname{vec}
 \bigl(b_eb_e^{\mathsf T}\Omega\bigr).
\]

### Theorem 2.1 (automatic structure)

If `gamma>=0` and `mathcal A gamma=b`, then

\[
 L_\gamma\mathbf 1=0,
 \qquad
 WL_\gamma=L_\gamma^{\mathsf T}W=-K(\gamma),
 \qquad
 L_\gamma\Omega=-2\Omega.
 \tag{2.4}
\]

The off-diagonal rates are nonnegative and `L_gamma` is negative
semidefinite in `ell^2(w)`.

**Proof.**  Incidence columns sum to zero, so `K(gamma)1=0`.  The matrix
`K(gamma)` is symmetric and positive semidefinite when `gamma>=0`, which
gives the first two claims and the sign statement.  Equation (2.3) gives the
coordinate identity.  No local-to-global inference is used.  `square`

The fixed rate cap is the linear system

\[
 C\gamma\le Rw.
 \tag{2.5}
\]

In particular the base feasible set

\[
 \mathcal F_R
 =\{\gamma:\mathcal A\gamma=b,\ \gamma\ge0,\ C\gamma\le Rw\}
 \tag{2.6}
\]

is a closed convex polyhedron.  It may be empty even when every row admits a
strictly positive local stencil.

## 3. Exact removal of sampling aliases

Let `S_l` be the sampling matrix of a fixed real basis of `H_l(S^2)`.
For degrees other than two the implementation uses its declared
spherical-`L^2`-orthonormal real harmonic convention.  For `ell=2` the
convention is instead the Paper-I Frobenius-orthonormal basis of trace-free
symmetric `3`-by-`3` matrices, sampled by
`A -> (Omega_i^T A Omega_i)_i`.  The subsequent quotient whitening makes
the construction invariant under either basis normalization.  The columns
span the sampled shell, but `S_l` need not be injective.  Choose a
matrix `U_l` with Euclidean-orthonormal columns spanning

\[
 (\ker S_\ell)^{\perp}.
\]

Set

\[
 G_\ell
 =U_\ell^{\mathsf T}S_\ell^{\mathsf T}WS_\ell U_\ell>0,
 \qquad
 V_\ell=S_\ell U_\ell G_\ell^{-1/2}.
 \tag{3.1}
\]

Then

\[
 V_\ell^{\mathsf T}WV_\ell=I.
 \tag{3.2}
\]

The columns of `V_l` are therefore a `W`-orthonormal basis of
`im S_l`.  Define

\[
\boxed{
 T_\ell(\gamma)
 =W^{1/2}(L_\gamma+\lambda_\ell I)V_\ell.}
 \tag{3.3}
\]

Equivalently, before choosing a basis define the sampled-shell quotient
defect by

\[
 \mathfrak D_\ell(L_\gamma)
 =\sup_{a\notin\ker S_\ell}
 \frac{\|(L_\gamma+\lambda_\ell I)S_\ell a\|_W}
      {\|S_\ell a\|_W}.
 \tag{3.3a}
\]

This quotient is well defined for every `gamma`: if `S_l a=0`, then
`(L_gamma+lambda_l I)S_l a=0` identically.

This matrix maps the sampled quotient into the **whole** weighted sample
space.  It is not compressed back into `im S_l`.

Using (1.1),

\[
 T_\ell(\gamma)
 =T_{\ell,0}+\sum_{e\in E}\gamma_eT_{\ell,e},
 \tag{3.4}
\]

where

\[
 T_{\ell,0}=\lambda_\ell W^{1/2}V_\ell,
 \qquad
 T_{\ell,e}=-W^{-1/2}b_eb_e^{\mathsf T}V_\ell.
 \tag{3.5}
\]

### Theorem 3.1 (kernel-correct norm identity)

For every conductance vector `gamma`,

\[
 \boxed{\mathfrak D_\ell(L_\gamma)=\|T_\ell(\gamma)\|_2.}
 \tag{3.6}
\]

For `ell=2`, `lambda_2=6` and (3.6) is exactly the Paper-I sampled
quadratic defect.

**Proof.**  Equation (3.2) identifies Euclidean coefficient vectors with
unit vectors in the sampled quotient equipped with its pulled-back
`ell^2(w)` metric.  Left multiplication by `W^{1/2}` identifies the output
with Euclidean `ell^2`.  The kernel implication follows directly from
linearity, as observed after (3.3a).  The induced map has matrix (3.3), hence
its operator norm is (3.6).  `square`

If `V_l` is replaced by another `W`-orthonormal basis, then
`V_l'=V_l O` for an orthogonal `O`, and `T_l'=T_l O`.  Therefore both the
spectral and Frobenius norms used below are basis independent.

Two implementation rules are part of the statement:

1. algebraic input uses an exact rank/nullspace calculation;
2. floating input uses an explicit rank policy whose guarded singular-value
   classification is separated from its ambiguity band.  An optional
   declared rank is accepted only when it satisfies the same two-sided
   separation guard.  An ambiguous rank raises a deterministic error.  No
   ridge, raw pseudoinverse, or undocumented tolerance is allowed.

The weighted SVD form is equivalent and often better conditioned.  If

\[
 W^{1/2}S_\ell=\widehat U_\ell\Sigma_\ell Q_\ell^{\mathsf T}
\]

is restricted to its certified nonzero singular values, then
`W^{1/2}V_l=widehat U_l` and

\[
 T_\ell(\gamma)
 =\left(-W^{-1/2}K(\gamma)W^{-1/2}
        +\lambda_\ell I\right)\widehat U_\ell.
 \tag{3.7}
\]

This avoids forming an ill-conditioned raw Gram inverse while retaining the
same exact quotient.

## 4. Seven convex design formulations

In this section write `T=T_2`, let `r=rank S_2`, and abbreviate

\[
 T(\gamma)=T_0+\sum_e\gamma_eT_e.
\]

### 4.1 Minimum quadratic defect at a fixed rate cap

The exact SDP is

\[
\begin{aligned}
 \text{minimize}\quad &t\\
 \text{over}\quad &\gamma\in\mathbb R^{|E|},\ t\in\mathbb R\\
 \text{subject to}\quad
 &\mathcal A\gamma=b,\quad \gamma\ge0,\quad C\gamma\le Rw,\\
 &\begin{bmatrix}
   tI_N&T(\gamma)\\ T(\gamma)^{\mathsf T}&tI_r
  \end{bmatrix}\succeq0.
\end{aligned}
 \tag{P-D(R)}
\]

The block LMI is equivalent to `||T(gamma)||_2<=t`.

### 4.2 Minimum rate cap at a fixed defect

For a prescribed `delta>0`, the exact SDP is

\[
\begin{aligned}
 \text{minimize}\quad &R\\
 \text{over}\quad &\gamma\in\mathbb R^{|E|},\ R\in\mathbb R\\
 \text{subject to}\quad
 &\mathcal A\gamma=b,\quad \gamma\ge0,\quad C\gamma\le Rw,\\
 &\begin{bmatrix}
   \delta I_N&T(\gamma)\\ T(\gamma)^{\mathsf T}&\delta I_r
  \end{bmatrix}\succeq0.
\end{aligned}
 \tag{P-R(delta)}
\]

The product `mathfrak D_2 r_max` is not asserted to be convex.  Programs
`P-D(R)` and `P-R(delta)` are the two convex epsilon-constraint slices of its
Pareto frontier.

### 4.3 Frobenius-shell residual

Let

\[
 h=\operatorname{vec}T_0,
 \qquad H_{:,e}=\operatorname{vec}T_e.
 \tag{4.1}
\]

Then

\[
 \text{minimize}\quad
 \frac12\|H\gamma+h\|_2^2
 \quad\text{over }\gamma\in\mathcal F_R
 \tag{P-F(R)}
\]

is a convex QP.  It minimizes the Hilbert--Schmidt norm of the quotient
map, not the unwhitened coefficient residual.  Its norm epigraph is an SOCP
alternative.

### 4.4 Minimax over selected physical or rotated modes

Let `u_k in R^r`, `||u_k||_2=1`, be fixed sampled-quotient coordinates.  A
physical coefficient `a_k` is admitted only if `S_2 a_k` is nonzero, and is
converted by

\[
 f_k=\frac{S_2a_k}{\|S_2a_k\|_W},
 \qquad u_k=V_2^{\mathsf T}Wf_k.
 \tag{4.2}
\]

Rotated matrices are normalized again in this sampled metric.  Define

\[
 h_k=T_0u_k,
 \qquad (H_k)_{:,e}=T_eu_k.
\]

The finite-mode minimax problem is the SOCP

\[
\begin{aligned}
 \text{minimize}\quad&t\\
 \text{subject to}\quad
 &\gamma\in\mathcal F_R,\\
 &\|H_k\gamma+h_k\|_2\le t,\qquad k=1,\ldots,K.
\end{aligned}
 \tag{P-SEL(R)}
\]

If only fixed scalar observations are retained, the absolute-value
epigraph is an LP.  A sum of squared selected-mode errors is a QP.  A finite
rotation list certifies that list only; it is not silently promoted to a
continuum rotation theorem.

### 4.5 Multi-shell objectives through degree `L`

Construct and deflate every shell separately before combining objectives.
For fixed weights `eta_l>0` (zero-weight shells are omitted),

\[
 \text{minimize}\quad
 \frac12\sum_{\ell=2}^L\eta_\ell
 \|T_\ell(\gamma)\|_F^2,
 \qquad \gamma\in\mathcal F_R,
 \tag{P-MS-F}
\]

is a QP after stacking `sqrt(eta_l) vec T_l`.  For fixed
`kappa_l>0`,

\[
 \text{minimize}\quad
 \max_{2\le\ell\le L}\kappa_\ell\|T_\ell(\gamma)\|_2,
 \qquad \gamma\in\mathcal F_R,
 \tag{P-MS-OP}
\]

is an SDP with one block LMI per shell.  Sampled images belonging to
different degrees are not merged: their target eigenvalues differ even if
the sampled subspaces intersect.

### 4.6 Fixed response-weighted objectives

Let fixed matrices `P_a,Q_a,D_a` define

\[
 E_a(\gamma)=P_aT_{\ell_a}(\gamma)Q_a-D_a.
 \tag{4.3}
\]

Then

- `(1/2) sum_a eta_a ||E_a||_F^2` is a QP;
- `max_a kappa_a ||E_a||_2` is an SDP;
- fixed vector-response norms give an SOCP;
- fixed scalar absolute responses give an LP.

All displayed response weights and norm scales `eta_a,kappa_a` are strictly
positive; zero-weight response terms are omitted.  This includes fixed
physical response weights and fixed linearized
sensitivity maps.  It does **not** include a `gamma`-dependent resolvent such
as `(zI-L_gamma)^{-1}`; that map is nonlinear and no convexity claim is made
for it.

### 4.7 Support pruning followed by exact reoptimization

For a fixed support `J subset E`, delete all columns outside `J` and solve
any program above.  This restriction is convex.  The outer choice of `J` is
combinatorial.

The implemented deterministic procedure is:

1. solve and independently verify at the reported certificate level on the
   current support;
2. order candidate edges by a fixed, recorded score and lexicographic
   tie break;
3. delete one edge;
4. re-solve the original exact constraints and objective;
5. retain the deletion only if primal and dual verification succeeds at that
   level;
6. otherwise save the rejection record and restore the edge; attach a
   Farkas or conic ray only when infeasibility was independently verified.

The result is a verified candidate on the returned support.  It is
proof-certified only after exact/algebraic reconstruction or genuine
outward interval enclosure, as in Section 7.  It is not a
minimum-cardinality theorem.

### Theorem 4.1 (convexity)

Every retained formulation in Sections 4.1--4.6, and every fixed-support
reoptimization in Section 4.7, is convex.

**Proof.**  Equations (3.4) and (4.3) are affine in `gamma`.  Squared
Frobenius objectives have positive-semidefinite Hessians.  Norms, maxima of
norms, and their epigraphs are convex.  All other constraints are affine,
second-order-cone, or positive-semidefinite-cone constraints.  A fixed
support is an affine coordinate face.  `square`

The spectral norm has a generic exact SDP epigraph.  It is an SOCP only in
special low-rank or simultaneously diagonal cases; no generic SOCP identity
is claimed.

## 5. Exact dual programs

Partition a positive-semidefinite dual matrix as

\[
 Z=\begin{bmatrix}Z_{11}&Z_{12}\\
 Z_{12}^{\mathsf T}&Z_{22}\end{bmatrix}\succeq0
\]

and define

\[
 \tau_e(Z)=2\langle T_e,Z_{12}\rangle_F,
 \qquad
 \tau_0(Z)=2\langle T_0,Z_{12}\rangle_F.
 \tag{5.1}
\]

The factor `2` is essential.

### 5.1 Dual of `P-D(R)`

\[
\begin{aligned}
 \text{maximize}\quad
 &-b^{\mathsf T}y-Rw^{\mathsf T}z-\tau_0(Z)\\
 \text{subject to}\quad
 &z\ge0,\quad Z\succeq0,\\
 &\operatorname{tr}Z_{11}+\operatorname{tr}Z_{22}=1,\\
 &\mathcal A^{\mathsf T}y+C^{\mathsf T}z-\tau(Z)\ge0.
\end{aligned}
 \tag{D-D(R)}
\]

### 5.2 Dual of `P-R(delta)`

\[
\begin{aligned}
 \text{maximize}\quad
 &-b^{\mathsf T}y
 -\delta\{\operatorname{tr}Z_{11}+\operatorname{tr}Z_{22}\}
 -\tau_0(Z)\\
 \text{subject to}\quad
 &z\ge0,\quad Z\succeq0,\\
 &w^{\mathsf T}z=1,\\
 &\mathcal A^{\mathsf T}y+C^{\mathsf T}z-\tau(Z)\ge0.
\end{aligned}
 \tag{D-R(delta)}
\]

### 5.3 Dual of `P-F(R)`

\[
\begin{aligned}
 \text{maximize}\quad
 &h^{\mathsf T}u-\frac12\|u\|_2^2
 -b^{\mathsf T}y-Rw^{\mathsf T}z\\
 \text{subject to}\quad
 &z\ge0,\\
 &H^{\mathsf T}u+\mathcal A^{\mathsf T}y+C^{\mathsf T}z\ge0.
\end{aligned}
 \tag{D-F(R)}
\]

At an optimum, `u=H gamma+h`.

### 5.4 Dual of `P-SEL(R)`

Let `Q_{N+1}` be the Lorentz cone.  The dual is

\[
\begin{aligned}
 \text{maximize}\quad
 &-b^{\mathsf T}y-Rw^{\mathsf T}z
 -\sum_kh_k^{\mathsf T}v_k\\
 \text{subject to}\quad
 &z\ge0,\qquad (\alpha_k,v_k)\in\mathcal Q_{N+1},\\
 &\sum_k\alpha_k=1,\\
 &\mathcal A^{\mathsf T}y+C^{\mathsf T}z
 -\sum_kH_k^{\mathsf T}v_k\ge0.
\end{aligned}
 \tag{D-SEL(R)}
\]

For scalar affine errors `a_k^T gamma+beta_k`, the LP dual can be written

\[
 \sum_k|s_k|\le1,
 \qquad
 \mathcal A^{\mathsf T}y+C^{\mathsf T}z+\sum_ks_ka_k\ge0,
\]

with objective

\[
 -b^{\mathsf T}y-Rw^{\mathsf T}z+\sum_k\beta_ks_k.
 \tag{5.2}
\]

### 5.5 Multi-shell and response duals

For `P-MS-F`, stack the matrices `sqrt(eta_l) H_l` and vectors
`sqrt(eta_l) h_l` in `D-F(R)`.  For `P-MS-OP`, use the primal blocks
`[[t I, kappa_l T_l], [kappa_l T_l^T, t I]]`, introduce one
`Z_l>=0` per shell, replace `tau` by the sum of the `kappa_l`-weighted
shell contributions, and impose

\[
 \sum_{\ell=2}^L
 \{\operatorname{tr}Z_{\ell,11}
   +\operatorname{tr}Z_{\ell,22}\}=1,
 \tag{5.3}
\]

when the primal epigraph is
`kappa_l ||T_l||_2<=t`.  Response-weighted duals are the same substitutions
after replacing `T_l` by the affine maps (4.3).  Selected vector and scalar
responses use `D-SEL(R)` and (5.2), respectively.

For reference, all these cases are instances of the following fixed-cone
master pair.  With self-dual cone signs encoded as
`F_j x+f_j in K_j`,

\[
\begin{aligned}
 \min_x\quad&c^{\mathsf T}x+\frac12\|Hx+h\|_2^2\\
 \text{s.t.}\quad&Ex=d,\qquad F_jx+f_j\in K_j
\end{aligned}
\]

has the exact Fenchel--conic dual

\[
\begin{aligned}
 \max_{u,y,z_j}\quad&
 h^{\mathsf T}u-\frac12\|u\|_2^2
 -d^{\mathsf T}y-\sum_j f_j^{\mathsf T}z_j\\
 \text{s.t.}\quad&z_j\in K_j^*,\\
 &c+H^{\mathsf T}u+E^{\mathsf T}y
   -\sum_jF_j^{\mathsf T}z_j=0.
\end{aligned}
 \tag{5.4}
\]

Deleting support columns gives the exact dual of every fixed-support
reoptimization.

## 6. Slater, strong duality, and complementary slackness

### Theorem 6.1 (sufficient strong-duality hypotheses)

For fixed `R`, a sufficient primal Slater point for the spectral,
multi-shell, response, and selected-mode epigraphs is an exact `gamma` with

\[
 \gamma_e>0\quad(e\in E),
 \qquad C\gamma<Rw,
 \tag{6.1}
\]

together with an epigraph variable strictly above every retained norm.  For
`P-R(delta)`, also require

\[
 \|T(\gamma)\|_2<\delta,
 \tag{6.2}
\]

and choose `R>r_max(gamma)`.

Under these hypotheses the corresponding primal and dual optima are
attained and equal.  More generally, if exactness forces any conductance,
rate-slack, PSD, or SOC coordinate into a proper cone face, first perform
facial reduction to the product cone's minimal face and apply relative
interior Slater there.  Deleting edges forced to zero is only the
conductance-coordinate instance of this general reduction.

**Proof.**  These are the relative-interior hypotheses of finite-dimensional
conic Slater duality; see Boyd and Vandenberghe,
[_Convex Optimization_, Sections 5.2 and 5.9](https://web.stanford.edu/~boyd/cvxbook/bv_cvxbook.pdf).
The norm epigraph becomes strictly positive definite
when its scalar is strictly larger than the norm.  The QP statement follows
from the same relative-interior condition and Fenchel duality.  Primal
attainment is also explicit here.  At fixed `R`, an edge `e={i,j}` satisfies

`0<=gamma_e<=(C gamma)_i<=R w_i`

(and likewise at `j`), so the feasible conductance set is compact.  In
`P-R(delta)`, after deleting zero-loss duplicate-node edges, Theorem 8.1
gives `0<=gamma_e<=sum_i w_i/ell_e`; the defect constraint is closed, and
the optimal `R` is the continuous function `r_max(gamma)` on this compact
set.  Thus every retained continuous primal objective attains its infimum;
Slater or minimal-face duality supplies the corresponding dual attainment
and equality.  `square`

Mere feasibility is not Slater.  If all exact points lie on any proper cone
face, any strong-duality claim based on Slater must be accompanied by an
independently exhibited primal or dual Slater point, or by an explicit
minimal-face reduction.  The implementation does not infer either from a
solver status.  Independently verified primal and dual feasible points with
matching certified objectives remain a separate optimality certificate and
do not require such an inference.

Let

\[
 q=\mathcal A^{\mathsf T}y+C^{\mathsf T}z-\tau(Z)\ge0.
\]

Complementary slackness for `P-D(R)` is

\[
 \gamma_eq_e=0,
 \qquad
 z_i\{Rw_i-(C\gamma)_i\}=0,
 \qquad
 \langle Z,M(t,\gamma)\rangle=0.
 \tag{6.3}
\]

For positive-semidefinite matrices, the last equality is equivalent to
`ZM=0`.  The SOCP condition is

\[
 \left\langle(\alpha_k,v_k),
 (t,H_k\gamma+h_k)\right\rangle=0.
 \tag{6.4}
\]

The QP additionally has `u=H gamma+h`, and scalar LP responses have the two
usual signed-slack products.

## 7. Solver-independent certificates

### 7.1 Linear Farkas certificates

The exact shared system `mathcal A gamma=b`, `gamma>=0` is infeasible if and
only if there exists `y` such that

\[
 \mathcal A^{\mathsf T}y\ge0,
 \qquad b^{\mathsf T}y<0.
 \tag{7.1}
\]

With a fixed rate cap, infeasibility is equivalent to a pair `(y,z)` with

\[
 z\ge0,
 \qquad
 \mathcal A^{\mathsf T}y+C^{\mathsf T}z\ge0,
 \qquad
 b^{\mathsf T}y+Rw^{\mathsf T}z<0.
 \tag{7.2}
\]

These signs follow by adding a nonnegative slack to `C gamma<=Rw`.

### 7.2 Conic infeasibility ray

For a fixed rate and fixed defect LMI, a sound infeasibility ray satisfies

\[
 z,q\ge0,\quad Z\succeq0,
 \quad
 \mathcal A^{\mathsf T}y+C^{\mathsf T}z-q-\tau(Z)=0,
 \tag{7.3}
\]

and

\[
 -b^{\mathsf T}y-Rw^{\mathsf T}z
 -\delta\operatorname{tr}Z-\tau_0(Z)>0.
 \tag{7.4}
\]

Substitution of any primal feasible point contradicts (7.4).  A normalized
rational ray or an outward-rounded interval ray is therefore independent of
the solver that suggested it.

### 7.3 Numerical optimality certificate

The verifier works in the original problem scaling and reports at least

- exactness residual `||mathcal A gamma-b||_inf`;
- minimum conductance;
- maximum rate-cap violation;
- minimum eigenvalue of every primal PSD slack;
- dual-cone and dual-stationarity residuals;
- complementarity residuals;
- a primal--dual objective bracket and gap;
- sampling orthonormality error;
- retained and discarded sampling singular values;
- nonzero-singular-value condition numbers of the sampling and exactness
  systems.

Primal feasibility, dual feasibility, and a certified gap imply an
objective bracket without trusting a solver status string.  Exact examples
use rational or algebraic reconstruction.  A floating report is explicitly
labeled tolerance-based; it becomes a proof certificate only after rational
or algebraic reconstruction, or after all displayed inequalities and cone
eigenvalue bounds are enclosed by outward intervals.  The implementation
does not relabel a raw floating residual as an exact certificate.

## 8. Conductance penalties and honest sparsity

For `e={i,j}` define the chord loss

\[
 \ell_e=1-\Omega_i\cdot\Omega_j.
\]

### Theorem 8.1 (fixed loss-weighted total conductance)

Every exact feasible conductance vector satisfies

\[
 \boxed{\sum_{e\in E}\ell_e\gamma_e=1.}
 \tag{8.1}
\]

**Proof.**  Set `y_i=-Omega_i/2`.  Directly from (2.1)--(2.2),

\[
 (\mathcal A^{\mathsf T}y)_e=\ell_e,
 \qquad b^{\mathsf T}y=1.
\]

Pairing `mathcal A gamma=b` with `y` gives (8.1).  Equivalently, dot the
`i`th row equation with `Omega_i`, obtaining
`sum_{e incident i} gamma_e ell_e=2w_i`, and sum over vertices.  `square`

Because `gamma>=0`, the geometrically natural penalty
`sum_e ell_e |gamma_e|` is identically constant.  It cannot select support.

Plain total conductance satisfies

\[
 \sum_e\gamma_e=\frac12\sum_iw_ir_i.
 \tag{8.2}
\]

It minimizes a weighted average rate, not cardinality, and can prefer long
edges.  On a one-shell graph it is also fixed by (8.1).

An exact counterexample uses

\[
 X=\{\pm e_1,\pm e_2\},\qquad w_i=\frac14,
\]

and the complete graph.  Give every perpendicular neighbor directed rate
`a` and the antipode rate `b`, with `a+b=1`.  Then `L Omega=-2 Omega`, while

\[
 \sum_e\gamma_e=a+\frac b2=1-\frac b2.
\]

Minimizing plain `ell^1` selects `b=1`, deleting the local perpendicular
edges and retaining only antipodal jumps.

### Proposition 8.2 (which linear costs are fixed)

If the exact feasible affine space contains a point strictly positive on all
permitted edges, then `c^T gamma` is constant on it if and only if

\[
 c\in\operatorname{range}\mathcal A^{\mathsf T}.
 \tag{8.3}
\]

If exactness forces a coordinate face, delete the forced-zero coordinates
and apply (8.3) on that minimal face.

**Proof.**  Membership in the range makes the cost a multiple of the fixed
right side.  Conversely, strict positivity permits two-sided small motions
in every direction of `ker mathcal A`; constancy makes `c` orthogonal to
that kernel, hence a member of `range mathcal A^T`.  `square`

Honest alternatives are:

- fixed weighted edge-group `ell^2` penalties, convex but not
  cardinality-optimal;
- reweighted `ell^1`, whose individual subproblems are convex but whose
  outer log-sum/MM iteration is nonconvex;
- binary support selection `0<=gamma_e<=M_e z_e`, with
  `M_e=R min(w_i,w_j)` under a rate cap, yielding MILP, MIQP, MISOCP, or
  MISDP models according to the residual objective;
- deterministic pruning with exact reoptimization and certificates.

No statement says that a generic `ell^1` objective yields useful sparsity.

## 9. Exact benchmarks and deterministic failures

### 9.1 Tetrahedral equality optimizer

Let `X` be the regular tetrahedron, `w_i=1/4`, `E=K_4`, and

\[
 \gamma_e=\frac18.
\]

Then

\[
 r_{\max}=\frac32,
 \qquad \operatorname{rank}S_2=3,
 \qquad T_2=4U,
 \qquad \mathfrak D_2=4,
 \tag{9.1}
\]

where `U` is any Euclidean-orthonormal basis of the three-dimensional
sample image.  Paper I gives `mathfrak D_2 r_max>=6`; hence

\[
 \operatorname{opt}P\text{-}D(3/2)=4,
 \qquad
 \operatorname{opt}P\text{-}R(4)=3/2.
 \tag{9.2}
\]

The half-squared Frobenius objective is `3*4^2/2=24`.

This equality has an exact primal--dual reconstruction.  Let
`P=UU^T`.  For fixed rate, take

\[
 Z=\frac16
 \begin{bmatrix}P&-U\\-U^{\mathsf T}&I_3\end{bmatrix},
 \qquad z_i=\frac43,\qquad y=0.
 \tag{9.3}
\]

Then `Z>=0`, `tr Z=1`, `C^Tz=tau(Z)`, and the dual objective is `4`.
For fixed defect `delta=4`, take the same block scaled by `1/8` and
`z_i=1`; then `w^Tz=1` and the dual objective is `3/2`.

The multipliers in (9.3) are a regression against a common factor-four
normalization error.

### 9.2 Octahedral alias benchmark

For

\[
 X=\{\pm e_1,\pm e_2,\pm e_3\},\qquad w_i=\frac16,
\]

use the twelve nonantipodal edges and `gamma_e=1/12`.  Then

\[
 r_i=2,
 \qquad L\Omega=-2\Omega,
 \qquad \operatorname{rank}S_2=2,
 \qquad (L+6I)S_2=3S_2.
\]

Thus

\[
 \mathfrak D_2=3,
 \qquad \mathfrak D_2r_{\max}=6.
 \tag{9.4}
\]

All three off-diagonal trace-free quadratics vanish on the nodes.  Any
implementation that assumes rank five fails this fixture.

### 9.3 Strictly local rows but no global reversible generator

Let

\[
 (\Omega_0,\Omega_1,\Omega_2,\Omega_3)
 =(e_1,e_2,-e_1,-e_2),
\]

use the four-cycle, and take

\[
 w=(1,2,1,2)/6.
\]

Every row uniquely assigns directed rate `1` to each neighbor and exactly
reproduces the coordinates.  Shared conductances do not exist.  Set

\[
 y_i=s_i\Omega_i,
 \qquad s=(-1,1,-1,1).
\]

Then, exactly,

\[
 \mathcal A^{\mathsf T}y=0,
 \qquad b^{\mathsf T}y=-\frac23<0.
 \tag{9.5}
\]

Equation (9.5) is the solver-independent Farkas certificate.

### 9.4 Full-rank ill-conditioned quadratures

For an integer `n>=2`, put

\[
 q_n=\frac{n^2-1}{n^2+1},
 \qquad s_n=\frac{2n}{n^2+1}
\]

and take the ten antipodally paired nodes generated by

\[
 e_1,\quad e_2,\quad (3,4,0)/5,\quad(3,0,4)/5,
 \quad(0,q_n,s_n),
\]

with weights `1/10`.  In coefficient coordinates `(a,b,d,e,f)` for

\[
 \begin{bmatrix}a&d&e\\d&b&f\\e&f&-a-b\end{bmatrix},
\]

the five line samples have determinant

\[
 \frac{1152}{625}q_ns_n\ne0.
\]

Thus the quadratic sampling rank is exactly five for every finite `n`, but

\[
 \lambda_{\min}(S_2^{\mathsf T}WS_2)
 \le\frac{2q_n^2s_n^2}{5}\longrightarrow0.
\tag{9.6}
\]

To prove (9.6), use the unit-Frobenius matrix

\[
 A=(e_2e_3^{\mathsf T}+e_3e_2^{\mathsf T})/\sqrt2.
\]

Its samples vanish on the first four antipodal lines and equal
`sqrt(2)q_n s_n` at each of the two samples on the last line.  Its sampled
Rayleigh quotient is therefore

\[
 2\cdot\frac1{10}\cdot 2q_n^2s_n^2
 =\frac{2q_n^2s_n^2}{5},
\]

which proves the displayed upper bound for the least Gram eigenvalue.  The
ten-node measure is antipodally centered.  Since its total mass is one,
`gamma_ij=1/50=2w_iw_j`; the centered complete-graph identity gives
`L Omega=-2Omega` exactly.  Thus the complete graph has exact `H_1` for
every `n`.
This is an exact all-`n` condition-number regression, not a fitted slope.

### 9.5 Further direct failures

- `sum_i w_i Omega_i !=0` is a necessary-centering Farkas obstruction.
- Every connected component of the active graph must be separately
  `w`-centered.
- A proposed rate cap below the row loss bound is infeasible.
- A selected physical mode in `ker S_l` is rejected rather than normalized.
- An undocumented SVD threshold, output compression, sign flip
  `L-6I`, missing factor two in (5.1), or raw coefficient Frobenius norm is a
  deterministic failed mutation.

## 10. Comparison with the sharp Paper-I lower bound

For every feasible `S^2` design, Paper I proves

\[
 \mathfrak D_2r_{\max}\ge6.
 \tag{10.1}
\]

Therefore, for `R>0` and `delta>0`,

\[
 \operatorname{opt}P\text{-}D(R)\ge\frac6R,
 \qquad
 \operatorname{opt}P\text{-}R(\delta)\ge\frac6\delta.
 \tag{10.2}
\]

The tetrahedral and octahedral reconstructions above attain (10.2) at their
respective caps.  The optimizer comparison reports the ratio to the lower
bound and never infers an all-graph theorem from a numerical equality.

## 11. Prior-art and hypothesis-transfer boundary

### 11.1 Angular Fokker--Planck finite differences

Bienvenue, Naceur, Carrier, and Hebert,
[_A Flexible, Moment-Preserving, and Monotone Discretization of the
Multidimensional Angular Fokker--Planck Operator_](https://doi.org/10.1080/00295639.2025.2462891),
already use quadrature masses and one symmetric shared coefficient per
Voronoi edge.  Their deposited manuscript reports pseudoinverse solutions
and positivity for tested product, level-symmetric, and Lebedev quadratures;
it explicitly leaves general exactness/positivity characterization for
further work.  P2A therefore does not claim the first positive,
moment-preserving, or shared-conductance angular scheme.

The accessible deposited manuscript also requires a convention note.  Its
generator and continuum first-shell target imply

\[
 \sum_j\gamma_{kj}(\Omega_j-\Omega_k)=-2w_k\Omega_k,
\]

whereas its printed moment system displays a factor `-4`.  P2A transfers no
factor silently and uses the explicit task/Paper-I convention `L Omega=-2
Omega`.

### 11.2 Positive meshfree stencils

Seibold,
[_Minimal Positive Stencils in Meshfree Finite Difference Methods for the
Poisson Equation_](https://arxiv.org/abs/0802.2674),
proves local Euclidean positive-stencil/Farkas geometry and basic-feasible
support bounds.  Those stencils are rowwise and the assembled matrix need
not be symmetric.  The theorem does not supply a globally shared reversible
spherical conductance, the prescribed coordinate eigenmap, or the sampled
harmonic quotient.

### 11.3 Eigenpair-preserving graph sparsifiers

Babecki, Steinerberger, and Thomas,
[_Spectrahedral Geometry of Graph Sparsifiers_](https://arxiv.org/abs/2306.06204),
already describe convex sets of positive subgraph reweightings preserving an
ordered initial segment of graph eigenpairs.  P2A does not claim the first
convex eigenpair-preserving graph design.  Here the fixed data are spherical
coordinates and a nonuniform mass matrix, only the geometric coordinate
module is prescribed, sampling aliases are explicitly quotiented, and the
next continuous shell is optimized under a maximum directed-rate cap.

The precise new package is the combination of the accepted Paper-I quotient
and sharp bound with arbitrary fixed `(X,w,E)`, globally shared exactness,
all seven invariant objectives, exact primal/dual and infeasibility
certificates, the conductance-penalty diagnosis, and the adversarial alias,
conditioning, and local/global fixtures.

## 12. Reproducible implementation contract and source map

The implementation under
`afp_barrier_gate1/pure_math/optimization/` provides:

- validation and assembly of `(X,w,E)`, `mathcal A,b,B,C`;
- trace-free quadratic and real harmonic sampling bases;
- exact or rank-certified kernel removal with ambiguous-rank failure;
- affine `T_l` assembly without output compression;
- SDP, SOCP, QP, and LP compilation behind one interface;
- explicit primal and dual solves for the principal formulations;
- solver-independent primal, dual, Farkas, conditioning, and gap reports;
- exact tetrahedral/octahedral reconstruction;
- deterministic ill-conditioned and local/global-infeasible fixtures;
- support pruning with exact reoptimization and rejected-deletion records.

The release workflow installs pinned solver versions, runs at least two
conic backends where supported, checks exact symmetric certificates, runs
the adversarial mutations, executes the Lean finite core, verifies the
literal baseline ancestry and changed-path allowlist, and archives the exact
head create-only.

| Result | Proof source | Test/certificate source | Registry key |
|---|---|---|---|
| affine shared system and rate cap | Sections 1--2 | model assembly audit; exact H1 fixtures | P2A-AFFINE |
| kernel-correct residual and norm | Section 3 | alias and leakage mutations | P2A-QUOTIENT |
| seven convex formulations | Section 4 | cross-formulation solver audit | P2A-PRIMAL |
| exact duals and slackness | Sections 5--6 | primal--dual gap and exact tetra dual | P2A-DUAL |
| Farkas/conic certificates | Section 7 | unequal-mass four-cycle; rate failures | P2A-CERT |
| conductance/sparsity theorem | Section 8 | exact variable-total and fixed-loss tests | P2A-SPARSITY |
| sharp comparison/equality | Sections 9--10 | tetra/octa exact reconstruction | P2A-SHARP |
| multi-shell/response objectives | Sections 4.5--4.6 | shell/response transformation tests | P2A-RESPONSE |
| finite formal identities | Sections 2, 3, 8 | `ConvexGeneratorDesign.lean` | P2A-FORMAL |

## 13. Limitations

The theorem is finite-dimensional and conditional only on the explicitly
given fixed data.  It does not assert that every quadrature/graph is
feasible.  It does not turn local row feasibility into global reversibility,
does not make ambiguous floating rank exact, does not prove that finite
rotations equal a continuum rotation supremum, and does not make nonlinear
transport resolvents convex.  Mixed-integer support selection and
iteratively reweighted penalties are labeled nonconvex.  Equal-cost
transport improvement remains a separate Paper-II response-validation
stage.

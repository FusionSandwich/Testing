# A sharp positivity--rate frontier for quadratic fidelity of reversible spherical generators

> **Scope note.** The frontier, equality, and stability theorems are valid in
> every ambient dimension `d>=2`. The matching constructions in Section 7 are
> proved only for `d=2,3`. No transport or physical-performance conclusion is
> made in this manuscript.

## Abstract

Let $X=(\Omega_i)_{i\in I}$ be a finite indexed sample in
$\mathbb S^{d-1}$ with positive masses $w_i$, and let $L$ be a reversible Markov
generator with nonnegative jump rates. Assume that constants and coordinate
functions are reproduced exactly:
$$
L\mathbf 1=0,
\qquad
L\Omega=-(d-1)\Omega .
$$
We study the residual of $L$ on sampled trace-free quadratic harmonics,
quotienting exactly by the quadratic forms that vanish on $X$. If
$r_{\max}$ is the largest outgoing rate and $\mathfrak D_2$ is the
operator norm of this alias-correct residual in the sampled $\ell^2(w)$
metric, then
$$
\mathfrak D_2 r_{\max}\ge d(d-1).
$$
The constant is sharp in every dimension. We derive an exact covariance
factorization into a scalar squared-loss component, with an exact
rate-floor-plus-variance identity, and an orthogonal anisotropy component;
we characterize equality by common rate and angular loss, with centered
tight-frame conditions in every tangent space in the nonantipodal branch,
a separate antipodal branch, and global reversible compatibility. We give
regular-simplex, cross-polytope, and hypercube extremizers. We also derive an
exact defect decomposition relative to the trace lower bound into radial and
anisotropy terms, together with an explicit weighted concentration
consequence. Stronger pointwise or global geometric conclusions require
additional graph and nondegeneracy hypotheses and are not asserted as
theorems here. The result is an operator frontier, not
a quadrature-design statement or a generic obstruction to signed high-order
discretizations. The order is attained by local positive families in dimensions
two and three. Regular polygons give the exact product in $d=2$. In $d=3$, an
explicit reflected adaptive-ring family has
$$
r_{max}(L_h)\le64\pi^2h^{-2},
\qquad
\mathfrak D_2(L_h)\le\frac{75}{2}h^2,
$$
and therefore
$$
\frac{3}{32\pi^2}h^2
\le\inf_{L\in\mathcal G_h(64\pi^2)}\mathfrak D_2(L)
\le\frac{75}{2}h^2.
$$
A perturbative robustness theorem for the three-dimensional construction is
not claimed here.  The fixed-support perturbation route is retained only as an
open certification problem.

## 1. Introduction

Positive graph generators are attractive because their semigroups preserve
order and mass. On a sampled sphere, exact reproduction of the coordinate
functions is also natural: the coordinates form the first nonconstant
Laplace--Beltrami eigenspace. These two requirements do not, however, leave
arbitrary freedom at the next harmonic degree. This paper identifies the exact
finite-dimensional obstruction.

Fix $d\ge2$. We consider all finite positive reversible generators whose
coordinate map is an eigenmap with eigenvalue $-(d-1)$. The next continuous
spherical eigenvalue is $-2d$, so the relevant finite residual is
$$
R_2=(L+2dI)S_2,
\qquad
(S_2A)_i=\Omega_i^{\mathsf T}A\Omega_i,
\quad A\in\operatorname{Sym}_0(d).
$$
The essential point is that $S_2$ need not be injective and its image need
not be invariant under $L$. We therefore take the domain to be the sampled
quotient $\operatorname{Sym}_0(d)/\ker S_2$, equipped with the norm induced
by $S_2$, and allow $R_2A$ to have components outside
$\operatorname{im}S_2$. This convention retains sampling aliases and
leakage rather than silently discarding them.

The central theorem is the sharp product inequality
$$
\boxed{\;\mathfrak D_2 r_{\max}\ge d(d-1)\;}
$$
together with its equality and stability theory. The proof is finite and
deterministic. It uses exact covariance identities forced by the coordinate
eigenmap, positivity of the jump rates, and a trace comparison in the sampled
metric.

### 1.1 Contributions

The paper makes the following mathematical contributions.

1. It gives an alias-correct formulation of sampled quadratic fidelity and an
   exact covariance representation of the residual.

2. It splits the rowwise residual into Frobenius-orthogonal scalar and
   anisotropic covariance components. The scalar squared-loss moment splits
   exactly into a rate floor and nonnegative angular-loss variance.

3. It proves the sharp all-dimensional frontier
   $\mathfrak D_2r_{\max}\ge d(d-1)$, without injectivity of $S_2$,
   connectedness, equal masses, or invariance of the sampled quadratic space.

4. It characterizes equality both algebraically and geometrically. In the
   nonantipodal branch, each row induces a centered weighted unit-norm tight
   frame in the tangent space, while reversibility imposes additional global
   assembly conditions that are not consequences of rowwise feasibility.

5. It exhibits three exact extremal families in every dimension and resolves
   their sampling kernels explicitly.

6. It proves a normalized near-extremizer defect budget and a weighted
   exceptional-mass consequence. Stronger local and global transfers are
   discussed only as conditional directions requiring explicit mass,
   edge-probability, connectivity, sampling-frame, and tangent-frame margins.

7. It constructs matching-order local positive families in `d=2,3`. The
   circle family is an exact regular-polygon calculation. The spherical
   family uses shared conductances on adaptive reflected rings, proves every
   row moment equation at all levels, and gives the explicit constants
   $\mathsf R_3=64\pi^2$ and $C_3=75/2$.

### 1.2 Priority boundary

The contribution is not the introduction of positive coordinate-exact
spherical Laplacians. Izmestiev and Lam already construct local reversible
spherical Delaunay Laplacians on geodesic triangulations of
$\mathbb S^2$, with nonnegative coefficients under their Delaunay condition
and exact coordinate eigenvalue $-2$
[@IzmestievLam2025DiscreteLaplacians]. Positive meshfree stencils, graphical
designs, prescribed graph eigenspaces, eigenpair-preserving Laplacian cones,
spherical designs, association schemes, graph-Laplacian convergence, and
signed higher-accuracy graph formulas likewise provide important adjacent
theory
[@Seibold2008MinimalPositiveStencils; @BabeckiThomas2022GraphicalDesigns;
@BabeckiShiroma2023Eigenpolytope;
@BabeckiSteinerbergerThomas2023Spectrahedral;
@BannaiBannai2009Survey; @MartinTanaka2008CommutativeSchemes;
@GarciaTrillosEtAl2020SpectralConvergence; @Yoon2025HigherAccuracy].

The distinction here is the joint theorem: a sampled, alias-correct
degree-two operator residual; a sharp universal positivity--rate product; its
full equality geometry subject to global detailed balance; and a quantitative
stability budget with all transfer parameters exposed. The matching
three-dimensional construction additionally derives one globally shared
positive stress on an explicit ring family along the discrete levels
$J=1,2,\ldots$; it is not inferred from
local positive-stencil feasibility, spherical quadrature, or a Delaunay
transfer. A source-by-source
hypothesis comparison and hostile-referee audit is supplied in
`PRIORITY_AND_HOSTILE_REFEREE_AUDIT.md`. Within that focused corpus, we did not
find the same joint package of frontier, equality characterization, exact
defect identity, and local positive constructions. This is a positioning
statement, not an exhaustive novelty or priority claim. Appendix G gives the
in-paper variables/hypotheses/conclusions matrix for every compared theorem.

### 1.3 Organization

Section 2 fixes conventions and the sampled quotient. Section 3 proves the
exact covariance and two-defect identities. Section 4 proves the sharp
frontier. Section 5 characterizes equality and global assembly. Section 6
gives the exact defect budget and concentration consequence. Section 7 proves matching constructions in
dimensions two and three. Section 8 gives exact extremizers and alias examples. Section 9 records
false or overbroad statements ruled out by the theory. The appendices collect
the dependency graph, provenance map, falsification protocol, formalization
scope, reproducibility record, and limitations.

### 1.4 Theorem hierarchy

| Level | Mathematical role | Principal statement | Status |
|---:|---|---|---|
| 1 | Positive reversible generators and sampled harmonic quotients | Proposition 2.1 | ordinary proof; finite Gram identities Lean-checked |
| 2 | Exact covariance and two-defect decomposition | Theorem 3.1 and Proposition 3.2 | ordinary assembly; finite identities Lean-checked |
| 3 | Sharp positivity--rate--quadratic-fidelity frontier | Theorem 4.1 | ordinary proof; lower-bound algebra Lean-checked |
| 4 | Equality geometry and exact extremizers | Theorems 5.1--5.3, Proposition 5.4, Corollaries 5.5--5.6, Section 8 | ordinary proof; selected local algebra Lean-checked; Corollary 5.5 uses a classical external theorem |
| 5 | Quantitative near-extremizer control | Theorem 6.1 and Corollary 6.2 | ordinary proof; stated scalar/tensor consequences Lean-checked |
| 6 | Matching-order local positive construction | Theorems 7.1--7.2 | Theorem 7.1 ordinary/finite Lean algebra; Theorem 7.2 computer-assisted exact-rational proof for `d=3` |
| 7 | Generator-lift or negativity consequences | Section 10 | deliberately not claimed |

### 1.5 Formalization and external-input map

There is no claim that the complete article is formalized. The exact Lean
declarations below are the checked finite components used by the ordinary
proof; an entry reading "none end-to-end" means precisely that no single Lean
theorem has the full manuscript signature.

| Numbered result | Exact Lean declaration(s) used | Ordinary proof | Exact certificate | External or open boundary |
|---|---|:---:|:---:|---|
| Proposition 2.1 | `sphereSamplingWeightedGram_quadratic`; `sphereResidualWeightedGram_quadratic` | yes | no | quotient/eigenvalue interpretation assembled in the article |
| Theorem 3.1 | `quadraticTwoDefect_pythagorean`; `exactLossSecondMoment_decomposition` | yes | no | none |
| Proposition 3.2 | `weightedFrobeniusRowGram_pairing`; `sphereResidualWeightedGram_pairing` | yes | no | none |
| Theorem 4.1 | `quadraticDefect_rate_product_lower`; `sTwo_quadraticDefect_rate_product_lower` | yes | no | sharpness families are ordinary mathematics |
| Theorem 5.1 | `quadraticEquality_rate_product`; `equalityRemainderEntry_zero_iff_axialCovariance` | yes | no | no end-to-end equality-classification declaration |
| Theorem 5.2 | `normalizedTangentTightFrame_iff_oneShellSecondMoment`; `scaledTangentTightFrame_iff_normalized_of_nonantipodal` | yes | no | no global embedding uniqueness is asserted |
| Theorem 5.3 | none end-to-end; local moment identities only | yes | no | Gram completion and Kolmogorov assembly are ordinary mathematics |
| Proposition 5.4 | `antipodalOnlyFeasible_iff_simplex` is a local component | yes | no | connected two-position classification is not one Lean theorem |
| Corollary 5.5 | `normalizedTangentTightFrame_iff_oneShellSecondMoment` is a local component | yes | no | convex regular-polyhedron classification is external [@Coxeter1973RegularPolytopes] |
| Corollary 5.6 | `detailedBalance_eigen_implies_weightedMean_zero`; covariance components | yes | no | no end-to-end declaration |
| Theorem 6.1 | `quadraticStability_master_square_consequences`; `quadraticStability_tensor_rate_bound`; `quadraticStability_weightedMean_le_delta` | yes | no | only the printed budget is claimed |
| Corollary 6.2 | `quadraticStability_badVertexMass_sharp`; `quadraticStability_pointwise_full_budget` | yes | no | retains the individual mass dependence |
| Theorem 7.1 | `regularPolygon_hOne_scalar_recurrence`; `regularPolygon_hTwo_scalar_residual` | yes | no | exact trigonometric assembly is ordinary mathematics |
| Theorem 7.2 | construction identities only; no complete schedule Lean declaration | yes | `certificate.json` plus standalone verifier | computer-assisted analytic/Cauchy and recurrence boundary; perturbations open |

## 2. Positive reversible spherical generators and sampled harmonic quotients

### 2.1 Notation

| Symbol | Meaning | Convention or standing hypothesis |
|---|---|---|
| $I$ | finite vertex set | nonempty |
| $d$ | ambient Euclidean dimension | $d\ge2$ |
| $\Omega_i$ | spherical node | $\Omega_i\in\mathbb S^{d-1}$ |
| $w_i$ | stationary mass | $w_i>0$, $\sum_iw_i=1$ |
| $\gamma_{ij}$ | shared conductance | $\gamma_{ij}=\gamma_{ji}\ge0$, $\gamma_{ii}=0$ |
| $a_{ij}$ | directed jump rate | $a_{ij}=\gamma_{ij}/w_i$ |
| $L$ | negative Markov generator | $(Lf)_i=\sum_{j\ne i}a_{ij}(f_j-f_i)$ |
| $r_i,r_{\max}$ | outgoing rate and its maximum | $r_i=\sum_ja_{ij}$, $r_{\max}=\max_i r_i$ |
| $\ell_{ij}$ | spherical loss | $1-\Omega_i\cdot\Omega_j\in[0,2]$ |
| $\Delta_{ij}$ | chord increment | $\Omega_j-\Omega_i$ |
| $V$ | quadratic coefficient space | $\operatorname{Sym}_0(d)$ |
| $m$ | dimension of $V$ | $d(d+1)/2-1$ |
| $S_2$ | quadratic sampling map | $(S_2A)_i=\Omega_i^{\mathsf T}A\Omega_i$ |
| $K_X$ | sampling-alias kernel | $\ker S_2\subseteq V$ |
| $R_2$ | degree-two residual | $(L+2dI)S_2$ |
| $Q_X$ | sampled quotient | $V/K_X$ with sampled metric |
| $\mathfrak D_2$ | sampled quadratic defect | $\sup_{A\notin K_X}\|R_2A\|_w/\|S_2A\|_w$ |
| $C_i$ | row chord covariance | $\sum_ja_{ij}\Delta_{ij}\Delta_{ij}^{\mathsf T}$ |
| $Z_i$ | centered rank-one tensor | $\Omega_i\Omega_i^{\mathsf T}-I/d$ |
| $M_i$ | trace-free residual tensor | $C_i+2\Omega_i\Omega_i^{\mathsf T}-2I$ |
| $\epsilon_i$ | squared-loss moment | $\sum_ja_{ij}\ell_{ij}^2$ |
| $B_i$ | anisotropy tensor | $M_i-\frac d{d-1}\epsilon_iZ_i$ |
| $E_\epsilon,E_B$ | weighted defect energies | $\sum_iw_i\epsilon_i^2$, $\sum_iw_i\|B_i\|_F^2$ |

The weighted inner product is
$$
\langle f,g\rangle_w=\sum_iw_if_ig_i.
$$
Detailed balance implies that $L$ is self-adjoint and negative
semidefinite in $\ell^2(w)$. Throughout,
$$
L\mathbf1=0,
\qquad
L\Omega=-(d-1)\Omega.
\tag{2.1}
$$
The second identity is componentwise in $\mathbb R^d$.

The quotient $Q_X=V/K_X$ carries the inner product
$$
\langle[A],[H]\rangle_S
=\langle S_2A,S_2H\rangle_w.
\tag{2.2}
$$
This is a genuine inner product on $Q_X$. It is not the quotient of the
Frobenius metric unless an additional sampling-frame identity happens to hold.

### Proposition 2.1 (sampled residual and aliases)

The inclusion $K_X\subseteq\ker R_2$ holds. Hence $R_2$ induces a
well-defined map
$$
\overline R_2:Q_X\longrightarrow\ell^2(w),
\qquad
\overline R_2[A]=R_2A,
$$
and
$$
\mathfrak D_2=\|\overline R_2\|_{Q_X\to\ell^2(w)}.
\tag{2.3}
$$
Equivalently, $\mathfrak D_2^2$ is the largest finite generalized
eigenvalue of the deflated Gram pencil
$$
G_R=R_2^*R_2,
\qquad
G_S=S_2^*S_2
$$
on the Frobenius complement $K_X^{\perp_F}\subseteq V$. No invariance of
$\operatorname{im}S_2$ under $L$ is required.

The genuinely sampled exact degree-two space is
$$
E_{\mathrm{sample}}
=\operatorname{im}S_2\cap\ker(L+2dI),
$$
while the algebraic exact-form space is
$E_{\mathrm{form}}=\ker R_2\subseteq V$. Then
$$
\dim K_X=m-\operatorname{rank}S_2,
\qquad
\dim E_{\mathrm{form}}=m-\operatorname{rank}R_2,
\qquad
\dim E_{\mathrm{sample}}
=\operatorname{rank}S_2-\operatorname{rank}R_2.
\tag{2.4}
$$
The space $E_{\mathrm{form}}$ may contain the alias kernel $K_X$; only
$E_{\mathrm{sample}}$ records genuinely sampled exact modes.

## 3. Exact covariance and the two-defect decomposition

The coordinate eigenmap fixes the first loss moment in every row:
$$
\sum_ja_{ij}\ell_{ij}=d-1.
\tag{3.1}
$$
This elementary identity is the point at which the continuous coordinate
eigenvalue enters all subsequent estimates.

### Theorem 3.1 (exact covariance representation)

For every $A\in\operatorname{Sym}_0(d)$ and every vertex $i$,
$$
(R_2A)_i=\langle A,M_i\rangle_F.
\tag{3.2}
$$
Moreover,
$$
\langle M_i,Z_i\rangle_F=\epsilon_i,
\qquad
\|Z_i\|_F^2=\frac{d-1}{d},
\qquad
\langle B_i,Z_i\rangle_F=0,
\tag{3.3}
$$
and therefore
$$
M_i=\frac d{d-1}\epsilon_iZ_i+B_i,
\qquad
\|M_i\|_F^2
=\frac d{d-1}\epsilon_i^2+\|B_i\|_F^2.
\tag{3.4}
$$

If
$$
V_i
=\sum_ja_{ij}
\left(\ell_{ij}-\frac{d-1}{r_i}\right)^2,
$$
then
$$
\epsilon_i=\frac{(d-1)^2}{r_i}+V_i.
\tag{3.5}
$$
Thus the scalar part of the quadratic residual is the unavoidable rate term
$(d-1)^2/r_i$ plus active-loss variance $V_i$, while $B_i$ is the orthogonal
covariance-anisotropy part.

### Proposition 3.2 (weighted adjoints and exact traces)

Use the Frobenius inner product on $V$ and the weighted inner product on
samples. The adjoints are
$$
S_2^*f=\sum_iw_if_iZ_i,
\qquad
R_2^*f=\sum_iw_if_iM_i.
\tag{3.6}
$$
Consequently,
$$
\operatorname{tr}G_S=\frac{d-1}{d},
\qquad
\operatorname{tr}G_R
=\frac d{d-1}E_\epsilon+E_B.
\tag{3.7}
$$
These trace identities use the sampled metric and remain valid when
$S_2$ has a nontrivial kernel.

### Proof architecture

Equation (3.2) follows by expanding each sampled quadratic along the chord
$\Delta_{ij}$ and applying (2.1). Equation (3.3) follows by contracting with
$Z_i$, after which (3.4) is an orthogonal projection. Equation (3.5) is the
weighted mean--variance identity with fixed mean (3.1). Finally, (3.6)--(3.7)
follow by weighted duality and the row-frame trace formula. Complete proofs are
assembled from the P1A source identified in Appendix B.

## 4. The sharp positivity--rate--quadratic-fidelity frontier

### Theorem 4.1 (sharp trace and product bounds)

Every generator satisfying the hypotheses of Section 2 obeys
$$
\mathfrak D_2^2
\ge
\frac{d^2}{(d-1)^2}E_\epsilon
+\frac d{d-1}E_B.
\tag{4.1}
$$
In particular,
$$
\mathfrak D_2
\ge\frac d{d-1}\sqrt{E_\epsilon}
\ge\frac{d(d-1)}{r_{\max}},
\tag{4.2}
$$
and hence
$$
\boxed{\mathfrak D_2r_{\max}\ge d(d-1).}
\tag{4.3}
$$
The constant is attained for every $d\ge2$.

### Proof architecture

On $K_X^{\perp_F}$, compare the trace of the positive Gram operator
$G_R$ with $\mathfrak D_2^2G_S$. The exact traces (3.7) give (4.1).
Next use (3.5), $V_i\ge0$, $r_i\le r_{\max}$, and
$\sum_iw_i=1$ to obtain (4.2). The regular-simplex family in Section 8
attains equality, so the constant cannot be improved.

### Remark 4.2 (scope of the frontier)

The theorem is neither a general no-go theorem for high-order graph
Laplacians nor a statement about quadrature exactness. It applies to the
specified class of nonnegative reversible generators, with exact coordinate
eigenvalue, the sampled degree-two quotient norm, and the maximum outgoing
rate. Signed formulas and other consistency norms lie outside its hypotheses.

## 5. Equality geometry and exact extremizers

### Theorem 5.1 (algebraic equality characterization)

Equality holds in (4.3) if and only if, for every $i\in I$,
$$
r_i=r_{\max},
\qquad
V_i=0,
\qquad
B_i=0.
\tag{5.1}
$$
Equivalently, with
$$
c_*=\frac{d(d-1)}{r_{\max}},
$$
one has
$$
\epsilon_i=\frac{(d-1)^2}{r_{\max}},
\qquad
M_i=c_*Z_i
\quad\text{for every }i,
\tag{5.2}
$$
and
$$
R_2=c_*S_2
\tag{5.3}
$$
on the full coefficient space and therefore on the sampled quotient.

At equality,
$$
\ker R_2=\ker S_2=K_X,
\qquad
E_{\mathrm{sample}}=\{0\}.
\tag{5.4}
$$
Thus equality does not reproduce the continuous degree-two eigenvalue; it
produces the smallest positive residual allowed by positivity and the rate
cap.

### 5.1 Tangent decomposition

Fix $i$, write $u=\Omega_i$, and let
$$
P_i=I-uu^{\mathsf T},
\qquad
\tau_{ij}=P_i\Omega_j.
$$
Then
$$
\Delta_{ij}=-\ell_{ij}u+\tau_{ij},
\qquad
\|\tau_{ij}\|^2=\ell_{ij}(2-\ell_{ij}),
\qquad
\sum_ja_{ij}\tau_{ij}=0.
\tag{5.5}
$$
Define
$$
h_i=\sum_ja_{ij}\ell_{ij}\tau_{ij},
\qquad
T_i=\sum_ja_{ij}\tau_{ij}\tau_{ij}^{\mathsf T}.
$$

### Theorem 5.2 (local block identity and tight-frame form)

The anisotropy tensor has the exact orthogonal block form
$$
B_i
=-u h_i^{\mathsf T}-h_iu^{\mathsf T}
+T_i-
\left(2-\frac{\epsilon_i}{d-1}\right)P_i,
\tag{5.6}
$$
and
$$
\|B_i\|_F^2
=2\|h_i\|^2
+\left\|
T_i-
\left(2-\frac{\epsilon_i}{d-1}\right)P_i
\right\|_F^2.
\tag{5.7}
$$

If $V_i=0$, all active edges in row $i$ have the common loss
$$
\bar\ell_i=\frac{d-1}{r_i}.
$$
In the nonantipodal case $0<\bar\ell_i<2$, let
$$
p_{ij}=\frac{a_{ij}}{r_i},
\qquad
y_{ij}
=\frac{\tau_{ij}}
{\sqrt{\bar\ell_i(2-\bar\ell_i)}}.
$$
Then $B_i=0$ if and only if
$$
\sum_jp_{ij}y_{ij}=0,
\qquad
\sum_jp_{ij}y_{ij}y_{ij}^{\mathsf T}
=\frac1{d-1}P_i.
\tag{5.8}
$$
Thus the active tangent directions form a centered weighted unit-norm tight
frame. The antipodal case $\bar\ell_i=2$ is governed by the
division-free identities (5.6)--(5.7), not by the normalization in (5.8).

### Theorem 5.3 (global reversible assembly)

In the nonantipodal branch, put
$$
t=1-\ell_*\in(-1,1),
\qquad
p_{ij}=a_{ij}/r_*.
$$
Frontier equality is equivalent to one common outgoing rate
$r_*=(d-1)/(1-t)$ together with
$$
\sum_jp_{ij}=1,
\qquad
w_ip_{ij}=w_jp_{ji},
\qquad
p_{ij}>0\Longrightarrow \Omega_i\cdot\Omega_j=t,
\tag{5.9}
$$
$$
\sum_jp_{ij}\Omega_j=t\Omega_i,
\tag{5.10}
$$
and
$$
\sum_jp_{ij}\Omega_j\Omega_j^{\mathsf T}
=t^2\Omega_i\Omega_i^{\mathsf T}
+\frac{1-t^2}{d-1}
(I-\Omega_i\Omega_i^{\mathsf T})
\tag{5.11}
$$
for every vertex $i$. Conversely, (5.9)--(5.11), with
$a_{ij}=r_*p_{ij}$, reconstruct the coordinate eigenmap and all equality
conditions.

Equivalently, retaining the Markov and detailed-balance conditions in (5.9),
the Gram formulation requires a single matrix
$G\succeq0$ with $G_{ii}=1$, $\operatorname{rank}G=d$, and
$p_{ij}>0\Rightarrow G_{ij}=t$, together with
$$
\sum_jp_{ij}G_{jk}=tG_{ik}
\tag{5.12}
$$
and, for all $i,k,l$,
$$
\sum_jp_{ij}G_{jk}G_{jl}
=\alpha G_{kl}+(t^2-\alpha)G_{ik}G_{il},
\qquad
\alpha=\frac{1-t^2}{d-1}.
\tag{5.13}
$$
On a connected bidirected support, positive reversible masses exist exactly
when the directed rates satisfy the Kolmogorov identity on every oriented
cycle. In particular, local row feasibility does not imply the existence of
a global reversible spherical generator.

### Proposition 5.4 (connected antipodal branch)

If the common equality loss is $\ell_*=2$ and the active graph is connected,
all indexed nodes occupy two antipodal positions $\pm u$, every active edge
joins opposite positions, and
$$
r_*=\frac{d-1}{2},
\qquad
R_2=2dS_2.
\tag{5.14}
$$
Conversely, every reversible connected constant-row-rate generator with this
geometry is an equality generator. Repeated indices at either antipode are
allowed.

### Corollary 5.5 (degree and classification consequences)

Every nonantipodal equality row has at least $d$ active neighbors. If it has
exactly $d$, its normalized tangent directions form a regular simplex with
equal weights. A distinct nonantipodal complete-support equality
configuration is the ambient regular simplex.

For $d=3$, assume additionally that $0<\ell_*<2$, the nodes are the
distinct vertices of a strictly convex inscribed polyhedron, the active graph
is exactly its one-skeleton, all active directed rates have one common value,
and the common vertex degree $q$ satisfies $3\le q\le5$. Then the local
equations force a regular vertex figure and the elementary face/Euler
reduction gives one of the five pairs $(p,q)$. The classical classification
theorem for convex regular polyhedra then implies that the configuration is
tetrahedral, octahedral, cubical, icosahedral, or dodecahedral
[@Coxeter1973RegularPolytopes]. This last classification input is external to
Lean. No corresponding classification is asserted for general weighted
equality configurations.

### Corollary 5.6 (global moment consequence)

Every nonantipodal equality generator satisfies
$$
\sum_iw_i\Omega_i=0,
\qquad
\sum_iw_i\Omega_i\Omega_i^{\mathsf T}=\frac1dI.
\tag{5.15}
$$
Thus its stationary node measure is a weighted spherical $2$-design. This
is a consequence of the reversible equality system; it is neither a standing
design hypothesis nor an identification of operator fidelity with quadrature
exactness.

## 6. Quantitative near-extremizer stability

Assume
$$
\mathfrak D_2r_{\max}
\le d(d-1)(1+\delta),
\qquad \delta\ge0.
\tag{6.1}
$$
Set
$$
n=d-1,
\qquad
a_0=\frac{n^2}{r_{\max}},
\qquad
c_0=\frac{dn}{r_{\max}},
\qquad
\eta=2\delta+\delta^2,
$$
and define
$$
x_i=\frac{\epsilon_i}{a_0},
\qquad
s_i=\frac{r_{\max}}{r_i}-1,
\qquad
v_i=\frac{V_i}{a_0},
\qquad
q_i=x_i-1=s_i+v_i.
\tag{6.2}
$$
The defects $s_i,v_i,q_i$ are nonnegative, and $x_i=1+q_i\ge1$.

### Theorem 6.1 (master stability budget)

Under (6.1),
$$
\sum_iw_i(2q_i+q_i^2)
+\frac{d-1}{d a_0^2}
\sum_iw_i\|B_i\|_F^2
\le\eta.
\tag{6.3}
$$
Consequently,
$$
\sum_iw_i(x_i-1)^2\le\eta,
\qquad
\sum_iw_i
\left(\frac{r_{\max}}{r_i}-1\right)^2
\le\eta,
\tag{6.4}
$$
$$
\sum_iw_i\|B_i\|_F^2
\le
\frac{d(d-1)^3}{r_{\max}^2}\eta,
\tag{6.5}
$$
and
$$
\sum_iw_iq_i\le\delta,
\quad
\sum_iw_is_i\le\delta,
\quad
\sum_iw_iv_i\le\delta,
\tag{6.6}
$$
$$
\sum_iw_iV_i\le a_0\delta,
\qquad
\sum_iw_iV_i^2\le a_0^2\eta.
\tag{6.7}
$$
The estimates are valid without connectedness, injectivity of $S_2$,
equal masses, or a uniform lower mass bound.

### Corollary 6.2 (exceptional mass and pointwise transfer)

Let
$$
H
=\eta-\frac{d-1}{d a_0^2}
\sum_iw_i\|B_i\|_F^2.
$$
Then $0\le H\le\eta$ and
$\sum_iw_i(2q_i+q_i^2)\le H$. For every $\rho>0$,
$$
\sum_{i:q_i\ge\rho}w_i
\le\min\left\{1,\frac{H}{\rho(2+\rho)}\right\}.
\tag{6.8}
$$
At an individual vertex,
$$
q_i\le
\sqrt{1+\frac{H}{w_i}}-1.
\tag{6.9}
$$
Thus a uniform pointwise conclusion requires an explicit lower bound on the
stationary masses.

### Conditional transfers from the defect budget (discussion)

Theorem 6.1 gives weighted mean-square control of radial nonuniformity and
local anisotropy. Pointwise, edgewise, graphwise, quotient, and frame
conclusions require additional assumptions, such as lower bounds on node or
edge weights, a quantitative spectral gap or diameter bound, and
nondegeneracy of reference tangent frames. No unconditional global
embedding-stability theorem is asserted here. The following list records what
a separately stated transfer theorem would have to retain; the list is not a
numbered corollary and is not itself a theorem.

- The global shell loss has an explicit second-moment bound in the symmetric
  directed conductance measure. To control every active edge, one assumes
  $p_{ij}=a_{ij}/r_i\ge\kappa>0$; the pointwise bound still displays $w_i$,
  and a uniform version requires $w_{\min}>0$.

- Graphwise propagation continues the hypotheses
  $p_{ij}\ge\kappa>0$ and $w_i\ge w_{\min}>0$ on the connected support.
  Multiplicative path bounds require the stated small-defect condition;
  additive path, effective-resistance, Poincaré-gap, and congestion variants
  retain their corresponding graph parameter.

- The orthogonal block identity (5.7) converts the tensor term of the master
  budget into weighted control of mixed radial--tangent covariance and tangent
  anisotropy. Together with the scalar term, it controls the full covariance
  relative to its stated target and its eigenvalue splitting. Eigenvector
  control further requires a spectral gap.

- For example, let $W_X=K_X^{\perp_F}$,
  $E=\operatorname{im}S_2$, and
  $$
  \alpha_X
  =\inf_{\substack{A\in W_X\\ \|A\|_F=1}}\|S_2A\|_w^2>0.
  $$
  Define $U:E\to\ell^2(w)$ by $U(S_2A)=R_2A$, and let
  $\iota_E:E\hookrightarrow\ell^2(w)$ denote inclusion. The lower
  sampling-frame bound converts the full master budget into quotient-correct operator
  scalarity, including leakage:
  $$
  \|U-c_0\iota_E\|_{\mathrm{op}}
  \le
  \sqrt{\frac{K_0}{\alpha_X}},
  \qquad
  K_0=\frac{d(d-1)^3}{r_{\max}^2}\eta.
  \tag{6.10}
  $$

- A tangent lower-frame bound gives rotation-quotiented distance to an exact
  centered weighted tight frame. A positive unit-frame and spherical-neighbor
  repair further requires nonantipodal shell margins, a lower active
  probability, and a feature-surjectivity bound.

No parameter-free pointwise, edgewise, graphwise, quotient, or frame-repair
statement is inferred from (6.3), and no claim in this discussion may be
cited as a proved geometric-stability theorem.

### Proof architecture

Insert the near-frontier assumption into the trace inequality (4.1), normalize
by $a_0$, and use $x_i=1+q_i$. This gives (6.3) exactly. The global
consequences follow by positivity and elementary moment inequalities. The
subsequent discussion is deliberately non-theorem scope; the counterexamples
in Section 9 show why its additional margins cannot simply be omitted.

## 7. Matching-order positive constructions in dimensions two and three

Write
$$
d_{\mathbb S}(x,y)=\arccos(x\cdot y),
\quad
h_{\rm fill}(X)=\sup_{x\in\mathbb S^{d-1}}\min_i d_{\mathbb S}(x,\Omega_i),
$$
$$
q_{\rm sep}(X)=\frac12\min_{i\ne j}d_{\mathbb S}(\Omega_i,\Omega_j),
\qquad
\rho_X=\frac{h_{\rm fill}(X)}{q_{\rm sep}(X)}.
$$
For a mesh $X_h$, let $\mathcal G_h(\mathsf R)$ denote the positive reversible
generators on $X_h$ that reproduce constants and coordinates exactly and
satisfy $r_{\max}\le\mathsf R h^{-2}$. Any further support restriction will be stated
with the construction. The lower half of each estimate below is Theorem 4.1;
the work in this section is the matching upper half.

### Theorem 7.1 (regular polygons on $\mathbb S^1$)

Let $N\ge5$, put $h=\pi/N$, and set
$$
\Omega_k=(\cos(2kh),\sin(2kh)),
\qquad k\in\mathbb Z/N\mathbb Z.
$$
Then $h_{\rm fill}(X_h)=q_{\rm sep}(X_h)=h$ and $\rho_{X_h}=1$.
Take $w_k=1/N$ and the two nearest-neighbor rates
$$
a_{k,k-1}=a_{k,k+1}
=\frac{1}{2\{1-\cos(2h)\}}.
\tag{7.1}
$$
Then the graph has degree two and active edge angle $2h$, and
$$
L\mathbf1=0,
\qquad
L\Omega=-\Omega,
$$
$$
r_{\max}=\frac1{1-\cos(2h)},
\qquad
\mathfrak D_2=2\{1-\cos(2h)\}=4\sin^2h,
\tag{7.2}
$$
so $\mathfrak D_2r_{\max}=2$. In particular, with
$$
\mathsf R_2=\frac{\pi^2}{8},
\qquad C_2=4,
\qquad c_2=\frac{16}{\pi^2},
$$
one has
$$
\frac{16}{\pi^2}h^2
\le
\inf_{L\in\mathcal G_h(\mathsf R_2)}\mathfrak D_2(L)
\le4h^2.
\tag{7.3}
$$

#### Proof

The nearest-neighbor sum sends the frequency-$m$ Fourier mode to
$2(\cos(2mh)-1)$ times that mode. With (7.1), the frequency-one eigenvalue is
$-1$, proving exact coordinate reproduction. The sampled trace-free
quadratics are the frequency-two sine and cosine modes; $N\ge5$ makes their
sampled space two-dimensional. Their generator eigenvalue is
$$
-\frac{1-\cos(4h)}{1-\cos(2h)}=-2\{1+\cos(2h)\}.
$$
Adding the continuous degree-two eigenvalue $4$ gives the scalar residual in
(7.2). For $0<h\le\pi/5$,
$$
\frac{2h}{\pi}\le\sin h\le h,
$$
and hence
$1-\cos(2h)=2\sin^2h\ge8h^2/\pi^2$. This proves the rate cap and upper
bound. Theorem 4.1 gives
$\mathfrak D_2\ge2/r_{\max}\ge2h^2/\mathsf R_2$, which is the lower bound in
(7.3). $\square$

### 7.2 The reflected adaptive-ring construction on $\mathbb S^2$

We give the construction data before stating the theorem. Fix
$$
M_0=2^{80},
\qquad a_{\rm pole}=\frac43,
\qquad g=\sqrt{\frac{29}{32}}.
\tag{7.4}
$$
At level $J\ge1$, put $M_m=M_02^m$ and $S_0=M_J/8$. For $0\le m<J$ define
$$
t_m^0=\frac{M_J}{4\pi}\arcsin(2^{m-J}),
\qquad
k_m=\operatorname{nint}(t_m^0-a_{\rm pole}-mg),
$$
and put
$$
K=\operatorname{nint}(S_0-a_{\rm pole}-Jg),
\quad
t_m=a_{\rm pole}+k_m+mg,
\quad
S=a_{\rm pole}+K+Jg,
\quad
h=\frac{\pi}{2S}.
\tag{7.5}
$$
Nearest-integer ties are broken downward. Starting with the north pole and a
first ring at latitude $a_{\rm pole}h$, insert $k_0$ gaps of size $h$, one gap of size
$gh$ at which the longitude count doubles, then
$k_{m+1}-k_m$ ordinary gaps between successive doublings, and finally
$K-k_{J-1}$ ordinary gaps before the equator. Reflect through the equator
without duplicating the equatorial ring. A ring in the $m$th band has $M_m$
equally spaced longitudes. The rounding identities give
$$
|t_m-t_m^0|\le\frac12,
\qquad
|S-S_0|\le\frac12,
\qquad
\left|\frac{2S}{M_m}
\sin\frac{\pi t_m}{2S}-\frac14\right|\le\frac3{M_m}.
\tag{7.6}
$$

Aligned rings use identity longitude matching. At a doubling interface
$M:2M$, put $\alpha=\pi/M$, $c_\alpha=\cos\alpha$, and
$$
p=\frac{4c_\alpha^2+2c_\alpha-1}
        {4c_\alpha(c_\alpha+1)},
\qquad
q=\frac{(2c_\alpha+1)(4c_\alpha^2+2c_\alpha-1)}
        {8c_\alpha^2(c_\alpha+1)}.
\tag{7.7}
$$
For coarse longitude $i$ and fine offset $r=j-2i$, the seven nonzero entries
of the shared radial mask are
$$
\begin{array}{c|rrrrrrr}
r&0&2&-2&1&-1&3&-3\\ \hline
Q_{i,2i+r}&p/2&(1-p)/4&(1-p)/4&q/4&q/4&(1-q)/4&(1-q)/4.
\end{array}
\tag{7.8}
$$
Its row sum is one, every column sum is one half, and its reverse even/odd
conditional laws have the same first two cosine moments.

Preliminary symmetric stresses $\Gamma_{ij}=\Gamma_{ji}$ are fixed recursively
from the pole. At every ordinary row,
two reflected horizontal pairs bracket the target loss by the integer rule
$$
t_- =\max\{1,\lfloor\phi_*/(2\delta)\rfloor\},
\qquad
t_+=\lceil2\phi_*/\delta\rceil,
\tag{7.9}
$$
where $\delta=2\pi/M$ and
$$
\sin(\phi_*/2)=\frac{\sin(h/2)}{\sin\theta}.
$$
Given the incoming radial stress, the outgoing radial stress and the two
horizontal stresses are the unique solution of the three even
moment equations
$$
\sum_j\Gamma_{ij}(\Delta_{ij}\cdot e_\theta)=0,
\qquad
\sum_j\Gamma_{ij}\ell_{ij}(\Delta_{ij}\cdot e_\theta)=0,
\tag{7.10}
$$
$$
\sum_j\Gamma_{ij}
\left\{(\Delta_{ij}\cdot e_\theta)^2
      -(\Delta_{ij}\cdot e_\phi)^2\right\}=0.
\tag{7.11}
$$
At a doubling, the two endpoint rows and their shared radial stress are
solved simultaneously in the corresponding $6\times6$ system using (7.8).
For the first ring, put $\delta_0=2\pi/M_0$ and choose the two horizontal jump
integers nearest to $(3/8)/\delta_0$ and $(9/8)/\delta_0$, with the same
downward tie rule. Set every pole-to-first-ring preliminary stress equal to
$1$, then solve the resulting $3\times3$ system for the outgoing
radial and two horizontal stresses. At the equator use equal reflected
incoming stresses and horizontal jump two; reflection cancels (7.10), and
the positive horizontal stress enforces (7.11). Longitude reflection
cancels every odd-$e_\phi$ equation.

The exact transition matrix has a removable $M^{-1}=0$ limit whose inverse
has norm below $3$ and whose solution has minimum greater than $1/500$.
On the correlated box from (7.6), a rational Cauchy estimate gives
$$
\|A-A_0\|_{\max}\le\frac{10^{12}}M,
\qquad
\|b-b_0\|_\infty\le\frac{10^{12}}M.
\tag{7.12}
$$
Here is the load-bearing transition certificate explicitly. After the row
scalings specified by (7.10)--(7.11), write $x=M^{-1}$,
$y=\eta/(\pi c)\in[-7/6,7/6]$, and $\sigma=\sqrt{58}$. The removable system
$A(x)z=b(x)$ has
$$
A_0=
\begin{pmatrix}
-29/8&\sigma/8&8\sigma&0&0&0\\
-29/8&\sigma/32&128\sigma&0&0&0\\
0&\sigma/8&8\sigma&0&0&0\\
29/8&0&0&-\sigma&\sigma/16&4\sigma\\
29/8&0&0&-\sigma&\sigma/256&16\sigma\\
0&0&0&0&\sigma/16&4\sigma
\end{pmatrix},
\tag{7.12a}
$$
$$
b_0(y)=
\begin{pmatrix}
-3/16\\
63/512+3\sigma y/32\\
13/8+\sigma/4\\
-3/16\\
-285/512-3\sigma y/32\\
13/8+\sigma/4
\end{pmatrix}.
\tag{7.12b}
$$
Exact arithmetic in $\mathbb Q(\sqrt{58})$ gives
$$
\det A_0=\frac{96799941}{512}\sqrt{58},
\qquad \|A_0^{-1}\|_\infty<3,
\qquad \frac1{500}<(A_0^{-1}b_0(y))_k<10.
\tag{7.12c}
$$
The Cauchy disk is $|x|\le10^{-4}$, with the rational guards
$a>1/5$, $c>6/7$, and $\cos(\pi x)>9/10$. On that disk every normalized
matrix entry is below $10^6$ and every right-hand entry is below $10^7$.
Cauchy's estimate yields the deliberately weaker bounds (7.12). Since
$$
18\frac{10^{12}}{2^{80}}<2^{-35},
\qquad
244\frac{10^{12}}{2^{80}}<\frac1{1000}<\frac1{500},
\tag{7.12d}
$$
the Neumann series preserves strict positivity throughout the correlated
transition box. These are exact rational comparisons, not sampled or
floating-point estimates.

For the separate first polar row, $a=4/3$,
$u\in(1/20,1/10)$ and $v\in(1/2,2/3)$. Its normalized limiting determinant is
$4a^3uv(a-1)(2a+1)(u-v)$, whose absolute value is at least $704/6075$.
The polar inverse has norm below $20{,}000$; the rational derivative bounds
$\|\partial_hA_{\rm pol}\|_{\max}\le22{,}000$ and
$\|\partial_hb_{\rm pol}\|_\infty\le1{,}600$, with
$h\le44/(7\cdot2^{80})$, make its finite solution differ from its positive
limiting solution by less than $10^{-6}$. For ordinary
rows, (7.9) gives the uniform bracket
$$
\frac1{16}<x_-<\frac13,
\qquad
2<x_+<7,
\qquad
\frac1{100}U_-<H_-,H_+<100U_-.
\tag{7.13}
$$
For completeness, if $z=\tan(h/2)\cot\theta$, the exact shared-edge
recurrence on an ordinary row is
$$
\frac{U_+}{U_-}
=\frac{(1-z)(1+2z)}{(1+z)(1-2z)},
\qquad
0\le E(z)\le\frac{16z^3}{1-4z^2},
\tag{7.13a}
$$
where
$\log(U_+/U_-)=\log\{\sin(\theta+h/2)/\sin(\theta-h/2)\}+E(z)$.
The sine quotient telescopes. The cap error sums to less than $12$, the
dyadic-band errors sum to less than $1$, and the $m$th count change has
$|\varepsilon_m|<256/M_m$. Put $a_m=256/M_m$ and
$a_*=256/M_0$. For $|x|\le a_*<1$,
$$
\log(1+x)\ge x-\frac{x^2}{2(1-a_*)},
\qquad \log(1+x)\le x.
\tag{7.13b}
$$
Since
$$
\sum_{m<J}a_m<\frac{512}{M_0},
\qquad
\sum_{m<J}a_m^2<\frac{262144}{3M_0^2},
\qquad
\frac1{2(1-a_*)}\sum_{m<J}a_m^2<\frac1{M_0},
$$
the cumulative transition product satisfies the signed second-order bound
$$
e^{-513/M_0}<\prod_{m<J}(1+\varepsilon_m)<e^{512/M_0}.
\tag{7.13c}
$$
The lower estimate does not use the false inequality
$\log(1+x)\ge-|x|$ for negative $x$. The exact telescoping recurrence, including
all count changes, therefore yields
the level-independent shared-stress margins
$$
\Gamma_-=M_0^{-20}\le\Gamma_{ij}\le M_0^{20}=\Gamma_+.
\tag{7.14}
$$
Thus positivity is certified before any normalization; it is not inferred
from the finite generator.

**Computer-assisted proof boundary.** The analytic reduction, literal
systems, recurrence, and geometric normalization are printed here and in the
mathematical supplement `P1E_SHORT_GAP_S2_CONSTRUCTION.md`. The remaining
finite rational inequalities are recorded in the immutable artifact
`afp_barrier_gate1/release/certificates/theorem_7_2/certificate.json` and
checked by the standalone standard-library program `verify_certificate.py`.
The verifier recomputes the determinant, inverse and affine solution in
$\mathbb Q(\sqrt{58})$, the finite rational Cauchy/Neumann and polar-row
budgets, the universal geometric-series and signed second-order transition
budget for arbitrary $J$, the positivity and normalization arithmetic, and
the published constants without floating point or third-party imports. Source
hashes bind provenance; they are not proofs of the hashed source text. The
ordinary proofs in this section and the supplement establish the schedule,
row equations, analytic Cauchy estimates, geometry, telescoping identity, and
quotient argument. The trusted computing base is the certificate and verifier
bytes, CPython arbitrary-precision integer/Fraction arithmetic, SHA-256, and
those explicitly stated analytic lemmas. The adaptive-ring schedule and Cauchy
argument are not Lean-checked. Theorem 7.2 is therefore explicitly a
computer-assisted exact-rational theorem, not a wholly machine-verified one.

### Theorem 7.2 (matching order on $\mathbb S^2$)

For every integer $J\ge1$, let $h_J=\pi/(2S_J)$ be the discrete scale defined
by (7.4)--(7.5). For this explicit sequence, the family (7.4)--(7.14) has
positive weights and a local reversible generator with
$$
L_h\mathbf1=0,
\qquad
L_h\Omega=-2\Omega,
\qquad
\gamma_{ij}=\gamma_{ji}\ge0.
\tag{7.15}
$$
The metrics defined above satisfy
$$
h_{\rm fill}(X_h)\le2h,
\qquad
q_{\rm sep}(X_h)\ge q_*h,
\qquad
\rho_{X_h}\le\frac2{q_*},
\qquad q_*=(8M_0)^{-1}.
$$
Every active edge lies in the angular window
$h/8\le d_{\mathbb S}(\Omega_i,\Omega_j)\le5h$, and the degree is at most
$D=M_0$. For every
vertex,
$$
B_i=0,
\qquad
(R_2A)_i=c_i(S_2A)_i,
\qquad
0<c_i\le\frac{75}{2}h^2.
\tag{7.16}
$$
Consequently,
$$
r_{\max}(L_h)\le64\pi^2h^{-2},
\qquad
\mathfrak D_2(L_h)\le\frac{75}{2}h^2.
\tag{7.17}
$$
With
$$
\mathsf R_3=64\pi^2,
\qquad C_3=\frac{75}{2},
\qquad c_3=\frac{3}{32\pi^2},
$$
one therefore has, for every $J\ge1$ at the corresponding scale $h_J$,
$$
\frac{3}{32\pi^2}h^2
\le
\inf_{L\in\mathcal G_h(\mathsf R_3)}\mathfrak D_2(L)
\le\frac{75}{2}h^2.
\tag{7.18}
$$


#### Proof

The schedule closes exactly because the terminal dimensionless latitude is
$a_{\rm pole}+k_{J-1}+(J-1)g+g+K-k_{J-1}=S$. Equations (7.6), the ring spacing, and
the active jumps prove the stated fill, separation, window, degree, and
packing bounds. The exact row systems (7.10)--(7.11), the shared column sum
in (7.8), the Cauchy bounds (7.12), the ordinary margins (7.13), and the
telescoping product (7.14) prove positivity and assign each undirected edge
one preliminary symmetric stress.

Set
$$
\mu_i=\frac12\sum_j\Gamma_{ij}\ell_{ij},
\qquad
W=\sum_i\mu_i,
\qquad
w_i=\frac{\mu_i}{W},
\qquad
\gamma_{ij}=\frac{\Gamma_{ij}}W.
\tag{7.19}
$$
The tangent force equation and radial contraction give
$$
\sum_j\Gamma_{ij}\Delta_{ij}=-2\mu_i\Omega_i.
$$
Therefore $a_{ij}=\gamma_{ij}/w_i=\Gamma_{ij}/\mu_i$ proves (7.15).
Let $R_i=\sum_j\Gamma_{ij}\ell_{ij}^2$. The loss-force and isotropy equations
give, in the radial--tangent frame,
$$
M_i=\frac1{\mu_i}
\operatorname{diag}(R_i,-R_i/2,-R_i/2)
=\frac{3R_i}{2\mu_i}Z_i.
\tag{7.20}
$$
This proves $B_i=0$ and (7.16) with
$c_i=3R_i/(2\mu_i)$. Since every active edge has angle at most $5h$,
$$
c_i\le3\ell_{\max}\le\frac{75}{2}h^2.
$$
The row multiplier descends directly to the sampled quotient: if $S_2A=0$,
then (7.16) gives $R_2A=0$. Thus no sampling-frame denominator occurs.

Every active edge has loss at least $h^2/(32\pi^2)$, so
$$
r_i
=\frac{2\sum_j\Gamma_{ij}}
       {\sum_j\Gamma_{ij}\ell_{ij}}
\le64\pi^2h^{-2},
$$
which proves (7.17). The lower half of (7.18) is Theorem 4.1:
$\mathfrak D_2\ge6/r_{\max}\ge6h^2/\mathsf R_3$.
$\square$

### Open problem 7.3 (support-preserving perturbations)

The fixed-support reflected-latitude perturbation route remains plausible, but
it is **not** a theorem of this paper.  The repository does not contain the
literal cancellation-free straight-line program, verified operation count,
complete denominator-guard inventory, or machine-checkable derivative and
global-recurrence certificate needed to justify the previously advertised
universal constant.  The associated scripts are retained as diagnostics and
falsification aids only.

A complete robustness theorem would have to preserve the ring counts,
longitude phases, radial masks, horizontal jump integers, pole and equator,
and north--south reflection; enumerate the exact normalized row programs;
certify every reciprocal guard and derivative bound; and propagate the local
bounds through the shared-conductance recurrence.  Until such a certificate is
committed and independently checked, no perturbation radius or constants
$\mathsf R_{\rm rob}$ and $C_{\rm rob}$ are asserted.

## 8. Exact examples

### 8.1 Three extremal families in every dimension

All entries below are exact. Every family has uniform stationary masses,
nonnegative reversible rates, exact coordinate eigenvalue $-(d-1)$, and
$\mathfrak D_2r_{\max}=d(d-1)$.

| Family | Nodes and active graph | Directed active rate | $r_{\max}$ | Common loss | $\mathfrak D_2$ | $\operatorname{rank}S_2$ | $\dim K_X$ |
|---|---|---:|---:|---:|---:|---:|---:|
| Regular simplex | $d+1$ simplex vertices; complete graph | $(d-1)/(d+1)$ | $d(d-1)/(d+1)$ | $(d+1)/d$ | $d+1$ | $d$ | $(d+1)(d-2)/2$ |
| Cross-polytope | $\{\pm e_k\}_{k=1}^d$; all nonantipodal pairs | $1/2$ | $d-1$ | $1$ | $d$ | $d-1$ | $d(d-1)/2$ |
| Hypercube | $\{\pm1/\sqrt d\}^d$; cube edges | $(d-1)/2$ | $d(d-1)/2$ | $2/d$ | $2$ | $\binom d2$ | $d-1$ |

For each family, (5.3) holds with
$c_*=d(d-1)/r_{\max}$. Consequently,
$$
L S_2=-d(2-\ell_*)S_2,
$$
where $\ell_*$ is the common active loss. These examples establish
sharpness in every ambient dimension; no extrapolation from fixed-dimensional
numerics is used.

### 8.2 Platonic examples in $d=3$

With uniform masses, natural shortest-edge graphs, and their exact equality
rates, the tetrahedron, octahedron, cube, icosahedron, and dodecahedron all
satisfy
$$
\mathfrak D_2r_{\max}=6,
\qquad
E_{\mathrm{sample}}=\{0\}.
$$
The tetrahedral, octahedral, and cubical coefficient spaces have alias
dimensions $2$, $3$, and $2$, respectively. Thus nonzero trace-free
quadratic forms may vanish on every node even at frontier equality. The
icosahedral and dodecahedral quadratic sampling maps are injective.

### 8.3 What the examples do and do not show

The examples prove attainment and demonstrate that sampling aliases are
compatible with equality. They do not classify all extremizers. Reversible
blowups, covers, long-chord symmetric shells, and higher-dimensional equality
families prevent such a classification without further hypotheses.
Separately, nonregular weighted tangent tight frames show that even local
equality does not force a regular vertex figure.

## 9. Rejected claims and deterministic counterexamples

The following statements are false or unsupported and are excluded from the
paper.

| Rejected claim | Obstruction retained in the proof package | Correct replacement |
|---|---|---|
| The Frobenius norm on $\operatorname{Sym}_0(d)$ can replace the sampled quotient norm. | Nontrivial $K_X$ in the simplex, cross-polytope, cube, and Platonic examples. | Work on $Q_X=V/K_X$ with metric (2.2). |
| Frontier equality reproduces $H_2$ exactly. | At equality $R_2=c_*S_2$ with $c_*>0$, while $E_{\mathrm{sample}}=\{0\}$. | Equality minimizes the sampled residual under the positivity--rate constraint. |
| Trace saturation alone implies full frontier equality. | Unequal-rate and repeated-node exact fixtures separate the trace step from the rate and variance steps. | Require all three conditions in (5.1). |
| Local positive row stencils automatically assemble into a reversible generator. | Cycle incompatibility and detailed-balance failures. | Impose the global Markov, Gram, and Kolmogorov conditions of Theorem 5.3. |
| Every connected equality generator is Platonic. | Exact blowups, covers, long-chord icosahedral shells, and all-dimensional families. | Use Corollary 5.5 only under its explicit support and convexity hypotheses. |
| Small weighted defect implies uniform vertexwise closeness. | An order-one defect can be hidden at a vertex of arbitrarily small stationary mass. | Retain (6.9) or assume $w_{\min}>0$. |
| Small global shell variance controls every active edge. | An edge of arbitrarily small directed conductance probability may carry order-one loss defect. | Assume $p_{ij}\ge\kappa$, retain the vertex-mass dependence, and use $w_{\min}>0$ for a uniform all-edge statement. |
| Local edge control propagates globally without a graph parameter. | Long paths, cycles, and small-gap graphs accumulate variation. | Retain the $\kappa,w_{\min}$ margins and the applicable path, resistance, gap, or congestion dependence. |
| Small covariance defect alone yields stable eigenvectors or frame repair. | Isotropic targets, nearly singular tangent frames, antipodal collapse, and zero-loss bridges. | Add spectral-gap, tangent-frame, shell, overlap, and surjectivity margins as appropriate. |
| A fitted $O(h^2)$ slope proves the matching upper theorem. | Any finite prefix is compatible with different asymptotics and does not certify exactness or positivity at all levels. | Use the all-orders symbolic, Cauchy, recurrence, and positivity proof of Theorem 7.2. |
| Positivity universally forbids higher-order graph Laplacians. | Signed high-order graph formulas use cancellation outside the present class. | State only the scoped product theorem (4.3). |

## 10. Consequences deliberately outside the flagship theorem

No generator-lift, semigroup comparison, transport-cost improvement, or
physical-model performance theorem is claimed here. A signed construction may
illustrate that leaving the positive cone changes the obstruction, but it does
not strengthen (4.3) unless its normalization and comparison class are made
identical. Such material should appear only in a later paper or a clearly
separated discussion after independent proof and model audits.

## Appendix A. Proof dependency graph

![Proof dependency graph. The lower frontier is independent of the explicit
meshes; the matching result combines the frontier with the construction
upper bounds.](proof_dependency_graph.png)

The all-dimensional lower frontier does not depend on the constructions. The
matching corollaries use it only after the independent `d=2` or `d=3` upper
family has verified positivity, exact coordinates, and the applicable rate
cap. No construction is asserted for `d>3`.

## Appendix B. Theorem-to-source-to-test-to-registry map

The proof source is controlling. A test source supplies falsification and
regression evidence but is not a substitute for proof.

| Manuscript result | Proof source | Test or audit source | Claim-registry entry | Status in this draft |
|---|---|---|---|---|
| Proposition 2.1, sampled quotient, Gram pencil, sampled exact-space dimension | `afp_barrier_gate1/pure_math/covariance/P1A_QUADRATIC_FIDELITY_FOUNDATION.md`, Sections 4--6 | `afp_barrier_gate1/pure_math/covariance/p1a_quadratic_fidelity_audit.py` | P1A-QUOT; P1A-GRAM | ordinary proof with Lean-checked finite identities |
| Theorem 3.1, exact covariance and two-defect identities | same P1A source, Sections 2--3 | same P1A audit | P1A-2DEF | ordinary proof with Lean-checked finite identities |
| Proposition 3.2, weighted adjoints and traces | same P1A source, Sections 4--6 | same P1A audit | P1A-GRAM | ordinary proof with Lean-checked finite identities |
| Theorem 4.1, trace inequality and sharp product | `afp_barrier_gate1/pure_math/covariance/P1B_SHARP_QUADRATIC_DEFECT_BOUND.md`, Sections 3--13 | `afp_barrier_gate1/pure_math/covariance/p1b_sharp_quadratic_defect_audit.py` | P1B-TRACE; P1B-SHARP | ordinary proof with Lean-checked lower-bound algebra |
| Theorem 5.1, equality characterization | same P1B source, Section 11; P1C source for geometric equivalences | P1B and P1C audits | P1B-EQUALITY; P1C-GLOBAL | ordinary proof; selected local algebra Lean-checked |
| Theorem 5.2, tangent block and tight-frame equivalence | `afp_barrier_gate1/pure_math/covariance/P1C_EQUALITY_GEOMETRY.md` | `afp_barrier_gate1/pure_math/covariance/p1c_equality_geometry_audit.py` | P1C-LOCAL | ordinary proof; selected equivalences Lean-checked |
| Theorem 5.3, global reversible assembly | same P1C source | same P1C audit | P1C-GLOBAL | ordinary mathematics; no end-to-end Lean theorem |
| Proposition 5.4 and Corollaries 5.5--5.6, antipodal, scoped classification, and global-moment consequences | same P1C source | same P1C audit | P1C-GLOBAL; P1C-CLASS; P1C-PLATONIC | ordinary mathematics; Corollary 5.5 uses the cited classical classification |
| Theorem 6.1, normalized stability budget | `afp_barrier_gate1/pure_math/covariance/P1D_QUANTITATIVE_STABILITY.md`, Sections 1--3 | `afp_barrier_gate1/pure_math/covariance/p1d_quantitative_stability_audit.py` | P1D-MASTER | ordinary proof with the printed finite consequences Lean-checked |
| Corollary 6.2, exceptional mass and pointwise transfer | same P1D source, Sections 4--5 | same P1D audit | P1D-VERTEX | ordinary proof with matching Lean inequalities |
| Conditional transfers discussion after Corollary 6.2 | same P1D source, Sections 6--10 | same P1D audit | P1D-EDGE; P1D-GRAPH; P1D-COV; P1D-QUOTIENT; P1D-FRAME | not a numbered theorem; no global embedding-stability claim |
| Section 8, all-dimensional and Platonic exact families and aliases | P1C source | P1C audit | P1C-FAMILIES; P1C-PLATONIC; P1C-ALIAS | ordinary exact mathematics |
| Section 9, unrestricted-classification rejection | P1C and P1D counterexample sections | P1C and P1D audits | P1C-UNRESTRICTED and caveats attached to P1D entries | rejected claims retained |
| Theorem 7.1, regular-polygon matching family | Section 7.1, direct Fourier proof | `p1e_asymptotic_family_audit.py`; `QuadraticFidelityConstruction.lean` | P1E-POLYGON | ordinary proof for `d=2`; finite recurrences Lean-checked |
| Theorem 7.2, adaptive-ring mesh, positivity and exact `H_0,H_1` | `docs/publication_program/P1E_SHORT_GAP_S2_CONSTRUCTION.md`, Sections 1--8 | exact-rational certificate and standalone verifier; derivation audits listed below | P1E-RING | computer-assisted exact-rational proof for `d=3` |
| Theorem 7.2, sampled quotient multiplier and matching constants | P1E proof source, Section 9 | certificate verifier; proof audit; hostile Cauchy audit | P1E-ROW; F-CONSTRUCT | computer-assisted exact-rational proof for `d=3` |
| Open problem 7.3, support-preserving perturbations | P1E source, Section 10, and retained diagnostic calculations | `p1e_no_guard_ring_independent_audit.py` | P1E-ROBUST | open; no perturbation radius or robustness constants are claimed |

The claim registry is `THEOREM_REGISTRY.md`. Any change in theorem
strength must first be reconciled with the proof source and then recorded in
that registry; a passing test alone cannot promote a claim.

## Appendix C. Falsification protocol

The computational appendices serve four limited purposes:

1. verify finite tensor identities and sign conventions on deterministic exact
   examples;

2. expose sampling aliases, leakage, and weighted-adjoint mistakes;

3. retain deterministic failure cases for omitted hypotheses; and

4. check explicit constants and extreme-scale conditioning with exact,
   algebraic, or outward-rounded interval arithmetic where appropriate.

The required audit programs are:

- `p1a_quadratic_fidelity_audit.py` for quotient, covariance, weighted Gram,
  and alias identities;

- `p1b_sharp_quadratic_defect_audit.py` for sharpness, degeneracy, sign, and
  normalization fixtures;

- `p1c_equality_geometry_audit.py` for tangent blocks, all-dimensional
  extremizers, Platonic exactness, aliases, antipodal branches, blowups,
  long-chord shells, weighted frames, and cycle compatibility; and

- `p1d_quantitative_stability_audit.py` for small masses, small active edge
  probabilities, long paths, small gaps, singular frames, sampling gaps,
  aliases, and certified extreme-scale inequalities;

- `p1e_short_gap_symbolic_matrix_audit.py`,
  `p1e_short_gap_cauchy_guard_audit.py`, and
  `p1e_short_gap_cauchy_hostile_audit.py` for the literal transition matrix
  and its uniform all-orders guard;

- `p1e_short_gap_polar_guard_audit.py`,
  `p1e_short_gap_proof_audit.py`, and
  `p1e_no_guard_ring_independent_audit.py` for the first row, exact constants,
  recurrence, and reachable-domain margins; its perturbation arithmetic is a
  retained candidate diagnostic, not theorem evidence; and

- `p1e_short_gap_family_audit.py` and
  `p1e_short_gap_referee_audit.py` for finite generator reconstruction and
  deterministic failed mutations. The six alternative-route audits are
  retained separately and cannot be read as a proof by exhaustion.

No numerical rank threshold is used in a theorem. Exact symbolic minors or
algebraic identities certify the ranks quoted in Section 8. Theorem 7.2 is
all-orders; its finite generator output and convergence measurements are
regressions only.

## Appendix D. Formalization

The finite algebraic core is formalized in the following Lean sources:

| Formal source | Mathematical scope |
|---|---|
| `AFPBarrier/QuadraticFidelityFoundation.lean` | weighted finite identities, sampling quotient foundations, covariance decomposition |
| `AFPBarrier/QuadraticFidelityLowerBound.lean` | trace comparison and sharp lower-bound algebra |
| `AFPBarrier/QuadraticEqualityGeometry.lean` | division-free tangent blocks and guarded normalized-frame identities |
| `AFPBarrier/QuadraticFidelityStability.lean` | normalized master-budget algebra and finite consequences |
| `AFPBarrier/QuadraticFidelityConstruction.lean` | shared-stress force and detailed-balance identities, moment normalization, four-point connectors, rate conversion, and regular-polygon residuals |

The formalization is a second proof surface for the stated finite identities.
It does not by itself formalize every geometric classification argument,
external-priority statement, adaptive-ring schedule, or analytic Cauchy guard. The manuscript
must not label an unformalized conclusion as machine-checked merely because a
nearby algebraic lemma is formalized.

## Appendix E. Reproducibility record

From the repository root, the deterministic theorem audits may be run with:

    python afp_barrier_gate1/pure_math/covariance/p1a_quadratic_fidelity_audit.py
    python afp_barrier_gate1/pure_math/covariance/p1b_sharp_quadratic_defect_audit.py
    python afp_barrier_gate1/pure_math/covariance/p1c_equality_geometry_audit.py
    python afp_barrier_gate1/pure_math/covariance/p1d_quantitative_stability_audit.py
    python afp_barrier_gate1/pure_math/covariance/p1e_short_gap_symbolic_matrix_audit.py
    python afp_barrier_gate1/pure_math/covariance/p1e_short_gap_cauchy_guard_audit.py
    python afp_barrier_gate1/pure_math/covariance/p1e_short_gap_cauchy_hostile_audit.py
    python afp_barrier_gate1/pure_math/covariance/p1e_short_gap_polar_guard_audit.py
    python afp_barrier_gate1/pure_math/covariance/p1e_short_gap_proof_audit.py
    python afp_barrier_gate1/pure_math/covariance/p1e_no_guard_ring_independent_audit.py
    python afp_barrier_gate1/pure_math/covariance/p1e_short_gap_family_audit.py
    python afp_barrier_gate1/pure_math/covariance/p1e_short_gap_referee_audit.py

The Lean surface may be checked from `afp_barrier_gate1` using the repository's
pinned toolchain and build command.

Release-specific workflow identifiers, continuous-integration run identifiers,
commit hashes, environment captures, and artifact checksums belong only in a
separate reproducibility manifest accompanying a tagged release. They are not
part of any hypothesis or mathematical argument and must not appear in
Sections 1--10.

The external-source bibliography for the priority audit is
`docs/publication_program/p1f_manuscript/priority_sources.bib`. Every imported
theorem must be accompanied by the source-specific hypothesis-transfer note in
`PRIORITY_AND_HOSTILE_REFEREE_AUDIT.md`; the present P1A--P1E proofs are
self-contained and use those sources for context rather than as hidden proof
lemmas.

## Appendix F. Limitations and future work

1. The matching construction is proved only in ambient dimensions two and
   three. The sharp frontier, equality theory, and quantitative stability are
   all-dimensional, but no matching local family is claimed for `d>3`.

2. The stability theorem is fundamentally weighted. Uniform pointwise
   rigidity requires a lower stationary mass; uniform edgewise rigidity
   requires a lower active conductance probability.

3. Graphwide rigidity depends on a quantitative connectivity parameter.
   Sampling-quotient scalarity depends on a lower sampling-frame bound, and
   tangent-frame repair depends on tangent conditioning and nondegeneracy
   margins.

4. Equality is not a classification by a short list of symmetric polytopes.
   The scoped three-dimensional convex classification has explicit hypotheses,
   while blowups, covers, long-chord shells, and higher-dimensional equality
   families remain; nonregular local frames separately obstruct local
   regularity.

5. Sampling aliases can occur for small or symmetric node sets. The theorem
   controls the genuinely sampled quotient and does not reconstruct
   coefficients in $K_X$.

6. No transport, physical-model, or application-level performance consequence
   follows from the harmonic operator norm alone. Such claims require separate
   models, normalizations, and audits.

7. Signed higher-accuracy graph operators are outside the positive reversible
   class. A future comparison should specify a common rate or cost constraint
   before drawing conclusions about the benefit of leaving the positive cone.

8. The candidate `d=3` support-preserving perturbation route fixes ring counts,
   phases, masks, horizontal jumps, pole/equator data, and reflection. It
   remains an open certification problem, supplies no theorem, perturbation
   radius, or constants, and does not cover arbitrary node motion or
   independent longitude perturbations.

The immediate construction question is now higher-dimensional: whether a
different local compiler can produce the matching order for `d>3` with shared
positive conductances and a quantitative global feasibility margin. A broader
robustness result in `d=3` would likewise require a uniform right inverse for
the full shared six-moment edge system.

## Appendix G. Related-theorem and hypothesis-transfer matrix

The table distinguishes external results from the theorems proved here. The
long-form line-by-line convention audit, including primary-source theorem
locations, is `PRIORITY_AND_HOSTILE_REFEREE_AUDIT.md`.

| Source and variables | External hypotheses | External conclusion used | Overlap | New distinction and transfer guard |
|---|---|---|---|---|
| Babecki--Thomas: graph eigenspaces, node subsets, quadrature weights | connected regular unweighted graph; normalized-adjacency ordering | graphical designs correspond through Gale duality to eigenpolytope faces, with support consequences | finite eigenspaces and positive weights | their weights average a fixed graph; $w_i$ and $\gamma_{ij}$ here define the operator. No spherical eigenmap, rate cap, or quadratic frontier transfers |
| Babecki--Shiroma: positive edge-weighted graphs and eigenpolytopes | connected graph; symmetric combinatorial Laplacian in uniform Euclidean metric | broad eigenspace and eigenpolytope universality for positive weighted graphs | prescribed eigenspaces with positive edges | universality need not preserve unit spherical geometry, locality, degree, nonuniform mass, target eigenvalue, or $H_2$ residual; flip the positive-semidefinite sign and retain the mass matrix |
| Steinerberger [@Steinerberger2021SpectralLimitations]: manifold eigenfunctions, $n$ quadrature nodes | compact boundaryless manifold; nonnegative quadrature exact on an initial spectral segment | asymptotic cardinality limitation for positive quadrature | positivity and continuous harmonic modes | integration is not a graph-operator identity. Keep manifold dimension $d-1$, multiplicity, volume measure, and the asymptotic $o(n)$ term; no finite frontier follows |
| Izmestiev--Lam: geodesic spherical triangulation, $c_{ij},d_i$ | closed triangulation; nonnegative Delaunay edge coefficients | their normalized spherical Laplacian is reversible and satisfies $\Delta_sp=-2p$ | local positive reversible coordinate-exact operators on $\mathbb S^2$ | this paper does not claim to introduce that object. Their theorem supplies neither the sampled quotient/frontier nor the adaptive-ring $H_2$ and mesh constants; conversion requires $w_i=d_i/\sum d$, $\gamma_{ij}=c_{ij}/\sum d$ |
| Seibold: Euclidean point cloud and row stencil coefficients | polynomial moment equations; local geometric cone conditions | sparse positive Poisson stencils and feasibility criteria | positive local moment cones | a rowwise stencil is generally nonsymmetric and gives no shared $\gamma_{ij}$ or stationary masses. Curvature, global reconciliation, and a strict margin must be proved separately |
| Babecki--Steinerberger--Thomas: base graph and first $k$ eigenpairs | connected positive weighted graph; candidate is a reweighted spanning subgraph | eigenpair-preserving Laplacians form a polyhedral/spectrahedral slice | positive eigenpair preservation | here the geometric coordinate module is prescribed, aliases are quotiented, and the next continuous shell is measured under $r_{\max}$. With nonuniform $w$, the comparison is a generalized eigenproblem |
| García Trillos--Gerlach--Hein--Slepčev: random manifold sample and kernel bandwidth | i.i.d. density bounds, compact manifold geometry, kernel and bandwidth conditions | high-probability eigenvalue/eigenvector convergence to a weighted Laplace--Beltrami operator | local positive graph Laplacians approaching a continuum operator | probabilistic spectral convergence does not give finite exact $H_1$, bounded degree, shared correction, or the deterministic $O(h^2)$ quotient bound. Their bandwidth is not silently identified with this fill parameter |
| Martin--Tanaka: association scheme adjacency algebra | finite commutative scheme; uniform counting metric | primitive idempotents and nonnegative Krein parameters organize products and embeddings | symmetric examples and harmonic-module products | one must first prove that $L$ lies in the Bose--Mesner algebra and identify its idempotents with sampled spherical harmonics. Unequal masses and aliases are not automatic |
| Bannai--Bannai: finite spherical sets and polynomial moments | usually uniform spherical $t$-design measure | harmonic-moment characterization and design bounds | common symmetric node sets and frame moments | design exactness is a measure identity, not a generator. It implies neither reversible local edges, sampled injectivity, nor $L$-invariance; frontier equality has positive residual, not exact $H_2$ |
| Ahrens--Beylkin [@AhrensBeylkin2009RotationalQuadratures]: icosahedral orbits and quadrature weights | rotational invariance; moment equations for targeted polynomial spaces | rotationally invariant spherical quadratures | symmetry-orbit reductions | quadrature weights are not conductances or stationary masses. Symmetry preserves a generator constraint only after support and orientation invariance are proved |
| Yoon: graph powers/walks and $m$-Laplacian coefficients | simple graph; signed higher-order finite-difference-inspired operator | high formal order on cycles using alternating coefficients for $m\ge2$ | graph-Laplacian accuracy | the signed class lies outside $\gamma\ge0$. The present theorem is only the sampled degree-two residual/rate frontier for positive reversible coordinate-exact generators |
| Benedetto--Fickus [@BenedettoFickus2003FiniteFrames]: unit vectors and frame operator | finite unit-norm frames in a Hilbert space | unit-norm tight frames minimize the frame potential | tangent tight-frame equality language | tight frames themselves are established theory. The new statement is their forced appearance together with common loss/rate and global detailed-balance compatibility in equality for this frontier |

No row is imported as a proof of Theorems 3.1, 4.1, 5.1--5.3, 6.1, or
7.1--7.2. External results supply context and established terminology; every
normalization used in the new theorem hierarchy is derived internally.

## References

Bibliographic data for the sources cited in the priority discussion are in
`priority_sources.bib`. Journal versions are used when available, and the
related-work discussion retains the convention-transfer notes needed to keep
the comparison classes distinct.

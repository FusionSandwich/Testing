# Finite positive eigenmap generators: feasibility, sampled quadratic rigidity, equality classification, and sharp graph barriers

## Manuscript theorem package

### Abstract

Let a finite positive jump generator carry a prescribed Euclidean eigenmap. We
study three questions that are usually separated: when nonnegative local rows
exist on a spherical node set, which algebraic quadratic forms survive as
genuine sampled eigenfunctions, and how equality or near-equality in the
associated rate--defect inequality constrains the active graph. The local
spherical problem is characterized exactly by an indexed tangent convex hull,
including repetitions, lower-dimensional spans, and antipodal neighbors. Its
reversible global counterpart is a shared-edge cone problem with an exact
Farkas alternative and sparse local-to-global obstructions. For quadratic
samples we prove that the covariance residual factors through the finite
sampling map. Consequently the genuine sampled exact space is an intersection
inside the sampled function space, rather than the algebraic kernel suggested
by form counting. Positive axial covariance annihilates every genuine sampled
quadratic mode, while exact Platonic examples show that large algebraic form
spaces may consist entirely of sampling aliases. We then classify equality in
the sharp spherical rate--defect inequality. On a connected symmetric active
support, equality propagates one common row rate and one common chord loss; for
strict convex geodesic triangulations this yields exactly the tetrahedral,
octahedral, and icosahedral embeddings. Quantitative variants give explicit
path- and diameter-dependent stability estimates. Finally, on the unreduced
latitude--longitude product graph, the polar coordinate equations uniquely
force a quartic row rate. This gives the exact graph-class minimax value, a
uniform asymptotic expansion with rigorous remainder, a nondegenerate
rate-capped extremal problem, and an LP-dual anisotropy invariant over the
entire feasible cone. Lean formalization covers the finite algebra, while exact
symbolic audits serve only as independent falsification and regression tools.

---

## 1. Setting

Let `I` be finite and

\[
(Lf)(i)=\sum_{j\ne i}a_{ij}(f(j)-f(i)),
\qquad a_{ij}\ge0.
\tag{1.1}
\]

Let

\[
\Phi:I\to\mathbb R^d,
\qquad
L\Phi=-\lambda\Phi
\tag{1.2}
\]

coordinatewise. Positivity means nonnegative off-diagonal rates; conservation
fixes the diagonal. Reversibility is a separate condition: for positive masses
`w_i`, there are shared conductances

\[
\gamma_{ij}=\gamma_{ji}\ge0,
\qquad
a_{ij}=\frac{\gamma_{ij}}{w_i}.
\tag{1.3}
\]

The theorem hierarchy is:

1. standard finite generator identities;
2. sampled quadratic covariance and rigidity;
3. exact spherical local feasibility and global shared-edge compatibility;
4. exact and quantitative spherical equality rigidity;
5. sharp product-graph and constrained extremal theory;
6. exact examples, counterexamples, and signed boundary cases;
7. formal and computational appendices.

The central contribution is Section 3. It is meaningful without any numerical
scheme or project terminology.

---

## 2. Foundational standard lemmas

For

\[
\Gamma(f,g)(i)=\frac12\sum_j a_{ij}
(f(j)-f(i))(g(j)-g(i)),
\tag{2.1}
\]

one has

\[
L(fg)-fLg-gLf=2\Gamma(f,g).
\tag{2.2}
\]

If `Lf=-lambda f` and `Lg=-nu g`, then

\[
L(fg-c)+\mu(fg-c)
=2\Gamma(f,g)+(\mu-\lambda-\nu)fg-\mu c.
\tag{2.3}
\]

At additive resonance,

\[
L(fg-c)=-(\lambda+\nu)(fg-c)
\iff
2\Gamma(f,g)=(\lambda+\nu)c.
\tag{2.4}
\]

For a square,

\[
L(f^2-c)=-2\lambda(f^2-c)
\iff
\Gamma(f,f)=\lambda c.
\tag{2.5}
\]

Thus an uncentered resonant square forces zero carré du champ, but a centered
one need not. The four-state Boolean square is the permanent counterexample to
any universal centered-square impossibility statement.

These product identities, finite rank-nullity, convex separation, Farkas
alternatives, finite LP duality, and compactness are standard inputs. They are
not publication novelty by themselves.

---

## 3. Central theorem: genuine sampled quadratic exactness

For a real matrix `A`, define

\[
Q_A(i)=\Phi_i^TA\Phi_i,
\qquad
C_i=\sum_j a_{ij}(\Phi_j-\Phi_i)(\Phi_j-\Phi_i)^T.
\tag{3.1}
\]

### Theorem 3.1 — exact covariance identity

For every real `A`,

\[
\boxed{
LQ_A(i)=-2\lambda Q_A(i)+\operatorname{tr}(A^TC_i).
}
\tag{3.2}
\]

For `q_{A,c}=Q_A-c`, target eigenvalue `-mu` is equivalent to

\[
\boxed{
\operatorname{tr}(A^TC_i)
+(\mu-2\lambda)Q_A(i)-\mu c=0
\quad\forall i.
}
\tag{3.3}
\]

No positivity or reversibility is needed for this identity.

### Spherical degree-two specialization

Assume

\[
\Phi_i\in S^{d-1},
\qquad
\lambda=d-1,
\qquad
\mu=2d,
\qquad
A\in\operatorname{Sym}_0(d).
\tag{3.4}
\]

Let

\[
P_0(T)=T-\frac{\operatorname{tr}T}{d}I,
\qquad
M_i=P_0(C_i+2\Phi_i\Phi_i^T).
\tag{3.5}
\]

Then

\[
E_{\rm form}
=\{A:\langle A,M_i\rangle_F=0\ \forall i\}
=\operatorname{span}\{M_i\}^{\perp}.
\tag{3.6}
\]

This is an algebraic form space, not yet a space of nonzero sampled functions.

Define

\[
S_X(A)_i=\Phi_i^TA\Phi_i,
\qquad
K_X=\ker S_X,
\tag{3.7}
\]

and let `R_X(A)_i=<A,M_i>_F`.

### Theorem 3.2 — residual-through-sampling factorization

\[
\boxed{R_X=(L+2dI)S_X.}
\tag{3.8}
\]

Consequently,

\[
\boxed{K_X\subseteq E_{\rm form},}
\tag{3.9}
\]

\[
\boxed{
E_{\rm sample}
:=S_X(E_{\rm form})
=\operatorname{im}S_X\cap\ker(L+2dI),
}
\tag{3.10}
\]

and

\[
\boxed{
\dim E_{\rm sample}
=\dim E_{\rm form}-\dim K_X
=\operatorname{rank}S_X-\operatorname{rank}R_X.
}
\tag{3.11}
\]

Equation (3.10), not the form-space dimension, is the genuine sampled theorem.
It survives every sampling-kernel and alias example in the package.

### Theorem 3.3 — positive axial rigidity

Suppose every row has axially isotropic covariance

\[
C_i=\tau_i(I-\Phi_i\Phi_i^T)+\beta_i\Phi_i\Phi_i^T,
\qquad \beta_i>0.
\tag{3.12}
\]

Then

\[
M_i=\frac{d\beta_i}{d-1}
\left(\Phi_i\Phi_i^T-\frac1dI\right),
\tag{3.13}
\]

so the constraint row is a positive multiple of the sampling row. Therefore

\[
\boxed{E_{\rm form}=K_X,
\qquad E_{\rm sample}=\{0\}.}
\tag{3.14}
\]

For a positive generator,

\[
\beta_i=\sum_j a_{ij}(1-\Phi_i\cdot\Phi_j)^2,
\tag{3.15}
\]

and one positive jump to a distinct embedded point ensures `beta_i>0`.

Regular simplices attain this theorem in every dimension while retaining a
large algebraic sampling kernel. This supplies sharpness beyond a tautological
rank identity.

### Theorem 3.4 — positive equivariant rigidity

Let a finite group act transitively on the state set and equivariantly on the
unit-sphere eigenmap. Assume every off-diagonal rate is nonnegative, the rate
system is invariant, the real conjugation representation on
`Sym_0(d)` is irreducible, and at least one positive jump joins distinct
embedded points. Then

\[
\boxed{E_{\rm form}=\{0\}.}
\tag{3.16}
\]

Reversibility is not needed. Global nonnegativity is essential: the exact
signed regular pentagon has irreducible conjugation action and a full
trace-free sampled quadratic eigenspace.

### Exact examples

For the shortest-edge Platonic generators on `S^2`:

| Graph | `dim E_form` | `dim K_X` | `dim E_sample` |
|---|---:|---:|---:|
| tetrahedron | 2 | 2 | 0 |
| octahedron | 3 | 3 | 0 |
| cube | 2 | 2 | 0 |
| icosahedron | 0 | 0 | 0 |
| dodecahedron | 0 | 0 | 0 |

The first three rows show why algebraically nonzero exact forms need not define
nonzero sampled modes.

---

## 4. Exact spherical local feasibility

Fix `Omega_i in S^2`. For each permitted non-antipodal neighbor,

\[
\Omega_j=\cos\theta_j\Omega_i+\sin\theta_j u_j,
\qquad0<\theta_j<\pi,
\tag{4.1}
\]

where `u_j` is a unit tangent vector. Antipodes are treated separately and are
never assigned a fictitious tangent direction.

### Theorem 4.1 — indexed local feasibility

A nonnegative degree-one-exact row supported on the permitted non-antipodal
neighbors exists if and only if

\[
0\in\operatorname{conv}\{u_j\}.
\tag{4.2}
\]

A row positive on every indexed permitted edge exists if and only if

\[
0\in\operatorname{relint}\operatorname{conv}\{u_j\}
\tag{4.3}
\]

in the affine span. Repeated directions, redundant points, and lower-dimensional
spans are included.

For a normalized dependence

\[
\beta_j\ge0,
\quad\sum_j\beta_j=1,
\quad\sum_j\beta_ju_j=0,
\tag{4.4}
\]

put

\[
S(\beta)=\sum_j\beta_j\tan(\theta_j/2).
\tag{4.5}
\]

The unique positive common scaling is

\[
\boxed{
a_j(\beta)=
\frac{2\beta_j}{\sin\theta_j\,S(\beta)}.
}
\tag{4.6}
\]

The row is unique exactly when the normalized tangent-dependence polytope is a
singleton.

### Antipodes

For antipodal-only support, feasibility is the simplex

\[
a_k\ge0,
\qquad\sum_k a_k=1.
\tag{4.7}
\]

In mixed support, the non-antipodal tangent cone may spend any normal budget
between zero and two; the remaining budget is allocated over the antipodal
simplex. Strict positivity on every mixed edge holds exactly when zero is in
the relative interior of the non-antipodal tangent hull.

### Quantitative margin

The relative inradius `rho` of the tangent hull is positive exactly under
robust strict feasibility. It gives an indexed dependence with

\[
\beta_j\ge\frac{\rho}{m(1+\rho)},
\tag{4.8}
\]

and explicit coefficient, rate, conditioning, and perturbation bounds. Under
`c_1h<=theta_j<=c_2h`, outgoing rates have explicit inverse-quadratic bounds.

---

## 5. Global reversible shared-edge compatibility

For positive masses and an undirected permitted graph, introduce one shared
conductance per undirected edge. The equilibrium system is

\[
A\gamma=b,
\qquad\gamma\ge0,
\qquad b_i=-2w_i\Omega_i.
\tag{5.1}
\]

### Theorem 5.1 — exact cone and dual characterization

The feasible set is the polytope

\[
\{\gamma\ge0:A\gamma=b\}.
\tag{5.2}
\]

Feasibility is equivalent to `b` belonging to the finitely generated
shared-edge cone. Equivalently, there is no Farkas certificate `y` with

\[
A^Ty\ge0,
\qquad\langle y,b\rangle<0.
\tag{5.3}
\]

Weighted centering

\[
\sum_iw_i\Omega_i=0
\tag{5.4}
\]

is necessary. On the complete graph it is sufficient, with the explicit
positive conductance

\[
\gamma_{ij}=2w_iw_j.
\tag{5.5}
\]

Finite LP duality and complementary slackness apply with the actual matrix and
sign conventions. Equivariant averaging and centered-clique decompositions are
valid reconciliation mechanisms for their stated sparse classes.

Local row feasibility plus weighted centering does not imply arbitrary sparse
shared-edge feasibility. Exact four-cycle and cube certificates remain
permanent counterexamples.

---

## 6. Equality and near-rigidity on `S^2`

For the spherical coordinate eigenmap, define

\[
\ell_{ij}=1-\Omega_i\cdot\Omega_j,
\quad r_i=\sum_ja_{ij},
\quad D_i=\sum_ja_{ij}\ell_{ij}^2,
\quad Q_i=\frac{r_iD_i}{4}.
\tag{6.1}
\]

The coordinate equation gives

\[
\sum_ja_{ij}\ell_{ij}=2.
\tag{6.2}
\]

### Theorem 6.1 — exact local equality

\[
\boxed{Q_i\ge1.}
\tag{6.3}
\]

Equality holds if and only if every active edge from `i` has

\[
\boxed{\ell_{ij}=\frac2{r_i}.}
\tag{6.4}
\]

Active zero-loss edges are impossible. An active antipodal edge forces
`r_i=1`.

### Theorem 6.2 — connected propagation

If the active relation is symmetric and connected, exact equality at every
node gives one common row rate and one common active chord loss.

### Theorem 6.3 — restricted triangulation classification

Assume the active support is exactly the one-skeleton of an injective, strict
convex, minor-geodesic triangulation of `S^2`, and every triangulation edge is
active. If the coordinate equation and `Q_i=1` hold everywhere, then the
embedding is, up to an orthogonal transformation,

\[
\boxed{
\text{the regular tetrahedron, regular octahedron, or regular icosahedron}.
}
\tag{6.5}
\]

The cube and dodecahedron show that triangulation cannot be omitted. The
classification fixes the embedded geometry and total row rate, not every
individual active rate.

### Theorem 6.4 — quantitative near-rigidity

Let

\[
p_{ij}=\frac{a_{ij}}{r_i},
\qquad m_i=\frac2{r_i}.
\tag{6.6}
\]

Then

\[
\boxed{
Q_i-1=
\sum_jp_{ij}
\left(\frac{\ell_{ij}}{m_i}-1\right)^2.
}
\tag{6.7}
\]

If `Q_i<=1+epsilon` and every active normalized weight is at least `p_*>0`,
put

\[
\delta=\sqrt{\epsilon/p_*}<1,
\qquad
\kappa=\frac{1+\delta}{1-\delta}.
\tag{6.8}
\]

Each active edge has relative loss error at most `delta`; neighboring row rates
are within a factor `kappa`; and a graph of active diameter `D` gives the
explicit global ratio factor `kappa^(2D+1)`.

An additive version follows from a raw gap bound together with lower row-rate
and active-rate floors. A rare-active-edge family proves that no uniform
edgewise theorem follows from small weighted variance alone. Edge-metric
stability does not imply coordinate-space stability without an additional
framework-rigidity singular-value margin.

---

## 7. Sharp product-graph barrier

For the square equal-angle product family, let

\[
h=\frac{\pi}{2N},
\qquad M=2N.
\tag{7.1}
\]

### Theorem 7.1 — exact polar graph-class minimax value

On the fixed unreduced latitude--longitude adjacency graph, every positive
shared-conductance degree-one-exact operator has polar row rate

\[
\boxed{
r_{\rm pole}(N)=
\frac1{2\sin^2(\pi/(2N))}
+
\frac1{2\sin^4(\pi/(2N))}.
}
\tag{7.2}
\]

The result does not assume ring-symmetric conductances. At one polar node, the
transverse coordinate forces the two azimuthal rates to agree, the axial
coordinate fixes the inward rate, and the remaining horizontal coordinate
fixes the azimuthal rate. The existing positive reversible construction
attains this row and has no larger interior rate. Therefore (7.2) is the exact
minimax value over the graph class.

In particular,

\[
\boxed{r_{\max}\ge\frac8{\pi^4}N^4.}
\tag{7.3}
\]

The sharp leading constant is `8/pi^4`.

### Theorem 7.2 — uniform asymptotic expansion

For every integer `N>=2`,

\[
0\le r_{\rm pole}(N)-
\left(
\frac8{\pi^4}N^4+
\frac{10}{3\pi^2}N^2+
\frac{13}{45}
\right)
\le\frac{\pi^2}{48N^2},
\tag{7.4}
\]

and

\[
0\le Q_{\rm pole}(N)-
\left(\frac1{\pi^2}N^2+\frac7{12}\right)
\le\frac{\pi^2}{12N^2}.
\tag{7.5}
\]

These are all-order analytic statements, not fitted slopes.

---

## 8. Universal and extremal rate barriers

### Theorem 8.1 — universal inverse-quadratic implication

If degree-one exactness gives `4<=r_i epsilon_i` and

\[
\varepsilon_i\le Ch^2,
\]

then

\[
\boxed{r_i\ge\frac4{Ch^2}.}
\tag{8.1}
\]

If every active loss lies in

\[
\frac2{\pi^2}h^2\le\ell_{ij}\le2h^2,
\tag{8.2}
\]

then

\[
\boxed{
1\le h^2r_i\le\pi^2,
\qquad
\frac4{\pi^2}h^2\le\varepsilon_i\le4h^2.
}
\tag{8.3}
\]

Positive spherical-Delaunay existence and exact coordinate modes are external
inputs unless separately formalized.

### Theorem 8.2 — constrained extremal lower bound and existence

Fix rate, degree, locality, separation, mesh-ratio, mass, positivity, and
reversibility constraints as in the Prompt 4 extremal class. Let `E_K` be the
minimum possible maximum defect under `r_max<=RK`. Then, whenever the class is
nonempty,

\[
\boxed{E_K\ge\frac4{RK},}
\tag{8.4}
\]

and hence

\[
\boxed{C^*:=\liminf_{K\to\infty}K E_K\ge\frac4R.}
\tag{8.5}
\]

For fixed `K`, the closed feasible class is compact and a minimizer exists.
The product graph, with `K=2N^2`, has `r_max>=2K^2/pi^4`, and therefore is
eventually excluded from every fixed linear-rate class. Quasi-uniform
families with `K comparable to h^-2` are compatible with such a rate cap.

---

## 9. A priori anisotropy of the feasible cone

At one row, let `v_j` be the tangent increments and `ell_j>0` the normal
losses. Define

\[
\mathcal P=
\left\{p\ge0:\sum_jp_j=1,
\quad\sum_jp_jv_j=0\right\}.
\tag{9.1}
\]

For `m(p)=sum p_j ell_j` and `s_2(p)=sum p_j ell_j^2`, every feasible row has

\[
Q=\frac{s_2(p)}{m(p)^2}.
\tag{9.2}
\]

For each attainable mean `m`, let

\[
\Psi(m)=\min
\left\{\sum_jp_j\ell_j^2:
 p\in\mathcal P,
 \sum_jp_j\ell_j=m\right\}.
\tag{9.3}
\]

### Theorem 9.1 — exact cone anisotropy constant and dual

\[
\boxed{
A=\min_m\left(\frac{\Psi(m)}{m^2}-1\right)
=\inf_{\text{feasible rows}}(Q-1).
}
\tag{9.4}
\]

For each `m`,

\[
\boxed{
\Psi(m)=
\max_{\alpha,\beta,z}
\left\{
\alpha+\beta m:
\alpha+\beta\ell_j+z\cdot v_j\le\ell_j^2
\ \forall j
\right\}.
}
\tag{9.5}
\]

Thus every dual-feasible triple is an explicit a priori certificate. The
constant is zero exactly when a tangent-balanced probability measure is
supported on one loss level.

For two opposite tangent directions with losses `ell_1,ell_2`,

\[
\boxed{A=rac{(\ell_1-\ell_2)^2}{(\ell_1+\ell_2)^2}.}
\tag{9.6}
\]

At the product-grid pole, the projective tangent solution is unique and
`A=Q_pole-1`, which grows quadratically in `N`.

---

## 10. Signed and positive boundary examples

The theorem hypotheses are delimited by exact examples:

1. tetrahedron, octahedron, and cube: nonzero form spaces consisting entirely
   of sampling aliases;
2. four cardinal points with a negative antipodal rate: one restored sampled
   quadratic mode;
3. signed regular pentagon: irreducible equivariance with a full quadratic
   sampled space, disproving signed equivariant rigidity;
4. Boolean square: a nonzero centered resonant square with positive constant
   carré du champ;
5. cube and dodecahedron: exact `Q=1` without triangular support;
6. rare active edge: small equality defect without edgewise control;
7. sparse centered local rows with an exact global Farkas obstruction;
8. one-to-one reduced-ring coupling: incidence forces equal neighboring ring
   populations.

These are regression controls, not evidence for the general theorems.

---

## 11. High-ambition branches

- Delsarte/Gegenbauer: `BLOCKED`; no new dual certificate survived sampling
  kernels and aliases.
- Bakry--Émery: `KILLED` for this stage; the computed `Gamma_2` identity only
  rewrites centered resonance on one eigenfunction and gives no full curvature
  theorem.
- Compact homogeneous spaces: `DEFERRED`; no second space strengthened the
  central theorem without substantial new representation theory.
- Discrete transport metrics: `DEFERRED`; continuum `W_2` contraction is not
  inferred from positivity.
- Reduced-ring graphs: `PROVED` only for the biregular/perfect-matching
  coupling class; general split/merge constructions remain numerical-analysis
  work.
- Formal discrete geometry: deliberately bounded to accepted finite algebra.

---

## 12. Verification boundary

Lean verifies selected finite algebra:

- local scaling and antipodal budgets;
- shared-edge balance, certificates, and complementarity;
- covariance and product identities;
- sampling-kernel and range formulas;
- exact equality propagation and local stability;
- polar rate uniqueness and coefficient extraction;
- universal and finite extremal inequalities;
- sharp two-loss anisotropy and reduced-ring incidence.

Ordinary proofs supply the finite convex-geometric equivalences, analytic
remainder estimate, LP dual transfer, compactness, graph classification, and
path induction. No user-declared axioms or proof placeholders are permitted.

Exact symbolic programs check rational and algebraic examples, determinants,
asymptotic coefficients, remainder constants, and adversarial families. Their
role is falsification and reproducibility, not proof of the general results.

---

## 13. Publication claim

The defensible central contribution is not a generic rank identity or a
rowwise restatement of positive-stencil theory. It is the integrated theorem
that the quadratic residual of a finite eigenmap generator factors through the
actual sampling map, together with structural positive rigidity, exact alias
classification, and signed boundary examples. The spherical feasibility,
shared-edge compatibility, equality classification, quantitative stability,
sharp product obstruction, constrained extremal lower bound, and cone
anisotropy theorem form a coherent supporting package.

The package does not claim priority for positive spherical Laplacians,
positive stencils, Farkas duality, spherical designs, association schemes,
weighted variance, Cauchy rigidity, curvature frameworks, or discrete
transport metrics. Those are precise adjacent inputs recorded in the prior-art
map.

## Reconciled stronger Prompt 3 companion theorem

The final hierarchy remains unchanged at the top: the sampled quadratic
covariance factorization is the candidate central theorem.  It is now joined by
a stronger accepted Prompt 3 companion theorem.

For a connected positive reversible coordinate eigenmap on `S^2`, exact
`Q_i=1` fixes every active loss and propagates one row rate.  If the active
support is exactly an injective, noncrossing, nondegenerate minor-arc
triangulation covering the round sphere without cone defect, the realization
is the regular tetrahedral, octahedral, or icosahedral triangulation.  Under
`p_ij>=kappa` and `Q_i<=1+eta`, the package gives explicit local, path,
diameter, graph-center, Poincaré, effective-resistance, loss, and geodesic
bounds.  The Gram/Heron determinant supplies an explicit positive angle
certificate and closed threshold `eta_*=kappa delta_*^2` for Platonic type and
edge-length sup-distance.

The covariance theorem is restricted to `0<ell<2`; the valid antipodal
boundary `ell=2`, `r=1`, `C=4 Omega Omega^T` is separate.  The weighted
octahedron proves that exact scalar quality does not control tangential
anisotropy, while an exact determinant certificate still gives genuine sampled
degree-two space `{0}`.

Prompt 4 remains supporting sharp-barrier and extremal theory.  Its exact
remainder constants, fixed-graph obstruction, universal rate bound,
constrained extremal class, feasible-cone formula, dual anisotropy certificate,
and reduced-ring obstruction are preserved without theorem-level rewrite.

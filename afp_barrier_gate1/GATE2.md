# Gate 2 closure: source audit, compatibility theory, and Lean verification

**Audit date:** 18 July 2026  
**Primary implementation audited:** [`CBienvenue/Radiant.jl`](https://github.com/CBienvenue/Radiant.jl/tree/205e07faa105854b0f27e95a02f01ebed08f84c1)  
**Primary paper:** C. Bienvenue, A. Naceur, J.-F. Carrier, and A. Hébert, “A Flexible, Moment-Preserving, and Monotone Discretization of the Multidimensional Angular Fokker–Planck Operator,” *Nuclear Science and Engineering* (2025), DOI: [10.1080/00295639.2025.2462891](https://doi.org/10.1080/00295639.2025.2462891).

## Decision

**Gate 2 passes with a narrowed publication claim.**

The standard finite-jump carré-du-champ identity is not claimed as new. The project’s defensible contribution is the AFP-specific combination of:

1. an explicit complete-degree-two obstruction for finite monotone AFP matrices;
2. a precise reversible shared-edge formulation matching the published implementation;
3. an exact dense existence theorem for centered quadratures;
4. a cone/duality framework for local positive compatibility;
5. an optimal degree-two-defect linear program with rigorous dual certificates.

The remaining local-graph positivity theorem and asymptotic defect theorem are the next research stage, not unresolved Gate 2 scope questions.

---

# Resolution of the five Gate 2 questions

## 1. Does the weighted-adjoint convention match Charles Bienvenue’s AFP matrix?

**Yes, after one important clarification: the unshifted finite-difference AFP operator is already weighted self-adjoint.**

Radiant constructs one coefficient `γ[e]` for each unordered Voronoi/Delaunay edge. The matrix assembly is

```julia
M[n,m] += γ[e] / w[n]
M[n,n] -= γ[e] / w[n]
```

so its action before stabilization is exactly

\[
(Lf)_i=\frac{1}{w_i}\sum_{j\sim i}\gamma_{ij}(f_j-f_i),
\qquad \gamma_{ij}=\gamma_{ji}.
\]

Consequently,

\[
w_iL_{ij}=\gamma_{ij}=w_jL_{ji},
\]

or

\[
WL=L^{T}W.
\]

Thus the weighted adjoint satisfies

\[
W^{-1}L^{T}W=L.
\]

The general `ForwardAdjoint.lean` reduction remains correct, but for Charles’s shared-edge matrix it collapses to the same operator. `ReversibleConductance.lean` now formalizes this detailed-balance identity.

Radiant subsequently shifts the diagonal by `λ₀` to create a nonnegative scattering matrix and applies the corresponding total-cross-section correction. The no-go and defect theorems concern the **unshifted AFP generator**, not the shifted scattering matrix in isolation.

Implementation sources:

- [`fokker_planck_weights_3D`](https://github.com/CBienvenue/Radiant.jl/blob/205e07faa105854b0f27e95a02f01ebed08f84c1/src/tools/voronoi.jl#L225-L264)
- [3D matrix assembly](https://github.com/CBienvenue/Radiant.jl/blob/205e07faa105854b0f27e95a02f01ebed08f84c1/src/particle_transport/fokker_planck_finite_difference.jl)

**Conclusion:** Question 1 is closed.

---

## 2. Is the complete-degree-two incompatibility theorem already explicit in AFP literature?

**It was not located in Charles’s paper, Radiant, or the principal AFP references cited there.**

The sources consistently distinguish two constructions:

- monotone finite differences preserving the constant and degree-one modes;
- Galerkin or differential-quadrature constructions preserving higher modes but not possessing the same local monotone jump structure.

The 2007 Morel–Larsen–Miller construction and the 2025 Bienvenue construction state degree-one moment preservation. Neither source located in this audit states the theorem

> a finite conservative monotone AFP jump matrix that is exact on the complete degree-one eigenspace cannot also be exact on the complete degree-two eigenspace.

The mechanism is nevertheless a standard Markov-generator chain-rule obstruction. Therefore the correct novelty wording is:

> **apparently the first explicit AFP specialization and quantitative design consequence, subject to specialist priority confirmation**,

not a claim that the underlying carré-du-champ principle is new.

References checked:

- Bienvenue et al. (2025), DOI above.
- E. W. Larsen, W. F. Miller Jr., and C. D. Morel, “A Discretization Scheme for the Three-Dimensional Angular Fokker–Planck Operator,” *Nuclear Science and Engineering* 156 (2007), DOI: [10.13182/NSE07-A2693](https://doi.org/10.13182/NSE07-A2693).
- The AFP source files and documentation in Radiant.

**Conclusion:** Question 2 is closed as a documented search conclusion, not as a logically absolute proof that no unpublished or obscure source contains the statement.

---

## 3. Is Charles’s shared-edge system equivalent to a known spherical Delaunay/cotangent Laplacian?

**It belongs to the same normalized reversible graph-Laplacian class, but it is not generally the same canonical operator.**

A canonical spherical Delaunay Laplacian has the form

\[
(\Delta_{\mathrm{geom}}f)_i
=\frac{1}{d_i}\sum_{j\sim i}c_{ij}(f_j-f_i),
\qquad c_{ij}=c_{ji},
\]

with edge and vertex weights derived from spherical geometry. Izmestiev and Lam prove nonnegativity under the Delaunay condition and identify exact eigenvalue `-2` modes arising from infinitesimal isometric deformations. For an inscribed polyhedron, translations yield the coordinate functions.

Charles’s operator is

\[
(Lf)_i=\frac{1}{w_i}\sum_{j\sim i}\gamma_{ij}(f_j-f_i),
\]

where `w_i` are externally prescribed quadrature weights and `γ` is solved from the degree-one moment equations.

On a connected graph, the two operators agree up to an overall scale only when

\[
w_i=\alpha d_i\quad\text{for every }i,
\qquad
\gamma_{ij}=\alpha\beta c_{ij}
\]

for constants `α>0` and operator scale `β>0`. Arbitrary Lebedev, Carlson, or product quadrature weights need not equal the canonical geometric vertex weights.

Thus:

- the adjacency is spherical Voronoi/Delaunay;
- the algebraic operator class is the same;
- the canonical geometric and quadrature-adapted operators are generally different members of that class.

Reference:

- I. Izmestiev and W. Y. Lam, “Discrete Laplacians — spherical and hyperbolic,” *Journal of the London Mathematical Society* (2025), DOI: [10.1112/jlms.70235](https://doi.org/10.1112/jlms.70235).

**Conclusion:** Question 3 is closed.

---

## 4. Which hypotheses guarantee an exact positive degree-one shared-edge solution?

There are three distinct answers, depending on the allowed graph.

### 4.1 Unrestricted complete graph: a necessary-and-sufficient theorem

Let

\[
W=\sum_i w_i,
\qquad w_i>0,
\]

and suppose the quadrature is weighted centered:

\[
\sum_i w_i\Omega_i=0.
\]

For any target eigenvalue `λ>0`, define

\[
\gamma_{ij}=\frac{\lambda w_iw_j}{W}
\quad(i\ne j).
\]

Then

\[
(Lf)_i=\frac{1}{w_i}\sum_j\gamma_{ij}(f_j-f_i)
\]

satisfies

\[
L(\Omega\cdot v)=-\lambda(\Omega\cdot v)
\]

for every vector `v`. Every off-diagonal conductance is strictly positive.

Conversely, for any reversible conductance operator and nonzero eigenvalue, exact coordinate eigenmodes imply

\[
\sum_i w_i\Omega_i=0.
\]

Therefore weighted centering is necessary and sufficient for a **dense strictly positive reversible** degree-one-exact operator. This result is formalized in `CompleteGraph.lean`.

Lebedev’s octahedral symmetry, Carlson/level symmetry, and symmetric product quadratures provide weighted centering when their paired or orbit-related weights agree.

### 4.2 Prescribed local graph: exact cone criterion

For one variable `γ_e` per allowed undirected edge, define the equilibrium matrix `A` by giving edge `e={i,j}` the column

\[
A_e|_i=\Omega_j-\Omega_i,
\qquad
A_e|_j=\Omega_i-\Omega_j.
\]

The required load is

\[
b_i=-\lambda w_i\Omega_i.
\]

Then a nonnegative local solution exists exactly when

\[
b\in\operatorname{cone}\{A_e:e\in E\}.
\]

A strictly positive solution exists when the load lies in the appropriate relative interior after redundant edge columns are removed. This is the complete finite-dimensional compatibility condition.

### 4.3 Convex triangulated/Delaunay graph

If the embedded edge framework is infinitesimally rigid, then the range of `A` is the orthogonal complement of rigid motions. The radial load above is automatically orthogonal to rotations and is orthogonal to translations precisely when the quadrature is centered. Hence:

> An infinitesimally rigid spherical triangulation plus weighted centering guarantees a unique **signed** exact shared-edge solution when the edge count is `3N-6`.

Positivity is additional and is not implied by rigidity alone.

The canonical Izmestiev–Lam Delaunay weights give a positive exact solution for their matched geometric vertex weights. For arbitrary prescribed quadrature weights, positivity is governed by the cone criterion.

Charles’s paper reports positive exact solutions for all tested product, level-symmetric, and Lebedev cases, but does not prove positivity for every order. The Radiant implementation checks full column rank through `pinv(Γ)Γ≈I`; a stronger implementation audit should also check

```julia
norm(Γ * γ - Q)
minimum(γ)
```

because full column rank alone does not establish right-hand-side compatibility or positivity for a general overdetermined system.

**Conclusion:** Question 4 is closed at the theorem/criterion level. Proving that every member of a specific infinite quadrature family lies in the positive cone remains a publishable next theorem.

---

## 5. Can the LP dual provide geometric infeasibility and optimality certificates?

**Yes.**

For the positive feasibility problem

\[
A\gamma=b,
\qquad \gamma\ge0,
\]

Farkas duality gives a certificate of infeasibility: if there is a nodal vector field `y` such that

\[
A^Ty\ge0,
\qquad
b\cdot y<0,
\]

then no nonnegative conductance solution exists.

For edge `e={i,j}`,

\[
(A^Ty)_e
=(\Omega_j-\Omega_i)\cdot(y_i-y_j).
\]

Thus a dual certificate is a nodal displacement field whose permitted edges satisfy one-sided infinitesimal length inequalities while its work against the required radial load has the wrong sign. This gives a geometric obstruction rather than only a failed numerical solve.

For the defect-minimizing LP

\[
\min_{\gamma\ge0} c\cdot\gamma
\quad\text{subject to}\quad A\gamma=b,
\]

its dual is

\[
\max_y b\cdot y
\quad\text{subject to}\quad A^Ty\le c.
\]

Every dual-feasible `y` gives a rigorous lower bound on the unavoidable defect. A primal/dual pair with equal objective values is a machine-checkable optimality certificate.

`DualCertificate.lean` formalizes:

- the finite transpose/bilinear identity;
- soundness of negative-work infeasibility certificates;
- weak duality for the positive equality-constrained LP.

Full Farkas completeness and strong duality are standard finite-dimensional results and are not claimed as new here.

**Conclusion:** Question 5 is closed.

---

# Implementation audit finding

Radiant currently uses

```julia
pinv_Γ = pinv(Γ)
if norm(pinv_Γ*Γ-I) > tolerance
    error(...)
end
γ = pinv_Γ*Q
```

The first check verifies full column rank. For a general overdetermined system it does not itself verify that `Q` lies in the column space. The mathematically complete runtime validation is:

```julia
γ = pinv(Γ) * Q
residual = norm(Γ * γ - Q)
minimum_weight = minimum(γ)
```

with declared tolerances. A dual LP can additionally produce a rigorous infeasibility or optimality certificate.

---

# Final scoped publication claim after Gate 2

The paper should not claim a new carré-du-champ principle. It may claim, subject to final AFP-specialist review:

> A finite conservative monotone AFP jump discretization cannot preserve the complete degree-one and degree-two spherical-harmonic eigenspaces simultaneously. For degree-one-exact reversible shared-edge operators, the unavoidable degree-two defect is an explicit positive quadratic variation obeying a sharp defect–stiffness inequality. Weighted centering exactly characterizes dense positive feasibility, while local positive feasibility and defect minimization admit cone and dual certificate formulations.

# Next gate

Gate 3 should prove at least one family-level local positivity or asymptotic theorem and compare the defect-minimizing LP against the existing pseudoinverse construction in Radiant.

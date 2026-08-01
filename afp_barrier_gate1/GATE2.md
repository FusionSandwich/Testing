# Gate 2 closure: Charles Bienvenue source audit, compatibility theory, and Lean verification

**Closed:** 18 July 2026  
**Radiant commit audited:** [`205e07faa105854b0f27e95a02f01ebed08f84c1`](https://github.com/CBienvenue/Radiant.jl/tree/205e07faa105854b0f27e95a02f01ebed08f84c1)  
**Primary paper:** C. Bienvenue, A. Naceur, J.-F. Carrier, and A. Hébert, “A Flexible, Moment-Preserving, and Monotone Discretization of the Multidimensional Angular Fokker–Planck Operator,” *Nuclear Science and Engineering* (2025), DOI: [10.1080/00295639.2025.2462891](https://doi.org/10.1080/00295639.2025.2462891).

## Decision

**Gate 2 passes with a narrowed publication claim.**

The finite-jump carré-du-champ identity and the generic jump-versus-diffusion chain-rule obstruction are standard and are not claimed as new. The candidate contribution is the AFP-specific combination of:

1. an explicit complete-degree-two obstruction for finite monotone AFP matrices;
2. an exact reversible shared-edge formulation matching Radiant;
3. a dense positive existence theorem for weighted-centered quadratures;
4. a cone and dual-certificate theory for local positive compatibility;
5. an optimal unavoidable-degree-two-defect linear program;
6. a source-pinned audit of product, Carlson, and Lebedev quadratures.

A final specialist review remains advisable before asserting priority, but the five Gate 2 technical questions are resolved.

---

# 1. Weighted-adjoint convention and Radiant matrix orientation

## Answer

The unshifted multidimensional finite-difference AFP matrix in Radiant is already self-adjoint in the quadrature-weighted inner product.

Radiant creates one coefficient `gamma[e]` for each unordered spherical Voronoi/Delaunay edge and assembles

```julia
M[n,m] += gamma[e] / w[n]
M[n,n] -= gamma[e] / w[n]
```

so

\[
(Lf)_i=\frac1{w_i}\sum_{j\sim i}\gamma_{ij}(f_j-f_i),
\qquad \gamma_{ij}=\gamma_{ji}.
\]

Hence

\[
w_iL_{ij}=\gamma_{ij}=w_jL_{ji},
\qquad WL=L^TW,
\qquad W^{-1}L^TW=L.
\]

The general weighted-adjoint reduction remains correct, but for Charles’s shared-edge matrix it returns the same operator.

Radiant later adds a scalar diagonal shift to form a nonnegative scattering matrix and applies the corresponding total-cross-section correction. Those two terms cancel in the transport equation. The no-go and defect theorems therefore concern the unshifted generator, not the shifted scattering matrix in isolation.

## Lean verification

- `ForwardAdjoint.lean`: general forward-matrix conversion.
- `ReversibleConductance.lean`: detailed balance, weighted conservation, and self-adjoint rates.
- `ImplementationConvention.lean`: full row-matrix action and exact diagonal-shift cancellation.

**Question 1: closed.**

---

# 2. Is the complete-degree-two obstruction already explicit in AFP literature?

## Answer

No explicit statement was located in Bienvenue et al. (2025), Radiant, or the principal AFP references checked, including the 2007 three-dimensional discretization paper.

The audited sources distinguish:

- monotone finite-difference schemes preserving constants and the complete degree-one space; and
- Galerkin or differential-quadrature schemes preserving higher modes without the same positive finite-jump structure.

The searched AFP sources do not state:

> No finite conservative monotone AFP jump matrix can be exact on both the complete degree-one and complete degree-two spherical-harmonic eigenspaces.

The proof mechanism is nevertheless a standard Markov-generator chain-rule obstruction. The defensible wording is therefore:

> an apparently new explicit AFP specialization, exact defect formula, and design consequence, subject to final specialist priority confirmation.

It would be inaccurate to claim discovery of the general carré-du-champ principle.

**Question 2: closed as a documented source audit, not as a logically absolute proof that no obscure or unpublished source contains the statement.**

---

# 3. Relation to spherical Delaunay/cotangent Laplacians

## Answer

Charles’s operator and the Izmestiev–Lam spherical Delaunay Laplacian belong to the same normalized reversible graph-Laplacian class:

\[
(Lf)_i=\frac1{m_i}\sum_{j\sim i}c_{ij}(f_j-f_i),
\qquad c_{ij}=c_{ji}.
\]

They are not generally the same canonical operator.

- In a geometric spherical Delaunay Laplacian, both edge conductances and vertex masses are determined by the spherical geometry.
- In Radiant, the masses are externally prescribed quadrature weights `w_i`, and `gamma_ij` is solved from the degree-one moment equations.

On a connected graph, a geometric pair `(c,d)` and an AFP pair `(gamma,w)` describe the same normalized operator up to an operator scale only when

\[
w_i=\alpha d_i,
\qquad
\gamma_{ij}=\alpha\beta c_{ij}
\]

for constants `alpha>0` and `beta>0`.

Thus the two constructions have:

- the same spherical Voronoi/Delaunay adjacency language;
- the same reversible normalized-graph algebra;
- generally different vertex masses and edge conductances.

`ScalingCompatibility.lean` verifies the common-scaling transfer algebra. The geometric positivity theorem remains an external input from Izmestiev and Lam.

**Question 3: closed.**

---

# 4. Conditions for an exact positive degree-one shared-edge solution

There are three levels of answer.

## 4.1 Complete graph: necessary and sufficient

Let positive weights satisfy

\[
W=\sum_iw_i>0,
\qquad
\sum_iw_i\Omega_i=0.
\]

For target eigenvalue `lambda>0`, define

\[
\gamma_{ij}=\frac{\lambda w_iw_j}{W}
\quad(i\ne j).
\]

Then every conductance is strictly positive and

\[
L(\Omega\cdot v)=-\lambda(\Omega\cdot v)
\]

for every vector `v`. In fact, the complete graph acts as `-lambda` on every sampled function of zero weighted mean.

Conversely, weighted conservation implies that every nonzero eigenmode of a reversible conductance operator has zero weighted mean. Therefore exact coordinate modes imply

\[
\sum_iw_i\Omega_i=0.
\]

Hence:

> Weighted centering is necessary and sufficient for a dense strictly positive reversible degree-one-exact construction.

This is kernel-verified in `CompleteGraph.lean`.

## 4.2 Prescribed local graph: exact cone criterion

Give every permitted undirected edge `e={i,j}` one variable `gamma_e`. Let the equilibrium matrix column for `e` have nodal blocks

\[
A_e|_i=\Omega_j-\Omega_i,
\qquad
A_e|_j=\Omega_i-\Omega_j,
\]

and define the radial load

\[
b_i=-\lambda w_i\Omega_i.
\]

Then

\[
\exists\gamma\ge0: A\gamma=b
\quad\Longleftrightarrow\quad
b\in\operatorname{cone}\{A_e:e\in E\}.
\]

Strict positivity is the corresponding relative-interior condition after redundant columns are handled.

## 4.3 Infinitesimally rigid triangulation

When the embedded framework is infinitesimally rigid, the signed equilibrium system has the expected range: the radial load is automatically orthogonal to rotations and is orthogonal to translations exactly when the quadrature is weighted-centered. Under the expected rank and edge-count conditions this gives a unique signed exact solution.

Positivity is additional. Rigidity alone does not imply that the load lies in the positive cone.

## Radiant implementation audit

Radiant checks approximately

```julia
pinv(Gamma) * Gamma == I
```

which verifies full column rank. For a general overdetermined system, a complete runtime validation should also record

```julia
gamma = pinv(Gamma) * Q
norm(Gamma * gamma - Q)
minimum(gamma)
```

with explicit tolerances. A reusable validation helper is included in `radiant_audit/validation_patch.jl`.

**Question 4: closed at the theorem and finite-dimensional criterion level. A family-wide local positivity theorem remains a Gate 3 research target.**

---

# 5. Geometric dual certificates

## Answer

Yes.

For positive feasibility

\[
A\gamma=b,
\qquad \gamma\ge0,
\]

any nodal dual vector field `y` satisfying

\[
A^Ty\ge0,
\qquad b\cdot y<0
\]

certifies infeasibility.

For edge `e={i,j}`,

\[
(A^Ty)_e=(\Omega_j-\Omega_i)\cdot(y_i-y_j),
\]

so the certificate has a geometric interpretation as a one-sided infinitesimal edge-length condition with negative work against the radial load.

For the defect-minimizing problem

\[
\min_{\gamma\ge0}c\cdot\gamma
\quad\text{subject to}\quad A\gamma=b,
\]

the dual is

\[
\max_y b\cdot y
\quad\text{subject to}\quad A^Ty\le c.
\]

Every dual-feasible vector gives a rigorous lower bound. Equal primal and dual objectives provide a compact optimality certificate.

`DualCertificate.lean` verifies the finite transpose identity, soundness of negative-work infeasibility certificates, and positive-LP weak duality. Full Farkas completeness and strong duality are standard finite-dimensional results and are not claimed as new.

**Question 5: closed.**

---

# Source-pinned Radiant audit

GitHub Actions evaluated ten finite cases at Radiant commit `205e07faa105854b0f27e95a02f01ebed08f84c1`:

- Gauss–Legendre–Chebyshev orders 2, 3, and 4;
- Carlson orders 2, 4, and 6;
- Lebedev orders 3, 5, 7, and 9.

All ten passed.

For every case:

- the weighted centroid was zero to roundoff;
- the equilibrium matrix had full column rank;
- Radiant’s pseudoinverse coefficients were strictly positive;
- the `-2` coordinate-balance residual was below `4e-15`;
- no negative conductance was found;
- the first-mode eigenrelation held to roundoff;
- the exact degree-two defect identity held to roundoff;
- the sharp Lean-verified inequality `4 <= rate_i * defect_i` held at every node.

The full table is in [`radiant_audit/radiant_afp_audit.md`](radiant_audit/radiant_afp_audit.md).

Audit provenance:

```text
GitHub Actions run: 29634439040
Artifact SHA-256: 3d395c99deb3cc73bcfb4c445a0f9425572994ccd7c4d4705e934e34f981ab81
Julia: 1.10.11
```

These are finite-instance certificates, not a proof for every order in an infinite family.

---

# Lean verification record

The expanded Gate 2 source was kernel-checked at source commit

```text
f48c52fc1b62834707a847880454b3dadda03c6d
```

GitHub Actions run `29634626374` passed:

- Lean `4.30.0`;
- Lake `5.0.0`;
- `lake build`: 2,955 jobs, success;
- axiom audit: 53 public theorem entries;
- no `sorryAx`;
- no `sorry` or `admit` placeholders;
- no user-declared axioms.

Artifact provenance:

```text
Artifact ID: 8426685500
Artifact SHA-256: e91e67114ad32a916eef6811c1e0a3916e42889e4007befc00fc62501b338eec
Built PR merge commit: e2378c5b4dbff3fec02475ca2523f2f0e635522e
```

The axiom report contains only the standard Mathlib foundations `propext`, `Classical.choice`, and `Quot.sound`.

---

# Final scoped publication claim after Gate 2

Subject to final AFP-specialist priority review, the manuscript may state:

> A finite conservative monotone AFP jump discretization cannot preserve the complete degree-one and degree-two spherical-harmonic eigenspaces simultaneously. For degree-one-exact reversible shared-edge operators, the unavoidable degree-two defect is an explicit positive quadratic variation satisfying a sharp defect–stiffness inequality. Weighted centering exactly characterizes dense positive feasibility, while local positive feasibility and defect minimization admit cone and dual-certificate formulations.

# Gate 3 target

Gate 3 should prove at least one of:

1. positive local feasibility for an infinite, practically used quadrature family;
2. a sharp `Theta(h^2)` optimal-defect theorem and corresponding `Theta(h^-2)` stiffness;
3. a dual geometric classification of infeasible local quadratures;
4. a benchmark comparison between Radiant’s pseudoinverse coefficients and the defect-minimizing positive LP.

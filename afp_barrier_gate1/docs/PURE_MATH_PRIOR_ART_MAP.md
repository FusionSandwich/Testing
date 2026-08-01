# Pure-math prior-art map — P0/M1 update

The main publication risk is that an AFP statement already exists under a
different vocabulary. This map separates standard inputs from the
sphere-specific package. It is a working priority audit, not a claim of an
exhaustive MathSciNet or zbMATH search.

## 1. Markov generators and carré-du-champ calculus

Known background includes

```text
Gamma(f,g) = 1/2 [L(fg) - f Lg - g Lf]
```

and Jensen positivity for Markov semigroups. Therefore the square identity,
weighted Cauchy–Schwarz inequality, and variance remainder are foundational,
not central novelty.

Remaining search targets:

- finite-state Markov generators with prescribed eigenfunctions;
- equality cases in Jensen or carré-du-champ identities;
- product closure of eigenspaces;
- finite-state diffusion algebras;
- eigenfunction multiplication formulas and spectral rigidity.

## 2. Positive and minimal stencils

### Principal comparator

Benjamin Seibold, *Minimal positive stencils in meshfree finite difference
methods for the Poisson equation*, Computer Methods in Applied Mechanics and
Engineering 198 (2008), 592–601, DOI `10.1016/j.cma.2008.09.001`, arXiv
`0802.2674`.

Seibold explicitly uses a finite Farkas alternative and geometric half-space /
cone criteria for local positive Poisson stencils. Consequently, the following
items are standard or close to standard and cannot be sold as the AFP result:

- local nonnegative consistency as a finite conic-feasibility problem;
- separation certificates for local infeasibility;
- geometric surrounding conditions for positive stencils;
- sparse/minimal positive selections from a larger candidate set.

The P0/M1 theorem proves the exact indexed convex-hull and relative-interior
statements directly, including repeated and redundant directions, but that
finite-convex lemma is supporting mathematics rather than the standalone
publication contribution.

### Added spherical structure not supplied by a Euclidean rowwise restatement

The completed theorem package adds all of the following simultaneously:

1. the exact decomposition
   `Omega_j = cos(theta_j) Omega_i + sin(theta_j) u_j`;
2. the fixed degree-one eigenvalue `-2` and the separate normal budget;
3. the angular renormalization
   `(1-cos(theta_j))/sin(theta_j) = tan(theta_j/2)`;
4. proof that a chosen tangent dependence has exactly one positive normal
   scale;
5. a complete division-free antipodal classification;
6. a relative cone margin with explicit minimum-coefficient, rate,
   conditioning, perturbation, and objective constants;
7. positive quadrature masses and one shared conductance per undirected edge;
8. the global cone, Farkas, LP, and complementary-slackness geometry;
9. a weighted-centered example that is locally strictly feasible but globally
   incompatible; and
10. a centered-clique mechanism that reconciles local blocks globally.

The publication argument must use this package, not the phrase “positive span.”

## 3. Finite convex geometry, oriented matroids, and LP duality

The following inputs are standard finite-dimensional results:

- convex-hull membership and barycentric coordinates;
- positive indexed barycentric coordinates and relative interior;
- minimal faces and affine-dependence descriptions of nonuniqueness;
- conic relative interior;
- Farkas alternatives;
- strong linear-programming duality and complementary slackness;
- singular-value and pseudoinverse perturbation estimates.

The shared-edge matrix is, up to sign, the transpose of a Euclidean
bar-framework rigidity matrix. Its left kernel contains translations and
rotations, so global perturbation bounds use a rigidity singular-value margin
and explicit compatibility rather than a false full-row-rank assumption.

For P0/M1, the barycentric and relative-interior equivalences are proved
explicitly rather than hidden behind a generic citation. The full Farkas and
strong-duality theorems are cited as standard external results, but the actual
AFP matrix, signs, edge blocks, objective coefficients, residual variables,
and every complementary-slackness condition are derived in
`SPHERICAL_FEASIBILITY_SHARED_EDGE_THEOREM.md`.

Oriented-matroid/circuit language is useful for minimal support and uniqueness,
but it does not remove the spherical normal equation or solve shared-edge
global compatibility. No novelty claim is made for general circuit theory.

## 4. Discrete spherical Laplacians and eigenmaps

### Principal comparator

Ivan Izmestiev and Wai Yeung Lam, *Discrete Laplacians — Spherical and
Hyperbolic*, Journal of the London Mathematical Society 112 (2025), article
e70235, DOI `10.1112/jlms.70235`, arXiv `2408.04877`.

This is a direct comparator because it develops nonnegative spherical and
hyperbolic discrete Laplacians on triangulated surfaces, relates positivity to
Delaunay structure, and proves `-2k` eigenfunction statements for discrete
conformal factors. It also connects the eigenfunctions with infinitesimal
polyhedral deformations.

The AFP package must therefore avoid broad claims such as “the first positive
spherical Laplacian with an exact `-2` mode.” The defensible distinction is the
specific arbitrary-node, arbitrary-permitted-graph feasibility theory with
positive masses, exact coordinate-vector balance, antipodal handling,
quantitative cone margins, shared-edge conductances, sparse global
compatibility, and LP dual geometry.

Remaining direct-comparison work before submission:

- compare the AFP edge column with the spherical cotangent/Delaunay weights;
- identify whether their infinitesimal deformation dual can be mapped to the
  AFP edge-strain certificate;
- determine overlap between centered-clique decompositions and polyhedral
  stress decompositions;
- compare strict positivity hypotheses and degeneracies at antipodes;
- review citation chains on spherical stresses and Colin-de-Verdière-type
  eigenmaps.

## 5. Spherical designs, distance-regular graphs, and association schemes

Search targets:

- unit-distance spherical graphs;
- Platonic and Archimedean eigenmaps;
- spherical two-distance sets;
- tight designs;
- Delsarte/Gegenbauer linear programming;
- harmonic-index designs;
- products of low-degree spherical harmonics on finite point sets.

This area supplies exact examples and is central to later `Q=1` and quadratic
exactness work. It also provides adversarial examples: cube and dodecahedron
embeddings invalidate unrestricted Platonic-only classifications.

## 6. Graph curvature

Search targets:

- `Gamma_2` on eigenfunction subspaces;
- curvature equality and rigidity;
- positive-curvature finite graphs;
- spectral-gap equality cases;
- curvature of embedded or distance-regular graphs.

No blanket finite-graph curvature-collapse conjecture is permitted.

## 7. Graph-Laplacian and manifold convergence

Search targets:

- constrained positive graph-Laplacian convergence;
- deterministic quasi-uniform point sets;
- tangent-moment consistency;
- spectral and semigroup convergence;
- monotonicity versus order;
- conditioning and perturbation estimates for positive stencils.

These topics primarily support the numerical-analysis track. The P0/M1
inverse-quadratic rate bounds are exact finite inequalities, not a continuum
convergence theorem.

## 7. Convex and linear-programming duality inputs

The following are standard finite-dimensional inputs and are cited/transferred,
not claimed as project discoveries: barycentric convex-hull representation,
supporting separation and relative interior, support-function inradius and
Hausdorff formulas, Farkas' lemma, finite LP strong duality and complementary
slackness, and pseudoinverse/Weyl singular-value inequalities.

The project-specific transfers are the spherical tangent/normal rescaling,
antipodal budget split, angle-explicit constants, shared-edge sign convention,
geometric interpretations of every dual block, and exact obstruction and
reconciliation results.

## 8. P0/M1 priority conclusion

Current defensible conclusions are:

- the local square and variance identities are standard;
- the local convex-hull/Farkas core has substantial prior art;
- the relative-interior use is standard convex geometry, though the indexed
  repeated/redundant proof is now complete;
- positive spherical Laplacians and exact low eigenmodes have direct prior art;
- the sphere-specific tangent/normal scale, division-free antipodal theorem,
  explicit quantitative margin, positive masses, shared-edge cone duality,
  weighted-centered incompatibility example, and centered-clique gluing form
  the potentially publishable combined contribution;
- no priority claim is made yet for the quadratic covariance dimension theorem,
  global equal-loss rigidity, or spectral-product hierarchy.

Before submission, complete MathSciNet/zbMATH and citation-chain review and seek
direct specialist review in positive stencils, discrete spherical geometry,
finite convexity, and reversible Markov generators.

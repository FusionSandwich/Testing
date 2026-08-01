# Pure-math prior-art map — sphere-feasibility stage

The main publication risk is that an AFP statement may already exist under a
different vocabulary. This map separates standard infrastructure from the
sphere-specific and globally reversible combination proved in this stage. It
is a priority-control document, not a claim that the literature search is
submission complete.

## 1. Markov generators and carré-du-champ calculus

Known background includes the product identity

```text
Gamma(f,g) = 1/2 [L(fg) - f Lg - g Lf]
```

and Jensen positivity for Markov semigroups. Therefore the square identity,
weighted Cauchy–Schwarz inequality, and variance remainder are not treated as
central novelty.

Search targets retained for later stages:

- finite-state Markov generators with prescribed eigenfunctions;
- equality cases in Jensen or carré-du-champ identities;
- product closure of eigenspaces;
- finite-state diffusion algebras;
- eigenfunction multiplication formulas and spectral rigidity.

## 2. Positive and minimal stencils

### Core comparator

Benjamin Seibold, *Minimal positive stencils in meshfree finite difference
methods for the Poisson equation*, Computer Methods in Applied Mechanics and
Engineering 198 (2008), 592–601; arXiv:0802.2674.

Seibold's setting already contains several ingredients that must not be claimed
as new:

- local derivative consistency is written as a finite linear system;
- positivity is imposed by nonnegative neighbor coefficients;
- local selection is a standard-form linear program;
- basic LP solutions give minimal/sparse stencils;
- geometric point-cloud conditions guarantee positive stencil existence; and
- generic meshfree rows are nonsymmetric, with conservation not automatic.

The constraints there reproduce the Euclidean Poisson operator on constants,
linear functions, and quadratic monomials. The present local tangent equation
is therefore adjacent to established positive-stencil geometry. Merely saying
that directions must positively surround the origin, or citing Farkas for one
row, is not a publication contribution.

### Distinguishing content of this stage

The theorem package being evaluated is the combination of:

1. a unit-sphere coordinate eigenmap equation with target eigenvalue `-2`;
2. exact orthogonal tangent/normal separation;
3. a normal equation that uniquely rescales every nonzero tangent dependence
   by the angular factor `(1-cos theta)/sin theta`;
4. a separate antipodal classification, where no tangent quotient exists;
5. strict positivity for every indexed candidate using relative interior,
   including repeated and redundant directions;
6. a relative cone margin with explicit all-index coefficient, rate,
   conditioning, perturbation, and objective constants;
7. positive quadrature masses; and
8. one conductance shared by both orientations of every undirected edge.

The last two items turn independent local stencil LPs into a coupled global
compatibility problem absent from a generic rowwise positive-stencil
construction.

Search targets still required before submission:

- quantitative positive-stencil coefficient lower bounds from inradius or cone
  width;
- perturbation bounds for sign-constrained stencil systems;
- conservative or symmetric meshfree positive stencils;
- mimetic and finite-volume reconciliation of independently selected rows;
- minimal positive stencils on manifolds and embedded surfaces.

## 3. Discrete spherical Laplacians and eigenmaps

### Core comparator

Ivan Izmestiev and Wai Yeung Lam, *Discrete Laplacians — Spherical and
Hyperbolic*, Journal of the London Mathematical Society 112 (2025), e70235;
arXiv:2408.04877.

That work introduces structure-preserving spherical and hyperbolic discrete
Laplacians, proves nonnegative weights exactly for Delaunay triangulations in
its setting, and obtains exact `-2k` eigenfunctions associated with discrete
conformal vector fields. Positive spherical weights and exact curvature-scale
eigenfunctions therefore predate this stage.

The present result is not a competing Delaunay construction. It fixes an
arbitrary permitted graph and asks for exact Cartesian coordinate eigenmap
rows, positive masses, and reversible shared conductances. It then gives the
local tangent/normal criterion, the global edge-column cone, exact dual
certificates, and sparse/dense compatibility mechanisms. Direct comparison of
operators, normalizations, eigenfunctions, and geometric hypotheses remains
necessary before a priority claim.

Search targets:

- exact `-2` Cartesian coordinate modes;
- convex-polyhedral and infinitesimal-rigidity interpretations;
- spherical Delaunay positivity;
- eigenmap rigidity;
- equal-edge spherical frameworks;
- stress matrices and equilibrium stresses on inscribed polyhedra; and
- quadratic products of coordinate eigenfunctions.

## 4. Finite convexity, Farkas, and linear-programming duality

The following are standard infrastructure and are not novelty claims:

- convex-hull membership as a normalized nonnegative dependence;
- positive indexed coefficients and relative-interior membership;
- supporting/separating hyperplanes for finite polytopes;
- closedness of finitely generated cones;
- Farkas' equality/nonnegative-variable alternative;
- finite LP strong duality and attainment; and
- complementary slackness.

The contribution can only lie in transferring these results to the exact AFP
edge columns and extracting sphere-specific geometry. The proof therefore
shows, rather than suppresses, all signs:

```text
(g_{pq})_p = Omega_q - Omega_p
(g_{pq})_q = Omega_p - Omega_q
b_i        = -2 w_i Omega_i
sigma_pq   = (y_p-y_q) dot (Omega_q-Omega_p)
```

The geometric interpretation of dual strain, radial work, endpoint prices,
and residual signs is part of the spherical package; the abstract duality
theorems are not.

## 5. Rigidity, stresses, and oriented matroids

The edge-column matrix is adjacent to equilibrium/rigidity matrices and the
dual strain is a first variation of squared chord length. Oriented-matroid
language also describes circuits and support-minimal tangent dependences. These
viewpoints are useful for classification and exact certificates, but they do
not by themselves prove:

- the angular normal rescaling;
- the antipodal budget;
- the quantitative all-index coefficient bound;
- mass-weighted right-hand sides;
- strict positive shared conductances; or
- the project LP dual blocks.

Search targets:

- positive self-stresses and tensegrity alternatives;
- equilibrium stresses for inscribed spherical frameworks;
- Maxwell–Cremona-type duality on the sphere;
- stress-cone relative interiors and perturbation theory; and
- oriented-matroid criteria for all-edge positive stresses.

## 6. Graph curvature

Core comparators include work on Bakry–Émery curvature matrices and curvature
functions of graphs.

Search targets:

- `Gamma_2` on eigenfunction subspaces;
- curvature equality and rigidity;
- positive-curvature finite graphs;
- spectral-gap equality cases;
- curvature of embedded or distance-regular graphs.

No blanket curvature-collapse conjecture is permitted.

## 7. Spherical designs, distance-regular graphs, and association schemes

Search targets:

- unit-distance spherical graphs;
- Platonic and Archimedean eigenmaps;
- spherical two-distance sets;
- tight designs;
- Delsarte/Gegenbauer linear programming;
- harmonic-index designs;
- products of low-degree spherical harmonics on finite point sets.

This area is particularly relevant to global `Q=1` examples and attainable
quadratic exactness. The exact cube examples in the current stage are
compatibility/certificate examples, not classification results.

## 8. Graph-Laplacian and manifold convergence

Core comparators include spectral convergence of graph Laplacians to
Laplace–Beltrami operators and meshfree maximum-principle convergence.

Search targets:

- constrained positive graph-Laplacian convergence;
- deterministic quasi-uniform point sets;
- tangent-moment consistency;
- spectral and semigroup convergence;
- monotonicity versus order;
- perturbation of reversible conductance systems.

These topics primarily support the numerical-analysis paper, but may contain
pure-math rigidity or impossibility results.

## 9. Current priority conclusion

As of this stage:

- the local square and variance identities are standard;
- positive stencil feasibility and LP selection have substantial prior art;
- positive spherical Laplacians with exact curvature-scale eigenfunctions have
  direct prior art;
- finite convexity, Farkas, and LP strong duality are standard;
- the exact AFP-specific combination of spherical tangent/normal scaling,
  antipodes, quantitative margin, positive masses, globally shared edges,
  compatibility certificates, and local/global separation may be useful; and
- no unrestricted priority claim is made for that combination until the
  rigidity/stress, conservative meshfree, and spherical-Laplacian searches are
  completed and reviewed by specialists.

Before submission, the search must include MathSciNet, zbMATH, citation chains,
and direct review by specialists in positive stencils, finite convexity,
discrete differential geometry, and rigidity theory.

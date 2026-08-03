# Pure-math prior-art map — Prompt 1 and Prompt 2

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

## 8. Convex and linear-programming duality inputs

The following are standard finite-dimensional inputs and are cited/transferred,
not claimed as project discoveries: barycentric convex-hull representation,
supporting separation and relative interior, support-function inradius and
Hausdorff formulas, Farkas' lemma, finite LP strong duality and complementary
slackness, and pseudoinverse/Weyl singular-value inequalities.

The project-specific transfers are the spherical tangent/normal rescaling,
antipodal budget split, angle-explicit constants, shared-edge sign convention,
geometric interpretations of every dual block, and exact obstruction and
reconciliation results.

## 9. P0/M1 priority conclusion

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
- this Prompt 1 review did not establish priority for the then-future
  quadratic covariance, rigidity, or spectral-product stages.

Before submission, complete MathSciNet/zbMATH and citation-chain review and seek
direct specialist review in positive stencils, discrete spherical geometry,
finite convexity, and reversible Markov generators.

## 10. Prompt 2 standard algebraic inputs

The following are standard and are labeled EXTERNAL or foundational PROVED
lemmas, never candidate novelty:

- the finite jump-product/carré-du-champ identity;
- weighted conservation under detailed balance;
- rank-nullity, kernels, images, quotients, and polynomial spectral
  projections;
- finite real Maschke semisimplicity and Schur-type arguments;
- the self-adjoint spectral theorem;
- Jensen variance, its support equality case, and finite-chain uniformization;
- tight-frame second moments;
- convex group averaging and subgradient/KKT optimality;
- the \(S^2\) Clebsch--Gordan decomposition; and
- completeness of positive solutions to the negative Pell equation.

The covariance expansion

\[
 L(\Phi^TA\Phi)
 =-2\lambda\Phi^TA\Phi+\operatorname{tr}(AC_i)
\]

is direct algebra. It cannot support an originality statement by itself.
Likewise, a finite exact rank or minor table is a certificate for an example,
not a general-theorem or priority argument.

## 11. Sampling, designs, and association-scheme boundary

Spherical designs, harmonic evaluation, distance-regular graphs, and
association schemes already provide:

- exact harmonic evaluation ranks and aliases;
- multiplicity decompositions of permutation modules;
- shell-constant eigenvalues and orbit matrices;
- tight vertex figures and tangent moments; and
- Platonic and hypercube character calculations.

Prompt 2 therefore does not claim the Platonic spectra, harmonic aliases,
Walsh characters, or tight-frame identities as new. The project-specific use
is their integration with the sampling kernel \(K_X\), residual kernel
\(E_{\rm form}\), and genuine sampled space \(E_{\rm sample}\). Any paper must
compare its formulation with finite-frame, spherical-design,
distance-regular-graph, and graph inverse-eigenvalue literature before making
a priority statement.

## 12. Equivariance and real representation theory

Equivariance of evaluation maps and multiplicity-free kernel selection are
standard finite representation theory. Real Schur's lemma does not say that
every real equivariant endomorphism is a scalar in complex or quaternionic
type. Prompt 2 instead uses the self-adjoint spectral theorem on an explicitly
preserved irreducible copy.

The two-layer \(D_3\) example is retained as a regression warning: an
equivariant operator may move one irreducible copy into another isomorphic
ambient copy. The potentially useful project result is the sampling-residual
quotient rank gap, not the standard isotypic vocabulary.

## 13. Signed restoration and optimization boundary

Symmetry reduction of a convex invariant optimization problem, orbit variables,
piecewise-linear negative-part objectives, and KKT certificates are standard.
The hypercube Hamming scheme is also standard. No novelty is claimed for those
ingredients separately.

The candidate project contribution is the precise constrained problem that
combines coordinate exactness, the full nonzero sampled quadratic module,
sampling aliases, reversible signed conductances, and undirected negative mass,
together with the exact optimum two. This claim still requires targeted review
against signed graph Laplacians, inverse eigenvalue problems, cubature with
negative weights, and invariant linear programming.

## 14. Spectral products and Pell boundary

Product decompositions of spherical harmonics and negative-Pell classifications
are EXTERNAL. The target-eigenvalue direct-sum theorem is elementary polynomial
spectral projection. The exact \(d=1\) rejection demonstrates why degree labels
cannot replace target scalars.

The conservative candidate contribution is the combined sampling-safe
interpretation: continuous product components may be killed or aliased by a
finite node set, and simultaneous exactness is constrained by the dimensions
of distinct sampled target classes. Component availability does not imply that
one product isolates it and is not a positivity obstruction.

## 15. Prompt 2 priority conclusion

The defensible boundary is:

- PROVED but standard/foundational: product and covariance expansions,
  weighted centering, finite quotient algebra, semigroup exponentiation, and
  target-eigenvalue separation;
- EXTERNAL: real semisimplicity/spectral inputs, Jensen/uniformization,
  tight-frame background, Clebsch--Gordan, and Pell completeness;
- COMPUTATIONAL: exact finite graph actions, ranks, minors, aliases, and KKT
  regressions;
- candidate combined project contribution: the sampling-kernel-aware
  covariance framework, signed one-shell full-tangent-isotropy factorization,
  positive prism sharpness, equivariant quotient rank gap, signed-cube
  negative-mass optimum, and their unified sampling-safe interpretation.

No unqualified first/novel/optimal-priority wording is authorized. Before
submission, perform targeted MathSciNet/zbMATH and citation-chain review in
finite frames and designs, discrete spherical Laplacians, association schemes,
signed inverse-eigenvalue problems, and invariant convex optimization, followed
by specialist review.

## 16. Prompt 3 equality and triangulation boundary

The weighted variance identity and equality in a finite nonnegative sum are
foundational PROVED algebra, not novelty.  Spherical cosine laws and excess,
Euler incidence identities, disk-curvature identities, links/collars in a
triangulated surface, and the classification of the three regular triangular
spherical maps are standard or EXTERNAL background.

Prompt 3 does not claim a new Platonic-solids classification in isolation.  Its
project-specific transfer is the hypothesis-audited chain from a positive
reversible coordinate eigenmap through exact `Q=1` edge-loss propagation to a
round minor-geodesic cellular triangulation, followed by a direct
separating-triangle/link proof and opposite-side face propagation.  Every use
of Euler or angle sum is confined to the ten embedded-triangulation premises.

Cube and dodecahedron remain decisive association-scheme/distance-regular
counterexamples to unrestricted wording.  The two-state antipodal model is the
separate degeneracy that prevents tangent normalization at `ell=2`.

## 17. Quantitative graph-analysis boundary

Poincare variational inequalities, reversible Dirichlet forms, and effective
resistance are EXTERNAL standard finite Markov-chain/electrical-network tools.
The spherical arccos derivative, the general spherical cosine formula, and its
Gram/Heron determinant factorization are standard trigonometry.

The Prompt 3 contribution boundary is the explicit defect transfer with its
fixed normalization:

```text
Q_i-1 -> pointwise x_ij -> shared-edge log r cocycle
      -> path/diameter/reference-loss bounds
      -> exact energy factor 2
      -> closed side-angle and integer-valence threshold.
```

No diameter-free theorem follows from only a local active-weight floor.  No
coordinate-space framework stability is claimed from edge-length control
without a separately proved rigidity-operator margin.

## 18. Covariance anisotropy and sampling boundary

The radial/tangent outer-product expansion is direct algebra and the one-shell
full-tangent-isotropy theorem is part of the verified Prompt 2 package.  Prompt
3 identifies their exact equality specialization: the Prompt 2 moment becomes
`T_i=P_i/2`, while global `Q=1` alone fixes only the radial coefficient.

The weighted-octahedron family is an exact boundary example, not a claim that
anisotropic weighted Platonic Laplacians are new.  Its role is to prevent two
false transfers: `Q=1` does not imply tangent isotropy, and a nonzero quadratic
form kernel is not a nonzero sampled exact space.

## 19. Plantri and computation boundary

Plantri (Brinkmann--McKay) is an EXTERNAL program.  The Prompt 3 workflow pins
an immutable source commit and blob, compiles that verified source in a fresh
temporary directory, and labels all counts through twelve vertices
COMPUTATIONAL.  The census is hostile falsification and regression only; the
all-orders proof is the direct ordinary argument.

No priority claim follows from a Plantri count, exact graph6 record,
automorphism order, finite minor, Lean job count, workflow status, or artifact
digest.

## 20. Prompt 4 targeted adjacent-field audit

This bounded audit rechecks the old Prompt-4 comparison against primary
sources; it is not an exhaustive MathSciNet/zbMATH priority search.  Every
literature input in this section is `EXTERNAL`.  Every project-specific theorem
named here is `PROVED`; finite exact fixtures are `COMPUTATIONAL`.

### Finite generator product calculus

Carré-du-champ product identities, Jensen inequalities for Markov semigroups,
and one-function `Gamma_2` calculations are `EXTERNAL` foundational calculus.
The Prompt-4 rate barrier is an exact specialization of weighted
Cauchy--Schwarz and is not presented as novelty.  The project-specific
contribution boundary is the combination with actual sampling, graph-class
polar uniqueness, and the constrained extremal/anisotropy structures.

### Positive and minimal stencils

Seibold's positive-stencil Farkas and half-space criteria (DOI
[`10.1016/j.cma.2008.09.001`](https://doi.org/10.1016/j.cma.2008.09.001),
arXiv [`0802.2674`](https://arxiv.org/abs/0802.2674)) remain the principal
`EXTERNAL` comparator.  Prompt 4 does not claim local cone feasibility as new.
Its distinct result is a sharp obstruction on one fixed spherical product
graph plus a conductance-aware optimization over every feasible local row.

### Discrete spherical Laplacians and eigenmaps

Izmestiev--Lam's spherical/hyperbolic discrete Laplacians
([arXiv `2408.04877`](https://arxiv.org/abs/2408.04877)) are `EXTERNAL`: their
spherical Delaunay positivity and exact low-mode conclusions must be invoked
only under their hypotheses.  The present package does not assert that a fixed
radial icosphere connectivity is Delaunay at every level.  The Prompt-4
product theorem instead fixes the unreduced adjacency and derives its polar
rates directly from the coordinate equations.

### Spherical designs, association schemes, and code LPs

Delsarte's association-scheme linear programming method (DOI
[`10.1007/BF03187604`](https://doi.org/10.1007/BF03187604)) and its
Gegenbauer/spherical-code descendants are `EXTERNAL`.  Platonic harmonic
aliases and finite ranks in this repository are `COMPUTATIONAL`.  The
proposition that a standard Delsarte reduction without a solved new dual is a
new Prompt-4 theorem is `REJECTED`: no candidate certificate survived the
sampling-kernel and cross-degree alias audit.

Unit-distance spherical graphs and association schemes supply exact examples,
not the graph-class minimax proof.  The latter begins with arbitrary polar
rates, proves uniqueness, and uses a separate positive reversible attaining
construction at every `N>=2`.

### Constrained weighted graph Laplacians

Fallat--Gupta--Lin study spectra and variance-type optimization for weighted
Laplacians with fixed support ([arXiv `2411.00292`](https://arxiv.org/abs/2411.00292));
this is an `EXTERNAL` adjacent comparator rather than a source of the present
theorems.  Prompt 4 fixes an eigenmap equilibrium, controls geometry, masses,
locality, degree, and a linear rate cap, and minimizes a defect rather than a
free support spectrum.  The lower bound `4/R` and finite-order attainment are
`PROVED`, but optimal upper bounds and convergence remain `CONJECTURE`.

### Finite-dimensional convex duality

Farkas alternatives, compact polytope minima, finite LP strong duality, and
complementary slackness are `EXTERNAL`.  What is `PROVED` here is the exact
spherical normalization, the affine-slice/projective distinction, the
arbitrary-moment invariant `Q_lambda`, the sign-correct sliced primal/dual,
and the transfer of every feasible dual triple to a rowwise certificate.

### Graph curvature

Cushing--Liu--Peyerimhoff's curvature functions
([arXiv `1606.01496`](https://arxiv.org/abs/1606.01496)) and
Cushing--Kamtue--Liu--Peyerimhoff's curvature-gap work
([arXiv `2102.08687`](https://arxiv.org/abs/2102.08687)) provide `EXTERNAL`
finite examples and rigidity frameworks.  They reject a blanket claim that
positive finite graphs have no useful positive/nonnegative curvature.  The
Prompt-4 one-function eigenmode identity is therefore a consistency check, not
a curvature-dimension theorem; the stronger formulation is `REJECTED`.

### Discrete transport metrics

Maas's finite-state transport metric ([arXiv `1102.5238`](https://arxiv.org/abs/1102.5238))
and Erbar--Maas's discrete Ricci-curvature theory
([arXiv `1111.2687`](https://arxiv.org/abs/1111.2687)) are `EXTERNAL`.
Positivity alone neither selects continuum `W_2` nor proves contraction, so
that metric-free claim is `REJECTED`.  A future theorem must name the discrete
metric and establish its curvature hypotheses.

## 21. Prompt 4 priority conclusion

The following are `EXTERNAL` or foundational and are not candidate novelty:
partial fractions and zeta values, weighted Cauchy--Schwarz, finite
compactness, LP duality, positive-stencil cone criteria, spherical-Delaunay
theory, spherical-code LPs, association-scheme examples, graph-curvature
frameworks, and discrete transport metrics.

The defensible `PROVED` supporting contributions are:

- direct asymmetric polar uniqueness and exact fixed-product-graph minimax;
- uniform polar rate and quality bounds valid for every `N>=2`;
- the fully constrained extremal lower bound, attainment, and product-family
  exclusion;
- the corrected conductance-aware `Q_lambda` feasible-family reduction,
  sliced dual certificates, equality classification, and sharp polar/two-ray
  examples; and
- the precise reduced-ring biregular/perfect-matching obstruction.

The central candidate contribution remains the Prompt-2 actual-sampling
quadratic residual factorization and positive structural rigidity.  No
unqualified first, novel, or globally optimal priority wording is authorized.
Before submission, specialist citation-chain review remains necessary in
positive stencils, discrete spherical geometry, finite frames/designs,
weighted graph inverse problems, and constrained Laplacian optimization.

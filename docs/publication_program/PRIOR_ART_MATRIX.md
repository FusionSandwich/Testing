# AFP publication program — prior-art matrix

## 1. Use policy

This matrix records external results as inputs or comparators, not as substitutes for the repository’s proofs. Every transfer must verify the external hypotheses against the AFP normalization, graph class, positivity assumptions, and sampling map.

The six sources M1–M6 were read from their primary arXiv records. The existing repository prior-art map remains a broader working bibliography and must be consulted before manuscript submission. A final MathSciNet/zbMATH and citation-chain review is still required for priority language.

## 2. Mandatory M1–M6 matrix

| ID | Primary source | External result or scope | Closest AFP overlap | AFP non-overlap / candidate contribution | Transfer status and warning |
|---|---|---|---|---|---|
| M1 | C. Babecki and R. R. Thomas, *Graphical Designs and Gale Duality*, arXiv:2204.01873 | For regular graphs, positively weighted graphical designs are related by Gale duality to faces of generalized eigenpolytopes; examples include Cayley graph families. | finite eigenvectors, positive quadrature weights, graph designs, polyhedral duality | AFP fixes a finite jump generator/eigenmap and proves a covariance residual factorization through the actual quadratic sampling map, plus positivity/shared-edge constraints | `EXTERNAL COMPARATOR`; do not claim first positive graph designs or generic Gale duality. M1 does not remove AFP sampling aliases or prove `R_X=(L+2dI)S_X`. |
| M2 | C. Babecki and D. Shiroma, *Eigenpolytope Universality and Graphical Designs*, arXiv:2209.06349 | Every polytope appears, up to affine equivalence, as an eigenpolytope of a positively weighted graph; graphical designs correspond to faces; complexity results are obtained. | positively weighted graphs, eigenpolytopes, graph quadrature, existence/complexity | AFP imposes an exact spherical coordinate eigenmap, shared conductances, local covariance, and a specified degree-two target; it studies genuine sampled exactness rather than design existence alone | `EXTERNAL COMPARATOR`; universality warns against broad geometric classification from eigenpolytope shape. |
| M3 | S. Steinerberger, *Spectral Limitations of Quadrature Rules and Generalized Spherical Designs*, arXiv:1708.08736 / IMRN | Nonnegative `n`-point quadrature rules on a compact `d`-manifold cannot integrate more than `c_d n+o(n)` initial eigenfunctions; `c_2=4`. | positive quadrature, spectral exactness, spherical designs | AFP gives exact finite structural identities and alias-aware dimensions for a prescribed generator and degree-two sample space, not an asymptotic upper bound for arbitrary quadrature | `EXTERNAL LIMITATION`; do not present the AFP finite factorization as a replacement for asymptotic quadrature bounds or vice versa. |
| M4 | I. Izmestiev and W. Y. Lam, *Discrete Laplacians—Spherical and Hyperbolic*, arXiv:2408.04877 / JLMS | Defines spherical/hyperbolic discrete Laplacians; edge weights are nonnegative exactly for Delaunay triangulations; conformal factors give `-2k` eigenfunctions; links to polyhedral deformations. | positive spherical Laplacians, `-2` spherical modes, triangulated surfaces, polyhedral geometry | AFP treats arbitrary finite positive eigenmap generators and shared conductances, exact sampling/covariance, local feasibility, restricted `Q=1` rigidity, and fixed-graph barriers | `EXTERNAL DIRECT COMPARATOR`; do not claim the first positive spherical Laplacian, Delaunay positivity theorem, or `-2` eigenmode. Verify Delaunay hypotheses before borrowing existence. |
| M5 | B. Seibold, *Minimal Positive Stencils in Meshfree Finite Difference Methods for the Poisson Equation*, arXiv:0802.2674 | Constructs minimal positive meshfree Poisson stencils and gives point-cloud geometric existence conditions. | positive local stencils, cone/Farkas geometry, minimal support | AFP’s Paper I adds exact spherical tangent/normal scaling, indexed repetitions and relative interiors, antipodal decomposition, quantitative margins, positive masses, and global shared-edge reversibility | `EXTERNAL METHOD COMPARATOR`; generic positive-stencil, cone, and Farkas language is not novelty. |
| M6 | C. Babecki, S. Steinerberger, and R. R. Thomas, *Spectrahedral Geometry of Graph Sparsifiers*, arXiv:2306.06204 | Weighted subgraphs preserving the first `k` Laplacian eigenpairs form an intersection of a polyhedron with a positive-semidefinite cone; develops geometry and scale of `k`. | fixed eigenpair preservation, weighted subgraphs, convex/spectrahedral feasible sets | AFP prescribes a spherical eigenmap and develops local/shared-edge positive feasibility, exact second-moment residuals, sampling aliases, and sharp fixed-graph rate obstructions | `EXTERNAL COMPARATOR`; do not claim generic novelty for convex feasible sets of eigenpair-preserving graph weights. |

Primary links:

```text
M1 https://arxiv.org/abs/2204.01873
M2 https://arxiv.org/abs/2209.06349
M3 https://arxiv.org/abs/1708.08736
M4 https://arxiv.org/abs/2408.04877
M5 https://arxiv.org/abs/0802.2674
M6 https://arxiv.org/abs/2306.06204
```

## 3. Additional external theorem families

| Family | Representative sources already mapped in the repository | Project use | Prohibited priority claim |
|---|---|---|---|
| Markov product calculus | carré-du-champ literature; diffusion-generator fourth-moment work; Steinerberger on products of eigenfunctions | exact finite product identities and centered-resonance boundary | generic product rule, positivity of `Gamma`, or Jensen equality is new |
| spherical designs | Delsarte–Goethals–Seidel; Bannai surveys | context for harmonic averaging and aliases | Platonic sample calculations are a new design classification |
| association schemes | Q-polynomial spherical embedding/design literature | equivariant comparators | classification of distance-regular graphs or schemes |
| convex separation and LP | standard convexity, Farkas, finite LP duality | Paper I shared-edge cone and Paper III sliced LP | generic Farkas or LP duality is new |
| planar maps | Euler identities; planar triangulation generation/classification literature | combinatorial step and hostile enumeration | finite catalog absence proves the theorem |
| convex polyhedral rigidity | Cauchy/Alexandrov-type rigidity; Connelly–Gortler stability comparators | exact geometric uniqueness after hypotheses are verified | an unstated uniform coordinate-stability constant |
| reversible chains | Poincaré inequalities, Dirichlet principle, effective resistance | Paper III global quantitative transfer | path, gap, and resistance normalizations are interchangeable without checking factors |
| trigonometric expansions | cotangent/cosecant Mittag–Leffler expansions, Bernoulli/zeta values | Prompt 4 analytic remainder | the classical expansion coefficients alone are the contribution |
| discrete transport/curvature | Maas, Erbar–Maas, graph Bakry–Émery literature | blocked future directions and consistency checks | ordinary continuum `W_2` or a one-function `Gamma_2` identity gives a full theory |

## 4. Paper-specific priority boundaries

### Paper I — feasibility and shared-edge compatibility

Safe contribution language:

- exact indexed spherical tangent/normal transfer;
- antipodal classification without fictitious tangent normalization;
- quantitative relative-inradius bounds;
- exact reversible shared-edge cone with project sign/mass conventions;
- sparse local-to-global obstruction and explicit reconciliation classes.

Do not claim:

- first positive stencil;
- first Farkas formulation of stencil feasibility;
- first convex-hull condition;
- first positive spherical Delaunay Laplacian.

### Paper II — sampled quadratic exactness

Safe contribution language:

- covariance residual factorization through the finite sampling map;
- automatic inclusion of every sampling alias in the exact-form kernel;
- genuine sampled-space intersection and rank-difference formula;
- sharp positive axial/equivariant rigidity with exact alias and signed boundaries.

Do not claim:

- generic rank-nullity;
- generic covariance expansion alone;
- generic graph quadrature or design existence;
- algebraic form dimension as sampled dimension.

### Paper III — equality geometry and sharp barriers

Safe contribution language:

- restricted round-sphere `Q=1` classification with all geometric hypotheses;
- explicit graph-global near-rigidity, spectral-gap, and resistance bounds;
- certified Gram/Heron edge-metric stability;
- exact covariance/tangent boundary and weighted-octahedral family;
- forced product-pole rates, rigorous all-`N` remainder, and rate-capped extremal/feasible-cone theory.

Do not claim:

- unrestricted Platonic classification;
- finite enumeration as proof;
- optimal stability constants;
- automatic coordinate stability;
- first spherical `-2` Laplacian;
- generic trigonometric expansion or generic LP duality.

## 5. External-transfer checklist

Before citing an external theorem as a proof step, record:

```text
the exact theorem statement;
the source version and publication;
finite versus asymptotic scope;
graph directedness and loop convention;
sign of the Laplacian/generator;
normalization of weights and inner products;
positivity and reversibility hypotheses;
sphere radius and curvature convention;
minor-arc, convexity, Delaunay, or triangulation hypotheses;
sampling injectivity or lack thereof;
factor 1/2 in the Dirichlet/Gamma form;
whether constants are quantitative and uniform;
the exact AFP conclusion transferred.
```

A citation is not a proof of a transfer whose hypotheses have not been matched.

## 6. Priority-audit status

| Program claim family | Priority status at baseline |
|---|---|
| local variance identity and product rule | standard / not flagship |
| generic cone, Farkas, and LP formulations | standard / not flagship |
| positive graph designs and eigenpolytope geometry | substantial adjacent prior art |
| spherical Delaunay Laplacians and `-2` modes | direct adjacent prior art |
| residual-through-sampling factorization and alias package | central candidate claim; still requires final specialist literature review |
| restricted global equality classification | strong companion claim; hypotheses are essential |
| explicit graph-global near-rigidity and covariance interaction | strong companion claim |
| fixed product-graph forced polar obstruction and certified remainder | supporting sharp-barrier claim |
| general higher-degree, curvature, transport, and reduced-ring extensions | rejected, conjectural, or blocked as registered |

This matrix controls manuscript wording but is not a substitute for final referee-level novelty review.

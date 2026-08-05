# Prior-art and transfer matrix

All rows are `EXTERNAL`.  The audit used the primary papers and the JLMS
version-of-record page; repository summaries are not substitutes for the
external theorem statements.

| ID / source | Exact external content used and hypotheses | Source convention / AFP conversion | Overlap and non-overlap boundary | Transfer status / paper |
|---|---|---|---|---|
| M1 — [Babecki–Thomas, Graphical Designs and Gale Duality](https://arxiv.org/abs/2204.01873) | Connected simple regular unweighted graphs: graphical designs correspond to complements of eigenpolytope faces; support-minimal designs to facet complements; a positive k-design support bound uses summed eigenspace dimensions. | Uses `AD^-1=A/delta` and a shifted normalized Laplacian with uniform vertex measure. Convert signs/eigenvalues explicitly. | Gale/eigenpolytope language overlaps design supports. It does not prove irregular weighted AFP conductance existence, locality, or spherical geometry; the complement operation is essential. | HYPOTHESES_AUDITED / I,III |
| M2 — [Babecki–Shiroma, Eigenpolytope Universality and Graphical Designs](https://arxiv.org/abs/2209.06349) | Every full-dimensional rational V-polytope is realizable as a Laplacian eigenpolytope of a connected positive rational weighted graph; design/face ideas extend to irregular weighted graphs. | Combinatorial `D-A` is positive semidefinite; AFP `L` is negative semidefinite. Graph edge weights and quadrature weights are distinct data. | Universality is existential and permissive; it need not preserve the prescribed graph, locality, spherical nodes, or sparsity. | HYPOTHESES_AUDITED / III |
| M3 — [Steinerberger, Spectral Limitations of Quadrature Rules](https://arxiv.org/abs/1708.08736) and [IMRN version](https://academic.oup.com/imrn/article/2021/16/12265/5551305) | An n-node nonnegative quadrature on a compact d-manifold integrates at most the first `c_d n+o(n)` eigenfunctions, with multiplicity and `c_d=(d/2+1)^(d/2+1)/Gamma(d/2+1)`. | Initial Laplace spectrum is positive-semidefinite; translate target signs only after fixing the full eigenspaces. | Cardinality limitation overlaps spectral design motivation. It is not sampling injectivity, nor a finite sharp theorem for arbitrarily selected degrees. | HYPOTHESES_AUDITED / I |
| M4 — [Izmestiev–Lam, Discrete Laplacians—Spherical and Hyperbolic](https://arxiv.org/abs/2408.04877), [JLMS](https://londmathsoc.onlinelibrary.wiley.com/doi/10.1112/jlms.70235) | Geodesic triangulations have specific spherical/hyperbolic coefficients; edge coefficient nonnegativity is equivalent to local Delaunay; the spherical coordinate eigenspace occurs under their geometric weights. | Their `Delta_s u_i=d_i^-1 sum c_ij(u_j-u_i)` is negative semidefinite in its weighted inner product, matching AFP sign only after identifying their particular `c_ij,d_i`. | Relevant construction geometry, but not arbitrary conductances/masses or fixed AFP locality classes. | HYPOTHESES_AUDITED / II,III |
| M5 — [Seibold, Minimal Positive Stencils](https://arxiv.org/abs/0802.2674) | Euclidean meshfree Poisson stencils exact on constants, linears, quadratics; nonnegative feasibility `Vs=b`; basic LP support at most `d(d+3)/2`; half-space condition necessary and cone condition sufficient under stated assumptions. | Poisson stencils use Euclidean consistency/sign conventions; translate before comparing to spherical jump rates. | Supports local positive-stencil ideas. It does not establish global shared-edge reversibility, spherical moment conditions, or necessity of its sufficient cone test. | HYPOTHESES_AUDITED / II,III |
| M6 — [Babecki–Steinerberger–Thomas, Spectrahedral Geometry of Graph Sparsifiers](https://arxiv.org/abs/2306.06204) | Subgraph Laplacians preserving the first k eigenpairs form a spectrahedral/polyhedral family `L=F+Phi_>k Y Phi_>k^T` for a fixed eigenbasis and connected weighted graphs. | Positive-semidefinite combinatorial Laplacian; AFP uses negative generator. Multiplicity requires basis/subspace care. | Overlaps eigenpair-preserving optimization. It is not a theorem about selected sampled harmonic components, spherical locality, or sampling injectivity; dimension heuristics are not theorems. | HYPOTHESES_AUDITED / II,III |
| M7 — [García Trillos–Gerlach–Hein–Slepčev, Graph-Laplacian Spectral Convergence](https://arxiv.org/abs/1801.10108) | Random geometric graph Laplacians on sampled manifolds converge in eigenvalues/eigenvectors to a weighted Laplace--Beltrami operator with explicit probabilistic rates under the paper's sampling and bandwidth hypotheses. | Their graph Laplacian sign/scaling and asymptotic probability regime must be converted before comparison with AFP's fixed finite negative generator. | Relevant to future construction and continuum validation. It does not prove the finite quotient trace inequality, its exact constant, or the P1B equality theorem. | HYPOTHESES_AUDITED / I,II |
| M8 — [Martin–Tanaka, Commutative Association Schemes](https://arxiv.org/abs/0811.2475) | A commutative association scheme has a Bose--Mesner algebra with primitive idempotents and nonnegative Krein parameters controlling Schur products. | Standard inner product/counting measure is uniform.  Unequal AFP weights require a separate weighted adjoint and generally leave the scheme category. | Organizes product components in symmetric finite examples.  It does not prove the P1A arbitrary-weight quotient theorem or identify a scheme idempotent with a continuous spherical harmonic module without an embedding proof. | HYPOTHESES_AUDITED / I,III |
| M9 — [Bannai--Bannai, Spherical Designs and Algebraic Combinatorics on Spheres](https://doi.org/10.1016/j.ejc.2008.11.007) | A spherical `t`-design is equivalent to vanishing sums of harmonics of degrees `1..t`, and to the stated characteristic-matrix/moment orthogonality under uniform averaging. | The survey uses the uniform design measure and continuous harmonic normalization.  AFP uses an arbitrary positive stationary `w` unless uniformity is separately proved. | Supplies design/frame language and symmetric checks.  It does not imply a positive reversible generator, `L`-invariance of `im S_2`, or sampling injectivity. | HYPOTHESES_AUDITED / I,III |

Global guardrails: operator conventions are not interchangeable; multiplicity
and sampled kernels must be explicit; none of M1–M9 proves unrestricted
Platonic classification, sampling injectivity, the future sharp AFP frontier,
or a global positive reversible lift for prescribed spherical geometry.

## P1C transfer additions

| ID / source | Exact external content used and hypotheses | Source convention / AFP conversion | Overlap and non-overlap boundary | Transfer status / paper |
|---|---|---|---|---|
| M10 — [Ahrens–Beylkin, Rotationally Invariant Quadratures for the Sphere](https://royalsocietypublishing.org/doi/10.1098/rspa.2009.0104) | Rotation-group-invariant spherical quadrature constructions, including icosahedral symmetry, under the paper's quadrature conventions. | Uniform rotational orbits are separate from AFP jump rates, shared conductances and sampled-quotient normalization. | Motivates symmetric exact checks. It does not prove the P1C local tight-frame equality theorem, reversible-generator existence, sampling aliases or global classification. | HYPOTHESES_AUDITED / I,III |

For P1C, M4 and M8–M10 supply adjacent special operators,
association-scheme structure, design/frame language and invariant-quadrature
examples. Every local block identity, rate normalization, sampled-kernel
statement, family construction and restricted classification is proved
internally; no external theorem is transferred as the equality result.

## P1D transfer audit

| Source or standard tool | External content used | P1D transfer boundary |
|---|---|---|
| finite-frame polar decomposition | positive-definite frame operators admit inverse square roots and whitening | P1D derives the weighted Procrustes constant directly; no published frame-stability theorem is imported |
| weighted Cauchy--Schwarz, Chebyshev and finite Poincare inequalities | standard finite Hilbert-space inequalities | all normalizations, stationary measures, gaps and equality-sensitive constants are recomputed in P1D |
| Hoffman--Wielandt spectral variation | Frobenius perturbation controls ordered eigenvalue displacement for symmetric matrices | applied only to explicit local covariance matrices; radial eigenvector stability still requires a nonzero spectral gap |
| effective resistance energy inequality | point differences are controlled by resistance times Dirichlet energy | P1D states its energy convention and retains resistance, path length, minimum conductance and congestion parameters |
| García Trillos--Gerlach--Hein--Slepčev, arXiv:1801.10108 | asymptotic spectral convergence of random geometric graph Laplacians under manifold/bandwidth hypotheses | adjacent spectral context only; it proves none of the finite P1D master, quotient, edge, or frame-repair constants |
| Izmestiev--Lam, arXiv:2408.04877 | geometry-specific spherical/hyperbolic discrete Laplacians | no transfer from their specialized weights to arbitrary positive reversible generators |
| Martin--Tanaka and Bannai--Bannai | association schemes and spherical-design moment structure for symmetric examples | symmetry does not supply `w_min`, `kappa`, sampling gaps, tangent lower bounds, or global gluing |

P1D invokes no external global embedding-stability theorem. Its local repairs
are constructive; its necessity examples prevent silent transfer of a
uniform frame or graph-rigidity constant.

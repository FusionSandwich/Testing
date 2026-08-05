# P2A prior-art, normalization, and hostile audit

## 1. Priority-safe boundary

P2A does **not** claim the first positive angular Fokker--Planck generator,
the first shared moment system, the first positive local stencil LP, or the
first convex eigenpair-preserving graph design.  Its defensible contribution
is the assembled fixed-data package:

- Paper-I's sampling-kernel-correct quotient and sharp rate lower bound;
- globally shared reversible coordinate exactness for arbitrary fixed
  `(X,w,E)`;
- exact affine shell residuals with output leakage retained;
- seven convex objective families and their exact duals;
- solver-independent exact or genuinely outward-enclosed optimality and
  infeasibility certificates, with raw floating residuals labeled only as
  tolerance diagnostics;
- analytic diagnosis of fixed or misleading conductance penalties;
- exact alias, ill-conditioning, and local-versus-global adversaries.

## 2. Primary-source transfer table

| Source | Variables and hypotheses | Result used | Exact distinction and transfer note |
|---|---|---|---|
| [Bienvenue, Naceur, Carrier, Hebert (2025)](https://doi.org/10.1080/00295639.2025.2462891) and the [deposited manuscript](https://publications.polymtl.ca/64454/2/2025_Bienvenue_Flexible__Moment-Preserving_Monotone_Discretization_Multidimensional_SUPP.pdf) | fixed spherical quadrature nodes/masses, Voronoi-neighbor graph, one symmetric shared coefficient per edge | a monotone moment-preserving angular finite-difference construction obtained from an overdetermined moment system/pseudoinverse; positivity and exactness reported on tested product, level-symmetric and Lebedev quadratures | direct precedent for the shared-coefficient angular object and moment equations. The source explicitly leaves a general characterization for further work. P2A instead optimizes positivity on arbitrary fixed permitted graphs, quotients aliases, and returns primal/dual/Farkas certificates |
| [Seibold (2008)](https://arxiv.org/abs/0802.2674) | one Euclidean point-cloud row, constant/linear/quadratic consistency, nonnegative off-center coefficients | local Farkas geometry and positive basic stencils with bounded basic support | direct local cone/support precedent. The assembled meshfree operator is generally nonsymmetric; the result does not imply a shared reversible spherical generator |
| [Babecki, Steinerberger, Thomas (2023)](https://arxiv.org/abs/2306.06204) | fixed connected weighted graph, positive-semidefinite Kirchhoff Laplacian, first ordered `k` eigenpairs, positive subgraph reweightings | the preserving set is a polyhedron intersected with a PSD cone; support deletion is movement to faces | direct convex eigenpair-preservation precedent. P2A uses a nonuniform mass matrix, prescribes a geometric coordinate subspace rather than an ordered initial spectrum, and optimizes an alias-correct continuous harmonic shell under directed-rate caps |
| [Boyd--Vandenberghe, _Convex Optimization_, Chapter 5](https://web.stanford.edu/~boyd/cvxbook/bv_cvxbook.pdf) | finite affine equalities and closed convex cones with Slater/minimal-face hypotheses | strong duality, cone self-duality and complementary slackness | only the generic theorem is external. Every AFP sign, cross-block factor, dual objective, face condition and exact certificate is derived in the P2A source |

## 3. Factor-two transfer warning

The accessible deposited 2025 angular Fokker--Planck manuscript has an
internal convention discrepancy.  Its shared generator equations and the
continuous first-shell condition give

\[
 \sum_j\gamma_{kj}(\Omega_j-\Omega_k)=-2w_k\Omega_k,
\]

but its printed moment system displays `-4 w_k Omega_k`.  Normalizing
`sum w` does not remove the discrepancy.  P2A uses the task's and Paper-I's
literal convention `L Omega=-2 Omega`; the source's printed factor is not
transferred.

## 4. Hostile mathematical checks

| Attack | Exact control |
|---|---|
| assume five sampled quadratic modes | octahedron has exact rank two and still saturates `D_2 rmax=6` |
| replace sampled denominator by coefficient Frobenius norm | theorem constructs a `W`-orthonormal basis of `im S_2` before forming the residual |
| compress output to `im S_2` | `T_2` retains the whole `N`-dimensional weighted output |
| silently threshold rank | exact/supplied separated rank is mandatory; ambiguous input fails |
| miss the SDP dual factor two | `tau_e=2<T_e,Z_12>` is checked symbolically and by exact tetra duals |
| infer Slater from feasibility | theorem requires strict positivity/rate/norm slack on the minimal face |
| trust `l1` sparsity | `sum ell gamma=1`; plain `sum gamma` favors antipodal edges in an exact fixture |
| infer global reversibility from local rows | unequal-mass four-cycle has `A^T y=0`, `b^T y=-2/3` |
| call a solver status a certificate | independent verifier checks primal/dual cones, stationarity, complementarity and gap |
| hide ill-conditioning behind full rank | exact ten-node family has rank five at every level and sampling gap tending to zero |
| claim all rotations from a finite mode list | finite selected-mode SOCP is explicitly scoped to its list |
| call a nonlinear resolvent response convex | only fixed affine response maps are retained |

## 5. Exact conductance penalty audit

The dual field `y_i=-Omega_i/2` gives

\[
 \mathcal A^{\mathsf T}y=\ell,
 \qquad b^{\mathsf T}y=1,
\]

so exactness fixes `ell^T gamma=1`.  Plain total conductance is
`(1/2) sum_i w_i r_i`.  It is therefore a legitimate average-rate cost but
not a support count.  Edge-group penalties are convex heuristics.  Reweighted
`l1`, binary support selection, and the pruning outer loop are labeled
nonconvex/combinatorial exactly where they are.

## 6. Audit verdict

The theorem is priority-safe and normalization-safe only with all the guards
above.  The implementation must keep these as deterministic mutations and
must not weaken them after a successful benchmark run.

# P2C independent theorem and hypothesis audit

## Audit scope

This audit rechecks the complete P2C theorem package independently of the
finite benchmark and solver status.  The historical P2C archive
`b34c29b1b04f5293eaa4007b39d189efa03c51f5` is treated as evidence, not as an
assumption of correctness.  The audit checks every theorem against the frozen
P2A sign, mass, sampling-quotient, and conductance conventions and against the
accepted P1B/P1E constants.

The audit also reopens three failure surfaces that a green numerical workflow
did not by itself exclude:

1. moving sampling kernels and full-output leakage;
2. nonsmooth/parametric outer optimization hypotheses; and
3. immutable publication provenance.

## Theorem-by-theorem audit

### Theorem 1 — raw moving-Gram epigraph

For `t>0`, the lower-right block is positive definite and its Schur complement
is

\[
 tG_\ell-t^{-1}Z_\ell^\top Z_\ell\succeq0.
\]

Testing against every coefficient vector gives
`||Z_l a||^2 <= t^2 a^T G_l a`.  On `ker G_l` this forces `Z_l a=0`; on the
positive sampling range it is exactly the sampled quotient norm bound.  For
`t=0`, a positive-semidefinite symmetric block with zero diagonal blocks must
have zero off-diagonal block, hence `Z_l=0`.  The proof therefore covers
sampling aliases without a pseudoinverse continuity assumption and retains
residual components outside `im S_l`.

**Audit result:** accepted.

### Theorem 2 — fixed-candidate global optimum and attainment

All fixed-candidate constraints are affine or affine LMIs in conductances and
epigraph variables.  The rate cap bounds every incident conductance.  The
independent trace calculation

\[
 \sum_e c_e\|x_i-x_j\|^2=\lambda_1
\]

provides the alternative bound when active chord lengths have a positive
floor.  Positive shell weights and `t_l >= 0`, forced by the LMI diagonal
block, bound epigraph variables on an objective sublevel.  The feasible
sublevel is closed and bounded in finite dimension.

**Audit result:** accepted.  Globality is confined to fixed `X,w,E`.

### Theorem 3 — compactness and existence

The original wording compressed a parametric-conic transfer into the phrase
“constant rank and uniform Robinson regularity make the feasible
correspondence continuous.”  That statement is safe only when the displayed
metric-regularity margin is actually verified on one protected stratum.

The corrected theorem therefore exposes the exact correspondence hypotheses:
nonempty values, closed graph, lower hemicontinuity, uniformly bounded
conductances, and positive coefficients on nonnegative epigraph variables.  A
verified constant-rank/Robinson margin is a sufficient gate for lower
hemicontinuity; it is not inferred from Slater feasibility.

The full feasible correspondence is intentionally not called bounded, because
an SDP epigraph variable can always be enlarged.  Instead, lower
hemicontinuity plus compactness of the parameter stratum gives a uniform
feasible objective bound by a finite-neighborhood argument.  Every optimizer
then lies in a common compact box: rates bound conductances and the positive
objective coefficients bound the nonnegative epigraph variables.  A direct
sequence proof gives upper continuity of the value from lower
hemicontinuity, lower continuity from compact optimizer subsequences and the
closed feasible graph, and hence a compact optimizer graph.  The continuous
lifted outer objective therefore attains a minimum.

Continuity or local Lipschitzness of the secondary reduced value requires a
continuous optimizer-face correspondence or a unique strongly regular
secondary selection.  Nonunique primary optimality alone is insufficient.

**Audit result:** accepted after hypothesis expansion.

### Theorem 4 — orbit covariance

A group element permutes nodes and edge orbits while preserving tied masses
and conductances.  Direct substitution proves generator commutation.  Harmonic
sampling intertwines the node permutation with the orthogonal harmonic
representation; Gram and raw epigraph blocks therefore transform by
congruence.  A general ambient rotation maps a fixed group stratum to the
conjugate-group stratum, while only the normalizer preserves the original
parameterization.

The application-weighted term is covariant only when coefficients, source,
geometry, spatial mesh, interpolation/reconstruction, and response functional
are co-rotated equivariantly.

**Audit result:** accepted with the stated application condition.

### Theorem 5 — exact proximal descent and limiting stationarity

The original theorem used an unspecified distance and omitted the bounded
subgradient extraction needed for the limiting-normal argument.  The corrected
version uses the ambient Euclidean squared norm on a finite-dimensional
embedded stratum, fixed `alpha>0`, a nonempty compact prox-regular set, and a
reduced value locally Lipschitz on a neighborhood of that compact set.

Comparison with the incumbent gives

\[
 V(z_{k+1})+\|z_{k+1}-z_k\|^2/(2\alpha)\le V(z_k),
\]

and telescoping gives an explicit finite sum of squared increments.  Fermat’s
rule and the limiting-subdifferential sum rule provide

\[
 v_{k+1}+(z_{k+1}-z_k)/\alpha+n_{k+1}=0,
\quad v_{k+1}\in\partial V(z_{k+1}),\quad
 n_{k+1}\in N_Z(z_{k+1}).
\]

Local Lipschitzness on a neighborhood of compact `Z` uniformly bounds the
subgradients; vanishing increments then bound the normals.  Along a cluster
subsequence, the next iterates share the same limit.  Closed subdifferential
and normal graphs give limiting stationarity.

**Audit result:** accepted after proof repair.  The finite-pool controller has
only its declared finite-pool descent claim.

### Theorem 6 — restored Riemannian convergence

The theorem explicitly assumes a compact boundaryless `C^2` equality
manifold, a uniform interior inequality margin, uniformly `C^2` first-order
restoration, exact inner solves, a `C^1` value with Lipschitz Riemannian
gradient, and initial Armijo trial steps uniformly bounded above and away from
zero.  Under those hypotheses the descent lemma and `O(alpha^2)` restoration
error give a uniform accepted Armijo interval.  Summed sufficient decrease
makes gradient norms square summable; continuity gives stationary cluster
points.  MFCQ is separately required to state full KKT multipliers.

Slater feasibility is not used as a differentiability theorem.  Nonsmooth
claims require the displayed Clarke residual, summable errors, displacement
control, and an explicit local-boundedness/closed-graph transfer gate for the
Clarke subdifferential and normal sum.

**Audit result:** accepted as a conditional algorithm theorem.

### Alternating strategy

Separate block stationarity can fail on coupled equality manifolds.  The
stated tangent-frame condition converts vanishing block projections into a
vanishing full gradient.  The executable alternative is one joint feasible
safeguard per sweep, to which Theorem 6 applies.  Without either mechanism the
ledger claims only certified nonincrease.

**Audit result:** accepted with no unconditional full-stationarity claim.

### Theorem 7 — graph updates

Adding permitted columns with zero conductance leaves every affine equality,
rate, shell residual, and fixed response term unchanged.  Hence the old
feasible set embeds in the enlarged graph and the exact optimum cannot worsen.
Deletion is correctly conditional on a restricted re-solve or exact kernel
move followed by all remaining conic checks.  Finite graph search termination
follows from no revisits; exact neighborhood stationarity requires final
exclusion certificates for every declared neighbor.

**Audit result:** accepted.  The finite zero-extension identity is included in
the P2C Lean kernel.

### Dense spherical-design initializer

For the complete graph `c_ij=lambda_1 w_i w_j`, direct summation gives

\[
 (-Lf)_i=\lambda_1\left(f_i-\sum_jw_jf_j\right).
\]

Positive weights give positive conductances.  Centering gives exact H1.  A
positive 2-design makes every H2 sample centered, so the H2 residual is the
scalar `lambda_2-lambda_1=d+1`.  This is a globally compatible initializer but
is nonlocal and nonconvergent in H2 defect.

**Audit result:** accepted.

### Adaptive response identity

The adjoint identity is exact for the declared enriched discrete system.  It
contains no continuum consistency or stability estimate.  Retention on failed
moment, positivity, graph, inner-feasibility, or descent gates preserves the
incumbent.

**Audit result:** accepted with enriched-reference scope only.

### Theorem 8 — all-orders quadratic order

At every accepted P1E level the constructive witness satisfies

\[
 r_{\max}\le64\pi^2h^{-2},\qquad
 \mathfrak D_2\le(75/2)h^2.
\]

The exact fixed-node inner optimum cannot exceed its feasible witness.  P1B
gives `D_2 r_max >= 6` for every feasible positive exact-H1 generator, hence

\[
 \mathfrak D_{2,\mathrm{opt}}
 \ge 6/(64\pi^2h^{-2})=3h^2/(32\pi^2).
\]

Both bounds hold at every theorem level.  No fitted slope enters the proof.
The finite `M0=32,64` rows remain regressions; the accepted analytic P1E
admissibility predicate uses its own fixed construction constants.

**Audit result:** accepted.

## Family and rotation audit

The eight requested family descriptors all state positive mass rules,
permitted graphs, exactness gates, conditioning, local/global feasibility, and
rotation metrics.  The correction adds a deterministic 60-rotation
icosahedral group and an orbit-table adapter that audits stabilizer-reduced
orbit sizes, strictly positive orbit masses, duplicate orbits, and harmonic
moments through the declared degree.  It can import AB orbit tables but does
not claim that the internal 12-vertex regression is a published table.

Collision-only physical rotation, joint collision covariance, streaming-only
rays, streaming joint rotation, coupled BFP response, and interpolation are
separate tests.  A finite rotation sample is empirical unless a covering
radius and Lipschitz remainder enclose the continuum extrema.

## Counterexample and transfer audit

The hostile examples remain load-bearing:

- strict positivity without a floor is noncompact;
- a sampling rank change invalidates smooth pseudoinverse differentiation;
- local row cones do not imply shared reversible conductances;
- arbitrary node motion need not admit restoration;
- block stationarity need not be full stationarity;
- Slater feasibility does not imply a differentiable value function;
- monotone objective values do not imply stationarity;
- local outer descent does not imply global optimality;
- edge deletion can destroy feasibility;
- coordinate-dependent Delaunay tie-breaking breaks covariance;
- nonzero shell defect need not produce rotation spread;
- joint rotation is not a ray-effect remedy; and
- an enriched discrete identity is not a continuum error theorem.

Every external paper supplies only the theorem recorded in the prior-art
ledger.  No quadrature theorem is transferred into shared-edge generator
feasibility, no Delaunay positivity theorem is transferred into the P2A shell
optimum, and no finite benchmark is transferred into an all-orders statement.

## Audit conclusion

The corrected P2C theorem package closes the prompt under its displayed
protected-stratum and algorithm hypotheses.  The global claims are exactly:

1. fixed-candidate convex inner optimality;
2. existence of a lifted outer minimizer on the protected compact graph; and
3. all-level quadratic order for the inherited P1E/P1B co-designed family.

Local outer algorithms retain only feasibility, descent, and the stated
subsequential stationarity conclusions.  No nonconvex global-discovery or
whole-sequence claim is made.

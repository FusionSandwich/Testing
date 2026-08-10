# P2B harmonic-defect transport approach registry

Status: **complete scoped registry**.  Exact-head acceptance is recorded by
the publication workflow and immutable archive.  A route is retained only if it gives
an explicit common-space identity or an independently checkable stability
constant.  Routes ending in an unnamed transport-stability theorem are
rejected.

| Approach family | Status | Concrete retained result | Rejected shortcut or remaining boundary |
|---|---|---|---|
| spectral Duhamel multiplier | PROVED | exact multiplier $k_{t,\lambda}(-L)$, sharp full-space transient constant, equilibrium-gap refinement | no sampled-shell invariance is assumed |
| algebraic resolvent | PROVED | exact resolvent residual identity, sharp $1/\alpha$ contraction, gap refinement | $\alpha=0$ requires kernel compatibility and a gap |
| sampled-shell quotient | PROVED | full-output $\mathfrak D_\ell$ controls an entire deflated shell | output compression and coefficient-Frobenius denominators rejected |
| band block Gram | PROVED | exact cross-shell block operator and safe direct-sum bound | an initial-sample bound requires kernel invariance or a positive global sampling angle |
| physical symmetrizer | PROVED_SCOPED | for an Euclidean metric $M=M^*>0$, constant-one bounds under $ML+L^*M\le0$; generalized $(M,W)$ norm-equivalence transfer otherwise | direction-dependent scattering weights are not automatically reversible |
| common-space reconstruction | PROVED | exact six-residual identity through $PJ=I$, including quadrature and time/iteration residuals | raw point sampling on $L^2$ and raw boundary mismatch rejected |
| variation of constants | PROVED | explicit evolution-family convolution and noncommuting intertwining identities | no factorization of streaming and angular semigroups |
| direct energy route | PROVED | Green identity, boundary flux, collision coercivity, stability kernel and six-way norm estimate | “standard Duhamel argument” without domains/constants rejected |
| steady resolvent | PROVED_SCOPED | coercive/inf-sup inverse bound and exact comparator identity | transient contraction with zero coercivity does not give a steady inverse |
| preconditioned residual | PROVED_SCOPED | Neumann/Richardson and inf-sup estimates in a declared norm | eigenvalue clustering alone rejected for nonnormal transport |
| multigroup block energy | PROVED | explicit weighted block coercivity and finite triangular downscatter inverse | triangularity alone does not imply transient contraction |
| adjoint-weighted response | PROVED | exact steady/transient identities and enriched-adjoint remainder estimator | point-detector responses need a separate dual-space theorem |
| $\mathfrak D_2$ predictor | PROVED_SCOPED | norm and adjoint-aligned shell indicators with quantitative dominance conditions | standalone physical-error prediction rejected |
| pure-angular exact fixtures | COMPUTATIONAL_EXACT | sharp alias case and accepted tetrahedral coordinate-exact case | floating matrix exponential is not a proof of the all-data theorem |
| noncommuting spatial fixture | COMPUTATIONAL_EXACT | rational four-state steady solve, exact residual/coercivity/adjoint effectivities | one manufactured problem is a regression, not transport well-posedness evidence |
| operator splitting | REJECTED_AS_NEEDED_PROOF | none required for the retained theorem | would need commutator-domain regularity and an additional splitting-error term |
| legacy Gate-6 convergence | CONTEXT_ONLY | reusable angular/spatial implementation conventions | fitted errors do not provide a residual bound or effectivity theorem |

## Portfolio control

The retained proof uses two incompatible analytic routes—evolution families
and energy estimates—and requires them to agree on the same residual ledger.
The spectral angular proof is independent of both.  Exact symbolic fixtures
test signs, normalizations, noncommutation, and effectivity but do not replace
the operator theorems.  The formal finite core checks only the finite algebra
it actually states; PDE generation, trace theory, and Bochner integration
remain the explicit analytic hypotheses of the manuscript.

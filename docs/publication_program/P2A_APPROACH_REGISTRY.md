# P2A approach registry

This registry groups the independent mechanisms explored for the
fixed-quadrature convex-design prompt.  `BLOCKED` is reserved for a real
missing theorem; `REJECTED` records an exact counterexample.  A numerical
solver result never upgrades a row to `PROVED`.

| Family | Status | Concrete result | Adversarial boundary |
|---|---|---|---|
| shared-incidence algebra | COMPLETE | `L=-W^-1 B Diag(gamma)B^T`, `A gamma=b`, `C gamma<=Rw` | independent row stencils do not ensure shared edges |
| sampled-quotient whitening | COMPLETE | full-output affine `T_l` and exact operator norm | output compression and raw Gram pseudoinverse rejected |
| spectral-norm epigraph | COMPLETE | fixed-rate and fixed-defect SDPs | PSD dual cross block has an essential factor two |
| Hilbert--Schmidt route | COMPLETE | quotient-invariant Frobenius QP and SOCP norm epigraph | raw coefficient Frobenius norm rejected |
| selected physical modes | COMPLETE_SCOPED | finite-list SOCP and scalar LP | sampled-zero modes rejected; finite rotations are not all rotations |
| multi-shell stacking | COMPLETE | shellwise-deflated QP and worst-shell SDP | shells with different eigenvalues are never merged |
| fixed response maps | COMPLETE_SCOPED | affine response QP/SDP/SOCP/LP | `gamma`-dependent resolvents are nonlinear and outside the claim |
| primal conic derivation | COMPLETE | seven convex formulations and fixed-support faces | product objective and support selection are not called convex |
| dual conic derivation | COMPLETE | exact SDP/QP/SOCP/LP duals and slackness | boundary strong duality needs Slater or facial reduction |
| Farkas/conic rays | COMPLETE | exact feasibility and rate-cap rays; original-scale verifier | solver status alone rejected |
| generic `l1` sparsity | REJECTED | loss-weighted `l1` is fixed; plain total conductance is mean rate | exact long-antipodal-edge preference witness |
| group penalties | COMPLETE_AS_HEURISTIC | convex edge-group norms | no support-optimality theorem |
| reweighted `l1` | NONCONVEX_OUTER | each subproblem convex | outer log-sum/MM process honestly nonconvex |
| mixed-integer support | COMPLETE_FORMULATION_SMALL_CASES | rate cap supplies `M_e=R min(w_i,w_j)` | combinatorial; MISDP not advertised as scalable |
| deterministic prune/reopt | COMPLETE_SCOPED | every accepted deletion is exactly re-solved and independently verified at its reported certificate level | returned support need not have minimum cardinality; floating diagnostics require exact reconstruction or genuine outward enclosure for proof status |
| exact equality reconstruction | COMPLETE | tetra/octa attain Paper-I lower bound with aliases | finite equality does not replace the lower-bound proof |
| local-to-global optimistic route | REJECTED | unequal-mass four-cycle has strict local rows and exact global Farkas ray | no rowwise assembly shortcut |
| floating rank heuristic | REJECTED | ambiguous rank is a deterministic failure | exact or separated rank certificate required |
| conditioning audit | COMPLETE | exact full-rank family with collapsing sampling gap | no fitted slope used as proof |
| external angular pseudoinverse | SCREENED_EXTERNAL | direct shared-coefficient prior art | general positivity/exactness not proved; deposited factor-two discrepancy |
| positive stencil LP | SCREENED_EXTERNAL | local Farkas/support precedent | generally nonsymmetric row assembly |
| eigenpair sparsifier spectrahedron | SCREENED_EXTERNAL | convex positive reweighting precedent | ordered first spectral segment differs from geometric module/quotient target |
| Lean finite core | COMPLETE_SCOPED | stable finite conductance and convex-combination identities | generic conic strong duality remains external |

## Dynamic search record

The early independent portfolio separated three incompatible viewpoints:

1. a quotient/operator route deriving exact SDP and Hilbert--Schmidt
   objectives;
2. a global edge-cone/Farkas route attacking shared reversibility and
   sparsity penalties;
3. an implementation/certificate route starting from incidence matrices and
   exact symmetric reconstructions.

Only after each route exposed its own normalization and failure modes were
they combined.  A separate hostile audit then checked the assembled theorem,
and the formalization route was kept independent of the numerical solver.

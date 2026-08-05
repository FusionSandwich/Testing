# P2C approach-family registry

This registry groups work by mathematical mechanism.  A status of PROVED means that the route has a complete theorem under the hypotheses recorded in the main P2C document.  COMPUTATIONAL means that the artifact is an audited finite implementation but is not used as an all-orders proof.  BLOCKED routes are retained to prevent an elegant reduction from being mistaken for a solution.

| Key | Mechanism | Status | Concrete result or blocker |
|---|---|---|---|
| ORBIT-PROX | finite group orbits plus exact inner SDP and compact-stratum proximal step | PROVED | covariance, feasibility, descent, subsequences, limiting stationarity; no outer globality |
| RAW-GRAM | coefficient-space moving-Gram LMI | PROVED | exact equivalence to full shell quotient, including sampling kernels |
| RIEMANN-RESTORE | coupled node/weight/witness tangent and exact equality restoration | PROVED | restored Armijo/KKT theorem under uniform reduced-Jacobian and strong-regularity gates |
| CLARKE-BUNDLE | exact/certified nonsmooth proximal model | PROVED | Clarke-stationary cluster points under the two residual inequalities in the theorem |
| ALTERNATING | weight-led, node-led, exact conductance blocks plus joint safeguard | PROVED | full stationarity with joint safeguard or tangent-frame condition; otherwise only block stationarity |
| GRAPH-ZERO | edge addition by zero extension | PROVED | feasibility preservation and nonincrease of every fixed convex inner optimum |
| GRAPH-DELETE | restricted conic reoptimization or exact kernel move | PROVED | conditional safe deletion; no unconditional deletion theorem |
| GRAPH-FINITE | interval-certified edge-orbit search on a finite master graph | PROVED | finite termination and declared graph-neighborhood stationarity |
| DESIGN-DENSE | positive centered quadrature plus complete-graph dense conductance | PROVED | exact H0/H1 and strict conductance positivity; H2 defect \(d+1\), hence nonconvergent |
| DESIGN-LOCAL | quasiuniform spherical design plus a local graph | BLOCKED | design exactness and local cones do not solve shared symmetric conductance compatibility; admitted only after global P2A/P1E certificate |
| ADAPT-ENRICHED | discrete adjoint residual, deterministic marking, retention on failure | PROVED | exact enriched-reference identity and feasibility/descent for accepted proposals |
| ADAPT-CONTINUUM | enriched estimator promoted directly to continuum error | BLOCKED | missing independent continuum consistency/stability enclosure; no such claim is made |
| P1-FRONTIER | reflected adaptive rings plus exact inner reoptimization | PROVED | all-level \(3h^2/(32\pi^2)\le\mathfrak D_2\le75h^2/2\) |
| ROT-COLLISION | physical harmonic rotated against fixed quadrature | PROVED | declared directional collision metric and shell-defect upper control |
| ROT-JOINT | physical problem and quadrature co-rotated | PROVED | exact mathematical covariance; floating result is a regression |
| ROT-STREAMING | collision-disabled ballistic test | COMPUTATIONAL | separates ray effects; certified extrema require a rotation net and Lipschitz bound |
| ROT-INTERP | quadrature rotation/interpolation | COMPUTATIONAL | separate remedy with constants, positivity, mass, first-moment, norm audit |
| FULL-NONCONVEX | local node method asserted globally optimal | REJECTED | explicit nonglobal local minima exist; the assertion is false without a global certificate |
| LOCAL-CONE | row-wise convex hull asserted globally compatible | REJECTED | shared reversibility couples rows; local feasibility is only necessary |
| STALE-INNER | outer descent evaluated without re-solving conductance | REJECTED | it is not descent for the bilevel value function |
| FLOAT-SLOPE | finite fitted slope asserted as asymptotic order | REJECTED | replaced by the P1B/P1E all-level sandwich |

## Independent development rounds

The initial portfolio kept three incompatible routes separate:

1. finite-group representation theory, invariant moments, and an exact orbit-proximal method;
2. raw moving-Gram semidefinite geometry, lifted feasibility witnesses, and Riemannian/Clarke restoration;
3. finite graph order, Farkas/conic certificates, adjoint adaptation, and physical rotation separation.

Only after each route exposed its own hypotheses were the results cross-audited.  The common conclusions were the raw LMI, a protected compact stratum, exact inner re-solves, retention on failed proposals, and restricted stationarity claims.  The routes disagree usefully on implementation: the orbit route has the cleanest invariance; the lifted route permits unsymmetric local adaptation; the finite graph route gives exact discrete termination.

## Adversarial audits assigned to every proved route

- normalization/sign audit against P2A;
- sampling-kernel and moving-Gram audit;
- strict-positivity/attainment audit;
- collision and vanishing-weight compactness audit;
- local-versus-global conductance compatibility audit;
- nonunique SDP and envelope-derivative audit;
- restoration-Jacobian and coupled-tangent audit;
- Delaunay degeneracy and rotation-equivariance audit;
- graph deletion and active-edge audit;
- physical collision/streaming/interpolation scope audit;
- P1B/P1E constant and mesh-parameter audit;
- exact/algebraic versus floating-certificate audit.

No route ending at a missing compatibility lemma was promoted from BLOCKED.  The convergence theorem uses the already accepted P1E global construction itself, so it does not depend on the blocked arbitrary-design compatibility route.

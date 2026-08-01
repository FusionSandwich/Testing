# Sphere-feasibility approach registry

The registry records genuinely different proof routes and why each was kept,
redirected, or rejected. A route was not counted as complete when it stopped at
a lemma equivalent to the target.

| ID | Approach family | Outcome | Audit disposition |
|---|---|---|---|
| L-A | Direct tangent/normal decomposition | Accepted | Gives the exact spherical algebra and exposes the antipodal singularity. |
| L-B | Convex-combination normalization | Accepted | Proves nonnegative feasibility with repeated indexed points and no rank hypothesis. |
| L-C | Supporting-hyperplane separation | Accepted as one direction | Proves positive coefficients imply relative interior and supplies exact boundary certificates. |
| L-D | Point-by-point inward displacement and averaging | Accepted | Supplies positive weight at every indexed candidate, including repeated and redundant candidates. |
| L-E | Oriented-matroid/circuit formulation | Redirected | Useful for support/minimality language, but by itself restates the dependence problem and supplies neither angular scaling nor quantitative constants. |
| L-F | Minimal-face/augmented-vector analysis | Accepted | Gives the exact uniqueness criterion and identifies all nonuniqueness from repeated or affine-redundant points. |
| A-A | Treat antipodes by a limiting tangent direction | Rejected | Introduces fictitious data and division by zero. |
| A-B | Split tangent cone plus scalar normal budget | Accepted | Gives a complete parameterization and all boundary cases. |
| Q-A | Euclidean inradius in the ambient plane | Rejected as stated | Fails for one-dimensional tangent hulls; replaced by the relative inradius in the affine span. |
| Q-B | Support-function primal/dual margin | Accepted | Gives the exact robust strict-feasibility margin and its dual formula. |
| Q-C | Carathéodory/basic feasible solution | Redirected | Produces sparse dependences but cannot control every indexed coefficient. |
| Q-D | Per-index inward representation followed by averaging | Accepted | Gives `lambda_j >= rho/[m(1+rho)]` for all candidates. |
| Q-E | Frame/singular-value analysis | Accepted | Converts the margin into explicit conditioning constants. |
| Q-F | Implicit continuity of LP bases | Rejected | Basis changes are discontinuous and do not give a uniform all-edge perturbation radius. |
| Q-G | Right-inverse residual correction | Accepted after audit | Gives explicit direction/angle perturbation and row-objective degradation. |
| Q-H | Apply the correction directly to an arbitrary optimizer | Rejected | An optimizer can lie on the coefficient boundary; the final proof mixes with the margin row before correction. |
| G-A | Rowwise reconciliation by averaging oriented rates | Rejected | Does not enforce `w_i a_ij = w_j a_ji`. |
| G-B | Finitely generated edge-column cone | Accepted | Gives the exact global feasibility set and full Farkas alternative. |
| G-C | Weighted conservation only | Retained as necessary, not sufficient | Produces centering but misses sparse-graph compatibility. |
| G-D | Complete-graph rank-one conductances | Accepted | Gives a dense strictly positive solution under exact weighted centering. |
| G-E | Direct edge-coordinate propagation | Accepted for examples | On the cube it proves conductance/mass incompatibility without numerical optimization. |
| G-F | Centered-clique decomposition | Accepted | Gives a nontrivial sparse sufficient reconciliation mechanism. |
| G-G | Unproved generic compatibility lemma | Blocked | This would be equivalent to the requested global theorem and is not used. |
| D-A | Generic weak-duality certificate only | Rejected as completion | Replaced by the full finite alternative, strong duals, and complementary slackness with actual AFP signs. |
| E-A | Floating-point LP examples | Retained only as optional diagnostics | The committed regressions use rational arithmetic and exact certificates. |
| F-A | Formalize all convex analysis before writing the proof | Redirected | Would delay the ordinary theorem; finite spherical consequences are formalized first with exact external theorem statements documented. |

# Spherical positive feasibility and shared-edge duality

The authoritative ordinary proof is split into reviewable theorem blocks:

1. [`SPHERICAL_LOCAL_EXACT.md`](SPHERICAL_LOCAL_EXACT.md) — exact
   non-antipodal convex-hull and relative-interior equivalences, uniqueness,
   rate formula, and complete antipodal classification.
2. [`SPHERICAL_LOCAL_QUANTITATIVE.md`](SPHERICAL_LOCAL_QUANTITATIVE.md) —
   relative cone margin, coefficient and rate bounds, inverse-quadratic
   constants, conditioning, perturbation radii, and objective degradation.
3. [`SHARED_EDGE_CONE_FARKAS.md`](SHARED_EDGE_CONE_FARKAS.md) — edge-column
   cone, feasible polytope, weighted centering, complete-graph construction,
   and the full spherical Farkas alternative.
4. [`SHARED_EDGE_OPTIMIZATION_DUALS.md`](SHARED_EDGE_OPTIMIZATION_DUALS.md) —
   strong duals and complementary slackness for linear rate/defect, peak-rate,
   and weighted residual formulations.
5. [`SHARED_EDGE_STRICT_SENSITIVITY.md`](SHARED_EDGE_STRICT_SENSITIVITY.md) —
   strict all-edge feasibility, dual-face criteria, and explicit perturbation
   and sensitivity estimates for targets, masses, and node positions.
6. [`SHARED_EDGE_RECONCILIATION_EXAMPLES.md`](SHARED_EDGE_RECONCILIATION_EXAMPLES.md)
   — centered-clique reconciliation, exact local and antipodal examples, the
   centered locally-feasible/global-incompatible cube, the strict symmetric
   cube, and the prior-art boundary.

Together these files are the complete ordinary theorem package for this stage.
The theorem-to-file map is in `../docs/THEOREM_TO_FILE_MAP.md`; exact rational
regressions are under `examples/`.

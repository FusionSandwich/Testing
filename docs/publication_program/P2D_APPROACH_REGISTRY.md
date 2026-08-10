# P2D approach registry

| Family | Mechanism | Status | Boundary |
|---|---|---|---|
| stationary residual correction | exact high-order residual, cached low-order inverse | PROVED | convergence needs a contraction or equivalent stability condition |
| constrained correction | Schur projection into `ker Q` | PROVED | compatible initial invariant and nonsingular Schur block required |
| commuting harmonic analysis | exact shell ratios | PROVED | only common reducing shells |
| SPD spectral equivalence | generalized Rayleigh bounds | PROVED | transformed matrices must be symmetric positive |
| nonsymmetric field of values | coercivity/norm disk | PROVED | metric-specific sufficient condition, not necessary |
| slow-subspace restriction | audit `||EV||` and leakage | PROVED/COMPUTATIONAL | basis must represent the actual slow error |
| left-preconditioned GMRES | cached low solve; original residual acceptance | COMPUTATIONAL | finite frozen systems |
| heat-kernel forward-peaking sweep | exact shell multipliers and same-node AFP lows | COMPUTATIONAL | controlled BFP family, not material cross sections |
| classical modified-FP comparator | signed spectral Laplace–Beltrami preconditioner | COMPUTATIONAL | comparator only; not monotone or a byte-identical external code reproduction |
| multigroup/boundary retention | identical nonangular blocks in high and low systems | COMPUTATIONAL | two-group/two-cell finite audit |
| eigenvalue-only inference | isolated angular eigenvalues imply full transport speedup | REJECTED | streaming, group, boundary, and leakage invalidate inference |
| universal H2 dominance | low `D_2` always predicts acceleration | REJECTED | higher-shell and ray adversaries |
| low operator fixes ray error | preconditioner changes fixed-quadrature production response | REJECTED | exact fixed-point preservation forbids it |

# P2D approach registry

| Family | Mechanism | Status | Boundary |
|---|---|---|---|
| stationary residual correction | exact high-order residual, low-order inverse | PROVED | requires low-order nonsingularity and contraction for convergence |
| constrained correction | KKT/Schur projection into `ker Q` | PROVED | requires compatible initial invariant and nonsingular Schur block |
| commuting harmonic analysis | exact shell ratios | PROVED | only common reducing shells |
| noncommuting perturbation | `A_L^-1(A_L-A_H)` norm | PROVED | may be pessimistic |
| noncommuting FOV | coercivity/norm disk | PROVED | metric-specific sufficient condition, not necessary |
| Krylov left preconditioning | low operator used only in `M^-1` | COMPUTATIONAL | convergence recorded in original residual |
| eigenvalue-only acceleration inference | isolated angular eigenvalues imply full transport speedup | REJECTED | streaming/energy/boundary noncommutation invalidates inference |
| universal H2 dominance | optimized H2 always improves iteration count | REJECTED | higher-shell hostile fixture |
| physical forward-peaking sweep | published electron/neutron/proton cases | DEFERRED_TO_P2E | belongs to benchmark hierarchy |

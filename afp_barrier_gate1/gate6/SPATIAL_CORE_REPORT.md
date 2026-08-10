# Gate 6 spatial transport implementation checkpoint

## Implemented

- reusable shared-edge angular API;
- positive first-order finite-volume upwind streaming;
- left and right inflow/vacuum boundary functions;
- spatially varying absorption and angular-diffusion coefficients;
- Euler and SSPRK2 time stepping;
- exact discrete inventory, boundary-current, source, absorption, and collision
  balance diagnostics;
- manufactured degree-one space--angle solution;
- piecewise material stacks and layer assignment;
- regional absorption and leakage tallies;
- thin functional-layer versus control benchmark.

## Verification performed locally

- Python compile/import check;
- deterministic unit and regression tests;
- all pre-existing Gate 6 audits;
- manufactured spatial-convergence audit;
- thin-interface response and conservative-balance audit.

## Main numerical results

Manufactured solution at 80 cells:

| Family | Directions | Relative error |
|---|---:|---:|
| Icosphere L1 | 42 | 3.945874e-4 |
| Product N5 | 50 | 4.081430e-4 |

Level-2 thin-film response:

| Family | Directions | Film/control transmission | Film/control thin absorption | Film steps |
|---|---:|---:|---:|---:|
| Icosphere L2 | 162 | 0.830061 | 9.251564 | 156 |
| Product N9 | 162 | 0.830190 | 9.269100 | 644 |

The physical response agrees closely at matched direction count, while the
product angular grid carries a 4.13x explicit-step penalty in this
streaming-dominated configuration.

## Formal scope

`AFPBarrier/SpatialUpwindTransport.lean` verifies the exact positive-row form,
the combined streaming--collision--absorption CFL condition, and its local
necessity for unconditional positivity. Repository status is recorded by the
Gate 6 CI artifact rather than inferred from local source scans.

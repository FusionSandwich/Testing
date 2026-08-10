# P2E clause closure matrix

| Prompt clause | Preregistered implementation/evidence |
|---|---|
| One frozen software version | `P2E_BENCHMARK_MANIFEST.json`; pinned CI workflow |
| Immutable manifest | Hash-bound manifest plus exact-head preregistration commit |
| Same nodes for operator quality | `P2E_FROZEN_OPERATOR_REGISTRY.json`; runner checks |
| Different quadrature separate | `ablations.py::co_design_ablation` |
| Seven mandatory cases | `cases.py`; manifest inventory |
| Conservation and positivity | generator audits and slab balance/positivity fields |
| H0/H1 and shell defects | frozen operator audits through degree six |
| Scalar/current/tensor/qn errors | common response records in every case |
| Response errors | case-specific linear or material response |
| Rotation spread | narrow beam and HTS orientation records |
| Rate/stiffness | operator audit records |
| Iterations/runtime/memory | direct group solves, matrix size, and P2D accelerator records |
| Equal direction count | same 32-node record |
| Equal wall time | common measured budget record |
| Wall time at equal error | reached/not-reached same-node record; no extrapolation |
| Independent reference | analytic, fine spectral, or full positive Boltzmann reference |
| Reference uncertainty separate | explicit `reference.uncertainty` |
| Training/validation/held-out | frozen manifest and no-held-out workflow gate |
| Seven ablations | `ablations.py` and accelerator-only P2D reuse |
| Strongest claim quantitative | final held-out audit and stage report, not preregistration prose |

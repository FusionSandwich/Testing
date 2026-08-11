# P2F claim matrix

| ID | Claim | Evidence | Status / boundary |
|---|---|---|---|
| F01 | Cu, Ag, REBCO, buffer, and substrate are separately resolved | Manifest and result layer inventories | COMPLETE |
| F02 | Normal, oblique, and grazing-sensitive cases are run | Three immutable incidence rows | COMPLETE |
| F03 | Neutral collision physics is not replaced by AFP | Identical full Boltzmann neutral records and audit | COMPLETE |
| F04 | AFP is confined to charged BFP transport | Physics firewall and charged block construction | COMPLETE |
| F05 | Secondary generation is explicit | Neutral reaction loss creates charged source | COMPLETE, surrogate coefficients |
| F06 | Spatial and energy discretizations are identical between methods | Result flags and shared mesh/group definitions | COMPLETE |
| F07 | Layer scalar/current/tensor/\(q_n\) outputs exist | Per-layer result records | COMPLETE |
| F08 | Heating, crossing, escape, and PKA descriptors exist | Per-layer/global response records | COMPLETE |
| F09 | Species-resolved PKA source and directional tensor exist | Species records; PSD/symmetry audit | COMPLETE, not recoil spectra |
| F10 | Orientation sensitivity is evaluated | 0°, 60°, and 84° cases | COMPLETE as a surrogate diagnostic |
| F11 | The nominal 72/50 plus spatial difference is a converged uncertainty | 50/72/98/128 sweep | FALSE; every incidence fails the declared convergence gate |
| F12 | Improved \(H_2\) fidelity predicts the selected responses | Maximum method-response relative difference `1.9424e-14` | NOT TESTED BY THIS FIXTURE; response map is operator-insensitive |
| F13 | Optimized AFP improves HTS response | 0/18 resolved improvements | NOT SUPPORTED |
| F14 | Optimized AFP degrades HTS response | 0/18 resolved degradations | NOT SUPPORTED |
| F15 | The P2F scientific conclusion is bounded negative | Revised audit | WITHDRAWN; outcome is `INCONCLUSIVE_REFERENCE_NOT_CONVERGED` |
| F16 | Evaluated nuclear-data performance | No evaluated data used | OUT OF SCOPE |
| F17 | DPA/defect/\(J_c\)/\(T_c\) benefit | No damage/property model | PROHIBITED |
| F18 | P2F integrity package is deterministic and fail-closed | Scientific hash, audit, tests, workflow | COMPLETE for record integrity, not scientific transfer |

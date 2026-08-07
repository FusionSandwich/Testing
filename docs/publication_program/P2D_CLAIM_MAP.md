# P2D claim map

| ID | Claim | Proof source | Test/audit source | Status |
|---|---|---|---|---|
| D01 | residual correction preserves the exact high-order fixed point | P2D manuscript §2 | `test_exact_fixed_point_and_error_operator` | PROVED |
| D02 | constrained inverse satisfies `QP_L=0` | P2D manuscript §2 | constrained conservation test | PROVED |
| D03 | error operator is `I-omega A_L^-1 A_H` | P2D manuscript §3 | exact error test | PROVED |
| D04 | commuting shell factor is exact | P2D manuscript §3 | shellwise formula test | PROVED |
| D05 | perturbation norm bound | P2D manuscript §3 | executable audit | PROVED |
| D06 | FOV contraction bound under displayed hypotheses | P2D manuscript §4 | executable audit | PROVED |
| D07 | GMRES retains the production fixed point | P2D manuscript §5 | all-comparator GMRES test | PROVED |
| D08 | optimized fixture can reduce noncommuting iterations | finite fixture only | audit row | COMPUTATIONAL |
| D09 | H2 optimization can fail for higher-shell slow modes | explicit fixture | hostile audit row | COMPUTATIONAL |
| D10 | finite algebra has no project axiom | Lean source | P2D axiom audit | FORMAL |

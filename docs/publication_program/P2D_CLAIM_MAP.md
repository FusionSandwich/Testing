# P2D claim map

| ID | Claim | Controlling proof source | Primary test/audit source | Status |
|---|---|---|---|---|
| D01 | residual correction preserves the exact high-order fixed point | manuscript §2 | fixed-point test | PROVED |
| D02 | constrained inverse satisfies `QP_L=0` | manuscript §2 | constrained conservation test | PROVED |
| D03 | error operator is `I-omega A_L^-1 A_H` | manuscript §3 | exact error test | PROVED |
| D04 | commuting shell factor is exact | manuscript §3 | shellwise test | PROVED |
| D05 | perturbation mismatch bound | manuscript §3 | finite audit | PROVED |
| D06 | SPD spectral-equivalence contraction | manuscript §4 | spectral-equivalence test | PROVED |
| D07 | metric FOV contraction under displayed hypotheses | manuscript §4 | FOV test | PROVED |
| D08 | contraction gives an explicit sufficient iteration count | manuscript §4 | iteration-bound test | PROVED |
| D09 | transport mismatch separates angular, streaming, group, and boundary blocks | manuscript §5 | decomposition audit | PROVED |
| D10 | GMRES retains the production fixed point and checks original residual | manuscript §§1,7 | all-comparator test | PROVED |
| D11 | frozen optimized/baseline generators are positive, reversible, H0/H1 exact | frozen data + manuscript §6 | independent generator audit | COMPUTATIONAL CERTIFICATE |
| D12 | slow H2 mode is selected without transport outcomes | manuscript §7 | mode-selection ledger | COMPUTATIONAL FIREWALL |
| D13 | optimized positive operator beats monotone baseline on every forward-peaked row | manuscript §7 | transport audit | COMPUTATIONAL |
| D14 | all required costs and robustness counters are recorded | manuscript §7 | transport audit rows | COMPUTATIONAL |
| D15 | signed classical FP can outperform positive methods but is not production eligible | manuscript §7 | comparator rows | COMPUTATIONAL |
| D16 | higher-shell dominance invalidates D2-only prediction | manuscript §8.1 | higher-shell audits | COMPUTATIONAL |
| D17 | fixed-quadrature ray error cannot be repaired by a fixed-point preconditioner | manuscript §8.2 | analytic ballistic audit | PROVED + COMPUTATIONAL |
| D18 | finite algebra has no project axiom | Lean boundary | P2D axiom audit | FORMAL |

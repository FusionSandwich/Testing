# Prompt 3 theorem-to-file map

This map separates ordinary all-orders proofs, Lean finite algebra,
deterministic finite certificates, and EXTERNAL standard inputs.  A finite
enumeration or exact example is never listed as the proof of a general theorem.

| Theorem family | Claim label | Ordinary proof | Lean support | Deterministic support |
|---|---|---|---|---|
| spherical loss moment and exact `Q-1` identity | PROVED | `pure_math/rigidity/GLOBAL_Q_RIGIDITY_THEOREM.md` §1 | `AFPBarrier/SphericalQEqualityRigidity.lean` | `global_near_rigidity_audit.py` |
| local equality and connected shared-edge transfer | PROVED | global theorem §2 | same module plus `GlobalLossRigidity.lean` | all five Platonic rows; degeneracy tests |
| ten-hypothesis exact classification | PROVED | global theorem §3 | finite scalar core only | source-pinned census is COMPUTATIONAL falsification |
| direct 5-valent 12-vertex uniqueness | PROVED | `pure_math/rigidity/ICOSAHEDRAL_GRAPH_LEMMA.md` | ordinary topology boundary | Plantri survivor isomorphism is COMPUTATIONAL |
| exact side/loss/rate table and face propagation | PROVED | global theorem §§3.5–3.6 | finite scalar identities | exact Gram/hull certificates |
| pointwise and adjacent near-rigidity | PROVED | global theorem §§4.1–4.2 | `AFPBarrier/QuantitativeGlobalNearRigidity.lean` | long-path/small-`kappa` stress |
| path, diameter, edge-ratio, and graph-center logarithmic bounds | PROVED | global theorem §§4.2–4.3 | length-indexed path/ratio/log declarations in the quantitative module | deterministic path/reference tests |
| arccos edge-length conversion | PROVED | global theorem §4.4 | ordinary calculus boundary | deterministic derivative audit |
| reversible stationary law and energy transfer | PROVED | global theorem §§5.1–5.2 | finite conductance algebra | exact rational energy audit |
| Poincare and effective-resistance refinements | PROVED | global theorem §§5.3–5.4 | EXTERNAL variational principles | exact rational spectral/resistance cases |
| corrected fixed-box angle constant | PROVED | global theorem §§6.2, 6.5 | ordinary trigonometric boundary | Gram/Heron threshold audit |
| closed `delta_*`, `eta_*`, valence, and Platonic edge sup bound | PROVED | global theorem §§6.3–6.5 | selected finite inequalities | threshold/valence stress |
| literal tangent normalization at `ell=2` | REJECTED | global theorem antipodal boundary | no false totalized-division theorem | two-state antipodal regression |
| exact `T,C,M` covariance decomposition for `0<ell<2` | PROVED | global theorem §7.2 | `AFPBarrier/QEqualityCovariance.lean` | exact weighted-octahedron matrices |
| Prompt-2 axial condition iff `T=P/2` | PROVED | global theorem §7.3 | covariance module plus `OneShellQuadraticRigidity.lean` | conductance-parameter identities |
| positive anisotropic weighted octahedron | PROVED | global theorem §7.4 | finite scalar entries | `q1_covariance_audit.py` |
| genuine sampled degree-two space `{0}` | PROVED | stochastic contraction in §7.4 | Prompt-2 sampling boundary | exact linear system/minors |
| five Platonic `Q=1` graphs | COMPUTATIONAL | global theorem falsification boundary | Prompt-2 one-shell support where applicable | exact instances supporting the ordinary formulas in the Prompt-2 and Prompt-3 covariance audits |

## Permanent rejected boundaries

| Rejected formulation | Claim label | Ordinary boundary | Lean boundary | Deterministic witness |
|---|---|---|---|---|
| only `K in {4,6,12}` can have `Q=1` | REJECTED | global theorem §8 | no unrestricted theorem | cube and dodecahedron |
| every finite spherical graph has `Q>1` | REJECTED | global theorem §8 | no strict universal inequality | all five Platonic `Q=1` rows |
| every equal-loss spherical graph is a triangulated Platonic graph | REJECTED | global theorem §8 | triangulation hypotheses are not removed | cube, dodecahedron, and inactive-diagonal tests |
| `Q=1` forces axial covariance | REJECTED | global theorem §§7.4–7.5 | `QEqualityCovariance.lean` retains the tangent term | weighted-octahedron anisotropy |
| form-space dimension equals sampled-space dimension | REJECTED | global theorem §7.4 and Prompt-2 sampling theorem | `QuadraticSampling.lean` uses the genuine sampled quotient | octahedral off-diagonal sampling kernel |
| near-rigidity is diameter-free under only a local active-weight floor | REJECTED | global theorem §§4.2–4.3 | path bounds retain path length | long-path accumulation stress |
| finite enumeration proves the classification | REJECTED | global theorem §§3, 8 | no finite-census proof theorem | source-pinned census is COMPUTATIONAL only |

## Control and provenance files

- `pure_math/rigidity/P3_BRANCH_PROTECTION_RECORD.md`
- `pure_math/rigidity/P3_SALVAGE_LEDGER.md`
- `pure_math/rigidity/P3_APPROACH_REGISTRY.md`
- `pure_math/rigidity/P3_THEOREM_REGISTRY.md`
- `docs/P3_STAGE_REPORT.md`
- `docs/CLAIM_MATRIX.md`
- `docs/CONJECTURE_REGISTER.md`
- `docs/PURE_MATH_PRIOR_ART_MAP.md`

The dedicated exact-head gate is
`.github/workflows/afp-prompt3-from-p2-rigidity.yml`.

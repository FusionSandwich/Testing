# Prompt 3 global rigidity theorem-to-artifact map

| Result | Ordinary proof | Lean declaration/module | Exact/certified regression |
|---|---|---|---|
| local normal loss moment and row-rate positivity | `GLOBAL_Q_RIGIDITY_THEOREM.md` §1 | `SphericalQEqualityRigidity.lean` | `global_near_rigidity_audit.py` |
| probability, mean, second moment, and variance identities | §1 | `SphericalQEqualityRigidity.lean` | exact rational variance case |
| local `Q=1` active-loss equality | §2.1 | `sphericalQ_eq_one_active_loss` | all five Platonic rows |
| shared-edge and connected global propagation | §2.2 | existing `GlobalLossRigidity.lean`; specialization helper | hypothesis-deletion audit |
| common equilateral spherical faces | §3.1 | ordinary proof | exact algebraic embeddings |
| round angle sum and constant valence | §3.2 | ordinary proof | cone-defect negative tests |
| Euler restriction and `q/V/E/F` table | §3.3 | selected arithmetic | exact symbolic table |
| combinatorial uniqueness for `q=3,4,5` | §3.4 | ordinary direct proof | source-pinned plantri census/isomorphism |
| exact side/loss/rate table | §3.5 | finite scalar identities | exact SymPy table |
| geometric uniqueness up to `O(3)`/`SO(3)` | §3.6 | ordinary face propagation | exact Gram/hull certificates |
| pointwise `delta` bound | §4.1 | `QuantitativeGlobalNearRigidity.lean` | path/small-`kappa` stress |
| adjacent/path/diameter rate bounds | §4.2 | selected adjacent algebra | long-path stress |
| incident/global/reference edge-loss bounds | §4.3 | selected finite algebra | reference-bound stress |
| geodesic arccos conversion | §4.4 | ordinary calculus | high-precision derivative audit |
| reversible stationary measure | §5.1 | finite conductance algebra | exact small graph |
| Dirichlet-energy bound | §5.2 | finite directed-sum boundary | exact energy audit |
| Poincare variance/sup bounds | §5.3 | ordinary variational proof | spectral-gap small graph checks |
| effective-resistance pointwise bound | §5.4 | ordinary Dirichlet principle | exact rational path resistance |
| uniform side reference and `Delta_theta` | §6.1 | ordinary proof | arc conversion audit |
| explicit positive angle-sine floor and `C_ang` | §6.2 | ordinary Gram/Heron factorization plus derivative proof | zero-defect and positive-width box audit |
| integer valence separation | §6.3 | ordinary proof | exact `g_kappa` values |
| edge distance to exact `theta_q` | §6.4 | ordinary mean-value proof | `alpha_eq'` audit |
| explicit conservative `eta_*` | §6.5 | ordinary inequalities with fixed Gram/Heron box | nonzero threshold tests at q=3,4,5 |
| `tr C_i=4`, radial covariance | §7.1 | `QEqualityCovariance.lean` | covariance audit |
| exact `T_i,C_i,M_i` decomposition | §7.2 | finite entrywise decomposition | weighted octahedron symbolic audit |
| axial iff tangent second moment is isotropic | §7.3 | scalar/tensor finite core | exact parameter equalities |
| antipodal radial boundary | §7.4 | `qOne_antipodal_*` | exact two-state regression |
| weighted octahedron counterexample | §7.5 | selected scalar identities | exact three-parameter SymPy family |
| genuine sampled degree-two space `{0}` | §7.5 | ordinary sampling-map argument | exact positive determinant of `P+2I` |
| near-equality radial bound and tangent non-control | §7.6 | finite inequality | exact anisotropy limit |

## Claim-control and stage records

* `docs/CLAIM_MATRIX.md`
* `docs/CONJECTURE_REGISTER.md`
* `docs/PURE_MATH_PRIOR_ART_MAP.md`
* `docs/THEOREM_TO_FILE_MAP.md`
* `docs/PROMPT3_GLOBAL_RIGIDITY_STAGE_REPORT.md`
* `docs/PROMPT3_FINAL_INTEGRATION_RECORD.md`
* `docs/PROMPT4_REACCEPTANCE_AFTER_P3_RECONCILIATION.md`
* `docs/FINAL_PURE_MATH_ACCEPTANCE.md`
* `pure_math/rigidity/APPROACH_REGISTRY.md`
* `pure_math/rigidity/THEOREM_REGISTRY.md`

## Verification workflow

`.github/workflows/afp-global-rigidity.yml` runs all accepted Prompt 1 and
Prompt 2 regressions, every Prompt 3 audit, literal source-pinned plantri
enumeration, Python syntax checks, the full Lean 4.30/Mathlib 4.30 build,
focused axiom output, aggregate placeholder/user-axiom rejection, independent
kernel checking where available, archive verification, and a pure-math-only
path audit on the literal checked-out head.

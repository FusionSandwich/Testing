# Prompt 2 theorem-to-file map — corrective closeout

This map distinguishes ordinary proof, Lean-checked finite algebra, exact
symbolic regression, and standard external input. A nonzero matrix, nonzero
exact form, nonzero sampled function, and nonzero exact sampled function remain
separate objects.

| Prompt 2 item | Ordinary proof | Lean support | Exact audit | Status |
|---|---|---|---|---|
| Finite covariance identity | Theorem 1.1 in `pure_math/covariance/SAMPLED_QUADRATIC_EXACTNESS_THEOREM.md` | `jumpGenerator_quadratic_covariance_identity` | Existing Platonic direct residual checks | PROVED / LEAN |
| Shifted quadratic target | Theorem 1.2 | `quadratic_target_eigen_iff` | Existing exact generator checks | PROVED / LEAN |
| Trace-free form characterization | Theorem 2.1 | trace-free contraction theorem | Exact constraint matrices | PROVED |
| Residual-through-sampling factorization | Theorem 2.2 | covariance identity plus `samplingKernel_le_residualKernel` | `R=(G+2dI)S` on exact examples | PROVED / LEAN CONSEQUENCE |
| Genuine sampled range | Theorem 2.2 | `sampledRange_exact_eq_range_inf_ker` | Exact ranks and kernels | PROVED / LEAN |
| Sampled dimension formula | Theorem 2.2 | `sampledRestriction_finrank` plus kernel inclusion | Existing and closeout rank checks | PROVED |
| Positive axial rigidity | Theorems 3.1–3.2 | axial coefficient and row-scaling lemmas | Platonic row scaling | PROVED / SHARP |
| Regular-simplex equality family | Corollary 3.3 | ordinary exact construction | `prompt2_closeout_audit.py`, dimensions `2,...,10` | PROVED EXACT FAMILY |
| Corrected equivariant rigidity | Theorem 4.1 | ordinary representation proof using exact covariance identity | Signed adversarial regression | PROVED WITH `a_ij>=0` FOR ALL `i!=j` |
| Signed pentagon counterexample | Counterexample 4.2 | not a Lean theorem | exact `Q(sqrt(5))` generator, ranks, and discriminant | PROVED EXACT COUNTEREXAMPLE |
| Tetrahedron classification | Section 5.1 | general Lean algebra | rank `R=S=3`, form/kernel dimension 2 | PROVED EXACT |
| Octahedron classification | Section 5.1 | general Lean algebra | rank `R=S=2`, form/kernel dimension 3 | PROVED EXACT |
| Cube classification | Section 5.1 | general Lean algebra | rank `R=S=3`, form/kernel dimension 2 | PROVED EXACT |
| Icosahedron classification | Section 5.1 | general Lean algebra | determinant `32(11+5sqrt(5))` | PROVED EXACT |
| Dodecahedron classification | Section 5.1 | general Lean algebra | determinant `-192` | PROVED EXACT |
| Four-point signed restoration | Section 5.2 | direct matrix algebra | sampled dimension one | PROVED EXACT |
| Forced negative rate `-1/2` | Section 5.2 | ordinary three-equation solve | exact solve | PROVED SHARP ON FIXED SUPPORT |
| Bilinear product identity | Theorem 6.1 | `jumpGenerator_product_identity_gamma` | symbolic residual audit | PROVED / LEAN |
| Arbitrary shifted product residual | Theorem 6.2 | `jumpGenerator_shifted_product_residual`, `shifted_product_target_iff` | exact symbolic identity | PROVED / LEAN |
| Additive product resonance | Theorem 6.2 | `additive_product_resonance_iff` | exact symbolic identity | PROVED / LEAN |
| Centered square resonance | Theorem 6.2 | `centered_square_resonance_iff` | exact symbolic identity | PROVED / LEAN |
| Uncentered square corollary | Theorem 6.2 consequences | `uncentered_square_resonance_iff_zero_gamma`, `uncentered_square_resonance_forces_value_zero` | `c=0` exact assertion | PROVED / LEAN |
| Boolean centered square | Counterexample 6.3 | general Lean theorem applies | exact four-state matrix and `Gamma=4` | PROVED EXACT EXAMPLE |
| Centered semigroup variance | Theorem 7.1 | ordinary finite matrix-semigroup proof | exact Boolean exponential identity | PROVED |
| Jensen inequality/equality support | Theorem 7.2 | standard external finite Markov result | Boolean positive-variance adversary | PROVED / EXTERNAL INPUT |
| Spherical target shift | Section 8 | arithmetic proof | exact integer assertion | PROVED |
| `S^2` `ell=1,...,6` table | Section 8 | not a Lean theorem | `prompt2_closeout_audit.py` exact rows | PROVED EXACT ARITHMETIC |
| Odd/even equality-set warnings | Section 8 | ordinary parity argument | adversarial audit | PROVED |
| Sampling kernels and cross-degree aliases | Sections 2 and 8 | sampling-map Lean core | Platonic exact aliases | PROVED BOUNDARY |
| Generalized Pell resonance | Section 9 | negative-Pell reformulation | existing and closeout exact assertions | PROVED ARITHMETIC / BOUNDED SEARCH |
| General spectral-product hierarchy | Section 9 | kill-criterion analysis | no sampled tradeoff/multiplicity/global theorem found | REJECTED FOR PROMPT 2 |
| Abstract equal-rate/equal-loss propagation | `AFPBarrier/GlobalLossRigidity.lean` and claim documents | three named Lean theorems | existing build/nanoda gates | PROVED / LEAN |
| Spherical `Q=1` specialization, restricted triangulation classification, near-rigidity | `docs/PROMPT3_READINESS_HANDOFF.md` | not yet formalized | not begun in closeout | PROMPT 3 TARGETS |
| Singular and plural user-axiom policy | workflow source | aggregate source scan and fixtures | exact workflow fixture step | VERIFIED CI POLICY |
| Claim and priority control | `CLAIM_MATRIX.md`, `CONJECTURE_REGISTER.md`, `PURE_MATH_PRIOR_ART_MAP.md` | not Lean claims | document cross-audit | CONTROLLED |

## File inventory

### Mathematical proof and summaries

- `pure_math/covariance/SAMPLED_QUADRATIC_EXACTNESS_THEOREM.md`
- `pure_math/covariance/QUADRATIC_COVARIANCE_DERIVATION.md`
- `docs/PROMPT2_QUADRATIC_COVARIANCE_STAGE_REPORT.md`
- `docs/PROMPT2_CLOSEOUT_AUDIT.md`

### Formalization

- `AFPBarrier/QuadraticCovariance.lean`
- `AFPBarrier/GlobalLossRigidity.lean`
- `AFPBarrier/PureMathAxiomAudit.lean`
- `AFPBarrier.lean`

### Exact regression

- `pure_math/covariance/quadratic_covariance_audit.py`
- `pure_math/covariance/prompt2_closeout_audit.py`
- existing Prompt 1 falsification and feasibility audits

### Verification policy

- `.github/workflows/afp-quadratic-covariance.yml`
- `.github/workflows/afp-spherical-feasibility.yml`
- `.github/workflows/afp-pure-math.yml`

## Standard external boundary

The project does not reprove finite Markov uniformization, strict-convexity
Jensen equality, the full spherical-harmonic product decomposition, or general
real representation irreducibility. Those inputs are stated with the exact
finite-generator, sampling, and positivity hypotheses required for transfer.

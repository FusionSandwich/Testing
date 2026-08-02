# Prompt 2 theorem-to-file map

This map distinguishes ordinary proof, Lean-checked finite algebra, exact
symbolic examples, and standard external inputs. A nonzero matrix, nonzero
exact form, nonzero sampled function, and nonzero exact sampled function are
separate objects throughout.

| Prompt 2 item | Ordinary proof | Lean support | Exact audit | Status |
|---|---|---|---|---|
| Finite covariance identity | Theorem 1.1 in `pure_math/covariance/SAMPLED_QUADRATIC_EXACTNESS_THEOREM.md` | `jumpGenerator_quadratic_covariance_identity` in `AFPBarrier/QuadraticCovariance.lean` | Direct generator residual equals covariance contraction for every Platonic basis form | PROVED / Lean |
| Shifted target-eigenvalue residual | Theorem 1.2, equations (1.8)–(1.11) | `quadratic_target_eigen_iff` | Direct residual checks use target `-6` | PROVED / Lean |
| Trace-free spherical form characterization | Theorem 2.1, equation (2.8) | `finiteMatrixContraction_tracelessProjection` | Constraint matrices built exactly | PROVED / Lean consequence |
| Shifted trace-free form condition | Equation (2.9) | Ordinary finite linear algebra | Exact Platonic first/second moments exclude nonzero constant samples | PROVED |
| Sampling map and kernel | Section 3 | Finite linear definitions | Exact evaluation matrices | PROVED |
| Residual-through-sampling factorization | Equation (3.5), `R_X=(L+2dI)S_X` | `samplingKernel_le_residualKernel` and covariance identity | Exact matrix identity `R=(G+6I)S` on every Platonic graph | PROVED / Lean consequence |
| Sampling aliases lie in form kernel | Equation (3.7), `K_X subset E_form` | `samplingKernel_le_residualKernel` | Every exact null vector of `S` is checked in `ker R` | PROVED / Lean |
| Genuine sampled exact space | Theorem 3.1, equation (3.8) | `sampledRange_exact_eq_range_inf_ker` | Exact sampled image/eigenspace intersection checked through factorization | PROVED / Lean |
| General restriction dimension identity | Equation (3.9) | `sampledRestriction_finrank` | Exact null-space dimensions | PROVED / Lean |
| Specialized dimension identity | Equations (3.10), (3.15): `dim E_sample=dim E_form-dim K_X=rank S-rank R` | Rank-nullity plus kernel inclusion | Exact symbolic ranks for all examples | PROVED / exact regression |
| Stacked-rank collapse | Equations (3.16)–(3.17): `rank([R;S])=rank S` | Consequence of factorization | Exact abstract and Platonic checks | PROVED / exact regression |
| Trace and radial covariance | Lemma 4.1 | Finite covariance algebra | Checked exactly at every Platonic vertex | PROVED |
| Local axial covariance formula | Theorem 4.2, equations (4.6)–(4.7) | `axialCovariance_projectionCoefficient`; trace-free contraction | Exact covariance tensors | PROVED / Lean consequence |
| Global axial sampled rigidity | Theorem 4.3 | `zero_constraints_iff_zero_samples_of_row_scaling` | Constraint matrix is an exact positive row scaling of sampling matrix | PROVED / sharp theorem |
| Local versus global axial exactness | Theorem 4.3 discussion | Ordinary proof | Vertexwise constraint checks | PROVED |
| Regular-simplex equality family | Corollary 4.4 | Ordinary exact construction | General formulas; tetrahedron is the `d=3` instance | PROVED / sharp family |
| Equivariant irreducibility rigidity | Theorem 4.5 | Ordinary representation argument plus positive radial covariance | Icosahedral examples are compatible with conclusion | PROVED / structural theorem |
| Tetrahedron exact classification | Section 5 | General Lean algebra | `rank R=rank S=3`, form/kernel dimension `2`, sampled dimension `0` | PROVED / exact certificate |
| Octahedron exact classification | Section 5 | General Lean algebra | `rank R=rank S=2`, form/kernel dimension `3`, sampled dimension `0` | PROVED / exact certificate |
| Cube exact classification | Section 5 | General Lean algebra | `rank R=rank S=3`, form/kernel dimension `2`, sampled dimension `0` | PROVED / exact certificate |
| Icosahedron exact classification | Section 5 | General Lean algebra | Evaluation determinant `32(11+5 sqrt(5))` | PROVED / exact certificate |
| Dodecahedron exact classification | Section 5 | General Lean algebra | Evaluation determinant `-192` | PROVED / exact certificate |
| Signed four-point restoration | Section 6 | Direct exact matrix proof in ordinary text | Exact matrix products | PROVED / exact certificate |
| Forced negative rate `-1/2` | Equations (6.6)–(6.7) | Ordinary three-equation solve | SymPy exact solve | PROVED / sharp fixed-support result |
| Carré-du-champ product obstruction | Section 7.1 | `jumpGenerator_product_identity`; square identity in `JumpGenerator.lean` | Sign/equality cases independently audited | PROVED / standard mechanism |
| Semigroup/Jensen obstruction | Section 7.2 | Standard finite Markov semigroup theorem used externally | Reachability/equality logic audited | PROVED / external standard input |
| Harmonic parity and product image | Section 8.1 | Ordinary harmonic decomposition | Exact degree enumeration | PROVED / standard representation input |
| Odd/even zonal equality sets | Section 8.2 | Ordinary Gegenbauer/trigonometric parity argument | Adversarial equality-set audit | PROVED |
| Sampling aliases and component identifiability | Section 8.3 | Ordinary sampling-map argument | Platonic kernels give exact aliases | PROVED |
| Additive resonance arithmetic | Section 8.4 | Generalized negative-Pell reformulation | Exact bounded list and infinite `d=4` family prefix | PROVED ARITHMETIC / COMPUTATIONAL SEARCH |
| General spectral-product hierarchy | Section 8 conclusion | Kill-criterion analysis | Pell resonances still give no sampled identifiability, dimension tradeoff, or global result | REJECTED FOR PROMPT 2 |
| Prior-art and novelty boundary | `docs/PURE_MATH_PRIOR_ART_MAP.md` | Not a Lean claim | Source-backed review | CONTROLLED |
| Claim/conjecture status | `docs/CLAIM_MATRIX.md`, `docs/CONJECTURE_REGISTER.md` | Not a Lean claim | Regression links retained | CONTROLLED |

## Standard external boundary

The project does not reprove equality in Jensen's inequality, finite
continuous-time Markov uniformization, spherical-harmonic Fischer/Clebsch–Gordan
decomposition, or elementary real representation irreducibility facts. General
finite-dimensional rank-nullity is imported from Mathlib and applied to the
sampling map restricted to the exact-form subspace. Every external input is
stated with the hypotheses needed to transfer it to the concrete finite
generator, embedding, sampling map, and target eigenvalue.

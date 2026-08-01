# Prompt 2 theorem-to-file map

This map distinguishes ordinary proof, Lean-checked finite algebra, exact
symbolic examples, and standard external inputs. A nonzero matrix, nonzero
exact form, nonzero sampled function, and nonzero exact sampled function are
separate objects throughout.

| Prompt 2 item | Ordinary proof | Lean support | Exact audit | Status |
|---|---|---|---|---|
| Finite covariance identity | Theorem 1.1 in `pure_math/covariance/SAMPLED_QUADRATIC_EXACTNESS_THEOREM.md` | `jumpGenerator_quadratic_covariance_identity` in `AFPBarrier/QuadraticCovariance.lean` | Direct generator residual equals covariance contraction for every Platonic basis form | PROVED / Lean |
| Shifted target-eigenvalue residual | Theorem 1.2, equations (1.8)–(1.11) | `quadratic_target_eigen_iff` | Direct residual checks use target `-6` | PROVED / Lean |
| Trace-free spherical form characterization | Theorem 2.1, equation (2.8) | Trace-free contraction lemma in `QuadraticCovariance.lean` | Constraint matrices built exactly | PROVED |
| Shifted trace-free form condition | Equation (2.9) | Ordinary finite linear algebra | Exact Platonic centering and second moments exclude nonzero constant samples | PROVED |
| Sampling map and kernel | Section 3 | Ordinary linear definitions | Exact evaluation matrices | PROVED |
| Genuine sampled exact space | Theorem 3.1, equation (3.3) | Restricted sampling map in `sampledRestriction_finrank` | Sampled image computed exactly | PROVED / Lean consequence |
| Dimension identity with intersection | Equation (3.4) | `sampledRestriction_finrank` formalizes rank-nullity on the exact-form subspace | Negative test rejects naive kernel subtraction | PROVED / Lean / exact regression |
| Stacked-rank and null-basis formulas | Equations (3.7)–(3.10) | Standard finite matrix rank algebra | Exact SymPy ranks | PROVED / exact regression |
| Trace and radial covariance | Lemma 4.1 | Finite algebra consequences | Checked at every Platonic vertex | PROVED |
| Local axial covariance formula | Theorem 4.2, equations (4.7)–(4.8) | `axialCovariance_projectionCoefficient`; trace-free contraction | Exact covariance tensors | PROVED / Lean consequence |
| Global axial sampled rigidity | Theorem 4.3 | `zero_constraints_iff_zero_samples_of_row_scaling` | Constraint matrix is exact row scaling of sampling matrix | PROVED / sharp theorem |
| Local versus global axial exactness | Theorem 4.3 discussion | Ordinary proof | Vertexwise constraint checks | PROVED |
| Regular-simplex equality family | Corollary 4.4 | Ordinary exact construction | General formulas; Platonic tetrahedron is `d=3` instance | PROVED / sharp family |
| Equivariant irreducibility rigidity | Theorem 4.5 | Ordinary representation argument plus positive radial covariance | Icosahedral examples are compatible with conclusion | PROVED / structural theorem |
| Tetrahedron exact classification | Section 5 | General Lean algebra only | Exact rank `3`, form/kernel dimension `2`, sample dimension `0` | PROVED / exact certificate |
| Octahedron exact classification | Section 5 | General Lean algebra only | Exact rank `2`, form/kernel dimension `3`, sample dimension `0` | PROVED / exact certificate |
| Cube exact classification | Section 5 | General Lean algebra only | Exact rank `3`, form/kernel dimension `2`, sample dimension `0` | PROVED / exact certificate |
| Icosahedron exact classification | Section 5 | General Lean algebra only | Evaluation determinant `32(11+5 sqrt(5))` | PROVED / exact certificate |
| Dodecahedron exact classification | Section 5 | General Lean algebra only | Evaluation determinant `-192` | PROVED / exact certificate |
| Signed four-point restoration | Section 6 | Direct exact matrix proof in ordinary text | Exact matrix products | PROVED / exact certificate |
| Forced negative rate `-1/2` | Equations (6.6)–(6.7) | Ordinary three-equation solve | SymPy exact solve | PROVED / sharp fixed-support result |
| Carré-du-champ product obstruction | Section 7.1 | `jumpGenerator_product_identity`; square identity already in `JumpGenerator.lean` | Sign cases independently audited | PROVED / standard mechanism |
| Semigroup/Jensen obstruction | Section 7.2 | Standard finite Markov semigroup theorem used externally | Reachability/equality logic audited | PROVED / external standard input |
| Harmonic parity and product image | Section 8.1 | Ordinary harmonic decomposition | Exact degree enumeration | PROVED / standard representation input |
| Odd/even zonal equality sets | Section 8.2 | Ordinary Gegenbauer parity argument | Adversarial equality-set audit | PROVED |
| Sampling aliases and component identifiability | Section 8.3 | Ordinary sampling-map argument | Platonic kernels are exact aliases | PROVED |
| Additive resonance arithmetic | Section 8.4 | Generalized negative-Pell reformulation | Exact bounded list and infinite `d=4` family prefix | PROVED ARITHMETIC / COMPUTATIONAL SEARCH |
| General spectral-product hierarchy | Section 8 conclusion | Kill-criterion analysis | Pell resonances still give no sampled identifiability, dimension tradeoff, or global result | REJECTED FOR PROMPT 2 |
| Prior-art and novelty boundary | `docs/PURE_MATH_PRIOR_ART_MAP.md` | Not a Lean claim | Source-backed review | CONTROLLED |
| Claim/conjecture status | `docs/CLAIM_MATRIX.md`, `docs/CONJECTURE_REGISTER.md` | Not a Lean claim | Regression links retained | CONTROLLED |

## Standard external boundary

The project does not reprove equality in Jensen's inequality, finite
continuous-time Markov uniformization, spherical-harmonic Fischer
decomposition, or basic real representation irreducibility facts. General
finite-dimensional rank-nullity is imported from Mathlib and applied to the
sampling map restricted to the exact-form subspace. The paper states the exact
hypotheses under which all external inputs are used, and transfers their
consequences to the concrete finite generator, embedding, matrices, and signs.

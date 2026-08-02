# Prompt 2 theorem-to-file map

This map distinguishes a mathematical claim from its ordinary proof, Lean
kernel proof, and deterministic finite certificate.  A finite computation is
never listed as a proof of the general theorem.

The only claim labels used are `PROVED`, `EXTERNAL`, `COMPUTATIONAL`,
`CONJECTURE`, and `REJECTED`.

| theorem family | claim label | ordinary proof | Lean kernel | deterministic certificate | completion note |
|---|---|---|---|---|---|
| product identity and arbitrary target | PROVED | `pure_math/spectral_products/SPECTRAL_PRODUCT_ANALYSIS.md` | `AFPBarrier/SpectralProductAlgebra.lean` | `exact_spectral_product_audit.py` | retain and audit |
| covariance identity and arbitrary target | PROVED | `pure_math/covariance/QUADRATIC_COVARIANCE_THEOREM.md` | `AFPBarrier/QuadraticCovariance.lean` | `exact_quadratic_covariance_audit.py` | weighted centering missing |
| sphere residual factorization | PROVED | `QUADRATIC_COVARIANCE_THEOREM.md` | pending narrow residual module | `exact_quadratic_covariance_audit.py` | explicit trace-free theorem missing in Lean |
| genuine sampled dimension | PROVED | `QUADRATIC_COVARIANCE_THEOREM.md` | generic part in `QuadraticSampling.lean` | exact sampling ranks | full finite-dimensional equality missing in Lean |
| positive full-module obstruction | PROVED | `QUADRATIC_COVARIANCE_THEOREM.md` | not separately required | exact positive examples | final proof audit pending |
| signed one-shell tangent-isotropy rigidity | PROVED | `QUADRATIC_COVARIANCE_THEOREM.md` | pending one-shell module | Platonic and prism audits | radial/tangent Lean core missing |
| positive hexagonal-prism sharpness | COMPUTATIONAL | draft proof in `QUADRATIC_COVARIANCE_THEOREM.md` | not required | `exact_quadratic_covariance_audit.py` | connectivity/transitivity checks missing |
| equivariance and multiplicity-free kernel formula | PROVED | proof completion pending in theorem document | broad representation formalization not required | finite examples | isotypic argument must be written explicitly |
| quotient residual rank gap | PROVED | proof completion pending in theorem document | broad representation formalization not required | cube/hexagon examples | exact hypotheses must remain visible |
| omitted-invariance `D_3` counterexample | COMPUTATIONAL | proof completion pending in theorem document | not required | tracked audit missing | mandatory file absent at WIP |
| five Platonic classification | COMPUTATIONAL | `QUADRATIC_COVARIANCE_THEOREM.md` | not required | `exact_quadratic_covariance_audit.py` | exact minors/rates must remain recorded |
| signed cube restoration and optimum `2` | PROVED | proof completion pending in theorem document | not required | `exact_signed_restoration_audit.py` | averaging, alias, and dual checks incomplete |
| finite spectral-sampling direct sum and rank bound | PROVED | `SPECTRAL_PRODUCT_ANALYSIS.md` | pending spectral-sampling module | exact harmonic ranks | Lean theorem missing |
| continuous `S^2` symmetric-square decomposition | EXTERNAL | `SPECTRAL_PRODUCT_ANALYSIS.md` | not required | dimension/eigenvalue checks | standard Clebsch--Gordan input |
| parity-filtered negative Pell classification | EXTERNAL | `SPECTRAL_PRODUCT_ANALYSIS.md` | not required | `exact_spectral_product_audit.py` | standard Pell input; recurrence retained |
| semigroup variance identity | PROVED | `SPECTRAL_PRODUCT_ANALYSIS.md` | not required | Boolean example | full finite-dimensional proof must be expanded |
| Jensen variance/equality and uniformization | EXTERNAL | `SPECTRAL_PRODUCT_ANALYSIS.md` | not required | Boolean non-equality example | standard finite Markov theory |
| universal positive spectral-product hierarchy | REJECTED | `SPECTRAL_PRODUCT_ANALYSIS.md` | not applicable | exact aliases | rejected without added nonaliasing/component hypotheses |

## Exact external inputs

- finite-dimensional rank-nullity and quotient dimension;
- finite real representation semisimplicity and Schur/spectral arguments;
- tight-frame moment algebra;
- Clebsch--Gordan decomposition for real spherical harmonics on `S^2`;
- classification of positive solutions of the negative Pell equation; and
- finite Markov-kernel Jensen equality and continuous-time uniformization.

These inputs are standard mathematics.  The project contribution boundary is
the sampling-kernel-aware covariance framework, the signed one-shell
full-tangent-isotropy factorization, the positive prism sharpness example, the
equivariant quotient rank gap, the signed-cube optimum, and their combined
sampling-safe interpretation.


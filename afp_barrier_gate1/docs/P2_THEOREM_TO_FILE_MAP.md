# Prompt 2 theorem-to-file map

This map separates complete ordinary proof, Lean kernel support, exact finite
regression, and EXTERNAL standard inputs. A deterministic finite calculation is
not presented as the proof of a general theorem.

| theorem family | label | ordinary proof | Lean support | exact finite support |
|---|---|---|---|---|
| finite product identity and arbitrary target | PROVED | pure_math/spectral_products/SPECTRAL_PRODUCT_ANALYSIS.md §§1–2 | AFPBarrier/SpectralProductAlgebra.lean | exact_spectral_product_audit.py |
| covariance identity and arbitrary target, including \(\mu=0\) | PROVED | pure_math/covariance/QUADRATIC_COVARIANCE_THEOREM.md §2 | AFPBarrier/QuadraticCovariance.lean | exact_quadratic_covariance_audit.py |
| weighted centering and zero-target independence | PROVED | covariance theorem §2 | AFPBarrier/QuadraticCovariance.lean | not required; the result is finite algebra |
| sphere residual factorization | PROVED | covariance theorem §3 | AFPBarrier/QuadraticSphereResidual.lean | exact_quadratic_covariance_audit.py |
| sampling kernel, range intersection, and dimension equality | PROVED | covariance theorem §3 | AFPBarrier/QuadraticSampling.lean and QuadraticSphereResidual.lean | all covariance sampling ranks |
| positive residual and Frobenius obstruction (nonempty \(I\), \(d>1\), nonnegative unit eigenmap) | PROVED | covariance theorem §4 | not separately formalized; the formal sphere-residual definitions fix the conventions | positive Platonic/prism regressions |
| signed one-shell tangent-isotropy rigidity (unit \(L\Phi=-(d-1)\Phi\) eigenmap, \(d>1\), nonempty shell, \(0<\ell_i<2\)) | PROVED | covariance theorem §5 | AFPBarrier/OneShellQuadraticRigidity.lean | Platonic \(R=\kappa S\) checks |
| positive hexagonal-prism sharpness | PROVED | covariance theorem §6 | no broad graph formalization required | exact_quadratic_covariance_audit.py |
| prism graph, action, matrices, ranks, and minors | COMPUTATIONAL | values recorded in covariance theorem §6 | not applicable | exact_quadratic_covariance_audit.py |
| multiplicity-free kernel formulas and quotient rank gap under invariant generator rates | PROVED | covariance theorem §7 | representation theory remains a stated EXTERNAL input | exact positive rank-gap examples |
| corrected scalar theorem for a preserved self-adjoint irreducible copy | PROVED | covariance theorem §7 | self-adjoint spectral theorem is EXTERNAL | exact \(D_3\) negative regression |
| omitted-invariance shortcut | REJECTED | covariance theorem §7 | not applicable | exact_d3_invariance_counterexample.py |
| five Platonic classification | PROVED | covariance theorem §8 | one-shell Lean core | exact_quadratic_covariance_audit.py |
| Platonic matrices, kernels, actions, and minors | COMPUTATIONAL | exact values recorded in theorem §8 | not applicable | exact_quadratic_covariance_audit.py |
| signed cube restoration at coordinate target \(-2\), cross target \(-6\), and global optimum two | PROVED | covariance theorem §9 | no LP formalization required | exact_signed_restoration_audit.py |
| signed cube matrices, aliases, group action, and KKT | COMPUTATIONAL | values recorded in theorem §9 | not applicable | exact_signed_restoration_audit.py |
| semigroup variance and derivative converse | PROVED | spectral analysis §3 | finite matrix-exponential proof in prose | Boolean exact regression |
| Jensen equality and irreducible uniformization | EXTERNAL | exact transfer in spectral analysis §3 | not required | Boolean non-equality regression |
| continuous \(S^2\) symmetric-square decomposition | EXTERNAL | spectral analysis §5 | not required | component/dimension checks |
| parity-filtered Pell completeness | EXTERNAL | parity transfer and recurrence in spectral analysis §5 | not required | exact_spectral_product_audit.py |
| common-operator target-eigenvalue-class direct sum, rank bound, and converse | PROVED | spectral analysis §6 | AFPBarrier/SpectralSamplingObstruction.lean | exact positive and rejection cases |
| unrestricted all-dimension distinct-degree theorem | REJECTED | exact \(d=1\) witness in spectral analysis §6 | rejection retained in spectral module boundary | exact_spectral_product_audit.py |
| Platonic \(H_2/H_4\) aliases and antipodal rank compression | COMPUTATIONAL | identities recorded in spectral analysis §6 | not required | exact_spectral_product_audit.py |
| universal positivity-only spectral hierarchy | REJECTED | spectral analysis final status | not applicable | Boolean and alias regressions |

## Exact external inputs

- finite-dimensional rank-nullity and quotient dimension;
- finite real Maschke semisimplicity and self-adjoint spectral arguments;
- tight-frame moment background;
- convex invariant averaging and subgradient/KKT optimality;
- Clebsch--Gordan decomposition for real spherical harmonics on \(S^2\);
- completeness of positive negative-Pell solutions; and
- finite Markov-kernel Jensen equality and continuous-time uniformization.

The candidate contribution boundary is the combined sampling-kernel-aware
covariance framework, signed one-shell factorization, positive prism sharpness,
equivariant quotient rank gap, signed-cube optimum, and sampling-safe spectral
interpretation. No priority claim is made from a standard input, covariance
identity, exact rank table, Lean build, or CI result alone.

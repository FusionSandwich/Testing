# Prompt 2 theorem registry

| theorem | exact hypotheses | conclusion | claim label | ordinary proof | formal or exact support |
|---|---|---|---|---|---|
| covariance identity | finite \(I\), coordinate eigenmap; no signs | \(LS_A=-2\lambda S_A+\operatorname{tr}(AC_i)\) | PROVED | Quadratic covariance theorem §2 | QuadraticCovariance.lean |
| arbitrary target | any \(c,\mu\), including \(\mu=0\) | exact pointwise residual iff | PROVED | theorem §2 | QuadraticCovariance.lean |
| weighted centering | nonempty \(I\), \(w_i>0\), detailed balance, \(\mu\ne0\) | \(c\) is weighted mean; pointwise residual still required | PROVED | theorem §2 | QuadraticCovariance.lean |
| zero-target center | arbitrary finite generator, form, and samples; \(\mu=0\) | the generator kills constants algebraically, so the equation is independent of \(c\) | PROVED | theorem §2 | QuadraticCovariance.lean |
| sphere residual | unit nodes, \(\lambda=d-1\), trace-free forms | \(R_X=(L+2dI)S_X\), \(R_X(A)_i=\langle A,M_i\rangle\) | PROVED | theorem §3 | QuadraticSphereResidual.lean |
| genuine sampled dimension | finite-dimensional sampling and residual maps | range intersection and \(\dim E_{\rm sample}=\operatorname{rank}S-\operatorname{rank}R\) | PROVED | theorem §3 | QuadraticSampling.lean |
| positive full-module obstruction | nonempty finite \(I\), \(d>1\), nonnegative rates, unit eigenmap with \(L\Phi=-(d-1)\Phi\) | every \(M_i\ne0\), rank gap and Frobenius bound | PROVED | theorem §4 | ordinary proof; exact positive regressions |
| signed one-shell rigidity | \(d>1\), unit nodes with \(L\Phi=-(d-1)\Phi\), nonempty noncoincident shell, \(0<\ell_i<2\), full signed tangent moment | covariance split, \(R_X=DS_X\), \(E_{\rm form}=K_X\), no genuine sample | PROVED | theorem §5 | OneShellQuadraticRigidity.lean |
| positive prism sharpness | specified 12-node prism, rates \(2,1\) | all graph properties; anisotropy; injective \(S\); two genuine modes | PROVED | theorem §6 | exact_quadratic_covariance_audit.py |
| multiplicity-free kernels | finite group, orthogonal equivariant embedding, invariant generator \(a_{gi,gj}=a_{ij}\), multiplicity-free real form module | exact \(E_{\rm form}\), \(K_X\), and \(E_{\rm sample}\) summand formulas | PROVED | theorem §7 | standard real semisimplicity is EXTERNAL |
| equivariant rank gap | positive sphere hypotheses, equivariant embedding, and invariant generator rates | \(\operatorname{rank}R_X\ge\kappa(V_2)\); irreducible \(V_2\) has no exact sample | PROVED | theorem §7 | quotient residual proof |
| omitted invariance shortcut | equivariance alone for a selected irreducible copy | false | REJECTED | theorem §7 | exact_d3_invariance_counterexample.py |
| corrected scalar theorem | irreducible \(U\), self-adjoint \(L\), and either \(L(U)\subseteq U\) or \(U\) equal to its entire ambient isotypic component | \(L|_U\) is a real scalar | PROVED | theorem §7 | standard spectral theorem is EXTERNAL |
| five Platonic classification | exact positive shortest-edge models scaled to coordinate target \(-2\) | table ranks/kernels; every \(E_{\rm sample}=0\) | PROVED | theorem §8 | exact_quadratic_covariance_audit.py |
| signed cube restoration | unit cube, complete symmetric conductances, coordinate target \(-2\), full sampled cross-module target \(-6\) | optimizer, dimensions, and \(\min N^-=2\) | PROVED | theorem §9 | exact_signed_restoration_audit.py |
| product resonance | finite generator, two eigenfunctions; no signs | arbitrary target and resonant constant-\(\Gamma\) iff | PROVED | Spectral product analysis §§1–2 | SpectralProductAlgebra.lean |
| blanket positive square obstruction | all positive generators | false | REJECTED | Boolean square proof | exact_spectral_product_audit.py |
| semigroup variance | finite matrix semigroup and square eigenfunction | exact variance identity and converse | PROVED | spectral analysis §3 | ordinary finite exponential proof |
| Jensen equality | positive Markov kernel; irreducible chain for global equality | support constancy; global constancy for \(t>0\) | EXTERNAL | spectral analysis §3 | exact Boolean non-equality regression |
| continuous \(S^2\) product | real spherical harmonics | \(\operatorname{Sym}^2(H_\ell)=\bigoplus_{r=0}^{\ell}H_{2r}\) | EXTERNAL | spectral analysis §5 | Clebsch--Gordan |
| Pell hierarchy | positive negative-Pell solutions plus even \(J\) | exponent \(4m+1\), first \((14,20)\), recurrence | EXTERNAL | parity transfer in spectral analysis §5 | exact_spectral_product_audit.py |
| target-class sampling separation | one common operator acts scalarly on finite sampled spaces grouped by equal target | distinct class sums are direct; rank bound; constants-safe signed and weighted converse | PROVED | spectral analysis §6 | SpectralSamplingObstruction.lean |
| unrestricted distinct-degree separation | no \(d\ge2\) or distinct-target hypothesis | false | REJECTED | exact \(d=1\) singleton witness | exact_spectral_product_audit.py |
| Platonic \(H_2/H_4\) aliases | five exact common-radius node sets | pair ranks, inclusions, and polynomial aliases | COMPUTATIONAL | spectral analysis §6 records identities | exact_spectral_product_audit.py |

## External-input boundary

EXTERNAL inputs are finite rank-nullity, real Maschke semisimplicity, the
self-adjoint spectral theorem, Jensen equality and uniformization,
Clebsch--Gordan decomposition on \(S^2\), and completeness of positive
negative-Pell solutions. Their project-specific hypotheses, signs, parity, and
sampling quotients are transferred explicitly.

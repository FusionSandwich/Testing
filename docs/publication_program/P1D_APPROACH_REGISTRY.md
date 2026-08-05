# P1D approach registry — quantitative frontier stability

This registry separates the unconditional stability mechanism from every
conditional geometric or graph upgrade. `COMPLETE` denotes an all-orders
proof in the ordinary theorem. `COMPLETE_AUDIT` denotes an exact or
outward-interval certificate for its implementation boundary. No numerical
fixture is used in place of a theorem.

| Mechanism family | Status | Concrete theorem or certificate | Necessary parameter or adversarial boundary |
|---|---|---|---|
| normalized frontier budget | COMPLETE | with `q_i=x_i-1=s_i+v_i` and `eta=2 delta+delta^2`, `sum w(2q+q^2)+(d-1)E_B/(d a_0^2)<=eta` | uses the P1B quotient trace theorem; no sampling injectivity or connectedness |
| scalar moment extraction | COMPLETE | requested `L^2(w)` bounds for `x-1`, `r_max/r_i-1`, and `V_i/a_0`, plus `L^1(w)` bounds by weighted Cauchy--Schwarz | normalization `sum w=1` is explicit |
| exceptional-vertex control | COMPLETE | mass of `{q,s,v>=rho}` is at most `H/[rho(2+rho)]`; pointwise envelope is `sqrt(1+H/w_i)-1` | unweighted and pointwise bounds require `w_min`; tiny-mass equality mixtures attain the scaling |
| residual tensor decomposition | COMPLETE | explicit weighted bounds for `B_i`, mixed covariance `h_i`, tangent anisotropy, and covariance eigenvalue splitting | radial eigenvector control additionally costs the local spectral gap `|c_0-2|` |
| conductance normalization | COMPLETE | symmetric directed probability `nu_ij=gamma_ij/bar r` and exact global-shell loss identity give conductance-mass Chebyshev bounds | vertex mass and conductance mass are not interchangeable |
| minimum transition probability | COMPLETE | `p_ij>=kappa` converts local variance into edgewise loss control with explicit `kappa^{-1/2}` | compass fixture has fixed vertex masses and a bad edge of mass `kappa` |
| path multiplication and path energy | COMPLETE | explicit multiplicative path factors, additive `sqrt(L)` estimate, effective-resistance, spectral-gap, and congestion alternatives | diameter, resistance, gap, and overlap/congestion cannot be suppressed |
| quotient Hilbert--Schmidt transfer | COMPLETE | `||R_2-c_0S_2||_HS^2<=K_0`; quotient operator deviation is at most `sqrt(K_0/alpha_X)` | coefficient aliases are quotiented; near-singular sampling attains `alpha_X^{-1/2}` |
| shell spectral splitting | COMPLETE | compressed sampled shell lies in `[mu_0-rho_X,mu_0+rho_X]`, including leakage control without range invariance | depends explicitly on the sampling lower-frame constant `alpha_X` |
| raw tangent whitening | COMPLETE | under `T_i/r_i >= lambda P_i`, polar whitening constructs a centered weighted tight frame with an explicit Procrustes bound | `lambda` is necessary; nearly rank-one vertex figures defeat an absolute `B,V` theorem |
| normalized-frame whitening | COMPLETE | under shell margins and tangent lower bound, normalized figures lie near exact weighted tight frames modulo tangent rotations | antipodal/vanishing shells require a separate branch |
| positive unit-frame repair | COMPLETE | feature-surjectivity margin `mu`, probability floor `kappa`, and shell floor `s_-` yield explicit positive weight and spherical-neighbor repair | active degree and feature overlap are stated, not inferred from connectivity |
| global embedding stability | NOT_USED | no external global gluing theorem is invoked | zero-loss bridges retain arbitrary relative tangent rotations |
| exact symbolic adversaries | COMPLETE_AUDIT | 30 deterministic fixtures cover master constants, tiny masses, aliases, small `kappa`, long paths, singular frames, sampling gaps, and interval scales | exact arithmetic makes every rank and alias decision |
| interval stress testing | COMPLETE_AUDIT | outward-rounded intervals cover `delta` and scale parameters over forty orders of magnitude | interval checks audit implementation only |
| Lean elementary core | COMPLETE_CANDIDATE | normalized square/linear/tensor budgets, component extraction, pointwise `w_min`, exceptional mass, and scaled variance | the geometric spectral and inverse-square-root calculus stays in the ordinary proof |
| semigroup restriction | REJECTED | no proof route | `im S_2` need not be invariant under `L`; P1D uses compression and leakage bounds instead |

## Search and adversarial rounds

1. Weighted-Gram, quotient Hilbert--Schmidt, and random-matrix routes were
   kept independent until they reproduced the same normalized master budget.
2. A separate conductance-probability route derived edge fractions before any
   lower edge-probability assumption was introduced.
3. Path multiplication, path energy, effective resistance, and Poincare-gap
   routes were compared so no diameter, gap, or congestion constant could be
   silently absorbed.
4. Raw polar whitening and unit-frame weight repair were developed as
   different geometric theorems. The latter requires feature surjectivity and
   positivity margins that the former does not.
5. Tiny-mass, compass-edge, long-cycle/ramp, nearly singular tangent-frame,
   sampling-gap, and zero-loss bridge constructions independently audit the
   necessity of each extra hypothesis.
6. The formalization track records only stable finite scalar interfaces after
   the ordinary theorem fixed all constants and normalizations.

Permanent rejected mutations are: replacing weighted fractions by vertex
counts without `w_min`; turning conductance-mass control into edgewise control
without `kappa`; propagating without diameter/resistance/gap/congestion;
recovering coefficients without quotienting `K_X` and paying `alpha_X`;
normalizing tangent increments at an antipodal shell; or deducing a globally
aligned embedding from independent local tight frames.

# P2B prior-art, hypothesis-transfer, and hostile-referee audit

Status: **controlling scope audit**.  Sources are used only for their stated
physical or numerical results.  None is treated as a substitute for the
P2B semigroup, residual, stability, or adjoint proofs.

## 1. Primary-source comparison

| Source | Variables and hypotheses in the source | Source conclusion | P2B use and precise distinction | Hypothesis-transfer note |
|---|---|---|---|---|
| [Morel, 1981](https://doi.org/10.13182/NSE79-340) | standard discrete ordinates in one-dimensional slab and spherical geometry; Fokker--Planck calculation; time/steady and forward/adjoint use cases | a way to perform Fokker--Planck calculations in existing transport codes, including physical response calculations | application precedent; not the present weighted-Hilbert contraction, six-residual decomposition, or adjoint remainder estimator | P2B independently states the phase norm, boundary traces, accretivity, and reconstruction; no 1D code property is transferred to the general theorem |
| [Pomraning, 1992](https://doi.org/10.1142/S021820259200003X) | a scaled family of highly peaked scattering kernels in the linear transport equation | the Fokker--Planck operator is a formal asymptotic limit under additional conditions; high forward peaking is necessary, not sufficient; the Henyey--Greenstein example does not have the asserted FP limit | requires keeping $R_1=(A_{FP}-A_B)v$ as a separate physical-model residual | P2B makes no asymptotic claim for a material kernel; any smallness of $R_1$ must be supplied by a separate modal or kernel theorem |
| [Morel, Prinja, McGhee, Wareing, and Franke, 2007](https://doi.org/10.13182/NSE07-A2693) | an $S_N$ discretization of the three-dimensional angular FP operator; product and more general quadratures | the abstract reports null/zeroth preservation, self-adjointness, monotonicity, and nonpositive definiteness; all three first moments for product quadratures with Chebyshev azimuth, otherwise two of three | direct angular-discretization precedent; P2B starts from a generator already verified reversible and uses its measured all-shell residual | every P2B generator must pass its own reversibility, positivity, and moment tests; the source's quadrature restrictions are not broadened |
| [Bienvenue, Naceur, Carrier, and Hébert, 2025](https://doi.org/10.1080/00295639.2025.2462891) | nonorthogonal quadrature sets and shared Voronoi-edge finite-difference coefficients; numerical product, level-symmetric, and Lebedev examples | a flexible monotone moment-preserving angular FP discretization and numerical suppression of selected oscillations | closest audited modern monotone/moment precedent; P2B's scoped contribution is the alias-correct connection from the accepted defect to transient/steady/response certificates with an explicit transport-residual ledger | the [deposited manuscript](https://publications.polymtl.ca/64454/2/2025_Bienvenue_Flexible__Moment-Preserving_Monotone_Discretization_Multidimensional_SUPP.pdf) has a factor discrepancy: Eqs. 35--36 imply the $S^2$ first-shell factor $-2$, while printed Eq. 38 uses $-4w_k\Omega_k$. P2B retains $L\Omega=-2\Omega$ and does not import Eq. 38 |
| [Bienvenue and Hébert, 2022](https://doi.org/10.1016/j.anucene.2022.109032) | one- and two-dimensional Cartesian BFP calculations with DD1/DD2 spatial closures and manufactured/numerical benchmarks | fourth- and sixth-order spatial schemes and improved observed behavior relative to lower-order alternatives | spatial-discretization precedent and motivation for retaining $R_4$ independently | no general coercivity, boundary, or interface theorem is transferred; an order statement additionally needs the source's smoothness and consistency hypotheses |
| finite-dimensional spectral theorem and Hille--Yosida resolvent estimate | self-adjoint nonnegative $A=-L$ or an explicitly m-accretive transport operator | contraction semigroup and resolvent norm | external functional-analysis tool; P2B computes the exact multiplier and all problem-specific constants | self-adjointness follows from accepted detailed balance; transport m-accretivity/range and boundary assumptions are stated in Section 5 rather than inferred |
| Green identity and Hilbert-space energy method | transport graph space with traces, positive density, declared inflow/albedo boundary | boundary flux and energy inequality | external analytic tool used to prove the stability kernel independently of variation of constants | a raw inflow discrepancy is lifted or retained in a boundary norm; point sampling and nonconforming face terms require their own bounded reconstruction/dual norms |

Bibliographic correction: publisher/Crossref metadata for the 2007 article give
pages **154--163**, not 154--167.  The DOI is `10.13182/NSE07-A2693`.

## 2. Novelty boundary

P2B does not claim the first Fokker--Planck discretization, the first positive
angular stencil, the first moment-preserving $S_N$ operator, the first BFP
transport calculation, or the first adjoint transport calculation.  Nor does
P2B claim priority for Duhamel/resolvent residual bounds, Hilbert
energy estimates, or dual-weighted residual estimators as general methods.
Its retained contribution is their exact, normalization-audited synthesis
with the accepted sampled-shell quotient, full-output alias handling, and the
six named BFP error channels.  The combined contribution is narrower:

1. the accepted alias-correct sampled harmonic residual is converted into a
   sharp, full-output transient and resolvent bound without assuming shell
   invariance;
2. the conversion is embedded in a common-space, six-way BFP residual identity
   with all stability and boundary constants exposed;
3. streaming--diffusion noncommutation is handled by two independent routes;
4. steady, preconditioned, multigroup, and adjoint-response bounds use the same
   auditable residual ledger; and
5. exact effectivity fixtures distinguish a worst-case shell norm from the
   source- and adjoint-aligned error actually observed.

## 3. Adversarial theorem audit

| Referee attack | Deterministic resolution |
|---|---|
| sampled shell is not invariant under $L$ | Duhamel acts in the full sample space; $T_\ell$ retains leakage |
| continuum harmonic is mean zero, so use a discrete spectral gap | false without quadrature exactness; the two-node quadratic fixture has constant contamination |
| combine shell errors by orthogonality | false under cross-shell aliases; use the exact block Gram or a declared global sampling angle |
| use a direction-dependent physical metric and keep contraction one | false unless its Euclidean Hermitian matrix satisfies $ML+L^*M\le0$; exact two-state mutation rejects it |
| forward peaking makes the BFP model exact | rejected by Pomraning's hypothesis boundary; $R_1$ remains separate |
| write “standard Duhamel” for streaming plus diffusion | rejected; Sections 5--7 supply domains, traces, range/accretivity, stability kernel, and a second energy proof |
| commute streaming and angular diffusion | exact continuum commutator and finite manufactured commutator are nonzero |
| contraction implies a steady inverse | false when constants survive; require onto plus positive coercivity (or a surjective coercive-form theorem), or onto plus a declared inf-sup condition |
| infer a nonnormal preconditioner bound from eigenvalues | rejected; require an induced-norm contraction or a certified lower singular/inf-sup constant |
| point detector is an $L^2$ response | false; require a $V$--$V'$ regularity theorem |
| omit time discretization from the six terms | temporal reconstruction belongs explicitly to $R_6$ |
| move a boundary residual into a volume norm | rejected; use a stable lift or the trace term in the squared energy estimate |
| triangular downscatter gives transient contraction | false; it gives a finite steady inverse expansion that may have a large norm |
| sum of norm contributions should have effectivity near one | cancellations can be large; signed adjoint contributions are reported separately |
| numerical quadrature of a residual proves an upper bound | only exact/algebraic or genuinely outward-enclosed integration is certified; ordinary floating output is diagnostic |
| copy the 2025 printed factor $-4$ | exact coordinate tests enforce the accepted $-2$ convention |
| Gate-6 weights and Paper-I weights are interchangeable in absolute responses | $\sum w=4\pi$ versus $1$ rescales absolute norms/responses; every artifact declares its convention |

## 4. Numerical and formal audit boundary

The exact angular fixtures use rational matrices and powers of two at
$t=\log2$ where possible.  The spatial manufactured problem uses an exact
rational solve, exact squared norms, and an exact discrete adjoint.  Floating
matrix exponentials are cross-checks only.  The formal finite core checks
resolvent algebra, finite residual telescoping, transpose/adjoint identities,
energy scalar inequalities, and geometric iteration estimates.  It does not
claim to formalize PDE generation, trace theory, Bochner integration, or
matrix exponentials.

## 5. Rejected overclaims

- A small $\mathfrak D_2$ does not by itself prove a small dose, detector, or
  deposition error.
- A response improvement on a manufactured system is not an equal-cost
  production-transport comparison.
- No nuclear-data, material-interface, stopping-power, or nonlinear feedback
  uncertainty is absorbed into the angular defect.
- No cited discretization theorem is silently upgraded from its quadrature,
  geometry, regularity, or boundary hypotheses.

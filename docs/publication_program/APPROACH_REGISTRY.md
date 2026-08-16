# Publication approach registry

This registry groups mechanisms, not wording.  `BLOCKED` means that a
theorem-strength missing lemma remains; reopening requires the concrete new
mechanism named below.

| Family / mechanism | Target | Status | Concrete output | Exact blocker or adversarial test | Reopen condition | Paper |
|---|---|---|---|---|---|---|
| immutable corrected archive selection | P0 | ACCEPTED | `6bac46ce…` selected by tree, ancestry, archive and theorem-content audit | survived comparison with all live candidates | immutable mismatch only | all |
| later administrative target | P0 | REJECTED_BASELINE_CANDIDATE | `c8505a70…`, PR #34 and six green runs preserved | missing d=1 spectral correction; superseded opposite-ray claim | additive reconciliation in a later authorized task | none |
| finite convex geometry | local positive feasibility/lifts | PROVED_LOCAL | tangent-hull and balanced-probability criteria | shared-edge reversibility is independent | new global compatibility invariant | I/III |
| Farkas/Gale duality | certificates and supports | ACTIVE | exact local/global dual certificates | cannot silently transfer regular-graph Gale statements | source-hypothesis-preserving global certificate | I/III |
| covariance algebra | sampled H2 fidelity | PROVED_P1B_SHARP_BOUND | P1A factorization plus the exact two-defect trace lower bound | sampling-kernel, mixed-Gram and equality audits | matching positive asymptotic construction | I |
| generalized eigenvalues | `mathfrak D_l` | PROVED_P1B_SHARP_BOUND | sampling-metric quotient, deflated pencil, sharp trace ratio and complete equality conditions for `mathfrak D_2` | raw singular pencil and non-invariant sampled range rejected | higher-degree or construction-specific frontier analysis | I/II |
| quotient Hilbert--Schmidt / random averaging | P1B universal lower bound | PROVED | independent quotient-map, isotropic-random-matrix and finite-frame proofs of the same sharp trace inequality | semigroup restriction rejected when `im S_2` is non-invariant | none for P1B | I |
| semigroup/resolvent | response error | PROVED_P2B | sharp full-output Duhamel multiplier and resolvent identity, with shell/band/physical-norm extensions | harmonic residual alone still does not control the other five transport residual channels | none for the scoped angular theorem | II |
| representation theory | equality/families | ACTIVE | symmetry reductions for exact examples | multiplicities and sampled kernels | family theorem, not dimension count | I/III |
| spherical designs | lift implication | ACTIVE | design moment identities | design does not imply positive local reversible lift | non-generic lift characterization | III |
| association schemes | exact families | ACTIVE | candidate simultaneous eigenspace calculations | locality/positivity may fail | infinite positive family with exact spectrum | I/III |
| frame theory | covariance/equality | PROVED_P1B_SHARP_BOUND | weighted row frames, exact trace split and `D_2^2 tr G_S>=tr G_R` with equality characterization | algebraic nonzero does not imply sampled nonzero; trace saturation need not imply scalar residual | matching-family stability | I |
| rigidity/propagation | equality and stability | PROVED_SCOPED | ten-hypothesis classification and quantitative propagation | deleted-hypothesis catalogue | only stronger hypotheses with audited necessity | I |
| exact symbolic computation | regressions | COMPUTATIONAL | algebraic Platonic table, 19 P1A fixtures and 24 P1B bound/equality/degeneracy fixtures | finite verification never replaces all-orders theorem | exact certificate for a theorem step | all |
| Plantri enumeration | adversarial census | COMPUTATIONAL | 9150 maps through 12 vertices | finite census is not classification | larger census only as regression, not proof | I |
| conic/SDP duality | fixed-quadrature optimizer | PROVED_P2A | exact SDP/SOCP/QP/LP primal-dual families on the sampled quotient | boundary Slater, factor-two cross block and output-leakage audits | none for fixed linear objectives | II/III |
| asymptotic construction | match frontier | PROVED_D2_D3 | regular polygons on `S^1` and a no-guard adaptive-ring family on `S^2`, with all-orders constants | no corresponding construction in `d>3`; only the fixed-support, fixed-level perturbation theorem is covered | a genuinely new higher-dimensional compiler with global shared-edge margins | I |
| Delsarte machinery | equality/optimality | BLOCKED | comparison framework only | no transferred certificate for AFP constraints | exact source theorem with every hypothesis checked | I/III |
| Bakry–Émery route | general P4 barrier | REJECTED | retained negative decision | route did not close the required sharp product theorem | genuinely different curvature mechanism | none |
| discrete Delaunay geometry | local construction | BLOCKED | relevant external special operator | fixed connectivity/AFP weights not covered | proved conversion preserving weights and sign | II/III |
| transport-error decomposition | response relevance | PROVED_P2B_SCOPED | exact common-space physical/angular/sampling/spatial/energy/iteration residual ledger, two noncommuting stability proofs, steady/multigroup/adjoint bounds | physical-model residual and all stability constants remain explicit inputs; no equal-cost production benchmark claim | none for the error-certificate theorem | II |
| Lean architecture | finite algebra kernel | ACTIVE_P1B | P1A quotient/Gram core plus P1B weighted trace domination and scalar sharp-bound algebra | exact-head build and axiom audit still control acceptance | formalize only stable algebraic interfaces | I/III |
| compact-space generalization | beyond sphere | DEFERRED | no claim | outside current paper boundary | Paper I completed first | future |

## P2A fixed-quadrature convex-design mechanisms

P2A is an additive descendant of the accepted Paper-I/P1F archive commit
`ab155b8e04bdf00306351b581739fb5feeb2979e`, tree
`61a07c6c187d3002d5ca433be16b26fb1bad73f1`.

| Family / mechanism | Target | Status | Concrete output | Exact blocker or adversarial test | Reopen condition | Paper |
|---|---|---|---|---|---|---|
| shared-edge affine cone | exact `H_0,H_1` and reversibility | PROVED_P2A | `A gamma=b`, `gamma>=0`, rate inequalities | unequal-mass four-cycle is locally strict but globally Farkas-infeasible | none for the finite characterization | II |
| sampled shell whitening | alias-correct residual | PROVED_P2A | `T_l=W^(1/2)(L+lambda_l I)V_l` with full output leakage | octahedral rank two; ambiguous numerical rank rejected | exact/certified rank input | I/II |
| spectral epigraph | minimum `D_2` or rate | PROVED_P2A | exact primal and dual SDPs | missing dual cross-block factor two mutation | none | II |
| Hilbert--Schmidt and selected modes | QP/SOCP alternatives | PROVED_P2A | invariant quotient Frobenius and finite-mode objectives | raw coefficient norm and sampled-zero mode mutations | none | II |
| multi-shell/fixed response | broader objectives | PROVED_P2A_SCOPED | shellwise QP/SDP/SOCP/LP assembly | nonlinear resolvent and continuum rotation not covered | separate response theorem | II |
| conductance penalty analysis | support control | PROVED_P2A | loss-weighted `l1` fixed; total conductance is mean-rate control | exact antipodal long-edge preference witness | none for diagnosis | II/III |
| pruning with reoptimization | sparse returned support | IMPLEMENTED_P2A_SCOPED | deterministic delete/re-solve/certify loop | outer support choice is combinatorial | exhaustive/MIP proof for cardinality | II/III |
| conic/Farkas certificate verification | solver independence | PROVED_P2A | exact rays, primal-dual feasibility and gap brackets | solver status alone explicitly rejected | rational or outward interval certificate | II |
| exact/ill-conditioned fixtures | adversarial regression | COMPUTATIONAL_P2A | tetra/octa equality, full-rank ill-conditioning, local/global failure | finite solver runs do not prove convex duality | retained exact proof source | all |
| Lean finite core | stable algebra | IMPLEMENTATION_P2A | conductance, mixture and fixed-loss identities | no formal generic SDP strong-duality theorem | exact-head build | II |

## P2B harmonic-defect transport mechanisms

P2B is an additive descendant of the accepted P2A archive
`07138547ff5c85df071e2067587dd83ca20b71b5`.  Its detailed portfolio and
rejections are in `P2B_APPROACH_REGISTRY.md`.

| Mechanism | Purpose | Status | Retained conclusion | Counterexample / transfer guard | Remaining condition | Consumer |
|---|---|---|---|---|---|---|
| spectral Duhamel multiplier | one-mode transient error | PROVED_P2B | exact $k_{t,\lambda}(-L)$ identity and sharp conservative-space constant | fixed-shell gap improvement needs a verified mean-zero/reducing subspace | none | II |
| resolvent residual identity | steady angular response | PROVED_P2B | exact identity and sharp $1/[\alpha(\alpha+\lambda)]$ bound | $\alpha=0$ fails on constants | positive shift or gap compatibility | II |
| shell/band synthesis | sampled harmonic extension | PROVED_P2B | alias-correct full-output shell theorem and exact cross-shell block Gram | two-equator alias rejects an initial-sample-only band claim | kernel invariance or global sampling angle for total-sample norm | I/II |
| common-space residual ledger | transport separation | PROVED_P2B | exact six-way residual closure through $PJ=I$ | raw point sampling and relabeled aliases rejected | bounded conforming reconstruction and declared residual norms | II |
| evolution-family route | noncommuting transient stability | PROVED_P2B | explicit variation-of-constants/intertwining estimates | no streaming--diffusion factorization | a well-posed evolution family under the stated common-form/Kato generation hypotheses | II |
| energy route | independent transport stability | PROVED_P2B | Green identity, boundary flux, collision coercivity and stability kernel | variable density and amplifying albedo mutations | displayed boundary/coercivity assumptions | II |
| steady/preconditioned route | residual-to-solution bound | PROVED_P2B_SCOPED | coercive/inf-sup resolvents, Neumann and lower-singular estimates | contraction without absorption and spectral-radius-only claims rejected | onto coercivity/inf-sup or induced-norm contraction | II |
| multigroup block route | group/slowing-down extension | PROVED_P2B | weighted block coercivity and finite triangular downscatter inverse | triangularity need not control transient growth | positive block certificate or explicit finite inverse | II |
| adjoint residual route | response estimation | PROVED_P2B | exact steady/transient identities and enriched-adjoint remainder | point detector is not an $L^2$ response | bounded response or separate dual-space theorem | II |
| exact manufactured fixtures | effectivity/falsification | COMPUTATIONAL_EXACT_P2B | angular sharpness, noncommuting spatial solve, six-ledger closure and adjoint effectivity | finite fixtures do not prove PDE well-posedness | retained theorem source | II |
| Lean finite core | algebraic audit | IMPLEMENTATION_P2B | finite resolvent, residual telescope, transpose, energy and iteration identities | no formal PDE/Bochner/trace theorem is claimed | exact-head build and axiom audit | II |

Adversarial controls applied to every future route: sign and weight
normalization, sampled-kernel aliasing, eigenvalue multiplicity, degenerate
supports, conditioning, external-theorem hypotheses, exact arithmetic, and
the distinction between computational evidence and proof.

## P1C equality-geometry mechanisms

P1C is an additive descendant of frozen P1B commit
`58b4fd93ea2bc95c4f1aee909a298e3a64a4d4fd`, tree
`4b715d6999a3b69baf9c08062cc5ea01f60a5498`.

| Family / mechanism | Target | Status | Concrete output | Exact blocker or adversarial test | Reopen condition | Paper |
|---|---|---|---|---|---|---|
| local radial/tangent block algebra | P1C equality geometry | PROVED_P1C | exact increment split, mixed-covariance/tangent-isotropy norm square, weighted-tight-frame equivalence | antipodal `ell=2` has zero tangent length and cannot be normalized | none for the division-free theorem | I |
| global Markov/Gram assembly | connected equality generators | PROVED_P1C_SCOPED | common-angle reversible kernel, two conditional moments, Gram completion and cycle/detailed-balance criterion | independent local tight frames do not solve shared-edge compatibility | none for the algebraic criterion | I/III |
| equality-family algebra | all-dimensional and Platonic sharpness | PROVED_P1C | simplex, cross-polytope, hypercube and five exact Platonic families with kernels and aliases | finite dimension checks cannot replace family proofs | none | I |
| global equality classification | geometry | PROVED_RESTRICTED | degree-`d`, complete-support and strict-convex `S^2` polyhedral classifications under explicit hypotheses | covers, blowups, long-chord shells and weighted frames reject an unrestricted Platonic claim | stronger explicit graph/embedding hypotheses only | I/III |
| exact symbolic P1C audit | regression | COMPUTATIONAL_CANDIDATE | rational/algebraic block, family, minor, alias and counterfamily fixtures | no numerical rank thresholds; computation is not the all-orders proof | exact-head execution | all |
| Lean equality geometry | finite algebra kernel | IMPLEMENTATION_P1C | `QuadraticEqualityGeometry.lean` over accepted P1B/P3 algebra | compilation and axiom audit remain acceptance gates | exact-head build | I |

## P1D quantitative-stability mechanisms

P1D is an additive descendant of frozen P1C commit
`9ae0c8f16e8cd97cd84ef89b25064512a04b308a`, tree
`289113bb760fbe079f5d581c10f1cefea8a72931`.

| Family / mechanism | Target | Status | Concrete output | Exact blocker or adversarial test | Reopen condition | Paper |
|---|---|---|---|---|---|---|
| normalized frontier budget | P1D stability | PROVED_P1D | exact `sum w(2q+q^2)+(d-1)E_B/(d a_0^2)<=2delta+delta^2` | every later conclusion must preserve its weighting and normalization | none | I |
| weighted exceptional sets | vertex stability | PROVED_P1D | exact `H/[rho(2+rho)]` mass bound and `sqrt(1+H/w_i)-1` pointwise envelope | tiny stationary masses reject unweighted control | add an explicit mass floor | I |
| reversible conductance measure | edge stability | PROVED_P1D | global-shell loss identity and active-conductance fraction bounds | an edge carrying probability `kappa` may retain order-one defect | add an explicit probability floor for edgewise claims | I/II |
| graph propagation | global rate stability | PROVED_P1D_SCOPED | multiplicative path, additive energy, effective-resistance and Poincare-gap bounds | long paths and vanishing gaps reject parameter-free propagation | diameter, resistance, gap or congestion must be displayed | I/II |
| local polar whitening | tangent geometry | PROVED_P1D_SCOPED | explicit Procrustes repair to a centered weighted tight frame | nearly singular tangent covariance and antipodal shells | retain tangent lower bound and shell margin | I/III |
| positive unit-frame repair | local spherical figure | PROVED_P1D_SCOPED | feature-operator pseudoinverse corrects weights while retaining unit directions and positivity | feature overlap, active degree, `kappa`, and shell floor are necessary | none under stated margins | I/III |
| quotient residual transfer | sampled shell | PROVED_P1D | Hilbert--Schmidt row control and `alpha_X^{-1/2}` quotient operator bound including leakage | sampling aliases and nearly singular sample frames | quotient `K_X`; expose `alpha_X` | I/II |
| exact/interval P1D audit | regression | COMPUTATIONAL_CANDIDATE | 30 symbolic and outward-rounded stress fixtures | no floating rank thresholds; finite checks are not theorem proofs | exact-head execution | all |
| Lean stability core | finite scalar algebra | IMPLEMENTATION_P1D | `QuadraticFidelityStability.lean` over accepted P1B/P1C interfaces | inverse-square-root and graph spectral calculus remain in the ordinary proof | exact-head full build | I |

## P1E matching-construction mechanisms

P1E is an additive descendant of the frozen P1D source. Its ordinary theorem
is accepted; the dedicated exact-head workflow and archive freeze have not yet
run and therefore have no recorded run or artifact status.

| Family / mechanism | Target | Status | Concrete output | Exact blocker or adversarial test | Reopen condition | Paper |
|---|---|---|---|---|---|---|
| regular polygon | matching family in `d=2` | PROVED_P1E | for fill `h=pi/N`, exact `mathfrak D_2=2(1-cos(2h))`, `r=(1-cos(2h))^-1`, product `2` | irregular gaps need different shared rates and can have first-order defect | none for the regular family | I |
| no-guard adaptive rings | matching family in `d=3` | PROVED_P1E | exact `H_0,H_1`, positive shared conductances, `B_i=0`, `R_3=64pi^2`, `C_3=75/2` | pre-repair equal-gap/cap formulas retained as failed mutations | none under the stated schedule | I |
| rational Cauchy compiler | all-orders transition and first-row margins | PROVED_P1E | literal symbolic limit plus uniform rational disk bounds | isotropy RHS has no removable quotient; direct overbound used instead | none | I |
| structured latitude perturbation | robustness | PROVED_FIXED_LEVEL | finite block-lower-triangular moment system, base nonsingularity and positivity, computable level-dependent radius, exact shared-edge repair | no inverse, positivity or radius bound uniform in refinement level; arbitrary support/longitude motion excluded | a uniform theorem requires an independently verified all-level expression and recurrence certificate | I/III |
| finite generator | regression | COMPUTATIONAL_CANDIDATE | deterministic nodes/conductances/masses and hostile mutations | finite levels and fitted slopes never establish all-orders behavior | exact-head execution for reproducibility only | all |
| six independent alternative routes | search boundary | REJECTED_AS_STANDALONE_ROUTES | exact Voronoi, cone, reconciliation, symmetry, covariance-floor and product obstructions | each rejection is scoped to its proposed mechanism | materially new compiler, invariant or uniform inverse | I/III |
| Lean construction core | finite algebra | IMPLEMENTATION_P1E | shared-stress, exact-force, moment, rate and polygon identities | analytic ring/Cauchy proof remains in ordinary mathematics | exact-head full build | I |

# Independent theorem-by-theorem audit of the corrected flagship

## Audit object and method

This audit covers the 16 numbered results in
`p1f_manuscript/FLAGSHIP_MANUSCRIPT.md` after the Proposition 7.3 repair. The
starting repository object is the live head of pull request 51 resolved on
2026-08-10:

| Record | Exact value |
|---|---|
| authoritative parent commit | `b8912c282a22420e8077c75929b16c7a33d189b2` |
| authoritative parent tree | `4c2175463a661ce3f2bb206f0cb7b5038183b2ab` |
| repair branch | `agent/afp-prop73-publication-safe-20260810` |
| corrected perturbation proof | `P1E_FIXED_LEVEL_LOCAL_PERSISTENCE.md` |
| rejected former claim | `P1E_REJECTED_UNIFORM_ROBUSTNESS_CLAIM.md` |

The audit is source-first. A theorem is not accepted because a stage report,
registry, archive name, test, or workflow calls it accepted. For each result,
the ordinary proof was matched to the hypotheses and conclusion printed in
the manuscript. Lean and computational columns state only their actual scope.
A regression is never listed as a proof dependency.

## Result ledger

| Result | Exact hypotheses | Conclusion | Ordinary-proof dependencies | Ordinary-proof status | Lean status | Computational dependency | Final classification |
|---|---|---|---|---|---|---|---|
| Proposition 2.1 | Finite indexed sample `X=(Omega_i)` on `S^(d-1)`; positive normalized masses; reversible nonnegative jump generator; sampled map `S_2` on `Sym_0(d)`; residual `R_2=(L+2dI)S_2`; quotient kernel `K_X=ker S_2`. | `K_X subset ker R_2`; `R_2` descends to the sampled quotient; its norm is `mathfrak D_2`; the finite generalized Gram pencil gives the same norm; the three displayed dimension formulas distinguish aliases from genuinely sampled exact modes. | Definitions of `S_2`, `R_2`, weighted adjoints, and finite-dimensional quotient linear algebra. | Complete ordinary proof in P1A; no image-invariance or injectivity assumption is used. | Finite algebra has a Lean surface, but the full quotient/Gram-pencil statement is not claimed as a complete formalization. | None; `p1a_quadratic_fidelity_audit.py` is regression evidence only. | accepted |
| Theorem 3.1 | Proposition 2.1 standing data plus exact coordinate reproduction `L Omega=-(d-1)Omega`; row losses, rates, covariance tensor `M_i`, axial tensor `Z_i`, anisotropy `B_i`, scalar defect `epsilon_i`, and loss variance `V_i` as defined. | Exact row residual representation; orthogonal scalar/anisotropic decomposition; norm identity; and `epsilon_i=(d-1)^2/r_i+V_i`. | Coordinate force identity, chord expansion, orthogonal projection onto `Z_i`, and the weighted mean-variance identity. | Complete ordinary algebraic proof in P1A. | Finite tensor identities are partially formalized; the manuscript theorem as a whole is not declared machine checked. | None; P1A exact checks guard signs and normalizations. | accepted |
| Proposition 3.2 | Theorem 3.1 data; Frobenius metric on coefficients and weighted `ell^2(w)` metric on samples. | Exact formulas for `S_2^*`, `R_2^*`, `tr G_S=(d-1)/d`, and `tr G_R=d E_epsilon/(d-1)+E_B`. | Weighted duality, unit-sphere identity for `Z_i`, and Theorem 3.1. | Complete ordinary finite-dimensional proof in P1A. | Partial finite-sum formalization only; no claim that the full weighted Gram statement is in Lean. | None; P1A audit is a regression. | accepted |
| Theorem 4.1 | `d>=2`; finite spherical sample; positive masses; nonnegative reversible generator; exact constants and coordinates; alias-correct sampled quotient; finite `r_max`. | Sharp trace lower bound, `mathfrak D_2 >= d(d-1)/r_max`, product frontier `mathfrak D_2 r_max>=d(d-1)`, and attainability in every dimension. | Proposition 3.2 trace identities; positive Gram comparison on `K_X^perp`; Theorem 3.1 variance decomposition; exact simplex extremizer. | Complete ordinary proof in P1B; the trace comparison retains aliases and output leakage. | A finite scalar/tensor core is formalized; the complete sampled spectral theorem is not represented as fully formal. | None; P1B exact audit checks algebra and extremizers. | accepted |
| Theorem 5.1 | All hypotheses of Theorem 4.1 and equality in its product bound. | Equality iff every positive-mass row has common maximum rate, zero active-loss variance, and zero anisotropy; equivalently `M_i=c_*Z_i` and `R_2=c_*S_2`; then `ker R_2=ker S_2` and there is no genuinely sampled exact degree-two mode. | Equality conditions in every nonnegative step of Theorem 4.1 and the P1C geometric translation. | Complete ordinary equality proof; positivity of every `w_i` is used to pass from weighted equality to every row. | Equality algebra has a finite Lean surface; the full iff including sampled kernels is not claimed fully formalized. | None; P1B/P1C audits test both directions and alias examples. | accepted |
| Theorem 5.2 | A row of a coordinate-exact generator; tangent decomposition. For the tight-frame equivalence, additionally `V_i=0` and common loss in the nonantipodal range `0<ell_bar_i<2`. | Division-free block identity and norm splitting for `B_i`; in the nonantipodal common-loss branch, `B_i=0` iff normalized tangent directions are a centered weighted unit-norm tight frame. | Exact radial-tangent expansion and Theorem 3.1 definitions; no global reversibility conclusion is inferred from the local frame. | Complete ordinary local proof in P1C, with the antipodal case kept outside the normalization. | Selected finite frame identities are formalized; the geometric theorem is not wholly machine checked. | None; P1C regressions include antipodal and nonregular-frame cases. | accepted |
| Theorem 5.3 | Nonantipodal equality branch; one common loss/rate; Markov rows and detailed balance. For the cycle criterion, connected bidirected support and positive directed rates. | Equivalent global system of row stochasticity, detailed balance, common Gram value, first and second conditional moments; equivalent positive-semidefinite Gram formulation; on connected support, reversible masses iff every oriented cycle satisfies Kolmogorov compatibility. | Theorems 5.1-5.2 plus finite Gram realization and standard detailed-balance cycle algebra proved in the P1C source. | Complete ordinary global-assembly proof; explicitly does not promote rowwise feasibility to global reversibility. | Finite detailed-balance identities are formalized in part; the full Gram-realization theorem is ordinary mathematics. | None; cycle-breaking mutations are regression evidence. | accepted |
| Proposition 5.4 | Frontier equality; common loss `ell_*=2`; connected active graph. | All nodes lie at two antipodal locations, every active edge crosses the antipodes, `r_*=(d-1)/2`, and `R_2=2dS_2`; conversely any reversible connected constant-rate generator of this form is an equality generator. | Division-free branch of Theorem 5.2, connectedness, and Theorem 5.1. | Complete ordinary proof in P1C. | Finite antipodal algebra only; no complete graph-classification formalization claimed. | None; exact antipodal examples are regressions. | accepted |
| Corollary 5.5 | First part: a nonantipodal equality row. Exact-degree part: exactly `d` active neighbors. Complete-support part: distinct nodes and nonantipodal complete support. Three-dimensional classification part: distinct vertices of a strictly convex inscribed polyhedron, support equal to its one-skeleton, common directed rate, and common degree `3<=q<=5`. | Minimum degree `d`; degree-`d` rows are regular simplices with equal weights; complete support gives the ambient regular simplex; under the additional `d=3` hypotheses only the five Platonic combinatorial/geometric cases occur. | Theorem 5.2 tight-frame consequences and the separately scoped Euler/convex-polyhedron argument. | Complete ordinary proof under every printed hypothesis; no unrestricted Platonic classification survives. | No complete classification formalization claimed. | None; counterexamples test omission of convexity, common rate, or graph hypotheses. | accepted under stated hypotheses |
| Corollary 5.6 | Connected nonantipodal equality generator with positive reversible masses. | Stationary node measure has zero first moment and isotropic second moment `I/d`, hence is a weighted spherical 2-design. | Sum the conditional first/second moment equations of Theorem 5.3 against the stationary measure and use connected nonantipodal parameters. | Complete ordinary consequence; design exactness is not assumed and is not equated with operator fidelity. | Finite moment summations have partial formal support; full corollary not claimed fully formalized. | None. | accepted |
| Theorem 6.1 | Theorem 4.1 class and near-frontier hypothesis `mathfrak D_2 r_max <= d(d-1)(1+delta)`, `delta>=0`; normalized nonnegative defects exactly as defined in (6.2). | Master weighted budget (6.3) and its rate, scalar, variance, and anisotropy consequences (6.4)-(6.7), without connectedness, a mass floor, or sampling injectivity. | Theorem 4.1 trace inequality, exact decomposition, and elementary nonnegative algebra. | Complete ordinary quantitative proof in P1D; normalization and weights are retained exactly. | `QuadraticFidelityStability.lean` checks the finite scalar core; graph/spectral/geometric transfers remain ordinary proofs. | None; P1D exact/interval fixtures are regressions. | accepted |
| Corollary 6.2 | Theorem 6.1 and a chosen threshold `rho>0`; pointwise statement at a vertex with its actual positive mass `w_i`. | Exceptional stationary-mass bound and pointwise envelope `q_i<=sqrt(1+H/w_i)-1`; any uniform pointwise conclusion therefore requires a lower mass bound. | Positivity and Markov/Chebyshev-type extraction from the master budget. | Complete ordinary proof in P1D. | Finite scalar inequality is within the formal core; no parameter-free rigidity theorem is formalized or claimed. | None; small-mass mutations demonstrate necessity. | accepted |
| Corollary 6.3 | Theorem 6.1 plus the separate hypothesis attached to each transfer: active probability floor for edgewise bounds; mass and connectivity/path/resistance/gap/congestion parameters for graphwise bounds; spectral gap for eigenvectors; sampling-frame lower bound `alpha_X` for quotient scalarity; tangent and feature-surjectivity/nonantipodal/positivity margins for frame repair. | The individually stated edge, graph, covariance, quotient-with-leakage, and tangent-frame transfer estimates; no parameter-free composite conclusion. | Master budget plus the corresponding P1D lemma for each named margin. | Complete ordinary scoped proofs in P1D. A consumer must cite the relevant substatement and all its margins. | Only finite scalar pieces are formalized; inverse-square-root, graph spectral, sampling, and repair calculus remain ordinary. | None; stress fixtures reject omitted margins. | accepted only with the named margin for the selected transfer |
| Theorem 7.1 | `d=2`; regular `N`-gon with `N>=5`; `h=pi/N`; nearest-neighbor support; equal rate `[2(1-cos(2h))]^-1`; uniform masses. | Exact constants/coordinates, reversibility, `r_max=(1-cos(2h))^-1`, `mathfrak D_2=2(1-cos(2h))=4sin^2 h`, exact product 2, and the displayed matching-order bounds with `R_2=pi^2/8`. | Direct Fourier/trigonometric calculation and Theorem 4.1 for the lower half. | Complete all-`N` ordinary proof; no irregular-circle extension. | Polygon recurrence and residual identities are machine checked in `QuadraticFidelityConstruction.lean`. | None; polygon script independently checks exact identities. | accepted for the stated regular family |
| Theorem 7.2 | `d=3`; the exact unperturbed reflected adaptive-ring schedule, counts, phases, masks, jumps, local systems, Cauchy guards, and shared-conductance recurrence in equations (7.4)-(7.14); no node perturbation. | Positive weights and one shared conductance per edge; locality, mesh, separation, window, and degree bounds; exact `H_0` and `H_1`; rowwise `B_i=0` and scalar sampled residual; `r_max<=64pi^2 h^-2`, `mathfrak D_2<=75h^2/2`, and matching-order sandwich (7.18). | P1E Sections 1-9: literal row systems, rational Cauchy/first-row guards, ordinary-row brackets, exact global recurrence, normalization, quotient descent; Theorem 4.1 supplies only the lower half of (7.18). | The unperturbed all-level proof remains accepted after removing the perturbation claim; no step of (7.15)-(7.18) depends on the former Proposition 7.3. | Lean certifies only finite stress-to-generator, moment, rate, and polygon identities; it does not formalize the schedule, analytic guards, recurrence, or all-level geometry. | The symbolic, Cauchy, polar, family, proof, referee, and hostile scripts are falsification/regression surfaces, not proof substitutes. | accepted for the unperturbed `d=3` family |
| Proposition 7.3 | One fixed level `J`; finitely many unperturbed local systems all nonsingular; finitely many unperturbed shared conductances all strictly positive; pole/equator, counts, phases, masks, jumps, support, and reflection fixed; sufficiently small reflected latitude displacement; optional common rotation. | There exists an existential level-dependent `delta_J>0` such that displacements smaller than `delta_J` retain unique solvability, positive shared conductances, positive masses, reversibility, and exact `H_0 direct-sum H_1` fidelity. No uniform radius, mesh-power law, or perturbed rate/defect constants are concluded. | `P1E_FIXED_LEVEL_LOCAL_PERSISTENCE.md`: finite guarded parameter domain; determinant and inverse continuity; finite recursive solution continuity; strict positivity margin; exact stress-to-generator normalization. | Complete fixed-level continuity proof. The former universal proposition and its constants are rejected and isolated in the historical record. | Not formalized. Lean supplies only the final finite algebra once a positive shared stress exists; it proves neither continuity nor existence of `delta_J`. | None for proof; the independent contract verifier checks quantifiers and mutations only. | accepted after exact weakening |

## Dependency and downstream audit

The corrected dependency chain is

```text
Proposition 2.1
  -> Theorem 3.1 and Proposition 3.2
  -> Theorem 4.1
  -> Theorems 5.1-5.3, Proposition 5.4, Corollaries 5.5-5.6
  -> Theorem 6.1 -> Corollaries 6.2-6.3

Theorem 7.1 -> its d=2 upper bound; Theorem 4.1 -> its lower bound
P1E Sections 1-9 -> Theorem 7.2 upper bound; Theorem 4.1 -> (7.18) lower bound
fixed level of Theorem 7.2 + finite continuity -> Proposition 7.3
```

No frontier, equality, stability, polygon, or unperturbed adaptive-ring result
uses Proposition 7.3. The stronger perturbation statement had no mathematical
downstream corollary; its downstream effects were advertising, source maps,
stage reports, registries, and release checks. Those surfaces are included in
the publication-safety scan.

## Independent blocker disposition

The former universal derivative argument is rejected because the repository
contained no literal expression graph, generated operation count, complete
denominator ledger, intermediate interval certificate, conductance-margin
propagation, or independent certificate consumer. The scalar exponent
recurrence in the old audit script did not establish any of those premises.
The exact fixed-level theorem requires none of them and makes every source of
level dependence explicit.

## Final classification

After the weakening and repository-wide propagation, all 16 numbered results
have an ordinary proof matching their final statement. The first 15 retain
their prior mathematical scope; Proposition 7.3 is accepted only in the
fixed-level existential form. The all-level unperturbed `d=3` construction is
preserved. No accepted result states a perturbation radius uniform in `J`, a
prescribed perturbation power in `h`, or perturbed all-level rate or defect
constants.

# R7 Lean claim and signature audit

## Exact release result

- Lean toolchain: `leanprover/lean4:v4.30.0`.
- Mathlib revision: `c5ea00351c28e24afc9f0f84379aa41082b1188f`.
- Non-audit AFP modules: 58.
- Public project theorem/lemma declarations: 512.
- Signatures inspected with `#check`: 512/512.
- Axiom dependencies inspected with `#print axioms`: 512/512.
- Project-local `sorry`, `admit`, `sorryAx`, or declared axiom used: none.
- Foundational dependencies printed by Lean are the expected `propext`,
  `Classical.choice`, and `Quot.sound`; two finite incidence theorems print no
  axiom dependency.

The historical six audit files covered 430/512 declarations in aggregate;
`AxiomAudit.lean` alone covered 189 while claiming completeness. R7 preserves
it as a legacy focused audit and adds the generated exhaustive
`AFPBarrier/ReleaseAxiomAudit.lean`. Generation stops if the reviewed count
changes from 512.

## Formalization boundary

| Claim family | Lean classification | Exact boundary |
|---|---|---|
| covariance, sampled quotient, trace and two-defect algebra | `FULLY_CHECKED_FINITE_ALGEBRA` | arbitrary finite types/matrices under explicit signatures; does not identify external spherical harmonics |
| sharp product lower-bound algebra | `FULLY_CHECKED_FINITE_ALGEBRA` | finite trace/rate implications; manuscript assembles definitions and sharpness family |
| equality and stability budgets | `FULLY_CHECKED_FINITE_ALGEBRA` | local scalar/tensor identities and weighted consequences; not unrestricted global embedding classification |
| construction identities | `EXPLICIT_EXTERNAL_HYPOTHESES` | shared conductance, force/moment, rate conversion, connectors, and polygon recurrences after inputs are supplied |
| adaptive-ring `d=3` schedule | `COMPUTER_ASSISTED_NOT_LEAN_CHECKED` | ordinary analytic reduction plus independently verified exact-rational certificate; no complete schedule Lean declaration |
| convex design | `FULLY_CHECKED_FINITE_ALGEBRA` | affine mixing, loss/rate, and certificate soundness; full conic strong duality/facial reduction is external finite mathematics |
| transport error algebra | `FULLY_CHECKED_FINITE_ALGEBRA` | finite Duhamel/resolvent/telescope/adjoint/energy identities; PDE generation, trace theory, and Bochner integration are not formalized |
| P2E/P2F | `NUMERICAL_EVIDENCE` | no physical or performance conclusion is Lean-checked |

## Signature-specific guards

- `finite_spherical_qOne_global_rigidity` proves common positive rate and
  common active loss under its explicit finite hypotheses. It does not prove
  the ten-hypothesis Platonic classification.
- `squarePolar_rates_forced` assumes three scalar balance equations;
  `squarePolar_forced_quartic_lower` assumes the displayed polar rate. Neither
  contains graph, reversibility, minimax, compactness, or attainment.
- The local feasibility declarations assume supplied dependence/equilibrium
  data. They do not formalize convex-hull relative-interior equivalences or the
  full Farkas alternative.
- No Lean theorem formalizes a P1E perturbation radius, a complete adaptive
  ring proof, a transport-improvement result, or a physical HTS model.
- Theorem 6.1 and Corollary 6.2 map to the exact declarations listed in the
  manuscript. The former Corollary 6.3 is non-theorem discussion in R7; Lean
  path and scalar lemmas are not promoted to one global geometric-stability
  signature.

Controlling artifacts: `LEAN_DECLARATION_INDEX.json`,
`AFPBarrier/ReleaseAxiomAudit.lean`, and `LEAN_RELEASE_AUDIT.log`.

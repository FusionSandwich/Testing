# P0/M1 spherical feasibility theorem-to-file map

The table distinguishes the complete ordinary proof, Lean-checked finite
consequences, exact regression examples, and standard external inputs. The
main theorem document is supplemented by
`SPHERICAL_FEASIBILITY_OPTIMAL_VALUE_SENSITIVITY.md` for the explicit transfer
from a robust feasible row to the actual perturbed optimum.

| Package item | Exact statement / location | Lean support | Exact regression | Status |
|---|---|---|---|---|
| Non-antipodal nonnegative feasibility | Theorem 1.2(1) in `SPHERICAL_FEASIBILITY_SHARED_EDGE_THEOREM.md` | Constructive directions in `LocalSphericalFeasibility.lean`; scale positivity in `SphericalFeasibilityAlgebra.lean` | outside, boundary, and interior rational tangent sets | PROVED |
| Strict all-index feasibility | Lemma 1.1 and Theorem 1.2(2) | Spherical scaling consequences formalized; finite relative-interior theorem proved in ordinary text | square and boundary examples; repeated points | PROVED |
| Repetitions and redundancies | Lemma 1.1; Theorem 1.4 | Indexed finite sums in all local Lean modules | duplicate-direction nonuniqueness certificates | PROVED |
| Dependence/row bijection | Theorem 1.2(3), equations (1.2)–(1.4) | `LocalSphericalFeasibility.lean`; `scaledSphericalRowRate_eq_commonScale` | exact rational rates with `sin=4/5`, `loss=2/5` | PROVED |
| Uniqueness | Theorem 1.4: affine independence in the minimal face | Ordinary proof; finite scaling injection formalized | duplicates demonstrate failure of uniqueness | PROVED |
| Unique positive common scale | Corollary 1.3 | `commonScale_eq_two_div`, `commonScale_pos` | direct exact rate reconstruction | PROVED / Lean |
| Antipodal-only theorem | Theorem 2.1 and Corollary 2.2 | `antipodalOnly_normalBalance_iff` | three-antipode simplex point | PROVED / Lean |
| Mixed antipodal theorem | Theorem 2.1, equations (2.1)–(2.4) | `antipodalTotalRate`, budget identity and strict/nonnegative iff lemmas | mixed boundary and mixed strict examples | PROVED / Lean |
| Relative margin | Equations (3.1)–(3.3) | Ordinary proof | boundary-crossing family | PROVED |
| Controlled minimum barycentric coefficient | Lemma 3.1, `delta=rho/[m(1+rho)]` | Ordinary proof | redundant all-positive examples | PROVED |
| Loss-window outgoing bounds | Equations (3.9)–(3.10) | `QuantitativeSphericalFeasibility.lean` | exact normal balances | PROVED / Lean |
| Margin-dependent coefficient bounds | Equations (3.11)–(3.12) and sensitivity note (2.2)–(2.3) | Ordinary proof plus Lean row formula | square rates | PROVED |
| Local conditioning | Equations (3.13)–(3.17) | Ordinary singular-value proof | deterministic matrix checks are optional, not evidentiary | PROVED |
| Local perturbation radius | Equations (3.18)–(3.22) | Ordinary proof | rational family crossing outside/boundary/interior | PROVED |
| Robust-row rate/objective perturbation | Equations (3.23)–(3.25) | Ordinary proof | exact examples guard signs and denominators | PROVED |
| Actual optimal-value perturbation | `SPHERICAL_FEASIBILITY_OPTIMAL_VALUE_SENSITIVITY.md`, equations (4.1)–(5.7) | Ordinary compactness, convex robustification, and right-inverse proof | boundary-crossing example establishes zero-margin limitation | PROVED |
| Shared-edge matrix and cone | Equations (4.1)–(4.4), Theorem 4.1 | `DualCertificate.lean`; edge block in `GlobalSharedEdgeDuality.lean` | cube matrix | PROVED |
| Compact feasible polytope and conductance budget | Equations (4.5)–(4.7) | Ordinary proof | cube conductances | PROVED |
| Weighted centering necessity | Equation (4.8), Theorem 4.2 | `ReversibleConductance.lean`, `CompleteGraph.lean` | centered and noncentered checks | PROVED / Lean |
| Dense complete-graph sufficiency | Equation (4.9) | `CompleteGraph.lean` | symmetric examples | PROVED / Lean |
| Full Farkas alternative | Theorem 4.3 with exact AFP matrix/signs | Standard external finite Farkas theorem; soundness in `DualCertificate.lean`; edge block in `GlobalSharedEdgeDuality.lean` | exact cube infeasibility field | PROVED / EXTERNAL CORE |
| Dual geometric interpretation | Equations (4.12)–(4.13) | `sharedEdgeDualWork_*` | zero-work cube certificate; radial optimal field | PROVED / Lean |
| Strict global feasibility | Equations (4.14)–(4.17) | Ordinary conic proof | strict equal-mass cube | PROVED |
| Strong LP duality | Problems `(P_c)` and `(D_c)`, equations (4.18)–(4.19) | Standard external strong-duality theorem; exact objective-gap and componentwise complementarity in `GlobalSharedEdgeDuality.lean` | cube primal/dual value 24 | PROVED / EXTERNAL CORE + Lean consequences |
| Rate and linear-defect minimization | Section 4.5 cost specializations | Same generic LP Lean consequences | cube total-rate optimum | PROVED |
| Peak row defect/rate epigraph dual | Equations (4.20)–(4.22) | Ordinary transfer of standard LP duality | algebraic sign checks | PROVED |
| Weighted residual minimization | Equations (4.23)–(4.25) | Ordinary transfer; generic weak duality in `DualCertificate.lean` | deterministic sign checks | PROVED |
| Global sensitivity | Equations (4.26)–(4.34) | Ordinary pseudoinverse proof | not used as proof | PROVED |
| Locally feasible, centered, globally incompatible example | Section 5.4 | Farkas soundness formalized generically | exact cube field with `A^T y=0`, `b.y=-4` | PROVED / exact certificate |
| Globally strict symmetric example | Section 5.5 | generic complementarity formalized | exact cube primal/dual value 24 | PROVED / exact certificate |
| Sparse reconciliation mechanism | Centered-clique Theorem 4.5 | Ordinary finite sum proof; complete-clique block already formalized in `CompleteGraph.lean` | block construction examples | PROVED |
| Placeholder / axiom policy | Workflow `.github/workflows/afp-spherical-feasibility.yml` | Lean build plus independent `nanoda`, `nanoda-allow-sorry: false`, and source grep | exact Python suite in same workflow | ENFORCED |

## External theorem boundary

The complete finite barycentric and relative-interior equivalences are proved
inside the theorem document. The general Farkas alternative and strong LP
duality are standard external finite-dimensional theorems. They are not
reproved in Lean at this stage; instead, every hypothesis, sign convention,
AFP edge block, objective, residual variable, and complementary-slackness
condition is transferred explicitly, while certificate soundness and the
spherical finite consequences are Lean checked.

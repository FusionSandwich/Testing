# Sphere-specific theorem-to-file map

The ordinary proof is authoritative for the complete theorem package. Lean
formalizes finite algebra and spherical consequences that can be checked
without delaying the ordinary finite convex and LP proof.

| Theorem or certificate | Ordinary proof | Lean / executable support | Status |
|---|---|---|---|
| Tangent/normal separation of the degree-one spherical row | `pure_math/SPHERICAL_LOCAL_EXACT.md` | `AFPBarrier/LocalSphericalFeasibility.lean` | PROVED |
| Nonnegative dependence iff `0` is in the tangent convex hull | `pure_math/SPHERICAL_LOCAL_EXACT.md` | Scaling consequences and exact examples | PROVED; convex lemma ordinary |
| Positive indexed dependence iff `0` is in relative interior | `pure_math/SPHERICAL_LOCAL_EXACT.md` | Boundary/interior/redundancy regressions | PROVED; convex lemma ordinary |
| Exact tangent-dependence uniqueness criterion | `pure_math/SPHERICAL_LOCAL_EXACT.md` | Repeated/redundant exact regressions | PROVED ordinary |
| Unique positive normal scale and explicit rate formula | `pure_math/SPHERICAL_LOCAL_EXACT.md` | `LocalSphericalFeasibility.lean`; `AntipodalSphericalFeasibility.lean` | PROVED and finite algebra formalized |
| Complete antipodal-only and mixed classification | `pure_math/SPHERICAL_LOCAL_EXACT.md` | `AntipodalSphericalFeasibility.lean`; exact regressions | PROVED; scalar core formalized |
| Relative cone margin and dual support formula | `pure_math/SPHERICAL_LOCAL_QUANTITATIVE.md` | Deterministic margin examples | PROVED ordinary |
| Controlled minimum barycentric coefficient | `pure_math/SPHERICAL_LOCAL_QUANTITATIVE.md` | Ordinary averaging proof | PROVED ordinary |
| Outgoing and coefficientwise rate bounds | `pure_math/SPHERICAL_LOCAL_QUANTITATIVE.md` | `LocalSphericalBounds.lean` formalizes the loss-window sandwich | PROVED; finite scalar core formalized |
| Conditioning of tangent and augmented systems | `pure_math/SPHERICAL_LOCAL_QUANTITATIVE.md` | Ordinary singular-value proof | PROVED ordinary |
| Direction/angle perturbation and objective degradation | `pure_math/SPHERICAL_LOCAL_QUANTITATIVE.md` | Rational boundary-crossing regression | PROVED ordinary |
| Edge-column cone and feasible-polytope characterization | `pure_math/SHARED_EDGE_CONE_FARKAS.md` | Generic finite matrix infrastructure in `DualCertificate.lean` | PROVED ordinary |
| Weighted centering necessity | `pure_math/SHARED_EDGE_CONE_FARKAS.md` | `ReversibleConductance.lean`; `CompleteGraph.lean` | PROVED and formalized |
| Dense complete-graph positive construction | `pure_math/SHARED_EDGE_CONE_FARKAS.md` | `CompleteGraph.lean` | PROVED and formalized |
| Full finite Farkas alternative with AFP signs | `pure_math/SHARED_EDGE_CONE_FARKAS.md` | Soundness in `DualCertificate.lean`; strain in `SharedEdgeGeometry.lean` | PROVED using a precisely stated standard finite theorem; consequences formalized |
| Linear-objective strong duality and complementarity | `pure_math/SHARED_EDGE_OPTIMIZATION_DUALS.md` | Weak duality in `DualCertificate.lean`; gap/complementarity in `DualComplementarity.lean` | PROVED using standard finite LP theorem; gap consequences formalized |
| Peak outgoing-rate dual | `pure_math/SHARED_EDGE_OPTIMIZATION_DUALS.md` | Ordinary endpoint-price derivation | PROVED ordinary |
| Weighted `l1` residual dual and signs | `pure_math/SHARED_EDGE_OPTIMIZATION_DUALS.md` | Ordinary standard-form derivation; exact sign regression | PROVED ordinary |
| Strict all-edge feasibility iff relative cone interior | `pure_math/SHARED_EDGE_STRICT_SENSITIVITY.md` | `DualComplementarity.lean` formalizes the strict-primal zero-work consequence | PROVED; one direction formalized |
| Node/mass sensitivity | `pure_math/SHARED_EDGE_STRICT_SENSITIVITY.md` | Ordinary pseudoinverse and norm estimates | PROVED ordinary |
| Centered-clique sparse reconciliation | `pure_math/SHARED_EDGE_RECONCILIATION_EXAMPLES.md` | Direct substitution proof | PROVED ordinary |
| Locally strict, centered, globally incompatible cube | `pure_math/SHARED_EDGE_RECONCILIATION_EXAMPLES.md` | `pure_math/examples/spherical_feasibility_examples.py` | PROVED by direct equations and exact Farkas certificate |
| Globally strict cube with exact LP primal/dual pair | `pure_math/SHARED_EDGE_RECONCILIATION_EXAMPLES.md` | Same exact regression script | PROVED by exact rational/scaled-coordinate checks |

## External finite theorems used

No user-declared axiom is added to Lean. The ordinary proof invokes only these
standard finite-dimensional results, with every hypothesis verified in the
proof:

1. supporting/separating hyperplane theorem for a compact finite polytope in
   its affine span;
2. closedness of a finitely generated cone;
3. Farkas' alternative in equality/nonnegative-variable form;
4. strong duality and attainment for a feasible bounded finite LP;
5. the Moore–Penrose minimum-norm correction bound; and
6. the support-function characterization of centered inradius.

The actual AFP matrices, transposes, right-hand sides, edge costs, and sign
conventions are displayed in the proof rather than hidden behind a generic
citation.

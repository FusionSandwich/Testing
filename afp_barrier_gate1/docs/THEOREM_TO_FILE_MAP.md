# Exact feasibility theorem-to-file map

The complete mathematical proof source is
`pure_math/EXACT_LOCAL_GLOBAL_THEOREM_PACKAGE.md`.  “Lean support” identifies
the finite algebra formalized in the project; standard finite convex geometry,
Farkas, LP strong duality, and SVD facts are transferred explicitly in the
proof document rather than misrepresented as locally formalized.
The non-antipodal and quantitative entries (Sections 1 and 3) assume
`J` is nonempty; the empty-`J` case belongs exclusively to the pure-antipodal
Theorem 2.1.

| Mandatory item | Mathematical proof | Lean support | Exact regression |
|---|---|---|---|
| 1.1 feasibility iff `0 in P` | Theorem 1.1 | `LocalSphericalFeasibility.lean`, `ExactLocalRows.lean` | outside/boundary cases |
| 1.2 strict iff relative interior | Theorems 1.1, 3.1 | indexed positivity in `ExactLocalRows.lean` | lower/full-dimensional cases |
| 1.3 repetitions and lower dimension | Theorem 1.1, Section 5 | indexed functions require no injectivity | repeated-direction case |
| 1.4 scaling and converse | Theorem 1.2 | `LocalSphericalFeasibility.lean`, `ExactLocalRows.lean`, `SphericalFeasibilityAlgebra.lean` | all local exact rows |
| 1.5 outgoing rate | Corollary 1.3 | `ExactLocalRows.lean` | equilateral rate |
| 1.6 uniqueness | Corollary 1.3 | inverse normalization/scaling algebra | singleton boundary case |
| 2.1 antipodal simplex | Theorem 2.1 | `AntipodalFeasibility.lean` | pure antipodes |
| 2.2 mixed feasibility | Theorem 2.1 | zero-tangent construction | mixed outside case |
| 2.3 mixed strict criterion | Theorem 2.1 | strict budget algebra plus convex transfer | mixed interior |
| 2.4 mixed parameterization | Theorem 2.2 | packaged iff and both directions in `AntipodalFeasibility.lean` | boundary/interior cases |
| 2.5 boundary case | Theorem 2.1 | finite balance algebra | forced zero coefficient |
| 2.6 no antipodal division | Theorem 2.2 | disjoint `J`/`A` types | source audit |
| 3.1 margin equivalence | Theorem 3.1 | standard compact convex transfer | exact strict/boundary margins |
| 3.2 constructive bound | Theorem 3.1 | finite uniform-mixture normalization and coefficient margin in `QuantitativeExactLocal.lean`; geometric inball selection in the proof | triangle/square margins |
| 3.3 rate/coefficient bounds | Theorem 3.3 | exact identity in `ExactLocalRows.lean`; weighted/two-factor bounds in `QuantitativeExactLocal.lean`; independent loss-window bounds in `QuantitativeSphericalFeasibility.lean` | equilateral rate |
| 3.4 dual and LP formulas | Theorem 3.2 | weak dual algebra plus exact strong-duality transfer | exact optima |
| 3.5 perturbation | Theorem 3.4 | finite column estimates where practical | boundary crossing/robust hull |
| 3.6 local matrix conditioning | Theorem 3.5 | finite algebra plus transferred SVD | explicit `1/sigma` bounds |
| 4.1 cone/polytope/Farkas | Theorem 4.1 | `DualCertificate.lean`, `SharedEdgeEquilibrium.lean` | exact square matrix |
| 4.2 centering | Theorem 4.2 | `ReversibleConductance.lean`, `SharedEdgeEquilibrium.lean` | centered obstruction |
| 4.3 complete graph | Theorem 4.2 | `CompleteGraph.lean` at eigenvalue two | symmetric strict cases |
| 4.4 full Farkas alternative | Theorem 4.1 | certificate soundness plus transferred separation | exact certificate |
| 4.5 LP duality/complementarity | Theorem 4.3 | `DualCertificate.lean`, objective-gap and componentwise complementarity in `GlobalSharedEdgeDuality.lean`; precise standard transfer | sign audit |
| 4.6 local-not-global | Theorem 4.4 | exact `Fin` proof in `SharedEdgeEquilibrium.lean` | four-cycle certificate |
| 4.7 averaging reconciliation | Theorem 4.5 | `GroupAveraging.lean`: invariant orbit average, unordered-edge transitivity, representative orientation propagation, off-edge support, nonnegativity, and exact balance | equal-mass square |
| 4.8 global perturbation | Theorem 4.6 | pseudoinverse/range transfer | explicit radius |
| 5 examples and claim control | Section 5 | exact finite examples where practical | `exact_local_global_audit.py`; independent rational `test_spherical_feasibility.py` cube and boundary suite |

The focused axiom report is `AFPBarrier/PureMathAxiomAudit.lean`.  CI builds
the aggregate library, runs the exact symbolic certificates, scans for proof
placeholders and user axioms, and checks the focused axiom output for
`sorryAx`.

## Prompt 2 and Prompt 3 extensions

Prompt 2's sampling-aware covariance and spectral-product package is mapped in
`P2_THEOREM_TO_FILE_MAP.md`.  Prompt 3's exact equality, fixed
ten-hypothesis classification, explicit graph/spectral/resistance
near-rigidity, corrected closed threshold, and covariance anisotropy package is
mapped in `P3_THEOREM_TO_FILE_MAP.md`.

The Prompt 3 map explicitly separates PROVED ordinary results, EXTERNAL
topological/variational inputs, COMPUTATIONAL finite certificates, and
REJECTED unrestricted formulations.  In particular, source-pinned Plantri
enumeration is not the classification proof, and the antipodal `ell=2` model
rejects tangent normalization without the corrected `0<ell<2` hypothesis.

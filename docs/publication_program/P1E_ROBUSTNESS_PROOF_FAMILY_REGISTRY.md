# Proposition 7.3 proof-family registry

| Proof family | Status | Exact surviving content | Missing lemma or rejection reason |
|---|---|---|---|
| global all-level straight-line majorant | REJECTED | none beyond diagnostic formulas | no literal expression DAG, verified operation count, denominator certificate, inverse bound, positivity margin, or recurrence estimate; the former enormous constant is unsupported |
| exact symbolic differentiation | BLOCKED_FOR_UNIFORM / RETAINED_DIAGNOSTIC | exact local row and transition formulas | derivatives are not assembled into a level-uniform global bound |
| interval arithmetic / Taylor models | BLOCKED_FOR_UNIFORM / AVAILABLE_FOR_FIXED_LEVEL | can compute outward-rounded bounds for any fixed finite level | no committed production-level all-level certificate or uniform compact box |
| compactness-only argument | REJECTED_AS_UNIFORM | continuity on each fixed finite parameter neighborhood | the disjoint sequence of refinement levels is not one compact parameter set and supplies no uniform radius |
| positive-cone perturbation | PROVED_FIXED_LEVEL | strict finite base margin plus continuity keeps all shared conductances positive | the margin may deteriorate with level |
| quantitative implicit-function / Neumann argument | PROVED_FIXED_LEVEL | literal finite system, block Jacobian nonsingularity, unique analytic conductance solution, computable level-dependent radius | no uniform inverse norm is asserted |
| exact rational certificate | INTERFACE_READY | conformance schema and two independent exact verifiers | committed fixture is conformance-only; a production certificate requires an extended status schema plus actual level data and hashes |
| adversarial counterexample search | ACTIVE_REGRESSION | rejects gap collapse, determinant collapse, zero margins, support mutations, rate/defect underclaims, and loss of reflection | finite attacks are not proof of a universal theorem |
| Lean formalization | FINITE_ALGEBRA_ONLY | shared-conductance reversibility, force/moment identities, polygon identities | analytic radius and construction recurrence are not formalized |

## Surviving theorem

The surviving route is the fixed-level theorem in
`P1E_FIXED_SUPPORT_ROBUSTNESS_THEOREM.md`. For each production level `J` of the `M_0=2^80` family, the
finite exact system is block lower triangular. Its first-row, ordinary,
transition, and equatorial diagonal blocks are nonsingular at the strictly
positive base point. Continuity and the Neumann lemma give a computable
level-dependent radius. This proves support preservation, positivity,
reversibility, exact `H_0 direct-sum H_1` fidelity, graph connectivity, and
conservative rate and quadratic-defect constants.

The uniform route remains rejected until every missing uniform lemma is
supplied by independently checkable evidence.

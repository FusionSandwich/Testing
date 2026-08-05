# P2A theorem--proof--test--registry map

Status: **release-candidate map**.  Every mathematical claim below has one
controlling proof source, one executable or kernel test source, and one
claim-registry entry.  The map does not promote numerical solver status to a
theorem: solver-independent residuals, exact reconstructions, or formal
identities are the controlling evidence.

## Controlling map

| Claim | Exact statement controlled here | Proof source | Test or certificate source | Registry entry |
|---|---|---|---|---|
| P2A-AFFINE | For shared conductances, `L_gamma=-W^-1 B Diag(gamma) B^T` has constants, positivity and `W`-reversibility automatically; coordinate exactness is exactly `A gamma=b`, and `C gamma<=Rw` is exactly the directed-rate cap. | `P2A_FIXED_QUADRATURE_CONVEX_DESIGN.md`, Sections 1--2, Theorem 2.1 | `pure_math/tests/test_p2a_convex_design.py`: assembly, sign, exact-coordinate, rate and reversibility tests; `AFPBarrier/ConvexGeneratorDesign.lean` | `THEOREM_REGISTRY.md`, `P2A-AFFINE`; `VALUE_REGISTRY.md`, `P2A-A`, `P2A-C` |
| P2A-QUOTIENT | Exact removal of the sampling kernel followed by `W`-orthonormal whitening produces `T_l(gamma)=W^(1/2)(L_gamma+l(l+1)I)V_l`, and `||T_l||_2` is the sampled quotient defect without output compression. | Main P2A document, Section 3, Theorem 3.1 | P2A test module: exact rank/nullspace, alias mutation, ambiguous-rank rejection and output-leakage tests | `THEOREM_REGISTRY.md`, `P2A-QUOTIENT`; `VALUE_REGISTRY.md`, `P2A-TL` |
| P2A-PRIMAL | The fixed-rate spectral defect, fixed-defect rate, Frobenius shell, selected vector/scalar minimax, multi-shell and fixed-response programs are SDP/SOCP/QP/LP formulations; reoptimization on a fixed retained support remains convex. | Main P2A document, Section 4, Theorem 4.1 | P2A test module: DCP/cone classification and cross-formulation solves through the unified interface | `THEOREM_REGISTRY.md`, `P2A-PRIMAL`; `VALUE_REGISTRY.md`, `DESIGN` |
| P2A-DUAL | The displayed conic duals, Slater/minimal-face qualifications and complementary-slackness equations are the exact dual systems for the retained formulations. | Main P2A document, Sections 5--6, Theorem 6.1 | `optimization/certificates.py`; P2A test module: primal/dual feasibility, complementarity, objective-gap and exact tetrahedral dual tests | `THEOREM_REGISTRY.md`, `P2A-DUAL` |
| P2A-CERT | Exact or genuinely outward-enclosed linear/conic Farkas rays are independently checkable infeasibility certificates.  Raw floating residuals and tolerance-padded primal/dual gaps are diagnostics until rational/algebraic reconstruction or a genuine outward interval enclosure is supplied. | Main P2A document, Section 7 | `optimization/certificates.py`; `optimization/exact_audit.py`; P2A test module: unequal-mass four-cycle and cube separators, rate-cap failure, rejected-invalid-ray tests and `tolerance_diagnostic` labeling | `THEOREM_REGISTRY.md`, `P2A-CERT` |
| P2A-SPARSITY | Exact `H_1` reproduction fixes `sum_e (1-Omega_i.Omega_j)gamma_e=sum_i w_i`; plain total conductance equals one half the stationary mean rate and is generally not fixed.  Group penalties are convex heuristics, whereas reweighting and support choice are nonconvex outer procedures. | Main P2A document, Section 8, Theorem 8.1 and Proposition 8.2 | P2A test module: fixed-loss identity, variable-total witnesses, group penalty, pruning/reoptimization and rejected-deletion tests; finite loss identity in Lean | `THEOREM_REGISTRY.md`, `P2A-SPARSITY`; `VALUE_REGISTRY.md`, `P2A-LOSS-L1`, `P2A-TOTAL` |
| P2A-SHARP | On `S^2`, accepted Paper I implies `opt_D(R)>=6/R` and `opt_R(delta)>=6/delta`; tetrahedral and nonantipodal-octahedral examples attain the frontier and exercise deficient sampled `H_2` ranks. | Main P2A document, Sections 9--10 | `optimization/exact_audit.py`; P2A test module: exact symmetric reconstruction, quotient rank, rate, defect, objective and solver comparison; retained P1A/P1B exact audits | `THEOREM_REGISTRY.md`, `P2A-SHARP`; `VALUE_REGISTRY.md`, `P2A-LOWER`, `P2A-TETRA`, `P2A-OCTA` |
| P2A-RESPONSE | Shellwise deflation preserves convexity for positive weighted multi-shell and fixed linear response Frobenius, operator, vector and scalar objectives. | Main P2A document, Sections 4.5--4.6 and 5.5 | P2A test module: affine response transformation, metric classification and solve tests | `THEOREM_REGISTRY.md`, `P2A-RESPONSE` |
| P2A-FORMAL | The finite shared-conductance, endpoint-rate, convex-combination and loss identities used above are machine checked without project-local axioms or proof holes. | `AFPBarrier/ConvexGeneratorDesign.lean` | `lake build`; focused Lean file check; `AxiomAudit.lean` and `PureMathAxiomAudit.lean` dependency audit | `THEOREM_REGISTRY.md`, `P2A-FORMAL` |

Bare `P2A*.md` names and “Main P2A document” references in the table mean
files under `docs/publication_program/`.  Paths beginning `pure_math/` or
`AFPBarrier/` are relative to `afp_barrier_gate1/`; explicitly written
`docs/...` paths are repository-relative.  The exact test function names are
allowed to evolve within the single controlling P2A test module; the release
workflow executes the complete module and checks its terminal acceptance
sentinel.

## External theorem transfer ledger

External results are comparison or finite-dimensional optimization tools;
none substitutes for the new fixed-quadrature construction.

| External result | Transferred hypothesis | Where checked | Permitted conclusion |
|---|---|---|---|
| finite-dimensional conic duality | closed finite-dimensional cones; affine constraints; the stated strict-feasibility or minimal-face condition | Main P2A document, Sections 5--6; program DCP audit and certificate verifier | the displayed dual and strong duality under the stated qualification |
| Paper-I sharp product lower bound | positive reversible spherical generator, exact constants and coordinates, accepted sampled quotient, finite rate | Main P2A document, Section 10; P1A/P1B regression jobs | `D_2 r_max >= 6`, hence the two optimizer lower bounds |
| Bienvenue--Naceur--Carrier--Hébert moment equations | their normalization and shared off-diagonal interpretation are compared explicitly; their printed factor convention is not imported | `P2A_PRIOR_ART_AND_HOSTILE_AUDIT.md` and main Section 11.1 | adjacent application context only |
| Seibold positive stencils | local positive consistency systems, generally without a shared reversible global matrix | main Section 11.2 and hostile prior-art audit | adjacent local-stencil precedent only |
| Babecki--Steinerberger--Thomas graph sparsifiers | positive subgraph reweightings preserving selected eigenpairs of a given graph | main Section 11.3 and hostile prior-art audit | direct convex eigenpair-preservation precedent, with the stated P2A distinction |

## Deliberately excluded claims

- No claim says local row feasibility implies a global reversible generator.
- No claim says a plain `l1` cost discovers a useful sparse support.
- No claim treats mixed-integer support selection or iterative reweighting as
  convex.
- No claim infers strong duality solely from a solver's status string.
- No claim identifies a finite rotated-mode set with a continuum rotation
  supremum.
- No claim transfers the fixed angular result to a transport improvement
  without the separate response-validation stage.

## Release evidence boundary

Commit identifiers, workflow run identifiers and artifact digests are
reproducibility metadata, not premises of any displayed theorem.  The P2A
workflow records the candidate commit and tree, exact changed-path set,
dependency versions, test logs, Lean logs and SHA-256 record manifest in its
release artifacts; the create-only archive ref is accepted only at that same
candidate commit.

# P2C stage report — quadrature–generator co-design

## Lineage

- repository: FusionSandwich/Testing
- literal parent commit: 9b39b6ad52213197c0af75d4988eccd1a29d66a9
- parent state: accepted P2B archive
- parent P2A commit: 07138547ff5c85df071e2067587dd83ca20b71b5
- candidate branch: agent/afp-publication-p2c-codesign-9b39b6ad-v2
- scope: new P2C package, tests, theorem/audit documents, and dedicated workflow

No untracked earlier P2C prototype was treated as evidence.  The implementation was rebuilt from the literal accepted P2B parent and the handoff’s frozen definitions.

## Mathematical result

The stage proves:

- exact equivalence of the raw moving-Gram LMI and full sampled shell defect;
- global fixed-candidate SDP optimality and attainment;
- protected compact outer existence;
- orbit covariance and proximal stationary accumulation;
- restored Riemannian and certified Clarke stationary accumulation;
- alternating convergence with a tangent-frame or joint safeguard;
- unconditional edge-addition monotonicity and conditional deletion;
- finite graph-search termination with no certified improving unvisited proposal, with exact neighbor stationarity reserved for exhaustive exclusion certificates;
- exact dense design initialization;
- enriched-discrete response refinement;
- collision/streaming/interpolation separation; and
- the every-level convergence sandwich
  3 h^2/(32 pi^2) <= D2_opt <= 75 h^2/2.

It does not claim a global solution of the nonconvex node problem, whole-sequence convergence, arbitrary-design local compatibility, continuum accuracy from an enriched discrete identity, or collision control of streaming rays.

## Artifact inventory

### Code

- pure_math/codesign/types.py
- pure_math/codesign/families.py
- pure_math/codesign/metrics.py
- pure_math/codesign/inner.py
- pure_math/codesign/feasibility.py
- pure_math/codesign/outer.py
- pure_math/codesign/graph_updates.py
- pure_math/codesign/adaptive.py
- pure_math/codesign/rotations.py
- pure_math/codesign/convergence.py
- pure_math/codesign/fixtures.py
- pure_math/codesign/exact_audit.py
- pure_math/codesign/audit.py

### Proof and audit documents

- P2C_QUADRATURE_GENERATOR_CODESIGN.md
- P2C_APPROACH_REGISTRY.md
- P2C_CLAIM_MAP.md
- P2C_CLAUSE_MATRIX.md
- P2C_PRIOR_ART_AND_HOSTILE_AUDIT.md
- this stage report

### Tests and automation

- test_p2c_codesign.py
- dedicated P2C GitHub Actions workflow
- retained P1E, P2A, and P2B regression gates
- symbolic exact finite-algebra audit
- changed-path and documentation-sentinel gates

## Multi-route search record

Three independent route families were kept separate through their first proof/audit cycle:

1. finite-group orbit reduction and exact proximal geometry;
2. raw moving-Gram SDP geometry and lifted Riemannian restoration;
3. graph-order certificates, adaptive adjoints, and physical rotation separation.

The arbitrary local spherical-design compatibility route remains explicitly BLOCKED.  The completed convergence theorem instead uses the accepted global P1E construction and therefore does not assume the blocked statement.

## Reproducibility contract

Each benchmark row carries node/edge counts, scale, D2, maximum rate, Gram conditioning, higher-shell residuals, a labelled 24-rotation empirical spread, formula bounds, time, memory, and whether the exact inner optimizer was run.  The practical M0=32,64 rows are finite regressions; the analytic theorem uses the accepted M0=2^80 admissibility predicate.  Exact symmetric identities are checked with SymPy.  Numerical design results must pass the accepted P2A independent verifier.  Graph updates require objective enclosures and rebuilt feasibility residuals.  The workflow pins its direct Python dependencies, records the complete transitive environment, archives the full exact candidate tree, and publishes the audit output.

## Acceptance gates

The stage is accepted only when all of the following pass on the exact candidate head:

1. compileall;
2. symbolic exact audit sentinel;
3. P2C hostile pytest suite;
4. P2C executable audit and convergence records;
5. retained P1E/P2A/P2B regressions;
6. documentation claim/placeholder scan;
7. changed-path allowlist;
8. independent theorem and hypothesis audit;
9. exact-head branch/archive check.

A green solver exit without the independent residual and documentation gates is insufficient.

# Paper II P2A–P2F final completion audit

**Audit date:** 2026-08-07  
**Repository:** `FusionSandwich/Testing`  
**Audited parent:** `archive/afp-publication-p2c-codesign-verified`  
**Audited SHA:** `b34c29b1b04f5293eaa4007b39d189efa03c51f5`  
**Audited tree:** `7db9e821738b0121ab3fdb1d1a40b76f85abed48`

## 1. Controlling scope

The controlling Paper-II prompt set contains exactly six stages:

1. P2A — fixed-quadrature convex design and certified solver;
2. P2B — semigroup, resolvent, and transport response-error estimates;
3. P2C — quadrature–generator co-design, rotational robustness, and convergence;
4. P2D — low-order acceleration or preconditioning;
5. P2E — preregistered equal-cost/equal-error benchmark hierarchy;
6. P2F — layered HTS response case and final Paper-II manuscript.

This audit treats a prompt as publication-complete only when its mathematical or explicitly computational deliverables are present in the repository, its tests and hostile audits are present, a prompt-specific workflow has passed on the literal candidate head, and an immutable `archive/...-verified` ref resolves to that same SHA. Open PR state and default-branch state are not acceptance signals.

## 2. Corrected live status

| Prompt | Live status | Exact accepted ref / evidence | Audit conclusion |
|---|---|---|---|
| P2A | **COMPLETE AND PUSHED** | `archive/afp-publication-p2a-convex-design-verified` at `07138547ff5c85df071e2067587dd83ca20b71b5`; PR #45; workflow run `31005575551` succeeded | Fixed-input theorem, implementation, certificates, tests, Lean boundary, and release evidence are present |
| P2B | **COMPLETE AND PUSHED** | `archive/afp-publication-p2b-harmonic-transport-verified` at `9b39b6ad52213197c0af75d4988eccd1a29d66a9`; PR #46; workflow run `31022719199` succeeded | Dynamical/steady/multigroup/adjoint theory, manufactured audits, tests, Lean boundary, and release evidence are present |
| P2C | **COMPLETE AND PUSHED** | `archive/afp-publication-p2c-codesign-verified` at `b34c29b1b04f5293eaa4007b39d189efa03c51f5`; PR #47; workflow run `31040201081` succeeded | Co-design theorem package, all six outer strategies, family descriptors, convergence inheritance, rotation scope, tests, and release evidence are present |
| P2D | **NOT IMPLEMENTED OR PUSHED** | No P2D branch, commit, PR, workflow, archive, stage report, claim map, tests, or acceleration package was found | Prompt remains open |
| P2E | **NOT IMPLEMENTED OR PUSHED** | No P2E branch, preregistration commit, immutable benchmark manifest, seven-case result package, ablation package, workflow, archive, or PR was found | Prompt remains open |
| P2F | **NOT IMPLEMENTED OR PUSHED** | No P2F branch, material-resolved HTS case, benchmark/reference package, engineering hostile audit, Paper-II manuscript, reproducibility package, workflow, archive, or PR was found | Prompt remains open; Paper II is not publication-complete |

The repository therefore contains **three of the six** required Paper-II prompts as accepted publication stages.

## 3. P2A clause audit

P2A is accepted within its fixed-node scope. The repository contains the fixed-quadrature theorem manuscript, seven retained formulations, exact sampled-kernel handling, conic/QP/LP interfaces, primal–dual and infeasibility verification, support pruning with reoptimization, exact/hostile fixtures, implementation tests, finite Lean core, claim map, stage report, dedicated workflow, candidate branch, PR, and immutable archive.

Accepted SHA:

```text
07138547ff5c85df071e2067587dd83ca20b71b5
```

Green exact-head workflow:

```text
31005575551 — AFP publication P2A fixed-quadrature convex design — success
```

No P2A completion blocker was found in this audit.

## 4. P2B clause audit

P2B is accepted within its stated analytical hypotheses. The repository contains the one-mode semigroup and resolvent identities, sampled-shell and band-limited extensions, physical-metric transfer, inhomogeneous/time-dependent/steady/multigroup theory, six-channel residual ledger, adjoint response representation, noncommuting streaming treatments, manufactured exact solutions, effectivity audits, tests, finite Lean core, claim map, stage report, dedicated workflow, candidate branch, PR, and immutable archive.

Accepted SHA:

```text
9b39b6ad52213197c0af75d4988eccd1a29d66a9
```

Green exact-head workflow:

```text
31022719199 — AFP publication P2B harmonic-defect transport — success
```

No P2B completion blocker was found in this audit.

## 5. P2C clause audit

P2C is accepted at the exact archive head. Its checked-in clause matrix maps every prompt clause to a theorem, implementation, metric, audit, or certification boundary. The package includes:

- the eight requested quadrature/node-family descriptors;
- positive masses, permitted graphs, conditioning, feasibility margins, and rotation metrics;
- exact inner P2A optimization;
- group-orbit, Riemannian, alternating, graph-update, spherical-design, and adaptive-response strategies;
- protected compactness/existence and correctly scoped descent/stationarity/subsequence claims;
- collision-versus-streaming rotation tests;
- the inherited every-level Paper-I convergence sandwich;
- deterministic benchmark records and memory/time metadata;
- exact, hostile, retained-regression, Lean, and release gates.

Accepted SHA:

```text
b34c29b1b04f5293eaa4007b39d189efa03c51f5
```

Accepted tree:

```text
7db9e821738b0121ab3fdb1d1a40b76f85abed48
```

Green exact-head workflow:

```text
31040201081 — AFP publication P2C quadrature-generator co-design — success
```

The branch `agent/afp-publication-p2c-completion-b34c29b1` resolves to the same SHA as the accepted P2C archive and contains no additional completion commit. This is not a defect in P2C because the archive itself already contains the completed P2C package. It must not be cited as evidence for P2D–P2F.

## 6. P2D missing deliverables

No repository evidence was found for the P2D prompt-specific deliverables:

- exact fixed-point/conservation-preserving synthetic acceleration or preconditioning package;
- derived error-propagation operator and harmonic-shell action;
- shell-mismatch, spectral-equivalence, or field-of-values bounds;
- streaming, energy-coupling, and boundary-condition dependence;
- sufficient iteration-reduction conditions and slow-subspace diagnostics;
- comparisons with the accepted monotone AFP baseline, classical modified FP acceleration, no acceleration, and an H2-poor positive generator;
- equal high-order discretization/stopping criteria;
- iteration, matvec, setup, wall-time, memory, and forward-peaking robustness records;
- higher-shell and ray-dominated adversarial cases;
- prompt-specific theorem/claim/approach maps, tests, workflow, PR, and immutable archive.

Older Gate-6 or surrogate transport files do not satisfy this prompt.

## 7. P2E missing deliverables

No repository evidence was found for the P2E prompt-specific deliverables:

- a preregistration commit predating all held-out runs;
- one frozen software version and immutable benchmark manifest;
- the seven mandatory benchmark cases;
- per-case conservation/positivity, H0/H1, H2/higher-shell, scalar/current/tensor, response, rotation, rate, iteration, runtime, memory, equal-direction, equal-wall-time, and equal-error records;
- an analytic, harmonic, fine-angular, Monte Carlo, or independently validated reference with uncertainty separated from method error;
- frozen training/validation/held-out partitions;
- all seven required ablations;
- raw outputs and independently reproducible benchmark runner;
- prompt-specific audits, workflow, PR, and immutable archive.

A benchmark created after held-out results would not retroactively satisfy preregistration.

## 8. P2F missing deliverables

No repository evidence was found for the P2F prompt-specific deliverables:

- an experimentally bounded and provenance-recorded Cu/Ag/REBCO/buffer/metal-substrate stack;
- normal, oblique, and grazing-sensitive cases;
- explicit separation of full neutral Boltzmann interactions, bounded BFP/FP use, secondary generation, space/energy discretization, and response tallies;
- layer scalar flux/current, traceless second angular tensor, tape-normal quadrupole, heating, charged-secondary crossing/escape, supported reaction or PKA source, directional PKA tensor, orientation sensitivity, and reference uncertainty;
- same-node optimized/baseline comparisons with a high-angular or independent reference;
- response-by-response assessment of when H2 is predictive and when higher shells dominate;
- explicit roadmap output/scope ledger;
- adversarial thin-layer/grazing/nuclear-data/ray/spatial-convergence/overclaiming review;
- complete Paper-II manuscript with formulation, convex design, error theory, implementation, benchmarks, HTS case, limitations, and reproducibility package;
- prompt-specific workflow, PR, and immutable archive.

The pre-existing synthetic/dimensionless HTS surrogate is antecedent regression material and is not a validated P2F engineering case.

## 9. Repository searches performed

The live audit checked:

- all branches matching `afp-publication-p2`, `p2d`, `p2e`, `p2f`, `paper2`, and `completion`;
- all PRs and targeted PR searches for P2D, P2E, and P2F;
- targeted commit searches for P2D, P2E, P2F, `Paper II`, and `HTS`;
- the recursive P2C archive tree;
- `docs/publication_program/`;
- `.github/workflows/`;
- the conversation and persistent file library for previously claimed Paper-II closeout artifacts.

No hidden differently named P2D, P2E, or P2F publication chain was found.

## 10. Correction of the earlier closeout statement

An earlier assistant response stated that a combined P2D–P2F archive and Paper-II closeout package had been completed. That statement is not supported by the live repository or the available file library and is withdrawn.

In particular, the following claimed items are not present and must not be cited as publication evidence:

```text
archive/afp-publication-p2def-paper2-closeout-verified
PAPER_II_P2DEF_CLOSEOUT_PACKAGE.zip
PAPER_II_P2DEF_IMMUTABLE_RELEASE_RECORD.md
PAPER_II_MANUSCRIPT.md
P2E_P2F_BENCHMARK_RESULTS.json
P2E_BENCHMARK_MANIFEST.json
P2F_ENGINEERING_HOSTILE_AUDIT.md
P2F_STAGE_REPORT.md
PAPER_II_RELEASE_SUMMARY.json
```

## 11. Required completion sequence

The safe continuation order is:

1. create P2D from the literal P2C archive SHA and close its theorem, implementation, comparisons, hostile audits, exact-head workflow, PR, and immutable archive;
2. create and commit the P2E preregistration and immutable manifest **before** running any held-out case;
3. execute all P2E cases and ablations, preserve raw outputs and reference uncertainty, then close P2E with exact-head CI and an immutable archive;
4. create P2F from the accepted P2E archive, complete the bounded HTS case and full manuscript/reproducibility package, then run the engineering hostile review;
5. only after P2F passes may a final Paper-II archive be created.

No `archive/...-verified` ref should be created for P2D, P2E, P2F, or Paper II until its literal head has passed the required gates.

## 12. Final verdict

```text
P2A  COMPLETE_AND_PUSHED
P2B  COMPLETE_AND_PUSHED
P2C  COMPLETE_AND_PUSHED
P2D  NOT_COMPLETE
P2E  NOT_COMPLETE
P2F  NOT_COMPLETE
PAPER_II  NOT_COMPLETE
```

This report is an audit record only. It deliberately does not promote missing work, invent benchmark evidence, or move any accepted archive.

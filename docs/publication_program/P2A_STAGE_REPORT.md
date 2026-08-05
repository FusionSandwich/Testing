# P2A fixed-quadrature convex-design stage report

Status: **complete release candidate, subject to the exact-head workflow**.

This stage starts literally from the accepted Paper-I/P1F state and adds a
finite-dimensional design theorem, a solver-independent implementation, an
adversarial test suite and a focused formal core.  It does not revise an
accepted Paper-I theorem or use repository state as a substitute for proof.

## 1. Frozen baseline and release refs

| Record | Exact value |
|---|---|
| accepted parent commit | `ab155b8e04bdf00306351b581739fb5feeb2979e` |
| accepted parent tree | `61a07c6c187d3002d5ca433be16b26fb1bad73f1` |
| accepted parent archive | `archive/afp-publication-p1f-flagship-paper-verified` |
| candidate branch | `agent/afp-publication-p2a-convex-design-ab155b8e` |
| create-only target archive | `archive/afp-publication-p2a-convex-design-verified` |

The workflow verifies the literal parent tree, ancestry, absence of merge
commits after the parent, exact remote branch head and exact changed-path
allowlist.  It accepts the target archive only if absent before freezing or
already equal to the candidate.  The freeze job uses an absent-ref lease, so
it cannot move an existing archive.

## 2. Delivered mathematical result

For fixed nodes `X` on `S^2`, positive masses `w` and permitted undirected
edges `E`, the stage supplies the complete shared-conductance model

`L_gamma = -W^-1 B Diag(gamma) B^T`, `gamma>=0`, `A gamma=b`,
`C gamma<=Rw`,

together with exact sampling-kernel removal and the affine shell residual

`T_l(gamma)=W^(1/2)(L_gamma+l(l+1)I)V_l`.

The main theorem document proves the following retained formulations convex:

1. minimum `D_2` at a fixed rate cap;
2. minimum rate cap at a fixed `D_2`;
3. Frobenius-shell residual minimization;
4. vector or scalar minimax over selected physical/rotated modes;
5. positive weighted multi-shell objectives through a declared degree;
6. fixed linear response-weighted objectives;
7. deterministic support pruning followed by a new exact fixed-support
   optimization.

It gives SDP spectral epigraphs, SOCP vector epigraphs, QP Frobenius
objectives and LP scalar epigraphs; exact primal and dual systems; Slater and
minimal-face qualifications; complementary slackness; exact/algebraic or
genuinely outward-enclosed linear/conic infeasibility certificates; and
independently recomputable floating diagnostics.  It also proves that the
loss-weighted conductance `l1` quantity is
fixed by exactness, diagnoses plain total conductance as a mean-rate cost,
and labels outer support choice, mixed-integer selection and reweighted
penalties nonconvex.

## 3. Requirement closure matrix

| Requested deliverable | Controlling artifact | Acceptance evidence |
|---|---|---|
| basis and sampling construction | `pure_math/optimization/model.py` | exact and guarded-rank shell tests |
| exact sampling-kernel removal | model module and main Section 3 | exact nullspace, alias mutation, ambiguous-rank rejection |
| conductance and rate assembly | model module and main Section 2 | sign, coordinate, rate, reversibility and loss-identity tests |
| one SDP/SOCP/QP/LP interface | `pure_math/optimization/programs.py` | DCP audit, cone classification and cross-formulation solves |
| primal/dual residual verification | `pure_math/optimization/certificates.py` | independent residual, complementarity and objective-gap checks |
| condition estimation | model shell diagnostics | full-rank ill-conditioned family and declared-rank guard tests |
| exact symmetric reconstruction | main Sections 9--10 and P2A tests | tetrahedral and octahedral rank/rate/defect identities |
| deterministic failure certificates | certificate module and main Section 7 | unequal-mass four-cycle/cube and rate-cap Farkas fixtures |
| support pruning/reoptimization | `prune_and_reoptimize` | deterministic order, exact re-solve and rejected deletion |
| lower-bound comparison | main Section 10 | retained P1A/P1B audits plus equality fixtures |
| local-feasible/global-infeasible graph | main Section 9.3 | exact four-cycle separating field |
| formal finite core | `AFPBarrier/ConvexGeneratorDesign.lean` | focused build and axiom-dependency audit |
| claim/source/test registry | `P2A_CLAIM_MAP.md` and global registries | exact registry-key and path sentinels |
| prior-art boundary | `P2A_PRIOR_ART_AND_HOSTILE_AUDIT.md` | hypothesis-transfer and overclaim sentinels |

## 4. Implementation contract

The package under `afp_barrier_gate1/pure_math/optimization/` separates
immutable numerical data from CVXPY expressions.  A solver returns a
candidate only.  Verification rebuilds `H_0`, coordinate, reversibility,
positivity, rate, shell, cone, stationarity, complementarity and objective
residuals from frozen arrays.  Exact sampling certificates use SymPy
rank/nullspace arithmetic; floating sampling uses an explicit ambiguity band
and fails deterministically instead of silently selecting a rank.

The solver interface pins CVXPY and the open-source backends exercised by CI.
It never treats a backend status as a proof.  Symmetric examples are checked
against exact rational/algebraic values.  Finite-precision primal and dual
data are accepted as numerical candidates only through declared scale-aware
tolerances; their reported `tolerance_diagnostic` bracket is not called a
certificate until reconstructed exactly or enclosed with genuine outward
interval arithmetic.

## 5. Adversarial closure

| Attack | Resolution |
|---|---|
| wrong generator or incidence sign | coordinate and reversibility mutations fail deterministic residual checks |
| sampling alias retained as a physical mode | exact nullspace removal and rank-nullity checks reject the mutation |
| output compressed to the sampled image | full-output residual test detects leakage outside the input quotient |
| local rows mistaken for a shared global conductance | unequal-mass four-cycle and cube fixtures have exact separating Farkas fields |
| `l1` objective advertised as sparsity | fixed loss-weighted identity is proved; support surrogates are labeled honestly |
| solver status substituted for duality | independent primal/dual/cone/complementarity verifier is mandatory |
| boundary Slater assumed | minimal-face alternative and explicit qualification are stated |
| asymptotic or transport claim smuggled into fixed design | theorem boundary excludes both; response objectives are fixed linear maps only |
| novelty reduced to missing terminology | prior-art audit grants positive-stencil and convex eigenpair-preserving precedents and states the narrower combined distinction |

No adversarial route left an unproved compatibility condition in the retained
theorem.  The implementation tests are falsification aids and computational
deliverables; they are not used in place of the all-data algebraic proofs.

## 6. Workflow acceptance gates

The exact-head workflow performs four independent gates:

- **scope and regressions:** verifies the baseline, no-merge ancestry, exact
  UTF-8 regular-file allowlist, dependency pins, the entire P2A suite,
  accepted P1A/P1B audits, deterministic sentinels, placeholder/control-byte
  scans and a clean worktree;
- **formal kernel:** builds the project, checks the focused P2A Lean file and
  both axiom-audit aggregates, rejects `sorry`, `admit`, project-local axioms
  and unauthorized constants;
- **integrity:** checks artifact identifiers/digests and writes commit, tree,
  workflow blob, dependency, branch/archive and source-archive records;
- **freeze:** after the preceding gates succeed on the candidate branch,
  creates the archive with an absent-ref lease and verifies its exact head.

The candidate commit/tree, workflow run identifiers and artifact digests are
intentionally not embedded in the mathematical proof.  They are resolved by
the workflow and retained only in reproducibility artifacts.

## 7. Exact source boundary

The workflow allowlist is the complete diff from the accepted parent.  It is
limited to the P2A workflow; the new optimization package and P2A test
module; the focused Lean source plus additive aggregate/audit imports; the
main P2A proof, claim map, approach/prior-art/stage audits; and additive
updates to the six publication-program registries.  Any missing or extra
path, non-regular blob, non-UTF-8 text file, merge commit or dirty generated
file fails the release.

## 8. Limitations carried forward

P2A is a fixed finite-dimensional design theorem.  It does not guarantee
feasibility for arbitrary input data, provide a universal sparse support,
turn outer support selection into a convex problem, identify finitely many
rotations with a continuum supremum, or prove transport improvement.  It
does not formalize a generic conic duality library in Lean; the formal layer
covers the finite algebraic identities used to assemble and audit the
programs.  These exclusions are claim boundaries, not deferred lemmas needed
for the stated result.

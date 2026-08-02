# Prompt 2 corrective closeout audit

## Status before final integration

```text
closeout_branch=agent/afp-pure-math-p2-closeout-corrected
closeout_start_head=1835918fe9d0b941395e9f00f6ac5514129cefa0
reported_694b913_resolves=no
closeout_pr=19
final_target_head=PENDING_FINAL_INTEGRATION
final_target_tree=PENDING_FINAL_INTEGRATION
```

This document becomes authoritative only after the final target-head fields,
workflow runs, jobs, archive check, and review-thread resolutions are filled.

## 1. Provenance audit

| Check | Evidence | Result |
|---|---|---|
| Actual remote target resolved before editing | GitHub branch/commit inspection | PASS — `1835918fe9d0b941395e9f00f6ac5514129cefa0` |
| Original Prompt 2 merge is an ancestor of target | compare `f9fb1e...` to target | PASS — one intervening integration-record commit |
| Previously reported `694b913...` resolves | direct commit lookup | FAIL AS PROVENANCE — no such remote commit |
| Closeout branch created from actual target | GitHub branch creation | PASS |
| Target history rewritten | branch comparison | PASS — no force-push or rewrite used |
| Immutable archive unchanged | direct branch resolution and CI fetch | PASS at start — `515f1aae6c20bd85711c90b5c1c21b4905252d01` |
| Closeout diff contains transport-scope paths | workflow path audit | PASS only when result is empty; final run pending |

The failed provenance item is corrected rather than waived: `694b913...` is
removed from authoritative baseline use.

## 2. Revised Prompt 2 theorem matrix

| Revised mandatory item | Proof/source | Exact or formal check | Closeout result |
|---|---|---|---|
| Finite quadratic covariance identity | Theorem 1.1 | Lean covariance theorem; existing exact audit | PASS |
| Arbitrary shifted quadratic target | Theorem 1.2 | `quadratic_target_eigen_iff` | PASS |
| Trace-free form characterization | Theorem 2.1 | trace-free contraction | PASS |
| Sampling factorization `R_X=(L+2dI)S_X` | Theorem 2.2 | kernel/range Lean lemmas; exact matrices | PASS |
| Genuine sampled space and dimension | Theorem 2.2 | restricted rank-nullity; exact ranks | PASS |
| Positive axial rigidity | Theorems 3.1–3.2 | row-scaling Lean algebra; Platonic audit | PASS |
| Regular-simplex equality family | Corollary 3.3 | exact Gram and inverse sampling checks for `d=2,...,10` | PASS |
| Equivariant theorem states every off-diagonal rate nonnegative | Corrected Theorem 4.1 | line-by-line hypothesis audit | PASS |
| Equivariant theorem states unit sphere and eigenvalue `-(d-1)` | Corrected Theorem 4.1 | statement audit | PASS |
| Equivariant theorem separates conservation from off-diagonal rates | Corrected Theorem 4.1 | statement audit | PASS |
| Equivariant theorem avoids unused reversibility | Corrected Theorem 4.1 | proof audit | PASS |
| Positive distinct jump is used only after global nonnegativity | Corrected Theorem 4.1 proof | radial-covariance audit | PASS |
| Signed pentagon exact counterexample | Counterexample 4.2 | `Q(sqrt(5))` matrix, ranks, discriminant | PASS |
| Signed pentagon has `E_form=Sym_0(2)` | Counterexample 4.2 | residual rank zero | PASS |
| Signed pentagon has `dim E_sample=2` | Counterexample 4.2 | sampling rank two | PASS |
| Real `C_5` conjugation action irreducible | Counterexample 4.2 | negative characteristic discriminant | PASS |
| Existing Platonic classifications | Section 5.1 | exact determinants and ranks | PASS |
| Four-point signed restoration and forced `-1/2` | Section 5.2 | existing exact solve | PASS |
| Bilinear product identity | Theorem 6.1 | `jumpGenerator_product_identity_gamma` | PASS |
| General shifted product residual | Theorem 6.2 | `jumpGenerator_shifted_product_residual` | PASS |
| Arbitrary-target product iff | Theorem 6.2 | `shifted_product_target_iff` | PASS |
| Additive product resonance iff | Theorem 6.2 | `additive_product_resonance_iff` | PASS |
| Centered square resonance iff | Theorem 6.2 | `centered_square_resonance_iff` | PASS |
| Uncentered `c=0` corollary | Theorem 6.2 | two Lean theorems and exact assertion | PASS |
| Boolean centered-square counterexample | Counterexample 6.3 | exact four-state matrix and `Gamma=4` | PASS |
| Centered semigroup variance identity | Theorem 7.1 | exact Boolean exponential identity | PASS |
| Converse by differentiation at zero | Theorem 7.1 | finite matrix-exponential proof | PASS |
| Jensen inequality/equality support separated | Theorem 7.2 | variance/equality audit | PASS |
| Boolean example has positive variance, not Jensen equality | Theorem 7.2 | `2(1-exp(-4t))` exact formula | PASS |
| Spherical coordinate/doubled/H2 eigenvalues distinguished | Section 8 | exact arithmetic | PASS |
| Spherical covariance shift equals `2` | Section 8 | exact arithmetic | PASS |
| `S^2` `ell=1,...,6` table present | Section 8 | exact generated rows | PASS |
| No additive resonance in six `S^2` rows | Section 8 | integer assertions | PASS |
| Maximizer and equality-set warnings retained | Section 8 | adversarial text audit | PASS |
| Sampling-kernel and alias caveats retained | Section 8 | text and exact examples | PASS |
| Generalized Pell assertions retained | Section 9 | bounded hits and family prefix | PASS |
| Hierarchy verdict uses identifiability/alias kill criterion | Section 9 | claim-control audit | PASS |
| Universal centered-square impossibility rejected | claim matrix/register | Boolean regression | PASS |

## 3. CI and axiom-policy matrix

| Verification requirement | Implementation | Result before final merge |
|---|---|---|
| Literal expected head checkout | all three workflows | IMPLEMENTED; exact PR-head run pending final head |
| Start and final tree SHA recorded | dedicated and repository-wide workflows | IMPLEMENTED |
| Existing exact covariance audit | dedicated and repository-wide workflows | IMPLEMENTED |
| Corrective exact audit | `prompt2_closeout_audit.py` | LOCAL PASS; CI pending current exact head |
| Aggregate `sorry/admit/sorryAx` scan | dedicated, spherical, pure-math workflows | IMPLEMENTED |
| Aggregate singular `axiom` scan | anchored declaration regex | IMPLEMENTED |
| Aggregate plural `axioms` scan | same anchored regex | IMPLEMENTED |
| Deterministic singular/plural fixtures | dedicated workflow and exact audit | LOCAL PASS; CI pending |
| False-positive fixture (`#print axioms`) | dedicated workflow and exact audit | LOCAL PASS; CI pending |
| Full Lean 4.30 / Mathlib 4.30 build | all workflows | PENDING CURRENT EXACT HEAD |
| Focused axiom audit | dedicated and pure-math workflows | PENDING CURRENT EXACT HEAD |
| `sorryAx` absent from nanoda allow-list | dedicated and spherical workflows | PASS BY SOURCE INSPECTION |
| Independent nanoda Prompt 2 declarations | expanded dedicated declaration list | PENDING CURRENT EXACT HEAD |
| Independent Prompt 1 compatibility nanoda | spherical workflow | PENDING CURRENT EXACT HEAD |
| Immutable archive check | all three workflows | IMPLEMENTED; final run pending |
| Pure-math-only path check | dedicated and pure-math workflows | IMPLEMENTED; final run pending |

## 4. Independent proof and adversarial routes

A literal multiagent-v2 runtime was unavailable. The following independent
routes were maintained instead.

### Route A — corrected equivariant proof

1. Equivariance makes `E_form` a real invariant subspace.
2. Irreducibility makes it zero or all of `Sym_0(d)`.
3. The full alternative gives every `M_i=0`.
4. Trace `C_i=2(d-1)` then gives
   `C_i=2(I-Phi_iPhi_i^T)`.
5. Its radial contraction is zero.
6. Because every off-diagonal rate is nonnegative and at least one positive
   jump changes the embedded point, the exact radial sum is strictly positive.
7. Contradiction.

No line uses reversibility. Step 6 fails for signed generators, exactly as the
review reported.

### Route B — signed pentagon

The circulant Fourier eigenvalue for mode `r` is

```text
2u(cos(2pi r/5)-1)+2v(cos(4pi r/5)-1).
```

Exact substitution gives `-1` for `r=1` and `-4` for `r=2`. The two mode-2
real samples span `Sym_0(2)`. The conjugation rotation has negative real
characteristic discriminant. This independently falsifies the unsigned
statement.

### Route C — centered product algebra

Expanding `L(fg)` first, then inserting the two eigenvalue equations, gives the
arbitrary-target residual directly. Specializing `mu=lambda+nu` and then
`g=f` gives the centered product and square equivalences. The Lean proof and
symbolic-polynomial audit are independent implementations of the same algebra.

### Route D — Jensen adversary

The semigroup centered-resonance identity gives nonzero variance whenever
`c>0`, `lambda>0`, and `t>0`. Jensen equality requires zero variance and
constancy on support. The Boolean example has `c=2` and therefore cannot be a
Jensen equality case.

### Route E — workflow policy

The anchored declaration regex is applied to separate singular and plural
fixture files and to an allowed file containing `#print axioms` and an
identifier containing the substring `axiom`. Both forbidden declarations are
matched and the allowed file is not.

### Route F — claim-state audit

The three `GlobalLossRigidity.lean` theorems were inspected directly. The
abstract propagation theorem is now `PROVED / LEAN`; only spherical
specialization, restricted classification, and near-rigidity remain Prompt 3
targets.

## 5. Local exact command record

The environment used for repository writes had no authenticated networked
local clone and no `gh` executable. GitHub branch, PR, and workflow operations
therefore use the connected GitHub application. The exact corrective Python
audit was reconstructed and executed locally before publication:

```text
python prompt2_closeout_audit.py
```

Result:

```text
regular-simplex formulas: PASS (d=2,...,10)
signed regular-pentagon counterexample: PASS
centered product residual identities: PASS
Boolean centered-square resonance: PASS
S^2 low-degree product table: PASS (ell=1,...,6)
generalized Pell resonance audit: PASS
workflow axiom/axioms regex self-test: PASS
Prompt 2 corrective closeout audit: PASS
```

The full repository commands are executed in GitHub Actions on the literal
head because the local container lacks Lean and the repository checkout. Final
run/job identifiers and command results are inserted after integration.

## 6. Review findings

| Original review | Thread | Correcting source | Resolution condition | Current state |
|---|---|---|---|---|
| PR #17 equivariant positivity | `PRRT_kwDOQtWJBc6VsMzA` | corrected theorem plus signed pentagon | target source merged and final CI green | NOT YET RESOLVED |
| PR #18 plural `axioms` scan | `PRRT_kwDOQtWJBc6VsRku` | aggregate anchored scan plus fixtures | target workflow merged and final CI green | NOT YET RESOLVED |

## 7. Final acceptance fields

```text
closeout_implementation_commit=PENDING
closeout_merge_commit=PENDING
actual_final_target_commit=PENDING
actual_final_target_tree=PENDING
quadratic_run=PENDING
quadratic_job=PENDING
spherical_run=PENDING
spherical_job=PENDING
pure_math_run=PENDING
pure_math_job=PENDING
archive_final=515f1aae6c20bd85711c90b5c1c21b4905252d01_PENDING_RECHECK
```

Prompt 2 must not be called closed until every pending field is replaced and
both review threads are resolved after final-target CI.

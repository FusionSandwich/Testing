# Prompt 2 corrective closeout audit

## 1. Provenance resolution

```text
repository=FusionSandwich/Testing
target_branch=agent/afp-pure-math-p0-m1
closeout_start_head=1835918fe9d0b941395e9f00f6ac5514129cefa0
closeout_start_tree=2f6678b1589e2561f6fc2cb44785f3c4989424b1
reported_694b913_resolves=no
closeout_branch=agent/afp-pure-math-p2-closeout-corrected
closeout_pr=19
implementation_head=afb31139cacdf1bf252e86e890c4792a03df4796
implementation_tree=2414b6048e3c0d090152b7873b8ee52b5e40ea3c
closeout_merge_commit=dbe5d5db315d4e99b75c775c269827ac906b4fad
closeout_merge_tree=2414b6048e3c0d090152b7873b8ee52b5e40ea3c
immutable_archive=515f1aae6c20bd85711c90b5c1c21b4905252d01
```

The actual remote target at the beginning of the closeout was
`1835918fe9d0b941395e9f00f6ac5514129cefa0`, not the previously reported
`694b913c99364bb0032a8ffbd7008b549b491af0`. Direct commit lookup established
that `694b913...` did not exist remotely. The only target change after the
original Prompt 2 merge `f9fb1e336a4569c2d7e2e440821976bd30a6c29f`
was the integration-record commit `1835918...`.

The closeout branch was created from the actual target without rewriting
history. PR #19 was squash-merged as `dbe5d5db315d4e99b75c775c269827ac906b4fad`.
The merge tree equals the accepted implementation tree.

A documentation-only fast-forward record is finalized through PR #20. Its
literal final commit and tree are recorded in the PR #20 acceptance discussion
and the final closeout response. A Git commit cannot contain its own SHA or
tree hash without a self-referential hash fixed point; this committed audit
therefore records the accepted mathematical merge and delegates the final
metadata-head pointer to that immutable GitHub discussion.

## 2. Theorem-by-theorem revised Prompt 2 matrix

| Revised mandatory item | Authoritative source | Independent check | Result |
|---|---|---|---|
| Finite covariance identity | Theorem 1.1, `QuadraticCovariance.lean` | exact Platonic generator residuals | PASS |
| Arbitrary shifted quadratic target | Theorem 1.2, `quadratic_target_eigen_iff` | exact residual audit | PASS |
| Trace-free form characterization | Theorem 2.1 | exact constraint matrices | PASS |
| `R_X=(L+2dI)S_X` | Theorem 2.2 | exact matrix factorization | PASS |
| `K_X subset E_form` | Theorem 2.2, Lean kernel lemma | exact nullspace audit | PASS |
| `E_sample=im S_X intersect ker(L+2dI)` | Theorem 2.2, Lean range theorem | exact sampled ranks | PASS |
| `dim E_sample=rank S_X-rank R_X` | Theorem 2.2, restricted rank-nullity | exact ranks | PASS |
| Positive axial rigidity | Theorems 3.1–3.2 | Platonic row scaling | PASS |
| Regular-simplex sharp family | Corollary 3.3 | exact Gram and inverse sampling checks for `d=2,...,10` | PASS |
| Equivariant theorem requires all off-diagonal rates nonnegative | Corrected Theorem 4.1 | line-by-line proof audit | PASS |
| Unit-sphere and `L Phi=-(d-1)Phi` hypotheses explicit | Corrected Theorem 4.1 | statement audit | PASS |
| Conservation separated from off-diagonal positivity | Corrected Theorem 4.1 | statement audit | PASS |
| Reversibility not assumed | Corrected Theorem 4.1 | dependency audit | PASS |
| Positive distinct jump used only after global nonnegativity | Corrected Theorem 4.1 proof | radial-sum audit | PASS |
| Signed regular-pentagon counterexample | Counterexample 4.2 | exact `Q(sqrt(5))` matrix | PASS |
| Pentagon coordinate eigenvalue `-1` | Counterexample 4.2 | exact modes `cos theta`, `sin theta` | PASS |
| Pentagon quadratic eigenvalue `-4` | Counterexample 4.2 | exact modes `cos 2theta`, `sin 2theta` | PASS |
| Pentagon `E_form=Sym_0(2)` | Counterexample 4.2 | residual rank zero | PASS |
| Pentagon `dim E_sample=2` | Counterexample 4.2 | sampling rank two | PASS |
| Real `C_5` conjugation irreducible | Counterexample 4.2 | discriminant `(sqrt(5)-5)/2<0` | PASS |
| Five Platonic exact classifications | Section 5.1 | exact rational/`Q(sqrt(5))` determinants | PASS |
| Four-cardinal-point signed restoration | Section 5.2 | exact sampled rank | PASS |
| Forced antipodal rate `-1/2` | Section 5.2 | exact three-equation solve | PASS |
| Bilinear product identity | Theorem 6.1 | Lean and symbolic expansion | PASS |
| General shifted product residual | Theorem 6.2 | `jumpGenerator_shifted_product_residual` | PASS |
| Arbitrary target iff | Theorem 6.2 | `shifted_product_target_iff` | PASS |
| Additive product resonance iff | Theorem 6.2 | `additive_product_resonance_iff` | PASS |
| Centered square resonance iff | Theorem 6.2 | `centered_square_resonance_iff` | PASS |
| Uncentered `c=0` corollary | Theorem 6.2 | two Lean corollaries | PASS |
| Positive uncentered pointwise obstruction | Theorem 6.2 | Lean zero-value theorem | PASS |
| Boolean centered square | Counterexample 6.3 | exact four-state matrix | PASS |
| Boolean `Gamma(f)=4` | Counterexample 6.3 | direct exact sum | PASS |
| Centered semigroup variance identity | Theorem 7.1 | exact Boolean matrix-exponential identity | PASS |
| Converse by differentiation at zero | Theorem 7.1 | finite matrix-exponential proof | PASS |
| Jensen equality stated separately | Theorem 7.2 | strict-convexity/support audit | PASS |
| Boolean centered resonance has positive variance | Theorem 7.2 | `2(1-exp(-4t))>0` | PASS |
| Coordinate/doubled/H2 eigenvalues separated | Section 8 | exact arithmetic | PASS |
| Spherical target shift equals `2` | Section 8 | exact arithmetic | PASS |
| `S^2` table for `ell=1,...,6` present | Section 8 | generated integer rows | PASS |
| No additive resonance in those six rows | Section 8 | exact integer assertions | PASS |
| Odd/even maximizing-set warnings | Section 8 | adversarial text audit | PASS |
| Sampling-kernel and alias caveats | Sections 2 and 8 | Platonic aliases | PASS |
| Generalized Pell assertions retained | Section 9 | bounded hits and family prefix | PASS |
| Hierarchy verdict uses identifiability/alias kill criterion | Section 9 | claim-control audit | PASS |
| Universal centered-square impossibility rejected | claim matrix/register | Boolean regression | PASS |
| Abstract equal-rate/equal-loss propagation marked proved | `GlobalLossRigidity.lean` and claim controls | three Lean theorem declarations | PASS |
| Spherical `Q=1`, restricted triangulation, near-rigidity remain Prompt 3 work | handoff/register | scope audit | PASS |

## 3. CI and axiom-policy matrix

| Verification requirement | Implementation | Accepted result |
|---|---|---|
| Literal expected head checkout | all three workflows | PASS on implementation head and merge tree |
| Existing exact covariance audit | two workflows | PASS |
| Corrective exact audit | `prompt2_closeout_audit.py` | PASS |
| Regular-simplex exact assertions | corrective audit | PASS |
| Signed pentagon exact assertions | corrective audit | PASS |
| Centered/Boolean/semigroup assertions | corrective audit | PASS |
| `S^2` low-degree table | corrective audit | PASS |
| Aggregate `sorry/admit/sorryAx` scan | all three workflows | PASS |
| Aggregate singular `axiom` scan | anchored declaration regex | PASS |
| Aggregate plural `axioms` scan | anchored declaration regex | PASS |
| Singular/plural deterministic fixtures | dedicated workflow and audit | PASS |
| `#print axioms` false-positive fixture | dedicated workflow and audit | PASS |
| Full Lean 4.30 / Mathlib 4.30 build | all three workflows | PASS — 3,101 jobs |
| Focused axiom audit | dedicated and repository-wide workflows | PASS — only standard allowed axioms |
| `sorryAx` absent from nanoda allow-list | dedicated and spherical workflows | PASS |
| Independent Prompt 2 nanoda check | dedicated workflow | PASS |
| Independent Prompt 1 compatibility nanoda | spherical workflow | PASS — 13,252 declarations |
| Immutable archive check | all three workflows | PASS |
| Pure-math-only closeout path check | dedicated and repository-wide workflows | PASS |
| Source snapshot artifact | repository-wide workflow | PASS — SHA-256 recorded in job log |

## 4. Independent proof and adversarial routes

Literal multiagent-v2 was unavailable. No multiagent use is claimed. Six
separate written routes were maintained:

1. **Equivariant proof audit.** Irreducibility gives a zero/full dichotomy;
   the full case forces zero radial covariance. Strict positivity of the
   radial square sum follows only after global off-diagonal nonnegativity is
   stated. Reversibility is unused.
2. **Signed pentagon.** The circulant Fourier eigenvalue
   `2u(cos(2pi r/5)-1)+2v(cos(4pi r/5)-1)` gives exactly `-1` for mode one and
   `-4` for mode two. The negative characteristic discriminant independently
   verifies real irreducibility.
3. **Centered product derivation.** Direct product expansion, symbolic
   polynomial normalization, and Lean proofs independently obtain the same
   shifted residual and resonance equivalences.
4. **Jensen adversary.** Centered resonance has variance
   `c(1-exp(-2lambda t))`; Jensen equality requires zero variance. The Boolean
   example separates the statements exactly.
5. **Workflow policy.** Singular and plural declaration fixtures must match;
   `#print axioms` and identifiers containing `axiom` must not match.
6. **Claim-state audit.** The three `GlobalLossRigidity.lean` theorems prove
   the abstract propagation result. Only its spherical specialization and
   stronger Prompt 3 consequences remain open.

## 5. Command and workflow record

The local container had no authenticated networked checkout, `gh`, or Lean.
GitHub operations therefore used the connected GitHub application. The exact
corrective Python audit was reconstructed and executed locally:

```text
python prompt2_closeout_audit.py
```

with all seven audit groups passing.

The complete repository command suite was then executed in GitHub Actions on
the literal implementation head:

```text
python -m compileall -q pure_math
python pure_math/falsification/claim_falsification_audit.py
python pure_math/covariance/quadratic_covariance_audit.py
python pure_math/covariance/prompt2_closeout_audit.py
python pure_math/examples/exact_local_global_audit.py
python pure_math/tests/test_spherical_feasibility.py
lake build
lake env lean AFPBarrier/PureMathAxiomAudit.lean
aggregate placeholder scan
aggregate axiom|axioms scan
git diff --check
independent nanoda exports
archive and path-scope checks
```

### Initial failed attempt and repair

```text
run=30734096975
job=91459513522
result=FAIL at Lean build
cause=jumpGamma used real division in a computable definition
repair=mark jumpGamma noncomputable
```

All exact symbolic and regex checks had already passed in that attempt. The
subsequent exact implementation head passed every gate.

### Accepted implementation-head workflows

```text
AFP quadratic covariance
run=30734370610
job=91460293629
result=SUCCESS

AFP spherical feasibility
run=30734370649
job=91460293565
result=SUCCESS

AFP Pure Mathematics
run=30734370607
job=91460293589
result=SUCCESS
```

### Accepted post-merge repository-wide workflow

```text
commit=dbe5d5db315d4e99b75c775c269827ac906b4fad
tree=2414b6048e3c0d090152b7873b8ee52b5e40ea3c
workflow=AFP Pure Mathematics
run=30734539844
job=91460829310
result=SUCCESS
```

Final literal-head run IDs for all three workflows are recorded in the PR #20
acceptance discussion and final response after the documentation-only
fast-forward integration.

## 6. Review findings

| Original review | Thread | Correcting commits/source | Status before final fast-forward |
|---|---|---|---|
| PR #17 equivariant positivity | `PRRT_kwDOQtWJBc6VsMzA` | theorem correction `1244a794...`; signed audit `313e54c...` | ADDRESSED; resolve after final-head CI |
| PR #18 plural `axioms` scan | `PRRT_kwDOQtWJBc6VsRku` | workflow correction `3f22b705...` and subsequent aggregate policies | ADDRESSED; resolve after final-head CI |

The response comments are `3697974708` and `3697975086` respectively.

## 7. Final acceptance pointer

```text
accepted_mathematical_merge=dbe5d5db315d4e99b75c775c269827ac906b4fad
accepted_mathematical_tree=2414b6048e3c0d090152b7873b8ee52b5e40ea3c
final_target_ref=refs/heads/agent/afp-pure-math-p0-m1
final_metadata_head=PR_20_FAST_FORWARD_HEAD_RECORDED_IN_PR_DISCUSSION
archive_final=515f1aae6c20bd85711c90b5c1c21b4905252d01
```

Prompt 2 closure is certified only after PR #20's literal head passes all three
workflows, the target ref is fast-forwarded to that same SHA, and both old
review threads are resolved. Those final records are immutable in the PR #20
and PR #19 discussions and are repeated in the final return.

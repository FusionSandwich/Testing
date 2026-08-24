# AFP R7 source-of-truth and ancestry map

R7 parent: `da137c157dbc92774cbf7e378efb5bf360be6ceb`, the final R6 head on
`codex/afp-major-revision-r6-20260823`. The R6 scientific snapshot is
`648691e9225359d0983d71fa332408fc7bdbadd9`.

R6 in turn was created from `653d8945a5e91515f7a382ed42a8f4f51c0f0094`, the final R5 head on
`codex/afp-major-revision-r5-20260822`. Its scientific snapshot is
`9783a69e8f079d61c100bc87ea653ec9c981c2fe` and its candidate tag is
`afp-r5-internal-rc-20260822`.

The historical R5 worktree was created from the R4 audit base
`f0ec4a8e539ebf72f5324f92439b56545ea8d2c5`. Branch and
archive names are provenance labels only; the SHA is controlling. Every
`archive/*` pointer below is an ordinary mutable branch, not a tag or release.

## Canonical theorem lineage

| Stage | Branch tip | SHA | R4 ancestry | Disposition |
|---|---|---|---|---|
| P1A | `agent/afp-publication-p1a-quadratic-foundation-b40ee289` | `5ef6bf3335f72e38987df6b06e30d712de4b86c7` | ancestor; archive pointer identical | `CANONICAL_DEPENDENCY` |
| P1B | `agent/afp-publication-p1b-sharp-defect-bound-5ef6bf33` | `58b4fd93ea2bc95c4f1aee909a298e3a64a4d4fd` | ancestor; archive pointer identical | `CANONICAL_DEPENDENCY` |
| P1C | `agent/afp-publication-p1c-equality-geometry-58b4fd93` | `9ae0c8f16e8cd97cd84ef89b25064512a04b308a` | ancestor; archive pointer identical | `CANONICAL_DEPENDENCY` |
| P1D | `agent/afp-publication-p1d-quantitative-stability-9ae0c8f1` | `368e709c15efc1d1d25ad063d79ebbd8feecd9ed` | ancestor; archive pointer identical | `CANONICAL_DEPENDENCY` |
| P1E | `agent/afp-publication-p1e-asymptotic-family-368e709c` | `4e461c10f069cd7eb4614e7d52b886637dff134b` | ancestor; archive pointer identical | `CANONICAL_WITH_R5_CORRECTIONS` |
| P1F | `agent/afp-publication-p1f-flagship-paper-4e461c10` | `ab155b8e04bdf00306351b581739fb5feeb2979e` | ancestor; archive pointer identical | `SUPERSEDED_BY_R5_PURE_RELEASE` |
| P2A | `agent/afp-publication-p2a-convex-design-ab155b8e` | `07138547ff5c85df071e2067587dd83ca20b71b5` | ancestor; archive pointer identical | `NUMERICAL_PAPER_DEPENDENCY` |
| P2B | `agent/afp-publication-p2b-harmonic-transport-07138547` | `9b39b6ad52213197c0af75d4988eccd1a29d66a9` | ancestor; archive pointer identical | `NUMERICAL_PAPER_DEPENDENCY` |
| P2C | `agent/afp-publication-p2c-codesign-9b39b6ad-v2` | `b34c29b1b04f5293eaa4007b39d189efa03c51f5` | ancestor; archive pointer identical | `NUMERICAL_PAPER_DEPENDENCY` |
| P2D | `agent/afp-publication-p2d-completion-2fb7a11b` | `d46979d2aa52d502915eea2355a64cb788aae4f6` | ancestor; 18 commits behind R4 | `NUMERICAL_PAPER_DEPENDENCY` |
| P2E | `agent/afp-publication-p2e-heldout-execution-df6f0e28` | `e60f5c7d6bb6dd3cf7557d504716d7f13403dd72` | ancestor; 15 commits behind R4 | `CANONICAL_MIXED_NEGATIVE_EVIDENCE` |
| P2F integration | `agent/afp-consolidated-p2e-p2f-e60f5c7` | `b8912c282a22420e8077c75929b16c7a33d189b2` | ancestor; 7 commits behind R4 | `INCONCLUSIVE_ARCHIVE_ONLY` |
| hostile audit | `agent/afp-audit-major-revisions-b8912c2` | `d56db0ba8c24b63e56ec107e2f044449c726ce20` | ancestor; 3 commits behind R4 | `CANONICAL_AUDIT_DEPENDENCY` |
| R4 | `agent/afp-r4-formalization-release-20260819` | `f0ec4a8e539ebf72f5324f92439b56545ea8d2c5` | exact base | `AUTHORITATIVE_BASE` |
| R5 scientific content | `codex/afp-major-revision-r5-20260822` | `9783a69e8f079d61c100bc87ea653ec9c981c2fe` | direct R4 descendant | `CORRECTED_INTERNAL_RELEASE` |
| R5 final head | `codex/afp-major-revision-r5-20260822` | `653d8945a5e91515f7a382ed42a8f4f51c0f0094` | descendant of R5 scientific content | `HOSTILE_REVIEWED_MAJOR_REVISION` |
| R6 scientific content | `codex/afp-major-revision-r6-20260823` | `648691e9225359d0983d71fa332408fc7bdbadd9` | direct R5-final descendant | `SUPERSEDED_AFTER_INTERNAL_AI_MAJOR_REVISION` |
| R6 final head / R7 base | `codex/afp-major-revision-r6-20260823` | `da137c157dbc92774cbf7e378efb5bf360be6ceb` | descendant of R6 scientific content | `AUTHORITATIVE_R7_BASE` |
| R7 scientific content | `codex/afp-major-revision-r7-20260824` | `d77295e8de3da230626818698b20ffea6584be3b` | direct R6-final descendant | `INTERNAL_REPAIR_CANDIDATE_AWAITING_INDEPENDENT_HOSTILE_REVIEW` |

## Divergent and noncanonical lines

| Branch | Tip | Relationship to R4 | Disposition and reason |
|---|---|---|---|
| `agent/afp-post-audit-prompt-pack-b8912c2` | `332fddff7fc91f9cf9464acbb98ec2fa4eb8432a` | one prompt-only commit off `b8912c2`; not ancestor | `DEPENDENCY_PROMPT_ONLY`; no scientific promotion |
| `agent/afp-post-audit-repair-d56db0b` | `67ec2ec52099056ddea2357fc3e1c8ecdfc2315f` | two unique commits after merge base `d05c98e`; R4 has one unique snapshot commit | `CANDIDATE_NOT_INTEGRATED`; proposes fixed-level Proposition 7.3 but lacks an independent R5 admission audit of every production block-nonsingularity premise |
| `agent/afp-publication-p2c-completion-b34c29b1` | `cf05561dc1bb2d0e68127c416e2559155a1609bc` | 29 unique commits after merge base `b34c29b1`; not ancestor | `DIVERGENT_SUPERSEDED`; not silently merged into authoritative R4 |
| `agent/afp-publication-p2e-benchmark-development-b34c29b1` | `44e77e5b703255c66ecd1c9e9d5b68341bad050b` | three unique commits after `b34c29b1`; not ancestor | `DIVERGENT_DEVELOPMENT`; superseded by preregistered/held-out line |
| P2E preregistration | `df6f0e285cb176f183930815967e43c36166928a` | ancestor; archive pointer identical | `FROZEN_INPUT_DEPENDENCY`, not outcome evidence by itself |

## R6 and R7 hostile-review correction lineage

Commit `d13e795a2cd09594b20812c88312278227bb5513` first removed the
unsupported uniform robustness claim, narrowed the whole-paper Lean language,
and changed P2F from `BOUNDED_NEGATIVE` to
`INCONCLUSIVE_REFERENCE_NOT_CONVERGED`. R5 closes surviving prose and legacy
route leaks, makes the 512-declaration formal audit exhaustive, separates the
two-paper architecture, and archives P2F outside both papers.

The earlier adversarial review of R5 reported no counterexample to the core
finite-dimensional frontier, equality, or defect-budget results, but issued
**MAJOR REVISION** for two publication blockers. R6 reproduced those findings
and responded as follows:

1. former Corollary 6.3 is demoted to clearly non-theorem discussion;
2. Theorem 7.2 is restricted to the proved discrete sequence and supplied with
   a printed exact reduction, packaged exact-rational certificate, standalone
   verifier, and explicit non-Lean trusted boundary; and
3. P2F remains `INCONCLUSIVE_REFERENCE_NOT_CONVERGED`.

The renewed ChatGPT Pro review `Review Math Revision Branch` in project `Math`
then issued **MAJOR REVISION** for four further blockers: the false lower
cumulative-product exponent, the overbroad certificate claim, the missing
`gamma=Gamma/W` normalization, and the false frontier-excess wording. R7
repairs those four blockers. Both reviews are treated as internal AI
adversarial reviews, not identifiable external human peer review. Neither
repair record claims acceptance.

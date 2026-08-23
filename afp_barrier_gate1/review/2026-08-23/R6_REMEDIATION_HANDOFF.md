# AFP R6 remediation handoff

## Immutable parent state

- Repository: `FusionSandwich/Testing`
- R5 final binding commit: `653d8945a5e91515f7a382ed42a8f4f51c0f0094`
- R5 scientific snapshot: `9783a69e8f079d61c100bc87ea653ec9c981c2fe`
- Review branch: `review/afp-hostile-external-20260823`
- Canonical full report: `afp_barrier_gate1/review/AFP_HOSTILE_INDEPENDENT_REFEREE_REPORT_2026-08-23.md`
- Exact PDF page map and dated evidence: `afp_barrier_gate1/review/2026-08-23/REVIEW_MANIFEST.json`

R5 is immutable. A correction pass belongs on a new child branch and should record an exact claim-level diff against the scientific snapshot.

## Required R6 work

1. Rewrite Corollary 6.3 as complete quantified propositions or demote it to discussion; propagate the narrower stability language through the abstract, contribution list, theorem hierarchy, and conclusion.
2. Repackage Theorem 7.2 as either a self-contained supplemented proof or an explicitly computer-assisted theorem with a compact exact certificate, immutable hashes, a trusted-computing-base statement, and a small independent checker.
3. Add a theorem-by-theorem map of Lean declarations, ordinary proofs, exact certificates, external inputs, and open steps.
4. State and cite the classical convex-polyhedral theorem used in Corollary 5.5.
5. Replace overbroad rigidity, novelty, release-authority, and all-small-`h` wording.
6. Preserve the P2F, robustness, transport, material, HTS, publication, and identifiable-human-review firewalls.
7. Rebuild, re-run the exact and Lean checks, regenerate deterministic manifests, and commission a new review round.

## Allowed internal terminal states

- `R6_INTERNAL_REVIEW_CANDIDATE`
- `BLOCKED_BY_SPECIFIC_REVIEW_ITEM`

Neither state constitutes identifiable human peer review or journal acceptance.

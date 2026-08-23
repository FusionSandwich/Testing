# AFP R6 major-revision repair report

## Identity and disposition

- Worktree: `D:\math_lean_1\Testing-afp-major-revision-r6-20260823`
- Branch: `codex/afp-major-revision-r6-20260823`
- Exact R5 parent: `653d8945a5e91515f7a382ed42a8f4f51c0f0094`
- R5 scientific snapshot: `9783a69e8f079d61c100bc87ea653ec9c981c2fe`
- R6 scientific-content commit: `648691e9225359d0983d71fa332408fc7bdbadd9`
- R5 hostile review: **MAJOR REVISION**
- R6 disposition: internal repair candidate; external acceptance not claimed

The final branch-head commit cannot contain its own SHA; the pushed head is
Git metadata reported at handoff.

## Completed repair

1. Independently reproduced both hostile-review publication blockers.
2. Demoted former Corollary 6.3 to conditional, explicitly non-theorem
   discussion rather than inventing unproved global constants.
3. Made Theorem 7.2 auditable as a computer-assisted exact-rational result:
   printed the load-bearing reduction, packaged the certificate, added an
   independent verifier, disclosed its trusted boundary, and restricted the
   statement to the discrete levels actually proved.
4. Added a theorem-by-theorem formal/external/open map and reconciled the
   manuscript, theorem registry, Lean claim audit, evidence matrix, reviewer
   bundle, and proof source.
5. Preserved the support-perturbation result as Open problem 7.3 and P2F as
   `INCONCLUSIVE_REFERENCE_NOT_CONVERGED`.
6. Rebuilt and inspected the release without modifying the original dirty
   `Testing` checkout.

## Principal artifact hashes

| Artifact | SHA-256 |
|---|---|
| manuscript source | `e03f0c7275c004c3826a00f43c17d1254caf8c322f16df86b474b81b260bdb0f` |
| selected PDF | `413a1c210668f3d84894f6118a0b65f376cc4a3fcf95935fb47f7718defa44b7` |
| Theorem 7.2 certificate | `093acef16582ec6ca0039b4a7408fc265871bdc849eef383905bd92b591b86cd` |
| standalone verifier | `58f4b21f3b40f9a7df1e28c6c99c7218ccc801c3c91e8026e9824ca76c6f6290` |

## Validation summary

```text
Lean full build                              PASS (3118 jobs)
Lean declaration and axiom audit            PASS (512/512)
Exact mathematical and certificate audits   PASS (14 checks)
Standalone Theorem 7.2 verifier             PASS
Repository Python suites                     180 pass, 1 known deselection
P2F                                          PASS integrity; INCONCLUSIVE science
Manuscript/citation validation               PASS (13 records)
PDF build/render inspection                  PASS (25/25 pages)
Release structural validation                PASS
```

## Remaining gates

- Renewed independent specialist review of the frontier/equality chain and
  the computer-assisted Theorem 7.2 certificate boundary.
- Support-preserving perturbation robustness, between-scale extension, and
  matching positive local construction in `d>3` remain open.
- The analytic schedule/Cauchy proof, global geometric arguments, and article
  prose are not end-to-end Lean formalizations.
- The known floating threshold regression remains platform-sensitive and is
  recorded without weakening its frozen test.
- P2F has no physical-performance conclusion and requires a new
  operator-sensitive, converged preregistration.
- Journal administration, submission, and acceptance remain outside R6.

The appropriate next action is renewed hostile external review of the exact
R6 commit and reviewer bundle, not an internal acceptance claim.

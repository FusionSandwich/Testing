# R8 internal validation report

Date: 2026-08-24 EDT

Status: `INTERNAL_R8_REPAIR_CANDIDATE_AFTER_AI_MINOR_REVISION`

The independent Math-project review of exact R7 head
`e5d023e50ead92f9d87c7e625860225b4e6aa89b` returned **MINOR REVISION**.
It is an independent internal AI adversarial review, not identifiable external
human peer review.

## Three repairs verified

- Polar `a_0=4/3` is no longer aliased to the transition envelope, now named
  `alpha_m` and `alpha_*` throughout the canonical surface.
- The full pairwise-separation constant `1/(4M_0)` and half-separation packing
  radius `1/(8M_0)` are separately named in theorem, supplement, certificate,
  verifier, registry, and claim ledger.
- Certificate v3 renames `z_upper` to
  `z_squared_denominator_guard_upper`. Verifier claims are limited to finite
  rational recurrence budgets; the recurrence and telescoping proof remain
  ordinary mathematics.

## Independently reproduced R8 checks

- Pinned Lean build: `PASS`, 3,118 jobs.
- Fresh generated Lean execution: 58 modules, 512/512 signatures, 512/512
  axiom reports, no `sorryAx` or error; only `propext`, `Classical.choice`, and
  `Quot.sound`.
- Exact/symbolic/certificate aggregate: `PASS`, 14/14 checks.
- Certificate v3 verifier: `PASS`; 4/4 hostile mutations rejected.
- Full Python suite: `180 passed`, one frozen platform-sensitive failure, two
  warnings. Scoped suite: `180 passed, 1 deselected, 2 warnings` in 36.70 s.
- Fresh P2F audit: `PASS`, semantically identical to the canonical audit;
  scientific outcome remains `INCONCLUSIVE_REFERENCE_NOT_CONVERGED`.
- Manuscript/citations: `PASS`, 13 cited records with exact BibTeX equality.
- PDF: 26 letter pages, 352,550 bytes, no form, JavaScript, or encryption; all
  pages inspected, with changed pages 14--16 inspected at full resolution.

## Inherited evidence explicitly not relabeled fresh

- `LEAN_RELEASE_AUDIT.log` is the R7 captured 512-signature/axiom output. The
  fresh R8 command was independently rerun and summarized above rather than
  silently rewriting the inherited log.
- Frozen P2E/P2F source records and their checksum ledger are inherited; R8
  reran P2F integrity without changing its scientific classification.
- Unchanged theorem-core Lean sources and prior exact fixtures retain their
  historical provenance; the current build/audit executions are fresh.

These checks repair the three **MINOR REVISION** findings but do not create a
human-review, acceptance, merge, tag, or release claim.

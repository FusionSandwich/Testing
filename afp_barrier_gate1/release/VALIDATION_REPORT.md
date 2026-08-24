# R7 internal validation report

Date: 2026-08-24 EDT

Status: `INTERNAL_R7_REPAIR_CANDIDATE_AWAITING_INDEPENDENT_HOSTILE_REVIEW`

The triggering ChatGPT Pro review `Review Math Revision Branch` in project
`Math` ended **MAJOR REVISION**. It is an internal AI adversarial review, not
identifiable external human peer review, and R7 does not relabel R6 as passed.

## Repairs verified

- Theorem 7.2 uses a valid signed, second-order logarithmic estimate. The exact
  lower exponent is `513/M_0`; an exact `J=80` hostile instance rejects the old
  `512/M_0` lower exponent.
- The version-2 certificate verifier derives theorem-scale schedule sums,
  transition errors, cumulative-product bounds, positivity margins, geometry,
  `gamma=Gamma/W` normalization, rate floors, and final constants. It rejects
  three mutations and narrows its own trusted boundary.
- The P1E supplement and manuscript consistently distinguish preliminary and
  normalized conductances.
- The core frontier, equality chain, and weighted defect budget were
  independently rederived. The manuscript now describes an exact defect
  decomposition relative to the trace lower bound, not the full frontier
  excess.

## Checks

- Pinned Lean build: `PASS`, 3,118 jobs.
- Generated Lean audit: 58 modules, 512 declarations, 512 signatures, and 512
  axiom reports; only `propext`, `Classical.choice`, and `Quot.sound`; no
  `sorryAx`.
- Exact/symbolic/hostile/certificate aggregate: `PASS`, 14 checks.
- Independent Theorem 7.2 verifier: `PASS`; exact `Q` and `Q(sqrt(58))`
  arithmetic, no floating point or third-party imports, and 3/3 hostile
  mutations rejected. Certificate SHA-256:
  `ff8f1b13a64d8a4f0ca281853d689f5aaf86f22db74cb0c3e4f0c9fe118484cc`.
- Repository-owned Python suites: the full run produced the one frozen
  platform-sensitive failure; the scoped run produced `180 passed, 1
  deselected, 2 warnings` in 17.33 seconds.
- P2F integrity: `PASS`; scientific outcome remains
  `INCONCLUSIVE_REFERENCE_NOT_CONVERGED`.
- Manuscript source/citations: `PASS`, 13 cited records with exact BibTeX set
  equality.
- PDF: 26 letter pages, 352,024 bytes, no form, JavaScript, or encryption; no
  box-overflow warning; all 26 pages inspected in contact sheets and the
  changed load-bearing pages inspected at full resolution.
- Release structural validation: `PASS` with R7 markers and certificate-v2
  boundary checks.

These internal checks do not clear the **MAJOR REVISION** decision. R7 requires
a new independent, non-concurrent hostile review.

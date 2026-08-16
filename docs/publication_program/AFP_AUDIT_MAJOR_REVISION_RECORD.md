# AFP independent-audit major-revision record

## Base and purpose

This revision descends from consolidated candidate
`b8912c282a22420e8077c75929b16c7a33d189b2`. It implements the first
submission-blocking corrections identified by an independent mathematical,
computational, formalization, and reproducibility audit. It does not alter the
accepted algebraic frontier, equality, stability, P2A--P2D, or P2E raw held-out
evidence.

## Corrections implemented

1. **P1E robustness claim.** Proposition 7.3 is repaired as a fixed-level,
   fixed-support theorem. For every `M_0=2^80` production level the finite block system
   has an invertible base Jacobian and a strict positive conductance margin,
   giving a computable level-dependent radius. Reversibility, exact coordinate
   fidelity, connectivity, and conservative constants `1024` and `54` persist.
   The former uniform all-level majorant is rejected as uncertified.
2. **Formalization boundary.** The paper and release audit now state that Lean
   verifies a finite algebraic core, not the adaptive mesh theorem, analytic
   Cauchy enclosures, global recurrence, physical benchmarks, or the whole
   paper.
3. **P2F scientific classification.** The former `BOUNDED_NEGATIVE` label is
   withdrawn. The revised v2 record adds a 50/72/98/128-direction reference
   sweep, separates structural integrity from scientific interpretation, and
   classifies the experiment as
   `INCONCLUSIVE_REFERENCE_NOT_CONVERGED`.
4. **P2F operator sensitivity.** The audit now records the direct
   baseline/optimized response difference. Across the 18 selected comparisons,
   the maximum relative difference is approximately `1.94e-14`; three selected
   PKA comparisons are neutral-only by construction. The fixture therefore
   cannot test transfer of improved sampled degree-two fidelity.
5. **Release boundary.** Historical branch and workflow records remain
   provenance only. A future submission release requires an immutable tag,
   archived artifacts, exact environment records, and revised hashes.

## Evidence boundary

The P2F structural audit may pass even when the reference-convergence gate
fails. `PASS` means that schema, positivity, balance, physics separation,
record consistency, and classification logic are valid; it is not a statement
of physical improvement, degradation, or reference convergence.

## Remaining major-revision work

- complete the novelty and prior-art rewrite in the paper prose;
- split the pure-mathematics, numerical-method, and negative/inconclusive
  benchmark material into defensible publication units;
- broaden equal-work numerical validation beyond the present surrogate suite;
- create signed immutable release tags and DOI-backed preservation; and
- obtain an independent rerun of the revised exact-head workflow and artifacts.

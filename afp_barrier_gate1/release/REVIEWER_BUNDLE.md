# R6 hostile-review repair bundle

Status: `PREPARED_FOR_RENEWED_EXTERNAL_REVIEW`; no R6 acceptance is certified.

The completed hostile external review of R5 returned **MAJOR REVISION**. It
found no counterexample to the finite-dimensional frontier, equality, or
defect-budget theorems, but identified two publication blockers: former
Corollary 6.3 was not auditable as a theorem, and Theorem 7.2 did not expose an
independently checkable exact-rational certificate. R6 repairs those defects;
the response is internal until the external reviewer evaluates it.

## R6 blocker repairs submitted for review

1. Former Corollary 6.3 is demoted to an explicitly non-theorem discussion.
   The abstract now claims only the exact weighted defect decomposition and
   concentration consequence. The theorem hierarchy, source map, claim
   matrix, and validator reject any surviving `Corollary 6.3` label.
2. Theorem 7.2 is explicitly classified as
   `COMPUTER_ASSISTED_EXACT_RATIONAL`. The article prints the transition
   matrix, phase box, determinant/inverse/cone margins, Cauchy and Neumann
   guards, polar determinant/derivative bounds, recurrence, discrete scale
   sequence, and trusted computing base.
3. `release/certificates/theorem_7_2/certificate.json` binds the load-bearing
   sources and exact constants. `verify_certificate.py` independently checks
   the closure in `Q` and `Q(sqrt(58))` using only the Python standard library.
4. A main-text theorem-by-theorem map names exact Lean declarations and marks
   ordinary proof, computer-assisted certificate, external classical input,
   and open components. No whole-paper Lean claim is made.
5. Corollary 5.5 now cites the external convex regular-polyhedron
   classification. Novelty language is explicitly a focused-corpus
   positioning statement, not an exhaustive priority claim.
6. Every summary of Theorem 7.2 identifies the discrete sequence `h_J`; no
   every-sufficiently-small-`h` or between-scale robustness claim is made.

## Earlier internal repairs retained

1. The uniform/unrestricted P1E robustness Proposition 7.3 is not a theorem.
   It is Open problem 7.3; no radius or constants survive.
2. A stale flagship limitation calling it a proposition was corrected.
3. The legacy stratified-lattice note now labels its fixed-`eps` robustness
   assertion `FALSIFIED` and retains the hostile `O(eps)` obstruction.
4. Coxeter and structured-stress robustness sections are labeled conditional
   calculations on blocked/rejected routes.
5. Whole-paper Lean language was replaced by a precise finite-algebra boundary.
   R5 audits all 512 public theorem/lemma signatures and axiom dependencies.
6. The P4 formal map now states that Lean supplies only local scalar and
   conditional lower-bound algebra, not graph/minimax/attainment.
7. P2E remains mixed/negative evidence, with all five physical differences
   unresolved.
8. P2F remains `INCONCLUSIVE_REFERENCE_NOT_CONVERGED`; synthetic geometry is
   not called representative or physically validated.
9. P2F was removed from the two-paper release architecture and given a
   separately preregistered redesign gate.
10. Historical PR #51 `BOUNDED_NEGATIVE` files remain byte-for-byte provenance
    but now carry a local supersession warning.

## Requested specialist checks

### Pure mathematics

- Re-derive the quotient trace identity and constant `d(d-1)` independently.
- Check necessity and sufficiency in the equality chain, especially aliases,
  antipodal rows, and global shared-edge compatibility.
- Confirm that demoting former Corollary 6.3 removes every theorem-grade
  pointwise/graphwise/global-stability overclaim.
- Re-derive the exact `d=3` adaptive-ring Cauchy/recurrence proof and run the
  packaged verifier without importing the original audit modules.
- Decide whether the divergent fixed-level robustness candidate has a complete
  proof of every production diagonal-block nonsingularity premise; it is not
  in this release.

### Formal verification

- Re-run `ReleaseAxiomAudit.lean` on the pinned toolchain.
- Compare each manuscript use against the exact signature, especially global
  classification, compactness/attainment, and analytic construction steps.
- Confirm that Theorem 7.2 remains outside the Lean boundary and that the
  certificate classification is not described as Lean verification.

### Numerical and reproducibility

- Re-run all exact/symbolic audits and frozen tests in an independently built
  environment.
- Confirm P2E immutability and P2F's operator-insensitivity/reference failure.
- Do not interpret synthetic P2F fields as evaluated or device data.

### Prior art and publication

- Check source coverage, normalization transfers, and novelty wording against
  the primary papers.
- Author, affiliation, ORCID, funding, conflicts, data-license, repository DOI,
  and journal-format fields remain external administrative work.

## Stop conditions

Any failure of the sharp trace identity, equality sufficiency, unperturbed
adaptive-ring all-level proof, or deterministic release verification downgrades
the release to `BLOCKED_BY_SPECIFIC_MATHEMATICAL_GAP`. A numerical or physical
failure does not invalidate the pure frontier unless it falsifies a stated
finite construction premise; it does block the corresponding numerical claim.

Passing internal checks does not clear the R5 hostile review. Only a renewed
external report can change the external **MAJOR REVISION** disposition.

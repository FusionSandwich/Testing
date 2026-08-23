# R6 response to the hostile external review

External disposition being answered: **MAJOR REVISION**. R6 does not claim
that the reviewer has accepted this response.

## Publication blocker B1: former Corollary 6.3

**Review finding.** The numbered corollary mixed pointwise, edgewise,
graphwise, quotient, covariance, and frame consequences without complete
constants and hypotheses, so it was not auditable and exceeded the Lean
boundary.

**R6 action.** The numbered corollary has been deleted. Its replacement is
headed “Conditional transfers from the defect budget (discussion)” and says
explicitly that it is not a theorem. The abstract, contribution list, theorem
hierarchy, Appendix B map, pure-release statement, claim matrix, and structural
validator now identify only Theorem 6.1 and Corollary 6.2 as unconditional
stability results. The validator fails if the phrase `Corollary 6.3` returns.

**Resulting claim.** The manuscript proves an exact weighted decomposition of
frontier excess into radial and anisotropy defects and an explicit weighted
concentration consequence. It does not assert unconditional pointwise or
global embedding stability.

## Publication blocker B2: Theorem 7.2 certificate boundary

**Review finding.** The theorem was not independently checkable because the
printed proof omitted load-bearing transition, inverse, contraction, and guard
information, while the exact-rational computer-assisted dependency was not
adequately disclosed.

**R6 action.** Section 7.2 now prints:

- the normalized limiting `6 x 6` transition matrix and affine right-hand
  side in `Q(sqrt(58))`;
- the exact determinant, inverse norm, phase box, solution cone, Cauchy disk,
  denominator guards, and Neumann contraction;
- the polar-row determinant lower bound, inverse/derivative bounds, and finite
  displacement;
- the exact ordinary-row recurrence, telescoping error, transition error, and
  global shared-stress margins; and
- the discrete level sequence, computer-assisted classification, immutable
  artifact paths, and trusted computing base.

The new `release/certificates/theorem_7_2/certificate.json` SHA-256 binds the
ordinary proof source and every load-bearing derivation audit. The independent
`verify_certificate.py` imports only Python's standard library and verifies
source hashes, the limiting system and cone in `Q(sqrt(58))`, rational
Cauchy/Neumann and polar budgets, recurrence closure, and published constants.
It performs no floating-point computation and imports none of the original
construction/audit modules.

**Resulting claim.** Theorem 7.2 is a
`COMPUTER_ASSISTED_EXACT_RATIONAL` theorem conditional on the stated analytic
reduction and trusted computing base. It is not Lean-checked, perturbatively
robust, valid between the discrete scales, or extended to `d>3`.

## Other major-review items

- A main-text table gives one row per numbered result and names exact Lean
  declarations, ordinary proof, certificate, external input, and open scope.
- Corollary 5.5 cites Coxeter's classical convex regular-polyhedron
  classification and labels that final input external to Lean.
- Equality is described as a necessary-and-sufficient characterization of the
  equality equations, not uniqueness of a labelled embedding.
- Literature language is a focused-corpus positioning statement, not an
  exhaustive novelty or priority claim.
- Internal workflow terms such as “accepted” and “controlling registry” have
  been removed from the scientific article.
- Exact-rational certificates, Lean checks, floating diagnostics, and
  inconclusive P2F comparisons remain separately classified.

## P2F

P2F remains `INCONCLUSIVE_REFERENCE_NOT_CONVERGED`. R6 makes no convergence,
model-validation, physical-prediction, or HTS-performance claim from P2F.

## Requested renewed disposition

The requested next step is renewed independent review of the repaired
manuscript and certificate. The repository records no claim of external
acceptance, journal readiness, submission, or publication.

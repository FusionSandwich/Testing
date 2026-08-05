# Prose overclaim audit for the flagship manuscript

**Audited file:** `FLAGSHIP_MANUSCRIPT.md`

**Audit basis:** accepted P1A--P1E proof sources, the final independent
Cauchy/first-row hostile audit, `THEOREM_REGISTRY.md`, and the primary-source
comparison in `PRIORITY_AND_HOSTILE_REFEREE_AUDIT.md`.

## Verdict

**PASS WITH EXPLICIT DIMENSION AND ROBUSTNESS BOUNDARIES.** The manuscript now
states the matching construction as an accepted theorem in `d=2,3`, while the
frontier, equality, and stability hierarchy remains all-dimensional. It does
not claim a construction for `d>3`, generic node perturbations, transport
improvement, or a universal obstruction to signed high-order formulas.

This is a prose and theorem-boundary audit. It does not replace the underlying
ordinary proofs, exact audits, or eventual release workflow.

## Claim-by-claim audit

| Risk | Text checked | Judgment | Guard retained |
|---|---|---|---|
| Positive coordinate-exact spherical Laplacians presented as new | Abstract; Introduction 1.1--1.2; Appendix G | PASS | Izmestiev--Lam is credited for a local positive reversible coordinate-exact spherical operator; novelty is located in the sampled frontier/equality/stability package and the separately derived matching stress |
| Eigenpair preservation, positive stencils, designs, schemes, quadrature, or frames presented as new concepts | Introduction 1.2; Section 5; Appendix G | PASS | each established concept is attributed; the new claim is their precise role inside the globally reversible frontier theorem |
| `d=2` mesh parameter normalized inconsistently | Theorem 7.1; abstract; registries | PASS | `h=pi/N` is fill/separation, active edge angle is `2h`, `R_2=pi^2/8`, `C_2=4`, `c_2=16/pi^2` |
| `d=3` construction promoted from fitted slopes | Abstract; contribution list; Theorem 7.2; Appendices B--C | PASS | the proof uses literal symbolic row systems, rational Cauchy guards, exact recurrence and positivity margins; finite generator output is regression only |
| Construction generalized beyond proved dimensions | Abstract; hierarchy; Theorems 7.1--7.2; limitations | PASS | matching families are stated only for `d=2,3`; the all-dimensional scope is reserved for the lower frontier, equality and stability |
| Generic perturbation robustness inferred | Theorem 7.2; limitations | PASS | counts, phases, masks, horizontal jumps, pole/equator data and reflection are fixed; only latitude perturbations at the displayed scale and a common rotation are allowed |
| Local row feasibility treated as global reversibility | Theorems 5.3 and 7.2; rejected-claim table | PASS | P1C keeps detailed balance/Gram/cycle compatibility; P1E assigns one conductance per undirected edge and proves the global recurrence |
| Positivity assumed to survive correction | Section 7.2 | PASS | strict transition, ordinary, polar and global conductance margins precede normalization |
| Equality conflated with exact sampled `H_2` | Theorem 5.1; examples; rejected claims | PASS | frontier equality is `R_2=c_*S_2` with `c_*>0`; the sampled exact shell is zero |
| Sampling aliases discarded | Proposition 2.1; Theorem 7.2; Section 8; Appendix B | PASS | all residual norms use `K_X=ker S_2`; the construction has a row multiplier that descends without injectivity or a sampling-frame denominator |
| Unrestricted Platonic classification | Corollary 5.5; Section 8.3 | PASS | every graph, convexity, common-rate, nonantipodal and dimensional hypothesis remains visible |
| Weighted stability promoted to parameter-free rigidity | Corollaries 6.2--6.3; limitations | PASS | mass, edge-probability, graph, sampling, shell, tangent and feature-surjectivity parameters remain explicit |
| Signed higher-order formulas ruled out | Abstract; Remark 4.2; Section 9; Appendix G | PASS | the theorem is restricted to the nonnegative reversible coordinate-exact class, sampled degree two, and the maximum-rate constraint |
| Formalization scope overstated | Appendix D; formal release audit | PASS | Lean certifies finite stress/force/moment/rate/polygon identities, not the adaptive mesh or analytic Cauchy proof |
| Transport relevance or physical benefit inferred | Scope note; Section 10; limitations | PASS | no transport, cost, semigroup, or physical-response theorem is claimed |
| Priority inferred from project terminology | Title; Introduction 1.2; Appendix G | PASS | flagship language is terminology-independent and every related theorem has a variables/hypotheses/conclusion/transfer row |
| Workflow records embedded in mathematics | Sections 1--10 | PASS | operational status appears only in the reproducibility/stage material; no run ID, workflow count or commit hash enters a proof |

## Construction activation audit

All mathematical activation conditions are now met in the controlling sources:

- [x] explicit all-level `d=3` nodes, support and shared-conductance recursion;
- [x] uniform positivity, reversibility, locality, degree, window, fill and
      separation constants;
- [x] exact `L_h1=0` and `L_hOmega=-2Omega`;
- [x] rowwise `B_i=0` and sampling-safe scalar residual;
- [x] `R_3=64pi^2`, `C_3=75/2`, and P1B transfer
      `c_3=3/(32pi^2)`;
- [x] structured robustness stated at exactly the proved scale;
- [x] independent symbolic, Cauchy, first-row, recurrence, generator and
      hostile-mutation audits;
- [x] abstract, contribution list, dependency graph, source map, limitations
      and priority comparison updated together.

The separate release workflow and archive freeze have not been represented as
completed. That operational hold does not weaken the ordinary mathematical
theorem and must remain outside the theorem prose.

## Editorial disposition

The manuscript is safe for publication assembly with the present theorem
scope. Any later edit that changes the mesh parameter, `d=3` row multiplier,
rate constants, perturbation class, or all-dimensional language requires a new
normalization and overclaim audit.

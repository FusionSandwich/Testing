# P2F stage report

## Status

`COMPLETED_DIAGNOSTIC_WITH_INCONCLUSIVE_SCIENTIFIC_RESULT`.

The implementation, balance, positivity, provenance, and deterministic-record
gates pass.  The transfer interpretation has been revised after independent
adversarial analysis.

## Frozen outputs

- Layers: Cu / Ag / REBCO / oxide buffer / Hastelloy C-276 / Cu.
- Incidences: 0°, 60°, and 84°.
- Selected response comparisons: `18`.
- Resolved improvements: `0`.
- Resolved degradations: `0`.
- Resolved method differences: `0`.
- Maximum relative baseline/optimized response difference:
  `1.9424183391e-14`.
- 50/72/98/128 angular-reference convergence gate: failed in all three
  incidence cases.
- Scientific outcome: `INCONCLUSIVE_REFERENCE_NOT_CONVERGED`.

## Interpretation

The result does not demonstrate that optimized AFP improves or worsens HTS
responses.  The selected response map is effectively insensitive to the
operator replacement, and the angular reference hierarchy is not converged.
The former `BOUNDED_NEGATIVE` label is withdrawn.

## Publication boundary

The software and physics-firewall evidence may be retained in a reproducibility
appendix or negative-methods discussion.  The P2F experiment is not ready as a
standalone transfer-result paper.  A successor must be separately
preregistered and must use operator-sensitive responses and a converged or
independently validated reference.

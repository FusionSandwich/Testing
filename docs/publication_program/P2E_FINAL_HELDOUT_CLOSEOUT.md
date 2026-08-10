# P2E final held-out closeout

## Terminal status

P2E is `COMPLETED_NEGATIVE_RESULT`.  The one-time held-out execution is
preserved exactly; the preregistered operator, cases, partitions, thresholds,
and scientific result are unchanged.

The execution-integrity checks pass.  The preregistered value hypothesis
fails because the worst response-error ratio is `8.0684117565954`, above the
frozen maximum `1.8`.

## Corrected audit interpretation

| Item | Result |
|---|---:|
| Angular geometric-mean ratio | `0.6714625543` |
| Median response ratio | `0.9999999999999513` |
| Cases improved by at least 5% | `3/7` |
| Overall response-error geometric-mean ratio | `1.1261611503` |
| Physical-case geometric-mean ratio | `1.6597191251` |
| Worst response ratio | `8.0684117566` — failed |
| Acceleration iterations | optimized `17`; baseline `23` |
| Acceleration reduction | `26.0869565%` — passed the frozen `10%` minimum |
| Response comparisons resolved beyond reference uncertainty | `2/7`, both analytic |

For P2E-07, the optimized-minus-baseline absolute response-error difference is
`5.5282e-6`, while the fine-versus-medium reference uncertainty is
`1.8921e-5`.  Thus the formal ratio gate fails, but the physical difference is
not resolved at the declared reference accuracy.

The legacy `equal_wall_time` object is retained for schema compatibility.  It
means only that both one-shot executions finished within the larger measured
runtime.  It is not an experiment that reallocates work to a fixed time budget.

## Claim boundary

The strongest supported statement is:

> The optimized positive generator improves the frozen low-degree angular
> aggregate and the acceleration fixture, but the preregistered benchmark does
> not establish reliable physical-response improvement.  All five physical
> method differences are unresolved relative to their declared reference
> uncertainty.

This closeout forbids claims of evaluated-data performance, production-code
superiority, or improved HTS damage prediction.

The original workflow artifact is retained verbatim as a ZIP in the final Git
tree, including the original empty log file and `records.sha256`.  Extracted
JSON records are included for review and machine audit.

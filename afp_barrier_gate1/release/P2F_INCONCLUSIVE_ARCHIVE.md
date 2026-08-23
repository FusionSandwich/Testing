# P2F inconclusive archive and redesign specification

## Archived classification

`COMPUTATIONAL_INCONCLUSIVE_REFERENCE_NOT_CONVERGED`

The current finite fixture passes schema, positivity, balance, record, and
physics-firewall integrity checks. That `PASS` is not a scientific transfer
result. Across the 18 selected comparisons the maximum relative
baseline/optimized response difference is approximately `1.94e-14`, while the
50/72/98/128-direction reference sweep fails its declared convergence gate.
Three selected substrate-PKA comparisons are neutral-only by construction.

Consequently P2F supports none of the following: improved or degraded HTS
response, a validated coated-conductor model, damage or DPA prediction,
evaluated-data accuracy, or production transport performance. P2F belongs to
neither the pure theorem paper nor the numerical/design paper.

The R5 pinned rerun retained the same inconclusive classification but changed
ten floating fields by at most `4.056255e-16` and flipped two unresolved
direction/improvement booleans. The byte-level scientific hashes therefore do
not match across the selected and rerun records. This sensitivity is preserved
as negative evidence; it is not repaired by choosing one roundoff sign.

## Required successor design

A successor may be admitted only if it is separately preregistered and closes
all of these gates before interpreting a method difference:

1. **Operator sensitivity:** pre-screen response functionals on disjoint
   development cases and require a baseline/optimized difference materially
   above floating-point and solver tolerances. The held-out responses must be
   frozen afterward.
2. **Reference convergence:** use at least one independently implemented
   angular reference and demonstrate the declared convergence threshold for
   every load-bearing response, not only scalar totals.
3. **Matched comparison:** identical geometry, data, nodes or charged cost,
   spatial/energy discretization, stopping criteria, and response extraction.
4. **Physics separation:** neutral Boltzmann, charged BFP, PKA, heating, damage,
   and superconducting-property claims remain separate. Evaluated data and
   material/device inputs require external provenance and validation.
5. **Uncertainty:** resolve method differences against angular, spatial,
   energy, iteration, and model/reference uncertainty with a frozen rule.
6. **Independent rerun:** reproduce scientific JSON through a distinct code
   path and archive exact software, BLAS, input, and artifact hashes.

No theorem-release work depends on this redesign.

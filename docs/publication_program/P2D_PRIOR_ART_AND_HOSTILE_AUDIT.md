# P2D prior-art and hostile audit

## Prior-art transfer firewall

Morel and Pomraning motivate the angular Fokker–Planck approximation but do
not prove that any particular discrete low-order operator accelerates a
noncommuting transport solve.  Kuczek–Patel–Vasques establish modified FP
acceleration for their stated slab setting; their fixed-point mechanism and
kernel tests are precedent, not a transfer of convergence to the present
multidimensional generator.  The Bienvenue–Naceur–Carrier–Hébert monotone AFP
is the same-node baseline, not evidence that a new conductance design wins.

## Hostile checks

- A low `H_2` defect is not accepted as acceleration evidence without a solve.
- All preconditioned solutions are checked against the original high-order
  residual and exact dense solution.
- A conservation claim is rejected unless the correction map has `QP_L=0`
  and the initial state is compatible.
- FOV certificates expose their metric, coercivity, and operator-norm inputs.
- The higher-shell fixture forces the optimized `H_2` operator to lose its
  presumed advantage.
- Streaming and group coupling are noncommuting matrix blocks, not scalar
  shell decorations.
- The classical comparator is labelled a finite model comparator; it is not a
  reproduction of every published MFPA implementation.

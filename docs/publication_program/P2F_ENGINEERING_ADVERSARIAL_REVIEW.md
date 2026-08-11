# P2F adversarial engineering review

## Verdict

`ACCEPT_INTEGRITY_ONLY`; reject the former `BOUNDED_NEGATIVE` transfer claim
and reject any production HTS benefit or degradation claim.

## Thin layers

The 0.2–2 µm buffer/REBCO/Ag layers are represented explicitly.  The coarse
mesh uses one or two cells in each thin layer and the spatial diagnostic
doubles that resolution.  Integrated changes are recorded, but the model does
not resolve charged-particle track structure, interface roughness, epitaxial
texture, or nanoscale energy-loss physics.

## Grazing paths and finite width

The 84° case increases the streaming path and activates a 4 mm lateral-leakage
surrogate.  It is not the nonlocal grazing surface equation required for a
rigorous thin-interface limit and does not model tape edges, curvature, folds,
or cable contact.

The angular reference is not converged.  The 50/72/98/128-direction grazing
sequence alternates between low and high response branches.  For total
heating the values are approximately `1.02e-7`, `3.79e-3`, `4.05e-5`, and
`3.69e-3`; the relative span is essentially one.  The same failure occurs for
every selected grazing response.  A 72-versus-50 difference therefore cannot
be treated as a credible reference uncertainty.

## Nuclear-data dependence

All material coefficients and secondary yields are positive frozen
verification surrogates.  They exercise conservation, positivity, material
separation, and response plumbing.  They are not ENDF/TENDL/JEFF data and have
no covariance provenance.  Absolute heating, reaction, PKA, and escape values
are not engineering predictions.

## Neutral/charged separation

The neutral matrix is a full positive reversible Boltzmann kernel and is
identical between baseline and optimized runs.  AFP enters only the charged-
secondary BFP block.  The audit fails if this separation is removed.  This is
a valid implementation firewall.

Three of the 18 selected comparisons—the substrate PKA-source total in each
incidence—are neutral-only by construction.  They cannot carry information
about the AFP operator.  The remaining selected responses are also nearly
identical: the largest relative baseline/optimized response difference is
`1.9424183391e-14`.  The current fixture is therefore not operator-sensitive.

## Conservation and numerical integrity

The minimum flux is positive to the declared tolerance, the largest balance
residual is approximately `5.02e-15`, the PKA tensors are symmetric positive
semidefinite, and the same-run outputs are deterministic.  These facts support
software integrity; they do not repair reference nonconvergence or response
insensitivity.

## Required successor experiment

A transfer benchmark should not be rerun with post-hoc thresholds.  A new,
separately preregistered experiment must:

1. choose responses with demonstrated first-order sensitivity to the angular
   generator while keeping the neutral physics fixed;
2. use a rotated/averaged or adaptively refined angular reference that passes a
   declared convergence gate, or compare against an independent production
   method;
3. separate neutral-only, charged-sensitive, and mixed responses;
4. compare equal work or equal accuracy rather than only common completion;
5. classify resolved improvement, resolved degradation, mixed response, and
   unresolved outcomes separately; and
6. retain the surrogate/engineering boundary unless evaluated data and an
   independently validated damage model are introduced.

## Final classification

The committed calculation is a useful structural and reproducibility
diagnostic.  Its scientific transfer result is **inconclusive**, not bounded
negative.

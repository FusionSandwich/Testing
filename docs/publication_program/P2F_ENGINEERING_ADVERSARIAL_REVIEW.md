# P2F adversarial engineering review

## Verdict

`ACCEPT_INTEGRITY_AND_BOUNDED_NEGATIVE_CLAIM`; reject any claim of production
HTS benefit.

## Thin layers

The 0.2–2 µm buffer/REBCO/Ag layers are represented explicitly.  The coarse
mesh uses one or two cells in each thin layer and the reference doubles that
resolution.  Integrated response differences are included in the spatial
uncertainty.  The calculation does not resolve charged-particle track
structure, interface roughness, epitaxial texture, or nanoscale energy-loss
physics.

## Grazing paths and finite width

The 84° case increases the streaming path and activates a 4 mm lateral-leakage
surrogate.  This detects sensitivity to a grazing-like geometry, but it is not
the nonlocal grazing surface equation required for rigorous thin-interface
limits, and it does not model tape edges, curvature, folds, or cable contact.
Those belong to the separate mixed-dimensional transport program.

## Nuclear-data dependence

All material coefficients and secondary yields are positive frozen
verification surrogates.  They exercise conservation, positivity, material
separation, and response plumbing.  They are not ENDF/TENDL/JEFF data and have
no covariance provenance.  Consequently absolute heating, reaction, PKA, and
escape values are not engineering predictions.

## Neutral/charged separation

The neutral matrix is a full positive reversible Boltzmann kernel and is
bitwise identical between baseline and optimized runs.  AFP enters only the
charged-secondary BFP block.  The audit fails if this separation is removed.
This closes the main physical-overreach risk.

## Ray effects and angular convergence

The production comparison uses the frozen 32-node rule.  Independent 50- and
72-direction references are used, but they remain structured product rules.
The conservative uncertainty is larger than every observed method advantage.
No ray-effect cancellation or asymptotic angular convergence rate is claimed.

## Spatial convergence

The declared uncertainty separates angular and two-level spatial components.
Two-level change is not an all-orders convergence proof.  The result is valid
as a bounded finite study only.

## Damage and superconducting-property firewall

The PKA tensor is a directional reaction-source descriptor.  It cannot be
mapped directly to DPA, defect survival, oxygen disorder, pinning, \(J_c\),
\(T_c\), or magnet performance.  Such a map requires evaluated recoil data,
atomistic/mesoscale damage evolution, temperature history, and experimental
calibration.

## Cost and value

P2E shows a valid 26.1% iteration reduction in one frozen acceleration fixture,
but its physical response hypothesis fails.  P2F shows zero resolved response
improvements out of 18 comparisons.  The defensible publication claim is a
negative transfer result plus a verified separation architecture, not an HTS
accuracy or cost advantage.

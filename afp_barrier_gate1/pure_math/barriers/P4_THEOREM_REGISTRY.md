# Prompt 4 theorem registry

The immutable dependency is Prompt-3 closeout
`8de4b94835137d1eaf32c14b626424f87d2e176d`.  `ACTIVE` below is a work state,
not a mathematical claim status.  Final publication claims receive exactly
one of `PROVED`, `EXTERNAL`, `COMPUTATIONAL`, `CONJECTURE`, or `REJECTED`.

| ID | Mandatory statement family | Work state | Intended final status | Ordinary proof | Lean / exact boundary |
|---|---|---|---|---|---|
| P4.1 | controlled `csc^2` expansion and explicit positive tail | PROVED | PROVED | sharp-barrier theorem §1 | finite coefficient algebra / exact audit |
| P4.2 | uniform polar rate and quality remainders and asymptotics | PROVED | PROVED | sharp-barrier theorem §1 | polar identities / exact audit |
| P4.3 | asymmetric polar-row uniqueness | PROVED | PROVED | sharp-barrier theorem §2 | `squarePolar_rates_forced` family |
| P4.4 | fixed unreduced product-graph minimax and quartic constants | PROVED | PROVED | sharp-barrier theorem §2 | forced total rate and quartic lower bound |
| P4.5 | universal rate barrier and exact quasi-uniform transfer | PROVED | PROVED | sharp-barrier theorem §3 | universal finite inequality |
| P4.6 | constrained extremal lower bound, compact minimizer, product exclusion | PROVED | PROVED | sharp-barrier theorem §4 | finite lower bound; compactness stays ordinary |
| P4.7 | feasible-family projective quality and variance identity | PROVED | PROVED | sharp-barrier theorem §5 | corrected arbitrary-moment algebra |
| P4.8 | sliced LP, dual certificate, equality characterization | PROVED | PROVED | sharp-barrier theorem §5; finite LP strong duality is separately EXTERNAL | exact finite certificate regression |
| P4.9 | weighted opposed-ray and polar-family anisotropy formulas | PROVED | PROVED | sharp-barrier theorem §5 | general `kappa` plus equal-weight corollary |
| P4.10 | biregular incidence and perfect-matching obstruction | PROVED | PROVED | sharp-barrier theorem §6 | incidence declarations |
| P4.11 | Delsarte route produces no new certificate | BLOCKED | REJECTED | approach registry | sampling audit boundary |
| P4.12 | blanket positive-graph curvature collapse | REJECTED | REJECTED | counterexample boundary | no false declaration |
| P4.13 | positive Delaunay/maximal-net existence and exact modes | BLOCKED | EXTERNAL | assumptions table | no project axiom |
| P4.14 | source-pinned finite regressions and Plantri census | PROVED | COMPUTATIONAL | not a general proof | exact CI only |
| P4.15 | final P1--P4 theorem hierarchy and numerical handoff | PROVED | PROVED | final synthesis | maps and claim controls |

No theorem is accepted from the old snapshot merely because it appeared in a
previously green workflow.  Each family is re-audited on the current API.

## Checkpoint resolution

P4.1--P4.10 and P4.15 have accepted ordinary proofs and independent
exact/adversarial audits in `SHARP_PRODUCT_GRAPH_BARRIERS.md` and the final
synthesis.  Their declarations and regressions are bound by the dedicated
current-API exact-head workflow; `PROVED` is the final registry state certified
by the resolved workflow artifact.

The feasible-cone audit found three literal boundary defects in the old
wording that must not be propagated: the fixed-`lambda` feasible set is an
affine slice rather than a cone modulo scaling; the scale-invariant quality is
`Q_lambda = r*epsilon/lambda^2` (equal to the global `Q` when `lambda=2`);
and the minimization theorem requires a nonempty tangent-balanced polytope.
The minimal corrected formulation is registered for P4.7--P4.9 and will be
used in the port.  The mandatory equal-weight two-direction formula is retained
only under its stated hypothesis that the unique balanced probability is
`(1/2,1/2)`.

The old downstream shorthand “two opposite tangent directions” is
`REJECTED` without an equal-magnitude or explicit half-weight hypothesis. A
literal spherical counterexample has colatitudes `pi/6` and `pi/2` on
opposite tangent rays, forcing weights `(2/3,1/3)`. The accepted stronger
formula for `v_2=-kappa v_1` is
`kappa*(ell_1-ell_2)^2/(kappa*ell_1+ell_2)^2`; the mandatory displayed formula
is its `kappa=1` corollary.

# R8 response to the independent Math-project review

## Review identity and disposition

The independent Math-project review examined exact clean R7 head
`e5d023e50ead92f9d87c7e625860225b4e6aa89b` and returned **MINOR
REVISION**. It is treated as an independent internal AI adversarial review,
not identifiable external human peer review. R8 repairs exactly its three
remaining notation and certificate-scope findings. It does not change theorem
scope, claim acceptance, merge, tag, release, or revive any global-stability or
physical claim.

## Finding 1 - transition envelope versus polar latitude

### Review line

The symbol `a_0` already denotes the polar latitude `4/3`, but the R7
transition-product paragraph also wrote `a_*=a_0=256/M_0`.

### R8 repair

The polar schedule retains `a_0=4/3` exclusively. The transition-error
envelope is now

`alpha_m=256/M_m`, `alpha_*=256/M_0`, and
`|epsilon_m|<alpha_m`.

The signed logarithmic estimate, geometric sums, level-80 hostile instance,
manuscript, supplement, exact proof audit, verifier variables, and historical
R7 response all use `alpha`. No mathematical constant changes.

## Finding 2 - full separation versus packing radius

### Review line

The supplement used the full pairwise-separation constant `1/(4M_0)`, while
the theorem displayed `1/(8M_0)` as if it were that same constant. The latter
is the half-separation radius of the disjoint packing balls.

### R8 repair

R8 distinguishes

`q_sep^*=1/(4M_0)` and
`q_pack^*=q_sep^*/2=1/(8M_0)`.

Theorem 7.2 now states `q_sep(X_h)>=q_sep^* h` and uses `q_sep^*` in the mesh
ratio. The supplement keeps its historical `q_*` notation but explicitly
identifies it as the full pairwise constant and names
`q_pack^*=q_*/2` as the packing radius. Its node count is therefore

`N_h<=4 pi^2 (q_sep^*)^-2 h^-2 = pi^2 (q_pack^*)^-2 h^-2`,

and the normalized weight floor continues to use the full pairwise constant.
Certificate v3 records both exact rationals in separately named fields; the
verifier checks their factor-two relation and rejects a mutation that
conflates them.

## Finding 3 - denominator guard and recurrence scope

### Review line

Certificate field `z_upper=1/16` was not an upper bound for `z`; it was the
bound on `z^2` used in `1-4z^2`. Statements that the verifier checked
“recurrence closure” also exceeded its finite scalar budget.

### R8 repair

Certificate v3 renames the field to
`z_squared_denominator_guard_upper` and the enclosing object to
`ordinary_rows_finite_rational_budgets`. The verifier now names the value
`z_squared_guard` and checks exactly

`16/(1-4 z_squared_guard)<22` with `z_squared_guard=1/16`.

Every claim that the verifier checks “recurrence closure” is replaced by the
accurate statement that it checks finite rational recurrence budgets. The
ordinary shared-edge recurrence and telescoping identity are explicitly
outside the verifier and remain ordinary proofs in the manuscript and
supplement. Scalar literals are not described as a recurrence proof.

## Preserved boundaries

- Theorem 7.2 remains a computer-assisted exact-rational theorem only on the
  discrete sequence `h_J`, `J>=1`; it is not wholly machine-verified or
  end-to-end Lean-checked.
- Support-preserving perturbation robustness, between-scale extension, and
  matching `d>3` constructions remain open.
- P2F remains `INCONCLUSIVE_REFERENCE_NOT_CONVERGED` and carries no physical,
  HTS, device, convergence, or performance conclusion.
- R8 is a repair candidate for later review, not acceptance or publication.

# Pure theorem release statement

## Classification

The frontier, equality equations, and defect budget relative to the trace
lower bound are proved by ordinary
finite mathematics, with the stated finite algebraic components Lean-checked.
Theorem 7.2 is a computer-assisted exact-rational theorem: its analytic
reduction is ordinary mathematics and its remaining finite rational closure is
packaged with an independent verifier. The complete paper is not formalized.
This is an internal repair candidate after the independent Math-project AI
review of exact R7 head `e5d023e50ead92f9d87c7e625860225b4e6aa89b`
returned **MINOR REVISION**. It awaits a later independent human specialist
review and does not claim human peer review or acceptance.

## Sharp positive-reversible generator frontier

Let `I` be a nonempty finite set, let `d >= 2`, choose nodes
`Omega_i in S^{d-1}`, positive masses `w_i` with sum one, and symmetric
conductances `gamma_ij = gamma_ji >= 0` with zero diagonal. Define

`a_ij = gamma_ij / w_i`,
`(L f)_i = sum_{j != i} a_ij (f_j-f_i)`, and
`r_max = max_i sum_j a_ij`.

Assume exact coordinate reproduction

`L 1 = 0` and `L Omega = -(d-1) Omega`.

For trace-free symmetric matrices `A`, let

`(S_2 A)_i = Omega_i^T A Omega_i`,
`R_2 = (L + 2 d I) S_2`, and

`D_2 = sup_{A notin ker S_2} ||R_2 A||_{l2(w)} / ||S_2 A||_{l2(w)}`.

Then

`D_2 r_max >= d(d-1)`.

The constant is sharp for every `d >= 2`. The quotient by `ker S_2` is part
of the theorem; no sampling-injectivity or sampled-space invariance assumption
is hidden. The lower frontier itself does not require connectedness, equal
masses, or a mesh limit.

## Equality and stability

Equality is equivalent to the simultaneous vanishing of the nonnegative
rate, loss-variance, and anisotropy budgets stated in Theorem 5.1 of the
flagship manuscript. In the nonantipodal one-shell branch this yields centered
weighted unit-norm tight frames in each tangent space. Reversibility adds
global shared-edge compatibility; local frames alone do not classify a global
embedding. The strongest unconditional near-extremizer statements are the
exact weighted defect budget relative to the trace lower bound and the
exceptional-mass consequence in Theorem 6.1
and Corollary 6.2. The former Corollary 6.3 has been demoted to non-theorem
discussion: no pointwise, graphwise, quotient, frame-repair, or global
embedding-stability theorem is asserted without complete additional
hypotheses and constants.

## Sharpness and constructions

- `PROVED`: regular-simplex, cross-polytope, and hypercube exact extremizers in
  every dimension under the stated sampling conventions.
- `PROVED`: regular-polygon matching family for ambient `d=2`.
- `COMPUTER_ASSISTED_EXACT_RATIONAL`: fixed unperturbed reflected adaptive-ring
  matching family for ambient `d=3`, along the explicit discrete sequence
  `h_J = pi/(2 S_J)`, `J>=1`, with `r_max <= 64 pi^2 h_J^-2` and
  `D_2 <= 75 h_J^2 / 2`, full pairwise separation `h_J/(4M_0)`, and
  packing-ball radius `h_J/(8M_0)`. The v3 exact-rational closure certificate
  and standalone verifier are in `release/certificates/theorem_7_2/`; they
  check finite rational recurrence budgets, not the ordinary recurrence and
  telescoping proof.
- `OPEN`: support-preserving perturbation robustness. No radius or constants
  are release claims.
- `OPEN`: a matching positive local family for `d > 3`.

The divergent repair branch's proposed fixed-level robustness statement is
preserved in the lineage map as an unadmitted candidate. It was not merged
merely because a theorem file and passing finite scripts exist; its production
block-nonsingularity chain requires a separate proof audit.

## Exclusions

This theorem is not a quadrature exactness theorem, a universal obstruction to
signed high-order graph Laplacians, a transport-performance theorem, a
material model, or an HTS irradiation result. P2A--P2F do not enter its proof.

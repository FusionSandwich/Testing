# Pure theorem release statement

## Classification

`PROVED` by ordinary finite mathematics, with a `PROVED` Lean-checked finite
algebraic core. The complete paper is not formalized. The release is an
internal candidate awaiting independent specialist review.

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
embedding. The quantitative stability theorem is weighted and retains every
mass floor, active-edge probability, connectivity, spectral-gap, sampling,
and tangent-frame conditioning parameter needed for pointwise or global
conclusions.

## Sharpness and constructions

- `PROVED`: regular-simplex, cross-polytope, and hypercube exact extremizers in
  every dimension under the stated sampling conventions.
- `PROVED`: regular-polygon matching family for ambient `d=2`.
- `PROVED`: fixed unperturbed reflected adaptive-ring matching family for
  ambient `d=3`, with `r_max <= 64 pi^2 h^-2` and
  `D_2 <= 75 h^2 / 2`.
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

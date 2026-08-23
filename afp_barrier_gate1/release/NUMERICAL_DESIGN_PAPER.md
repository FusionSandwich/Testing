# Positive reversible angular generators: certified finite design and mixed benchmark evidence

Status: `INTERNAL_NUMERICAL_DESIGN_DRAFT_AWAITING_EXTERNAL_REVIEW`

## Abstract

We study finite convex design of positive reversible angular generators after
the node set, masses, support, exact coordinate module, rate cap, and sampled
quadratic metric are fixed. The design problem admits explicit finite
primal/dual and infeasibility certificates, alias-correct shell objectives,
and exact rechecks of generated conductances. Harmonic semigroup, resolvent,
six-channel transport-residual, and selected acceleration bounds are proved
under their stated finite or analytic hypotheses. Co-design and acceleration
experiments show useful finite cases but do not establish universal
convergence or transport superiority. In the preregistered P2E hierarchy, the
optimized operator improves the frozen angular geometric mean and one
preconditioned iteration count, while the preregistered physical-response
hypothesis fails and all five physical method differences remain unresolved
relative to reference uncertainty. We therefore report mixed/negative
computational evidence, not a transport-improvement theorem.

## 1. Fixed design problem

P2A optimizes shared conductances on a fixed `(X,w,E)`. Positivity,
reversibility, constants, the coordinate target, each deflated sampled shell,
and the rate cap are explicit constraints. Sampling kernels are removed from
the domain but full output leakage is retained. Solver termination is not a
certificate: every retained finite result must be checked on the original
scale by a primal residual plus a dual/complementarity or Farkas witness.

## 2. Error interpretation

P2B converts a declared sampled harmonic residual into transient and resolvent
bounds for a reversible nonpositive generator. Physical weighted norms require
an explicit symmetrizer/dissipativity condition or a stated norm-equivalence
factor. The transport comparison retains six distinct channels: physical
model, angular generator, sampling/averaging, space/boundary, energy/group,
and algebraic/iteration error. No single `D_2` value controls a physical
response without observability, stability, and the remaining channels.

## 3. Co-design and acceleration

P2C provides finite co-design algorithms and exact regression fixtures. It is
an implemented method, not a proof of continuum convergence, rotational
robustness, or global optimality. P2D proves finite scalar/energy bounds under
declared symmetry, coercivity, or field-of-values hypotheses and records
selected iteration reductions. Higher-shell and streaming adversaries prevent
an unconditional acceleration theorem.

## 4. P2E preregistered outcome

The frozen held-out execution is immutable evidence. The optimized generator
reduces the frozen angular-error geometric mean to `0.671` of baseline and one
preconditioned solve from `23` to `17` iterations. The worst response-error
ratio is `8.06841`, so the preregistered no-worst-degradation hypothesis fails.
The apparent HTS degradation is not physically resolved: its method-error
difference is smaller than the declared independent reference change. Only
two analytic comparisons distinguish the methods beyond reference
uncertainty; all five physical comparisons are unresolved.

Classification: `COMPUTATIONAL_MIXED_NEGATIVE`. This result does not prove
improvement, degradation, or equivalence on a physical transport problem.

## 5. Reproducibility and limitations

The finite algorithms, frozen operators, manifests, exact algebraic fixtures,
and tests are retained in the repository. Runtime records are single
executions, not an equal-wall-time performance study. No evaluated nuclear
data, manufacturer geometry, production transport solve, or externally
validated response enters the release.

P2F is intentionally excluded from this paper. Its surrogate integrity record
and exact redesign gate are archived separately because its response map is
operator-insensitive and its reference hierarchy is unconverged.

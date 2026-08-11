# Rejected claim record: former uniform support-preserving robustness statement

## Classification

**HISTORICAL / REJECTED CLAIM — NOT AN ACCEPTED THEOREM.**

This record is the only publication-program document that retains the former
universal statement and its constants. It is preserved to make the correction
auditable and to prevent the statement from silently re-entering accepted
sources.

## Provenance of the rejected statement

| Record | Exact value |
|---|---|
| repository | `FusionSandwich/Testing` |
| live PR resolved for the repair | `51` |
| authoritative parent commit | `b8912c282a22420e8077c75929b16c7a33d189b2` |
| authoritative parent tree | `4c2175463a661ce3f2bb206f0cb7b5038183b2ab` |
| former manuscript location | Proposition 7.3 in `FLAGSHIP_MANUSCRIPT.md` |
| former construction location | Section 10 of `P1E_SHORT_GAP_S2_CONSTRUCTION.md` |
| replacement | `P1E_FIXED_LEVEL_LOCAL_PERSISTENCE.md` |

## Former statement

The rejected statement introduced

\[
 K_*=2^{28\cdot2^{10^6}}
\]

and claimed that, at every refinement level, every reflected
support-preserving latitude perturbation of size at most `h^3/K_*` could be
re-solved while preserving positive conductances, exact reproduction, and the
uniform bounds

\[
 r_{\max}\le \mathsf R_{\rm rob}h^{-2},
 \qquad
 \mathfrak D_2\le C_{\rm rob}h^2,
 \qquad
 \mathsf R_{\rm rob}=256\pi^2,
 \qquad
 C_{\rm rob}=54.
\]

No part of the preceding paragraph is an accepted result in the corrected
repository.

## Why the statement was rejected

The purported proof referred to a cancellation-free differentiated
straight-line program with at most `10^6` operations. The repository did not
contain the objects required to turn that description into a universal
certificate:

1. no complete expression DAG for the ordinary, transition, polar, and
   equatorial solves;
2. no generator-derived operation count;
3. no list of every analytic or divided-difference atom and its domain;
4. no interval or exact-rational enclosure for every intermediate expression;
5. no explicit lower bound for every reciprocal denominator;
6. no determinant or inverse-norm ledger for every perturbed local system;
7. no conductance-margin ledger propagated through the global recurrence;
8. no proof that the perturbation estimate is uniform in the level;
9. no independent verifier that consumes a literal certificate; and
10. no certificate-level mutations for omitted guards, signs, scaling,
    transition rows, or perturbation powers.

The script formerly cited as an independent audit checked only the scalar
recurrence

\[
 e_{k+1}=12+2e_k
\]

and its closed-form exponent arithmetic. That calculation is correct as an
abstract recurrence, but it does not prove that the actual construction has a
program of the claimed length, that its leaves and denominators satisfy the
assumed bounds, or that every construction output is represented by the
program. Passing that script, sampled evaluations, and continuous-integration
success therefore supplied no universal derivative certificate.

The prior independent audit document itself stated that a generator should
emit the expression DAG and count its nodes. That uncompleted obligation is
incompatible with treating the universal statement as proved.

## Correct disposition

The all-level **unperturbed** reflected adaptive-ring construction remains in
force with its proved constants

\[
 R_3=64\pi^2,
 \qquad
 C_3=75/2.
\]

The perturbation result is weakened to the fixed-level theorem:
for each fixed level `J`, nonsingularity of the finitely many unperturbed local
systems and strict positivity of the finitely many unperturbed conductances
imply the existence of an existential, level-dependent radius `\delta_J>0` on
which support-preserving reflected latitude perturbations retain solvability,
positivity, reversibility, and exact `H_0\oplus H_1` fidelity.

No relation between `\delta_J` and a power of `h`, no lower bound uniform in
`J`, and no perturbed all-level rate or defect constants are claimed.

## Reopening condition

A future uniform theorem may be proposed only with either:

- the full literal certificate and independent verifier specified above; or
- a different analytic argument that supplies explicit level-uniform
  determinant, inverse, denominator, conductance, and recurrence margins.

Until then, the former statement remains rejected and may be cited only as a
historical failed claim.

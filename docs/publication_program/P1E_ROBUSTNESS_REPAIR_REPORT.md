# Proposition 7.3 repair report

## Authoritative repair base

- repository: `FusionSandwich/Testing`;
- branch: `agent/afp-post-audit-repair-d56db0b`;
- parent commit: `d05c98e5f1e211228940c7094df661c27d9e040b`;
- parent tree: `3c23cec0ebd25ca49706402774c25c395789a0d4`.

The final repair commit and tree are external exact-head metadata emitted by
the dedicated workflow; they are not self-referential fields in this source.

## Decision

Resolution family **B** was selected. The unsupported uniform all-level
statement was replaced by the strongest theorem justified by the construction:
a theorem valid at every fixed production level with fixed support and a
computable, level-dependent perturbation radius.

## Proved result

For each fixed level of the `M_0=2^80` family, reflected latitude perturbations preserve the exact
support pattern. The finite row-moment system has an invertible block
Jacobian at the strictly positive base solution. A Neumann/implicit-function
argument gives a unique positive shared-conductance solution in a
level-dependent neighborhood. Reversibility, exact coordinate fidelity,
connectivity, and the rowwise scalar quadratic residual persist. After
shrinking the neighborhood to preserve active chord bounds,

`r_max <= 1024 h_J^-2` and `D_2 <= 54 h_J^2`.

## Rejected result

No radius uniform over all refinement levels is proved. The former enormous
majorant is unsupported and has been removed from theorem status and value
registries. A uniform theorem would require a literal expression graph,
verified operation count, complete denominator separation, uniform inverse
bounds, positivity margins, derivative bounds, recurrence control, and two
independent certificate verifiers applied to production data.

## Repository synchronization

The manuscript, construction source, theorem and value registries, approach
registries, stage and release reports, boundary matrix, formalization notes,
CI firewalls, numerical scripts, adversarial tests, and dependency tables now
use the same fixed-level boundary. The committed certificate fixture is
explicitly conformance-only and cannot be cited as a production radius.

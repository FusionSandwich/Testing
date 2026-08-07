# P2D completion stage report

## Lineage

- repository: `FusionSandwich/Testing`
- accepted predecessor: `archive/afp-publication-p2d-acceleration-verified`
- predecessor SHA: `2fb7a11b75a9699a7afc8a2ee16c90656c58fb28`
- completion branch: `agent/afp-publication-p2d-completion-2fb7a11b`
- immutable completion archive: created only after the literal completion head passes all gates

The predecessor archive remains immutable.  This descendant closes clauses
that the earlier stage had deferred: a genuine forward-peaking robustness
sweep, a stronger classical FP comparator, separate setup cost, explicit
slow-subspace representation, and a ray-dominated adversary.

## Completed result

The package now contains the complete P2D mechanism and audit surface:

- exact high-order fixed point and compatible conservation constraints;
- error-propagation, shellwise, perturbation, spectral-equivalence, FOV, and
  sufficient iteration-count results;
- explicit angular/streaming/group/boundary mismatch decomposition;
- cached stationary and GMRES low solves with original-residual acceptance;
- frozen same-node optimized, monotone-baseline, and H2-poor positive
  generators;
- signed spectral modified-FP/FPSA comparator;
- a four-level forward-peaked heat-kernel/BFP slab sweep;
- a two-group reflective-boundary case;
- higher-shell and ray-dominated adversaries;
- 15 focused hostile tests and retained P2A–P2C regressions;
- finite Lean fixed-point/conservation core and axiom audit.

## Quantitative result

Across first moments 0.92312, 0.96079, 0.98020, and 0.99005, optimized versus
baseline iterations are respectively 12/22, 11/27, 12/31, and 13/30.  The
minimum reduction is 45.45%; the geometric-mean ratio is 0.4394.  The signed
spectral FP comparator is faster in the most forward-peaked rows but is not
positive.  The analytic grazing-ray adversary has 446.98% relative ballistic
transmission error, unchanged by the low operator at convergence.

## Changed inventory

- `pure_math/acceleration/core.py`
- `pure_math/acceleration/transport.py`
- `pure_math/acceleration/p2d_frozen_operators.json`
- `pure_math/acceleration/audit.py`
- `pure_math/acceleration/__init__.py`
- `pure_math/tests/test_p2d_acceleration.py`
- P2D manuscript, approach registry, claim map, clause matrix, hostile audit,
  and this report
- completion exact-head workflow

## Acceptance gate

Acceptance requires exact predecessor ancestry; an exact changed-path
allowlist; frozen Python dependencies; compile; the 15-test hostile suite;
the full audit sentinel; all forward-sweep comparators and metrics; retained
P2A–P2C exact regressions; Lean build and axiom scan; document/claim inventory;
source and evidence hashes; and a green workflow at the literal candidate
head.  Only then may a create-only completion archive be created.

# P2D stage report — fixed-point-preserving acceleration

## Lineage

- repository: `FusionSandwich/Testing`
- literal parent: `archive/afp-publication-p2c-codesign-verified`
- parent SHA: `b34c29b1b04f5293eaa4007b39d189efa03c51f5`
- candidate branch: `agent/afp-publication-p2d-acceleration-b34c29b1`

## Result

The stage supplies an exact residual-correction fixed point, an exact
constraint-preserving low inverse, shellwise and FOV sufficient contraction
conditions, original-residual GMRES verification, streaming and multigroup
noncommuting fixtures, all required comparators, and a higher-shell negative
control.  It does not claim universal acceleration.

## Inventory

- `pure_math/acceleration/{__init__,core,fixtures,audit}.py`
- `pure_math/tests/test_p2d_acceleration.py`
- `AFPBarrier/AccelerationFixedPoint.lean`
- `AFPBarrier/P2DAccelerationAxiomAudit.lean`
- P2D manuscript, clause matrix, claim map, approach registry, hostile audit,
  and this report
- dedicated exact-head workflow

## Release gate

Acceptance requires exact P2C ancestry, the exact changed-path allowlist,
Python compile/tests, the executable audit sentinel, retained P2A–P2C
regressions, Lean build/axiom scan, document/placeholder audit, and a green
workflow at the literal candidate head.  The archive must be create-only.

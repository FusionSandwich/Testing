"""Preregistered Paper-II benchmark hierarchy (P2E).

All production and ablation conductances are frozen in a hashed operator
registry before held-out cases are run.  Execution modules are intentionally
not imported here so ``python -m`` entry points remain side-effect free.
"""

from .operators import FrozenOperators, load_frozen_operators

__all__ = ["FrozenOperators", "load_frozen_operators"]

# Gate 1: kernel verification

Gate 1 requires all of the following on the pinned Lean/Mathlib toolchain:

1. `lake update` resolves the dependency graph.
2. `lake exe cache get` obtains the matching Mathlib cache.
3. `lake build` succeeds.
4. `lake env lean AFPBarrier/AxiomAudit.lean` succeeds.
5. The axiom audit reports no `sorryAx`, `propext`, `Classical.choice`, or `Quot.sound` dependency for the listed theorems.
6. A source scan finds no `sorry`, `admit`, or user-declared `axiom` in the project.

The repository workflow `.github/workflows/afp-barrier-gate1.yml` performs these checks and uploads the full logs as an artifact.

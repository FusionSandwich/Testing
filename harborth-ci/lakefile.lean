import Lake
open Lake DSL

package «harborth» where
  version := v!"0.1.0"

require mathlib from git
  "https://github.com/leanprover-community/mathlib4.git" @ "905b95818eb32af7874a58b427f50c1711a5e96c"

require classificationOfSurfaces from git
  "https://github.com/mccorvie/classification-of-surfaces.git" @
    "bb5db8b116d9c8fc2845123e8f724d0ca38a5378"

@[default_target]
lean_lib Harborth where

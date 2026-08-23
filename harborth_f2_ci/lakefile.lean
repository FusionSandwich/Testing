import Lake

open Lake DSL

package HarborthF2

require JordanCurveTheorem from git
  "https://github.com/epfl-lara/jordan-curve-theorem.git" @
  "e442525a662e9e3beb8205b9fa1fc99509076ded" / "HOLLight-Lean"

@[default_target]
lean_lib HarborthF2

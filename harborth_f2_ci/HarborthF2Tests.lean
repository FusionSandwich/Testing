import HarborthF2
import JordanCurveTheorem.JordanCurveTheoremStatement

open HarborthF2

example : harborthReal 1 = 0 := by
  norm_num [harborthReal]

#check OneSeparated
#check contactCount
#check f₂
#check JordanCurveTheorem.jordan_curve_theorem
#print axioms JordanCurveTheorem.jordan_curve_theorem

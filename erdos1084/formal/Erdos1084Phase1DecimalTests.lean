import Erdos1084.Phase1DecimalTheorem

open Erdos1084

example : kpClean = (4093 : ℝ) / 2000 :=
  UnitSeparatedConfiguration.kpClean_eq_20465

example {n : ℕ}
    (h : UnitSeparatedConfiguration.Phase1F3Certificate n) :
    (UnitSeparatedConfiguration.f3Nat n : ℝ) <
      6 * (n : ℝ) - ((4093 : ℝ) / 2000) * h.geometry.x :=
  UnitSeparatedConfiguration.phase1_f3Nat_bound_20465 h

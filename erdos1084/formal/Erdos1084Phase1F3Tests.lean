import Erdos1084.Phase1F3Theorem

open Erdos1084

/-! Smoke tests for the final formal `f₃(n)` theorem. -/

example {n : ℕ}
    (h : UnitSeparatedConfiguration.Phase1F3Certificate n) :
    (UnitSeparatedConfiguration.f3Nat n : ℝ) <
      6 * (n : ℝ) - kpClean * h.geometry.x :=
  UnitSeparatedConfiguration.phase1_f3Nat_bound h

example {n : ℕ}
    (h : UnitSeparatedConfiguration.Phase1F3Certificate n) :
    kpClean * h.geometry.x <
      6 * (n : ℝ) - (UnitSeparatedConfiguration.f3Nat n : ℝ) :=
  UnitSeparatedConfiguration.phase1_f3Nat_deficit_bound h

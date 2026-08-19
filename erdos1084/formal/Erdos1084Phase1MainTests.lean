import Erdos1084.Phase1MainTheorem

open Erdos1084

/-! Smoke tests for the complete relational Phase-I theorem. -/

example : kpClean = (2.0465 : ℝ) :=
  kpClean_eq_20465

example
    (geometry : Phase1PublishedInput)
    {n m : ℕ}
    (hn : 2 ≤ n)
    (hmax : IsThreeDimensionalContactNumber n m) :
    ∃ x : ℝ,
      KeplerPowerScale (n : ℝ) x ∧
      (m : ℝ) < 6 * (n : ℝ) - kpClean * x :=
  phase1_main_relational geometry hn hmax

example
    (geometry : Phase1PublishedInput)
    {n m : ℕ}
    (hn : 2 ≤ n)
    (hmax : IsThreeDimensionalContactNumber n m) :
    ∃ x : ℝ,
      KeplerPowerScale (n : ℝ) x ∧
      (m : ℝ) < 6 * (n : ℝ) - (2.0465 : ℝ) * x :=
  phase1_main_relational_decimal geometry hn hmax

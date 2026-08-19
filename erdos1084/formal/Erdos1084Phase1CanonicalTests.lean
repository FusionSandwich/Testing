import Erdos1084.Phase1CanonicalScale

open Erdos1084

/-! Smoke tests for the canonical Phase-I theorem. -/

example {n : ℕ} (hn : 0 < n) :
    KeplerPowerScale (n : ℝ) (phase1TwoThirdsScale n) :=
  phase1TwoThirdsScale_power hn

example {n : ℕ} {x : ℝ}
    (hx : KeplerPowerScale (n : ℝ) x) :
    x = phase1TwoThirdsScale n :=
  hx.eq_phase1TwoThirdsScale

example
    (geometry : Phase1PublishedInput)
    {n m : ℕ}
    (hn : 2 ≤ n)
    (hmax : IsThreeDimensionalContactNumber n m) :
    (m : ℝ) <
      6 * (n : ℝ) - (2.0465 : ℝ) * phase1TwoThirdsScale n :=
  phase1_main_canonical_decimal geometry hn hmax

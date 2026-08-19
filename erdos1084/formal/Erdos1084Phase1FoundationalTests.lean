import Erdos1084.Phase1FoundationalInterfaces

open Erdos1084

/-! Smoke tests for the granular Phase-I foundational interfaces. -/

example (foundation : Phase1FoundationalInput) :
    Phase1PublishedInput :=
  foundation.toPublishedInput

example
    (foundation : Phase1FoundationalInput)
    {n m : ℕ}
    (hn : 2 ≤ n)
    (hmax : IsThreeDimensionalContactNumber n m) :
    (m : ℝ) <
      6 * (n : ℝ) - (2.0465 : ℝ) * phase1TwoThirdsScale n :=
  foundation.main_canonical hn hmax

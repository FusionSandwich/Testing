import Erdos1084.Phase1FoundationalInterfacesFinal

open Erdos1084

/-! Smoke tests for the final Phase-I foundational interfaces. -/

example (foundation : Phase1FoundationalInputFinal) :
    Phase1PublishedInput :=
  foundation.toPublishedInput

example
    (foundation : Phase1FoundationalInputFinal)
    {n m : ℕ}
    (hn : 2 ≤ n)
    (hmax : IsThreeDimensionalContactNumber n m) :
    (m : ℝ) <
      6 * (n : ℝ) - (2.0465 : ℝ) * phase1TwoThirdsScale n :=
  foundation.main_canonical hn hmax

example
    (foundation : Phase1FoundationalInputFinal)
    {n : ℕ} (hn : 2 ≤ n) :
    (contactNumber3 n : ℝ) <
      6 * (n : ℝ) - (2.0465 : ℝ) * phase1TwoThirdsScale n :=
  foundation.contactNumber3_main_canonical hn

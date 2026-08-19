import Erdos1084.Phase1FoundationalInterfacesComplete

open Erdos1084

/-! Smoke tests for the complete granular Phase-I interfaces. -/

example (foundation : Phase1FoundationalInputComplete) :
    Phase1PublishedInput :=
  foundation.toPublishedInput

example
    (foundation : Phase1FoundationalInputComplete)
    {n : ℕ} (hn : 2 ≤ n) :
    (contactNumber3 n : ℝ) <
      6 * (n : ℝ) - (2.0465 : ℝ) * phase1TwoThirdsScale n :=
  foundation.contactNumber3_main_canonical hn

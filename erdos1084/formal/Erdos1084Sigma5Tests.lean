import Erdos1084

open Erdos1084

/-! Smoke tests for the Sigma-5 [001] two-lattice transition certificate. -/

example : sigma5NonnegativeCheck = true :=
  sigma5_transition_cost_nonnegative

example : sigma5BellmanCheck = true :=
  sigma5_bellman_certificate

example : sigma5PotentialValue sigma5LowerBulk = 0 :=
  sigma5_lower_bulk_potential

example : sigma5PotentialValue sigma5UpperBulk = 16 :=
  sigma5_upper_bulk_potential

example : sigma5PotentialValue 996 = 19 :=
  sigma5_exceptional_state_potential

example :
    sigma5Compatible sigma5LowerBulk sigma5MixedLayer = true ∧
    sigma5Compatible sigma5MixedLayer sigma5UpperBulk = true ∧
    sigma5TransitionCost sigma5LowerBulk sigma5MixedLayer = 16 ∧
    sigma5TransitionCost sigma5MixedLayer sigma5UpperBulk = 0 :=
  sigma5_abrupt_witness

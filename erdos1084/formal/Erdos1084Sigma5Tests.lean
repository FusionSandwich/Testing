import Erdos1084

open Erdos1084

/-! Smoke tests for the Sigma-5 [001] two-lattice transition certificate. -/

example : sigma5Potential.size = 1024 :=
  sigma5_potential_size

example : sigma5NonnegativeCheck = true :=
  sigma5_transition_cost_nonnegative

example : sigma5BellmanCheck = true :=
  sigma5_bellman_certificate

example : sigma5PotentialValue 31 = 0 :=
  sigma5_lower_bulk_potential

example : sigma5PotentialValue 992 = 16 :=
  sigma5_upper_bulk_potential

example :
    sigma5Compatible 31 1023 = true ∧
    sigma5Compatible 1023 992 = true ∧
    sigma5TransitionCost 31 1023 = 16 ∧
    sigma5TransitionCost 1023 992 = 0 :=
  sigma5_abrupt_witness

import Erdos1084.Phase1HiddenCapAlgebra

open Erdos1084

example {r z : ℝ} (hr : 0 < r) :
    r ^ 2 + 4 - 4 * r * z ≤ r ^ 2 ↔ 1 / r ≤ z :=
  phase1_hidden_cap_scalar_iff hr

example {z : ℝ} (h : 1 ≤ 2 - 2 * z) : z ≤ 1 / 2 :=
  phase1_contact_direction_dot_le_half h

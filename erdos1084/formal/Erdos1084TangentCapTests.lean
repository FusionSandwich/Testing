import Erdos1084.TangentCapGeometry

open Erdos1084
open scoped InnerProductSpace

/-! Smoke tests for tangent-neighbor cap geometry. -/

example {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
    {u v : E} {r : ℝ}
    (hu : ‖u‖ = 1) (hv : ‖v‖ = 1) (hr : 0 ≤ r) :
    ‖r • u - (2 : ℝ) • v‖ ^ 2 =
      r ^ 2 + 4 - 4 * r * ⟪u, v⟫_ℝ :=
  tangent_neighbor_norm_sq hu hv hr

example {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
    {u v : E} {r : ℝ}
    (hu : ‖u‖ = 1) (hv : ‖v‖ = 1) (hr : 0 < r) :
    ‖r • u - (2 : ℝ) • v‖ ≤ r ↔
      1 / r ≤ ⟪u, v⟫_ℝ :=
  tangent_neighbor_mem_iff_inner hu hv hr

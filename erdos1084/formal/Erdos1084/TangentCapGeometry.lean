import Mathlib

namespace Erdos1084

/-!
# Tangent-neighbor cap geometry

For two unit directions `u,v` and enlarged radius `r>0`, a point `r u` on the central enlarged
sphere lies in the enlarged sphere centered at the tangent neighbor `2 v` exactly when

`1/r ≤ <u,v>`.

This is the algebraic geometric identity that turns tangent-neighbor occlusion into a spherical
cap of angular radius `arccos(1/r)`.
-/

noncomputable section

open Real

variable {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]

/-- Squared-distance expansion for the tangent-neighbor geometry. -/
theorem tangent_neighbor_norm_sq
    {u v : E} {r : ℝ}
    (hu : ‖u‖ = 1) (hv : ‖v‖ = 1) (hr : 0 ≤ r) :
    ‖r • u - (2 : ℝ) • v‖ ^ 2 =
      r ^ 2 + 4 - 4 * r * ⟪u, v⟫_ℝ := by
  rw [norm_sub_sq_real]
  simp [norm_smul, hu, hv, abs_of_nonneg hr]
  ring

/-- Exact tangent-neighbor hidden-cap condition. -/
theorem tangent_neighbor_mem_iff_inner
    {u v : E} {r : ℝ}
    (hu : ‖u‖ = 1) (hv : ‖v‖ = 1) (hr : 0 < r) :
    ‖r • u - (2 : ℝ) • v‖ ≤ r ↔
      1 / r ≤ ⟪u, v⟫_ℝ := by
  have hsq := tangent_neighbor_norm_sq hu hv (le_of_lt hr)
  constructor
  · intro hnorm
    have hnorm0 : 0 ≤ ‖r • u - (2 : ℝ) • v‖ := norm_nonneg _
    have hsquare :
        ‖r • u - (2 : ℝ) • v‖ ^ 2 ≤ r ^ 2 := by
      nlinarith
    apply (div_le_iff₀ hr).2
    rw [hsq] at hsquare
    nlinarith
  · intro hinner
    have hprod : 1 ≤ ⟪u, v⟫_ℝ * r :=
      (div_le_iff₀ hr).1 hinner
    have hsquare :
        ‖r • u - (2 : ℝ) • v‖ ^ 2 ≤ r ^ 2 := by
      rw [hsq]
      nlinarith
    have hnorm0 : 0 ≤ ‖r • u - (2 : ℝ) • v‖ := norm_nonneg _
    nlinarith

end

end Erdos1084

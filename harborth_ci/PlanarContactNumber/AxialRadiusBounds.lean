import PlanarContactNumber.AxialBallMembership

namespace PlanarContactNumber

/-- The max/absolute-value definition of axial radius is equivalent to six
linear coordinate bounds. -/
theorem axialHexRadius_le_iff_bounds {p : Axial} {R : ℤ} :
    axialHexRadius p ≤ R ↔
      -R ≤ p.1 ∧ p.1 ≤ R ∧
      -R ≤ p.2 ∧ p.2 ≤ R ∧
      -R ≤ p.1 + p.2 ∧ p.1 + p.2 ≤ R := by
  unfold axialHexRadius
  rw [max_le_iff, max_le_iff]
  constructor
  · rintro ⟨hx, hy, hs⟩
    have hx' := (abs_le.mp hx)
    have hy' := (abs_le.mp hy)
    have hs' := (abs_le.mp hs)
    omega
  · rintro ⟨hxl, hxu, hyl, hyu, hsl, hsu⟩
    exact ⟨abs_le.mpr ⟨hxl, hxu⟩,
      abs_le.mpr ⟨hyl, hyu⟩,
      abs_le.mpr ⟨hsl, hsu⟩⟩

/-- Coordinate-bound membership criterion for centered axial balls. -/
theorem mem_axialBall_iff_bounds {s : ℕ} {p : Axial} :
    p ∈ axialBall s ↔
      -((s : ℕ) : ℤ) ≤ p.1 ∧ p.1 ≤ (s : ℤ) ∧
      -((s : ℕ) : ℤ) ≤ p.2 ∧ p.2 ≤ (s : ℤ) ∧
      -((s : ℕ) : ℤ) ≤ p.1 + p.2 ∧ p.1 + p.2 ≤ (s : ℤ) := by
  rw [mem_axialBall_iff_axialHexRadius_le, axialHexRadius_le_iff_bounds]

end PlanarContactNumber

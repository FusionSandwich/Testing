import PlanarContactNumber.Definitions

namespace PlanarContactNumber

/-- Axial integer coordinates for the triangular lattice. -/
abbrev Axial := ℤ × ℤ

/-- The positive-definite quadratic form governing squared distances in axial
coordinates. -/
def axialNormSq (d : Axial) : ℤ :=
  d.1 ^ 2 + d.1 * d.2 + d.2 ^ 2

/-- The standard unit triangular-lattice embedding into the actual Euclidean
plane used by the contact-number definition. -/
noncomputable def triangularPoint (p : Axial) : Point :=
  !₂[(p.1 : ℝ) + (p.2 : ℝ) / 2,
      Real.sqrt 3 * (p.2 : ℝ) / 2]

/-- Coordinate criterion for unit distance in the Euclidean plane. -/
theorem plane_dist_eq_one_iff {x₀ y₀ x₁ y₁ : ℝ} :
    dist !₂[x₀, y₀] !₂[x₁, y₁] = 1 ↔
      (x₀ - x₁) ^ 2 + (y₀ - y₁) ^ 2 = 1 := by
  simp [dist_eq_norm_sub, PiLp.norm_eq_of_L2]

/-- The axial quadratic form is nonnegative. -/
theorem axialNormSq_nonneg (d : Axial) : 0 ≤ axialNormSq d := by
  rcases d with ⟨a, b⟩
  dsimp [axialNormSq]
  nlinarith [sq_nonneg a, sq_nonneg b, sq_nonneg (a + b)]

end PlanarContactNumber

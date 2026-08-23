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

/-- Coordinate criterion for squared distance in the Euclidean plane. -/
theorem plane_dist_sq {x₀ y₀ x₁ y₁ : ℝ} :
    dist !₂[x₀, y₀] !₂[x₁, y₁] ^ 2 =
      (x₀ - x₁) ^ 2 + (y₀ - y₁) ^ 2 := by
  simp [EuclideanSpace.dist_sq_eq, Real.dist_eq, sq_abs]

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

/-- Squared Euclidean distance in the embedded triangular lattice is exactly
its integral axial quadratic form. -/
theorem triangularPoint_dist_sq (p q : Axial) :
    dist (triangularPoint p) (triangularPoint q) ^ 2 =
      (axialNormSq (p.1 - q.1, p.2 - q.2) : ℝ) := by
  rcases p with ⟨a, b⟩
  rcases q with ⟨c, d⟩
  change
    dist !₂[(a : ℝ) + (b : ℝ) / 2, Real.sqrt 3 * (b : ℝ) / 2]
        !₂[(c : ℝ) + (d : ℝ) / 2, Real.sqrt 3 * (d : ℝ) / 2] ^ 2 =
      (axialNormSq (a - c, b - d) : ℝ)
  rw [plane_dist_sq]
  dsimp [axialNormSq]
  push_cast
  nlinarith [Real.sq_sqrt (by norm_num : (0 : ℝ) ≤ 3)]

/-- Unit distance in the embedded lattice is equivalent to the axial norm
being exactly one. -/
theorem triangularPoint_dist_eq_one_iff (p q : Axial) :
    dist (triangularPoint p) (triangularPoint q) = 1 ↔
      axialNormSq (p.1 - q.1, p.2 - q.2) = 1 := by
  have hsq := triangularPoint_dist_sq p q
  constructor
  · intro h
    rw [h] at hsq
    norm_num at hsq
    exact_mod_cast hsq.symm
  · intro h
    have hsq' : dist (triangularPoint p) (triangularPoint q) ^ 2 = 1 := by
      rw [triangularPoint_dist_sq, h]
      norm_num
    have hnonneg := dist_nonneg (triangularPoint p) (triangularPoint q)
    nlinarith

end PlanarContactNumber

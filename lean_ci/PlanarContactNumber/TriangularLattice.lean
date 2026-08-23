import PlanarContactNumber.UpperArithmetic

open scoped EuclideanGeometry

namespace PlanarContactNumber

/-- Integer axial coordinates for the triangular lattice. -/
abbrev Axial := ℤ × ℤ

/-- Difference of axial coordinates. -/
def axialSub (p q : Axial) : Axial := (p.1 - q.1, p.2 - q.2)

/-- The positive-definite quadratic form governing triangular-lattice distances. -/
def axialQ (p : Axial) : ℤ := p.1 ^ 2 + p.1 * p.2 + p.2 ^ 2

/-- The standard triangular-lattice embedding in the Euclidean plane. -/
noncomputable def axialPoint (p : Axial) : Point :=
  !₂[(p.1 : ℝ) + (p.2 : ℝ) / 2, Real.sqrt 3 / 2 * (p.2 : ℝ)]

/-- Four times the axial quadratic form is a visibly nonnegative sum of squares. -/
theorem four_mul_axialQ (p : Axial) :
    4 * axialQ p = (2 * p.1 + p.2) ^ 2 + 3 * p.2 ^ 2 := by
  simp [axialQ]
  ring

/-- The axial quadratic form is positive away from the origin. -/
theorem axialQ_pos {p : Axial} (hp : p ≠ (0, 0)) : 0 < axialQ p := by
  by_contra hnot
  have hle : axialQ p ≤ 0 := le_of_not_gt hnot
  have hid := four_mul_axialQ p
  have hsq1 : 0 ≤ (2 * p.1 + p.2) ^ 2 := sq_nonneg _
  have hsq2 : 0 ≤ p.2 ^ 2 := sq_nonneg _
  have hb : p.2 = 0 := by nlinarith
  have ha : p.1 = 0 := by nlinarith
  apply hp
  ext <;> simp [ha, hb]

/-- Integer positivity upgrades to a lower bound by one. -/
theorem one_le_axialQ {p : Axial} (hp : p ≠ (0, 0)) : 1 ≤ axialQ p := by
  omega

/-- The six unit directions in axial coordinates. -/
theorem axialQ_eq_one_iff (p : Axial) :
    axialQ p = 1 ↔
      p = (1, 0) ∨ p = (-1, 0) ∨ p = (0, 1) ∨
      p = (0, -1) ∨ p = (1, -1) ∨ p = (-1, 1) := by
  rcases p with ⟨a, b⟩
  constructor
  · intro h
    have hid := four_mul_axialQ (a, b)
    simp only [h] at hid
    have hb_lo : -1 ≤ b := by nlinarith [sq_nonneg (2 * a + b)]
    have hb_hi : b ≤ 1 := by nlinarith [sq_nonneg (2 * a + b)]
    have hb_cases : b = -1 ∨ b = 0 ∨ b = 1 := by omega
    rcases hb_cases with rfl | rfl | rfl
    · have ha_lo : 0 ≤ a := by
        simp [axialQ] at h
        nlinarith [sq_nonneg (a - 1)]
      have ha_hi : a ≤ 1 := by
        simp [axialQ] at h
        nlinarith [sq_nonneg a]
      have ha_cases : a = 0 ∨ a = 1 := by omega
      rcases ha_cases with rfl | rfl <;> simp
    · have ha_lo : -1 ≤ a := by
        simp [axialQ] at h
        nlinarith [sq_nonneg (a + 1)]
      have ha_hi : a ≤ 1 := by
        simp [axialQ] at h
        nlinarith [sq_nonneg (a - 1)]
      have ha_cases : a = -1 ∨ a = 0 ∨ a = 1 := by omega
      rcases ha_cases with rfl | rfl | rfl <;> simp [axialQ] at h ⊢
    · have ha_lo : -1 ≤ a := by
        simp [axialQ] at h
        nlinarith [sq_nonneg (a + 1)]
      have ha_hi : a ≤ 0 := by
        simp [axialQ] at h
        nlinarith [sq_nonneg a]
      have ha_cases : a = -1 ∨ a = 0 := by omega
      rcases ha_cases with rfl | rfl <;> simp
  · rintro (rfl | rfl | rfl | rfl | rfl | rfl) <;> norm_num [axialQ]

/-- Exact squared-distance formula for the triangular-lattice embedding. -/
theorem axialPoint_dist_sq (p q : Axial) :
    dist (axialPoint p) (axialPoint q) ^ 2 = (axialQ (axialSub p q) : ℝ) := by
  rw [EuclideanSpace.dist_sq_eq]
  simp [axialPoint, axialSub, axialQ, Fin.sum_univ_two, Real.dist_eq]
  have hsqrt : Real.sqrt (3 : ℝ) ^ 2 = 3 := Real.sq_sqrt (by norm_num)
  nlinarith

/-- Distinct lattice points are at least unit distance apart. -/
theorem axialPoint_oneSeparated {p q : Axial} (hpq : p ≠ q) :
    (1 : ℝ) ≤ dist (axialPoint p) (axialPoint q) := by
  have hsub : axialSub p q ≠ (0, 0) := by
    intro h
    apply hpq
    rcases p with ⟨p₁, p₂⟩
    rcases q with ⟨q₁, q₂⟩
    simp [axialSub] at h ⊢
    omega
  have hQ : (1 : ℝ) ≤ (axialQ (axialSub p q) : ℝ) := by
    exact_mod_cast one_le_axialQ hsub
  have hdist := axialPoint_dist_sq p q
  have hdist0 : 0 ≤ dist (axialPoint p) (axialPoint q) := dist_nonneg
  nlinarith

/-- Unit distance is exactly axial quadratic distance one. -/
theorem axialPoint_contact_iff (p q : Axial) :
    dist (axialPoint p) (axialPoint q) = 1 ↔ axialQ (axialSub p q) = 1 := by
  have hdist := axialPoint_dist_sq p q
  have hdist0 : 0 ≤ dist (axialPoint p) (axialPoint q) := dist_nonneg
  constructor
  · intro h
    rw [h] at hdist
    norm_num at hdist
    exact_mod_cast hdist.symm
  · intro h
    have hQ : (axialQ (axialSub p q) : ℝ) = 1 := by exact_mod_cast h
    nlinarith

/-- The triangular-lattice embedding is injective. -/
theorem axialPoint_injective : Function.Injective axialPoint := by
  intro p q hpq
  by_contra hne
  have hsep := axialPoint_oneSeparated hne
  rw [hpq, dist_self] at hsep
  norm_num at hsep

end PlanarContactNumber

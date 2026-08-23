import PlanarContactNumber.Definitions

namespace PlanarContactNumber

/-- Axial integer coordinates for the triangular lattice. -/
abbrev Axial := ℤ × ℤ

/-- The integral quadratic form whose square root is the triangular-lattice distance. -/
def axialQ (a b : ℤ) : ℤ := a ^ 2 + a * b + b ^ 2

/-- A useful sum-of-squares identity for the triangular quadratic form. -/
theorem four_mul_axialQ (a b : ℤ) :
    4 * axialQ a b = (2 * a + b) ^ 2 + 3 * b ^ 2 := by
  ring

/-- The triangular quadratic form is nonnegative. -/
theorem axialQ_nonneg (a b : ℤ) : 0 ≤ axialQ a b := by
  have hident := four_mul_axialQ a b
  nlinarith [sq_nonneg (2 * a + b), sq_nonneg b]

/-- The triangular quadratic form vanishes only at the origin. -/
theorem axialQ_eq_zero_iff (a b : ℤ) :
    axialQ a b = 0 ↔ a = 0 ∧ b = 0 := by
  constructor
  · intro hq
    have hident := four_mul_axialQ a b
    have hb2 : b ^ 2 = 0 := by
      nlinarith [sq_nonneg (2 * a + b), sq_nonneg b]
    have hb : b = 0 := by nlinarith [sq_nonneg b]
    subst b
    have ha2 : a ^ 2 = 0 := by simpa [axialQ] using hq
    have ha : a = 0 := by nlinarith [sq_nonneg a]
    exact ⟨ha, rfl⟩
  · rintro ⟨rfl, rfl⟩
    norm_num [axialQ]

/-- Every nonzero axial displacement has squared lattice length at least one. -/
theorem one_le_axialQ_of_ne (a b : ℤ) (h : a ≠ 0 ∨ b ≠ 0) :
    1 ≤ axialQ a b := by
  have hnonneg := axialQ_nonneg a b
  have hne : axialQ a b ≠ 0 := by
    intro hq
    rcases (axialQ_eq_zero_iff a b).mp hq with ⟨ha, hb⟩
    exact h.elim (fun hna => hna ha) (fun hnb => hnb hb)
  omega

/-- The six unit directions are exactly the integral solutions of `axialQ = 1`. -/
theorem axialQ_eq_one_iff (a b : ℤ) :
    axialQ a b = 1 ↔
      (a = 1 ∧ b = 0) ∨ (a = -1 ∧ b = 0) ∨
      (a = 0 ∧ b = 1) ∨ (a = 0 ∧ b = -1) ∨
      (a = 1 ∧ b = -1) ∨ (a = -1 ∧ b = 1) := by
  constructor
  · intro hq
    have h1 := four_mul_axialQ a b
    have h2 : 4 * axialQ a b = (2 * b + a) ^ 2 + 3 * a ^ 2 := by
      ring
    have ha2 : a ^ 2 ≤ 1 := by
      nlinarith [sq_nonneg (2 * b + a)]
    have hb2 : b ^ 2 ≤ 1 := by
      nlinarith [sq_nonneg (2 * a + b)]
    have ha_lower : -1 ≤ a := by nlinarith
    have ha_upper : a ≤ 1 := by nlinarith
    have hb_lower : -1 ≤ b := by nlinarith
    have hb_upper : b ≤ 1 := by nlinarith
    interval_cases a <;> interval_cases b <;> norm_num [axialQ] at hq ⊢
  · rintro (⟨rfl, rfl⟩ | ⟨rfl, rfl⟩ | ⟨rfl, rfl⟩ |
      ⟨rfl, rfl⟩ | ⟨rfl, rfl⟩ | ⟨rfl, rfl⟩) <;>
      norm_num [axialQ]

/-- Coordinate formula for squared Euclidean distance in the plane. -/
theorem plane_dist_sq (x₀ y₀ x₁ y₁ : ℝ) :
    dist !₂[x₀, y₀] !₂[x₁, y₁] ^ 2 =
      (x₀ - x₁) ^ 2 + (y₀ - y₁) ^ 2 := by
  simp [dist_eq_norm_sub, PiLp.norm_sq_eq_of_L2]

/-- The standard isometric embedding of axial triangular-lattice coordinates. -/
noncomputable def triangularPoint (p : Axial) : Point :=
  !₂[(p.1 : ℝ) + (p.2 : ℝ) / 2,
      (Real.sqrt 3 / 2) * (p.2 : ℝ)]

/-- Squared Euclidean distance between embedded lattice points is the integral
triangular quadratic form of their axial displacement. -/
theorem triangularPoint_dist_sq (p q : Axial) :
    dist (triangularPoint p) (triangularPoint q) ^ 2 =
      (axialQ (p.1 - q.1) (p.2 - q.2) : ℝ) := by
  rw [show triangularPoint p =
      !₂[(p.1 : ℝ) + (p.2 : ℝ) / 2,
          (Real.sqrt 3 / 2) * (p.2 : ℝ)] from rfl,
    show triangularPoint q =
      !₂[(q.1 : ℝ) + (q.2 : ℝ) / 2,
          (Real.sqrt 3 / 2) * (q.2 : ℝ)] from rfl,
    plane_dist_sq]
  have hsqrt : (Real.sqrt (3 : ℝ)) ^ 2 = 3 := Real.sq_sqrt (by norm_num)
  norm_num [axialQ]
  push_cast
  nlinarith

/-- Distinct triangular-lattice points are at Euclidean distance at least one. -/
theorem one_le_dist_triangularPoint {p q : Axial} (hpq : p ≠ q) :
    (1 : ℝ) ≤ dist (triangularPoint p) (triangularPoint q) := by
  have hdelta : p.1 - q.1 ≠ 0 ∨ p.2 - q.2 ≠ 0 := by
    by_contra h
    push_neg at h
    apply hpq
    apply Prod.ext <;> omega
  have hq := one_le_axialQ_of_ne (p.1 - q.1) (p.2 - q.2) hdelta
  have hqR : (1 : ℝ) ≤ (axialQ (p.1 - q.1) (p.2 - q.2) : ℝ) := by
    exact_mod_cast hq
  have hsq := triangularPoint_dist_sq p q
  have hdist := dist_nonneg (triangularPoint p) (triangularPoint q)
  nlinarith

/-- The triangular-lattice embedding is injective. -/
theorem triangularPoint_injective : Function.Injective triangularPoint := by
  intro p q hpq
  by_contra hne
  have hsep := one_le_dist_triangularPoint hne
  rw [hpq, dist_self] at hsep
  norm_num at hsep

/-- Any injectively indexed family of axial lattice points gives an actual
one-separated Euclidean configuration. -/
theorem oneSeparated_triangularPoint {n : ℕ} (z : Fin n → Axial)
    (hz : Function.Injective z) :
    OneSeparated (fun i => triangularPoint (z i)) := by
  intro i j hij
  exact one_le_dist_triangularPoint (hz.ne hij)

/-- Euclidean contacts in the triangular lattice are exactly the six axial
unit directions. -/
theorem triangularPoint_dist_eq_one_iff (p q : Axial) :
    dist (triangularPoint p) (triangularPoint q) = 1 ↔
      axialQ (p.1 - q.1) (p.2 - q.2) = 1 := by
  constructor
  · intro hd
    have hsq := triangularPoint_dist_sq p q
    have hcast : (axialQ (p.1 - q.1) (p.2 - q.2) : ℝ) = 1 := by
      nlinarith
    exact_mod_cast hcast
  · intro hq
    have hsq := triangularPoint_dist_sq p q
    have hcast : (axialQ (p.1 - q.1) (p.2 - q.2) : ℝ) = 1 := by
      exact_mod_cast hq
    have hdist := dist_nonneg (triangularPoint p) (triangularPoint q)
    nlinarith

/-- Fully expanded six-direction contact criterion. -/
theorem triangularPoint_contact_iff (p q : Axial) :
    dist (triangularPoint p) (triangularPoint q) = 1 ↔
      (p.1 - q.1 = 1 ∧ p.2 - q.2 = 0) ∨
      (p.1 - q.1 = -1 ∧ p.2 - q.2 = 0) ∨
      (p.1 - q.1 = 0 ∧ p.2 - q.2 = 1) ∨
      (p.1 - q.1 = 0 ∧ p.2 - q.2 = -1) ∨
      (p.1 - q.1 = 1 ∧ p.2 - q.2 = -1) ∨
      (p.1 - q.1 = -1 ∧ p.2 - q.2 = 1) := by
  rw [triangularPoint_dist_eq_one_iff, axialQ_eq_one_iff]

end PlanarContactNumber

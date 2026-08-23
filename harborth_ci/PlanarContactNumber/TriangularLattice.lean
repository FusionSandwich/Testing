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

/-- The axial quadratic form vanishes only at the origin. -/
theorem axialNormSq_eq_zero_iff (d : Axial) :
    axialNormSq d = 0 ↔ d = (0, 0) := by
  rcases d with ⟨a, b⟩
  constructor
  · intro h
    have hsum : (2 * a + b) ^ 2 + 3 * b ^ 2 = 0 := by
      dsimp [axialNormSq] at h
      nlinarith
    have hb2 : b ^ 2 = 0 := by
      nlinarith [sq_nonneg (2 * a + b)]
    have hb : b = 0 := sq_eq_zero_iff.mp hb2
    have ha2 : a ^ 2 = 0 := by
      dsimp [axialNormSq] at h
      rw [hb] at h
      norm_num at h ⊢
      exact h
    have ha : a = 0 := sq_eq_zero_iff.mp ha2
    exact Prod.ext ha hb
  · intro h
    have ha : a = 0 := congrArg Prod.fst h
    have hb : b = 0 := congrArg Prod.snd h
    norm_num [axialNormSq, ha, hb]

/-- A nonzero axial vector has strictly positive integral norm. -/
theorem axialNormSq_pos_of_ne_zero {d : Axial} (hd : d ≠ (0, 0)) :
    0 < axialNormSq d := by
  have hnonneg := axialNormSq_nonneg d
  have hne : axialNormSq d ≠ 0 := by
    intro hzero
    exact hd ((axialNormSq_eq_zero_iff d).mp hzero)
  omega

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
    have hnonneg : 0 ≤ dist (triangularPoint p) (triangularPoint q) := dist_nonneg
    nlinarith

/-- The six unit vectors in axial coordinates are the only vectors of axial
norm one. -/
theorem axialNormSq_eq_one_iff (d : Axial) :
    axialNormSq d = 1 ↔
      d = (1, 0) ∨ d = (0, 1) ∨ d = (-1, 1) ∨
        d = (-1, 0) ∨ d = (0, -1) ∨ d = (1, -1) := by
  constructor
  · rcases d with ⟨a, b⟩
    intro h
    have hsum : a ^ 2 + b ^ 2 + (a + b) ^ 2 = 2 := by
      dsimp [axialNormSq] at h
      nlinarith
    have ha_sq : a ^ 2 ≤ 2 := by
      nlinarith [sq_nonneg b, sq_nonneg (a + b)]
    have hb_sq : b ^ 2 ≤ 2 := by
      nlinarith [sq_nonneg a, sq_nonneg (a + b)]
    have ha_lo : -1 ≤ a := by
      by_contra hnot
      have ha : a ≤ -2 := by omega
      nlinarith [sq_nonneg (a + 1)]
    have ha_hi : a ≤ 1 := by
      by_contra hnot
      have ha : 2 ≤ a := by omega
      nlinarith [sq_nonneg (a - 1)]
    have hb_lo : -1 ≤ b := by
      by_contra hnot
      have hb : b ≤ -2 := by omega
      nlinarith [sq_nonneg (b + 1)]
    have hb_hi : b ≤ 1 := by
      by_contra hnot
      have hb : 2 ≤ b := by omega
      nlinarith [sq_nonneg (b - 1)]
    interval_cases a <;> interval_cases b <;>
      norm_num [axialNormSq] at h
    all_goals norm_num
  · rintro (rfl | rfl | rfl | rfl | rfl | rfl) <;>
      norm_num [axialNormSq]

/-- Unit contacts in the triangular lattice are exactly the six nearest-neighbor
differences. -/
theorem triangularPoint_dist_eq_one_iff_neighbor (p q : Axial) :
    dist (triangularPoint p) (triangularPoint q) = 1 ↔
      (p.1 - q.1, p.2 - q.2) = (1, 0) ∨
      (p.1 - q.1, p.2 - q.2) = (0, 1) ∨
      (p.1 - q.1, p.2 - q.2) = (-1, 1) ∨
      (p.1 - q.1, p.2 - q.2) = (-1, 0) ∨
      (p.1 - q.1, p.2 - q.2) = (0, -1) ∨
      (p.1 - q.1, p.2 - q.2) = (1, -1) := by
  rw [triangularPoint_dist_eq_one_iff, axialNormSq_eq_one_iff]

/-- Distinct triangular-lattice points are at least unit distance apart. -/
theorem one_le_dist_triangularPoint_of_ne {p q : Axial} (hpq : p ≠ q) :
    (1 : ℝ) ≤ dist (triangularPoint p) (triangularPoint q) := by
  have hdiff : (p.1 - q.1, p.2 - q.2) ≠ (0, 0) := by
    intro hzero
    apply hpq
    apply Prod.ext
    · have h := congrArg Prod.fst hzero
      dsimp at h
      omega
    · have h := congrArg Prod.snd hzero
      dsimp at h
      omega
  have hpos := axialNormSq_pos_of_ne_zero hdiff
  have hone : 1 ≤ axialNormSq (p.1 - q.1, p.2 - q.2) := by omega
  have hsq : (1 : ℝ) ^ 2 ≤ dist (triangularPoint p) (triangularPoint q) ^ 2 := by
    rw [triangularPoint_dist_sq]
    exact_mod_cast hone
  have hnonneg : 0 ≤ dist (triangularPoint p) (triangularPoint q) := dist_nonneg
  exact le_of_sq_le_sq hsq hnonneg

/-- Any injective finite enumeration of axial lattice points gives an actual
one-separated Euclidean configuration. -/
theorem oneSeparated_triangularPoint_comp {n : ℕ} {a : Fin n → Axial}
    (ha : Function.Injective a) :
    OneSeparated (fun i => triangularPoint (a i)) := by
  intro i j hij
  exact one_le_dist_triangularPoint_of_ne (fun h => hij (ha h))

end PlanarContactNumber

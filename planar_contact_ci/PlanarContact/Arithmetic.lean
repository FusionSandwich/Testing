import PlanarContact.Definitions

namespace PlanarContact

private theorem one_le_natCast {n : ℕ} (hn : 1 ≤ n) : (1 : ℝ) ≤ n := by
  exact_mod_cast hn

/-- The square-root radicand in the Harborth expression is nonnegative for `n ≥ 1`. -/
theorem radicand_nonneg {n : ℕ} (hn : 1 ≤ n) :
    0 ≤ 12 * (n : ℝ) - 3 := by
  have hn' := one_le_natCast hn
  nlinarith

/-- For every positive size, the square root occurring in the formula is at least three. -/
theorem three_le_sqrt_radicand {n : ℕ} (hn : 1 ≤ n) :
    (3 : ℝ) ≤ Real.sqrt (12 * (n : ℝ) - 3) := by
  have hrad := radicand_nonneg hn
  rw [Real.le_sqrt (by norm_num) hrad]
  have hn' := one_le_natCast hn
  nlinarith

/-- The real Harborth expression is nonnegative on positive integers. -/
theorem harborthReal_nonneg {n : ℕ} (hn : 1 ≤ n) :
    0 ≤ harborthReal n := by
  have hn' := one_le_natCast hn
  have hrad := radicand_nonneg hn
  have hsnon := Real.sqrt_nonneg (12 * (n : ℝ) - 3)
  have hsq := Real.sq_sqrt hrad
  have hprod : 0 ≤ 3 * (3 * (n : ℝ) - 1) * ((n : ℝ) - 1) := by positivity
  unfold harborthReal
  nlinarith

/-- The concavity inequality used when the contact graph is disconnected. -/
theorem harborthReal_add_le {a b : ℕ} (ha : 1 ≤ a) (hb : 1 ≤ b) :
    harborthReal a + harborthReal b ≤ harborthReal (a + b) := by
  have hA : 0 ≤ 12 * (a : ℝ) - 3 := radicand_nonneg ha
  have hB : 0 ≤ 12 * (b : ℝ) - 3 := radicand_nonneg hb
  have hab : 1 ≤ a + b := by omega
  have hT : 0 ≤ 12 * ((a + b : ℕ) : ℝ) - 3 := radicand_nonneg hab
  have ha3 := three_le_sqrt_radicand ha
  have hb3 := three_le_sqrt_radicand hb
  have hsqA := Real.sq_sqrt hA
  have hsqB := Real.sq_sqrt hB
  have hmul :
      0 ≤ (Real.sqrt (12 * (a : ℝ) - 3) - 3) *
        (Real.sqrt (12 * (b : ℝ) - 3) - 3) := by positivity
  have hsum_nonneg :
      0 ≤ Real.sqrt (12 * (a : ℝ) - 3) + Real.sqrt (12 * (b : ℝ) - 3) := by
    positivity
  have hsqrt :
      Real.sqrt (12 * (((a + b : ℕ) : ℝ)) - 3) ≤
        Real.sqrt (12 * (a : ℝ) - 3) + Real.sqrt (12 * (b : ℝ) - 3) := by
    rw [Real.sqrt_le_left hsum_nonneg]
    rw [Real.sq_sqrt hT]
    norm_num at hsqA hsqB ⊢
    push_cast
    nlinarith
  unfold harborthReal
  push_cast
  linarith

/-- The concavity inequality used when two induced subgraphs overlap in one cut vertex. -/
theorem harborthReal_oneVertexSum_le {a b : ℕ} (ha : 2 ≤ a) (hb : 2 ≤ b) :
    harborthReal a + harborthReal b ≤ harborthReal (a + b - 1) := by
  have ha1 : 1 ≤ a := by omega
  have hb1 : 1 ≤ b := by omega
  have hA : 0 ≤ 12 * (a : ℝ) - 3 := radicand_nonneg ha1
  have hB : 0 ≤ 12 * (b : ℝ) - 3 := radicand_nonneg hb1
  have hab : 1 ≤ a + b - 1 := by omega
  have hT : 0 ≤ 12 * (((a + b - 1 : ℕ) : ℝ)) - 3 := radicand_nonneg hab
  have ha3 := three_le_sqrt_radicand ha1
  have hb3 := three_le_sqrt_radicand hb1
  have hsqA := Real.sq_sqrt hA
  have hsqB := Real.sq_sqrt hB
  have hmul :
      0 ≤ (Real.sqrt (12 * (a : ℝ) - 3) - 3) *
        (Real.sqrt (12 * (b : ℝ) - 3) - 3) := by positivity
  have hsum_nonneg :
      0 ≤ Real.sqrt (12 * (a : ℝ) - 3) +
        Real.sqrt (12 * (b : ℝ) - 3) - 3 := by linarith
  have hsqrt :
      Real.sqrt (12 * (((a + b - 1 : ℕ) : ℝ)) - 3) ≤
        Real.sqrt (12 * (a : ℝ) - 3) + Real.sqrt (12 * (b : ℝ) - 3) - 3 := by
    rw [Real.sqrt_le_left hsum_nonneg]
    rw [Real.sq_sqrt hT]
    norm_num at hsqA hsqB ⊢
    have hcast : (((a + b - 1 : ℕ) : ℝ)) = (a : ℝ) + (b : ℝ) - 1 := by
      omega
    rw [hcast]
    nlinarith
  unfold harborthReal
  have hcast : (((a + b - 1 : ℕ) : ℝ)) = (a : ℝ) + (b : ℝ) - 1 := by
    omega
  rw [hcast]
  push_cast
  linarith

/-- A convenient exact-floor criterion for a nonnegative real number. -/
theorem natFloor_eq_of_bounds {x : ℝ} {z : ℕ}
    (hx0 : 0 ≤ x) (hzx : (z : ℝ) ≤ x) (hxz : x < (z : ℝ) + 1) :
    ⌊x⌋₊ = z := by
  exact (Nat.floor_eq_iff hx0).2 ⟨hzx, hxz⟩

end PlanarContact

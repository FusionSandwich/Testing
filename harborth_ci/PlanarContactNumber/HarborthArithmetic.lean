import PlanarContactNumber.Definitions

namespace PlanarContactNumber

/-- The real-valued expression whose floor is the planar contact number. -/
noncomputable def harborthReal (n : ℕ) : ℝ :=
  3 * (n : ℝ) - Real.sqrt (12 * (n : ℝ) - 3)

/-- Number of lattice points in the centered hexagon of radius `s`. -/
def shellN (s : ℕ) : ℕ := 3 * s ^ 2 + 3 * s + 1

/-- Number of contacts in the centered hexagon of radius `s`. -/
def shellE (s : ℕ) : ℕ := 9 * s ^ 2 + 3 * s

/-- The size obtained from a centered hexagon and a partial next shell. -/
def partialN (s i j : ℕ) : ℕ := shellN s + (s + 1) * i + j

/-- The contact count for a nonempty partial next shell, written in `ℤ` to avoid
truncated subtraction. -/
def partialZ (s i j : ℕ) : ℤ :=
  9 * (s : ℤ) ^ 2 + 3 * (s : ℤ) +
    (3 * (s : ℤ) + 2) * (i : ℤ) + 3 * (j : ℤ) - 1

/-- The centered-hexagon radicand is a perfect square. -/
theorem shell_radicand (s : ℕ) :
    12 * (shellN s : ℝ) - 3 = (6 * (s : ℝ) + 3) ^ 2 := by
  norm_num [shellN]
  ring

/-- At a centered hexagonal number, the real Harborth expression is integral. -/
theorem harborthReal_shellN (s : ℕ) :
    harborthReal (shellN s) = (shellE s : ℝ) := by
  rw [harborthReal, shell_radicand, Real.sqrt_sq (by positivity : (0 : ℝ) ≤ 6 * s + 3)]
  norm_num [shellN, shellE]
  ring

/-- Exact floor identity at centered hexagonal numbers. -/
theorem floor_harborthReal_shellN (s : ℕ) :
    ⌊harborthReal (shellN s)⌋ = (shellE s : ℤ) := by
  rw [harborthReal_shellN]
  simp

/-- The two consecutive integer squares that trap the radicand for a nonempty
partial shell. -/
theorem partial_sqrt_window (s i j : ℕ) (hi : i ≤ 5) (hj : j ≤ s)
    (hpos : 0 < i ∨ 0 < j) :
    (6 * (s : ℝ) + 3 + (i : ℝ)) <
        Real.sqrt (12 * (partialN s i j : ℝ) - 3) ∧
      Real.sqrt (12 * (partialN s i j : ℝ) - 3) <
        (6 * (s : ℝ) + 4 + (i : ℝ)) := by
  let A : ℝ := 12 * (partialN s i j : ℝ) - 3
  let lo : ℝ := 6 * (s : ℝ) + 3 + (i : ℝ)
  let hiR : ℝ := 6 * (s : ℝ) + 4 + (i : ℝ)
  have hi_cast : (i : ℝ) ≤ 5 := by exact_mod_cast hi
  have hj_cast : (j : ℝ) ≤ (s : ℝ) := by exact_mod_cast hj
  have hi_nonneg : (0 : ℝ) ≤ i := by positivity
  have hj_nonneg : (0 : ℝ) ≤ j := by positivity
  have hs_nonneg : (0 : ℝ) ≤ s := by positivity
  have h_hi_diff :
      hiR ^ 2 - A = ((i : ℝ) - 2) ^ 2 + 3 + 12 * ((s : ℝ) - (j : ℝ)) := by
    dsimp [hiR, A]
    norm_num [partialN, shellN]
    ring
  have h_lo_diff :
      A - lo ^ 2 = (i : ℝ) * (6 - (i : ℝ)) + 12 * (j : ℝ) := by
    dsimp [lo, A]
    norm_num [partialN, shellN]
    ring
  have h_hi_sq : A < hiR ^ 2 := by
    nlinarith [sq_nonneg ((i : ℝ) - 2)]
  have h_lo_rhs_pos : 0 < (i : ℝ) * (6 - (i : ℝ)) + 12 * (j : ℝ) := by
    rcases hpos with hi_pos | hj_pos
    · have hi_pos_cast : (0 : ℝ) < i := by exact_mod_cast hi_pos
      have hsix : (0 : ℝ) < 6 - (i : ℝ) := by nlinarith
      have hmul : 0 < (i : ℝ) * (6 - (i : ℝ)) := mul_pos hi_pos_cast hsix
      nlinarith
    · have hj_pos_cast : (0 : ℝ) < j := by exact_mod_cast hj_pos
      have hsix : (0 : ℝ) ≤ 6 - (i : ℝ) := by nlinarith
      have hmul : 0 ≤ (i : ℝ) * (6 - (i : ℝ)) := mul_nonneg hi_nonneg hsix
      nlinarith
  have h_lo_sq : lo ^ 2 < A := by nlinarith
  have hn : 1 ≤ partialN s i j := by
    unfold partialN shellN
    omega
  have hA : 0 ≤ A := by
    dsimp [A]
    have hn_cast : (1 : ℝ) ≤ partialN s i j := by exact_mod_cast hn
    nlinarith
  have hlo_nonneg : 0 ≤ lo := by
    dsimp [lo]
    positivity
  have hhi_nonneg : 0 ≤ hiR := by
    dsimp [hiR]
    positivity
  have hsqrt_sq : Real.sqrt A ^ 2 = A := Real.sq_sqrt hA
  have hsqrt_nonneg : 0 ≤ Real.sqrt A := Real.sqrt_nonneg A
  constructor
  · change lo < Real.sqrt A
    nlinarith
  · change Real.sqrt A < hiR
    nlinarith

/-- Exact floor identity for every nonempty partial shell. -/
theorem floor_harborthReal_partial (s i j : ℕ) (hi : i ≤ 5) (hj : j ≤ s)
    (hpos : 0 < i ∨ 0 < j) :
    ⌊harborthReal (partialN s i j)⌋ = partialZ s i j := by
  have hwindow := partial_sqrt_window s i j hi hj hpos
  have hlink :
      3 * (partialN s i j : ℝ) - (partialZ s i j : ℝ) =
        6 * (s : ℝ) + 4 + (i : ℝ) := by
    norm_num [partialN, shellN, partialZ]
    ring
  apply Int.floor_eq_iff.mpr
  constructor
  · dsimp [harborthReal]
    nlinarith
  · dsimp [harborthReal]
    norm_num
    nlinarith

end PlanarContactNumber

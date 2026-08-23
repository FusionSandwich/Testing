import PlanarContactNumber.HarborthArithmetic

namespace PlanarContactNumber

/-- A radicand occurring in Harborth's expression is nonnegative as soon as
there is at least one point. -/
theorem harborth_radicand_nonneg (n : ℕ) (hn : 1 ≤ n) :
    0 ≤ 12 * (n : ℝ) - 3 := by
  have hn' : (1 : ℝ) ≤ n := by exact_mod_cast hn
  nlinarith

/-- The square root of a Harborth radicand is at least three. -/
theorem three_le_sqrt_harborth_radicand (n : ℕ) (hn : 1 ≤ n) :
    3 ≤ Real.sqrt (12 * (n : ℝ) - 3) := by
  have hrad := harborth_radicand_nonneg n hn
  have hn' : (1 : ℝ) ≤ n := by exact_mod_cast hn
  have hsquare := Real.sq_sqrt hrad
  have hsqrt := Real.sqrt_nonneg (12 * (n : ℝ) - 3)
  nlinarith

/-- The square-root inequality used when two disconnected components are
merged in the induction. -/
theorem sqrt_merge_three {x y : ℝ} (hx : 9 ≤ x) (hy : 9 ≤ y) :
    Real.sqrt (x + y + 3) ≤ Real.sqrt x + Real.sqrt y := by
  have hx0 : 0 ≤ x := le_trans (by norm_num) hx
  have hy0 : 0 ≤ y := le_trans (by norm_num) hy
  have hxy0 : 0 ≤ x + y + 3 := by nlinarith
  have hsx0 := Real.sqrt_nonneg x
  have hsy0 := Real.sqrt_nonneg y
  have hst0 := Real.sqrt_nonneg (x + y + 3)
  have hsx2 := Real.sq_sqrt hx0
  have hsy2 := Real.sq_sqrt hy0
  have hst2 := Real.sq_sqrt hxy0
  have hsx3 : 3 ≤ Real.sqrt x := by nlinarith
  have hsy3 : 3 ≤ Real.sqrt y := by nlinarith
  have hprod :
      0 ≤ (Real.sqrt x - 3) * (Real.sqrt y - 3) :=
    mul_nonneg (sub_nonneg.mpr hsx3) (sub_nonneg.mpr hsy3)
  nlinarith

/-- The square-root inequality used at a cut vertex. -/
theorem sqrt_cut_merge {x y : ℝ} (hx : 9 ≤ x) (hy : 9 ≤ y) :
    3 + Real.sqrt (x + y - 9) ≤ Real.sqrt x + Real.sqrt y := by
  have hx0 : 0 ≤ x := le_trans (by norm_num) hx
  have hy0 : 0 ≤ y := le_trans (by norm_num) hy
  have hxy0 : 0 ≤ x + y - 9 := by nlinarith
  have hsx0 := Real.sqrt_nonneg x
  have hsy0 := Real.sqrt_nonneg y
  have hst0 := Real.sqrt_nonneg (x + y - 9)
  have hsx2 := Real.sq_sqrt hx0
  have hsy2 := Real.sq_sqrt hy0
  have hst2 := Real.sq_sqrt hxy0
  have hsx3 : 3 ≤ Real.sqrt x := by nlinarith
  have hsy3 : 3 ≤ Real.sqrt y := by nlinarith
  have hprod :
      0 ≤ (Real.sqrt x - 3) * (Real.sqrt y - 3) :=
    mul_nonneg (sub_nonneg.mpr hsx3) (sub_nonneg.mpr hsy3)
  nlinarith

/-- Harborth's real expression is superadditive on positive integers. This is
exactly the inequality required for a disconnected contact graph. -/
theorem harborthReal_add_le (a b : ℕ) (ha : 1 ≤ a) (hb : 1 ≤ b) :
    harborthReal a + harborthReal b ≤ harborthReal (a + b) := by
  have hxa : (9 : ℝ) ≤ 12 * (a : ℝ) - 3 := by
    have ha' : (1 : ℝ) ≤ a := by exact_mod_cast ha
    nlinarith
  have hyb : (9 : ℝ) ≤ 12 * (b : ℝ) - 3 := by
    have hb' : (1 : ℝ) ≤ b := by exact_mod_cast hb
    nlinarith
  have hmerge := sqrt_merge_three hxa hyb
  have hrad :
      12 * ((a + b : ℕ) : ℝ) - 3 =
        (12 * (a : ℝ) - 3) + (12 * (b : ℝ) - 3) + 3 := by
    push_cast
    ring
  rw [harborthReal, harborthReal, harborthReal, hrad]
  push_cast
  nlinarith

/-- If two positive induced subconfigurations overlap in one cut vertex, their
Harborth bounds add to at most the bound for the union. -/
theorem harborthReal_cut_le {a b n : ℕ} (ha : 1 ≤ a) (hb : 1 ≤ b)
    (hsum : a + b = n + 1) :
    harborthReal a + harborthReal b ≤ harborthReal n := by
  have hxa : (9 : ℝ) ≤ 12 * (a : ℝ) - 3 := by
    have ha' : (1 : ℝ) ≤ a := by exact_mod_cast ha
    nlinarith
  have hyb : (9 : ℝ) ≤ 12 * (b : ℝ) - 3 := by
    have hb' : (1 : ℝ) ≤ b := by exact_mod_cast hb
    nlinarith
  have hmerge := sqrt_cut_merge hxa hyb
  have hsum' : (a : ℝ) + (b : ℝ) = (n : ℝ) + 1 := by
    exact_mod_cast hsum
  have hrad :
      12 * (n : ℝ) - 3 =
        (12 * (a : ℝ) - 3) + (12 * (b : ℝ) - 3) - 9 := by
    nlinarith
  rw [harborthReal, harborthReal, harborthReal, hrad]
  nlinarith

/-- Algebraic closure of the two inequalities in the nonempty-interior case
of Harborth's induction.

`m ≥ e - 2n + 3` comes from the degree sum.  The second hypothesis comes from
deleting the outer boundary and applying the induction hypothesis to the `m`
remaining points. -/
theorem interior_induction_closure {n e m : ℝ}
    (hn : 1 ≤ n) (hm : 1 ≤ m)
    (hdegree : e - 2 * n + 3 ≤ m)
    (hdelete : e ≤ 3 * n - 6 - Real.sqrt (12 * m - 3)) :
    e ≤ 3 * n - Real.sqrt (12 * n - 3) := by
  have hmrad : 0 ≤ 12 * m - 3 := by nlinarith
  have hnrad : 0 ≤ 12 * n - 3 := by nlinarith
  have hsm0 := Real.sqrt_nonneg (12 * m - 3)
  have hsn0 := Real.sqrt_nonneg (12 * n - 3)
  have hsm2 := Real.sq_sqrt hmrad
  have hsn2 := Real.sq_sqrt hnrad
  let y : ℝ := 3 * n - e
  have hy : 6 + Real.sqrt (12 * m - 3) ≤ y := by
    dsimp [y]
    nlinarith
  have hminus : 0 ≤ y - 6 - Real.sqrt (12 * m - 3) := by nlinarith
  have hplus : 0 ≤ y - 6 + Real.sqrt (12 * m - 3) := by nlinarith
  have hprod :
      0 ≤ (y - 6 - Real.sqrt (12 * m - 3)) *
        (y - 6 + Real.sqrt (12 * m - 3)) :=
    mul_nonneg hminus hplus
  have hy_sq : 12 * m - 3 ≤ (y - 6) ^ 2 := by
    nlinarith
  have htarget_sq : 12 * n - 3 ≤ y ^ 2 := by
    dsimp [y] at hdegree
    nlinarith
  have hy0 : 0 ≤ y := by nlinarith
  have hsqrt_le : Real.sqrt (12 * n - 3) ≤ y := by
    nlinarith
  dsimp [y] at hsqrt_le ⊢
  nlinarith

/-- Algebraic closure when the chosen outer boundary contains every vertex.
The correct boundary estimate is `2e ≤ 4n - 6`; the weaker planar estimate
`e ≤ 3n - 6` is not sufficient here. -/
theorem boundary_only_closure {n e : ℝ} (hn : 3 ≤ n)
    (hdegree : 2 * e ≤ 4 * n - 6) :
    e ≤ 3 * n - Real.sqrt (12 * n - 3) := by
  have hnrad : 0 ≤ 12 * n - 3 := by nlinarith
  have hsn0 := Real.sqrt_nonneg (12 * n - 3)
  have hsn2 := Real.sq_sqrt hnrad
  have hsquare : 12 * n - 3 < (n + 3) ^ 2 := by
    nlinarith [sq_nonneg (n - 3)]
  have hsqrt_lt : Real.sqrt (12 * n - 3) < n + 3 := by
    nlinarith
  nlinarith

end PlanarContactNumber

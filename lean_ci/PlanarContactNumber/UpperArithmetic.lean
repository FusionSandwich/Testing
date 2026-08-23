import PlanarContactNumber.HarborthArithmetic

namespace PlanarContactNumber

/-- Positivity of the radicand on the domain of the theorem. -/
theorem harborth_radicand_nonneg {n : ℕ} (hn : 1 ≤ n) :
    0 ≤ 12 * (n : ℝ) - 3 := by
  have hnR : (1 : ℝ) ≤ n := by exact_mod_cast hn
  nlinarith

/-- The Harborth real expression is nonnegative for `n ≥ 1`. -/
theorem harborthReal_nonneg {n : ℕ} (hn : 1 ≤ n) : 0 ≤ harborthReal n := by
  have hnR : (1 : ℝ) ≤ n := by exact_mod_cast hn
  have hrad := harborth_radicand_nonneg hn
  have hs := Real.sq_sqrt hrad
  have hs0 := Real.sqrt_nonneg (12 * (n : ℝ) - 3)
  dsimp [harborthReal]
  nlinarith [mul_nonneg (sub_nonneg.mpr hnR) (by nlinarith : 0 ≤ 3 * (n : ℝ) - 1)]

@[simp] theorem harborthReal_one : harborthReal 1 = 0 := by
  norm_num [harborthReal]

/-- The two-point base value dominates its unique possible contact. -/
theorem one_le_harborthReal_two : (1 : ℝ) ≤ harborthReal 2 := by
  have hs : Real.sqrt (21 : ℝ) ^ 2 = 21 := Real.sq_sqrt (by norm_num)
  have hs0 : 0 ≤ Real.sqrt (21 : ℝ) := Real.sqrt_nonneg 21
  norm_num [harborthReal]
  nlinarith

/-- Superadditivity needed when a contact graph is disconnected. -/
theorem harborthReal_disjoint_superadditive {m k : ℕ} (hm : 1 ≤ m) (hk : 1 ≤ k) :
    harborthReal m + harborthReal k ≤ harborthReal (m + k) := by
  let A : ℝ := 12 * (m : ℝ) - 3
  let B : ℝ := 12 * (k : ℝ) - 3
  let C : ℝ := 12 * ((m + k : ℕ) : ℝ) - 3
  have hA : 0 ≤ A := by
    dsimp [A]
    exact harborth_radicand_nonneg hm
  have hB : 0 ≤ B := by
    dsimp [B]
    exact harborth_radicand_nonneg hk
  have hC : 0 ≤ C := by
    dsimp [C]
    exact harborth_radicand_nonneg (by omega)
  have hAsq : Real.sqrt A ^ 2 = A := Real.sq_sqrt hA
  have hBsq : Real.sqrt B ^ 2 = B := Real.sq_sqrt hB
  have hCsq : Real.sqrt C ^ 2 = C := Real.sq_sqrt hC
  have hA0 : 0 ≤ Real.sqrt A := Real.sqrt_nonneg A
  have hB0 : 0 ≤ Real.sqrt B := Real.sqrt_nonneg B
  have hC0 : 0 ≤ Real.sqrt C := Real.sqrt_nonneg C
  have hmR : (1 : ℝ) ≤ m := by exact_mod_cast hm
  have hkR : (1 : ℝ) ≤ k := by exact_mod_cast hk
  have hA9 : 9 ≤ A := by dsimp [A]; nlinarith
  have hB9 : 9 ≤ B := by dsimp [B]; nlinarith
  have hsA3 : 3 ≤ Real.sqrt A := by nlinarith
  have hsB3 : 3 ≤ Real.sqrt B := by nlinarith
  have hCrel : C = A + B + 3 := by
    dsimp [A, B, C]
    norm_num
    ring
  have hsumsq : C ≤ (Real.sqrt A + Real.sqrt B) ^ 2 := by
    rw [hCrel]
    nlinarith [mul_nonneg hA0 hB0]
  have hsqrt : Real.sqrt C ≤ Real.sqrt A + Real.sqrt B := by
    nlinarith [sq_nonneg (Real.sqrt C - (Real.sqrt A + Real.sqrt B))]
  dsimp [harborthReal, A, B, C] at *
  norm_num at *
  nlinarith

/-- Superadditivity needed when two induced subconfigurations meet in one cut vertex. -/
theorem harborthReal_cut_superadditive {m k n : ℕ} (hm : 2 ≤ m) (hk : 2 ≤ k)
    (hsize : n + 1 = m + k) :
    harborthReal m + harborthReal k ≤ harborthReal n := by
  have hn : 1 ≤ n := by omega
  let A : ℝ := 12 * (m : ℝ) - 3
  let B : ℝ := 12 * (k : ℝ) - 3
  let C : ℝ := 12 * (n : ℝ) - 3
  have hA : 0 ≤ A := by
    dsimp [A]
    exact harborth_radicand_nonneg (by omega)
  have hB : 0 ≤ B := by
    dsimp [B]
    exact harborth_radicand_nonneg (by omega)
  have hC : 0 ≤ C := by
    dsimp [C]
    exact harborth_radicand_nonneg hn
  have hAsq : Real.sqrt A ^ 2 = A := Real.sq_sqrt hA
  have hBsq : Real.sqrt B ^ 2 = B := Real.sq_sqrt hB
  have hCsq : Real.sqrt C ^ 2 = C := Real.sq_sqrt hC
  have hA0 : 0 ≤ Real.sqrt A := Real.sqrt_nonneg A
  have hB0 : 0 ≤ Real.sqrt B := Real.sqrt_nonneg B
  have hC0 : 0 ≤ Real.sqrt C := Real.sqrt_nonneg C
  have hmR : (2 : ℝ) ≤ m := by exact_mod_cast hm
  have hkR : (2 : ℝ) ≤ k := by exact_mod_cast hk
  have hA21 : 21 ≤ A := by dsimp [A]; nlinarith
  have hB21 : 21 ≤ B := by dsimp [B]; nlinarith
  have hsA3 : 3 ≤ Real.sqrt A := by nlinarith
  have hsB3 : 3 ≤ Real.sqrt B := by nlinarith
  have hsizeR : (n : ℝ) + 1 = (m : ℝ) + (k : ℝ) := by exact_mod_cast hsize
  have hCrel : C = A + B - 9 := by
    dsimp [A, B, C]
    nlinarith
  have hprod : 0 ≤ (Real.sqrt A - 3) * (Real.sqrt B - 3) :=
    mul_nonneg (sub_nonneg.mpr hsA3) (sub_nonneg.mpr hsB3)
  have hsumsq : C ≤ (Real.sqrt A + Real.sqrt B - 3) ^ 2 := by
    rw [hCrel]
    nlinarith
  have hsum0 : 0 ≤ Real.sqrt A + Real.sqrt B - 3 := by nlinarith
  have hsqrt : Real.sqrt C ≤ Real.sqrt A + Real.sqrt B - 3 := by
    nlinarith [sq_nonneg (Real.sqrt C - (Real.sqrt A + Real.sqrt B - 3))]
  dsimp [harborthReal, A, B, C] at *
  nlinarith

/-- The `t=0` numerical branch of Harborth's boundary induction. -/
theorem harborth_boundary_step_zero {n e : ℕ} (hn : 3 ≤ n)
    (hdegree : e + 3 ≤ 2 * n) :
    (e : ℝ) ≤ harborthReal n := by
  have hn1 : 1 ≤ n := by omega
  have hnR : (3 : ℝ) ≤ n := by exact_mod_cast hn
  have heR : (e : ℝ) + 3 ≤ 2 * (n : ℝ) := by exact_mod_cast hdegree
  have hrad := harborth_radicand_nonneg hn1
  have hs := Real.sq_sqrt hrad
  have hs0 := Real.sqrt_nonneg (12 * (n : ℝ) - 3)
  have hsqrt_le : Real.sqrt (12 * (n : ℝ) - 3) ≤ (n : ℝ) + 3 := by
    nlinarith [sq_nonneg ((n : ℝ) - 3)]
  dsimp [harborthReal]
  nlinarith

/-- The `t>0` numerical branch of Harborth's boundary induction. -/
theorem harborth_boundary_step_pos {n e a t et : ℕ}
    (hsize : n = a + t) (ha : 3 ≤ a) (ht : 1 ≤ t)
    (hdegree : e + 3 ≤ 2 * n + t)
    (hremove : e + 6 ≤ et + 3 * a)
    (hind : (et : ℝ) ≤ harborthReal t) :
    (e : ℝ) ≤ harborthReal n := by
  have hn : 1 ≤ n := by omega
  have hsizeR : (n : ℝ) = (a : ℝ) + (t : ℝ) := by exact_mod_cast hsize
  have haR : (3 : ℝ) ≤ a := by exact_mod_cast ha
  have htR : (1 : ℝ) ≤ t := by exact_mod_cast ht
  have hdegreeR : (e : ℝ) + 3 ≤ 2 * (n : ℝ) + (t : ℝ) := by exact_mod_cast hdegree
  have hremoveR : (e : ℝ) + 6 ≤ (et : ℝ) + 3 * (a : ℝ) := by exact_mod_cast hremove
  let At : ℝ := 12 * (t : ℝ) - 3
  let An : ℝ := 12 * (n : ℝ) - 3
  have hAt : 0 ≤ At := by
    dsimp [At]
    exact harborth_radicand_nonneg ht
  have hAn : 0 ≤ An := by
    dsimp [An]
    exact harborth_radicand_nonneg hn
  have hAtsq : Real.sqrt At ^ 2 = At := Real.sq_sqrt hAt
  have hAnsq : Real.sqrt An ^ 2 = An := Real.sq_sqrt hAn
  have hAt0 : 0 ≤ Real.sqrt At := Real.sqrt_nonneg At
  have hAn0 : 0 ≤ Real.sqrt An := Real.sqrt_nonneg An
  have hind' : (et : ℝ) ≤ 3 * (t : ℝ) - Real.sqrt At := by
    simpa [harborthReal, At] using hind
  let y : ℝ := 3 * (n : ℝ) - (e : ℝ)
  have hy : 6 + Real.sqrt At ≤ y := by
    dsimp [y]
    nlinarith
  have ht_lower : (n : ℝ) - y + 3 ≤ (t : ℝ) := by
    dsimp [y]
    nlinarith
  have hy6 : 0 ≤ y - 6 := by nlinarith
  have hsq1 : At ≤ (y - 6) ^ 2 := by
    nlinarith [sq_nonneg ((y - 6) - Real.sqrt At)]
  have hlin : An ≤ At + 12 * y - 36 := by
    dsimp [At, An]
    nlinarith
  have hpoly : At + 12 * y - 36 ≤ y ^ 2 := by
    nlinarith
  have hsq2 : An ≤ y ^ 2 := hlin.trans hpoly
  have hy0 : 0 ≤ y := by nlinarith
  have hsqrt_le : Real.sqrt An ≤ y := by
    nlinarith [sq_nonneg (Real.sqrt An - y)]
  dsimp [harborthReal]
  dsimp [An, y] at hsqrt_le
  nlinarith

/-- Convert a real upper bound on an integer contact count into the exact floor bound. -/
theorem int_le_floor_harborth {n e : ℕ} (h : (e : ℝ) ≤ harborthReal n) :
    (e : ℤ) ≤ ⌊harborthReal n⌋ := by
  exact Int.le_floor.mpr (by simpa using h)

end PlanarContactNumber

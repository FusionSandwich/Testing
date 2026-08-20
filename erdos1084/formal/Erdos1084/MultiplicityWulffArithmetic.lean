import Mathlib

namespace Erdos1084

/-!
# Arithmetic spine for the developed-multiplicity FCC lower bound

A compatible coherent grain complex can be developed into one reference FCC
orientation while retaining overlaps as an integer multiplicity.  Anisotropic
coarea reduces the sharp lower bound to the finite power inequality

`(sum x_i^3)^2 <= (sum x_i^2)^3`.

This module proves that inequality by Cauchy--Schwarz, records the exact two-level
factorization, packages the finite Wulff-energy assembly, and checks the FCC
coefficient cube `432`.  BV coarea, the Wulff inequality, and existence of the
geometric development remain the explicit analytic inputs.
-/

open scoped BigOperators

/-- Exact two-level factorization behind `2/3`-power subadditivity. -/
theorem multiplicity_twoLevel_factorization (x y : ℝ) :
    (x ^ 2 + y ^ 2) ^ 3 - (x ^ 3 + y ^ 3) ^ 2 =
      x ^ 2 * y ^ 2 * (3 * x ^ 2 - 2 * x * y + 3 * y ^ 2) := by
  ring

/-- The quadratic factor in the two-level identity is nonnegative. -/
theorem multiplicity_quadraticFactor_nonneg (x y : ℝ) :
    0 ≤ 3 * x ^ 2 - 2 * x * y + 3 * y ^ 2 := by
  nlinarith [sq_nonneg (x - y), sq_nonneg x, sq_nonneg y]

/-- Exact two-level cube inequality. -/
theorem multiplicity_twoLevel_cube_bound (x y : ℝ) :
    (x ^ 3 + y ^ 3) ^ 2 ≤ (x ^ 2 + y ^ 2) ^ 3 := by
  rw [← sub_nonneg]
  rw [multiplicity_twoLevel_factorization]
  positivity

/--
Finite `l^3` to `l^2` power comparison:
`(sum x_i^3)^2 <= (sum x_i^2)^3`.
-/
theorem multiplicity_finset_cube_bound
    {ι : Type*} (s : Finset ι) (x : ι → ℝ) :
    (∑ i in s, x i ^ 3) ^ 2 ≤ (∑ i in s, x i ^ 2) ^ 3 := by
  have hcs := Finset.sum_mul_sq_le_sq_mul_sq s
    (fun i => x i ^ 2) x
  have hsum4 :
      (∑ i in s, (x i ^ 2) ^ 2) ≤
        (∑ i in s, x i ^ 2) ^ 2 := by
    exact Finset.sum_sq_le_sq_sum_of_nonneg
      (fun i hi => sq_nonneg (x i))
  have hsum2 : 0 ≤ ∑ i in s, x i ^ 2 := by
    exact Finset.sum_nonneg fun i hi => sq_nonneg (x i)
  calc
    (∑ i in s, x i ^ 3) ^ 2 =
        (∑ i in s, (x i ^ 2) * x i) ^ 2 := by
      congr 2
      apply Finset.sum_congr rfl
      intro i hi
      ring
    _ ≤ (∑ i in s, (x i ^ 2) ^ 2) *
          (∑ i in s, x i ^ 2) := hcs
    _ ≤ (∑ i in s, x i ^ 2) ^ 2 *
          (∑ i in s, x i ^ 2) :=
      mul_le_mul_of_nonneg_right hsum4 hsum2
    _ = (∑ i in s, x i ^ 2) ^ 3 := by ring

/-- Cubing is order-reflecting on nonnegative real numbers. -/
theorem nonneg_le_of_cube_le_cube
    {a b : ℝ} (ha : 0 ≤ a) (hb : 0 ≤ b)
    (h : a ^ 3 ≤ b ^ 3) : a ≤ b := by
  by_contra hnot
  have hba : b < a := lt_of_not_ge hnot
  have haPos : 0 < a := lt_of_le_of_lt hb hba
  have hfactorPos : 0 < b ^ 2 + a * b + a ^ 2 := by
    nlinarith [sq_pos_of_pos haPos, sq_nonneg b]
  have hdiff : b ^ 3 - a ^ 3 < 0 := by
    calc
      b ^ 3 - a ^ 3 = (b - a) * (b ^ 2 + a * b + a ^ 2) := by ring
      _ < 0 := mul_neg_of_neg_of_pos (sub_neg.mpr hba) hfactorPos
  linarith

/--
Cube-root coordinate form of finite `2/3`-power subadditivity.
If `totalRoot^3` is the sum of the level cubes, then its square is at most the
sum of the level squares.
-/
theorem multiplicity_totalRoot_square_le
    {ι : Type*} (s : Finset ι) (root : ι → ℝ) (totalRoot : ℝ)
    (hroot : ∀ i ∈ s, 0 ≤ root i)
    (htotal : totalRoot ^ 3 = ∑ i in s, root i ^ 3)
    (htotalNonneg : 0 ≤ totalRoot) :
    totalRoot ^ 2 ≤ ∑ i in s, root i ^ 2 := by
  let sumSq : ℝ := ∑ i in s, root i ^ 2
  have hsumSq : 0 ≤ sumSq := by
    dsimp [sumSq]
    exact Finset.sum_nonneg fun i hi => sq_nonneg (root i)
  have hcube : (totalRoot ^ 2) ^ 3 ≤ sumSq ^ 3 := by
    calc
      (totalRoot ^ 2) ^ 3 = (totalRoot ^ 3) ^ 2 := by ring
      _ = (∑ i in s, root i ^ 3) ^ 2 := by rw [htotal]
      _ ≤ (∑ i in s, root i ^ 2) ^ 3 :=
        multiplicity_finset_cube_bound s root
      _ = sumSq ^ 3 := rfl
  exact nonneg_le_of_cube_le_cube (sq_nonneg totalRoot) hsumSq hcube

/--
Finite developed-multiplicity Wulff assembly.  Each level has energy at least
`C*root_i^2`, the total mass root cubes to the sum of level masses, and therefore
the total energy is at least `C*totalRoot^2`.
-/
theorem multiplicity_wulff_energy_assembly
    {ι : Type*} (s : Finset ι)
    (root energy : ι → ℝ) (totalRoot C : ℝ)
    (hroot : ∀ i ∈ s, 0 ≤ root i)
    (hC : 0 ≤ C)
    (hlevel : ∀ i ∈ s, C * root i ^ 2 ≤ energy i)
    (htotal : totalRoot ^ 3 = ∑ i in s, root i ^ 3)
    (htotalNonneg : 0 ≤ totalRoot) :
    C * totalRoot ^ 2 ≤ ∑ i in s, energy i := by
  have hrootSq := multiplicity_totalRoot_square_le
    s root totalRoot hroot htotal htotalNonneg
  have hscaled : C * totalRoot ^ 2 ≤ C * ∑ i in s, root i ^ 2 :=
    mul_le_mul_of_nonneg_left hrootSq hC
  have hlevels : C * ∑ i in s, root i ^ 2 ≤ ∑ i in s, energy i := by
    calc
      C * ∑ i in s, root i ^ 2 = ∑ i in s, C * root i ^ 2 := by
        rw [Finset.mul_sum]
      _ ≤ ∑ i in s, energy i := by
        exact Finset.sum_le_sum hlevel
  exact hscaled.trans hlevels

/-- Exact particle-coefficient cube from Wulff volume `32` and particle volume `1/sqrt(2)`. -/
theorem developedMultiplicity_fcc_coefficient_cube :
    (27 : ℝ) * 32 * (1 / 2) = 432 := by
  norm_num

end Erdos1084

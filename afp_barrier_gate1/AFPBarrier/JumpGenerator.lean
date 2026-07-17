import Mathlib.Algebra.Order.BigOperators.Ring.Finset
import Mathlib.Tactic

/-!
# Finite jump generators

This module formalizes the algebraic identities used in the AFP monotonicity
barrier. Rates are stored only on the off-diagonal finite set
`Finset.univ.erase i`, so the hypotheses match the usual nonnegative
transition-rate convention.
-/

open scoped BigOperators

namespace AFPBarrier

variable {ι : Type*} [Fintype ι] [DecidableEq ι]

/-- All states other than `i`. -/
def offdiag (i : ι) : Finset ι := Finset.univ.erase i

/-- A finite-state jump generator. -/
def jumpGenerator (a : ι → ι → ℝ) (f : ι → ℝ) (i : ι) : ℝ :=
  ∑ j in offdiag i, a i j * (f j - f i)

/-- Total outgoing jump rate at `i`. -/
def jumpRate (a : ι → ι → ℝ) (i : ι) : ℝ :=
  ∑ j in offdiag i, a i j

/-- The pointwise carré du champ of a finite jump generator. -/
def carreDuChamp (a : ι → ι → ℝ) (f : ι → ℝ) (i : ι) : ℝ :=
  ∑ j in offdiag i, a i j * (f j - f i) ^ 2

@[simp] theorem jumpGenerator_const
    (a : ι → ι → ℝ) (c : ℝ) (i : ι) :
    jumpGenerator a (fun _ => c) i = 0 := by
  simp [jumpGenerator]

/-- Adding a constant does not change a jump generator. -/
theorem jumpGenerator_add_const
    (a : ι → ι → ℝ) (f : ι → ℝ) (c : ℝ) (i : ι) :
    jumpGenerator a (fun j => f j + c) i = jumpGenerator a f i := by
  simp [jumpGenerator]

/-- Subtracting a constant does not change a jump generator. -/
theorem jumpGenerator_sub_const
    (a : ι → ι → ℝ) (f : ι → ℝ) (c : ℝ) (i : ι) :
    jumpGenerator a (fun j => f j - c) i = jumpGenerator a f i := by
  simp [jumpGenerator]

/-- Exact finite-state carré-du-champ identity. -/
theorem jumpGenerator_square_identity
    (a : ι → ι → ℝ) (f : ι → ℝ) (i : ι) :
    jumpGenerator a (fun j => (f j) ^ 2) i
          - 2 * f i * jumpGenerator a f i
      = carreDuChamp a f i := by
  classical
  simp only [jumpGenerator, carreDuChamp]
  rw [Finset.mul_sum]
  rw [← Finset.sum_sub_distrib]
  apply Finset.sum_congr rfl
  intro j hj
  ring

/-- The total rate is nonnegative when every off-diagonal rate is. -/
theorem jumpRate_nonneg
    (a : ι → ι → ℝ) (i : ι)
    (ha : ∀ j, j ≠ i → 0 ≤ a i j) :
    0 ≤ jumpRate a i := by
  unfold jumpRate
  apply Finset.sum_nonneg
  intro j hj
  exact ha j (Finset.mem_erase.mp hj).1

/-- The carré du champ is nonnegative for nonnegative rates. -/
theorem carreDuChamp_nonneg
    (a : ι → ι → ℝ) (f : ι → ℝ) (i : ι)
    (ha : ∀ j, j ≠ i → 0 ≤ a i j) :
    0 ≤ carreDuChamp a f i := by
  unfold carreDuChamp
  apply Finset.sum_nonneg
  intro j hj
  exact mul_nonneg (ha j (Finset.mem_erase.mp hj).1) (sq_nonneg (f j - f i))

/-- Weighted finite Cauchy-Schwarz: drift squared is bounded by
rate times carré du champ. -/
theorem jumpGenerator_sq_le_rate_mul_carre
    (a : ι → ι → ℝ) (f : ι → ℝ) (i : ι)
    (ha : ∀ j, j ≠ i → 0 ≤ a i j) :
    (jumpGenerator a f i) ^ 2 ≤ jumpRate a i * carreDuChamp a f i := by
  classical
  have h := Finset.sum_sq_le_sum_mul_sum_of_sq_le_mul
    (offdiag i)
    (r := fun j => a i j * (f j - f i))
    (f := fun j => a i j)
    (g := fun j => a i j * (f j - f i) ^ 2)
    (fun j hj => ha j (Finset.mem_erase.mp hj).1)
    (fun j hj =>
      mul_nonneg (ha j (Finset.mem_erase.mp hj).1) (sq_nonneg (f j - f i)))
    (fun j hj => by ring)
  simpa [jumpGenerator, jumpRate, carreDuChamp] using h

/-- If the carré du champ vanishes, then the generator vanishes on that
function at the same state. -/
theorem zero_carreDuChamp_forces_generator_zero
    (a : ι → ι → ℝ) (f : ι → ℝ) (i : ι)
    (ha : ∀ j, j ≠ i → 0 ≤ a i j)
    (hzero : carreDuChamp a f i = 0) :
    jumpGenerator a f i = 0 := by
  have hcs := jumpGenerator_sq_le_rate_mul_carre
    (a := a) (f := f) (i := i) ha
  rw [hzero] at hcs
  have hsquare : (jumpGenerator a f i) ^ 2 = 0 := by
    apply le_antisymm
    · simpa using hcs
    · exact sq_nonneg _
  exact sq_eq_zero_iff.mp hsquare

end AFPBarrier

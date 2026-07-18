import AFPBarrier.ReversibleConductance

/-!
# The matrix convention used in Radiant

The AFP implementation stores an unshifted row matrix with off-diagonal entry
`gamma i j / w i` and diagonal equal to minus the outgoing row sum. It then
adds a scalar diagonal shift `lambda0` to the scattering matrix and adds the
same scalar times the momentum-transfer coefficient to the total cross
section. The two shifts cancel in the transport equation.

This module formalizes those two algebraic facts.
-/

open scoped BigOperators

namespace AFPBarrier

variable {ι : Type*} [Fintype ι] [DecidableEq ι]

/-- Action of a finite row matrix on a sampled function. -/
def matrixAction (M : ι → ι → ℝ) (f : ι → ℝ) (i : ι) : ℝ :=
  Finset.univ.sum (fun j => M i j * f j)

/-- The unshifted row matrix associated with shared-edge conductances. -/
noncomputable def conductanceMatrix
    (γ : ι → ι → ℝ) (w : ι → ℝ) (i j : ι) : ℝ :=
  if j = i then
    -(offdiag i).sum (fun k => conductanceRate γ w i k)
  else
    conductanceRate γ w i j

/-- The full row-matrix action equals the jump-generator action. -/
theorem matrixAction_conductanceMatrix_eq_jumpGenerator
    (γ : ι → ι → ℝ) (w f : ι → ℝ) (i : ι) :
    matrixAction (conductanceMatrix γ w) f i
      = jumpGenerator (conductanceRate γ w) f i := by
  classical
  unfold matrixAction conductanceMatrix jumpGenerator
  rw [← Finset.sum_erase_add
    Finset.univ
    (fun j => (if j = i then
      -(offdiag i).sum (fun k => conductanceRate γ w i k)
    else conductanceRate γ w i j) * f j)
    (Finset.mem_univ i)]
  simp only [if_pos, Finset.sum_erase]
  have hi : i ∉ offdiag i := by simp [offdiag]
  simp only [Finset.mem_univ, hi, not_false_eq_true]
  calc
    (offdiag i).sum
          (fun j => conductanceRate γ w i j * f j)
        + (-(offdiag i).sum
          (fun k => conductanceRate γ w i k)) * f i
        = (offdiag i).sum
          (fun j => conductanceRate γ w i j * (f j - f i)) := by
            rw [Finset.sum_sub_distrib, ← Finset.sum_mul]
            apply congrArg₂ (· + ·) ?_ ?_
            · rfl
            · ring
    _ = _ := rfl

/-- Add a scalar multiple of the identity to a matrix. -/
def diagonalShift (M : ι → ι → ℝ) (s : ℝ) (i j : ι) : ℝ :=
  M i j + if j = i then s else 0

/-- A diagonal matrix shift adds exactly `s * f i` to the row action. -/
theorem matrixAction_diagonalShift
    (M : ι → ι → ℝ) (f : ι → ℝ) (s : ℝ) (i : ι) :
    matrixAction (diagonalShift M s) f i
      = matrixAction M f i + s * f i := by
  classical
  unfold matrixAction diagonalShift
  calc
    Finset.univ.sum
        (fun j => (M i j + if j = i then s else 0) * f j)
        = Finset.univ.sum (fun j => M i j * f j)
          + Finset.univ.sum
            (fun j => (if j = i then s else 0) * f j) := by
              rw [← Finset.sum_add_distrib]
              apply Finset.sum_congr rfl
              intro j hj
              ring
    _ = Finset.univ.sum (fun j => M i j * f j) + s * f i := by
          simp

/-- The diagonal source shift and the equal removal shift cancel. -/
theorem shifted_source_minus_total_shift
    (M : ι → ι → ℝ) (f : ι → ℝ) (s : ℝ) (i : ι) :
    matrixAction (diagonalShift M s) f i - s * f i
      = matrixAction M f i := by
  rw [matrixAction_diagonalShift]
  ring

/-- In the exact form used by the implementation, the shifted scattering
matrix together with the matching total-cross-section correction recovers the
unshifted shared-edge jump generator. -/
theorem shifted_conductance_action_recovers_jumpGenerator
    (γ : ι → ι → ℝ) (w f : ι → ℝ) (s : ℝ) (i : ι) :
    matrixAction (diagonalShift (conductanceMatrix γ w) s) f i - s * f i
      = jumpGenerator (conductanceRate γ w) f i := by
  rw [shifted_source_minus_total_shift]
  exact matrixAction_conductanceMatrix_eq_jumpGenerator
    (γ := γ) (w := w) (f := f) (i := i)

end AFPBarrier

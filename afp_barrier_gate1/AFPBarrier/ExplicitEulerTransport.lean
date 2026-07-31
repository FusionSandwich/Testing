import AFPBarrier.ReversibleConductance
import Mathlib.Tactic

/-!
# Explicit-Euler transport consequences

This module connects the AFP jump-generator rate to a concrete transport time
step.  For

  u^{n+1}(i) = u^n(i) + dt * L u^n(i),

nonnegative off-diagonal rates preserve pointwise nonnegativity whenever

  dt * jumpRate(i) <= 1.

The condition is also necessary at a row: if it is violated, the nonnegative
unit mass concentrated at that row becomes negative after one step.

For reversible shared-edge conductances, the explicit-Euler update preserves
the weighted angular integral exactly.  Exact eigenmodes have the expected
one-step amplification factor `1 - dt * lam`.
-/

open scoped BigOperators

namespace AFPBarrier

variable {ι : Type*} [Fintype ι] [DecidableEq ι]

/-- One forward-Euler step for a finite jump generator. -/
def explicitEulerStep
    (a : ι → ι → ℝ) (dt : ℝ) (f : ι → ℝ) (i : ι) : ℝ :=
  f i + dt * jumpGenerator a f i

/-- Convex-combination form of one explicit-Euler row. -/
theorem explicitEulerStep_eq_self_weight_add_neighbors
    (a : ι → ι → ℝ) (dt : ℝ) (f : ι → ℝ) (i : ι) :
    explicitEulerStep a dt f i
      = (1 - dt * jumpRate a i) * f i
        + dt * (offdiag i).sum (fun j => a i j * f j) := by
  classical
  have hsum :
      (offdiag i).sum (fun j => a i j * (f j - f i))
        = (offdiag i).sum (fun j => a i j * f j)
          - (offdiag i).sum (fun j => a i j) * f i := by
    calc
      (offdiag i).sum (fun j => a i j * (f j - f i))
          = (offdiag i).sum (fun j => (a i j * f j) - (a i j * f i)) := by
              apply Finset.sum_congr rfl
              intro j hj
              ring
      _ = (offdiag i).sum (fun j => a i j * f j)
            - (offdiag i).sum (fun j => a i j * f i) := by
              rw [Finset.sum_sub_distrib]
      _ = (offdiag i).sum (fun j => a i j * f j)
            - (offdiag i).sum (fun j => a i j) * f i := by
              rw [Finset.sum_mul]
  unfold explicitEulerStep jumpGenerator jumpRate
  rw [hsum]
  ring

/-- Exact eigenmodes have the usual forward-Euler amplification factor. -/
theorem explicitEulerStep_eigenmode
    (a : ι → ι → ℝ) (dt lam : ℝ) (f : ι → ℝ) (i : ι)
    (heigen : jumpGenerator a f i = -lam * f i) :
    explicitEulerStep a dt f i = (1 - dt * lam) * f i := by
  unfold explicitEulerStep
  rw [heigen]
  ring

/-- The local CFL condition is sufficient for pointwise positivity. -/
theorem explicitEulerStep_nonneg
    (a : ι → ι → ℝ) (dt : ℝ) (f : ι → ℝ) (i : ι)
    (ha : ∀ j, j ≠ i → 0 ≤ a i j)
    (hdt : 0 ≤ dt)
    (hcfl : dt * jumpRate a i ≤ 1)
    (hf : ∀ j, 0 ≤ f j) :
    0 ≤ explicitEulerStep a dt f i := by
  rw [explicitEulerStep_eq_self_weight_add_neighbors]
  apply add_nonneg
  · exact mul_nonneg (sub_nonneg.mpr hcfl) (hf i)
  · apply mul_nonneg hdt
    apply Finset.sum_nonneg
    intro j hj
    have hji : j ≠ i := (Finset.mem_erase.mp hj).1
    exact mul_nonneg (ha j hji) (hf j)

/-- Unit mass concentrated at one state. -/
def unitAt (i : ι) (j : ι) : ℝ := if j = i then 1 else 0

@[simp] theorem unitAt_self (i : ι) : unitAt i i = 1 := by
  simp [unitAt]

@[simp] theorem unitAt_of_ne (i j : ι) (hji : j ≠ i) : unitAt i j = 0 := by
  simp [unitAt, hji]

/-- A concentrated unit mass exposes the exact diagonal Euler coefficient. -/
theorem explicitEulerStep_unitAt
    (a : ι → ι → ℝ) (dt : ℝ) (i : ι) :
    explicitEulerStep a dt (unitAt i) i = 1 - dt * jumpRate a i := by
  rw [explicitEulerStep_eq_self_weight_add_neighbors]
  have hsum : (offdiag i).sum (fun j => a i j * unitAt i j) = 0 := by
    apply Finset.sum_eq_zero
    intro j hj
    have hji : j ≠ i := (Finset.mem_erase.mp hj).1
    simp [unitAt, hji]
  rw [hsum]
  simp [unitAt]

/-- Violating the row CFL condition produces a negative value from nonnegative
initial data, so the condition is necessary for unconditional row positivity. -/
theorem explicitEulerStep_unitAt_neg_of_cfl_violation
    (a : ι → ι → ℝ) (dt : ℝ) (i : ι)
    (hcfl : 1 < dt * jumpRate a i) :
    explicitEulerStep a dt (unitAt i) i < 0 := by
  rw [explicitEulerStep_unitAt]
  linarith

/-- A reversible conductance Euler step preserves the weighted angular integral. -/
theorem weighted_sum_explicitEuler_conductanceRate
    (γ : ι → ι → ℝ) (w f : ι → ℝ) (dt : ℝ)
    (hγsymm : ∀ i j, γ i j = γ j i)
    (hw : ∀ i, w i ≠ 0) :
    Finset.univ.sum
        (fun i => w i * explicitEulerStep (conductanceRate γ w) dt f i)
      = Finset.univ.sum (fun i => w i * f i) := by
  have hconserve := weighted_sum_jumpGenerator_conductanceRate_eq_zero
    (γ := γ) (w := w) (f := f) hγsymm hw
  calc
    Finset.univ.sum
        (fun i => w i * explicitEulerStep (conductanceRate γ w) dt f i)
        = Finset.univ.sum (fun i => w i * f i)
          + dt * Finset.univ.sum
              (fun i => w i * jumpGenerator (conductanceRate γ w) f i) := by
            unfold explicitEulerStep
            rw [Finset.mul_sum]
            rw [← Finset.sum_add_distrib]
            apply Finset.sum_congr rfl
            intro i hi
            ring
    _ = Finset.univ.sum (fun i => w i * f i) := by
          rw [hconserve]
          ring

end AFPBarrier

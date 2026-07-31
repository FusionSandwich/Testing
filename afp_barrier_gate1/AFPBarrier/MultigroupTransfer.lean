import AFPBarrier.ExplicitEulerTransport
import Mathlib.Algebra.Order.BigOperators.Ring.Finset
import Mathlib.Tactic

/-!
# Conservative multigroup transfer

`T g h` is the nonnegative transfer rate from source group `g` to destination
group `h`.  The continuous group-transfer operator is

  incoming(g) - outgoing(g) * f(g).

This module verifies particle conservation, positivity of an explicit-Euler
step under the group-removal CFL condition, necessity of that condition for
unconditional positivity, and the exact energy-deposition identity.
-/

open scoped BigOperators

namespace AFPBarrier

variable {ι : Type*} [Fintype ι] [DecidableEq ι]

/-- Total transfer rate leaving one energy group. -/
def groupTransferOutRate (T : ι → ι → ℝ) (g : ι) : ℝ :=
  Finset.univ.sum (fun h => T g h)

/-- Conservative multigroup transfer operator. -/
def multigroupTransfer (T : ι → ι → ℝ) (f : ι → ℝ) (g : ι) : ℝ :=
  Finset.univ.sum (fun h => T h g * f h)
    - groupTransferOutRate T g * f g

/-- One explicit-Euler group-transfer step. -/
def multigroupEulerStep
    (T : ι → ι → ℝ) (dt : ℝ) (f : ι → ℝ) (g : ι) : ℝ :=
  f g + dt * multigroupTransfer T f g

/-- Summing the transfer operator over all groups gives zero. -/
theorem sum_multigroupTransfer_eq_zero
    (T : ι → ι → ℝ) (f : ι → ℝ) :
    Finset.univ.sum (fun g => multigroupTransfer T f g) = 0 := by
  classical
  unfold multigroupTransfer groupTransferOutRate
  rw [Finset.sum_sub_distrib]
  have hincoming :
      Finset.univ.sum
          (fun g => Finset.univ.sum (fun h => T h g * f h))
        = Finset.univ.sum
          (fun h => Finset.univ.sum (fun g => T h g) * f h) := by
    calc
      Finset.univ.sum
          (fun g => Finset.univ.sum (fun h => T h g * f h))
          = Finset.univ.sum
              (fun h => Finset.univ.sum (fun g => T h g * f h)) := by
                rw [Finset.sum_comm]
      _ = Finset.univ.sum
            (fun h => Finset.univ.sum (fun g => T h g) * f h) := by
              apply Finset.sum_congr rfl
              intro h hh
              rw [Finset.sum_mul]
  rw [hincoming]

/-- Explicit Euler written as a nonnegative incoming combination plus its
remaining diagonal coefficient. -/
theorem multigroupEulerStep_eq_positive_form
    (T : ι → ι → ℝ) (dt : ℝ) (f : ι → ℝ) (g : ι) :
    multigroupEulerStep T dt f g
      = (1 - dt * groupTransferOutRate T g) * f g
        + dt * Finset.univ.sum (fun h => T h g * f h) := by
  unfold multigroupEulerStep multigroupTransfer
  ring

/-- The group-removal CFL condition is sufficient for positivity. -/
theorem multigroupEulerStep_nonneg
    (T : ι → ι → ℝ) (dt : ℝ) (f : ι → ℝ) (g : ι)
    (hT : ∀ p q, 0 ≤ T p q)
    (hdt : 0 ≤ dt)
    (hf : ∀ p, 0 ≤ f p)
    (hcfl : dt * groupTransferOutRate T g ≤ 1) :
    0 ≤ multigroupEulerStep T dt f g := by
  rw [multigroupEulerStep_eq_positive_form]
  apply add_nonneg
  · exact mul_nonneg (sub_nonneg.mpr hcfl) (hf g)
  · apply mul_nonneg hdt
    apply Finset.sum_nonneg
    intro h hh
    exact mul_nonneg (hT h g) (hf h)

/-- A transfer Euler step conserves the unweighted total group population. -/
theorem sum_multigroupEulerStep_eq_sum
    (T : ι → ι → ℝ) (dt : ℝ) (f : ι → ℝ) :
    Finset.univ.sum (fun g => multigroupEulerStep T dt f g)
      = Finset.univ.sum f := by
  classical
  unfold multigroupEulerStep
  calc
    Finset.univ.sum (fun g => f g + dt * multigroupTransfer T f g)
        = Finset.univ.sum f
          + dt * Finset.univ.sum (fun g => multigroupTransfer T f g) := by
            rw [Finset.mul_sum]
            rw [← Finset.sum_add_distrib]
    _ = Finset.univ.sum f := by
          rw [sum_multigroupTransfer_eq_zero]
          ring

/-- With zero self-transfer, a unit population in the current group exposes the
exact outgoing diagonal coefficient. -/
theorem multigroupEulerStep_unitAt
    (T : ι → ι → ℝ) (dt : ℝ) (g : ι)
    (hdiag : T g g = 0) :
    multigroupEulerStep T dt (unitAt g) g
      = 1 - dt * groupTransferOutRate T g := by
  rw [multigroupEulerStep_eq_positive_form]
  have hincoming :
      Finset.univ.sum (fun h => T h g * unitAt g h) = 0 := by
    calc
      Finset.univ.sum (fun h => T h g * unitAt g h)
          = T g g := by
              classical
              rw [← Finset.sum_erase_add
                Finset.univ
                (fun h => T h g * unitAt g h)
                (Finset.mem_univ g)]
              simp [unitAt]
      _ = 0 := hdiag
  rw [hincoming]
  simp [unitAt]

/-- Violating the outgoing group CFL condition produces a negative value from
nonnegative unit data. -/
theorem multigroupEulerStep_unitAt_neg_of_cfl_violation
    (T : ι → ι → ℝ) (dt : ℝ) (g : ι)
    (hdiag : T g g = 0)
    (hcfl : 1 < dt * groupTransferOutRate T g) :
    multigroupEulerStep T dt (unitAt g) g < 0 := by
  rw [multigroupEulerStep_unitAt T dt g hdiag]
  linarith

/-- Energy removed by down-transfer and deposited locally. -/
def groupTransferEnergyDeposition
    (T : ι → ι → ℝ) (energy f : ι → ℝ) : ℝ :=
  Finset.univ.sum
    (fun g => Finset.univ.sum
      (fun h => T g h * f g * (energy g - energy h)))

/-- The energy-weighted transfer balance is the negative of the deposited
energy.  This is an algebraic identity and does not require ordering the group
energies. -/
theorem weighted_sum_multigroupTransfer_eq_neg_deposition
    (T : ι → ι → ℝ) (energy f : ι → ℝ) :
    Finset.univ.sum (fun g => energy g * multigroupTransfer T f g)
      = -groupTransferEnergyDeposition T energy f := by
  classical
  unfold multigroupTransfer groupTransferOutRate groupTransferEnergyDeposition
  calc
    Finset.univ.sum
        (fun g => energy g *
          (Finset.univ.sum (fun h => T h g * f h)
            - Finset.univ.sum (fun h => T g h) * f g))
        = Finset.univ.sum
            (fun g => Finset.univ.sum
              (fun h => energy g * (T h g * f h)))
          - Finset.univ.sum
            (fun g => Finset.univ.sum
              (fun h => energy g * (T g h * f g))) := by
                rw [Finset.sum_sub_distrib]
                congr 1
                · apply Finset.sum_congr rfl
                  intro g hg
                  rw [Finset.mul_sum]
                · apply Finset.sum_congr rfl
                  intro g hg
                  rw [Finset.sum_mul]
                  apply Finset.sum_congr rfl
                  intro h hh
                  ring
    _ = Finset.univ.sum
          (fun g => Finset.univ.sum
            (fun h => energy h * (T g h * f g)))
        - Finset.univ.sum
          (fun g => Finset.univ.sum
            (fun h => energy g * (T g h * f g))) := by
              congr 1
              rw [Finset.sum_comm]
    _ = -Finset.univ.sum
          (fun g => Finset.univ.sum
            (fun h => T g h * f g * (energy g - energy h))) := by
              simp only [Finset.sum_sub_distrib, Finset.sum_neg_distrib]
              ring

end AFPBarrier

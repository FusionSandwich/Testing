import AFPBarrier.ExplicitEulerTransport
import Mathlib.Tactic

/-!
# Positivity of a space--angle upwind Euler row

At one spatial cell and one angular direction, a first-order upwind transport
step has three nonnegative incoming mechanisms:

* streaming from the upwind cell or inflow boundary;
* angular jumps from neighbouring directions;
* an external source.

The outgoing coefficient contains streaming, angular jump rate, and absorption.
This file proves the exact convex-combination formula and the sharp local CFL
condition used by the deterministic Gate 6 slab solver.
-/

open scoped BigOperators

namespace AFPBarrier

variable {ι : Type*} [Fintype ι] [DecidableEq ι]

/-- One explicit-Euler update at one space--angle degree of freedom. -/
def spatialUpwindEulerCell
    (a : ι → ι → ℝ)
    (dt stream absorption source upwind : ℝ)
    (f : ι → ℝ) (i : ι) : ℝ :=
  f i + dt *
    (stream * (upwind - f i)
      + jumpGenerator a f i
      - absorption * f i
      + source)

/-- Exact positive-coefficient form of the local space--angle row. -/
theorem spatialUpwindEulerCell_eq_positive_form
    (a : ι → ι → ℝ)
    (dt stream absorption source upwind : ℝ)
    (f : ι → ℝ) (i : ι) :
    spatialUpwindEulerCell a dt stream absorption source upwind f i
      = (1 - dt * (stream + jumpRate a i + absorption)) * f i
        + dt * stream * upwind
        + dt * (offdiag i).sum (fun j => a i j * f j)
        + dt * source := by
  have hgenerator :=
    explicitEulerStep_eq_self_weight_add_neighbors
      (a := a) (dt := dt) (f := f) (i := i)
  unfold explicitEulerStep at hgenerator
  unfold spatialUpwindEulerCell
  calc
    f i + dt *
        (stream * (upwind - f i)
          + jumpGenerator a f i
          - absorption * f i
          + source)
        = (f i + dt * jumpGenerator a f i)
          + dt * stream * (upwind - f i)
          - dt * absorption * f i
          + dt * source := by ring
    _ = ((1 - dt * jumpRate a i) * f i
          + dt * (offdiag i).sum (fun j => a i j * f j))
          + dt * stream * (upwind - f i)
          - dt * absorption * f i
          + dt * source := by rw [hgenerator]
    _ = (1 - dt * (stream + jumpRate a i + absorption)) * f i
          + dt * stream * upwind
          + dt * (offdiag i).sum (fun j => a i j * f j)
          + dt * source := by ring

/-- The combined streaming--collision--absorption CFL condition is sufficient
for positivity of one upwind Euler row. -/
theorem spatialUpwindEulerCell_nonneg
    (a : ι → ι → ℝ)
    (dt stream absorption source upwind : ℝ)
    (f : ι → ℝ) (i : ι)
    (ha : ∀ j, j ≠ i → 0 ≤ a i j)
    (hdt : 0 ≤ dt)
    (hstream : 0 ≤ stream)
    (habsorption : 0 ≤ absorption)
    (hsource : 0 ≤ source)
    (hupwind : 0 ≤ upwind)
    (hf : ∀ j, 0 ≤ f j)
    (hcfl : dt * (stream + jumpRate a i + absorption) ≤ 1) :
    0 ≤ spatialUpwindEulerCell a dt stream absorption source upwind f i := by
  rw [spatialUpwindEulerCell_eq_positive_form]
  have hself :
      0 ≤ (1 - dt * (stream + jumpRate a i + absorption)) * f i :=
    mul_nonneg (sub_nonneg.mpr hcfl) (hf i)
  have hupwindTerm : 0 ≤ dt * stream * upwind :=
    mul_nonneg (mul_nonneg hdt hstream) hupwind
  have hangular :
      0 ≤ dt * (offdiag i).sum (fun j => a i j * f j) := by
    apply mul_nonneg hdt
    apply Finset.sum_nonneg
    intro j hj
    have hji : j ≠ i := (Finset.mem_erase.mp hj).1
    exact mul_nonneg (ha j hji) (hf j)
  have hsourceTerm : 0 ≤ dt * source := mul_nonneg hdt hsource
  positivity

/-- With unit mass at the current row and zero incoming data, the update is the
outgoing diagonal coefficient. -/
theorem spatialUpwindEulerCell_unitAt
    (a : ι → ι → ℝ)
    (dt stream absorption : ℝ) (i : ι) :
    spatialUpwindEulerCell a dt stream absorption 0 0 (unitAt i) i
      = 1 - dt * (stream + jumpRate a i + absorption) := by
  rw [spatialUpwindEulerCell_eq_positive_form]
  have hsum :
      (offdiag i).sum (fun j => a i j * unitAt i j) = 0 := by
    apply Finset.sum_eq_zero
    intro j hj
    have hji : j ≠ i := (Finset.mem_erase.mp hj).1
    simp [unitAt, hji]
  rw [hsum]
  simp [unitAt]

/-- The local CFL condition is also necessary for unconditional positivity. -/
theorem spatialUpwindEulerCell_unitAt_neg_of_cfl_violation
    (a : ι → ι → ℝ)
    (dt stream absorption : ℝ) (i : ι)
    (hcfl : 1 < dt * (stream + jumpRate a i + absorption)) :
    spatialUpwindEulerCell a dt stream absorption 0 0 (unitAt i) i < 0 := by
  rw [spatialUpwindEulerCell_unitAt]
  linarith

end AFPBarrier

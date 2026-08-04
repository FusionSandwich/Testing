import AFPBarrier.QuadraticFidelityFoundation
import Mathlib.Tactic

/-!
# Finite trace core for the sharp quadratic-fidelity lower bound

This module formalizes the coordinate finite-sum step used by P1B.  It keeps
sample weights explicit and does not assume that the sampling rows are
independent.  The quotient and residual-kernel facts used by the ordinary
proof are formalized in `QuadraticSampling`, `QuadraticSphereResidual`, and
`QuadraticFidelityFoundation`.
-/

open scoped BigOperators

namespace AFPBarrier

variable {I J : Type*}
  [Fintype I] [DecidableEq I]
  [Fintype J] [DecidableEq J]

/-- Analysis by a finite coordinate row family. -/
def coordinateRowAnalysis
    (rows : I → J → ℝ) (x : J → ℝ) : I → ℝ :=
  fun i => ∑ j, rows i j * x j

/-- Weighted squared analysis norm of a coordinate row family. -/
def weightedCoordinateEnergy
    (w : I → ℝ) (rows : I → J → ℝ) (x : J → ℝ) : ℝ :=
  ∑ i, w i * (coordinateRowAnalysis rows x i) ^ 2

/-- Sum of the weighted squared row coordinates.  In an orthonormal
coefficient basis this is the Hilbert--Schmidt trace. -/
def weightedCoordinateTrace
    (w : I → ℝ) (rows : I → J → ℝ) : ℝ :=
  ∑ j, ∑ i, w i * (rows i j) ^ 2

/-- A coordinate unit vector. -/
def coordinateUnit (j : J) : J → ℝ :=
  fun k => if k = j then 1 else 0

/-- Analysis of a coordinate unit vector selects the corresponding row
coordinate. -/
theorem coordinateRowAnalysis_coordinateUnit
    (rows : I → J → ℝ) (i : I) (j : J) :
    coordinateRowAnalysis rows (coordinateUnit j) i = rows i j := by
  classical
  unfold coordinateRowAnalysis coordinateUnit
  simp

/-- An operator-norm quadratic domination implies the corresponding weighted
trace domination, with no row-independence or injectivity hypothesis. -/
theorem weightedCoordinateTrace_le_of_energy_domination
    (w : I → ℝ) (sampleRows residualRows : I → J → ℝ) (Dsq : ℝ)
    (hdom : ∀ x : J → ℝ,
      weightedCoordinateEnergy w residualRows x ≤
        Dsq * weightedCoordinateEnergy w sampleRows x) :
    weightedCoordinateTrace w residualRows ≤
      Dsq * weightedCoordinateTrace w sampleRows := by
  classical
  unfold weightedCoordinateTrace
  calc
    (∑ j, ∑ i, w i * (residualRows i j) ^ 2) ≤
        ∑ j, Dsq * (∑ i, w i * (sampleRows i j) ^ 2) := by
          apply Finset.sum_le_sum
          intro j hj
          simpa [weightedCoordinateEnergy,
            coordinateRowAnalysis_coordinateUnit] using
            hdom (coordinateUnit j)
    _ = Dsq * (∑ j, ∑ i, w i * (sampleRows i j) ^ 2) := by
          rw [Finset.mul_sum]

/-- The exact scalar conversion from the trace inequality to the P1B
strong two-defect coefficient. -/
theorem quadraticDefect_twoDefect_lower_sq
    (d Dsq Eepsilon EB : ℝ)
    (hd : 1 < d)
    (htrace : d / (d - 1) * Eepsilon + EB ≤
      Dsq * ((d - 1) / d)) :
    d ^ 2 / (d - 1) ^ 2 * Eepsilon +
        d / (d - 1) * EB ≤ Dsq := by
  have hdpos : 0 < d := lt_trans zero_lt_one hd
  have hdm1pos : 0 < d - 1 := sub_pos.mpr hd
  have hcoef : 0 ≤ d / (d - 1) :=
    le_of_lt (div_pos hdpos hdm1pos)
  have hmul := mul_le_mul_of_nonneg_left htrace hcoef
  calc
    d ^ 2 / (d - 1) ^ 2 * Eepsilon +
        d / (d - 1) * EB =
        d / (d - 1) * (d / (d - 1) * Eepsilon + EB) := by
          field_simp [ne_of_gt hdpos, ne_of_gt hdm1pos]
          ring
    _ ≤ d / (d - 1) * (Dsq * ((d - 1) / d)) := hmul
    _ = Dsq := by
          field_simp [ne_of_gt hdpos, ne_of_gt hdm1pos]
          ring

/-- The scalar final step of the universal rate--defect product bound. -/
theorem quadraticDefect_rate_product_lower
    (d D rms rmax : ℝ)
    (hd : 1 < d)
    (hrmax : 0 < rmax)
    (hradial : d / (d - 1) * rms ≤ D)
    (hrms : (d - 1) ^ 2 / rmax ≤ rms) :
    d * (d - 1) ≤ D * rmax := by
  have hdpos : 0 < d := lt_trans zero_lt_one hd
  have hdm1pos : 0 < d - 1 := sub_pos.mpr hd
  have hcoef : 0 ≤ d / (d - 1) :=
    le_of_lt (div_pos hdpos hdm1pos)
  have hchain :
      d / (d - 1) * ((d - 1) ^ 2 / rmax) ≤ D :=
    le_trans (mul_le_mul_of_nonneg_left hrms hcoef) hradial
  have hrewrite :
      d / (d - 1) * ((d - 1) ^ 2 / rmax) =
        d * (d - 1) / rmax := by
    field_simp [ne_of_gt hdpos, ne_of_gt hdm1pos, ne_of_gt hrmax]
    ring
  rw [hrewrite] at hchain
  calc
    d * (d - 1) = (d * (d - 1) / rmax) * rmax := by
      field_simp [ne_of_gt hrmax]
    _ ≤ D * rmax :=
      mul_le_mul_of_nonneg_right hchain (le_of_lt hrmax)

/-- The specialized `S^2` scalar product inequality. -/
theorem sTwo_quadraticDefect_rate_product_lower
    (D rms rmax : ℝ)
    (hrmax : 0 < rmax)
    (hradial : (3 : ℝ) / 2 * rms ≤ D)
    (hrms : (4 : ℝ) / rmax ≤ rms) :
    6 ≤ D * rmax := by
  have h := quadraticDefect_rate_product_lower
    (d := (3 : ℝ)) (D := D) (rms := rms) (rmax := rmax)
    (by norm_num) hrmax hradial
    (by norm_num at hrms ⊢; exact hrms)
  norm_num at h ⊢
  exact h

end AFPBarrier

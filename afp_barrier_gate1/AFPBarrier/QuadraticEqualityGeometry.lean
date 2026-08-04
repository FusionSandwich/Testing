import AFPBarrier.QuadraticFidelityLowerBound
import AFPBarrier.QEqualityCovariance
import Mathlib.Tactic

/-!
# Local geometry of equality in the quadratic-fidelity frontier

This module isolates the finite row algebra behind the equality case.  The
raw projected-tangent statements are division-free, so they continue to make
sense on an antipodal shell.  Unit-tangent normalization is kept in a
separate theorem with explicit nonzero-denominator hypotheses.
-/

open scoped BigOperators

namespace AFPBarrier

variable {I K : Type*}
  [Fintype I] [DecidableEq I]
  [Fintype K] [DecidableEq K]

/-- The tangent part of the increment from `z` to `y` when the chordal loss
is `ell`: `tau = (y-z) + ell z`. -/
def projectedTangentIncrement
    (z y : K → ℝ) (ell : ℝ) : K → ℝ :=
  fun p => y p - z p + ell * z p

/-- Exact radial--tangent decomposition of a spherical increment. -/
theorem increment_radial_tangent_decomposition
    (z y : K → ℝ) (ell : ℝ) (p : K) :
    y p - z p =
      -ell * z p + projectedTangentIncrement z y ell p := by
  simp only [projectedTangentIncrement]
  ring

/-- The projected increment is tangent when `z` and `y` have the stated
unit-sphere inner products. -/
theorem projectedTangentIncrement_orthogonal
    (z y : K → ℝ) (ell : ℝ)
    (hzz : oneShellFiniteDot z z = 1)
    (hzy : oneShellFiniteDot z y = 1 - ell) :
    oneShellFiniteDot z (projectedTangentIncrement z y ell) = 0 := by
  unfold oneShellFiniteDot at hzz hzy ⊢
  unfold projectedTangentIncrement
  calc
    (∑ p, z p * (y p - z p + ell * z p)) =
        (∑ p, z p * y p) - (∑ p, z p * z p) +
          ell * (∑ p, z p * z p) := by
            rw [Finset.mul_sum]
            simp only [← Finset.sum_add_distrib,
              ← Finset.sum_sub_distrib]
            apply Finset.sum_congr rfl
            intro p hp
            ring
    _ = 0 := by rw [hzy, hzz]; ring

/-- Exact squared length of the projected tangent increment. -/
theorem projectedTangentIncrement_normSq
    (z y : K → ℝ) (ell : ℝ)
    (hzz : oneShellFiniteDot z z = 1)
    (hyy : oneShellFiniteDot y y = 1)
    (hzy : oneShellFiniteDot z y = 1 - ell) :
    oneShellFiniteDot
        (projectedTangentIncrement z y ell)
        (projectedTangentIncrement z y ell) =
      ell * (2 - ell) := by
  unfold oneShellFiniteDot at hzz hyy hzy ⊢
  unfold projectedTangentIncrement
  calc
    (∑ p,
        (y p - z p + ell * z p) *
          (y p - z p + ell * z p)) =
        (∑ p, y p * y p) +
          (ell - 1) ^ 2 * (∑ p, z p * z p) +
          2 * (ell - 1) * (∑ p, z p * y p) := by
            rw [Finset.mul_sum, Finset.mul_sum]
            simp only [← Finset.sum_add_distrib]
            apply Finset.sum_congr rfl
            intro p hp
            ring
    _ = ell * (2 - ell) := by
      rw [hyy, hzz, hzy]
      ring

/-- A denominator-free entrywise form of `B=0` on an equality shell.  Here
`diag` is the corresponding identity-matrix entry and `zz` is the entry of
`z zᵀ`. -/
theorem equalityRemainderEntry_zero_iff_axialCovariance
    (d ell zz diag C B : ℝ)
    (hB :
      B = C + 2 * zz - 2 * diag - d * ell * zz + ell * diag) :
    B = 0 ↔
      C =
        (2 - ell) * (diag - zz) +
          (d - 1) * ell * zz := by
  constructor
  · intro hzero
    rw [hB] at hzero
    ring_nf at hzero ⊢
    linarith
  · intro haxial
    rw [hB, haxial]
    ring

/-- With a common loss and vanishing tangent first moment, axial covariance
is equivalent to the raw projected tangent second moment being isotropic.
This statement does not divide by `ell * (2-ell)` and remains valid at an
antipodal shell. -/
theorem oneShell_axialCovariance_iff_tangentSecondMoment
    (J : Finset I) (row : I → ℝ)
    (z : K → ℝ) (tau : I → K → ℝ)
    (d ell r : ℝ)
    (hr : r = oneShellRate J row)
    (hradial : r * ell = d - 1)
    (hfirst : ∀ p, oneShellFirstMoment J row tau p = 0) :
    (∀ p q,
      oneShellCovariance J row z tau ell 1 p q =
        (2 - ell) *
            ((if p = q then 1 else 0) - z p * z q) +
          (d - 1) * ell * z p * z q) ↔
    (∀ p q,
      oneShellSecondMoment J row tau p q =
        (2 - ell) *
          ((if p = q then 1 else 0) - z p * z q)) := by
  have hradialCoefficient :
      ell ^ 2 * r = (d - 1) * ell := by
    calc
      ell ^ 2 * r = (r * ell) * ell := by ring
      _ = (d - 1) * ell := by rw [hradial]
  constructor
  · intro hcov p q
    have hpq := hcov p q
    rw [oneShell_covariance_expansion, ← hr,
      hfirst q, hfirst p, hradialCoefficient] at hpq
    norm_num at hpq
    linarith
  · intro hsecond p q
    rw [oneShell_covariance_expansion, ← hr,
      hfirst q, hfirst p, hsecond p q, hradialCoefficient]
    norm_num
    ring

/-- Scaling every tangent vector by `s` scales its second moment by `s²`. -/
theorem oneShellSecondMoment_scaled
    (J : Finset I) (row : I → ℝ)
    (u : I → K → ℝ) (s : ℝ) (p q : K) :
    oneShellSecondMoment J row (fun j k => s * u j k) p q =
      s ^ 2 * oneShellSecondMoment J row u p q := by
  unfold oneShellSecondMoment
  rw [Finset.mul_sum]
  apply Finset.sum_congr rfl
  intro j hj
  ring

/-- General-dimensional normalization/converse for a weighted tight-frame
second moment.  Positivity and unit tangency are geometric hypotheses of the
calling theorem; this lemma performs only the exact normalization algebra. -/
theorem normalizedTangentTightFrame_iff_oneShellSecondMoment
    (J : Finset I) (row : I → ℝ)
    (u : I → K → ℝ) (z : K → ℝ)
    (rate d : ℝ)
    (hrate : 0 < rate)
    (hd : d - 1 ≠ 0) :
    (∀ p q,
      normalizedTangentSecondMoment J
          (fun j => row j / rate) u p q =
        tangentProjectorEntry z p q / (d - 1)) ↔
    (∀ p q,
      oneShellSecondMoment J row u p q =
        (rate / (d - 1)) * tangentProjectorEntry z p q) := by
  constructor
  · intro hnormalized p q
    rw [oneShellSecondMoment_eq_rate_mul_normalized
      J row u rate hrate p q, hnormalized p q]
    field_simp [hd]
  · intro hsecond p q
    have hpq := hsecond p q
    rw [oneShellSecondMoment_eq_rate_mul_normalized
      J row u rate hrate p q] at hpq
    have hrne : rate ≠ 0 := ne_of_gt hrate
    calc
      normalizedTangentSecondMoment J
          (fun j => row j / rate) u p q =
          (rate * normalizedTangentSecondMoment J
            (fun j => row j / rate) u p q) / rate := by
              field_simp [hrne]
      _ = ((rate / (d - 1)) * tangentProjectorEntry z p q) /
            rate := by rw [hpq]
      _ = tangentProjectorEntry z p q / (d - 1) := by
            field_simp [hrne, hd]

/-- Normalized one-shell weights sum to one when `rate` is the row sum. -/
theorem oneShell_normalizedWeights_sum_one
    (J : Finset I) (row : I → ℝ) (rate : ℝ)
    (hrate : 0 < rate)
    (hr : rate = oneShellRate J row) :
    ∑ j ∈ J, row j / rate = 1 := by
  have hrne : rate ≠ 0 := ne_of_gt hrate
  unfold oneShellRate at hr
  calc
    ∑ j ∈ J, row j / rate =
        (∑ j ∈ J, row j) / rate := by
          rw [Finset.sum_div]
    _ = rate / rate := by rw [← hr]
    _ = 1 := div_self hrne

/-- Raw tightness for scaled tangent increments is equivalent to the
normalized unit-frame equation.  The `ell ≠ 2` guard is the exact
nonantipodal denominator condition. -/
theorem scaledTangentTightFrame_iff_normalized
    (J : Finset I) (row : I → ℝ)
    (u : I → K → ℝ) (z : K → ℝ)
    (rate d ell s : ℝ)
    (hrate : 0 < rate)
    (hd : d - 1 ≠ 0)
    (hell : 2 - ell ≠ 0)
    (hradial : rate * ell = d - 1)
    (hsquare : s ^ 2 = ell * (2 - ell)) :
    (∀ p q,
      oneShellSecondMoment J row (fun j k => s * u j k) p q =
        (2 - ell) * tangentProjectorEntry z p q) ↔
    (∀ p q,
      normalizedTangentSecondMoment J
          (fun j => row j / rate) u p q =
        tangentProjectorEntry z p q / (d - 1)) := by
  have hcoefficient :
      s ^ 2 * rate = (d - 1) * (2 - ell) := by
    calc
      s ^ 2 * rate = (ell * (2 - ell)) * rate := by rw [hsquare]
      _ = (rate * ell) * (2 - ell) := by ring
      _ = (d - 1) * (2 - ell) := by rw [hradial]
  constructor
  · intro hraw p q
    have hpq := hraw p q
    rw [oneShellSecondMoment_scaled,
      oneShellSecondMoment_eq_rate_mul_normalized
        J row u rate hrate p q] at hpq
    rw [← mul_assoc, hcoefficient] at hpq
    calc
      normalizedTangentSecondMoment J
          (fun j => row j / rate) u p q =
          ((d - 1) * (2 - ell) *
            normalizedTangentSecondMoment J
              (fun j => row j / rate) u p q) /
              ((d - 1) * (2 - ell)) := by
                field_simp [hd, hell]
      _ = ((2 - ell) * tangentProjectorEntry z p q) /
              ((d - 1) * (2 - ell)) := by rw [hpq]
      _ = tangentProjectorEntry z p q / (d - 1) := by
            field_simp [hd, hell]
  · intro hnormalized p q
    rw [oneShellSecondMoment_scaled,
      oneShellSecondMoment_eq_rate_mul_normalized
        J row u rate hrate p q, hnormalized p q]
    rw [← mul_assoc, hcoefficient]
    field_simp [hd]

/-- Geometric wrapper with the explicit positive-rate, `d>1`, and
nonantipodal hypotheses used by the equality theorem. -/
theorem scaledTangentTightFrame_iff_normalized_of_nonantipodal
    (J : Finset I) (row : I → ℝ)
    (u : I → K → ℝ) (z : K → ℝ)
    (rate d ell s : ℝ)
    (hd : 1 < d)
    (hrate : 0 < rate)
    (hell : ell < 2)
    (hradial : rate * ell = d - 1)
    (hsquare : s ^ 2 = ell * (2 - ell)) :
    (∀ p q,
      oneShellSecondMoment J row (fun j k => s * u j k) p q =
        (2 - ell) * tangentProjectorEntry z p q) ↔
    (∀ p q,
      normalizedTangentSecondMoment J
          (fun j => row j / rate) u p q =
        tangentProjectorEntry z p q / (d - 1)) := by
  exact scaledTangentTightFrame_iff_normalized
    J row u z rate d ell s hrate
      (ne_of_gt (sub_pos.mpr hd))
      (ne_of_gt (sub_pos.mpr hell)) hradial hsquare

/-- Scalar equality certificate for the sharp quadratic-fidelity product. -/
theorem quadraticEquality_rate_product
    (d ell r D : ℝ)
    (hradial : r * ell = d - 1)
    (hdefect : D = d * ell) :
    D * r = d * (d - 1) := by
  rw [hdefect]
  calc
    d * ell * r = d * (r * ell) := by ring
    _ = d * (d - 1) := by rw [hradial]

end AFPBarrier

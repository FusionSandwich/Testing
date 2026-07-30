import AFPBarrier.EqualAngleEdges
import Mathlib.Analysis.SpecialFunctions.Trigonometric.Bounds
import Mathlib.Tactic

/-!
# Explicit finite-order error and stiffness bounds

The first Gate 3 audit fitted numerical slopes.  This file replaces those fits
with explicit inequalities, valid at every order.  For the square product
family the half polar step is `h = π/(2n)`.

* every ring defect lies between `2/n²` and `π²/n²`;
* the polar jump rate lies between `(8/π⁴)n⁴` and `n⁴`.

These are finite-`n` inequalities, not asymptotic heuristics, and they imply the
reported `Theta(n⁻²)` defect and `Theta(n⁴)` polar stiffness.
-/

namespace AFPBarrier

noncomputable section

/-- Degree-two peak defect on a square equal-angle ring, where `st` is the sine
of the ring latitude and `h` is half the common angular step. -/
def squareRingDefect (h st : ℝ) : ℝ :=
  2 * Real.sin h ^ 2 + 2 * st ^ 2 * Real.sin h ^ 2

/-- Total outgoing rate on a square equal-angle ring. -/
def squareRingRate (h st : ℝ) : ℝ :=
  1 / (2 * Real.sin h ^ 2)
    + 1 / (2 * Real.sin h ^ 2 * st ^ 2)

/-- The polar-ring specialization `st = sin h`. -/
def squarePolarRateFromStep (h : ℝ) : ℝ :=
  1 / (2 * Real.sin h ^ 2) + 1 / (2 * Real.sin h ^ 4)

/-- Algebraic ring-defect bounds when the latitude sine has magnitude at most
one. -/
theorem squareRingDefect_between_sin_bounds
    (h st : ℝ) (hst : st ^ 2 ≤ 1) :
    2 * Real.sin h ^ 2 ≤ squareRingDefect h st
      ∧ squareRingDefect h st ≤ 4 * Real.sin h ^ 2 := by
  unfold squareRingDefect
  have hst0 : 0 ≤ st ^ 2 := sq_nonneg st
  have hs0 : 0 ≤ Real.sin h ^ 2 := sq_nonneg (Real.sin h)
  constructor
  · nlinarith [mul_nonneg hst0 hs0]
  · have hprod : st ^ 2 * Real.sin h ^ 2 ≤ Real.sin h ^ 2 :=
      mul_le_of_le_one_left hs0 hst
    nlinarith

/-- Jordan's inequality converts the exact ring defect into explicit angular
step bounds. -/
theorem squareRingDefect_trig_bounds
    (h st : ℝ)
    (hh0 : 0 ≤ h) (hhhalf : h ≤ Real.pi / 2)
    (hst : st ^ 2 ≤ 1) :
    2 * (2 / Real.pi * h) ^ 2 ≤ squareRingDefect h st
      ∧ squareRingDefect h st ≤ 4 * h ^ 2 := by
  have hbase := squareRingDefect_between_sin_bounds h st hst
  have hslo : 2 / Real.pi * h ≤ Real.sin h :=
    Real.mul_le_sin hh0 hhhalf
  have ha0 : 0 ≤ 2 / Real.pi * h := by positivity
  have hspi : h ≤ Real.pi := by linarith [Real.pi_pos]
  have hs0 : 0 ≤ Real.sin h :=
    Real.sin_nonneg_of_nonneg_of_le_pi hh0 hspi
  have hsqlo : (2 / Real.pi * h) ^ 2 ≤ Real.sin h ^ 2 := by
    have hp := mul_nonneg (sub_nonneg.mpr hslo) (add_nonneg ha0 hs0)
    nlinarith
  have hsqhi : Real.sin h ^ 2 ≤ h ^ 2 := Real.sin_sq_le_sq
  constructor
  · exact le_trans (by nlinarith :
        2 * (2 / Real.pi * h) ^ 2 ≤ 2 * Real.sin h ^ 2) hbase.1
  · exact hbase.2.trans (by nlinarith)

/-- The Jordan scale of the actual grid half-step is exactly `1/n`. -/
theorem equalAngleGrid_jordanScale
    (n : ℝ) (hn : n ≠ 0) :
    2 / Real.pi * equalAngleGridHalfStep n = 1 / n := by
  unfold equalAngleGridHalfStep
  field_simp [Real.pi_ne_zero, hn]
  ring

/-- Exact finite-order defect bounds for every ring of the square product
family. -/
theorem squareRingDefect_grid_bounds
    (n st : ℝ) (hn : 2 ≤ n) (hst : st ^ 2 ≤ 1) :
    2 / n ^ 2 ≤ squareRingDefect (equalAngleGridHalfStep n) st
      ∧ squareRingDefect (equalAngleGridHalfStep n) st
          ≤ Real.pi ^ 2 / n ^ 2 := by
  have hn0 : 0 < n := by linarith
  have hh0 := (equalAngleGridHalfStep_pos n hn0).le
  have hhhalf := (equalAngleGridHalfStep_lt_pi_div_two n hn).le
  have hbounds := squareRingDefect_trig_bounds
    (equalAngleGridHalfStep n) st hh0 hhhalf hst
  have hscale := equalAngleGrid_jordanScale n hn0.ne'
  have hlower :
      2 * (2 / Real.pi * equalAngleGridHalfStep n) ^ 2
        = 2 / n ^ 2 := by
    rw [hscale]
    field_simp [hn0.ne']
    ring
  have hupper :
      4 * equalAngleGridHalfStep n ^ 2
        = Real.pi ^ 2 / n ^ 2 := by
    unfold equalAngleGridHalfStep
    field_simp [hn0.ne']
    ring
  constructor
  · rw [← hlower]
    exact hbounds.1
  · rw [← hupper]
    exact hbounds.2

/-- The polar-rate formula is bounded below by the inverse fourth power of the
angular step. -/
theorem squarePolarRate_lower_step
    (h : ℝ) (hh0 : 0 < h) (hhhalf : h ≤ Real.pi / 2) :
    1 / (2 * h ^ 4) ≤ squarePolarRateFromStep h := by
  have hspi : h < Real.pi := by linarith [Real.pi_pos]
  have hspos : 0 < Real.sin h :=
    Real.sin_pos_of_pos_of_lt_pi hh0 hspi
  have hsle : Real.sin h ≤ h := Real.sin_le hh0.le
  have hs2le : Real.sin h ^ 2 ≤ h ^ 2 := by
    have hp := mul_nonneg (sub_nonneg.mpr hsle)
      (add_nonneg hspos.le hh0.le)
    nlinarith
  have hs4le : Real.sin h ^ 4 ≤ h ^ 4 := by
    have hp := mul_nonneg (sub_nonneg.mpr hs2le)
      (add_nonneg (sq_nonneg (Real.sin h)) (sq_nonneg h))
    nlinarith
  have hrecip :
      1 / (2 * h ^ 4) ≤ 1 / (2 * Real.sin h ^ 4) := by
    apply (div_le_div_iff₀ (by positivity : 0 < 2 * h ^ 4)
      (by positivity : 0 < 2 * Real.sin h ^ 4)).2
    nlinarith
  unfold squarePolarRateFromStep
  have hfirst : 0 ≤ 1 / (2 * Real.sin h ^ 2) := by positivity
  linarith

/-- Jordan's lower bound on sine gives an explicit upper bound on the polar
rate. -/
theorem squarePolarRate_upper_jordan
    (h : ℝ) (hh0 : 0 < h) (hhhalf : h ≤ Real.pi / 2) :
    squarePolarRateFromStep h
      ≤ 1 / (2 * (2 / Real.pi * h) ^ 2)
        + 1 / (2 * (2 / Real.pi * h) ^ 4) := by
  have hslo : 2 / Real.pi * h ≤ Real.sin h :=
    Real.mul_le_sin hh0.le hhhalf
  have ha0 : 0 < 2 / Real.pi * h := by positivity
  have hspi : h < Real.pi := by linarith [Real.pi_pos]
  have hs0 : 0 < Real.sin h :=
    Real.sin_pos_of_pos_of_lt_pi hh0 hspi
  have hsq : (2 / Real.pi * h) ^ 2 ≤ Real.sin h ^ 2 := by
    have hp := mul_nonneg (sub_nonneg.mpr hslo)
      (add_nonneg ha0.le hs0.le)
    nlinarith
  have hfour : (2 / Real.pi * h) ^ 4 ≤ Real.sin h ^ 4 := by
    have hp := mul_nonneg (sub_nonneg.mpr hsq)
      (add_nonneg (sq_nonneg (2 / Real.pi * h))
        (sq_nonneg (Real.sin h)))
    nlinarith
  have hrec2 :
      1 / (2 * Real.sin h ^ 2)
        ≤ 1 / (2 * (2 / Real.pi * h) ^ 2) := by
    apply (div_le_div_iff₀ (by positivity : 0 < 2 * Real.sin h ^ 2)
      (by positivity : 0 < 2 * (2 / Real.pi * h) ^ 2)).2
    nlinarith
  have hrec4 :
      1 / (2 * Real.sin h ^ 4)
        ≤ 1 / (2 * (2 / Real.pi * h) ^ 4) := by
    apply (div_le_div_iff₀ (by positivity : 0 < 2 * Real.sin h ^ 4)
      (by positivity : 0 < 2 * (2 / Real.pi * h) ^ 4)).2
    nlinarith
  unfold squarePolarRateFromStep
  linarith

/-- Explicit finite-order polar stiffness bounds. -/
theorem squarePolarRate_grid_bounds
    (n : ℝ) (hn : 2 ≤ n) :
    8 * n ^ 4 / Real.pi ^ 4
        ≤ squarePolarRateFromStep (equalAngleGridHalfStep n)
      ∧ squarePolarRateFromStep (equalAngleGridHalfStep n) ≤ n ^ 4 := by
  have hn0 : 0 < n := by linarith
  have hh0 := equalAngleGridHalfStep_pos n hn0
  have hhhalf := (equalAngleGridHalfStep_lt_pi_div_two n hn).le
  have hlo := squarePolarRate_lower_step
    (equalAngleGridHalfStep n) hh0 hhhalf
  have hup := squarePolarRate_upper_jordan
    (equalAngleGridHalfStep n) hh0 hhhalf
  have hscale := equalAngleGrid_jordanScale n hn0.ne'
  have hlowerForm :
      1 / (2 * equalAngleGridHalfStep n ^ 4)
        = 8 * n ^ 4 / Real.pi ^ 4 := by
    unfold equalAngleGridHalfStep
    field_simp [hn0.ne', Real.pi_ne_zero]
    ring
  have hupperForm :
      1 / (2 * (2 / Real.pi * equalAngleGridHalfStep n) ^ 2)
          + 1 / (2 * (2 / Real.pi * equalAngleGridHalfStep n) ^ 4)
        = (n ^ 2 + n ^ 4) / 2 := by
    rw [hscale]
    field_simp [hn0.ne']
    ring
  have hn2ge1 : 1 ≤ n ^ 2 := by nlinarith
  have hn2le4 : n ^ 2 ≤ n ^ 4 := by
    calc
      n ^ 2 = n ^ 2 * 1 := by ring
      _ ≤ n ^ 2 * n ^ 2 :=
        mul_le_mul_of_nonneg_left hn2ge1 (sq_nonneg n)
      _ = n ^ 4 := by ring
  constructor
  · rw [← hlowerForm]
    exact hlo
  · calc
      squarePolarRateFromStep (equalAngleGridHalfStep n)
          ≤ (n ^ 2 + n ^ 4) / 2 := by
            rw [← hupperForm]
            exact hup
      _ ≤ n ^ 4 := by nlinarith

end

end AFPBarrier

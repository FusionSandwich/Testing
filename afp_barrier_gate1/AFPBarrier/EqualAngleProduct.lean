import AFPBarrier.Quantitative
import Mathlib.Tactic

/-!
# Equal-angle product-grid AFP identities

This module formalizes the algebraic core of the all-orders equal-angle
latitude--longitude construction developed in Gate 3.

The geometric construction uses

* polar step `delta`, represented algebraically by `sh = sin(delta / 2)`;
* azimuthal step `alpha`, represented by `v = 1 - cos(alpha)`;
* `st = sin(theta)` at the current latitude ring;
* cell weight `q = 2 * alpha * st * sh`;
* total meridional conductance `alpha * st / sh`;
* each azimuthal conductance `alpha * sh / (v * st)`.

The trigonometric derivation of these formulas is given in `GATE3.md` and is
checked independently by the deterministic Python audit. Lean verifies here
that the formulas imply the claimed peak-defect and jump-rate identities, the
polar stiffness formula, positivity, and exactness whenever the local balance
equation holds.
-/

namespace AFPBarrier

/-- Four-neighbour local product-grid action. `bm` and `bp` are the two
meridional conductances and `c` is the conductance of each azimuthal edge. -/
def productNodeAction
    (q bm bp c f0 fm fp fl fr : ℝ) : ℝ :=
  (bm * (fm - f0) + bp * (fp - f0)
    + c * (fl - f0) + c * (fr - f0)) / q

/-- The local action annihilates constants. -/
@[simp] theorem productNodeAction_const
    (q bm bp c f0 : ℝ) :
    productNodeAction q bm bp c f0 f0 f0 f0 f0 = 0 := by
  simp [productNodeAction]

/-- Any exact unnormalised balance equation gives the corresponding normalised
eigenvalue equation. -/
theorem productNodeAction_eq_of_balance
    (q bm bp c f0 fm fp fl fr lam : ℝ)
    (hq : q ≠ 0)
    (hbalance :
      bm * (fm - f0) + bp * (fp - f0)
        + c * (fl - f0) + c * (fr - f0)
        = -lam * q * f0) :
    productNodeAction q bm bp c f0 fm fp fl fr = -lam * f0 := by
  unfold productNodeAction
  rw [hbalance]
  field_simp [hq]

/-- Axial-coordinate specialization: azimuthal neighbours have the same value,
so only the meridional balance remains. -/
theorem productNodeAction_axial
    (q bm bp c x xm xp lam : ℝ)
    (hq : q ≠ 0)
    (hbalance : bm * (xm - x) + bp * (xp - x) = -lam * q * x) :
    productNodeAction q bm bp c x xm xp x x = -lam * x := by
  apply productNodeAction_eq_of_balance
    (q := q) (bm := bm) (bp := bp) (c := c)
    (f0 := x) (fm := xm) (fp := xp) (fl := x) (fr := x)
    (lam := lam) hq
  simpa using hbalance

/-- Total outgoing rate of the four-neighbour product stencil. -/
def productLocalRate (q bm bp c : ℝ) : ℝ :=
  (bm + bp + 2 * c) / q

/-- Peak defect for two meridional neighbours with common dot-product loss
`dmer` and two azimuthal neighbours with common loss `dazi`. -/
def productLocalPeakDefect
    (q bm bp c dmer dazi : ℝ) : ℝ :=
  ((bm + bp) * dmer ^ 2 + 2 * c * dazi ^ 2) / q

/-- Cell-area weight of the equal-angle product family. -/
def equalAngleWeight (alpha st sh : ℝ) : ℝ :=
  2 * alpha * st * sh

/-- Sum of the two meridional conductances incident to one node. -/
def equalAngleMeridionalTotal (alpha st sh : ℝ) : ℝ :=
  alpha * st / sh

/-- Conductance of each of the two azimuthal edges. -/
def equalAngleAzimuthConductance
    (alpha sh v st : ℝ) : ℝ :=
  alpha * sh / (v * st)

/-- Positive geometric factors give a positive cell weight. -/
theorem equalAngleWeight_pos
    (alpha st sh : ℝ)
    (halpha : 0 < alpha) (hst : 0 < st) (hsh : 0 < sh) :
    0 < equalAngleWeight alpha st sh := by
  unfold equalAngleWeight
  positivity

/-- Positive geometric factors give positive total meridional conductance. -/
theorem equalAngleMeridionalTotal_pos
    (alpha st sh : ℝ)
    (halpha : 0 < alpha) (hst : 0 < st) (hsh : 0 < sh) :
    0 < equalAngleMeridionalTotal alpha st sh := by
  unfold equalAngleMeridionalTotal
  exact div_pos (mul_pos halpha hst) hsh

/-- Positive geometric factors give positive azimuthal conductance. -/
theorem equalAngleAzimuthConductance_pos
    (alpha sh v st : ℝ)
    (halpha : 0 < alpha) (hsh : 0 < sh)
    (hv : 0 < v) (hst : 0 < st) :
    0 < equalAngleAzimuthConductance alpha sh v st := by
  unfold equalAngleAzimuthConductance
  exact div_pos (mul_pos halpha hsh) (mul_pos hv hst)

/-- The total meridional rate is exactly `1 / (2 sh^2)`. -/
theorem equalAngle_meridional_rate
    (alpha st sh : ℝ)
    (halpha : alpha ≠ 0) (hst : st ≠ 0) (hsh : sh ≠ 0) :
    equalAngleMeridionalTotal alpha st sh
        / equalAngleWeight alpha st sh
      = 1 / (2 * sh ^ 2) := by
  unfold equalAngleMeridionalTotal equalAngleWeight
  field_simp [halpha, hst, hsh]
  ring

/-- The rate of each azimuthal edge is exactly
`1 / (2 * v * st^2)`. -/
theorem equalAngle_azimuth_rate
    (alpha st sh v : ℝ)
    (halpha : alpha ≠ 0) (hst : st ≠ 0)
    (hsh : sh ≠ 0) (hv : v ≠ 0) :
    equalAngleAzimuthConductance alpha sh v st
        / equalAngleWeight alpha st sh
      = 1 / (2 * v * st ^ 2) := by
  unfold equalAngleAzimuthConductance equalAngleWeight
  field_simp [halpha, hst, hsh, hv]
  ring

/-- Closed-form peak defect of the equal-angle stencil:

`epsilon = 2 sh^2 + st^2 v`,

where `2 sh^2 = 1 - cos(delta)` and `st^2 v` is the azimuthal
dot-product loss. -/
theorem equalAngle_peakDefect_formula
    (alpha st sh v bm bp : ℝ)
    (halpha : alpha ≠ 0) (hst : st ≠ 0)
    (hsh : sh ≠ 0) (hv : v ≠ 0)
    (hsum : bm + bp = equalAngleMeridionalTotal alpha st sh) :
    productLocalPeakDefect
        (equalAngleWeight alpha st sh)
        bm bp (equalAngleAzimuthConductance alpha sh v st)
        (2 * sh ^ 2) (st ^ 2 * v)
      = 2 * sh ^ 2 + st ^ 2 * v := by
  unfold productLocalPeakDefect
  rw [hsum]
  unfold equalAngleMeridionalTotal equalAngleAzimuthConductance
    equalAngleWeight
  field_simp [halpha, hst, hsh, hv]
  ring

/-- Closed-form total jump rate of the equal-angle stencil. -/
theorem equalAngle_rate_formula
    (alpha st sh v bm bp : ℝ)
    (halpha : alpha ≠ 0) (hst : st ≠ 0)
    (hsh : sh ≠ 0) (hv : v ≠ 0)
    (hsum : bm + bp = equalAngleMeridionalTotal alpha st sh) :
    productLocalRate
        (equalAngleWeight alpha st sh)
        bm bp (equalAngleAzimuthConductance alpha sh v st)
      = 1 / (2 * sh ^ 2) + 1 / (v * st ^ 2) := by
  unfold productLocalRate
  rw [hsum]
  unfold equalAngleMeridionalTotal equalAngleAzimuthConductance
    equalAngleWeight
  field_simp [halpha, hst, hsh, hv]
  ring

/-- On the polar ring of a square product grid, `st = sh` and
`v = 2 sh^2`; the maximum jump rate therefore has an explicit quartic term. -/
theorem squarePolar_rate_formula
    (alpha sh bm bp : ℝ)
    (halpha : alpha ≠ 0) (hsh : sh ≠ 0)
    (hsum : bm + bp = equalAngleMeridionalTotal alpha sh sh) :
    productLocalRate
        (equalAngleWeight alpha sh sh)
        bm bp
        (equalAngleAzimuthConductance alpha sh (2 * sh ^ 2) sh)
      = 1 / (2 * sh ^ 2) + 1 / (2 * sh ^ 4) := by
  have hv : 2 * sh ^ 2 ≠ 0 := by
    nlinarith [sq_pos_of_ne_zero hsh]
  rw [equalAngle_rate_formula
    (alpha := alpha) (st := sh) (sh := sh) (v := 2 * sh ^ 2)
    (bm := bm) (bp := bp) halpha hsh hsh hv hsum]
  field_simp [hsh]
  ring

/-- The polar peak defect on the same square product grid. -/
theorem squarePolar_peakDefect_formula
    (alpha sh bm bp : ℝ)
    (halpha : alpha ≠ 0) (hsh : sh ≠ 0)
    (hsum : bm + bp = equalAngleMeridionalTotal alpha sh sh) :
    productLocalPeakDefect
        (equalAngleWeight alpha sh sh)
        bm bp
        (equalAngleAzimuthConductance alpha sh (2 * sh ^ 2) sh)
        (2 * sh ^ 2) (sh ^ 2 * (2 * sh ^ 2))
      = 2 * sh ^ 2 + 2 * sh ^ 4 := by
  have hv : 2 * sh ^ 2 ≠ 0 := by
    nlinarith [sq_pos_of_ne_zero hsh]
  rw [equalAngle_peakDefect_formula
    (alpha := alpha) (st := sh) (sh := sh) (v := 2 * sh ^ 2)
    (bm := bm) (bp := bp) halpha hsh hsh hv hsum]
  ring

/-- The closed-form defect is strictly positive under nondegenerate angular
steps and an interior latitude. -/
theorem equalAngle_defect_pos
    (st sh v : ℝ) (hst : 0 < st) (hsh : 0 < sh) (hv : 0 < v) :
    0 < 2 * sh ^ 2 + st ^ 2 * v := by
  positivity

end AFPBarrier

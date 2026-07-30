import AFPBarrier.QuasiUniformLossBounds
import Mathlib.Analysis.SpecialFunctions.Trigonometric.Bounds
import Mathlib.Tactic

/-!
# Explicit scaling for maximal spherical nets

For a spherical degree-one zonal mode at a node `i`, the loss to a neighbour at
geodesic angle `theta` is

  `1 - cos theta`.

A maximal `h`-separated spherical set has covering radius at most `h`. Every
edge of its spherical Delaunay graph therefore has angle in `[h, 2h]`: the
lower bound is separation, while a shared Voronoi point gives the upper bound.

For `0 < h <= pi/4`, this module proves the explicit loss window

  `(2/pi^2) h^2 <= 1 - cos theta <= 2 h^2`.

Combined with `QuasiUniformLossBounds`, this yields the natural diffusion
scales `rate = Theta(h^-2)` and `defect = Theta(h^2)` with explicit constants.
The metric-net and Delaunay incidence statements are geometric inputs; all
analytic and jump-generator consequences are kernel checked here.
-/

namespace AFPBarrier

noncomputable section

variable {ι : Type*} [Fintype ι] [DecidableEq ι]

/-- Angular chord loss associated with a geodesic separation. -/
def sphericalLoss (theta : ℝ) : ℝ := 1 - Real.cos theta

/-- Half-angle representation of spherical angular loss. -/
theorem sphericalLoss_eq_two_sin_sq_half (theta : ℝ) :
    sphericalLoss theta = 2 * Real.sin (theta / 2) ^ 2 := by
  unfold sphericalLoss
  have hcos := Real.cos_two_mul (theta / 2)
  rw [show 2 * (theta / 2) = theta by ring] at hcos
  have htrig := Real.sin_sq_add_cos_sq (theta / 2)
  rw [hcos]
  nlinarith

/-- Jordan's inequality gives a quadratic lower bound on angular loss. -/
theorem sphericalLoss_lower_quadratic
    (h : ℝ) (hh0 : 0 ≤ h) (hhpi : h ≤ Real.pi) :
    (2 / Real.pi ^ 2) * h ^ 2 ≤ sphericalLoss h := by
  have hx0 : 0 ≤ h / 2 := by linarith
  have hxhalf : h / 2 ≤ Real.pi / 2 := by linarith
  have hslo : 2 / Real.pi * (h / 2) ≤ Real.sin (h / 2) :=
    Real.mul_le_sin hx0 hxhalf
  have ha0 : 0 ≤ 2 / Real.pi * (h / 2) := by positivity
  have hs0 : 0 ≤ Real.sin (h / 2) := le_trans ha0 hslo
  have hsq : (2 / Real.pi * (h / 2)) ^ 2 ≤ Real.sin (h / 2) ^ 2 := by
    have hp := mul_nonneg (sub_nonneg.mpr hslo) (add_nonneg ha0 hs0)
    nlinarith
  rw [sphericalLoss_eq_two_sin_sq_half]
  have hform :
      2 * (2 / Real.pi * (h / 2)) ^ 2
        = (2 / Real.pi ^ 2) * h ^ 2 := by
    field_simp [Real.pi_ne_zero]
  rw [← hform]
  nlinarith

/-- The loss at angular separation `2h` is at most `2h^2`. -/
theorem sphericalLoss_two_mul_upper (h : ℝ) :
    sphericalLoss (2 * h) ≤ 2 * h ^ 2 := by
  rw [sphericalLoss_eq_two_sin_sq_half]
  rw [show (2 * h) / 2 = h by ring]
  have hs : Real.sin h ^ 2 ≤ h ^ 2 := Real.sin_sq_le_sq
  nlinarith

/-- Every angle in `[h,2h]`, for `h <= pi/4`, has a uniformly quadratic loss. -/
theorem sphericalLoss_between_of_angle_window
    (h theta : ℝ)
    (hh0 : 0 ≤ h) (hhquarter : h ≤ Real.pi / 4)
    (htlower : h ≤ theta) (htupper : theta ≤ 2 * h) :
    (2 / Real.pi ^ 2) * h ^ 2 ≤ sphericalLoss theta
      ∧ sphericalLoss theta ≤ 2 * h ^ 2 := by
  have ht0 : 0 ≤ theta := le_trans hh0 htlower
  have htwopi : 2 * h ≤ Real.pi := by linarith [Real.pi_pos]
  have htpi : theta ≤ Real.pi := htupper.trans htwopi
  have hcosLower : Real.cos theta ≤ Real.cos h :=
    Real.cos_le_cos_of_nonneg_of_le_pi hh0 htpi htlower
  have hcosUpper : Real.cos (2 * h) ≤ Real.cos theta :=
    Real.cos_le_cos_of_nonneg_of_le_pi ht0 htwopi htupper
  have hlo := sphericalLoss_lower_quadratic h hh0 (by linarith [Real.pi_pos])
  have hup := sphericalLoss_two_mul_upper h
  unfold sphericalLoss at hlo hup ⊢
  constructor <;> linarith

/-- Explicit rate and defect bounds for a degree-one exact spherical net row.

The geometric input says each active neighbour has some angular separation in
`[h,2h]`, and its zonal loss is exactly `1-cos(theta)`.
-/
theorem sphericalNet_peak_rate_defect_bounds
    (a : ι → ι → ℝ) (f : ι → ℝ) (i : ι) (h : ℝ)
    (hh0 : 0 < h) (hhquarter : h ≤ Real.pi / 4)
    (ha : ∀ j, j ≠ i → 0 ≤ a i j)
    (hfi : f i = 1)
    (hlinear : jumpGenerator a f i = -(2 : ℝ))
    (hangle : ∀ j, j ≠ i → ∃ theta : ℝ,
      h ≤ theta ∧ theta ≤ 2 * h ∧ f i - f j = sphericalLoss theta) :
    2 / (2 * h ^ 2) ≤ jumpRate a i
      ∧ jumpRate a i ≤ 2 / ((2 / Real.pi ^ 2) * h ^ 2)
      ∧ ((2 / Real.pi ^ 2) * h ^ 2) * 2 ≤ peakDefect a f i 2
      ∧ peakDefect a f i 2 ≤ (2 * h ^ 2) * 2 := by
  have hlower : ∀ j, j ≠ i → (2 / Real.pi ^ 2) * h ^ 2 ≤ f i - f j := by
    intro j hji
    rcases hangle j hji with ⟨theta, htlo, hthi, hloss⟩
    rw [hloss]
    exact (sphericalLoss_between_of_angle_window h theta hh0.le hhquarter htlo hthi).1
  have hupper : ∀ j, j ≠ i → f i - f j ≤ 2 * h ^ 2 := by
    intro j hji
    rcases hangle j hji with ⟨theta, htlo, hthi, hloss⟩
    rw [hloss]
    exact (sphericalLoss_between_of_angle_window h theta hh0.le hhquarter htlo hthi).2
  exact quadraticLoss_rate_defect_bounds
    a f i 2 (2 / Real.pi ^ 2) 2 h ha
    (by positivity) (by norm_num) hh0 hlower hupper hfi hlinear

/-- Multiplicative form of the explicit spherical-net bounds.

This avoids inverse notation and is convenient for asymptotic and node-count
comparisons.
-/
theorem sphericalNet_peak_rate_defect_bounds_mul
    (a : ι → ι → ℝ) (f : ι → ℝ) (i : ι) (h : ℝ)
    (hh0 : 0 < h) (hhquarter : h ≤ Real.pi / 4)
    (ha : ∀ j, j ≠ i → 0 ≤ a i j)
    (hfi : f i = 1)
    (hlinear : jumpGenerator a f i = -(2 : ℝ))
    (hangle : ∀ j, j ≠ i → ∃ theta : ℝ,
      h ≤ theta ∧ theta ≤ 2 * h ∧ f i - f j = sphericalLoss theta) :
    1 ≤ h ^ 2 * jumpRate a i
      ∧ h ^ 2 * jumpRate a i ≤ Real.pi ^ 2
      ∧ (4 / Real.pi ^ 2) * h ^ 2 ≤ peakDefect a f i 2
      ∧ peakDefect a f i 2 ≤ 4 * h ^ 2 := by
  have hb := sphericalNet_peak_rate_defect_bounds
    a f i h hh0 hhquarter ha hfi hlinear hangle
  have hh2 : 0 < h ^ 2 := sq_pos_of_pos hh0
  constructor
  · have hm := mul_le_mul_of_nonneg_left hb.1 hh2.le
    have hleft : h ^ 2 * (2 / (2 * h ^ 2)) = 1 := by
      field_simp [hh0.ne']
    rw [hleft] at hm
    simpa [mul_comm] using hm
  constructor
  · have hm := mul_le_mul_of_nonneg_left hb.2.1 hh2.le
    have hright :
        h ^ 2 * (2 / ((2 / Real.pi ^ 2) * h ^ 2)) = Real.pi ^ 2 := by
      field_simp [Real.pi_ne_zero, hh0.ne']
    rw [hright] at hm
    simpa [mul_comm] using hm
  constructor
  · have hd := hb.2.2.1
    convert hd using 1 <;> ring
  · have hd := hb.2.2.2
    convert hd using 1 <;> ring

end

end AFPBarrier

import AFPBarrier.QuadraticEqualityGeometry
import Mathlib.Tactic

/-!
# Elementary finite core for quantitative stability at the quadratic frontier

This module formalizes the scalar budget extraction used by P1D.  The main
hypothesis is the normalized master inequality

`sum w_i (2 q_i + q_i^2) + beta * E_B <= eta`.

The proofs keep the weights, the two nonnegative components of `q`, and the
coefficient of the tensor defect explicit.  In particular, no lower bound on
an individual weight is used until the pointwise theorem.
-/

open scoped BigOperators

namespace AFPBarrier

variable {I : Type*} [Fintype I] [DecidableEq I]

/-- The normalized frontier slack is `(1 + delta)^2 - 1`. -/
theorem quadraticStability_slack_identity (delta : ℝ) :
    (1 + delta) ^ 2 - 1 = 2 * delta + delta ^ 2 := by
  ring

/-- Dropping the nonnegative linear and tensor parts of the master budget
gives the weighted quadratic bound for the total scalar defect. -/
theorem quadraticStability_total_sq_budget
    (w q : I → ℝ) (beta EB eta : ℝ)
    (hw : ∀ i, 0 ≤ w i)
    (hq : ∀ i, 0 ≤ q i)
    (hbeta : 0 ≤ beta)
    (hEB : 0 ≤ EB)
    (hmaster :
      (∑ i, w i * (2 * q i + (q i) ^ 2)) + beta * EB ≤ eta) :
    ∑ i, w i * (q i) ^ 2 ≤ eta := by
  have htensor : 0 ≤ beta * EB := mul_nonneg hbeta hEB
  calc
    (∑ i, w i * (q i) ^ 2) ≤
        ∑ i, w i * (2 * q i + (q i) ^ 2) := by
      apply Finset.sum_le_sum
      intro i hi
      have hlinear : 0 ≤ w i * (2 * q i) :=
        mul_nonneg (hw i) (mul_nonneg (by norm_num) (hq i))
      nlinarith
    _ ≤ (∑ i, w i * (2 * q i + (q i) ^ 2)) + beta * EB :=
      le_add_of_nonneg_right htensor
    _ ≤ eta := hmaster

/-- The same master budget controls the weighted first moment of the total
scalar defect.  The sharper `delta` bound in the ordinary theorem additionally
uses normalized weights and weighted Cauchy--Schwarz. -/
theorem quadraticStability_total_linear_budget
    (w q : I → ℝ) (beta EB eta : ℝ)
    (hw : ∀ i, 0 ≤ w i)
    (hq : ∀ i, 0 ≤ q i)
    (hbeta : 0 ≤ beta)
    (hEB : 0 ≤ EB)
    (hmaster :
      (∑ i, w i * (2 * q i + (q i) ^ 2)) + beta * EB ≤ eta) :
    2 * (∑ i, w i * q i) ≤ eta := by
  have htensor : 0 ≤ beta * EB := mul_nonneg hbeta hEB
  calc
    2 * (∑ i, w i * q i) = ∑ i, w i * (2 * q i) := by
      rw [Finset.mul_sum]
      apply Finset.sum_congr rfl
      intro i hi
      ring
    _ ≤ ∑ i, w i * (2 * q i + (q i) ^ 2) := by
      apply Finset.sum_le_sum
      intro i hi
      have hsquare : 0 ≤ w i * (q i) ^ 2 :=
        mul_nonneg (hw i) (sq_nonneg (q i))
      nlinarith
    _ ≤ (∑ i, w i * (2 * q i + (q i) ^ 2)) + beta * EB :=
      le_add_of_nonneg_right htensor
    _ ≤ eta := hmaster

/-- If the total normalized defect splits as `q = s + v` with nonnegative
rate and variance defects, each component inherits the total square budget. -/
theorem quadraticStability_component_sq_budget
    (w q s v : I → ℝ) (eta : ℝ)
    (hw : ∀ i, 0 ≤ w i)
    (hs : ∀ i, 0 ≤ s i)
    (hv : ∀ i, 0 ≤ v i)
    (hsplit : ∀ i, q i = s i + v i)
    (hqSq : ∑ i, w i * (q i) ^ 2 ≤ eta) :
    (∑ i, w i * (s i) ^ 2 ≤ eta) ∧
      (∑ i, w i * (v i) ^ 2 ≤ eta) := by
  constructor
  · calc
      (∑ i, w i * (s i) ^ 2) ≤ ∑ i, w i * (q i) ^ 2 := by
        apply Finset.sum_le_sum
        intro i hi
        have hsq : (s i) ^ 2 ≤ (q i) ^ 2 := by
          rw [hsplit i]
          have hsv : 0 ≤ s i * v i := mul_nonneg (hs i) (hv i)
          nlinarith [sq_nonneg (v i)]
        exact mul_le_mul_of_nonneg_left hsq (hw i)
      _ ≤ eta := hqSq
  · calc
      (∑ i, w i * (v i) ^ 2) ≤ ∑ i, w i * (q i) ^ 2 := by
        apply Finset.sum_le_sum
        intro i hi
        have hsq : (v i) ^ 2 ≤ (q i) ^ 2 := by
          rw [hsplit i]
          have hsv : 0 ≤ s i * v i := mul_nonneg (hs i) (hv i)
          nlinarith [sq_nonneg (s i)]
        exact mul_le_mul_of_nonneg_left hsq (hw i)
      _ ≤ eta := hqSq

/-- At a positive-mass vertex the global square budget gives the exact
`1 / w_i` pointwise dependence. -/
theorem quadraticStability_pointwise_sq_budget
    (w q : I → ℝ) (eta : ℝ) (i : I)
    (hw : ∀ j, 0 ≤ w j)
    (hwi : 0 < w i)
    (hbudget : ∑ j, w j * (q j) ^ 2 ≤ eta) :
    (q i) ^ 2 ≤ eta / w i := by
  have hterm : w i * (q i) ^ 2 ≤ ∑ j, w j * (q j) ^ 2 := by
    exact Finset.single_le_sum
      (fun j hj => mul_nonneg (hw j) (sq_nonneg (q j)))
      (Finset.mem_univ i)
  apply (le_div_iff₀ hwi).2
  simpa [mul_comm] using le_trans hterm hbudget

/-- Uniform positive vertex mass turns the weighted estimate into a uniform
pointwise estimate, with the exact inverse dependence on `wmin`. -/
theorem quadraticStability_pointwise_sq_budget_of_wmin
    (w q : I → ℝ) (eta wmin : ℝ)
    (hwmin : 0 < wmin)
    (hw : ∀ i, wmin ≤ w i)
    (hbudget : ∑ i, w i * (q i) ^ 2 ≤ eta) :
    ∀ i, (q i) ^ 2 ≤ eta / wmin := by
  intro i
  have hnonneg : ∀ j, 0 ≤ w j := fun j =>
    le_trans (le_of_lt hwmin) (hw j)
  have hterm : wmin * (q i) ^ 2 ≤ w i * (q i) ^ 2 :=
    mul_le_mul_of_nonneg_right (hw i) (sq_nonneg (q i))
  apply (le_div_iff₀ hwmin).2
  have hiWeighted : w i * (q i) ^ 2 ≤ eta := by
    have hsingle : w i * (q i) ^ 2 ≤
        ∑ j, w j * (q j) ^ 2 := by
      exact Finset.single_le_sum
        (fun j hj => mul_nonneg (hnonneg j) (sq_nonneg (q j)))
        (Finset.mem_univ i)
    exact le_trans hsingle hbudget
  simpa [mul_comm] using le_trans hterm hiWeighted

/-- Weighted Chebyshev bound, represented without a filtered subtype: the
indicator sum is the stationary mass of vertices with `t <= q_i`. -/
theorem quadraticStability_badVertexMass
    (w q : I → ℝ) (eta t : ℝ)
    (hw : ∀ i, 0 ≤ w i)
    (ht : 0 ≤ t)
    (hbudget : ∑ i, w i * (q i) ^ 2 ≤ eta) :
    t ^ 2 * (∑ i, if t ≤ q i then w i else 0) ≤ eta := by
  calc
    t ^ 2 * (∑ i, if t ≤ q i then w i else 0) =
        ∑ i, t ^ 2 * (if t ≤ q i then w i else 0) := by
          rw [Finset.mul_sum]
    _ ≤ ∑ i, w i * (q i) ^ 2 := by
      apply Finset.sum_le_sum
      intro i hi
      by_cases hbad : t ≤ q i
      · simp only [hbad, if_true]
        have hfactor : 0 ≤ (q i - t) * (q i + t) :=
          mul_nonneg (sub_nonneg.mpr hbad) (by linarith)
        have hsq : t ^ 2 ≤ (q i) ^ 2 := by nlinarith
        nlinarith [mul_le_mul_of_nonneg_left hsq (hw i)]
      · simp only [hbad, if_false]
        exact mul_nonneg (hw i) (sq_nonneg (q i))
    _ ≤ eta := hbudget

/-- Retaining the linear part gives the sharper bad-vertex denominator
`t (2+t)`, which is attained by a defect concentrated on one mass block. -/
theorem quadraticStability_badVertexMass_sharp
    (w q : I → ℝ) (eta t : ℝ)
    (hw : ∀ i, 0 ≤ w i)
    (hq : ∀ i, 0 ≤ q i)
    (ht : 0 ≤ t)
    (hbudget : ∑ i, w i * (2 * q i + (q i) ^ 2) ≤ eta) :
    t * (2 + t) * (∑ i, if t ≤ q i then w i else 0) ≤ eta := by
  calc
    t * (2 + t) * (∑ i, if t ≤ q i then w i else 0) =
        ∑ i, (t * (2 + t)) *
          (if t ≤ q i then w i else 0) := by
            rw [Finset.mul_sum]
    _ ≤ ∑ i, w i * (2 * q i + (q i) ^ 2) := by
      apply Finset.sum_le_sum
      intro i hi
      by_cases hbad : t ≤ q i
      · simp only [hbad, if_true]
        have hfactor : 0 ≤ (q i - t) * (q i + t + 2) :=
          mul_nonneg (sub_nonneg.mpr hbad) (by linarith)
        have hpoly : t * (2 + t) ≤ 2 * q i + (q i) ^ 2 := by
          nlinarith
        nlinarith [mul_le_mul_of_nonneg_left hpoly (hw i)]
      · simp only [hbad, if_false]
        have hinside : 0 ≤ 2 * q i + (q i) ^ 2 := by
          nlinarith [hq i, sq_nonneg (q i)]
        exact mul_nonneg (hw i) hinside
    _ ≤ eta := hbudget

/-- The full local scalar budget at a positive-mass vertex.  Solving this
quadratic inequality gives `q_i <= sqrt (1 + eta / w_i) - 1`. -/
theorem quadraticStability_pointwise_full_budget
    (w q : I → ℝ) (eta : ℝ) (i : I)
    (hw : ∀ j, 0 ≤ w j)
    (hwi : 0 < w i)
    (hq : ∀ j, 0 ≤ q j)
    (hbudget : ∑ j, w j * (2 * q j + (q j) ^ 2) ≤ eta) :
    2 * q i + (q i) ^ 2 ≤ eta / w i := by
  have hterm : w i * (2 * q i + (q i) ^ 2) ≤
      ∑ j, w j * (2 * q j + (q j) ^ 2) := by
    exact Finset.single_le_sum
      (fun j hj => by
        have hinside : 0 ≤ 2 * q j + (q j) ^ 2 := by
          nlinarith [hq j, sq_nonneg (q j)]
        exact mul_nonneg (hw j) hinside)
      (Finset.mem_univ i)
  apply (le_div_iff₀ hwi).2
  simpa [mul_comm] using le_trans hterm hbudget

/-- The tensor part of the master inequality, before substituting the
geometric value of `a0`. -/
theorem quadraticStability_tensor_budget
    (w q : I → ℝ) (d a0 EB eta : ℝ)
    (hd : 1 < d)
    (ha0 : 0 < a0)
    (hw : ∀ i, 0 ≤ w i)
    (hq : ∀ i, 0 ≤ q i)
    (hEB : 0 ≤ EB)
    (hmaster :
      (∑ i, w i * (2 * q i + (q i) ^ 2)) +
          (d - 1) / (d * a0 ^ 2) * EB ≤ eta) :
    EB ≤ d * a0 ^ 2 / (d - 1) * eta := by
  have hdpos : 0 < d := lt_trans zero_lt_one hd
  have hdm1pos : 0 < d - 1 := sub_pos.mpr hd
  have hcoefpos : 0 < (d - 1) / (d * a0 ^ 2) := by positivity
  have hscalar : 0 ≤ ∑ i, w i * (2 * q i + (q i) ^ 2) := by
    apply Finset.sum_nonneg
    intro i hi
    have hinside : 0 ≤ 2 * q i + (q i) ^ 2 := by
      nlinarith [hq i, sq_nonneg (q i)]
    exact mul_nonneg (hw i) hinside
  have hcoefEB : (d - 1) / (d * a0 ^ 2) * EB ≤ eta := by
    linarith
  have hdiv : EB ≤ eta / ((d - 1) / (d * a0 ^ 2)) :=
    (le_div_iff₀ hcoefpos).2 hcoefEB
  calc
    EB ≤ eta / ((d - 1) / (d * a0 ^ 2)) := hdiv
    _ = d * a0 ^ 2 / (d - 1) * eta := by
      field_simp [ne_of_gt hdpos, ne_of_gt hdm1pos, ne_of_gt ha0]
      <;> ring

/-- Substituting `a0 = (d-1)^2 / rmax` gives the published tensor constant
`d (d-1)^3 / rmax^2`. -/
theorem quadraticStability_tensor_rate_bound
    (w q : I → ℝ) (d rmax EB eta : ℝ)
    (hd : 1 < d)
    (hrmax : 0 < rmax)
    (hw : ∀ i, 0 ≤ w i)
    (hq : ∀ i, 0 ≤ q i)
    (hEB : 0 ≤ EB)
    (hmaster :
      (∑ i, w i * (2 * q i + (q i) ^ 2)) +
          (d - 1) /
              (d * (((d - 1) ^ 2 / rmax) ^ 2)) * EB ≤ eta) :
    EB ≤ d * (d - 1) ^ 3 / rmax ^ 2 * eta := by
  have ha0 : 0 < (d - 1) ^ 2 / rmax := by
    have hdm1 : 0 < d - 1 := sub_pos.mpr hd
    positivity
  have h := quadraticStability_tensor_budget
    (w := w) (q := q) (d := d) (a0 := (d - 1) ^ 2 / rmax)
    (EB := EB) (eta := eta) hd ha0 hw hq hEB hmaster
  calc
    EB ≤ d * ((d - 1) ^ 2 / rmax) ^ 2 / (d - 1) * eta := h
    _ = d * (d - 1) ^ 3 / rmax ^ 2 * eta := by
      have hdpos : 0 < d := lt_trans zero_lt_one hd
      have hdm1pos : 0 < d - 1 := sub_pos.mpr hd
      field_simp [ne_of_gt hdpos, ne_of_gt hdm1pos, ne_of_gt hrmax]
      <;> ring

/-- Restoring dimensions from `v_i = V_i / a0`: the weighted squared loss
variance is at most `a0^2 eta`. -/
theorem quadraticStability_scaledVariance_sq_budget
    (w v V : I → ℝ) (a0 eta : ℝ)
    (hw : ∀ i, 0 ≤ w i)
    (hscale : ∀ i, V i = a0 * v i)
    (hbudget : ∑ i, w i * (v i) ^ 2 ≤ eta) :
    ∑ i, w i * (V i) ^ 2 ≤ a0 ^ 2 * eta := by
  calc
    (∑ i, w i * (V i) ^ 2) =
        a0 ^ 2 * (∑ i, w i * (v i) ^ 2) := by
      rw [Finset.mul_sum]
      apply Finset.sum_congr rfl
      intro i hi
      rw [hscale i]
      ring
    _ ≤ a0 ^ 2 * eta :=
      mul_le_mul_of_nonneg_left hbudget (sq_nonneg a0)

/-- A convenient all-at-once wrapper for the three requested scalar square
bounds with `eta = 2 delta + delta^2`. -/
theorem quadraticStability_master_square_consequences
    (w q s v : I → ℝ) (beta EB delta : ℝ)
    (hw : ∀ i, 0 ≤ w i)
    (hq : ∀ i, 0 ≤ q i)
    (hs : ∀ i, 0 ≤ s i)
    (hv : ∀ i, 0 ≤ v i)
    (hsplit : ∀ i, q i = s i + v i)
    (hbeta : 0 ≤ beta)
    (hEB : 0 ≤ EB)
    (hmaster :
      (∑ i, w i * (2 * q i + (q i) ^ 2)) + beta * EB ≤
        2 * delta + delta ^ 2) :
    (∑ i, w i * (q i) ^ 2 ≤ 2 * delta + delta ^ 2) ∧
      (∑ i, w i * (s i) ^ 2 ≤ 2 * delta + delta ^ 2) ∧
      (∑ i, w i * (v i) ^ 2 ≤ 2 * delta + delta ^ 2) := by
  have hqSq := quadraticStability_total_sq_budget
    w q beta EB (2 * delta + delta ^ 2) hw hq hbeta hEB hmaster
  have hcomponents := quadraticStability_component_sq_budget
    w q s v (2 * delta + delta ^ 2) hw hs hv hsplit hqSq
  exact ⟨hqSq, hcomponents.1, hcomponents.2⟩

/-- Pure scalar endgame: once a nonnegative mean `m` satisfies the normalized
quadratic slack inequality, it is at most `delta`. -/
theorem quadraticStability_mean_le_delta
    (m delta : ℝ)
    (hm : 0 ≤ m)
    (hdelta : 0 ≤ delta)
    (hbudget : 2 * m + m ^ 2 ≤ 2 * delta + delta ^ 2) :
    m ≤ delta := by
  by_contra hnot
  have hmd : delta < m := lt_of_not_ge hnot
  have hpos : 0 < (m - delta) * (m + delta + 2) := by
    apply mul_pos
    · linarith
    · linarith
  nlinarith

/-- With normalized nonnegative weights, weighted Cauchy--Schwarz upgrades
the linear part of the master budget to the sharp bound
`sum_i w_i q_i <= delta`. -/
theorem quadraticStability_weightedMean_le_delta
    (w q : I → ℝ) (beta EB delta : ℝ)
    (hw : ∀ i, 0 ≤ w i)
    (hsum : ∑ i, w i = 1)
    (hq : ∀ i, 0 ≤ q i)
    (hbeta : 0 ≤ beta)
    (hEB : 0 ≤ EB)
    (hdelta : 0 ≤ delta)
    (hmaster :
      (∑ i, w i * (2 * q i + (q i) ^ 2)) + beta * EB ≤
        2 * delta + delta ^ 2) :
    ∑ i, w i * q i ≤ delta := by
  let m : ℝ := ∑ i, w i * q i
  have hm : 0 ≤ m := by
    dsimp [m]
    apply Finset.sum_nonneg
    intro i hi
    exact mul_nonneg (hw i) (hq i)
  have hcsRaw := Finset.sum_sq_le_sum_mul_sum_of_sq_le_mul
    Finset.univ
    (r := fun i => w i * q i)
    (f := fun i => w i)
    (g := fun i => w i * (q i) ^ 2)
    (fun i hi => hw i)
    (fun i hi => mul_nonneg (hw i) (sq_nonneg (q i)))
    (fun i hi => by
      apply le_of_eq
      ring)
  have hcs : m ^ 2 ≤ ∑ i, w i * (q i) ^ 2 := by
    dsimp [m]
    simpa [hsum] using hcsRaw
  have htensor : 0 ≤ beta * EB := mul_nonneg hbeta hEB
  have hscalar :
      ∑ i, w i * (2 * q i + (q i) ^ 2) ≤
        2 * delta + delta ^ 2 := by
    linarith
  have hdecompose :
      ∑ i, w i * (2 * q i + (q i) ^ 2) =
        2 * m + ∑ i, w i * (q i) ^ 2 := by
    dsimp [m]
    calc
      (∑ i, w i * (2 * q i + (q i) ^ 2)) =
          ∑ i, (2 * (w i * q i) + w i * (q i) ^ 2) := by
        apply Finset.sum_congr rfl
        intro i hi
        ring
      _ = 2 * (∑ i, w i * q i) +
          ∑ i, w i * (q i) ^ 2 := by
        rw [Finset.sum_add_distrib, Finset.mul_sum]
  have hmeanBudget : 2 * m + m ^ 2 ≤ 2 * delta + delta ^ 2 := by
    rw [hdecompose] at hscalar
    linarith
  exact quadraticStability_mean_le_delta m delta hm hdelta hmeanBudget

end AFPBarrier

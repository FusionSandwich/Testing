import Mathlib
import Mathlib.Analysis.Real.Pi.Bounds
import Erdos1084.RadiusTwoAssembly

namespace Erdos1084

/-!
# Audited Kepler / outer-parallel arithmetic bridge

This module certifies the algebraic and abstract local-to-global part of the candidate
coefficient `2.0465`.

There are **no project-specific axioms** in this file. The external geometric content is passed
through explicit theorem parameters:

* `KeplerGlobalSurfaceInput` records the surface lower bound obtained from the Kepler density,
  the outer-parallel truncated-density identity for `λ ≥ 1`, and Euclidean isoperimetry;
* local degree charges are converted to `KeplerLocalSurfaceInput` by a proved finite-sum lemma.

The positive scale `K` is not arbitrary: `KeplerScaleSpec K` states exactly
`K^3 * π^2 = 18`. The power variable `x` is tied to the packing size by
`KeplerPowerScale n x`, namely `n > 0`, `x ≥ 0`, and `x^3 = n^2`.
-/

noncomputable section

/-- `sqrt 3`. -/
def kpS : ℝ := Real.sqrt 3

/-- The common endpoint charge `1 - sqrt 3 / 2`. -/
def kpQ : ℝ := 1 - kpS / 2

/-- The exact optimized enlargement radius. -/
def kpRadius : ℝ := (40 + 22 * kpS) / 37

/-- The reciprocal of `kpRadius^2 * kpQ`. -/
def kpLocalCoeff : ℝ := 103 - 117 * kpS / 2

/-- The clean advertised coefficient `2.0465`. -/
def kpClean : ℝ := 4093 / 2000

@[simp] theorem kpS_sq : kpS ^ 2 = 3 := by
  norm_num [kpS]

@[simp] theorem kpS_nonneg : 0 ≤ kpS := by
  exact Real.sqrt_nonneg _

@[simp] theorem kpS_pos : 0 < kpS := by
  exact Real.sqrt_pos.2 (by norm_num)

/-- A rational upper bound for `sqrt 3` used by the exact decimal certificate. -/
theorem kpS_lt_compact : kpS < (1732050808 : ℝ) / 1000000000 := by
  have hs0 : 0 ≤ kpS := kpS_nonneg
  have hs2 : kpS ^ 2 = 3 := kpS_sq
  have hu0 : 0 ≤ (1732050808 : ℝ) / 1000000000 := by norm_num
  have hu2 : (3 : ℝ) < ((1732050808 : ℝ) / 1000000000) ^ 2 := by
    norm_num
  nlinarith

@[simp] theorem kpQ_pos : 0 < kpQ := by
  have hslt : kpS < 2 := by
    have hs0 : 0 ≤ kpS := kpS_nonneg
    have hs2 : kpS ^ 2 = 3 := kpS_sq
    nlinarith
  dsimp [kpQ]
  linarith

/-- The optimized radius is strictly larger than two. -/
theorem two_lt_kpRadius : 2 < kpRadius := by
  have h17 : (17 : ℝ) < 11 * kpS := by
    have hs0 : 0 ≤ kpS := kpS_nonneg
    have hs2 : kpS ^ 2 = 3 := kpS_sq
    nlinarith
  dsimp [kpRadius]
  nlinarith

@[simp] theorem kpRadius_pos : 0 < kpRadius := by
  exact lt_trans (by norm_num : (0 : ℝ) < 2) two_lt_kpRadius

/-- The corresponding outer-parallel radius `λ = kpRadius - 1` exceeds one. -/
theorem one_lt_kpOuterRadius : 1 < kpRadius - 1 := by
  linarith [two_lt_kpRadius]

/-- Product form of the reciprocal-radius identity. -/
theorem kpRadius_times_reciprocal_rhs :
    kpRadius * (10 - 11 * kpS / 2) = 1 := by
  dsimp [kpRadius]
  field_simp
  nlinarith [kpS_sq]

/-- Exact reciprocal-radius identity. -/
theorem kpRadius_reciprocal :
    1 / kpRadius = 10 - 11 * kpS / 2 := by
  have hrne : kpRadius ≠ 0 := ne_of_gt kpRadius_pos
  apply (div_eq_iff hrne).2
  calc
    1 = kpRadius * (10 - 11 * kpS / 2) := by
      symm
      exact kpRadius_times_reciprocal_rhs
    _ = (10 - 11 * kpS / 2) * kpRadius := by ring

/-- Exact simplification of the local coefficient. -/
theorem kp_local_identity :
    kpRadius ^ 2 * kpQ * kpLocalCoeff = 1 := by
  have h37 : (37 : ℝ) ≠ 0 := by norm_num
  dsimp [kpRadius, kpQ, kpLocalCoeff]
  field_simp [h37]
  nlinarith [kpS_sq]

/-- Rational lower bound for the exact local coefficient. -/
theorem kp_local_compact_lower :
    (418756933 : ℝ) / 250000000 < kpLocalCoeff := by
  have hs := kpS_lt_compact
  dsimp [kpLocalCoeff]
  linarith

@[simp] theorem kpLocalCoeff_pos : 0 < kpLocalCoeff := by
  have h := kp_local_compact_lower
  have hrat : 0 < (418756933 : ℝ) / 250000000 := by norm_num
  linarith

@[simp] theorem kpClean_pos : 0 < kpClean := by
  norm_num [kpClean]

/-- Exact cubed certificate: `kpClean^3 * π^2 < 18 * kpLocalCoeff^3`. -/
theorem kp_clean_cubed_certificate :
    kpClean ^ 3 * Real.pi ^ 2 < 18 * kpLocalCoeff ^ 3 := by
  have hp : Real.pi < (3.141593 : ℝ) := Real.pi_lt_d6
  have hpSq : Real.pi ^ 2 < (3.141593 : ℝ) ^ 2 := by
    nlinarith [Real.pi_pos]
  let a : ℝ := (418756933 : ℝ) / 250000000
  have ha0 : 0 < a := by norm_num [a]
  have hL : a < kpLocalCoeff := by
    simpa [a] using kp_local_compact_lower
  have hdiff : 0 < kpLocalCoeff - a := sub_pos.mpr hL
  have hb2 : 0 < kpLocalCoeff ^ 2 := sq_pos_of_pos kpLocalCoeff_pos
  have hba : 0 < kpLocalCoeff * a := mul_pos kpLocalCoeff_pos ha0
  have ha2 : 0 < a ^ 2 := sq_pos_of_pos ha0
  have hsum : 0 < kpLocalCoeff ^ 2 + kpLocalCoeff * a + a ^ 2 := by
    linarith
  have hprod : 0 < (kpLocalCoeff - a) *
      (kpLocalCoeff ^ 2 + kpLocalCoeff * a + a ^ 2) :=
    mul_pos hdiff hsum
  have haCube : a ^ 3 < kpLocalCoeff ^ 3 := by
    nlinarith
  have hrat :
      kpClean ^ 3 * (3.141593 : ℝ) ^ 2 < 18 * a ^ 3 := by
    norm_num [kpClean, a]
  have hcleanCube : 0 < kpClean ^ 3 := pow_pos kpClean_pos 3
  calc
    kpClean ^ 3 * Real.pi ^ 2
        < kpClean ^ 3 * (3.141593 : ℝ) ^ 2 := by
          exact mul_lt_mul_of_pos_left hpSq hcleanCube
    _ < 18 * a ^ 3 := hrat
    _ < 18 * kpLocalCoeff ^ 3 :=
      mul_lt_mul_of_pos_left haCube (by norm_num)

/-- Positive Kepler surface scale: `K^3 * π^2 = 18`. -/
def KeplerScaleSpec (K : ℝ) : Prop :=
  0 < K ∧ K ^ 3 * Real.pi ^ 2 = 18

/-- Positive representative of `n^(2/3)` without using the real-power API. -/
structure KeplerPowerScale (n x : ℝ) : Prop where
  n_pos : 0 < n
  x_nonneg : 0 ≤ x
  cube : x ^ 3 = n ^ 2

/-- The power-scale conditions force `x` to be strictly positive. -/
theorem KeplerPowerScale.x_pos {n x : ℝ} (h : KeplerPowerScale n x) :
    0 < x := by
  by_contra hnot
  have hxle : x ≤ 0 := le_of_not_gt hnot
  have hx0 : x = 0 := le_antisymm hxle h.x_nonneg
  have hn2 : 0 < n ^ 2 := sq_pos_of_pos h.n_pos
  have hcube := h.cube
  rw [hx0] at hcube
  norm_num at hcube
  nlinarith

/-- The cubed certificate implies the actual linear coefficient comparison. -/
theorem kp_clean_lt_scale_mul_local {K : ℝ}
    (hscale : KeplerScaleSpec K) :
    kpClean < K * kpLocalCoeff := by
  rcases hscale with ⟨hKpos, hKcube⟩
  have hpi2 : 0 < Real.pi ^ 2 := sq_pos_of_pos Real.pi_pos
  have hscaled :
      kpClean ^ 3 * Real.pi ^ 2 <
        (K * kpLocalCoeff) ^ 3 * Real.pi ^ 2 := by
    calc
      kpClean ^ 3 * Real.pi ^ 2
          < 18 * kpLocalCoeff ^ 3 := kp_clean_cubed_certificate
      _ = (K * kpLocalCoeff) ^ 3 * Real.pi ^ 2 := by
        rw [← hKcube]
        ring
  have hcube : kpClean ^ 3 < (K * kpLocalCoeff) ^ 3 := by
    by_contra hnot
    have hle : (K * kpLocalCoeff) ^ 3 ≤ kpClean ^ 3 := le_of_not_gt hnot
    have hmul := mul_le_mul_of_nonneg_right hle (le_of_lt hpi2)
    exact (not_le_of_gt hscaled) hmul
  have htarget0 : 0 ≤ K * kpLocalCoeff :=
    mul_nonneg (le_of_lt hKpos) (le_of_lt kpLocalCoeff_pos)
  by_contra hnot
  have hle : K * kpLocalCoeff ≤ kpClean := le_of_not_gt hnot
  have hdiff : 0 ≤ kpClean - K * kpLocalCoeff := sub_nonneg.mpr hle
  have hclean2 : 0 < kpClean ^ 2 := sq_pos_of_pos kpClean_pos
  have hmiddle : 0 ≤ kpClean * (K * kpLocalCoeff) :=
    mul_nonneg (le_of_lt kpClean_pos) htarget0
  have htarget2 : 0 ≤ (K * kpLocalCoeff) ^ 2 := sq_nonneg _
  have hsum : 0 < kpClean ^ 2 + kpClean * (K * kpLocalCoeff) +
      (K * kpLocalCoeff) ^ 2 := by
    linarith
  have hprod : 0 ≤ (kpClean - K * kpLocalCoeff) *
      (kpClean ^ 2 + kpClean * (K * kpLocalCoeff) +
        (K * kpLocalCoeff) ^ 2) :=
    mul_nonneg hdiff (le_of_lt hsum)
  have hcubeLe : (K * kpLocalCoeff) ^ 3 ≤ kpClean ^ 3 := by
    nlinarith
  exact (not_lt_of_ge hcubeLe) hcube

/-- Global surface lower-bound interface supplied by published density and isoperimetric inputs. -/
structure KeplerGlobalSurfaceInput (x A K : ℝ) : Prop where
  scale : KeplerScaleSpec K
  surface_lower : 4 * Real.pi * K * x ≤ A

/-- Local surface upper-bound interface. -/
structure KeplerLocalSurfaceInput (A D : ℝ) : Prop where
  surface_upper : A ≤ 4 * Real.pi * kpRadius ^ 2 * kpQ * D

/-- Build the local surface interface from per-sphere charges and the degree-sum identity. -/
theorem kp_local_surface_input_of_charges
    {ι : Type*} [Fintype ι]
    (d exposure : ι → ℝ)
    (n E A : ℝ)
    (hn : (Fintype.card ι : ℝ) = n)
    (hdeg : (∑ i, d i) = 2 * E)
    (hBoundary : A ≤ ∑ i, exposure i)
    (hLocal : ∀ i,
      exposure i ≤ 2 * Real.pi * kpRadius ^ 2 * kpQ * (12 - d i)) :
    KeplerLocalSurfaceInput A (6 * n - E) := by
  have hsum :
      (∑ i, exposure i) ≤
        ∑ i, 2 * Real.pi * kpRadius ^ 2 * kpQ * (12 - d i) :=
    Finset.sum_le_sum fun i _ => hLocal i
  have hdef := radiusTwo_degree_deficit_sum d n E hn hdeg
  constructor
  calc
    A ≤ ∑ i, exposure i := hBoundary
    _ ≤ ∑ i, 2 * Real.pi * kpRadius ^ 2 * kpQ * (12 - d i) := hsum
    _ = (2 * Real.pi * kpRadius ^ 2 * kpQ) * ∑ i, (12 - d i) := by
      rw [Finset.mul_sum]
    _ = (2 * Real.pi * kpRadius ^ 2 * kpQ) * (2 * (6 * n - E)) := by
      rw [hdef]
    _ = 4 * Real.pi * kpRadius ^ 2 * kpQ * (6 * n - E) := by ring

/-- Strict scalar assembly for the clean coefficient `2.0465`. -/
theorem kp_surface_assembly_strict
    {x A D K : ℝ}
    (hx : 0 < x)
    (hg : KeplerGlobalSurfaceInput x A K)
    (hl : KeplerLocalSurfaceInput A D) :
    kpClean * x < D := by
  have hcoeff : kpClean < K * kpLocalCoeff :=
    kp_clean_lt_scale_mul_local hg.scale
  have hchain :
      4 * Real.pi * K * x ≤
        4 * Real.pi * kpRadius ^ 2 * kpQ * D :=
    le_trans hg.surface_lower hl.surface_upper
  have hfourpi : 0 < 4 * Real.pi := by positivity
  have hchain' :
      (4 * Real.pi) * (K * x) ≤
        (4 * Real.pi) * (kpRadius ^ 2 * kpQ * D) := by
    simpa [mul_assoc] using hchain
  have hKx : K * x ≤ kpRadius ^ 2 * kpQ * D := by
    by_contra hnot
    have hrev : kpRadius ^ 2 * kpQ * D < K * x := lt_of_not_ge hnot
    have hmul := mul_lt_mul_of_pos_left hrev hfourpi
    exact (not_lt_of_ge hchain') hmul
  have hmul := mul_le_mul_of_nonneg_right hKx (le_of_lt kpLocalCoeff_pos)
  have hKlocal : K * kpLocalCoeff * x ≤ D := by
    calc
      K * kpLocalCoeff * x = (K * x) * kpLocalCoeff := by ring
      _ ≤ (kpRadius ^ 2 * kpQ * D) * kpLocalCoeff := hmul
      _ = (kpRadius ^ 2 * kpQ * kpLocalCoeff) * D := by ring
      _ = D := by rw [kp_local_identity]; ring
  have hclean : kpClean * x < K * kpLocalCoeff * x :=
    mul_lt_mul_of_pos_right hcoeff hx
  exact lt_of_lt_of_le hclean hKlocal

/-- Contact-number form, with `x` explicitly tied to `n^(2/3)`. -/
theorem kp_contact_upper_from_surface
    {n E x A K : ℝ}
    (hpower : KeplerPowerScale n x)
    (hg : KeplerGlobalSurfaceInput x A K)
    (hl : KeplerLocalSurfaceInput A (6 * n - E)) :
    E < 6 * n - kpClean * x := by
  have hD := kp_surface_assembly_strict hpower.x_pos hg hl
  linarith

end

end Erdos1084

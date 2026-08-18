import Mathlib
import Mathlib.Analysis.Real.Pi.Bounds

namespace Erdos1084

/-!
# Audited Kepler / outer-parallel arithmetic bridge

This module certifies the algebraic and scalar-assembly part of the candidate coefficient
`2.0465`.

There are **no project-specific axioms** in this file.  The geometric content is represented by
explicit theorem parameters:

* `KeplerGlobalSurfaceInput` packages the surface lower bound obtained from the Kepler density,
  the outer-parallel truncated-density identity for `λ ≥ 1`, and Euclidean isoperimetry;
* `KeplerLocalSurfaceInput` packages the surface upper bound obtained from the kissing-number
  coverage, spherical-neighborhood isoperimetry, the affine degree charge, and the degree sum.

The positive scale `K` is not arbitrary: `KeplerScaleSpec K` states exactly
`K^3 * π^2 = 18`, so `K = (18 / π^2)^(1/3)` among positive reals.
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

@[simp] theorem kpRadius_pos : 0 < kpRadius := lt_trans (by norm_num) two_lt_kpRadius

/-- The corresponding outer-parallel radius `λ = kpRadius - 1` exceeds one. -/
theorem one_lt_kpOuterRadius : 1 < kpRadius - 1 := by
  linarith [two_lt_kpRadius]

/-- Exact reciprocal-radius identity. -/
theorem kpRadius_reciprocal :
    1 / kpRadius = 10 - 11 * kpS / 2 := by
  have hden : (40 + 22 * kpS : ℝ) ≠ 0 := by positivity
  have h37 : (37 : ℝ) ≠ 0 := by norm_num
  field_simp [kpRadius, hden, h37]
  nlinarith [kpS_sq]

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

/--
Exact cubed certificate for the clean coefficient.

It proves
`kpClean^3 * π^2 < 18 * kpLocalCoeff^3`.
No cube root, floating-point value, or unproved scale comparison occurs in the statement.
-/
theorem kp_clean_cubed_certificate :
    kpClean ^ 3 * Real.pi ^ 2 < 18 * kpLocalCoeff ^ 3 := by
  have hp0 : 0 < Real.pi := Real.pi_pos
  have hp : Real.pi < (3141593 : ℝ) / 1000000 := Real.pi_lt_d6
  have hpSq : Real.pi ^ 2 < ((3141593 : ℝ) / 1000000) ^ 2 := by
    nlinarith
  have hL : (418756933 : ℝ) / 250000000 < kpLocalCoeff :=
    kp_local_compact_lower
  let a : ℝ := (418756933 : ℝ) / 250000000
  have ha0 : 0 < a := by norm_num [a]
  have hb0 : 0 < kpLocalCoeff := kpLocalCoeff_pos
  have hdiff : 0 < kpLocalCoeff - a := sub_pos.mpr hL
  have hsum : 0 < kpLocalCoeff ^ 2 + kpLocalCoeff * a + a ^ 2 := by
    positivity
  have hcubeDiff : 0 < kpLocalCoeff ^ 3 - a ^ 3 := by
    have hprod : 0 < (kpLocalCoeff - a) *
        (kpLocalCoeff ^ 2 + kpLocalCoeff * a + a ^ 2) :=
      mul_pos hdiff hsum
    nlinarith
  have hrat :
      kpClean ^ 3 * ((3141593 : ℝ) / 1000000) ^ 2 < 18 * a ^ 3 := by
    norm_num [kpClean, a]
  calc
    kpClean ^ 3 * Real.pi ^ 2
        < kpClean ^ 3 * ((3141593 : ℝ) / 1000000) ^ 2 := by
          exact mul_lt_mul_of_pos_left hpSq (by positivity)
    _ < 18 * a ^ 3 := hrat
    _ < 18 * kpLocalCoeff ^ 3 := by nlinarith

/--
Algebraic specification of the positive Kepler surface scale.

For a positive real `K`, this equation characterizes
`K = (18 / π^2)^(1/3) = δ_3^(-2/3)`.
-/
def KeplerScaleSpec (K : ℝ) : Prop :=
  0 < K ∧ K ^ 3 * Real.pi ^ 2 = 18

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
  have hcube : kpClean ^ 3 < (K * kpLocalCoeff) ^ 3 :=
    (mul_lt_mul_right hpi2).mp hscaled
  have htarget0 : 0 ≤ K * kpLocalCoeff :=
    mul_nonneg (le_of_lt hKpos) (le_of_lt kpLocalCoeff_pos)
  by_contra hnot
  have hle : K * kpLocalCoeff ≤ kpClean := le_of_not_gt hnot
  have hdiff : 0 ≤ kpClean - K * kpLocalCoeff := sub_nonneg.mpr hle
  have hsum : 0 ≤ kpClean ^ 2 + kpClean * (K * kpLocalCoeff) +
      (K * kpLocalCoeff) ^ 2 := by
    positivity
  have hprod : 0 ≤ (kpClean - K * kpLocalCoeff) *
      (kpClean ^ 2 + kpClean * (K * kpLocalCoeff) +
        (K * kpLocalCoeff) ^ 2) :=
    mul_nonneg hdiff hsum
  have hcubeLe : (K * kpLocalCoeff) ^ 3 ≤ kpClean ^ 3 := by
    nlinarith
  exact (not_lt_of_ge hcubeLe) hcube

/--
The exact global surface lower-bound interface.

The field `surface_lower` is the scalar conclusion that must be supplied by the finite-packing
outer-parallel density theorem together with Euclidean isoperimetry.  It is a theorem parameter,
not an axiom introduced by this development.
-/
structure KeplerGlobalSurfaceInput (x A K : ℝ) : Prop where
  x_pos : 0 < x
  scale : KeplerScaleSpec K
  surface_lower : 4 * Real.pi * K * x ≤ A

/--
The exact local surface upper-bound interface.

For the packing proof this is obtained from degree-twelve kissing coverage, spherical-neighborhood
isoperimetry, the optimized affine charge, boundary subadditivity, and the degree-sum identity.
-/
structure KeplerLocalSurfaceInput (A D : ℝ) : Prop where
  surface_upper : A ≤ 4 * Real.pi * kpRadius ^ 2 * kpQ * D

/--
Strict scalar assembly for the clean coefficient `2.0465`.

Unlike the earlier draft, this theorem does not assume the desired coefficient comparison as an
independent hypothesis.  It derives that comparison from `kp_clean_cubed_certificate` and the
exact Kepler scale equation.
-/
theorem kp_surface_assembly_strict
    {x A D K : ℝ}
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
  have hKx : K * x ≤ kpRadius ^ 2 * kpQ * D := by
    apply (mul_le_mul_left hfourpi).mp
    simpa [mul_assoc] using hchain
  have hmul := mul_le_mul_of_nonneg_right hKx (le_of_lt kpLocalCoeff_pos)
  have hKlocal : K * kpLocalCoeff * x ≤ D := by
    calc
      K * kpLocalCoeff * x = (K * x) * kpLocalCoeff := by ring
      _ ≤ (kpRadius ^ 2 * kpQ * D) * kpLocalCoeff := hmul
      _ = (kpRadius ^ 2 * kpQ * kpLocalCoeff) * D := by ring
      _ = D := by rw [kp_local_identity]; ring
  have hclean : kpClean * x < K * kpLocalCoeff * x := by
    exact mul_lt_mul_of_pos_right hcoeff hg.x_pos
  exact lt_of_lt_of_le hclean hKlocal

/-- Contact-number form of the audited strict assembly. -/
theorem kp_contact_upper_from_surface
    {n E x A K : ℝ}
    (hg : KeplerGlobalSurfaceInput x A K)
    (hl : KeplerLocalSurfaceInput A (6 * n - E)) :
    E < 6 * n - kpClean * x := by
  have hD := kp_surface_assembly_strict hg hl
  linarith

end

end Erdos1084

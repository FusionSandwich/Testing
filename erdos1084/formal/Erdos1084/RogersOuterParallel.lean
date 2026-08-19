import Mathlib
import Erdos1084.KeplerOuterParallel

namespace Erdos1084

/-!
# Corrected Rogers finite outer-parallel arithmetic

This module certifies the rational coefficient and the abstract local-to-global
assembly for the repaired universal coefficient `1.9773`.

The finite Rogers truncated-Voronoi density theorem, Euclidean isoperimetry,
kissing number twelve, and spherical-neighborhood isoperimetry remain explicit
geometric inputs. They are not introduced as project axioms.
-/

noncomputable section

/-- Certified rational upper bound for Rogers' three-dimensional simplex density. -/
def rogersSigmaUpper : ℝ := 5457713997657 / 7000000000000

/-- Rational surface scale below `rogersSigmaUpper^(-2/3)`. -/
def rogersSurfaceScale : ℝ := 59023 / 50000

/-- Clean corrected universal coefficient `1.9773`. -/
def rogersClean : ℝ := 19773 / 10000

@[simp] theorem rogersSigmaUpper_pos : 0 < rogersSigmaUpper := by
  norm_num [rogersSigmaUpper]

@[simp] theorem rogersSurfaceScale_pos : 0 < rogersSurfaceScale := by
  norm_num [rogersSurfaceScale]

@[simp] theorem rogersClean_pos : 0 < rogersClean := by
  norm_num [rogersClean]

/-- Exact rational certificate that the chosen surface scale is conservative. -/
theorem rogers_surface_scale_cubed_certificate :
    rogersSurfaceScale ^ 3 * rogersSigmaUpper ^ 2 < 1 := by
  norm_num [rogersSurfaceScale, rogersSigmaUpper]

/-- Exact rational comparison with the lower bound for the optimized local factor. -/
theorem rogers_clean_lt_scale_mul_local_lower :
    rogersClean <
      rogersSurfaceScale * ((418756933 : ℝ) / 250000000) := by
  norm_num [rogersClean, rogersSurfaceScale]

/-- The clean coefficient is below the Rogers surface scale times the exact local factor. -/
theorem rogers_clean_lt_scale_mul_local :
    rogersClean < rogersSurfaceScale * kpLocalCoeff := by
  have hmul := mul_lt_mul_of_pos_left
    kp_local_compact_lower rogersSurfaceScale_pos
  exact lt_trans rogers_clean_lt_scale_mul_local_lower hmul

/--
Global finite surface lower-bound interface.

In the geometric proof this is obtained from Rogers' finite simplex-density bound
and Euclidean isoperimetry. Keeping it as an ordinary theorem parameter makes the
formal boundary visible in the theorem signature.
-/
structure RogersGlobalSurfaceInput (x A : ℝ) : Prop where
  surface_lower : 4 * Real.pi * rogersSurfaceScale * x ≤ A

/-- Strict scalar assembly for the corrected universal coefficient `1.9773`. -/
theorem rogers_surface_assembly_strict
    {x A D : ℝ}
    (hx : 0 < x)
    (hg : RogersGlobalSurfaceInput x A)
    (hl : KeplerLocalSurfaceInput A D) :
    rogersClean * x < D := by
  have hcoeff : rogersClean < rogersSurfaceScale * kpLocalCoeff :=
    rogers_clean_lt_scale_mul_local
  have hchain :
      4 * Real.pi * rogersSurfaceScale * x ≤
        4 * Real.pi * kpRadius ^ 2 * kpQ * D :=
    le_trans hg.surface_lower hl.surface_upper
  have hfourpi : 0 < 4 * Real.pi := by positivity
  have hchain' :
      (4 * Real.pi) * (rogersSurfaceScale * x) ≤
        (4 * Real.pi) * (kpRadius ^ 2 * kpQ * D) := by
    simpa [mul_assoc] using hchain
  have hscaleX :
      rogersSurfaceScale * x ≤ kpRadius ^ 2 * kpQ * D := by
    by_contra hnot
    have hrev :
        kpRadius ^ 2 * kpQ * D < rogersSurfaceScale * x :=
      lt_of_not_ge hnot
    have hmul := mul_lt_mul_of_pos_left hrev hfourpi
    exact (not_lt_of_ge hchain') hmul
  have hmul := mul_le_mul_of_nonneg_right hscaleX
    (le_of_lt kpLocalCoeff_pos)
  have htarget : rogersSurfaceScale * kpLocalCoeff * x ≤ D := by
    calc
      rogersSurfaceScale * kpLocalCoeff * x =
          (rogersSurfaceScale * x) * kpLocalCoeff := by ring
      _ ≤ (kpRadius ^ 2 * kpQ * D) * kpLocalCoeff := hmul
      _ = (kpRadius ^ 2 * kpQ * kpLocalCoeff) * D := by ring
      _ = D := by rw [kp_local_identity]; ring
  have hclean :
      rogersClean * x < rogersSurfaceScale * kpLocalCoeff * x :=
    mul_lt_mul_of_pos_right hcoeff hx
  exact lt_of_lt_of_le hclean htarget

/-- Contact-number form with `x` tied explicitly to `n^(2/3)`. -/
theorem rogers_contact_upper_from_surface
    {n E x A : ℝ}
    (hpower : KeplerPowerScale n x)
    (hg : RogersGlobalSurfaceInput x A)
    (hl : KeplerLocalSurfaceInput A (6 * n - E)) :
    E < 6 * n - rogersClean * x := by
  have hD := rogers_surface_assembly_strict hpower.x_pos hg hl
  linarith

end

end Erdos1084

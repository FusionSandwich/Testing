import Mathlib
import Erdos1084.KeplerOuterParallel

namespace Erdos1084

/-!
# Publication-core dodecahedral finite coefficient

This module checks the exact rational coefficient and abstract local-to-global
assembly for the clean universal coefficient `2.0207`.

The geometric proof obtains the global surface input from the finite
regular-dodecahedron Voronoi truncation of Bezdek--Reid and Euclidean
isoperimetry. Those published geometric inputs remain ordinary theorem parameters;
they are not introduced as project axioms.
-/

noncomputable section

/-- Published strict upper bound for the regular-dodecahedron packing ratio. -/
def dodecahedralDensityUpper : ℝ := 7547 / 10000

/-- Rational surface scale strictly below `dodecahedralDensityUpper^(-2/3)`. -/
def dodecahedralSurfaceScale : ℝ := 120637 / 100000

/-- Clean publication coefficient `2.0207`. -/
def dodecahedralClean : ℝ := 20207 / 10000

@[simp] theorem dodecahedralDensityUpper_pos :
    0 < dodecahedralDensityUpper := by
  norm_num [dodecahedralDensityUpper]

@[simp] theorem dodecahedralSurfaceScale_pos :
    0 < dodecahedralSurfaceScale := by
  norm_num [dodecahedralSurfaceScale]

@[simp] theorem dodecahedralClean_pos : 0 < dodecahedralClean := by
  norm_num [dodecahedralClean]

/-- Exact rational certificate for the conservative surface scale. -/
theorem dodecahedral_surface_scale_cubed_certificate :
    dodecahedralSurfaceScale ^ 3 * dodecahedralDensityUpper ^ 2 < 1 := by
  norm_num [dodecahedralSurfaceScale, dodecahedralDensityUpper]

/-- Exact rational comparison with the certified lower bound for the local factor. -/
theorem dodecahedral_clean_lt_scale_mul_local_lower :
    dodecahedralClean <
      dodecahedralSurfaceScale * ((418756933 : ℝ) / 250000000) := by
  norm_num [dodecahedralClean, dodecahedralSurfaceScale]

/-- The clean publication coefficient is below the surface scale times the exact local factor. -/
theorem dodecahedral_clean_lt_scale_mul_local :
    dodecahedralClean < dodecahedralSurfaceScale * kpLocalCoeff := by
  have hmul := mul_lt_mul_of_pos_left
    kp_local_compact_lower dodecahedralSurfaceScale_pos
  exact lt_trans dodecahedral_clean_lt_scale_mul_local_lower hmul

/--
Global finite surface lower-bound interface.

The mathematical manuscript derives this from the finite dodecahedral Voronoi
truncation and Euclidean isoperimetry. The ordinary hypothesis keeps the external
geometric content visible in the theorem signature.
-/
structure DodecahedralGlobalSurfaceInput (x A : ℝ) : Prop where
  surface_lower : 4 * Real.pi * dodecahedralSurfaceScale * x ≤ A

/-- Strict scalar assembly for the clean coefficient `2.0207`. -/
theorem dodecahedral_surface_assembly_strict
    {x A D : ℝ}
    (hx : 0 < x)
    (hg : DodecahedralGlobalSurfaceInput x A)
    (hl : KeplerLocalSurfaceInput A D) :
    dodecahedralClean * x < D := by
  have hcoeff :
      dodecahedralClean < dodecahedralSurfaceScale * kpLocalCoeff :=
    dodecahedral_clean_lt_scale_mul_local
  have hchain :
      4 * Real.pi * dodecahedralSurfaceScale * x ≤
        4 * Real.pi * kpRadius ^ 2 * kpQ * D :=
    le_trans hg.surface_lower hl.surface_upper
  have hfourpi : 0 < 4 * Real.pi := by positivity
  have hchain' :
      (4 * Real.pi) * (dodecahedralSurfaceScale * x) ≤
        (4 * Real.pi) * (kpRadius ^ 2 * kpQ * D) := by
    simpa [mul_assoc] using hchain
  have hscaleX :
      dodecahedralSurfaceScale * x ≤ kpRadius ^ 2 * kpQ * D := by
    by_contra hnot
    have hrev :
        kpRadius ^ 2 * kpQ * D < dodecahedralSurfaceScale * x :=
      lt_of_not_ge hnot
    have hmul := mul_lt_mul_of_pos_left hrev hfourpi
    exact (not_lt_of_ge hchain') hmul
  have hmul := mul_le_mul_of_nonneg_right hscaleX
    (le_of_lt kpLocalCoeff_pos)
  have htarget : dodecahedralSurfaceScale * kpLocalCoeff * x ≤ D := by
    calc
      dodecahedralSurfaceScale * kpLocalCoeff * x =
          (dodecahedralSurfaceScale * x) * kpLocalCoeff := by ring
      _ ≤ (kpRadius ^ 2 * kpQ * D) * kpLocalCoeff := hmul
      _ = (kpRadius ^ 2 * kpQ * kpLocalCoeff) * D := by ring
      _ = D := by rw [kp_local_identity]; ring
  have hclean :
      dodecahedralClean * x <
        dodecahedralSurfaceScale * kpLocalCoeff * x :=
    mul_lt_mul_of_pos_right hcoeff hx
  exact lt_of_lt_of_le hclean htarget

/-- Contact-number form with `x` explicitly tied to `n^(2/3)`. -/
theorem dodecahedral_contact_upper_from_surface
    {n E x A : ℝ}
    (hpower : KeplerPowerScale n x)
    (hg : DodecahedralGlobalSurfaceInput x A)
    (hl : KeplerLocalSurfaceInput A (6 * n - E)) :
    E < 6 * n - dodecahedralClean * x := by
  have hD := dodecahedral_surface_assembly_strict hpower.x_pos hg hl
  linarith

end

end Erdos1084

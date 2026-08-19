import Mathlib
import Erdos1084.KeplerOuterParallel

namespace Erdos1084

/-!
# Cubic global-surface algebra for Phase I

The finite outer-parallel density theorem and Euclidean isoperimetry naturally provide a cubed
surface lower bound. This module performs the exact conversion to the linear surface input used by
the contact-deficit assembly.
-/

noncomputable section

/-- Cubic form of the global Phase-I surface information. -/
structure Phase1GlobalCubicInput (n x A K : ℝ) : Prop where
  power : KeplerPowerScale n x
  scale : KeplerScaleSpec K
  surface_nonneg : 0 ≤ A
  surface_cube_lower : 1152 * Real.pi * n ^ 2 ≤ A ^ 3

/-- Exact cube of the Kepler target surface coefficient. -/
theorem phase1_kepler_surface_cube
    {n x K : ℝ} (hp : KeplerPowerScale n x) (hK : KeplerScaleSpec K) :
    (4 * Real.pi * K * x) ^ 3 = 1152 * Real.pi * n ^ 2 := by
  calc
    (4 * Real.pi * K * x) ^ 3 =
        64 * Real.pi * (K ^ 3 * Real.pi ^ 2) * x ^ 3 := by ring
    _ = 64 * Real.pi * 18 * n ^ 2 := by rw [hK.2, hp.x_cubed]
    _ = 1152 * Real.pi * n ^ 2 := by ring

/-- A nonnegative cubic lower bound implies the required linear surface lower bound. -/
theorem phase1_global_surface_input_of_cubic
    {n x A K : ℝ} (h : Phase1GlobalCubicInput n x A K) :
    KeplerGlobalSurfaceInput x A K := by
  have htargetPos : 0 < 4 * Real.pi * K * x := by
    exact mul_pos (mul_pos (mul_pos (by norm_num) Real.pi_pos) h.scale.1) h.power.x_pos
  have hcube : (4 * Real.pi * K * x) ^ 3 ≤ A ^ 3 := by
    rw [phase1_kepler_surface_cube h.power h.scale]
    exact h.surface_cube_lower
  have hlinear : 4 * Real.pi * K * x ≤ A := by
    by_contra hnot
    have hAlt : A < 4 * Real.pi * K * x := lt_of_not_ge hnot
    let L : ℝ := 4 * Real.pi * K * x
    have hLpos : 0 < L := by simpa [L] using htargetPos
    have hsum : 0 < L ^ 2 + L * A + A ^ 2 := by
      have hLsq : 0 < L ^ 2 := sq_pos_of_pos hLpos
      have hLA : 0 ≤ L * A := mul_nonneg (le_of_lt hLpos) h.surface_nonneg
      have hAsq : 0 ≤ A ^ 2 := sq_nonneg A
      nlinarith
    have hprod : 0 < (L - A) * (L ^ 2 + L * A + A ^ 2) :=
      mul_pos (sub_pos.mpr (by simpa [L] using hAlt)) hsum
    have hcubestrict : A ^ 3 < L ^ 3 := by
      nlinarith
    have : L ^ 3 ≤ A ^ 3 := by simpa [L] using hcube
    exact (not_lt_of_ge this) hcubestrict
  exact ⟨h.scale, hlinear⟩

end

end Erdos1084

import Mathlib
import Erdos1084.Phase1GlobalAlgebra

namespace Erdos1084

/-!
# Finite density plus Euclidean isoperimetry bridge

This module converts the two geometric conclusions used globally in Phase I into the cubic
surface input. The exact finite-density conclusion is `4 * sqrt 2 * n ≤ V`; the Euclidean
isoperimetric conclusion is `36*pi*V² ≤ A³`.
-/

noncomputable section

/-- Direct scalar output of finite outer-parallel density and Euclidean isoperimetry. -/
structure Phase1FiniteDensityIsoperimetricInput (n x V A K : ℝ) : Prop where
  power : KeplerPowerScale n x
  scale : KeplerScaleSpec K
  n_nonneg : 0 ≤ n
  volume_nonneg : 0 ≤ V
  surface_nonneg : 0 ≤ A
  finite_density : 4 * Real.sqrt 2 * n ≤ V
  isoperimetric_cube : 36 * Real.pi * V ^ 2 ≤ A ^ 3

/-- Exact square of the finite Kepler volume coefficient. -/
theorem phase1_four_sqrt_two_square (n : ℝ) :
    (4 * Real.sqrt 2 * n) ^ 2 = 32 * n ^ 2 := by
  have hsqrt : (Real.sqrt 2) ^ 2 = (2 : ℝ) :=
    Real.sq_sqrt (by norm_num)
  calc
    (4 * Real.sqrt 2 * n) ^ 2 =
        16 * (Real.sqrt 2) ^ 2 * n ^ 2 := by ring
    _ = 32 * n ^ 2 := by rw [hsqrt]; ring

/-- The finite density and isoperimetric inequalities imply the cubic global input. -/
theorem phase1_global_cubic_of_density_isoperimetry
    {n x V A K : ℝ}
    (h : Phase1FiniteDensityIsoperimetricInput n x V A K) :
    Phase1GlobalCubicInput n x A K := by
  have hbase0 : 0 ≤ 4 * Real.sqrt 2 * n := by positivity
  have hprod :
      0 ≤ (V - 4 * Real.sqrt 2 * n) *
        (V + 4 * Real.sqrt 2 * n) :=
    mul_nonneg (sub_nonneg.mpr h.finite_density)
      (add_nonneg h.volume_nonneg hbase0)
  have hsq : (4 * Real.sqrt 2 * n) ^ 2 ≤ V ^ 2 := by
    nlinarith
  have hsq' : 32 * n ^ 2 ≤ V ^ 2 := by
    rw [← phase1_four_sqrt_two_square n]
    exact hsq
  have hscaled :
      36 * Real.pi * (32 * n ^ 2) ≤ 36 * Real.pi * V ^ 2 :=
    mul_le_mul_of_nonneg_left hsq' (by positivity)
  refine ⟨h.power, h.scale, h.surface_nonneg, ?_⟩
  calc
    1152 * Real.pi * n ^ 2 = 36 * Real.pi * (32 * n ^ 2) := by ring
    _ ≤ 36 * Real.pi * V ^ 2 := hscaled
    _ ≤ A ^ 3 := h.isoperimetric_cube

/-- Direct conversion to the linear global surface interface. -/
theorem phase1_global_surface_of_density_isoperimetry
    {n x V A K : ℝ}
    (h : Phase1FiniteDensityIsoperimetricInput n x V A K) :
    KeplerGlobalSurfaceInput x A K :=
  phase1_global_surface_input_of_cubic
    (phase1_global_cubic_of_density_isoperimetry h)

end

end Erdos1084

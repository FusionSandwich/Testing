import Mathlib
import Erdos1084.FiniteSpherePacking
import Erdos1084.KeplerOptimizedChord

namespace Erdos1084

/-!
# Integer-degree bridge from spherical cap geometry to the optimized affine charge

The external spherical-neighborhood and kissing-number geometry is exposed through elementary
per-vertex hypotheses.  This file proves all remaining degree case splits and converts the
continuous optimized chord theorem into the exact local charge used by the global assembly.
-/

noncomputable section

namespace UnitSeparatedConfiguration

variable {n : ℕ} (X : UnitSeparatedConfiguration (Fin n))

/--
Concrete local spherical data at every packing center.

For degrees below twelve, `capBound` is the direct geometric estimate obtained by applying the
spherical-neighborhood theorem to the union of tangent-neighbor base caps.  At degree twelve,
`coveredAtTwelve` is the complete-coverage conclusion from kissing number twelve.  The minimum-
degree field is supplied for a contact maximizer (or any configuration without isolated points).
-/
structure Phase1LocalCapCertificate where
  exposure : Fin n → ℝ
  minimumDegree : ∀ i, 1 ≤ X.contactDegree i
  maximumDegree : ∀ i, X.contactDegree i ≤ 12
  capBound : ∀ i, X.contactDegree i ≤ 11 →
    exposure i ≤
      (2 * Real.pi * kpRadius ^ 2) *
        kpOptimizedH (rtX (X.contactDegree i : ℝ))
  coveredAtTwelve : ∀ i, X.contactDegree i = 12 → exposure i ≤ 0

/-- The optimized local affine charge for every actual integer contact degree. -/
theorem phase1_local_degree_charge
    (h : X.Phase1LocalCapCertificate) (i : Fin n) :
    h.exposure i ≤
      2 * Real.pi * kpRadius ^ 2 * kpQ *
        (12 - (X.contactDegree i : ℝ)) := by
  have hmax := h.maximumDegree i
  by_cases h12 : X.contactDegree i = 12
  · have hzero := h.coveredAtTwelve i h12
    norm_num [h12] at hzero ⊢
    exact hzero
  · have h11 : X.contactDegree i ≤ 11 := by omega
    have hmin : 1 ≤ (X.contactDegree i : ℝ) := by
      exact_mod_cast h.minimumDegree i
    have hmaxReal : (X.contactDegree i : ℝ) ≤ 11 := by
      exact_mod_cast h11
    have hgeom := h.capBound i h11
    have hchord := kp_optimized_degree_charge hmin hmaxReal
    have hfactor : 0 ≤ 2 * Real.pi * kpRadius ^ 2 := by positivity
    have hmul := mul_le_mul_of_nonneg_left hchord hfactor
    calc
      h.exposure i ≤
          (2 * Real.pi * kpRadius ^ 2) *
            kpOptimizedH (rtX (X.contactDegree i : ℝ)) := hgeom
      _ ≤ (2 * Real.pi * kpRadius ^ 2) *
            (kpQ * (12 - (X.contactDegree i : ℝ))) := hmul
      _ = 2 * Real.pi * kpRadius ^ 2 * kpQ *
            (12 - (X.contactDegree i : ℝ)) := by ring

/-- Convert a local cap certificate into the exact function required by the surface assembly. -/
theorem phase1_all_local_degree_charges
    (h : X.Phase1LocalCapCertificate) :
    ∀ i, h.exposure i ≤
      2 * Real.pi * kpRadius ^ 2 * kpQ *
        (12 - (X.contactDegree i : ℝ)) :=
  X.phase1_local_degree_charge h

end UnitSeparatedConfiguration

end

end Erdos1084

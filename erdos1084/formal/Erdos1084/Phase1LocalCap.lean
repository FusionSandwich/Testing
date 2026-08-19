import Mathlib
import Erdos1084.FiniteSpherePacking
import Erdos1084.KeplerOptimizedChord

namespace Erdos1084

/-!
# Integer contact-degree bridge to the optimized local charge

The spherical-neighborhood theorem and kissing number appear as explicit per-center hypotheses.
The degree case split and optimized affine charge are proved in Lean.
-/

noncomputable section

namespace UnitSeparatedConfiguration

variable {n : ℕ} (X : UnitSeparatedConfiguration (Fin n))

/-- Local geometric conclusions at all packing centers. -/
structure Phase1LocalCapCertificate where
  exposure : Fin n → ℝ
  minimumDegree : ∀ i, 1 ≤ X.contactDegree i
  maximumDegree : ∀ i, X.contactDegree i ≤ 12
  capBound : ∀ i, X.contactDegree i ≤ 11 →
    exposure i ≤
      (2 * Real.pi * kpRadius ^ 2) *
        kpOptimizedH (rtX (X.contactDegree i : ℝ))
  coveredAtTwelve : ∀ i, X.contactDegree i = 12 → exposure i ≤ 0

/-- The exact affine charge for every actual integer contact degree. -/
theorem phase1_local_degree_charge
    (h : X.Phase1LocalCapCertificate) (i : Fin n) :
    h.exposure i ≤
      2 * Real.pi * kpRadius ^ 2 * kpQ *
        (12 - (X.contactDegree i : ℝ)) := by
  by_cases h12 : X.contactDegree i = 12
  · simpa [h12] using h.coveredAtTwelve i h12
  · have h11 : X.contactDegree i ≤ 11 := by
      have hmax := h.maximumDegree i
      omega
    have hminReal : (1 : ℝ) ≤ (X.contactDegree i : ℝ) := by
      exact_mod_cast h.minimumDegree i
    have hmaxReal : (X.contactDegree i : ℝ) ≤ (11 : ℝ) := by
      exact_mod_cast h11
    have hgeom := h.capBound i h11
    have hchord :
        kpOptimizedH (rtX (X.contactDegree i : ℝ)) ≤
          kpQ * (12 - (X.contactDegree i : ℝ)) :=
      kp_optimized_degree_charge
        (d := (X.contactDegree i : ℝ)) hminReal hmaxReal
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

end UnitSeparatedConfiguration

end

end Erdos1084

import Mathlib
import Erdos1084.KissingCoverage
import Erdos1084.KeplerOuterParallel

namespace Erdos1084

/-!
# Degree-twelve tangent exposure vanishes

Using only the kissing-number covering consequence and `r_*>2`, this file proves that a
degree-twelve contact environment has no unit direction left uncovered by the tangent-neighbor
hidden caps at the optimized radius.
-/

noncomputable section

/-- Unit directions not hidden by any tangent contact neighbor at the optimized radius. -/
def phase1TangentExposedDirections {n : ℕ}
    (X : UnitSeparatedConfiguration (Fin n)) (i : Fin n) : Set Point3 :=
  {u | ‖u‖ = 1 ∧
    ∀ j : ContactNeighbor X i,
      ⟪u, contactNeighborDirection X i j⟫_ℝ < 1 / kpRadius}

/-- The optimized cap threshold is strictly below the kissing-cover threshold `1/2`. -/
theorem kpRadius_reciprocal_lt_half :
    1 / kpRadius < (1 / 2 : ℝ) := by
  apply (div_lt_iff₀ kpRadius_pos).2
  nlinarith [two_lt_kpRadius]

/-- Degree twelve leaves no tangent-exposed unit direction. -/
theorem phase1TangentExposedDirections_eq_empty_of_degree_twelve
    (hk : KissingNumberThreeAtMostTwelve)
    {n : ℕ} (X : UnitSeparatedConfiguration (Fin n)) (i : Fin n)
    (hdegree : X.contactDegree i = 12) :
    phase1TangentExposedDirections X i = ∅ := by
  ext u
  constructor
  · intro hu
    rcases hu with ⟨huNorm, huExposed⟩
    obtain ⟨j, hj⟩ :=
      degree_twelve_contact_directions_cover hk X i hdegree u huNorm
    have hstrict := huExposed j
    exact (not_lt_of_ge hj)
      (lt_trans hstrict kpRadius_reciprocal_lt_half)
  · simp

end

end Erdos1084

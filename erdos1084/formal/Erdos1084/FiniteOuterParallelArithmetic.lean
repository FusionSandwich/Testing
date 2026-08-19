import Mathlib

namespace Erdos1084

/-!
# Finite Kepler outer-parallel arithmetic

This file formalizes the exact normalization used after applying the finite truncated-density
corollary. The geometric source theorem supplies

`n * vol(B³) / vol(U) ≤ π / sqrt(18)`.

The theorems below prove inside Lean that this is exactly the volume lower bound

`4 * sqrt(2) * n ≤ vol(U)`.
-/

noncomputable section

/-- Volume of the Euclidean unit ball in dimension three. -/
def phase1UnitBallVolume : ℝ := 4 * Real.pi / 3

/-- The Kepler density in dimension three. -/
def phase1KeplerDensity : ℝ := Real.pi / Real.sqrt 18

/-- Exact square-root normalization used in the Kepler density. -/
theorem phase1_sqrt_eighteen :
    Real.sqrt 18 = 3 * Real.sqrt 2 := by
  have h18 : (Real.sqrt 18) ^ 2 = 18 := by
    norm_num
  have h2 : (Real.sqrt 2) ^ 2 = 2 := by
    norm_num
  have hs18 : 0 ≤ Real.sqrt 18 := Real.sqrt_nonneg _
  have hs2 : 0 ≤ Real.sqrt 2 := Real.sqrt_nonneg _
  nlinarith

/-- The Kepler density is strictly positive. -/
theorem phase1KeplerDensity_pos : 0 < phase1KeplerDensity := by
  exact div_pos Real.pi_pos (Real.sqrt_pos.2 (by norm_num))

/-- Exact reciprocal-density volume factor. -/
theorem phase1_ballVolume_div_keplerDensity :
    phase1UnitBallVolume / phase1KeplerDensity = 4 * Real.sqrt 2 := by
  have hpi : Real.pi ≠ 0 := ne_of_gt Real.pi_pos
  have hs2 : Real.sqrt 2 ≠ 0 := ne_of_gt (Real.sqrt_pos.2 (by norm_num))
  rw [phase1UnitBallVolume, phase1KeplerDensity, phase1_sqrt_eighteen]
  field_simp [hpi, hs2]

/--
The finite truncated-density inequality implies the exact finite outer-parallel volume bound.
-/
theorem phase1_finite_volume_lower_of_density
    {n volumeU : ℝ}
    (hvolume : 0 < volumeU)
    (hdensity :
      n * phase1UnitBallVolume / volumeU ≤ phase1KeplerDensity) :
    4 * Real.sqrt 2 * n ≤ volumeU := by
  have hdelta : 0 < phase1KeplerDensity := phase1KeplerDensity_pos
  have hmul :
      n * phase1UnitBallVolume ≤ volumeU * phase1KeplerDensity := by
    have h := (div_le_iff₀ hvolume).mp hdensity
    nlinarith
  have hdiv :
      n * phase1UnitBallVolume / phase1KeplerDensity ≤ volumeU := by
    apply (div_le_iff₀ hdelta).2
    simpa [mul_comm, mul_left_comm, mul_assoc] using hmul
  calc
    4 * Real.sqrt 2 * n =
        n * (phase1UnitBallVolume / phase1KeplerDensity) := by
      rw [phase1_ballVolume_div_keplerDensity]
      ring
    _ = n * phase1UnitBallVolume / phase1KeplerDensity := by
      ring
    _ ≤ volumeU := hdiv

end

end Erdos1084

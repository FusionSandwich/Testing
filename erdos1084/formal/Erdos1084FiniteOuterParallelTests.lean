import Erdos1084.FiniteOuterParallelArithmetic

open Erdos1084

/-! Smoke tests for finite Kepler outer-parallel arithmetic. -/

example : Real.sqrt 18 = 3 * Real.sqrt 2 :=
  phase1_sqrt_eighteen

example : 0 < phase1KeplerDensity :=
  phase1KeplerDensity_pos

example :
    phase1UnitBallVolume / phase1KeplerDensity = 4 * Real.sqrt 2 :=
  phase1_ballVolume_div_keplerDensity

example {n volumeU : ℝ}
    (hvolume : 0 < volumeU)
    (hdensity :
      n * phase1UnitBallVolume / volumeU ≤ phase1KeplerDensity) :
    4 * Real.sqrt 2 * n ≤ volumeU :=
  phase1_finite_volume_lower_of_density hvolume hdensity

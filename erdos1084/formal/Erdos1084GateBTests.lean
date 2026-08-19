import Erdos1084

open Erdos1084

/-! Smoke tests for Gate B invariant-measure arithmetic and relaxation audit. -/

example (p : ℝ) :
    invariantBarlowCoefficientCube p =
      (27 / 2 : ℝ) * invariantBarlowWulffVolume p :=
  invariantBarlow_cube_from_volume p

example {p : ℝ} (hp0 : 0 ≤ p) (hp1 : p ≤ 1) :
    (432 : ℝ) ≤ invariantBarlowCoefficientCube p :=
  invariantBarlow_cube_ge_fcc hp0 hp1

example {p : ℝ} (hp0 : 0 < p) (hp1 : p < 1) :
    (432 : ℝ) < invariantBarlowCoefficientCube p :=
  invariantBarlow_cube_gt_fcc hp0 hp1

example {p : ℝ} (hp0 : 0 ≤ p) (hp1 : p ≤ 1) :
    invariantBarlowCoefficientCube p = 432 ↔ p = 0 ∨ p = 1 :=
  invariantBarlow_cube_eq_fcc_iff hp0 hp1

example : Continuous invariantBarlowCoefficientCube :=
  invariantBarlowCoefficientCube_continuous

example :
    gateBRawSupport 3 1 1 = 9 / 2 ∧
    gateBRawSupport 3 (-1) 1 = 9 / 2 ∧
    gateBRawSupport 6 0 2 = 10 :=
  gateB_raw_non_subadditivity_values

example :
    gateBRawSupport 6 0 2 >
      gateBRawSupport 3 1 1 + gateBRawSupport 3 (-1) 1 :=
  gateB_raw_non_subadditive

example :
    gateBConvexEnvelopeSupport 2 (1 / 4) = 3 ∧
    gateBRawSupport 2 0 (1 / 4) = 25 / 8 :=
  gateB_convex_envelope_strict_test

example :
    gateBCommonPhysicalVolume = 2 * gateBCommonScaledVolume ∧
    gateBCommonCoefficientCube =
      (27 / 2 : ℚ) * gateBCommonPhysicalVolume ∧
    gateBCommonCoefficientCube < 432 :=
  gateB_common_body_arithmetic

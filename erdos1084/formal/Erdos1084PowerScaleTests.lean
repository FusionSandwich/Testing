import Erdos1084.PowerScaleUniqueness

open Erdos1084

/-! Smoke test for uniqueness of the positive `n^(2/3)` scale. -/

example {n x y : ℝ}
    (hx : KeplerPowerScale n x)
    (hy : KeplerPowerScale n y) :
    x = y :=
  hx.unique hy

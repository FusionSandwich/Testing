import Erdos1084

open Erdos1084

/-!
# Fully concrete one-radius calculus smoke tests
-/

example {r : ℝ} (hr : 1 < r) :
    HasDerivAt kpEndpointElevenProfile (kpEndpointElevenDerivative r) r :=
  kpEndpointElevenProfile_hasDerivAt hr

example :
    StrictAntiOn kpEndpointElevenProfile (Set.Icc (2 : ℝ) kpRadius) :=
  kpEndpointElevenProfile_strictAntiOn

example {r : ℝ} (hr : 2 ≤ r) (hne : r ≠ kpRadius) :
    max (kpEndpointOneProfile r) (kpEndpointElevenProfile r) >
      kpEndpointOneProfile kpRadius :=
  kpRadius_unique_oneRadius_optimum_fullyConcrete hr hne

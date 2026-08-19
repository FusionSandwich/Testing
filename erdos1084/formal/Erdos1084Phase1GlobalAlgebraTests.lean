import Erdos1084.Phase1GlobalAlgebra

open Erdos1084

example {n x K : ℝ}
    (hp : KeplerPowerScale n x) (hK : KeplerScaleSpec K) :
    (4 * Real.pi * K * x) ^ 3 = 1152 * Real.pi * n ^ 2 :=
  phase1_kepler_surface_cube hp hK

example {n x A K : ℝ}
    (h : Phase1GlobalCubicInput n x A K) :
    KeplerGlobalSurfaceInput x A K :=
  phase1_global_surface_input_of_cubic h

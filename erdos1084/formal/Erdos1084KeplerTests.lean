import Erdos1084

open Erdos1084

/-! Smoke tests for the audited Kepler / outer-parallel bridge and optimized local chord. -/

example : kpS ^ 2 = 3 := kpS_sq

example : 2 < kpRadius := two_lt_kpRadius

example : 1 < kpRadius - 1 := one_lt_kpOuterRadius

example : 1 / kpRadius = 10 - 11 * kpS / 2 :=
  kpRadius_reciprocal

example : kpRadius ^ 2 * kpQ * kpLocalCoeff = 1 :=
  kp_local_identity

example : (418756933 : ℝ) / 250000000 < kpLocalCoeff :=
  kp_local_compact_lower

example : kpClean ^ 3 * Real.pi ^ 2 < 18 * kpLocalCoeff ^ 3 :=
  kp_clean_cubed_certificate

example {n x : ℝ} (h : KeplerPowerScale n x) : 0 < x :=
  h.x_pos

example {K : ℝ} (hK : KeplerScaleSpec K) :
    kpClean < K * kpLocalCoeff :=
  kp_clean_lt_scale_mul_local hK

/-! Optimized convex-chord envelope. -/

example : 0 < kpSinShift := kpSinShift_pos

example : kpOptimizedH rtLower = kpQ :=
  kpOptimizedH_lower

example : kpOptimizedH rtUpper = 11 * kpQ :=
  kpOptimizedH_upper

example {x : ℝ} (hxL : rtLower ≤ x) (hxU : x ≤ rtUpper) :
    kpOptimizedH x ≤ kpOptimizedChord x :=
  kpOptimizedH_le_chord hxL hxU

example {d : ℝ} (hd1 : 1 ≤ d) (hd11 : d ≤ 11) :
    kpOptimizedH (rtX d) ≤ kpQ * (12 - d) :=
  kp_optimized_degree_charge hd1 hd11

/-! Finite-sum and final scalar assembly. -/

example
    {ι : Type*} [Fintype ι]
    (d exposure : ι → ℝ)
    (n E A : ℝ)
    (hn : (Fintype.card ι : ℝ) = n)
    (hdeg : (∑ i, d i) = 2 * E)
    (hBoundary : A ≤ ∑ i, exposure i)
    (hLocal : ∀ i,
      exposure i ≤ 2 * Real.pi * kpRadius ^ 2 * kpQ * (12 - d i)) :
    KeplerLocalSurfaceInput A (6 * n - E) :=
  kp_local_surface_input_of_charges
    d exposure n E A hn hdeg hBoundary hLocal

example {x A D K : ℝ}
    (hx : 0 < x)
    (hg : KeplerGlobalSurfaceInput x A K)
    (hl : KeplerLocalSurfaceInput A D) :
    kpClean * x < D :=
  kp_surface_assembly_strict hx hg hl

example {n E x A K : ℝ}
    (hpower : KeplerPowerScale n x)
    (hg : KeplerGlobalSurfaceInput x A K)
    (hl : KeplerLocalSurfaceInput A (6 * n - E)) :
    E < 6 * n - kpClean * x :=
  kp_contact_upper_from_surface hpower hg hl

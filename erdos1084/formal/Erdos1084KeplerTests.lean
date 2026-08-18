import Erdos1084

open Erdos1084

/-! Smoke tests for the audited Kepler, stability, degree, and limit modules. -/

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

/-! One-radius endpoint minimax core. -/

example :
    StrictMonoOn kpEndpointOneProfile (Set.Ici (0 : ℝ)) :=
  kpEndpointOneProfile_strictMonoOn

example :
    kpEndpointOneProfile kpRadius = kpRadius ^ 2 * kpQ :=
  kpEndpointOneProfile_at_optimizer

example
    (degreeElevenProfile : ℝ → ℝ)
    (hdecrease :
      StrictAntiOn degreeElevenProfile (Set.Icc (2 : ℝ) kpRadius))
    (hcross :
      degreeElevenProfile kpRadius = kpEndpointOneProfile kpRadius)
    {r : ℝ} (hr : 2 ≤ r) (hne : r ≠ kpRadius) :
    max (kpEndpointOneProfile r) (degreeElevenProfile r) >
      kpEndpointOneProfile kpRadius :=
  kpRadius_unique_oneRadius_optimum
    degreeElevenProfile hdecrease hcross hr hne

/-! Separated-cap stability core. -/

example {eta : ℝ} (heta0 : 0 < eta) (hetaQ : eta < kpQ) :
    kpLocalCoeff < kpStableLocalCoeff eta :=
  kpStableLocalCoeff_gt heta0 hetaQ

example {eta : ℝ} (hetaQ : eta < kpQ) :
    kpRadius ^ 2 * (kpQ - eta) * kpStableLocalCoeff eta = 1 :=
  kp_stable_local_identity hetaQ

example {K eta : ℝ}
    (hK : 0 < K) (heta0 : 0 < eta) (hetaQ : eta < kpQ) :
    K * kpLocalCoeff < kpStabilityMidCoeff K eta :=
  kpStabilityMidCoeff_gt_endpoint hK heta0 hetaQ

example
    {ι : Type*} [Fintype ι]
    (d exposure : ι → ℝ)
    (n E A eta : ℝ)
    (heta0 : 0 < eta) (hetaQ : eta < kpQ)
    (hn : (Fintype.card ι : ℝ) = n)
    (hdeg : (∑ i, d i) = 2 * E)
    (hBoundary : A ≤ ∑ i, exposure i)
    (hLocal : ∀ i,
      exposure i ≤
        2 * Real.pi * kpRadius ^ 2 * (kpQ - eta) * (12 - d i)) :
    KeplerStableLocalSurfaceInput eta A (6 * n - E) :=
  kp_stable_local_surface_input_of_charges
    d exposure n E A eta heta0 hetaQ hn hdeg hBoundary hLocal

example {x A D K eta : ℝ}
    (hx : 0 < x)
    (hg : KeplerGlobalSurfaceInput x A K)
    (hl : KeplerStableLocalSurfaceInput eta A D) :
    kpStabilityMidCoeff K eta * x < D :=
  kp_stability_midpoint_strict hx hg hl

/-! Degree-eleven and minimum-degree constraints. -/

example
    {ι : Type*} [Fintype ι] [DecidableEq ι]
    (degree : ι → ℕ) (D : ℕ)
    (hdeficit : ∑ i, (12 - degree i) = 2 * D) :
    (degreeElevenVertices degree).card ≤ 2 * D :=
  degreeEleven_card_le_twice_contact_deficit degree D hdeficit

example {d : ℕ} (hmin : 2 ≤ d) (hEndpoint : d = 1 ∨ d = 11) :
    d = 11 :=
  endpoint_degree_reduction_of_minimum_two hmin hEndpoint

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

/-! Conditional normalized-deficit limit closure. -/

example {a : ℕ → ℝ} {c : ℝ}
    (h : MatchingSurfaceBounds a c) :
    HasRealSequenceLimit a c :=
  hasRealSequenceLimit_of_matchingSurfaceBounds h

example {a : ℕ → ℝ} {c : ℝ}
    (h : UnrestrictedWulffInput a c) :
    HasRealSequenceLimit a c :=
  unrestricted_normalized_deficit_limit h

example {c₁ c₂ : ℝ}
    (h₁ : 0 ≤ c₁) (h₂ : 0 ≤ c₂)
    (hCube : c₁ ^ 3 < c₂ ^ 3) :
    c₁ < c₂ :=
  positive_cube_gap_implies_positive_coefficient_gap h₁ h₂ hCube

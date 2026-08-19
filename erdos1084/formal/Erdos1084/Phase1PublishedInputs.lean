import Mathlib
import Erdos1084.FiniteSpherePacking
import Erdos1084.KeplerOuterParallel
import Erdos1084.KeplerOptimizedChord

namespace Erdos1084

/-!
# Phase-I geometric input interfaces

This module connects the direct finite-packing/contact-graph model to the already certified
Kepler algebraic assembly. The geometric content remains visible as ordinary theorem data:

* the exact finite truncated-density inequality;
* Euclidean isoperimetry for the enlarged union;
* ownership of the boundary by exposed sphere patches;
* spherical-neighborhood and kissing-number local bounds.

No geometric statement is declared as a project axiom.
-/

noncomputable section

/-- Abstract nonnegative representative of `n^(2/3)`, avoiding real-power APIs. -/
structure TwoThirdPowerScale (n x : ℝ) : Prop where
  n_pos : 0 < n
  x_nonneg : 0 ≤ x
  cube_eq : x ^ 3 = n ^ 2

namespace TwoThirdPowerScale

/-- The selected two-thirds-power representative is strictly positive. -/
theorem x_pos {n x : ℝ} (h : TwoThirdPowerScale n x) : 0 < x := by
  by_contra hnot
  have hx0 : x = 0 := le_antisymm (le_of_not_gt hnot) h.x_nonneg
  have hcube := h.cube_eq
  rw [hx0] at hcube
  norm_num at hcube
  have hn2 : 0 < n ^ 2 := sq_pos_of_pos h.n_pos
  nlinarith

end TwoThirdPowerScale

/-- Exact square-root normalization used by the finite density reduction. -/
theorem phase1_sqrt_eighteen : Real.sqrt 18 = 3 * Real.sqrt 2 := by
  have h18 : (Real.sqrt 18) ^ 2 = 18 := by norm_num
  have h2 : (Real.sqrt 2) ^ 2 = 2 := by norm_num
  have h18nonneg := Real.sqrt_nonneg 18
  have h2nonneg := Real.sqrt_nonneg 2
  nlinarith

/--
Convert the exact finite truncated-density inequality at the Kepler density to the volume bound
`4*sqrt(2)*n ≤ V`.
-/
theorem phase1_volume_lower_of_kepler_density
    {n V : ℝ}
    (hDensity : (4 * Real.pi / 3) * n ≤
      (Real.pi / Real.sqrt 18) * V) :
    4 * Real.sqrt 2 * n ≤ V := by
  have hs18pos : 0 < Real.sqrt 18 := Real.sqrt_pos.2 (by norm_num)
  have hdiv : (4 * Real.pi / 3) * n ≤
      (Real.pi * V) / Real.sqrt 18 := by
    simpa [div_eq_mul_inv, mul_assoc, mul_left_comm, mul_comm] using hDensity
  have hmul : ((4 * Real.pi / 3) * n) * Real.sqrt 18 ≤ Real.pi * V :=
    (le_div_iff₀ hs18pos).1 hdiv
  have hcancel : (4 / 3 : ℝ) * n * Real.sqrt 18 ≤ V := by
    by_contra hnot
    have hrev : V < (4 / 3 : ℝ) * n * Real.sqrt 18 := lt_of_not_ge hnot
    have hmulRev :
        Real.pi * V < Real.pi * ((4 / 3 : ℝ) * n * Real.sqrt 18) :=
      mul_lt_mul_of_pos_left hrev Real.pi_pos
    have hright :
        Real.pi * ((4 / 3 : ℝ) * n * Real.sqrt 18) =
          ((4 * Real.pi / 3) * n) * Real.sqrt 18 := by
      ring
    rw [hright] at hmulRev
    exact (not_lt_of_ge hmul) hmulRev
  calc
    4 * Real.sqrt 2 * n = (4 / 3 : ℝ) * n * Real.sqrt 18 := by
      rw [phase1_sqrt_eighteen]
      ring
    _ ≤ V := hcancel

/-- Exact finite outer-parallel volume conclusion at the optimized radius. -/
structure Phase1OuterParallelInput (n V : ℝ) : Prop where
  n_nonneg : 0 ≤ n
  volume_nonneg : 0 ≤ V
  volume_lower : 4 * Real.sqrt 2 * n ≤ V

/--
Euclidean isoperimetry and the finite outer-parallel volume bound imply the exact global surface
lower bound used by the Kepler assembly.
-/
theorem phase1_global_surface_of_volume_isoperimetry
    {n x V A K : ℝ}
    (hpower : TwoThirdPowerScale n x)
    (hscale : KeplerScaleSpec K)
    (hV : 4 * Real.sqrt 2 * n ≤ V)
    (hVnonneg : 0 ≤ V)
    (hAnonneg : 0 ≤ A)
    (hIso : 36 * Real.pi * V ^ 2 ≤ A ^ 3) :
    4 * Real.pi * K * x ≤ A := by
  have hsqrt2nonneg : 0 ≤ Real.sqrt 2 := Real.sqrt_nonneg _
  have hnnonneg : 0 ≤ n := le_of_lt hpower.n_pos
  have hbaseNonneg : 0 ≤ 4 * Real.sqrt 2 * n := by
    exact mul_nonneg (mul_nonneg (by norm_num) hsqrt2nonneg) hnnonneg
  have hV2 : (4 * Real.sqrt 2 * n) ^ 2 ≤ V ^ 2 := by
    have hprod : 0 ≤
        (V - 4 * Real.sqrt 2 * n) * (V + 4 * Real.sqrt 2 * n) :=
      mul_nonneg (sub_nonneg.mpr hV) (add_nonneg hVnonneg hbaseNonneg)
    nlinarith
  have hs2 : (Real.sqrt 2) ^ 2 = 2 := by norm_num
  have hbaseSq : (4 * Real.sqrt 2 * n) ^ 2 = 32 * n ^ 2 := by
    nlinarith
  have htargetCube : (4 * Real.pi * K * x) ^ 3 ≤ A ^ 3 := by
    calc
      (4 * Real.pi * K * x) ^ 3 =
          64 * Real.pi * (K ^ 3 * Real.pi ^ 2) * x ^ 3 := by ring
      _ = 64 * Real.pi * 18 * n ^ 2 := by
        rw [hscale.2, hpower.cube_eq]
      _ = 36 * Real.pi * (4 * Real.sqrt 2 * n) ^ 2 := by
        rw [hbaseSq]
        ring
      _ ≤ 36 * Real.pi * V ^ 2 := by
        have hfactor : 0 ≤ 36 * Real.pi := by positivity
        exact mul_le_mul_of_nonneg_left hV2 hfactor
      _ ≤ A ^ 3 := hIso
  have htargetNonneg : 0 ≤ 4 * Real.pi * K * x := by
    exact mul_nonneg
      (mul_nonneg (mul_nonneg (by norm_num) (le_of_lt Real.pi_pos)) (le_of_lt hscale.1))
      hpower.x_nonneg
  by_contra hnot
  have hlt : A < 4 * Real.pi * K * x := lt_of_not_ge hnot
  have htargetPos : 0 < 4 * Real.pi * K * x := lt_of_le_of_lt hAnonneg hlt
  have hsum :
      0 < (4 * Real.pi * K * x) ^ 2 +
        (4 * Real.pi * K * x) * A + A ^ 2 := by
    have hsq : 0 < (4 * Real.pi * K * x) ^ 2 := sq_pos_of_pos htargetPos
    have hmid : 0 ≤ (4 * Real.pi * K * x) * A :=
      mul_nonneg htargetNonneg hAnonneg
    have hA2 : 0 ≤ A ^ 2 := sq_nonneg A
    linarith
  have hprod : 0 <
      ((4 * Real.pi * K * x) - A) *
        ((4 * Real.pi * K * x) ^ 2 +
          (4 * Real.pi * K * x) * A + A ^ 2) :=
    mul_pos (sub_pos.mpr hlt) hsum
  have hcubes : A ^ 3 < (4 * Real.pi * K * x) ^ 3 := by
    nlinarith
  exact (not_lt_of_ge htargetCube) hcubes

/-- Exact local exposed-area conclusion for one contact degree. -/
structure Phase1LocalChargeInput (d exposure : ℝ) : Prop where
  degree_lower : 1 ≤ d
  degree_upper : d ≤ 12
  exposure_nonneg : 0 ≤ exposure
  exposure_upper :
    exposure ≤ 2 * Real.pi * kpRadius ^ 2 * kpQ * (12 - d)

/-- The optimized convex chord converts the normalized exposed-area formula to the local charge. -/
theorem phase1_local_charge_of_normalized_exposure
    {d exposure : ℝ}
    (hd1 : 1 ≤ d) (hd11 : d ≤ 11)
    (hExposure :
      exposure ≤ 2 * Real.pi * kpRadius ^ 2 * kpOptimizedH (rtX d)) :
    exposure ≤ 2 * Real.pi * kpRadius ^ 2 * kpQ * (12 - d) := by
  have hopt := kp_optimized_degree_charge hd1 hd11
  calc
    exposure ≤ 2 * Real.pi * kpRadius ^ 2 * kpOptimizedH (rtX d) := hExposure
    _ ≤ 2 * Real.pi * kpRadius ^ 2 * (kpQ * (12 - d)) := by
      exact mul_le_mul_of_nonneg_left hopt (by positivity)
    _ = 2 * Real.pi * kpRadius ^ 2 * kpQ * (12 - d) := by ring

/-- Degree twelve has the required local charge as soon as its exposed area vanishes. -/
theorem phase1_local_charge_of_degree_twelve
    {exposure : ℝ} (hExposure : exposure ≤ 0) :
    exposure ≤ 2 * Real.pi * kpRadius ^ 2 * kpQ * (12 - (12 : ℝ)) := by
  simpa using hExposure

/--
The published/geometric content needed for one actual finite contact configuration.

`A` is the boundary area of the enlarged union and `exposure i` is the actual exposed area owned
by sphere `i`. The positive scale `K` is constrained by `K^3*pi^2=18` through
`KeplerScaleSpec K`.
-/
structure Phase1GeometricCertificate
    {ι : Type*} [Fintype ι]
    (X : UnitSeparatedConfiguration ι)
    (n E x A K : ℝ)
    (exposure : ι → ℝ) : Prop where
  card_eq : (Fintype.card ι : ℝ) = n
  contact_eq : (X.contactCount : ℝ) = E
  power : TwoThirdPowerScale n x
  scale : KeplerScaleSpec K
  global_surface : 4 * Real.pi * K * x ≤ A
  boundary_owned : A ≤ ∑ i, exposure i
  local_charge : ∀ i,
    exposure i ≤
      2 * Real.pi * kpRadius ^ 2 * kpQ * (12 - (X.contactDegree i : ℝ))

/-- The degree sum converts the local certificate to the scalar local surface input. -/
theorem phase1_local_surface_of_certificate
    {ι : Type*} [Fintype ι]
    (X : UnitSeparatedConfiguration ι)
    {n E x A K : ℝ}
    {exposure : ι → ℝ}
    (h : Phase1GeometricCertificate X n E x A K exposure) :
    KeplerLocalSurfaceInput A (6 * n - E) := by
  have hdegreeNat := X.sum_contactDegrees_eq_twice_contactCount
  have hdegreeReal :
      (∑ i, (X.contactDegree i : ℝ)) = 2 * E := by
    rw [← h.contact_eq]
    exact_mod_cast hdegreeNat
  exact kp_local_surface_input_of_charges
    (fun i => (X.contactDegree i : ℝ)) exposure n E A
    h.card_eq hdegreeReal h.boundary_owned h.local_charge

/-- Package the exact Kepler global surface input from the geometric certificate. -/
theorem phase1_global_surface_of_certificate
    {ι : Type*} [Fintype ι]
    (X : UnitSeparatedConfiguration ι)
    {n E x A K : ℝ}
    {exposure : ι → ℝ}
    (h : Phase1GeometricCertificate X n E x A K exposure) :
    KeplerGlobalSurfaceInput x A K :=
  ⟨h.scale, h.global_surface⟩

/--
End-to-end Phase-I scalar conclusion from a direct finite packing and an explicit geometric
certificate. No scalar contact deficit is assumed: it is derived from the actual contact graph.
-/
theorem phase1_contact_upper_from_certificate
    {ι : Type*} [Fintype ι]
    (X : UnitSeparatedConfiguration ι)
    {n E x A K : ℝ}
    {exposure : ι → ℝ}
    (h : Phase1GeometricCertificate X n E x A K exposure) :
    E < 6 * n - kpClean * x := by
  have hpower : KeplerPowerScale n x :=
    ⟨h.power.n_pos, h.power.x_nonneg, h.power.cube_eq⟩
  exact kp_contact_upper_from_surface hpower
    (phase1_global_surface_of_certificate X h)
    (phase1_local_surface_of_certificate X h)

end

end Erdos1084

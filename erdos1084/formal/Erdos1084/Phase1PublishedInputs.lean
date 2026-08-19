import Mathlib
import Erdos1084.FiniteSpherePacking
import Erdos1084.KeplerOuterParallel
import Erdos1084.KeplerOptimizedChord

namespace Erdos1084

/-!
# Phase-I geometric input interfaces

This module connects the direct finite-packing/contact-graph model to the already certified
Kepler algebraic assembly.  The geometric content remains visible as ordinary theorem data:

* the exact positive Kepler scale;
* the global surface lower bound for the enlarged union;
* ownership of the boundary by exposed sphere patches;
* the local degreewise exposed-area bounds.

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
  rw [hx0] at h.cube_eq
  have hn2 : 0 < n ^ 2 := sq_pos_of_pos h.n_pos
  norm_num at h.cube_eq
  nlinarith

end TwoThirdPowerScale

/-- Exact finite outer-parallel volume conclusion at the optimized radius. -/
structure Phase1OuterParallelInput (n V : ℝ) : Prop where
  n_nonneg : 0 ≤ n
  volume_nonneg : 0 ≤ V
  volume_lower : 4 * Real.sqrt 2 * n ≤ V

/-- Exact local exposed-area conclusion for one contact degree. -/
structure Phase1LocalChargeInput (d exposure : ℝ) : Prop where
  degree_lower : 1 ≤ d
  degree_upper : d ≤ 12
  exposure_nonneg : 0 ≤ exposure
  exposure_upper :
    exposure ≤ 2 * Real.pi * kpRadius ^ 2 * kpQ * (12 - d)

/--
The published/geometric content needed for one actual finite contact configuration.

`A` is the boundary area of the enlarged union and `exposure i` is the actual exposed area owned
by sphere `i`.  The positive scale `K` is constrained by `K^3*pi^2=18` through
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
certificate.  No scalar contact deficit is assumed: it is derived from the actual contact graph.
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

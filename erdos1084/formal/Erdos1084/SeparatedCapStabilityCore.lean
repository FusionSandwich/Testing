import Mathlib
import Erdos1084.KeplerOuterParallel

namespace Erdos1084

/-!
# Abstract separated-cap stability assembly

The geometric compactness theorem supplies a number `eta` with `0 < eta < kpQ` such that every
nonzero local degree deficit is charged by `kpQ - eta` rather than `kpQ`.  This file proves the
exact algebraic consequence: any such uniform remainder gives a coefficient strictly larger than
the endpoint Kepler coefficient.

The existence or numerical value of `eta` is not postulated as a project axiom.  It is an ordinary
theorem parameter whose geometric proof is recorded in `SEPARATED_CAP_STABILITY.md`.
-/

/-- Reciprocal local factor after a uniform separated-cap improvement `eta`. -/
def kpStableLocalCoeff (eta : ℝ) : ℝ :=
  kpLocalCoeff * kpQ / (kpQ - eta)

/-- Midpoint between the endpoint and stability-improved global coefficients. -/
def kpStabilityMidCoeff (K eta : ℝ) : ℝ :=
  K * (kpLocalCoeff + kpStableLocalCoeff eta) / 2

/-- The improved local denominator is positive. -/
theorem kp_stable_denominator_pos {eta : ℝ}
    (heta : eta < kpQ) :
    0 < kpQ - eta := sub_pos.mpr heta

/-- The stability-improved reciprocal factor is strictly larger. -/
theorem kpStableLocalCoeff_gt {eta : ℝ}
    (heta0 : 0 < eta) (hetaQ : eta < kpQ) :
    kpLocalCoeff < kpStableLocalCoeff eta := by
  have hden : 0 < kpQ - eta := kp_stable_denominator_pos hetaQ
  have hq : 0 < kpQ := kpQ_pos
  have hratio : 1 < kpQ / (kpQ - eta) := by
    apply (lt_div_iff₀ hden).2
    linarith
  dsimp [kpStableLocalCoeff]
  have hmul := mul_lt_mul_of_pos_left hratio kpLocalCoeff_pos
  simpa using hmul

/-- Exact reciprocal identity for the stability-improved local charge. -/
theorem kp_stable_local_identity {eta : ℝ}
    (hetaQ : eta < kpQ) :
    kpRadius ^ 2 * (kpQ - eta) * kpStableLocalCoeff eta = 1 := by
  have hden : kpQ - eta ≠ 0 := ne_of_gt (kp_stable_denominator_pos hetaQ)
  dsimp [kpStableLocalCoeff]
  field_simp [hden]
  nlinarith [kp_local_identity]

/-- The midpoint coefficient is strictly above the endpoint coefficient. -/
theorem kpStabilityMidCoeff_gt_endpoint {K eta : ℝ}
    (hK : 0 < K)
    (heta0 : 0 < eta) (hetaQ : eta < kpQ) :
    K * kpLocalCoeff < kpStabilityMidCoeff K eta := by
  have himprove := kpStableLocalCoeff_gt heta0 hetaQ
  dsimp [kpStabilityMidCoeff]
  nlinarith

/-- Stable local surface upper-bound interface. -/
structure KeplerStableLocalSurfaceInput (eta A D : ℝ) : Prop where
  eta_pos : 0 < eta
  eta_lt_q : eta < kpQ
  surface_upper : A ≤ 4 * Real.pi * kpRadius ^ 2 * (kpQ - eta) * D

/-- Build the stable local surface interface from per-sphere improved charges. -/
theorem kp_stable_local_surface_input_of_charges
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
    KeplerStableLocalSurfaceInput eta A (6 * n - E) := by
  have hsum :
      (∑ i, exposure i) ≤
        ∑ i,
          2 * Real.pi * kpRadius ^ 2 * (kpQ - eta) * (12 - d i) :=
    Finset.sum_le_sum fun i _ => hLocal i
  have hdef := radiusTwo_degree_deficit_sum d n E hn hdeg
  refine ⟨heta0, hetaQ, ?_⟩
  calc
    A ≤ ∑ i, exposure i := hBoundary
    _ ≤ ∑ i,
        2 * Real.pi * kpRadius ^ 2 * (kpQ - eta) * (12 - d i) := hsum
    _ = (2 * Real.pi * kpRadius ^ 2 * (kpQ - eta)) *
        ∑ i, (12 - d i) := by
          rw [Finset.mul_sum]
    _ = (2 * Real.pi * kpRadius ^ 2 * (kpQ - eta)) *
        (2 * (6 * n - E)) := by rw [hdef]
    _ = 4 * Real.pi * kpRadius ^ 2 * (kpQ - eta) * (6 * n - E) := by
      ring

/-- The improved global coefficient is bounded above by the contact deficit. -/
theorem kp_stability_improved_assembly
    {x A D K eta : ℝ}
    (hx : 0 < x)
    (hg : KeplerGlobalSurfaceInput x A K)
    (hl : KeplerStableLocalSurfaceInput eta A D) :
    K * kpStableLocalCoeff eta * x ≤ D := by
  have hchain :
      4 * Real.pi * K * x ≤
        4 * Real.pi * kpRadius ^ 2 * (kpQ - eta) * D :=
    le_trans hg.surface_lower hl.surface_upper
  have hfourpi : 0 < 4 * Real.pi := by positivity
  have hchain' :
      (4 * Real.pi) * (K * x) ≤
        (4 * Real.pi) *
          (kpRadius ^ 2 * (kpQ - eta) * D) := by
    simpa [mul_assoc] using hchain
  have hKx : K * x ≤ kpRadius ^ 2 * (kpQ - eta) * D := by
    by_contra hnot
    have hrev : kpRadius ^ 2 * (kpQ - eta) * D < K * x :=
      lt_of_not_ge hnot
    have hmul := mul_lt_mul_of_pos_left hrev hfourpi
    exact (not_lt_of_ge hchain') hmul
  have hstablePos : 0 < kpStableLocalCoeff eta := by
    dsimp [kpStableLocalCoeff]
    exact div_pos (mul_pos kpLocalCoeff_pos kpQ_pos)
      (kp_stable_denominator_pos hl.eta_lt_q)
  have hmul := mul_le_mul_of_nonneg_right hKx (le_of_lt hstablePos)
  calc
    K * kpStableLocalCoeff eta * x = (K * x) * kpStableLocalCoeff eta := by
      ring
    _ ≤ (kpRadius ^ 2 * (kpQ - eta) * D) *
        kpStableLocalCoeff eta := hmul
    _ = (kpRadius ^ 2 * (kpQ - eta) * kpStableLocalCoeff eta) * D := by
      ring
    _ = D := by rw [kp_stable_local_identity hl.eta_lt_q]; ring

/-- A coefficient strictly above the endpoint Kepler value is valid. -/
theorem kp_stability_midpoint_strict
    {x A D K eta : ℝ}
    (hx : 0 < x)
    (hg : KeplerGlobalSurfaceInput x A K)
    (hl : KeplerStableLocalSurfaceInput eta A D) :
    kpStabilityMidCoeff K eta * x < D := by
  have hK : 0 < K := hg.scale.1
  have hmidEndpoint :=
    kpStabilityMidCoeff_gt_endpoint hK hl.eta_pos hl.eta_lt_q
  have hmidStable :
      kpStabilityMidCoeff K eta < K * kpStableLocalCoeff eta := by
    have himprove := kpStableLocalCoeff_gt hl.eta_pos hl.eta_lt_q
    dsimp [kpStabilityMidCoeff]
    nlinarith
  have hstrict :
      kpStabilityMidCoeff K eta * x <
        K * kpStableLocalCoeff eta * x :=
    mul_lt_mul_of_pos_right hmidStable hx
  exact lt_of_lt_of_le hstrict (kp_stability_improved_assembly hx hg hl)

end Erdos1084

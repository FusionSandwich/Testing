import Mathlib
import Erdos1084.KeplerOneRadiusConcrete

namespace Erdos1084

/-!
# Calculus closure of the one-radius optimizer

`KeplerOneRadiusConcrete.lean` proves the exact endpoint algebra, the negative
candidate derivative on `[2,kpRadius]`, and the endpoint crossing. This module
checks the derivative formula, turns derivative negativity into strict decrease,
and invokes the abstract minimax theorem to obtain the fully concrete unique
optimizer with no ordinary monotonicity parameter.
-/

noncomputable section

/-- Exact derivative of the concrete degree-eleven endpoint profile. -/
theorem kpEndpointElevenProfile_hasDerivAt
    {r : ℝ} (hr : 1 < r) :
    HasDerivAt kpEndpointElevenProfile (kpEndpointElevenDerivative r) r := by
  have hrad : 0 < r ^ 2 - 1 := by nlinarith
  have hradne : r ^ 2 - 1 ≠ 0 := ne_of_gt hrad
  have hsqrtne : Real.sqrt (r ^ 2 - 1) ≠ 0 :=
    ne_of_gt (Real.sqrt_pos.2 hrad)

  have hsq : HasDerivAt (fun x : ℝ => x ^ 2) (2 * r) r := by
    simpa using (hasDerivAt_pow 2 r)

  have hinner :
      HasDerivAt (fun x : ℝ => x ^ 2 - 1) (2 * r) r :=
    hsq.sub_const 1

  have hsqrt :
      HasDerivAt
        (fun x : ℝ => Real.sqrt (x ^ 2 - 1))
        ((2 * r) / (2 * Real.sqrt (r ^ 2 - 1))) r :=
    hinner.sqrt hradne

  have hprodRaw :
      HasDerivAt
        (fun x : ℝ => x * Real.sqrt (x ^ 2 - 1))
        (r * ((2 * r) / (2 * Real.sqrt (r ^ 2 - 1))) +
          Real.sqrt (r ^ 2 - 1)) r := by
    simpa [Pi.smul_apply, smul_eq_mul] using
      (hasDerivAt_id r).smul hsqrt

  have hprodDeriv :
      r * ((2 * r) / (2 * Real.sqrt (r ^ 2 - 1))) +
          Real.sqrt (r ^ 2 - 1) =
        (2 * r ^ 2 - 1) / Real.sqrt (r ^ 2 - 1) := by
    field_simp [hsqrtne]
    rw [Real.sq_sqrt (le_of_lt hrad)]
    ring

  have hprod :
      HasDerivAt
        (fun x : ℝ => x * Real.sqrt (x ^ 2 - 1))
        ((2 * r ^ 2 - 1) / Real.sqrt (r ^ 2 - 1)) r := by
    simpa only [hprodDeriv] using hprodRaw

  have hlinear :
      HasDerivAt (fun x : ℝ => kpEndpointElevenCos * x)
        kpEndpointElevenCos r := by
    simpa [Pi.smul_apply, smul_eq_mul] using
      (hasDerivAt_id r).const_smul kpEndpointElevenCos

  have hpoly :
      HasDerivAt
        (fun x : ℝ => x ^ 2 + kpEndpointElevenCos * x)
        (2 * r + kpEndpointElevenCos) r :=
    hsq.add hlinear

  have hscaled :
      HasDerivAt
        (fun x : ℝ => kpEndpointElevenSin *
          (x * Real.sqrt (x ^ 2 - 1)))
        (kpEndpointElevenSin * (2 * r ^ 2 - 1) /
          Real.sqrt (r ^ 2 - 1)) r := by
    simpa [Pi.smul_apply, smul_eq_mul, div_eq_mul_inv, mul_assoc] using
      hprod.const_smul kpEndpointElevenSin

  have hprofile :
      HasDerivAt
        (fun x : ℝ =>
          x ^ 2 + kpEndpointElevenCos * x -
            kpEndpointElevenSin * (x * Real.sqrt (x ^ 2 - 1)))
        ((2 * r + kpEndpointElevenCos) -
          kpEndpointElevenSin * (2 * r ^ 2 - 1) /
            Real.sqrt (r ^ 2 - 1)) r :=
    hpoly.sub hscaled

  change HasDerivAt
    (fun x : ℝ =>
      x ^ 2 + kpEndpointElevenCos * x -
        kpEndpointElevenSin * (x * Real.sqrt (x ^ 2 - 1)))
    ((2 * r + kpEndpointElevenCos) -
      kpEndpointElevenSin * (2 * r ^ 2 - 1) /
        Real.sqrt (r ^ 2 - 1)) r
  exact hprofile

/-- The concrete degree-eleven endpoint profile is strictly decreasing. -/
theorem kpEndpointElevenProfile_strictAntiOn :
    StrictAntiOn kpEndpointElevenProfile (Set.Icc (2 : ℝ) kpRadius) := by
  refine strictAntiOn_of_deriv_neg (convex_Icc _ _) ?_ ?_
  · intro r hr
    have hr1 : 1 < r := by linarith [hr.1]
    exact (kpEndpointElevenProfile_hasDerivAt hr1).continuousAt.continuousWithinAt
  · intro r hr
    have hrIcc : r ∈ Set.Icc (2 : ℝ) kpRadius := interior_subset hr
    have hr1 : 1 < r := by linarith [hrIcc.1]
    rw [(kpEndpointElevenProfile_hasDerivAt hr1).deriv]
    exact kpEndpointElevenDerivative_neg hrIcc.1 hrIcc.2

/-- Fully concrete unique minimax theorem, with no endpoint-profile hypothesis. -/
theorem kpRadius_unique_oneRadius_optimum_fullyConcrete :
    ∀ ⦃r : ℝ⦄, 2 ≤ r → r ≠ kpRadius →
      max (kpEndpointOneProfile r) (kpEndpointElevenProfile r) >
        kpEndpointOneProfile kpRadius := by
  exact kpRadius_unique_oneRadius_optimum
    kpEndpointElevenProfile
    kpEndpointElevenProfile_strictAntiOn
    kpEndpointElevenProfile_at_optimizer

end

end Erdos1084

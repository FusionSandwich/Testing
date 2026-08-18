import Mathlib
import Erdos1084.KeplerOuterParallel

namespace Erdos1084

/-!
# One-radius minimax optimality core

The exact human proof shows that the degreewise affine method reduces to two endpoint profiles:

* `B₁(r) = (r²+r)/11`, strictly increasing for `r >= 2`;
* the degree-eleven profile `B₁₁(r)`, strictly decreasing on `[2,r_*]`;
* the two profiles agree at `r_*`.

This file machine-checks the minimax logic, the degree-one monotonicity, and the exact endpoint
value. The trigonometric proof that the concrete degree-eleven profile is strictly decreasing is
kept as an explicit hypothesis; it is proved in `ONE_RADIUS_OPTIMALITY.md`.
-/

noncomputable section

/-- Scaled degree-one endpoint charge. -/
def kpEndpointOneProfile (r : ℝ) : ℝ :=
  (r ^ 2 + r) / 11

/-- The degree-one endpoint charge is strictly increasing on nonnegative radii. -/
theorem kpEndpointOneProfile_strictMonoOn :
    StrictMonoOn kpEndpointOneProfile (Set.Ici (0 : ℝ)) := by
  intro a ha b hb hab
  have ha0 : 0 ≤ a := ha
  have hb0 : 0 ≤ b := hb
  have hsum : 0 < a + b + 1 := by linarith
  have hprod : 0 < (b - a) * (a + b + 1) :=
    mul_pos (sub_pos.mpr hab) hsum
  have hdiff :
      (b ^ 2 + b) - (a ^ 2 + a) =
        (b - a) * (a + b + 1) := by ring
  dsimp [kpEndpointOneProfile]
  nlinarith

/-- Exact degree-one endpoint value at the optimized radius. -/
theorem kpEndpointOneProfile_at_optimizer :
    kpEndpointOneProfile kpRadius = kpRadius ^ 2 * kpQ := by
  have hrec : 1 / kpRadius = 10 - 11 * kpS / 2 :=
    kpRadius_reciprocal
  have hQ : kpQ = (1 + 1 / kpRadius) / 11 := by
    rw [hrec]
    dsimp [kpQ]
    ring
  have hrne : kpRadius ≠ 0 := ne_of_gt kpRadius_pos
  unfold kpEndpointOneProfile
  rw [hQ]
  field_simp [hrne]
  ring

/--
Abstract unique minimax lemma.

No behavior of `g` to the right of `rStar` is needed: there the increasing profile `f` alone
forces the maximum above its crossing value.
-/
theorem unique_minimax_of_increasing_decreasing_crossing
    {f g : ℝ → ℝ} {a rStar : ℝ}
    (ha : a ≤ rStar)
    (hf : StrictMonoOn f (Set.Ici a))
    (hg : StrictAntiOn g (Set.Icc a rStar))
    (heq : f rStar = g rStar) :
    ∀ ⦃r : ℝ⦄, a ≤ r → r ≠ rStar →
      max (f r) (g r) > f rStar := by
  intro r har hrne
  rcases lt_or_gt_of_ne hrne with hlt | hgt
  · have hra : r ∈ Set.Icc a rStar := ⟨har, le_of_lt hlt⟩
    have hstar : rStar ∈ Set.Icc a rStar := ⟨ha, le_rfl⟩
    have hglt : g rStar < g r := hg hra hstar hlt
    calc
      f rStar = g rStar := heq
      _ < g r := hglt
      _ ≤ max (f r) (g r) := le_max_right _ _
  · have hrmem : r ∈ Set.Ici a := har
    have hsmem : rStar ∈ Set.Ici a := ha
    have hflt : f rStar < f r := hf hsmem hrmem hgt
    exact lt_of_lt_of_le hflt (le_max_left _ _)

/-- The degree-one profile is strictly increasing on radii at least two. -/
theorem kpEndpointOneProfile_strictMonoOn_two :
    StrictMonoOn kpEndpointOneProfile (Set.Ici (2 : ℝ)) := by
  intro a ha b hb hab
  apply kpEndpointOneProfile_strictMonoOn
  · show (0 : ℝ) ≤ a
    linarith
  · show (0 : ℝ) ≤ b
    linarith
  · exact hab

/--
Unique optimality of `kpRadius` once the concrete degree-eleven monotonicity theorem is supplied.
-/
theorem kpRadius_unique_oneRadius_optimum
    (degreeElevenProfile : ℝ → ℝ)
    (hdecrease :
      StrictAntiOn degreeElevenProfile (Set.Icc (2 : ℝ) kpRadius))
    (hcross :
      degreeElevenProfile kpRadius = kpEndpointOneProfile kpRadius) :
    ∀ ⦃r : ℝ⦄, 2 ≤ r → r ≠ kpRadius →
      max (kpEndpointOneProfile r) (degreeElevenProfile r) >
        kpEndpointOneProfile kpRadius := by
  apply unique_minimax_of_increasing_decreasing_crossing
  · exact le_of_lt two_lt_kpRadius
  · exact kpEndpointOneProfile_strictMonoOn_two
  · exact hdecrease
  · exact hcross.symm

end

end Erdos1084

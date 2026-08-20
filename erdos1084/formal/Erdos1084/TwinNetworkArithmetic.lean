import Mathlib

namespace Erdos1084

/-!
# Arithmetic spine for coherent-twin network junctions

A geometric coherent-twin complex has perfect degree twelve away from a fixed
neighborhood of its external boundary and codimension-two skeleton.  This module
formalizes the finite combinatorial conclusion: if only `B` sites can have degree
below twelve, then the contact deficit is at most `6 B`; if `B` is line order,
then so is the junction deficit.
-/

open scoped BigOperators

/--
If all vertices outside `bad` have degree twelve, then the total natural degree
deficit is at most twelve times `bad.card`.
-/
theorem degreeDeficitSum_le_twelve_badCard
    {ι : Type*} [Fintype ι] [DecidableEq ι]
    (degree : ι → ℕ) (bad : Finset ι)
    (hgood : ∀ i, i ∉ bad → degree i = 12) :
    (∑ i : ι, (12 - degree i)) ≤ 12 * bad.card := by
  calc
    (∑ i : ι, (12 - degree i))
        ≤ ∑ i : ι, if i ∈ bad then 12 else 0 := by
      apply Finset.sum_le_sum
      intro i _
      by_cases hi : i ∈ bad
      · simp [hi]
      · simp [hi, hgood i hi]
    _ = 12 * bad.card := by
      simp
      omega

/--
If the degree-deficit sum equals `2 D` and only `bad` vertices can be defective,
then `D ≤ 6 * bad.card`.
-/
theorem contactDeficit_le_six_badCard
    {ι : Type*} [Fintype ι] [DecidableEq ι]
    (degree : ι → ℕ) (bad : Finset ι) (D : ℕ)
    (hgood : ∀ i, i ∉ bad → degree i = 12)
    (hdeficit : ∑ i : ι, (12 - degree i) = 2 * D) :
    D ≤ 6 * bad.card := by
  have hsum : 2 * D ≤ 12 * bad.card := by
    rw [← hdeficit]
    exact degreeDeficitSum_le_twelve_badCard degree bad hgood
  omega

/-- A line-order bad-site bound gives a line-order contact-deficit bound. -/
theorem contactDeficit_le_lineOrder
    {D bad C₁ C₀ T : ℕ}
    (hD : D ≤ 6 * bad)
    (hbad : bad ≤ C₁ * T + C₀) :
    D ≤ 6 * C₁ * T + 6 * C₀ := by
  calc
    D ≤ 6 * bad := hD
    _ ≤ 6 * (C₁ * T + C₀) := Nat.mul_le_mul_left 6 hbad
    _ = 6 * C₁ * T + 6 * C₀ := by ring

/--
Scalar form of the deletion estimate: if deleting `removed` sites changes the
deficit by `-6*removed + incident` and at most twelve incident contacts are
charged per removed site, the deficit rises by at most `6*removed`.
-/
theorem deletion_deficit_increase_le_six
    {oldD newD removed incident : ℤ}
    (hidentity : newD - oldD = -6 * removed + incident)
    (hincident : incident ≤ 12 * removed) :
    newD ≤ oldD + 6 * removed := by
  linarith

/-- A cost bounded by `A*T+B` has the corresponding surface-scaled estimate. -/
theorem lineOrder_surfaceScale_bound
    {T A B cost : ℝ}
    (hT : 0 < T)
    (hcost : cost ≤ A * T + B) :
    cost / T ^ 2 ≤ A / T + B / T ^ 2 := by
  have hT2 : 0 < T ^ 2 := sq_pos_of_pos hT
  exact (div_le_iff₀ hT2).2 <| by
    have hmul := mul_le_mul_of_nonneg_right hcost (le_of_lt hT2)
    field_simp [ne_of_gt hT]
    nlinarith

/-- Pure line-order cost gives the simpler `A/T` surface-density bound. -/
theorem pureLineOrder_surfaceScale_bound
    {T A cost : ℝ}
    (hT : 0 < T)
    (hcost : cost ≤ A * T) :
    cost / T ^ 2 ≤ A / T := by
  have hbound :
      cost / T ^ 2 ≤ A / T + (0 : ℝ) / T ^ 2 :=
    lineOrder_surfaceScale_bound
      (T := T) (A := A) (B := 0) (cost := cost) hT (by simpa using hcost)
  simpa using hbound

end Erdos1084

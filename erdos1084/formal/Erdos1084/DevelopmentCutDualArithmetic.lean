import Mathlib
import Erdos1084.AveragedDevelopmentArithmetic

namespace Erdos1084

/-!
# Dual arithmetic for fractional development cuts

A feasible averaged development gives a probability distribution whose expected
jump vector is componentwise bounded by the physical interface vector. Every
nonnegative interface-price vector must therefore price the physical vector at
least as highly as the cheapest admissible development cut.

This module proves that easy dual implication and the strict dual obstruction.
The converse from absence of a dual obstruction to primal feasibility is the
finite-dimensional polyhedral separation theorem and remains an explicit linear-
programming input in the human proof.
-/

open scoped BigOperators

/-- Priced developed jump of one admissible development. -/
def pricedDevelopmentCut
    {D I : Type*} (interfaces : Finset I)
    (price : I → ℝ) (jump : D → I → ℝ) (d : D) : ℝ :=
  ∑ i ∈ interfaces, price i * jump d i

/-- Priced physical interface budget. -/
def pricedPhysicalInterfaces
    {I : Type*} (interfaces : Finset I)
    (price physical : I → ℝ) : ℝ :=
  ∑ i ∈ interfaces, price i * physical i

/-- Expected priced cut equals the price of the expected jump vector. -/
theorem expectedPricedCut_eq_priceExpectedJump
    {D I : Type*} (developments : Finset D) (interfaces : Finset I)
    (weight : D → ℝ) (price : I → ℝ) (jump : D → I → ℝ) :
    expectedDevelopmentCost developments weight
        (pricedDevelopmentCut interfaces price jump) =
      ∑ i ∈ interfaces,
        price i * expectedInterfaceJump developments weight jump i := by
  unfold expectedDevelopmentCost pricedDevelopmentCut expectedInterfaceJump
  calc
    (∑ d ∈ developments,
        weight d * (∑ i ∈ interfaces, price i * jump d i)) =
      ∑ d ∈ developments, ∑ i ∈ interfaces,
        price i * (weight d * jump d i) := by
        apply Finset.sum_congr rfl
        intro d hd
        rw [Finset.mul_sum]
        apply Finset.sum_congr rfl
        intro i hi
        ring
    _ = ∑ i ∈ interfaces, ∑ d ∈ developments,
        price i * (weight d * jump d i) := by
      rw [Finset.sum_comm]
    _ = ∑ i ∈ interfaces,
        price i * (∑ d ∈ developments, weight d * jump d i) := by
      apply Finset.sum_congr rfl
      intro i hi
      rw [Finset.mul_sum]

/-- Componentwise primal feasibility gives the corresponding priced upper bound. -/
theorem priceExpectedJump_le_physical
    {D I : Type*} (developments : Finset D) (interfaces : Finset I)
    (weight : D → ℝ) (price : I → ℝ)
    (jump : D → I → ℝ) (physical : I → ℝ)
    (hprice : ∀ i ∈ interfaces, 0 ≤ price i)
    (hfeasible : ∀ i ∈ interfaces,
      expectedInterfaceJump developments weight jump i ≤ physical i) :
    (∑ i ∈ interfaces,
      price i * expectedInterfaceJump developments weight jump i) ≤
      pricedPhysicalInterfaces interfaces price physical := by
  unfold pricedPhysicalInterfaces
  exact Finset.sum_le_sum fun i hi =>
    mul_le_mul_of_nonneg_left (hfeasible i hi) (hprice i hi)

/--
Every feasible fractional development satisfies every nonnegative-price dual
lower bound.
-/
theorem feasibleDevelopment_implies_dualBound
    {D I : Type*} (developments : Finset D) (interfaces : Finset I)
    (weight : D → ℝ) (price : I → ℝ)
    (jump : D → I → ℝ) (physical : I → ℝ)
    {lower : ℝ}
    (hweight : ∀ d ∈ developments, 0 ≤ weight d)
    (hsum : (∑ d ∈ developments, weight d) = 1)
    (hfeasible : ∀ i ∈ interfaces,
      expectedInterfaceJump developments weight jump i ≤ physical i)
    (hprice : ∀ i ∈ interfaces, 0 ≤ price i)
    (hcutLower : ∀ d ∈ developments,
      lower ≤ pricedDevelopmentCut interfaces price jump d) :
    lower ≤ pricedPhysicalInterfaces interfaces price physical := by
  have haverage :
      lower ≤ expectedDevelopmentCost developments weight
        (pricedDevelopmentCut interfaces price jump) := by
    have hraw := averagedDevelopment_scalar_bound
      developments weight (pricedDevelopmentCut interfaces price jump)
      (sharp := lower) (exterior := 0)
      hweight hsum (fun d hd => by simpa using hcutLower d hd)
    simpa using hraw
  rw [expectedPricedCut_eq_priceExpectedJump
    developments interfaces weight price jump] at haverage
  exact haverage.trans
    (priceExpectedJump_le_physical developments interfaces
      weight price jump physical hprice hfeasible)

/-- Fractional-development feasibility predicate. -/
def IsFractionalDevelopmentFeasible
    {D I : Type*} (developments : Finset D) (interfaces : Finset I)
    (jump : D → I → ℝ) (physical : I → ℝ) : Prop :=
  ∃ weight : D → ℝ,
    (∀ d ∈ developments, 0 ≤ weight d) ∧
    (∑ d ∈ developments, weight d) = 1 ∧
    ∀ i ∈ interfaces,
      expectedInterfaceJump developments weight jump i ≤ physical i

/-- A strict nonnegative-price dual gap rules out every primal distribution. -/
theorem not_feasible_of_strict_dualGap
    {D I : Type*} (developments : Finset D) (interfaces : Finset I)
    (price : I → ℝ) (jump : D → I → ℝ) (physical : I → ℝ)
    {lower : ℝ}
    (hprice : ∀ i ∈ interfaces, 0 ≤ price i)
    (hcutLower : ∀ d ∈ developments,
      lower ≤ pricedDevelopmentCut interfaces price jump d)
    (hgap : pricedPhysicalInterfaces interfaces price physical < lower) :
    ¬ IsFractionalDevelopmentFeasible developments interfaces jump physical := by
  intro hfeasible
  rcases hfeasible with ⟨weight, hweight, hsum, hinterfaces⟩
  have hdual := feasibleDevelopment_implies_dualBound
    developments interfaces weight price jump physical
    hweight hsum hinterfaces hprice hcutLower
  linarith

/-- Easy dual direction in minimum form, supplied as a common lower bound. -/
theorem minimumPricedCut_le_physical_of_feasible
    {D I : Type*} (developments : Finset D) (interfaces : Finset I)
    (weight : D → ℝ) (price : I → ℝ)
    (jump : D → I → ℝ) (physical : I → ℝ)
    {minimum : ℝ}
    (hweight : ∀ d ∈ developments, 0 ≤ weight d)
    (hsum : (∑ d ∈ developments, weight d) = 1)
    (hfeasible : ∀ i ∈ interfaces,
      expectedInterfaceJump developments weight jump i ≤ physical i)
    (hprice : ∀ i ∈ interfaces, 0 ≤ price i)
    (hminimum : ∀ d ∈ developments,
      minimum ≤ pricedDevelopmentCut interfaces price jump d) :
    minimum ≤ pricedPhysicalInterfaces interfaces price physical :=
  feasibleDevelopment_implies_dualBound
    developments interfaces weight price jump physical
    hweight hsum hfeasible hprice hminimum

end Erdos1084

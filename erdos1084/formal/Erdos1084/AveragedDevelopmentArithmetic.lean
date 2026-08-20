import Mathlib
import Erdos1084.CalibrationDeficitArithmetic

namespace Erdos1084

/-!
# Averaged-development selector arithmetic

Different crystallographic developments can place the necessary branch cuts on
different interfaces. Averaging the sharp Wulff inequalities only requires the
physical interface vector to dominate the expected developed cut vector. This
module proves the finite averaging, interface-sum rearrangement, aggregate and
interfacewise selector criteria, and the uniform-cycle threshold.
-/

open scoped BigOperators

/-- Expected scalar cut cost of a finite distribution of developments. -/
def expectedDevelopmentCost
    {D : Type*} (developments : Finset D)
    (weight cutCost : D → ℝ) : ℝ :=
  ∑ d ∈ developments, weight d * cutCost d

/-- Expected developed jump on one interface. -/
def expectedInterfaceJump
    {D I : Type*} (developments : Finset D)
    (weight : D → ℝ) (jump : D → I → ℝ) (i : I) : ℝ :=
  ∑ d ∈ developments, weight d * jump d i

/-- Averaging sharp lower bounds over a probability distribution of developments. -/
theorem averagedDevelopment_scalar_bound
    {D : Type*} (developments : Finset D)
    (weight cutCost : D → ℝ)
    {sharp exterior : ℝ}
    (hweight : ∀ d ∈ developments, 0 ≤ weight d)
    (hsum : (∑ d ∈ developments, weight d) = 1)
    (hdevelopment : ∀ d ∈ developments,
      sharp ≤ exterior + cutCost d) :
    sharp ≤ exterior + expectedDevelopmentCost developments weight cutCost := by
  have hweighted :
      (∑ d ∈ developments, weight d * sharp) ≤
        ∑ d ∈ developments, weight d * (exterior + cutCost d) := by
    exact Finset.sum_le_sum fun d hd =>
      mul_le_mul_of_nonneg_left (hdevelopment d hd) (hweight d hd)
  calc
    sharp = 1 * sharp := by ring
    _ = (∑ d ∈ developments, weight d) * sharp := by rw [hsum]
    _ = ∑ d ∈ developments, weight d * sharp := by
      rw [Finset.sum_mul]
    _ ≤ ∑ d ∈ developments, weight d * (exterior + cutCost d) :=
      hweighted
    _ = exterior + expectedDevelopmentCost developments weight cutCost := by
      unfold expectedDevelopmentCost
      calc
        (∑ d ∈ developments, weight d * (exterior + cutCost d)) =
            ∑ d ∈ developments,
              (weight d * exterior + weight d * cutCost d) := by
          apply Finset.sum_congr rfl
          intro d hd
          ring
        _ = (∑ d ∈ developments, weight d * exterior) +
              ∑ d ∈ developments, weight d * cutCost d := by
          rw [Finset.sum_add_distrib]
        _ = (∑ d ∈ developments, weight d) * exterior +
              ∑ d ∈ developments, weight d * cutCost d := by
          rw [Finset.sum_mul]
        _ = exterior + ∑ d ∈ developments, weight d * cutCost d := by
          rw [hsum]
          ring

/-- Expected total cut cost equals the sum of expected interface jumps. -/
theorem expectedDevelopmentCost_eq_sum_expectedInterface
    {D I : Type*} (developments : Finset D) (interfaces : Finset I)
    (weight : D → ℝ) (jump : D → I → ℝ) :
    expectedDevelopmentCost developments weight
        (fun d => ∑ i ∈ interfaces, jump d i) =
      ∑ i ∈ interfaces,
        expectedInterfaceJump developments weight jump i := by
  unfold expectedDevelopmentCost expectedInterfaceJump
  calc
    (∑ d ∈ developments, weight d * (∑ i ∈ interfaces, jump d i)) =
        ∑ d ∈ developments, ∑ i ∈ interfaces, weight d * jump d i := by
      apply Finset.sum_congr rfl
      intro d hd
      rw [Finset.mul_sum]
    _ = ∑ i ∈ interfaces, ∑ d ∈ developments, weight d * jump d i := by
      rw [Finset.sum_comm]

/-- Aggregate expected-cut domination proves the sharp selector. -/
theorem averagedDevelopment_selector_aggregate
    {D I : Type*} (developments : Finset D) (interfaces : Finset I)
    (weight : D → ℝ) (jump : D → I → ℝ) (physical : I → ℝ)
    {sharp exterior : ℝ}
    (hweight : ∀ d ∈ developments, 0 ≤ weight d)
    (hsum : (∑ d ∈ developments, weight d) = 1)
    (hdevelopment : ∀ d ∈ developments,
      sharp ≤ exterior + ∑ i ∈ interfaces, jump d i)
    (haggregate :
      (∑ i ∈ interfaces,
        expectedInterfaceJump developments weight jump i) ≤
        ∑ i ∈ interfaces, physical i) :
    sharp ≤ exterior + ∑ i ∈ interfaces, physical i := by
  have haverage := averagedDevelopment_scalar_bound
    developments weight (fun d => ∑ i ∈ interfaces, jump d i)
    hweight hsum hdevelopment
  rw [expectedDevelopmentCost_eq_sum_expectedInterface
    developments interfaces weight jump] at haverage
  linarith

/-- Interfacewise expected-cut domination implies the aggregate selector condition. -/
theorem averagedDevelopment_selector_interfacewise
    {D I : Type*} (developments : Finset D) (interfaces : Finset I)
    (weight : D → ℝ) (jump : D → I → ℝ) (physical : I → ℝ)
    {sharp exterior : ℝ}
    (hweight : ∀ d ∈ developments, 0 ≤ weight d)
    (hsum : (∑ d ∈ developments, weight d) = 1)
    (hdevelopment : ∀ d ∈ developments,
      sharp ≤ exterior + ∑ i ∈ interfaces, jump d i)
    (hinterface : ∀ i ∈ interfaces,
      expectedInterfaceJump developments weight jump i ≤ physical i) :
    sharp ≤ exterior + ∑ i ∈ interfaces, physical i := by
  apply averagedDevelopment_selector_aggregate
    developments interfaces weight jump physical hweight hsum hdevelopment
  exact Finset.sum_le_sum hinterface

/--
Uniform `k`-cycle threshold: if every one of `k` interfaces pays at least `J/k`,
the total physical interface cost is at least one full developed cut `J`.
-/
theorem uniformCycle_totalPhysical_ge_jump
    {I : Type*} (interfaces : Finset I) (physical : I → ℝ)
    {k : ℕ} {J : ℝ}
    (hk : 0 < k)
    (hcard : interfaces.card = k)
    (hinterface : ∀ i ∈ interfaces, J / k ≤ physical i) :
    J ≤ ∑ i ∈ interfaces, physical i := by
  have hsum :
      (∑ i ∈ interfaces, J / k) ≤
        ∑ i ∈ interfaces, physical i :=
    Finset.sum_le_sum hinterface
  have hkR : (0 : ℝ) < k := by exact_mod_cast hk
  have hleft : (∑ i ∈ interfaces, J / k) = J := by
    simp [hcard, Nat.cast_ofNat]
    field_simp [ne_of_gt hkR]
  rw [hleft] at hsum
  exact hsum

/-- Fivefold uniform threshold in exact rational form. -/
theorem fivefold_uniform_threshold
    {I : Type*} (interfaces : Finset I) (physical : I → ℝ)
    {J : ℝ}
    (hcard : interfaces.card = 5)
    (hinterface : ∀ i ∈ interfaces, J / 5 ≤ physical i) :
    J ≤ ∑ i ∈ interfaces, physical i := by
  exact uniformCycle_totalPhysical_ge_jump interfaces physical
    (k := 5) (J := J) (by norm_num) hcard hinterface

/-- Averaging positive-part deficits before taking the positive part can only improve the bound. -/
theorem calibrationUnderpayment_expected_le_average
    {D : Type*} (developments : Finset D)
    (weight jump : D → ℝ) (physical : ℝ)
    (hweight : ∀ d ∈ developments, 0 ≤ weight d)
    (hsum : (∑ d ∈ developments, weight d) = 1) :
    calibrationUnderpayment
        (∑ d ∈ developments, weight d * jump d) physical ≤
      ∑ d ∈ developments,
        weight d * calibrationUnderpayment (jump d) physical := by
  let rhs : ℝ := ∑ d ∈ developments,
    weight d * calibrationUnderpayment (jump d) physical
  have hrhs : 0 ≤ rhs := by
    dsimp [rhs]
    exact Finset.sum_nonneg fun d hd =>
      mul_nonneg (hweight d hd) (calibrationUnderpayment_nonneg _ _)
  have hlinear :
      (∑ d ∈ developments, weight d * jump d) - physical ≤ rhs := by
    have hpoint :
        (∑ d ∈ developments, weight d * (jump d - physical)) ≤ rhs := by
      dsimp [rhs]
      exact Finset.sum_le_sum fun d hd =>
        mul_le_mul_of_nonneg_left
          (show jump d - physical ≤ calibrationUnderpayment (jump d) physical by
            exact le_max_right _ _)
          (hweight d hd)
    have hrewrite :
        (∑ d ∈ developments, weight d * (jump d - physical)) =
          (∑ d ∈ developments, weight d * jump d) - physical := by
      calc
        (∑ d ∈ developments, weight d * (jump d - physical)) =
            (∑ d ∈ developments, weight d * jump d) -
              (∑ d ∈ developments, weight d) * physical := by
          simp_rw [mul_sub]
          rw [Finset.sum_sub_distrib, Finset.sum_mul]
        _ = (∑ d ∈ developments, weight d * jump d) - physical := by
          rw [hsum]
          ring
    rw [hrewrite] at hpoint
    exact hpoint
  unfold calibrationUnderpayment
  exact max_le hrhs hlinear

end Erdos1084

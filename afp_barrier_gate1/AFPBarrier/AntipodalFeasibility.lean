import AFPBarrier.LocalSphericalFeasibility
import Mathlib.Tactic.Linarith

/-!
# Algebraic feasibility with antipodal neighbors

Antipodal neighbors have zero tangent increment and normal loss exactly two.
This module never assigns them a tangent direction and never divides by
`sin pi`.  Non-antipodal coefficients are parameterized by tangent weights;
antipodal coefficients receive the remaining scalar normal budget.
-/

open scoped BigOperators

namespace AFPBarrier

variable {ι κ ν : Type*} [Fintype ι] [Fintype κ] [Fintype ν]

def antipodalOnlyFeasible (a : ν → ℝ) : Prop :=
  (∀ k, 0 ≤ a k) ∧ 2 * Finset.univ.sum a = 2

theorem antipodalOnlyFeasible_iff_simplex (a : ν → ℝ) :
    antipodalOnlyFeasible a ↔
      (∀ k, 0 ≤ a k) ∧ Finset.univ.sum a = 1 := by
  constructor
  · rintro ⟨ha, hbudget⟩
    refine ⟨ha, ?_⟩
    linarith
  · rintro ⟨ha, hsum⟩
    refine ⟨ha, ?_⟩
    rw [hsum]
    norm_num

theorem antipodalOnlyFeasible_of_positive_simplex
    (p : ν → ℝ)
    (hp : ∀ k, 0 < p k)
    (hpsum : Finset.univ.sum p = 1) :
    antipodalOnlyFeasible p ∧ ∀ k, 0 < p k := by
  refine ⟨(antipodalOnlyFeasible_iff_simplex p).2 ?_, hp⟩
  exact ⟨fun k => le_of_lt (hp k), hpsum⟩

noncomputable def uniformAntipodalRate (k : ν) : ℝ :=
  1 / (Fintype.card ν : ℝ)

theorem uniformAntipodalRate_strictly_feasible [Nonempty ν] :
    antipodalOnlyFeasible (uniformAntipodalRate : ν → ℝ) ∧
      ∀ k, 0 < uniformAntipodalRate k := by
  have hcardNat : Fintype.card ν ≠ 0 := Fintype.card_ne_zero
  have hcardReal : (Fintype.card ν : ℝ) ≠ 0 := by
    exact_mod_cast hcardNat
  have hcardPos : (0 : ℝ) < Fintype.card ν := by
    exact_mod_cast Nat.pos_of_ne_zero hcardNat
  have hpos : ∀ k, 0 < uniformAntipodalRate k := by
    intro k
    exact div_pos zero_lt_one hcardPos
  apply antipodalOnlyFeasible_of_positive_simplex
      (uniformAntipodalRate : ν → ℝ) hpos
  simp [uniformAntipodalRate, nsmul_eq_mul, hcardReal]

def tangentNormalBudget (x halfTan : ι → ℝ) : ℝ :=
  Finset.univ.sum (fun j => x j * halfTan j)

def mixedNormalBudgetFeasible
    (x halfTan : ι → ℝ) (z : ν → ℝ) : Prop :=
  tangentNormalBudget x halfTan + 2 * Finset.univ.sum z = 2

noncomputable def rowRateFromTangentWeight
    (x sinTheta : ι → ℝ) (j : ι) : ℝ :=
  x j / sinTheta j

theorem rowRateFromTangentWeight_nonneg
    (x sinTheta : ι → ℝ)
    (hx : ∀ j, 0 ≤ x j)
    (hsin : ∀ j, 0 < sinTheta j) :
    ∀ j, 0 ≤ rowRateFromTangentWeight x sinTheta j := by
  intro j
  exact div_nonneg (hx j) (le_of_lt (hsin j))

theorem rowRateFromTangentWeight_pos
    (x sinTheta : ι → ℝ)
    (hx : ∀ j, 0 < x j)
    (hsin : ∀ j, 0 < sinTheta j) :
    ∀ j, 0 < rowRateFromTangentWeight x sinTheta j := by
  intro j
  exact div_pos (hx j) (hsin j)

theorem rowRateFromTangentWeight_balance
    (x sinTheta : ι → ℝ) (u : ι → κ → ℝ)
    (hsin : ∀ j, 0 < sinTheta j)
    (htangent : ∀ k,
      Finset.univ.sum (fun j => x j * u j k) = 0) :
    ∀ k,
      Finset.univ.sum
          (fun j => rowRateFromTangentWeight x sinTheta j
            * sinTheta j * u j k) = 0 := by
  intro k
  calc
    Finset.univ.sum
        (fun j => rowRateFromTangentWeight x sinTheta j
          * sinTheta j * u j k) =
        Finset.univ.sum (fun j => x j * u j k) := by
          apply Finset.sum_congr rfl
          intro j hj
          unfold rowRateFromTangentWeight
          field_simp [ne_of_gt (hsin j)]
    _ = 0 := htangent k

theorem rowRateFromTangentWeight_normal
    (x sinTheta halfTan : ι → ℝ)
    (hsin : ∀ j, 0 < sinTheta j) :
    Finset.univ.sum
        (fun j => rowRateFromTangentWeight x sinTheta j
          * (sinTheta j * halfTan j)) =
      tangentNormalBudget x halfTan := by
  unfold tangentNormalBudget
  apply Finset.sum_congr rfl
  intro j hj
  unfold rowRateFromTangentWeight
  field_simp [ne_of_gt (hsin j)]

/-- Converting the tangent weights induced by a non-antipodal row recovers
that row coefficientwise.  This inverse identity is stated only for the
non-antipodal index type, where `sinTheta` is strictly positive. -/
theorem rowRateFromTangentDependenceWeight
    (a sinTheta : ι → ℝ)
    (hsin : ∀ j, 0 < sinTheta j) :
    ∀ j, rowRateFromTangentWeight
      (tangentDependenceWeight a sinTheta) sinTheta j = a j := by
  intro j
  unfold rowRateFromTangentWeight tangentDependenceWeight
  field_simp [ne_of_gt (hsin j)]

theorem mixedRow_from_tangentBudget
    (x sinTheta halfTan : ι → ℝ) (z : ν → ℝ)
    (u : ι → κ → ℝ)
    (hx : ∀ j, 0 ≤ x j)
    (hz : ∀ k, 0 ≤ z k)
    (hsin : ∀ j, 0 < sinTheta j)
    (htangent : ∀ k,
      Finset.univ.sum (fun j => x j * u j k) = 0)
    (hbudget : mixedNormalBudgetFeasible x halfTan z) :
    (∀ j, 0 ≤ rowRateFromTangentWeight x sinTheta j) ∧
    (∀ k, 0 ≤ z k) ∧
    (∀ k,
      Finset.univ.sum
          (fun j => rowRateFromTangentWeight x sinTheta j
            * sinTheta j * u j k) = 0) ∧
    Finset.univ.sum
          (fun j => rowRateFromTangentWeight x sinTheta j
            * (sinTheta j * halfTan j)) +
        2 * Finset.univ.sum z = 2 := by
  refine ⟨rowRateFromTangentWeight_nonneg x sinTheta hx hsin,
    hz, rowRateFromTangentWeight_balance x sinTheta u hsin htangent, ?_⟩
  rw [rowRateFromTangentWeight_normal x sinTheta halfTan hsin]
  exact hbudget

theorem mixedRow_to_tangentBudget
    (a : ι → ℝ) (z : ν → ℝ)
    (sinTheta halfTan : ι → ℝ) (u : ι → κ → ℝ)
    (ha : ∀ j, 0 ≤ a j)
    (hz : ∀ k, 0 ≤ z k)
    (hsin : ∀ j, 0 ≤ sinTheta j)
    (htangent : ∀ k,
      Finset.univ.sum (fun j => a j * sinTheta j * u j k) = 0)
    (hnormal :
      Finset.univ.sum
          (fun j => a j * (sinTheta j * halfTan j)) +
        2 * Finset.univ.sum z = 2) :
    (∀ j, 0 ≤ tangentDependenceWeight a sinTheta j) ∧
    (∀ k,
      Finset.univ.sum
          (fun j => tangentDependenceWeight a sinTheta j * u j k) = 0) ∧
    mixedNormalBudgetFeasible
      (tangentDependenceWeight a sinTheta) halfTan z ∧
    (∀ k, 0 ≤ z k) := by
  refine ⟨tangentDependenceWeight_nonneg a sinTheta ha hsin,
    tangentDependenceWeight_balance a sinTheta u htangent, ?_, hz⟩
  unfold mixedNormalBudgetFeasible tangentNormalBudget tangentDependenceWeight
  convert hnormal using 1 <;> ring

/-- A physical mixed row induces a tangent normal expenditure in the exact
interval `[0,2]`. -/
theorem mixedRow_tangentNormalBudget_bounds
    (a : ι → ℝ) (z : ν → ℝ) (sinTheta halfTan : ι → ℝ)
    (ha : ∀ j, 0 ≤ a j)
    (hz : ∀ k, 0 ≤ z k)
    (hsin : ∀ j, 0 ≤ sinTheta j)
    (hhalfTan : ∀ j, 0 < halfTan j)
    (hnormal :
      Finset.univ.sum
          (fun j => a j * (sinTheta j * halfTan j)) +
        2 * Finset.univ.sum z = 2) :
    0 ≤ tangentNormalBudget
        (tangentDependenceWeight a sinTheta) halfTan ∧
      tangentNormalBudget
        (tangentDependenceWeight a sinTheta) halfTan ≤ 2 := by
  have hq : 0 ≤ tangentNormalBudget
      (tangentDependenceWeight a sinTheta) halfTan := by
    unfold tangentNormalBudget tangentDependenceWeight
    apply Finset.sum_nonneg
    intro j hj
    exact mul_nonneg (mul_nonneg (ha j) (hsin j)) (le_of_lt (hhalfTan j))
  have hzsum : 0 ≤ Finset.univ.sum z :=
    Finset.sum_nonneg (fun k hk => hz k)
  have heq :
      tangentNormalBudget
          (tangentDependenceWeight a sinTheta) halfTan +
        2 * Finset.univ.sum z = 2 := by
    unfold tangentNormalBudget tangentDependenceWeight
    convert hnormal using 1 <;> ring
  constructor
  · exact hq
  · linarith

theorem mixedNormalBudgetFeasible_iff_remaining
    (x halfTan : ι → ℝ) (z : ν → ℝ) :
    mixedNormalBudgetFeasible x halfTan z ↔
      Finset.univ.sum z = 1 - tangentNormalBudget x halfTan / 2 := by
  unfold mixedNormalBudgetFeasible
  constructor <;> intro h <;> linarith

noncomputable def scaledAntipodalAllocation
    (q : ℝ) (p : ν → ℝ) (k : ν) : ℝ :=
  (1 - q / 2) * p k

theorem scaledAntipodalAllocation_sum
    (q : ℝ) (p : ν → ℝ)
    (hpsum : Finset.univ.sum p = 1) :
    Finset.univ.sum (scaledAntipodalAllocation q p) = 1 - q / 2 := by
  unfold scaledAntipodalAllocation
  rw [← Finset.mul_sum, hpsum, mul_one]

theorem scaledAntipodalAllocation_nonneg
    (q : ℝ) (p : ν → ℝ)
    (hq : q ≤ 2)
    (hp : ∀ k, 0 ≤ p k) :
    ∀ k, 0 ≤ scaledAntipodalAllocation q p k := by
  intro k
  unfold scaledAntipodalAllocation
  exact mul_nonneg (by linarith) (hp k)

theorem scaledAntipodalAllocation_pos
    (q : ℝ) (p : ν → ℝ)
    (hq : q < 2)
    (hp : ∀ k, 0 < p k) :
    ∀ k, 0 < scaledAntipodalAllocation q p k := by
  intro k
  unfold scaledAntipodalAllocation
  exact mul_pos (by linarith) (hp k)

theorem mixedNormalBudgetFeasible_scaledAntipodalAllocation
    (x halfTan : ι → ℝ) (p : ν → ℝ)
    (hbudget : tangentNormalBudget x halfTan ≤ 2)
    (hp : ∀ k, 0 ≤ p k)
    (hpsum : Finset.univ.sum p = 1) :
    mixedNormalBudgetFeasible x halfTan
      (scaledAntipodalAllocation (tangentNormalBudget x halfTan) p) ∧
    (∀ k, 0 ≤
      scaledAntipodalAllocation (tangentNormalBudget x halfTan) p k) := by
  refine ⟨(mixedNormalBudgetFeasible_iff_remaining x halfTan _).2 ?_, ?_⟩
  · exact scaledAntipodalAllocation_sum
      (tangentNormalBudget x halfTan) p hpsum
  · exact scaledAntipodalAllocation_nonneg
      (tangentNormalBudget x halfTan) p hbudget hp

theorem mixedNormalBudgetFeasible_zero_tangent
    (halfTan : ι → ℝ) (p : ν → ℝ)
    (hpsum : Finset.univ.sum p = 1) :
    mixedNormalBudgetFeasible (fun _ => 0) halfTan p := by
  unfold mixedNormalBudgetFeasible tangentNormalBudget
  simp [hpsum]

theorem mixedNormalBudgetFeasible_zero_tangent_uniform
    [Nonempty ν] (halfTan : ι → ℝ) :
    mixedNormalBudgetFeasible (fun _ => 0) halfTan
        (uniformAntipodalRate : ν → ℝ) ∧
      ∀ k, 0 < uniformAntipodalRate k := by
  have hu := (uniformAntipodalRate_strictly_feasible (ν := ν))
  refine ⟨mixedNormalBudgetFeasible_zero_tangent halfTan
    (uniformAntipodalRate : ν → ℝ) ?_, hu.2⟩
  exact ((antipodalOnlyFeasible_iff_simplex
    (uniformAntipodalRate : ν → ℝ)).1 hu.1).2

end AFPBarrier

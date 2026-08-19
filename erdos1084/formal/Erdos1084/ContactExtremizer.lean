import Mathlib
import Mathlib.Combinatorics.SimpleGraph.Finite
import Erdos1084.FiniteSpherePacking

namespace Erdos1084

/-!
# Existence of a finite contact-count extremizer

The contact count is integer-valued and bounded by `n.choose 2`. This module defines `f₃(n)` as
the greatest attainable contact count and proves that it is attained. No compactness theorem is
needed for this existence statement.
-/

noncomputable section

/-- The first standard unit vector in Euclidean three-space. -/
def phase1Axis : Point3 := !₂[1, 0, 0]

@[simp] theorem phase1Axis_norm : ‖phase1Axis‖ = 1 := by
  rw [EuclideanSpace.norm_eq]
  norm_num [phase1Axis, Fin.sum_univ_succ]

/-- A point on the first coordinate axis of Euclidean three-space. -/
def phase1LinePoint (t : ℝ) : Point3 := t • phase1Axis

/-- Distance on the embedded coordinate line is ordinary absolute distance. -/
theorem phase1LinePoint_dist (a b : ℝ) :
    dist (phase1LinePoint a) (phase1LinePoint b) = |a - b| := by
  rw [dist_eq_norm_sub]
  change ‖a • phase1Axis - b • phase1Axis‖ = |a - b|
  rw [← sub_smul, norm_smul, phase1Axis_norm]
  simp

/-- A canonical widely separated `n`-point configuration. -/
def phase1SeparatedLineConfiguration (n : ℕ) : UnitSeparatedConfiguration (Fin n) where
  point i := phase1LinePoint (3 * (i.1 : ℝ))
  separated := by
    intro i j hij
    rw [phase1LinePoint_dist]
    have hval : i.1 ≠ j.1 := by
      intro h
      exact hij (Fin.ext h)
    rcases Nat.lt_or_gt_of_ne hval with hlt | hgt
    · have hstep : i.1 + 1 ≤ j.1 := Nat.succ_le_iff.mpr hlt
      have hstepR : (i.1 : ℝ) + 1 ≤ (j.1 : ℝ) := by exact_mod_cast hstep
      have hnonpos : 3 * (i.1 : ℝ) - 3 * (j.1 : ℝ) ≤ 0 := by linarith
      rw [abs_of_nonpos hnonpos]
      linarith
    · have hstep : j.1 + 1 ≤ i.1 := Nat.succ_le_iff.mpr hgt
      have hstepR : (j.1 : ℝ) + 1 ≤ (i.1 : ℝ) := by exact_mod_cast hstep
      have hnonneg : 0 ≤ 3 * (i.1 : ℝ) - 3 * (j.1 : ℝ) := by linarith
      rw [abs_of_nonneg hnonneg]
      linarith

/-- `k` is attained as the contact count of an admissible `n`-point configuration. -/
def AttainableContactCount (n k : ℕ) : Prop :=
  ∃ X : UnitSeparatedConfiguration (Fin n), X.contactCount = k

/-- Every attainable contact count is bounded by the number of unordered pairs. -/
theorem attainableContactCount_le_choose
    {n k : ℕ} (h : AttainableContactCount n k) :
    k ≤ n.choose 2 := by
  classical
  rcases h with ⟨X, rfl⟩
  exact X.contactGraph.card_edgeFinset_le_card_choose_two

/-- The set of attainable contact counts is nonempty. -/
theorem attainableContactCount_nonempty (n : ℕ) :
    ∃ k, AttainableContactCount n k := by
  exact ⟨(phase1SeparatedLineConfiguration n).contactCount,
    phase1SeparatedLineConfiguration n, rfl⟩

/-- The maximum three-dimensional contact number. -/
noncomputable def f3 (n : ℕ) : ℕ := by
  classical
  exact Nat.findGreatest (AttainableContactCount n) (n.choose 2)

/-- The defining upper bound for `f3`. -/
theorem f3_le_choose (n : ℕ) : f3 n ≤ n.choose 2 := by
  classical
  unfold f3
  exact Nat.findGreatest_le _

/-- Every attainable contact count is at most `f3 n`. -/
theorem attainableContactCount_le_f3
    {n k : ℕ} (h : AttainableContactCount n k) :
    k ≤ f3 n := by
  classical
  unfold f3
  exact Nat.le_findGreatest (attainableContactCount_le_choose h) h

/-- The maximum contact count is attained by an actual finite configuration. -/
theorem exists_contact_extremizer (n : ℕ) :
    ∃ X : UnitSeparatedConfiguration (Fin n), X.contactCount = f3 n := by
  classical
  rcases attainableContactCount_nonempty n with ⟨k, hk⟩
  have hkbound := attainableContactCount_le_choose hk
  have hspec : AttainableContactCount n (f3 n) := by
    unfold f3
    exact Nat.findGreatest_spec hkbound hk
  exact hspec

/-- A selected contact-maximizing configuration. -/
def contactExtremizer (n : ℕ) : UnitSeparatedConfiguration (Fin n) :=
  Classical.choose (exists_contact_extremizer n)

@[simp] theorem contactExtremizer_contactCount (n : ℕ) :
    (contactExtremizer n).contactCount = f3 n :=
  Classical.choose_spec (exists_contact_extremizer n)

end

end Erdos1084

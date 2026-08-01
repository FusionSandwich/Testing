import AFPBarrier.DualCertificate
import Mathlib.Tactic

/-!
# Duality gaps and complementary slackness

`DualCertificate.lean` proves finite transpose identities, Farkas-certificate
soundness, and weak LP duality. This module records the exact finite duality
gap decomposition and the resulting componentwise complementary-slackness
consequences used by the shared-edge spherical specialization.
-/

open scoped BigOperators

namespace AFPBarrier

variable {ρ κ : Type*} [Fintype ρ] [Fintype κ]

/-- A finite sum of nonnegative real terms can vanish only termwise. -/
theorem finite_sum_nonneg_eq_zero_termwise
    (f : κ → ℝ)
    (hf : ∀ q, 0 ≤ f q)
    (hsum : Finset.univ.sum f = 0) :
    ∀ q, f q = 0 := by
  classical
  intro q
  have hle : f q ≤ Finset.univ.sum f := by
    exact Finset.single_le_sum (fun j hj => hf j) (Finset.mem_univ q)
  rw [hsum] at hle
  exact le_antisymm hle (hf q)

/-- Exact duality-gap identity for

`min c · x` subject to `A x = b`, `x ≥ 0`

and a dual vector `y`. -/
theorem positiveLP_gap_eq_weighted_slack_sum
    (A : ρ → κ → ℝ) (b y : ρ → ℝ) (c x : κ → ℝ)
    (hAx : ∀ r, finiteMatrixApply A x r = b r) :
    finiteDot c x - finiteDot b y =
      Finset.univ.sum
        (fun q => x q * (c q - finiteTransposeApply A y q)) := by
  have hpair :
      finiteDot b y = finiteDot x (finiteTransposeApply A y) := by
    calc
      finiteDot b y = finiteDot (finiteMatrixApply A x) y := by
        unfold finiteDot
        apply Finset.sum_congr rfl
        intro r hr
        rw [hAx r]
      _ = finiteDot x (finiteTransposeApply A y) :=
        finiteMatrix_bilinear_identity A x y
  rw [hpair]
  unfold finiteDot
  rw [← Finset.sum_sub_distrib]
  apply Finset.sum_congr rfl
  intro q hq
  ring

/-- Zero primal-dual gap plus primal and dual feasibility gives every
complementary-slackness product separately. -/
theorem positiveLP_complementary_slackness
    (A : ρ → κ → ℝ) (b y : ρ → ℝ) (c x : κ → ℝ)
    (hx : ∀ q, 0 ≤ x q)
    (hAx : ∀ r, finiteMatrixApply A x r = b r)
    (hdual : ∀ q, finiteTransposeApply A y q ≤ c q)
    (hzeroGap : finiteDot c x = finiteDot b y) :
    ∀ q, x q * (c q - finiteTransposeApply A y q) = 0 := by
  have hsum :
      Finset.univ.sum
          (fun q => x q * (c q - finiteTransposeApply A y q)) = 0 := by
    have hgap := positiveLP_gap_eq_weighted_slack_sum
      (A := A) (b := b) (y := y) (c := c) (x := x) hAx
    rw [hzeroGap, sub_self] at hgap
    exact hgap.symm
  apply finite_sum_nonneg_eq_zero_termwise
  · intro q
    exact mul_nonneg (hx q) (sub_nonneg.mpr (hdual q))
  · exact hsum

/-- If a Farkas-dual vector has nonnegative edge work and zero total work
against a strictly positive primal solution, it annihilates every column.
This is the formal finite core of the dual-face strict-feasibility criterion. -/
theorem strict_solution_zero_dualWork_forces_column_annihilation
    (A : ρ → κ → ℝ) (b y : ρ → ℝ) (x : κ → ℝ)
    (hx : ∀ q, 0 < x q)
    (hAx : ∀ r, finiteMatrixApply A x r = b r)
    (hdual : ∀ q, 0 ≤ finiteTransposeApply A y q)
    (hwork : finiteDot b y = 0) :
    ∀ q, finiteTransposeApply A y q = 0 := by
  have hpair : finiteDot x (finiteTransposeApply A y) = 0 := by
    rw [← finiteMatrix_bilinear_identity A x y]
    unfold finiteDot
    calc
      Finset.univ.sum
          (fun r => finiteMatrixApply A x r * y r) =
          Finset.univ.sum (fun r => b r * y r) := by
            apply Finset.sum_congr rfl
            intro r hr
            rw [hAx r]
      _ = 0 := by simpa [finiteDot] using hwork
  have hproducts :
      ∀ q, x q * finiteTransposeApply A y q = 0 := by
    apply finite_sum_nonneg_eq_zero_termwise
    · intro q
      exact mul_nonneg (le_of_lt (hx q)) (hdual q)
    · exact hpair
  intro q
  exact (mul_eq_zero.mp (hproducts q)).resolve_left (ne_of_gt (hx q))

end AFPBarrier

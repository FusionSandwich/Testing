import AFPBarrier.DualCertificate
import Mathlib.Algebra.Order.BigOperators.Ring.Finset
import Mathlib.Tactic

/-!
# Shared-edge dual geometry and complementary slackness

The full finite-dimensional Farkas alternative and strong linear-programming
duality are invoked with precise hypotheses in the ordinary theorem document.
This module formalizes their AFP-specific finite consequences: the shared-edge
dual block, its geometric sign convention, the exact primal-dual objective gap,
and componentwise complementary slackness.
-/

open scoped BigOperators

namespace AFPBarrier

variable {ι ε κ ρ : Type*}
variable [Fintype κ] [Fintype ρ] [Fintype ε]

/-- Transpose block for one undirected edge `e={p e,q e}`.  It is independent
of which endpoint is listed first. -/
def sharedEdgeDualWork
    (p q : ε → ι) (Ω y : ι → κ → ℝ) (e : ε) : ℝ :=
  Finset.univ.sum (fun k =>
    (y (p e) k - y (q e) k) * (Ω (q e) k - Ω (p e) k))

/-- Reversing the arbitrary orientation of an undirected edge leaves its dual
block unchanged. -/
theorem sharedEdgeDualWork_swap
    (p q : ε → ι) (Ω y : ι → κ → ℝ) (e : ε) :
    sharedEdgeDualWork q p Ω y e = sharedEdgeDualWork p q Ω y e := by
  unfold sharedEdgeDualWork
  apply Finset.sum_congr rfl
  intro k hk
  ring

/-- A constant nodal displacement has zero work on every shared edge. -/
@[simp] theorem sharedEdgeDualWork_constant
    (p q : ε → ι) (Ω : ι → κ → ℝ) (v : κ → ℝ) (e : ε) :
    sharedEdgeDualWork p q Ω (fun _ => v) e = 0 := by
  simp [sharedEdgeDualWork]

/-- For the radial displacement `y_i=-c Ω_i`, the transpose block is `c`
times the squared chord length.  This fixes the sign convention used by the
LP dual throughout the stage report. -/
theorem sharedEdgeDualWork_radial
    (p q : ε → ι) (Ω : ι → κ → ℝ) (c : ℝ) (e : ε) :
    sharedEdgeDualWork p q Ω (fun i k => -c * Ω i k) e
      = c * Finset.univ.sum (fun k => (Ω (q e) k - Ω (p e) k) ^ 2) := by
  unfold sharedEdgeDualWork
  calc
    Finset.univ.sum (fun k =>
        ((-c * Ω (p e) k) - (-c * Ω (q e) k)) *
          (Ω (q e) k - Ω (p e) k))
      = Finset.univ.sum (fun k =>
          c * (Ω (q e) k - Ω (p e) k) ^ 2) := by
            apply Finset.sum_congr rfl
            intro k hk
            ring
    _ = c * Finset.univ.sum
          (fun k => (Ω (q e) k - Ω (p e) k) ^ 2) := by
            rw [Finset.mul_sum]

/-- Nonnegative radial coefficient gives a nonnegative shared-edge dual block. -/
theorem sharedEdgeDualWork_radial_nonneg
    (p q : ε → ι) (Ω : ι → κ → ℝ) (c : ℝ) (e : ε)
    (hc : 0 ≤ c) :
    0 ≤ sharedEdgeDualWork p q Ω (fun i k => -c * Ω i k) e := by
  rw [sharedEdgeDualWork_radial]
  exact mul_nonneg hc (Finset.sum_nonneg (fun k hk => sq_nonneg _))

variable {σ : Type*} [Fintype σ]

/-- Slack of the dual inequality `Aᵀ y ≤ c`. -/
def positiveLPDualSlack
    (A : ρ → σ → ℝ) (c : σ → ℝ) (y : ρ → ℝ) (q : σ) : ℝ :=
  c q - finiteTransposeApply A y q

/-- Dual feasibility is exactly nonnegativity of every dual slack. -/
theorem positiveLPDualSlack_nonneg
    (A : ρ → σ → ℝ) (c : σ → ℝ) (y : ρ → ℝ)
    (hdual : ∀ q, finiteTransposeApply A y q ≤ c q) :
    ∀ q, 0 ≤ positiveLPDualSlack A c y q := by
  intro q
  exact sub_nonneg.mpr (hdual q)

/-- Exact objective-gap identity for the equality-constrained positive LP. -/
theorem positiveLP_objectiveGap_eq_slackPairing
    (A : ρ → σ → ℝ) (b y : ρ → ℝ) (c x : σ → ℝ)
    (hAx : ∀ r, finiteMatrixApply A x r = b r) :
    finiteDot c x - finiteDot b y
      = finiteDot x (positiveLPDualSlack A c y) := by
  have hdot :
      finiteDot b y = finiteDot (finiteMatrixApply A x) y := by
    unfold finiteDot
    apply Finset.sum_congr rfl
    intro r hr
    rw [hAx r]
  calc
    finiteDot c x - finiteDot b y
      = finiteDot c x - finiteDot (finiteMatrixApply A x) y := by rw [hdot]
    _ = finiteDot c x - finiteDot x (finiteTransposeApply A y) := by
          rw [finiteMatrix_bilinear_identity A x y]
    _ = finiteDot x (positiveLPDualSlack A c y) := by
          unfold finiteDot positiveLPDualSlack
          rw [← Finset.sum_sub_distrib]
          apply Finset.sum_congr rfl
          intro q hq
          ring

/-- Equality of primal and dual objectives forces the sum of nonnegative
complementarity products to vanish. -/
theorem positiveLP_complementaritySum_eq_zero
    (A : ρ → σ → ℝ) (b y : ρ → ℝ) (c x : σ → ℝ)
    (hAx : ∀ r, finiteMatrixApply A x r = b r)
    (hobjective : finiteDot c x = finiteDot b y) :
    finiteDot x (positiveLPDualSlack A c y) = 0 := by
  calc
    finiteDot x (positiveLPDualSlack A c y)
      = finiteDot c x - finiteDot b y :=
        (positiveLP_objectiveGap_eq_slackPairing A b y c x hAx).symm
    _ = 0 := by rw [hobjective]; ring

/-- Componentwise complementary slackness follows from primal nonnegativity,
dual feasibility, and equality of objective values. -/
theorem positiveLP_complementarySlackness
    (A : ρ → σ → ℝ) (b y : ρ → ℝ) (c x : σ → ℝ)
    (hx : ∀ q, 0 ≤ x q)
    (hAx : ∀ r, finiteMatrixApply A x r = b r)
    (hdual : ∀ q, finiteTransposeApply A y q ≤ c q)
    (hobjective : finiteDot c x = finiteDot b y) :
    ∀ q, x q * positiveLPDualSlack A c y q = 0 := by
  have hsum := positiveLP_complementaritySum_eq_zero
    (A := A) (b := b) (y := y) (c := c) (x := x) hAx hobjective
  unfold finiteDot at hsum
  have hall :
      ∀ q, x q * positiveLPDualSlack A c y q = 0 :=
    (Fintype.sum_eq_zero_iff_of_nonneg
      (fun q => mul_nonneg (hx q)
        (positiveLPDualSlack_nonneg A c y hdual q))).1 hsum
  exact hall

/-- Every edge carrying positive primal conductance saturates its dual edge
constraint. -/
theorem positiveLP_active_forces_dualSaturation
    (A : ρ → σ → ℝ) (b y : ρ → ℝ) (c x : σ → ℝ)
    (hx : ∀ q, 0 ≤ x q)
    (hAx : ∀ r, finiteMatrixApply A x r = b r)
    (hdual : ∀ q, finiteTransposeApply A y q ≤ c q)
    (hobjective : finiteDot c x = finiteDot b y)
    (q : σ) (hxq : 0 < x q) :
    finiteTransposeApply A y q = c q := by
  have hcomp := positiveLP_complementarySlackness
    (A := A) (b := b) (y := y) (c := c) (x := x)
    hx hAx hdual hobjective q
  have hslack : positiveLPDualSlack A c y q = 0 :=
    (mul_eq_zero.mp hcomp).resolve_left (ne_of_gt hxq)
  exact (sub_eq_zero.mp hslack).symm

/-- A strictly slack dual edge constraint forces zero primal conductance on
that edge. -/
theorem positiveLP_strictDualSlack_forces_inactive
    (A : ρ → σ → ℝ) (b y : ρ → ℝ) (c x : σ → ℝ)
    (hx : ∀ q, 0 ≤ x q)
    (hAx : ∀ r, finiteMatrixApply A x r = b r)
    (hdual : ∀ q, finiteTransposeApply A y q ≤ c q)
    (hobjective : finiteDot c x = finiteDot b y)
    (q : σ) (hstrict : finiteTransposeApply A y q < c q) :
    x q = 0 := by
  have hcomp := positiveLP_complementarySlackness
    (A := A) (b := b) (y := y) (c := c) (x := x)
    hx hAx hdual hobjective q
  have hslack : 0 < positiveLPDualSlack A c y q := by
    exact sub_pos.mpr hstrict
  exact (mul_eq_zero.mp hcomp).resolve_right (ne_of_gt hslack)

end AFPBarrier

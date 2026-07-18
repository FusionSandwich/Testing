import Mathlib.Algebra.Order.BigOperators.Ring.Finset
import Mathlib.Tactic

/-!
# Dual certificates for positive shared-edge systems

This module formalizes the finite-dimensional weak-duality argument underlying
Farkas certificates. In the AFP application, columns index undirected edges,
rows index node-coordinate balance equations, primal variables are the
nonnegative conductances, and dual variables are nodal displacement vectors.
-/

open scoped BigOperators

namespace AFPBarrier

variable {ρ κ : Type*} [Fintype ρ] [Fintype κ]

/-- Finite Euclidean pairing. -/
def finiteDot (x y : ρ → ℝ) : ℝ :=
  Finset.univ.sum (fun r => x r * y r)

/-- Action of a finite matrix on a column vector. -/
def finiteMatrixApply (A : ρ → κ → ℝ) (x : κ → ℝ) (r : ρ) : ℝ :=
  Finset.univ.sum (fun c => A r c * x c)

/-- Action of the transpose matrix. -/
def finiteTransposeApply (A : ρ → κ → ℝ) (y : ρ → ℝ) (c : κ) : ℝ :=
  Finset.univ.sum (fun r => A r c * y r)

/-- Finite bilinear transpose identity. -/
theorem finiteMatrix_bilinear_identity
    (A : ρ → κ → ℝ) (x : κ → ℝ) (y : ρ → ℝ) :
    finiteDot (finiteMatrixApply A x) y
      = finiteDot x (finiteTransposeApply A y) := by
  classical
  unfold finiteDot finiteMatrixApply finiteTransposeApply
  calc
    Finset.univ.sum
        (fun r => (Finset.univ.sum (fun c => A r c * x c)) * y r)
        = Finset.univ.sum
            (fun r => Finset.univ.sum
              (fun c => x c * (A r c * y r))) := by
                apply Finset.sum_congr rfl
                intro r hr
                rw [Finset.sum_mul]
                apply Finset.sum_congr rfl
                intro c hc
                ring
    _ = Finset.univ.sum
          (fun c => Finset.univ.sum
            (fun r => x c * (A r c * y r))) := by
              rw [Finset.sum_comm]
    _ = Finset.univ.sum
          (fun c => x c * Finset.univ.sum (fun r => A r c * y r)) := by
              apply Finset.sum_congr rfl
              intro c hc
              rw [Finset.mul_sum]

/-- Soundness of a Farkas-type infeasibility certificate: if `A x = b` has a
nonnegative solution and `Aᵀ y` is nonnegative, then `b · y` cannot be
negative. -/
theorem nonnegative_solution_forces_dualWork_nonneg
    (A : ρ → κ → ℝ) (b y : ρ → ℝ) (x : κ → ℝ)
    (hx : ∀ c, 0 ≤ x c)
    (hAx : ∀ r, finiteMatrixApply A x r = b r)
    (hdual : ∀ c, 0 ≤ finiteTransposeApply A y c) :
    0 ≤ finiteDot b y := by
  calc
    finiteDot b y = finiteDot (finiteMatrixApply A x) y := by
      unfold finiteDot
      apply Finset.sum_congr rfl
      intro r hr
      rw [hAx r]
    _ = finiteDot x (finiteTransposeApply A y) :=
      finiteMatrix_bilinear_identity A x y
    _ ≥ 0 := by
      unfold finiteDot
      apply Finset.sum_nonneg
      intro c hc
      exact mul_nonneg (hx c) (hdual c)

/-- A negative dual work value certifies that no nonnegative solution exists. -/
theorem negative_dualWork_certifies_infeasible
    (A : ρ → κ → ℝ) (b y : ρ → ℝ)
    (hdual : ∀ c, 0 ≤ finiteTransposeApply A y c)
    (hwork : finiteDot b y < 0) :
    ¬ ∃ x : κ → ℝ,
      (∀ c, 0 ≤ x c) ∧
      (∀ r, finiteMatrixApply A x r = b r) := by
  rintro ⟨x, hx, hAx⟩
  have hnonneg := nonnegative_solution_forces_dualWork_nonneg
    (A := A) (b := b) (y := y) (x := x) hx hAx hdual
  linarith

/-- Weak duality for the positive equality-constrained linear program

  minimize `c · x` subject to `A x = b`, `x ≥ 0`,

with dual constraint `Aᵀ y ≤ c`. -/
theorem positiveLP_weak_duality
    (A : ρ → κ → ℝ) (b y : ρ → ℝ) (c x : κ → ℝ)
    (hx : ∀ q, 0 ≤ x q)
    (hAx : ∀ r, finiteMatrixApply A x r = b r)
    (hdual : ∀ q, finiteTransposeApply A y q ≤ c q) :
    finiteDot b y ≤ finiteDot c x := by
  calc
    finiteDot b y = finiteDot (finiteMatrixApply A x) y := by
      unfold finiteDot
      apply Finset.sum_congr rfl
      intro r hr
      rw [hAx r]
    _ = finiteDot x (finiteTransposeApply A y) :=
      finiteMatrix_bilinear_identity A x y
    _ ≤ finiteDot c x := by
      unfold finiteDot
      apply Finset.sum_le_sum
      intro q hq
      have hmul := mul_le_mul_of_nonneg_left (hdual q) (hx q)
      nlinarith

end AFPBarrier

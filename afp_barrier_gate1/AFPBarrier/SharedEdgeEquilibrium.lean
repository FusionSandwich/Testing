import AFPBarrier.DualCertificate
import Mathlib.LinearAlgebra.Matrix.Notation
import Mathlib.Tactic.FinCases
import Mathlib.Tactic.NormNum

/-!
# Finite shared-edge equilibrium algebra

This module records the coordinate matrix used by the global reversible
problem.  Each undirected edge has two equal-and-opposite node blocks.  The
resulting cancellation proves the weighted-centering obstruction without any
geometric genericity assumption.  The final section gives an exact four-cycle
whose local rows are positive but whose shared-edge system has a rational
Farkas certificate.
-/

open scoped BigOperators Matrix

namespace AFPBarrier

variable {ι κ ε : Type*}
  [Fintype ι] [DecidableEq ι] [Fintype κ] [Fintype ε]

/-- Coordinate column of an undirected edge.  The two endpoint blocks are
equal and opposite, so this definition is independent of a later choice of
conductance orientation.  The formula also cancels for a loop. -/
def sharedEdgeColumn
    (Ω : ι → κ → ℝ) (left right : ε → ι)
    (i : ι) (k : κ) (e : ε) : ℝ :=
  (if i = left e then Ω (right e) k - Ω (left e) k else 0) +
  (if i = right e then Ω (left e) k - Ω (right e) k else 0)

/-- Swapping the names of the two endpoints does not change an undirected
edge column. -/
theorem sharedEdgeColumn_swap
    (Ω : ι → κ → ℝ) (left right : ε → ι)
    (i : ι) (k : κ) (e : ε) :
    sharedEdgeColumn Ω left right i k e =
      sharedEdgeColumn Ω right left i k e := by
  unfold sharedEdgeColumn
  rw [add_comm]

/-- Every edge-equilibrium column has zero node sum, coordinate by
coordinate. -/
theorem sharedEdgeColumn_nodeSum_zero
    (Ω : ι → κ → ℝ) (left right : ε → ι) (k : κ) (e : ε) :
    Finset.univ.sum (fun i => sharedEdgeColumn Ω left right i k e) = 0 := by
  classical
  by_cases h : left e = right e
  · simp [sharedEdgeColumn, h]
  · simp [sharedEdgeColumn, Finset.sum_add_distrib, h]

/-- Application of the finite shared-edge equilibrium matrix to one
conductance per edge. -/
def sharedEdgeApply
    (Ω : ι → κ → ℝ) (left right : ε → ι) (γ : ε → ℝ)
    (i : ι) (k : κ) : ℝ :=
  Finset.univ.sum (fun e => sharedEdgeColumn Ω left right i k e * γ e)

/-- Shared-edge forces cancel after summing over all nodes. -/
theorem sharedEdgeApply_nodeSum_zero
    (Ω : ι → κ → ℝ) (left right : ε → ι) (γ : ε → ℝ) (k : κ) :
    Finset.univ.sum (fun i => sharedEdgeApply Ω left right γ i k) = 0 := by
  classical
  unfold sharedEdgeApply
  rw [Finset.sum_comm]
  apply Finset.sum_eq_zero
  intro e he
  rw [← Finset.sum_mul]
  simp [sharedEdgeColumn_nodeSum_zero]

/-- Any right-hand side represented by shared-edge columns is node-centered. -/
theorem sharedEdge_equilibrium_implies_rhs_nodeSum_zero
    (Ω : ι → κ → ℝ) (left right : ε → ι) (γ : ε → ℝ)
    (b : ι → κ → ℝ)
    (heq : ∀ i k, sharedEdgeApply Ω left right γ i k = b i k)
    (k : κ) :
    Finset.univ.sum (fun i => b i k) = 0 := by
  calc
    Finset.univ.sum (fun i => b i k) =
        Finset.univ.sum (fun i => sharedEdgeApply Ω left right γ i k) := by
          apply Finset.sum_congr rfl
          intro i hi
          exact (heq i k).symm
    _ = 0 := sharedEdgeApply_nodeSum_zero Ω left right γ k

/-- For the spherical target `b_i = -2 w_i Ω_i`, shared-edge feasibility
forces exact weighted centering in every Cartesian coordinate. -/
theorem sharedEdge_equilibrium_implies_weightedCentering
    (Ω : ι → κ → ℝ) (left right : ε → ι) (γ : ε → ℝ)
    (w : ι → ℝ)
    (heq : ∀ i k,
      sharedEdgeApply Ω left right γ i k = -2 * w i * Ω i k)
    (k : κ) :
    Finset.univ.sum (fun i => w i * Ω i k) = 0 := by
  have hb : Finset.univ.sum (fun i => -2 * w i * Ω i k) = 0 :=
    sharedEdge_equilibrium_implies_rhs_nodeSum_zero
      Ω left right γ (fun i k => -2 * w i * Ω i k) heq k
  have hfactor :
      Finset.univ.sum (fun i => -2 * w i * Ω i k) =
        -2 * Finset.univ.sum (fun i => w i * Ω i k) := by
    rw [Finset.mul_sum]
    apply Finset.sum_congr rfl
    intro i hi
    ring
  rw [hfactor] at hb
  linarith

/-! ## Exact centered four-cycle obstruction -/

/-- Equatorial square nodes, ordered east, north, west, south. -/
def squareOmega : Fin 4 → Fin 2 → ℝ :=
  ![![1, 0], ![0, 1], ![-1, 0], ![0, -1]]

/-- Alternating positive masses. -/
def squareWeight : Fin 4 → ℝ := ![1, 2, 1, 2]

/-- Positive local row on the two cycle neighbours of every square node. -/
def squareLocalRate : Fin 4 → Fin 4 → ℝ :=
  ![![0, 1, 0, 1],
    ![1, 0, 1, 0],
    ![0, 1, 0, 1],
    ![1, 0, 1, 0]]

theorem squareLocalRate_nonneg (i j : Fin 4) :
    0 ≤ squareLocalRate i j := by
  fin_cases i <;> fin_cases j <;> norm_num [squareLocalRate]

/-- All eight oriented incidences of the permitted four-cycle are strictly
positive. -/
theorem squareLocalRate_permitted_pos :
    0 < squareLocalRate 0 1 ∧ 0 < squareLocalRate 1 0 ∧
    0 < squareLocalRate 1 2 ∧ 0 < squareLocalRate 2 1 ∧
    0 < squareLocalRate 2 3 ∧ 0 < squareLocalRate 3 2 ∧
    0 < squareLocalRate 3 0 ∧ 0 < squareLocalRate 0 3 := by
  change 0 < (1 : ℝ) ∧ 0 < 1 ∧ 0 < 1 ∧ 0 < 1 ∧
    0 < 1 ∧ 0 < 1 ∧ 0 < 1 ∧ 0 < 1
  norm_num [squareLocalRate]

/-- Every square node has an exact positive degree-one row on its two
permitted cycle edges. -/
theorem squareLocalRate_coordinate_exact (i : Fin 4) (k : Fin 2) :
    Finset.univ.sum
        (fun j => squareLocalRate i j * (squareOmega j k - squareOmega i k))
      = -2 * squareOmega i k := by
  fin_cases i <;> fin_cases k <;>
    norm_num [squareLocalRate, squareOmega, Fin.sum_univ_succ]

theorem squareWeight_pos (i : Fin 4) : 0 < squareWeight i := by
  fin_cases i <;> norm_num [squareWeight]

theorem square_weighted_centering (k : Fin 2) :
    Finset.univ.sum (fun i => squareWeight i * squareOmega i k) = 0 := by
  fin_cases k <;> norm_num [squareWeight, squareOmega, Fin.sum_univ_succ]

/-- The `8 x 4` shared-edge balance matrix.  Rows are `(x_1,y_1,...,x_4,y_4)`
and columns are the cycle edges `12,23,34,41`. -/
def squareBalanceMatrix : Fin 8 → Fin 4 → ℝ :=
  ![![-1,  0,  0, -1],
    ![ 1,  0,  0, -1],
    ![ 1, -1,  0,  0],
    ![-1, -1,  0,  0],
    ![ 0,  1,  1,  0],
    ![ 0,  1, -1,  0],
    ![ 0,  0, -1,  1],
    ![ 0,  0,  1,  1]]

theorem squareBalanceMatrix_columnSum_zero (e : Fin 4) :
    Finset.univ.sum (fun r => squareBalanceMatrix r e) = 0 := by
  fin_cases e <;>
    norm_num [squareBalanceMatrix, Fin.sum_univ_succ]

/-- Right-hand side `b_i=-2w_iΩ_i` in the same row order. -/
def squareBalanceRhs : Fin 8 → ℝ := ![-2, 0, 0, -4, 2, 0, 0, 4]

/-- Exact virtual-displacement certificate `y_i=s_iΩ_i`, with alternating
signs `s=(-1,1,-1,1)`. -/
def squareDualVector : Fin 8 → ℝ := ![-1, 0, 0, 1, 1, 0, 0, -1]

/-- Every square edge has zero virtual work under the certificate. -/
theorem squareDual_transpose_zero (e : Fin 4) :
    finiteTransposeApply squareBalanceMatrix squareDualVector e = 0 := by
  fin_cases e <;>
    norm_num [finiteTransposeApply, squareBalanceMatrix, squareDualVector,
      Fin.sum_univ_succ]

/-- The certificate has strictly negative work against the centered target. -/
theorem squareDual_work :
    finiteDot squareBalanceRhs squareDualVector = -4 := by
  norm_num [finiteDot, squareBalanceRhs, squareDualVector, Fin.sum_univ_succ]

/-- Although all four local rows are positive and the masses are centered, no
nonnegative shared conductance solves the four-cycle equilibrium system. -/
theorem square_sharedEdge_infeasible :
    ¬ ∃ γ : Fin 4 → ℝ,
      (∀ e, 0 ≤ γ e) ∧
      (∀ r, finiteMatrixApply squareBalanceMatrix γ r = squareBalanceRhs r) := by
  apply negative_dualWork_certifies_infeasible
    (A := squareBalanceMatrix) (b := squareBalanceRhs) (y := squareDualVector)
  · intro e
    rw [squareDual_transpose_zero]
  · rw [squareDual_work]
    norm_num

end AFPBarrier

import Mathlib.Algebra.Order.BigOperators.Ring.Finset
import Mathlib.Tactic

/-!
# Geometry of one reversible shared edge

For an undirected edge `{p,q}`, the global balance column has endpoint blocks
`Omega_q - Omega_p` and `Omega_p - Omega_q`. Pairing that column with nodal
dual vectors gives the edge strain used in the Farkas and LP duals.
-/

open scoped BigOperators

namespace AFPBarrier

variable {ι κ : Type*} [Fintype κ]

/-- Finite coordinate dot product. -/
def coordinateDot (x y : κ → ℝ) : ℝ :=
  Finset.univ.sum (fun k => x k * y k)

/-- Pairing of one shared-edge column with nodal dual vectors. -/
def sharedEdgeEndpointWork
    (Omega y : ι → κ → ℝ) (p q : ι) : ℝ :=
  coordinateDot (fun k => Omega q k - Omega p k) (y p) +
  coordinateDot (fun k => Omega p k - Omega q k) (y q)

/-- The orientation-independent edge dual strain. -/
def sharedEdgeStrain
    (Omega y : ι → κ → ℝ) (p q : ι) : ℝ :=
  Finset.univ.sum
    (fun k => (y p k - y q k) * (Omega q k - Omega p k))

/-- Endpoint-column work is exactly the strain appearing in `A^T y`. -/
theorem sharedEdgeEndpointWork_eq_sharedEdgeStrain
    (Omega y : ι → κ → ℝ) (p q : ι) :
    sharedEdgeEndpointWork Omega y p q =
      sharedEdgeStrain Omega y p q := by
  unfold sharedEdgeEndpointWork sharedEdgeStrain coordinateDot
  rw [← Finset.sum_add_distrib]
  apply Finset.sum_congr rfl
  intro k hk
  ring

/-- Reversing the arbitrary endpoint order does not change the strain. -/
theorem sharedEdgeStrain_symm
    (Omega y : ι → κ → ℝ) (p q : ι) :
    sharedEdgeStrain Omega y p q =
      sharedEdgeStrain Omega y q p := by
  unfold sharedEdgeStrain
  apply Finset.sum_congr rfl
  intro k hk
  ring

/-- First variation of one half of the squared chord length. -/
def halfSquaredChordFirstVariation
    (Omega y : ι → κ → ℝ) (p q : ι) : ℝ :=
  Finset.univ.sum
    (fun k => (Omega q k - Omega p k) * (y q k - y p k))

/-- Nonnegative dual strain means the squared chord does not increase to first
order under the associated nodal displacement. -/
theorem halfSquaredChordFirstVariation_eq_neg_sharedEdgeStrain
    (Omega y : ι → κ → ℝ) (p q : ι) :
    halfSquaredChordFirstVariation Omega y p q =
      -sharedEdgeStrain Omega y p q := by
  unfold halfSquaredChordFirstVariation sharedEdgeStrain
  rw [← Finset.sum_neg_distrib]
  apply Finset.sum_congr rfl
  intro k hk
  ring

end AFPBarrier

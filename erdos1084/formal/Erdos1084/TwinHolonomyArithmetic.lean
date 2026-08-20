import Mathlib
import Erdos1084.FccTwinArithmetic

namespace Erdos1084

/-!
# Exact two-plane coherent-twin holonomy obstruction

Two distinct `{111}` twin planes through one FCC `<110>` edge divide a transverse
plane into four sectors.  Returning around the edge crosses the two reflections
twice, so the orientation holonomy is `(S₁ S₂)²`.  This module checks its exact
rational matrix and trace.  A proper cubic lattice symmetry has integer trace;
the exact trace `115/81` is not an integer, so the naive four-sector cross cannot
close crystallographically.
-/

/-- Reflection in the plane normal to `(1,1,1)`. -/
def fccReflectionOne : RatMat3 where
  a00 := 1 / 3;  a01 := -2 / 3; a02 := -2 / 3
  a10 := -2 / 3; a11 := 1 / 3;  a12 := -2 / 3
  a20 := -2 / 3; a21 := -2 / 3; a22 := 1 / 3

/-- Reflection in the plane normal to `(1,1,-1)`. -/
def fccReflectionTwo : RatMat3 where
  a00 := 1 / 3;  a01 := -2 / 3; a02 := 2 / 3
  a10 := -2 / 3; a11 := 1 / 3;  a12 := 2 / 3
  a20 := 2 / 3;  a21 := 2 / 3;  a22 := 1 / 3

/-- Product of the two face reflections. -/
def fccReflectionProduct : RatMat3 :=
  RatMat3.mul fccReflectionOne fccReflectionTwo

/-- Holonomy around the four-sector cross. -/
def fccFourSectorHolonomy : RatMat3 :=
  RatMat3.mul fccReflectionProduct fccReflectionProduct

/-- Each face map is an exact reflection. -/
theorem fccReflectionOne_orthogonal :
    RatMat3.mul (RatMat3.transpose fccReflectionOne) fccReflectionOne =
      RatMat3.ident := by
  native_decide

/-- Each face map is an exact reflection. -/
theorem fccReflectionTwo_orthogonal :
    RatMat3.mul (RatMat3.transpose fccReflectionTwo) fccReflectionTwo =
      RatMat3.ident := by
  native_decide

@[simp] theorem fccReflectionOne_det : RatMat3.det fccReflectionOne = -1 := by
  native_decide

@[simp] theorem fccReflectionTwo_det : RatMat3.det fccReflectionTwo = -1 := by
  native_decide

/-- Exact product of the two reflections. -/
theorem fccReflectionProduct_value :
    fccReflectionProduct =
      { a00 := 1 / 9,  a01 := -8 / 9, a02 := -4 / 9,
        a10 := -8 / 9, a11 := 1 / 9,  a12 := -4 / 9,
        a20 := 4 / 9,  a21 := 4 / 9,  a22 := -7 / 9 } := by
  native_decide

/-- The two-reflection rotation has exact trace `-5/9`. -/
theorem fccReflectionProduct_trace :
    RatMat3.trace fccReflectionProduct = -5 / 9 := by
  native_decide

/-- Exact four-sector holonomy matrix. -/
theorem fccFourSectorHolonomy_value :
    fccFourSectorHolonomy =
      { a00 := 49 / 81,  a01 := -32 / 81, a02 := 56 / 81,
        a10 := -32 / 81, a11 := 49 / 81,  a12 := 56 / 81,
        a20 := -56 / 81, a21 := -56 / 81, a22 := 17 / 81 } := by
  native_decide

/-- Exact trace of the four-sector holonomy. -/
theorem fccFourSectorHolonomy_trace :
    RatMat3.trace fccFourSectorHolonomy = 115 / 81 := by
  native_decide

/-- The holonomy trace is not an integer. -/
theorem fccFourSectorHolonomy_trace_not_integer :
    ¬ ∃ z : ℤ, (z : ℚ) = 115 / 81 := by
  intro h
  rcases h with ⟨z, hz⟩
  have hzq : (81 : ℚ) * (z : ℚ) = 115 := by
    rw [hz]
    norm_num
  have hzz : (81 : ℤ) * z = 115 := by
    exact_mod_cast hzq
  omega

/--
Abstract crystallographic conclusion: any candidate class whose allowed closure
symmetries all have integer trace cannot contain the four-sector holonomy.
-/
theorem fourSectorHolonomy_not_allowed_of_integerTrace
    (allowed : RatMat3 → Prop)
    (htrace : ∀ A, allowed A → ∃ z : ℤ, (z : ℚ) = RatMat3.trace A) :
    ¬ allowed fccFourSectorHolonomy := by
  intro hallowed
  obtain ⟨z, hz⟩ := htrace fccFourSectorHolonomy hallowed
  apply fccFourSectorHolonomy_trace_not_integer
  refine ⟨z, ?_⟩
  simpa [fccFourSectorHolonomy_trace] using hz

end Erdos1084

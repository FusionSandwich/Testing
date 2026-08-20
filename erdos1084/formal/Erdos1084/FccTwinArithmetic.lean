import Mathlib

namespace Erdos1084

/-!
# Exact FCC coherent-twin matrix arithmetic

This module gives a solver-free Lean certificate for the two rational 60-degree
rotations used in the coherent-twin closure audit.  A custom 3-by-3 rational
matrix type keeps the exact computation independent of floating point and of any
specialized crystallographic library.
-/

structure RatMat3 where
  a00 : ℚ
  a01 : ℚ
  a02 : ℚ
  a10 : ℚ
  a11 : ℚ
  a12 : ℚ
  a20 : ℚ
  a21 : ℚ
  a22 : ℚ
  deriving DecidableEq, Repr

namespace RatMat3

/-- Identity matrix. -/
def ident : RatMat3 where
  a00 := 1; a01 := 0; a02 := 0
  a10 := 0; a11 := 1; a12 := 0
  a20 := 0; a21 := 0; a22 := 1

/-- Matrix transpose. -/
def transpose (A : RatMat3) : RatMat3 where
  a00 := A.a00; a01 := A.a10; a02 := A.a20
  a10 := A.a01; a11 := A.a11; a12 := A.a21
  a20 := A.a02; a21 := A.a12; a22 := A.a22

/-- Exact matrix multiplication. -/
def mul (A B : RatMat3) : RatMat3 where
  a00 := A.a00 * B.a00 + A.a01 * B.a10 + A.a02 * B.a20
  a01 := A.a00 * B.a01 + A.a01 * B.a11 + A.a02 * B.a21
  a02 := A.a00 * B.a02 + A.a01 * B.a12 + A.a02 * B.a22
  a10 := A.a10 * B.a00 + A.a11 * B.a10 + A.a12 * B.a20
  a11 := A.a10 * B.a01 + A.a11 * B.a11 + A.a12 * B.a21
  a12 := A.a10 * B.a02 + A.a11 * B.a12 + A.a12 * B.a22
  a20 := A.a20 * B.a00 + A.a21 * B.a10 + A.a22 * B.a20
  a21 := A.a20 * B.a01 + A.a21 * B.a11 + A.a22 * B.a21
  a22 := A.a20 * B.a02 + A.a21 * B.a12 + A.a22 * B.a22

/-- Matrix negation. -/
def neg (A : RatMat3) : RatMat3 where
  a00 := -A.a00; a01 := -A.a01; a02 := -A.a02
  a10 := -A.a10; a11 := -A.a11; a12 := -A.a12
  a20 := -A.a20; a21 := -A.a21; a22 := -A.a22

/-- Exact determinant. -/
def det (A : RatMat3) : ℚ :=
  A.a00 * (A.a11 * A.a22 - A.a12 * A.a21) -
  A.a01 * (A.a10 * A.a22 - A.a12 * A.a20) +
  A.a02 * (A.a10 * A.a21 - A.a11 * A.a20)

/-- Exact trace. -/
def trace (A : RatMat3) : ℚ := A.a00 + A.a11 + A.a22

/-- Natural matrix power. -/
def pow (A : RatMat3) : ℕ → RatMat3
  | 0 => ident
  | n + 1 => mul (pow A n) A

end RatMat3

/-- 60-degree coherent-twin rotation about `(1,1,1)/sqrt 3`. -/
def fccTwinOne : RatMat3 where
  a00 := 2 / 3;  a01 := -1 / 3; a02 := 2 / 3
  a10 := 2 / 3;  a11 := 2 / 3;  a12 := -1 / 3
  a20 := -1 / 3; a21 := 2 / 3;  a22 := 2 / 3

/-- 60-degree coherent-twin rotation about `(1,-1,-1)/sqrt 3`. -/
def fccTwinTwo : RatMat3 where
  a00 := 2 / 3;  a01 := 1 / 3;  a02 := -2 / 3
  a10 := -2 / 3; a11 := 2 / 3;  a12 := -1 / 3
  a20 := 1 / 3;  a21 := 2 / 3;  a22 := 2 / 3

/-- The first square is a cubic coordinate cycle. -/
def fccTwinOneSquare : RatMat3 where
  a00 := 0; a01 := 0; a02 := 1
  a10 := 1; a11 := 0; a12 := 0
  a20 := 0; a21 := 1; a22 := 0

/-- The second square is a signed cubic coordinate cycle. -/
def fccTwinTwoSquare : RatMat3 where
  a00 := 0;  a01 := 0; a02 := -1
  a10 := -1; a11 := 0; a12 := 0
  a20 := 0;  a21 := 1; a22 := 0

/-- Minus reflection in the first coherent twin plane. -/
def fccTwinOneCube : RatMat3 where
  a00 := -1 / 3; a01 := 2 / 3;  a02 := 2 / 3
  a10 := 2 / 3;  a11 := -1 / 3; a12 := 2 / 3
  a20 := 2 / 3;  a21 := 2 / 3;  a22 := -1 / 3

/-- Minus reflection in the second coherent twin plane. -/
def fccTwinTwoCube : RatMat3 where
  a00 := -1 / 3; a01 := -2 / 3; a02 := -2 / 3
  a10 := -2 / 3; a11 := -1 / 3; a12 := 2 / 3
  a20 := -2 / 3; a21 := 2 / 3;  a22 := -1 / 3

/-- Exact product of the two twin generators. -/
def fccTwinProduct : RatMat3 := RatMat3.mul fccTwinOne fccTwinTwo

/-- The first twin matrix is orthogonal. -/
theorem fccTwinOne_orthogonal :
    RatMat3.mul (RatMat3.transpose fccTwinOne) fccTwinOne = RatMat3.ident := by
  native_decide

/-- The second twin matrix is orthogonal. -/
theorem fccTwinTwo_orthogonal :
    RatMat3.mul (RatMat3.transpose fccTwinTwo) fccTwinTwo = RatMat3.ident := by
  native_decide

@[simp] theorem fccTwinOne_det : RatMat3.det fccTwinOne = 1 := by
  native_decide

@[simp] theorem fccTwinTwo_det : RatMat3.det fccTwinTwo = 1 := by
  native_decide

/-- Each coherent-twin rotation has sixth power equal to the identity. -/
theorem fccTwinOne_pow_six : RatMat3.pow fccTwinOne 6 = RatMat3.ident := by
  native_decide

/-- Each coherent-twin rotation has sixth power equal to the identity. -/
theorem fccTwinTwo_pow_six : RatMat3.pow fccTwinTwo 6 = RatMat3.ident := by
  native_decide

/-- The first square is an exact proper cubic symmetry. -/
theorem fccTwinOne_pow_two : RatMat3.pow fccTwinOne 2 = fccTwinOneSquare := by
  native_decide

/-- The second square is an exact proper cubic symmetry. -/
theorem fccTwinTwo_pow_two : RatMat3.pow fccTwinTwo 2 = fccTwinTwoSquare := by
  native_decide

/-- The first cube is minus reflection in its twin plane. -/
theorem fccTwinOne_pow_three : RatMat3.pow fccTwinOne 3 = fccTwinOneCube := by
  native_decide

/-- The second cube is minus reflection in its twin plane. -/
theorem fccTwinTwo_pow_three : RatMat3.pow fccTwinTwo 3 = fccTwinTwoCube := by
  native_decide

/-- Exact product matrix. -/
theorem fccTwinProduct_value :
    fccTwinProduct =
      { a00 := 8 / 9,  a01 := 4 / 9, a02 := 1 / 9,
        a10 := -1 / 9, a11 := 4 / 9, a12 := -8 / 9,
        a20 := -4 / 9, a21 := 7 / 9, a22 := 4 / 9 } := by
  native_decide

/-- The exact rotation trace used in the infinite-order argument. -/
theorem fccTwinProduct_trace : RatMat3.trace fccTwinProduct = 16 / 9 := by
  native_decide

/-- Exact quaternion scalar part for the product. -/
theorem fccTwinProduct_quaternionScalar :
    (3 : ℚ) / 4 - ((1 : ℚ) / 4) * (-1 / 3) = 5 / 6 := by
  norm_num

/-- The quaternion trace formula reproduces `16/9`. -/
theorem fccTwinProduct_trace_from_quaternion :
    4 * ((5 : ℚ) / 6) ^ 2 - 1 = 16 / 9 := by
  norm_num

/-- The product trace is not the rational image of an integer. -/
theorem fccTwinProduct_trace_not_integer :
    ¬ ∃ z : ℤ, (z : ℚ) = 16 / 9 := by
  intro h
  rcases h with ⟨z, hz⟩
  have hzq : (9 : ℚ) * (z : ℚ) = 16 := by
    rw [hz]
    norm_num
  have hzz : (9 : ℤ) * z = 16 := by
    exact_mod_cast hzq
  omega

end Erdos1084

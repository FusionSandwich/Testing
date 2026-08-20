import Mathlib
import Erdos1084.FccTwinArithmetic

namespace Erdos1084

/-!
# Exact seven-letter coherent-twin normal approximation

The finite word

`T2⁻¹ T1 T2⁻¹ T1⁻¹ T2 T1⁻¹ T2`

sends the reference tetrahedral normal `(1,1,1)/sqrt 3` to a unit normal whose
squared transverse component relative to `[001]` is exactly
`68066/14348907 < 1/200`.
-/

structure RatVec3 where
  x : ℚ
  y : ℚ
  z : ℚ
  deriving DecidableEq, Repr

namespace RatMat3

/-- Apply a rational matrix to a rational vector. -/
def apply (A : RatMat3) (v : RatVec3) : RatVec3 where
  x := A.a00 * v.x + A.a01 * v.y + A.a02 * v.z
  y := A.a10 * v.x + A.a11 * v.y + A.a12 * v.z
  z := A.a20 * v.x + A.a21 * v.y + A.a22 * v.z

/-- Left-to-right product of a finite matrix word. -/
def wordProduct (word : List RatMat3) : RatMat3 :=
  word.foldl RatMat3.mul RatMat3.ident

end RatMat3

namespace RatVec3

/-- Rational squared norm. -/
def normSq (v : RatVec3) : ℚ := v.x ^ 2 + v.y ^ 2 + v.z ^ 2

/--
For a vector whose squared norm is three, `(x²+y²)/3` is the squared sine of the
angle between `v/sqrt 3` and `[001]`.
-/
def transverseSqTo001 (v : RatVec3) : ℚ := (v.x ^ 2 + v.y ^ 2) / 3

end RatVec3

/-- Exact seven-letter word used by the certificate. -/
def fccNormal001Word : List RatMat3 :=
  [ RatMat3.transpose fccTwinTwo,
    fccTwinOne,
    RatMat3.transpose fccTwinTwo,
    RatMat3.transpose fccTwinOne,
    fccTwinTwo,
    RatMat3.transpose fccTwinOne,
    fccTwinTwo ]

/-- Reference tetrahedral normal numerator. -/
def fccReference111Numerator : RatVec3 := { x := 1, y := 1, z := 1 }

/-- Exact image numerator under the seven-letter word. -/
def fccNormal001Image : RatVec3 :=
  RatMat3.apply (RatMat3.wordProduct fccNormal001Word) fccReference111Numerator

/-- The word has exactly seven coherent-twin letters. -/
theorem fccNormal001Word_length : fccNormal001Word.length = 7 := by
  native_decide

/-- Exact image of the reference normal numerator. -/
theorem fccNormal001Image_value :
    fccNormal001Image =
      { x := -125 / 2187, y := -229 / 2187, z := 3779 / 2187 } := by
  native_decide

/-- Orthogonality is visible in the exact squared norm. -/
theorem fccNormal001Image_normSq : RatVec3.normSq fccNormal001Image = 3 := by
  native_decide

/-- Exact squared transverse error relative to `[001]`. -/
theorem fccNormal001Image_transverseSq :
    RatVec3.transverseSqTo001 fccNormal001Image = 68066 / 14348907 := by
  native_decide

/-- Certified quantitative normal-approximation bound. -/
theorem fccNormal001Image_transverseSq_lt :
    RatVec3.transverseSqTo001 fccNormal001Image < 1 / 200 := by
  native_decide

end Erdos1084

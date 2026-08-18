import Mathlib
import Erdos1084.BarlowSequence

namespace Erdos1084

/-!
# Exact arithmetic of the periodic Barlow surface cell

The complete geometric and LP derivation is certified by the exact Python implementation. This
module checks the rational coordinate normalization, contact-vector lengths, Wulff-volume formula,
and periodic optimization theorem.
-/

structure BarlowVec where
  x : ℚ
  y : ℚ
  z : ℚ
  deriving DecidableEq, Repr

/-- Squared physical norm in the basis `(a₁,a₂,h e₃)`, where `h²=2/3`. -/
def barlowNormSq (v : BarlowVec) : ℚ :=
  v.x ^ 2 + v.x * v.y + v.y ^ 2 + (2 / 3 : ℚ) * v.z ^ 2

/-- Three in-plane undirected contact representatives. -/
def barlowInPlane₁ : BarlowVec := ⟨1, 0, 0⟩
def barlowInPlane₂ : BarlowVec := ⟨0, 1, 0⟩
def barlowInPlane₃ : BarlowVec := ⟨-1, 1, 0⟩

/-- Three upward contacts across a positive-chirality interface. -/
def barlowUpPlus₁ : BarlowVec := ⟨1 / 3, 1 / 3, 1⟩
def barlowUpPlus₂ : BarlowVec := ⟨-2 / 3, 1 / 3, 1⟩
def barlowUpPlus₃ : BarlowVec := ⟨1 / 3, -2 / 3, 1⟩

/-- Three upward contacts across a negative-chirality interface. -/
def barlowUpMinus₁ : BarlowVec := ⟨-1 / 3, -1 / 3, 1⟩
def barlowUpMinus₂ : BarlowVec := ⟨2 / 3, -1 / 3, 1⟩
def barlowUpMinus₃ : BarlowVec := ⟨-1 / 3, 2 / 3, 1⟩

@[simp] theorem barlow_contact_norms :
    barlowNormSq barlowInPlane₁ = 1 ∧
    barlowNormSq barlowInPlane₂ = 1 ∧
    barlowNormSq barlowInPlane₃ = 1 ∧
    barlowNormSq barlowUpPlus₁ = 1 ∧
    barlowNormSq barlowUpPlus₂ = 1 ∧
    barlowNormSq barlowUpPlus₃ = 1 ∧
    barlowNormSq barlowUpMinus₁ = 1 ∧
    barlowNormSq barlowUpMinus₂ = 1 ∧
    barlowNormSq barlowUpMinus₃ = 1 := by
  norm_num [barlowNormSq, barlowInPlane₁, barlowInPlane₂, barlowInPlane₃,
    barlowUpPlus₁, barlowUpPlus₂, barlowUpPlus₃,
    barlowUpMinus₁, barlowUpMinus₂, barlowUpMinus₃]

/-- Rationally scaled Wulff volume. Physical Wulff volume is twice this value. -/
def periodicBarlowScaledWulffVolume (plus minus : ℕ) : ℚ :=
  16 + ((plus : ℚ) * (minus : ℚ)) /
    ((((plus + minus : ℕ) : ℚ)) ^ 2)

/-- Physical Wulff volume of the contact-deficit anisotropy. -/
def periodicBarlowWulffVolume (plus minus : ℕ) : ℚ :=
  2 * periodicBarlowScaledWulffVolume plus minus

/-- Cube of the particle-number Wulff coefficient. -/
def periodicBarlowCoefficientCube (plus minus : ℕ) : ℚ :=
  432 + 27 * ((plus : ℚ) * (minus : ℚ)) /
    ((((plus + minus : ℕ) : ℚ)) ^ 2)

/-- The mixed-area polynomial used in the exact cross-section integration. -/
def periodicBarlowMixedArea (period a b : ℚ) : ℚ :=
  3 * period ^ 2 + 3 * period * (a + b) +
    (a ^ 2 + b ^ 2) / 2 + 2 * a * b

/-- Algebraic symmetry of the mixed-area polynomial. -/
theorem periodicBarlowMixedArea_swap (period a b : ℚ) :
    periodicBarlowMixedArea period a b =
      periodicBarlowMixedArea period b a := by
  unfold periodicBarlowMixedArea
  ring

/-- Exact integrated raw section area. -/
def periodicBarlowIntegratedSectionArea (plus minus : ℕ) : ℚ :=
  16 * ((((plus + minus : ℕ) : ℚ)) ^ 2) + (plus : ℚ) * (minus : ℚ)

/-- The scaled volume is the integrated section area divided by the squared period. -/
theorem periodicBarlow_scaled_volume_from_sections
    {plus minus : ℕ} (hperiod : 0 < plus + minus) :
    periodicBarlowScaledWulffVolume plus minus =
      periodicBarlowIntegratedSectionArea plus minus /
        ((((plus + minus : ℕ) : ℚ)) ^ 2) := by
  have hneNat : plus + minus ≠ 0 := Nat.ne_of_gt hperiod
  have hne : (((plus + minus : ℕ) : ℚ)) ≠ 0 := by
    exact_mod_cast hneNat
  unfold periodicBarlowScaledWulffVolume periodicBarlowIntegratedSectionArea
  field_simp [hne]

/-- Conversion from physical Wulff volume to the coefficient cube. -/
theorem periodicBarlow_cube_from_wulff_volume
    (plus minus : ℕ) :
    periodicBarlowCoefficientCube plus minus =
      (27 / 2 : ℚ) * periodicBarlowWulffVolume plus minus := by
  unfold periodicBarlowCoefficientCube periodicBarlowWulffVolume
  unfold periodicBarlowScaledWulffVolume
  ring

/-- Every periodic Barlow coefficient is at least the FCC value. -/
theorem periodicBarlow_cube_ge_fcc (plus minus : ℕ) :
    (432 : ℚ) ≤ periodicBarlowCoefficientCube plus minus := by
  unfold periodicBarlowCoefficientCube
  have hden : 0 ≤ ((((plus + minus : ℕ) : ℚ)) ^ 2) := sq_nonneg _
  have hfrac :
      0 ≤ (27 : ℚ) * ((plus : ℚ) * (minus : ℚ)) /
        ((((plus + minus : ℕ) : ℚ)) ^ 2) := by
    exact div_nonneg (by positivity) hden
  linarith

/-- A genuinely mixed chirality word has a strict surface coefficient gap over FCC. -/
theorem periodicBarlow_cube_gt_fcc
    {plus minus : ℕ} (hplus : 0 < plus) (hminus : 0 < minus) :
    (432 : ℚ) < periodicBarlowCoefficientCube plus minus := by
  have hperiod : 0 < plus + minus := Nat.add_pos_left hplus _
  have hden : 0 < ((((plus + minus : ℕ) : ℚ)) ^ 2) := by
    have hcast : (0 : ℚ) < ((plus + minus : ℕ) : ℚ) := by exact_mod_cast hperiod
    positivity
  have hnum : 0 < (27 : ℚ) * ((plus : ℚ) * (minus : ℚ)) := by
    have hp : (0 : ℚ) < plus := by exact_mod_cast hplus
    have hm : (0 : ℚ) < minus := by exact_mod_cast hminus
    positivity
  unfold periodicBarlowCoefficientCube
  have hfrac :
      0 < (27 : ℚ) * ((plus : ℚ) * (minus : ℚ)) /
        ((((plus + minus : ℕ) : ℚ)) ^ 2) := div_pos hnum hden
  linarith

/-- Constant positive chirality gives the FCC coefficient. -/
theorem periodicBarlow_cube_all_plus (period : ℕ) :
    periodicBarlowCoefficientCube period 0 = 432 := by
  simp [periodicBarlowCoefficientCube]

/-- Constant negative chirality gives the reflected FCC coefficient. -/
theorem periodicBarlow_cube_all_minus (period : ℕ) :
    periodicBarlowCoefficientCube 0 period = 432 := by
  simp [periodicBarlowCoefficientCube]

/-- HCP calibration. -/
theorem periodicBarlow_cube_hcp :
    periodicBarlowCoefficientCube 1 1 = 1755 / 4 := by
  norm_num [periodicBarlowCoefficientCube]

/-- The formula is invariant under global chirality reversal. -/
theorem periodicBarlow_cube_swap (plus minus : ℕ) :
    periodicBarlowCoefficientCube plus minus =
      periodicBarlowCoefficientCube minus plus := by
  unfold periodicBarlowCoefficientCube
  rw [Nat.add_comm plus minus]
  ring_nf

/-- Surface energy depends only on the two symbol counts. -/
def periodicBarlowWordCoefficientCube (word : List BarlowChirality) : ℚ :=
  periodicBarlowCoefficientCube (barlowPlusCount word) (barlowMinusCount word)

@[simp] theorem periodicBarlowWordCoefficientCube_reverseChirality
    (word : List BarlowChirality) :
    periodicBarlowWordCoefficientCube (word.map reverseBarlowChirality) =
      periodicBarlowWordCoefficientCube word := by
  unfold periodicBarlowWordCoefficientCube
  rw [barlowPlusCount_map_reverse, barlowMinusCount_map_reverse]
  exact periodicBarlow_cube_swap _ _

/-- Every finite periodic word satisfies the FCC lower bound. -/
theorem periodicBarlowWord_cube_ge_fcc (word : List BarlowChirality) :
    (432 : ℚ) ≤ periodicBarlowWordCoefficientCube word :=
  periodicBarlow_cube_ge_fcc _ _

end Erdos1084

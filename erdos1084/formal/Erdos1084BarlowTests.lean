import Erdos1084.BarlowSequence
import Erdos1084.BarlowCellArithmetic

open Erdos1084
open Erdos1084.BarlowChirality

/-! Smoke tests for the exact periodic Barlow Gate-A arithmetic. -/

example :
    barlowPlusCount [plus, minus, plus, plus] = 3 := by
  norm_num [barlowPlusCount]

example :
    barlowMinusCount [plus, minus, plus, plus] = 1 := by
  norm_num [barlowMinusCount]

example (word : List BarlowChirality) :
    barlowPlusCount word + barlowMinusCount word = word.length :=
  barlow_counts_sum_length word

example : barlowNormSq barlowUpPlus₂ = 1 := by
  norm_num [barlowNormSq, barlowUpPlus₂]

example :
    periodicBarlowCoefficientCube 1 0 = 432 :=
  periodicBarlow_cube_all_plus 1

example :
    periodicBarlowCoefficientCube 1 1 = 1755 / 4 :=
  periodicBarlow_cube_hcp

example (plus minus : ℕ) :
    (432 : ℚ) ≤ periodicBarlowCoefficientCube plus minus :=
  periodicBarlow_cube_ge_fcc plus minus

example {plus minus : ℕ} (hp : 0 < plus) (hm : 0 < minus) :
    (432 : ℚ) < periodicBarlowCoefficientCube plus minus :=
  periodicBarlow_cube_gt_fcc hp hm

example (plus minus : ℕ) :
    periodicBarlowCoefficientCube plus minus =
      (27 / 2 : ℚ) * periodicBarlowWulffVolume plus minus :=
  periodicBarlow_cube_from_wulff_volume plus minus

example (word : List BarlowChirality) :
    periodicBarlowWordCoefficientCube (word.map reverseBarlowChirality) =
      periodicBarlowWordCoefficientCube word :=
  periodicBarlowWordCoefficientCube_reverseChirality word

example (word : List BarlowChirality) :
    (432 : ℚ) ≤ periodicBarlowWordCoefficientCube word :=
  periodicBarlowWord_cube_ge_fcc word

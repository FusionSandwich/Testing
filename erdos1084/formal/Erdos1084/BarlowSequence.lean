import Mathlib

namespace Erdos1084

/-!
# Finite periodic Barlow chirality words

A periodic Barlow stacking is represented by a nonempty finite word in two chiralities.
The geometric symmetry quotient is handled by the exact Python enumerator; this Lean module
formalizes the symbol counts used by the exact periodic cell theorem.
-/

inductive BarlowChirality where
  | plus
  | minus
  deriving DecidableEq, Repr

open BarlowChirality

/-- Number of positive chirality symbols. -/
def barlowPlusCount : List BarlowChirality → ℕ
  | [] => 0
  | plus :: tail => barlowPlusCount tail + 1
  | minus :: tail => barlowPlusCount tail

/-- Number of negative chirality symbols. -/
def barlowMinusCount : List BarlowChirality → ℕ
  | [] => 0
  | plus :: tail => barlowMinusCount tail
  | minus :: tail => barlowMinusCount tail + 1

@[simp] theorem barlow_counts_sum_length (word : List BarlowChirality) :
    barlowPlusCount word + barlowMinusCount word = word.length := by
  induction word with
  | nil => rfl
  | cons head tail ih =>
      cases head <;>
        simp only [barlowPlusCount, barlowMinusCount, List.length_cons]
      all_goals omega

/-- Global chirality reversal swaps the two symbols. -/
def reverseBarlowChirality : BarlowChirality → BarlowChirality
  | plus => minus
  | minus => plus

@[simp] theorem reverseBarlowChirality_involutive (chirality : BarlowChirality) :
    reverseBarlowChirality (reverseBarlowChirality chirality) = chirality := by
  cases chirality <;> rfl

@[simp] theorem barlowPlusCount_map_reverse (word : List BarlowChirality) :
    barlowPlusCount (word.map reverseBarlowChirality) = barlowMinusCount word := by
  induction word with
  | nil => rfl
  | cons head tail ih =>
      cases head <;>
        simp only [List.map_cons, reverseBarlowChirality,
          barlowPlusCount, barlowMinusCount, ih]

@[simp] theorem barlowMinusCount_map_reverse (word : List BarlowChirality) :
    barlowMinusCount (word.map reverseBarlowChirality) = barlowPlusCount word := by
  induction word with
  | nil => rfl
  | cons head tail ih =>
      cases head <;>
        simp only [List.map_cons, reverseBarlowChirality,
          barlowPlusCount, barlowMinusCount, ih]

end Erdos1084

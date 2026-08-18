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
  | nil => simp [barlowPlusCount, barlowMinusCount]
  | cons head tail ih =>
      cases head <;> simp [barlowPlusCount, barlowMinusCount, ih, Nat.add_assoc,
        Nat.add_comm, Nat.add_left_comm]

@[simp] theorem barlowPlusCount_all_plus (n : ℕ) :
    barlowPlusCount (List.replicate n plus) = n := by
  induction n with
  | zero => simp [barlowPlusCount]
  | succ n ih => simp [barlowPlusCount, ih]

@[simp] theorem barlowMinusCount_all_plus (n : ℕ) :
    barlowMinusCount (List.replicate n plus) = 0 := by
  induction n with
  | zero => simp [barlowMinusCount]
  | succ n ih => simp [barlowMinusCount, ih]

@[simp] theorem barlowPlusCount_all_minus (n : ℕ) :
    barlowPlusCount (List.replicate n minus) = 0 := by
  induction n with
  | zero => simp [barlowPlusCount]
  | succ n ih => simp [barlowPlusCount, ih]

@[simp] theorem barlowMinusCount_all_minus (n : ℕ) :
    barlowMinusCount (List.replicate n minus) = n := by
  induction n with
  | zero => simp [barlowMinusCount]
  | succ n ih => simp [barlowMinusCount, ih]

/-- Global chirality reversal swaps the two counts. -/
def reverseBarlowChirality : BarlowChirality → BarlowChirality
  | plus => minus
  | minus => plus

@[simp] theorem barlowPlusCount_map_reverse (word : List BarlowChirality) :
    barlowPlusCount (word.map reverseBarlowChirality) = barlowMinusCount word := by
  induction word with
  | nil => simp [barlowPlusCount]
  | cons head tail ih =>
      cases head <;> simp [barlowPlusCount, barlowMinusCount,
        reverseBarlowChirality, ih]

@[simp] theorem barlowMinusCount_map_reverse (word : List BarlowChirality) :
    barlowMinusCount (word.map reverseBarlowChirality) = barlowPlusCount word := by
  induction word with
  | nil => simp [barlowMinusCount]
  | cons head tail ih =>
      cases head <;> simp [barlowPlusCount, barlowMinusCount,
        reverseBarlowChirality, ih]

end Erdos1084

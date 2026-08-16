import Mathlib

namespace ErdosGyarfas

/-- Number of odd entries in a list. -/
def oddCount : List Nat → Nat
  | [] => 0
  | x :: xs => (if x % 2 = 1 then 1 else 0) + oddCount xs

/-- Parity of a sum equals parity of the number of odd summands. -/
theorem oddCount_mod_two (xs : List Nat) :
    oddCount xs % 2 = xs.sum % 2 := by
  induction xs with
  | nil => simp [oddCount]
  | cons x xs ih =>
      have hlt : x % 2 < 2 := Nat.mod_lt x (by decide)
      by_cases hx : x % 2 = 1
      · simp [oddCount, Nat.add_mod, ih, hx]
      · have hx0 : x % 2 = 0 := by omega
        simp [oddCount, Nat.add_mod, ih, hx0]

theorem even_oddCount_of_even_sum (xs : List Nat) (h : xs.sum % 2 = 0) :
    oddCount xs % 2 = 0 := by
  rw [oddCount_mod_two, h]

/-- Nondecreasing lists of a fixed length with entries in `{lo,...,7}`. -/
def nondecreasingResidueLists : Nat → Nat → List (List Nat)
  | 0, _ => [[]]
  | n + 1, lo =>
      (List.range (8 - lo)).flatMap fun offset =>
        let x := lo + offset
        (nondecreasingResidueLists n x).map fun tail => x :: tail

/-- All nondecreasing nonempty residue sequences of lengths at most eight. -/
def residueCandidates8 : List (List Nat) :=
  (List.range 8).flatMap fun n => nondecreasingResidueLists (n + 1) 1

def isZeroSum8 (xs : List Nat) : Bool := xs.sum % 8 == 0

def isProperNonemptySubsequence (xs ys : List Nat) : Bool :=
  !ys.isEmpty && ys.length < xs.length

def isMinimalZeroSum8 (xs : List Nat) : Bool :=
  isZeroSum8 xs &&
    xs.sublists.all fun ys =>
      !(isProperNonemptySubsequence xs ys) || !(isZeroSum8 ys)

def minimalZeroSumSequences8 : List (List Nat) :=
  residueCandidates8.filter isMinimalZeroSum8

def minimalZeroSumLengthHistogram8 : List Nat :=
  (List.range 9).map fun n =>
    (minimalZeroSumSequences8.filter fun xs => xs.length == n).length

/-- Exact executable classification recovered independently in Python. -/
theorem minimalZeroSumSequences8_count : minimalZeroSumSequences8.length = 64 := by
  native_decide

theorem minimalZeroSumSequences8_length_histogram :
    minimalZeroSumLengthHistogram8 = [0, 0, 4, 10, 18, 16, 8, 4, 4] := by
  native_decide

end ErdosGyarfas

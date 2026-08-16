import Mathlib

namespace ErdosGyarfas

abbrev CompletionEdge := Nat × Nat

def normalizeCompletionEdge (u v : Nat) : CompletionEdge :=
  if u ≤ v then (u, v) else (v, u)

/-- The recovered four-theta obstruction with branch lengths `2,4,5,5`. -/
def fourTheta2455Edges : List CompletionEdge :=
  [(0, 2), (0, 3), (0, 6), (0, 10),
   (1, 2), (1, 5), (1, 9), (1, 13),
   (3, 4), (4, 5),
   (6, 7), (7, 8), (8, 9),
   (10, 11), (11, 12), (12, 13)]

def fourTheta2455InternalVertices : List Nat := List.range' 2 12

/-- Fuelled enumeration of unordered perfect matchings. -/
def perfectMatchingsAux : Nat → List Nat → List (List CompletionEdge)
  | 0, vertices => if vertices.isEmpty then [[]] else []
  | _ + 1, [] => [[]]
  | fuel + 1, x :: xs =>
      xs.flatMap fun y =>
        (perfectMatchingsAux fuel (xs.erase y)).map fun rest =>
          normalizeCompletionEdge x y :: rest

def perfectMatchings (vertices : List Nat) : List (List CompletionEdge) :=
  perfectMatchingsAux vertices.length vertices

def matchingAvoidsThetaEdges (matching : List CompletionEdge) : Bool :=
  matching.all fun edge => !(fourTheta2455Edges.contains edge)

def validFourTheta2455InternalMatchings : List (List CompletionEdge) :=
  (perfectMatchings fourTheta2455InternalVertices).filter matchingAvoidsThetaEdges

def completionAdjacent (edges : List CompletionEdge) (u v : Nat) : Bool :=
  edges.contains (normalizeCompletionEdge u v)

/-- Exact simple-cycle search with the start vertex forced to be the least
vertex on the cycle. -/
def completionCycleSearchAux
    (edges : List CompletionEdge) (start current : Nat) (used : List Nat) : Nat → Bool
  | 0 => completionAdjacent edges current start
  | remaining + 1 =>
      (List.range 14).any fun next =>
        decide (start < next) &&
        !(used.contains next) &&
        completionAdjacent edges current next &&
        completionCycleSearchAux edges start next (next :: used) remaining

def completionHasCycleLength (edges : List CompletionEdge) (length : Nat) : Bool :=
  if length < 3 then false
  else
    (List.range 14).any fun start =>
      completionCycleSearchAux edges start start [start] (length - 1)

def classifyFourTheta2455Completion (matching : List CompletionEdge) : Nat :=
  let edges := fourTheta2455Edges ++ matching
  if completionHasCycleLength edges 4 then 0
  else if completionHasCycleLength edges 8 then 1
  else 2

def fourTheta2455CompletionHistogram : List Nat :=
  (List.range 3).map fun classification =>
    (validFourTheta2455InternalMatchings.filter fun matching =>
      classifyFourTheta2455Completion matching == classification).length

/-- Independent Lean replay of the Python local-completion classification:
4,867 valid internal perfect matchings; 4,647 force a 4-cycle, and each of the
remaining 220 forces an 8-cycle. -/
theorem fourTheta2455_internal_matching_certificate :
    validFourTheta2455InternalMatchings.length = 4867 ∧
    fourTheta2455CompletionHistogram = [4647, 220, 0] := by
  native_decide

end ErdosGyarfas

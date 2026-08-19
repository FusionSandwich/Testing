import Mathlib

namespace Erdos1084

/-!
# Finite-word approximation from a qualitative density hypothesis

This module separates finite-word bookkeeping from the geometric theorem that
the concrete FCC twin generators are dense in `SO(3)`. Once a generator family
is known to hit every nonempty open set by finite words, the existence of a
finite approximating word and its recursively evaluated intermediate states is
formalized here.
-/

/-- A generator letter, with either positive or inverse orientation. -/
inductive SignedGenerator (ι : Type*) where
  | positive : ι → SignedGenerator ι
  | negative : ι → SignedGenerator ι
  deriving DecidableEq, Repr

namespace SignedGenerator

variable {ι G : Type*} [Group G]

/-- Evaluate one signed generator. -/
def eval (generator : ι → G) : SignedGenerator ι → G
  | positive i => generator i
  | negative i => (generator i)⁻¹

end SignedGenerator

section Words

variable {ι G : Type*} [Group G]

/-- Evaluate a finite signed word, from left to right. -/
def evalGeneratorWord (generator : ι → G) : List (SignedGenerator ι) → G
  | [] => 1
  | letter :: rest =>
      SignedGenerator.eval generator letter * evalGeneratorWord generator rest

@[simp] theorem evalGeneratorWord_nil (generator : ι → G) :
    evalGeneratorWord generator [] = 1 :=
  rfl

@[simp] theorem evalGeneratorWord_cons
    (generator : ι → G) (letter : SignedGenerator ι)
    (rest : List (SignedGenerator ι)) :
    evalGeneratorWord generator (letter :: rest) =
      SignedGenerator.eval generator letter * evalGeneratorWord generator rest :=
  rfl

/--
The suffix states of a finite word, listed from the identity state to the value
of the full word. In particular, the final entry is always the word value.
-/
def generatorWordStates
    (generator : ι → G) : List (SignedGenerator ι) → List G
  | [] => [1]
  | letter :: rest =>
      generatorWordStates generator rest ++
        [evalGeneratorWord generator (letter :: rest)]

/-- The final recorded state is the value of the word. -/
theorem generatorWordStates_getLast?_eq
    (generator : ι → G) (word : List (SignedGenerator ι)) :
    (generatorWordStates generator word).getLast? =
      some (evalGeneratorWord generator word) := by
  cases word with
  | nil => rfl
  | cons letter rest =>
      simp [generatorWordStates]

/-- The set of values represented by finite signed generator words. -/
def finiteWordValues (generator : ι → G) : Set G :=
  {g | ∃ word : List (SignedGenerator ι), evalGeneratorWord generator word = g}

/-- The identity is represented by the empty word. -/
theorem one_mem_finiteWordValues (generator : ι → G) :
    (1 : G) ∈ finiteWordValues generator := by
  exact ⟨[], rfl⟩

/-- A qualitative finite-word density predicate. -/
def FiniteWordsHitEveryNonemptyOpen
    [TopologicalSpace G] (generator : ι → G) : Prop :=
  ∀ U : Set G, IsOpen U → U.Nonempty →
    ∃ word : List (SignedGenerator ι), evalGeneratorWord generator word ∈ U

/-- The density predicate directly supplies a finite word in any target open set. -/
theorem exists_word_mem_open
    [TopologicalSpace G]
    (generator : ι → G)
    (hdense : FiniteWordsHitEveryNonemptyOpen generator)
    {U : Set G} (hUopen : IsOpen U) (hUne : U.Nonempty) :
    ∃ word : List (SignedGenerator ι), evalGeneratorWord generator word ∈ U :=
  hdense U hUopen hUne

/-- Pointwise neighborhood approximation form of finite-word density. -/
theorem exists_word_in_neighborhood
    [TopologicalSpace G]
    (generator : ι → G)
    (hdense : FiniteWordsHitEveryNonemptyOpen generator)
    {q : G} {U : Set G}
    (hUopen : IsOpen U) (hq : q ∈ U) :
    ∃ word : List (SignedGenerator ι), evalGeneratorWord generator word ∈ U := by
  exact hdense U hUopen ⟨q, hq⟩

/--
Every successful approximation property has a witness with some finite natural
word length. Minimality is an ordinary well-ordering consequence and is not
needed for the qualitative diagonal argument.
-/
theorem exists_finite_word_length
    (P : G → Prop)
    (generator : ι → G)
    (h : ∃ word : List (SignedGenerator ι),
      P (evalGeneratorWord generator word)) :
    ∃ n : ℕ, ∃ word : List (SignedGenerator ι),
      word.length = n ∧ P (evalGeneratorWord generator word) := by
  rcases h with ⟨word, hword⟩
  exact ⟨word.length, word, rfl, hword⟩

end Words

end Erdos1084

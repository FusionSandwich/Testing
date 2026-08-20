import Mathlib

namespace Erdos1084

open MeasureTheory Set

/-!
# Doubly countable unions of null parameter sets

This module supplies the measure-theoretic bookkeeping used for rigid abrupt
translation parameters.  The geometric application assigns one null set to each
pair of sites.  Nullity of the individual geometric sets is kept as an explicit
hypothesis.
-/

variable {α ι κ : Type*} [MeasurableSpace α]

/-- Union of a doubly indexed family of parameter sets. -/
def pairParameterUnion (s : ι → κ → Set α) : Set α :=
  ⋃ i, ⋃ j, s i j

/-- A doubly countable union of null sets is null. -/
theorem measure_pairParameterUnion_zero
    [Countable ι] [Countable κ]
    (μ : Measure α)
    (s : ι → κ → Set α)
    (hnull : ∀ i j, μ (s i j) = 0) :
    μ (pairParameterUnion s) = 0 := by
  unfold pairParameterUnion
  exact measure_iUnion_null fun i =>
    measure_iUnion_null fun j => hnull i j

/-- Each member of the family is contained in the full pair union. -/
theorem subset_pairParameterUnion
    (s : ι → κ → Set α) (i : ι) (j : κ) :
    s i j ⊆ pairParameterUnion s := by
  intro x hx
  exact mem_iUnion_of_mem i (mem_iUnion_of_mem j hx)

/-- Any subset of the pair union is null when every pair set is null. -/
theorem measure_zero_of_subset_pairParameterUnion
    [Countable ι] [Countable κ]
    (μ : Measure α)
    (s : ι → κ → Set α)
    (u : Set α)
    (hu : u ⊆ pairParameterUnion s)
    (hnull : ∀ i j, μ (s i j) = 0) :
    μ u = 0 := by
  exact measure_mono_null hu (measure_pairParameterUnion_zero μ s hnull)

/-- A pair witness for every point gives the required containment automatically. -/
theorem measure_zero_of_pair_witness
    [Countable ι] [Countable κ]
    (μ : Measure α)
    (s : ι → κ → Set α)
    (u : Set α)
    (hwitness : ∀ x, x ∈ u → ∃ i j, x ∈ s i j)
    (hnull : ∀ i j, μ (s i j) = 0) :
    μ u = 0 := by
  apply measure_zero_of_subset_pairParameterUnion μ s u
  · intro x hx
    obtain ⟨i, j, hij⟩ := hwitness x hx
    exact mem_iUnion_of_mem i (mem_iUnion_of_mem j hij)
  · exact hnull

end Erdos1084

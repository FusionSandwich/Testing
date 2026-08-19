import Mathlib
import Erdos1084.RadiusTwoCore

namespace Erdos1084

/-- A finite sum is strict when every summand is bounded above and one is strict. -/
theorem finite_sum_lt_of_one_strict
    {ι : Type*} [Fintype ι]
    (f g : ι → ℝ)
    (hle : ∀ i, f i ≤ g i)
    (i₀ : ι)
    (hlt : f i₀ < g i₀) :
    (∑ i, f i) < ∑ i, g i := by
  refine Finset.sum_lt_sum ?_ ?_
  · intro i hi
    exact hle i
  · exact ⟨i₀, Finset.mem_univ i₀, hlt⟩

/-- The degree-sum identity in the form used by the radius-two surface charge. -/
theorem radiusTwo_degree_deficit_sum
    {ι : Type*} [Fintype ι]
    (d : ι → ℝ)
    (n E : ℝ)
    (hn : (Fintype.card ι : ℝ) = n)
    (hdeg : (∑ i, d i) = 2 * E) :
    (∑ i, (12 - d i)) = 2 * (6 * n - E) := by
  have hconst : (∑ _ : ι, (12 : ℝ)) = 12 * n := by
    calc
      (∑ _ : ι, (12 : ℝ)) = (Fintype.card ι : ℝ) * 12 := by simp
      _ = 12 * n := by rw [hn]; ring
  calc
    (∑ i, (12 - d i)) = (∑ _ : ι, (12 : ℝ)) - ∑ i, d i := by
      rw [Finset.sum_sub_distrib]
    _ = 12 * n - 2 * E := by rw [hconst, hdeg]
    _ = 2 * (6 * n - E) := by ring

/--
Abstract local-to-global assembly for the radius-two proof.

All geometry has been reduced to the boundary lower bound, boundary subadditivity,
and local exposed-area charges. The conclusion is the `5/3` contact deficit.
-/
theorem radiusTwo_global_assembly
    {ι : Type*} [Fintype ι]
    (d exposure : ι → ℝ)
    (n E x A : ℝ)
    (hn : (Fintype.card ι : ℝ) = n)
    (hdeg : (∑ i, d i) = 2 * E)
    (hBoundary : A ≤ ∑ i, exposure i)
    (hLocal : ∀ i,
      exposure i ≤ (6 * Real.pi / 5) * (12 - d i))
    (i₀ : ι)
    (hStrict :
      exposure i₀ < (6 * Real.pi / 5) * (12 - d i₀))
    (hLower : 4 * Real.pi * x ≤ A) :
    (5 / 3 : ℝ) * x < 6 * n - E := by
  have hsum :
      (∑ i, exposure i) <
        ∑ i, (6 * Real.pi / 5) * (12 - d i) :=
    finite_sum_lt_of_one_strict
      exposure (fun i => (6 * Real.pi / 5) * (12 - d i))
      hLocal i₀ hStrict
  have hdef := radiusTwo_degree_deficit_sum d n E hn hdeg
  have hcharge :
      (∑ i, (6 * Real.pi / 5) * (12 - d i)) =
        (12 * Real.pi / 5) * (6 * n - E) := by
    calc
      (∑ i, (6 * Real.pi / 5) * (12 - d i)) =
          (6 * Real.pi / 5) * ∑ i, (12 - d i) := by
        rw [Finset.mul_sum]
      _ = (6 * Real.pi / 5) * (2 * (6 * n - E)) := by rw [hdef]
      _ = (12 * Real.pi / 5) * (6 * n - E) := by ring
  have hUpper : A < (12 * Real.pi / 5) * (6 * n - E) := by
    calc
      A ≤ ∑ i, exposure i := hBoundary
      _ < ∑ i, (6 * Real.pi / 5) * (12 - d i) := hsum
      _ = (12 * Real.pi / 5) * (6 * n - E) := hcharge
  exact radiusTwo_surface_to_deficit hLower hUpper

end Erdos1084

import Mathlib
import Erdos1084.RadiusTwoAssembly
import Erdos1084.RadiusTwoOptimized

namespace Erdos1084

/--
Abstract local-to-global assembly for the clean strengthened radius-two coefficient `1673/1000`.

All geometric inputs have been reduced to a boundary lower bound, boundary subadditivity,
and the strengthened local exposed-area charges.
-/
theorem radiusTwo_global_assembly_1673
    {ι : Type*} [Fintype ι]
    (d exposure : ι → ℝ)
    (n E x A : ℝ)
    (hn : (Fintype.card ι : ℝ) = n)
    (hdeg : (∑ i, d i) = 2 * E)
    (hBoundary : A ≤ ∑ i, exposure i)
    (hLocal : ∀ i,
      exposure i ≤ (2000 * Real.pi / 1673) * (12 - d i))
    (i₀ : ι)
    (hStrict :
      exposure i₀ < (2000 * Real.pi / 1673) * (12 - d i₀))
    (hLower : 4 * Real.pi * x ≤ A) :
    (1673 / 1000 : ℝ) * x < 6 * n - E := by
  have hsum :
      (∑ i, exposure i) <
        ∑ i, (2000 * Real.pi / 1673) * (12 - d i) :=
    finite_sum_lt_of_one_strict
      exposure (fun i => (2000 * Real.pi / 1673) * (12 - d i))
      hLocal i₀ hStrict
  have hdef := radiusTwo_degree_deficit_sum d n E hn hdeg
  have hcharge :
      (∑ i, (2000 * Real.pi / 1673) * (12 - d i)) =
        (4000 * Real.pi / 1673) * (6 * n - E) := by
    calc
      (∑ i, (2000 * Real.pi / 1673) * (12 - d i)) =
          (2000 * Real.pi / 1673) * ∑ i, (12 - d i) := by
        rw [Finset.mul_sum]
      _ = (2000 * Real.pi / 1673) * (2 * (6 * n - E)) := by
        rw [hdef]
      _ = (4000 * Real.pi / 1673) * (6 * n - E) := by ring
  have hUpper : A < (4000 * Real.pi / 1673) * (6 * n - E) := by
    calc
      A ≤ ∑ i, exposure i := hBoundary
      _ < ∑ i, (2000 * Real.pi / 1673) * (12 - d i) := hsum
      _ = (4000 * Real.pi / 1673) * (6 * n - E) := hcharge
  exact radiusTwo_surface_to_deficit_1673 hLower hUpper

end Erdos1084

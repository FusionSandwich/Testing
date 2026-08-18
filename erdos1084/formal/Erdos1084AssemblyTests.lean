import Erdos1084

open Erdos1084

example {ι : Type*} [Fintype ι]
    (f g : ι → ℝ)
    (hle : ∀ i, f i ≤ g i)
    (i₀ : ι)
    (hlt : f i₀ < g i₀) :
    (∑ i, f i) < ∑ i, g i :=
  finite_sum_lt_of_one_strict f g hle i₀ hlt

example {ι : Type*} [Fintype ι]
    (d : ι → ℝ)
    (n E : ℝ)
    (hn : (Fintype.card ι : ℝ) = n)
    (hdeg : (∑ i, d i) = 2 * E) :
    (∑ i, (12 - d i)) = 2 * (6 * n - E) :=
  radiusTwo_degree_deficit_sum d n E hn hdeg

example {ι : Type*} [Fintype ι]
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
    (5 / 3 : ℝ) * x < 6 * n - E :=
  radiusTwo_global_assembly
    d exposure n E x A hn hdeg hBoundary hLocal i₀ hStrict hLower

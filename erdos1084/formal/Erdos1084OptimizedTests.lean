import Erdos1084

open Erdos1084

/-! End-to-end smoke test for the strengthened `1673/1000` assembly. -/

example
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
    (1673 / 1000 : ℝ) * x < 6 * n - E :=
  radiusTwo_global_assembly_1673
    d exposure n E x A hn hdeg hBoundary hLocal i₀ hStrict hLower

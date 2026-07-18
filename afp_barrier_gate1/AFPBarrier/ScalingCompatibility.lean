import AFPBarrier.ReversibleConductance

/-!
# Scaling compatibility of normalized spherical graph Laplacians

Both the AFP construction and geometric spherical Delaunay Laplacians have the
normalized conductance form

  `(L f)(i) = (1 / w i) * sum_j gamma i j * (f j - f i)`.

A common nonzero scaling of all edge conductances and all vertex weights leaves
the normalized operator unchanged. This is the precise condition under which
a geometric conductance/vertex-weight pair transfers directly to prescribed
quadrature weights.
-/

namespace AFPBarrier

variable {ι : Type*} [Fintype ι] [DecidableEq ι]

/-- A common nonzero scale leaves every normalized conductance rate unchanged. -/
theorem conductanceRate_common_scale
    (c : ι → ι → ℝ) (d : ι → ℝ) (α : ℝ)
    (hα : α ≠ 0) (hd : ∀ i, d i ≠ 0)
    (i j : ι) :
    conductanceRate (fun p q => α * c p q) (fun p => α * d p) i j
      = conductanceRate c d i j := by
  unfold conductanceRate
  field_simp [hα, hd i]

/-- The whole jump generator is invariant under a common nonzero scale. -/
theorem jumpGenerator_conductance_common_scale
    (c : ι → ι → ℝ) (d : ι → ℝ) (α : ℝ)
    (hα : α ≠ 0) (hd : ∀ i, d i ≠ 0)
    (f : ι → ℝ) (i : ι) :
    jumpGenerator
        (conductanceRate (fun p q => α * c p q) (fun p => α * d p)) f i
      = jumpGenerator (conductanceRate c d) f i := by
  unfold jumpGenerator
  apply Finset.sum_congr rfl
  intro j hj
  rw [conductanceRate_common_scale c d α hα hd i j]

/-- A coordinate equilibrium system transfers under a common scale. -/
theorem equilibrium_common_scale
    (c : ι → ι → ℝ) (d f : ι → ℝ) (α lam : ℝ) (i : ι)
    (hequilibrium :
      Finset.univ.sum (fun j => c i j * (f j - f i))
        = -lam * d i * f i) :
    Finset.univ.sum
        (fun j => (α * c i j) * (f j - f i))
      = -lam * (α * d i) * f i := by
  calc
    Finset.univ.sum
        (fun j => (α * c i j) * (f j - f i))
        = α * Finset.univ.sum (fun j => c i j * (f j - f i)) := by
            rw [Finset.mul_sum]
            apply Finset.sum_congr rfl
            intro j hj
            ring
    _ = α * (-lam * d i * f i) := by rw [hequilibrium]
    _ = -lam * (α * d i) * f i := by ring

/-- If a geometric spherical Laplacian has exact coordinate eigenvalue
`-lam`, then any common scaling of its edge and vertex weights gives the same
exact normalized operator. -/
theorem geometric_pair_transfers_to_scaled_quadrature
    (c : ι → ι → ℝ) (d : ι → ℝ) (α lam : ℝ)
    {κ : Type*} [Fintype κ]
    (Ω : ι → κ → ℝ)
    (hα : α ≠ 0) (hd : ∀ i, d i ≠ 0)
    (heigen : ∀ i k,
      jumpGenerator (conductanceRate c d) (fun j => Ω j k) i
        = -lam * Ω i k) :
    ∀ i k,
      jumpGenerator
        (conductanceRate (fun p q => α * c p q) (fun p => α * d p))
        (fun j => Ω j k) i
        = -lam * Ω i k := by
  intro i k
  rw [jumpGenerator_conductance_common_scale c d α hα hd]
  exact heigen i k

end AFPBarrier

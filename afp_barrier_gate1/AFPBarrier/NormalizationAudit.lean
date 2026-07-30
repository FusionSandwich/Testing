import AFPBarrier.ReversibleConductance

/-!
# Normalization of the coordinate-balance equation

For the spherical Laplacian on `S^2`, every Cartesian coordinate has
Laplace--Beltrami eigenvalue `-2`. In a shared-edge discretization this means

  `sum_j gamma_ij (f_j - f_i) = -2 * w_i * f_i`.

This module proves the general scalar identity and records that the `-2` and
`-4` balance targets cannot both be correct at a node where `w_i f_i` is
nonzero.
-/

open scoped BigOperators

namespace AFPBarrier

variable {ι : Type*} [Fintype ι] [DecidableEq ι]

/-- A normalized eigenfunction equation is equivalent to its unnormalized
shared-edge balance equation. -/
theorem conductance_eigen_iff_equilibrium
    (γ : ι → ι → ℝ) (w f : ι → ℝ) (i : ι) (lam : ℝ)
    (hw : ∀ p, w p ≠ 0) :
    jumpGenerator (conductanceRate γ w) f i = -lam * f i
      ↔ Finset.univ.sum (fun j => γ i j * (f j - f i))
          = -lam * w i * f i := by
  rw [← weight_mul_jumpGenerator_conductanceRate
    (γ := γ) (w := w) (f := f) (hw := hw) (i := i)]
  constructor
  · intro h
    rw [h]
    ring
  · intro h
    have hdiv := congrArg (fun x : ℝ => x / w i) h
    field_simp [hw i] at hdiv ⊢
    linarith

/-- The exact `S^2` coordinate balance carries the factor `-2`. -/
theorem S2_coordinate_eigen_implies_minus_two_balance
    (γ : ι → ι → ℝ) (w f : ι → ℝ) (i : ι)
    (hw : ∀ p, w p ≠ 0)
    (heigen : jumpGenerator (conductanceRate γ w) f i = -2 * f i) :
    Finset.univ.sum (fun j => γ i j * (f j - f i))
      = -2 * w i * f i := by
  exact (conductance_eigen_iff_equilibrium
    (γ := γ) (w := w) (f := f) (i := i) (lam := 2) hw).mp heigen

/-- The `-2` and `-4` balance normalizations are incompatible whenever the
weighted sampled coordinate is nonzero. -/
theorem minus_two_and_minus_four_balance_incompatible
    (γ : ι → ι → ℝ) (w f : ι → ℝ) (i : ι)
    (hnonzero : w i * f i ≠ 0)
    (h2 : Finset.univ.sum (fun j => γ i j * (f j - f i))
      = -2 * w i * f i)
    (h4 : Finset.univ.sum (fun j => γ i j * (f j - f i))
      = -4 * w i * f i) :
    False := by
  have hzero : 2 * (w i * f i) = 0 := by linarith
  exact hnonzero (by nlinarith)

end AFPBarrier

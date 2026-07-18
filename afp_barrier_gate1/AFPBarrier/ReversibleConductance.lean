import AFPBarrier.ForwardAdjoint

/-!
# Reversible shared-edge conductances

The multidimensional finite-difference AFP matrix in Bienvenue et al. is built
from one symmetric coefficient `γ i j = γ j i` per undirected Voronoi edge and
positive quadrature weights `w i`. Its off-diagonal jump rate is

  `a i j = γ i j / w i`.

This module formalizes detailed balance, weighted self-adjointness through the
weighted-adjoint construction, weighted conservation, and the resulting
necessary weighted-mean condition for nonzero eigenmodes.
-/

open scoped BigOperators

namespace AFPBarrier

variable {ι : Type*} [Fintype ι] [DecidableEq ι]

/-- Jump rates induced by shared-edge conductances and vertex weights. -/
noncomputable def conductanceRate
    (γ : ι → ι → ℝ) (w : ι → ℝ) (i j : ι) : ℝ :=
  γ i j / w i

/-- Positive conductances and positive vertex weights give nonnegative rates. -/
theorem conductanceRate_nonneg
    (γ : ι → ι → ℝ) (w : ι → ℝ)
    (hγ : ∀ i j, i ≠ j → 0 ≤ γ i j)
    (hw : ∀ i, 0 < w i)
    (i j : ι) (hij : i ≠ j) :
    0 ≤ conductanceRate γ w i j := by
  exact div_nonneg (hγ i j hij) (le_of_lt (hw i))

/-- Symmetric conductances satisfy detailed balance. -/
theorem conductanceRate_detailedBalance
    (γ : ι → ι → ℝ) (w : ι → ℝ)
    (hγsymm : ∀ i j, γ i j = γ j i)
    (hw : ∀ i, w i ≠ 0)
    (i j : ι) :
    w i * conductanceRate γ w i j
      = w j * conductanceRate γ w j i := by
  unfold conductanceRate
  calc
    w i * (γ i j / w i) = γ i j := by field_simp [hw i]
    _ = γ j i := hγsymm i j
    _ = w j * (γ j i / w j) := by field_simp [hw j]

/-- The weighted adjoint of a reversible conductance operator has exactly the
same off-diagonal rates. -/
theorem weightedAdjointRate_conductanceRate_eq
    (γ : ι → ι → ℝ) (w : ι → ℝ)
    (hγsymm : ∀ i j, γ i j = γ j i)
    (hw : ∀ i, w i ≠ 0)
    (i j : ι) :
    weightedAdjointRate (conductanceRate γ w) w i j
      = conductanceRate γ w i j := by
  unfold weightedAdjointRate conductanceRate
  have hj : w j * (γ j i / w j) = γ j i := by
    field_simp [hw j]
  rw [hj, hγsymm j i]

/-- Multiplying a conductance-generated row by its vertex weight removes the
normalization. The diagonal term can be included because its difference is
zero. -/
theorem weight_mul_jumpGenerator_conductanceRate
    (γ : ι → ι → ℝ) (w f : ι → ℝ)
    (hw : ∀ i, w i ≠ 0)
    (i : ι) :
    w i * jumpGenerator (conductanceRate γ w) f i
      = Finset.univ.sum (fun j => γ i j * (f j - f i)) := by
  classical
  rw [jumpGenerator]
  calc
    w i * (offdiag i).sum
        (fun j => conductanceRate γ w i j * (f j - f i))
        = (offdiag i).sum (fun j => γ i j * (f j - f i)) := by
            rw [Finset.mul_sum]
            apply Finset.sum_congr rfl
            intro j hj
            unfold conductanceRate
            field_simp [hw i]
    _ = Finset.univ.sum (fun j => γ i j * (f j - f i)) := by
          rw [← Finset.sum_erase_add
            Finset.univ
            (fun j => γ i j * (f j - f i))
            (Finset.mem_univ i)]
          simp [offdiag]

/-- A reversible conductance generator conserves every weighted integral. -/
theorem weighted_sum_jumpGenerator_conductanceRate_eq_zero
    (γ : ι → ι → ℝ) (w f : ι → ℝ)
    (hγsymm : ∀ i j, γ i j = γ j i)
    (hw : ∀ i, w i ≠ 0) :
    Finset.univ.sum
        (fun i => w i * jumpGenerator (conductanceRate γ w) f i)
      = 0 := by
  classical
  let S : ℝ := Finset.univ.sum
    (fun i => Finset.univ.sum (fun j => γ i j * (f j - f i)))
  have hrewrite :
      Finset.univ.sum
          (fun i => w i * jumpGenerator (conductanceRate γ w) f i)
        = S := by
    unfold S
    apply Finset.sum_congr rfl
    intro i hi
    exact weight_mul_jumpGenerator_conductanceRate
      (γ := γ) (w := w) (f := f) hw i
  have hneg : S = -S := by
    unfold S
    calc
      Finset.univ.sum
          (fun i => Finset.univ.sum (fun j => γ i j * (f j - f i)))
          = Finset.univ.sum
              (fun j => Finset.univ.sum (fun i => γ i j * (f j - f i))) := by
                rw [Finset.sum_comm]
      _ = Finset.univ.sum
              (fun j => Finset.univ.sum
                (fun i => -(γ j i * (f i - f j)))) := by
            apply Finset.sum_congr rfl
            intro j hj
            apply Finset.sum_congr rfl
            intro i hi
            rw [← hγsymm i j]
            ring
      _ = -Finset.univ.sum
              (fun j => Finset.univ.sum (fun i => γ j i * (f i - f j))) := by
            simp only [Finset.sum_neg_distrib]
      _ = -Finset.univ.sum
              (fun i => Finset.univ.sum (fun j => γ i j * (f j - f i))) := by
            rfl
  rw [hrewrite]
  linarith

/-- A nonzero eigenmode of a reversible conductance generator must have zero
weighted mean. -/
theorem conductance_eigen_implies_weightedMean_zero
    (γ : ι → ι → ℝ) (w f : ι → ℝ) (lam : ℝ)
    (hγsymm : ∀ i j, γ i j = γ j i)
    (hw : ∀ i, w i ≠ 0)
    (hlam : lam ≠ 0)
    (heigen : ∀ i,
      jumpGenerator (conductanceRate γ w) f i = -lam * f i) :
    Finset.univ.sum (fun i => w i * f i) = 0 := by
  have hsum := weighted_sum_jumpGenerator_conductanceRate_eq_zero
    (γ := γ) (w := w) (f := f) hγsymm hw
  have hfactor :
      Finset.univ.sum
          (fun i => w i * jumpGenerator (conductanceRate γ w) f i)
        = -lam * Finset.univ.sum (fun i => w i * f i) := by
    calc
      Finset.univ.sum
          (fun i => w i * jumpGenerator (conductanceRate γ w) f i)
          = Finset.univ.sum (fun i => w i * (-lam * f i)) := by
              apply Finset.sum_congr rfl
              intro i hi
              rw [heigen i]
      _ = -lam * Finset.univ.sum (fun i => w i * f i) := by
            rw [Finset.mul_sum]
            apply Finset.sum_congr rfl
            intro i hi
            ring
  rw [hfactor] at hsum
  exact (mul_eq_zero.mp hsum).resolve_left (neg_ne_zero.mpr hlam)

/-- The finite degree-two obstruction applies directly to the reversible
shared-edge form used in the multidimensional AFP implementation. -/
theorem no_exact_conductance_linear_and_square_at_peak
    (γ : ι → ι → ℝ) (w f : ι → ℝ) (i : ι) (lam : ℝ)
    (hγ : ∀ p q, p ≠ q → 0 ≤ γ p q)
    (hw : ∀ p, 0 < w p)
    (hlam : 0 < lam)
    (hfi : f i = 1)
    (hlinear : jumpGenerator (conductanceRate γ w) f i = -lam)
    (hsquare :
      jumpGenerator (conductanceRate γ w) (fun j => (f j) ^ 2) i
        = -2 * lam) :
    False := by
  apply no_exact_linear_and_square_at_peak
    (a := conductanceRate γ w) (f := f) (i := i) (lam := lam)
  · intro j hji
    exact conductanceRate_nonneg γ w hγ hw i j (Ne.symm hji)
  · exact hlam
  · exact hfi
  · exact hlinear
  · exact hsquare

end AFPBarrier

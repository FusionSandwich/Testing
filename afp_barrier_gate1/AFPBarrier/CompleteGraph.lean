import AFPBarrier.ReversibleConductance

/-!
# A universal complete-graph AFP construction

For any positive quadrature with zero weighted mean, the complete graph carries
a strictly positive reversible conductance system that preserves every
weighted-mean-zero sampled function with one common eigenvalue. Applied to the
Cartesian coordinate functions, this proves that weighted centering is both
necessary and sufficient for a dense positive degree-one-exact AFP operator.
-/

open scoped BigOperators

namespace AFPBarrier

variable {ι : Type*} [Fintype ι] [DecidableEq ι]

/-- Total quadrature weight. -/
def totalWeight (w : ι → ℝ) : ℝ :=
  Finset.univ.sum w

/-- Dense complete-graph jump rates. -/
noncomputable def completeRate
    (w : ι → ℝ) (lam : ℝ) (i j : ι) : ℝ :=
  lam * w j / totalWeight w

/-- Corresponding symmetric shared-edge conductances. -/
noncomputable def completeConductance
    (w : ι → ℝ) (lam : ℝ) (i j : ι) : ℝ :=
  lam * w i * w j / totalWeight w

@[simp] theorem completeConductance_symm
    (w : ι → ℝ) (lam : ℝ) (i j : ι) :
    completeConductance w lam i j = completeConductance w lam j i := by
  unfold completeConductance
  ring

/-- Dividing the complete conductance by the source vertex weight recovers the
complete rate. -/
theorem conductanceRate_completeConductance_eq_completeRate
    (w : ι → ℝ) (lam : ℝ)
    (hw : ∀ i, w i ≠ 0)
    (i j : ι) :
    conductanceRate (completeConductance w lam) w i j
      = completeRate w lam i j := by
  unfold conductanceRate completeConductance completeRate
  field_simp [hw i]

/-- The complete graph acts as `-lam` on every weighted-mean-zero sampled
function. -/
theorem completeRate_eigen_of_weightedMean_zero
    (w f : ι → ℝ) (lam : ℝ) (i : ι)
    (hW : totalWeight w ≠ 0)
    (hmean : Finset.univ.sum (fun j => w j * f j) = 0) :
    jumpGenerator (completeRate w lam) f i = -lam * f i := by
  classical
  have hfull :
      (offdiag i).sum
          (fun j => completeRate w lam i j * (f j - f i))
        = Finset.univ.sum
          (fun j => completeRate w lam i j * (f j - f i)) := by
    rw [← Finset.sum_erase_add
      Finset.univ
      (fun j => completeRate w lam i j * (f j - f i))
      (Finset.mem_univ i)]
    simp [offdiag]
  rw [jumpGenerator, hfull]
  unfold completeRate
  calc
    Finset.univ.sum
        (fun j => (lam * w j / totalWeight w) * (f j - f i))
        = (lam / totalWeight w) *
            Finset.univ.sum (fun j => w j * (f j - f i)) := by
              rw [Finset.mul_sum]
              apply Finset.sum_congr rfl
              intro j hj
              ring
    _ = (lam / totalWeight w) *
          (Finset.univ.sum (fun j => w j * f j)
            - totalWeight w * f i) := by
          congr 1
          simp only [mul_sub, Finset.sum_sub_distrib]
          rw [← Finset.sum_mul]
          rfl
    _ = -lam * f i := by
          rw [hmean]
          field_simp [hW]
          ring

/-- Positive weights and a positive target eigenvalue give strictly positive
complete-graph off-diagonal rates. -/
theorem completeRate_pos
    (w : ι → ℝ) (lam : ℝ)
    (hw : ∀ i, 0 < w i)
    (hlam : 0 < lam)
    (hW : 0 < totalWeight w)
    (i j : ι) :
    0 < completeRate w lam i j := by
  exact div_pos (mul_pos hlam (hw j)) hW

/-- Positive weights and a positive target eigenvalue give strictly positive
shared-edge conductances. -/
theorem completeConductance_pos
    (w : ι → ℝ) (lam : ℝ)
    (hw : ∀ i, 0 < w i)
    (hlam : 0 < lam)
    (hW : 0 < totalWeight w)
    (i j : ι) :
    0 < completeConductance w lam i j := by
  unfold completeConductance
  exact div_pos (mul_pos (mul_pos hlam (hw i)) (hw j)) hW

/-- Coordinatewise form: a weighted-centered node set admits a dense positive
reversible operator with the exact degree-one eigenvalue. -/
theorem completeRate_preserves_centered_coordinates
    {κ : Type*} [Fintype κ]
    (Ω : ι → κ → ℝ) (w : ι → ℝ) (lam : ℝ)
    (hW : totalWeight w ≠ 0)
    (hcenter : ∀ k,
      Finset.univ.sum (fun i => w i * Ω i k) = 0) :
    ∀ i k,
      jumpGenerator (completeRate w lam) (fun j => Ω j k) i
        = -lam * Ω i k := by
  intro i k
  exact completeRate_eigen_of_weightedMean_zero
    (w := w) (f := fun j => Ω j k) (lam := lam) (i := i)
    hW (hcenter k)

/-- Conversely, every nonzero coordinate eigenmode of a reversible
conductance operator is weighted centered. -/
theorem reversible_coordinate_exactness_implies_centered
    {κ : Type*} [Fintype κ]
    (γ : ι → ι → ℝ) (Ω : ι → κ → ℝ) (w : ι → ℝ) (lam : ℝ)
    (hγsymm : ∀ i j, γ i j = γ j i)
    (hw : ∀ i, w i ≠ 0)
    (hlam : lam ≠ 0)
    (heigen : ∀ i k,
      jumpGenerator (conductanceRate γ w) (fun j => Ω j k) i
        = -lam * Ω i k) :
    ∀ k, Finset.univ.sum (fun i => w i * Ω i k) = 0 := by
  intro k
  exact conductance_eigen_implies_weightedMean_zero
    (γ := γ) (w := w) (f := fun i => Ω i k) (lam := lam)
    hγsymm hw hlam (fun i => heigen i k)

end AFPBarrier

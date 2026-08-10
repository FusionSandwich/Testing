import AFPBarrier.JumpGenerator

/-!
# Spectral products for finite jump generators

The identities in this file are purely algebraic: rates may have either sign.
Positivity is needed only for later probabilistic interpretations of the
carré du champ.
-/

open scoped BigOperators

namespace AFPBarrier

variable {ι : Type*} [Fintype ι] [DecidableEq ι]

/-- The polarized carré du champ.  The existing `carreDuChamp` is twice the
usual diagonal convention; this polarized form includes the factor `1 / 2`.
-/
noncomputable def mixedCarreDuChamp
    (a : ι → ι → ℝ) (f g : ι → ℝ) (i : ι) : ℝ :=
  (1 / 2 : ℝ) * (offdiag i).sum
    (fun j => a i j * (f j - f i) * (g j - g i))

/-- A jump generator commutes with finite sums. -/
theorem jumpGenerator_finset_sum
    {κ : Type*} (a : ι → ι → ℝ) (s : Finset κ)
    (f : κ → ι → ℝ) (i : ι) :
    jumpGenerator a (fun j => s.sum (fun k => f k j)) i =
      s.sum (fun k => jumpGenerator a (f k) i) := by
  classical
  unfold jumpGenerator
  calc
    (offdiag i).sum (fun j =>
        a i j * (s.sum (fun k => f k j) - s.sum (fun k => f k i))) =
        (offdiag i).sum (fun j =>
          s.sum (fun k => a i j * (f k j - f k i))) := by
            apply Finset.sum_congr rfl
            intro j hj
            rw [← Finset.mul_sum, Finset.sum_sub_distrib]
    _ = s.sum (fun k =>
          (offdiag i).sum (fun j => a i j * (f k j - f k i))) := by
            rw [Finset.sum_comm]

/-- A jump generator commutes with multiplication by a scalar. -/
theorem jumpGenerator_const_mul
    (a : ι → ι → ℝ) (c : ℝ) (f : ι → ℝ) (i : ι) :
    jumpGenerator a (fun j => c * f j) i = c * jumpGenerator a f i := by
  classical
  unfold jumpGenerator
  calc
    (offdiag i).sum (fun j => a i j * (c * f j - c * f i)) =
        (offdiag i).sum (fun j => c * (a i j * (f j - f i))) := by
          apply Finset.sum_congr rfl
          intro j hj
          ring
    _ = c * (offdiag i).sum (fun j => a i j * (f j - f i)) := by
          rw [Finset.mul_sum]

/-- Exact product rule, valid without a sign assumption on the rates. -/
theorem jumpGenerator_product_identity
    (a : ι → ι → ℝ) (f g : ι → ℝ) (i : ι) :
    jumpGenerator a (fun j => f j * g j) i
        - f i * jumpGenerator a g i
        - g i * jumpGenerator a f i
      = 2 * mixedCarreDuChamp a f g i := by
  classical
  simp only [jumpGenerator, mixedCarreDuChamp]
  rw [Finset.mul_sum, Finset.mul_sum]
  rw [← Finset.sum_sub_distrib, ← Finset.sum_sub_distrib]
  have htwo :
      2 * ((1 / 2 : ℝ) * (offdiag i).sum
        (fun j => a i j * (f j - f i) * (g j - g i))) =
        (offdiag i).sum
          (fun j => a i j * (f j - f i) * (g j - g i)) := by
    ring
  rw [htwo]
  apply Finset.sum_congr rfl
  intro j hj
  ring

/-- Pointwise arbitrary-target residual for a product of two eigenfunctions.
The centering convention is always `f * g - c`.
-/
theorem spectralProduct_arbitraryTarget
    (a : ι → ι → ℝ) (f g : ι → ℝ)
    (lambda nu mu c : ℝ) (i : ι)
    (hf : jumpGenerator a f i = -lambda * f i)
    (hg : jumpGenerator a g i = -nu * g i) :
    jumpGenerator a (fun j => f j * g j - c) i
          + mu * (f i * g i - c)
      = 2 * mixedCarreDuChamp a f g i
          + (mu - lambda - nu) * (f i * g i) - mu * c := by
  rw [jumpGenerator_sub_const]
  have hprod := jumpGenerator_product_identity a f g i
  rw [hf, hg] at hprod
  linarith

/-- At product-sum resonance, exactness is equivalent to a constant polarized
carré du champ. -/
theorem spectralProduct_resonance_iff
    (a : ι → ι → ℝ) (f g : ι → ℝ)
    (lambda nu c : ℝ)
    (hf : ∀ i, jumpGenerator a f i = -lambda * f i)
    (hg : ∀ i, jumpGenerator a g i = -nu * g i) :
    (∀ i, jumpGenerator a (fun j => f j * g j - c) i =
        -(lambda + nu) * (f i * g i - c)) ↔
      (∀ i, 2 * mixedCarreDuChamp a f g i = (lambda + nu) * c) := by
  constructor
  · intro hexact i
    have h := spectralProduct_arbitraryTarget
      a f g lambda nu (lambda + nu) c i (hf i) (hg i)
    rw [hexact i] at h
    linarith
  · intro hgamma i
    have h := spectralProduct_arbitraryTarget
      a f g lambda nu (lambda + nu) c i (hf i) (hg i)
    rw [hgamma i] at h
    linarith

/-- The polarized convention agrees with half of the existing diagonal
`carreDuChamp` convention. -/
theorem two_mixedCarreDuChamp_self
    (a : ι → ι → ℝ) (f : ι → ℝ) (i : ι) :
    2 * mixedCarreDuChamp a f f i = carreDuChamp a f i := by
  simp only [mixedCarreDuChamp, carreDuChamp]
  have htwo :
      2 * ((1 / 2 : ℝ) * (offdiag i).sum
        (fun j => a i j * (f j - f i) * (f j - f i))) =
        (offdiag i).sum
          (fun j => a i j * (f j - f i) * (f j - f i)) := by
    ring
  rw [htwo]
  apply Finset.sum_congr rfl
  intro j hj
  ring

/-- A centered square is resonant at the doubled eigenvalue exactly when its
carré du champ is the constant `lambda * c`. -/
theorem spectralSquare_resonance_iff
    (a : ι → ι → ℝ) (f : ι → ℝ) (lambda c : ℝ)
    (hf : ∀ i, jumpGenerator a f i = -lambda * f i) :
    (∀ i, jumpGenerator a (fun j => (f j) ^ 2 - c) i =
        -(2 * lambda) * ((f i) ^ 2 - c)) ↔
      (∀ i, mixedCarreDuChamp a f f i = lambda * c) := by
  constructor
  · intro hsquare
    have hproduct :
        ∀ i, jumpGenerator a (fun j => f j * f j - c) i =
          -(lambda + lambda) * (f i * f i - c) := by
      intro i
      convert hsquare i using 1 <;> simp only [pow_two] <;> ring
    have hgamma :=
      (spectralProduct_resonance_iff a f f lambda lambda c hf hf).mp hproduct
    intro i
    have := hgamma i
    linarith
  · intro hhalf
    have hgamma :
        ∀ i, 2 * mixedCarreDuChamp a f f i = (lambda + lambda) * c := by
      intro i
      have := hhalf i
      linarith
    have hproduct :=
      (spectralProduct_resonance_iff a f f lambda lambda c hf hf).mpr hgamma
    intro i
    convert hproduct i using 1 <;> simp only [pow_two] <;> ring

end AFPBarrier

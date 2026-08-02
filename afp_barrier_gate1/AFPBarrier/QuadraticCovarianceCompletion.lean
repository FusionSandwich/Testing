import AFPBarrier.QuadraticCovariance
import AFPBarrier.ReversibleConductance

/-!
# Compatibility layer for the verified Prompt 2 completion

The later corrective covariance module uses `finiteQuadraticSample` and
`quadraticCovarianceContraction`.  The independently verified Prompt 2
completion used the names `sampledQuadratic` and
`quadraticCovariancePairing`.  This module identifies the two APIs and retains
the weighted-centering consequences without replacing either proof line.
-/

open scoped BigOperators

namespace AFPBarrier

variable {ι κ : Type*}
  [Fintype ι] [DecidableEq ι] [Fintype κ]

/-- Prompt 2 completion name for the finite quadratic sample. -/
def sampledQuadratic
    (A : κ → κ → ℝ) (x : ι → κ → ℝ) (i : ι) : ℝ :=
  finiteQuadraticSample A x i

/-- Prompt 2 completion name for covariance contraction. -/
def quadraticCovariancePairing
    (a : ι → ι → ℝ) (A : κ → κ → ℝ)
    (x : ι → κ → ℝ) (i : ι) : ℝ :=
  quadraticCovarianceContraction A a x i

/-- Covariance identity in the completion API. -/
theorem jumpGenerator_sampledQuadratic
    (a : ι → ι → ℝ) (A : κ → κ → ℝ)
    (x : ι → κ → ℝ) (lambda : ℝ)
    (hx : ∀ p i, jumpGenerator a (fun j => x j p) i =
      -lambda * x i p)
    (i : ι) :
    jumpGenerator a (sampledQuadratic A x) i =
      -2 * lambda * sampledQuadratic A x i +
        quadraticCovariancePairing a A x i := by
  simpa [sampledQuadratic, quadraticCovariancePairing] using
    (jumpGenerator_quadratic_covariance_identity
      (a := a) (A := A) (Φ := x) (i := i) (lam := lambda)
      (fun p => hx p i))

/-- Arbitrary-target shifted residual in the completion API. -/
theorem sampledQuadratic_arbitraryTarget
    (a : ι → ι → ℝ) (A : κ → κ → ℝ)
    (x : ι → κ → ℝ) (lambda mu c : ℝ)
    (hx : ∀ p i, jumpGenerator a (fun j => x j p) i =
      -lambda * x i p)
    (i : ι) :
    jumpGenerator a (fun j => sampledQuadratic A x j - c) i
          + mu * (sampledQuadratic A x i - c)
      = quadraticCovariancePairing a A x i
          + (mu - 2 * lambda) * sampledQuadratic A x i - mu * c := by
  rw [jumpGenerator_sub_const]
  rw [jumpGenerator_sampledQuadratic a A x lambda hx i]
  ring

/-- Pointwise target exactness is equivalent to the displayed covariance
residual, including the zero-target case. -/
theorem sampledQuadratic_eigen_iff
    (a : ι → ι → ℝ) (A : κ → κ → ℝ)
    (x : ι → κ → ℝ) (lambda mu c : ℝ)
    (hx : ∀ p i, jumpGenerator a (fun j => x j p) i =
      -lambda * x i p) :
    (∀ i, jumpGenerator a (fun j => sampledQuadratic A x j - c) i =
        -mu * (sampledQuadratic A x i - c)) ↔
      (∀ i, quadraticCovariancePairing a A x i
          + (mu - 2 * lambda) * sampledQuadratic A x i - mu * c = 0) := by
  constructor
  · intro hexact i
    have h := sampledQuadratic_arbitraryTarget
      a A x lambda mu c hx i
    rw [hexact i] at h
    linarith
  · intro hres i
    have h := sampledQuadratic_arbitraryTarget
      a A x lambda mu c hx i
    rw [hres i] at h
    linarith

/-- Detailed balance implies weighted conservation. -/
theorem weighted_sum_jumpGenerator_eq_zero_of_detailedBalance
    (a : ι → ι → ℝ) (w f : ι → ℝ)
    (hw : ∀ i, w i ≠ 0)
    (hbalance : ∀ i j, w i * a i j = w j * a j i) :
    Finset.univ.sum (fun i => w i * jumpGenerator a f i) = 0 := by
  let γ : ι → ι → ℝ := fun i j => w i * a i j
  have hγsymm : ∀ i j, γ i j = γ j i := by
    intro i j
    exact hbalance i j
  have hrates : conductanceRate γ w = a := by
    funext i j
    simp only [conductanceRate, γ]
    field_simp [hw i]
  have hconservation :=
    weighted_sum_jumpGenerator_conductanceRate_eq_zero
      (γ := γ) (w := w) (f := f) hγsymm hw
  simpa only [hrates] using hconservation

/-- A nonzero detailed-balance eigenmode has zero weighted mean. -/
theorem detailedBalance_eigen_implies_weightedMean_zero
    (a : ι → ι → ℝ) (w f : ι → ℝ) (mu : ℝ)
    (hw : ∀ i, w i ≠ 0)
    (hbalance : ∀ i j, w i * a i j = w j * a j i)
    (hmu : mu ≠ 0)
    (heigen : ∀ i, jumpGenerator a f i = -mu * f i) :
    Finset.univ.sum (fun i => w i * f i) = 0 := by
  have hsum := weighted_sum_jumpGenerator_eq_zero_of_detailedBalance
    a w f hw hbalance
  have hrewrite :
      Finset.univ.sum (fun i => w i * jumpGenerator a f i) =
        -mu * Finset.univ.sum (fun i => w i * f i) := by
    calc
      Finset.univ.sum (fun i => w i * jumpGenerator a f i) =
          Finset.univ.sum (fun i => w i * (-mu * f i)) := by
            apply Finset.sum_congr rfl
            intro i hi
            rw [heigen i]
      _ = -mu * Finset.univ.sum (fun i => w i * f i) := by
            rw [Finset.mul_sum]
            apply Finset.sum_congr rfl
            intro i hi
            ring
  rw [hrewrite] at hsum
  exact (mul_eq_zero.mp hsum).resolve_left (neg_ne_zero.mpr hmu)

/-- A nonzero reversible quadratic target fixes its centering constant as the
weighted sample mean. -/
theorem sampledQuadratic_center_eq_weightedMean
    [Nonempty ι]
    (a : ι → ι → ℝ) (A : κ → κ → ℝ)
    (x : ι → κ → ℝ) (w : ι → ℝ) (mu c : ℝ)
    (hw : ∀ i, 0 < w i)
    (hbalance : ∀ i j, w i * a i j = w j * a j i)
    (hmu : mu ≠ 0)
    (heigen : ∀ i,
      jumpGenerator a (fun j => sampledQuadratic A x j - c) i =
        -mu * (sampledQuadratic A x i - c)) :
    c = Finset.univ.sum (fun i => w i * sampledQuadratic A x i) /
        Finset.univ.sum (fun i => w i) := by
  classical
  have hwne : ∀ i, w i ≠ 0 := fun i => ne_of_gt (hw i)
  have hmean := detailedBalance_eigen_implies_weightedMean_zero
    a w (fun i => sampledQuadratic A x i - c) mu hwne hbalance hmu heigen
  have hweights_pos : 0 < Finset.univ.sum (fun i => w i) := by
    exact Finset.sum_pos (fun i hi => hw i) Finset.univ_nonempty
  have hweights_ne : Finset.univ.sum (fun i => w i) ≠ 0 :=
    ne_of_gt hweights_pos
  have hexpand :
      Finset.univ.sum
          (fun i => w i * (sampledQuadratic A x i - c)) =
        Finset.univ.sum (fun i => w i * sampledQuadratic A x i) -
          c * Finset.univ.sum (fun i => w i) := by
    calc
      Finset.univ.sum
          (fun i => w i * (sampledQuadratic A x i - c)) =
          Finset.univ.sum
            (fun i => w i * sampledQuadratic A x i - c * w i) := by
              apply Finset.sum_congr rfl
              intro i hi
              ring
      _ = Finset.univ.sum (fun i => w i * sampledQuadratic A x i) -
          Finset.univ.sum (fun i => c * w i) := by
            rw [Finset.sum_sub_distrib]
      _ = Finset.univ.sum (fun i => w i * sampledQuadratic A x i) -
          c * Finset.univ.sum (fun i => w i) := by rw [Finset.mul_sum]
  rw [hexpand] at hmean
  rw [eq_div_iff hweights_ne]
  linarith

/-- At target zero, changing the centering constant does not change
harmonicity. -/
theorem sampledQuadratic_zeroTarget_center_independent
    (a : ι → ι → ℝ) (A : κ → κ → ℝ)
    (x : ι → κ → ℝ) (c c' : ℝ) :
    (∀ i, jumpGenerator a (fun j => sampledQuadratic A x j - c) i = 0) ↔
      (∀ i, jumpGenerator a (fun j => sampledQuadratic A x j - c') i = 0) := by
  constructor <;> intro h i
  · rw [jumpGenerator_sub_const]
    simpa only [jumpGenerator_sub_const] using h i
  · rw [jumpGenerator_sub_const]
    simpa only [jumpGenerator_sub_const] using h i

end AFPBarrier

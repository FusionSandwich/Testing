import AFPBarrier.SpectralProductAlgebra
import AFPBarrier.ReversibleConductance

/-!
# Quadratic covariance identity

This module separates a coefficient matrix from the finite function obtained
by sampling its quadratic form.  No positivity or symmetry assumption on the
matrix or rates is used by the algebraic identity.
-/

open scoped BigOperators

namespace AFPBarrier

variable {ι κ : Type*}
  [Fintype ι] [DecidableEq ι] [Fintype κ]

/-- Sample the (not necessarily symmetric) coefficient matrix `A` on `x`. -/
def sampledQuadratic
    (A : κ → κ → ℝ) (x : ι → κ → ℝ) (i : ι) : ℝ :=
  Finset.univ.sum (fun p =>
    Finset.univ.sum (fun q => A p q * x i p * x i q))

/-- Pair `A` with the row covariance
`sum_j a_ij (x_j-x_i)(x_j-x_i)^T`. -/
def quadraticCovariancePairing
    (a : ι → ι → ℝ) (A : κ → κ → ℝ)
    (x : ι → κ → ℝ) (i : ι) : ℝ :=
  Finset.univ.sum (fun p =>
    Finset.univ.sum (fun q => A p q *
      ((offdiag i).sum (fun j =>
        a i j * (x j p - x i p) * (x j q - x i q)))))

/-- Finite covariance identity

`L (x^T A x) = -2 lambda (x^T A x) + <A,C>`

for a coordinate eigenmap.  This theorem is purely algebraic.
-/
theorem jumpGenerator_sampledQuadratic
    (a : ι → ι → ℝ) (A : κ → κ → ℝ)
    (x : ι → κ → ℝ) (lambda : ℝ)
    (hx : ∀ p i, jumpGenerator a (fun j => x j p) i =
      -lambda * x i p)
    (i : ι) :
    jumpGenerator a (sampledQuadratic A x) i =
      -2 * lambda * sampledQuadratic A x i +
        quadraticCovariancePairing a A x i := by
  classical
  unfold sampledQuadratic quadraticCovariancePairing
  rw [jumpGenerator_finset_sum]
  rw [Finset.mul_sum]
  rw [← Finset.sum_add_distrib]
  apply Finset.sum_congr rfl
  intro p hp
  rw [jumpGenerator_finset_sum]
  rw [Finset.mul_sum]
  rw [← Finset.sum_add_distrib]
  apply Finset.sum_congr rfl
  intro q hq
  rw [show (fun j => A p q * x j p * x j q) =
      (fun j => A p q * (x j p * x j q)) by
        funext j
        ring]
  rw [jumpGenerator_const_mul]
  have hprod := jumpGenerator_product_identity a
    (fun j => x j p) (fun j => x j q) i
  rw [hx p i, hx q i] at hprod
  have hgamma :
      2 * mixedCarreDuChamp a (fun j => x j p) (fun j => x j q) i =
        (offdiag i).sum (fun j =>
          a i j * (x j p - x i p) * (x j q - x i q)) := by
    simp only [mixedCarreDuChamp]
    ring
  rw [hgamma] at hprod
  calc
    A p q * jumpGenerator a (fun j => x j p * x j q) i =
        A p q * (-2 * lambda * (x i p * x i q) +
          (offdiag i).sum (fun j =>
            a i j * (x j p - x i p) * (x j q - x i q))) := by
              congr 1
              linarith
    _ = -2 * lambda * (A p q * x i p * x i q) +
          A p q * (offdiag i).sum (fun j =>
            a i j * (x j p - x i p) * (x j q - x i q)) := by ring

/-- The arbitrary-target centered quadratic residual, with the centering
constant displayed explicitly. -/
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

/-- Pointwise eigenfunction exactness is equivalent to vanishing of the
displayed covariance residual.  This also covers `mu = 0`; in that exceptional
case the residual is independent of `c`.
-/
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

/-- Detailed balance implies conservation of the weighted sum.  This version
is stated for arbitrary reversible rates, rather than requiring callers to
present the rates in conductance-normalized form. -/
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

/-- A nonzero eigenmode of a finite detailed-balance generator has zero
weighted mean. -/
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

/-- Exact necessary centering for a nonzero quadratic target eigenmode on a
nonempty positive-weight reversible state space.  Pointwise covariance
exactness remains a separate condition. -/
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

/-- At target `mu = 0`, changing the centering constant does not change
harmonicity.  In particular weighted conservation cannot determine `c`. -/
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

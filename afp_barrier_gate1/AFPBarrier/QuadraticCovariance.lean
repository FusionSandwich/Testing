import AFPBarrier.SpectralProductAlgebra

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

end AFPBarrier

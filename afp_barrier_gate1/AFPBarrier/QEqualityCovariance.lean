import AFPBarrier.QuantitativeGlobalNearRigidity
import Mathlib.Tactic

/-!
# Covariance consequences of spherical `Q=1`

The module formalizes the finite scalar/entrywise algebra behind the exact
radial--tangential decomposition.  Matrix and sampling-map conclusions are
stated and proved in the ordinary theorem document.
-/

open scoped BigOperators

namespace AFPBarrier

variable {ι κ : Type*}
variable [Fintype ι] [DecidableEq ι]

/-- Trace as a weighted sum of squared displacement norms is four when the
normal loss moment is two and `|Omega_j-Omega_i|^2=2 ell_ij`. -/
theorem covarianceTrace_eq_four_of_normLoss
    (a loss normDiffSq : ι → ι → ℝ) (i : ι)
    (hnorm : ∀ j ∈ offdiag i, normDiffSq i j = 2 * loss i j)
    (hmoment : (offdiag i).sum (fun j => a i j * loss i j) = 2) :
    (offdiag i).sum (fun j => a i j * normDiffSq i j) = 4 := by
  calc
    (offdiag i).sum (fun j => a i j * normDiffSq i j)
        = (offdiag i).sum (fun j => a i j * (2 * loss i j)) := by
            apply Finset.sum_congr rfl
            intro j hj
            rw [hnorm j hj]
    _ = 2 * (offdiag i).sum (fun j => a i j * loss i j) := by
          rw [Finset.mul_sum]
          apply Finset.sum_congr rfl
          intro j hj
          ring
    _ = 4 := by rw [hmoment]; norm_num

/-- The covariance radial quadratic form is the spherical second loss moment
when the radial displacement is `-ell_ij`. -/
theorem radialCovariance_eq_sphericalEpsilon
    (a loss radialDiff : ι → ι → ℝ) (i : ι)
    (hradial : ∀ j ∈ offdiag i, radialDiff i j = -loss i j) :
    (offdiag i).sum (fun j => a i j * (radialDiff i j) ^ 2)
      = sphericalEpsilonAt a loss i := by
  unfold sphericalEpsilonAt
  apply Finset.sum_congr rfl
  intro j hj
  rw [hradial j hj]
  ring

/-- Rearrangement of `Q=r epsilon/4`: the radial covariance is `4Q/r`. -/
theorem sphericalEpsilon_eq_four_mul_Q_div_rate
    (a loss : ι → ι → ℝ) (i : ι)
    (hrate : 0 < jumpRate a i) :
    sphericalEpsilonAt a loss i
      = 4 * sphericalQAt a loss i / jumpRate a i := by
  have hrne : jumpRate a i ≠ 0 := ne_of_gt hrate
  unfold sphericalQAt
  field_simp [hrne]
  ring

/-- A centered weighted affine product has only its constant and second-moment
terms. -/
theorem weighted_centered_affine_product_sum
    (s : Finset ι) (p u v : ι → ℝ)
    (A B C D : ℝ)
    (hsum : s.sum p = 1)
    (hcenterU : s.sum (fun j => p j * u j) = 0)
    (hcenterV : s.sum (fun j => p j * v j) = 0) :
    s.sum (fun j => p j * ((A + B * u j) * (C + D * v j)))
      = A * C + B * D * s.sum (fun j => p j * u j * v j) := by
  calc
    s.sum (fun j => p j * ((A + B * u j) * (C + D * v j)))
        = s.sum (fun j =>
            p j * A * C
              + (A * D) * (p j * v j)
              + (B * C) * (p j * u j)
              + (B * D) * (p j * u j * v j)) := by
                apply Finset.sum_congr rfl
                intro j hj
                ring
    _ = s.sum (fun j => p j * A * C)
          + s.sum (fun j => (A * D) * (p j * v j))
          + s.sum (fun j => (B * C) * (p j * u j))
          + s.sum (fun j => (B * D) * (p j * u j * v j)) := by
            simp only [Finset.sum_add_distrib]
    _ = (s.sum p) * A * C
          + (A * D) * s.sum (fun j => p j * v j)
          + (B * C) * s.sum (fun j => p j * u j)
          + (B * D) * s.sum (fun j => p j * u j * v j) := by
            congr 1
            · rw [← Finset.sum_mul, ← Finset.sum_mul]
            · rw [Finset.mul_sum]
            · rw [Finset.mul_sum]
            · rw [Finset.mul_sum]
    _ = A * C + B * D * s.sum (fun j => p j * u j * v j) := by
          rw [hsum, hcenterU, hcenterV]
          ring

/-- Entrywise exact `Q=1` covariance decomposition.  The displacement is
`-ell*omega + sigma*u`; centered tangent directions remove the mixed blocks. -/
theorem qOne_covarianceEntry_decomposition
    (s : Finset ι) (p : ι → ℝ) (u : ι → κ → ℝ)
    (omega : κ → ℝ) (k l : κ)
    (rate ell sigma : ℝ)
    (hsum : s.sum p = 1)
    (hcenterK : s.sum (fun j => p j * u j k) = 0)
    (hcenterL : s.sum (fun j => p j * u j l) = 0)
    (hrateLoss : rate * ell = 2)
    (hsigma : sigma ^ 2 = ell * (2 - ell)) :
    rate * s.sum (fun j =>
      p j *
        ((-ell * omega k + sigma * u j k) *
          (-ell * omega l + sigma * u j l)))
      = 2 * (2 - ell) * s.sum (fun j => p j * u j k * u j l)
          + 2 * ell * omega k * omega l := by
  have hcentered := weighted_centered_affine_product_sum
    (s := s) (p := p) (u := fun j => u j k) (v := fun j => u j l)
    (A := -ell * omega k) (B := sigma)
    (C := -ell * omega l) (D := sigma)
    hsum hcenterK hcenterL
  rw [hcentered]
  rw [hsigma]
  calc
    rate *
        ((-ell * omega k) * (-ell * omega l)
          + ell * (2 - ell) * s.sum (fun j => p j * u j k * u j l))
        = (rate * ell) * ell * omega k * omega l
            + (rate * ell) * (2 - ell) *
                s.sum (fun j => p j * u j k * u j l) := by ring
    _ = 2 * (2 - ell) * s.sum (fun j => p j * u j k * u j l)
          + 2 * ell * omega k * omega l := by
            rw [hrateLoss]
            ring

/-- Because the tangential coefficient is positive for `ell<2`, equality with
an axially isotropic tangent entry is equivalent to tangent isotropy itself. -/
theorem qOne_tangent_entry_isotropic_iff
    (ell T target radial : ℝ)
    (hell : ell < 2) :
    2 * (2 - ell) * T + radial =
        2 * (2 - ell) * target + radial ↔ T = target := by
  constructor
  · intro h
    have hcoeff : 0 < 2 * (2 - ell) := by nlinarith
    nlinarith
  · intro h
    rw [h]

/-- The two tangent probabilities at a weighted octahedral axis sum to one. -/
theorem weightedOctahedron_tangentWeights_sum_one
    (g₁ g₂ : ℝ) (hsum : 0 < g₁ + g₂) :
    g₁ / (g₁ + g₂) + g₂ / (g₁ + g₂) = 1 := by
  field_simp [ne_of_gt hsum]
  ring

/-- At one weighted octahedral axis, equal tangent weights are equivalent to
equal conductances. -/
theorem weightedOctahedron_axis_axial_iff
    (g₁ g₂ : ℝ) (hsum : 0 < g₁ + g₂) :
    g₁ / (g₁ + g₂) = g₂ / (g₁ + g₂) ↔ g₁ = g₂ := by
  have hne : g₁ + g₂ ≠ 0 := ne_of_gt hsum
  constructor
  · intro h
    field_simp [hne] at h
    linarith
  · intro h
    rw [h]

end AFPBarrier

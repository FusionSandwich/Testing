import AFPBarrier.ReversibleConductance
import Mathlib.Tactic

/-!
# Finite construction identities for the asymptotic quadratic family

This module contains the division-safe finite algebra used by the P1E
construction.  The analytic mesh construction and its uniform constants live
in the ordinary proof; the statements here certify the identities that turn a
shared positive moment stress into a reversible generator with exact linear
reproduction.  No injectivity of a sampling map is used.
-/

open scoped BigOperators

namespace AFPBarrier

variable {I J K E : Type*}
  [Fintype I] [DecidableEq I]
  [Fintype J] [DecidableEq J]
  [Fintype K] [DecidableEq K]
  [Fintype E] [DecidableEq E]

/-- Entrywise projected tangent increment.  In the spherical application
`ell j = 1 - <omega, omega_j>` and hence
`omega_j - omega = tau_j - ell_j omega`. -/
def constructionTangentIncrement
    (omega : K → ℝ) (neighbor : J → K → ℝ)
    (ell : J → ℝ) (j : J) (p : K) : ℝ :=
  neighbor j p - omega p + ell j * omega p

/-- Every jump-form row annihilates constants.  This is the finite `H_0`
identity used by the construction and requires no positivity or division. -/
theorem construction_constant_reproduction
    (gamma : J → ℝ) (constant : ℝ) :
    ∑ j, gamma j * (constant - constant) = 0 := by
  simp

/-- The radial--tangent decomposition used by the construction, stated
entrywise so it does not depend on a choice of matrix representation. -/
theorem construction_increment_decomposition
    (omega : K → ℝ) (neighbor : J → K → ℝ)
    (ell : J → ℝ) (j : J) (p : K) :
    neighbor j p - omega p =
      constructionTangentIncrement omega neighbor ell j p -
        ell j * omega p := by
  simp only [constructionTangentIncrement]
  ring

/-- Tangent force zero together with the radial mass identity gives the exact
coordinate force.  This is the finite core of exact `H_1` reproduction before
division by the vertex mass. -/
theorem tangentForce_zero_radialMass_exactForce
    (gamma ell : J → ℝ)
    (omega : K → ℝ) (neighbor : J → K → ℝ)
    (n mu : ℝ)
    (htangent : ∀ p,
      ∑ j, gamma j *
        constructionTangentIncrement omega neighbor ell j p = 0)
    (hradial : ∑ j, gamma j * ell j = n * mu) :
    ∀ p, ∑ j, gamma j * (neighbor j p - omega p) =
      -n * mu * omega p := by
  intro p
  calc
    (∑ j, gamma j * (neighbor j p - omega p)) =
        ∑ j, gamma j *
          (constructionTangentIncrement omega neighbor ell j p -
            ell j * omega p) := by
              apply Finset.sum_congr rfl
              intro j hj
              rw [construction_increment_decomposition]
    _ =
        ∑ j, (gamma j *
          constructionTangentIncrement omega neighbor ell j p -
            (gamma j * ell j) * omega p) := by
              apply Finset.sum_congr rfl
              intro j hj
              ring
    _ =
        (∑ j, gamma j *
          constructionTangentIncrement omega neighbor ell j p) -
          (∑ j, gamma j * ell j) * omega p := by
            rw [Finset.sum_sub_distrib, Finset.sum_mul]
    _ = -n * mu * omega p := by rw [htangent p, hradial]; ring

/-- After division by a nonzero vertex mass, the exact force identity is the
scalar coordinate eigen-equation `L omega_p = -n omega_p`. -/
theorem tangentForce_zero_radialMass_hOne
    (gamma ell : J → ℝ)
    (omega : K → ℝ) (neighbor : J → K → ℝ)
    (n mu : ℝ) (hmu : mu ≠ 0)
    (htangent : ∀ p,
      ∑ j, gamma j *
        constructionTangentIncrement omega neighbor ell j p = 0)
    (hradial : ∑ j, gamma j * ell j = n * mu) :
    ∀ p, (∑ j, gamma j * (neighbor j p - omega p)) / mu =
      -n * omega p := by
  intro p
  rw [tangentForce_zero_radialMass_exactForce
    gamma ell omega neighbor n mu htangent hradial p]
  field_simp [hmu]

/-- The detailed-balance cancellation associated with one shared symmetric
edge coefficient.  Positivity is not needed for this algebraic identity. -/
theorem sharedConductance_detailedBalance_entry
    (gammaIJ gammaJI wi wj : ℝ)
    (hsymm : gammaIJ = gammaJI)
    (hwi : wi ≠ 0) (hwj : wj ≠ 0) :
    wi * (gammaIJ / wi) = wj * (gammaJI / wj) := by
  calc
    wi * (gammaIJ / wi) = gammaIJ := by field_simp [hwi]
    _ = gammaJI := hsymm
    _ = wj * (gammaJI / wj) := by field_simp [hwj]

/-- Dividing an unnormalized moment identity by its nonzero mass yields the
normalized entry.  Keeping this lemma scalar makes it reusable for vector and
matrix entries without importing a coordinate convention. -/
theorem unnormalizedMoment_div_mass_entry
    (raw mu target : ℝ) (hmu : mu ≠ 0)
    (hraw : raw = mu * target) :
    raw / mu = target := by
  rw [hraw]
  field_simp [hmu]

/-- Finite-sum form of `unnormalizedMoment_div_mass_entry`. -/
theorem unnormalizedMomentSum_div_mass_entry
    (gamma phi : J → ℝ) (mu target : ℝ) (hmu : mu ≠ 0)
    (hraw : ∑ j, gamma j * phi j = mu * target) :
    (∑ j, gamma j * phi j) / mu = target := by
  exact unnormalizedMoment_div_mass_entry
    (raw := ∑ j, gamma j * phi j) (mu := mu) (target := target)
    hmu hraw

/-- A finite correction operator, written entrywise. -/
def constructionCorrectionOperator
    (kernel : I → K → E → ℝ) (u : E → ℝ) (i : I) (p : K) : ℝ :=
  ∑ e, kernel i p e * u e

/-- If the correction equation `K u = b` is solved, the corrected defect
`b - K u` vanishes exactly. -/
theorem constructionCorrection_closes
    (kernel : I → K → E → ℝ) (u : E → ℝ) (b : I → K → ℝ)
    (hsolve : ∀ i p, constructionCorrectionOperator kernel u i p = b i p) :
    ∀ i p, b i p - constructionCorrectionOperator kernel u i p = 0 := by
  intro i p
  rw [hsolve i p]
  ring

/-- Version of the correction identity that separates the base force and the
added correction force. -/
theorem constructionCorrection_force_zero
    (kernel : I → K → E → ℝ) (u : E → ℝ)
    (base correction : I → K → ℝ)
    (hbase : ∀ i p, base i p =
      constructionCorrectionOperator kernel u i p)
    (hcorrection : ∀ i p, correction i p =
      -constructionCorrectionOperator kernel u i p) :
    ∀ i p, base i p + correction i p = 0 := by
  intro i p
  rw [hbase i p, hcorrection i p]
  ring

/-- A four-point affine-coset connector is most cleanly specified by its
positive fluxes.  Equality of the total negative and positive fluxes is
exactly the vanishing first-moment equation after division by the four
positive lengths. -/
theorem fourPointConnector_firstMoment
    (a b p q alpha beta gamma delta : ℝ)
    (ha : a ≠ 0) (hb : b ≠ 0) (hp : p ≠ 0) (hq : q ≠ 0)
    (hflux : alpha + beta = gamma + delta) :
    (alpha / a) * (-a) + (beta / b) * (-b) +
      (gamma / p) * p + (delta / q) * q = 0 := by
  calc
    (alpha / a) * (-a) + (beta / b) * (-b) +
        (gamma / p) * p + (delta / q) * q =
      -alpha - beta + gamma + delta := by
        field_simp [ha, hb, hp, hq]
        <;> ring
    _ = 0 := by linarith

/-- Matching the flux-weighted squared lengths on the two sides of the same
four-point connector kills its full one-dimensional cubic moment.  Tensor
products of this identity kill every component of the multivariate cubic
tensor because each mixed cubic monomial contains a first-moment factor. -/
theorem fourPointConnector_cubicMoment
    (a b p q alpha beta gamma delta : ℝ)
    (ha : a ≠ 0) (hb : b ≠ 0) (hp : p ≠ 0) (hq : q ≠ 0)
    (hsquare : alpha * a ^ 2 + beta * b ^ 2 =
      gamma * p ^ 2 + delta * q ^ 2) :
    (alpha / a) * (-a) ^ 3 + (beta / b) * (-b) ^ 3 +
      (gamma / p) * p ^ 3 + (delta / q) * q ^ 3 = 0 := by
  calc
    (alpha / a) * (-a) ^ 3 + (beta / b) * (-b) ^ 3 +
        (gamma / p) * p ^ 3 + (delta / q) * q ^ 3 =
      -alpha * a ^ 2 - beta * b ^ 2 +
        gamma * p ^ 2 + delta * q ^ 2 := by
          field_simp [ha, hb, hp, hq]
          <;> ring
    _ = 0 := by nlinarith

/-- Positive flux divided by a positive connector length remains a strictly
positive shared conductance. -/
theorem fourPointConnector_weight_pos
    (flux length : ℝ) (hflux : 0 < flux) (hlength : 0 < length) :
    0 < flux / length := by
  exact div_pos hflux hlength

/-- A positive lower chord bound converts the radial mass identity into the
division-free outgoing-conductance bound. -/
theorem chordMass_outgoingConductance_bound
    (gamma ell : J → ℝ) (ellMin n mu : ℝ)
    (hgamma : ∀ j, 0 ≤ gamma j)
    (hell : ∀ j, ellMin ≤ ell j)
    (hradial : ∑ j, gamma j * ell j = n * mu) :
    ellMin * (∑ j, gamma j) ≤ n * mu := by
  calc
    ellMin * (∑ j, gamma j) =
        ∑ j, gamma j * ellMin := by
          rw [Finset.mul_sum]
          apply Finset.sum_congr rfl
          intro j hj
          ring
    _ ≤ ∑ j, gamma j * ell j := by
      apply Finset.sum_le_sum
      intro j hj
      exact mul_le_mul_of_nonneg_left (hell j) (hgamma j)
    _ = n * mu := hradial

/-- Normalizing by the positive mass gives the exact rate bound
`sum gamma / mu <= n / ellMin`. -/
theorem chordMass_normalizedRate_bound
    (gamma ell : J → ℝ) (ellMin n mu : ℝ)
    (hgamma : ∀ j, 0 ≤ gamma j)
    (hellMin : 0 < ellMin) (hmu : 0 < mu)
    (hell : ∀ j, ellMin ≤ ell j)
    (hradial : ∑ j, gamma j * ell j = n * mu) :
    (∑ j, gamma j) / mu ≤ n / ellMin := by
  apply (div_le_div_iff₀ hmu hellMin).2
  simpa [mul_comm] using
    chordMass_outgoingConductance_bound
      gamma ell ellMin n mu hgamma hell hradial

/-- Scalar nearest-neighbor recurrence for the degree-one samples on a
regular polygon.  The denominator `2(1-c)` is the exact positive row scale. -/
theorem regularPolygon_hOne_scalar_recurrence
    (previous current next c : ℝ) (hc : 1 - c ≠ 0)
    (hrec : previous + next = 2 * c * current) :
    ((previous - current) + (next - current)) /
        (2 * (1 - c)) = -current := by
  apply (div_eq_iff (mul_ne_zero (by norm_num) hc)).2
  calc
    (previous - current) + (next - current) =
        (previous + next) - 2 * current := by ring
    _ = 2 * c * current - 2 * current := by rw [hrec]
    _ = -current * (2 * (1 - c)) := by ring

/-- Scalar degree-two recurrence and its exact residual on a regular polygon.
For `c = cos(alpha)`, the multiplier `2*c^2-1` is `cos(2 alpha)`;
the residual relative to the circle eigenvalue `-4` is `2(1-c)`. -/
theorem regularPolygon_hTwo_scalar_residual
    (previous current next c : ℝ) (hc : 1 - c ≠ 0)
    (hrec : previous + next = 2 * (2 * c ^ 2 - 1) * current) :
    ((previous - current) + (next - current)) /
          (2 * (1 - c)) + 4 * current =
      2 * (1 - c) * current := by
  have heigen :
      ((previous - current) + (next - current)) /
          (2 * (1 - c)) = -2 * (1 + c) * current := by
    apply (div_eq_iff (mul_ne_zero (by norm_num) hc)).2
    calc
      (previous - current) + (next - current) =
          (previous + next) - 2 * current := by ring
      _ = 2 * (2 * c ^ 2 - 1) * current - 2 * current := by
            rw [hrec]
      _ = (-2 * (1 + c) * current) * (2 * (1 - c)) := by ring
  rw [heigen]
  ring

/-- The degree-two regular-polygon recurrence itself, useful when cosine and
sine samples have already been reduced to the same scalar relation. -/
theorem regularPolygon_hTwo_scalar_eigenvalue
    (previous current next c : ℝ) (hc : 1 - c ≠ 0)
    (hrec : previous + next = 2 * (2 * c ^ 2 - 1) * current) :
    ((previous - current) + (next - current)) /
        (2 * (1 - c)) = -2 * (1 + c) * current := by
  apply (div_eq_iff (mul_ne_zero (by norm_num) hc)).2
  calc
    (previous - current) + (next - current) =
        (previous + next) - 2 * current := by ring
    _ = 2 * (2 * c ^ 2 - 1) * current - 2 * current := by
          rw [hrec]
    _ = (-2 * (1 + c) * current) * (2 * (1 - c)) := by ring

end AFPBarrier

import AFPBarrier.GlobalLossRigidity
import AFPBarrier.LossVarianceSharpness
import AFPBarrier.ReversibleConductance
import AFPBarrier.SpectralProductAlgebra
import Mathlib.Tactic

/-!
# Exact spherical `Q` equality and global propagation

This module specializes the finite loss-variance identity to a unit-sphere
coordinate eigenmap with target eigenvalue `-2`.  It keeps the coordinate
normalization, the normalized edge weights, and the equality propagation as
separate finite-algebra steps.
-/

open scoped BigOperators

namespace AFPBarrier

variable {ι : Type*} [Fintype ι] [DecidableEq ι]

/-- Coordinate pairing used by the spherical specialization. -/
def sphericalPairing
    {κ : Type*} [Fintype κ]
    (Omega : ι → κ → ℝ) (i j : ι) : ℝ :=
  ∑ p, Omega i p * Omega j p

/-- Spherical chord loss `1 - Omega_i dot Omega_j`. -/
def sphericalChordLoss
    {κ : Type*} [Fintype κ]
    (Omega : ι → κ → ℝ) (i j : ι) : ℝ :=
  1 - sphericalPairing Omega i j

/-- Spherical loss is symmetric. -/
theorem sphericalChordLoss_symmetric
    {κ : Type*} [Fintype κ]
    (Omega : ι → κ → ℝ) (i j : ι) :
    sphericalChordLoss Omega i j = sphericalChordLoss Omega j i := by
  classical
  unfold sphericalChordLoss sphericalPairing
  apply congrArg (fun t : ℝ => 1 - t)
  apply Finset.sum_congr rfl
  intro p hp
  ring

/-- Pairing a coordinate eigenmap with the base point gives the zonal
eigen-equation at that base point. -/
theorem jumpGenerator_sphericalPairing
    {κ : Type*} [Fintype κ]
    (a : ι → ι → ℝ) (Omega : ι → κ → ℝ) (i : ι)
    (hcoord : ∀ p v,
      jumpGenerator a (fun j => Omega j p) v = -2 * Omega v p) :
    jumpGenerator a (fun j => sphericalPairing Omega i j) i =
      -2 * sphericalPairing Omega i i := by
  classical
  unfold sphericalPairing
  rw [jumpGenerator_finset_sum]
  calc
    ∑ p, jumpGenerator a (fun j => Omega i p * Omega j p) i =
        ∑ p, Omega i p *
          jumpGenerator a (fun j => Omega j p) i := by
            apply Finset.sum_congr rfl
            intro p hp
            exact jumpGenerator_const_mul
              a (Omega i p) (fun j => Omega j p) i
    _ = ∑ p, Omega i p * (-2 * Omega i p) := by
          apply Finset.sum_congr rfl
          intro p hp
          rw [hcoord p i]
    _ = -2 * ∑ p, Omega i p * Omega i p := by
          rw [Finset.mul_sum]
          apply Finset.sum_congr rfl
          intro p hp
          ring

/-- The coordinate eigenmap equation and unit normalization imply the first
spherical loss moment `2`. -/
theorem coordinateEigenmap_lossMoment_two
    {κ : Type*} [Fintype κ]
    (a : ι → ι → ℝ) (Omega : ι → κ → ℝ) (i : ι)
    (hunit : sphericalPairing Omega i i = 1)
    (hcoord : ∀ p v,
      jumpGenerator a (fun j => Omega j p) v = -2 * Omega v p) :
    (offdiag i).sum (fun j => a i j * sphericalChordLoss Omega i j) = 2 := by
  have hlinear :
      jumpGenerator a (fun j => sphericalPairing Omega i j) i = -(2 : ℝ) := by
    rw [jumpGenerator_sphericalPairing a Omega i hcoord, hunit]
    norm_num
  have hm := lossMoment_eq_eigenvalue
    (a := a) (f := fun j => sphericalPairing Omega i j)
    (i := i) (lam := 2) hlinear
  simpa [sphericalChordLoss, hunit] using hm

/-- Dividing the coordinate eigenmap equation by the positive row rate gives
the normalized spherical barycenter.  Under the equality normalization
`r_i * ell = 2`, the neighbour mean is `(1-ell) Omega_i`. -/
theorem normalizedOmega_barycenter_of_coordinateEigenmap
    {κ : Type*} [Fintype κ]
    (a : ι → ι → ℝ) (Omega : ι → κ → ℝ) (i : ι)
    (ell : ℝ)
    (hrate : 0 < jumpRate a i)
    (hcoord : ∀ p v,
      jumpGenerator a (fun j => Omega j p) v = -2 * Omega v p)
    (hrateLoss : jumpRate a i * ell = 2) :
    ∀ p, (offdiag i).sum (fun j =>
      (a i j / jumpRate a i) * Omega j p) = (1 - ell) * Omega i p := by
  intro p
  have hgenerator := hcoord p i
  have hexpand :
      jumpGenerator a (fun j => Omega j p) i =
        (offdiag i).sum (fun j => a i j * Omega j p) -
          jumpRate a i * Omega i p := by
    unfold jumpGenerator jumpRate
    calc
      (offdiag i).sum (fun j => a i j * (Omega j p - Omega i p)) =
          (offdiag i).sum (fun j =>
            a i j * Omega j p - a i j * Omega i p) := by
              apply Finset.sum_congr rfl
              intro j hj
              ring
      _ = (offdiag i).sum (fun j => a i j * Omega j p) -
            (offdiag i).sum (fun j => a i j * Omega i p) := by
              rw [Finset.sum_sub_distrib]
      _ = (offdiag i).sum (fun j => a i j * Omega j p) -
            (offdiag i).sum (fun j => a i j) * Omega i p := by
              rw [Finset.sum_mul]
  have hsum :
      (offdiag i).sum (fun j => a i j * Omega j p) =
        (jumpRate a i - 2) * Omega i p := by
    rw [hexpand] at hgenerator
    linarith
  have hrne : jumpRate a i ≠ 0 := ne_of_gt hrate
  calc
    (offdiag i).sum (fun j =>
        (a i j / jumpRate a i) * Omega j p) =
        (offdiag i).sum (fun j =>
          (a i j * Omega j p) / jumpRate a i) := by
            apply Finset.sum_congr rfl
            intro j hj
            field_simp [hrne]
    _ =
        (offdiag i).sum (fun j => a i j * Omega j p) /
          jumpRate a i := by
            rw [Finset.sum_div]
    _ = ((jumpRate a i - 2) * Omega i p) / jumpRate a i := by
          rw [hsum]
    _ = (1 - ell) * Omega i p := by
          rw [← hrateLoss]
          field_simp [hrne]

/-- Spherical second loss moment at a state. -/
def sphericalEpsilonAt
    (a loss : ι → ι → ℝ) (i : ι) : ℝ :=
  (offdiag i).sum (fun j => a i j * (loss i j) ^ 2)

/-- Local quality factor `Q_i = r_i epsilon_i / 4`. -/
noncomputable def sphericalQAt
    (a loss : ι → ι → ℝ) (i : ι) : ℝ :=
  jumpRate a i * sphericalEpsilonAt a loss i / 4

/-- A nonnegative row whose first loss moment is two has positive total rate.
No sign assumption on the losses is needed. -/
theorem jumpRate_pos_of_lossMoment_two
    (a loss : ι → ι → ℝ) (i : ι)
    (ha : ∀ j, j ≠ i → 0 ≤ a i j)
    (hmoment : (offdiag i).sum (fun j => a i j * loss i j) = 2) :
    0 < jumpRate a i := by
  have hrnonneg : 0 ≤ jumpRate a i := jumpRate_nonneg a i ha
  by_contra hnot
  have hrle : jumpRate a i ≤ 0 := le_of_not_gt hnot
  have hrzero : jumpRate a i = 0 := le_antisymm hrle hrnonneg
  have hnonneg : ∀ j ∈ offdiag i, 0 ≤ a i j := by
    intro j hj
    exact ha j (Finset.mem_erase.mp hj).1
  have hrateTerms : ∀ j ∈ offdiag i, a i j = 0 := by
    unfold jumpRate at hrzero
    exact (Finset.sum_eq_zero_iff_of_nonneg hnonneg).mp hrzero
  have hlossMomentZero :
      (offdiag i).sum (fun j => a i j * loss i j) = 0 := by
    apply Finset.sum_eq_zero
    intro j hj
    rw [hrateTerms j hj]
    ring
  rw [hlossMomentZero] at hmoment
  norm_num at hmoment

/-- Normalized active weights sum to one. -/
theorem normalizedEdgeWeight_sum_one
    (a : ι → ι → ℝ) (i : ι)
    (hrate : 0 < jumpRate a i) :
    (offdiag i).sum (fun j => a i j / jumpRate a i) = 1 := by
  rw [← Finset.sum_div]
  change jumpRate a i / jumpRate a i = 1
  exact div_self (ne_of_gt hrate)

/-- The normalized loss scale has weighted mean one. -/
theorem normalizedLossScale_mean_one
    (a loss : ι → ι → ℝ) (i : ι)
    (hrate : 0 < jumpRate a i)
    (hmoment : (offdiag i).sum (fun j => a i j * loss i j) = 2) :
    (offdiag i).sum (fun j =>
      (a i j / jumpRate a i) * (jumpRate a i * loss i j / 2)) = 1 := by
  have hrne : jumpRate a i ≠ 0 := ne_of_gt hrate
  calc
    (offdiag i).sum (fun j =>
        (a i j / jumpRate a i) * (jumpRate a i * loss i j / 2)) =
        (offdiag i).sum (fun j => (1 / 2 : ℝ) * (a i j * loss i j)) := by
          apply Finset.sum_congr rfl
          intro j hj
          field_simp [hrne]
    _ = (1 / 2 : ℝ) *
          (offdiag i).sum (fun j => a i j * loss i j) := by
          rw [Finset.mul_sum]
    _ = 1 := by rw [hmoment]; norm_num

/-- The normalized second moment is exactly `Q_i`. -/
theorem normalizedLossScale_secondMoment
    (a loss : ι → ι → ℝ) (i : ι)
    (hrate : 0 < jumpRate a i) :
    (offdiag i).sum (fun j =>
      (a i j / jumpRate a i) *
        (jumpRate a i * loss i j / 2) ^ 2) =
      sphericalQAt a loss i := by
  have hrne : jumpRate a i ≠ 0 := ne_of_gt hrate
  calc
    (offdiag i).sum (fun j =>
        (a i j / jumpRate a i) *
          (jumpRate a i * loss i j / 2) ^ 2) =
        (offdiag i).sum (fun j =>
          (jumpRate a i / 4) * (a i j * (loss i j) ^ 2)) := by
            apply Finset.sum_congr rfl
            intro j hj
            field_simp [hrne]
            ring
    _ = (jumpRate a i / 4) *
          (offdiag i).sum (fun j => a i j * (loss i j) ^ 2) := by
          rw [Finset.mul_sum]
    _ = sphericalQAt a loss i := by
          unfold sphericalQAt sphericalEpsilonAt
          ring

/-- Abstract weighted second-moment minus mean-square identity. -/
theorem weightedSecondMoment_sub_one_eq_variance
    (s : Finset ι) (p x : ι → ℝ)
    (hsum : s.sum p = 1)
    (hmean : s.sum (fun j => p j * x j) = 1) :
    s.sum (fun j => p j * (x j) ^ 2) - 1 =
      s.sum (fun j => p j * (x j - 1) ^ 2) := by
  calc
    s.sum (fun j => p j * (x j) ^ 2) - 1 =
        s.sum (fun j => p j * (x j) ^ 2) -
          2 * s.sum (fun j => p j * x j) + s.sum p := by
            rw [hmean, hsum]
            ring
    _ = s.sum (fun j =>
          p j * (x j) ^ 2 - 2 * (p j * x j) + p j) := by
          rw [Finset.mul_sum]
          rw [← Finset.sum_sub_distrib, ← Finset.sum_add_distrib]
    _ = s.sum (fun j => p j * (x j - 1) ^ 2) := by
          apply Finset.sum_congr rfl
          intro j hj
          ring

/-- Exact normalized local variance identity. -/
theorem sphericalQ_sub_one_eq_normalizedLossVariance
    (a loss : ι → ι → ℝ) (i : ι)
    (hrate : 0 < jumpRate a i)
    (hmoment : (offdiag i).sum (fun j => a i j * loss i j) = 2) :
    sphericalQAt a loss i - 1 =
      (offdiag i).sum (fun j =>
        (a i j / jumpRate a i) *
          (jumpRate a i * loss i j / 2 - 1) ^ 2) := by
  have hsum := normalizedEdgeWeight_sum_one (a := a) (i := i) hrate
  have hmean := normalizedLossScale_mean_one
    (a := a) (loss := loss) (i := i) hrate hmoment
  have hvar := weightedSecondMoment_sub_one_eq_variance
    (s := offdiag i)
    (p := fun j => a i j / jumpRate a i)
    (x := fun j => jumpRate a i * loss i j / 2)
    hsum hmean
  rw [normalizedLossScale_secondMoment
    (a := a) (loss := loss) (i := i) hrate] at hvar
  exact hvar

/-- Nonnegative rates imply the sharp lower bound `Q_i >= 1`. -/
theorem one_le_sphericalQAt
    (a loss : ι → ι → ℝ) (i : ι)
    (ha : ∀ j, j ≠ i → 0 ≤ a i j)
    (hrate : 0 < jumpRate a i)
    (hmoment : (offdiag i).sum (fun j => a i j * loss i j) = 2) :
    1 ≤ sphericalQAt a loss i := by
  have hid := sphericalQ_sub_one_eq_normalizedLossVariance
    (a := a) (loss := loss) (i := i) hrate hmoment
  have hnonneg : 0 ≤ (offdiag i).sum (fun j =>
      (a i j / jumpRate a i) *
        (jumpRate a i * loss i j / 2 - 1) ^ 2) := by
    apply Finset.sum_nonneg
    intro j hj
    have hji : j ≠ i := (Finset.mem_erase.mp hj).1
    exact mul_nonneg
      (div_nonneg (ha j hji) (le_of_lt hrate)) (sq_nonneg _)
  linarith

/-- Local `Q_i=1` forces every strictly active edge loss to equal `2/r_i`. -/
theorem sphericalQ_eq_one_active_loss
    (a loss : ι → ι → ℝ) (i j : ι)
    (ha : ∀ k, k ≠ i → 0 ≤ a i k)
    (hji : j ≠ i)
    (hactive : 0 < a i j)
    (hrate : 0 < jumpRate a i)
    (hmoment : (offdiag i).sum (fun k => a i k * loss i k) = 2)
    (hQ : sphericalQAt a loss i = 1) :
    loss i j = 2 / jumpRate a i := by
  have hvar := sphericalQ_sub_one_eq_normalizedLossVariance
    (a := a) (loss := loss) (i := i) hrate hmoment
  have hsumzero :
      (offdiag i).sum (fun k =>
        (a i k / jumpRate a i) *
          (jumpRate a i * loss i k / 2 - 1) ^ 2) = 0 := by
    rw [← hvar, hQ]
    ring
  have hnonneg : ∀ k ∈ offdiag i,
      0 ≤ (a i k / jumpRate a i) *
        (jumpRate a i * loss i k / 2 - 1) ^ 2 := by
    intro k hk
    have hki : k ≠ i := (Finset.mem_erase.mp hk).1
    exact mul_nonneg
      (div_nonneg (ha k hki) (le_of_lt hrate)) (sq_nonneg _)
  have hjmem : j ∈ offdiag i :=
    Finset.mem_erase.mpr ⟨hji, Finset.mem_univ j⟩
  have hterm :=
    ((Finset.sum_eq_zero_iff_of_nonneg hnonneg).mp hsumzero) j hjmem
  have hp : 0 < a i j / jumpRate a i := div_pos hactive hrate
  have hsquare : (jumpRate a i * loss i j / 2 - 1) ^ 2 = 0 :=
    (mul_eq_zero.mp hterm).resolve_left (ne_of_gt hp)
  have hx : jumpRate a i * loss i j / 2 - 1 = 0 :=
    sq_eq_zero_iff.mp hsquare
  apply (eq_div_iff (ne_of_gt hrate)).2
  nlinarith

/-- Positivity of masses and shared positive conductances makes activity
symmetric. -/
theorem active_symmetric_of_shared_conductance
    (a gamma : ι → ι → ℝ) (w : ι → ℝ)
    (ha : ∀ i j, a i j = gamma i j / w i)
    (hgamma : ∀ i j, gamma i j = gamma j i)
    (hw : ∀ i, 0 < w i)
    {i j : ι} (hactive : 0 < a i j) :
    0 < a j i := by
  have hgi : gamma i j = a i j * w i := by
    rw [ha]
    field_simp [ne_of_gt (hw i)]
  have hgpos : 0 < gamma i j := by
    rw [hgi]
    exact mul_pos hactive (hw i)
  rw [ha, ← hgamma i j]
  exact div_pos hgpos (hw j)

/-- The spherical local formula plugs into the accepted abstract connected
equality-propagation theorem. -/
theorem connected_spherical_active_loss_rigidity
    (active : ι → ι → Prop)
    (loss : ι → ι → ℝ)
    (rate : ι → ℝ)
    (root : ι)
    (hRate : ∀ i, 0 < rate i)
    (hActiveSymm : ∀ {i j}, active i j → active j i)
    (hLossSymm : ∀ i j, loss i j = loss j i)
    (hLocal : ∀ {i j}, active i j → loss i j = 2 / rate i)
    (hConnected : ∀ j, Relation.ReflTransGen active root j) :
    (∀ j, rate j = rate root) ∧
      (∀ {i j}, active i j → loss i j = 2 / rate root) := by
  exact connected_active_loss_rigidity
    active loss rate 2 root (by norm_num) hRate hActiveSymm hLossSymm
    hLocal hConnected

/-- Complete finite spherical specialization: coordinate exactness supplies
the loss moment and positive rates, exact `Q=1` supplies the local active-edge
formula, and shared conductances plus connectedness propagate one global rate
and loss.  Loops are excluded explicitly because the generator is stored on
`offdiag`. -/
theorem finite_spherical_qOne_global_rigidity
    {κ : Type*} [Fintype κ]
    (a gamma : ι → ι → ℝ) (w : ι → ℝ)
    (Omega : ι → κ → ℝ) (root : ι)
    (ha : ∀ i j, j ≠ i → 0 ≤ a i j)
    (haGamma : ∀ i j, a i j = gamma i j / w i)
    (hgamma : ∀ i j, gamma i j = gamma j i)
    (hw : ∀ i, 0 < w i)
    (hunit : ∀ i, sphericalPairing Omega i i = 1)
    (hcoord : ∀ p v,
      jumpGenerator a (fun j => Omega j p) v = -2 * Omega v p)
    (hQ : ∀ i,
      sphericalQAt a (sphericalChordLoss Omega) i = 1)
    (hConnected : ∀ j,
      Relation.ReflTransGen (fun i j => i ≠ j ∧ 0 < a i j) root j) :
    0 < jumpRate a root ∧
      (∀ j, jumpRate a j = jumpRate a root) ∧
      (∀ {i j}, i ≠ j ∧ 0 < a i j →
        sphericalChordLoss Omega i j = 2 / jumpRate a root) := by
  have hmoment : ∀ i,
      (offdiag i).sum (fun j =>
        a i j * sphericalChordLoss Omega i j) = 2 := by
    intro i
    exact coordinateEigenmap_lossMoment_two a Omega i (hunit i) hcoord
  have hrate : ∀ i, 0 < jumpRate a i := by
    intro i
    exact jumpRate_pos_of_lossMoment_two
      a (sphericalChordLoss Omega) i (ha i) (hmoment i)
  have hActiveSymm : ∀ {i j},
      (i ≠ j ∧ 0 < a i j) → (j ≠ i ∧ 0 < a j i) := by
    intro i j hij
    exact ⟨Ne.symm hij.1,
      active_symmetric_of_shared_conductance
        a gamma w haGamma hgamma hw hij.2⟩
  have hLocal : ∀ {i j}, i ≠ j ∧ 0 < a i j →
      sphericalChordLoss Omega i j = 2 / jumpRate a i := by
    intro i j hij
    exact sphericalQ_eq_one_active_loss
      a (sphericalChordLoss Omega) i j (ha i) (Ne.symm hij.1) hij.2
      (hrate i) (hmoment i) (hQ i)
  have hglobal := connected_spherical_active_loss_rigidity
    (fun i j => i ≠ j ∧ 0 < a i j)
    (sphericalChordLoss Omega)
    (jumpRate a)
    root
    hrate
    hActiveSymm
    (sphericalChordLoss_symmetric Omega)
    hLocal
    hConnected
  exact ⟨hrate root, hglobal.1, hglobal.2⟩

end AFPBarrier

import AFPBarrier.GlobalLossRigidity
import AFPBarrier.JumpGenerator
import Mathlib.Tactic

/-!
# Spherical `Q=1` equality transfer

Finite algebra behind the Prompt 3 spherical specialization.  The topological
triangulation classification remains in the ordinary theorem document.
-/

open scoped BigOperators

namespace AFPBarrier

variable {ι : Type*} [Fintype ι] [DecidableEq ι]

/-- Spherical second loss moment at a state. -/
def sphericalEpsilonAt
    (a loss : ι → ι → ℝ) (i : ι) : ℝ :=
  (offdiag i).sum (fun j => a i j * (loss i j) ^ 2)

/-- Prompt 3 local quality factor `Q_i=r_i epsilon_i/4`. -/
noncomputable def sphericalQAt
    (a loss : ι → ι → ℝ) (i : ι) : ℝ :=
  jumpRate a i * sphericalEpsilonAt a loss i / 4

/-- The normal loss moment `2` forces a strictly positive row rate when rates
and losses are nonnegative. -/
theorem jumpRate_pos_of_lossMoment_two
    (a loss : ι → ι → ℝ) (i : ι)
    (ha : ∀ j, j ≠ i → 0 ≤ a i j)
    (hloss : ∀ j, j ≠ i → 0 ≤ loss i j)
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
        (a i j / jumpRate a i) * (jumpRate a i * loss i j / 2))
        = (offdiag i).sum (fun j => (1 / 2 : ℝ) * (a i j * loss i j)) := by
            apply Finset.sum_congr rfl
            intro j hj
            field_simp [hrne] <;> ring
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
        (jumpRate a i * loss i j / 2) ^ 2)
      = sphericalQAt a loss i := by
  have hrne : jumpRate a i ≠ 0 := ne_of_gt hrate
  calc
    (offdiag i).sum (fun j =>
        (a i j / jumpRate a i) *
          (jumpRate a i * loss i j / 2) ^ 2)
        = (offdiag i).sum (fun j =>
            (jumpRate a i / 4) * (a i j * (loss i j) ^ 2)) := by
              apply Finset.sum_congr rfl
              intro j hj
              field_simp [hrne] <;> ring
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
    s.sum (fun j => p j * (x j) ^ 2) - 1
      = s.sum (fun j => p j * (x j - 1) ^ 2) := by
  calc
    s.sum (fun j => p j * (x j) ^ 2) - 1
        = s.sum (fun j => p j * (x j) ^ 2)
            - 2 * s.sum (fun j => p j * x j) + s.sum p := by
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

/-- Exact Prompt 3 local variance identity. -/
theorem sphericalQ_sub_one_eq_normalizedLossVariance
    (a loss : ι → ι → ℝ) (i : ι)
    (hrate : 0 < jumpRate a i)
    (hmoment : (offdiag i).sum (fun j => a i j * loss i j) = 2) :
    sphericalQAt a loss i - 1
      = (offdiag i).sum (fun j =>
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
    exact mul_nonneg (div_nonneg (ha k hki) (le_of_lt hrate)) (sq_nonneg _)
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
    calc
      gamma i j = (gamma i j / w i) * w i := by
        field_simp [ne_of_gt (hw i)]
      _ = a i j * w i := by rw [← ha i j]
  have hgpos : 0 < gamma i j := by
    rw [hgi]
    exact mul_pos hactive (hw i)
  rw [ha j i, ← hgamma i j]
  exact div_pos hgpos (hw j)

/-- Symmetry of the pairing gives symmetry of the spherical loss. -/
theorem one_sub_pairing_symmetric
    (pairing : ι → ι → ℝ)
    (hpairing : ∀ i j, pairing i j = pairing j i)
    (i j : ι) :
    1 - pairing i j = 1 - pairing j i := by
  rw [hpairing i j]

/-- The spherical local formula plugs directly into the accepted abstract
connected equality-propagation theorem. -/
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

end AFPBarrier

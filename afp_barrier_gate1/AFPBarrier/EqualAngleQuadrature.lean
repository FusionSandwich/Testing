import AFPBarrier.EqualAngleConnectivity
import Mathlib.Tactic

/-!
# Exact normalization of the equal-angle quadrature

The cell weights are exact spherical-zone areas. A product-to-sum identity
turns each ring weight into a cosine difference, so the polar sum telescopes.
This proves exact total weight `4π` for every finite `N × M` grid.
-/

namespace AFPBarrier

noncomputable section

/-- Elementary telescoping identity over a finite range. -/
theorem sum_range_sub_succ_real
    (f : ℕ → ℝ) (N : ℕ) :
    (Finset.range N).sum (fun i => f i - f (i + 1))
      = f 0 - f N := by
  induction N with
  | zero => simp
  | succ N ih =>
      rw [Finset.sum_range_succ, ih]
      ring

/-- A spherical-zone cell weight is a cosine difference. -/
theorem equalAngleTrigWeight_eq_cos_difference
    (alpha theta h : ℝ) :
    equalAngleTrigWeight alpha theta h
      = alpha * (Real.cos (theta - h) - Real.cos (theta + h)) := by
  unfold equalAngleTrigWeight equalAngleWeight
  simp only [Real.cos_sub, Real.cos_add]
  ring

/-- The weight of ring `i` has the exact telescoping form. -/
theorem equalAngleGrid_weight_telescope
    (n alpha : ℝ) (i : ℕ) :
    equalAngleTrigWeight alpha
        (equalAngleGridTheta n i) (equalAngleGridHalfStep n)
      = alpha *
        (Real.cos (2 * (i : ℝ) * equalAngleGridHalfStep n)
          - Real.cos (2 * ((i + 1 : ℕ) : ℝ)
              * equalAngleGridHalfStep n)) := by
  rw [equalAngleTrigWeight_eq_cos_difference]
  congr 2
  · unfold equalAngleGridTheta
    ring_nf
  · unfold equalAngleGridTheta
    norm_num
    ring_nf

/-- The sum of the per-direction ring weights is exactly `2*alpha`. -/
theorem sum_equalAngleGrid_ringWeights
    (N : ℕ) (hN : 0 < N) (alpha : ℝ) :
    (Finset.range N).sum (fun i =>
        equalAngleTrigWeight alpha
          (equalAngleGridTheta (N : ℝ) i)
          (equalAngleGridHalfStep (N : ℝ)))
      = 2 * alpha := by
  have hNc : (N : ℝ) ≠ 0 := by exact_mod_cast hN.ne'
  let f : ℕ → ℝ := fun i =>
    Real.cos (2 * (i : ℝ) * equalAngleGridHalfStep (N : ℝ))
  calc
    (Finset.range N).sum (fun i =>
        equalAngleTrigWeight alpha
          (equalAngleGridTheta (N : ℝ) i)
          (equalAngleGridHalfStep (N : ℝ)))
        = (Finset.range N).sum (fun i => alpha * (f i - f (i + 1))) := by
            apply Finset.sum_congr rfl
            intro i hi
            simpa [f] using
              equalAngleGrid_weight_telescope (N : ℝ) alpha i
    _ = alpha * (Finset.range N).sum (fun i => f i - f (i + 1)) := by
          rw [Finset.mul_sum]
    _ = alpha * (f 0 - f N) := by
          rw [sum_range_sub_succ_real]
    _ = 2 * alpha := by
      have hangle :
          2 * (N : ℝ) * equalAngleGridHalfStep (N : ℝ) = Real.pi := by
        unfold equalAngleGridHalfStep
        field_simp [hNc]
      simp [f, hangle]
      ring

/-- The full product quadrature has exact total area `4π`. -/
theorem sum_equalAngleGrid_allWeights
    (N M : ℕ) (hN : 0 < N) (hM : 0 < M) :
    (Finset.range N).sum (fun i =>
      (Finset.range M).sum (fun _j =>
        equalAngleTrigWeight
          (equalAngleGridAzimuthStep (M : ℝ))
          (equalAngleGridTheta (N : ℝ) i)
          (equalAngleGridHalfStep (N : ℝ))))
      = 4 * Real.pi := by
  have hMc : (M : ℝ) ≠ 0 := by exact_mod_cast hM.ne'
  calc
    (Finset.range N).sum (fun i =>
      (Finset.range M).sum (fun _j =>
        equalAngleTrigWeight
          (equalAngleGridAzimuthStep (M : ℝ))
          (equalAngleGridTheta (N : ℝ) i)
          (equalAngleGridHalfStep (N : ℝ))))
        = (Finset.range N).sum (fun i =>
          (M : ℝ) * equalAngleTrigWeight
            (equalAngleGridAzimuthStep (M : ℝ))
            (equalAngleGridTheta (N : ℝ) i)
            (equalAngleGridHalfStep (N : ℝ))) := by
              apply Finset.sum_congr rfl
              intro i hi
              simp
    _ = (M : ℝ) * (Finset.range N).sum (fun i =>
          equalAngleTrigWeight
            (equalAngleGridAzimuthStep (M : ℝ))
            (equalAngleGridTheta (N : ℝ) i)
            (equalAngleGridHalfStep (N : ℝ))) := by
          rw [Finset.mul_sum]
    _ = (M : ℝ) * (2 * equalAngleGridAzimuthStep (M : ℝ)) := by
          rw [sum_equalAngleGrid_ringWeights N hN]
    _ = 4 * Real.pi := by
      unfold equalAngleGridAzimuthStep
      field_simp [hMc]
      ring

end

end AFPBarrier

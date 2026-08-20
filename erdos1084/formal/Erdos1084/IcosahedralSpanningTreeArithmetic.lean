import Mathlib

namespace Erdos1084

/-!
# Exact arithmetic for icosahedral spanning-tree developments

The human proof and Matrix-Tree certificate show that the icosahedron graph has
`5,184,000` spanning trees and that each fixed edge belongs to `1,900,800` of
them. Hence the uniform branch marginal is `11/30`. This module certifies the
integer identities and the corresponding equal-interface selector arithmetic.
-/

open scoped BigOperators

/-- Exact spanning-tree incidence identity. -/
theorem icosa_spanningTree_incidence_identity :
    30 * 1900800 = 11 * 5184000 := by
  norm_num

/-- Exact edge marginal under the uniform spanning-tree distribution. -/
theorem icosa_spanningTree_edge_marginal :
    (1900800 : ℝ) / 5184000 = 11 / 30 := by
  norm_num

/-- The uniform marginal is strictly larger than the simple five-cycle threshold. -/
theorem icosa_spanningTree_marginal_gt_oneFifth :
    (1 : ℝ) / 5 < 11 / 30 := by
  norm_num

/-- The restricted Sigma-5 ratio `4/5` is above the spanning-tree threshold. -/
theorem sigma5_ratio_gt_icosa_spanningTree_threshold :
    (11 : ℝ) / 30 < 4 / 5 := by
  norm_num

/--
On thirty equal-jump interfaces, an interfacewise physical ratio `11/30`
provides eleven full developed cuts in aggregate.
-/
theorem icosa_uniformPhysical_ge_elevenCuts
    {I : Type*} (interfaces : Finset I) (physical : I → ℝ)
    {J : ℝ}
    (hcard : interfaces.card = 30)
    (hinterface : ∀ i ∈ interfaces, (11 / 30 : ℝ) * J ≤ physical i) :
    11 * J ≤ ∑ i ∈ interfaces, physical i := by
  have hsum :
      (∑ i ∈ interfaces, (11 / 30 : ℝ) * J) ≤
        ∑ i ∈ interfaces, physical i :=
    Finset.sum_le_sum hinterface
  have hleft :
      (∑ i ∈ interfaces, (11 / 30 : ℝ) * J) = 11 * J := by
    simp [hcard]
    ring
  rw [hleft] at hsum
  exact hsum

/--
If every valid spanning-tree development has eleven equal cut jumps, the
aggregate physical threshold proves the sharp bound.
-/
theorem icosa_spanningTree_selector_scalar
    {sharp exterior physicalTotal J : ℝ}
    (hdevelopment : sharp ≤ exterior + 11 * J)
    (hphysical : 11 * J ≤ physicalTotal) :
    sharp ≤ exterior + physicalTotal := by
  linarith

/-- Exact decimal comparison used in reports. -/
theorem icosa_spanningTree_threshold_gt_3666 :
    (3666 : ℝ) / 10000 < 11 / 30 := by
  norm_num

end Erdos1084

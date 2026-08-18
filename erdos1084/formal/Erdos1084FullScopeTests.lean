import Erdos1084

open Erdos1084

/-! Smoke tests for the FCC Wulff, HCP audit, and crystallization-core arithmetic. -/

example (t : ℕ) :
    fccWulffD t = 6 * fccWulffB t :=
  fccWulff_deficit_eq_six_projection t

example (t : ℕ) :
    6 * fccWulffN t = fccWulffE t + fccWulffD t :=
  fccWulff_bulk_split t

example : (192 : ℕ) ^ 3 = 432 * (128 : ℕ) ^ 2 :=
  fccWulff_leading_cube

example : (192 : ℝ) ^ 3 / (128 : ℝ) ^ 2 = 432 :=
  fccWulff_leading_ratio_cube

example : publishedFccDeficitCube < publishedHcpDeficitCube :=
  published_hcp_strictly_above_fcc

example : publishedHcpDeficitCube - publishedFccDeficitCube = 27 / 4 :=
  published_hcp_fcc_cube_gap

example : publishedHcpDeficitCube < naiveFrequencyHcpCube :=
  naive_frequency_model_fails_at_hcp

example : naiveFrequencyHcpCube - publishedHcpDeficitCube = 135 / 4 :=
  naive_hcp_cube_excess

example
    {ι : Type*} [Fintype ι] [DecidableEq ι]
    (degree : ι → ℕ) (D : ℕ)
    (hdeficit : ∑ i, (12 - degree i) = 2 * D) :
    (defectiveVertices degree).card ≤ 2 * D :=
  defective_card_le_twice_contact_deficit degree D hdeficit

example
    {ι : Type*} [DecidableEq ι]
    (bad halo : Finset ι) (D : ℕ)
    (hbad : bad.card ≤ 2 * D)
    (hhalo : halo.card ≤ 12 * bad.card) :
    halo.card ≤ 24 * D :=
  defective_halo_card_le_twentyfour_deficit bad halo D hbad hhalo

example
    {ι : Type*} [Fintype ι] [DecidableEq ι]
    (localBarlow : ι → Prop) [DecidablePred localBarlow]
    (halo : Finset ι) (D : ℕ)
    (hlocal : ∀ i, i ∉ halo → localBarlow i)
    (hhalo : halo.card ≤ 24 * D) :
    (nonBarlowVertices localBarlow).card ≤ 24 * D :=
  nonBarlow_card_le_twentyfour_deficit localBarlow halo D hlocal hhalo

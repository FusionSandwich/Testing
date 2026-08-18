import Mathlib

namespace Erdos1084

/-- Vertices whose local kissing configuration is not certified as FCC/HCP. -/
def nonBarlowVertices
    {ι : Type*} [Fintype ι] [DecidableEq ι]
    (localBarlow : ι → Prop) [DecidablePred localBarlow] : Finset ι :=
  Finset.univ.filter fun i => ¬ localBarlow i

/--
If every vertex outside an exceptional halo has an FCC/HCP local pattern,
then every non-Barlow vertex belongs to that halo.
-/
theorem nonBarlowVertices_subset_halo
    {ι : Type*} [Fintype ι] [DecidableEq ι]
    (localBarlow : ι → Prop) [DecidablePred localBarlow]
    (halo : Finset ι)
    (hlocal : ∀ i, i ∉ halo → localBarlow i) :
    nonBarlowVertices localBarlow ⊆ halo := by
  intro i hi
  have hnot : ¬ localBarlow i := by
    exact (Finset.mem_filter.mp hi).2
  by_contra hihalo
  exact hnot (hlocal i hihalo)

/-- Cardinality form of the preceding localization statement. -/
theorem nonBarlow_card_le_halo
    {ι : Type*} [Fintype ι] [DecidableEq ι]
    (localBarlow : ι → Prop) [DecidablePred localBarlow]
    (halo : Finset ι)
    (hlocal : ∀ i, i ∉ halo → localBarlow i) :
    (nonBarlowVertices localBarlow).card ≤ halo.card :=
  Finset.card_le_card (nonBarlowVertices_subset_halo localBarlow halo hlocal)

/--
Abstract quantitative Hales bridge. Once the localized Fejes--Tóth/Hales
classification identifies every vertex outside the defective closed
neighborhood as FCC/HCP, at most `24D` vertices have a non-Barlow local
kissing configuration.
-/
theorem nonBarlow_card_le_twentyfour_deficit
    {ι : Type*} [Fintype ι] [DecidableEq ι]
    (localBarlow : ι → Prop) [DecidablePred localBarlow]
    (halo : Finset ι) (D : ℕ)
    (hlocal : ∀ i, i ∉ halo → localBarlow i)
    (hhalo : halo.card ≤ 24 * D) :
    (nonBarlowVertices localBarlow).card ≤ 24 * D := by
  exact le_trans (nonBarlow_card_le_halo localBarlow halo hlocal) hhalo

end Erdos1084

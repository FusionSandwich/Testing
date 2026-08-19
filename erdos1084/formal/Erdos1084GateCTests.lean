import Erdos1084

/-!
# Gate-C occupied-compactness combinatorial smoke tests

The geometric FCC/HCP recognition and Voronoi-cell calculation are checked in the canonical Math
dossier and exact Python certificate. This file checks the Lean combinatorial spine used to bound
the surface-order defect halo.
-/

#check Erdos1084.degreeDefectVertices
#check Erdos1084.degreeDefectHalo
#check Erdos1084.degreeDefectVertices_card_le_deficit_sum
#check Erdos1084.degreeDefectHalo_card_le_thirteen_mul
#check Erdos1084.degreeDefectHalo_card_le_twentySix_mul

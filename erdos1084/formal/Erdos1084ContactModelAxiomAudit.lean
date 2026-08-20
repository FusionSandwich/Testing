import Erdos1084

/-!
# Axiom audit for the foundational finite contact model

These theorems use only mathlib's Euclidean metric and finite simple-graph infrastructure. No
geometric packing theorem is assumed at this layer.
-/

#print axioms Erdos1084.UnitSeparatedConfiguration.contactGraph_adj
#print axioms Erdos1084.UnitSeparatedConfiguration.dist_eq_one_of_adj
#print axioms Erdos1084.UnitSeparatedConfiguration.one_lt_dist_of_not_adj
#print axioms Erdos1084.UnitSeparatedConfiguration.sum_contactDegrees_eq_twice_contactCount
#print axioms Erdos1084.UnitSeparatedConfiguration.degree_deficit_sum_Z
#print axioms Erdos1084.UnitSeparatedConfiguration.contactCount_le_six_card
#print axioms Erdos1084.UnitSeparatedConfiguration.contactDeficit_cast

#check Erdos1084.Point3
#check Erdos1084.UnitSeparatedConfiguration
#check Erdos1084.UnitSeparatedConfiguration.contactGraph
#check Erdos1084.UnitSeparatedConfiguration.contactCount
#check Erdos1084.UnitSeparatedConfiguration.contactDeficit

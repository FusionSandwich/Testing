import Erdos1084

/-!
# Axiom audit for the direct Phase-I contact model

The finite contact model introduces no project-specific axiom. The geometric kissing-number
statement remains a visible ordinary hypothesis through `HasContactDegreeAtMostTwelve`.
-/

#print axioms Erdos1084.UnitSeparatedConfiguration.point_injective
#print axioms Erdos1084.UnitSeparatedConfiguration.sum_contactDegrees_eq_twice_contactCount
#print axioms Erdos1084.UnitSeparatedConfiguration.degree_deficit_sum_Z
#print axioms Erdos1084.UnitSeparatedConfiguration.contactCount_le_six_card
#print axioms Erdos1084.UnitSeparatedConfiguration.contactDeficit_cast

#check Erdos1084.UnitSeparatedConfiguration
#check Erdos1084.UnitSeparatedConfiguration.contactGraph
#check Erdos1084.UnitSeparatedConfiguration.HasContactDegreeAtMostTwelve
#check Erdos1084.UnitSeparatedConfiguration.degree_deficit_sum_Z

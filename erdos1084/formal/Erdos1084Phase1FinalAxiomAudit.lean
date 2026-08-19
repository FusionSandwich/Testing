import Erdos1084

/-!
# Clean Phase-I theorem axiom and signature audit

Ordinary theorem arguments do not appear in `#print axioms`; the complete certificate and theorem
signatures are therefore printed after the axiom reports.
-/

#print axioms Erdos1084.UnitSeparatedConfiguration.sum_realContactDegree_eq_twice_contactCount
#print axioms Erdos1084.UnitSeparatedConfiguration.phase1_local_degree_charge
#print axioms Erdos1084.UnitSeparatedConfiguration.phase1_local_surface_input
#print axioms Erdos1084.UnitSeparatedConfiguration.phase1_published_inputs_contact_bound
#print axioms Erdos1084.UnitSeparatedConfiguration.kpClean_eq_20465
#print axioms Erdos1084.UnitSeparatedConfiguration.phase1_universal_contact_bound
#print axioms Erdos1084.UnitSeparatedConfiguration.phase1_universal_deficit_bound

#check Erdos1084.UnitSeparatedConfiguration.Phase1LocalCapCertificate
#check Erdos1084.UnitSeparatedConfiguration.Phase1PublishedInputCertificate
#check Erdos1084.UnitSeparatedConfiguration.Phase1UniversalCertificate
#check Erdos1084.UnitSeparatedConfiguration.phase1_universal_contact_bound

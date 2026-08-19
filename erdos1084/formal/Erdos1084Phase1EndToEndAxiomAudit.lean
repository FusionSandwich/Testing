import Erdos1084

/-!
# Phase-I end-to-end axiom and signature audit

`#print axioms` does not display ordinary theorem parameters or structure fields.  This audit
therefore prints both the axiom reports and the complete certificate/theorem signatures.
-/

#print axioms Erdos1084.Phase1PackingCertificate.toKeplerLocalSurfaceInput
#print axioms Erdos1084.Phase1PackingCertificate.contactCount_lt_clean_bound
#print axioms Erdos1084.Phase1PackingCertificate.contactCount_le_six_card
#print axioms Erdos1084.Phase1PackingCertificate.contactDeficit_cast

#check Erdos1084.Phase1PackingCertificate
#check Erdos1084.Phase1PackingCertificate.power
#check Erdos1084.Phase1PackingCertificate.globalSurface
#check Erdos1084.Phase1PackingCertificate.boundary_le_exposure_sum
#check Erdos1084.Phase1PackingCertificate.no_isolated
#check Erdos1084.Phase1PackingCertificate.degree_le_twelve
#check Erdos1084.Phase1PackingCertificate.local_exposure_charge
#check Erdos1084.Phase1PackingCertificate.contactCount_lt_clean_bound

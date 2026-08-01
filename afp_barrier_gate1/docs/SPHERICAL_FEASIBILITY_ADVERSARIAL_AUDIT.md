# Sphere-feasibility adversarial audit

The final proof was checked against the following failure modes.

| Failure mode | Audit result |
|---|---|
| Division by `sin(theta)` at an antipode | Eliminated by disjoint index sets `N` and `P`; antipodes appear only through normal loss two. |
| Ambient interior used instead of relative interior | Eliminated; all strict local statements use `ri` in `aff conv(U)`. |
| Hidden full-dimensionality | Eliminated; the margin is relative, and ambient perturbation claims explicitly require full tangent dimension or span-preserving perturbations. |
| Repeated or redundant candidate points omitted | Eliminated; all coefficient statements are indexed, and the averaging proof puts positive mass on every index. |
| Strict positivity confused with positivity on selected support | Eliminated; support-specific and all-permitted-edge statements are separated. |
| Tangent dependence called unique without a rank test | Eliminated; uniqueness is exactly augmented affine independence in the minimal face containing zero. |
| Normal scale allowed to remain free | Eliminated; `D(b)>0` and `cD(b)=2` give the unique positive scale `c=2/D(b)`. |
| Antipodal normal budget not divided explicitly | Eliminated; `sum_P a_p = 1-D(b)/2`. |
| Rate scaling stated only as asymptotic notation | Eliminated; all `h^-2` bounds have displayed constants. |
| Coefficientwise rate bounds inferred from the loss window alone | Eliminated; only outgoing-rate bounds use the loss window alone; lower coefficient bounds use `rho`. |
| Perturbation of a boundary optimizer treated as uniformly stable | Eliminated; the proof mixes an optimizer with the margin row before right-inverse correction. |
| Equal masses silently assumed globally | Eliminated; masses appear in `b_i=-2w_i Omega_i`, the complete construction, all dual objectives, and sensitivity estimates. |
| Sign error in `A gamma=b` or `A^T y` | Checked by endpoint expansion and the exact cube Farkas certificate. |
| Weak duality presented as the full alternative | Eliminated; infeasibility completeness follows from strict separation of a finitely generated closed cone. |
| Residual positive/negative parts assigned the wrong dual signs | Checked from columns `-I` and `+I`; complementarity is `p_r(tau_r+y_r)=0`, `n_r(tau_r-y_r)=0`. |
| Feasible set called a polytope despite zero edge columns | Eliminated; compactness is proved for nonzero chord columns, and zero-length duplicate-node edges are identified as recession factors. |
| Local feasibility claimed to imply global reversibility | Falsified by the weighted-centered cube with an exact Farkas certificate. |

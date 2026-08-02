# Prompt 3 theorem and hypothesis registry

| ID | Exact hypotheses | Conclusion | Dependencies | Counterexample boundary | Ordinary proof | Lean state | Exact audit |
|---|---|---|---|---|---|---|---|
| P3-1 | finite positive spherical coordinate eigenmap `L Omega=-2Omega` | normal loss moment, `r_i>0`, probability/mean/variance identities | finite sums, inner product | signed rates invalidate nonnegative variance | §1 | `SphericalQEqualityRigidity.lean` | near-rigidity audit |
| P3-2 | P3-1 and local `Q_i=1` | every active loss is `2/r_i` | equality in nonnegative sum | inactive edges uncontrolled | §2.1 | same | all Platonic rows |
| P3-3 | P3-2, shared conductances, positive masses, connected active graph | one global rate and one active-edge loss | abstract `GlobalLossRigidity.lean` | disconnected components; nonreversible rows | §2.2 | imported + specialization | hypothesis deletion audit |
| P3-R | P3-3 plus ten explicit nondegenerate minor-arc round triangulation hypotheses | tetrahedral/octahedral/icosahedral realization up to `O(3)` | spherical cosine law, round angle sum, Euler, direct map uniqueness, face propagation | cube/dodecahedron; cones; major arcs; inactive diagonals | §3 | selected finite identities only | plantri + exact Gram/hull |
| P3-4 | `p_ij>=kappa`, `Q_i<=1+eta`, `delta<1` | `|x_ij-1|<=delta` | P3-1 variance | small `kappa` stress | §4.1 | `QuantitativeGlobalNearRigidity.lean` | near-rigidity audit |
| P3-5 | P3-4, symmetric active losses, connected graph | adjacent/path/diameter rate bounds | shared-edge ratio, path multiplication | long paths show dependence | §4.2 | selected cross-ratio lemmas | path stress |
| P3-6 | P3-5 | incident/global/reference loss bounds | graph center and logarithms | inactive edges excluded | §4.3 | selected algebra | path stress |
| P3-7 | P3-6, losses in `[ell_-,ell_+] subset (0,2)` | explicit arccos Lipschitz conversion | mean-value theorem | endpoint degeneracy makes constant diverge | §4.4 | ordinary proof | arc audit |
| P3-8 | reversible shared conductance graph | `P` reversible for `pi_i proportional w_i r_i` | conductance algebra | nonreversible variants | §5.1 | finite algebra | exact small graphs |
| P3-9 | P3-4 and P3-8 | `E_P(log r)<=2eta/(1-delta)^2` | logarithm bound, detailed-balance swap | no bound without defect control | §5.2 | finite algebra boundary | resistance audit |
| P3-10 | P3-9, spectral gap `lambda_P>0` | variance and `pi_min` sup bounds | Poincare definition | small gap stress | §5.3 | external variational input | exact small graphs |
| P3-11 | P3-9, connected conductance graph | effective-resistance pointwise bound | Dirichlet principle | large resistance stress | §5.4 | external variational input | exact rational paths |
| P3-S | near-equality and round triangulation hypotheses plus explicit domain inequalities | common valence, Platonic type, edge-length distance to `theta_q` | P3-4–11, explicit angle derivatives, integer gap | domain margins are mandatory | §6.1–6.4 | selected finite inequalities | angle/valence audit |
| P3-S* | P3-S reference loss satisfies explicit margins (6.16) | single threshold `eta_*=kappa delta_*^2` suffices | logarithmic upper bounds and fixed derivative box | no uniform threshold at geometric degeneracy | §6.5 | ordinary proof | threshold stress |
| P3-C1 | any spherical coordinate eigenmap | `tr C_i=4`, radial covariance `=4Q_i/r_i` | loss moment | sign convention audited | §7.1 | `QEqualityCovariance.lean` | covariance audit |
| P3-C2 | local `Q_i=1`, `0<ell_i<2` | exact `T_i,C_i,M_i` decomposition | tangent expansion | antipodal case excluded | §7.2 | finite entrywise decomposition | covariance audit |
| P3-C3 | P3-C2 | axial iff `T_i=P_i/2` | positive tangent coefficient | weighted octahedron | §7.3 | finite algebra | covariance audit |
| P3-C4 | positive weighted octahedral family | `L Omega=-2Omega`, `r=2`, `ell=1`, `Q=1`, axial iff all `g` equal | exact conductance computation | none within stated family | §7.4 | selected scalar identities | exact SymPy |
| P3-C5 | P3-C4 and genuine sampling map | degree-two sampled exact space is `{0}` | `P` is an infinity-norm contraction | form aliases retained | §7.4 | ordinary finite proof | exact linear system |
| P3-C6 | `1<=Q_i<=1+eta` | radial error in `[0,4eta/r_i]`; no tangent bound | P3-C1 | anisotropy tends to `1/2` at `eta=0` | §7.5 | finite scalar inequality | exact parameter limit |

## Constants

```text
x_ij      = r_i ell_ij/2
delta     = sqrt(eta/kappa)
q_delta   = (1+delta)/(1-delta)
s_delta   = log q_delta
h_delta   = -log(1-delta)
B_delta   = h_delta+R_G s_delta
sigma_arc = min(sqrt(ell_-(2-ell_-)),sqrt(ell_+(2-ell_+)))
Delta_theta = ell_ref(exp(B_delta)-1)/sigma_ref
C_ang     = 1/(s_A s_theta^2)+4/(s_A s_theta^3)
g_kappa   = min{|2pi/m-2pi/n|:3<=m<n<=floor(1/kappa)}
m_eq      = inf_J alpha_eq'(theta), with m_eq>=s_J/4
```

The conservative single-threshold constants `rho,b_0,C_R,sigma_0,K_theta,
tau,delta_*,eta_*` are defined in §6.5 of the theorem document.

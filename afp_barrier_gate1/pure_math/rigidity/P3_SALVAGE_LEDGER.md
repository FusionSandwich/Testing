# Prompt 3 immutable-source salvage ledger

## Method and baseline

This ledger was written and published before substantial Prompt 3
implementation.  Every source was read from a literal commit object with
`git show <commit>:<path>` and its blob identifier was obtained with
`git ls-tree -r <commit> -- <path>`.  No old Prompt 3 branch was merged or
cherry-picked.

```text
verified target baseline:
  commit 31ea6a49f006df10ca633eafd6848ad43b51ac3f
  tree   879b88de81eeb52ebb09373c2ccb77cb7cb7642c

narrow source:
  commit 65821ff1ebd47fbee1098b30c552906cd6e03b46

narrow integration-history source:
  commit 6b5d7ad53d704b7ff1b96d40abbef19f6e6a2125

rich source:
  commit d9304b5d19a1bbe69fe4ac23736308f9efe9d694
```

The old sources descend from an older Prompt 1/2 line and contain obsolete
workflows and generated files.  Accepted mathematics is manually re-proved or
ported into the verified Prompt 2 API.  Old provenance is never reused as
evidence for this branch.

## Narrow-source candidates

Files shared by the two narrow commits are byte-identical unless noted.

| Candidate | Immutable source and blob | Accepted material | Rejected material / assumptions | Disposition |
|---|---|---|---|---|
| `AFPBarrier/SphericalQOneRigidity.lean` | `65821ff...` and `6b5d7ad...`; `3361336839758030934493bb57bf3d2808bfbf9b` | PROVED finite row-rate positivity, active-loss equality, connected transfer, antipodal and tangent scalar algebra | It lacks the canonical normalized `Q-1` identity and required full path/logarithmic package; its old module name would duplicate the coherent rich-source module set | manually re-prove selected lemmas in the new coherent modules; do not copy the file wholesale |
| `pure_math/rigidity/SPHERICAL_Q1_RIGIDITY_THEOREM.md` | both; `18596bc700851abdcd8aa377073e6db48f6ea9e1` | PROVED equality propagation, restricted classification route, exact constants, and edge-metric stability derivations | Stale baseline and incomplete Prompt 2 covariance/sampling boundary | re-derive into `GLOBAL_Q_RIGIDITY_THEOREM.md` |
| `pure_math/rigidity/ICOSAHEDRAL_GRAPH_LEMMA.md` | both; `2ecbc89db0664a2e3001c52406710bd5ae1f4a55` | PROVED cyclic-link/collar mechanism for the 5-valent 12-vertex case | Requires the simple cellular triangulated-manifold hypotheses at every use | manually port with the link and disk-frontier premises explicit |
| `pure_math/rigidity/prompt3_rigidity_audit.py` | both; `4f1e1833e4bf5d57d5140bd6b17b0420fc7008b5` | COMPUTATIONAL exact Platonic coordinates, `Q`, Euler, variance, and constant checks | Its rare-edge family is only an abstract probability model; its finite `is_triangular_sphere` check is not a planarity/classification proof; SymPy was not provisioned by the historical local run | salvage exact cases into the new pinned audits and workflow; do not cite enumeration as proof |
| `docs/PROMPT3_APPROACH_REGISTRY.md` | both; `77b682ddc6a5ca2297ca6ab219614f4361c262c4` | Useful independent proof/counterexample mechanism families | The claim that multiagent execution was unavailable is false for this run; status/provenance is stale | rewrite as `P3_APPROACH_REGISTRY.md` |
| `docs/PROMPT3_STAGE_REPORT.md` | both; `17db2b8a47f8ff2fd153e394fbd09a7289eeffee` | Useful theorem-family summary | REJECTED as current provenance: baseline `c88b575...`, branch, jobs, and scope are not this Prompt 2 line | discard provenance; rewrite the stage report |
| `docs/PROMPT3_THEOREM_MAP.md` | both; `d85c28c932af94e57edadf33ee5f6291adaa1158` | Useful theorem decomposition | Incomplete for the required covariance, resistance, threshold, and full Lean path/log results; one entry conflates equality support with a lower-bound source | rewrite and extend |
| `docs/PROMPT3_INTEGRATION_RECORD.md` | `6b5d7ad...` only; `fbd825d4f57ee119188a1cc5a2521d66e8f93c03` | Historical pointer only | REJECTED as evidence: its base, PR, integration commit, and CI runs certify a different ancestry | discard; retain only this immutable ledger citation |

## Rich-source candidates

| Candidate | Immutable source blob at `d9304b5d...` | Accepted material | Rejected material / required change | Disposition |
|---|---|---|---|---|
| `AFPBarrier/SphericalQEqualityRigidity.lean` | `d5df6b66804fdce591538da14171207847a11058` | PROVED normalized-weight, moment, variance, equality, conductance-symmetry, and abstract connected-transfer algebra | It assumes the loss moment rather than deriving the complete coordinate spherical specialization | manually port and extend against the verified Prompt 2 API |
| `AFPBarrier/QuantitativeGlobalNearRigidity.lean` | `1b50f3051fd556672d654d997ca134253bf4ad0b` | PROVED pointwise and adjacent ratio algebra after their stated domain assumptions | REJECTED literal `incident_loss_cross_bounds`: it omits `delta<1` (countermodel `rate=1`, `delta=2`, `x_1=x_2=-1`, `ell_1=ell_2=-2`); path, diameter, and logarithmic formalization is absent | port only corrected lemmas, add `delta<1`, and formalize the missing finite path/log package |
| `AFPBarrier/QEqualityCovariance.lean` | `59d7bc45441c28bc5135db6218ac4dc0e9cc702b` | PROVED trace/radial scalar identities, centered entrywise expansion, and weighted-octahedron scalar equivalence | Matrix/tangent projection and genuine sampling conclusions remain ordinary; tangent normalization requires `0<ell<2` | port, extend, and keep the antipodal case separate |
| `pure_math/rigidity/GLOBAL_Q_RIGIDITY_THEOREM.md` | `4556eb60a28a5d096343aae9a3d2e6812d43f91` | PROVED Sections 1–5, direct 3/4/5-valent combinatorial uniqueness, face propagation, covariance split, and weighted-octahedron construction, subject to their displayed hypotheses | REJECTED old fixed-box `C_A<1` threshold route: at the exact icosahedral reference with its prescribed `tau`, the old enclosure gives `C_A>1`; it was an extra unsatisfied assumption.  The new proof must use an explicit positive Gram/Heron factor bound. | manually port all accepted derivations and independently re-prove the closed threshold |
| `pure_math/rigidity/triangulation_counterexample_audit.py` | `44b7aebea9a1d642f0c48026722a38623175951a` | COMPUTATIONAL pinned `plantri` commit/blob constants, pinned counts, graph records, exact graph/Gram/hull certificates, and finite hostile-search design | Enumeration through 12 vertices is REJECTED as the all-orders proof.  The old program trusts an arbitrary environment/PATH/cache executable without verifying its source, uses a floating minor-arc check, and represents several negative tests only by strings. | compile and use only the verified pinned source in CI, make algebraic checks exact, execute every negative test, and leave generated source/binary/catalog untracked |
| `pure_math/rigidity/global_near_rigidity_audit.py` | `011a33a7af987f2dc1f129fc7b5a19a58a5c191d` | COMPUTATIONAL variance/resistance/Platonic constants and long-path, small-`kappa`, arc, derivative stress ideas | Despite its description, several checks are high-precision rather than exact.  Its small angle box does not test `(6.16)`–`(6.19)` or the mandated fixed box and hides the icosahedral failure. | port after replacing the angle-box test by the explicit Gram/Heron certificate and closed-threshold stress |
| `pure_math/rigidity/q1_covariance_audit.py` | `e1933aa1b115575d30a9bf60c798b2f060fc0e27` | COMPUTATIONAL weighted-octahedron `T,C,M`, axial iff, sampled-space contraction idea, anisotropy, and five Platonic `Q=1` checks | The tangent formula is undefined at the valid antipodal case `ell=2`; the old script does not coordinate-check all five eigenmaps, assert the displayed minors are nonzero, or execute the norm-contraction certificate. | port with `0<ell<2`, exact coordinate/eigenmap checks, nonzero-minor assertions, and an executable sampling certificate |
| `pure_math/rigidity/APPROACH_REGISTRY.md` | `664154b467be672420d41ddeb949fd8c4e4091ac` | Useful mechanism grouping and adversarial matrix | Obsolete execution note; old angle-certificate route is BLOCKED | rewrite with actual multiagent routes and correction history |
| `pure_math/rigidity/THEOREM_REGISTRY.md` | `6ed7149206fd708d9589b70d702d983dd121d2f2` | Useful hypothesis-granular theorem partition | Threshold and Lean-completeness entries overclaim the rejected old material | rewrite with controlled claim labels and corrected constants |
| `docs/PROMPT3_GLOBAL_RIGIDITY_STAGE_REPORT.md` | `77c9fc7ed351e2b46f88b6a6f5b1c4cf52c16c10` | Useful package inventory | REJECTED as current branch/CI provenance and inherits the old threshold overclaim | rewrite as `P3_STAGE_REPORT.md` |
| `docs/PROMPT3_GLOBAL_RIGIDITY_THEOREM_MAP.md` | `6e5a46ad6e06a82cf846d24057d17e02982ffddf` | Useful artifact taxonomy | Missing corrected threshold and required expanded Lean map | rewrite as `P3_THEOREM_TO_FILE_MAP.md` |
| `.github/workflows/afp-global-rigidity.yml` | `dceeef160d49724e1d3ff14b81026b5301172fd6` | Useful job separation, exact-head checkout, audit, build, and artifact patterns | Wrong base ancestry and allowlist for verified Prompt 2; does not protect all required old refs | discard and build `.github/workflows/afp-prompt3-from-p2-rigidity.yml` from the new contract |

## Permanently discarded source artifacts

These are not theorem sources and are never ported:

| Artifact | Blob | Status and reason |
|---|---|---|
| `.github/p3-patch-00.b64` | `1d93f5f9506789afd38cf3dc12781226eba34e80` | REJECTED generated transport blob |
| `.github/p3-patch-01.b64` | `4766ddcdb439b4fc4614835022ae75991d15ff5a` | REJECTED generated transport blob |
| `.github/p3-patch-02.b64` | `36207efead90d798b7085178cb90b5b8bbd4e6de` | REJECTED generated transport blob |
| `.github/p3-patch-03.b64` | `1d5be025d1412b1cffb4a5d58384ba7f0b2f3fea` | REJECTED generated transport blob |
| `.github/workflows/afp-p3-bootstrap.yml` | `74566dad0c58ca3986c5af38accd1316e6b294db` | REJECTED self-materializing obsolete workflow |
| tracked `__pycache__/*.pyc` files | `3093c688...`, `c7715d68...`, `c687b80e...`, `15254540...`, `7efb1298...`, `9a7d2def...` | REJECTED generated bytecode |

## Truth-safeguard corrections discovered during salvage

1. **REJECTED literal unrestricted tangent normalization.**  Exact global
   `Q=1` permits the two-state antipodal model with `ell=2`, `r=1`.  Then
   `sqrt(ell(2-ell))=0`, so the displayed `u_ij` quotient is undefined.  The
   valid covariance theorem assumes `0<ell<2`; the antipodal equality case is
   retained separately.
2. **REJECTED old angle enclosure, not the stability program.**  The old
   endpoint-product `C_A` bound fails at the mandated icosahedral box.  The
   corrected proof lower-bounds `sin A` explicitly by factoring the spherical
   Gram determinant on the fixed side box; no compactness supremum or added
   assumption remains.  It also uses the fixed box when `eta=0`; the old
   dynamic interval collapsed to `t_-=t_+` and did not satisfy its own strict
   interval display.
3. **REJECTED old Lean incident-loss statement.**  Add `0<=delta<1` (which
   also makes normalized scales positive) before dividing or multiplying its
   bounds.
4. **Connected-component boundary.**  Pointwise and adjacent estimates are
   componentwise.  Finite diameter, graph center, positive spectral gap, and
   one global reference require a connected active component; the final
   theorem states this rather than assigning a finite distance across
   components.

## Port policy

Accepted source text is a lead, not authority.  Every accepted family must
survive an independent ordinary derivation, an adversarial exact audit, and the
verified Prompt 2 Lean/CI gate.  The final ancestry audit must show that none of
the three old Prompt 3 commits is an ancestor of the new candidate.

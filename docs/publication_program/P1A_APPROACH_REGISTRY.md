# P1A approach registry

This registry records mechanism families considered for the sampling-quotient
foundation.  `COMPLETE` means that the mechanism supplied a proof or exact
certificate used by P1A.  `SCREENED` means that it was checked independently
but is not an input to this finite algebraic theorem.  `BLOCKED` is reserved
for a theorem-strength gap; no P1A deliverable is left in that state.

| Mechanism family | Status | Concrete P1A output | Adversarial boundary |
|---|---|---|---|
| covariance / tensor algebra | COMPLETE | jump expansion, covariance trace and radial contraction, `M_i` projection, local Pythagoras | requires unit nodes, trace-free symmetric forms and `d>=2` |
| operator / Gram analysis | COMPLETE | independent evaluation of `R_2 Z_i`, row-representer projection, weighted adjoints, global trace split | `B_i perp Z_i` does not erase mixed rank-one operators |
| generalized eigenvalues | COMPLETE | sampled quotient metric and deflated positive pencil on `K_X^perp` | raw singular determinant is invalid; `im S_2` need not be invariant |
| finite convex geometry | SCREENED | positivity only supplies nonnegative loss weights and automatic `r_i>0` | no hull or lift theorem is needed here |
| frame theory | COMPLETE_SUPPORT | `Z_i` and `M_i` are the sampling/residual frame rows; exact Gram traces | frame vectors may be dependent and sampling may be noninjective |
| representation theory | SCREENED | explains scalar rows in regular families | no irreducibility or multiplicity-free hypothesis is used in the theorem |
| spherical designs | SCREENED_EXTERNAL | harmonic moment language and symmetric example checks | uniform design moments do not imply generator existence or invariance |
| association schemes | SCREENED_EXTERNAL | organizes simplex/cube/cross-polytope eigenspaces | arbitrary unequal weights and conductances need not form a scheme |
| semigroup / resolvent | SCREENED | `T=L+2dI` is used only as a finite operator | no response or long-time estimate is claimed |
| graph rigidity | SCREENED | Platonic and prism fixtures retained | no P3 classification hypothesis enters P1A |
| exact symbolic computation | COMPLETE | 19 fixtures in exact real algebraic arithmetic (rational and certified radical expressions); sign, weight, quotient, basis and compression mutations rejected | computation is regression evidence, not the proof of the all-dimensional identities |
| conic / semidefinite duality | SCREENED | future quotient pencil can be an optimization input | no optimizer or frontier inequality is claimed in P1A |
| asymptotic construction | DEFERRED | none | belongs to P1E after the quotient normalization is frozen |
| transport error analysis | DEFERRED | none | belongs to Paper II and cannot be inferred from harmonic residual alone |
| Lean architecture | COMPLETE_CANDIDATE | finite weighted-row, projection, loss-variance, sampling-kernel and rank core | exact-head build and focused axiom audit are mandatory before acceptance |

## Independent rounds

1. A direct tensor agent derived all local identities and audited the literal
   hypotheses, independently identifying `d>=2` and automatic `r_i>0`.
2. An operator/Gram agent derived the quotient metric, weighted adjoints and
   deflated generalized pencil, and rejected a Frobenius quotient norm.
3. An exact-example adversary supplied non-invariant, aliased, repeated-node,
   nonzero-two-defect and genuinely sampled-exact fixtures.
4. A second proof adversary was instructed to try to corrupt the candidate
   while preserving the displayed tests; its accepted corrections are
   recorded in the stage report.
5. A separate Lean architecture track formalized only the stable finite
   algebraic interfaces after the ordinary proof was complete.

No route was allowed to promote a finite rank pattern, an unproved invariant
subspace, a raw singular determinant, or an external design theorem into the
general theorem.

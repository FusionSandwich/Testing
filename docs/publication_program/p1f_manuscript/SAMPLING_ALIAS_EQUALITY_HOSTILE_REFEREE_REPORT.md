# Sampling-alias and equality hostile-referee report

**Manuscript audited:** `FLAGSHIP_MANUSCRIPT.md`

**Controlling sources:** accepted P1A--P1E ordinary proofs and their exact
audits.

## Verdict

**ACCEPT.** The theorem hierarchy retains the pulled-back sampled quotient,
the whole weighted-sample codomain, normalized trace convention, complete
equality conditions, and every stability transfer parameter. The activated
construction is also sampling-safe: its `d=3` residual is a row multiplier of
the sample vector itself, so aliases are annihilated and no sampling-frame
denominator is introduced.

## Convention audit

| Object | Manuscript convention | Hostile check | Verdict |
|---|---|---|---|
| generator | `(Lf)_i=sum_j a_ij(f_j-f_i)` | negative-semidefinite Markov sign | exact |
| reversibility | `a_ij=gamma_ij/w_i`, `gamma_ij=gamma_ji>=0` | detailed balance in `l2(w)` | exact |
| masses | `w_i>0`, `sum_i w_i=1` | normalization needed for trace identities | visible |
| coordinate shell | `L Omega=-(d-1)Omega` | componentwise target | exact |
| quadratic target | `R_2=(L+2d I)S_2` | continuous eigenvalue is `-2d` | exact |
| alias kernel | `K_X=ker S_2` | nonzero forms may vanish on all nodes | retained |
| quotient metric | `||[A]||_S=||S_2A||_w` | not a Frobenius quotient | exact |
| residual codomain | `Q_X -> l2(w)` | no projection to `im S_2` | leakage retained |
| deflated coordinates | `K_X^{perp_F}` | representation of quotient only | exact |
| sampled exact shell | `im S_2 cap ker(L+2dI)` | distinct from algebraic `ker R_2` | exact |

The indexed sample convention permits repeats. No general theorem silently
assumes connectedness, transitivity, equal masses, sampling injectivity, or
invariance of `im S_2`.

## Displayed theorem audit

| Manuscript result | Attack | Controlling check | Verdict |
|---|---|---|---|
| Proposition 2.1 | raw singular Gram pencil or coefficient norm used | first quotient by `K_X`, then represent on `K_X^{perp_F}`; codomain is all samples | survives |
| Theorem 3.1 | wrong projection coefficient or loss-floor normalization | `M_i=d epsilon_i Z_i/(d-1)+B_i`, `||Z_i||_F^2=(d-1)/d`, `epsilon_i=(d-1)^2/r_i+V_i` | survives |
| Proposition 3.2 | unweighted adjoint or missing mass normalization | `S_2^*f=sum_i w_i f_iZ_i`, `tr G_S=(d-1)/d` | survives |
| Theorem 4.1 | trace saturation substituted for full equality | trace bound, rate step, loss variance and tensor defect remain separate | survives |
| Theorem 5.1 | equality called exact sampled `H_2` | equality is `R_2=c_*S_2` with `c_*>0`, hence sampled exact shell is zero | survives |
| Theorem 5.2 | antipodal tangent vector divided by zero | unit tangent normalization appears only for `0<ell<2`; antipodal case is separate | survives |
| Theorem 5.3 | local tight frames silently glued | global Gram, Markov, detailed-balance, conditional-moment and cycle conditions remain | survives |
| Corollary 5.5 | unrestricted Platonic classification | dimension, nonantipodality, strict convexity, one-skeleton support, common rate and degree hypotheses remain | survives |
| Theorem 6.1 | incorrect stability variables/constants | `q_i=s_i+v_i`, tensor coefficient and `eta=2delta+delta^2` match P1D | survives |
| Corollaries 6.2--6.3 | weighted average promoted to uniform control | `w_min`, `kappa`, graph, sampling, shell, frame and feature margins are explicit | survives |
| Theorem 7.1 | edge angle confused with fill distance | `h=pi/N`, edge angle `2h`, residual `4sin^2h`, rate cap `pi^2/(8h^2)` | survives |
| Theorem 7.2 | coefficient alias or sampling-frame denominator | rowwise `R_2A(i)=c_iS_2A(i)` implies `K_X subset ker R_2`; weighted multiplication norm is `max_i c_i` | survives |
| Theorem 7.2 | rate/loss convention mismatch | `mu_i=(1/2)sum gamma ell`, `a_ij=gamma_ij/mu_i`, `r_i=2sum gamma/sum gamma ell` | survives |

## Exact alias attacks

- Tetrahedral, octahedral, cubical, simplex, and cross-polytope examples have
  nontrivial `K_X`; any coefficient-space denominator would fail on them.
- At frontier equality `R_2=c_*S_2`, so `ker R_2=ker S_2` and the genuinely
  sampled exact degree-two space is zero. Equality is optimal positive
  residual, not exact degree-two reproduction.
- The P1D sampling transfer explicitly pays `alpha_X^{-1/2}` because it moves
  from coefficient Frobenius control to the sampled quotient. The P1E ring
  bound does not pay this factor for a different reason: it proves an exact
  row multiplier before taking the quotient.

## Construction-specific hostile checks

1. Each undirected ring edge receives one shared conductance; rowwise
   feasibility is not substituted for reversibility.
2. Transition column sum `1/2`, mask moments, force signs and row scalings are
   audited literally.
3. The pole, first ring, ordinary rows, both transition endpoints and equator
   are separate row classes.
4. Strict positivity is proved through limiting cone, Cauchy, floor/ceiling,
   polar, and global telescoping margins.
5. The quadratic residual bound is taken in the exact P1A quotient convention.
6. Robustness fixes support, counts, phases, masks, horizontal jumps and
   reflection; arbitrary motion is not claimed.

## Residual conditions

- Any later display of a P1D edge, path, resistance, spectral-gap, congestion
  or frame-repair estimate must carry its complete hypotheses and constants.
- The matching construction remains restricted to `d=2,3`.
- The source map must distinguish ordinary proof, exact audit, finite
  regression and Lean finite algebra.
- Release workflow execution and archive freezing are reproducibility facts,
  not mathematical proof steps.

The deterministic P1A--P1E audits completed in the shared worktree. Markdown
and whitespace checks support this convention audit but do not replace the
ordinary proofs.

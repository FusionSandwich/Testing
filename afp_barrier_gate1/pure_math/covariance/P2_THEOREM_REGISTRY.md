# Prompt 2 theorem registry

| theorem | exact hypotheses | conclusion | dependencies | counterexample/sharpness | claim label | completion gap |
|---|---|---|---|---|---|---|
| covariance identity | finite (I), coordinate eigenmap; no signs | (LS_A=-2\lambda S_A+\operatorname{tr}(AC_i)) | finite sums | signed examples allowed | PROVED | final Lean rerun |
| arbitrary target | covariance identity, any (c,\mu) | displayed pointwise iff; (\mu=0) separated | algebra | none | PROVED | weighted centering corollary |
| sphere factorization | unit nodes, (\lambda=d-1), traceless forms | (R=(L+2dI)S) | covariance | curvature shift 2 | PROVED | explicit Lean theorem |
| genuine sampled dimension | finite-dimensional maps | (K\subset E_f), (\dim E_s=\operatorname{rank}S-\operatorname{rank}R) | rank-nullity | tetra/octa/cube aliases | PROVED | full Lean dimension equality |
| positive full-module no-go | (a_{ij}\ge0,d>1), coordinate eigenmap | not every tracefree sampled form is exact | radial sum of squares | signed cube | PROVED | final proof audit |
| one-shell tangent-isotropy rigidity | every nonzero embedded jump on one non-antipodal shell; coincident jumps omitted; full tangent second moment | (R=DS,D>0,E_f=K,E_s=0) | eigenmap split | full-dimensional hexagonal prism without isotropy has (\dim E_s=2) | PROVED | finite algebraic Lean core |
| equivariant rank gap | positive sphere eigenmap and equivariance | (\operatorname{rank}R\ge\kappa(V_2)); irreducible (V_2\Rightarrow E_s=0) | quotient residual | cube/hexagon equality | PROVED | explicit isotypic proof |
| corrected scalar decomposition | self-adjoint equivariant (L), preserved irreducible (U), or full ambient isotypic component | real scalar on (U) | real spectral theorem | two-layer (D_3) disproves omitted invariance | PROVED | tracked exact counterexample |
| Platonic table | exact shortest-edge models | ranks ((3,2,3,5,5)), all (E_s=0) | one-shell theorem + exact minors | five equality cases | COMPUTATIONAL | record residual minors and shortest shells |
| signed cube restoration | cube, unit masses, complete graph, full cross-quadratic module | coordinates (-2), quadratics (-6), (\dim E_s=3), (N_-^{E,min}=2) | orbit averaging | optimum only for full module | PROVED | explicit averaging and dual/alias checks |
| product resonance | finite generator, two eigenfunctions | arbitrary target and resonance iff | finite product identity | Boolean square | PROVED | final Lean rerun |
| semigroup variance | finite differentiable semigroup, eigenfunction | variance formula iff constant (\Gamma) at derivative level | matrix exponential | Boolean positive variance | PROVED | expand ordinary proof |
| Jensen equality | positive Markov kernel | equality iff constant on support; irreducible (t>0) gives global constant | uniformization | not resonance | EXTERNAL | state standard input exactly |
| Pell hierarchy | continuous (S^2) harmonics | admissible doubled components are ((1+\sqrt2)^{4m+1}) | Clebsch--Gordan, Pell | first ((14,20)) | EXTERNAL | prove parity transfer and record recurrence |
| sampling separation | exact sampled harmonic spaces | distinct targets iff internal directness for signed realization; rank bound | eigenspace independence | Platonic (H_2/H_4) aliases | PROVED | finite Lean direct-sum theorem and explicit aliases |

External inputs are standard finite rank-nullity, finite real representation
semisimplicity/spectral theory, Clebsch--Gordan decomposition on (S^2), and
the elementary classification of negative Pell solutions.  No external input
is used without the sampling quotient or project sign conventions being
transferred explicitly.

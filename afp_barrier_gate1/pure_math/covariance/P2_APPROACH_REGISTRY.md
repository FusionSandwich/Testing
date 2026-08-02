# Prompt 2 mechanism registry

Claim labels are restricted to PROVED, EXTERNAL, COMPUTATIONAL, CONJECTURE, and
REJECTED. A PROVED mechanism has a complete ordinary argument under the stated
hypotheses; COMPUTATIONAL denotes an exact finite certificate, not a general
proof.

`BLOCKED` below is a route-control disposition, not a claim label. It records
an invalid proof mechanism whose conclusion is instead classified in the main
registry under one of the five claim labels.

| family | mechanism and exact boundary | claim label | decisive proof or certificate |
|---|---|---|---|
| covariance algebra | expand each quadratic jump and contract \(C_i\); no signs or reversibility | PROVED | \(R_X=(L+2dI)S_X\) |
| weighted centering | detailed balance, nonempty state set, positive weights, and nonzero target | PROVED | weighted conservation; zero target leaves \(c\) free |
| sampling quotient | distinguish form kernel from sampled image | PROVED | \(K_X\subset E_{\rm form}\), quotient dimension |
| positive radial obstruction | nonempty finite state set, \(d>1\), nonnegative rates, unit eigenmap with \(L\Phi=-(d-1)\Phi\) | PROVED | strict radial sum of squares and Frobenius test |
| signed one-shell geometry | \(d>1\), unit eigenmap with \(L\Phi=-(d-1)\Phi\), nonempty noncoincident shell, \(0<\ell_i<2\), full signed tangent moment | PROVED | \(R_X=DS_X\), \(D_{ii}=d\ell_i>0\) |
| positive sharpness | hexagonal prism without tangent isotropy | PROVED | ordinary Fourier proof plus exact minors |
| prism finite regression | graph action, matrices, ranks, minors, anisotropy | COMPUTATIONAL | exact_quadratic_covariance_audit.py |
| equivariant kernel decomposition | orthogonal equivariant embedding, invariant generator \(a_{gi,gj}=a_{ij}\), and multiplicity-free real form module | PROVED | Maschke plus restrictions of equivariant maps |
| quotient rank gap | positive residual, invariant generator, and irreducible constituents of \(V_2\) | PROVED | \(\operatorname{rank}R_X\ge\kappa(V_2)\) |
| naive symmetry scalarity | equivariance of one selected irreducible copy without invariance | REJECTED | exact two-layer \(D_3\) counterexample |
| corrected symmetry | irreducible \(U\), self-adjoint \(L\), and either explicit \(L(U)\subseteq U\) or \(U\) equal to its entire ambient isotypic component | PROVED | invariant real eigenspaces force a scalar |
| Platonic classification | five positive shortest-edge models | PROVED | one-shell theorem plus exact algebraic minors |
| Platonic finite regression | exact ranks, kernels, rates, shells, and minors | COMPUTATIONAL | exact_quadratic_covariance_audit.py |
| signed cube restoration | arbitrary symmetric conductance feasible for coordinate target \(-2\) and cross-module target \(-6\), averaged over the full cube group | PROVED | convex averaging, orbit equations, global lower bound, KKT |
| signed cube finite regression | optimizer, aliases, 48 actions, KKT, positive comparison | COMPUTATIONAL | exact_signed_restoration_audit.py |
| product resonance | finite jump-product expansion; no signs | PROVED | SpectralProductAlgebra.lean and ordinary expansion |
| blanket positive square obstruction | claim that no nonzero centered doubled square exists | REJECTED | positive Boolean square |
| semigroup resonance | exponentiate the two eigenfunction identities and differentiate conversely | PROVED | finite matrix exponential |
| Jensen equality | positive Markov kernel and irreducible uniformization | EXTERNAL | standard variance-support equality |
| continuous harmonic product | \(\operatorname{Sym}^2(H_\ell)=\bigoplus_{r=0}^{\ell}H_{2r}\) on \(S^2\) | EXTERNAL | Clebsch--Gordan decomposition |
| parity-filtered Pell completeness | all positive solutions of the negative Pell equation | EXTERNAL | standard Pell classification; project parity transfer is explicit |
| corrected sampled hierarchy | one common operator acts scalarly on spaces grouped by target eigenvalue | PROVED | Lagrange spectral projections and constants-safe converse |
| unrestricted distinct-degree hierarchy | omit \(d\ge2\) or distinct target eigenvalues | REJECTED | \(d=1\) singleton has \(V_0=V_1\) |
| Platonic harmonic aliases | exact \(H_2/H_4\) ranks and polynomial witnesses | COMPUTATIONAL | exact_spectral_product_audit.py |
| universal positive hierarchy | positivity alone yields a new all-degree obstruction | REJECTED | aliases and Boolean resonance reduce it to pointwise residuals |

## Blocked proof routes

| attempted route | route state | obstruction |
|---|---|---|
| identify algebraic exact forms with sampled modes | BLOCKED | sampling aliases require the quotient by \(K_X\) |
| infer a positive obstruction in the signed theorem | BLOCKED | the one-shell result permits signed rates; invertibility comes from \(d\ell_i>0\) |
| infer scalarity from equivariance of a selected copy | BLOCKED | an isomorphic ambient copy can mix unless invariance is proved |
| certify ranks by floating-point thresholds | BLOCKED | exact rational or \(\mathbb Q(\sqrt5)\) minors are required |
| restrict signed-cube optimality to orbit rates without averaging | BLOCKED | arbitrary feasibility, constraint preservation, and convex nonincrease must first be proved |
| omit constants or add them twice in the signed converse | BLOCKED | constants belong exactly once to the zero-target eigenvalue class |
| count distinct degrees without checking target collisions | BLOCKED | the \(d=1\) degree-zero/one collision invalidates the literal route |

## Standard-input boundary

Rank-nullity, finite real semisimplicity, self-adjoint spectral theory, convex
subgradient optimality, Jensen equality, Clebsch--Gordan decomposition, and
negative-Pell completeness are standard inputs. The candidate project
contribution is the combined sampling-kernel-aware covariance framework,
signed one-shell rigidity, positive prism sharpness, equivariant quotient rank
gap, signed-cube optimum, and their sampling-safe interpretation. No priority
claim is made from the covariance identity, finite ranks, or standard inputs
alone.

# Prompt 2 approach registry

Completion audit note: this registry came from the saved WIP commit.  An
`ACCEPTED` route records a mathematically viable mechanism, not completion of
the mandatory Lean, exact-regression, documentation, or CI gate.  The durable
gate state is tracked in `P2_COMPLETION_PROGRESS.md` and
`docs/P2_THEOREM_TO_FILE_MAP.md`.

Routes are grouped by mechanism.  `BLOCKED` means a theorem-strength missing
lemma or exact counterexample ended that route; it is not partial completion.

| family | independent mechanism | status | decisive invariant/certificate |
|---|---|---|---|
| covariance algebra | expand each quadratic jump and contract (C_i) | ACCEPTED | (R=(L+2dI)S), (K_X\subset E_{form}) |
| quotient linear algebra | pass residual through sampled quotient | ACCEPTED | (E_{sample}\cong E_{form}/K_X), rank gap |
| positive radial covariance | test (M_i) on (P_0(\Phi_i\Phi_i^T)) | ACCEPTED | strictly positive radial sum of squares |
| local shell geometry | combine one shell with full tangent tight frame | ACCEPTED MAIN | exact (R=DS), (D>0) |
| covariance propagation | irreducible quotient image under group action | ACCEPTED | (\operatorname{rank}R\ge\kappa(V_2)) |
| naive symmetry scalarity | multiplicity-free sampled subspace alone | REJECTED | exact positive reversible (D_3) counterexample; (V_2) not invariant |
| corrected symmetry | add (L(V_2)\subset V_2) or ambient multiplicity one | ACCEPTED STANDARD | real self-adjoint eigenspaces are invariant |
| association schemes | orbital conductances and sampled products | ACCEPTED SUPPORT | Platonic and cube orbit certificates |
| spherical designs | harmonic evaluation/tight frames | ACCEPTED INPUT | exact evaluation ranks over (\mathbb Q(\sqrt5)) |
| signed construction | cube Hamming orbit rates | ACCEPTED | ((r_1,r_2,r_3)=(3/2,0,-1/2)), (N_-^E=2) |
| semigroup | differentiate variance identity at zero | ACCEPTED | recovers constant carré-du-champ criterion |
| Jensen obstruction | confuse zero variance with centered resonance | REJECTED | four-state Boolean square has positive variance and exact resonance |
| harmonic product | Clebsch--Gordan plus negative Pell equation | ACCEPTED BOUNDED | first nonconstant resonance ((14,20)) |
| sampled hierarchy | distinct desired eigenvalues force direct sampled sum | ACCEPTED | (\sum_J\operatorname{rank}E_J\le |I|) |
| universal positive hierarchy | repeat product residual at each degree | BLOCKED/REJECTED | no new restriction beyond (\Gamma) without extra hypotheses |
| Lean architecture | finite sums, functions, pointwise predicates | ACCEPTED | three narrow no-positivity modules, no placeholders |
| weighted centering | reversible weighted conservation | BLOCKED | WIP has no formal corollary |
| explicit sphere/one-shell formalization | coordinate-indexed finite matrices | BLOCKED | required residual and `R=DS_X` modules absent |
| exact invariance counterexample | two-layer `D_3` graph | BLOCKED | theorem draft names it but no tracked implementation exists |
| final verification | dedicated Prompt-2 workflow and exact-head artifact | BLOCKED | no WIP workflow or successful run |

Adversarial checks explicitly covered sampling aliases, coincident nodes,
antipodes, signed rates, hidden equal weights, real representation types,
ambient multiplicities, conservation, spherical eigenvalue shift, and the
difference between one mode and a full module.

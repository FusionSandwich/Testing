# Prompt 3 final integration record

## Source and ancestry

The rich Prompt 3 package enters the final pure-mathematics baseline through the clean, non-destructive descendant:

```text
clean branch:
    agent/afp-pure-math-p3-p4-final-acceptance

preserved PR #30 source commit:
    19a5001158cb40fbb0adc92813cc3abd5dfa583d

rich Prompt 3 source commit:
    f1ef5b3c3107d2dfc835ed84c443eb82d752cb56
rich Prompt 3 source tree:
    2d6214753fa7ac4ffcda941f7b9dcc431c7b0b5c

accepted target ancestor:
    94aebf6578a43516cce4bb7c042fc57681c93890
accepted target tree:
    872828f5099aeb7df4e0ab871b9e881de4054a97
```

PR #25 remains preserved source history. PR #28 remains a protected divergent audit/implementation history; no PR #28 commit is merged or cherry-picked. PR #23 remains provenance-only history. The exact branch table and source blob ledger are in `P3_P4_BRANCH_PRESERVATION_REGISTRY.md` and `P3_P4_FILE_RECONCILIATION_LEDGER.md`.

## Integrated theorem package

### Exact equality transfer

For the positive reversible spherical coordinate eigenmap,

```text
x_ij=r_i ell_ij/2,
p_ij=a_ij/r_i,
Q_i=r_i epsilon_i/4,
```

the package proves

```text
sum_j p_ij=1,
sum_j p_ij x_ij=1,
Q_i=sum_j p_ij x_ij^2,
Q_i-1=sum_j p_ij(x_ij-1)^2.
```

At `Q_i=1`, all active incident losses equal `2/r_i`; shared positive conductances and connectedness propagate a common row rate and active-edge loss.

### Restricted classification

Under the complete finite simple, injective, minor-arc, noncrossing, geodesically convex, disjoint-interior, full-round-sphere, no-cone-defect, all-edges-active triangulation hypotheses, exact equality yields only the regular tetrahedral, octahedral, or icosahedral realization, up to `O(3)` and up to `SO(3)` after orientation is fixed.

The proof uses common side length and face angle, angle sum `2*pi`, Euler restriction, direct combinatorial uniqueness for `q=3,4,5`, and forced adjacent-face propagation. The source-pinned plantri census is a hostile finite audit, not the proof.

### Quantitative near-rigidity

For `p_ij>=kappa>0`, `1<=Q_i<=1+eta`, and

```text
delta=sqrt(eta/kappa)<1,
q_delta=(1+delta)/(1-delta),
s_delta=log(q_delta),
h_delta=-log(1-delta),
```

the package proves explicit pointwise, adjacent, path, diameter, graph-radius, edge-loss, and arclength bounds. With the reversible normalization

```text
mu_i=w_i r_i,
pi_i=mu_i/sum_k mu_k,
P_ij=p_ij,
c_ij=pi_i p_ij,
```

it proves

```text
E_P(log r)<=2eta/(1-delta)^2,
Var_pi(log r)<=2eta/((1-delta)^2 lambda_P),
|log r_i-log r_j|
  <=sqrt(2eta R_eff(i,j))/(1-delta).
```

### Quantitative triangulation stability

The accepted angle route is the positive spherical Gram/Heron determinant factorization, not the failed endpoint-product enclosure. It gives positive angle-sine floors, explicit derivative constants, exact integer-valence separation, and an explicit edge-sup bound to the corresponding Platonic edge length. The accepted conservative `eta_*` values are recorded in the final theorem registry and exact audit.

### Covariance interaction

The package proves `tr C_i=4`, `Omega_i^T C_i Omega_i=4Q_i/r_i`, and, at exact `Q_i=1` with `0<ell_i<2`,

```text
C_i=2(2-ell_i)T_i+2ell_i Omega_i Omega_i^T,
M_i=3ell_i(Omega_i Omega_i^T-I/3)
    +2(2-ell_i)(T_i-P_i/2).
```

Axial covariance holds iff `T_i=P_i/2`. The antipodal case is separate: `ell=2`, `r=1`, and `C=4 Omega Omega^T`, with no geometrically determined normalized tangent direction.

The weighted-octahedral family proves that `Q=1` does not force axial covariance and that tangential anisotropy can approach operator norm `1/2` at zero scalar defect. Its genuine sampled degree-two exact space is `{0}`, certified by the exact positive determinant of `P+2I`.

## Formal repairs verified by the gate

The integrated Lean source retains:

```text
simpa [mul_comm]
```

for the weighted-product orientation, explicit multiplication by nonnegative inverses for adjacent-rate and incident-loss inequalities, and the necessary `0<=delta<1` domain. The redundant post-simplification tactic is absent.

The aggregate imports and focused axiom audit include the new equality, pointwise, rate, incident-loss, radial covariance, antipodal, and weighted-octahedral declarations. The independent nanoda slice exports the same accepted finite-algebra core with `sorryAx` forbidden.

## Exact computational record

The source-pinned plantri audit verifies the exact counts

```text
V=4       1
V=5       1
V=6       2
V=7       5
V=8      14
V=9      50
V=10    233
V=11   1249
V=12   7595
total   9150
```

and isolates the tetrahedral, octahedral, and icosahedral graphs as the only equivelar candidates compatible with the theorem’s round equal-angle mechanism in that range.

## Integration policy

The target may be advanced only by a non-forced fast-forward to the literal implementation head after all six workflows pass that exact SHA. If the target moves first, its current head must be merged additively into the closeout branch and all six workflows repeated. No untested synthetic merge is accepted.

The literal final candidate SHA/tree, implementation-head run/job identifiers, artifacts and digests, integration method, final target SHA/tree, post-integration run/job identifiers, preservation-comment IDs, and review resolution IDs are recorded in the authoritative acceptance comment on the clean final reconciliation PR. That comment is incorporated here by reference.

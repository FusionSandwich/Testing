# P1E Coxeter--harmonic source and claim map

This map prevents conditional compiler statements from being promoted to an
all-dimensional construction.

## Unconditional results

| Claim | Source | Audit |
|---|---|---|
| For \(d=2\), regular \(N\)-gons, \(N\geq5\), give positive reversible generators with \(L1=0\), \(L\Omega=-\Omega\), \(\mathfrak D_2=2(1-\cos(2\pi/N))\), \(r=(1-\cos(2\pi/N))^{-1}\), and \(\mathfrak D_2r=2\). | P1E_COXETER_HARMONIC_CONSTRUCTION.md, (0.1) | audit_polygon_symbolic, audit_polygon_level, and interval polygon fixtures |
| A zero of the normalized tangent tension built from shared positive coefficients gives positive reversible masses and exact \(H_0/H_1\). | Same file, (1.1)--(1.4) | shared-stress fixtures |
| The explicit four-point law on every one-dimensional lattice coset has positive weights, zero first and third moments, and a uniform second-moment interval. Tensor products kill the full cubic tensor. | Same file, (2.13)--(2.13h) | balanced_coset_law, audit_crystal_connector, audit_tensor_crystal_connector |
| On a **given genuine finite periodic crystal**, strong \(h^{n-2}\) tree connectors plus tensor subtraction give a positive acoustic/optical principal symbol with an \(h^{-2}\) optical gap and second-order midpoint truncation. | Same file, (2.14)--(2.18b) | finite connector fixtures; the global-crystal premise is not audited because it is false for raw \(K_N\) |
| On \(W\)-equivariant tangent fields, finite symmetry removes rotational and, for \(n=2\), conformal Jacobi kernels. | Same file, Section 3 | representation-theoretic proof in text |
| Given a globally consistent second-order compiler and the displayed uniform discrete inverse, Newton correction gives exact \(H_1\) and preserves the \(O(h^2)\) quadratic row bound. | Same file, Sections 4--6 | conditional finite algebra only |
| The weighted cap estimate includes the fill constant \(H=H_0+1\): \(\alpha_d=\frac{\omega_-}{4d}(2/\pi)^{d-2}(8H\sqrt d)^{-(d-1)}\). | Same file, (6.11)--(6.12) | elementary cap-volume proof in text |

## Exact rejections

| Rejected claim | Certificate | Audit |
|---|---|---|
| Raw \(K_N\) is a finite-basis periodic crystal in every mixed stratum chart. | For \(d=4\), \((|Z|,|B|)=(2,3)\), the points satisfy \(p+q+|a|\equiv N\pmod3\). Every translation period has zero \(a\)-component, so no full-rank period lattice exists. | audit_parabolic_nonperiodicity_blocker |
| Conductance-\(h^n\) optical connectors suffice for an ordinary discrete \(C^{2,\alpha}\) inverse. | A basis-oscillatory mode has normalized eigenvalue \(O(1)\) but discrete second derivative \(O(h^{-2})\). | rejected scaling note in the construction file |
| A rotation gauge alone makes the \(S^2\) Jacobi operator invertible. | The three fields \(P_xa\) are conformal zero modes. | Section 3 and the harmonic audit |
| Local positive row feasibility implies a shared reversible stress. | Exact octahedral Kolmogorov cycle ratio \(21/4\). | audit_cycle_ratio_blocker |
| The current Coxeter draft proves an all-\(d\) family. | It assumes the compiler premise contradicted by the raw-\(K_N\) residue certificate. | status block and Section 2.1 |

## Missing theorem-strength item

The route becomes complete only after one supplies all of the following as a
single compatible construction:

1. a globally defined \(W\)-invariant completed or reflected stratified node
   family, with explicit ownership and overlap identifications;
2. uniform fill, separation, mesh ratio, degree, and angular-window bounds;
3. a shared undirected positive midpoint edge set across every stratum and
   overlap, with exact first/third moment cancellation and a uniform tensor
   floor;
4. a proof that every local completed lattice is realized by the same global
   node set, without duplicates, near-collisions, dead boundary layers, or
   unmatched connector endpoints;
5. a uniform discrete Schauder/spectral inverse across the actual stratified
   interfaces, not merely the Bloch inverse of a hypothetical periodic
   crystal.

Until these five items are proved, the higher-dimensional theorem remains
conditional and must not be used as the P1E matching upper construction.

## Deterministic command

Run:

    python3 afp_barrier_gate1/pure_math/covariance/p1e_asymptotic_family_audit.py

The current inventory has 25 exact/interval fixtures. It verifies the
unconditional finite algebra and deliberately rejects the raw-\(K_N\)
periodicity mutation; it does not substitute finite computation for the
missing global compiler.

# AFP Barrier — Gate 2 closure review

**Closure date:** 18 July 2026

## Decision

**Pass, with a narrowed publication claim.**

Charles Bienvenue’s 2025 paper and the corresponding `Radiant.jl` implementation answer the outstanding operator and compatibility questions sufficiently to close the source-audit gate. The standard finite-jump carré-du-champ mechanism is not claimed as new. The candidate contribution is the AFP-specific no-go theorem together with reversible shared-edge feasibility, defect optimization, and dual certification.

The detailed five-question resolution is in [`afp_barrier_gate1/GATE2.md`](afp_barrier_gate1/GATE2.md).

## Source conclusions

1. **Operator convention:** Radiant assembles the unshifted AFP generator as
   \[
   (Lf)_i=\frac1{w_i}\sum_{j\sim i}\gamma_{ij}(f_j-f_i),
   \qquad \gamma_{ij}=\gamma_{ji}.
   \]
   Hence `WL=LᵀW`; the weighted adjoint is the same operator. The later diagonal `λ₀` shift belongs to the scattering-matrix/total-cross-section decomposition.

2. **Degree-two priority:** no explicit complete-degree-two monotonicity obstruction was located in Bienvenue et al., Radiant, or the principal AFP references checked. The underlying jump-versus-diffusion chain-rule mechanism is standard, so only the AFP specialization and consequences are candidate novelty.

3. **Delaunay comparison:** Charles’s construction and the Izmestiev–Lam spherical Delaunay Laplacian are members of the same normalized reversible graph-Laplacian class. They coincide up to scale only when the prescribed quadrature weights are proportional to the canonical geometric vertex weights and the conductances scale accordingly.

4. **Compatibility:** weighted centering is necessary and sufficient for a dense strictly positive reversible degree-one-exact construction. For a prescribed local graph, positivity is exactly a finite cone-membership problem. Infinitesimal rigidity plus centering guarantees a signed exact solution; positivity is additional.

5. **Dual certificate:** the local positive feasibility and defect-minimization problems admit Farkas and LP dual certificates. A dual nodal displacement field can certify infeasibility or provide a rigorous lower bound and optimality certificate.

## New Lean modules

- `ReversibleConductance.lean`
  - detailed balance;
  - weighted self-adjointness;
  - weighted conservation;
  - weighted-centering necessity;
  - conductance-form degree-two obstruction.

- `CompleteGraph.lean`
  - explicit strictly positive dense construction;
  - exact eigenvalue theorem for every weighted-mean-zero sampled function;
  - necessity and sufficiency of weighted centering for coordinate exactness.

- `DualCertificate.lean`
  - finite transpose identity;
  - sound Farkas-type infeasibility certificates;
  - positive-LP weak duality.

## Lean validation

The closure build used Lean `v4.30.0` and completed all `2952` Lake jobs. The axiom audit covered `42` public theorems. No `sorry`, `admit`, `sorryAx`, or user-declared axiom was present. The only dependencies reported were the standard Mathlib foundations `propext`, `Classical.choice`, and `Quot.sound`.

GitHub Actions run: `29633967639`  
Source branch commit: `9434ab3efd6d0f7ffef3e183ad2194f636d83948`  
Built PR merge commit: `ec610a767550abc0aa5e679f37ba97de8d2908b9`  
Artifact digest: `sha256:e67e6c5e52ee0348de9f1e2a72fe0826a8250eccd7d97c2673b4e5b05f5174f1`

## Implementation audit finding

Radiant checks `pinv(Γ)Γ≈I`, which verifies full column rank. A robust general-purpose implementation should additionally verify the actual residual and positivity:

```julia
γ = pinv(Γ) * Q
norm(Γ * γ - Q)
minimum(γ)
```

A positive LP can replace or supplement the pseudoinverse and return a dual certificate.

## Gate 3 target

The next gate should prove a local family-level theorem—such as positivity for a specified quadrature/Delaunay family or sharp `Theta(h^2)` optimal defect scaling—and compare the LP-optimal operator against Radiant’s pseudoinverse construction in transport benchmarks.

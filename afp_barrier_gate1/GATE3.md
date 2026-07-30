# Gate 3 — Gauss–Legendre–Chebyshev tensor-product AFP analysis

**Status:** active proof and verification stage  
**Audit date:** 30 July 2026  
**Radiant source pinned for comparison:** `CBienvenue/Radiant.jl@205e07faa105854b0f27e95a02f01ebed08f84c1`

## 1. Revised objective

The initial Gate 3 objective was to prove, for every Gauss–Legendre–Chebyshev
(GLC) order, positivity of the tensor-product angular Fokker–Planck stencil and
a global `Theta(N^-2)` degree-two defect estimate.

The source and literature audit changes that objective:

1. The product-quadrature scheme of Morel et al. is already presented as
   self-adjoint, monotone, and nonpositive definite. Radiant implements that
   explicit stencil for GLC quadrature.
2. Several *uniform* Gauss–Legendre node/weight inequalities used in rigorous
   second-order convergence arguments remain conjectural or supported by
   asymptotic evidence rather than a completed all-node proof.
3. The new contribution should therefore focus on exact second-harmonic defect
   identities and a previously overlooked polar stiffness mechanism, while
   stating the global uniform defect law as a research target until the needed
   Gauss–Legendre inequalities are proved.

The current Gate 3 targets are:

- machine-check the exact tensor-product algebra;
- derive the fixed-endpoint polar asymptotics rigorously from standard Bessel
  expansions of Gauss–Legendre zeros;
- audit the complete finite family over a large deterministic order range;
- separate proved statements from numerically supported uniform conjectures.

## 2. Radiant's GLC stencil

Let `N >= 2`. Let

\[
-1 < \mu_1 < \cdots < \mu_N < 1,
\qquad w_n>0,
\qquad \rho_n=\sqrt{1-\mu_n^2}
\]

be the sorted `N`-point Gauss–Legendre nodes and weights. Radiant uses `2N`
equispaced azimuthal angles

\[
\phi_j=\frac{\pi}{N}\left(j-\frac12\right),
\qquad h=\frac{\pi}{N}.
\]

Define the Morel interface moments

\[
\beta_{1/2}=0,
\qquad
\beta_{n+1/2}=\beta_{n-1/2}-2w_n\mu_n,
\qquad
\beta_{N+1/2}=0.
\]

The latitude rates are

\[
a_n^-=
\frac{\beta_{n-1/2}}{w_n(\mu_n-\mu_{n-1})},
\qquad
a_n^+=
\frac{\beta_{n+1/2}}{w_n(\mu_{n+1}-\mu_n)},
\]

with missing boundary terms omitted. Let

\[
c_n=a_n^-(\rho_{n-1}-\rho_n)
     +a_n^+(\rho_{n+1}-\rho_n),
\]

\[
K_n=2\rho_n^2+\rho_n c_n,
\]

and

\[
q_n=\frac{K_n}{2\rho_n^2(1-\cos h)}.
\]

The unshifted row action is

\[
\begin{aligned}
(Lf)_{n,j}={}&a_n^-(f_{n-1,j}-f_{n,j})
+a_n^+(f_{n+1,j}-f_{n,j})\\
&+q_n(f_{n,j-1}+f_{n,j+1}-2f_{n,j}).
\end{aligned}
\]

These equations were reconstructed directly from Radiant's
`fokker_planck_finite_difference.jl` rather than inferred from numerical output.

## 3. Exact algebraic results

The following results are formalized in `AFPBarrier/GLCTensorProduct.lean`.
They do not assume asymptotic approximations.

### 3.1 Exact latitude coordinate mode

The interface recurrence gives

\[
a_n^-(\mu_{n-1}-\mu_n)
+a_n^+(\mu_{n+1}-\mu_n)
=-2\mu_n.
\]

Thus the axial Cartesian coordinate is an exact eigenmode with eigenvalue `-2`.

### 3.2 Exact transverse coordinate modes

For an equispaced azimuthal grid,

\[
u_{j-1}+u_{j+1}-2u_j
=-2(1-\cos h)u_j
\]

for `u_j=cos(phi_j)` and `u_j=sin(phi_j)`. Substituting the definition of
`q_n` gives

\[
L(\rho_n\cos\phi_j)=-2\rho_n\cos\phi_j,
\]

\[
L(\rho_n\sin\phi_j)=-2\rho_n\sin\phi_j.
\]

### 3.3 Geometric identity for `K_n`

Let

\[
d_n^- = 1-(\rho_n\rho_{n-1}+\mu_n\mu_{n-1}),
\qquad
d_n^+ = 1-(\rho_n\rho_{n+1}+\mu_n\mu_{n+1}).
\]

These are chord deficits between neighbouring meridian nodes. Exact coordinate
balance implies

\[
\boxed{
K_n=2-a_n^-d_n^- -a_n^+d_n^+.
}
\]

Consequently, nonnegative latitude rates imply `K_n <= 2`. Positivity of
`K_n` is exactly the remaining condition needed for positive azimuthal rates.

### 3.4 Exact degree-two peak defect

At node `p=(rho_n cos(phi_j),rho_n sin(phi_j),mu_n)`, let

\[
g_p(\Omega)=p\cdot\Omega.
\]

Since `g_p(p)=1`, define the peak degree-two defect by

\[
\varepsilon_n=L(g_p^2)(p)+4.
\]

The finite jump-generator identity gives

\[
\boxed{
\varepsilon_n
=a_n^-(d_n^-)^2+a_n^+(d_n^+)^2
+K_n\rho_n^2(1-\cos h).
}
\]

This is independent of the azimuth index.

### 3.5 Exact row rate

The outgoing rate is

\[
\boxed{
R_n=a_n^-+a_n^+
+\frac{K_n}{\rho_n^2(1-\cos h)}.
}
\]

Together with the Gate 1 theorem, every positive row satisfies

\[
R_n\varepsilon_n\ge 4.
\]

## 4. Exact outer-ring reduction

For the southern outer ring, only the upper latitude neighbour exists. The
weight cancels exactly:

\[
a_1^+=\frac{-2\mu_1}{\mu_2-\mu_1}.
\]

Therefore

\[
\boxed{
K_1=2\rho_1^2
-2\mu_1\rho_1
\frac{\rho_2-\rho_1}{\mu_2-\mu_1}.
}
\]

Because `mu_1<0`, `mu_2>mu_1`, `rho_1>0`, and `rho_2>=rho_1`, this expression
is strictly positive. The corresponding positivity theorem is included in the
Lean file.

## 5. Polar Bessel asymptotics

Let

\[
\kappa=N+\frac12
\]

and let `j_1,j_2` be the first two positive zeros of `J_0`. Standard endpoint
Gauss–Legendre asymptotics give, for the two southern extreme nodes,

\[
\mu_k=-1+\frac{j_k^2}{2\kappa^2}+O(\kappa^{-4}),
\qquad
\rho_k=\frac{j_k}{\kappa}+O(\kappa^{-3}).
\]

Substitution into the exact outer formula yields

\[
\boxed{
K_1\longrightarrow K_*:=\frac{4j_1}{j_1+j_2}
=1.213806833974\ldots
}
\]

The latitude rate is only `O(kappa^2)`, while

\[
1-\cos(\pi/N)=\frac{\pi^2}{2N^2}+O(N^{-4}).
\]

Hence the two azimuthal rates dominate and

\[
\boxed{
R_1=\frac{8}{\pi^2j_1(j_1+j_2)}N^2\kappa^2+O(N^2).
}
\]

Equivalently,

\[
\boxed{
\frac{R_1}{N^4}\longrightarrow
C_R:=\frac{8}{\pi^2j_1(j_1+j_2)}
=0.0425316930562\ldots
}
\]

This `N^4` polar stiffness is the principal new Gate 3 finding. It is caused by
combining:

- polar radius squared `rho_1^2=Theta(N^-2)`;
- azimuthal spacing factor `1-cos(pi/N)=Theta(N^-2)`;
- a nonzero limiting correction `K_*`.

The same endpoint expansion gives the outer defect

\[
\boxed{
\varepsilon_1=
\frac{(j_2-j_1)^3}{(j_1+j_2)\kappa^2}+O(\kappa^{-4}).
}
\]

Thus the outer defect is `Theta(N^-2)` even though its row rate is
`Theta(N^4)`.

The algebraic reduction is Lean-verified. The endpoint asymptotic step uses
standard Bessel expansions for fixed extreme Gauss–Legendre nodes and is a
conventional analytic proof, not yet formalized in Lean.

## 6. Deterministic verification

Two independent tests accompany the proof work.

### 6.1 Exact symbolic `N=2` case

`gate3/glc_exact_n2.py` uses SymPy exact arithmetic and proves without floating
point tolerances that

\[
a_{\mathrm{lat}}=1,
\quad K=\frac43,
\quad q=1,
\quad \varepsilon=\frac43,
\quad R=3,
\quad R\varepsilon=4.
\]

### 6.2 Family audit through `N=512`

`gate3/glc_deterministic_audit.py` independently reconstructs the Radiant
formulas using SciPy Gauss–Legendre nodes. It checks orders

`2,3,4,5,6,8,10,12,16,20,24,32,48,64,96,128,192,256,384,512`.

For every tested order:

- every interior `beta` is positive;
- every `K_n` is positive;
- all three coordinate residuals are at roundoff;
- the geometric `K_n` identity is at roundoff;
- the defect decomposition is at roundoff;
- `R_n epsilon_n >= 4` at every row.

The tail fits are

\[
\max_n\varepsilon_n\approx C N^{-1.99464},
\]

\[
R_1\approx C N^{3.98846}.
\]

At `N=512`,

\[
N^2\max_n\varepsilon_n=9.859898295,
\]

which is approaching `pi^2=9.869604401...`, while

\[
R_1/N^4=0.042615954,
\]

which is approaching the Bessel constant above.

### 6.3 Direct Radiant comparison

`gate3/radiant_glc_direct_audit.jl` calls Radiant's public GLC matrix
constructor with identity moment transforms, removes the documented diagonal
stabilization, and compares the result entry-by-entry with an independent
implementation of the published formulas.

## 7. What is not yet proved

The deterministic evidence strongly supports

\[
\max_n\varepsilon_n\sim\frac{\pi^2}{N^2}.
\]

This is **not yet a completed theorem**. A global upper bound uniform over all
latitude indices appears to require uniform relations among Gauss–Legendre
nodes, weights, and partial first moments. Recent work identifies several of
those relations as conjectural despite strong Bessel and numerical evidence.

Therefore Gate 3 does not claim:

- a complete all-node proof that `K_n>0` derived independently of the original
  Morel monotonicity result;
- a rigorous global `max epsilon_n ~ pi^2/N^2` theorem;
- a uniform condition-number estimate for the full transport solve.

## 8. Next proof targets

1. Prove a uniform lower bound `K_n >= k_0>0` directly from Gauss–Legendre
   partial-moment inequalities, or identify the minimal existing theorem that
   implies it.
2. Prove central-ring defect asymptotics using compact-interior expansions.
3. Combine endpoint and interior estimates with an intermediate-index argument
   to establish a uniform `O(N^-2)` defect bound.
4. Determine whether the sharp maximum is attained at the central ring and
   whether the constant is exactly `pi^2`.
5. Compare an LP defect-minimizing stencil with the explicit Morel stencil while
   constraining maximum row rate, since defect-only optimization may worsen the
   newly identified polar stiffness.

## 9. Sources

- C. Bienvenue, A. Naceur, J.-F. Carrier, and A. Hébert, “A Flexible,
  Moment-Preserving, and Monotone Discretization of the Multidimensional
  Angular Fokker–Planck Operator,” *Nuclear Science and Engineering* (2025),
  DOI: https://doi.org/10.1080/00295639.2025.2462891
- J. E. Morel et al., “A Discretization Scheme for the Three-Dimensional
  Angular Fokker–Planck Operator,” *Nuclear Science and Engineering* 156
  (2007), DOI: https://doi.org/10.13182/NSE07-A2693
- Ó. López Pouso and J. Segura, “Uniform relations between the Gauss–Legendre
  nodes and weights,” *Journal of Inequalities and Applications* 2025:40,
  DOI: https://doi.org/10.1186/s13660-025-03283-w
- N. Hale and A. Townsend, “Fast and Accurate Computation of Gauss–Legendre and
  Gauss–Jacobi Quadrature Nodes and Weights,” *SIAM Journal on Scientific
  Computing* 35 (2013), DOI: https://doi.org/10.1137/120889873
- Radiant implementation:
  https://github.com/CBienvenue/Radiant.jl/tree/205e07faa105854b0f27e95a02f01ebed08f84c1

# Odd-order central-ring asymptotics for the GLC AFP stencil

## Statement

Let `N=2m+1` be odd and let

\[
-1<\mu_{1,N}<\cdots<\mu_{N,N}<1
\]

be the sorted roots of the Legendre polynomial `P_N`, with Gauss–Legendre
weights `w_{k,N}`. Set

\[
\kappa_N=N+\frac12.
\]

The central node is exactly

\[
\mu_{m+1,N}=0.
\]

Let

\[
a_N:=\mu_{m+2,N}>0,
\qquad
w_{0,N}:=w_{m+1,N},
\qquad
r_N:=\sqrt{1-a_N^2},
\qquad
d_N:=1-r_N.
\]

Let `B_N` be the Morel interface moment immediately to either side of the
central ring. By symmetry and the recurrence,

\[
B_N=2\sum_{k=m+2}^{N}w_{k,N}\mu_{k,N}
=\sum_{k=1}^{N}w_{k,N}|\mu_{k,N}|.
\]

Define the common latitude rate

\[
A_N:=\frac{B_N}{w_{0,N}a_N},
\]

the azimuthal spacing deficit

\[
D_N:=1-\cos\frac{\pi}{N},
\]

and the central correction

\[
K_N:=2-2A_Nd_N.
\]

The exact central peak defect and outgoing rate are

\[
\varepsilon_N^{\mathrm{eq}}
=2A_Nd_N^2+K_ND_N,
\]

\[
R_N^{\mathrm{eq}}
=2A_N+\frac{K_N}{D_N}.
\]

Then

\[
\boxed{
N^2\varepsilon_N^{\mathrm{eq}}\longrightarrow\pi^2
}
\]

and

\[
\boxed{
\frac{R_N^{\mathrm{eq}}}{N^2}\longrightarrow\frac{4}{\pi^2}.
}
\]

Consequently,

\[
\boxed{
R_N^{\mathrm{eq}}\varepsilon_N^{\mathrm{eq}}\longrightarrow4.
}
\]

Thus the sharp finite jump-generator inequality becomes asymptotically an
equality at the equatorial ring.

## Proof

### 1. The Morel interface moment converges to one

The identity

\[
B_N=\sum_{k=1}^{N}w_{k,N}|\mu_{k,N}|
\]

is exact. Gauss–Legendre quadrature converges for every continuous function on
`[-1,1]`. Applying this to `|x|` gives

\[
B_N\longrightarrow\int_{-1}^{1}|x|\,dx=1.
\]

No differentiability of `|x|` is needed for this limit.

### 2. Central node and weight asymptotics

The standard compact-interior Gauss–Legendre expansions give

\[
a_N\kappa_N\longrightarrow\pi,
\]

and

\[
\frac{w_{0,N}\kappa_N}{\pi}\longrightarrow1.
\]

Therefore

\[
\frac{A_N}{N^2}
=\frac{B_N}{w_{0,N}a_NN^2}
\longrightarrow\frac{1}{\pi^2}.
\]

### 3. Latitude chord deficit

Since

\[
d_N=1-\sqrt{1-a_N^2}
=\frac{a_N^2}{1+\sqrt{1-a_N^2}},
\]

we have

\[
N^2d_N\longrightarrow\frac{\pi^2}{2}.
\]

It follows that

\[
A_Nd_N\longrightarrow\frac12,
\]

and hence

\[
K_N=2-2A_Nd_N\longrightarrow1.
\]

### 4. Defect limit

For the latitude contribution,

\[
N^2(2A_Nd_N^2)
=2\left(\frac{A_N}{N^2}\right)(N^2d_N)^2
\longrightarrow
2\left(\frac{1}{\pi^2}\right)
\left(\frac{\pi^2}{2}\right)^2
=\frac{\pi^2}{2}.
\]

Also,

\[
N^2D_N
=N^2\left(1-\cos\frac{\pi}{N}\right)
\longrightarrow\frac{\pi^2}{2}.
\]

Since `K_N -> 1`,

\[
N^2K_ND_N\longrightarrow\frac{\pi^2}{2}.
\]

Adding the two contributions gives

\[
N^2\varepsilon_N^{\mathrm{eq}}\longrightarrow\pi^2.
\]

### 5. Rate limit

The latitude part satisfies

\[
\frac{2A_N}{N^2}\longrightarrow\frac{2}{\pi^2}.
\]

For the azimuthal part,

\[
\frac{K_N}{N^2D_N}
\longrightarrow\frac{2}{\pi^2}.
\]

Therefore

\[
\frac{R_N^{\mathrm{eq}}}{N^2}
\longrightarrow\frac{4}{\pi^2}.
\]

Multiplying the two limits yields

\[
R_N^{\mathrm{eq}}\varepsilon_N^{\mathrm{eq}}
\longrightarrow4.
\]

## What this proves about the global defect

Because the central ring is one of the rows of every odd-order GLC stencil,

\[
\liminf_{\substack{N\to\infty\\N\;\mathrm{odd}}}
N^2\max_n\varepsilon_{n,N}
\ge\pi^2.
\]

The deterministic family audit indicates the stronger statement

\[
N^2\max_n\varepsilon_{n,N}\longrightarrow\pi^2
\]

for all orders and suggests that the maximum is attained at, or immediately
adjacent to, the equatorial ring. The matching global upper bound remains to be
proved because it requires uniform control across endpoint, intermediate, and
central Gauss–Legendre index regimes.

## Formal and computational status

The exact finite formulas for `K_N`, `epsilon_N`, and `R_N` are kernel-checked
in `AFPBarrier/GLCCentral.lean`. The asymptotic input concerning the central
Gauss–Legendre root and weight is standard analytic literature and is not yet
formalized in Lean.

`glc_central_audit.py` deterministically checks the exact formulas and all nine
limits through order `N=511`.

# Finite Kepler outer-parallel theorem by torus completion

Source provenance:

```text
FusionSandwich/Math
branch: agent/erdos-1084-target-a-publication-20260819
source head: 21c25ce3a6f13f46ab5af4289043ed6edb2215aa
```

## Theorem

For every finite unit-ball packing with centers `C={c_1,...,c_n}` in `R^3` and every `r>=2`,

\[
n\operatorname{vol}(B^3)
\le
\frac\pi{\sqrt{18}}
\operatorname{vol}\left(\bigcup_i(c_i+rB^3)\right).
\]

Equivalently, the radius-`r` union has volume at least `4sqrt(2)n`.

## Proof certificate

1. Use the FCC lattice
   \[
   \Lambda=\sqrt2D_3,
   \qquad
   D_3=\{z\in\mathbb Z^3:z_1+z_2+z_3\text{ even}\}.
   \]
   Its shortest vector has length two and its determinant is `4sqrt(2)`.

2. If `D=max_{i,j}|c_i-c_j|`, choose an integer `N` with
   \[
   2N>D+2r.
   \]
   In the torus `T=R^3/NLambda`, the quotient map is injective on the complete radius-`r` union: any nonzero period has length at least `2N`, while any difference of two points of the union has length at most `D+2r`.

3. The quotient `Lambda/NLambda` has `N^3` FCC centers. Uniformly translate this finite orbit on `T`. Translation invariance gives expected filler count outside the embedded radius-`r` union
   \[
   N^3\left(1-\frac{\operatorname{vol}(U_r)}{V}\right).
   \]

4. Choose a translate with at least this average. Every retained filler center has torus distance strictly greater than `r>=2` from each original center. The original cluster plus retained filler is therefore a torus unit-ball packing.

5. Lift periodically to `R^3` and apply the Kepler theorem:
   \[
   (n+m)\operatorname{vol}(B^3)\le\frac\pi{\sqrt{18}}V.
   \]
   The filler averaging lower bound is
   \[
   m\operatorname{vol}(B^3)
   \ge
   \frac\pi{\sqrt{18}}(V-\operatorname{vol}(U_r)).
   \]
   Subtraction gives the theorem.

No Bezdek--Lángi equation (1.2), limsup product, or asymptotic passage in `n` is used.

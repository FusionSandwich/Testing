# P1A: sampling quotient and the exact two-defect decomposition

## 1. Hypotheses and conventions

Let `I` be a nonempty finite set, let `d >= 2`, and let

\[
 w_i>0,\qquad \sum_iw_i=1,\qquad \Omega_i\in S^{d-1}.
\]

A *positive reversible jump generator with shared conductances* means that
there are numbers

\[
 \gamma_{ij}=\gamma_{ji}\geq0,\qquad \gamma_{ii}=0,
 \qquad a_{ij}=\frac{\gamma_{ij}}{w_i},
\]

and

\[
 (Lf)_i=\sum_{j\ne i}a_{ij}(f_j-f_i).                 \tag{1.1}
\]

Thus `positive` refers to the off-diagonal rates.  With this sign convention
`L` is negative semidefinite.  The sample inner product and the coefficient
inner product are

\[
 \langle f,g\rangle_w=\sum_iw_if_ig_i,
 \qquad \langle A,H\rangle_F=\operatorname{tr}(AH)
 \quad(A,H\in V:=\operatorname{Sym}_0(d)).             \tag{1.2}
\]

Detailed balance gives the exact Green identity

\[
 \langle Lf,g\rangle_w
 =-\frac12\sum_{i,j}\gamma_{ij}(f_j-f_i)(g_j-g_i)
 =\langle f,Lg\rangle_w.                              \tag{1.3}
\]

Assume coordinatewise

\[
 L\Omega=-(d-1)\Omega.                                \tag{1.4}
\]

Put

\[
 \Delta_{ij}=\Omega_j-\Omega_i,\quad
 \ell_{ij}=1-\Omega_i\mathbin\cdot\Omega_j,\quad
 r_i=\sum_{j\ne i}a_{ij},                              \tag{1.5}
\]

and define `S_2`, `R_2`, `C_i`, `M_i`, `Z_i`, `epsilon_i`, and `B_i` as in
the prompt.  Here

\[
 P_0(H)=H-\frac{\operatorname{tr}H}{d}I_d.             \tag{1.6}
\]

The restriction `d >= 2` is literal: both `d/(d-1)` and the loss mean below
are undefined at `d=1`.  It is also the intended spherical regime.  No
injectivity of `S_2`, distinctness of the sampled nodes, graph transitivity,
or connectedness is assumed.

## 2. The local identities

### 2.1 First loss moment and positivity of the row rate

Taking the scalar product of (1.4) at `i` with `Omega_i` gives

\[
 \boxed{\sum_{j\ne i}a_{ij}\ell_{ij}=d-1.}             \tag{2.1}
\]

Every `ell_ij` lies in `[0,2]` and every rate is nonnegative.  Since the
right side of (2.1) is positive, every `r_i` is positive.  Consequently all
divisions by `r_i` below are justified by the stated hypotheses.

### 2.2 Covariance and residual

For `A in V`, expansion of one jump gives

\[
 \Omega_j^TA\Omega_j-\Omega_i^TA\Omega_i
 =2\Omega_i^TA\Delta_{ij}+\Delta_{ij}^TA\Delta_{ij}.
\]

After summing and using (1.4),

\[
 L(S_2A)_i=-2(d-1)(S_2A)_i+\langle A,C_i\rangle_F.
\]

Hence

\[
 \begin{aligned}
 (R_2A)_i
 &=\langle A,C_i+2\Omega_i\Omega_i^T\rangle_F\\
 &=\boxed{\langle A,M_i\rangle_F},                    \tag{2.2}
 \end{aligned}
\]

because trace-free `A` is orthogonal to the scalar matrices and `P_0` is the
orthogonal projection onto `V`.

Independently of (2.2), `R_2=(L+2dI)S_2` immediately implies

\[
 \boxed{K_X:=\ker S_2\subseteq\ker R_2}.               \tag{2.3}
\]

Thus there is a unique induced map

\[
 \bar R_2:V/K_X\longrightarrow\mathbb R^I,
 \qquad \bar R_2[A]=R_2A.                              \tag{2.4}
\]

Combining (2.2) and (2.3) also proves the useful row statement
`M_i in K_X^perp` for every `i`.

### 2.3 Trace, radial contraction, and the distinguished tensor

Since `||Delta_ij||^2=2 ell_ij`, (2.1) yields

\[
 \boxed{\operatorname{tr}C_i=2(d-1).}                  \tag{2.5}
\]

Moreover `Omega_i dot Delta_ij=-ell_ij`, so

\[
 \boxed{\Omega_i^TC_i\Omega_i
 =\sum_{j\ne i}a_{ij}\ell_{ij}^2=\epsilon_i.}         \tag{2.6}
\]

The matrix inside `P_0` has trace `2d`; therefore

\[
 M_i=C_i+2\Omega_i\Omega_i^T-2I_d.                    \tag{2.7}
\]

It follows from (2.6) that

\[
 \boxed{\langle M_i,Z_i\rangle_F
 =\Omega_i^TM_i\Omega_i=\epsilon_i.}                  \tag{2.8}
\]

Finally, using `(Omega Omega^T)^2=Omega Omega^T`,

\[
 \boxed{\|Z_i\|_F^2
 =\operatorname{tr}\!\left(\Omega_i\Omega_i^T-I/d\right)^2
 =1-\frac1d=\frac{d-1}{d}.}                           \tag{2.9}
\]

### 2.4 The tensor defect and the scalar loss defect

Equations (2.8)--(2.9) show that the Frobenius projection of `M_i` onto
`R Z_i` is exactly

\[
 \frac{\langle M_i,Z_i\rangle_F}{\|Z_i\|_F^2}Z_i
 =\frac d{d-1}\epsilon_iZ_i.
\]

Thus the definition of `B_i` is the orthogonal remainder, and

\[
 \boxed{\langle B_i,Z_i\rangle_F=0},                  \tag{2.10}
\]

\[
 \boxed{\|M_i\|_F^2
 =\frac d{d-1}\epsilon_i^2+\|B_i\|_F^2.}              \tag{2.11}
\]

The other defect is the variance of the chord losses.  Put
`m_i=(d-1)/r_i`.  Expanding a square and using (2.1) gives

\[
 \begin{aligned}
 \sum_{j\ne i}a_{ij}(\ell_{ij}-m_i)^2
 &=\epsilon_i-2m_i(d-1)+m_i^2r_i\\
 &=\epsilon_i-\frac{(d-1)^2}{r_i}.
 \end{aligned}
\]

Therefore

\[
 \boxed{\epsilon_i=\frac{(d-1)^2}{r_i}
 +\sum_{j\ne i}a_{ij}
   \left(\ell_{ij}-\frac{d-1}{r_i}\right)^2.}         \tag{2.12}
\]

Equations (2.11) and (2.12) are the exact two-defect decomposition: the
radial coefficient contains an unavoidable Cauchy--Schwarz term and a scalar
loss-variance defect, while `B_i` is the independent tensor-anisotropy
defect.  Summing (2.11) with the vertex weights gives, without any symmetry
or constant-rate assumption,

\[
 \sum_iw_i\|M_i\|_F^2
 =\frac d{d-1}\sum_iw_i\epsilon_i^2
  +\sum_iw_i\|B_i\|_F^2.                               \tag{2.13}
\]

## 3. A second proof through the sampled operator and Gram rows

This route does not contract `C_i` radially.  Fix `i` and use `Z_i` as the
coefficient form.  At a sample `k`,

\[
 (S_2Z_i)_k=(\Omega_i\mathbin\cdot\Omega_k)^2-1/d.
\]

At the `i`th row,

\[
 \begin{aligned}
 L(S_2Z_i)_i
 &=\sum_{j\ne i}a_{ij}
   \big((1-\ell_{ij})^2-1\big)\\
 &=-2(d-1)+\epsilon_i,
 \end{aligned}
\]

where only the first moment (2.1) was used.  Since
`(S_2Z_i)_i=(d-1)/d`, the `2dI` term cancels `-2(d-1)` and gives

\[
 (R_2Z_i)_i=\epsilon_i.                                \tag{3.1}
\]

The row-representer identity (2.2) turns (3.1) into
`<M_i,Z_i>_F=epsilon_i`.  In the Hilbert space `V`, orthogonally project the
residual row representer `M_i` onto the sampling row representer `Z_i`.
Equation (2.9) gives the coefficient `d epsilon_i/(d-1)`, and the Hilbert
space projection theorem gives (2.10)--(2.11).  This is the operator/Gram
proof of the central split; it uses the action of `R_2` on a sampled
quadratic rather than the direct tensor contraction (2.6)--(2.8).

## 4. Weighted adjoints and exact Gram operators

For every `A in V`, trace-freeness gives

\[
 (S_2A)_i=\langle A,Z_i\rangle_F,
 \qquad (R_2A)_i=\langle A,M_i\rangle_F.                \tag{4.1}
\]

Consequently the adjoints relative to (1.2), not the unweighted transpose,
are

\[
 \boxed{S_2^*f=\sum_iw_if_iZ_i,\qquad
 R_2^*f=\sum_iw_if_iM_i.}                              \tag{4.2}
\]

The exact bilinear and operator Gram formulas are

\[
 \boxed{\langle A,S_2^*S_2H\rangle_F
 =\sum_iw_i\langle A,Z_i\rangle_F\langle H,Z_i\rangle_F,}
                                                                    \tag{4.3}
\]

\[
 \boxed{S_2^*S_2H=\sum_iw_i\langle H,Z_i\rangle_FZ_i,}             \tag{4.4}
\]

\[
 \boxed{\langle A,R_2^*R_2H\rangle_F
 =\sum_iw_i\langle A,M_i\rangle_F\langle H,M_i\rangle_F,}         \tag{4.5}
\]

\[
 \boxed{R_2^*R_2H=\sum_iw_i\langle H,M_i\rangle_FM_i.}             \tag{4.6}
\]

Comparing the `i`th row of `R_2=(L+2dI)S_2` with the two row
representers in (4.1) also gives the exact tensor identity

\[
 \boxed{M_i=(2d-r_i)Z_i+\sum_{j\ne i}a_{ij}Z_j.}       \tag{4.7}
\]

In particular `span{M_i} subset span{Z_i}`, another direct proof of
`rank R_2 <= rank S_2`.

Writing `T=L+2dI`, (1.3) says `T^*=T`, so a third equivalent formula is

\[
 \boxed{R_2^*R_2=S_2^*T^2S_2.}                       \tag{4.8}
\]

In coordinates, if columns are expressed in a Frobenius-orthonormal basis
of `V` and `W=diag(w_i)`, (4.4)--(4.6) read

\[
 G_S=S^TWS,\qquad G_R=R^TWR.                           \tag{4.9}
\]

Using `S^TS` would be wrong unless all weights happen to be equal up to a
common scalar.

Taking Hilbert--Schmidt traces and using `sum_i w_i=1` yields

\[
 \boxed{\operatorname{tr}G_S=\frac{d-1}{d}},           \tag{4.10}
\]

\[
 \boxed{\operatorname{tr}G_R
 =\frac d{d-1}\sum_iw_i\epsilon_i^2
  +\sum_iw_i\|B_i\|_F^2.}                             \tag{4.11}
\]

Pointwise `B_i perpendicular Z_i` is enough for (4.11), but it does **not**
annihilate the mixed rank-one operators
`Z_i tensor B_i+B_i tensor Z_i` in `G_R`.

## 5. The sampling quotient and the generalized eigenvalue

The quotient required by the fidelity problem is not equipped with the
Frobenius quotient norm.  Give `Q_X=V/K_X` the pulled-back sampling product

\[
 \langle[A],[H]\rangle_S
 :=\langle S_2A,S_2H\rangle_w.                         \tag{5.1}
\]

It is well defined and positive definite precisely because the nullspace of
the right side is `K_X`.  The induced map

\[
 \bar S_2:Q_X\longrightarrow\operatorname{im}S_2
\]

is an isometric isomorphism, while `bar R_2=T bar S_2` is a map from `Q_X`
to the whole weighted sample space (the image of `S_2` need not be
`T`-invariant).

The sample map is automatically nonzero: for every `i`,
`(S_2Z_i)_i=||Z_i||_F^2=(d-1)/d>0`.  Define the genuinely sampled
quadratic defect by

\[
 \mathfrak D_2
 :=\|\bar R_2\|_{Q_X\to\ell^2(w)}
 =\sup_{A\notin K_X}\frac{\|R_2A\|_w}{\|S_2A\|_w}.     \tag{5.2}
\]

Set

\[
 G_S=S_2^*S_2,\qquad G_R=R_2^*R_2,
 \qquad W_X=K_X^{\perp_F}.                             \tag{5.3}
\]

On `W_X`, `G_S` is positive definite.  Because `K_X subset ker R_2`, both
operators preserve `W_X`.  The finite-dimensional spectral theorem gives
the basis-independent formulas

\[
 \boxed{\mathfrak D_2^2
 =\max_{0\ne A\in W_X}
   \frac{\langle A,G_RA\rangle_F}{\langle A,G_SA\rangle_F}}
                                                                    \tag{5.4}
\]

and

\[
 \boxed{\mathfrak D_2^2
 =\lambda_{\max}\!\left(
 G_S^{-1/2}G_RG_S^{-1/2}\big|_{W_X}\right).}           \tag{5.5}
\]

Equivalently, it is the largest generalized eigenvalue `lambda` in the
**deflated** pencil

\[
 G_RA=\lambda G_SA,\qquad 0\ne A\in W_X,              \tag{5.6}
\]

followed by a square root.  These statements are invariant under every
change of basis in `V`.  The raw singular pencil on all of `V` is invalid
when `K_X` is nonzero: every kernel vector satisfies `0=lambda 0` for every
`lambda`, and its determinant is identically zero.  In an abstract problem
where `S_2=0`, the Rayleigh set would be empty and would require an explicit
convention; valid unit-sphere data with `d>=2` never enter that case.

## 6. Three exact spaces and all rank formulas

The coefficient-space identities are

\[
 \boxed{E_{\rm form}:=\ker R_2
 =\operatorname{span}\{M_i:i\in I\}^{\perp_F},}        \tag{6.1}
\]

\[
 \boxed{K_X:=\ker S_2
 =\operatorname{span}\{Z_i:i\in I\}^{\perp_F}.}        \tag{6.2}
\]

The genuinely sampled exact space is instead

\[
 \begin{aligned}
 E_{\rm sample}
 &:=S_2(E_{\rm form})\\
 &=\boxed{\operatorname{im}S_2\cap\ker(L+2dI)}.        \tag{6.3}
 \end{aligned}
\]

Indeed, one inclusion follows from the definition of `R_2`; for the reverse
inclusion choose any preimage under `S_2`.  The kernel of
`S_2|E_form` is exactly `K_X`, by (2.3).  If

\[
 m=\dim V=\frac{d(d+1)}2-1,
\]

rank-nullity therefore gives, with no injectivity assumption,

\[
 \boxed{\dim K_X=m-\operatorname{rank}S_2,}            \tag{6.4}
\]

\[
 \boxed{\dim E_{\rm form}=m-\operatorname{rank}R_2,}  \tag{6.5}
\]

\[
 \boxed{\dim E_{\rm sample}
 =\dim E_{\rm form}-\dim K_X
 =\operatorname{rank}S_2-\operatorname{rank}R_2.}     \tag{6.6}
\]

In particular `rank R_2 <= rank S_2`.  A nonzero member of `K_X` is an
algebraically nonzero quadratic form but the zero sampled function.  It is
form-exact only vacuously and contributes nothing to `E_sample`.

## 7. Exact family checks and deliberate aliases

The accompanying deterministic audit constructs the coordinates and the
shared conductances in exact SymPy algebra.  In all three regular families
below, the one-shell tangent frame is isotropic, so `B_i=0` and
`M_i=cZ_i`:

| family in `S^(d-1)` | nodes | active rate | loss | `M_i` | `rank S_2` | `dim K_X` | `mathfrak D_2` |
|---|---:|---:|---:|---:|---:|---:|---:|
| regular simplex | `d+1` | `(d-1)/(d+1)` | `(d+1)/d` | `(d+1)Z_i` | `d` | `m-d` | `d+1` |
| cross-polytope | `2d` | `1/2` | `1` | `d Z_i` | `d-1` | `d(d-1)/2` | `d` |
| hypercube | `2^d` | `(d-1)/2` | `2/d` | `2Z_i` | `d(d-1)/2` | `d-1` | `2` |

For each row in these families, `rank R_2=rank S_2`, hence
`E_sample={0}` even though `K_X` can be large.

These are all-dimensional algebraic formulas, not extrapolations from the
finite regression dimensions.  For the simplex,
`<Z_i,Z_i>=(d-1)/d` and `<Z_i,Z_j>=-(d-1)/d^2` for `i!=j`; its row Gram has
rank `d`.  Cross-polytope samples see exactly the trace-free diagonal part,
of dimension `d-1`.  Hypercube samples are the independent degree-two Walsh
characters `s_p s_q`, `p<q`, so their dimension is `d(d-1)/2`.  The common
loss shell and its regular tangent frame give the displayed scalar `M_i` in
each case.  The audit instantiates these proofs at `d=2,3,4` as regression
checks.

The five three-dimensional Platonic shortest-edge generators give:

| graph | `N` | `r_i` | `epsilon_i` | `M_i/Z_i` | `rank S_2=rank R_2` | `dim E_form=dim K_X` | `mathfrak D_2` |
|---|---:|---:|---:|---:|---:|---:|---:|
| tetrahedron | 4 | `3/2` | `8/3` | `4` | 3 | 2 | `4` |
| octahedron | 6 | `2` | `2` | `3` | 2 | 3 | `3` |
| cube | 8 | `3` | `4/3` | `2` | 3 | 2 | `2` |
| icosahedron | 12 | `(5+sqrt(5))/2` | `2-2sqrt(5)/5` | `3-3sqrt(5)/5` | 5 | 0 | `3-3sqrt(5)/5` |
| dodecahedron | 20 | `(9+3sqrt(5))/2` | `2-2sqrt(5)/3` | `3-sqrt(5)` | 5 | 0 | `3-sqrt(5)` |

The audit also includes two configurations designed to defeat hidden
injectivity and weighting assumptions.

1. On `S^1`, the antipodal pair `(+e_1,-e_1)` with edge rate `1/2`
   satisfies `L Omega=-Omega`.  Its off-diagonal trace-free form lies in
   `K_X`, so `rank S_2=1<dim Sym_0(2)=2`; nevertheless all quotient and rank
   identities above remain exact.
2. A five-index multiset `(+e_1,+e_1,-e_1,+e_2,-e_2)` with unequal positive
   weights (the repeated `+e_1` mass is split) is centered.  The complete
   conductances `gamma_ij=w_iw_j` give `L Omega=-Omega`.  It simultaneously
   tests coincident nodes, repeated sampling rows, a nontrivial kernel, and
   the fact that the adjoint is `S^T W`, not `S^T`.
3. The exact spherical hexagonal prism has `rank S_2=5`, `rank R_2=3`,
   `dim K_X=0`, `dim E_form=2`, and `dim E_sample=2`.  Its deflated squared
   spectrum is `{0,0,4,4,36}`.  It forces all three spaces in Section 6 to
   be distinguished even when sampling is injective.
4. The degenerate equatorial hexagon in `R^3` has
   `(rank S_2,rank R_2)=(3,1)` and
   `(dim K_X,dim E_form,dim E_sample)=(2,4,2)`, testing the rank identity
   with a nonzero alias space and nonzero genuinely sampled exact space at
   the same time.
5. A positive full cube with seven distinct flip rates has scalar loss
   variance `1/6` and `||B_i||_F^2=1/81`, proving that both defects can be
   simultaneously nonzero.  Its quotient squared spectrum is
   `{64/9,25/4,49/9}`.

The sign mutation `R_2=(L-2dI)S_2`, the unweighted-adjoint mutation, and the
false dimension mutation `dim E_sample=dim E_form` are each required to fail
on explicit fixtures.

## 8. Prior-art boundary

Steinerberger's spectral quadrature bounds concern exact integration of an
initial Laplace spectrum with nonnegative quadrature weights; they do not
identify an algebraic quadratic form with its finite sample.  Izmestiev and
Lam use the same negative-semidefinite generator sign and weighted Green
identity for their geometry-specific spherical and hyperbolic Laplacians,
but their cotangent/Delaunay conductances are not assumed here.  The
Martin--Tanaka association-scheme framework and the Bannai--Bannai spherical
design survey explain harmonic characteristic matrices and symmetry-driven
orthogonality in regular examples.  No association scheme or design
hypothesis is used in Sections 1--6.  The quotient, row tensors, two-defect
split, and weighted generalized pencil above are the finite algebraic
specialization proved here.

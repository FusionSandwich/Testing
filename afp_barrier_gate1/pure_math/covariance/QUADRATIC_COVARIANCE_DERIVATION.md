# Quadratic covariance derivation — Prompt 2 closeout summary

The authoritative proof is
`SAMPLED_QUADRATIC_EXACTNESS_THEOREM.md`. This file records the algebraic spine
and the corrected claim boundaries required by Prompt 3.

## 1. Quadratic covariance

For

```text
(Lf)(i) = sum_{j != i} a_ij (f(j)-f(i)),
L Phi = -lambda Phi,
Delta_ij = Phi_j-Phi_i,
C_i = sum_j a_ij Delta_ij Delta_ij^T,
Q_A(i) = Phi_i^T A Phi_i,
```

coordinate expansion gives

```text
L Q_A(i)
  = -2 lambda Q_A(i) + tr(A^T C_i).
```

For `q_{A,c}=Q_A-c` and target `-mu`, exactness is equivalent to

```text
tr(A^T C_i)
  + (mu-2 lambda) Q_A(i)
  - mu c = 0
```

at every state.

## 2. Spherical sampling factorization

For

```text
lambda=d-1,
mu=2d,
A in Sym_0(d),
M_i=P_0(C_i+2 Phi_i Phi_i^T),
S_X(A)_i=Phi_i^T A Phi_i,
R_X(A)_i=<A,M_i>_F,
```

one has

```text
E_form=ker R_X=span{M_i}^perp,
R_X=(L+2d I)S_X,
K_X=ker S_X subset E_form,
E_sample=im(S_X) intersect ker(L+2d I),
dim E_sample=rank(S_X)-rank(R_X).
```

A form-space dimension is never a sampled-mode count unless the sampling
kernel has been removed.

## 3. Positive rigidity

If

```text
C_i=tau_i(I-Phi_i Phi_i^T)+beta_i Phi_i Phi_i^T,
beta_i>0,
```

then

```text
M_i=d beta_i/(d-1)(Phi_i Phi_i^T-I/d).
```

Axial covariance at every state gives

```text
E_form=K_X,
E_sample={0}.
```

Regular simplices attain this theorem in every dimension.

The independent equivariant theorem is valid only with the complete positive
generator hypothesis:

```text
a_ij >= 0 for every i != j.
```

Together with a transitive equivariant unit-sphere eigenmap, irreducibility of
the real conjugation action on `Sym_0(d)`, and one positive jump between
distinct embedded points, this gives `E_form={0}`. Reversibility is not used.

The signed regular pentagon with

```text
u=(5+3 sqrt(5))/10,
v=(5-3 sqrt(5))/10
```

is the permanent counterexample when global nonnegativity is omitted:
coordinate eigenvalue `-1`, both trace-free quadratic samples at `-4`,
`E_form=Sym_0(2)`, and `dim E_sample=2`, despite irreducible `C_5` conjugation.

## 4. Centered product resonance

Define

```text
Gamma(f,g)(i)
  = 1/2 sum_j a_ij(f(j)-f(i))(g(j)-g(i)).
```

Then

```text
L(fg)-f Lg-g Lf=2 Gamma(f,g).
```

If `Lf=-lambda f` and `Lg=-nu g`, then

```text
L(fg-c)+mu(fg-c)
  =2 Gamma(f,g)+(mu-lambda-nu)fg-mu c.
```

At additive resonance:

```text
L(fg-c)=-(lambda+nu)(fg-c)
iff
2 Gamma(f,g)=(lambda+nu)c.
```

For a square:

```text
L(f^2-c)=-2lambda(f^2-c)
iff
Gamma(f,f)=lambda c.
```

Thus `c=0` forces zero carré du champ, while a centered square may be nonzero.
The four-state Boolean example has

```text
Lf=-2f,
f^2-2=2x_1x_2 != 0,
L(f^2-2)=-4(f^2-2),
Gamma(f,f)=4.
```

Its semigroup variance is `2(1-exp(-4t))`, so centered resonance is not Jensen
equality.

## 5. Spherical shift and hierarchy boundary

On `S^(d-1)`:

```text
coordinate eigenvalue:          d-1,
doubled coordinate eigenvalue:  2(d-1),
degree-two eigenvalue:           2d.
```

The covariance theorem therefore has shift `2`, and it is not the additive
square problem.

The exact `S^2` table for `ell=1,...,6` has pointwise component degrees
`0,2,...,2ell` and no additive resonance. The generalized resonance equation
is Pell-type and has sparse higher-dimensional solutions, but no sampled
dimension tradeoff, multiplicity obstruction, or new global consequence
survives the kernel and alias audits. The general hierarchy remains
`REJECTED FOR PROMPT 2` for that reason only.

## 6. Status

- covariance identity and target residual: `PROVED / LEAN`;
- sampling factorization and genuine sampled-space formula: `PROVED / LEAN`;
- positive axial rigidity and regular-simplex equality family: `PROVED`;
- positive equivariant irreducibility rigidity: `PROVED WITH GLOBAL
  NONNEGATIVITY`;
- signed pentagon without positivity: `PROVED EXACT COUNTEREXAMPLE`;
- centered product and square resonance: `PROVED / LEAN`;
- Boolean centered square: `PROVED EXACT EXAMPLE`;
- uncentered positive-chain obstruction: `PROVED`;
- universal centered-square impossibility: `REJECTED`;
- general spectral-product hierarchy: `REJECTED FOR PROMPT 2`.

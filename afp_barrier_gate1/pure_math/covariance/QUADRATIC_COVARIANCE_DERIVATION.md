# Quadratic covariance derivation — corrected sampled-space summary

The complete Prompt 2 theorem is
`SAMPLED_QUADRATIC_EXACTNESS_THEOREM.md`. This file records the short derivation
and the claim-control distinctions that must not be lost in later work.

## 1. General identity

For

```text
(Lf)(i) = sum_j a_ij (f(j)-f(i)),
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

For symmetric `A`, the contraction is `tr(A C_i)`. For a shifted target
`q_{A,c}=Q_A-c` with eigenvalue `-mu`, exactness is equivalent to

```text
tr(A^T C_i)
  + (mu-2 lambda) Q_A(i)
  - mu c = 0
```

at every state. Trace-freeness does not by itself determine `c` on an
arbitrary finite sample.

## 2. Sphere specialization

For the coordinate eigenmap on `S^(d-1)`,

```text
lambda = d-1,
mu = 2d,
A in Sym_0(d),
M_i = P_0(C_i + 2 Phi_i Phi_i^T).
```

The zero-centered exact-form space is

```text
E_form
  = {A : <A,M_i>_F = 0 for every i}
  = span{M_i}^perp.
```

This is a matrix space, not yet a sampled function space.

## 3. Sampling factorization

Define

```text
S_X(A)_i = Phi_i^T A Phi_i,
K_X = ker S_X,
B = L + 2d I,
R_X(A)_i = <A,M_i>_F.
```

The covariance identity gives the exact factorization

```text
R_X = B S_X.
```

Therefore

```text
K_X subset E_form,
E_sample = S_X(E_form)
         = im(S_X) intersect ker(L+2d I).
```

Rank-nullity may first be written in the general restriction form

```text
dim E_sample
  = dim E_form - dim(E_form intersect K_X).
```

Here the intersection is exactly `K_X`, so the specialized formulas are

```text
dim E_sample
  = dim E_form - dim K_X
  = rank(S_X) - rank(R_X).
```

For basis matrices, if `S` is the sampling matrix and `R` the covariance
constraint matrix, then

```text
R = (G + 2d I) S,
rank([R;S]) = rank(S).
```

Any audit that treats `R` and `S` as unrelated matrices is not auditing this
quadratic covariance problem.

## 4. Sharp structural theorem

If every local covariance is axially isotropic,

```text
C_i = tau_i(I-Phi_i Phi_i^T)
      + beta_i Phi_i Phi_i^T,
beta_i > 0,
```

then

```text
M_i = d beta_i/(d-1)
      (Phi_i Phi_i^T-I/d).
```

Thus every constraint row is a positive scaling of the corresponding sampling
row. Consequently

```text
E_form = K_X,
E_sample = {0}.
```

This applies to regular simplices in every dimension and to all five Platonic
shortest-edge generators. Their exact form dimensions can be nonzero while
their sampled exact dimensions are zero.

## 5. Status

- covariance identity and target residual: `PROVED`;
- sampling factorization and exact sampled-space formula: `PROVED`;
- axial and equivariant rigidity: `PROVED`;
- Platonic rank table: exact proof plus exact symbolic regression;
- signed four-point restoration: `PROVED`;
- general spectral-product hierarchy: `REJECTED` for this stage under its kill
  criterion.

The exact symbolic audit remains `COMPUTATIONAL` infrastructure and is not the
proof of the general theorem.

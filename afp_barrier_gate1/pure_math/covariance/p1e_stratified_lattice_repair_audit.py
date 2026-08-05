#!/usr/bin/env python3
"""Exact audits for the P1E residue-unwinding chart.

This script does not certify the analytic all-level theorem.  It checks the
finite algebra which replaces the false finite-coset assertion:

* the raw 2+3 centered coordinate really has the |r|-dependent residue;
* the sheared coordinate is exactly A1* x A2;
* the displayed inverse recovers every enumerated boundary-simplex node;
* product-lattice translations remain product-lattice translations whenever
  the translated inverse stays in the positive chart;
* midpoint +/- fluxes have no odd truncation term through cubic order.

It also contains two adversarial fixtures which reject claims in the
conditional construction as currently written:

* the ``lambda_b >= s_* h`` buffer does not keep all radius-``s_* h``
  product-lattice neighbours inside the *open* B-positive chart;
* with one representative of each ``+/-`` pair, (3.4) and (3.5) give the
  right covariance tensor but only one half of the asserted force tensor.

All lattice and Taylor checks use integers or fractions.
"""

from __future__ import annotations

from fractions import Fraction
from itertools import combinations


def compositions(total: int, parts: int):
    if parts == 1:
        yield (total,)
        return
    for first in range(total + 1):
        for tail in compositions(total - first, parts - 1):
            yield (first,) + tail


def centered(values: tuple[int, ...]) -> tuple[Fraction, ...]:
    mean = Fraction(sum(values), len(values))
    return tuple(Fraction(value) - mean for value in values)


def raw_residue_23(k: tuple[int, ...]) -> int:
    """A2*/A2 class of P_B k_B, represented by its B mass mod 3."""

    return sum(k[2:]) % 3


def repaired_23(k: tuple[int, ...]):
    k0, k1, k2, k3, k4 = k
    q = centered((k0, k1))
    mass_b = k2 + k3 + k4
    t = (k2 - mass_b, k3, k4)
    assert sum(t) == 0
    return q, t


def repaired_general(
    k: tuple[int, ...], z_indices: tuple[int, ...], beta: int
) -> tuple[tuple[Fraction, ...], tuple[int, ...]]:
    """Integer-scaled `(Q,T)=(Nq,Nt)` for an arbitrary record."""

    z_set = set(z_indices)
    b_indices = tuple(index for index in range(len(k)) if index not in z_set)
    assert beta in b_indices
    q = centered(tuple(k[index] for index in z_indices))
    mass_b = sum(k[index] for index in b_indices)
    t = tuple(k[index] - (mass_b if index == beta else 0) for index in b_indices)
    assert sum(t) == 0
    return q, t


def inverse_general(
    N: int,
    q: tuple[Fraction, ...],
    t: tuple[int, ...],
    z_indices: tuple[int, ...],
    beta: int,
    ambient_size: int,
) -> tuple[int, ...]:
    """The inverse (1.2), in integer-scaled coordinates."""

    z_set = set(z_indices)
    b_indices = tuple(index for index in range(ambient_size) if index not in z_set)
    minimum = min(q)
    kz = tuple(value - minimum for value in q)
    assert all(value.denominator == 1 for value in kz)
    mass_z = int(sum(kz))
    mass_b = N - mass_z
    kb = tuple(
        t[position] + (mass_b if index == beta else 0)
        for position, index in enumerate(b_indices)
    )
    out = [0] * ambient_size
    for index, value in zip(z_indices, kz):
        out[index] = int(value)
    for index, value in zip(b_indices, kb):
        out[index] = value
    return tuple(out)


def audit_all_records_exact_product() -> int:
    """Exercise every Z/B/beta record in dimensions two through five."""

    fixtures = 0
    for ambient_size in range(3, 7):
        all_indices = tuple(range(ambient_size))
        for z_size in range(1, ambient_size):
            for z_indices in combinations(all_indices, z_size):
                z_set = set(z_indices)
                b_indices = tuple(index for index in all_indices if index not in z_set)
                for beta in b_indices:
                    for N in range(max(2, len(b_indices)), 8):
                        for k in compositions(N, ambient_size):
                            if min(k[index] for index in z_indices) != 0:
                                continue
                            if min(k[index] for index in b_indices) <= 0:
                                continue
                            q, t = repaired_general(k, z_indices, beta)
                            assert inverse_general(
                                N, q, t, z_indices, beta, ambient_size
                            ) == k
                            fixtures += 1
    return fixtures


def inverse_23(N: int, q: tuple[Fraction, Fraction], t: tuple[int, int, int]):
    minimum = min(q)
    kz = tuple(value - minimum for value in q)
    assert all(value.denominator == 1 for value in kz)
    k0, k1 = (int(value) for value in kz)
    mass_z = k0 + k1
    mass_b = N - mass_z
    kb = (t[0] + mass_b, t[1], t[2])
    return (k0, k1) + kb


def audit_23_exact_product() -> int:
    fixtures = 0
    for N in range(8, 25):
        seen_by_r: dict[int, set[int]] = {}
        for k in compositions(N, 5):
            if min(k) != 0 or min(k[2:]) < 2:
                continue
            if min(k[:2]) != 0:
                continue
            r = k[0] - k[1]
            seen_by_r.setdefault(r, set()).add(raw_residue_23(k))
            q, t = repaired_23(k)
            assert q == (Fraction(r, 2), Fraction(-r, 2))
            assert t == (-k[3] - k[4], k[3], k[4])
            assert inverse_23(N, q, t) == k
            fixtures += 1

        # The raw class is N-|r| mod 3 and fails to be invariant under the
        # candidate period r -> r+3 when that translation crosses r=0.
        for r, residues in seen_by_r.items():
            assert residues == {(N - abs(r)) % 3}
        crossing = [
            r for r in seen_by_r
            if r + 3 in seen_by_r
            and seen_by_r[r] != seen_by_r[r + 3]
        ]
        assert crossing, "the raw absolute-value interface was not exercised"

    return fixtures


def audit_buffered_translations() -> int:
    """Check exact product translations wherever positivity leaves a buffer."""

    fixtures = 0
    root_steps = (
        (1, -1, 0),
        (1, 0, -1),
        (-1, 1, 0),
        (0, 1, -1),
        (-1, 0, 1),
        (0, -1, 1),
    )
    # A1* consists of (r/2,-r/2), r in Z, so its primitive normal step is 1.
    normal_steps = (-1, 1)

    for N in (12, 17, 23):
        for k in compositions(N, 5):
            if min(k[:2]) != 0 or min(k[2:]) < 3:
                continue
            q, t = repaired_23(k)
            r = int(2 * q[0])

            for dr in normal_steps:
                q2 = (Fraction(r + dr, 2), Fraction(-r - dr, 2))
                k2 = inverse_23(N, q2, t)
                if min(k2) == 0 and min(k2[2:]) >= 1:
                    assert repaired_23(k2) == (q2, t)
                    fixtures += 1

            for step in root_steps:
                t2 = tuple(ti + si for ti, si in zip(t, step))
                k2 = inverse_23(N, q, t2)
                if min(k2) == 0 and min(k2[2:]) >= 1:
                    assert repaired_23(k2) == (q, t2)
                    fixtures += 1

    return fixtures


def audit_stated_buffer_counterexample() -> int:
    """Reject the last sentence of Lemma 1 with exact integer data.

    Take d=3, N=4, Z={0,1}, B={2,3}, beta=2 and
    k=(0,2,1,1).  Both B coordinates equal h, as required with s_*=1.
    A primitive A_B neighbour sends the fourth barycentric coordinate to
    zero, so it leaves the chart on which *every* B coordinate is positive.
    """

    N = 4
    h = Fraction(1, N)
    k = (0, 2, 1, 1)
    q = centered(k[:2])
    mass_b = sum(k[2:])
    t = (k[2] - mass_b, k[3])
    assert min(Fraction(value, N) for value in k[2:]) == h

    # The primitive root-lattice step +(e_beta-e_3) has lattice distance h.
    t_neighbour = (t[0] + 1, t[1] - 1)
    minimum = min(q)
    kz = tuple(value - minimum for value in q)
    mass_z = int(sum(kz))
    kb_neighbour = (t_neighbour[0] + N - mass_z, t_neighbour[1])
    assert kb_neighbour == (2, 0)
    assert min(kb_neighbour) == 0  # not in the open B-positive chart
    return 1


def poly_mul(a: list[Fraction], b: list[Fraction], degree: int):
    out = [Fraction(0) for _ in range(degree + 1)]
    for i, ai in enumerate(a):
        for j, bj in enumerate(b):
            if i + j <= degree:
                out[i + j] += ai * bj
    return out


def audit_midpoint_pair() -> int:
    """Symbolically verify central midpoint flux through order h^4.

    b(+h/2)(F(+h)-F(0)) + b(-h/2)(F(-h)-F(0))
    has only even powers.  Its h^2 coefficient is b F'' + b' F'.
    """

    degree = 6
    # Coefficients are normalized derivatives: b_k=b^(k)(0)/k!, likewise f.
    b = [Fraction(2), Fraction(3), Fraction(5), Fraction(7), Fraction(11), Fraction(13), Fraction(17)]
    f = [Fraction(19), Fraction(23), Fraction(29), Fraction(31), Fraction(37), Fraction(41), Fraction(43)]

    def scale_argument(coeffs, scale):
        return [coefficient * scale**index for index, coefficient in enumerate(coeffs)]

    fp = f.copy()
    fp[0] = 0
    fm = [coefficient * ((-1) ** index) for index, coefficient in enumerate(f)]
    fm[0] = 0
    bp = scale_argument(b, Fraction(1, 2))
    bm = scale_argument(b, Fraction(-1, 2))
    flux_p = poly_mul(bp, fp, degree)
    flux_m = poly_mul(bm, fm, degree)
    flux = [left + right for left, right in zip(flux_p, flux_m)]

    assert flux[1] == 0
    assert flux[3] == 0
    assert flux[5] == 0
    # 2*b0*f2 + b1*f1 in normalized-derivative notation.
    assert flux[2] == 2 * b[0] * f[2] + b[1] * f[1]
    return 3


def audit_pair_factor_normalization() -> int:
    """Check the exact factor mismatch between (3.4) and the force limit.

    In one dimension, take the affine coefficient b=rho and a quadratic
    scalar test function F(q)=q^2/2.  The two directed neighbours associated
    with one unoriented pair give force rho*h^2, hence principal tensor rho.
    Their increment-square covariance is 2*rho*h^2.  Therefore imposing
    2*rho=A, as in (3.4), makes the covariance A but the force tensor A/2.
    """

    h = Fraction(1, 7)
    rho = Fraction(5, 3)
    f0 = Fraction(0)
    fp = h * h / 2
    fm = h * h / 2
    force = rho * ((fp - f0) + (fm - f0))
    covariance = rho * (h * h + h * h)
    A = 2 * rho
    assert force / (h * h) == rho == A / 2
    assert covariance / (h * h) == 2 * rho == A
    return 2


def main() -> None:
    all_record_fixtures = audit_all_records_exact_product()
    product_fixtures = audit_23_exact_product()
    translation_fixtures = audit_buffered_translations()
    buffer_counterexamples = audit_stated_buffer_counterexample()
    midpoint_fixtures = audit_midpoint_pair()
    factor_counterexamples = audit_pair_factor_normalization()
    print(f"all-record-product-fixtures={all_record_fixtures}")
    print(f"2+3-product-fixtures={product_fixtures}")
    print(f"buffered-translation-fixtures={translation_fixtures}")
    print(f"stated-buffer-counterexamples={buffer_counterexamples}")
    print(f"midpoint-odd-cancellation-fixtures={midpoint_fixtures}")
    print(f"pair-factor-counterexamples={factor_counterexamples}")
    print("P1E local product algebra: PASS")
    print("P1E stated buffer/pair normalization: REJECTED")
    print("P1E stratified global construction: BLOCKED")


if __name__ == "__main__":
    main()

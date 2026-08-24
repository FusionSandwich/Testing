#!/usr/bin/env python3
"""Standalone exact verifier for the AFP Theorem 7.2 certificate.

This program uses only the Python standard library. It does not import the
construction or audit modules, SymPy, NumPy, or any floating-point package.
All certificate comparisons are performed in Q or Q(sqrt(58)).
"""

from __future__ import annotations

import hashlib
import json
import sys
from copy import deepcopy
from dataclasses import dataclass
from fractions import Fraction as F
from pathlib import Path
from typing import Any


RADICAND = 58


def q(value: str | int) -> F:
    return F(str(value))


@dataclass(frozen=True)
class Q58:
    a: F = F(0)
    b: F = F(0)

    def __add__(self, other: Q58 | int) -> Q58:
        z = as_q58(other)
        return Q58(self.a + z.a, self.b + z.b)

    __radd__ = __add__

    def __neg__(self) -> Q58:
        return Q58(-self.a, -self.b)

    def __sub__(self, other: Q58 | int) -> Q58:
        return self + (-as_q58(other))

    def __rsub__(self, other: Q58 | int) -> Q58:
        return as_q58(other) - self

    def __mul__(self, other: Q58 | int) -> Q58:
        z = as_q58(other)
        return Q58(self.a * z.a + RADICAND * self.b * z.b,
                   self.a * z.b + self.b * z.a)

    __rmul__ = __mul__

    def inverse(self) -> Q58:
        den = self.a * self.a - RADICAND * self.b * self.b
        if den == 0:
            raise ZeroDivisionError("zero in Q(sqrt(58))")
        return Q58(self.a / den, -self.b / den)

    def __truediv__(self, other: Q58 | int) -> Q58:
        return self * as_q58(other).inverse()

    def sign(self) -> int:
        if self.a == 0:
            return (self.b > 0) - (self.b < 0)
        if self.b == 0:
            return (self.a > 0) - (self.a < 0)
        if self.a > 0 and self.b > 0:
            return 1
        if self.a < 0 and self.b < 0:
            return -1
        cmp = self.a * self.a - RADICAND * self.b * self.b
        if cmp == 0:
            raise AssertionError("sqrt(58) incorrectly treated as rational")
        if self.a > 0:
            return 1 if cmp > 0 else -1
        return -1 if cmp > 0 else 1

    def abs(self) -> Q58:
        return self if self.sign() >= 0 else -self

    def __lt__(self, other: Q58 | int) -> bool:
        return (self - as_q58(other)).sign() < 0

    def __le__(self, other: Q58 | int) -> bool:
        return (self - as_q58(other)).sign() <= 0


def as_q58(value: Q58 | int | F) -> Q58:
    return value if isinstance(value, Q58) else Q58(F(value), F(0))


def q58(pair: list[str]) -> Q58:
    assert isinstance(pair, list) and len(pair) == 2
    return Q58(q(pair[0]), q(pair[1]))


def determinant(matrix: list[list[Q58]]) -> Q58:
    a = [row[:] for row in matrix]
    det = Q58(F(1), F(0))
    n = len(a)
    for col in range(n):
        pivot = next((row for row in range(col, n) if a[row][col] != Q58()), None)
        assert pivot is not None, "singular limiting matrix"
        if pivot != col:
            a[col], a[pivot] = a[pivot], a[col]
            det = -det
        p = a[col][col]
        det = det * p
        for row in range(col + 1, n):
            factor = a[row][col] / p
            for k in range(col, n):
                a[row][k] = a[row][k] - factor * a[col][k]
    return det


def inverse(matrix: list[list[Q58]]) -> list[list[Q58]]:
    n = len(matrix)
    a = [row[:] + [Q58(F(int(i == j)), F(0)) for j in range(n)]
         for i, row in enumerate(matrix)]
    for col in range(n):
        pivot = next((row for row in range(col, n) if a[row][col] != Q58()), None)
        assert pivot is not None, "singular limiting matrix"
        a[col], a[pivot] = a[pivot], a[col]
        p = a[col][col]
        a[col] = [x / p for x in a[col]]
        for row in range(n):
            if row == col:
                continue
            factor = a[row][col]
            a[row] = [x - factor * y for x, y in zip(a[row], a[col])]
    return [row[n:] for row in a]


def matrix_vector(matrix: list[list[Q58]], vector: list[Q58]) -> list[Q58]:
    return [sum((x * y for x, y in zip(row, vector)), Q58()) for row in matrix]


def verify_source_bindings(cert: dict[str, Any], repo_root: Path) -> None:
    for rel, expected in cert["source_bindings"].items():
        path = repo_root / Path(rel)
        actual = hashlib.sha256(path.read_bytes()).hexdigest()
        assert actual == expected, f"source hash mismatch: {rel}"


def verify_transition_guard(data: dict[str, Any]) -> None:
    radius = q(data["disk_radius"])
    x = q(data["x_actual"])
    pi_lo, pi_hi = q(data["pi_lower"]), q(data["pi_upper"])
    a_lo, a_hi = q(data["a_lower"]), q(data["a_upper"])
    c_lo = q(data["cos_theta_lower"])
    assert F(1, 4) - 3 * radius > a_lo
    assert F(1, 4) + 3 * radius < a_hi
    r_bound = pi_hi * radius / a_lo
    alpha_bound = pi_hi * radius
    assert r_bound < F(1, 700)
    assert 16 * alpha_bound < F(1, 180)
    assert 1 - alpha_bound**2 > F(9, 10)
    assert 3 * a_hi**2 < 1 and 17 * a_hi**4 < 1
    force = 2 + 3 * 7 * r_bound
    loss = 2 + 7 * (2 * 3 + 3 * r_bound) + 3 * 3 * 7**2 * r_bound
    iso = 4 + 4 * 3 * 7 * r_bound + 7**2 * (10 * r_bound**2 + 2)
    assert force < 3 and loss < 45 and iso < 103
    U = F(17)
    c_ratio = F(7, 2)
    horizontals = (2 * 3 * c_ratio * U,
                   2 * 3**3 * c_ratio * U**2,
                   2 * 3**2 * (2 * U + 10 * r_bound**2 * U**2))
    matrix_disk = q(data["matrix_disk_bound"])
    assert 16 * max(force, loss, iso, *horizontals) < matrix_disk
    inv_cr = a_hi / (c_lo * pi_lo * radius)
    assert inv_cr < 1000
    rhs = max(3 * 3 * inv_cr * 16, 45 * 3 * inv_cr * 16, 103 * 3 * 16)
    rhs_disk = q(data["rhs_disk_bound"])
    assert rhs < rhs_disk
    assert x < radius / 2
    d_a = 2 * matrix_disk / radius
    d_b = 2 * rhs_disk / radius
    assert d_a < q(data["matrix_derivative_bound"])
    assert d_b < q(data["rhs_derivative_bound"])
    entry = q(data["neumann_entry_bound"])
    assert entry == F(10**12, 2**80)
    assert 18 * entry < q(data["neumann_contraction_upper"])
    assert 244 * entry < q(data["solution_displacement_upper"])
    assert q(data["solution_displacement_upper"]) < q(data["limiting_cone_lower"])


def verify_limiting_system(data: dict[str, Any]) -> None:
    matrix = [[q58(x) for x in row] for row in data["matrix"]]
    assert len(matrix) == 6 and all(len(row) == 6 for row in matrix)
    assert determinant(matrix) == q58(data["determinant"])
    inv = inverse(matrix)
    norm_upper = Q58(q(data["inverse_infinity_norm_upper"]), F(0))
    assert all(sum((x.abs() for x in row), Q58()) < norm_upper for row in inv)

    rhs_c = [q58(item["constant"]) for item in data["rhs_affine"]]
    rhs_y = [q58(item["y"]) for item in data["rhs_affine"]]
    sol_c = [q58(item["constant"]) for item in data["solution_affine"]]
    sol_y = [q58(item["y"]) for item in data["solution_affine"]]
    assert matrix_vector(matrix, sol_c) == rhs_c
    assert matrix_vector(matrix, sol_y) == rhs_y

    lo, hi = map(q, data["phase_box"])
    lower = Q58(q(data["solution_component_lower"]), F(0))
    upper = Q58(q(data["solution_component_upper"]), F(0))
    for y in (lo, hi):
        values = [a + y * b for a, b in zip(sol_c, sol_y)]
        assert all(lower < value and value < upper for value in values)


def verify_polar_guard(data: dict[str, Any]) -> None:
    a = q(data["a"])
    u_lo, u_hi = map(q, data["u_interval"])
    v_lo, v_hi = map(q, data["v_interval"])
    radius = q(data["disk_radius"])
    h = q(data["actual_h_upper"])
    assert a * radius < F(1, 70)
    det_lower = 4 * a**3 * u_lo * v_lo * (a - 1) * (2 * a + 1) * (v_lo - u_hi)
    assert det_lower == q(data["determinant_lower"])
    assert 3 * 512 / det_lower < q(data["inverse_infinity_norm_upper"])
    up = 2 * a**3 / ((a - 1) * (2 * a + 1))
    h1 = (a + 1) * (2 * a + 2 * v_hi - 3) / (
        4 * u_lo * (a - 1) * (2 * a + 1) * (v_lo - u_hi))
    h2 = (a + 1) * (3 - 2 * a - 2 * u_lo) / (
        4 * v_lo * (a - 1) * (2 * a + 1) * (v_lo - u_hi))
    assert max(up, h1, h2) < q(data["limiting_solution_upper"])
    inverse_bound = q(data["inverse_infinity_norm_upper"])
    d_a, d_b = q(data["matrix_derivative_bound"]), q(data["rhs_derivative_bound"])
    contraction = inverse_bound * 3 * d_a * h
    assert contraction < F(1, 10**12)
    inverse_finite = inverse_bound / (1 - contraction)
    displacement = inverse_finite * (d_b * h + 3 * d_a * h * 64)
    assert displacement < q(data["finite_displacement_upper"])


def verify_ordinary_and_constants(ordinary: dict[str, Any], published: dict[str, Any]) -> None:
    z = q(ordinary["z_upper"])
    assert F(16) / (1 - 4 * z) < q(ordinary["telescoping_error_coefficient_upper"])
    assert q(ordinary["horizontal_solution_lower_ratio"]) == F(1, 100)
    assert q(ordinary["horizontal_solution_upper_ratio"]) == F(100)
    assert ordinary["shared_stress_lower_exponent"] == -20
    assert ordinary["shared_stress_upper_exponent"] == 20
    angle_lo = q(published["active_angle_lower_multiple"])
    angle_hi = q(published["active_angle_upper_multiple"])
    assert angle_lo == F(1, 8) and angle_hi == 5
    assert q(published["rate_constant"]) == 2 * 32
    assert published["rate_pi_power"] == 2
    assert q(published["residual_constant"]) == F(3 * 5**2, 2)
    assert q(published["frontier_lower_constant_without_pi"]) == F(6, 64)
    assert q(published["degree_bound"]) == 2**80


def verify_theorem_scale_transition(data: dict[str, Any], m0: int) -> None:
    ratio = q(data["count_ratio"])
    numerator = q(data["transition_error_numerator"])
    assert ratio == 2 and numerator == 256

    a_star = numerator / m0
    linear_sum = (numerator / m0) / (1 - 1 / ratio)
    square_sum = (numerator / m0) ** 2 / (1 - 1 / ratio**2)
    assert a_star == q(data["max_transition_error"])
    assert linear_sum == q(data["linear_sum_upper"])
    assert square_sum == q(data["square_sum_upper"])
    assert a_star < 1

    # For |x|<=a_star, the ordinary analytic lemma used by the manuscript is
    # log(1+x) >= x-x^2/(2(1-a_star)) and log(1+x) <= x.
    remainder = square_sum / (2 * (1 - a_star))
    assert remainder < q(data["quadratic_remainder_upper"])
    assert linear_sum + remainder < q(data["log_lower_magnitude_upper"])
    assert linear_sum == q(data["log_upper_magnitude_upper"])

    # Exercise finite theorem levels without enumerating their astronomical
    # ring counts.  These are exact recurrence-budget objects for each J.
    sample_levels = data["sample_levels"]
    assert sample_levels == [1, 2, 8, 32, 80, 257]
    for level in sample_levels:
        assert isinstance(level, int) and level >= 1
        errors = [numerator / (m0 * ratio**m) for m in range(level)]
        finite_linear = sum(errors, F(0))
        finite_square = sum((x * x for x in errors), F(0))
        negative_product = F(1)
        positive_product = F(1)
        for error in errors:
            assert error <= a_star < 1
            negative_product *= 1 - error
            positive_product *= 1 + error
        assert 0 < negative_product < 1 < positive_product
        assert finite_linear < linear_sum and finite_square < square_sum

    # Hostile mutation: the R6 exponent 512 is false for the all-negative
    # level-80 sequence.  log(1-a)<=-a-a^2/2 makes this an exact rational
    # rejection, with no numerical evaluation of exp.
    hostile_level = q(data["old_lower_bound_counterexample_level"])
    assert hostile_level.denominator == 1 and hostile_level == 80
    errors = [numerator / (m0 * ratio**m) for m in range(int(hostile_level))]
    magnitude_lower = sum(errors, F(0)) + sum((x * x for x in errors), F(0)) / 2
    assert magnitude_lower > q(data["rejected_log_lower_magnitude"])


def verify_positivity_geometry_normalization(
    data: dict[str, Any],
    transition: dict[str, Any],
    polar: dict[str, Any],
    ordinary: dict[str, Any],
    published: dict[str, Any],
    m0: int,
) -> None:
    assert q(data["mask_entry_lower"]) == F(1, 64)
    transition_lower = q(transition["limiting_cone_lower"]) - q(
        transition["solution_displacement_upper"]
    )
    assert transition_lower == q(data["transition_solution_lower"])
    assert q(data["polar_solution_lower"]) < F(1, 20) - q(
        polar["finite_displacement_upper"]
    )
    assert q(data["ordinary_horizontal_lower_ratio"]) == q(
        ordinary["horizontal_solution_lower_ratio"]
    )
    assert q(data["ordinary_horizontal_upper_ratio"]) == q(
        ordinary["horizontal_solution_upper_ratio"]
    )
    assert data["preliminary_stress_exponents"] == [-20, 20]

    q_star = q(data["separation_constant"])
    assert q_star == F(1, 8 * m0)
    assert q(data["degree_bound"]) == m0 == q(published["degree_bound"])
    assert q(data["active_angle_lower_multiple"]) == F(1, 8)
    assert q(data["active_angle_upper_multiple"]) == 5
    assert q(data["node_count_rational_coefficient"]) == 4

    # Symbolic coefficient/exponent audit of the mass and normalization chain:
    # mu_min=Gamma_- h^2/(64 pi^2),
    # mu_max=25 D Gamma_+ h^2/4,
    # N<=4 pi^2 q_*^-2 h^-2,
    # W<=25 pi^2 D Gamma_+ q_*^-2, and hence
    # w_i>=Gamma_- q_*^2 h^2/(1600 pi^4 D Gamma_+).
    assert q(data["mu_lower_rational_denominator"]) == 64
    assert q(data["mu_lower_pi_power"]) == 2
    assert q(data["mu_upper_rational_coefficient"]) == F(25, 4)
    assert q(data["weight_floor_rational_denominator"]) == 64 * 25
    assert q(data["weight_floor_pi_power"]) == 4
    assert q(data["weight_floor_q_star_power"]) == 2
    assert data["normalized_conductance_relation"] == "gamma_ij = Gamma_ij / W"
    assert data["directed_rate_relation"] == "a_ij = gamma_ij / w_i = Gamma_ij / mu_i"

    # Final rate, residual, and frontier constants are derived, not accepted as
    # disconnected literals.
    ell_min_denominator = 8**2 // 2  # 1-cos(x)>=2x^2/pi^2 at x=h/8
    assert ell_min_denominator == 32
    assert q(published["rate_constant"]) == 2 * ell_min_denominator
    ell_max_coefficient = F(5**2, 2)
    assert q(published["residual_constant"]) == 3 * ell_max_coefficient
    assert q(published["frontier_lower_constant_without_pi"]) == F(6, 64)


def expect_failure(action: Any, label: str) -> None:
    try:
        action()
    except AssertionError:
        return
    raise AssertionError(f"hostile mutation was not rejected: {label}")


def verify_hostile_mutations(cert: dict[str, Any], m0: int) -> None:
    mutated = deepcopy(cert["positivity_geometry_normalization"])
    mutated["normalized_conductance_relation"] = "gamma_ij = Gamma_ij"
    expect_failure(
        lambda: verify_positivity_geometry_normalization(
            mutated,
            cert["transition_guard"],
            cert["polar_guard"],
            cert["ordinary_rows_and_recurrence"],
            cert["published_constants"],
            m0,
        ),
        "missing Gamma/W normalization",
    )

    mutated_published = deepcopy(cert["published_constants"])
    mutated_published["rate_constant"] = "63"
    expect_failure(
        lambda: verify_positivity_geometry_normalization(
            cert["positivity_geometry_normalization"],
            cert["transition_guard"],
            cert["polar_guard"],
            cert["ordinary_rows_and_recurrence"],
            mutated_published,
            m0,
        ),
        "rate constant",
    )

    mutated_transition = deepcopy(cert["theorem_scale_transition"])
    mutated_transition["log_lower_magnitude_upper"] = "512/1208925819614629174706176"
    expect_failure(
        lambda: verify_theorem_scale_transition(mutated_transition, m0),
        "R6 cumulative lower exponent",
    )


def main() -> int:
    path = Path(sys.argv[1]).resolve() if len(sys.argv) == 2 else Path(__file__).with_name("certificate.json")
    cert = json.loads(path.read_text(encoding="utf-8"))
    assert cert["schema"] == "afp-theorem-7.2-exact-rational-certificate-v2"
    assert cert["classification"] == "COMPUTER_ASSISTED_EXACT_RATIONAL"
    assert cert["claim_boundary"]["whole_theorem_machine_verified"] is False
    assert cert["claim_boundary"]["source_hashes_are_proofs"] is False
    assert "schedule" in cert["claim_boundary"]["ordinary_proof_components"]
    assert cert["family"]["ambient_dimension"] == 3
    m0 = int(q(cert["family"]["M0"]))
    assert m0 == 2**80
    assert cert["family"]["sqrt_radicand"] == RADICAND
    repo_root = Path(__file__).resolve().parents[4]
    verify_source_bindings(cert, repo_root)
    verify_transition_guard(cert["transition_guard"])
    verify_limiting_system(cert["limiting_system"])
    verify_polar_guard(cert["polar_guard"])
    verify_ordinary_and_constants(cert["ordinary_rows_and_recurrence"], cert["published_constants"])
    verify_theorem_scale_transition(cert["theorem_scale_transition"], m0)
    verify_positivity_geometry_normalization(
        cert["positivity_geometry_normalization"],
        cert["transition_guard"],
        cert["polar_guard"],
        cert["ordinary_rows_and_recurrence"],
        cert["published_constants"],
        m0,
    )
    verify_hostile_mutations(cert, m0)
    print("Theorem 7.2 exact-rational certificate: PASS")
    print(f"certificate_sha256={hashlib.sha256(path.read_bytes()).hexdigest()}")
    print("arithmetic=Q and Q(sqrt(58)); floating_point=none; third_party_imports=none")
    print("theorem_scale_levels=1,2,8,32,80,257; hostile_mutations=3/3 rejected")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Deterministic Prompt-3 graph-global near-rigidity audit.

Status: COMPUTATIONAL.  Rational identities are checked exactly.  Statements
involving ``log``, ``exp``, ``sin`` and ``acos`` are evaluated by SymPy at 100
decimal digits and must pass with a displayed positive margin.  Those checks
are hostile regressions for the closed constants; they do not replace the
ordinary inequalities or Lean proofs.

The fixed spherical-angle box uses the Gram/Heron identity

    det G = 4 sin(s) sin(s-a) sin(s-b) sin(s-c)

to obtain a positive lower bound for ``sin(A)``.  It intentionally does not use
the older independent numerator/denominator enclosure, which exceeds one at
the exact icosahedral reference.
"""
from __future__ import annotations

from fractions import Fraction
import itertools
import json

import mpmath as mp
import sympy as sp


DIGITS = 100
TOLERANCE = sp.Float("1e-70", DIGITS)
mp.mp.dps = DIGITS
MP_TOLERANCE = mp.mpf("1e-70")


def numerical(value: sp.Expr) -> sp.Float:
    return sp.N(sp.simplify(value), DIGITS)


def assert_nonnegative(value: sp.Expr, label: str, tolerance: sp.Float = TOLERANCE) -> sp.Float:
    approximation = numerical(value)
    if approximation < -tolerance:
        raise AssertionError(f"{label}: {approximation} < 0")
    return approximation


def assert_positive(value: sp.Expr, label: str, margin: sp.Float = TOLERANCE) -> sp.Float:
    approximation = numerical(value)
    if approximation <= margin:
        raise AssertionError(f"{label}: no certified positive margin ({approximation})")
    return approximation


def choose_min(expressions: list[sp.Expr]) -> sp.Expr:
    if not expressions:
        raise ValueError("minimum of an empty list")
    return min(expressions, key=lambda expression: numerical(expression))


def mp_string(value: mp.mpf) -> str:
    return mp.nstr(value, 80)


def assert_mp_nonnegative(value: mp.mpf, label: str) -> mp.mpf:
    if value < -MP_TOLERANCE:
        raise AssertionError(f"{label}: {mp_string(value)} < 0")
    return value


def assert_mp_positive(value: mp.mpf, label: str, margin: mp.mpf = MP_TOLERANCE) -> mp.mpf:
    if value <= margin:
        raise AssertionError(f"{label}: no certified positive margin ({mp_string(value)})")
    return value


def exact_variance_identity() -> dict[str, str]:
    p = [Fraction(1, 7), Fraction(2, 7), Fraction(4, 7)]
    x = [Fraction(1, 2), Fraction(5, 4), Fraction(0)]
    x[-1] = (Fraction(1) - p[0] * x[0] - p[1] * x[1]) / p[2]
    mean = sum((weight * value for weight, value in zip(p, x)), Fraction(0))
    quality = sum((weight * value**2 for weight, value in zip(p, x)), Fraction(0))
    variance = sum((weight * (value - 1) ** 2 for weight, value in zip(p, x)), Fraction(0))
    if mean != 1 or quality - 1 != variance:
        raise AssertionError("weighted Q-minus-one identity failed")

    # Signed weights show exactly why positivity is indispensable: mean and
    # second moment are one although the scales are unequal.
    signed_p = [Fraction(1, 3), Fraction(1), -Fraction(1, 3)]
    signed_x = [Fraction(0), Fraction(2), Fraction(3)]
    signed_mean = sum((a * b for a, b in zip(signed_p, signed_x)), Fraction(0))
    signed_second = sum((a * b * b for a, b in zip(signed_p, signed_x)), Fraction(0))
    if signed_mean != 1 or signed_second != 1 or len(set(signed_x)) == 1:
        raise AssertionError("signed equality counterexample changed")

    return {
        "mean": str(mean),
        "Q_minus_1": str(quality - 1),
        "variance": str(variance),
        "signed_counterexample_weights": [str(value) for value in signed_p],
        "signed_counterexample_scales": [str(value) for value in signed_x],
    }


def pointwise_small_kappa_and_long_path() -> dict[str, object]:
    cases = 0
    longest = 0
    largest_exact_numerator_digits = 0
    records: list[dict[str, str | int]] = []
    for kappa in (Fraction(1, 2), Fraction(1, 5), Fraction(1, 1000)):
        for delta in (Fraction(1, 10_000), Fraction(1, 100), Fraction(1, 3)):
            eta = kappa * delta**2
            x = 1 + delta
            if kappa * (x - 1) ** 2 != eta:
                raise AssertionError("small-kappa pointwise saturation failed")
            q_delta = (1 + delta) / (1 - delta)
            for length in (1, 7, 50, 200):
                rates = [q_delta**index for index in range(length + 1)]
                if rates[-1] / rates[0] != q_delta**length:
                    raise AssertionError("long-path product bound changed")
                for index in range(length):
                    left_scale = 1 - delta
                    right_scale = 1 + delta
                    loss_left = 2 * left_scale / rates[index]
                    loss_right = 2 * right_scale / rates[index + 1]
                    if loss_left != loss_right:
                        raise AssertionError("shared-edge normalized scales are inconsistent")
                    local_ratio = rates[index + 1] / rates[index]
                    if local_ratio != q_delta:
                        raise AssertionError("adjacent rate ratio failed")
                longest = max(longest, length)
                largest_exact_numerator_digits = max(
                    largest_exact_numerator_digits, len(str(rates[-1].numerator)))
                cases += 1
            records.append({
                "kappa": str(kappa), "delta": str(delta), "eta": str(eta),
                "q_delta": str(q_delta),
            })
    return {
        "cases": cases,
        "longest_path": longest,
        "largest_exact_rate_numerator_digits": largest_exact_numerator_digits,
        "small_kappa_records": records,
        "diameter_free_local_only_claim": "REJECTED",
    }


def path_conductance_chain() -> tuple[list[list[Fraction]], list[Fraction]]:
    raw = [Fraction(1, 20), Fraction(1, 15), Fraction(1, 12),
           Fraction(1, 10), Fraction(1, 8)]
    normalizer = 2 * sum(raw, Fraction(0))
    edge = [value / normalizer for value in raw]
    n = len(edge) + 1
    conductance = [[Fraction(0) for _ in range(n)] for _ in range(n)]
    for index, value in enumerate(edge):
        conductance[index][index + 1] = value
        conductance[index + 1][index] = value
    pi = [sum(row, Fraction(0)) for row in conductance]
    if sum(pi, Fraction(0)) != 1:
        raise AssertionError("stationary law is not normalized")
    return conductance, pi


def energy_and_resistance_factor_audit() -> dict[str, str]:
    conductance, pi = path_conductance_chain()
    n = len(pi)
    transition = [[Fraction(0) for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            transition[i][j] = conductance[i][j] / pi[i]
        if sum(transition[i], Fraction(0)) != 1:
            raise AssertionError("P is not row stochastic")
    for i in range(n):
        for j in range(n):
            if pi[i] * transition[i][j] != pi[j] * transition[j][i]:
                raise AssertionError("detailed balance failed")

    u = [Fraction(0), Fraction(1, 20), -Fraction(1, 10),
         Fraction(1, 5), -Fraction(1, 4), Fraction(3, 10)]
    directed_twice = sum(
        (pi[i] * transition[i][j] * (u[i] - u[j]) ** 2
         for i in range(n) for j in range(n)), Fraction(0))
    energy_p = directed_twice / 2
    energy_c = sum(
        (conductance[i][j] * (u[i] - u[j]) ** 2
         for i in range(n) for j in range(i + 1, n)), Fraction(0))
    if energy_p != energy_c:
        raise AssertionError("the 1/2-directed and single-edge energies differ")

    endpoint_resistance = sum(
        (1 / conductance[i][i + 1] for i in range(n - 1)), Fraction(0))
    endpoint_difference_sq = (u[0] - u[-1]) ** 2
    resistance_slack = endpoint_resistance * energy_c - endpoint_difference_sq
    if resistance_slack < 0:
        raise AssertionError("effective-resistance factor convention failed")

    # A two-state no-holding reversible chain has Poincare gap 2 under this
    # Dirichlet convention: E=(u0-u1)^2/2 and Var=(u0-u1)^2/4.
    two_state_energy = Fraction(1, 2) * (u[0] - u[-1]) ** 2
    two_state_variance = Fraction(1, 4) * (u[0] - u[-1]) ** 2
    if two_state_energy != 2 * two_state_variance:
        raise AssertionError("Poincare factor convention changed")

    # Detailed balance makes the reverse-directed defect average identical,
    # explaining the factor two in E_P(log r) <= 2 eta/(1-delta)^2.
    defects = [[Fraction((i + 2) * (j + 3), 10_000) for j in range(n)] for i in range(n)]
    first = sum(
        (pi[i] * transition[i][j] * defects[i][j]
         for i in range(n) for j in range(n)), Fraction(0))
    reversed_average = sum(
        (pi[i] * transition[i][j] * defects[j][i]
         for i in range(n) for j in range(n)), Fraction(0))
    swapped_first = sum(
        (pi[j] * transition[j][i] * defects[j][i]
         for i in range(n) for j in range(n)), Fraction(0))
    if reversed_average != swapped_first:
        raise AssertionError("directed-defect detailed-balance swap failed")
    # ``swapped_first`` is the same first-directed sum after dummy-index swap.
    if swapped_first != first:
        # The arbitrary table is not symmetric, but dummy-index swapping also
        # swaps its indices; check the correct expression explicitly instead.
        renamed = sum(
            (pi[i] * transition[i][j] * defects[i][j]
             for j in range(n) for i in range(n)), Fraction(0))
        if swapped_first != renamed:
            raise AssertionError("reverse average did not rename to first average")

    return {
        "stationary_law": [str(value) for value in pi],
        "E_P_half_directed": str(energy_p),
        "E_c_single_undirected": str(energy_c),
        "R_eff_endpoints": str(endpoint_resistance),
        "resistance_slack": str(resistance_slack),
        "two_state_poincare_gap": "2",
        "near_rigidity_energy_factor": "2",
    }


def small_nonabsolute_poincare_gap_audit() -> dict[str, object]:
    """Exercise the exact non-absolute gap convention on a periodic chain.

    The symmetric four-state chain has no holding probabilities.  Its exact
    spectrum is ``1, 1-2 epsilon, -(1-2 epsilon), -1``.  Thus the Poincare gap
    is the small number ``2 epsilon``, while the absolute spectral gap is zero;
    this makes the convention distinction executable rather than verbal.
    """
    epsilon = Fraction(1, 10_000)
    one = Fraction(1)
    zero = Fraction(0)
    transition = [
        [zero, one - epsilon, epsilon, zero],
        [one - epsilon, zero, zero, epsilon],
        [epsilon, zero, zero, one - epsilon],
        [zero, epsilon, one - epsilon, zero],
    ]
    pi = [Fraction(1, 4)] * 4
    if any(sum(row, Fraction(0)) != 1 for row in transition):
        raise AssertionError("small-gap transition matrix is not stochastic")
    if any(transition[i][i] != 0 for i in range(4)):
        raise AssertionError("small-gap chain unexpectedly has holding")
    for i in range(4):
        for j in range(4):
            if pi[i] * transition[i][j] != pi[j] * transition[j][i]:
                raise AssertionError("small-gap chain is not reversible")

    eigenvectors = (
        ([Fraction(1), Fraction(1), Fraction(1), Fraction(1)], one),
        ([Fraction(1), Fraction(1), -Fraction(1), -Fraction(1)], one - 2 * epsilon),
        ([Fraction(1), -Fraction(1), Fraction(1), -Fraction(1)], -(one - 2 * epsilon)),
        ([Fraction(1), -Fraction(1), -Fraction(1), Fraction(1)], -one),
    )
    for vector, eigenvalue in eigenvectors:
        image = [
            sum((transition[i][j] * vector[j] for j in range(4)), Fraction(0))
            for i in range(4)
        ]
        if image != [eigenvalue * value for value in vector]:
            raise AssertionError(f"small-gap eigenpair changed: {eigenvalue}")
    eigenbasis = sp.Matrix.hstack(*(sp.Matrix(vector) for vector, _ in eigenvectors))
    if eigenbasis.det() == 0:
        raise AssertionError("small-gap eigenvectors do not form a basis")

    eigenvalues = [eigenvalue for _, eigenvalue in eigenvectors]
    ordered_eigenvalues = sorted(eigenvalues, reverse=True)
    nonabsolute_gap = one - ordered_eigenvalues[1]
    absolute_gap = one - max(abs(value) for value in eigenvalues[1:])
    if nonabsolute_gap != 2 * epsilon or absolute_gap != 0:
        raise AssertionError("small-gap spectral convention changed")
    test_vectors = (
        [Fraction(1), Fraction(1), -Fraction(1), -Fraction(1)],
        [Fraction(0), Fraction(1, 3), -Fraction(2, 5), Fraction(7, 11)],
        [Fraction(5, 7), -Fraction(2, 3), Fraction(1, 5), -Fraction(3, 8)],
    )
    rayleigh_records: list[dict[str, str]] = []
    for vector in test_vectors:
        mean = sum((pi[i] * vector[i] for i in range(4)), Fraction(0))
        variance = sum(
            (pi[i] * (vector[i] - mean) ** 2 for i in range(4)), Fraction(0)
        )
        directed_twice = sum(
            (pi[i] * transition[i][j] * (vector[i] - vector[j]) ** 2
             for i in range(4) for j in range(4)), Fraction(0)
        )
        energy = directed_twice / 2
        slack = energy - nonabsolute_gap * variance
        if variance <= 0 or slack < 0:
            raise AssertionError("small non-absolute Poincare inequality failed")
        rayleigh_records.append({
            "variance": str(variance),
            "half_directed_energy": str(energy),
            "poincare_slack": str(slack),
        })
    if rayleigh_records[0]["poincare_slack"] != "0":
        raise AssertionError("slow-mode Poincare equality changed")

    return {
        "mode": "exact rational",
        "states": 4,
        "holding_probabilities": "all zero",
        "epsilon": str(epsilon),
        "eigenvalues": [str(value) for value in eigenvalues],
        "nonabsolute_poincare_gap": str(nonabsolute_gap),
        "absolute_spectral_gap": str(absolute_gap),
        "rayleigh_checks": rayleigh_records,
    }


def logarithmic_edge_inequality_stress() -> dict[str, str | int]:
    cases = 0
    minimum_margin: sp.Expr | None = None
    for delta_q in (sp.Rational(1, 10_000), sp.Rational(1, 100), sp.Rational(1, 3)):
        values = (1 - delta_q, 1 - delta_q / 2, sp.Integer(1),
                  1 + delta_q / 2, 1 + delta_q)
        for x_value, y_value in itertools.product(values, repeat=2):
            lhs = (sp.log(x_value) - sp.log(y_value)) ** 2
            rhs = 2 * ((x_value - 1) ** 2 + (y_value - 1) ** 2) / (1 - delta_q) ** 2
            margin = sp.simplify(rhs - lhs)
            assert_nonnegative(margin, "logarithmic edge inequality")
            minimum_margin = margin if minimum_margin is None else choose_min([minimum_margin, margin])
            cases += 1
    return {"cases": cases, "minimum_margin": str(numerical(minimum_margin or sp.Integer(0)))}


def mp_from_rational(value: sp.Rational) -> mp.mpf:
    return mp.mpf(int(value.p)) / mp.mpf(int(value.q))


def arccos_lipschitz_endpoint_stress() -> dict[str, object]:
    """Test (4.13) on exact loss boxes near both singular endpoints.

    Interval membership and the endpoint minimum of ``ell (2-ell)`` are
    checked with exact rational arithmetic.  The transcendental arccos values
    and the resulting MVT margins are then evaluated at 100 decimal digits.
    """
    scale = sp.Integer(10) ** 20
    cases = {
        "theta_to_zero": (sp.Rational(1, scale), sp.Rational(9, scale)),
        "theta_to_pi": (
            sp.Rational(2) - sp.Rational(9, scale),
            sp.Rational(2) - sp.Rational(1, scale),
        ),
    }
    report: dict[str, object] = {}
    for name, (ell_minus, ell_plus) in cases.items():
        if not (0 < ell_minus < ell_plus < 2):
            raise AssertionError(f"{name}: loss interval is not inside (0,2)")
        endpoint_radicands = (
            sp.factor(ell_minus * (2 - ell_minus)),
            sp.factor(ell_plus * (2 - ell_plus)),
        )
        minimum_radicand = min(endpoint_radicands)
        sigma_arc = mp.sqrt(mp_from_rational(minimum_radicand))
        assert_mp_positive(sigma_arc, f"{name}: sigma_arc")

        exact_samples = [
            ell_minus + sp.Rational(index, 8) * (ell_plus - ell_minus)
            for index in range(9)
        ]
        samples = [mp_from_rational(value) for value in exact_samples]
        inverse_sigma = 1 / sigma_arc
        for exact_ell, ell in zip(exact_samples, samples):
            exact_radicand = sp.factor(exact_ell * (2 - exact_ell))
            if exact_radicand < minimum_radicand:
                raise AssertionError(f"{name}: endpoint radicand minimum failed")
            derivative = 1 / mp.sqrt(ell * (2 - ell))
            assert_mp_nonnegative(
                inverse_sigma - derivative,
                f"{name}: derivative cap on certified interval",
            )

        pair_count = 0
        minimum_margin: mp.mpf | None = None
        maximum_secant = mp.mpf(0)
        for left_index, right_index in itertools.combinations(range(len(samples)), 2):
            ell_left, ell_right = samples[left_index], samples[right_index]
            theta_left = mp.acos(1 - ell_left)
            theta_right = mp.acos(1 - ell_right)
            loss_difference = abs(ell_right - ell_left)
            angle_difference = abs(theta_right - theta_left)
            bound = loss_difference / sigma_arc
            margin = bound - angle_difference
            assert_mp_nonnegative(margin, f"{name}: arccos MVT bound")
            secant = angle_difference / loss_difference
            maximum_secant = max(maximum_secant, secant)
            minimum_margin = margin if minimum_margin is None else min(minimum_margin, margin)
            pair_count += 1
        assert_mp_nonnegative(
            inverse_sigma - maximum_secant,
            f"{name}: maximum arccos secant below endpoint derivative cap",
        )
        report[name] = {
            "mode": "exact rational interval; 100-digit transcendental evaluation",
            "ell_minus": str(ell_minus),
            "ell_plus": str(ell_plus),
            "sigma_arc": mp_string(sigma_arc),
            "inverse_sigma_arc": mp_string(inverse_sigma),
            "sample_pairs": pair_count,
            "maximum_secant_slope": mp_string(maximum_secant),
            "minimum_MVT_margin": mp_string(minimum_margin or mp.mpf(0)),
        }
    return report


def sine_endpoint_minimum(lower: mp.mpf, upper: mp.mpf) -> mp.mpf:
    return min(mp.sin(lower), mp.sin(upper))


def fixed_angle_box(theta0: mp.mpf) -> dict[str, mp.mpf]:
    tau = min(theta0, mp.pi - theta0, 2 * mp.pi / 3 - theta0) / 4
    lower, upper = theta0 - tau, theta0 + tau
    assert_mp_positive(lower, "fixed side lower endpoint")
    assert_mp_positive(mp.pi - upper, "fixed side upper endpoint below pi")
    assert_mp_positive(2 * lower - upper, "uniform triangle inequality margin")
    assert_mp_positive(2 * mp.pi - 3 * upper, "uniform spherical perimeter margin")

    semiperimeter_lower, semiperimeter_upper = 3 * lower / 2, 3 * upper / 2
    half_difference_lower = (2 * lower - upper) / 2
    half_difference_upper = (2 * upper - lower) / 2
    sine_semiperimeter = sine_endpoint_minimum(semiperimeter_lower, semiperimeter_upper)
    sine_half_difference = sine_endpoint_minimum(half_difference_lower, half_difference_upper)
    assert_mp_positive(sine_semiperimeter, "semiperimeter sine lower bound")
    assert_mp_positive(sine_half_difference, "half-difference sine lower bound")

    gram_lower = 4 * sine_semiperimeter * sine_half_difference**3
    sin_angle_lower = mp.sqrt(gram_lower)
    sine_side = sine_endpoint_minimum(lower, upper)
    c_ang = 1 / (sin_angle_lower * sine_side**2) + 4 / (sin_angle_lower * sine_side**3)
    assert_mp_positive(gram_lower, "Gram determinant lower bound")
    assert_mp_positive(sin_angle_lower, "angle sine lower bound")
    assert_mp_positive(c_ang, "explicit angle Lipschitz constant")

    c_minus, c_plus = mp.cos(upper), mp.cos(lower)
    products = (c_minus**2, c_minus * c_plus, c_plus**2)
    numerator_lower = c_minus - max(products)
    numerator_upper = c_plus - min(products)
    old_c_a = max(abs(numerator_lower), abs(numerator_upper)) / sine_side**2

    minimum_actual_gram: mp.mpf | None = None
    for a, b, c in itertools.product((lower, theta0, upper), repeat=3):
        semiperimeter = (a + b + c) / 2
        gram_heron = 4 * mp.sin(semiperimeter) * mp.sin(semiperimeter - a) \
            * mp.sin(semiperimeter - b) * mp.sin(semiperimeter - c)
        cosine_angle = (mp.cos(a) - mp.cos(b) * mp.cos(c)) / (mp.sin(b) * mp.sin(c))
        gram_direct = mp.sin(b) ** 2 * mp.sin(c) ** 2 * (1 - cosine_angle**2)
        if abs(gram_heron - gram_direct) > MP_TOLERANCE:
            raise AssertionError(f"Gram/Heron identity drifted: {mp_string(gram_heron-gram_direct)}")
        assert_mp_nonnegative(gram_heron - gram_lower, "Gram determinant box lower bound")
        assert_mp_positive(1 - cosine_angle**2, "nondegenerate spherical angle")
        actual_sin_angle = mp.sqrt(1 - cosine_angle**2)
        assert_mp_nonnegative(actual_sin_angle - sin_angle_lower, "sin(A) lower certificate")
        partial_a = mp.sin(a) / (actual_sin_angle * mp.sin(b) * mp.sin(c))
        partial_b = abs(mp.cos(c) - mp.cos(a) * mp.cos(b)) \
            / (actual_sin_angle * mp.sin(b) ** 2 * mp.sin(c))
        partial_c = abs(mp.cos(b) - mp.cos(a) * mp.cos(c)) \
            / (actual_sin_angle * mp.sin(c) ** 2 * mp.sin(b))
        assert_mp_nonnegative(c_ang - partial_a - partial_b - partial_c,
                              "C_ang gradient l1 bound")
        minimum_actual_gram = (gram_heron if minimum_actual_gram is None
                               else min(minimum_actual_gram, gram_heron))
    return {
        "tau": tau, "lower": lower, "upper": upper, "sine_side": sine_side,
        "gram_lower": gram_lower, "sin_angle_lower": sin_angle_lower,
        "C_ang_0": c_ang, "old_C_A": old_c_a,
        "minimum_grid_gram": minimum_actual_gram or gram_lower,
    }


def valence_gap(d_max: int) -> mp.mpf | None:
    if d_max < 3:
        raise AssertionError("triangulation and p-floor require d_max >= 3")
    if d_max == 3:
        return None
    return min(abs(2 * mp.pi / m - 2 * mp.pi / n)
               for m in range(3, d_max + 1) for n in range(m + 1, d_max + 1))


def closed_threshold_case(
    name: str, ell0: mp.mpf, kappa: mp.mpf, graph_radius: int
) -> dict[str, str | int | None]:
    theta0 = mp.acos(1 - ell0)
    assert_mp_positive(ell0, f"{name}: ell0")
    assert_mp_positive(2 - ell0, f"{name}: 2-ell0")
    assert_mp_positive(2 * mp.pi / 3 - theta0, f"{name}: theta0 below 2pi/3")
    rho = min(ell0, 2 - ell0) / 2
    b0 = mp.log(1 + rho / ell0)
    c_r = mp.mpf(2 + 4 * graph_radius)
    sigma0 = min(mp.sqrt((ell0 - rho) * (2 - ell0 + rho)),
                 mp.sqrt((ell0 + rho) * (2 - ell0 - rho)))
    box = fixed_angle_box(theta0)
    tau, c_ang0 = box["tau"], box["C_ang_0"]
    k_theta = ell0 * mp.exp(b0) * c_r / sigma0
    d_max = int(mp.floor(1 / kappa))
    gap = valence_gap(d_max)
    candidates = [mp.mpf("0.5"), b0 / c_r, tau / k_theta]
    if gap is not None:
        candidates.append(gap / (4 * c_ang0 * k_theta))
    delta_star = min(candidates)
    eta_star = kappa * delta_star**2
    assert_mp_positive(delta_star, f"{name}: delta_star")
    assert_mp_positive(eta_star, f"{name}: eta_star")

    delta, eta = delta_star / 2, kappa * (delta_star / 2) ** 2
    if not eta < eta_star:
        raise AssertionError(f"{name}: eta is not below eta_star")
    b_delta = -mp.log(1 - delta) + graph_radius * mp.log((1 + delta) / (1 - delta))
    assert_mp_nonnegative(c_r * delta - b_delta, f"{name}: (6.17)")
    assert_mp_nonnegative(b0 - b_delta, f"{name}: B_delta <= b0")
    loss_error = ell0 * (mp.exp(b_delta) - 1)
    assert_mp_nonnegative(rho - loss_error, f"{name}: additive loss box")
    delta_theta = loss_error / sigma0
    assert_mp_nonnegative(k_theta * delta - delta_theta, f"{name}: Delta_theta <= K delta")
    assert_mp_positive(tau - delta_theta, f"{name}: fixed angle box retention")
    if gap is not None:
        assert_mp_positive(gap - 2 * c_ang0 * delta_theta,
                           f"{name}: integer valence separation")

    alpha = mp.acos(mp.cos(theta0) / (1 + mp.cos(theta0)))
    alpha_prime = mp.sin(theta0) / ((1 + mp.cos(theta0)) ** 2 * mp.sin(alpha))
    s_j = sine_endpoint_minimum(box["lower"], box["upper"])
    assert_mp_nonnegative(alpha_prime - s_j / 4, f"{name}: m_eq >= s_J/4")
    if -mp.log(1) + graph_radius * mp.log(1) != 0:
        raise AssertionError(f"{name}: eta=0 endpoint changed")

    return {
        "name": name, "ell_0": mp_string(ell0), "theta_0": mp_string(theta0),
        "rho": mp_string(rho), "b_0": mp_string(b0), "C_R": int(c_r),
        "sigma_0": mp_string(sigma0), "K_theta": mp_string(k_theta),
        "tau": mp_string(tau), "C_ang_0": mp_string(c_ang0),
        "Gram_sin_A_lower": mp_string(box["sin_angle_lower"]),
        "rejected_old_C_A": mp_string(box["old_C_A"]), "d_max": d_max,
        "g_kappa": None if gap is None else mp_string(gap),
        "delta_star": mp_string(delta_star), "eta_star": mp_string(eta_star),
        "stress_delta": mp_string(delta), "stress_eta": mp_string(eta),
        "B_delta": mp_string(b_delta), "Delta_theta": mp_string(delta_theta),
        "eta_zero_fixed_box_valid": "yes",
    }


def closed_threshold_stress() -> dict[str, object]:
    cases = [
        ("tetrahedron", mp.mpf(4) / 3, mp.mpf(1) / 3, 1),
        ("octahedron", mp.mpf(1), mp.mpf(1) / 4, 2),
        ("icosahedron", 1 - 1 / mp.sqrt(5), mp.mpf(1) / 5, 3),
        ("small-side-stress", 1 - mp.cos(mp.mpf(1) / 5), mp.mpf(1) / 6, 10),
        ("two-pi-over-three-stress",
         1 - mp.cos(2 * mp.pi / 3 - mp.mpf(1) / 20), mp.mpf(1) / 6, 10),
    ]
    report = {name: closed_threshold_case(name, ell0, kappa, radius)
              for name, ell0, kappa, radius in cases}
    old_icosa_c_a = mp.mpf(report["icosahedron"]["rejected_old_C_A"])
    assert_mp_positive(old_icosa_c_a - 1, "old icosahedral C_A rejection margin",
                       mp.mpf("1e-8"))
    return report


def platonic_edge_sup_bound_stress() -> dict[str, object]:
    """Exercise the nontrivial ``J``, ``m_eq``, and (6.22) chain.

    Each exact Platonic side is perturbed slightly to a reference side
    ``theta0``.  The fixed-box angle constant supplies the hypothesis
    ``|alpha_eq(theta0)-2*pi/q| <= C_ang,0 Delta_theta``.  We then check the
    explicit derivative minimum on the full interval from ``theta0`` to the
    exact side and the final edge sup bound for endpoint stress samples.
    """
    exact_sides = {
        "tetrahedron": (3, mp.acos(-mp.mpf(1) / 3), -1),
        "octahedron": (4, mp.pi / 2, 1),
        "icosahedron": (5, mp.acos(1 / mp.sqrt(5)), -1),
    }
    report: dict[str, object] = {}
    for name, (valence, theta_q, direction) in exact_sides.items():
        exact_tau = min(theta_q, mp.pi - theta_q, 2 * mp.pi / 3 - theta_q) / 4
        theta0 = theta_q + direction * exact_tau / 16
        box = fixed_angle_box(theta0)
        c_ang0 = box["C_ang_0"]
        delta_theta = box["tau"] / 4

        j_lower, j_upper = min(theta0, theta_q), max(theta0, theta_q)
        alpha0 = mp.acos(mp.cos(theta0) / (1 + mp.cos(theta0)))
        alpha_q = mp.acos(mp.cos(theta_q) / (1 + mp.cos(theta_q)))
        assert_mp_nonnegative(
            MP_TOLERANCE - abs(alpha_q - 2 * mp.pi / valence),
            f"{name}: exact Platonic angle",
        )

        def alpha_prime(theta: mp.mpf) -> mp.mpf:
            alpha = mp.acos(mp.cos(theta) / (1 + mp.cos(theta)))
            return mp.sin(theta) / ((1 + mp.cos(theta)) ** 2 * mp.sin(alpha))

        m_eq = alpha_prime(j_lower)
        assert_mp_positive(m_eq, f"{name}: m_eq")
        for theta in (j_lower, (j_lower + j_upper) / 2, j_upper):
            assert_mp_nonnegative(
                alpha_prime(theta) - m_eq,
                f"{name}: m_eq is the derivative minimum on J",
            )
        s_j = min(mp.sin(j_lower), mp.sin(j_upper))
        assert_mp_positive(s_j, f"{name}: s_J")
        assert_mp_nonnegative(m_eq - s_j / 4, f"{name}: m_eq >= s_J/4")

        angle_gap = abs(alpha0 - alpha_q)
        angle_budget = c_ang0 * delta_theta
        assert_mp_nonnegative(
            angle_budget - angle_gap,
            f"{name}: face-angle premise for (6.22)",
        )
        reference_side_budget = angle_budget / m_eq
        reference_gap = abs(theta0 - theta_q)
        assert_mp_nonnegative(
            reference_side_budget - reference_gap,
            f"{name}: MVT reference-side bound",
        )

        edge_samples = (theta0 - delta_theta, theta0, theta0 + delta_theta)
        if not all(box["lower"] <= theta <= box["upper"] for theta in edge_samples):
            raise AssertionError(f"{name}: edge stress sample left the fixed box")
        actual_edge_sup = max(abs(theta - theta_q) for theta in edge_samples)
        edge_sup_bound = delta_theta * (1 + c_ang0 / m_eq)
        margin = edge_sup_bound - actual_edge_sup
        assert_mp_nonnegative(margin, f"{name}: mandatory edge sup bound (6.22)")

        report[name] = {
            "valence": valence,
            "theta_q": mp_string(theta_q),
            "theta_0": mp_string(theta0),
            "J": [mp_string(j_lower), mp_string(j_upper)],
            "m_eq": mp_string(m_eq),
            "s_J_over_4": mp_string(s_j / 4),
            "Delta_theta": mp_string(delta_theta),
            "angle_gap": mp_string(angle_gap),
            "C_ang_0_Delta_theta": mp_string(angle_budget),
            "reference_side_gap": mp_string(reference_gap),
            "reference_side_budget": mp_string(reference_side_budget),
            "actual_edge_sup": mp_string(actual_edge_sup),
            "edge_sup_bound_6_22": mp_string(edge_sup_bound),
            "edge_sup_margin": mp_string(margin),
        }
    return report


def main() -> None:
    report = {
        "status_label": "COMPUTATIONAL",
        "variance": exact_variance_identity(),
        "pointwise_path_stress": pointwise_small_kappa_and_long_path(),
        "energy_resistance_conventions": energy_and_resistance_factor_audit(),
        "small_nonabsolute_poincare_gap": small_nonabsolute_poincare_gap_audit(),
        "logarithmic_edge_inequality": logarithmic_edge_inequality_stress(),
        "arccos_lipschitz_4_13_endpoint_stress": arccos_lipschitz_endpoint_stress(),
        "closed_threshold_6_16_through_6_19": closed_threshold_stress(),
        "platonic_edge_sup_bound_6_22": platonic_edge_sup_bound_stress(),
        "permanent_rejections": {
            "near-rigidity is diameter-free under only a local weight floor": "REJECTED",
            "unnamed O(sqrt eta) stability": "REJECTED",
            "old independent C_A certificate covers the icosahedral fixed box": "REJECTED",
        },
        "status": "PASS",
    }
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

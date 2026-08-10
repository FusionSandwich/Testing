"""Independent SymPy certificate for the manufactured transport fixture."""

from __future__ import annotations

import sympy as sp

from .manufactured import multigroup_exact_symbols, spatial_exact_symbols


def run_exact_audit() -> dict[str, str]:
    data = spatial_exact_symbols()
    operator = data["reference_operator"]
    discrete_operator = data["discrete_operator"]
    error = data["error"]
    residual = data["residual"]
    comparator_residual = data["comparator_residual"]
    streaming = data["streaming"]
    angular = data["discrete_angular"]
    symmetric_part = sp.simplify((operator + operator.T) / 2)
    assert operator * error == residual
    assert discrete_operator * error == comparator_residual
    assert data["response_error"] == data["response_estimator"] == sp.Rational(5, 3)
    assert data["comparator_response_estimator"] == sp.Rational(5, 3)
    assert data["error_squared"] == sp.Rational(26, 81)
    assert data["residual_squared"] == sp.Rational(784, 81)
    assert data["comparator_residual_squared"] == 4
    assert streaming * angular - angular * streaming == data["commutator"]
    assert data["commutator"] != sp.zeros(4)
    # Exact Sylvester certificate: H-(3/2)I is positive semidefinite because
    # all principal minors are nonnegative (eigenvalues are 0,1,4,5).
    shifted = symmetric_part - sp.Rational(3, 2) * sp.eye(4)
    principal_minors = []
    for mask in range(1, 1 << 4):
        indices = [index for index in range(4) if mask & (1 << index)]
        principal_minors.append(sp.factor(shifted.extract(indices, indices).det()))
    assert all(value >= 0 for value in principal_minors)
    assert sorted(symmetric_part.eigenvals().keys()) == [
        sp.Rational(3, 2),
        sp.Rational(5, 2),
        sp.Rational(11, 2),
        sp.Rational(13, 2),
    ]
    multigroup = multigroup_exact_symbols()
    assert multigroup["discrete_amplitude"] == sp.Matrix(
        [sp.Rational(1, 8), sp.Rational(3, 16)]
    )
    assert multigroup["target_amplitude"] == sp.Matrix(
        [sp.Rational(1, 32), sp.Rational(7, 96)]
    )
    assert multigroup["angular_error"] == sp.Matrix(
        [sp.Rational(3, 32), sp.Rational(11, 96)]
    )
    assert multigroup["low_group_response_error"] == sp.Rational(11, 96)
    assert multigroup["commutator"] == multigroup["expected_commutator"]
    assert multigroup["commutator"] != sp.zeros(2)
    assert multigroup["equal_kappa_commutator"] == sp.zeros(2)
    assert multigroup["changed_rate_amplitude"] == sp.Matrix(
        [sp.Rational(1, 16), sp.Rational(7, 24)]
    )
    assert multigroup["group_rate_error"] == sp.Matrix(
        [sp.Rational(-1, 16), sp.Rational(5, 48)]
    )
    return {
        "error_squared": str(data["error_squared"]),
        "residual_squared": str(data["residual_squared"]),
        "comparator_residual_squared": str(data["comparator_residual_squared"]),
        "response": str(data["response_error"]),
        "coercivity": str(data["coercivity"]),
        "commutator_rank": str(data["commutator"].rank()),
        "low_group_response_error": str(multigroup["low_group_response_error"]),
        "multigroup_commutator_rank": str(multigroup["commutator"].rank()),
    }


if __name__ == "__main__":
    print(run_exact_audit())
    print("P2B exact manufactured audit: PASS")

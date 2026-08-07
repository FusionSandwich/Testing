from __future__ import annotations

import numpy as np
import pytest

from pure_math.acceleration import (
    constrained_defect_correction,
    constrained_error_propagation_operator,
    constrained_low_inverse,
    defect_correction,
    error_propagation_operator,
    preconditioned_gmres,
    shellwise_contraction,
)
from pure_math.acceleration.audit import run_audit
from pure_math.acceleration.fixtures import commuting_shell_fixture


def test_exact_fixed_point_and_error_operator() -> None:
    fixture = commuting_shell_fixture()
    exact = np.linalg.solve(fixture.high, fixture.rhs)
    e = error_propagation_operator(fixture.high, fixture.optimized_low)
    update = exact + np.linalg.solve(
        fixture.optimized_low, fixture.rhs - fixture.high @ exact
    )
    assert np.linalg.norm(update - exact) < 1e-13
    arbitrary = np.linspace(-0.2, 0.5, len(exact))
    next_error = (
        arbitrary
        + np.linalg.solve(
            fixture.optimized_low,
            fixture.rhs - fixture.high @ arbitrary,
        )
        - exact
    )
    assert np.linalg.norm(next_error - e @ (arbitrary - exact)) < 1e-12


def test_shellwise_formula() -> None:
    fixture = commuting_shell_fixture()
    report = shellwise_contraction(fixture.shell_high, fixture.shell_optimized)
    assert np.allclose(report.factors, 1.0 - fixture.shell_high / fixture.shell_optimized)
    assert report.spectral_radius < 0.2


def test_defect_correction_converges() -> None:
    fixture = commuting_shell_fixture()
    result = defect_correction(
        fixture.high,
        fixture.rhs,
        fixture.optimized_low,
        rtol=1e-11,
        max_iterations=200,
    )
    assert result.converged
    assert np.linalg.norm(result.solution - np.linalg.solve(fixture.high, fixture.rhs)) < 1e-9


def test_constrained_correction_preserves_declared_conservation() -> None:
    fixture = commuting_shell_fixture()
    exact = np.linalg.solve(fixture.high, fixture.rhs)
    q = np.ones((1, len(exact)))
    perturbation = np.arange(len(exact), dtype=float)
    perturbation -= np.mean(perturbation)
    initial = exact + 0.04 * perturbation
    inverse = constrained_low_inverse(fixture.optimized_low, q)
    assert np.linalg.norm(q @ inverse) < 1e-11
    e = constrained_error_propagation_operator(
        fixture.high, fixture.optimized_low, q
    )
    assert np.linalg.norm(q @ (np.eye(len(exact)) - e)) < 1e-11
    result = constrained_defect_correction(
        fixture.high,
        fixture.rhs,
        fixture.optimized_low,
        q,
        initial=initial,
        rtol=1e-11,
        max_iterations=400,
    )
    assert result.converged
    assert np.linalg.norm(q @ (result.solution - initial)) < 1e-10
    assert np.linalg.norm(result.solution - exact) < 1e-8


def test_constrained_correction_rejects_incompatible_initial_state() -> None:
    fixture = commuting_shell_fixture()
    q = np.ones((1, len(fixture.rhs)))
    with pytest.raises(ValueError, match="conservation-incompatible"):
        constrained_defect_correction(
            fixture.high,
            fixture.rhs,
            fixture.optimized_low,
            q,
            initial=np.zeros_like(fixture.rhs),
        )


def test_gmres_uses_low_operator_only_as_preconditioner() -> None:
    fixture = commuting_shell_fixture()
    exact = np.linalg.solve(fixture.high, fixture.rhs)
    for low in (
        None,
        fixture.optimized_low,
        fixture.baseline_low,
        fixture.classical_low,
        fixture.poor_low,
    ):
        result = preconditioned_gmres(
            fixture.high,
            fixture.rhs,
            low_order=low,
            rtol=1e-11,
            restart=4,
            max_iterations=100,
        )
        assert result.converged
        assert np.linalg.norm(result.solution - exact) < 1e-9


def test_executable_audit() -> None:
    result = run_audit()
    assert result["status"] == "PASS"
    assert result["fixed_point_preserved"] is True
    assert result["conservation_constraint_preserved"] is True
    assert len(result["rows"]) == 4
    assert result["checks"]["higher_shell_failure_exposed"] is True

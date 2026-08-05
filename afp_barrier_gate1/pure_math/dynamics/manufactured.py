"""Exact manufactured angular and noncommuting spatial problems."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from numpy.typing import NDArray
from scipy import linalg
import sympy as sp

from .bounds import RESIDUAL_COMPONENTS, ResidualLedger
from .core import ModeErrorReport, resolvent_mode_error, semigroup_mode_error

FloatArray = NDArray[np.float64]


@dataclass(frozen=True)
class AngularManufactured:
    weights: FloatArray
    generator: FloatArray
    mode: FloatArray
    target_lambda: float
    nodes: FloatArray | None = None

    def transient(self, time: float) -> ModeErrorReport:
        return semigroup_mode_error(
            self.generator, self.weights, self.mode, self.target_lambda, time
        )

    def resolvent(self, alpha: float) -> ModeErrorReport:
        return resolvent_mode_error(
            self.generator, self.weights, self.mode, self.target_lambda, alpha
        )


def two_node_defect_fixture() -> AngularManufactured:
    """Return ``L=[[-1,1],[1,-1]]``, target ``-6``, and a unit H2 proxy.

    The weighted unit mode ``(1,-1)`` has actual eigenvalue ``-2`` and
    residual ``4u``.  Thus both exact errors and effectivities have closed
    forms and exercise nonzero (rather than equality-case) defects.
    """

    return AngularManufactured(
        np.asarray([0.5, 0.5]),
        np.asarray([[-1.0, 1.0], [1.0, -1.0]]),
        np.asarray([1.0, -1.0]),
        6.0,
    )


def two_node_alias_fixture() -> AngularManufactured:
    """Return the sharp constant-alias example for the semigroup estimate.

    The angular generator has eigenvalues ``0`` and ``-6`` while the sampled
    quadratic proxy ``(1,0)`` contains equal constant and ``-6`` components.
    Its residual is ``3(1,1)``.  Consequently the semigroup estimate is an
    equality for every positive time; this detects the forbidden assumption
    that a sampled continuum shell is automatically invariant.
    """

    return AngularManufactured(
        np.asarray([0.5, 0.5]),
        3.0 * np.asarray([[-1.0, 1.0], [1.0, -1.0]]),
        np.asarray([1.0, 0.0]),
        6.0,
        np.asarray([[1.0, 0.0, 0.0], [0.0, 1.0, 0.0]]),
    )


def tetrahedron_h1_exact_fixture() -> AngularManufactured:
    """Return the accepted tetrahedral K4 generator and one sampled H2 mode.

    With masses ``1/4`` and every conductance ``1/8``, the generator equals
    ``-2 I`` on the three-dimensional mean-zero space, which is exactly the
    sampled H2 quotient.  The selected mode is weighted-unit and has residual
    norm four against the continuum H2 eigenvalue six.
    """

    generator = np.full((4, 4), 0.5)
    np.fill_diagonal(generator, -1.5)
    nodes = np.asarray(
        [
            [1.0, 1.0, 1.0],
            [1.0, -1.0, -1.0],
            [-1.0, 1.0, -1.0],
            [-1.0, -1.0, 1.0],
        ]
    ) / np.sqrt(3.0)
    return AngularManufactured(
        np.full(4, 0.25),
        generator,
        np.sqrt(2.0) * np.asarray([1.0, -1.0, 0.0, 0.0]),
        6.0,
        nodes,
    )


# Backward-compatible descriptive name for the nonzero-defect two-node case.
two_node_angular_fixture = two_node_defect_fixture


def spatial_exact_symbols() -> dict[str, sp.Matrix | sp.Rational | sp.Expr]:
    """Build the exact rational 2-cell by 2-direction steady fixture."""

    streaming = sp.Matrix(
        [[1, 0, 0, 0], [0, 1, 0, -1], [-1, 0, 1, 0], [0, 0, 0, 1]]
    )

    def angular(rate: sp.Rational) -> sp.Matrix:
        block = sp.Matrix([[-rate, rate], [rate, -rate]])
        return sp.diag(block, block)

    sigma = sp.Rational(1)
    discrete_angular = angular(sp.Rational(1))
    reference_angular = angular(sp.Rational(2))
    discrete_operator = streaming + sigma * sp.eye(4) - discrete_angular
    reference_operator = streaming + sigma * sp.eye(4) - reference_angular
    exact_solution = sp.Matrix([1, 2, 3, 4])
    source = reference_operator * exact_solution
    computed_solution = discrete_operator.inv() * source
    error = exact_solution - computed_solution
    residual = (discrete_operator - reference_operator) * computed_solution
    comparator_residual = discrete_operator * exact_solution - source
    response = sp.Matrix([1, -1, 2, -2])
    adjoint = reference_operator.T.inv() * response
    comparator_adjoint = discrete_operator.T.inv() * response
    commutator = streaming * discrete_angular - discrete_angular * streaming
    return {
        "streaming": streaming,
        "discrete_angular": discrete_angular,
        "reference_angular": reference_angular,
        "discrete_operator": discrete_operator,
        "reference_operator": reference_operator,
        "exact_solution": exact_solution,
        "source": source,
        "computed_solution": computed_solution,
        "error": error,
        "residual": residual,
        "comparator_residual": comparator_residual,
        "response": response,
        "adjoint": adjoint,
        "comparator_adjoint": comparator_adjoint,
        "commutator": commutator,
        "coercivity": sp.Rational(3, 2),
        "error_squared": sp.simplify(error.dot(error)),
        "residual_squared": sp.simplify(residual.dot(residual)),
        "comparator_residual_squared": sp.simplify(
            comparator_residual.dot(comparator_residual)
        ),
        "response_error": sp.simplify(response.dot(error)),
        "response_estimator": sp.simplify(adjoint.dot(residual)),
        "comparator_response_estimator": sp.simplify(
            comparator_adjoint.dot(comparator_residual)
        ),
    }


@dataclass(frozen=True)
class SpatialManufactured:
    streaming: FloatArray
    discrete_angular: FloatArray
    reference_angular: FloatArray
    discrete_operator: FloatArray
    reference_operator: FloatArray
    exact_solution: FloatArray
    source: FloatArray
    computed_solution: FloatArray
    error: FloatArray
    residual: FloatArray
    comparator_residual: FloatArray
    commutator: FloatArray
    coercivity: float
    exact_error: float
    coercive_bound: float
    effectivity: float
    response: FloatArray
    adjoint: FloatArray
    comparator_adjoint: FloatArray
    response_error: float
    response_estimator: float
    ledger: ResidualLedger


def multigroup_exact_symbols() -> dict[str, sp.Matrix | sp.Rational]:
    """Exact two-group amplitude comparison at ``t=log(2)``.

    Group one transfers to group two at rate ``a``.  On an angular eigenmode
    with positive decay rate ``eta``, the amplitude generator is
    ``G - eta*diag(kappa)``.  The exact rational values below distinguish the
    angular-eigenvalue defect from an independent group-rate mutation.
    """

    def transfer(rate: sp.Rational) -> sp.Matrix:
        return sp.Matrix([[-rate, 0], [rate, 0]])

    def amplitudes(
        rate: sp.Rational,
        kappa_high: sp.Rational,
        kappa_low: sp.Rational,
        eta: sp.Rational,
    ) -> sp.Matrix:
        high_decay = rate + kappa_high * eta
        high = sp.Rational(1, 2) ** high_decay
        low = rate * (
            sp.Rational(1, 2) ** (kappa_low * eta) - high
        ) / (high_decay - kappa_low * eta)
        return sp.Matrix([sp.factor(high), sp.factor(low)])

    rate = sp.Rational(1)
    kappa = sp.diag(sp.Rational(2), sp.Rational(1))
    discrete_eta = sp.Rational(1)
    target_lambda = sp.Rational(2)
    group_transfer = transfer(rate)
    angular_diffusion = -discrete_eta * kappa
    commutator = group_transfer * angular_diffusion - angular_diffusion * group_transfer
    expected_commutator = sp.Matrix(
        2,
        2,
        lambda row, column: group_transfer[row, column]
        * (angular_diffusion[column, column] - angular_diffusion[row, row]),
    )
    equal_diffusion = -discrete_eta * sp.eye(2)
    equal_kappa_commutator = (
        group_transfer * equal_diffusion - equal_diffusion * group_transfer
    )
    discrete = amplitudes(rate, sp.Rational(2), sp.Rational(1), discrete_eta)
    target = amplitudes(rate, sp.Rational(2), sp.Rational(1), target_lambda)
    angular_error = discrete - target
    changed_rate = amplitudes(
        sp.Rational(2), sp.Rational(2), sp.Rational(1), discrete_eta
    )
    return {
        "group_transfer": group_transfer,
        "angular_diffusion": angular_diffusion,
        "commutator": commutator,
        "expected_commutator": expected_commutator,
        "equal_kappa_commutator": equal_kappa_commutator,
        "discrete_amplitude": discrete,
        "target_amplitude": target,
        "angular_error": angular_error,
        "low_group_response_error": angular_error[1],
        "changed_rate_amplitude": changed_rate,
        "group_rate_error": changed_rate - discrete,
    }


@dataclass(frozen=True)
class MultigroupManufactured:
    discrete_amplitude: FloatArray
    target_amplitude: FloatArray
    angular_error: FloatArray
    low_group_response_error: float
    commutator: FloatArray
    equal_kappa_commutator: FloatArray
    changed_rate_amplitude: FloatArray
    group_rate_error: FloatArray


def multigroup_manufactured_fixture() -> MultigroupManufactured:
    """Recompute the exact two-group fixture with SciPy matrix exponentials."""

    time = np.log(2.0)
    initial = np.asarray([1.0, 0.0])

    def generator(rate: float, eta: float, kappa: tuple[float, float]) -> FloatArray:
        transfer = np.asarray([[-rate, 0.0], [rate, 0.0]])
        return transfer - eta * np.diag(kappa)

    discrete_generator = generator(1.0, 1.0, (2.0, 1.0))
    target_generator = generator(1.0, 2.0, (2.0, 1.0))
    changed_rate_generator = generator(2.0, 1.0, (2.0, 1.0))
    discrete = linalg.expm(time * discrete_generator) @ initial
    target = linalg.expm(time * target_generator) @ initial
    changed_rate = linalg.expm(time * changed_rate_generator) @ initial
    transfer = np.asarray([[-1.0, 0.0], [1.0, 0.0]])
    diffusion = -np.diag([2.0, 1.0])
    equal_diffusion = -np.eye(2)
    commutator = transfer @ diffusion - diffusion @ transfer
    equal_commutator = transfer @ equal_diffusion - equal_diffusion @ transfer
    error = discrete - target
    return MultigroupManufactured(
        discrete,
        target,
        error,
        float(error[1]),
        commutator,
        equal_commutator,
        changed_rate,
        changed_rate - discrete,
    )


def spatial_manufactured_fixture() -> SpatialManufactured:
    """Return a floating audit view, recomputed independently by SciPy."""

    exact = spatial_exact_symbols()

    def array(name: str) -> FloatArray:
        return np.asarray(exact[name], dtype=float).reshape(np.asarray(exact[name]).shape)

    discrete_operator = array("discrete_operator")
    source = array("source").reshape(-1)
    exact_solution = array("exact_solution").reshape(-1)
    computed_solution = linalg.solve(discrete_operator, source, assume_a="gen")
    error = exact_solution - computed_solution
    residual = discrete_operator @ exact_solution - source
    reference_operator = array("reference_operator")
    comparator_residual = residual
    residual = (discrete_operator - reference_operator) @ computed_solution
    components = {name: np.zeros(4) for name in RESIDUAL_COMPONENTS}
    components["angular_generator"] = residual.copy()
    ledger = ResidualLedger.build(components)
    coercivity = float(exact["coercivity"])
    exact_error = float(np.linalg.norm(error, 2))
    bound = ledger.coercive_error_bound(coercivity)
    response = array("response").reshape(-1)
    adjoint = linalg.solve(reference_operator.T, response, assume_a="gen")
    comparator_adjoint = linalg.solve(discrete_operator.T, response, assume_a="gen")
    response_error = float(response @ error)
    response_estimator = float(adjoint @ residual)
    return SpatialManufactured(
        array("streaming"),
        array("discrete_angular"),
        array("reference_angular"),
        discrete_operator,
        reference_operator,
        exact_solution,
        source,
        computed_solution,
        error,
        residual,
        comparator_residual,
        array("commutator"),
        coercivity,
        exact_error,
        bound,
        bound / exact_error,
        response,
        adjoint,
        comparator_adjoint,
        response_error,
        response_estimator,
        ledger,
    )

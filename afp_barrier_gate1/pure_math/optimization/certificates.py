"""Solver-independent primal, dual, and Farkas certificate verification."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

import numpy as np
from numpy.typing import ArrayLike, NDArray
from scipy.optimize import linprog

from .model import AffineShell, DesignModel

FloatArray = NDArray[np.float64]


@dataclass(frozen=True)
class VerificationTolerance:
    absolute: float = 3e-6
    relative: float = 3e-6
    cone: float = 5e-6
    gap: float = 1e-5


@dataclass
class VerificationReport:
    passed: bool
    primal_passed: bool
    dual_passed: bool | None
    metrics: dict[str, float | int | bool | str | None] = field(default_factory=dict)
    failures: list[str] = field(default_factory=list)
    objective_interval: tuple[float, float] | None = None
    certificate_level: str = "tolerance_diagnostic"


@dataclass(frozen=True)
class FarkasCertificate:
    equality_field: FloatArray
    rate_field: FloatArray | None = None
    label: str = "numerical Farkas ray"


@dataclass(frozen=True)
class ConicInfeasibilityCertificate:
    """Ray for fixed-rate plus fixed-defect SDP feasibility.

    The normalization is the original raw cap
    ``H gamma <= rate_cap * w``.  The cross block occurs with factor two in
    both stationarity and strict separation.
    """

    equality_field: FloatArray
    rate_field: FloatArray
    positivity_field: FloatArray
    psd_field: FloatArray
    rate_cap: float
    defect_cap: float
    degree: int = 2
    label: str = "fixed-rate/fixed-defect SDP infeasibility ray"


def _finite_value(value: Any) -> bool:
    if value is None:
        return True
    if isinstance(value, (list, tuple)):
        return all(_finite_value(item) for item in value)
    try:
        return bool(np.all(np.isfinite(np.asarray(value, dtype=float))))
    except (TypeError, ValueError):
        return False


def _valid_tolerance(tolerance: VerificationTolerance) -> bool:
    values = np.asarray([
        tolerance.absolute, tolerance.relative, tolerance.cone, tolerance.gap,
    ], dtype=float)
    return bool(np.all(np.isfinite(values)) and np.all(values >= 0))


def _scale_residual(residual: ArrayLike, scale: float) -> float:
    return float(np.linalg.norm(np.asarray(residual, dtype=float).reshape(-1), ord=np.inf) / max(1.0, scale))


def _cone_minimum(matrix: FloatArray) -> float:
    return float(np.min(np.linalg.eigvalsh((matrix + matrix.T) / 2.0)))


def _constraint_duals(result: Any) -> tuple[FloatArray, FloatArray, FloatArray]:
    graph = result.metadata["model_graph"] if "model_graph" in result.metadata else None
    y = np.asarray(result.duals.get("exactness"), dtype=float).reshape(-1)
    q = np.asarray(result.duals.get("positivity"), dtype=float).reshape(-1)
    z = np.asarray(result.duals.get("rate"), dtype=float).reshape(-1)
    if graph is not None and (len(y), len(q), len(z)) != (3 * graph.node_count, graph.edge_count, graph.node_count):
        raise ValueError("common dual shape mismatch")
    return y, q, z


def _affine_gradient(affine: AffineShell, multiplier: FloatArray) -> FloatArray:
    return np.einsum("enr,nr->e", affine.edge_terms, multiplier)


def _response_values(model: DesignModel, result: Any) -> list[FloatArray]:
    handles = result.metadata["handles"]
    assert result.gamma is not None
    return [affine.evaluate(result.gamma) for affine in handles["affines"]]


def _true_objective(model: DesignModel, result: Any) -> float:
    request = result.request
    gamma = np.asarray(result.gamma, dtype=float)
    handles = result.metadata["handles"]
    values = _response_values(model, result)
    if request.kind == "min_defect":
        return float(np.linalg.svd(values[0], compute_uv=False)[0])
    if request.kind == "min_rate":
        return float(np.max(model.graph.rates(gamma)))
    if request.kind == "frobenius":
        value = 0.5 * float(np.sum(values[0] ** 2))
        if request.group_penalty_weight:
            value += request.group_penalty_weight * sum(
                float(np.linalg.norm(gamma[list(group)])) for group in request.edge_groups
            )
        return value
    if request.kind == "mode_minimax":
        assert request.modes is not None
        return max(float(np.linalg.norm(values[0] @ request.modes[:, k])) for k in range(request.modes.shape[1]))
    if request.kind == "scalar_minimax":
        assert request.modes is not None and request.scalar_outputs is not None
        return max(abs(float(request.scalar_outputs[:, k] @ values[0] @ request.modes[:, k])) for k in range(request.modes.shape[1]))
    if request.kind == "multi_shell":
        weights = handles["shell_objective_weights"]
        if request.metric == "frobenius":
            return sum(0.5 * weight * float(np.sum(value**2)) for weight, value in zip(weights, values, strict=True))
        return max(weight * float(np.linalg.svd(value, compute_uv=False)[0]) for weight, value in zip(weights, values, strict=True))
    if request.kind == "response":
        weights = handles["response_weights"]
        if request.metric == "frobenius":
            return sum(0.5 * weight * float(np.sum(value**2)) for weight, value in zip(weights, values, strict=True))
        if request.metric == "spectral_max":
            return max(weight * float(np.linalg.svd(value, compute_uv=False)[0]) for weight, value in zip(weights, values, strict=True))
        if request.metric == "column_max":
            return max(
                weight * float(np.linalg.norm(value[:, k]))
                for weight, value in zip(weights, values, strict=True)
                for k in range(value.shape[1])
            )
        return max(weight * abs(float(value[0, 0])) for weight, value in zip(weights, values, strict=True))
    raise ValueError(request.kind)


def _primal_report(
    model: DesignModel, result: Any, tolerance: VerificationTolerance,
) -> tuple[bool, dict[str, float | int | bool | str | None], list[str]]:
    graph, request = model.graph, result.request
    gamma = np.asarray(result.gamma, dtype=float)
    failures: list[str] = []
    metrics: dict[str, float | int | bool | str | None] = {}
    exactness = graph.h1_matrix @ gamma - graph.h1_rhs
    exact_scale = 1.0 + np.linalg.norm(graph.h1_matrix, ord=np.inf) * np.linalg.norm(gamma, ord=np.inf) + np.linalg.norm(graph.h1_rhs, ord=np.inf)
    metrics["h1_residual_inf"] = float(np.linalg.norm(exactness, ord=np.inf))
    metrics["h1_residual_scaled"] = _scale_residual(exactness, exact_scale)
    metrics["gamma_min"] = float(np.min(gamma))
    raw_rate = graph.endpoint_incidence @ gamma
    rates = raw_rate / graph.weights
    cap = result.rate_bound
    metrics["rate_max"] = float(np.max(rates))
    metrics["rate_bound"] = None if cap is None else float(cap)
    metrics["rate_raw_violation"] = (
        0.0 if cap is None else float(max(0.0, np.max(raw_rate - cap * graph.weights)))
    )
    # Feasibility is a directed-rate statement.  Checking only the raw
    # conductance slack would become arbitrarily weak when a quadrature mass
    # is tiny, so the controlling diagnostic is divided by w_i.
    metrics["rate_violation"] = (
        0.0 if cap is None else float(max(0.0, np.max(rates - cap)))
    )
    metrics["rate_violation_scaled"] = (
        0.0 if cap is None else metrics["rate_violation"] / max(1.0, abs(float(cap)))
    )
    generator = graph.generator(gamma)
    metrics["h0_residual"] = float(np.linalg.norm(generator @ np.ones(graph.node_count), ord=np.inf))
    metrics["coordinate_residual"] = float(np.linalg.norm(generator @ graph.nodes + 2.0 * graph.nodes, ord=np.inf))
    w = np.diag(graph.weights)
    metrics["reversibility_residual"] = float(np.linalg.norm(w @ generator - generator.T @ w, ord=np.inf))
    metrics["loss_identity_residual"] = abs(float(graph.losses @ gamma - graph.total_mass))
    true_objective = _true_objective(model, result)
    metrics["objective_recomputed"] = true_objective
    metrics["solver_objective"] = result.objective
    objective_error = abs(true_objective - float(result.objective)) / max(1.0, abs(true_objective))
    metrics["objective_relative_error"] = objective_error
    if result.epigraph is not None:
        metrics["epigraph_slack"] = float(result.epigraph - true_objective)
    if request.kind == "min_rate":
        defect = model.defect(gamma, request.degree)
        metrics["defect"] = defect
        metrics["defect_cap_violation"] = max(0.0, defect - float(request.defect_cap))

    # Reconstruct every explicit primal cone slack from the frozen affine
    # arrays.  Solver status and a recomputed objective are not substitutes
    # for checking the LMI/SOC/LP epigraph actually used by the program.
    handles = result.metadata["handles"]
    if "psd" in handles:
        affines = handles["affines"]
        scales = handles.get("psd_scales", [1.0] * len(affines))
        psd_minima: list[float] = []
        for affine, scale in zip(affines, scales, strict=True):
            bound = (
                float(request.defect_cap)
                if request.kind == "min_rate"
                else float(result.epigraph)
            )
            value = float(scale) * affine.evaluate(gamma)
            block = np.block([
                [bound * np.eye(value.shape[0]), value],
                [value.T, bound * np.eye(value.shape[1])],
            ])
            psd_minima.append(_cone_minimum(block))
        metrics["primal_psd_block_count"] = len(psd_minima)
        metrics["primal_psd_min_eigenvalue"] = min(psd_minima)
        if metrics["primal_psd_min_eigenvalue"] < -tolerance.cone:
            failures.append("primal PSD cone")
    if "soc" in handles:
        assert result.epigraph is not None
        margins = [
            float(result.epigraph) - float(np.linalg.norm(constant + gamma @ terms))
            for constant, terms in handles["mode_affines"]
        ]
        metrics["primal_soc_block_count"] = len(margins)
        metrics["primal_soc_min_margin"] = min(margins)
        if metrics["primal_soc_min_margin"] < -tolerance.cone:
            failures.append("primal SOC cone")
    if "upper" in handles:
        assert result.epigraph is not None
        margins = [
            float(result.epigraph) - abs(float(constant + terms @ gamma))
            for constant, terms in handles["scalar_affines"]
        ]
        metrics["primal_lp_block_count"] = len(margins)
        metrics["primal_lp_min_margin"] = min(margins)
        if metrics["primal_lp_min_margin"] < -tolerance.cone:
            failures.append("primal LP epigraph")
    checks = {
        "negative conductance": metrics["gamma_min"] < -tolerance.cone,
        "H1 residual": metrics["h1_residual_scaled"] > tolerance.relative,
        "rate cap": metrics["rate_violation"]
        > tolerance.absolute + tolerance.relative * max(1.0, 0.0 if cap is None else abs(float(cap))),
        "H0 residual": metrics["h0_residual"] > tolerance.absolute,
        "coordinate residual": metrics["coordinate_residual"] > tolerance.absolute,
        "reversibility residual": metrics["reversibility_residual"] > tolerance.absolute,
        "fixed loss identity": metrics["loss_identity_residual"] > tolerance.absolute * max(1.0, graph.total_mass),
        "objective recomputation": objective_error > 2e-5,
    }
    if request.kind == "min_rate" and metrics["defect_cap_violation"] > tolerance.cone:
        checks["defect cap"] = True
    for label, failed in checks.items():
        if failed:
            failures.append(label)
    return not failures, metrics, failures


def _common_dual_terms(model: DesignModel, result: Any) -> tuple[FloatArray, FloatArray, FloatArray, FloatArray, float]:
    graph = model.graph
    y, q, z = _constraint_duals(result)
    common_stationarity = graph.h1_matrix.T @ y + graph.endpoint_incidence.T @ z - q
    cap = float(result.rate_bound)
    common_objective = -float(graph.h1_rhs @ y) - cap * float(graph.weights @ z)
    return y, q, z, common_stationarity, common_objective


def _soc_dual(value: Any) -> tuple[float, FloatArray]:
    if not isinstance(value, list) or len(value) != 2:
        raise ValueError("unexpected SOC dual representation")
    alpha = float(np.asarray(value[0]).reshape(-1)[0])
    vector = np.asarray(value[1], dtype=float).reshape(-1)
    return alpha, vector


def _dual_report(
    model: DesignModel, result: Any, tolerance: VerificationTolerance,
) -> tuple[bool | None, dict[str, float | bool | None], list[str], float | None]:
    request, graph = result.request, model.graph
    handles = result.metadata["handles"]
    failures: list[str] = []
    metrics: dict[str, float | bool | None] = {}
    if any(result.duals.get(key) is None for key in ("exactness", "positivity", "rate")):
        return None, {"dual_available": False}, ["common dual variables unavailable"], None
    y, q, z, stationarity, dual_objective = _common_dual_terms(model, result)
    metrics["dual_available"] = True
    metrics["dual_nonnegative_min"] = float(min(np.min(q), np.min(z)))
    conductance_products = q * np.asarray(result.gamma)
    complementarity = float(np.sum(np.abs(conductance_products)))
    rate_slack = graph.endpoint_incidence @ np.asarray(result.gamma) - float(result.rate_bound) * graph.weights
    rate_products = z * rate_slack
    complementarity += float(np.sum(np.abs(rate_products)))
    metrics["conductance_complementarity_max"] = float(
        np.max(np.abs(conductance_products))
    )
    metrics["rate_complementarity_max"] = float(np.max(np.abs(rate_products)))

    if request.kind in {"min_defect", "min_rate"} or (
        request.kind == "multi_shell" and request.metric == "spectral_max"
    ) or (request.kind == "response" and request.metric == "spectral_max"):
        matrices = result.duals.get("psd")
        if not matrices or any(matrix is None for matrix in matrices):
            return None, {"dual_available": False}, ["PSD dual unavailable"], None
        affines = handles["affines"]
        scales = handles.get("psd_scales", [1.0] * len(affines))
        trace_sum = 0.0
        psd_min = float("inf")
        psd_symmetry_max = 0.0
        cross_constant = 0.0
        psd_complementarity = 0.0
        gamma_term = np.zeros(graph.edge_count)
        for matrix, affine, scale in zip(matrices, affines, scales, strict=True):
            zmat = np.asarray(matrix, dtype=float)
            symmetry_error = float(np.linalg.norm(zmat - zmat.T, ord=np.inf))
            symmetry_scale = max(1.0, float(np.linalg.norm(zmat, ord=np.inf)))
            psd_symmetry_max = max(psd_symmetry_max, symmetry_error / symmetry_scale)
            n = affine.constant.shape[0]
            cross = zmat[:n, n:]
            trace_sum += float(np.trace(zmat[:n, :n]) + np.trace(zmat[n:, n:]))
            psd_min = min(psd_min, _cone_minimum(zmat))
            cross_constant += -2.0 * scale * float(np.sum(cross * affine.constant))
            gamma_term += -2.0 * scale * np.asarray([
                float(np.sum(cross * term)) for term in affine.edge_terms
            ])
            bound = float(request.defect_cap) if request.kind == "min_rate" else float(result.epigraph)
            block = np.block([
                [bound * np.eye(affine.constant.shape[0]), scale * affine.evaluate(result.gamma)],
                [scale * affine.evaluate(result.gamma).T, bound * np.eye(affine.constant.shape[1])],
            ])
            psd_complementarity += abs(float(np.sum(zmat * block)))
        stationarity += gamma_term
        if request.kind == "min_rate":
            metrics["rate_dual_normalization"] = float(graph.weights @ z)
            dual_objective = (
                -float(graph.h1_rhs @ y)
                - float(request.defect_cap) * trace_sum
                + cross_constant
            )
            if abs(float(graph.weights @ z) - 1.0) > tolerance.relative:
                failures.append("rate-dual normalization")
        else:
            metrics["psd_trace_normalization"] = trace_sum
            dual_objective += cross_constant
            if abs(trace_sum - 1.0) > tolerance.relative * max(1.0, len(matrices)):
                failures.append("PSD trace normalization")
        metrics["psd_dual_min_eigenvalue"] = psd_min
        metrics["psd_dual_symmetry_error_scaled"] = psd_symmetry_max
        metrics["psd_complementarity"] = psd_complementarity
        complementarity += psd_complementarity
        if psd_min < -tolerance.cone:
            failures.append("PSD dual cone")
        if psd_symmetry_max > tolerance.relative:
            failures.append("PSD dual symmetry")
    elif request.kind in {"frobenius", "multi_shell"} or (
        request.kind == "response" and request.metric == "frobenius"
    ):
        affines = handles["affines"]
        values = _response_values(model, result)
        weights = handles.get(
            "shell_objective_weights",
            handles.get("response_weights", [1.0] * len(affines)),
        )
        dual_objective_extra = 0.0
        for affine, value, weight in zip(affines, values, weights, strict=True):
            eta = weight * value
            stationarity += _affine_gradient(affine, eta)
            dual_objective_extra += float(np.sum(eta * affine.constant)) - 0.5 * float(np.sum(eta**2)) / weight
        dual_objective += dual_objective_extra
        if request.kind == "frobenius" and request.group_penalty_weight > 0:
            subgradient = np.zeros(graph.edge_count)
            grouped: set[int] = set()
            group_violation = 0.0
            threshold = tolerance.cone * max(1.0, np.linalg.norm(np.asarray(result.gamma), ord=np.inf))
            for group_tuple in request.edge_groups:
                group = np.asarray(group_tuple, dtype=int)
                grouped.update(map(int, group))
                values = np.asarray(result.gamma)[group]
                norm = float(np.linalg.norm(values))
                if norm > threshold:
                    subgradient[group] = request.group_penalty_weight * values / norm
                else:
                    required = -stationarity[group]
                    group_violation = max(
                        group_violation,
                        float(np.linalg.norm(required) - request.group_penalty_weight),
                    )
                    subgradient[group] = required
            stationarity += subgradient
            metrics["group_zero_threshold"] = threshold
            metrics["group_subgradient_cone_violation"] = max(0.0, group_violation)
            metrics["grouped_edge_count"] = len(grouped)
            if group_violation > tolerance.cone:
                failures.append("group-norm subgradient cone")
    elif request.kind == "mode_minimax" or (
        request.kind == "response" and request.metric == "column_max"
    ):
        soc_duals = result.duals.get("soc")
        if not soc_duals or any(value is None for value in soc_duals):
            return None, {"dual_available": False}, ["SOC dual unavailable"], None
        alpha_sum = 0.0
        cone_violation = 0.0
        soc_comp = 0.0
        for value, (constant, terms) in zip(soc_duals, handles["mode_affines"], strict=True):
            alpha, vector = _soc_dual(value)
            alpha_sum += alpha
            cone_violation = max(cone_violation, np.linalg.norm(vector) - alpha)
            stationarity -= terms @ vector
            dual_objective -= float(vector @ constant)
            sample = constant + np.asarray(result.gamma) @ terms
            soc_comp += abs(alpha * float(result.epigraph) + float(vector @ sample))
        metrics["soc_alpha_sum"] = alpha_sum
        metrics["soc_dual_violation"] = cone_violation
        metrics["soc_complementarity"] = soc_comp
        complementarity += soc_comp
        if abs(alpha_sum - 1.0) > tolerance.relative:
            failures.append("SOC epigraph normalization")
        if cone_violation > tolerance.cone:
            failures.append("SOC dual cone")
    elif request.kind == "scalar_minimax" or (
        request.kind == "response" and request.metric == "scalar_max"
    ):
        upper, lower = result.duals.get("upper"), result.duals.get("lower")
        if not upper or not lower or any(value is None for value in upper + lower):
            return None, {"dual_available": False}, ["LP epigraph dual unavailable"], None
        normalization = 0.0
        lp_comp = 0.0
        lp_dual_min = float("inf")
        for up_raw, low_raw, (constant, terms) in zip(upper, lower, handles["scalar_affines"], strict=True):
            up = float(np.asarray(up_raw).reshape(-1)[0])
            low = float(np.asarray(low_raw).reshape(-1)[0])
            lp_dual_min = min(lp_dual_min, up, low)
            normalization += up + low
            difference = up - low
            stationarity += difference * terms
            dual_objective += difference * constant
            sample = constant + float(terms @ np.asarray(result.gamma))
            lp_comp += abs(up * (sample - float(result.epigraph))) + abs(low * (-sample - float(result.epigraph)))
        metrics["lp_epigraph_normalization"] = normalization
        metrics["lp_dual_nonnegative_min"] = lp_dual_min
        metrics["lp_complementarity"] = lp_comp
        complementarity += lp_comp
        if abs(normalization - 1.0) > tolerance.relative:
            failures.append("LP epigraph normalization")
        if lp_dual_min < -tolerance.cone:
            failures.append("LP dual cone")
    else:
        return None, {"dual_available": False}, ["unsupported dual verifier branch"], None

    stationarity_scaled = _scale_residual(
        stationarity,
        1.0 + np.linalg.norm(graph.h1_matrix.T, ord=np.inf) * np.linalg.norm(y, ord=np.inf)
        + np.linalg.norm(graph.endpoint_incidence.T, ord=np.inf) * np.linalg.norm(z, ord=np.inf)
        + np.linalg.norm(q, ord=np.inf),
    )
    metrics["dual_stationarity_inf"] = float(np.linalg.norm(stationarity, ord=np.inf))
    metrics["dual_stationarity_scaled"] = stationarity_scaled
    metrics["dual_objective"] = dual_objective
    metrics["complementarity_abs"] = complementarity
    if metrics["dual_nonnegative_min"] < -tolerance.cone:
        failures.append("negative inequality dual")
    if stationarity_scaled > tolerance.relative * 3:
        failures.append("dual stationarity")
    if complementarity > tolerance.gap * max(1.0, abs(float(result.objective))):
        failures.append("complementarity")
    gap = float(result.objective) - dual_objective
    metrics["primal_dual_gap"] = gap
    if gap < -tolerance.gap * max(1.0, abs(float(result.objective))) or abs(gap) > 5 * tolerance.gap * max(1.0, abs(float(result.objective))):
        failures.append("primal-dual gap")
    return not failures, metrics, failures, dual_objective


def verify_result(
    model: DesignModel,
    result: Any,
    tolerance: VerificationTolerance | None = None,
) -> VerificationReport:
    """Recompute a candidate without consulting the solver status."""
    tol = tolerance or VerificationTolerance()
    if not _valid_tolerance(tol):
        return VerificationReport(False, False, None, failures=["invalid verification tolerance"])
    if result.gamma is None or result.objective is None:
        return VerificationReport(False, False, None, failures=["no finite primal candidate"])
    gamma = np.asarray(result.gamma, dtype=float)
    if gamma.shape != (model.graph.edge_count,) or not _finite_value(gamma):
        return VerificationReport(False, False, None, failures=["nonfinite or malformed primal conductance"])
    if not np.isfinite(float(result.objective)):
        return VerificationReport(False, False, None, failures=["nonfinite primal objective"])
    if result.rate_bound is None or not np.isfinite(float(result.rate_bound)):
        return VerificationReport(False, False, None, failures=["nonfinite rate bound"])
    if result.epigraph is not None and not np.isfinite(float(result.epigraph)):
        return VerificationReport(False, False, None, failures=["nonfinite epigraph"])
    if not all(_finite_value(value) for value in result.duals.values()):
        return VerificationReport(False, False, None, failures=["nonfinite dual field"])
    # Recompile the declared request without solving it.  The verifier uses
    # these fresh request-bound affine arrays, not mutable handles left by a
    # previous solve, so a certificate cannot be relabeled with a new cap,
    # target, shell weight, or response map.
    try:
        from .programs import _compile_problem

        _, _, bound_handles = _compile_problem(model, result.request)
    except (AssertionError, KeyError, TypeError, ValueError) as exc:
        return VerificationReport(
            False, False, None,
            failures=[f"invalid declared request: {type(exc).__name__}: {exc}"],
        )
    if result.metadata.get("problem_class") != bound_handles.get("problem_class"):
        return VerificationReport(False, False, None, failures=["problem-class binding mismatch"])
    cap_scale = max(1.0, abs(float(result.rate_bound)))
    cap_tolerance = tol.absolute + tol.relative * cap_scale
    if result.request.kind == "min_rate":
        if abs(float(result.rate_bound) - float(result.objective)) > cap_tolerance:
            return VerificationReport(False, False, None, failures=["optimized-rate binding mismatch"])
    else:
        declared_cap = float(result.request.rate_cap)
        if abs(float(result.rate_bound) - declared_cap) > cap_tolerance:
            return VerificationReport(False, False, None, failures=["fixed-rate binding mismatch"])
    if ("epigraph" in bound_handles) != (result.epigraph is not None):
        return VerificationReport(False, False, None, failures=["epigraph binding mismatch"])
    result.metadata["handles"] = bound_handles
    result.metadata["model_graph"] = model.graph
    try:
        primal_ok, primal_metrics, primal_failures = _primal_report(model, result, tol)
        dual_ok, dual_metrics, dual_failures, dual_objective = _dual_report(model, result, tol)
    except (IndexError, TypeError, ValueError, np.linalg.LinAlgError) as exc:
        return VerificationReport(
            False, False, False,
            failures=[f"malformed primal/dual data: {type(exc).__name__}: {exc}"],
        )
    metrics = {**primal_metrics, **dual_metrics}
    failures = primal_failures + ([] if dual_ok is None else dual_failures)
    interval = None
    if dual_objective is not None:
        slack = tol.gap * max(1.0, abs(float(result.objective)))
        interval = (dual_objective - slack, float(result.objective) + slack)
    # A formulation whose solver does not export its dual is reported
    # honestly; the primal candidate may pass but is not certified complete.
    passed = primal_ok and dual_ok is True
    if dual_ok is None:
        failures.extend(dual_failures)
    return VerificationReport(
        passed, primal_ok, dual_ok, metrics, failures, interval,
        "tolerance_diagnostic",
    )


def verify_farkas_certificate(
    model: DesignModel,
    certificate: FarkasCertificate,
    *,
    rate_cap: float | None = None,
    tolerance: VerificationTolerance | None = None,
) -> VerificationReport:
    tol = tolerance or VerificationTolerance()
    graph = model.graph
    y = np.asarray(certificate.equality_field, dtype=float)
    if not _valid_tolerance(tol):
        return VerificationReport(False, False, True, failures=["invalid verification tolerance"])
    if y.shape != (3 * graph.node_count,):
        return VerificationReport(False, False, True, failures=["Farkas equality field shape"])
    if not _finite_value(y):
        return VerificationReport(False, False, True, failures=["nonfinite Farkas equality field"])
    if rate_cap is None:
        edge_work = graph.h1_matrix.T @ y
        rhs_work = float(graph.h1_rhs @ y)
        rate_min = 0.0
    else:
        if not np.isfinite(float(rate_cap)) or float(rate_cap) < 0:
            return VerificationReport(False, False, True, failures=["invalid Farkas rate cap"])
        if certificate.rate_field is None:
            return VerificationReport(False, False, True, failures=["missing Farkas rate field"])
        z = np.asarray(certificate.rate_field, dtype=float)
        if z.shape != (graph.node_count,):
            return VerificationReport(False, False, True, failures=["Farkas rate field shape"])
        if not _finite_value(z):
            return VerificationReport(False, False, True, failures=["nonfinite Farkas rate field"])
        edge_work = graph.h1_matrix.T @ y + graph.endpoint_incidence.T @ z
        rhs_work = float(graph.h1_rhs @ y + rate_cap * graph.weights @ z)
        rate_min = float(np.min(z))
    edge_min = float(np.min(edge_work))
    scale = 1.0 + np.linalg.norm(y, ord=np.inf)
    separation = -rhs_work / scale
    failures: list[str] = []
    if edge_min < -tol.cone * scale:
        failures.append("negative Farkas edge work")
    if rate_min < -tol.cone * scale:
        failures.append("negative Farkas slack-field work")
    if rhs_work >= -tol.absolute * scale:
        failures.append("Farkas separation is not strict")
    metrics: dict[str, float | int | bool | str | None] = {
        "edge_work_min": edge_min,
        "rate_field_min": rate_min,
        "rhs_work": rhs_work,
        "normalized_separation": separation,
        "label": certificate.label,
    }
    return VerificationReport(not failures, False, True, metrics, failures)


def find_farkas_certificate(
    model: DesignModel,
    *,
    rate_cap: float | None = None,
    separation_tolerance: float = 1e-8,
) -> FarkasCertificate | None:
    """Find a bounded representative of a homogeneous Farkas ray by LP."""
    graph = model.graph
    p, n = 3 * graph.node_count, graph.node_count
    if rate_cap is None:
        objective = graph.h1_rhs.copy()
        inequality = -graph.h1_matrix.T
        bounds = [(-1.0, 1.0)] * p
    else:
        objective = np.concatenate([graph.h1_rhs, rate_cap * graph.weights])
        inequality = -np.column_stack([graph.h1_matrix.T, graph.endpoint_incidence.T])
        bounds = [(-1.0, 1.0)] * p + [(0.0, 1.0)] * n
    outcome = linprog(
        objective,
        A_ub=inequality,
        b_ub=np.zeros(graph.edge_count),
        bounds=bounds,
        method="highs",
    )
    if not outcome.success or outcome.fun >= -separation_tolerance:
        return None
    if rate_cap is None:
        return FarkasCertificate(np.asarray(outcome.x, dtype=float), None, "HiGHS bounded Farkas ray")
    return FarkasCertificate(
        np.asarray(outcome.x[:p], dtype=float), np.asarray(outcome.x[p:], dtype=float),
        "HiGHS bounded exactness-plus-rate Farkas ray",
    )


def verify_conic_infeasibility_certificate(
    model: DesignModel,
    certificate: ConicInfeasibilityCertificate,
    *,
    tolerance: VerificationTolerance | None = None,
) -> VerificationReport:
    """Verify a strict separating ray for an infeasible capped SDP."""
    tol = tolerance or VerificationTolerance()
    graph = model.graph
    if not _valid_tolerance(tol):
        return VerificationReport(False, False, True, failures=["invalid verification tolerance"])
    affine = model.shell(certificate.degree)
    y = np.asarray(certificate.equality_field, dtype=float)
    z = np.asarray(certificate.rate_field, dtype=float)
    q = np.asarray(certificate.positivity_field, dtype=float)
    zmat = np.asarray(certificate.psd_field, dtype=float)
    expected = (graph.node_count + affine.shell.rank,) * 2
    failures: list[str] = []
    if y.shape != (3 * graph.node_count,):
        failures.append("conic ray equality-field shape")
    if z.shape != (graph.node_count,):
        failures.append("conic ray rate-field shape")
    if q.shape != (graph.edge_count,):
        failures.append("conic ray positivity-field shape")
    if zmat.shape != expected:
        failures.append("conic ray PSD-field shape")
    if failures:
        return VerificationReport(False, False, True, failures=failures)
    if not all(_finite_value(value) for value in (y, z, q, zmat)):
        return VerificationReport(False, False, True, failures=["nonfinite conic ray field"])
    if (
        not np.isfinite(float(certificate.rate_cap))
        or not np.isfinite(float(certificate.defect_cap))
        or certificate.rate_cap <= 0
        or certificate.defect_cap <= 0
    ):
        return VerificationReport(False, False, True, failures=["invalid conic ray cap"])
    symmetry_error = float(np.linalg.norm(zmat - zmat.T, ord=np.inf))
    symmetry_scale = max(1.0, float(np.linalg.norm(zmat, ord=np.inf)))
    if symmetry_error > tol.relative * symmetry_scale:
        failures.append("conic ray PSD field is not symmetric")
    n = graph.node_count
    cross = zmat[:n, n:]
    derivative = np.asarray([float(np.sum(cross * term)) for term in affine.edge_terms])
    stationarity = (
        graph.h1_matrix.T @ y + graph.endpoint_incidence.T @ z - q
        - 2.0 * derivative
    )
    stationarity_scaled = _scale_residual(
        stationarity,
        1.0 + np.linalg.norm(y, ord=np.inf) + np.linalg.norm(z, ord=np.inf)
        + np.linalg.norm(q, ord=np.inf) + np.linalg.norm(zmat, ord=np.inf),
    )
    psd_min = _cone_minimum(zmat)
    trace = float(np.trace(zmat[:n, :n]) + np.trace(zmat[n:, n:]))
    separation = (
        -float(graph.h1_rhs @ y)
        - certificate.rate_cap * float(graph.weights @ z)
        - certificate.defect_cap * trace
        - 2.0 * float(np.sum(cross * affine.constant))
    )
    scale = max(
        1.0, abs(float(graph.h1_rhs @ y)),
        certificate.rate_cap * abs(float(graph.weights @ z)),
        certificate.defect_cap * abs(trace),
        2.0 * abs(float(np.sum(cross * affine.constant))),
    )
    if np.min(z) < -tol.cone:
        failures.append("conic ray negative rate multiplier")
    if np.min(q) < -tol.cone:
        failures.append("conic ray negative positivity multiplier")
    if psd_min < -tol.cone:
        failures.append("conic ray PSD violation")
    if stationarity_scaled > tol.relative * 3:
        failures.append("conic ray stationarity")
    if separation <= tol.absolute * scale:
        failures.append("conic ray separation is not strictly positive")
    metrics: dict[str, float | int | bool | str | None] = {
        "dual_stationarity_scaled": stationarity_scaled,
        "rate_multiplier_min": float(np.min(z)),
        "positivity_multiplier_min": float(np.min(q)),
        "psd_min_eigenvalue": psd_min,
        "psd_symmetry_error": symmetry_error,
        "psd_trace": trace,
        "strict_separation": separation,
        "normalized_separation": separation / scale,
        "cross_block_factor": 2,
        "label": certificate.label,
    }
    return VerificationReport(not failures, False, True, metrics, failures)

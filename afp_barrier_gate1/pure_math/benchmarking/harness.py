"""Deterministic P2E benchmark harness.

The harness consumes two immutable JSON inputs: the frozen operator registry
and the benchmark manifest.  It has no tuning branch.  Partition selection is
an input gate, and the held-out partition is rejected unless the manifest is
marked immutable and contains the exact operator-registry digest.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
import gc
import hashlib
import json
import math
from pathlib import Path
import resource
import time
import tracemalloc
from typing import Any, Callable, Iterable, Mapping

import numpy as np
from scipy import linalg
from scipy.sparse.linalg import LinearOperator, expm_multiply, gmres

from pure_math.codesign.families import product_rule
from pure_math.codesign.types import QuadratureCandidate
from pure_math.optimization import QuadratureGraph, real_harmonic_samples

from .transport import TransportProfile, electron_depth_dose, layered_slab

FloatArray = np.ndarray

_REFERENCE_CACHE: dict[str, Any] = {}


@dataclass(frozen=True)
class FrozenOperator:
    name: str
    role: str
    nodes: FloatArray
    weights: FloatArray
    matrix: FloatArray
    rate_max: float
    shell_defects: dict[int, float]
    training_rotation_spread: float
    positivity_expected: bool
    source_digest: str

    @property
    def node_count(self) -> int:
        return int(self.nodes.shape[0])


@dataclass(frozen=True)
class TimedResult:
    value: Any
    wall_seconds: float
    process_seconds: float
    python_peak_bytes: int
    process_peak_rss_bytes: int


def _strict_load(path: Path) -> dict[str, Any]:
    return json.loads(
        path.read_text(encoding="utf-8"),
        parse_constant=lambda value: (_ for _ in ()).throw(
            ValueError(f"non-RFC JSON constant {value!r} in {path}")
        ),
    )


def _canonical(payload: object) -> str:
    return json.dumps(payload, sort_keys=True, separators=(",", ":"), allow_nan=False)


def _sha256(payload: object) -> str:
    return hashlib.sha256(_canonical(payload).encode("utf-8")).hexdigest()


def _weighted_norm(values: FloatArray, weights: FloatArray) -> float:
    array = np.asarray(values, dtype=float)
    if array.ndim == 1:
        return float(np.sqrt(np.sum(weights * array**2)))
    return float(np.sqrt(np.sum(weights[:, None] * array**2)))


def _relative_error(value: FloatArray | float, reference: FloatArray | float, floor: float = 1e-14) -> float:
    a = np.asarray(value, dtype=float)
    b = np.asarray(reference, dtype=float)
    return float(np.linalg.norm(a - b) / max(floor, float(np.linalg.norm(b))))


def _moments(nodes: FloatArray, weights: FloatArray, density: FloatArray) -> dict[str, Any]:
    f = np.asarray(density, dtype=float)
    scalar = float(np.dot(weights, f))
    current = np.einsum("n,ni,n->i", weights, nodes, f)
    identity = np.eye(3) / 3.0
    tensor = np.einsum("n,nij,n->ij", weights, np.einsum("ni,nj->nij", nodes, nodes) - identity, f)
    return {
        "scalar": scalar,
        "current": current.tolist(),
        "tensor": tensor.tolist(),
        "tensor_norm": float(np.linalg.norm(tensor)),
    }


def _normalize_density(values: FloatArray, weights: FloatArray) -> FloatArray:
    f = np.asarray(values, dtype=float)
    mass = float(np.dot(weights, f))
    if not np.isfinite(mass) or mass <= 0:
        raise ValueError("density has nonpositive mass")
    return f / mass


def _vmf(nodes: FloatArray, weights: FloatArray, axis: FloatArray, concentration: float) -> FloatArray:
    direction = np.asarray(axis, dtype=float)
    direction /= np.linalg.norm(direction)
    shifted = concentration * (nodes @ direction - 1.0)
    return _normalize_density(np.exp(np.clip(shifted, -700.0, 0.0)), weights)


def _graph_matrix(payload: Mapping[str, Any]) -> FloatArray:
    nodes = np.asarray(payload["nodes"], dtype=float)
    weights = np.asarray(payload["weights"], dtype=float)
    edges = np.asarray(payload["edges"], dtype=int)
    gamma = np.asarray(payload["gamma"], dtype=float)
    graph = QuadratureGraph.build(nodes, weights, [tuple(map(int, edge)) for edge in edges])
    if gamma.shape != (graph.edge_count,):
        raise ValueError("gamma size does not match edge count")
    return graph.generator(gamma)


def _spectral_operator(nodes: FloatArray, weights: FloatArray, lmax: int) -> FloatArray:
    shells: list[FloatArray] = []
    eigenvalues: list[float] = []
    for degree in range(lmax + 1):
        sample = real_harmonic_samples(nodes, degree)
        shells.append(sample)
        eigenvalues.extend([-float(degree * (degree + 1))] * sample.shape[1])
    y = np.column_stack(shells)
    gram = y.T @ (weights[:, None] * y)
    inverse = np.linalg.pinv(gram, rcond=1e-12)
    projector = inverse @ (y.T * weights[None, :])
    return y @ (np.diag(eigenvalues) @ projector)


def _operator_shell_defect(operator: FrozenOperator, degree: int) -> float:
    samples = real_harmonic_samples(operator.nodes, degree)
    weighted = np.sqrt(operator.weights)[:, None] * samples
    q, _, _ = linalg.qr(weighted, mode="economic", pivoting=True)
    rank = int(np.linalg.matrix_rank(weighted, tol=1e-11 * max(1.0, np.linalg.norm(weighted, 2))))
    frame = q[:, :rank]
    basis = frame / np.sqrt(operator.weights)[:, None]
    residual = operator.matrix @ basis + degree * (degree + 1) * basis
    return float(np.linalg.norm(np.sqrt(operator.weights)[:, None] * residual, ord=2))


def _operator_invariants(operator: FrozenOperator) -> dict[str, Any]:
    lmat = operator.matrix
    n = operator.node_count
    h0 = float(np.linalg.norm(lmat @ np.ones(n), ord=np.inf))
    h1 = float(np.linalg.norm(lmat @ operator.nodes + 2.0 * operator.nodes, ord=np.inf))
    conservation = float(np.linalg.norm(operator.weights @ lmat, ord=np.inf))
    offdiag = lmat.copy()
    np.fill_diagonal(offdiag, np.inf)
    min_offdiag = float(np.min(offdiag))
    reversibility = float(np.linalg.norm(operator.weights[:, None] * lmat - (operator.weights[:, None] * lmat).T, ord=np.inf))
    return {
        "conservation_residual": conservation,
        "h0_residual": h0,
        "h1_residual": h1,
        "reversibility_residual": reversibility,
        "minimum_offdiagonal": min_offdiag,
        "monotone_generator": bool(min_offdiag >= -3e-10),
        "rate_max_recomputed": float(np.max(-np.diag(lmat))),
        "shell_defects": {str(degree): _operator_shell_defect(operator, degree) for degree in (2, 3, 4, 5, 6)},
    }


def _load_method(name: str, payload: Mapping[str, Any]) -> FrozenOperator:
    summary = payload["summary"]
    nodes = np.asarray(payload["nodes"], dtype=float)
    weights = np.asarray(payload["weights"], dtype=float)
    matrix = _graph_matrix(payload)
    return FrozenOperator(
        name=name,
        role=str(summary["role"]),
        nodes=nodes,
        weights=weights,
        matrix=matrix,
        rate_max=float(summary["rate_max"]),
        shell_defects={int(k): float(v) for k, v in summary["shell_defects"].items()},
        training_rotation_spread=float(summary["training_rotation_spread"]),
        positivity_expected=bool(summary.get("positivity_expected", True)),
        source_digest=str(summary["gamma_sha256"]),
    )


def load_operators(registry: Mapping[str, Any]) -> tuple[dict[str, FrozenOperator], dict[str, FrozenOperator]]:
    if registry.get("schema") != "afp-p2e-frozen-operator-registry-v1":
        raise ValueError("unexpected operator registry schema")
    methods = {name: _load_method(name, payload) for name, payload in registry["methods"].items()}
    fixed = methods["harmonic_fidelity"]
    signed_matrix = _spectral_operator(fixed.nodes, fixed.weights, 6)
    methods["signed_higher_accuracy"] = FrozenOperator(
        name="signed_higher_accuracy",
        role="ablation",
        nodes=fixed.nodes.copy(),
        weights=fixed.weights.copy(),
        matrix=signed_matrix,
        rate_max=float(np.max(-np.diag(signed_matrix))),
        shell_defects={degree: _operator_shell_defect(FrozenOperator(
            "signed_higher_accuracy", "ablation", fixed.nodes, fixed.weights,
            signed_matrix, 0.0, {}, 0.0, False, "spectral-l6"), degree) for degree in (2, 3, 4, 5, 6)},
        training_rotation_spread=0.0,
        positivity_expected=False,
        source_digest="weighted-spherical-harmonic-collocation-l6",
    )
    co_design: dict[str, FrozenOperator] = {}
    for name, payload in registry.get("co_design_levels", {}).items():
        co_design[name] = _load_method(name, payload)
    if not co_design and "co_design_ablation" in registry:
        co_design["alter_quadrature"] = _load_method("alter_quadrature", registry["co_design_ablation"])
    return methods, co_design


def _timed(function: Callable[[], Any], repeats: int) -> TimedResult:
    if repeats <= 0:
        raise ValueError("repeats must be positive")
    walls: list[float] = []
    processes: list[float] = []
    peaks: list[int] = []
    last: Any = None
    for _ in range(repeats):
        gc.collect()
        tracemalloc.start()
        wall0 = time.perf_counter()
        process0 = time.process_time()
        last = function()
        processes.append(time.process_time() - process0)
        walls.append(time.perf_counter() - wall0)
        _, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        peaks.append(int(peak))
    return TimedResult(
        value=last,
        wall_seconds=float(np.median(walls)),
        process_seconds=float(np.median(processes)),
        python_peak_bytes=max(peaks),
        process_peak_rss_bytes=int(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss * 1024),
    )


def _evaluate_common(
    operator: FrozenOperator,
    final: FloatArray,
    reference_moments: Mapping[str, Any],
    response: FloatArray,
    reference_response: FloatArray,
    timed: TimedResult,
) -> dict[str, Any]:
    moments = _moments(operator.nodes, operator.weights, final)
    return {
        "minimum_flux": float(np.min(final)),
        "positivity_passed": bool(np.min(final) >= -3e-9),
        "moments": moments,
        "scalar_error": abs(float(moments["scalar"]) - float(reference_moments["scalar"])),
        "current_error": _relative_error(moments["current"], reference_moments["current"]),
        "tensor_error": _relative_error(moments["tensor"], reference_moments["tensor"]),
        "response": np.asarray(response, dtype=float).tolist(),
        "response_error": _relative_error(response, reference_response),
        "runtime_wall_seconds": timed.wall_seconds,
        "runtime_process_seconds": timed.process_seconds,
        "python_peak_bytes": timed.python_peak_bytes,
        "process_peak_rss_bytes": timed.process_peak_rss_bytes,
        "iterations": 1,
        "matvecs": 1,
    }


def _analytic_shell_state(operator: FrozenOperator, specification: Mapping[str, Any]) -> tuple[FloatArray, FloatArray]:
    degree = int(specification["degree"])
    column = int(specification["column"])
    depth = float(specification["depth"])
    diffusion = float(specification.get("diffusion", 1.0))
    samples = real_harmonic_samples(operator.nodes, degree)[:, column]
    final = expm_multiply(diffusion * depth * operator.matrix, samples)
    exact = math.exp(-diffusion * depth * degree * (degree + 1)) * samples
    return np.asarray(final), exact


def _mode_case(operator: FrozenOperator, spec: Mapping[str, Any], repeats: int) -> dict[str, Any]:
    timed = _timed(lambda: _analytic_shell_state(operator, spec), repeats)
    final, exact = timed.value
    degree = int(spec["degree"])
    column = int(spec["column"])
    samples = real_harmonic_samples(operator.nodes, degree)[:, column]
    response = np.asarray([np.dot(operator.weights * samples, final)])
    reference_response = np.asarray([np.dot(operator.weights * samples, exact)])
    companion0 = _normalize_density(1.0 + 0.20 * samples / max(1e-15, np.max(np.abs(samples))), operator.weights)
    companion = expm_multiply(float(spec.get("diffusion", 1.0)) * float(spec["depth"]) * operator.matrix, companion0)
    exact_moments = _moments(operator.nodes, operator.weights, exact)
    output = _evaluate_common(operator, final, exact_moments, response, reference_response, timed)
    output.update({
        "weighted_state_error": _weighted_norm(final - exact, operator.weights) / max(1e-14, _weighted_norm(exact, operator.weights)),
        "companion_minimum_flux": float(np.min(companion)),
        "reference_uncertainty": 0.0,
        "physical_model_uncertainty": 0.0,
    })
    return output


def _bandlimited_state(operator: FrozenOperator, spec: Mapping[str, Any]) -> tuple[FloatArray, FloatArray, FloatArray]:
    seed = int(spec["seed"])
    maximum_degree = int(spec["maximum_degree"])
    depth = float(spec["depth"])
    rng = np.random.default_rng(seed)
    initial = np.ones(operator.node_count)
    exact = np.ones(operator.node_count)
    for degree in range(1, maximum_degree + 1):
        shell = real_harmonic_samples(operator.nodes, degree)
        coefficient = rng.normal(size=shell.shape[1]) / (degree + 1.0) ** 2
        contribution = shell @ coefficient
        initial += contribution
        exact += math.exp(-depth * degree * (degree + 1)) * contribution
    floor = float(np.min(initial))
    if floor <= 0:
        initial += 1.05 * abs(floor) + 0.05
        exact += 1.05 * abs(floor) + 0.05
    initial = _normalize_density(initial, operator.weights)
    exact = _normalize_density(exact, operator.weights)
    final = expm_multiply(depth * operator.matrix, initial)
    return np.asarray(final), exact, initial


def _bandlimited_case(operator: FrozenOperator, spec: Mapping[str, Any], repeats: int) -> dict[str, Any]:
    timed = _timed(lambda: _bandlimited_state(operator, spec), repeats)
    final, exact, initial = timed.value
    probe = real_harmonic_samples(operator.nodes, min(2, int(spec["maximum_degree"])))[:, 0]
    response = np.asarray([np.dot(operator.weights * probe, final), np.dot(operator.weights * (operator.nodes[:, 2] > 0), final)])
    reference_response = np.asarray([np.dot(operator.weights * probe, exact), np.dot(operator.weights * (operator.nodes[:, 2] > 0), exact)])
    output = _evaluate_common(operator, final, _moments(operator.nodes, operator.weights, exact), response, reference_response, timed)
    output.update({
        "weighted_state_error": _weighted_norm(final - exact, operator.weights) / max(1e-14, _weighted_norm(exact, operator.weights)),
        "initial_minimum_flux": float(np.min(initial)),
        "reference_uncertainty": 0.0,
        "physical_model_uncertainty": 0.0,
    })
    return output


def _reference_candidate(spec: Mapping[str, Any]) -> QuadratureCandidate:
    n_mu = int(spec.get("reference_n_mu", 7))
    n_phi = int(spec.get("reference_n_phi", 16))
    return product_rule(n_mu, n_phi, graph="complete")


def _beam_outputs(operator: FrozenOperator, spec: Mapping[str, Any], l_override: FloatArray | None = None) -> tuple[FloatArray, FloatArray]:
    axis = np.asarray(spec["axis"], dtype=float)
    initial = _vmf(operator.nodes, operator.weights, axis, float(spec["concentration"]))
    matrix = operator.matrix if l_override is None else l_override
    final = expm_multiply(float(spec["depth"]) * matrix, initial)
    direction = axis / np.linalg.norm(axis)
    cosine = operator.nodes @ direction
    response = np.asarray([
        np.dot(operator.weights * (cosine >= float(spec.get("cone_cosine", 0.85))), final),
        np.dot(operator.weights * cosine, final),
        np.dot(operator.weights * (cosine**2 - 1.0 / 3.0), final),
    ])
    return np.asarray(final), response


def _fine_reference(spec: Mapping[str, Any], evaluator: Callable[[FrozenOperator, FloatArray], tuple[FloatArray, FloatArray]]) -> tuple[dict[str, Any], FloatArray, float, float]:
    key = _sha256({"kind": "fine-angular", "parameters": spec})
    cached = _REFERENCE_CACHE.get(key)
    if cached is not None:
        moments, response, uncertainty, negative = cached
        return moments, np.asarray(response, dtype=float), float(uncertainty), float(negative)
    candidate = _reference_candidate(spec)
    l_hi = int(spec.get("reference_lmax", 8))
    l_lo = max(2, int(spec.get("reference_lmax_low", l_hi - 2)))
    hi = _reference_operator(candidate, l_hi)
    lo = _reference_operator(candidate, l_lo)
    hi_state, hi_response = evaluator(hi, hi.matrix)
    lo_state, lo_response = evaluator(lo, lo.matrix)
    uncertainty = _relative_error(lo_response, hi_response)
    negative = float(min(np.min(hi_state), np.min(lo_state)))
    moments = _moments(hi.nodes, hi.weights, hi_state)
    _REFERENCE_CACHE[key] = (moments, np.asarray(hi_response, dtype=float), uncertainty, negative)
    return moments, np.asarray(hi_response, dtype=float), uncertainty, negative



def _profile_moments(profile: TransportProfile) -> dict[str, Any]:
    scalar = float(np.sum(profile.scalar))
    current = np.sum(profile.current, axis=0)
    tensor = np.sum(profile.tensor, axis=0)
    return {
        "scalar": scalar,
        "current": np.asarray(current, dtype=float).tolist(),
        "tensor": np.asarray(tensor, dtype=float).tolist(),
        "tensor_norm": float(np.linalg.norm(tensor)),
    }


def _reference_operator(candidate: QuadratureCandidate, lmax: int) -> FrozenOperator:
    matrix = _spectral_operator(candidate.nodes, candidate.weights, lmax)
    return FrozenOperator(
        f"reference_l{lmax}",
        "reference",
        candidate.nodes,
        candidate.weights,
        matrix,
        float(np.max(-np.diag(matrix))),
        {},
        0.0,
        False,
        f"weighted-spherical-harmonic-reference-l{lmax}",
    )


def _transport_reference(
    kind: str,
    spec: Mapping[str, Any],
) -> tuple[TransportProfile, float, float]:
    key = _sha256({"kind": kind, "parameters": spec, "reference": "transport-v2"})
    cached = _REFERENCE_CACHE.get(key)
    if cached is not None:
        profile, angular_uncertainty, minimum = cached
        return profile, float(angular_uncertainty), float(minimum)
    candidate = _reference_candidate(spec)
    l_hi = int(spec.get("reference_lmax", 8))
    l_lo = max(2, int(spec.get("reference_lmax_low", l_hi - 2)))
    high = _reference_operator(candidate, l_hi)
    low = _reference_operator(candidate, l_lo)
    if kind == "electron_published":
        high_profile = electron_depth_dose(
            high.nodes, high.weights, high.matrix, spec, direct=True
        )
        low_profile = electron_depth_dose(
            low.nodes, low.weights, low.matrix, spec, direct=True
        )
    elif kind in {"proton_layered", "hts_oblique"}:
        high_profile = layered_slab(
            high.nodes, high.weights, high.matrix, spec, direct=True
        )
        low_profile = layered_slab(
            low.nodes, low.weights, low.matrix, spec, direct=True
        )
    else:
        raise ValueError(f"unsupported transport reference kind {kind!r}")
    angular_uncertainty = _relative_error(low_profile.response, high_profile.response)
    minimum = float(min(low_profile.minimum_state, high_profile.minimum_state))
    _REFERENCE_CACHE[key] = (high_profile, angular_uncertainty, minimum)
    return high_profile, angular_uncertainty, minimum


def _transport_common(
    operator: FrozenOperator,
    profile: TransportProfile,
    reference: TransportProfile,
    reference_uncertainty: float,
    physical_uncertainty: float,
    timed: TimedResult,
) -> dict[str, Any]:
    moments = _profile_moments(profile)
    reference_moments = _profile_moments(reference)
    return {
        "minimum_flux": float(profile.minimum_state),
        "positivity_passed": bool(profile.minimum_state >= -3e-9),
        "moments": moments,
        "scalar_error": _relative_error(moments["scalar"], reference_moments["scalar"]),
        "current_error": _relative_error(moments["current"], reference_moments["current"]),
        "tensor_error": _relative_error(moments["tensor"], reference_moments["tensor"]),
        "response": np.asarray(profile.response, dtype=float).tolist(),
        "response_labels": list(profile.response_labels),
        "response_error": _relative_error(profile.response, reference.response),
        "runtime_wall_seconds": timed.wall_seconds,
        "runtime_process_seconds": timed.process_seconds,
        "python_peak_bytes": timed.python_peak_bytes,
        "process_peak_rss_bytes": timed.process_peak_rss_bytes,
        "iterations": int(profile.iterations),
        "matvecs": int(profile.matvecs),
        "converged": bool(profile.converged),
        "particle_balance_error": float(profile.particle_balance_error),
        "reference_uncertainty": float(reference_uncertainty),
        "physical_model_uncertainty": float(physical_uncertainty),
        "reference_minimum_flux": float(reference.minimum_state),
        "extra": profile.extra,
    }


def _electron_case(operator: FrozenOperator, spec: Mapping[str, Any], repeats: int) -> dict[str, Any]:
    reference, angular_uncertainty, _ = _transport_reference("electron_published", spec)
    timed = _timed(
        lambda: electron_depth_dose(
            operator.nodes, operator.weights, operator.matrix, spec, direct=False
        ),
        repeats,
    )
    profile = timed.value
    output = _transport_common(
        operator,
        profile,
        reference,
        angular_uncertainty,
        float(spec.get("physical_model_uncertainty", 0.05)),
        timed,
    )
    output["published_case_scope"] = profile.extra["scope"]
    output["published_geometry"] = profile.extra["published_geometry"]
    return output


def _physical_sensitivity(
    kind: str,
    spec: Mapping[str, Any],
    reference: TransportProfile,
) -> float:
    key = _sha256({"kind": kind, "parameters": spec, "reference": "physical-envelope-v1"})
    cached = _REFERENCE_CACHE.get(key)
    if cached is not None:
        return float(cached)
    candidate = _reference_candidate(spec)
    operator = _reference_operator(candidate, int(spec.get("reference_lmax", 8)))
    low = layered_slab(
        operator.nodes,
        operator.weights,
        operator.matrix,
        spec,
        direct=True,
        coefficient_scale=float(spec.get("coefficient_scale_low", 0.95)),
    )
    high = layered_slab(
        operator.nodes,
        operator.weights,
        operator.matrix,
        spec,
        direct=True,
        coefficient_scale=float(spec.get("coefficient_scale_high", 1.05)),
    )
    value = max(
        _relative_error(low.response, reference.response),
        _relative_error(high.response, reference.response),
    )
    _REFERENCE_CACHE[key] = float(value)
    return float(value)


def _slab_case(
    operator: FrozenOperator,
    spec: Mapping[str, Any],
    repeats: int,
    *,
    kind: str,
) -> dict[str, Any]:
    reference, angular_uncertainty, _ = _transport_reference(kind, spec)
    physical_uncertainty = _physical_sensitivity(kind, spec, reference)
    timed = _timed(
        lambda: layered_slab(
            operator.nodes, operator.weights, operator.matrix, spec, direct=False
        ),
        repeats,
    )
    profile = timed.value
    return _transport_common(
        operator,
        profile,
        reference,
        angular_uncertainty,
        physical_uncertainty,
        timed,
    )


def _beam_case(operator: FrozenOperator, spec: Mapping[str, Any], repeats: int) -> dict[str, Any]:
    ref_moments, ref_response, ref_uncertainty, ref_minimum = _fine_reference(
        spec, lambda op, mat: _beam_outputs(op, spec, mat)
    )
    timed = _timed(lambda: _beam_outputs(operator, spec), repeats)
    final, response = timed.value
    output = _evaluate_common(operator, final, ref_moments, response, ref_response, timed)
    output.update({
        "reference_uncertainty": ref_uncertainty,
        "reference_minimum_flux": ref_minimum,
        "physical_model_uncertainty": 0.0,
    })
    return output


def _layer_profile(
    operator: FrozenOperator,
    spec: Mapping[str, Any],
    matrix: FloatArray | None = None,
    coefficient_scale: float = 1.0,
) -> tuple[FloatArray, FloatArray, dict[str, Any]]:
    direction = np.asarray(spec["axis"], dtype=float)
    direction /= np.linalg.norm(direction)
    normal = np.asarray(spec.get("normal", [0.0, 0.0, 1.0]), dtype=float)
    normal /= np.linalg.norm(normal)
    state = _vmf(operator.nodes, operator.weights, direction, float(spec.get("concentration", 24.0)))
    lmat = operator.matrix if matrix is None else matrix
    energy = float(spec.get("energy_mev", 1.0))
    deposition: list[float] = []
    layer_current: list[float] = []
    layer_qn: list[float] = []
    profile_labels: list[str] = []
    for layer in spec["layers"]:
        cells = int(layer.get("cells", 1))
        total_thickness = float(layer["thickness_cm"])
        ds = total_thickness / cells
        for cell in range(cells):
            mu = np.maximum(np.abs(operator.nodes @ normal), float(spec.get("mu_floor", 0.08)))
            scatter = coefficient_scale * float(layer["scatter_power"])
            removal = coefficient_scale * float(layer.get("removal", 0.0))
            stopping = coefficient_scale * float(layer.get("stopping_mev_per_cm", 0.0))
            before_mass = float(np.dot(operator.weights, state))
            system = scatter * lmat - np.diag(removal / mu)
            next_state = expm_multiply(ds * system, state)
            after_mass = float(np.dot(operator.weights, next_state))
            mean_mass = 0.5 * (before_mass + after_mass)
            deposited = max(0.0, energy * (before_mass - after_mass)) + stopping * ds * mean_mass
            deposition.append(float(deposited))
            energy = max(float(spec.get("cutoff_mev", 0.0)), energy - stopping * ds)
            state = np.asarray(next_state)
            layer_current.append(float(np.dot(operator.weights * np.maximum(operator.nodes @ normal, 0.0), state)))
            layer_qn.append(float(np.dot(operator.weights * ((operator.nodes @ normal) ** 2 - 1.0 / 3.0), state)))
            profile_labels.append(f"{layer['material']}:{cell}")
    response = np.concatenate([
        np.asarray(deposition),
        np.asarray([sum(deposition), layer_current[-1], layer_qn[-1], energy]),
    ])
    extra = {
        "deposition_profile": deposition,
        "layer_current": layer_current,
        "layer_qn": layer_qn,
        "profile_labels": profile_labels,
        "final_energy_mev": energy,
    }
    return state, response, extra


def _layered_case(operator: FrozenOperator, spec: Mapping[str, Any], repeats: int) -> dict[str, Any]:
    evaluator = lambda op, mat: _layer_profile(op, spec, mat)[:2]
    ref_moments, ref_response, ref_uncertainty, ref_minimum = _fine_reference(spec, evaluator)
    # A deterministic coefficient-uncertainty envelope, kept separate from
    # angular/reference error.  It is sensitivity, not a claim of evaluated
    # nuclear-data covariance.
    ref_candidate = _reference_candidate(spec)
    ref_matrix = _spectral_operator(ref_candidate.nodes, ref_candidate.weights, int(spec.get("reference_lmax", 8)))
    ref_operator = FrozenOperator("reference", "reference", ref_candidate.nodes, ref_candidate.weights, ref_matrix, 0.0, {}, 0.0, False, "reference")
    _, response_low, _ = _layer_profile(ref_operator, spec, ref_matrix, coefficient_scale=0.95)
    _, response_high, _ = _layer_profile(ref_operator, spec, ref_matrix, coefficient_scale=1.05)
    physical_uncertainty = max(_relative_error(response_low, ref_response), _relative_error(response_high, ref_response))

    timed = _timed(lambda: _layer_profile(operator, spec), repeats)
    final, response, extra = timed.value
    output = _evaluate_common(operator, final, ref_moments, response, ref_response, timed)
    output.update(extra)
    output.update({
        "reference_uncertainty": ref_uncertainty,
        "reference_minimum_flux": ref_minimum,
        "physical_model_uncertainty": physical_uncertainty,
    })
    return output


def _neutron_state(operator: FrozenOperator, spec: Mapping[str, Any]) -> tuple[FloatArray, FloatArray, FloatArray, float]:
    seed = int(spec["seed"])
    maximum_degree = int(spec["maximum_degree"])
    epsilon = float(spec["epsilon"])
    collision_depth = float(spec["collision_depth"])
    rng = np.random.default_rng(seed)
    initial = np.ones(operator.node_count)
    exact = np.ones(operator.node_count)
    fp_exact = np.ones(operator.node_count)
    maximum_bound = 0.0
    for degree in range(1, maximum_degree + 1):
        shell = real_harmonic_samples(operator.nodes, degree)
        coefficients = rng.normal(size=shell.shape[1]) / (degree + 1) ** 2
        contribution = shell @ coefficients
        lam = float(degree * (degree + 1))
        boltzmann_rate = (1.0 - math.exp(-epsilon * lam)) / epsilon
        initial += contribution
        exact += math.exp(-collision_depth * boltzmann_rate) * contribution
        fp_exact += math.exp(-collision_depth * lam) * contribution
        maximum_bound = max(maximum_bound, 0.5 * epsilon * lam * lam)
    minimum = float(np.min(initial))
    if minimum <= 0:
        shift = 1.05 * abs(minimum) + 0.05
        initial += shift; exact += shift; fp_exact += shift
    initial = _normalize_density(initial, operator.weights)
    exact = _normalize_density(exact, operator.weights)
    fp_exact = _normalize_density(fp_exact, operator.weights)
    final = expm_multiply(collision_depth * operator.matrix, initial)
    return np.asarray(final), exact, fp_exact, maximum_bound


def _neutron_case(operator: FrozenOperator, spec: Mapping[str, Any], repeats: int) -> dict[str, Any]:
    timed = _timed(lambda: _neutron_state(operator, spec), repeats)
    final, exact_boltzmann, exact_fp, bound = timed.value
    probe = real_harmonic_samples(operator.nodes, 2)[:, 0]
    response = np.asarray([np.dot(operator.weights * probe, final)])
    reference_response = np.asarray([np.dot(operator.weights * probe, exact_boltzmann)])
    output = _evaluate_common(operator, final, _moments(operator.nodes, operator.weights, exact_boltzmann), response, reference_response, timed)
    output.update({
        "weighted_state_error": _weighted_norm(final - exact_boltzmann, operator.weights) / max(1e-14, _weighted_norm(exact_boltzmann, operator.weights)),
        "angular_discretization_error_against_fp": _weighted_norm(final - exact_fp, operator.weights) / max(1e-14, _weighted_norm(exact_fp, operator.weights)),
        "bfp_physical_model_error": _weighted_norm(exact_fp - exact_boltzmann, operator.weights) / max(1e-14, _weighted_norm(exact_boltzmann, operator.weights)),
        "bfp_rate_error_bound": bound,
        "reference_uncertainty": 0.0,
        "physical_model_uncertainty": _weighted_norm(exact_fp - exact_boltzmann, operator.weights) / max(1e-14, _weighted_norm(exact_boltzmann, operator.weights)),
    })
    return output


def _accelerator_case(methods: Mapping[str, FrozenOperator], spec: Mapping[str, Any]) -> dict[str, Any]:
    baseline = methods["monotone_afp_baseline"]
    primary = methods["harmonic_fidelity"]
    if baseline.node_count != primary.node_count or np.max(np.abs(baseline.nodes - primary.nodes)) > 1e-13:
        raise ValueError("accelerator ablation requires identical nodes")
    nodes = baseline.nodes
    diagonal = float(spec.get("diagonal", 1.0)) + float(spec.get("streaming", 0.2)) * np.abs(nodes[:, 2])
    beta = float(spec.get("beta", 0.95))
    production = np.diag(diagonal) - beta * baseline.matrix
    preconditioner = np.diag(diagonal) - beta * primary.matrix
    rhs = _normalize_density(np.exp(float(spec.get("source_concentration", 8.0)) * (nodes[:, 2] - 1.0)), baseline.weights)
    reference = np.linalg.solve(production, rhs)

    def solve(preconditioned: bool) -> tuple[FloatArray, int, int]:
        count = 0
        def callback(_: Any) -> None:
            nonlocal count
            count += 1
        matvecs = 0
        def matvec(x: FloatArray) -> FloatArray:
            nonlocal matvecs
            matvecs += 1
            return production @ x
        operator = LinearOperator(production.shape, matvec=matvec, dtype=float)
        pre = None
        if preconditioned:
            lu, piv = linalg.lu_factor(preconditioner)
            pre = LinearOperator(preconditioner.shape, matvec=lambda x: linalg.lu_solve((lu, piv), x), dtype=float)
        solution, info = gmres(operator, rhs, M=pre, rtol=float(spec.get("rtol", 1e-10)), atol=0.0, restart=50, maxiter=1000, callback=callback, callback_type="pr_norm")
        if info != 0:
            raise RuntimeError(f"GMRES failed with info={info}")
        return np.asarray(solution), count, matvecs

    unpre = _timed(lambda: solve(False), int(spec.get("timing_repeats", 3)))
    accel = _timed(lambda: solve(True), int(spec.get("timing_repeats", 3)))
    unpre_solution, unpre_iterations, unpre_matvecs = unpre.value
    accel_solution, accel_iterations, accel_matvecs = accel.value
    return {
        "scope": "ACCELERATOR_ONLY_FIXED_PRODUCTION_OPERATOR_NOT_P2D_COMPLETION",
        "production_operator": "monotone_afp_baseline",
        "preconditioner": "harmonic_fidelity",
        "fixed_point_reference_sha256": hashlib.sha256(np.asarray(reference, dtype="<f8").tobytes()).hexdigest(),
        "unpreconditioned": {
            "iterations": unpre_iterations, "matvecs": unpre_matvecs,
            "wall_seconds": unpre.wall_seconds,
            "relative_error": _relative_error(unpre_solution, reference),
        },
        "accelerated": {
            "iterations": accel_iterations, "matvecs": accel_matvecs,
            "wall_seconds": accel.wall_seconds,
            "relative_error": _relative_error(accel_solution, reference),
        },
        "iteration_ratio": float(accel_iterations / max(1, unpre_iterations)),
        "matvec_ratio": float(accel_matvecs / max(1, unpre_matvecs)),
        "wall_time_ratio": float(accel.wall_seconds / max(1e-15, unpre.wall_seconds)),
        "production_matrix_unchanged": True,
    }


def _run_case(operator: FrozenOperator, case: Mapping[str, Any], repeats: int) -> dict[str, Any]:
    kind = case["kind"]
    spec = case["parameters"]
    if kind == "mode_decay":
        return _mode_case(operator, spec, repeats)
    if kind == "bandlimited":
        return _bandlimited_case(operator, spec, repeats)
    if kind == "narrow_beam":
        return _beam_case(operator, spec, repeats)
    if kind in {"electron_published", "electron_depth_dose"}:
        return _electron_case(operator, spec, repeats)
    if kind in {"proton_layered", "hts_oblique"}:
        return _slab_case(operator, spec, repeats, kind=kind)
    if kind == "neutron_bfp":
        return _neutron_case(operator, spec, repeats)
    raise ValueError(f"unknown benchmark kind {kind!r}")


def _collision_rotation_spread(operator: FrozenOperator) -> dict[str, Any]:
    values: list[float] = []
    directions = (
        [0.0, 0.0, 1.0], [1.0, 0.0, 0.0], [0.0, 1.0, 0.0],
        [1.0, 1.0, 1.0], [1.0, -1.0, 0.5], [-0.5, 1.0, 1.0],
        [2.0, -3.0, 1.0], [-1.0, -2.0, 4.0],
    )
    for raw in directions:
        direction = np.asarray(raw, dtype=float)
        direction /= np.linalg.norm(direction)
        samples = (operator.nodes @ direction) ** 2 - 1.0 / 3.0
        residual = operator.matrix @ samples + 6.0 * samples
        values.append(_weighted_norm(residual, operator.weights) / max(1e-14, _weighted_norm(samples, operator.weights)))
    minimum, maximum = min(values), max(values)
    return {
        "sample_count": len(values),
        "minimum": minimum,
        "maximum": maximum,
        "absolute": maximum - minimum,
        "relative": (maximum - minimum) / max(1e-14, abs(minimum)),
        "scope": "COLLISION_ONLY_FIXED_QUADRATURE_DIRECTIONAL_H2_PROBES",
    }


def _physical_rotation_response(
    operator: FrozenOperator,
    kind: str,
    parameters: Mapping[str, Any],
    directions: tuple[tuple[float, float, float], ...],
) -> dict[str, Any]:
    values: list[float] = []
    for raw in directions:
        axis = np.asarray(raw, dtype=float)
        axis /= np.linalg.norm(axis)
        rotated = dict(parameters)
        rotated["axis"] = axis.tolist()
        if kind == "narrow_beam":
            _, response = _beam_outputs(operator, rotated)
        elif kind in {"proton_layered", "hts_oblique"}:
            # Keep incidence angle fixed while rotating the entire physical
            # problem relative to the fixed quadrature.
            base_axis = np.asarray(parameters["axis"], dtype=float)
            base_normal = np.asarray(parameters.get("normal", [0.0, 0.0, 1.0]), dtype=float)
            base_axis /= np.linalg.norm(base_axis)
            base_normal /= np.linalg.norm(base_normal)
            cosine = float(np.clip(base_axis @ base_normal, -1.0, 1.0))
            tangent = np.asarray([axis[1], -axis[0], 0.0])
            if np.linalg.norm(tangent) < 1e-10:
                tangent = np.asarray([1.0, 0.0, 0.0])
            tangent /= np.linalg.norm(tangent)
            normal = cosine * axis + math.sqrt(max(0.0, 1.0 - cosine * cosine)) * tangent
            normal /= np.linalg.norm(normal)
            rotated["normal"] = normal.tolist()
            response = layered_slab(
                operator.nodes, operator.weights, operator.matrix, rotated, direct=False
            ).response
        else:
            raise ValueError(f"unsupported physical rotation kind {kind!r}")
        values.append(float(np.linalg.norm(response)))
    if not values:
        return {"sample_count": 0, "scope": "NOT_RUN"}
    minimum, maximum = min(values), max(values)
    return {
        "sample_count": len(values),
        "minimum": minimum,
        "maximum": maximum,
        "absolute": maximum - minimum,
        "relative": (maximum - minimum) / max(1e-14, abs(minimum)),
        "scope": "PHYSICAL_PROBLEM_ROTATED_RELATIVE_TO_FIXED_QUADRATURE_FINITE_SAMPLE",
    }


def _rotation_spread(operator: FrozenOperator, case: Mapping[str, Any], repeats: int) -> dict[str, Any]:
    del repeats
    parameters = case["parameters"]
    kind = str(case["kind"])
    count = int(parameters.get("physical_rotation_samples", 0))
    pool = (
        (0.0, 0.0, 1.0), (1.0, 0.0, 0.0), (0.0, 1.0, 0.0),
        (1.0, 1.0, 1.0), (1.0, -1.0, 0.5), (-0.5, 1.0, 1.0),
    )
    physical = {"sample_count": 0, "scope": "NOT_REQUESTED_FOR_CASE"}
    if count > 0 and kind in {"narrow_beam", "proton_layered", "hts_oblique"}:
        physical = _physical_rotation_response(operator, kind, parameters, pool[:count])
    return {
        "collision_only": _collision_rotation_spread(operator),
        "physical_problem": physical,
        "separation_note": "collision-shell rotation is separated from streaming-ray and boundary orientation effects",
    }


def _paired_equal_cost(case_results: Mapping[str, Mapping[str, Any]]) -> dict[str, Any]:
    baseline = case_results["monotone_afp_baseline"]
    primary = case_results["harmonic_fidelity"]
    common_budget = max(float(baseline["runtime_wall_seconds"]), float(primary["runtime_wall_seconds"]))
    target = max(float(baseline["response_error"]), float(primary["response_error"]))
    return {
        "direction_count": int(primary["node_count"]),
        "error_at_equal_direction_count": {
            "monotone_afp_baseline": float(baseline["response_error"]),
            "harmonic_fidelity": float(primary["response_error"]),
        },
        "equal_wall_time_budget_seconds": common_budget,
        "error_at_equal_wall_time": {
            "monotone_afp_baseline": float(baseline["response_error"]),
            "harmonic_fidelity": float(primary["response_error"]),
            "protocol": "one paired fixed-node solve; both are below the common max-of-pair budget",
        },
        "equal_response_error_target": target,
        "wall_time_at_equal_response_error": {
            "monotone_afp_baseline": float(baseline["runtime_wall_seconds"]) if float(baseline["response_error"]) <= target else None,
            "harmonic_fidelity": float(primary["runtime_wall_seconds"]) if float(primary["response_error"]) <= target else None,
            "protocol": "fixed-node paired target; co-design scaling is reported separately",
        },
    }



def _co_design_summary(
    operators: Mapping[str, FrozenOperator],
    case: Mapping[str, Any],
    repeats: int,
) -> dict[str, Any]:
    rows: dict[str, Any] = {}
    for name in sorted(operators):
        operator = operators[name]
        row = _run_case(operator, case, repeats)
        row["node_count"] = operator.node_count
        row["rate_max"] = operator.rate_max
        row["rotation_spread"] = _rotation_spread(operator, case, repeats)
        rows[name] = row

    levels: dict[str, dict[str, Any]] = {}
    for level in ("product_3x8", "product_4x8"):
        baseline_name = f"baseline_{level}"
        harmonic_name = f"harmonic_{level}"
        if baseline_name in rows and harmonic_name in rows:
            baseline = rows[baseline_name]
            harmonic = rows[harmonic_name]
            levels[level] = {
                "direction_count": int(harmonic["node_count"]),
                "baseline_response_error": float(baseline["response_error"]),
                "harmonic_response_error": float(harmonic["response_error"]),
                "error_ratio": float(harmonic["response_error"]) / max(1e-15, float(baseline["response_error"])),
                "baseline_wall_seconds": float(baseline["runtime_wall_seconds"]),
                "harmonic_wall_seconds": float(harmonic["runtime_wall_seconds"]),
            }

    families = {
        "baseline": [name for name in rows if name.startswith("baseline_")],
        "harmonic": [name for name in rows if name.startswith("harmonic_")],
    }
    budgets = sorted({float(row["runtime_wall_seconds"]) for row in rows.values()})
    equal_wall: list[dict[str, Any]] = []
    for budget in budgets:
        entry: dict[str, Any] = {"budget_seconds": budget}
        for family, names in families.items():
            admissible = [rows[name] for name in names if float(rows[name]["runtime_wall_seconds"]) <= budget * (1.0 + 1e-12)]
            if not admissible:
                entry[family] = None
            else:
                best = min(admissible, key=lambda row: (float(row["response_error"]), int(row["node_count"])))
                entry[family] = {
                    "response_error": float(best["response_error"]),
                    "node_count": int(best["node_count"]),
                    "wall_seconds": float(best["runtime_wall_seconds"]),
                }
        equal_wall.append(entry)

    target = float(rows.get("baseline_product_4x8", next(iter(rows.values())))["response_error"])
    equal_error: dict[str, Any] = {"target": target}
    for family, names in families.items():
        admissible = [rows[name] for name in names if float(rows[name]["response_error"]) <= target]
        if not admissible:
            equal_error[family] = None
        else:
            best = min(admissible, key=lambda row: (float(row["runtime_wall_seconds"]), int(row["node_count"])))
            equal_error[family] = {
                "wall_seconds": float(best["runtime_wall_seconds"]),
                "response_error": float(best["response_error"]),
                "node_count": int(best["node_count"]),
            }
    return {
        "scope": "SEPARATE_QUADRATURE_CO_DESIGN_STUDY_NOT_FIXED_NODE_OPERATOR_QUALITY",
        "methods": rows,
        "equal_direction_levels": levels,
        "equal_wall_time_frontier": equal_wall,
        "wall_time_at_equal_response_error": equal_error,
    }


def run_benchmarks(
    registry: Mapping[str, Any],
    manifest: Mapping[str, Any],
    partition: str,
) -> dict[str, Any]:
    if manifest.get("schema") != "afp-p2e-benchmark-manifest-v1":
        raise ValueError("unexpected benchmark manifest schema")
    if manifest.get("operator_registry_sha256") != registry.get("registry_sha256"):
        raise ValueError("manifest/operator registry digest mismatch")
    if partition == "heldout" and manifest.get("status") != "IMMUTABLE_PREREGISTERED":
        raise ValueError("held-out execution requires immutable preregistration")
    methods, co_design = load_operators(registry)
    fixed_names = tuple(manifest["fixed_node_method_order"])
    repeats = int(manifest["timing"]["repeats"])
    cases = [case for case in manifest["cases"] if case["partition"] == partition]
    if not cases:
        raise ValueError(f"manifest has no {partition} cases")
    results: dict[str, Any] = {}
    invariants = {name: _operator_invariants(methods[name]) for name in fixed_names}
    for case in cases:
        case_rows: dict[str, Any] = {}
        for name in fixed_names:
            operator = methods[name]
            row = _run_case(operator, case, repeats)
            row["node_count"] = operator.node_count
            row["rate_max"] = operator.rate_max
            row["rotation_spread"] = _rotation_spread(operator, case, repeats)
            case_rows[name] = row
        case_payload: dict[str, Any] = {
            "category": case["category"],
            "kind": case["kind"],
            "partition": partition,
            "methods": case_rows,
            "equal_cost": _paired_equal_cost(case_rows),
        }
        if case["id"] in set(manifest.get("co_design_case_ids", [])):
            case_payload["co_design_ablation"] = _co_design_summary(co_design, case, repeats)
        results[case["id"]] = case_payload

    accelerator = _accelerator_case(methods, manifest["accelerator_ablation"])
    payload: dict[str, Any] = {
        "schema": "afp-p2e-benchmark-results-v1",
        "partition": partition,
        "manifest_sha256": manifest["manifest_sha256"],
        "operator_registry_sha256": registry["registry_sha256"],
        "method_invariants": invariants,
        "cases": results,
        "accelerator_only_ablation": accelerator,
        "co_design_scope": {
            "available_levels": sorted(co_design),
            "status": "SEPARATE_FROM_FIXED_NODE_OPERATOR_QUALITY",
        },
    }
    digest_payload = dict(payload)
    payload["results_sha256"] = _sha256(digest_payload)
    return payload


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--registry", type=Path, required=True)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--partition", choices=("training", "validation", "heldout"), required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    registry = _strict_load(args.registry)
    manifest = _strict_load(args.manifest)
    payload = run_benchmarks(registry, manifest, args.partition)
    rendered = json.dumps(payload, indent=2, sort_keys=True, allow_nan=False) + "\n"
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(rendered, encoding="utf-8")
    print(rendered, end="")
    print(f"P2E_BENCHMARK_{args.partition.upper()}_PASS")


if __name__ == "__main__":
    main()

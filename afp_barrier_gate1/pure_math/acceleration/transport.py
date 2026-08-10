"""Same-node forward-peaked transport comparisons for P2D.

The module deliberately separates three objects:

* the high-order production matrix, assembled from streaming, boundary,
  optional group coupling, and a sampled spherical heat-kernel collision;
* positive reversible AFP generators used only as low-order solvers;
* a signed spectral Fokker--Planck comparator, never production-eligible.

The spherical heat-kernel family has continuum shell multipliers
``exp(-epsilon*l*(l+1))`` and becomes increasingly forward peaked as
``epsilon -> 0``.  It is used here as a controlled BFP/forward-peaked
manufactured family, not as a substitute for material cross sections.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
import math
from pathlib import Path
import resource
import time
import tracemalloc
from typing import Any, Iterable, Mapping

import numpy as np
from numpy.typing import ArrayLike, NDArray
from scipy import linalg, special

from .core import (
    IterationResult,
    defect_correction,
    preconditioned_gmres,
    slow_subspace_report,
    transport_mismatch_decomposition,
)

FloatArray = NDArray[np.float64]
IntArray = NDArray[np.int64]


@dataclass(frozen=True)
class GeneratorAudit:
    name: str
    h0_residual: float
    h1_residual: float
    reversibility_residual: float
    minimum_offdiagonal: float
    rate_max: float
    shell_defects: dict[int, float]
    positive: bool


@dataclass(frozen=True)
class HarmonicFrame:
    weighted_basis: FloatArray
    degrees: IntArray
    weights: FloatArray


@dataclass(frozen=True)
class MethodPerformance:
    name: str
    role: str
    positivity_expected: bool
    iterations: int
    high_order_matvecs: int
    low_order_solves: int
    setup_seconds: float
    solve_seconds: float
    total_seconds: float
    python_peak_bytes: int
    matrix_bytes: int
    preconditioner_bytes: int
    converged: bool
    final_high_order_residual: float
    solution_error: float
    relevant_slow_mode_contraction: float | None
    relevant_slow_mode_leakage: float | None


@dataclass(frozen=True)
class ForwardPeakedRow:
    epsilon: float
    first_moment: float
    diffusion_scale: float
    high_order_condition: float
    methods: dict[str, MethodPerformance]


def _strict_json(payload: object) -> str:
    return json.dumps(payload, sort_keys=True, separators=(",", ":"), allow_nan=False)


def _data_path() -> Path:
    return Path(__file__).with_name("p2d_frozen_operators.json")


def load_frozen_operator_data(path: str | Path | None = None) -> dict[str, Any]:
    source = _data_path() if path is None else Path(path)
    payload = json.loads(source.read_text(encoding="utf-8"), parse_constant=lambda value: (_ for _ in ()).throw(ValueError(value)))
    claimed = str(payload.pop("scientific_sha256"))
    actual = hashlib.sha256(_strict_json(payload).encode("utf-8")).hexdigest()
    payload["scientific_sha256"] = claimed
    if actual != claimed:
        raise ArithmeticError(f"frozen operator payload hash mismatch: {actual} != {claimed}")
    return payload


def generator_from_edges(
    weights: ArrayLike,
    edges: ArrayLike,
    conductance: ArrayLike,
) -> FloatArray:
    w = np.asarray(weights, dtype=float)
    e = np.asarray(edges, dtype=np.int64)
    gamma = np.asarray(conductance, dtype=float)
    if (
        w.ndim != 1
        or np.min(w) <= 0.0
        or abs(float(np.sum(w)) - 1.0) > 5e-12
        or e.ndim != 2
        or e.shape[1] != 2
        or gamma.shape != (len(e),)
        or np.min(gamma) < -2e-12
        or not np.all(np.isfinite(gamma))
    ):
        raise ValueError("invalid frozen generator arrays")
    gamma = np.maximum(gamma, 0.0)
    matrix = np.zeros((len(w), len(w)), dtype=float)
    for value, (i_raw, j_raw) in zip(gamma, e, strict=True):
        i, j = int(i_raw), int(j_raw)
        if not 0 <= i < len(w) or not 0 <= j < len(w) or i == j:
            raise ValueError(f"invalid edge {(i, j)}")
        matrix[i, j] += value / w[i]
        matrix[j, i] += value / w[j]
        matrix[i, i] -= value / w[i]
        matrix[j, j] -= value / w[j]
    return matrix


def dense_centered_generator(nodes: ArrayLike, weights: ArrayLike) -> FloatArray:
    """Positive complete-graph H0/H1-exact but deliberately H2-poor control."""

    x = np.asarray(nodes, dtype=float)
    w = np.asarray(weights, dtype=float)
    if np.linalg.norm(w @ x) > 2e-12:
        raise ValueError("dense centered formula requires a centered quadrature")
    n = len(w)
    matrix = np.zeros((n, n), dtype=float)
    for i in range(n):
        for j in range(i + 1, n):
            value = 2.0 * w[i] * w[j]
            matrix[i, j] += value / w[i]
            matrix[j, i] += value / w[j]
            matrix[i, i] -= value / w[i]
            matrix[j, j] -= value / w[j]
    return matrix


def real_harmonic_samples(nodes: ArrayLike, degree: int) -> FloatArray:
    x = np.asarray(nodes, dtype=float)
    if x.ndim != 2 or x.shape[1] != 3 or degree < 0:
        raise ValueError("invalid nodes or degree")
    polar = np.arccos(np.clip(x[:, 2], -1.0, 1.0))
    azimuth = np.mod(np.arctan2(x[:, 1], x[:, 0]), 2.0 * np.pi)
    columns: list[FloatArray] = [
        np.asarray(special.sph_harm_y(degree, 0, polar, azimuth).real, dtype=float)
    ]
    for order in range(1, degree + 1):
        value = special.sph_harm_y(degree, order, polar, azimuth)
        phase = (-1.0) ** order
        columns.append(np.asarray(math.sqrt(2.0) * phase * value.real, dtype=float))
        columns.append(np.asarray(math.sqrt(2.0) * phase * value.imag, dtype=float))
    return np.column_stack(columns)


def weighted_harmonic_frame(
    nodes: ArrayLike,
    weights: ArrayLike,
    *,
    maximum_degree: int = 12,
    tolerance: float = 1e-11,
) -> HarmonicFrame:
    """Build a complete W-orthonormal frame, preserving shell order.

    On a finite quadrature higher continuum shells can alias lower shells.  The
    sequential projection records only newly sampled directions at each
    degree; this makes the finite sampling boundary explicit.
    """

    x = np.asarray(nodes, dtype=float)
    w = np.asarray(weights, dtype=float)
    root = np.sqrt(w)
    columns: list[FloatArray] = []
    degrees: list[int] = []
    for degree in range(maximum_degree + 1):
        samples = np.ones((len(x), 1)) if degree == 0 else real_harmonic_samples(x, degree)
        weighted = root[:, None] * samples
        if columns:
            existing = np.column_stack(columns)
            weighted = weighted - existing @ (existing.T @ weighted)
            # A second pass controls loss of orthogonality near aliases.
            weighted = weighted - existing @ (existing.T @ weighted)
        u, singular, _ = np.linalg.svd(weighted, full_matrices=False)
        if singular.size and singular[0] > 0.0:
            rank = int(np.sum(singular > tolerance * singular[0]))
            for index in range(rank):
                columns.append(u[:, index])
                degrees.append(degree)
                if len(columns) == len(x):
                    break
        if len(columns) == len(x):
            break
    if len(columns) != len(x):
        raise ArithmeticError("harmonic samples did not span the nodal space")
    q = np.column_stack(columns)
    residual = float(np.linalg.norm(q.T @ q - np.eye(len(x)), ord=np.inf))
    if residual > 2e-10:
        raise ArithmeticError(f"weighted harmonic frame residual {residual:.3e}")
    return HarmonicFrame(q, np.asarray(degrees, dtype=np.int64), w.copy())


def weighted_spectral_operator(frame: HarmonicFrame, eigenvalues: ArrayLike) -> FloatArray:
    values = np.asarray(eigenvalues, dtype=float)
    if values.shape != frame.degrees.shape or not np.all(np.isfinite(values)):
        raise ValueError("one finite eigenvalue is required per frame column")
    root = np.sqrt(frame.weights)
    q = frame.weighted_basis
    # W^{-1/2} Q diag(values) Q^T W^{1/2}.
    return (q * values[None, :]) @ q.T * (root[None, :] / root[:, None])


def sampled_shell_defect(
    nodes: ArrayLike,
    weights: ArrayLike,
    generator: ArrayLike,
    degree: int,
) -> float:
    x = np.asarray(nodes, dtype=float)
    w = np.asarray(weights, dtype=float)
    matrix = np.asarray(generator, dtype=float)
    samples = real_harmonic_samples(x, degree)
    weighted = np.sqrt(w)[:, None] * samples
    _, singular, vh = np.linalg.svd(weighted, full_matrices=False)
    rank = int(np.sum(singular > 1e-11 * singular[0]))
    quotient = vh[:rank].T / singular[:rank]
    residual = np.sqrt(w)[:, None] * (
        matrix @ samples + degree * (degree + 1) * samples
    ) @ quotient
    return float(np.linalg.norm(residual, ord=2))


def audit_generator(
    name: str,
    nodes: ArrayLike,
    weights: ArrayLike,
    generator: ArrayLike,
    degrees: Iterable[int] = (2, 3, 4, 5, 6),
) -> GeneratorAudit:
    x = np.asarray(nodes, dtype=float)
    w = np.asarray(weights, dtype=float)
    matrix = np.asarray(generator, dtype=float)
    offdiagonal = matrix.copy()
    np.fill_diagonal(offdiagonal, np.inf)
    return GeneratorAudit(
        name,
        float(np.linalg.norm(matrix @ np.ones(len(w)), ord=np.inf)),
        float(np.linalg.norm(matrix @ x + 2.0 * x, ord=np.inf)),
        float(np.linalg.norm(w[:, None] * matrix - matrix.T * w[None, :], ord=np.inf)),
        float(np.min(offdiagonal)),
        float(np.max(-np.diag(matrix))),
        {int(degree): sampled_shell_defect(x, w, matrix, int(degree)) for degree in degrees},
        bool(np.min(offdiagonal) >= -2e-12),
    )


def load_generators() -> tuple[FloatArray, FloatArray, dict[str, FloatArray], dict[str, GeneratorAudit], dict[str, Any]]:
    payload = load_frozen_operator_data()
    nodes = np.asarray(payload["nodes"], dtype=float)
    weights = np.asarray(payload["weights"], dtype=float)
    generators: dict[str, FloatArray] = {}
    audits: dict[str, GeneratorAudit] = {}
    for name, method in payload["methods"].items():
        matrix = generator_from_edges(weights, method["edges"], method["gamma"])
        generators[name] = matrix
        audits[name] = audit_generator(name, nodes, weights, matrix)
    generators["h2_poor_positive"] = dense_centered_generator(nodes, weights)
    audits["h2_poor_positive"] = audit_generator(
        "h2_poor_positive", nodes, weights, generators["h2_poor_positive"]
    )
    return nodes, weights, generators, audits, payload


def exponential_forward_peaked_collision(
    frame: HarmonicFrame,
    epsilon: float,
    *,
    scattering_strength: float = 1.0,
) -> FloatArray:
    """Sample ``sigma_s (I-exp(epsilon Delta_S2))`` shellwise."""

    if epsilon <= 0.0 or scattering_strength <= 0.0:
        raise ValueError("epsilon and scattering_strength must be positive")
    degree = frame.degrees.astype(float)
    eigenvalues = scattering_strength * (
        1.0 - np.exp(-epsilon * degree * (degree + 1.0))
    )
    eigenvalues[frame.degrees == 0] = 0.0
    return weighted_spectral_operator(frame, eigenvalues)


def matched_fp_diffusion_scale(epsilon: float, scattering_strength: float = 1.0) -> float:
    """Match the exact first-shell removal ``1-exp(-2 epsilon)``."""

    if epsilon <= 0.0 or scattering_strength <= 0.0:
        raise ValueError("epsilon and scattering_strength must be positive")
    return float(scattering_strength * (1.0 - math.exp(-2.0 * epsilon)) / 2.0)


def classical_spectral_fp_collision(frame: HarmonicFrame, diffusion_scale: float) -> FloatArray:
    """Signed spectral Laplace--Beltrami comparator used only as a preconditioner."""

    if diffusion_scale <= 0.0:
        raise ValueError("diffusion_scale must be positive")
    degree = frame.degrees.astype(float)
    eigenvalues = diffusion_scale * degree * (degree + 1.0)
    eigenvalues[frame.degrees == 0] = 0.0
    return weighted_spectral_operator(frame, eigenvalues)


def _reflection_map(nodes: FloatArray, normal: FloatArray) -> IntArray:
    reflected = nodes - 2.0 * (nodes @ normal)[:, None] * normal[None, :]
    return np.argmax(reflected @ nodes.T, axis=1).astype(np.int64)


def upwind_streaming_and_boundary(
    nodes: ArrayLike,
    normal: ArrayLike,
    cells: int,
    width: float,
    *,
    left_albedo: float = 0.0,
    right_albedo: float = 0.0,
) -> tuple[FloatArray, FloatArray, FloatArray]:
    """Return interior upwind streaming, reflected-boundary block, and cosines."""

    x = np.asarray(nodes, dtype=float)
    n = np.asarray(normal, dtype=float)
    n /= np.linalg.norm(n)
    if cells <= 0 or width <= 0.0 or not 0.0 <= left_albedo <= 1.0 or not 0.0 <= right_albedo <= 1.0:
        raise ValueError("invalid slab or albedo data")
    mu = x @ n
    size = cells * len(x)
    streaming = np.zeros((size, size), dtype=float)
    boundary = np.zeros_like(streaming)
    reflect = _reflection_map(x, n)
    dx = width / cells
    for cell in range(cells):
        for angle, cosine in enumerate(mu):
            row = cell * len(x) + angle
            if cosine > 0.0:
                coefficient = cosine / dx
                streaming[row, row] += coefficient
                if cell > 0:
                    streaming[row, (cell - 1) * len(x) + angle] -= coefficient
                elif left_albedo > 0.0:
                    boundary[row, int(reflect[angle])] -= coefficient * left_albedo
            elif cosine < 0.0:
                coefficient = -cosine / dx
                streaming[row, row] += coefficient
                if cell + 1 < cells:
                    streaming[row, (cell + 1) * len(x) + angle] -= coefficient
                elif right_albedo > 0.0:
                    boundary[row, (cells - 1) * len(x) + int(reflect[angle])] -= coefficient * right_albedo
    return streaming, boundary, mu


def repeat_angular(matrix: ArrayLike, cells: int) -> FloatArray:
    return np.kron(np.eye(cells), np.asarray(matrix, dtype=float))


def h2_stress_mode(
    nodes: ArrayLike,
    weights: ArrayLike,
    optimized: ArrayLike,
    baseline: ArrayLike,
) -> tuple[FloatArray, dict[str, float]]:
    """Choose an H2 mode from operator data only, never transport outcomes."""

    x = np.asarray(nodes, dtype=float)
    w = np.asarray(weights, dtype=float)
    opt = np.asarray(optimized, dtype=float)
    base = np.asarray(baseline, dtype=float)
    samples = real_harmonic_samples(x, 2)
    weighted = np.sqrt(w)[:, None] * samples
    _, singular, vh = np.linalg.svd(weighted, full_matrices=False)
    rank = int(np.sum(singular > 1e-11 * singular[0]))
    quotient = vh[:rank].T / singular[:rank]
    r_opt = np.sqrt(w)[:, None] * (opt @ samples + 6.0 * samples) @ quotient
    r_base = np.sqrt(w)[:, None] * (base @ samples + 6.0 * samples) @ quotient
    difference = r_base.T @ r_base - r_opt.T @ r_opt
    eigenvalues, vectors = np.linalg.eigh(0.5 * (difference + difference.T))
    coefficient = vectors[:, -1]
    mode = samples @ quotient @ coefficient
    norm = float(np.sqrt(np.sum(w * mode**2)))
    mode /= norm
    return mode, {
        "selection_eigenvalue": float(eigenvalues[-1]),
        "optimized_h2_residual": float(np.linalg.norm(r_opt @ coefficient)),
        "baseline_h2_residual": float(np.linalg.norm(r_base @ coefficient)),
        "selection_uses_transport_results": False,
    }


def _profile_gmres(
    name: str,
    role: str,
    positivity_expected: bool,
    high: FloatArray,
    rhs: FloatArray,
    exact: FloatArray,
    low: FloatArray | None,
    slow_basis: FloatArray | None,
) -> MethodPerformance:
    tracemalloc.start()
    wall_start = time.perf_counter()
    result = preconditioned_gmres(
        high,
        rhs,
        low_order=low,
        rtol=1e-10,
        atol=1e-13,
        restart=20,
        max_iterations=300,
    )
    total = time.perf_counter() - wall_start
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    contraction: float | None = None
    leakage: float | None = None
    if low is not None and slow_basis is not None:
        slow = slow_subspace_report(high, low, slow_basis)
        contraction = slow.contraction_norm
        leakage = slow.invariance_leakage
    return MethodPerformance(
        name,
        role,
        positivity_expected,
        result.iterations,
        result.matvecs,
        result.low_solves,
        result.setup_seconds,
        result.solve_seconds,
        total,
        int(peak),
        int(high.nbytes + (0 if low is None else low.nbytes)),
        result.preconditioner_bytes,
        result.converged,
        result.final_residual,
        float(np.linalg.norm(result.solution - exact)),
        contraction,
        leakage,
    )


def forward_peaked_sweep(
    *,
    epsilons: Iterable[float] = (0.04, 0.02, 0.01, 0.005),
) -> dict[str, Any]:
    nodes, weights, generators, audits, payload = load_generators()
    frame = weighted_harmonic_frame(nodes, weights)
    cells = 6
    width = 30.0
    absorption = 5e-4
    scattering = 1.0
    streaming, boundary, _ = upwind_streaming_and_boundary(
        nodes, np.asarray([1.0, 0.0, 0.0]), cells, width
    )
    mode, mode_selection = h2_stress_mode(
        nodes,
        weights,
        generators["optimized_harmonic_fidelity"],
        generators["moment_monotone_baseline"],
    )
    spatial_profile = np.zeros(cells)
    spatial_profile[cells // 2 - 1] = 1.0
    rhs = np.kron(spatial_profile, mode)
    slow_basis = np.kron(np.ones(cells) / math.sqrt(cells), mode)[:, None]
    zero = np.zeros_like(streaming)
    rows: list[ForwardPeakedRow] = []
    decomposition: dict[str, Any] | None = None

    for epsilon_raw in epsilons:
        epsilon = float(epsilon_raw)
        high_collision = exponential_forward_peaked_collision(
            frame, epsilon, scattering_strength=scattering
        )
        diffusion = matched_fp_diffusion_scale(epsilon, scattering)
        classical_collision = classical_spectral_fp_collision(frame, diffusion)
        high_angular = repeat_angular(high_collision + absorption * np.eye(len(nodes)), cells)
        high = streaming + boundary + high_angular
        exact = linalg.solve(high, rhs, assume_a="gen")
        low_angular: dict[str, FloatArray] = {
            "optimized_harmonic_fidelity": repeat_angular(
                -diffusion * generators["optimized_harmonic_fidelity"]
                + absorption * np.eye(len(nodes)), cells
            ),
            "moment_monotone_baseline": repeat_angular(
                -diffusion * generators["moment_monotone_baseline"]
                + absorption * np.eye(len(nodes)), cells
            ),
            "classical_modified_fp": repeat_angular(
                classical_collision + absorption * np.eye(len(nodes)), cells
            ),
            "h2_poor_positive": repeat_angular(
                -diffusion * generators["h2_poor_positive"]
                + absorption * np.eye(len(nodes)), cells
            ),
        }
        lows = {name: streaming + boundary + value for name, value in low_angular.items()}
        methods = {
            "none": _profile_gmres(
                "none", "unpreconditioned high-order GMRES", True,
                high, rhs, exact, None, None,
            ),
            "optimized_harmonic_fidelity": _profile_gmres(
                "optimized_harmonic_fidelity",
                "positive reversible optimized AFP preconditioner",
                True,
                high, rhs, exact, lows["optimized_harmonic_fidelity"], slow_basis,
            ),
            "moment_monotone_baseline": _profile_gmres(
                "moment_monotone_baseline",
                "same-node moment-preserving monotone AFP baseline",
                True,
                high, rhs, exact, lows["moment_monotone_baseline"], slow_basis,
            ),
            "classical_modified_fp": _profile_gmres(
                "classical_modified_fp",
                "signed spectral modified-FP/FPSA comparator",
                False,
                high, rhs, exact, lows["classical_modified_fp"], slow_basis,
            ),
            "h2_poor_positive": _profile_gmres(
                "h2_poor_positive",
                "deliberately H2-poor positive complete-graph generator",
                True,
                high, rhs, exact, lows["h2_poor_positive"], slow_basis,
            ),
        }
        if decomposition is None:
            decomposition = asdict(transport_mismatch_decomposition(
                high,
                lows["optimized_harmonic_fidelity"],
                angular_high=high_angular,
                angular_low=low_angular["optimized_harmonic_fidelity"],
                streaming_high=streaming,
                streaming_low=streaming,
                energy_high=zero,
                energy_low=zero,
                boundary_high=boundary,
                boundary_low=boundary,
            ))
        rows.append(ForwardPeakedRow(
            epsilon,
            math.exp(-2.0 * epsilon),
            diffusion,
            float(np.linalg.cond(high)),
            methods,
        ))

    optimized_iterations = [row.methods["optimized_harmonic_fidelity"].iterations for row in rows]
    baseline_iterations = [row.methods["moment_monotone_baseline"].iterations for row in rows]
    none_iterations = [row.methods["none"].iterations for row in rows]
    reductions = [
        1.0 - optimized / baseline
        for optimized, baseline in zip(optimized_iterations, baseline_iterations, strict=True)
    ]
    return {
        "schema": "afp-p2d-forward-peaked-sweep-v1",
        "high_order_family": "sampled spherical heat-kernel/BFP collision with exact shell multipliers exp(-epsilon*l(l+1))",
        "same_high_order_discretization_per_row": True,
        "same_stopping_rule_per_row": True,
        "spatial_cells": cells,
        "direction_count": len(nodes),
        "width": width,
        "absorption": absorption,
        "operator_registry_sha256": payload["scientific_sha256"],
        "mode_selection": mode_selection,
        "generator_audits": {name: asdict(value) for name, value in audits.items()},
        "mismatch_decomposition": decomposition,
        "rows": [
            {
                **{key: value for key, value in asdict(row).items() if key != "methods"},
                "methods": {name: asdict(value) for name, value in row.methods.items()},
            }
            for row in rows
        ],
        "summary": {
            "optimized_beats_baseline_every_forward_peaked_row": all(
                optimized < baseline
                for optimized, baseline in zip(optimized_iterations, baseline_iterations, strict=True)
            ),
            "optimized_beats_no_acceleration_every_row": all(
                optimized < none
                for optimized, none in zip(optimized_iterations, none_iterations, strict=True)
            ),
            "minimum_iteration_reduction_vs_baseline": float(min(reductions)),
            "geometric_mean_iteration_ratio_vs_baseline": float(
                math.exp(np.mean(np.log(np.asarray(optimized_iterations) / np.asarray(baseline_iterations))))
            ),
            "signed_classical_comparator_is_not_production_eligible": True,
        },
    }


def higher_shell_adversary() -> dict[str, Any]:
    """Expose a degree-seven slow mode for which H2 is not the controller."""

    nodes, weights, generators, audits, _ = load_generators()
    frame = weighted_harmonic_frame(nodes, weights)
    indices = np.where(frame.degrees == 7)[0]
    if len(indices) == 0:
        raise ArithmeticError("the frozen frame has no new degree-seven direction")
    root = np.sqrt(weights)
    mode = frame.weighted_basis[:, int(indices[0])] / root
    mode /= math.sqrt(float(np.sum(weights * mode**2)))
    target = 56.0
    rows = {}
    for name in ("optimized_harmonic_fidelity", "moment_monotone_baseline", "h2_poor_positive"):
        action = -generators[name] @ mode
        rayleigh = float(np.sum(weights * mode * action))
        mismatch = float(math.sqrt(np.sum(weights * (action - target * mode) ** 2)))
        rows[name] = {
            "degree_two_defect": audits[name].shell_defects[2],
            "degree_seven_rayleigh": rayleigh,
            "degree_seven_mismatch": mismatch,
        }
    classical_mismatch = 0.0
    return {
        "schema": "afp-p2d-higher-shell-adversary-v1",
        "sampled_degree": 7,
        "target_eigenvalue": target,
        "rows": rows,
        "classical_spectral_fp_degree_seven_mismatch": classical_mismatch,
        "h2_metric_is_controller": False,
        "reason": "the source and declared slow direction are degree seven; the relevant mismatch is degree seven, not D2",
    }


def ray_dominated_adversary() -> dict[str, Any]:
    """Analytic ballistic case where fixed-quadrature ray error dominates."""

    nodes, _, generators, audits, _ = load_generators()
    normal = np.asarray([1.0, 0.0, 0.0])
    mu_true = 0.1
    azimuth = 2.5656340004316642
    direction = np.asarray([
        mu_true,
        math.sqrt(1.0 - mu_true**2) * math.cos(azimuth),
        math.sqrt(1.0 - mu_true**2) * math.sin(azimuth),
    ])
    incoming = np.where(nodes @ normal > 0.0)[0]
    nearest = int(incoming[np.argmax(nodes[incoming] @ direction)])
    mu_discrete = float(nodes[nearest] @ normal)
    optical_thickness = 0.2
    reference = math.exp(-optical_thickness / mu_true)
    discrete = math.exp(-optical_thickness / mu_discrete)
    relative_error = abs(discrete - reference) / reference
    return {
        "schema": "afp-p2d-ray-adversary-v1",
        "true_incidence_cosine": mu_true,
        "nearest_discrete_direction": nearest,
        "discrete_incidence_cosine": mu_discrete,
        "optical_thickness": optical_thickness,
        "analytic_ballistic_transmission": reference,
        "fixed_quadrature_ballistic_transmission": discrete,
        "relative_ray_error": relative_error,
        "optimized_h2_defect": audits["optimized_harmonic_fidelity"].shell_defects[2],
        "baseline_h2_defect": audits["moment_monotone_baseline"].shell_defects[2],
        "low_operator_can_change_converged_high_order_ray_error": False,
        "reason": "all fixed-point-preserving preconditioners converge to the same coarse high-order discrete-ordinates solution; quadrature refinement or a separately audited ray remedy is required",
    }


def multigroup_boundary_case() -> dict[str, Any]:
    """Two-group noncommuting case with downscatter and reflective boundaries."""

    nodes, weights, generators, _, _ = load_generators()
    frame = weighted_harmonic_frame(nodes, weights)
    cells = 2
    streaming, boundary, _ = upwind_streaming_and_boundary(
        nodes,
        np.asarray([1.0, 0.0, 0.0]),
        cells,
        3.0,
        left_albedo=0.15,
        right_albedo=0.05,
    )
    epsilon = 0.02
    diffusion = matched_fp_diffusion_scale(epsilon)
    high_collision = exponential_forward_peaked_collision(frame, epsilon)
    angular_high = streaming + boundary + repeat_angular(high_collision + 0.02 * np.eye(len(nodes)), cells)
    angular_opt = streaming + boundary + repeat_angular(
        -diffusion * generators["optimized_harmonic_fidelity"] + 0.02 * np.eye(len(nodes)), cells
    )
    block = len(angular_high)
    coupling = 0.035 * np.eye(block)
    high = np.block([[angular_high, np.zeros((block, block))], [-coupling, angular_high + 0.04 * np.eye(block)]])
    low = np.block([[angular_opt, np.zeros((block, block))], [-coupling, angular_opt + 0.04 * np.eye(block)]])
    rhs = np.zeros(2 * block)
    rhs[: len(nodes)] = 1.0
    exact = linalg.solve(high, rhs)
    performance = _profile_gmres(
        "optimized_harmonic_fidelity",
        "positive optimized preconditioner with retained group and boundary blocks",
        True,
        high,
        rhs,
        exact,
        low,
        None,
    )
    commutator = angular_opt @ coupling - coupling @ angular_opt
    return {
        "schema": "afp-p2d-multigroup-boundary-v1",
        "performance": asdict(performance),
        "group_coupling_norm": float(np.linalg.norm(coupling, ord=2)),
        "boundary_block_norm": float(np.linalg.norm(boundary, ord=2)),
        "angular_group_commutator_norm": float(np.linalg.norm(commutator, ord=2)),
        "full_blocks_retained_in_low_operator": True,
    }


def complete_transport_audit() -> dict[str, Any]:
    sweep = forward_peaked_sweep()
    higher = higher_shell_adversary()
    ray = ray_dominated_adversary()
    multigroup = multigroup_boundary_case()
    generator_pass = all(
        row["h0_residual"] < 2e-10
        and row["h1_residual"] < 2e-10
        and row["reversibility_residual"] < 2e-10
        and row["positive"]
        for row in sweep["generator_audits"].values()
    )
    all_converged = all(
        method["converged"]
        for row in sweep["rows"]
        for method in row["methods"].values()
    )
    passed = bool(
        generator_pass
        and all_converged
        and sweep["summary"]["optimized_beats_baseline_every_forward_peaked_row"]
        and sweep["summary"]["optimized_beats_no_acceleration_every_row"]
        and higher["h2_metric_is_controller"] is False
        and ray["relative_ray_error"] > 1.0
        and multigroup["performance"]["converged"]
        and sweep["mismatch_decomposition"]["decomposition_residual"] < 1e-10
    )
    return {
        "schema": "afp-p2d-complete-transport-audit-v1",
        "status": "PASS" if passed else "FAIL",
        "checks": {
            "positive_generator_invariants": generator_pass,
            "all_comparators_converged": all_converged,
            "forward_peaked_optimized_beats_baseline": sweep["summary"]["optimized_beats_baseline_every_forward_peaked_row"],
            "forward_peaked_optimized_beats_none": sweep["summary"]["optimized_beats_no_acceleration_every_row"],
            "higher_shell_failure_exposed": higher["h2_metric_is_controller"] is False,
            "ray_error_dominates": ray["relative_ray_error"] > 1.0,
            "multigroup_boundary_converged": multigroup["performance"]["converged"],
            "transport_decomposition_exact": sweep["mismatch_decomposition"]["decomposition_residual"] < 1e-10,
        },
        "forward_peaked_sweep": sweep,
        "higher_shell_adversary": higher,
        "ray_dominated_adversary": ray,
        "multigroup_boundary_case": multigroup,
        "process_peak_rss_bytes": int(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss * 1024),
    }

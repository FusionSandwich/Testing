"""All-orders Paper-I sandwich and reproducible finite benchmarks."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from importlib.metadata import PackageNotFoundError, version as distribution_version
import math
import resource
import sys
import time
import tracemalloc
from typing import Iterable

import numpy as np

from .families import reflected_ring_candidate
from .inner import solve_global_inner
from .metrics import generator_report, sampling_reports
from .rotations import collision_rotation_spread, signed_permutation_rotations
from .types import canonical_array_sha256


PAPER_I_RATE_CONSTANT = 64.0 * math.pi**2
PAPER_I_UPPER_CONSTANT = 75.0 / 2.0
PAPER_I_LOWER_CONSTANT = 3.0 / (32.0 * math.pi**2)


@dataclass(frozen=True)
class TheoremSandwich:
    h: float
    lower: float
    upper: float
    rate_cap: float

    def contains(self, defect: float, tolerance: float = 2e-7) -> bool:
        scale = max(1.0, abs(defect), abs(self.upper))
        return self.lower - tolerance * scale <= defect <= self.upper + tolerance * scale


def paper_i_sandwich(h: float) -> TheoremSandwich:
    if not np.isfinite(h) or h <= 0:
        raise ValueError("h must be finite and positive")
    return TheoremSandwich(
        float(h),
        PAPER_I_LOWER_CONSTANT * h**2,
        PAPER_I_UPPER_CONSTANT * h**2,
        PAPER_I_RATE_CONSTANT / h**2,
    )


@dataclass(frozen=True)
class ConvergenceRow:
    M0: int
    J: int
    node_count: int
    edge_count: int
    h: float
    defect2: float
    rate_max: float
    sampling_condition2: float
    shell_defect3: float
    shell_defect4: float
    sampled_collision_spread_24: float
    theorem_lower: float
    theorem_upper: float
    inner_solve_seconds: float
    benchmark_wall_seconds: float
    process_peak_rss_bytes: int
    python_tracemalloc_peak_bytes: int
    inner_python_tracemalloc_peak_bytes: int
    memory_scope: str
    optimized_inner: bool
    input_sha256: str
    conductance_sha256: str
    solver: str
    solver_version: str
    solver_status: str
    inner_objective_lower: float | None
    inner_objective_upper: float | None
    inner_duality_gap: float | None
    inner_certificate_level: str
    inner_primal_passed: bool | None
    inner_dual_passed: bool | None
    verification: str

    def serializable(self) -> dict[str, int | float | bool | str | None]:
        return asdict(self)


def _process_peak_rss_bytes() -> int:
    value = int(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    return value if sys.platform == "darwin" else value * 1024


def benchmark_reflected_ring_level(
    M0: int,
    J: int,
    *,
    optimize_inner: bool,
    solver: str = "CLARABEL",
) -> ConvergenceRow:
    """Benchmark one finite P1E specialization.

    The finite row is regression evidence.  The all-orders order claim comes
    from paper_i_sandwich and the accepted P1B/P1E theorems.
    """

    tracemalloc.start()
    started = time.perf_counter()
    try:
        candidate = reflected_ring_candidate(M0, J)
        h = float(candidate.metadata["h"])
        theorem = paper_i_sandwich(h)
        if candidate.seed_conductance is None:
            raise AssertionError("reflected-ring adapter lost its constructive conductance")
        input_sha256 = canonical_array_sha256({
            "nodes": candidate.nodes,
            "weights": candidate.weights,
            "edges": candidate.edges,
            "rate_cap": np.asarray([theorem.rate_cap]),
        })
        gamma = candidate.seed_conductance
        optimized = False
        inner_seconds = 0.0
        inner_peak = 0
        solver_name = "NOT_RUN"
        solver_version = "NOT_RUN"
        solver_status = "NOT_RUN"
        objective_lower = None
        objective_upper = None
        objective_gap = None
        certificate_level = "NOT_RUN"
        primal_passed = None
        dual_passed = None
        if optimize_inner:
            inner = solve_global_inner(
                candidate, theorem.rate_cap, degree=2, solver=solver
            )
            if inner.result.gamma is None:
                raise AssertionError("verified inner solve returned no conductance")
            verification = inner.result.verification
            if (
                verification is None
                or verification.objective_interval is None
                or verification.dual_passed is not True
            ):
                raise AssertionError(
                    "inner solve lacks a verified primal-dual objective enclosure"
                )
            gamma = inner.result.gamma
            optimized = True
            inner_seconds = inner.elapsed_seconds
            inner_peak = inner.python_tracemalloc_peak_bytes
            solver_name = str(inner.result.solver)
            try:
                solver_version = distribution_version(solver_name)
            except PackageNotFoundError:
                solver_version = "UNKNOWN_DISTRIBUTION_VERSION"
            solver_status = str(inner.result.status)
            objective_lower, objective_upper = map(
                float, verification.objective_interval
            )
            objective_gap = objective_upper - objective_lower
            certificate_level = str(verification.certificate_level)
            primal_passed = bool(verification.primal_passed)
            dual_passed = bool(verification.dual_passed)
        report = generator_report(candidate, gamma, (2, 3, 4))
        condition = sampling_reports(candidate, (2,))[0].gram_condition
        rotation = collision_rotation_spread(
            candidate,
            gamma,
            np.asarray([1.0, -0.5, 0.25, 0.0, 0.75]),
            signed_permutation_rotations(),
        )
        elapsed = time.perf_counter() - started
        _, peak = tracemalloc.get_traced_memory()
        process_peak = _process_peak_rss_bytes()
    finally:
        tracemalloc.stop()
    defect = report.shell_defects[2]
    scale = max(1.0, theorem.upper)
    if defect < theorem.lower - 3e-7 * scale:
        raise AssertionError("finite result violates the Paper-I lower frontier")
    if defect > theorem.upper + 3e-5 * scale:
        raise AssertionError("finite incumbent exceeds the accepted P1E upper constant")
    if report.rate_max > theorem.rate_cap * (1.0 + 3e-7):
        raise AssertionError("finite result violates the Paper-I rate cap")
    if report.h1_residual > 5e-8:
        raise AssertionError("finite result lost exact H1 beyond regression tolerance")
    return ConvergenceRow(
        int(M0), int(J), candidate.node_count, candidate.edge_count, h,
        defect, report.rate_max, condition,
        report.shell_defects[3], report.shell_defects[4],
        rotation.absolute_spread,
        theorem.lower, theorem.upper,
        inner_seconds,
        float(elapsed),
        int(process_peak),
        int(peak),
        int(inner_peak),
        "PROCESS_MAX_RSS_AND_PYTHON_TRACEMALLOC_BYTES",
        optimized,
        input_sha256,
        canonical_array_sha256({"conductance": gamma}),
        solver_name,
        solver_version,
        solver_status,
        objective_lower,
        objective_upper,
        objective_gap,
        certificate_level,
        primal_passed,
        dual_passed,
        "VERIFIED_FLOAT_FINITE_REGRESSION+EMPIRICAL_ROTATION_SAMPLE",
    )


def benchmark_reflected_ring_family(
    levels: Iterable[tuple[int, int]] = ((32, 1), (32, 2), (32, 3), (64, 1)),
    *,
    optimize_indices: Iterable[int] = (0,),
    solver: str = "CLARABEL",
) -> tuple[ConvergenceRow, ...]:
    selected = set(map(int, optimize_indices))
    return tuple(
        benchmark_reflected_ring_level(
            M0, J, optimize_inner=index in selected, solver=solver
        )
        for index, (M0, J) in enumerate(levels)
    )


def fitted_log_slope(rows: Iterable[ConvergenceRow]) -> float:
    """Supplementary finite slope; never returned as the theorem."""

    data = tuple(rows)
    if len(data) < 2:
        raise ValueError("at least two rows are needed for a fitted slope")
    x = np.log([row.h for row in data])
    y = np.log([row.defect2 for row in data])
    return float(np.polyfit(x, y, 1)[0])


def certified_pair_slope_interval(
    h_coarse: float,
    h_fine: float,
    coarse_interval: tuple[float, float],
    fine_interval: tuple[float, float],
) -> tuple[float, float]:
    if not 0 < h_fine < h_coarse:
        raise ValueError("mesh scales must be positive and decreasing")
    lc, uc = coarse_interval
    lf, uf = fine_interval
    if not 0 < lc <= uc or not 0 < lf <= uf:
        raise ValueError("defect intervals must be positive")
    denominator = math.log(h_coarse / h_fine)
    return (
        math.log(lc / uf) / denominator,
        math.log(uc / lf) / denominator,
    )

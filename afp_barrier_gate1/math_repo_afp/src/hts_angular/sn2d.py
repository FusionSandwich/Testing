"""Verified Cartesian finite-volume S_N prototype for angular benchmarks."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Mapping
import warnings

import numpy as np
from numpy.typing import ArrayLike, NDArray
from scipy.sparse import csr_matrix, lil_matrix
from scipy.sparse.linalg import MatrixRankWarning, spsolve

from .graph_generator import GraphGenerator
from .quadrature import PositiveQuadrature

FloatArray = NDArray[np.float64]


def circle_quadrature(n: int, phase: float = 0.0) -> PositiveQuadrature:
    if int(n) != n or n < 2:
        raise ValueError("at least two integer-valued directions are required")
    if not np.isfinite(phase):
        raise ValueError("phase must be finite")
    n = int(n)
    phi = 2.0 * np.pi * (np.arange(n) + phase) / n
    nodes = np.column_stack([np.cos(phi), np.sin(phi), np.zeros(n)])
    return PositiveQuadrature(nodes, np.full(n, 2.0 * np.pi / n), {"family": "uniform circle", "phase": phase})


@dataclass(frozen=True)
class CartesianGrid2D:
    x_edges: FloatArray
    y_edges: FloatArray

    def __post_init__(self) -> None:
        x = np.asarray(self.x_edges, dtype=float).reshape(-1)
        y = np.asarray(self.y_edges, dtype=float).reshape(-1)
        if (
            x.size < 2
            or y.size < 2
            or np.any(~np.isfinite(x))
            or np.any(~np.isfinite(y))
            or np.any(np.diff(x) <= 0.0)
            or np.any(np.diff(y) <= 0.0)
        ):
            raise ValueError("grid edges must be finite and strictly increasing")
        object.__setattr__(self, "x_edges", x)
        object.__setattr__(self, "y_edges", y)

    @property
    def nx(self) -> int:
        return self.x_edges.size - 1

    @property
    def ny(self) -> int:
        return self.y_edges.size - 1

    @property
    def dx(self) -> FloatArray:
        return np.diff(self.x_edges)

    @property
    def dy(self) -> FloatArray:
        return np.diff(self.y_edges)

    @property
    def x_centers(self) -> FloatArray:
        return 0.5 * (self.x_edges[:-1] + self.x_edges[1:])

    @property
    def y_centers(self) -> FloatArray:
        return 0.5 * (self.y_edges[:-1] + self.y_edges[1:])

    @property
    def cell_areas(self) -> FloatArray:
        return self.dx[:, None] * self.dy[None, :]


@dataclass(frozen=True)
class BoundaryData2D:
    left: FloatArray
    right: FloatArray
    bottom: FloatArray
    top: FloatArray

    @classmethod
    def zeros(cls, n_group: int, n_angle: int, grid: CartesianGrid2D) -> "BoundaryData2D":
        return cls(
            np.zeros((n_group, n_angle, grid.ny)),
            np.zeros((n_group, n_angle, grid.ny)),
            np.zeros((n_group, n_angle, grid.nx)),
            np.zeros((n_group, n_angle, grid.nx)),
        )


@dataclass(frozen=True)
class SN2DProblem:
    grid: CartesianGrid2D
    quadrature: PositiveQuadrature
    sigma_t: FloatArray
    sigma_s: FloatArray
    source: FloatArray
    boundary: BoundaryData2D
    response_kernels: Mapping[str, FloatArray] = field(default_factory=dict)
    graph: GraphGenerator | None = None
    angular_diffusion: float | FloatArray = 0.0

    def __post_init__(self) -> None:
        na, nx, ny = self.quadrature.n_node, self.grid.nx, self.grid.ny
        st = np.asarray(self.sigma_t, dtype=float)
        if st.ndim != 3 or st.shape[1:] != (nx, ny) or st.shape[0] < 1:
            raise ValueError("sigma_t must have shape (group,x,y)")
        ng = st.shape[0]
        ss = np.asarray(self.sigma_s, dtype=float)
        q = np.asarray(self.source, dtype=float)
        if ss.shape != (ng, ng, nx, ny) or q.shape != (ng, na, nx, ny):
            raise ValueError("transport coefficient/source shapes are inconsistent")
        if (
            np.any(~np.isfinite(st))
            or np.any(~np.isfinite(ss))
            or np.any(~np.isfinite(q))
            or np.any(st < 0.0)
            or np.any(ss < 0.0)
            or np.any(q < 0.0)
        ):
            raise ValueError("physical coefficients and sources must be finite and nonnegative")
        if np.any(np.sum(ss, axis=1) - st > 1e-12 * np.maximum(1.0, st)):
            raise ValueError("out-scattering cannot exceed total cross section")
        expected_boundary = (
            (ng, na, ny),
            (ng, na, ny),
            (ng, na, nx),
            (ng, na, nx),
        )
        boundary_values = []
        for arr, shape in zip(
            (
                self.boundary.left,
                self.boundary.right,
                self.boundary.bottom,
                self.boundary.top,
            ),
            expected_boundary,
            strict=True,
        ):
            value = np.asarray(arr, dtype=float)
            if (
                value.shape != shape
                or np.any(~np.isfinite(value))
                or np.any(value < 0.0)
            ):
                raise ValueError(
                    "boundary arrays must be finite, nonnegative, and correctly shaped"
                )
            boundary_values.append(value)
        kernels = {
            str(name): np.asarray(kernel, dtype=float)
            for name, kernel in self.response_kernels.items()
        }
        for name, kernel in kernels.items():
            if kernel.shape != (ng, na, nx, ny) or np.any(~np.isfinite(kernel)):
                raise ValueError(
                    f"response kernel {name!r} must be finite with shape (group,angle,x,y)"
                )
        if self.graph is not None and (
            self.graph.weights.shape != self.quadrature.weights.shape
            or not np.allclose(
                self.graph.weights, self.quadrature.weights, rtol=1e-12, atol=1e-14
            )
            or not np.allclose(
                self.graph.nodes, self.quadrature.nodes, rtol=1e-12, atol=1e-14
            )
        ):
            raise ValueError("angular graph nodes and weights must align with quadrature")
        diffusion = np.asarray(self.angular_diffusion, dtype=float)
        if (
            (diffusion.ndim != 0 and diffusion.shape != st.shape)
            or np.any(~np.isfinite(diffusion))
            or np.any(diffusion < 0.0)
        ):
            raise ValueError(
                "angular_diffusion must be finite, nonnegative, and scalar or shaped like sigma_t"
            )
        object.__setattr__(self, "sigma_t", st)
        object.__setattr__(self, "sigma_s", ss)
        object.__setattr__(self, "source", q)
        object.__setattr__(
            self,
            "boundary",
            BoundaryData2D(*boundary_values),
        )
        object.__setattr__(self, "response_kernels", kernels)
        object.__setattr__(
            self, "angular_diffusion", float(diffusion) if diffusion.ndim == 0 else diffusion
        )

    @property
    def n_group(self) -> int:
        return int(self.sigma_t.shape[0])

    @property
    def n_unknown(self) -> int:
        return self.n_group * self.quadrature.n_node * self.grid.nx * self.grid.ny


@dataclass(frozen=True)
class SN2DSolution:
    angular_flux: FloatArray
    responses: dict[str, float]
    iterations: int
    converged: bool
    residual_norm: float


def _index(problem: SN2DProblem, g: int, a: int, i: int, j: int) -> int:
    na, nx, ny = problem.quadrature.n_node, problem.grid.nx, problem.grid.ny
    return (((g * na + a) * nx + i) * ny + j)


def _angular_diffusion_value(problem: SN2DProblem, g: int, i: int, j: int) -> float:
    d = np.asarray(problem.angular_diffusion, dtype=float)
    if d.ndim == 0:
        return float(d)
    if d.shape == problem.sigma_t.shape:
        return float(d[g, i, j])
    raise ValueError("angular_diffusion must be scalar or shaped like sigma_t")


def assemble_system(problem: SN2DProblem, include_scattering: bool = True) -> tuple[csr_matrix, FloatArray]:
    ng, na, nx, ny = problem.n_group, problem.quadrature.n_node, problem.grid.nx, problem.grid.ny
    A = lil_matrix((problem.n_unknown, problem.n_unknown), dtype=float)
    b = problem.source.reshape(-1).copy()
    directions = problem.quadrature.nodes[:, :2]
    angular_mass = float(np.sum(problem.quadrature.weights))
    for g in range(ng):
        for a, (ox, oy) in enumerate(directions):
            for i in range(nx):
                for j in range(ny):
                    row = _index(problem, g, a, i, j)
                    dx, dy = problem.grid.dx[i], problem.grid.dy[j]
                    diag = problem.sigma_t[g, i, j] + abs(ox) / dx + abs(oy) / dy
                    A[row, row] += diag
                    if ox > 0.0:
                        if i > 0:
                            A[row, _index(problem, g, a, i - 1, j)] -= ox / dx
                        else:
                            b[row] += ox / dx * problem.boundary.left[g, a, j]
                    elif ox < 0.0:
                        if i < nx - 1:
                            A[row, _index(problem, g, a, i + 1, j)] -= -ox / dx
                        else:
                            b[row] += -ox / dx * problem.boundary.right[g, a, j]
                    if oy > 0.0:
                        if j > 0:
                            A[row, _index(problem, g, a, i, j - 1)] -= oy / dy
                        else:
                            b[row] += oy / dy * problem.boundary.bottom[g, a, i]
                    elif oy < 0.0:
                        if j < ny - 1:
                            A[row, _index(problem, g, a, i, j + 1)] -= -oy / dy
                        else:
                            b[row] += -oy / dy * problem.boundary.top[g, a, i]
                    if problem.graph is not None:
                        diffusion = _angular_diffusion_value(problem, g, i, j)
                        if diffusion:
                            for ap in range(na):
                                A[row, _index(problem, g, ap, i, j)] -= diffusion * problem.graph.generator[a, ap]
                    if include_scattering:
                        for gin in range(ng):
                            sigma = problem.sigma_s[gin, g, i, j]
                            if sigma:
                                for ap in range(na):
                                    A[row, _index(problem, gin, ap, i, j)] -= sigma * problem.quadrature.weights[ap] / angular_mass
    return A.tocsr(), b


def _reshape(problem: SN2DProblem, vector: FloatArray) -> FloatArray:
    return vector.reshape(problem.n_group, problem.quadrature.n_node, problem.grid.nx, problem.grid.ny)


def compute_responses(problem: SN2DProblem, angular_flux: FloatArray) -> dict[str, float]:
    area = problem.grid.cell_areas
    weights = problem.quadrature.weights
    return {
        name: float(np.einsum("gaij,gaij,a,ij->", kernel, angular_flux, weights, area))
        for name, kernel in problem.response_kernels.items()
    }


def _checked_sparse_solve(matrix: csr_matrix, rhs: FloatArray) -> FloatArray:
    with warnings.catch_warnings():
        warnings.simplefilter("error", MatrixRankWarning)
        try:
            vector = np.asarray(spsolve(matrix, rhs), dtype=float)
        except MatrixRankWarning as exc:
            raise np.linalg.LinAlgError("transport matrix is singular") from exc
    if vector.shape != rhs.shape or np.any(~np.isfinite(vector)):
        raise np.linalg.LinAlgError("sparse transport solve returned nonfinite values")
    return vector


def solve_direct(
    problem: SN2DProblem, residual_tolerance: float = 1e-9
) -> SN2DSolution:
    if not np.isfinite(residual_tolerance) or residual_tolerance <= 0.0:
        raise ValueError("residual_tolerance must be finite and positive")
    A, b = assemble_system(problem, include_scattering=True)
    vector = _checked_sparse_solve(A, b)
    residual = float(np.linalg.norm(A @ vector - b))
    relative = residual / max(float(np.linalg.norm(b)), 1.0)
    flux = _reshape(problem, vector)
    return SN2DSolution(
        flux,
        compute_responses(problem, flux),
        1,
        relative <= residual_tolerance,
        residual,
    )


def _scattering_source(problem: SN2DProblem, flux: FloatArray) -> FloatArray:
    angular_mass = float(np.sum(problem.quadrature.weights))
    phi = np.einsum("gaij,a->gij", flux, problem.quadrature.weights)
    out = np.zeros_like(flux)
    for gin in range(problem.n_group):
        for gout in range(problem.n_group):
            out[gout] += problem.sigma_s[gin, gout][None, :, :] * phi[gin][None, :, :] / angular_mass
    return out


def solve_source_iteration(
    problem: SN2DProblem,
    tolerance: float = 1e-10,
    maximum_iterations: int = 10000,
) -> SN2DSolution:
    if not np.isfinite(tolerance) or tolerance <= 0.0:
        raise ValueError("tolerance must be finite and positive")
    if int(maximum_iterations) != maximum_iterations or maximum_iterations < 1:
        raise ValueError("maximum_iterations must be a positive integer")
    maximum_iterations = int(maximum_iterations)
    A0, b0 = assemble_system(problem, include_scattering=False)
    vector = np.zeros(problem.n_unknown)
    converged = False
    for iteration in range(1, maximum_iterations + 1):
        flux = _reshape(problem, vector)
        rhs = b0 + _scattering_source(problem, flux).reshape(-1)
        new = _checked_sparse_solve(A0, rhs)
        relative = np.linalg.norm(new - vector) / max(np.linalg.norm(new), 1e-30)
        vector = new
        if relative <= tolerance:
            converged = True
            break
    A, b = assemble_system(problem, include_scattering=True)
    residual = float(np.linalg.norm(A @ vector - b))
    flux = _reshape(problem, vector)
    return SN2DSolution(flux, compute_responses(problem, flux), iteration, converged, residual)


def response_vector(problem: SN2DProblem, response_name: str) -> FloatArray:
    kernel = problem.response_kernels[response_name]
    return (kernel * problem.quadrature.weights[None, :, None, None] * problem.grid.cell_areas[None, None, :, :]).reshape(-1)


def solve_discrete_adjoint(problem: SN2DProblem, response_name: str) -> FloatArray:
    A, _b = assemble_system(problem, include_scattering=True)
    c = response_vector(problem, response_name)
    return _checked_sparse_solve(A.T.tocsr(), c)


def forward_adjoint_identity(problem: SN2DProblem, solution: SN2DSolution, response_name: str) -> dict[str, float]:
    A, b = assemble_system(problem, include_scattering=True)
    psi = solution.angular_flux.reshape(-1)
    c = response_vector(problem, response_name)
    z = _checked_sparse_solve(A.T.tocsr(), c)
    forward = float(c @ psi)
    adjoint = float(z @ b)
    return {"forward": forward, "adjoint": adjoint, "absolute_difference": abs(forward - adjoint), "relative_difference": abs(forward - adjoint) / max(abs(forward), 1e-30)}


def global_particle_balance(problem: SN2DProblem, solution: SN2DSolution) -> dict[str, float]:
    flux = solution.angular_flux
    q = problem.source
    w = problem.quadrature.weights
    ox, oy = problem.quadrature.nodes[:, 0], problem.quadrature.nodes[:, 1]
    incoming = outgoing = 0.0
    # Vertical faces, integrated over y.
    for j, dy in enumerate(problem.grid.dy):
        for g in range(problem.n_group):
            incoming += float(np.sum(w[ox > 0] * ox[ox > 0] * problem.boundary.left[g, ox > 0, j]) * dy)
            incoming += float(np.sum(w[ox < 0] * (-ox[ox < 0]) * problem.boundary.right[g, ox < 0, j]) * dy)
            outgoing += float(np.sum(w[ox < 0] * (-ox[ox < 0]) * flux[g, ox < 0, 0, j]) * dy)
            outgoing += float(np.sum(w[ox > 0] * ox[ox > 0] * flux[g, ox > 0, -1, j]) * dy)
    for i, dx in enumerate(problem.grid.dx):
        for g in range(problem.n_group):
            incoming += float(np.sum(w[oy > 0] * oy[oy > 0] * problem.boundary.bottom[g, oy > 0, i]) * dx)
            incoming += float(np.sum(w[oy < 0] * (-oy[oy < 0]) * problem.boundary.top[g, oy < 0, i]) * dx)
            outgoing += float(np.sum(w[oy < 0] * (-oy[oy < 0]) * flux[g, oy < 0, i, 0]) * dx)
            outgoing += float(np.sum(w[oy > 0] * oy[oy > 0] * flux[g, oy > 0, i, -1]) * dx)
    source = float(np.einsum("gaij,a,ij->", q, w, problem.grid.cell_areas))
    phi = np.einsum("gaij,a->gij", flux, w)
    absorption_xs = problem.sigma_t - np.sum(problem.sigma_s, axis=1)
    absorption = float(np.einsum("gij,gij,ij->", absorption_xs, phi, problem.grid.cell_areas))
    residual = outgoing + absorption - incoming - source
    return {"incoming": incoming, "outgoing": outgoing, "source": source, "absorption": absorption, "residual": residual, "relative_residual": abs(residual) / max(incoming + source, 1e-30)}

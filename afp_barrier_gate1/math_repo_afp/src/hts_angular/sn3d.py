"""Deterministic Cartesian three-dimensional multigroup :math:`S_N` reference solver.

The spatial discretization is first-order conservative upwind finite volume.
It is intended for verification, local curved-tape patches, and algorithmic
experiments rather than production full-device transport.
"""
from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, field
import hashlib
from typing import Mapping
import warnings

import numpy as np
from numpy.typing import ArrayLike, NDArray
from scipy.sparse import csr_matrix, lil_matrix
from scipy.sparse.linalg import MatrixRankWarning, spsolve

from .graph_generator import GraphGenerator
from .quadrature import PositiveQuadrature

FloatArray = NDArray[np.float64]


def axis_quadrature_sphere() -> PositiveQuadrature:
    """Six Cartesian axis directions with equal positive weights."""
    nodes = np.array(
        [
            [1.0, 0.0, 0.0],
            [-1.0, 0.0, 0.0],
            [0.0, 1.0, 0.0],
            [0.0, -1.0, 0.0],
            [0.0, 0.0, 1.0],
            [0.0, 0.0, -1.0],
        ]
    )
    return PositiveQuadrature(nodes, np.full(6, 4.0 * np.pi / 6.0), {"family": "Cartesian axes"})


@dataclass(frozen=True)
class CartesianGrid3D:
    x_edges: FloatArray
    y_edges: FloatArray
    z_edges: FloatArray

    def __post_init__(self) -> None:
        values = []
        for name, raw in (("x_edges", self.x_edges), ("y_edges", self.y_edges), ("z_edges", self.z_edges)):
            array = np.asarray(raw, dtype=float).reshape(-1)
            if array.size < 2 or np.any(~np.isfinite(array)) or np.any(np.diff(array) <= 0.0):
                raise ValueError(f"{name} must be finite and strictly increasing")
            values.append(array)
        object.__setattr__(self, "x_edges", values[0])
        object.__setattr__(self, "y_edges", values[1])
        object.__setattr__(self, "z_edges", values[2])

    @property
    def nx(self) -> int:
        return self.x_edges.size - 1

    @property
    def ny(self) -> int:
        return self.y_edges.size - 1

    @property
    def nz(self) -> int:
        return self.z_edges.size - 1

    @property
    def shape(self) -> tuple[int, int, int]:
        return self.nx, self.ny, self.nz

    @property
    def dx(self) -> FloatArray:
        return np.diff(self.x_edges)

    @property
    def dy(self) -> FloatArray:
        return np.diff(self.y_edges)

    @property
    def dz(self) -> FloatArray:
        return np.diff(self.z_edges)

    @property
    def cell_volumes(self) -> FloatArray:
        return self.dx[:, None, None] * self.dy[None, :, None] * self.dz[None, None, :]

    @property
    def x_centers(self) -> FloatArray:
        return 0.5 * (self.x_edges[:-1] + self.x_edges[1:])

    @property
    def y_centers(self) -> FloatArray:
        return 0.5 * (self.y_edges[:-1] + self.y_edges[1:])

    @property
    def z_centers(self) -> FloatArray:
        return 0.5 * (self.z_edges[:-1] + self.z_edges[1:])


@dataclass(frozen=True)
class BoundaryData3D:
    x_min: FloatArray
    x_max: FloatArray
    y_min: FloatArray
    y_max: FloatArray
    z_min: FloatArray
    z_max: FloatArray

    @classmethod
    def vacuum(cls, n_group: int, n_angle: int, grid: CartesianGrid3D) -> "BoundaryData3D":
        return cls(
            np.zeros((n_group, n_angle, grid.ny, grid.nz)),
            np.zeros((n_group, n_angle, grid.ny, grid.nz)),
            np.zeros((n_group, n_angle, grid.nx, grid.nz)),
            np.zeros((n_group, n_angle, grid.nx, grid.nz)),
            np.zeros((n_group, n_angle, grid.nx, grid.ny)),
            np.zeros((n_group, n_angle, grid.nx, grid.ny)),
        )


@dataclass(frozen=True)
class SN3DProblem:
    grid: CartesianGrid3D
    quadrature: PositiveQuadrature
    sigma_t: FloatArray
    sigma_s: FloatArray
    fixed_source: FloatArray
    boundary: BoundaryData3D
    response_kernels: Mapping[str, FloatArray] = field(default_factory=dict)
    graph: GraphGenerator | None = None
    angular_diffusion: float | FloatArray = 0.0

    def __post_init__(self) -> None:
        na = self.quadrature.n_node
        nx, ny, nz = self.grid.shape
        st = np.asarray(self.sigma_t, dtype=float)
        if st.ndim != 4 or st.shape[1:] != (nx, ny, nz) or st.shape[0] < 1:
            raise ValueError("sigma_t must have shape (group,x,y,z)")
        ng = st.shape[0]
        ss = np.asarray(self.sigma_s, dtype=float)
        source = np.asarray(self.fixed_source, dtype=float)
        if ss.shape != (ng, ng, nx, ny, nz):
            raise ValueError("sigma_s must have shape (incoming_group,outgoing_group,x,y,z)")
        if source.shape != (ng, na, nx, ny, nz):
            raise ValueError("fixed_source must have shape (group,angle,x,y,z)")
        if any(np.any(~np.isfinite(a)) or np.any(a < 0.0) for a in (st, ss, source)):
            raise ValueError("transport coefficients and sources must be finite and nonnegative")
        if np.any(np.sum(ss, axis=1) - st > 1e-12 * np.maximum(1.0, st)):
            raise ValueError("out-scattering cannot exceed total cross section in this particle-balance model")
        shapes = (
            (ng, na, ny, nz),
            (ng, na, ny, nz),
            (ng, na, nx, nz),
            (ng, na, nx, nz),
            (ng, na, nx, ny),
            (ng, na, nx, ny),
        )
        boundary_values: list[FloatArray] = []
        for value, shape in zip(
            (
                self.boundary.x_min,
                self.boundary.x_max,
                self.boundary.y_min,
                self.boundary.y_max,
                self.boundary.z_min,
                self.boundary.z_max,
            ),
            shapes,
            strict=True,
        ):
            array = np.asarray(value, dtype=float)
            if array.shape != shape or np.any(~np.isfinite(array)) or np.any(array < 0.0):
                raise ValueError("boundary data are nonfinite, negative, or incorrectly shaped")
            boundary_values.append(array)
        kernels = {str(name): np.asarray(value, dtype=float) for name, value in self.response_kernels.items()}
        for name, kernel in kernels.items():
            if kernel.shape != source.shape or np.any(~np.isfinite(kernel)):
                raise ValueError(f"response kernel {name!r} must align with fixed_source")
        if self.graph is not None:
            if (
                self.graph.nodes.shape != self.quadrature.nodes.shape
                or not np.allclose(self.graph.nodes, self.quadrature.nodes, rtol=1e-12, atol=1e-14)
                or not np.allclose(self.graph.weights, self.quadrature.weights, rtol=1e-12, atol=1e-14)
            ):
                raise ValueError("angular graph must align with the quadrature")
        diffusion = np.asarray(self.angular_diffusion, dtype=float)
        if diffusion.ndim != 0 and diffusion.shape != st.shape:
            raise ValueError("angular_diffusion must be scalar or shaped like sigma_t")
        if np.any(~np.isfinite(diffusion)) or np.any(diffusion < 0.0):
            raise ValueError("angular_diffusion must be finite and nonnegative")
        object.__setattr__(self, "sigma_t", st)
        object.__setattr__(self, "sigma_s", ss)
        object.__setattr__(self, "fixed_source", source)
        object.__setattr__(self, "boundary", BoundaryData3D(*boundary_values))
        object.__setattr__(self, "response_kernels", kernels)
        object.__setattr__(self, "angular_diffusion", float(diffusion) if diffusion.ndim == 0 else diffusion)

    @property
    def n_group(self) -> int:
        return int(self.sigma_t.shape[0])

    @property
    def n_unknown(self) -> int:
        nx, ny, nz = self.grid.shape
        return self.n_group * self.quadrature.n_node * nx * ny * nz

    @property
    def source(self) -> FloatArray:
        """Compatibility alias for the fixed source."""
        return self.fixed_source


@dataclass(frozen=True)
class SN3DSolution:
    angular_flux: FloatArray
    responses: dict[str, float]
    iterations: int
    converged: bool
    residual_norm: float
    relative_residual: float
    flux_sha256: str


def _index(problem: SN3DProblem, g: int, a: int, i: int, j: int, k: int) -> int:
    na = problem.quadrature.n_node
    nx, ny, nz = problem.grid.shape
    return ((((g * na + a) * nx + i) * ny + j) * nz + k)


def _reshape(problem: SN3DProblem, vector: FloatArray) -> FloatArray:
    nx, ny, nz = problem.grid.shape
    return vector.reshape(problem.n_group, problem.quadrature.n_node, nx, ny, nz)


def _diffusion_value(problem: SN3DProblem, g: int, i: int, j: int, k: int) -> float:
    value = np.asarray(problem.angular_diffusion, dtype=float)
    return float(value) if value.ndim == 0 else float(value[g, i, j, k])


def assemble_system(problem: SN3DProblem, include_scattering: bool = True) -> tuple[csr_matrix, FloatArray]:
    ng, na = problem.n_group, problem.quadrature.n_node
    nx, ny, nz = problem.grid.shape
    A = lil_matrix((problem.n_unknown, problem.n_unknown), dtype=float)
    b = problem.fixed_source.reshape(-1).copy()
    mass = float(np.sum(problem.quadrature.weights))
    for g in range(ng):
        for a, (ox, oy, oz) in enumerate(problem.quadrature.nodes):
            for i in range(nx):
                for j in range(ny):
                    for k in range(nz):
                        row = _index(problem, g, a, i, j, k)
                        diag = (
                            problem.sigma_t[g, i, j, k]
                            + abs(ox) / problem.grid.dx[i]
                            + abs(oy) / problem.grid.dy[j]
                            + abs(oz) / problem.grid.dz[k]
                        )
                        A[row, row] += diag
                        if ox > 0.0:
                            if i > 0:
                                A[row, _index(problem, g, a, i - 1, j, k)] -= ox / problem.grid.dx[i]
                            else:
                                b[row] += ox / problem.grid.dx[i] * problem.boundary.x_min[g, a, j, k]
                        elif ox < 0.0:
                            if i < nx - 1:
                                A[row, _index(problem, g, a, i + 1, j, k)] -= -ox / problem.grid.dx[i]
                            else:
                                b[row] += -ox / problem.grid.dx[i] * problem.boundary.x_max[g, a, j, k]
                        if oy > 0.0:
                            if j > 0:
                                A[row, _index(problem, g, a, i, j - 1, k)] -= oy / problem.grid.dy[j]
                            else:
                                b[row] += oy / problem.grid.dy[j] * problem.boundary.y_min[g, a, i, k]
                        elif oy < 0.0:
                            if j < ny - 1:
                                A[row, _index(problem, g, a, i, j + 1, k)] -= -oy / problem.grid.dy[j]
                            else:
                                b[row] += -oy / problem.grid.dy[j] * problem.boundary.y_max[g, a, i, k]
                        if oz > 0.0:
                            if k > 0:
                                A[row, _index(problem, g, a, i, j, k - 1)] -= oz / problem.grid.dz[k]
                            else:
                                b[row] += oz / problem.grid.dz[k] * problem.boundary.z_min[g, a, i, j]
                        elif oz < 0.0:
                            if k < nz - 1:
                                A[row, _index(problem, g, a, i, j, k + 1)] -= -oz / problem.grid.dz[k]
                            else:
                                b[row] += -oz / problem.grid.dz[k] * problem.boundary.z_max[g, a, i, j]
                        if problem.graph is not None:
                            diffusion = _diffusion_value(problem, g, i, j, k)
                            if diffusion:
                                for ap in range(na):
                                    A[row, _index(problem, g, ap, i, j, k)] -= diffusion * problem.graph.generator[a, ap]
                        if include_scattering:
                            for gin in range(ng):
                                sigma = problem.sigma_s[gin, g, i, j, k]
                                if sigma:
                                    for ap in range(na):
                                        A[row, _index(problem, gin, ap, i, j, k)] -= sigma * problem.quadrature.weights[ap] / mass
    return A.tocsr(), b


def _checked_sparse_solve(matrix: csr_matrix, rhs: FloatArray) -> FloatArray:
    with warnings.catch_warnings():
        warnings.simplefilter("error", MatrixRankWarning)
        try:
            vector = np.asarray(spsolve(matrix, rhs), dtype=float)
        except MatrixRankWarning as exc:
            raise np.linalg.LinAlgError("transport matrix is singular") from exc
    if vector.shape != rhs.shape or np.any(~np.isfinite(vector)):
        raise np.linalg.LinAlgError("sparse solve returned nonfinite values")
    return vector


def flux_sha256(flux: ArrayLike) -> str:
    canonical = np.ascontiguousarray(np.asarray(flux, dtype="<f8"))
    return hashlib.sha256(canonical.tobytes(order="C")).hexdigest()


def compute_responses(problem: SN3DProblem, angular_flux: FloatArray) -> dict[str, float]:
    return {
        name: float(
            np.einsum(
                "gaijk,gaijk,a,ijk->",
                kernel,
                angular_flux,
                problem.quadrature.weights,
                problem.grid.cell_volumes,
            )
        )
        for name, kernel in problem.response_kernels.items()
    }


def _solution(problem: SN3DProblem, vector: FloatArray, iterations: int, converged: bool, A: csr_matrix, b: FloatArray) -> SN3DSolution:
    residual = float(np.linalg.norm(A @ vector - b))
    relative = residual / max(float(np.linalg.norm(b)), 1e-30)
    flux = _reshape(problem, vector)
    return SN3DSolution(
        flux,
        compute_responses(problem, flux),
        int(iterations),
        bool(converged),
        residual,
        relative,
        flux_sha256(flux),
    )


def solve_direct(problem: SN3DProblem, residual_tolerance: float = 1e-9) -> SN3DSolution:
    if not np.isfinite(residual_tolerance) or residual_tolerance <= 0.0:
        raise ValueError("residual_tolerance must be finite and positive")
    A, b = assemble_system(problem, include_scattering=True)
    vector = _checked_sparse_solve(A, b)
    result = _solution(problem, vector, 1, True, A, b)
    return SN3DSolution(
        result.angular_flux,
        result.responses,
        result.iterations,
        result.relative_residual <= residual_tolerance,
        result.residual_norm,
        result.relative_residual,
        result.flux_sha256,
    )


def _scattering_source(problem: SN3DProblem, flux: FloatArray) -> FloatArray:
    mass = float(np.sum(problem.quadrature.weights))
    scalar = np.einsum("gaijk,a->gijk", flux, problem.quadrature.weights)
    out = np.zeros_like(flux)
    for gin in range(problem.n_group):
        for gout in range(problem.n_group):
            out[gout] += problem.sigma_s[gin, gout][None, ...] * scalar[gin][None, ...] / mass
    return out


def _sweep_one(problem: SN3DProblem, g: int, a: int, source: FloatArray) -> FloatArray:
    nx, ny, nz = problem.grid.shape
    ox, oy, oz = problem.quadrature.nodes[a]
    i_order = range(nx) if ox >= 0.0 else range(nx - 1, -1, -1)
    j_order = range(ny) if oy >= 0.0 else range(ny - 1, -1, -1)
    k_order = range(nz) if oz >= 0.0 else range(nz - 1, -1, -1)
    flux = np.zeros((nx, ny, nz))
    for i in i_order:
        for j in j_order:
            for k in k_order:
                rhs = float(source[i, j, k])
                diag = float(problem.sigma_t[g, i, j, k])
                if ox > 0.0:
                    coeff = ox / problem.grid.dx[i]
                    diag += coeff
                    rhs += coeff * (flux[i - 1, j, k] if i > 0 else problem.boundary.x_min[g, a, j, k])
                elif ox < 0.0:
                    coeff = -ox / problem.grid.dx[i]
                    diag += coeff
                    rhs += coeff * (flux[i + 1, j, k] if i < nx - 1 else problem.boundary.x_max[g, a, j, k])
                if oy > 0.0:
                    coeff = oy / problem.grid.dy[j]
                    diag += coeff
                    rhs += coeff * (flux[i, j - 1, k] if j > 0 else problem.boundary.y_min[g, a, i, k])
                elif oy < 0.0:
                    coeff = -oy / problem.grid.dy[j]
                    diag += coeff
                    rhs += coeff * (flux[i, j + 1, k] if j < ny - 1 else problem.boundary.y_max[g, a, i, k])
                if oz > 0.0:
                    coeff = oz / problem.grid.dz[k]
                    diag += coeff
                    rhs += coeff * (flux[i, j, k - 1] if k > 0 else problem.boundary.z_min[g, a, i, j])
                elif oz < 0.0:
                    coeff = -oz / problem.grid.dz[k]
                    diag += coeff
                    rhs += coeff * (flux[i, j, k + 1] if k < nz - 1 else problem.boundary.z_max[g, a, i, j])
                if diag <= 0.0:
                    raise np.linalg.LinAlgError("sweep cell has no removal or streaming diagonal")
                flux[i, j, k] = rhs / diag
    return flux


def solve_source_iteration(
    problem: SN3DProblem,
    tolerance: float = 1e-10,
    maximum_iterations: int = 10000,
    *,
    workers: int = 1,
) -> SN3DSolution:
    if not np.isfinite(tolerance) or tolerance <= 0.0:
        raise ValueError("tolerance must be finite and positive")
    if int(maximum_iterations) != maximum_iterations or maximum_iterations < 1:
        raise ValueError("maximum_iterations must be a positive integer")
    if int(workers) != workers or workers < 1:
        raise ValueError("workers must be a positive integer")
    maximum_iterations, workers = int(maximum_iterations), int(workers)
    flux = np.zeros_like(problem.fixed_source)
    converged = False
    if problem.graph is not None and np.any(np.asarray(problem.angular_diffusion) > 0.0):
        A0, b0 = assemble_system(problem, include_scattering=False)
        vector = flux.reshape(-1)
        for iteration in range(1, maximum_iterations + 1):
            rhs = b0 + _scattering_source(problem, _reshape(problem, vector)).reshape(-1)
            new = _checked_sparse_solve(A0, rhs)
            relative = float(np.linalg.norm(new - vector) / max(np.linalg.norm(new), 1e-30))
            vector = new
            if relative <= tolerance:
                converged = True
                break
        flux = _reshape(problem, vector)
    else:
        tasks = [(g, a) for g in range(problem.n_group) for a in range(problem.quadrature.n_node)]
        for iteration in range(1, maximum_iterations + 1):
            total_source = problem.fixed_source + _scattering_source(problem, flux)
            new = np.empty_like(flux)
            if workers == 1:
                results = [(g, a, _sweep_one(problem, g, a, total_source[g, a])) for g, a in tasks]
            else:
                def execute(task: tuple[int, int]) -> tuple[int, int, FloatArray]:
                    g, a = task
                    return g, a, _sweep_one(problem, g, a, total_source[g, a])

                with ThreadPoolExecutor(max_workers=workers) as pool:
                    results = list(pool.map(execute, tasks))
            # Assignment order is canonical even if worker completion order differs.
            for g, a, values in results:
                new[g, a] = values
            relative = float(np.linalg.norm(new - flux) / max(np.linalg.norm(new), 1e-30))
            flux = new
            if relative <= tolerance:
                converged = True
                break
        vector = flux.reshape(-1)
    A, b = assemble_system(problem, include_scattering=True)
    return _solution(problem, vector, iteration, converged, A, b)


def response_vector(problem: SN3DProblem, response_name: str) -> FloatArray:
    kernel = problem.response_kernels[response_name]
    return (
        kernel
        * problem.quadrature.weights[None, :, None, None, None]
        * problem.grid.cell_volumes[None, None, :, :, :]
    ).reshape(-1)


def solve_discrete_adjoint(problem: SN3DProblem, response_name: str) -> FloatArray:
    A, _ = assemble_system(problem, include_scattering=True)
    return _checked_sparse_solve(A.T.tocsr(), response_vector(problem, response_name))


def forward_adjoint_identity(problem: SN3DProblem, solution: SN3DSolution, response_name: str) -> dict[str, float]:
    A, b = assemble_system(problem, include_scattering=True)
    c = response_vector(problem, response_name)
    z = _checked_sparse_solve(A.T.tocsr(), c)
    forward = float(c @ solution.angular_flux.reshape(-1))
    adjoint = float(z @ b)
    difference = abs(forward - adjoint)
    return {
        "forward": forward,
        "adjoint": adjoint,
        "absolute_difference": difference,
        "relative_difference": difference / max(abs(forward), 1e-30),
    }


def global_particle_balance(problem: SN3DProblem, solution: SN3DSolution) -> dict[str, float]:
    flux = solution.angular_flux
    w = problem.quadrature.weights
    ox, oy, oz = problem.quadrature.nodes.T
    incoming = 0.0
    outgoing = 0.0
    # x faces
    for j, dy in enumerate(problem.grid.dy):
        for k, dz in enumerate(problem.grid.dz):
            area = dy * dz
            for g in range(problem.n_group):
                incoming += float(np.sum(w[ox > 0] * ox[ox > 0] * problem.boundary.x_min[g, ox > 0, j, k]) * area)
                incoming += float(np.sum(w[ox < 0] * (-ox[ox < 0]) * problem.boundary.x_max[g, ox < 0, j, k]) * area)
                outgoing += float(np.sum(w[ox < 0] * (-ox[ox < 0]) * flux[g, ox < 0, 0, j, k]) * area)
                outgoing += float(np.sum(w[ox > 0] * ox[ox > 0] * flux[g, ox > 0, -1, j, k]) * area)
    # y faces
    for i, dx in enumerate(problem.grid.dx):
        for k, dz in enumerate(problem.grid.dz):
            area = dx * dz
            for g in range(problem.n_group):
                incoming += float(np.sum(w[oy > 0] * oy[oy > 0] * problem.boundary.y_min[g, oy > 0, i, k]) * area)
                incoming += float(np.sum(w[oy < 0] * (-oy[oy < 0]) * problem.boundary.y_max[g, oy < 0, i, k]) * area)
                outgoing += float(np.sum(w[oy < 0] * (-oy[oy < 0]) * flux[g, oy < 0, i, 0, k]) * area)
                outgoing += float(np.sum(w[oy > 0] * oy[oy > 0] * flux[g, oy > 0, i, -1, k]) * area)
    # z faces
    for i, dx in enumerate(problem.grid.dx):
        for j, dy in enumerate(problem.grid.dy):
            area = dx * dy
            for g in range(problem.n_group):
                incoming += float(np.sum(w[oz > 0] * oz[oz > 0] * problem.boundary.z_min[g, oz > 0, i, j]) * area)
                incoming += float(np.sum(w[oz < 0] * (-oz[oz < 0]) * problem.boundary.z_max[g, oz < 0, i, j]) * area)
                outgoing += float(np.sum(w[oz < 0] * (-oz[oz < 0]) * flux[g, oz < 0, i, j, 0]) * area)
                outgoing += float(np.sum(w[oz > 0] * oz[oz > 0] * flux[g, oz > 0, i, j, -1]) * area)
    source = float(
        np.einsum(
            "gaijk,a,ijk->",
            problem.fixed_source,
            w,
            problem.grid.cell_volumes,
        )
    )
    scalar = np.einsum("gaijk,a->gijk", flux, w)
    absorption_xs = problem.sigma_t - np.sum(problem.sigma_s, axis=1)
    absorption = float(np.einsum("gijk,gijk,ijk->", absorption_xs, scalar, problem.grid.cell_volumes))
    residual = outgoing + absorption - incoming - source
    return {
        "incoming": incoming,
        "outgoing": outgoing,
        "source": source,
        "absorption": absorption,
        "residual": residual,
        "relative_residual": abs(residual) / max(incoming + source, 1e-30),
    }


def execution_plan(problem: SN3DProblem, workers: int = 1) -> dict[str, int | float]:
    if int(workers) != workers or workers < 1:
        raise ValueError("workers must be a positive integer")
    workers = int(workers)
    unknowns = problem.n_unknown
    dense_flux_bytes = unknowns * 8
    return {
        "groups": problem.n_group,
        "angles": problem.quadrature.n_node,
        "cells": int(np.prod(problem.grid.shape)),
        "unknowns": unknowns,
        "workers": workers,
        "angular_tasks": problem.n_group * problem.quadrature.n_node,
        "flux_bytes": dense_flux_bytes,
        "two_iterate_bytes": 2 * dense_flux_bytes,
    }


__all__ = [
    "BoundaryData3D",
    "CartesianGrid3D",
    "SN3DProblem",
    "SN3DSolution",
    "assemble_system",
    "axis_quadrature_sphere",
    "compute_responses",
    "execution_plan",
    "flux_sha256",
    "forward_adjoint_identity",
    "global_particle_balance",
    "response_vector",
    "solve_direct",
    "solve_discrete_adjoint",
    "solve_source_iteration",
]

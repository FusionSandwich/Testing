"""Sparse one-dimensional discrete-ordinates and layered BFP utilities.

The solver keeps neutral Boltzmann collision matrices separate from charged
Fokker--Planck generators.  It is a verification model, not an evaluated
nuclear-data transport code.
"""
from __future__ import annotations

from dataclasses import dataclass
import math
import time
import tracemalloc
from typing import Sequence

import numpy as np
from numpy.typing import ArrayLike, NDArray
from scipy import sparse
from scipy.sparse.linalg import spsolve

FloatArray = NDArray[np.float64]


@dataclass(frozen=True)
class Layer:
    name: str
    thickness_cm: float
    cells: int
    material: str

    def __post_init__(self) -> None:
        if self.thickness_cm <= 0 or self.cells < 1:
            raise ValueError("layer thickness and cell count must be positive")


@dataclass(frozen=True)
class Mesh:
    layers: tuple[Layer, ...]
    widths: FloatArray
    layer_index: NDArray[np.int64]
    centers: FloatArray

    @property
    def cell_count(self) -> int:
        return int(len(self.widths))

    @property
    def thickness_cm(self) -> float:
        return float(np.sum(self.widths))


@dataclass(frozen=True)
class SlabSolution:
    angular_flux: FloatArray
    scalar_flux: FloatArray
    current: FloatArray
    tensor: FloatArray
    q_normal: FloatArray
    left_outflow: float
    right_outflow: float
    lateral_escape: float
    balance_residual: float
    minimum_flux: float
    solve_seconds: float
    peak_memory_bytes: int
    matrix_nonzeros: int


def build_mesh(layers: Sequence[Layer]) -> Mesh:
    widths: list[float] = []
    indices: list[int] = []
    centers: list[float] = []
    cursor = 0.0
    for index, layer in enumerate(layers):
        dx = layer.thickness_cm / layer.cells
        for _ in range(layer.cells):
            widths.append(dx)
            indices.append(index)
            centers.append(cursor + 0.5 * dx)
            cursor += dx
    return Mesh(tuple(layers), np.asarray(widths), np.asarray(indices, dtype=np.int64), np.asarray(centers))


def product_quadrature(n_mu: int, n_phi: int) -> tuple[FloatArray, FloatArray]:
    from numpy.polynomial.legendre import leggauss

    if n_mu < 2 or n_phi < 4:
        raise ValueError("product quadrature requires n_mu>=2,n_phi>=4")
    mu, polar = leggauss(n_mu)
    nodes: list[list[float]] = []
    weights: list[float] = []
    for a in range(n_mu):
        radius = math.sqrt(max(0.0, 1.0 - float(mu[a]) ** 2))
        for b in range(n_phi):
            phi = 2.0 * math.pi * b / n_phi
            nodes.append([radius * math.cos(phi), radius * math.sin(phi), float(mu[a])])
            weights.append(float(polar[a]) / (2.0 * n_phi))
    return np.asarray(nodes), np.asarray(weights)


def normalized_beam(
    nodes: ArrayLike,
    weights: ArrayLike,
    direction: ArrayLike,
    concentration: float,
) -> FloatArray:
    x = np.asarray(nodes, dtype=float)
    w = np.asarray(weights, dtype=float)
    d = np.asarray(direction, dtype=float)
    d /= np.linalg.norm(d)
    exponent = concentration * (x @ d - 1.0)
    value = np.exp(np.clip(exponent, -700.0, 0.0))
    mass = float(w @ value)
    if mass <= 0:
        raise ArithmeticError("beam normalization failed")
    return value / mass


def reversible_positive_kernel(
    nodes: ArrayLike,
    weights: ArrayLike,
    concentration: float,
    *,
    tolerance: float = 2e-13,
) -> FloatArray:
    """Positive W-reversible Markov matrix by symmetric Sinkhorn scaling."""

    x = np.asarray(nodes, dtype=float)
    w = np.asarray(weights, dtype=float)
    raw = np.exp(np.clip(concentration * (x @ x.T - 1.0), -700.0, 0.0))
    scale = np.sqrt(w / np.maximum(raw @ np.ones(len(w)), 1e-300))
    for _ in range(10000):
        new = w / np.maximum(raw @ scale, 1e-300)
        # Damped symmetric balancing is robust for sharply peaked kernels.
        new = np.sqrt(np.maximum(scale * new, 1e-300))
        if np.linalg.norm(new - scale, ord=np.inf) <= tolerance * max(1.0, np.linalg.norm(scale, ord=np.inf)):
            scale = new
            break
        scale = new
    conductance = scale[:, None] * raw * scale[None, :]
    # A final symmetric diagonal correction enforces exact row mass to roundoff.
    for _ in range(100):
        row = conductance @ np.ones(len(w))
        correction = np.sqrt(w / np.maximum(row, 1e-300))
        conductance = correction[:, None] * conductance * correction[None, :]
        if np.linalg.norm(conductance @ np.ones(len(w)) - w, ord=np.inf) < 2e-13:
            break
    kernel = conductance / w[:, None]
    if (
        np.min(kernel) < -1e-14
        or np.linalg.norm(kernel @ np.ones(len(w)) - 1.0, ord=np.inf) > 2e-10
        or np.linalg.norm(w[:, None] * kernel - kernel.T * w[None, :], ord=np.inf) > 2e-10
    ):
        raise ArithmeticError("positive reversible kernel balancing failed")
    return kernel


def angular_moments(
    angular_flux: ArrayLike,
    nodes: ArrayLike,
    weights: ArrayLike,
    normal: ArrayLike,
) -> tuple[FloatArray, FloatArray, FloatArray, FloatArray]:
    psi = np.asarray(angular_flux, dtype=float)
    x = np.asarray(nodes, dtype=float)
    w = np.asarray(weights, dtype=float)
    n = np.asarray(normal, dtype=float)
    n /= np.linalg.norm(n)
    weighted = psi * w[None, :]
    scalar = np.sum(weighted, axis=1)
    current = weighted @ x
    second = np.einsum("cd,di,dj->cij", weighted, x, x)
    tensor = second - scalar[:, None, None] * np.eye(3)[None, :, :] / 3.0
    qn = np.einsum("i,cij,j->c", n, tensor, n)
    return scalar, current, tensor, qn


def solve_steady_slab(
    mesh: Mesh,
    nodes: ArrayLike,
    weights: ArrayLike,
    normal: ArrayLike,
    collision_blocks: ArrayLike,
    absorption: ArrayLike,
    source: ArrayLike,
    *,
    inflow_left: ArrayLike | None = None,
    inflow_right: ArrayLike | None = None,
    lateral_width_cm: float | None = None,
    lateral_factor: float = 0.0,
) -> SlabSolution:
    x = np.asarray(nodes, dtype=float)
    w = np.asarray(weights, dtype=float)
    nvec = np.asarray(normal, dtype=float)
    nvec /= np.linalg.norm(nvec)
    mu = x @ nvec
    blocks = np.asarray(collision_blocks, dtype=float)
    sigma_a = np.asarray(absorption, dtype=float)
    q = np.asarray(source, dtype=float)
    cells, directions = mesh.cell_count, len(w)
    if blocks.shape != (cells, directions, directions):
        raise ValueError("collision block shape mismatch")
    if sigma_a.shape != (cells,) or q.shape != (cells, directions):
        raise ValueError("absorption/source shape mismatch")
    left = np.zeros(directions) if inflow_left is None else np.asarray(inflow_left, dtype=float)
    right = np.zeros(directions) if inflow_right is None else np.asarray(inflow_right, dtype=float)
    if left.shape != (directions,) or right.shape != (directions,):
        raise ValueError("inflow shape mismatch")
    leak = np.zeros(directions)
    if lateral_width_cm is not None and lateral_factor > 0:
        if lateral_width_cm <= 0:
            raise ValueError("lateral width must be positive")
        leak = lateral_factor * np.sqrt(np.maximum(0.0, 1.0 - mu * mu)) / lateral_width_cm

    matrix = sparse.lil_matrix((cells * directions, cells * directions), dtype=float)
    rhs = q.reshape(-1).copy()
    for cell in range(cells):
        sl = slice(cell * directions, (cell + 1) * directions)
        matrix[sl, sl] = blocks[cell] + np.diag(leak)
        dx = float(mesh.widths[cell])
        for direction, cosine in enumerate(mu):
            row = cell * directions + direction
            speed = abs(float(cosine))
            if cosine > 1e-14:
                matrix[row, row] += speed / dx
                if cell == 0:
                    rhs[row] += speed * left[direction] / dx
                else:
                    matrix[row, (cell - 1) * directions + direction] -= speed / dx
            elif cosine < -1e-14:
                matrix[row, row] += speed / dx
                if cell == cells - 1:
                    rhs[row] += speed * right[direction] / dx
                else:
                    matrix[row, (cell + 1) * directions + direction] -= speed / dx
            else:
                matrix[row, row] += 1e-12 / dx

    csr = matrix.tocsr()
    tracemalloc.start()
    started = time.perf_counter()
    try:
        solution = np.asarray(spsolve(csr, rhs), dtype=float).reshape(cells, directions)
        elapsed = time.perf_counter() - started
        _, peak = tracemalloc.get_traced_memory()
    finally:
        tracemalloc.stop()
    scalar, current, tensor, qn = angular_moments(solution, x, w, nvec)
    left_out = float(np.sum(w[mu < 0] * (-mu[mu < 0]) * solution[0, mu < 0]))
    right_out = float(np.sum(w[mu > 0] * mu[mu > 0] * solution[-1, mu > 0]))
    lateral = float(np.sum(mesh.widths[:, None] * w[None, :] * leak[None, :] * solution))
    volume_source = float(np.sum(mesh.widths[:, None] * w[None, :] * q))
    boundary_in = float(np.sum(w[mu > 0] * mu[mu > 0] * left[mu > 0])) + float(
        np.sum(w[mu < 0] * (-mu[mu < 0]) * right[mu < 0])
    )
    absorbed = float(np.sum(mesh.widths * sigma_a * scalar))
    incoming = volume_source + boundary_in
    outgoing = left_out + right_out + lateral + absorbed
    balance = abs(incoming - outgoing) / max(1e-14, abs(incoming), abs(outgoing))
    return SlabSolution(
        solution,
        scalar,
        current,
        tensor,
        qn,
        left_out,
        right_out,
        lateral,
        float(balance),
        float(np.min(solution)),
        float(elapsed),
        int(peak),
        int(csr.nnz),
    )

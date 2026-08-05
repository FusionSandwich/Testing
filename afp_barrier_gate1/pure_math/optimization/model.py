"""Solver-independent fixed-quadrature and sampling-quotient assembly."""

from __future__ import annotations

from dataclasses import dataclass, field
from math import sqrt
from typing import Iterable, Mapping

import numpy as np
from numpy.typing import ArrayLike, NDArray
from scipy import linalg, special
import sympy as sp

FloatArray = NDArray[np.float64]
IntArray = NDArray[np.int64]


class AmbiguousSamplingRank(ValueError):
    """Raised when a singular value lies inside the declared rank guard."""


def _as_float_matrix(value: ArrayLike, name: str, columns: int | None = None) -> FloatArray:
    out = np.asarray(value, dtype=float)
    if out.ndim != 2 or (columns is not None and out.shape[1] != columns):
        suffix = "" if columns is None else f" with {columns} columns"
        raise ValueError(f"{name} must be a two-dimensional array{suffix}")
    if not np.all(np.isfinite(out)):
        raise ValueError(f"{name} contains a nonfinite entry")
    return out


def _canonical_edges(edges: Iterable[tuple[int, int]], node_count: int) -> IntArray:
    canonical: list[tuple[int, int]] = []
    seen: set[tuple[int, int]] = set()
    for raw_i, raw_j in edges:
        i, j = int(raw_i), int(raw_j)
        if not (0 <= i < node_count and 0 <= j < node_count):
            raise ValueError(f"edge {(i, j)} has an endpoint outside 0..{node_count - 1}")
        if i == j:
            raise ValueError(f"self edge {(i, j)} is not permitted")
        edge = (i, j) if i < j else (j, i)
        if edge in seen:
            raise ValueError(f"duplicate undirected edge {edge}")
        seen.add(edge)
        canonical.append(edge)
    if not canonical:
        raise ValueError("at least one permitted edge is required")
    return np.asarray(sorted(canonical), dtype=np.int64)


@dataclass(frozen=True)
class QuadratureGraph:
    """Fixed nodes, positive masses, and one permitted undirected graph.

    The masses need not sum to one.  Their total is retained explicitly, and
    the exact identity is ``sum_e gamma_e ell_e = sum_i w_i``.
    """

    nodes: FloatArray
    weights: FloatArray
    edges: IntArray
    incidence: FloatArray = field(repr=False)
    endpoint_incidence: FloatArray = field(repr=False)
    h1_matrix: FloatArray = field(repr=False)
    h1_rhs: FloatArray = field(repr=False)
    losses: FloatArray

    @classmethod
    def build(
        cls,
        nodes: ArrayLike,
        weights: ArrayLike,
        edges: Iterable[tuple[int, int]],
        *,
        unit_tolerance: float = 5e-12,
        reject_zero_edge_columns: bool = True,
    ) -> "QuadratureGraph":
        x = _as_float_matrix(nodes, "nodes", 3)
        n = x.shape[0]
        if n < 2:
            raise ValueError("at least two nodes are required")
        norms = np.linalg.norm(x, axis=1)
        if np.max(np.abs(norms - 1.0)) > unit_tolerance:
            raise ValueError("every node must be unit length within unit_tolerance")
        w = np.asarray(weights, dtype=float)
        if w.shape != (n,) or not np.all(np.isfinite(w)) or np.min(w) <= 0:
            raise ValueError("weights must be a finite positive vector with one entry per node")
        edge_array = _canonical_edges(edges, n)
        m = len(edge_array)
        bmat = np.zeros((n, m), dtype=float)
        endpoint = np.zeros((n, m), dtype=float)
        amat = np.zeros((3 * n, m), dtype=float)
        losses = np.empty(m, dtype=float)
        for e, (i_raw, j_raw) in enumerate(edge_array):
            i, j = int(i_raw), int(j_raw)
            bmat[i, e], bmat[j, e] = 1.0, -1.0
            endpoint[i, e] = endpoint[j, e] = 1.0
            delta = x[j] - x[i]
            losses[e] = 1.0 - float(x[i] @ x[j])
            if reject_zero_edge_columns and losses[e] <= unit_tolerance:
                raise ValueError(f"edge {(i, j)} joins coincident nodes and has a zero column")
            amat[3 * i : 3 * i + 3, e] = delta
            amat[3 * j : 3 * j + 3, e] = -delta
        rhs = (-2.0 * w[:, None] * x).reshape(-1)
        return cls(x.copy(), w.copy(), edge_array, bmat, endpoint, amat, rhs, losses)

    @property
    def node_count(self) -> int:
        return int(self.nodes.shape[0])

    @property
    def edge_count(self) -> int:
        return int(self.edges.shape[0])

    @property
    def total_mass(self) -> float:
        return float(np.sum(self.weights))

    @property
    def centered_moment(self) -> FloatArray:
        return self.weights @ self.nodes

    def generator(self, gamma: ArrayLike) -> FloatArray:
        conductance = np.asarray(gamma, dtype=float)
        if conductance.shape != (self.edge_count,):
            raise ValueError("gamma has the wrong shape")
        kirchhoff = (self.incidence * conductance[None, :]) @ self.incidence.T
        return -kirchhoff / self.weights[:, None]

    def symmetric_generator(self, gamma: ArrayLike) -> FloatArray:
        conductance = np.asarray(gamma, dtype=float)
        inverse_root = 1.0 / np.sqrt(self.weights)
        scaled_incidence = inverse_root[:, None] * self.incidence
        return -(scaled_incidence * conductance[None, :]) @ scaled_incidence.T

    def rates(self, gamma: ArrayLike) -> FloatArray:
        conductance = np.asarray(gamma, dtype=float)
        return (self.endpoint_incidence @ conductance) / self.weights

    def dense_centered_conductance(self) -> FloatArray:
        """Return ``2 w_i w_j / sum(w)`` on a complete permitted graph."""
        lookup = {tuple(map(int, edge)): e for e, edge in enumerate(self.edges)}
        expected = self.node_count * (self.node_count - 1) // 2
        if len(lookup) != expected:
            raise ValueError("dense_centered_conductance requires the complete graph")
        if np.linalg.norm(self.centered_moment, ord=np.inf) > 5e-11 * self.total_mass:
            raise ValueError("the weighted node set is not centered")
        out = np.empty(self.edge_count, dtype=float)
        for (i, j), e in lookup.items():
            out[e] = 2.0 * self.weights[i] * self.weights[j] / self.total_mass
        return out

    def restrict_edges(self, kept: Iterable[int]) -> "QuadratureGraph":
        indices = tuple(sorted({int(e) for e in kept}))
        if not indices:
            raise ValueError("cannot restrict to the empty edge set")
        edges = [tuple(map(int, self.edges[e])) for e in indices]
        return QuadratureGraph.build(self.nodes, self.weights, edges)


def degree_two_basis() -> FloatArray:
    """Frobenius-orthonormal basis of ``Sym_0(3)`` used by Paper I."""
    basis: list[FloatArray] = [
        np.diag([1.0, -1.0, 0.0]) / sqrt(2.0),
        np.diag([1.0, 1.0, -2.0]) / sqrt(6.0),
    ]
    for p, q in ((0, 1), (0, 2), (1, 2)):
        matrix = np.zeros((3, 3), dtype=float)
        matrix[p, q] = matrix[q, p] = 1.0 / sqrt(2.0)
        basis.append(matrix)
    return np.asarray(basis)


def real_harmonic_samples(nodes: ArrayLike, degree: int) -> FloatArray:
    """Sample one declared real orthonormal spherical-harmonic convention.

    Columns are ``m=0, cos(m phi), sin(m phi)`` for ``m=1,...,degree``.
    The Condon--Shortley phases do not affect the sampled quotient, but are
    fixed here so physical mode coefficients are reproducible.
    """
    x = _as_float_matrix(nodes, "nodes", 3)
    if degree < 0:
        raise ValueError("degree must be nonnegative")
    if degree == 2:
        basis = degree_two_basis()
        return np.asarray([[float(node @ a @ node) for a in basis] for node in x])
    polar = np.arccos(np.clip(x[:, 2], -1.0, 1.0))
    azimuth = np.mod(np.arctan2(x[:, 1], x[:, 0]), 2.0 * np.pi)
    columns: list[FloatArray] = [
        np.asarray(special.sph_harm_y(degree, 0, polar, azimuth).real, dtype=float)
    ]
    for m in range(1, degree + 1):
        value = special.sph_harm_y(degree, m, polar, azimuth)
        phase = (-1.0) ** m
        columns.append(np.asarray(sqrt(2.0) * phase * value.real, dtype=float))
        columns.append(np.asarray(sqrt(2.0) * phase * value.imag, dtype=float))
    return np.column_stack(columns)


@dataclass(frozen=True)
class RankPolicy:
    relative_tolerance: float = 1e-10
    absolute_tolerance: float = 1e-13
    ambiguity_factor: float = 32.0
    declared_rank: int | None = None

    def threshold(self, largest: float) -> float:
        return max(self.absolute_tolerance, self.relative_tolerance * largest)

    def classify(self, singular_values: FloatArray, coefficient_dimension: int) -> int:
        if singular_values.size == 0 or singular_values[0] <= 0:
            raise AmbiguousSamplingRank("the sampling matrix is identically zero")
        if self.relative_tolerance <= 0 or self.absolute_tolerance < 0:
            raise ValueError("rank tolerances must be positive/nonnegative")
        if self.ambiguity_factor <= 1:
            raise ValueError("ambiguity_factor must exceed one")
        if self.declared_rank is not None:
            rank = int(self.declared_rank)
            if not 1 <= rank <= min(coefficient_dimension, len(singular_values)):
                raise ValueError("declared_rank is outside the possible range")
            cutoff = self.threshold(float(singular_values[0]))
            if singular_values[rank - 1] <= cutoff * self.ambiguity_factor:
                raise AmbiguousSamplingRank("the declared rank is not separated above the guarded cutoff")
            if rank < len(singular_values) and singular_values[rank] >= cutoff / self.ambiguity_factor:
                raise AmbiguousSamplingRank("the declared rank truncates a singular value not separated below the guarded cutoff")
            return rank
        cutoff = self.threshold(float(singular_values[0]))
        lower, upper = cutoff / self.ambiguity_factor, cutoff * self.ambiguity_factor
        guarded = singular_values[(singular_values >= lower) & (singular_values <= upper)]
        if guarded.size:
            raise AmbiguousSamplingRank(
                f"{guarded.size} singular value(s) lie in the guarded interval "
                f"[{lower:.3e}, {upper:.3e}] around cutoff {cutoff:.3e}"
            )
        rank = int(np.sum(singular_values > cutoff))
        if rank == 0:
            raise AmbiguousSamplingRank("the declared tolerance removes the whole shell")
        return rank


def _canonicalize_column_signs(matrix: FloatArray) -> FloatArray:
    out = np.asarray(matrix, dtype=float).copy()
    for col in range(out.shape[1]):
        pivot = int(np.argmax(np.abs(out[:, col])))
        if out[pivot, col] < 0:
            out[:, col] *= -1.0
    return out


@dataclass(frozen=True)
class ExactSamplingCertificate:
    """Exact algebraic rank and alias-kernel certificate for one shell.

    Entries may be rational or algebraic SymPy expressions.  Construction
    invokes exact ``rank`` and ``nullspace``; the resulting numeric frame is
    used only after the exact and floating sample matrices are cross-checked.
    """

    samples: sp.ImmutableMatrix
    weights: tuple[sp.Expr, ...]
    rank: int
    nullspace: tuple[sp.ImmutableMatrix, ...]
    rref_pivots: tuple[int, ...]

    @classmethod
    def build(
        cls,
        samples: sp.MatrixBase | list[list[sp.Expr]],
        weights: Iterable[sp.Expr],
    ) -> "ExactSamplingCertificate":
        matrix = sp.ImmutableMatrix(samples)
        exact_weights = tuple(sp.sympify(value) for value in weights)
        if matrix.rows != len(exact_weights):
            raise ValueError("exact sampling weights have the wrong length")
        for value in exact_weights:
            if value.is_positive is not True:
                raise ValueError(f"exact sampling weight is not certified positive: {value}")
        rank = int(matrix.rank())
        if rank <= 0:
            raise ValueError("exact sample matrix has zero rank")
        nullspace = tuple(sp.ImmutableMatrix(vector) for vector in matrix.nullspace())
        _, pivots = matrix.rref()
        if len(nullspace) != matrix.cols - rank or len(pivots) != rank:
            raise ArithmeticError("exact sampling rank-nullity audit failed")
        for vector in nullspace:
            if matrix * vector != sp.zeros(matrix.rows, 1):
                raise ArithmeticError("SymPy returned a nonzero alias residual")
        return cls(matrix, exact_weights, rank, nullspace, tuple(map(int, pivots)))

    def numerical_samples(self, digits: int = 50) -> FloatArray:
        return np.asarray(self.samples.evalf(digits).tolist(), dtype=float)

    def numerical_weights(self, digits: int = 50) -> FloatArray:
        return np.asarray([float(sp.N(value, digits)) for value in self.weights], dtype=float)


@dataclass(frozen=True)
class ShellData:
    degree: int
    eigenvalue: int
    raw_samples: FloatArray = field(repr=False)
    quotient_frame: FloatArray = field(repr=False)
    singular_values: FloatArray
    rank: int
    cutoff: float
    rank_declared: bool
    exact_rank_certified: bool
    exact_nullity: int | None

    @classmethod
    def build(
        cls,
        graph: QuadratureGraph,
        degree: int,
        *,
        rank_policy: RankPolicy | None = None,
        samples: ArrayLike | None = None,
        exact_certificate: ExactSamplingCertificate | None = None,
    ) -> "ShellData":
        policy = rank_policy or RankPolicy()
        raw = real_harmonic_samples(graph.nodes, degree) if samples is None else _as_float_matrix(samples, "samples")
        if raw.shape[0] != graph.node_count:
            raise ValueError("sample matrix row count must equal the node count")
        weighted = np.sqrt(graph.weights)[:, None] * raw
        singular = np.linalg.svd(weighted, compute_uv=False)
        if exact_certificate is not None:
            exact_raw = exact_certificate.numerical_samples()
            exact_weights = exact_certificate.numerical_weights()
            if exact_raw.shape != raw.shape or np.linalg.norm(exact_raw - raw, ord=np.inf) > 2e-11:
                raise ValueError("exact sampling certificate does not match the numeric sample matrix")
            if exact_weights.shape != graph.weights.shape or np.linalg.norm(exact_weights - graph.weights, ord=np.inf) > 2e-11:
                raise ValueError("exact sampling certificate does not match the numeric weights")
            rank = exact_certificate.rank
            numeric_rank = int(np.sum(singular > policy.threshold(float(singular[0]))))
            if numeric_rank != rank:
                raise AmbiguousSamplingRank("exact and numerical sampling ranks disagree")
        else:
            rank = policy.classify(singular, raw.shape[1])
        # Pivoted QR supplies a deterministic basis of the retained sampled
        # range.  Rank selection itself remains SVD/gap based.
        q, _, _ = linalg.qr(weighted, mode="economic", pivoting=True)
        frame = _canonicalize_column_signs(q[:, :rank])
        orthogonality = np.linalg.norm(frame.T @ frame - np.eye(rank), ord=np.inf)
        if orthogonality > 5e-11:
            raise ArithmeticError(f"quotient frame lost orthogonality: {orthogonality:.3e}")
        return cls(
            int(degree), int(degree * (degree + 1)), raw, frame,
            singular, rank, policy.threshold(float(singular[0])),
            policy.declared_rank is not None,
            exact_certificate is not None,
            None if exact_certificate is None else len(exact_certificate.nullspace),
        )

    @property
    def retained_condition(self) -> float:
        return float(self.singular_values[0] / self.singular_values[self.rank - 1])

    @property
    def gram_condition(self) -> float:
        return self.retained_condition**2

    @property
    def discarded_largest(self) -> float:
        return 0.0 if self.rank >= len(self.singular_values) else float(self.singular_values[self.rank])

    def quotient_mode_from_samples(self, graph: QuadratureGraph, samples: ArrayLike) -> FloatArray:
        f = np.asarray(samples, dtype=float)
        if f.shape != (graph.node_count,):
            raise ValueError("mode samples have the wrong shape")
        weighted = np.sqrt(graph.weights) * f
        # scipy.linalg.norm uses a scaled BLAS norm and remains nonzero for
        # representable subnormal-scale modes where sum-of-squares underflows.
        norm = float(linalg.norm(weighted))
        if not np.isfinite(norm) or norm == 0.0:
            raise ValueError("the selected physical mode is a sampling alias")
        coordinates = self.quotient_frame.T @ weighted / norm
        projection_error = np.linalg.norm(weighted / norm - self.quotient_frame @ coordinates)
        if projection_error > 1e-8:
            raise ValueError("the selected samples do not lie in this sampled harmonic shell")
        return coordinates


@dataclass(frozen=True)
class AffineShell:
    shell: ShellData
    constant: FloatArray = field(repr=False)
    edge_terms: FloatArray = field(repr=False)

    def evaluate(self, gamma: ArrayLike) -> FloatArray:
        value = np.asarray(gamma, dtype=float)
        if value.shape != (self.edge_terms.shape[0],):
            raise ValueError("gamma has the wrong shape")
        return self.constant + np.tensordot(value, self.edge_terms, axes=(0, 0))


@dataclass
class DesignModel:
    graph: QuadratureGraph
    shells: dict[int, AffineShell]

    @classmethod
    def build(
        cls,
        graph: QuadratureGraph,
        degrees: Iterable[int] = (2,),
        *,
        rank_policies: Mapping[int, RankPolicy] | None = None,
        sample_overrides: Mapping[int, ArrayLike] | None = None,
        exact_sampling_certificates: Mapping[int, ExactSamplingCertificate] | None = None,
    ) -> "DesignModel":
        policies = rank_policies or {}
        overrides = sample_overrides or {}
        exact_certificates = exact_sampling_certificates or {}
        inverse_root = 1.0 / np.sqrt(graph.weights)
        scaled_incidence = inverse_root[:, None] * graph.incidence
        output: dict[int, AffineShell] = {}
        for degree in sorted(set(int(d) for d in degrees)):
            if degree < 2:
                raise ValueError("optimized shells must have degree at least two")
            shell = ShellData.build(
                graph, degree, rank_policy=policies.get(degree),
                samples=overrides.get(degree),
                exact_certificate=exact_certificates.get(degree),
            )
            u = shell.quotient_frame
            terms = np.empty((graph.edge_count, graph.node_count, shell.rank), dtype=float)
            for e in range(graph.edge_count):
                v = scaled_incidence[:, e]
                terms[e] = -np.outer(v, v) @ u
            output[degree] = AffineShell(shell, shell.eigenvalue * u, terms)
        return cls(graph, output)

    def shell(self, degree: int = 2) -> AffineShell:
        try:
            return self.shells[int(degree)]
        except KeyError as exc:
            raise KeyError(f"degree {degree} was not assembled") from exc

    def residual(self, gamma: ArrayLike, degree: int = 2) -> FloatArray:
        return self.shell(degree).evaluate(gamma)

    def defect(self, gamma: ArrayLike, degree: int = 2) -> float:
        return float(np.linalg.svd(self.residual(gamma, degree), compute_uv=False)[0])

    def condition_report(self) -> dict[str, object]:
        a_singular = np.linalg.svd(self.graph.h1_matrix, compute_uv=False)
        a_cut = max(1e-14, (a_singular[0] if a_singular.size else 0.0) * 1e-12)
        nonzero = a_singular[a_singular > a_cut]
        h1_condition = float(nonzero[0] / nonzero[-1]) if nonzero.size else float("inf")
        shells = {
            degree: {
                "rank": affine.shell.rank,
                "coefficient_dimension": affine.shell.raw_samples.shape[1],
                "sigma_max": float(affine.shell.singular_values[0]),
                "sigma_min_retained": float(affine.shell.singular_values[affine.shell.rank - 1]),
                "sigma_max_discarded": affine.shell.discarded_largest,
                "rank_cutoff": affine.shell.cutoff,
                "rank_declared": affine.shell.rank_declared,
                "exact_rank_certified": affine.shell.exact_rank_certified,
                "exact_nullity": affine.shell.exact_nullity,
                "condition_sampling": affine.shell.retained_condition,
                "condition_sampling_gram": affine.shell.gram_condition,
                "orthonormality_error": float(np.linalg.norm(
                    affine.shell.quotient_frame.T @ affine.shell.quotient_frame
                    - np.eye(affine.shell.rank),
                    ord=np.inf,
                )),
            }
            for degree, affine in self.shells.items()
        }
        return {
            "weight_dynamic_range": float(np.max(self.graph.weights) / np.min(self.graph.weights)),
            "h1_rank": int(nonzero.size),
            "h1_nonzero_singular_condition": h1_condition,
            "shells": shells,
        }

    def affine_cost_certificate(self, cost: ArrayLike, *, tolerance: float = 1e-10) -> dict[str, object]:
        """Test fixedness on the affine H1 system via ``A^T y = cost``.

        This deliberately does not claim to detect additional fixedness caused
        by a forced face of the nonnegative feasible polytope.
        """
        c = np.asarray(cost, dtype=float)
        if c.shape != (self.graph.edge_count,):
            raise ValueError("cost has the wrong shape")
        y, *_ = np.linalg.lstsq(self.graph.h1_matrix.T, c, rcond=None)
        residual = self.graph.h1_matrix.T @ y - c
        fixed = np.linalg.norm(residual, ord=np.inf) <= tolerance * (1.0 + np.linalg.norm(c, ord=np.inf))
        return {
            "affine_fixed": bool(fixed),
            "witness": y,
            "residual_inf": float(np.linalg.norm(residual, ord=np.inf)),
            "fixed_value": float(self.graph.h1_rhs @ y) if fixed else None,
            "scope": "affine H1 equations; forced nonnegative faces not analyzed",
        }

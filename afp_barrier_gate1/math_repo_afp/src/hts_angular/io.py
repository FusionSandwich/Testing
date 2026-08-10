"""HDF5 serialization for positive quadratures and angular graph generators."""
from __future__ import annotations

import json
from pathlib import Path

import h5py

from .graph_generator import GraphGenerator
from .quadrature import PositiveQuadrature


def save_quadrature_hdf5(quadrature: PositiveQuadrature, path: str | Path) -> None:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    with h5py.File(target, "w") as h5:
        h5.attrs["schema"] = "hts-positive-quadrature-v1"
        h5.attrs["metadata"] = json.dumps(
            quadrature.metadata, sort_keys=True, default=str
        )
        h5.create_dataset("nodes", data=quadrature.nodes)
        h5.create_dataset("weights", data=quadrature.weights)


def load_quadrature_hdf5(path: str | Path) -> PositiveQuadrature:
    with h5py.File(path, "r") as h5:
        if h5.attrs.get("schema") != "hts-positive-quadrature-v1":
            raise ValueError("unsupported positive-quadrature HDF5 schema")
        return PositiveQuadrature(
            h5["nodes"][...],
            h5["weights"][...],
            json.loads(h5.attrs["metadata"]),
        )


def save_graph_hdf5(graph: GraphGenerator, path: str | Path) -> None:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    with h5py.File(target, "w") as h5:
        h5.attrs["schema"] = "hts-angular-graph-v1"
        h5.attrs["fit_residual_norm"] = graph.fit_residual_norm
        h5.attrs["metadata"] = json.dumps(graph.metadata, sort_keys=True, default=str)
        h5.create_dataset("nodes", data=graph.nodes)
        h5.create_dataset("weights", data=graph.weights)
        h5.create_dataset("conductances", data=graph.conductances)
        h5.create_dataset("generator", data=graph.generator)
        h5.create_dataset("edges", data=graph.edges)


def load_graph_hdf5(path: str | Path) -> GraphGenerator:
    with h5py.File(path, "r") as h5:
        if h5.attrs.get("schema") != "hts-angular-graph-v1":
            raise ValueError("unsupported angular-graph HDF5 schema")
        return GraphGenerator(
            nodes=h5["nodes"][...],
            weights=h5["weights"][...],
            conductances=h5["conductances"][...],
            generator=h5["generator"][...],
            edges=h5["edges"][...],
            fit_residual_norm=float(h5.attrs["fit_residual_norm"]),
            metadata=json.loads(h5.attrs["metadata"]),
        )

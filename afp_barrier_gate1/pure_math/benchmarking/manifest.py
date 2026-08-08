"""Immutable P2E manifest loading and scientific hashing."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any


def strict_json(payload: object) -> str:
    return json.dumps(payload, sort_keys=True, separators=(",", ":"), allow_nan=False)


def scientific_hash(payload: object) -> str:
    return hashlib.sha256(strict_json(payload).encode("utf-8")).hexdigest()


def manifest_path() -> Path:
    return Path(__file__).with_name("P2E_BENCHMARK_MANIFEST.json")


def load_manifest(path: str | Path | None = None) -> dict[str, Any]:
    source = manifest_path() if path is None else Path(path)
    payload = json.loads(
        source.read_text(encoding="utf-8"),
        parse_constant=lambda value: (_ for _ in ()).throw(ValueError(value)),
    )
    claimed = str(payload.pop("scientific_sha256"))
    actual = scientific_hash(payload)
    payload["scientific_sha256"] = claimed
    if claimed != actual:
        raise ArithmeticError(f"P2E manifest hash mismatch: {actual} != {claimed}")
    return payload

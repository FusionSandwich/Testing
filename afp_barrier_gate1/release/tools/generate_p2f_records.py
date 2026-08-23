#!/usr/bin/env python3
"""Regenerate the fixed P2F record checksum list without changing its scope."""

from __future__ import annotations

import hashlib
from pathlib import Path


PROJECT = Path(__file__).resolve().parents[2]
REPOSITORY = PROJECT.parent
RECORD = PROJECT / "benchmarks" / "p2f" / "P2F_RECORDS.sha256"


def main() -> None:
    paths: list[str] = []
    for line in RECORD.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        _, separator, path = line.partition("  ")
        if not separator:
            raise SystemExit(f"malformed record line: {line!r}")
        paths.append(path)

    output: list[str] = []
    for relative in paths:
        source = REPOSITORY / relative
        if not source.is_file():
            raise SystemExit(f"missing P2F record: {relative}")
        digest = hashlib.sha256(source.read_bytes()).hexdigest()
        output.append(f"{digest}  {relative}")
    RECORD.write_text("\n".join(output) + "\n", encoding="utf-8", newline="\n")
    print(f"P2F_RECORDS_REGENERATED files={len(output)}")


if __name__ == "__main__":
    main()

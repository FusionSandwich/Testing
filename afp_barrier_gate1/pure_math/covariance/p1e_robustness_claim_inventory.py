#!/usr/bin/env python3
"""List repository references to the former uniform robustness claim."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

TOKENS = (
    "Proposition 7.3",
    "K_*",
    "K_\\*",
    "R_rob",
    "C_rob",
    "R_{\\rm rob}",
    "C_{\\rm rob}",
    "support-preserving robustness",
    "robustness proposition",
    "all-level robustness",
    "uniform robustness",
    "latitude perturb",
    "perturb every northern ring",
    "perturb each northern ring",
    "straight-line differentiation",
    "h^3/K",
)
TEXT_SUFFIXES = {".md", ".py", ".lean", ".yml", ".yaml", ".json", ".toml", ".txt", ".tex", ".bib", ".cff", ".csv"}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path("."))
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()
    root = args.root.resolve()
    rows: list[dict[str, object]] = []
    for path in sorted(root.rglob("*")):
        if not path.is_file() or ".git" in path.parts or path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        try:
            lines = path.read_text(encoding="utf-8").splitlines()
        except UnicodeDecodeError:
            continue
        for number, line in enumerate(lines, 1):
            hits = [token for token in TOKENS if token in line]
            if hits:
                rows.append({"path": path.relative_to(root).as_posix(), "line": number, "tokens": hits, "text": line.strip()})
    payload = {"schema": "afp-prop73-inventory-v1", "count": len(rows), "rows": rows}
    rendered = json.dumps(payload, indent=2) + "\n"
    if args.report:
        args.report.write_text(rendered, encoding="utf-8")
    print(rendered, end="")


if __name__ == "__main__":
    main()

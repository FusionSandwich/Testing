"""Command-line runner for the deterministic P2F HTS case."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from .model import run_p2f


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    result = run_p2f()
    text = json.dumps(result, indent=2, sort_keys=True, allow_nan=False) + "\n"
    Path(args.output).write_text(text, encoding="utf-8")
    print(result["scientific_sha256"])
    print(result["summary"]["scientific_outcome"])


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Normalize the manifest-controlled release text surface to LF bytes."""

from __future__ import annotations

from pathlib import Path

from generate_release_manifest import OUTSIDE_RELEASE, RELEASE


TEXT_SUFFIXES = {
    ".bib",
    ".json",
    ".lean",
    ".log",
    ".lua",
    ".md",
    ".py",
    ".sha256",
    ".yaml",
    ".yml",
}


def normalize(path: Path) -> bool:
    if path.suffix.lower() not in TEXT_SUFFIXES:
        return False
    before = path.read_bytes()
    after = before.replace(b"\r\n", b"\n").replace(b"\r", b"\n")
    if path.suffix.lower() == ".log":
        after = b"\n".join(line.rstrip(b" \t") for line in after.split(b"\n"))
    if after == before:
        return False
    path.write_bytes(after)
    return True


def main() -> None:
    paths = [
        path
        for path in RELEASE.rglob("*")
        if path.is_file() and "tmp" not in path.relative_to(RELEASE).parts
    ]
    paths.extend(OUTSIDE_RELEASE)
    paths = sorted(set(paths))
    changed = sum(int(normalize(path)) for path in paths)
    remaining = [
        str(path)
        for path in paths
        if path.suffix.lower() in TEXT_SUFFIXES and b"\r" in path.read_bytes()
    ]
    if remaining:
        raise SystemExit(f"CR bytes remain: {remaining}")
    print(f"AFP_R6_TEXT_LF_NORMALIZED changed={changed} files={len(paths)}")


if __name__ == "__main__":
    main()

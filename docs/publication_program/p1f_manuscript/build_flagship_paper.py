#!/usr/bin/env python3
"""Build the flagship manuscript and its publication figure.

Run this file from any directory.  The output PDF is written to
``output/pdf/FLAGSHIP_MANUSCRIPT.pdf`` at the repository root.
"""

from __future__ import annotations

import os
from pathlib import Path
import subprocess

import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
SOURCE = HERE / "FLAGSHIP_MANUSCRIPT.md"
BIBLIOGRAPHY = HERE / "priority_sources.bib"
FIGURE = HERE / "proof_dependency_graph.png"
FILTER = HERE / "table_layout.lua"
HEADER = HERE / "paper_header.tex"
OUTPUT = ROOT / "output" / "pdf" / "FLAGSHIP_MANUSCRIPT.pdf"
TEMP = ROOT / "tmp" / "pdfs" / "p1f-build"


def draw_dependency_graph() -> None:
    """Render the audited proof dependency graph at publication resolution."""

    fig, ax = plt.subplots(figsize=(10.8, 7.0), constrained_layout=True)
    ax.set_xlim(0, 10.8)
    ax.set_ylim(0, 8.2)
    ax.axis("off")

    colors = {
        "foundation": "#E8F1FA",
        "frontier": "#D9EAD3",
        "geometry": "#FCE5CD",
        "stability": "#EADCF8",
        "construction": "#FFF2CC",
        "matching": "#CFE2F3",
    }

    nodes = {
        "definitions": (3.0, 7.55, "Definitions and\nsampled quotient", "foundation"),
        "covariance": (3.0, 6.55, "Exact covariance and\ntwo-defect identities", "foundation"),
        "trace": (3.0, 5.55, "Sharp trace bound", "frontier"),
        "frontier": (3.0, 4.55, "Product frontier", "frontier"),
        "equality": (1.65, 3.35, "Equality conditions", "geometry"),
        "assembly": (1.65, 2.15, "Tangent frames and\nglobal assembly", "geometry"),
        "master": (4.35, 3.35, "Normalized master budget", "stability"),
        "transfers": (4.35, 2.15, "Conditional stability\ntransfers", "stability"),
        "meshes": (8.45, 4.55, "Explicit local meshes\nin d = 2, 3", "construction"),
        "upper": (8.45, 3.35, "Construction upper bounds", "construction"),
        "matching": (6.65, 1.15, "Matching-order theorem", "matching"),
    }

    box_w, box_h = 2.55, 0.66
    for _, (x, y, label, kind) in nodes.items():
        patch = FancyBboxPatch(
            (x - box_w / 2, y - box_h / 2),
            box_w,
            box_h,
            boxstyle="round,pad=0.05,rounding_size=0.08",
            linewidth=1.25,
            edgecolor="#334155",
            facecolor=colors[kind],
        )
        ax.add_patch(patch)
        ax.text(x, y, label, ha="center", va="center", fontsize=10.2, color="#172033")

    def arrow(source: str, target: str) -> None:
        x1, y1, *_ = nodes[source]
        x2, y2, *_ = nodes[target]
        ax.annotate(
            "",
            xy=(x2, y2 + box_h / 2),
            xytext=(x1, y1 - box_h / 2),
            arrowprops={"arrowstyle": "-|>", "lw": 1.35, "color": "#475569"},
        )

    for source, target in (
        ("definitions", "covariance"),
        ("covariance", "trace"),
        ("trace", "frontier"),
        ("frontier", "equality"),
        ("equality", "assembly"),
        ("trace", "master"),
        ("master", "transfers"),
        ("meshes", "upper"),
        ("upper", "matching"),
        ("frontier", "matching"),
    ):
        arrow(source, target)

    ax.text(
        5.4,
        0.25,
        "The all-dimensional lower frontier does not depend on the explicit meshes.",
        ha="center",
        va="center",
        fontsize=9.5,
        color="#475569",
    )
    fig.savefig(FIGURE, dpi=240, facecolor="white")
    plt.close(fig)


def build_pdf() -> None:
    draw_dependency_graph()
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    TEMP.mkdir(parents=True, exist_ok=True)

    lines = SOURCE.read_text(encoding="utf-8").splitlines()
    if not lines or not lines[0].startswith("# "):
        raise RuntimeError("the manuscript must begin with one level-one title")
    title = lines[0][2:].strip()
    body = "\n".join(lines[1:]) + "\n"
    prepared = TEMP / "FLAGSHIP_MANUSCRIPT.prepared.md"
    prepared.write_text(body, encoding="utf-8")

    env = dict(os.environ)
    env.setdefault("SOURCE_DATE_EPOCH", "1785900000")
    command = [
        "pandoc",
        str(prepared),
        "--from=markdown",
        "--standalone",
        "--toc",
        "--citeproc",
        f"--bibliography={BIBLIOGRAPHY}",
        f"--lua-filter={FILTER}",
        f"--include-in-header={HEADER}",
        "--pdf-engine=xelatex",
        f"--resource-path={HERE}",
        f"--metadata=title:{title}",
        "--metadata=date:",
        "-V",
        "documentclass=article",
        "-V",
        "fontsize=10pt",
        "-V",
        "geometry:margin=0.82in",
        "-V",
        "colorlinks=true",
        "-V",
        "linkcolor=blue",
        "-V",
        "urlcolor=blue",
        "-o",
        str(OUTPUT),
    ]
    subprocess.run(command, cwd=ROOT, env=env, check=True)
    print(OUTPUT)


if __name__ == "__main__":
    build_pdf()

#!/usr/bin/env python3
"""
Build a φ / Fibonacci-scaled tesseract lattice and project it.

Demonstrates hierarchical spatial structure usable for indexing.
"""

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from tesseract_medium.lattice import TesseractLattice, PHI
from tesseract_medium.visualize import save_lattice_projection

OUT = Path(__file__).resolve().parent / "out"
OUT.mkdir(exist_ok=True)


def main() -> None:
    print(f"φ = {PHI:.10f}")
    lat = TesseractLattice(depth=2, use_fibonacci_ratios=True)
    print(f"Lattice points at depth=2: {len(lat)}")

    # Show a few hierarchical indices
    for pt in [(0.1, 0.2, 0.3, 0.4), (0.7, 0.7, 0.7, 0.7)]:
        idx = lat.hierarchical_index(pt)
        print(f"  hierarchical_index{pt} = {idx}")

    proj = lat.project_3d(drop_axis=3)
    path = save_lattice_projection(
        proj,
        OUT / "tesseract_lattice_depth2.png",
        title="Tesseract lattice (depth=2, φ-scaled) — 3D projection",
    )
    print(f"Wrote {path}")


if __name__ == "__main__":
    main()

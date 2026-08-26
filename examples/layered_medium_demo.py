#!/usr/bin/env python3
"""
Demonstrate the layered multi-sheet tesseract medium and
kaleidoscopic / mirror branching.

Produces two PNGs:
  - layered_medium.png          : multi-sheet stack at angles with variance
  - kaleidoscope_branch.png     : single lattice + recursive mirror branches
"""

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from tesseract_medium.lattice import TesseractLattice, LayeredTesseractMedium, PHI
from tesseract_medium.visualize import save_lattice_projection, save_layered_projection

OUT = Path(__file__).resolve().parent / "out"
OUT.mkdir(exist_ok=True)


def main() -> None:
    print(f"φ = {PHI:.10f}")

    # ------------------------------------------------------------------
    # 1. Layered multi-sheet medium (pack-of-paper model)
    # ------------------------------------------------------------------
    medium = LayeredTesseractMedium(
        n_layers=6,
        depth=1,
        use_fibonacci_ratios=True,
        angle_span_deg=30.0,
        variance=0.04,
        seed=42,
    )
    print(f"Layered medium: {medium.n_layers} sheets, total points = {len(medium)}")

    layer_projs = [medium.project_layer_3d(i) for i in range(medium.n_layers)]
    path = save_layered_projection(
        layer_projs,
        OUT / "layered_medium.png",
        title="Layered Tesseract Medium — angled sheets with variance (non-interfering)",
    )
    print(f"Wrote {path}")

    # ------------------------------------------------------------------
    # 2. Kaleidoscopic branching around a single lattice
    # ------------------------------------------------------------------
    lat = TesseractLattice(depth=1, use_fibonacci_ratios=True)
    print(f"Base lattice points: {len(lat)}")

    branches = lat.kaleidoscope_branch(
        center=(0.5, 0.5, 0.5, 0.5),
        scale=1.0 / PHI,
        n_mirrors=6,
    )
    # Project the 4D branch cloud to 3D
    branch_3d = branches[:, [0, 1, 2]]  # drop w
    path2 = save_lattice_projection(
        branch_3d,
        OUT / "kaleidoscope_branch.png",
        title="Kaleidoscopic mirror branching (φ-scaled, 6 mirrors)",
        color="C1",
        alpha=0.65,
        s=12,
    )
    print(f"Wrote {path2}")
    print("Done.")


if __name__ == "__main__":
    main()

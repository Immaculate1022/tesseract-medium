#!/usr/bin/env python3
"""
Demonstrate orientation reversal around a loop that crosses the twist seam.

This is the concrete signature of Möbius-type structure inside the medium.
"""

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from tesseract_medium.lattice import TesseractLattice
from tesseract_medium.orientation import OrientationTracker


def nearest(lat: TesseractLattice, target):
    import numpy as np

    pts = lat.as_array()
    d = np.linalg.norm(pts - np.asarray(target), axis=1)
    return int(np.argmin(d))


def main() -> None:
    lat = TesseractLattice(depth=1)
    tracker = OrientationTracker(lat)

    # Build a simple rectangular loop in the (w, y) directions that crosses
    # the twist seam (w=0.5, y>0.5).
    # We pick four corners that approximate that loop on the lattice.
    a = nearest(lat, (0.0, 0.5, 0.8, 0.5))
    b = nearest(lat, (1.0, 0.5, 0.8, 0.5))
    c = nearest(lat, (1.0, 0.5, 0.2, 0.5))
    d = nearest(lat, (0.0, 0.5, 0.2, 0.5))

    loop = [a, b, c, d, a]
    print("Loop indices:", loop)
    print("Loop points:")
    for i in loop:
        print(" ", lat.points[i])

    reversed_orient = tracker.closed_loop_reverses(loop)
    print(f"Orientation reversed after loop: {reversed_orient}")
    print(f"Final orientation sign: {tracker.orientation_sign():+.0f}")

    # A loop that stays away from the seam should preserve orientation
    a2 = nearest(lat, (0.0, 0.5, 0.2, 0.5))
    b2 = nearest(lat, (1.0, 0.5, 0.2, 0.5))
    c2 = nearest(lat, (1.0, 0.5, 0.0, 0.5))
    d2 = nearest(lat, (0.0, 0.5, 0.0, 0.5))
    loop2 = [a2, b2, c2, d2, a2]
    reversed2 = tracker.closed_loop_reverses(loop2)
    print(f"Control loop (away from seam) reversed: {reversed2}")


if __name__ == "__main__":
    main()

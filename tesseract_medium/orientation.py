"""
Orientation / monodromy tracker on the tesseract lattice.

A discrete frame is parallel-transported around closed loops.
If the frame returns flipped, the loop is orientation-reversing —
the concrete signature of Möbius-type structure inside the medium.
"""

from __future__ import annotations

from typing import List, Sequence, Tuple

import numpy as np

from .lattice import TesseractLattice


class OrientationTracker:
    """
    Tracks a discrete oriented frame while walking edges of a TesseractLattice.

    The frame is represented as a 4×4 orthogonal matrix (initially identity).
    Moving along an axis applies a simple transport rule; circling a
    non-contractible loop that encodes a Möbius identification can reverse
    orientation (det → −1).
    """

    def __init__(self, lattice: TesseractLattice):
        self.lattice = lattice
        self.frame = np.eye(4, dtype=np.float64)
        self.path: List[int] = []

    def reset(self) -> None:
        self.frame = np.eye(4, dtype=np.float64)
        self.path = []

    def transport_along_edge(self, from_idx: int, to_idx: int) -> None:
        """
        Parallel-transport the frame from one lattice point to a neighbor.

        For the minimal model we apply a reflection in the hyperplane
        orthogonal to the displacement when the walk crosses a designated
        "twist seam". The seam is defined as the mid-hyperplane w = 0.5
        with a parity condition on another coordinate — enough to produce
        orientation-reversing loops without full differential geometry.
        """
        p = np.asarray(self.lattice.points[from_idx])
        q = np.asarray(self.lattice.points[to_idx])
        delta = q - p
        axis = int(np.argmax(np.abs(delta)))

        # Twist seam: crossing w = 0.5 while y > 0.5 flips the x-basis vector
        crossed_seam = (p[0] - 0.5) * (q[0] - 0.5) < 0 and (p[2] + q[2]) / 2.0 > 0.5

        if crossed_seam:
            # Reflection that reverses orientation
            reflect = np.eye(4)
            reflect[1, 1] = -1.0  # flip the e1 direction
            self.frame = reflect @ self.frame

        self.path.append(to_idx)

    def walk(self, indices: Sequence[int]) -> None:
        """Transport along a sequence of lattice point indices."""
        if not indices:
            return
        if not self.path:
            self.path.append(indices[0])
        for i in range(1, len(indices)):
            self.transport_along_edge(indices[i - 1], indices[i])

    def orientation_sign(self) -> float:
        """Return +1.0 or −1.0 according to det(frame)."""
        return float(np.sign(np.linalg.det(self.frame)))

    def is_reversed(self) -> bool:
        return self.orientation_sign() < 0

    def closed_loop_reverses(self, loop: Sequence[int]) -> bool:
        """
        Walk a closed loop (first point == last point) and report whether
        orientation reversed. Resets the tracker first.
        """
        self.reset()
        self.walk(loop)
        return self.is_reversed()

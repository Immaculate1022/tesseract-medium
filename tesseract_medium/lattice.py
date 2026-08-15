"""
4D tesseract lattice with Fibonacci / golden-ratio recursive subdivision.

Provides a discrete spatial medium that can be used for hierarchical
indexing, adjacency queries, and as the ambient space for orientation
transport and dynamical slices.
"""

from __future__ import annotations

import itertools
from typing import Iterable, List, Sequence, Tuple

import numpy as np

# Golden ratio
PHI = (1.0 + 5.0 ** 0.5) / 2.0


def fibonacci(n: int) -> int:
    """Return the n-th Fibonacci number (F0=0, F1=1)."""
    if n < 0:
        raise ValueError("n must be non-negative")
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a


Point4 = Tuple[float, float, float, float]


class TesseractLattice:
    """
    Unit tesseract [0,1]^4 with optional recursive subdivision.

    Subdivision ratios default to successive approximations of 1/φ so that
    the hierarchy is self-similar under golden-ratio scaling.
    """

    def __init__(self, depth: int = 0, use_fibonacci_ratios: bool = True):
        """
        Parameters
        ----------
        depth :
            Number of recursive subdivision levels (0 = only the 16 corners).
        use_fibonacci_ratios :
            If True, split ratios follow Fibonacci proportions;
            otherwise pure powers of 1/φ are used.
        """
        self.depth = max(0, int(depth))
        self.use_fibonacci_ratios = use_fibonacci_ratios
        self.points: List[Point4] = []
        self._build()

    # ------------------------------------------------------------------
    # Construction
    # ------------------------------------------------------------------
    def _split_ratios(self, level: int) -> List[float]:
        """Return ordered split positions in (0,1) for a given level."""
        if level <= 0:
            return []
        if self.use_fibonacci_ratios:
            # Use ratios F_k / F_{k+2} which converge to 1/φ², etc.
            ratios = []
            for k in range(1, level + 1):
                fk = fibonacci(k)
                fk2 = fibonacci(k + 2)
                if fk2 > 0:
                    ratios.append(fk / fk2)
            # Also include the complementary φ-related cuts
            ratios = sorted(set(ratios + [1.0 - r for r in ratios]))
            return [r for r in ratios if 0.0 < r < 1.0]
        else:
            # Pure geometric sequence of 1/φ powers
            ratios = [PHI ** (-k) for k in range(1, level + 1)]
            ratios = sorted(set(ratios + [1.0 - r for r in ratios]))
            return [r for r in ratios if 0.0 < r < 1.0]

    def _build(self) -> None:
        # Base corners of the unit tesseract
        corners = list(itertools.product([0.0, 1.0], repeat=4))
        points = set(corners)

        if self.depth > 0:
            cuts = self._split_ratios(self.depth)
            # Add all combinations of {0,1} ∪ cuts in each coordinate
            coords = [0.0, 1.0] + cuts
            for p in itertools.product(coords, repeat=4):
                points.add(tuple(float(x) for x in p))

        self.points = sorted(points)

    # ------------------------------------------------------------------
    # Queries
    # ------------------------------------------------------------------
    def __len__(self) -> int:
        return len(self.points)

    def as_array(self) -> np.ndarray:
        """Return points as an (N, 4) float64 array."""
        return np.asarray(self.points, dtype=np.float64)

    def neighbors(self, idx: int, tol: float = 1e-9) -> List[int]:
        """
        Return indices of points that differ in exactly one coordinate
        by a single edge step (axis-aligned adjacency on the current lattice).
        """
        p = np.asarray(self.points[idx])
        pts = self.as_array()
        diff = np.abs(pts - p)
        # Exactly one coordinate differs; others match
        n_diff = (diff > tol).sum(axis=1)
        mask = n_diff == 1
        return list(np.where(mask)[0])

    def project_3d(self, drop_axis: int = 3) -> np.ndarray:
        """Orthographic projection by dropping one coordinate (default w)."""
        pts = self.as_array()
        keep = [i for i in range(4) if i != drop_axis]
        return pts[:, keep]

    def hierarchical_index(self, point: Sequence[float]) -> Tuple[int, ...]:
        """
        Map a point in [0,1]^4 to a coarse hierarchical multi-index
        based on which φ-scaled cell it falls into at each level.

        Returns a tuple of length `depth` (empty if depth=0).
        Useful as a starting point for fractal / hierarchical storage keys.
        """
        if self.depth == 0:
            return tuple()
        cuts = [0.0] + self._split_ratios(self.depth) + [1.0]
        cuts = sorted(set(cuts))
        indices = []
        for coord in point:
            # Find the interval index
            idx = 0
            for i in range(len(cuts) - 1):
                if cuts[i] <= coord <= cuts[i + 1]:
                    idx = i
                    break
            indices.append(idx)
        return tuple(indices)

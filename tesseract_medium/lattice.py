"""
4D tesseract lattice with Fibonacci / golden-ratio recursive subdivision,
infinite kaleidoscopic branching helpers, and layered multi-sheet medium.

Provides a discrete spatial medium that can be used for hierarchical
indexing, adjacency queries, and as the ambient space for orientation
transport and dynamical slices.

New in this version:
  - LayeredTesseractMedium: stack of sheets at arbitrary angles with
    controlled positional / rotational variance so layers never coincide.
  - Simple kaleidoscopic / mirror point generators for fractal branching.
"""

from __future__ import annotations

import itertools
from typing import Iterable, List, Optional, Sequence, Tuple

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

    # ------------------------------------------------------------------
    # Kaleidoscopic / mirror helpers
    # ------------------------------------------------------------------
    def mirror_points(self, axis: int = 0) -> np.ndarray:
        """
        Return a mirrored copy of the lattice points reflected across
        the mid-hyperplane of the chosen axis (default w = 0.5).
        This is the elementary building block of kaleidoscopic branching.
        """
        pts = self.as_array().copy()
        pts[:, axis] = 1.0 - pts[:, axis]
        return pts

    def kaleidoscope_branch(
        self,
        center: Optional[Sequence[float]] = None,
        scale: float = 1.0 / PHI,
        n_mirrors: int = 4,
    ) -> np.ndarray:
        """
        Generate a simple kaleidoscopic branch set around a center point.

        Starts from the lattice points, scales them toward `center` by
        `scale`, then produces `n_mirrors` reflected copies. Returns an
        (M, 4) array of points that can be used for fractal visualization
        or as seeds for further recursive branching.
        """
        pts = self.as_array()
        if center is None:
            center = np.array([0.5, 0.5, 0.5, 0.5])
        else:
            center = np.asarray(center, dtype=np.float64)

        # Contract toward center
        contracted = center + scale * (pts - center)

        branches = [contracted]
        for k in range(1, n_mirrors):
            # Cycle reflections across successive axes for a kaleidoscope effect
            axis = k % 4
            mirrored = contracted.copy()
            mirrored[:, axis] = 2.0 * center[axis] - mirrored[:, axis]
            branches.append(mirrored)

        return np.vstack(branches)


class LayeredTesseractMedium:
    """
    Multi-sheet tesseract medium: a stack of TesseractLattice instances
    placed at arbitrary angles with controlled variance so that layers
    never occupy identical coordinates (non-interfering pack-of-paper model).

    Each sheet is an independent lattice that can carry its own orientation
    and dynamics. The collection forms a dense volumetric medium while
    remaining geometrically distinct layer-by-layer.
    """

    def __init__(
        self,
        n_layers: int = 5,
        depth: int = 1,
        use_fibonacci_ratios: bool = True,
        angle_span_deg: float = 25.0,
        variance: float = 0.03,
        seed: Optional[int] = 42,
    ):
        """
        Parameters
        ----------
        n_layers :
            Number of sheets in the stack.
        depth :
            Subdivision depth for each individual lattice.
        use_fibonacci_ratios :
            Passed through to each TesseractLattice.
        angle_span_deg :
            Total angular fan (degrees) across which the sheets are tilted.
            Sheets are spaced evenly within [-span/2, +span/2].
        variance :
            Maximum random translational offset (in lattice units) applied
            independently to each sheet so they never perfectly coincide.
        seed :
            RNG seed for reproducible variance. None → non-deterministic.
        """
        self.n_layers = max(1, int(n_layers))
        self.depth = depth
        self.use_fibonacci_ratios = use_fibonacci_ratios
        self.angle_span_deg = float(angle_span_deg)
        self.variance = float(variance)
        self.seed = seed

        rng = np.random.default_rng(seed)

        self.layers: List[TesseractLattice] = []
        self.rotations: List[np.ndarray] = []   # 4×4 rotation matrices
        self.offsets: List[np.ndarray] = []     # 4-vectors

        if self.n_layers == 1:
            angles = [0.0]
        else:
            angles = np.linspace(
                -angle_span_deg / 2.0, angle_span_deg / 2.0, self.n_layers
            )

        for i, ang_deg in enumerate(angles):
            lat = TesseractLattice(depth=depth, use_fibonacci_ratios=use_fibonacci_ratios)
            self.layers.append(lat)

            # Simple rotation in the (x,y) plane (extendable to full SO(4))
            theta = np.deg2rad(ang_deg)
            c, s = np.cos(theta), np.sin(theta)
            R = np.eye(4)
            R[1, 1] = c
            R[1, 2] = -s
            R[2, 1] = s
            R[2, 2] = c
            self.rotations.append(R)

            # Small random translational variance
            off = rng.uniform(-variance, variance, size=4)
            self.offsets.append(off)

    def __len__(self) -> int:
        return sum(len(layer) for layer in self.layers)

    def layer_points(self, layer_idx: int) -> np.ndarray:
        """Return the transformed (rotated + offset) points of one sheet."""
        pts = self.layers[layer_idx].as_array()
        R = self.rotations[layer_idx]
        off = self.offsets[layer_idx]
        # Center → rotate → un-center → offset
        center = np.array([0.5, 0.5, 0.5, 0.5])
        centered = pts - center
        rotated = (R @ centered.T).T + center + off
        return rotated

    def all_points(self) -> np.ndarray:
        """Concatenate transformed points from every layer."""
        return np.vstack([self.layer_points(i) for i in range(self.n_layers)])

    def project_3d(self, drop_axis: int = 3) -> np.ndarray:
        """Orthographic 3D projection of the entire layered medium."""
        pts = self.all_points()
        keep = [i for i in range(4) if i != drop_axis]
        return pts[:, keep]

    def project_layer_3d(self, layer_idx: int, drop_axis: int = 3) -> np.ndarray:
        """3D projection of a single sheet."""
        pts = self.layer_points(layer_idx)
        keep = [i for i in range(4) if i != drop_axis]
        return pts[:, keep]

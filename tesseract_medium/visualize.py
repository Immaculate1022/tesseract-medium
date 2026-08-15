"""
Simple visualization helpers for escape-time images and lattice projections.
"""

from __future__ import annotations

from pathlib import Path
from typing import Optional

import numpy as np

try:
    import matplotlib.pyplot as plt
except ImportError:  # pragma: no cover
    plt = None


def save_escape_image(
    escape: np.ndarray,
    path: str | Path,
    cmap: str = "turbo",
    title: Optional[str] = None,
) -> Path:
    """Save an escape-time array as a PNG."""
    if plt is None:
        raise ImportError("matplotlib is required for visualization")

    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)

    fig, ax = plt.subplots(figsize=(8, 6))
    ax.imshow(escape, cmap=cmap, origin="lower")
    ax.set_axis_off()
    if title:
        ax.set_title(title)
    fig.tight_layout()
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    return path


def save_lattice_projection(
    points_3d: np.ndarray,
    path: str | Path,
    title: Optional[str] = None,
) -> Path:
    """Scatter-plot a 3D projection of the lattice."""
    if plt is None:
        raise ImportError("matplotlib is required for visualization")

    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)

    fig = plt.figure(figsize=(7, 7))
    ax = fig.add_subplot(111, projection="3d")
    ax.scatter(points_3d[:, 0], points_3d[:, 1], points_3d[:, 2], s=8, alpha=0.7)
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_zlabel("z")
    if title:
        ax.set_title(title)
    fig.tight_layout()
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    return path

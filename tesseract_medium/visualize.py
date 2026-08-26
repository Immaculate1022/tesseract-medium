"""
Simple visualization helpers for escape-time images, lattice projections,
and layered multi-sheet media.
"""

from __future__ import annotations

from pathlib import Path
from typing import List, Optional, Sequence

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
    color: str = "C0",
    alpha: float = 0.7,
    s: float = 8,
) -> Path:
    """Scatter-plot a 3D projection of the lattice."""
    if plt is None:
        raise ImportError("matplotlib is required for visualization")

    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)

    fig = plt.figure(figsize=(7, 7))
    ax = fig.add_subplot(111, projection="3d")
    ax.scatter(
        points_3d[:, 0], points_3d[:, 1], points_3d[:, 2],
        s=s, alpha=alpha, c=color,
    )
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_zlabel("z")
    if title:
        ax.set_title(title)
    fig.tight_layout()
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    return path


def save_layered_projection(
    layer_points_3d: Sequence[np.ndarray],
    path: str | Path,
    title: Optional[str] = None,
    alphas: Optional[Sequence[float]] = None,
    cmap_name: str = "viridis",
) -> Path:
    """
    Scatter-plot multiple layers of a multi-sheet medium in one 3D figure.

    Each layer is drawn with a distinct color and (optionally) its own alpha
    so the non-interfering pack-of-paper structure is visible.
    """
    if plt is None:
        raise ImportError("matplotlib is required for visualization")

    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)

    n = len(layer_points_3d)
    if alphas is None:
        alphas = [0.55] * n

    cmap = plt.get_cmap(cmap_name)
    colors = [cmap(i / max(n - 1, 1)) for i in range(n)]

    fig = plt.figure(figsize=(8, 8))
    ax = fig.add_subplot(111, projection="3d")

    for i, pts in enumerate(layer_points_3d):
        ax.scatter(
            pts[:, 0], pts[:, 1], pts[:, 2],
            s=10, alpha=alphas[i], c=[colors[i]],
            label=f"layer {i}",
        )

    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_zlabel("z")
    if title:
        ax.set_title(title)
    ax.legend(loc="upper right", fontsize=8)
    fig.tight_layout()
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    return path

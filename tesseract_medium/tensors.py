"""
Tensor mathematics layer for Tesseract Medium / PegaConstellation.

Provides practical multilinear algebra primitives that sit on top of the
existing 4D/5D geometric substrate:

- Rotation tensors (SO(4) / SO(5) plane rotations)
- Kronecker / tensor-product constructions for recursive nesting
- Simple contractions and einsum helpers
- Reflection / mirror operators as involutory tensors
- Hierarchical indexing via multi-linear maps

Backend: NumPy. Designed to be lightweight and immediately usable by
lattice.py, orientation.py, and the penteract kaleidoscope.
"""

from __future__ import annotations

import itertools
from typing import Iterable, List, Optional, Sequence, Tuple, Union

import numpy as np

# Re-export the golden ratio used throughout the constellation
PHI = (1.0 + np.sqrt(5.0)) / 2.0

ArrayLike = Union[np.ndarray, Sequence[float]]


# ---------------------------------------------------------------------------
# Core helpers
# ---------------------------------------------------------------------------

def as_tensor(x: ArrayLike, dtype=np.float64) -> np.ndarray:
    """Convert input to a contiguous float tensor."""
    return np.asarray(x, dtype=dtype)


def kron(*arrays: np.ndarray) -> np.ndarray:
    """Multi-argument Kronecker product (tensor product of matrices)."""
    result = arrays[0]
    for a in arrays[1:]:
        result = np.kron(result, a)
    return result


def tensor_product(*arrays: np.ndarray) -> np.ndarray:
    """
    Outer / tensor product of vectors or higher-rank arrays.
    Equivalent to successive np.multiply.outer.
    """
    result = arrays[0]
    for a in arrays[1:]:
        result = np.multiply.outer(result, a)
    return result


def contract(a: np.ndarray, b: np.ndarray, axes: Union[int, Tuple[int, int]] = -1) -> np.ndarray:
    """
    Simple contraction of the last axis of `a` with the first axis of `b`
    (or an explicit pair of axes).
    """
    if isinstance(axes, int):
        return np.tensordot(a, b, axes=([axes], [0]))
    return np.tensordot(a, b, axes=axes)


def einsum(subscripts: str, *operands: np.ndarray) -> np.ndarray:
    """Thin wrapper around np.einsum for discoverability."""
    return np.einsum(subscripts, *operands)


# ---------------------------------------------------------------------------
# Plane rotations → rotation tensors
# ---------------------------------------------------------------------------

def plane_rotation_matrix(dim: int, i: int, j: int, theta: float) -> np.ndarray:
    """
    Elementary Givens / plane rotation in R^dim that rotates the (i,j)-plane
    by angle theta. Returns a dim × dim orthogonal matrix.
    """
    R = np.eye(dim)
    c, s = np.cos(theta), np.sin(theta)
    R[i, i] = c
    R[i, j] = -s
    R[j, i] = s
    R[j, j] = c
    return R


def so_n_rotation(dim: int, angles: Sequence[float]) -> np.ndarray:
    """
    Build an element of SO(dim) from a sequence of plane angles.

    The number of independent planes is C(dim, 2).
    Order of planes follows the lexicographic ordering of pairs (i < j).

    Parameters
    ----------
    dim : int
        Ambient dimension (4 for tesseract, 5 for penteract, …).
    angles : sequence of float
        Length must equal C(dim, 2). Missing angles are treated as 0.

    Returns
    -------
    R : (dim, dim) ndarray
        Orthogonal matrix with det = +1 (up to floating-point error).
    """
    planes = list(itertools.combinations(range(dim), 2))
    n_planes = len(planes)
    if len(angles) < n_planes:
        angles = list(angles) + [0.0] * (n_planes - len(angles))

    R = np.eye(dim)
    for (i, j), theta in zip(planes, angles):
        if abs(theta) > 1e-15:
            R = plane_rotation_matrix(dim, i, j, theta) @ R
    return R


def rotate_points(points: np.ndarray, R: np.ndarray) -> np.ndarray:
    """
    Apply a linear transformation R to a set of points.

    points : (N, dim) or (dim,)
    R      : (dim, dim)
    """
    points = as_tensor(points)
    if points.ndim == 1:
        return R @ points
    return points @ R.T


# ---------------------------------------------------------------------------
# Reflection / mirror tensors (involutions)
# ---------------------------------------------------------------------------

def reflection_tensor(dim: int, axis: int) -> np.ndarray:
    """
    Householder-style reflection across the hyperplane orthogonal to the
    given coordinate axis. Satisfies R @ R = I.
    """
    R = np.eye(dim)
    R[axis, axis] = -1.0
    return R


def mirror_operator(dim: int, normal: ArrayLike) -> np.ndarray:
    """
    Reflection through the hyperplane with the given normal vector.
    Returns an orthogonal involution (R @ R = I, det = -1).
    """
    n = as_tensor(normal)
    n = n / (np.linalg.norm(n) + 1e-15)
    return np.eye(dim) - 2.0 * np.outer(n, n)


# ---------------------------------------------------------------------------
# Recursive / hierarchical constructions
# ---------------------------------------------------------------------------

def phi_scaled_embedding(dim: int, scale: float = None) -> np.ndarray:
    """
    Diagonal scaling tensor that implements one step of φ-recursive nesting.
    Used by kaleidoscopic branching and hierarchical lattices.
    """
    if scale is None:
        scale = 1.0 / PHI
    return np.eye(dim) * scale


def recursive_kronecker_nest(
    base: np.ndarray,
    depth: int,
    scale: float = None,
) -> np.ndarray:
    """
    Build a hierarchical operator by repeated Kronecker product with a
    scaled identity. Useful for generating multi-scale adjacency or
    transition tensors.

    depth=0 → base
    depth=1 → kron(base, scale*I)
    depth=2 → kron(kron(base, scale*I), scale*I)  etc.
    """
    if scale is None:
        scale = 1.0 / PHI
    result = base
    I = np.eye(base.shape[0]) * scale
    for _ in range(depth):
        result = np.kron(result, I)
    return result


def hierarchical_index_tensor(
    levels: Sequence[int],
    base_dim: int = 4,
) -> np.ndarray:
    """
    Construct a multi-linear index map that encodes a hierarchical address
    (level_0, level_1, …) into a single vector in R^{base_dim}.

    This is a lightweight stand-in for a full tensor-train / Tucker core;
    it already lets downstream code treat hierarchical lattice keys as
    ordinary vectors that can be rotated, reflected, and contracted.
    """
    # Simple φ-weighted embedding of integer coordinates
    coords = as_tensor(levels, dtype=np.float64)
    n = len(coords)
    weights = np.array([PHI ** (-k) for k in range(n)])
    # Pad or project to base_dim
    if n >= base_dim:
        return (coords * weights)[:base_dim]
    out = np.zeros(base_dim)
    out[:n] = coords * weights
    return out


# ---------------------------------------------------------------------------
# Orientation-aware transport helpers
# ---------------------------------------------------------------------------

def parallel_transport_step(
    frame: np.ndarray,
    connection: np.ndarray,
    delta: ArrayLike,
) -> np.ndarray:
    """
    First-order parallel transport of an orthonormal frame along a discrete
    displacement `delta` under a connection form `connection`.

    frame      : (dim, dim)   current orthonormal frame (columns = basis vectors)
    connection : (dim, dim, dim)  or a simpler (dim, dim) matrix for the step
    delta      : (dim,) displacement vector

    Returns the transported frame (still approximately orthonormal).
    """
    frame = as_tensor(frame)
    delta = as_tensor(delta)

    if connection.ndim == 2:
        # Simple matrix connection: Γ · δ
        omega = connection @ delta
        # Infinitesimal rotation generated by the skew-symmetric part
        skew = 0.5 * (omega - omega.T)
        # Approximate exp(skew) ≈ I + skew
        return frame + frame @ skew

    # Full Christoffel-style (dim, dim, dim) – contract last index with delta
    omega = np.einsum("ijk,k->ij", connection, delta)
    skew = 0.5 * (omega - omega.T)
    return frame + frame @ skew


def orientation_sign(frame: np.ndarray) -> float:
    """Return +1 or -1 according to the orientation of the frame."""
    return float(np.sign(np.linalg.det(frame)))


# ---------------------------------------------------------------------------
# Convenience factories for the constellation
# ---------------------------------------------------------------------------

def tesseract_rotation(angles: Sequence[float]) -> np.ndarray:
    """SO(4) rotation from 6 plane angles."""
    return so_n_rotation(4, angles)


def penteract_rotation(angles: Sequence[float]) -> np.ndarray:
    """SO(5) rotation from 10 plane angles."""
    return so_n_rotation(5, angles)


def phi_harmonic_angles(time: float, dim: int = 4, speed: float = 1.0) -> List[float]:
    """
    Generate a set of plane angles whose frequencies are successive powers
    of φ — the same harmonic family used by the kaleidoscope engines.
    """
    n_planes = dim * (dim - 1) // 2
    return [time * speed * 0.2 * (PHI ** (i * 0.35)) for i in range(n_planes)]


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

__all__ = [
    "PHI",
    "as_tensor",
    "kron",
    "tensor_product",
    "contract",
    "einsum",
    "plane_rotation_matrix",
    "so_n_rotation",
    "rotate_points",
    "reflection_tensor",
    "mirror_operator",
    "phi_scaled_embedding",
    "recursive_kronecker_nest",
    "hierarchical_index_tensor",
    "parallel_transport_step",
    "orientation_sign",
    "tesseract_rotation",
    "penteract_rotation",
    "phi_harmonic_angles",
]

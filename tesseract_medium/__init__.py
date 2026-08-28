"""
Tesseract Medium — 4D non-orientable fractal geometry substrate.

Modules:
  lattice      – unit tesseract + φ / Fibonacci subdivision,
                 kaleidoscopic mirror helpers,
                 LayeredTesseractMedium (angled multi-sheet stack)
  dynamics     – Möbius-composed quadratic maps
  orientation  – monodromy / orientation-flip tracker
  visualize    – 2D/3D rendering helpers (including layered projections)
  tensors      – multilinear algebra layer (rotations, Kronecker nesting,
                 reflections, hierarchical indices, parallel transport)
"""

from .lattice import TesseractLattice, LayeredTesseractMedium, PHI, fibonacci
from .dynamics import moebius, iterate, mandelbrot_escape, julia_escape
from .orientation import OrientationTracker
from .tensors import (
    so_n_rotation,
    tesseract_rotation,
    penteract_rotation,
    rotate_points,
    reflection_tensor,
    mirror_operator,
    phi_scaled_embedding,
    recursive_kronecker_nest,
    hierarchical_index_tensor,
    parallel_transport_step,
    orientation_sign,
    phi_harmonic_angles,
    kron,
    tensor_product,
    contract,
    einsum,
)

__version__ = "0.3.0"
__all__ = [
    "TesseractLattice",
    "LayeredTesseractMedium",
    "PHI",
    "fibonacci",
    "moebius",
    "iterate",
    "mandelbrot_escape",
    "julia_escape",
    "OrientationTracker",
    # tensor layer
    "so_n_rotation",
    "tesseract_rotation",
    "penteract_rotation",
    "rotate_points",
    "reflection_tensor",
    "mirror_operator",
    "phi_scaled_embedding",
    "recursive_kronecker_nest",
    "hierarchical_index_tensor",
    "parallel_transport_step",
    "orientation_sign",
    "phi_harmonic_angles",
    "kron",
    "tensor_product",
    "contract",
    "einsum",
]

"""
Tesseract Medium — 4D non-orientable fractal geometry substrate.

Modules:
  lattice      – unit tesseract + φ / Fibonacci subdivision,
                 kaleidoscopic mirror helpers,
                 LayeredTesseractMedium (angled multi-sheet stack)
  dynamics     – Möbius-composed quadratic maps
  orientation  – monodromy / orientation-flip tracker
  visualize    – 2D/3D rendering helpers (including layered projections)
"""

from .lattice import TesseractLattice, LayeredTesseractMedium, PHI, fibonacci
from .dynamics import moebius, iterate, mandelbrot_escape, julia_escape
from .orientation import OrientationTracker

__version__ = "0.2.0"
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
]

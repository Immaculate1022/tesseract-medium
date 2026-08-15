"""
Tesseract Medium — 4D non-orientable fractal geometry substrate.

Modules:
  lattice      – unit tesseract + φ / Fibonacci subdivision
  dynamics     – Möbius-composed quadratic maps
  orientation  – monodromy / orientation-flip tracker
  visualize    – 2D rendering helpers
"""

from .lattice import TesseractLattice, PHI, fibonacci
from .dynamics import moebius, iterate, mandelbrot_escape, julia_escape
from .orientation import OrientationTracker

__version__ = "0.1.0"
__all__ = [
    "TesseractLattice",
    "PHI",
    "fibonacci",
    "moebius",
    "iterate",
    "mandelbrot_escape",
    "julia_escape",
    "OrientationTracker",
]

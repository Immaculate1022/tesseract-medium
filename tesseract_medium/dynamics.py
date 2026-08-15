"""
Möbius-composed quadratic dynamics (Mandelbrot / Julia style).

Implements iteration of the form
    z ↦ M(z² + c)
where M is a Möbius transformation. This injects controlled twist /
inversion into the classical fractal iteration while remaining
computationally cheap and easy to visualize on 2D slices.
"""

from __future__ import annotations

from typing import Callable, Optional, Tuple

import numpy as np

ComplexArray = np.ndarray


def moebius(
    z: ComplexArray,
    a: complex = 1.0,
    b: complex = 0.0,
    c: complex = 0.0,
    d: complex = 1.0,
) -> ComplexArray:
    """
    Apply the Möbius transformation (a z + b) / (c z + d).

    Default is the identity. Choosing c ≠ 0 introduces inversion;
    non-real coefficients introduce rotation / twist.
    """
    return (a * z + b) / (c * z + d)


def iterate(
    z0: ComplexArray,
    c: complex,
    max_iter: int = 100,
    escape_radius: float = 2.0,
    moebius_params: Optional[Tuple[complex, complex, complex, complex]] = None,
) -> Tuple[ComplexArray, np.ndarray]:
    """
    Iterate z ↦ M(z² + c) starting from z0.

    Returns
    -------
    z_final : final complex values (escaped points may be large)
    escape_iter : iteration count at which |z| first exceeded escape_radius
                  (max_iter if never escaped)
    """
    if moebius_params is None:
        a, b, c_m, d = 1.0 + 0j, 0.0 + 0j, 0.0 + 0j, 1.0 + 0j
    else:
        a, b, c_m, d = moebius_params

    z = np.array(z0, dtype=np.complex128, copy=True)
    escape = np.full(z.shape, max_iter, dtype=np.int32)
    active = np.ones(z.shape, dtype=bool)

    for i in range(max_iter):
        z_sq_c = z * z + c
        z_new = moebius(z_sq_c, a, b, c_m, d)
        # Only update still-active points
        z = np.where(active, z_new, z)
        escaped_now = active & (np.abs(z) > escape_radius)
        escape[escaped_now] = i + 1
        active &= ~escaped_now
        if not np.any(active):
            break

    return z, escape


def mandelbrot_escape(
    width: int = 800,
    height: int = 600,
    re_min: float = -2.0,
    re_max: float = 1.0,
    im_min: float = -1.2,
    im_max: float = 1.2,
    max_iter: int = 120,
    moebius_params: Optional[Tuple[complex, complex, complex, complex]] = None,
) -> np.ndarray:
    """
    Compute escape-time image for the Möbius-twisted Mandelbrot set.

    Returns an (height, width) array of iteration counts.
    """
    xs = np.linspace(re_min, re_max, width)
    ys = np.linspace(im_min, im_max, height)
    re, im = np.meshgrid(xs, ys)
    c = re + 1j * im
    z0 = np.zeros_like(c)
    _, escape = iterate(z0, c, max_iter=max_iter, moebius_params=moebius_params)
    # When c is an array we need a slight adaptation: iterate each c
    # The simple vectorised path above assumes scalar c; for full
    # Mandelbrot we re-implement a tight loop over c.
    escape = np.zeros(c.shape, dtype=np.int32)
    z = np.zeros_like(c)
    active = np.ones(c.shape, dtype=bool)

    if moebius_params is None:
        a, b, cm, d = 1.0 + 0j, 0.0 + 0j, 0.0 + 0j, 1.0 + 0j
    else:
        a, b, cm, d = moebius_params

    for i in range(max_iter):
        z_sq_c = z * z + c
        z_new = (a * z_sq_c + b) / (cm * z_sq_c + d)
        z = np.where(active, z_new, z)
        escaped_now = active & (np.abs(z) > 2.0)
        escape[escaped_now] = i + 1
        active &= ~escaped_now
        if not np.any(active):
            break

    escape[active] = max_iter
    return escape


def julia_escape(
    c: complex,
    width: int = 800,
    height: int = 600,
    re_min: float = -1.5,
    re_max: float = 1.5,
    im_min: float = -1.5,
    im_max: float = 1.5,
    max_iter: int = 120,
    moebius_params: Optional[Tuple[complex, complex, complex, complex]] = None,
) -> np.ndarray:
    """
    Compute escape-time image for the Möbius-twisted Julia set of a fixed c.
    """
    xs = np.linspace(re_min, re_max, width)
    ys = np.linspace(im_min, im_max, height)
    re, im = np.meshgrid(xs, ys)
    z0 = re + 1j * im
    _, escape = iterate(z0, c, max_iter=max_iter, moebius_params=moebius_params)
    return escape

#!/usr/bin/env python3
"""
Render classical and Möbius-twisted Mandelbrot slices.

Demonstrates the dynamics layer of the Tesseract Medium.
Output images are written to examples/out/.
"""

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from tesseract_medium.dynamics import mandelbrot_escape
from tesseract_medium.visualize import save_escape_image

OUT = Path(__file__).resolve().parent / "out"
OUT.mkdir(exist_ok=True)


def main() -> None:
    print("Computing classical Mandelbrot slice …")
    esc_classical = mandelbrot_escape(width=720, height=540, max_iter=100)
    p1 = save_escape_image(
        esc_classical,
        OUT / "mandelbrot_classical.png",
        title="Classical Mandelbrot (identity Möbius)",
    )
    print(f"  wrote {p1}")

    # A simple twist: rotation + mild inversion
    twist = (
        0.8 + 0.3j,   # a
        0.1j,         # b
        0.15,         # c  (introduces inversion)
        1.0 + 0.0j,   # d
    )
    print("Computing Möbius-twisted Mandelbrot slice …")
    esc_twist = mandelbrot_escape(
        width=720, height=540, max_iter=100, moebius_params=twist
    )
    p2 = save_escape_image(
        esc_twist,
        OUT / "mandelbrot_moebius_twist.png",
        title="Möbius-twisted Mandelbrot",
    )
    print(f"  wrote {p2}")
    print("Done.")


if __name__ == "__main__":
    main()

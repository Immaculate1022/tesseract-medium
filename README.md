# Tesseract Medium

**An experimental Python toolkit for exploring a discrete 4D tesseract lattice, φ/Fibonacci subdivision, Möbius-composed fractal slices, orientation flips, layered point sets, and NumPy tensor utilities.**

It is for Python users who want a small, runnable starting point for geometric experiments, visualizations, or related research prototypes. Clone the repository, install its two dependencies, and run an example to get started.

PegaConstellation · Gregory Scott Davis · Princeton, NC

## Quick start

The examples run from a checkout; this repository does not currently include package-installation metadata.

```bash
git clone https://github.com/Immaculate1022/tesseract-medium.git
cd tesseract-medium
python -m pip install -r requirements.txt

# Render classical and Möbius-composed Mandelbrot slices.
python examples/mandelbrot_slice.py
```

The command writes PNG images to `examples/out/`. To explore the other components, run:

```bash
python examples/fibonacci_lattice_walk.py
python examples/orientation_demo.py
python examples/layered_medium_demo.py

# This demo imports the source package directly, so expose the checkout on the Python path.
PYTHONPATH=. python examples/tensor_layer_demo.py
```

## What is included

| Component | What it provides |
|---|---|
| `TesseractLattice` | A unit tesseract `[0, 1]^4` with optional φ/Fibonacci-ratio subdivision, hierarchical-index helper, 3D projection, and mirror/branch helpers. |
| `LayeredTesseractMedium` | Multiple lattices transformed by a configurable angular fan and seeded random offsets, plus per-layer and combined 3D projections. |
| `dynamics.py` | Escape-time arrays for Mandelbrot- and Julia-style iteration composed with a configurable Möbius transformation. |
| `OrientationTracker` | A discrete frame tracker that applies an orientation-reversing reflection when a walk crosses its designated twist seam. |
| `tensors.py` | NumPy helpers for SO(4)/SO(5) rotations, reflections, tensor/Kronecker products, φ-scaled embeddings, hierarchical vectors, and first-order transport steps. |
| `visualize.py` | Matplotlib helpers for saving escape-time and 3D point-projection PNGs. |

## Status and scope

The current source version is **0.3.0**. It is an **experimental, runnable substrate** for exploration rather than a complete geometric engine or a validated physical model. The repository contains source modules and demonstration scripts, including a tensor-layer self-check; it does not contain packaging metadata or an automated test suite.

Several details are intentionally lightweight and should be read as modeling choices, not general-purpose guarantees:

- The lattice is a discrete point set in a unit 4D hypercube, and the supplied visualizations are 2D escape-time images or 3D projections.
- `OrientationTracker` uses a designated seam and a simple reflection rule to demonstrate a Möbius-type orientation flip; its own documentation notes that this is not full differential geometry.
- `kaleidoscope_branch()` creates one φ-scaled collection of reflected copies that can be used as seeds for further recursion; recursive branching is not implemented as a built-in depth parameter.
- `parallel_transport_step()` is a first-order update and returns a frame that is only approximately orthonormal.
- Layer offsets are reproducible when a seed is supplied; use the parameters deliberately when comparing runs.

## Related projects

The repository identifies these related projects:

| Project | Relationship stated or linked by this repository |
|---|---|
| [research / `tesseract-medium-geometry.md`](https://github.com/Immaculate1022/research/blob/main/tesseract-medium-geometry.md) | Geometry specification referenced by this codebase. |
| [moebius-llama](https://github.com/Immaculate1022/moebius-llama) | Related PegaConstellation project. |
| [IOF-Resonance-Core](https://github.com/Immaculate1022/IOF-Resonance-Core) | Related PegaConstellation project. |
| [penteract-kaleidoscope](https://github.com/Immaculate1022/penteract-kaleidoscope) | Related PegaConstellation project. |
| [pegaconstellation-hub](https://github.com/Immaculate1022/pegaconstellation-hub) | Constellation hub linked by this repository. |

## License

This project is released under the **IOF Attribution License v1.0**. Public use, derivative work, or implementation must include the following attribution:

> PegaConstellation / Tesseract Medium by Gregory Scott Davis, Princeton, NC.

See [LICENSE](LICENSE) for the full terms and warranty disclaimer.

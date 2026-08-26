# Tesseract Medium

**4D non-orientable fractal geometry for hierarchical indexing, orientation-aware transport, and self-reflective systems.**

PegaConstellation · Gregory Scott Davis · Princeton, NC

---

## Why this exists

The [Tesseract Medium Geometry](https://github.com/Immaculate1022/research/blob/main/tesseract-medium-geometry.md) specification unifies:

- Möbius orientation twist
- Klein-bottle non-orientable topology
- Fibonacci / golden-ratio (φ) recursive scaling
- Mandelbrot-type fractal dynamics
- Residence in a tesseract (4-dimensional hypercube) vector medium
- **Infinite kaleidoscopic branching at vertices with mirror images**
- **Layered multi-sheet structure** (stacked like a fanned pack of paper at arbitrary angles with controlled variance so layers do not interfere)

This repository is the **runnable substrate**. It turns the abstract object into code that you (or any AI system) can execute, visualize, and build on.

### Concrete benefits

| Benefit | How this code delivers it |
|---------|---------------------------|
| Hierarchical / fractal indexing | φ-scaled subdivision of a 4D lattice (`lattice.py`) |
| Orientation-aware state transport | Parallel-transport monodromy tracker (`orientation.py`) |
| Immediate visual feedback | Möbius-twisted Mandelbrot / Julia slices (`dynamics.py` + examples) |
| Reusable geometric kernel | Clean modules other PegaConstellation projects can import |
| Infinite self-similar branching | `TesseractLattice.kaleidoscope_branch()` + `mirror_points()` |
| Multi-layer non-interfering medium | `LayeredTesseractMedium` — angled sheets with controlled variance |

---

## Geometric Vision (implemented v0.2)

### Infinite Kaleidoscopic Branching + Mirrors
At every vertex the structure can branch kaleidoscopically, spawning recursive mirror images of the local tesseract neighborhood. The `kaleidoscope_branch` and `mirror_points` helpers generate these sets; further recursive depth is straightforward to add.

### Layered Multi-Sheet Medium
The complete geometry is realized as a stack of slightly offset sheets — analogous to a fanned pack of translucent paper:

- Each sheet is a full `TesseractLattice`.
- Sheets are tilted across a configurable angular span.
- Small positional variance ensures no two sheets occupy identical coordinates.
- Result: dense volumetric presence without destructive interference. Orientation transport and hierarchical keys stay clean on every layer.

Use `LayeredTesseractMedium` and the layered projection helpers in `visualize.py`.

---

## Quick start

```bash
git clone https://github.com/Immaculate1022/tesseract-medium.git
cd tesseract-medium
pip install numpy matplotlib

# Run examples (writes PNG files into examples/out/)
python examples/mandelbrot_slice.py
python examples/fibonacci_lattice_walk.py
python examples/orientation_demo.py
python examples/layered_medium_demo.py   # new in v0.2
```

### Verified results

**v0.1**
- Orientation demo — loop crossing the twist seam reverses orientation (`sign = −1`); control loop away from the seam preserves orientation (`sign = +1`).
- Lattice — depth-2 φ/Fibonacci subdivision yields 625 points; hierarchical indices are stable and usable as storage keys.
- Dynamics — classical and Möbius-twisted Mandelbrot slices render successfully to PNG.

**v0.2**
- `LayeredTesseractMedium` constructs multi-sheet stacks with angular fan + variance.
- Kaleidoscopic / mirror helpers available on every lattice.
- New example `layered_medium_demo.py` writes both a layered projection and a kaleidoscope branch image.

---

## Package layout

```
tesseract_medium/
  __init__.py
  lattice.py          # Unit tesseract + φ / Fibonacci subdivision
                      # + LayeredTesseractMedium + kaleidoscope helpers
  dynamics.py         # Möbius-composed quadratic maps (Mandelbrot / Julia)
  orientation.py      # Simple monodromy / orientation-flip tracker
  visualize.py        # 2D/3D rendering helpers (incl. layered projections)
examples/
  mandelbrot_slice.py
  fibonacci_lattice_walk.py
  orientation_demo.py
  layered_medium_demo.py   # new
```

---

## Core ideas in code

**Lattice** — A discrete 4D hypercube whose edges and cells can be subdivided by successive Fibonacci ratios or pure powers of φ. Supports mirror reflection and kaleidoscopic branching operators.

**LayeredTesseractMedium** — A stack of lattices rotated through an angular span and given small random offsets so that layers never coincide. Provides `layer_points`, `all_points`, and 3D projection helpers.

**Dynamics** — Iteration of the form `z ↦ M(z² + c)` where `M` is a Möbius transformation. Classic Mandelbrot / Julia sets appear as 2D slices; the Möbius map injects controlled twist / inversion.

**Orientation** — Parallel transport of a discrete frame around closed loops in the lattice. After a full circuit the frame may return flipped — the concrete signature of the Möbius / Klein structure. Layer-wise transport is a natural next step.

---

## Relation to the constellation

| Project | Relationship |
|---------|--------------|
| [research / tesseract-medium-geometry.md](https://github.com/Immaculate1022/research/blob/main/tesseract-medium-geometry.md) | Formal specification this code implements (layered + kaleidoscopic extensions) |
| [moebius-llama](https://github.com/Immaculate1022/moebius-llama) | Self-reflective transformer architecture that uses Möbius + φ ideas; this geometry is a natural substrate |
| [IOF-Resonance-Core](https://github.com/Immaculate1022/IOF-Resonance-Core) | High-dimensional resonance / topological computing platform |
| [pegaconstellation-hub](https://github.com/Immaculate1022/pegaconstellation-hub) | Central map and status pulse |

---

## Status

- **v0.1** — Minimal working substrate: lattice, dynamics, orientation tracker, three examples.
- **v0.2** (2026-08-26) — `LayeredTesseractMedium`, kaleidoscopic / mirror helpers, layered visualization, new demo example. Version bumped to 0.2.0.
- Further mathematical formalization, deeper recursive branching, full SO(4) rotations, and performance-oriented ports remain open under the AI-first maintenance model.

---

## License

**IOF Attribution License v1.0**

Any public use, derivative work, or implementation must include clear attribution to:

> PegaConstellation / Tesseract Medium by Gregory Scott Davis, Princeton, NC.

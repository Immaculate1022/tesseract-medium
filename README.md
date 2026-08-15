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

This repository is the **runnable substrate**. It turns the abstract object into code that you (or any AI system) can execute, visualize, and build on.

### Concrete benefits

| Benefit | How this code delivers it |
|---------|---------------------------|
| Hierarchical / fractal indexing | φ-scaled subdivision of a 4D lattice (`lattice.py`) |
| Orientation-aware state transport | Parallel-transport monodromy tracker (`orientation.py`) |
| Immediate visual feedback | Möbius-twisted Mandelbrot / Julia slices (`dynamics.py` + examples) |
| Reusable geometric kernel | Clean modules other PegaConstellation projects can import |

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
```

---

## Package layout

```
tesseract_medium/
  __init__.py
  lattice.py          # Unit tesseract + φ / Fibonacci recursive subdivision
  dynamics.py         # Möbius-composed quadratic maps (Mandelbrot / Julia)
  orientation.py      # Simple monodromy / orientation-flip tracker
  visualize.py        # 2D rendering helpers
examples/
  mandelbrot_slice.py
  fibonacci_lattice_walk.py
  orientation_demo.py
```

---

## Core ideas in code

**Lattice** — A discrete 4D hypercube whose edges and cells can be subdivided by successive Fibonacci ratios or pure powers of φ. This is the spatial medium.

**Dynamics** — Iteration of the form `z ↦ M(z² + c)` where `M` is a Möbius transformation. Classic Mandelbrot / Julia sets appear as 2D slices; the Möbius map injects controlled twist / inversion.

**Orientation** — Parallel transport of a discrete frame around closed loops in the lattice. After a full circuit the frame may return flipped — the concrete signature of the Möbius / Klein structure.

---

## Relation to the constellation

| Project | Relationship |
|---------|--------------|
| [research / tesseract-medium-geometry.md](https://github.com/Immaculate1022/research/blob/main/tesseract-medium-geometry.md) | Formal specification this code implements |
| [moebius-llama](https://github.com/Immaculate1022/moebius-llama) | Self-reflective transformer architecture that uses Möbius + φ ideas; this geometry is a natural substrate |
| [IOF-Resonance-Core](https://github.com/Immaculate1022/IOF-Resonance-Core) | High-dimensional resonance / topological computing platform |

---

## Status

- **v0.1** — Minimal working substrate: lattice, dynamics, orientation tracker, three examples.
- Further mathematical formalization and performance-oriented ports are open under the AI-first maintenance model.

---

## License

**IOF Attribution License v1.0**

Any public use, derivative work, or implementation must include clear attribution to:

> PegaConstellation / Tesseract Medium by Gregory Scott Davis, Princeton, NC.

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
| Infinite self-similar branching | Target aesthetic & future extension: kaleidoscopic mirrors at every vertex |
| Multi-layer non-interfering medium | Target aesthetic & future extension: angled sheets with small variance |

---

## Geometric Vision (updated 2026-08-26)

### Infinite Kaleidoscopic Branching + Mirrors
At every vertex the structure branches kaleidoscopically, spawning recursive mirror images of the local tesseract neighborhood. Branches continue infinitely, producing a fractal web of hypercubes and their reflections that remains compatible with the global Möbius / Klein orientation rules.

### Layered Multi-Sheet Medium
The complete geometry is realized as a stack of slightly offset sheets — analogous to a fanned pack of translucent paper:

- Each sheet carries a full tesseract + mirror + kaleidoscopic structure.
- Sheets may be tilted at any chosen angles.
- Small positional / rotational / shear variance ensures no two sheets occupy identical coordinates.
- Result: dense volumetric presence without destructive interference. Orientation transport and hierarchical keys stay clean on every layer.

These ideas are now part of the formal specification and serve as the visual and structural targets for ongoing development of the lattice, dynamics, and visualization modules.

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

### Verified results (v0.1)

- **Orientation demo** — loop crossing the twist seam reverses orientation (`sign = −1`); control loop away from the seam preserves orientation (`sign = +1`).
- **Lattice** — depth-2 φ/Fibonacci subdivision yields 625 points; hierarchical indices are stable and usable as storage keys.
- **Dynamics** — classical and Möbius-twisted Mandelbrot slices render successfully to PNG.

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

**Lattice** — A discrete 4D hypercube whose edges and cells can be subdivided by successive Fibonacci ratios or pure powers of φ. This is the spatial medium. Future extensions will support kaleidoscopic branching operators and multi-sheet layering with angular/positional variance.

**Dynamics** — Iteration of the form `z ↦ M(z² + c)` where `M` is a Möbius transformation. Classic Mandelbrot / Julia sets appear as 2D slices; the Möbius map injects controlled twist / inversion.

**Orientation** — Parallel transport of a discrete frame around closed loops in the lattice. After a full circuit the frame may return flipped — the concrete signature of the Möbius / Klein structure. Layer-wise transport is a natural next step.

---

## Relation to the constellation

| Project | Relationship |
|---------|--------------|
| [research / tesseract-medium-geometry.md](https://github.com/Immaculate1022/research/blob/main/tesseract-medium-geometry.md) | Formal specification this code implements (now includes layered + kaleidoscopic extensions) |
| [moebius-llama](https://github.com/Immaculate1022/moebius-llama) | Self-reflective transformer architecture that uses Möbius + φ ideas; this geometry is a natural substrate |
| [IOF-Resonance-Core](https://github.com/Immaculate1022/IOF-Resonance-Core) | High-dimensional resonance / topological computing platform |
| [pegaconstellation-hub](https://github.com/Immaculate1022/pegaconstellation-hub) | Central map and status pulse |

---

## Status

- **v0.1** — Minimal working substrate: lattice, dynamics, orientation tracker, three examples. **Verified runnable.**
- Geometric vision extended (2026-08-26): infinite kaleidoscopic branching with mirrors + layered multi-sheet medium at arbitrary angles with non-interfering variance.
- Further mathematical formalization, visualization modes that realize the layered/kaleidoscopic aesthetic, and performance-oriented ports are open under the AI-first maintenance model.

---

## License

**IOF Attribution License v1.0**

Any public use, derivative work, or implementation must include clear attribution to:

> PegaConstellation / Tesseract Medium by Gregory Scott Davis, Princeton, NC.

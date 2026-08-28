#!/usr/bin/env python3
"""
Self-checking demonstration / smoke test of the tensor mathematics layer.

Run from the repository root:

    python examples/tensor_layer_demo.py

Exits with code 0 only if every mathematical invariant holds.
"""

import sys
import numpy as np

from tesseract_medium import (
    PHI,
    tesseract_rotation,
    penteract_rotation,
    rotate_points,
    rotate_lattice_points,
    reflection_tensor,
    mirror_operator,
    is_special_orthogonal,
    is_involution,
    phi_scaled_embedding,
    recursive_kronecker_nest,
    hierarchical_index_tensor,
    parallel_transport_step,
    orientation_sign,
    phi_harmonic_angles,
    tensor_product,
)


def check(name: str, condition: bool) -> None:
    status = "PASS" if condition else "FAIL"
    print(f"  [{status}] {name}")
    if not condition:
        raise AssertionError(name)


def main() -> int:
    print("=== Tesseract Medium — Tensor Layer Self-Check (v0.3) ===\n")

    try:
        # ------------------------------------------------------------------
        # 1. SO(4) / SO(5) rotations are special-orthogonal
        # ------------------------------------------------------------------
        print("1. Rotation tensors")
        t = 1.7
        R4 = tesseract_rotation(phi_harmonic_angles(t, dim=4))
        R5 = penteract_rotation(phi_harmonic_angles(t, dim=5))
        check("SO(4) is special-orthogonal", is_special_orthogonal(R4))
        check("SO(5) is special-orthogonal", is_special_orthogonal(R5))
        check("SO(4) det ≈ +1", abs(np.linalg.det(R4) - 1.0) < 1e-9)
        check("SO(5) det ≈ +1", abs(np.linalg.det(R5) - 1.0) < 1e-9)

        # ------------------------------------------------------------------
        # 2. Rotations preserve distances
        # ------------------------------------------------------------------
        print("\n2. Distance preservation")
        pts = np.array(
            [[1, 1, 1, 1], [-1, 1, -1, 1], [1, -1, 1, -1], [0.5, -0.5, 0.2, 0.8]],
            dtype=float,
        )
        rotated = rotate_points(pts, R4)
        d0 = np.linalg.norm(pts[0] - pts[1])
        d1 = np.linalg.norm(rotated[0] - rotated[1])
        check("Distances preserved under SO(4)", abs(d0 - d1) < 1e-9)

        # Bridge helper
        rotated2 = rotate_lattice_points(pts, phi_harmonic_angles(t, dim=4), dim=4)
        check("rotate_lattice_points matches rotate_points", np.allclose(rotated, rotated2))

        # ------------------------------------------------------------------
        # 3. Reflections are involutions with det = -1
        # ------------------------------------------------------------------
        print("\n3. Reflections / mirrors")
        M_axis = reflection_tensor(4, axis=2)
        M_gen = mirror_operator(4, [1.0, 0.3, -0.2, 0.5])
        check("Axis reflection is involution", is_involution(M_axis))
        check("General mirror is involution", is_involution(M_gen))
        check("Axis reflection det = -1", abs(np.linalg.det(M_axis) + 1.0) < 1e-9)
        check("General mirror det = -1", abs(np.linalg.det(M_gen) + 1.0) < 1e-9)

        # ------------------------------------------------------------------
        # 4. φ-scaling and Kronecker nesting
        # ------------------------------------------------------------------
        print("\n4. Hierarchical constructions")
        S = phi_scaled_embedding(4)
        check("φ-scale diagonal entries == 1/φ", np.allclose(np.diag(S), 1.0 / PHI))
        nest = recursive_kronecker_nest(np.eye(2), depth=2)
        check("Kronecker nest shape (depth=2) is (8,8)", nest.shape == (8, 8))

        key = hierarchical_index_tensor([3, 1, 4, 2], base_dim=4)
        check("Hierarchical index has length 4", key.shape == (4,))
        check("Hierarchical index is finite", np.all(np.isfinite(key)))

        # ------------------------------------------------------------------
        # 5. Parallel transport roughly preserves orientation for small steps
        # ------------------------------------------------------------------
        print("\n5. Parallel transport")
        frame = np.eye(4)
        connection = np.zeros((4, 4))
        connection[0, 1] = 0.25
        connection[1, 0] = -0.25
        delta = np.array([0.05, 0.0, 0.0, 0.0])
        new_frame = parallel_transport_step(frame, connection, delta)
        check("Transported frame orientation is +1", orientation_sign(new_frame) > 0)
        check(
            "Transported frame still nearly orthonormal",
            np.allclose(new_frame @ new_frame.T, np.eye(4), atol=1e-3),
        )

        # ------------------------------------------------------------------
        # 6. Outer product sanity
        # ------------------------------------------------------------------
        print("\n6. Tensor product")
        v = np.array([1.0, PHI])
        w = np.array([1.0, 1.0 / PHI])
        outer = tensor_product(v, w)
        check("Outer product shape (2,2)", outer.shape == (2, 2))
        check("Outer product [0,0] == 1", abs(outer[0, 0] - 1.0) < 1e-12)

        print("\n✓ All tensor-layer invariants hold.")
        return 0

    except AssertionError as e:
        print(f"\n✗ Failed: {e}")
        return 1
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())

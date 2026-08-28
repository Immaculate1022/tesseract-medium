#!/usr/bin/env python3
"""
Quick demonstration of the new tensor mathematics layer.

Run from the repository root:

    python examples/tensor_layer_demo.py
"""

import numpy as np
from tesseract_medium import (
    PHI,
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
)


def main():
    print("=== Tesseract Medium — Tensor Layer Demo (v0.3) ===\n")

    # 1. SO(4) and SO(5) rotations driven by φ-harmonic angles
    t = 1.7
    angles4 = phi_harmonic_angles(t, dim=4)
    angles5 = phi_harmonic_angles(t, dim=5)
    R4 = tesseract_rotation(angles4)
    R5 = penteract_rotation(angles5)
    print(f"SO(4) det = {np.linalg.det(R4):.6f}  (should be ≈ +1)")
    print(f"SO(5) det = {np.linalg.det(R5):.6f}  (should be ≈ +1)")

    # 2. Rotate a simple set of points
    pts = np.array([[1, 1, 1, 1], [-1, 1, -1, 1], [1, -1, 1, -1]], dtype=float)
    rotated = rotate_points(pts, R4)
    print(f"\nRotated 3 points in 4D (first row): {rotated[0].round(4)}")

    # 3. Reflection / mirror involution
    M = reflection_tensor(4, axis=2)
    print(f"Reflection R@R == I ? {np.allclose(M @ M, np.eye(4))}")

    # 4. φ-scaled embedding and recursive Kronecker nesting
    S = phi_scaled_embedding(4)
    print(f"φ-scale diagonal: {np.diag(S).round(4)}")
    nest = recursive_kronecker_nest(np.eye(2), depth=2)
    print(f"Kronecker nest shape (depth=2): {nest.shape}")

    # 5. Hierarchical index → vector
    key = hierarchical_index_tensor([3, 1, 4, 2], base_dim=4)
    print(f"Hierarchical key [3,1,4,2] → {key.round(4)}")

    # 6. Parallel transport of a frame
    frame = np.eye(4)
    connection = np.zeros((4, 4))
    connection[0, 1] = 0.3   # simple connection component
    connection[1, 0] = -0.3
    delta = np.array([0.1, 0.0, 0.0, 0.0])
    new_frame = parallel_transport_step(frame, connection, delta)
    print(f"Orientation after transport: {orientation_sign(new_frame):+.0f}")

    # 7. Outer / tensor product example
    v = np.array([1.0, PHI])
    w = np.array([1.0, 1.0 / PHI])
    outer = tensor_product(v, w)
    print(f"\nOuter product shape: {outer.shape}")
    print("Demo finished successfully.")


if __name__ == "__main__":
    main()

import math
import unittest

import numpy as np

from project1_bloch_sphere import (
    H,
    X,
    Z,
    apply_gate,
    apply_sequence,
    bloch_vector,
    normalize,
    parse_sequence,
    relative_phase,
    repeated_z_rotation,
    rotation_closed_form,
    rotation_matrix_exponential,
    state_from_angles,
)


class BlochSphereTests(unittest.TestCase):
    def test_angles_produce_unit_bloch_vector(self):
        state = state_from_angles(0.73 * math.pi, 0.31 * math.pi)
        self.assertTrue(np.allclose(np.linalg.norm(state), 1.0))
        self.assertTrue(np.allclose(np.linalg.norm(bloch_vector(state)), 1.0))

    def test_hadamard_maps_zero_to_plus(self):
        zero = np.array([1, 0], dtype=complex)
        plus = apply_gate(H, zero)
        self.assertTrue(np.allclose(bloch_vector(plus), [1, 0, 0]))

    def test_pauli_x_flips_z_axis(self):
        zero = np.array([1, 0], dtype=complex)
        self.assertTrue(np.allclose(bloch_vector(apply_gate(X, zero)), [0, 0, -1]))

    def test_z_rotation_closed_form_matches_exponential(self):
        for axis in ("x", "y", "z"):
            left = rotation_closed_form(axis, math.pi / 3)
            right = rotation_matrix_exponential(axis, math.pi / 3)
            self.assertTrue(np.allclose(left, right, atol=1e-12))

    def test_eight_rotations_return_bloch_point_and_add_global_minus_sign(self):
        plus = state_from_angles(math.pi / 2, 0.0)
        states, vectors = repeated_z_rotation(plus)
        self.assertTrue(np.allclose(vectors[0], vectors[-1], atol=1e-12))
        self.assertTrue(np.allclose(relative_phase(plus, states[-1]), -1.0 + 0j, atol=1e-12))

    def test_custom_sequence_and_input_validation(self):
        state = state_from_angles(0.73 * math.pi, 0.31 * math.pi)
        result = apply_sequence(state, parse_sequence("H, T, X, S, H"))
        self.assertTrue(np.allclose(np.linalg.norm(result), 1.0))
        with self.assertRaises(ValueError):
            parse_sequence("H, NOT_A_GATE")

    def test_normalize_rejects_zero_vector(self):
        with self.assertRaises(ValueError):
            normalize(np.zeros(2, dtype=complex))


if __name__ == "__main__":
    unittest.main()

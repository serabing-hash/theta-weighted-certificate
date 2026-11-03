#!/usr/bin/env python3
"""Small positive/negative tests for the public exact-matrix helper contract."""
from fractions import Fraction as F
import unittest
from replay_saved_gates import exact_linear_combination, congruence_sign


class ExactHelperTests(unittest.TestCase):
    def test_rational_matrix_assembly(self):
        a = [[2, -1], [-1, 3]]
        b = [[1, 4], [4, -2]]
        rows, den = exact_linear_combination([(F(3, 7), a, 5), (F(-2, 3), b, 11)], F(1, 13))
        for i in range(2):
            for j in range(2):
                expected = F(3, 7) * F(a[i][j], 5) - F(2, 3) * F(b[i][j], 11)
                if i == j: expected += F(1, 13)
                self.assertEqual(F(rows[i][j], den), expected)

    def test_positive_congruence(self):
        result = congruence_sign([[3, -1], [-1, 3]], 2, [[1, 0], [0, 1]], F(1, 4))
        self.assertEqual(result['positive_integer_congruence_margins'], 2)

    def test_negative_matrix_rejected(self):
        with self.assertRaises(AssertionError):
            congruence_sign([[1, 2], [2, 1]], 1, [[1, 0], [0, 1]])

    def test_singular_witness_rejected(self):
        with self.assertRaises(AssertionError):
            congruence_sign([[2, 0], [0, 2]], 1, [[1, 1], [1, 1]])

    def test_zero_margin_rejected(self):
        with self.assertRaises(AssertionError):
            congruence_sign([[1, 0], [0, 1]], 1, [[1, 0], [0, 1]], F(1))


if __name__ == '__main__':
    if not __debug__: raise SystemExit('Run without Python -O.')
    unittest.main()

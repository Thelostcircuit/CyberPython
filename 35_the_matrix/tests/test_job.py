import unittest

import numpy as np
from numpy.testing import assert_allclose, assert_array_equal

import job


class Matrix(unittest.TestCase):
    def test_to_array(self):
        a = job.to_array([[1, 2], [3, 4]])
        self.assertEqual((a.shape, a.dtype), ((2, 2), np.float64))

    def test_standardise(self):
        a = np.array([[1.0, 10.0], [3.0, 10.5], [5.0, 12.5]])
        z = job.standardise(a)
        assert_allclose(z.mean(axis=0), [0, 0], atol=1e-12)
        assert_allclose(z.std(axis=0), [1, 1])
        assert_allclose(z[:, 0], [-1.224744871, 0, 1.224744871])

    def test_hot_racks(self):
        assert_array_equal(job.hot_racks(np.array([30, 71, 45, 90, 70]), 70), [1, 3])
        self.assertEqual(len(job.hot_racks(np.array([1.0]), 5)), 0)

    def test_rolling_mean(self):
        assert_allclose(job.rolling_mean(np.array([1.0, 2, 3, 4, 5]), 2), [1.5, 2.5, 3.5, 4.5])
        assert_allclose(job.rolling_mean(np.arange(10.0), 5), [2, 3, 4, 5, 6, 7])

    def test_distance_matrix(self):
        pts = np.array([[0.0, 0], [3, 4], [6, 8]])
        assert_allclose(job.distance_matrix(pts), [[0, 5, 10], [5, 0, 5], [10, 5, 0]])
        big = np.random.default_rng(0).random((50, 3))
        d = job.distance_matrix(big)
        self.assertEqual(d.shape, (50, 50))
        assert_allclose(d, d.T)

    def test_solve(self):
        A = np.array([[3.0, 1], [1, 2]])
        b = np.array([9.0, 8])
        assert_allclose(job.solve_loads(A, b), [2, 3])

    def test_clip_count(self):
        clipped, n = job.clip_count(np.array([-5, 0, 5, 10, 15]), 0, 10)
        assert_array_equal(clipped, [0, 0, 5, 10, 10])
        self.assertEqual(n, 2)
        self.assertIsInstance(n, int)

    def test_noise(self):
        a = job.noise(7, 1000)
        assert_array_equal(a, job.noise(7, 1000))
        self.assertFalse(np.array_equal(a, job.noise(8, 1000)))
        assert_array_equal(a[:5], np.random.default_rng(7).standard_normal(5))
        self.assertLess(abs(a.mean()), 0.15)

    def test_wing_means(self):
        values = np.array([10.0, 20, 30, 40, 50])
        wings = np.array(["C", "A", "C", "A", "B"])
        self.assertEqual(job.wing_means(values, wings), {"A": 30.0, "B": 50.0, "C": 20.0})

    def test_dominant_frequency(self):
        rate = 1000
        t = np.arange(0, 1, 1 / rate)
        sig = 3 + np.sin(2 * np.pi * 50 * t) + 0.3 * np.sin(2 * np.pi * 120 * t)
        self.assertEqual(job.dominant_frequency(sig, rate), 50.0)


if __name__ == "__main__":
    unittest.main()

import cmath
import random
import unittest
from decimal import Decimal
from fractions import Fraction

import job


class Money(unittest.TestCase):
    def test_split_pot(self):
        self.assertEqual(job.split_pot(Decimal("100.00"), 3),
                         [Decimal("33.34"), Decimal("33.33"), Decimal("33.33")])
        shares = job.split_pot(Decimal("0.05"), 3)
        self.assertEqual(shares, [Decimal("0.02"), Decimal("0.02"), Decimal("0.01")])
        self.assertEqual(sum(job.split_pot(Decimal("12000.01"), 7)), Decimal("12000.01"))

    def test_compound(self):
        self.assertEqual(job.compound(Decimal("1000"), Decimal("0.05"), 2), Decimal("1102.50"))
        self.assertEqual(job.compound(Decimal("100"), Decimal("0.035"), 3), Decimal("110.87"))
        self.assertEqual(job.compound(Decimal("5"), Decimal("0"), 10), Decimal("5.00"))


class Odds(unittest.TestCase):
    def test_odds(self):
        self.assertEqual(job.odds_of_total(7), Fraction(1, 6))
        self.assertEqual(job.odds_of_total(2), Fraction(1, 36))
        self.assertEqual(job.odds_of_total(13), 0)
        self.assertEqual(job.odds_of_total(3, dice=3), Fraction(1, 216))
        self.assertEqual(job.odds_of_total(2, dice=1, sides=4), Fraction(1, 4))

    def test_report(self):
        r = job.roll_report([1, 2, 2, 3, 3, 6])
        self.assertEqual(r["mean"], 17 / 6)
        self.assertEqual(r["median"], 2.5)
        self.assertEqual(r["modes"], [2, 3])
        self.assertEqual(r["stdev"], 1.722)

    def test_z_score(self):
        self.assertEqual(job.z_score(10, [2, 4, 4, 4, 5, 5, 7, 9]), 2.34)

    def test_rigged(self):
        fair = [1, 2, 3, 4, 5, 6] * 10
        self.assertFalse(job.rigged(fair, 6, 0.01))
        loaded = fair + [6] * 20
        self.assertTrue(job.rigged(loaded, 6, 0.05))


class Random(unittest.TestCase):
    def test_simulate(self):
        state = random.getstate()
        a = job.simulate(7, 50)
        self.assertEqual(random.getstate(), state)
        self.assertEqual(a, job.simulate(7, 50))
        self.assertNotEqual(a, job.simulate(8, 50))
        self.assertTrue(all(2 <= x <= 12 for x in a))
        rng = random.Random(7)
        self.assertEqual(a[0], rng.randint(1, 6) + rng.randint(1, 6))

    def test_shuffled(self):
        deck = list(range(20))
        s = job.shuffled(deck, 1)
        self.assertEqual(deck, list(range(20)))
        self.assertEqual(sorted(s), deck)
        self.assertEqual(s, job.shuffled(deck, 1))
        self.assertNotEqual(s, deck)


class MathBits(unittest.TestCase):
    def test_math(self):
        self.assertEqual(job.hand_count(52, 5), 2598960)
        self.assertEqual(job.dist((0, 0), (3, 4)), 5.0)
        self.assertEqual(job.dist((1, 1, 1), (1, 1, 1)), 0.0)

    def test_roots(self):
        self.assertEqual(job.quadratic_roots(1, -3, 2), (2, 1))
        r1, r2 = job.quadratic_roots(1, 0, 1)
        self.assertTrue(cmath.isclose(r1, 1j) and cmath.isclose(r2, -1j))

    def test_kind(self):
        self.assertEqual(job.kind(3), "integral")
        self.assertEqual(job.kind(Fraction(1, 3)), "rational")
        self.assertEqual(job.kind(0.5), "real")
        self.assertEqual(job.kind(2j), "complex")
        self.assertEqual(job.kind("5"), "not a number")
        self.assertEqual(job.kind(True), "not a number")


if __name__ == "__main__":
    unittest.main()

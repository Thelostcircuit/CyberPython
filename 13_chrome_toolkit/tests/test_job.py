import unittest

import job


class Iter(unittest.TestCase):
    def test_combinatorics(self):
        self.assertEqual(job.guard_pairs(["a", "b", "c"]), [("a", "b"), ("a", "c"), ("b", "c")])
        self.assertEqual(len(job.routes(["a", "b", "c", "d"])), 24)
        self.assertEqual(job.routes(["x", "y"]), [("x", "y"), ("y", "x")])
        self.assertEqual(job.codes("01", 2), ["00", "01", "10", "11"])
        self.assertEqual(len(job.codes("0123456789", 4)), 10000)

    def test_streams(self):
        self.assertEqual(job.running_totals([1, 2, 3, 4]), [1, 3, 6, 10])
        self.assertEqual(job.rle("aaabcc"), [("a", 3), ("b", 1), ("c", 2)])
        self.assertEqual(job.rle(""), [])
        self.assertEqual(job.card_batches(range(5), 2), [(0, 1), (2, 3), (4,)])
        self.assertEqual(job.deltas([1, 4, 9, 16]), [3, 5, 7])
        self.assertEqual(job.until_alarm(iter(["a", "b", "ALARM", "c"])), ["a", "b"])

    def test_assign_shifts(self):
        self.assertEqual(job.assign_shifts(["t1", "t2", "t3", "t4", "t5"], ["dex", "sable"]),
                         {"dex": ["t1", "t3", "t5"], "sable": ["t2", "t4"]})
        self.assertEqual(job.assign_shifts([], ["dex"]), {"dex": []})


class Func(unittest.TestCase):
    def test_cache(self):
        self.assertEqual(job.ways_to_climb(0), 1)
        self.assertEqual(job.ways_to_climb(5), 8)
        self.assertEqual(job.ways_to_climb(10), 89)
        self.assertGreater(job.ways_to_climb(300), 10 ** 60)

    def test_reduce_partial(self):
        self.assertEqual(job.product_of([1, 2, 3, 4]), 24)
        self.assertEqual(job.product_of([]), 1)
        self.assertEqual(job.hex_reader("ff"), 255)
        self.assertEqual(job.hex_reader("0x10"), 16)

    def test_singledispatch(self):
        self.assertEqual(job.describe(7), "int:7")
        self.assertEqual(job.describe("abc"), "str:3")
        self.assertEqual(job.describe([1, 2]), "list of 2")
        self.assertEqual(job.describe(1.5), "unknown")

    def test_total_ordering(self):
        a, b = job.Clearance(1), job.Clearance(3)
        self.assertTrue(a < b and b > a and a <= a and b >= a)
        self.assertEqual(a, job.Clearance(1))
        self.assertEqual(max([b, a]).level, 3)

    def test_cached_property(self):
        d = job.Dossier("voss", ["x", "y"])
        self.assertEqual(d.summary, "voss: 2 entries")
        self.assertEqual(d.summary, "voss: 2 entries")
        self.assertEqual(d.computations, 1)

    def test_sort_roster(self):
        rows = [{"rank": 2, "name": "dex"}, {"rank": 1, "name": "sable"},
                {"rank": 2, "name": "adder"}]
        self.assertEqual([r["name"] for r in job.sort_roster(rows)], ["sable", "adder", "dex"])


if __name__ == "__main__":
    unittest.main()

import gc
import unittest

import job


class Crate:
    pass


class NightMarket(unittest.TestCase):
    def test_counter_defaultdict(self):
        self.assertEqual(job.best_sellers(["n", "c", "n", "u", "n", "c"], 2), [("n", 3), ("c", 2)])
        self.assertEqual(job.by_stall([("s9", "noodles"), ("s2", "chips"), ("s9", "tea")]),
                         {"s9": ["noodles", "tea"], "s2": ["chips"]})
        self.assertIs(type(job.by_stall([])), dict)

    def test_item(self):
        i = job.Item("chip", 40)
        self.assertEqual(i, ("chip", 40, 1))
        self.assertEqual(i.price, 40)
        self.assertEqual(i._replace(qty=3).qty, 3)
        self.assertIsInstance(i, tuple)

    def test_last_n(self):
        self.assertEqual(job.last_n(range(10), 3), [7, 8, 9])
        self.assertEqual(job.last_n([1], 3), [1])

    def test_lru(self):
        c = job.LRU(2)
        c.put("a", 1)
        c.put("b", 2)
        self.assertEqual(c.get("a"), 1)
        c.put("c", 3)                      # evicts b
        self.assertNotIn("b", c)
        self.assertEqual(c.keys(), ["a", "c"])
        self.assertIn("a", c)
        self.assertEqual(c.keys(), ["a", "c"])  # membership isn't a use
        c.put("a", 10)
        self.assertEqual(c.keys(), ["c", "a"])
        self.assertEqual(c.get("zz", "none"), "none")
        self.assertEqual(len(c), 2)

    def test_settings(self):
        self.assertEqual(job.resolve_settings({"port": 1, "host": "h", "x": 0},
                                              {"port": 2, "host": "e"}, {"port": 3}),
                         {"port": 3, "host": "e", "x": 0})

    def test_container_kind(self):
        self.assertEqual(job.container_kind({}), "mapping")
        self.assertEqual(job.container_kind("ab"), "sequence")
        self.assertEqual(job.container_kind((1,)), "sequence")
        self.assertEqual(job.container_kind(frozenset()), "set")
        self.assertEqual(job.container_kind(iter([])), "iterable")
        self.assertEqual(job.container_kind(5), "other")

    def test_heapq(self):
        offers = [job.Item("a", 50), job.Item("b", 5), job.Item("c", 20), job.Item("d", 7)]
        self.assertEqual([o.name for o in job.cheapest(offers, 2)], ["b", "d"])
        self.assertEqual(list(job.merge_feeds([1, 4, 9], [2, 3], [0, 10])), [0, 1, 2, 3, 4, 9, 10])

    def test_price_band(self):
        self.assertEqual([job.price_band(p) for p in (0, 9.99, 10, 99, 100, 999.5, 1000, 1e6)],
                         ["scrap", "scrap", "street", "street", "pro", "pro", "corp", "corp"])

    def test_array(self):
        data = job.pack([1, -2, 300])
        self.assertIsInstance(data, bytes)
        self.assertEqual(len(data), 6)
        self.assertEqual(job.unpack(data), [1, -2, 300])

    def test_job_order(self):
        order = job.job_order({"heist": {"recon", "gear"}, "gear": {"cash"}, "recon": set()})
        self.assertEqual(set(order), {"heist", "recon", "gear", "cash"})
        self.assertLess(order.index("cash"), order.index("gear"))
        self.assertEqual(order[-1], "heist")
        self.assertIsNone(job.job_order({"a": {"b"}, "b": {"a"}}))

    def test_access(self):
        A = job.Access
        self.assertTrue(job.can(A.ALL, A.READ | A.EXEC))
        self.assertTrue(job.can(A.READ | A.WRITE, A.WRITE))
        self.assertFalse(job.can(A.READ, A.READ | A.WRITE))
        self.assertEqual(A.ALL, A.READ | A.WRITE | A.EXEC)

    def test_clone(self):
        orig = {"arms": ["blade"], "meta": {"tags": ["x"]}}
        c = job.clone_loadout(orig)
        c["arms"].append("gun")
        c["meta"]["tags"].clear()
        self.assertEqual(orig, {"arms": ["blade"], "meta": {"tags": ["x"]}})

    def test_registry(self):
        r = job.Registry()
        a, b = Crate(), Crate()
        r.register("a", a)
        r.register("b", b)
        self.assertIs(r.get("a"), a)
        del b
        gc.collect()
        self.assertEqual(r.names(), ["a"])
        self.assertIsNone(r.get("b"))

    def test_frozen_view(self):
        d = {"x": 1}
        v = job.frozen_view(d)
        with self.assertRaises(TypeError):
            v["x"] = 2
        d["y"] = 2
        self.assertEqual(v["y"], 2)


if __name__ == "__main__":
    unittest.main()

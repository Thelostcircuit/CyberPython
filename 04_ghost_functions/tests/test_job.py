import unittest

from job import (build_request, depth, log_calls, make_counter, make_payload, pipeline, retry,
                 tag_target, total_loot)


class GhostFunctions(unittest.TestCase):
    def test_total_loot(self):
        self.assertEqual(total_loot(100, 50, cut=0.1), 135.0)
        self.assertEqual(total_loot(), 0)
        self.assertEqual(total_loot(10.25, 1), 11.25)
        self.assertEqual(total_loot(3, 3, 3, cut=1 / 3), 6.0)

    def test_make_payload(self):
        self.assertEqual(make_payload("locker-7"),
                         {"target": "locker-7", "retries": 3, "stealth": False})
        self.assertEqual(make_payload("x", stealth=True, retries=1),
                         {"target": "x", "retries": 1, "stealth": True})
        with self.assertRaises(TypeError):
            make_payload("x", 5)

    def test_build_request(self):
        self.assertEqual(build_request("get", port=9, host="x"), "GET host=x;port=9")
        self.assertEqual(build_request("post"), "POST")
        self.assertEqual(build_request("put", method="spoof"), "PUT method=spoof")
        with self.assertRaises(TypeError):
            build_request(method="GET")

    def test_tag_target(self):
        mine = ["hot"]
        self.assertEqual(tag_target("a", mine), ["hot", "a"])
        self.assertEqual(mine, ["hot"])
        self.assertEqual(tag_target("a"), ["a"])
        self.assertEqual(tag_target("b"), ["b"])

    def test_make_counter(self):
        c1, c2 = make_counter(10), make_counter()
        self.assertEqual([c1(), c1(), c1()], [11, 12, 13])
        self.assertEqual(c2(), 1)
        self.assertEqual(c1(), 14)

    def test_pipeline(self):
        p = pipeline(str.strip, str.upper, lambda s: s + "!")
        self.assertEqual(p("  go "), "GO!")
        self.assertEqual(pipeline()(42), 42)
        self.assertEqual(pipeline(lambda x: x * 2, lambda x: x + 1)(5), 11)

    def test_log_calls(self):
        @log_calls
        def add(a, b=0):
            """adds"""
            return a + b

        self.assertEqual(add(1, b=2), 3)
        self.assertEqual(add(5), 5)
        self.assertEqual(add.calls, [((1,), {"b": 2}), ((5,), {})])
        self.assertEqual(add.__name__, "add")
        self.assertEqual(add.__doc__, "adds")

        @log_calls
        def other():
            return 1
        other()
        self.assertEqual(len(add.calls), 2)

    def test_retry(self):
        attempts = []

        @retry(3)
        def flaky():
            attempts.append(1)
            if len(attempts) < 3:
                raise ConnectionError("blip")
            return "in"

        self.assertEqual(flaky(), "in")
        self.assertEqual(len(attempts), 3)
        self.assertEqual(flaky.__name__, "flaky")

        count = []

        @retry(2)
        def doomed(tag):
            count.append(tag)
            raise ValueError(f"fail {len(count)}")

        with self.assertRaisesRegex(ValueError, "fail 2"):
            doomed("t")
        self.assertEqual(count, ["t", "t"])

    def test_depth(self):
        self.assertEqual(depth(5), 0)
        self.assertEqual(depth([]), 1)
        self.assertEqual(depth([1, 2]), 1)
        self.assertEqual(depth([1, [2]]), 2)
        self.assertEqual(depth([[[]]]), 3)
        self.assertEqual(depth([1, [2, [3, [4]]], [5]]), 4)


if __name__ == "__main__":
    unittest.main()

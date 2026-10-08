import math
import threading
import time
import unittest

import job


class Threads(unittest.TestCase):
    def test_hammer(self):
        self.assertEqual(job.hammer(job.SafeCounter(), 8, 5000), 40000)

    def test_fan_out(self):
        funcs = [lambda i=i: (time.sleep(0.05 * (3 - i)), i)[1] for i in range(3)]
        start = time.perf_counter()
        self.assertEqual(job.fan_out(funcs), [0, 1, 2])
        self.assertLess(time.perf_counter() - start, 0.25)
        self.assertEqual(job.fan_out([]), [])

    def test_fastest(self):
        def slow():
            time.sleep(1.0)
            return "slow"

        def quick():
            time.sleep(0.05)
            return "quick"
        start = time.perf_counter()
        self.assertEqual(job.fastest([slow, quick]), "quick")
        self.assertLess(time.perf_counter() - start, 0.6)

    def test_pipeline(self):
        self.assertEqual(job.pipeline(list(range(100)), 4), [x * 2 for x in range(100)])
        self.assertEqual(job.pipeline([], 3), [])

    def test_delayed_signal(self):
        ev = job.delayed_signal(0.1)
        self.assertIsInstance(ev, threading.Event)
        self.assertFalse(ev.is_set())
        self.assertTrue(ev.wait(2))


class Processes(unittest.TestCase):
    def test_count_primes(self):
        self.assertEqual(job.count_primes(list(range(1000))), 168)

    def test_shm(self):
        self.assertEqual(job.shm_roundtrip(b"release order #22"), b"release order #22")

    def test_subinterpreter(self):
        self.assertEqual(job.in_subinterpreter(math.factorial, 10), 3628800)
        self.assertEqual(job.in_subinterpreter(pow, 2, 10), 1024)


class Context(unittest.TestCase):
    def test_with_run_id(self):
        self.assertEqual(job.with_run_id("gap-22", lambda: job.RUN_ID.get()), "gap-22")
        self.assertEqual(job.RUN_ID.get(), "none")

    def test_run_schedule(self):
        events = [(0.06, 1, "loop cameras"), (0.02, 1, "call lift"), (0.06, 0, "unlock crawl"),
                  (0.0, 5, "stage payload")]
        self.assertEqual(job.run_schedule(events),
                         ["stage payload", "call lift", "unlock crawl", "loop cameras"])


if __name__ == "__main__":
    unittest.main()

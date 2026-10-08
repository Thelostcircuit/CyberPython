import doctest
import time
import unittest

import job


def run_suite(func):
    cls = type("Probe", (job.ChecksumTests,), {"func": staticmethod(func)})
    suite = unittest.TestLoader().loadTestsFromTestCase(cls)
    result = unittest.TestResult()
    suite.run(result)
    return suite.countTestCases(), result


def mutant_no_weights(text):
    return sum(ord(c) for c in text) % 997


def mutant_zero_based(text):
    return sum(i * ord(c) for i, c in enumerate(text)) % 997


def mutant_no_modulo(text):
    return sum(i * ord(c) for i, c in enumerate(text, start=1))


class YourTests(unittest.TestCase):
    def test_passes_on_real_checksum(self):
        count, result = run_suite(job.checksum)
        self.assertGreater(count, 0, "write at least one test_ method")
        self.assertTrue(result.wasSuccessful(), result.failures + result.errors)

    def test_kills_mutants(self):
        for mutant in (mutant_no_weights, mutant_zero_based, mutant_no_modulo):
            with self.subTest(mutant=mutant.__name__):
                _, result = run_suite(mutant)
                self.assertFalse(result.wasSuccessful(),
                                 f"your tests didn't notice {mutant.__name__}")


class Mocks(unittest.TestCase):
    def test_frozen_stamp(self):
        self.assertEqual(job.frozen_stamp(4102444800.4), "4102444800")
        self.assertNotEqual(job.stamp(), "4102444800")

    def test_fake_door(self):
        door = job.fake_door()
        self.assertEqual(door.status, "sealed")
        self.assertIs(door.open(), True)
        with self.assertRaisesRegex(PermissionError, "locked out"):
            door.open()
        self.assertEqual(door.open.call_count, 2)

    def test_spy_on(self):
        class Lift:
            def go(self, floor):
                return f"moving to {floor}"
        lift = Lift()
        self.assertEqual(job.spy_on(lift, "go", -6), ("moving to -6", 2))
        self.assertEqual(lift.go(1), "moving to 1")
        self.assertNotIn("go", vars(lift))


class Doctests(unittest.TestCase):
    def test_rack_number_doctests(self):
        tests = doctest.DocTestFinder().find(job.rack_number, "rack_number", globs={"rack_number": job.rack_number})
        examples = sum(len(t.examples) for t in tests)
        self.assertGreaterEqual(examples, 3, "write at least three >>> examples")
        runner = doctest.DocTestRunner(verbose=False)
        for t in tests:
            runner.run(t, out=lambda s: None)
        self.assertEqual(runner.failures, 0)
        doc = job.rack_number.__doc__
        self.assertIn("ValueError", doc)

    def test_rack_number(self):
        self.assertEqual(job.rack_number("C-17"), 17)
        with self.assertRaises(ValueError):
            job.rack_number("C17")


def slow_part():
    total = 0
    for i in range(300_000):
        total += i * i
    return total


def fast_part():
    return sum(range(100))


def workload():
    fast_part()
    return slow_part()


def branchy(x=3):
    y = x * 2
    if y > 100:
        y = 0
    return y


class Measure(unittest.TestCase):
    def test_best_time(self):
        t = job.best_time(lambda: time.sleep(0.01), 2)
        self.assertGreaterEqual(t, 0.018)
        self.assertLess(t, 1)

    def test_hottest(self):
        self.assertEqual(job.hottest(workload), "slow_part")

    def test_lines_run(self):
        first = branchy.__code__.co_firstlineno
        self.assertEqual(job.lines_run(branchy), [first + 1, first + 2, first + 4])

    def test_peak_bytes(self):
        self.assertGreaterEqual(job.peak_bytes(lambda: bytearray(2_000_000)), 2_000_000)
        self.assertLess(job.peak_bytes(lambda: None), 100_000)

    def test_line_recorder(self):
        rec = job.LineRecorder("branchy")
        self.assertEqual(rec.runcall(branchy, 60), 0)
        first = branchy.__code__.co_firstlineno
        self.assertEqual(rec.lines, [first + 1, first + 2, first + 3, first + 4])


if __name__ == "__main__":
    unittest.main()

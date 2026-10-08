import inspect
import itertools
import unittest

import job
from job import Countdown, Tap, chunked, flatten, frames, interleave, running_max, take, windows


def naturals():
    n = 0
    while True:
        yield n
        n += 1


class Streams(unittest.TestCase):
    def test_countdown(self):
        self.assertEqual(list(Countdown(3)), [3, 2, 1])
        self.assertEqual(list(Countdown(0)), [])
        c = Countdown(2)
        self.assertIs(iter(c), c)
        self.assertEqual(next(c), 2)
        self.assertEqual(next(c), 1)
        with self.assertRaises(StopIteration):
            next(c)
        self.assertFalse(inspect.isgeneratorfunction(Countdown.__next__))

    def test_frames(self):
        src = ["  alpha \n", "\n", "# comment\n", "   # also\n", "beta"]
        self.assertEqual(list(frames(src)), ["alpha", "beta"])
        self.assertTrue(inspect.isgeneratorfunction(job.frames))
        consumed = []

        def source():
            for l in ["a", "b", "c"]:
                consumed.append(l)
                yield l
        g = frames(source())
        self.assertEqual(next(g), "a")
        self.assertEqual(consumed, ["a"])

    def test_chunked(self):
        self.assertEqual(list(chunked(range(7), 3)), [[0, 1, 2], [3, 4, 5], [6]])
        self.assertEqual(list(chunked([], 3)), [])
        self.assertEqual(next(chunked(naturals(), 2)), [0, 1])

    def test_flatten(self):
        self.assertEqual(list(flatten([1, [2, (3, [4])], "ab"])), [1, 2, 3, 4, "ab"])
        self.assertEqual(list(flatten([[], [[]]])), [])
        self.assertIn("yield from", inspect.getsource(job.flatten))

    def test_take(self):
        self.assertEqual(take(3, naturals()), [0, 1, 2])
        self.assertEqual(take(5, "ab"), ["a", "b"])
        self.assertEqual(take(0, naturals()), [])
        it = iter(range(10))
        take(2, it)
        self.assertEqual(next(it), 2)

    def test_windows(self):
        self.assertEqual(list(windows([1, 2, 3, 4], 3)), [(1, 2, 3), (2, 3, 4)])
        self.assertEqual(list(windows([1, 2], 3)), [])
        self.assertEqual(list(windows("abc", 1)), [("a",), ("b",), ("c",)])
        self.assertEqual(list(itertools.islice(windows(naturals(), 2), 2)), [(0, 1), (1, 2)])

    def test_interleave(self):
        self.assertEqual("".join(map(str, interleave("abc", [1, 2], "XYZW"))), "a1Xb2YcZW")
        self.assertEqual(list(interleave()), [])
        self.assertEqual(take(4, interleave(naturals(), "ab")), [0, "a", 1, "b"])

    def test_tap(self):
        t = Tap([1, 2, 3])
        self.assertEqual(list(t), [1, 2, 3])
        self.assertEqual(list(t), [1, 2, 3])
        self.assertEqual([(a, b) for a in t for b in t][:2], [(1, 1), (1, 2)])
        self.assertEqual(t.passes, 2 + 1 + 3)

    def test_running_max(self):
        g = running_max()
        self.assertIsNone(next(g))
        self.assertEqual([g.send(x) for x in (3, 1, 9, 4, -2, 12)], [3, 3, 9, 9, 9, 12])
        g.close()


if __name__ == "__main__":
    unittest.main()

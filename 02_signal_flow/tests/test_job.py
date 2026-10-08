import inspect
import unittest

import job
from job import (countdown, drone_response, first_blind_spot, longest_quiet, patrol_path,
                 scan_code, threat_level, walk)


class SignalFlow(unittest.TestCase):
    def test_threat_level(self):
        self.assertEqual([threat_level(n) for n in range(6)],
                         ["clear", "watch", "watch", "run", "run", "run"])

    def test_countdown(self):
        self.assertEqual(countdown(3), "3..2..1..GO")
        self.assertEqual(countdown(1), "1..GO")
        self.assertEqual(countdown(0), "GO")
        self.assertIn("while", inspect.getsource(job.countdown))

    def test_patrol_path(self):
        self.assertEqual(patrol_path(8, 3, 4, 10), [8, 1, 4, 7])
        self.assertEqual(patrol_path(0, 1, 3, 2), [0, 1, 0])
        self.assertEqual(patrol_path(5, 0, 2, 10), [5, 5])
        self.assertEqual(patrol_path(0, 1, 0, 10), [])

    def test_first_blind_spot(self):
        self.assertEqual(first_blind_spot([3, 1, 0, 2, 0]), 2)
        self.assertEqual(first_blind_spot([0]), 0)
        self.assertEqual(first_blind_spot([1, 2, 3]), -1)
        self.assertEqual(first_blind_spot([]), -1)
        self.assertNotIn(".index(", inspect.getsource(job.first_blind_spot))

    def test_scan_code(self):
        self.assertEqual([scan_code(n) for n in range(1, 16)],
                         ["1", "2", "SCAN", "4", "LOCK", "SCAN", "7", "8", "SCAN", "LOCK",
                          "11", "SCAN", "13", "14", "SCANLOCK"])

    def test_longest_quiet(self):
        self.assertEqual(longest_quiet([1, 2, None, 3, 9, 1], 5), 3)
        self.assertEqual(longest_quiet([9, 9, 9], 5), 0)
        self.assertEqual(longest_quiet([], 5), 0)
        self.assertEqual(longest_quiet([None, None], 5), 0)
        self.assertEqual(longest_quiet([1, 7, 1, 1, 7, 1], 5), 2)
        self.assertEqual(longest_quiet([5, 4], 5), 1)

    def test_walk(self):
        self.assertEqual(walk([]), (0, 0))
        self.assertEqual(walk(["go north", "go east 3", "wait", "go south 2"]), (3, -1))
        self.assertEqual(walk(["jump 10 10", "go west", "hide"]), (9, 10))
        with self.assertRaises(ValueError):
            walk(["fly north"])
        with self.assertRaises(ValueError):
            walk(["go"])
        self.assertIn("match", inspect.getsource(job.walk))

    def test_drone_response(self):
        self.assertEqual(drone_response({"type": "scan", "hit": True}), "RUN")
        self.assertEqual(drone_response({"type": "scan", "hit": False, "range": 4}), "HOLD")
        self.assertEqual(drone_response({"type": "patrol", "id": "W-17"}), "AVOID W-17")
        self.assertEqual(drone_response({"type": "patrol", "id": "C-02"}), "IGNORE C-02")
        self.assertEqual(drone_response({"type": "alarm", "zone": 2}), "EVACUATE ZONE 2")
        self.assertEqual(drone_response({"type": "alarm", "zone": 9}), "UNKNOWN")
        self.assertEqual(drone_response({"type": "scan"}), "UNKNOWN")
        self.assertEqual(drone_response({}), "UNKNOWN")


if __name__ == "__main__":
    unittest.main()

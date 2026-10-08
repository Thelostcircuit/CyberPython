import inspect
import unittest

import job
from job import (checksum, index_by_owner, invert, leaderboard, owners, reassemble,
                 shared_contacts, split_packet, transpose, valid_shards)


def mk(seq, owner, text, good=True):
    c = sum(map(ord, text)) % 256
    return (seq, owner, text, c if good else (c + 1) % 256)


SHARDS = [
    mk(3, "iris", "coil "),
    mk(1, "iris", "the "),
    mk(2, "iris", "key to "),
    mk(9, "dex", "nope"),
    mk(2, "iris", "key to "),        # duplicate copy
    mk(4, "iris", "GARBAGE", good=False),
    mk(4, "iris", "is MONTY"),
    mk(1, "dex", "x", good=False),
]


class DataShards(unittest.TestCase):
    def test_checksum(self):
        self.assertEqual(checksum(""), 0)
        self.assertEqual(checksum("A"), 65)
        self.assertEqual(checksum("zzz"), (122 * 3) % 256)

    def test_valid_shards(self):
        v = valid_shards(SHARDS)
        self.assertEqual(len(v), 6)
        self.assertNotIn(SHARDS[5], v)
        self.assertEqual(v[0], SHARDS[0])
        self.assertIn("[", inspect.getsource(job.valid_shards))  # a comprehension

    def test_reassemble(self):
        self.assertEqual(reassemble(SHARDS, "iris"), "the key to coil is MONTY")
        self.assertEqual(reassemble(SHARDS, "dex"), "nope")
        self.assertEqual(reassemble(SHARDS, "nobody"), "")

    def test_owners(self):
        self.assertEqual(owners(SHARDS), ["dex", "iris"])
        self.assertEqual(owners([]), [])

    def test_index_by_owner(self):
        self.assertEqual(index_by_owner(SHARDS), {"iris": [1, 2, 3, 4], "dex": [1, 9]})

    def test_split_packet(self):
        self.assertEqual(split_packet(["H", "a", "b", "F"]), ("H", ["a", "b"], "F"))
        self.assertEqual(split_packet(["H", "F"]), ("H", [], "F"))

    def test_shared_contacts(self):
        a = ["mako", "juno", "adder", "dex"]
        b = ["adder", "dex", "sable"]
        c = ["dex", "adder", "adder"]
        self.assertEqual(shared_contacts(a, b, c), ["adder", "dex"])
        self.assertEqual(shared_contacts(a), sorted(a))
        self.assertEqual(shared_contacts(), [])

    def test_leaderboard(self):
        scores = {"dex": 90, "sable": 95, "adder": 90, "mako": 10, "juno": 95}
        self.assertEqual(leaderboard(scores, 3), ["juno", "sable", "adder"])
        self.assertEqual(leaderboard(scores, 10), ["juno", "sable", "adder", "dex", "mako"])
        self.assertEqual(leaderboard({}, 2), [])

    def test_invert(self):
        self.assertEqual(invert({"a": "x", "b": "y", "c": "x"}), {"x": ["a", "c"], "y": "b"})
        self.assertEqual(invert({}), {})

    def test_transpose(self):
        self.assertEqual(transpose([[1, 2, 3], [4, 5, 6]]), [[1, 4], [2, 5], [3, 6]])
        self.assertEqual(transpose([[7]]), [[7]])
        self.assertEqual(transpose([]), [])


if __name__ == "__main__":
    unittest.main()

import pickle
import sqlite3
import tempfile
import unittest
from pathlib import Path

import job

ROWS = [("OS-ENG-4471", "Iris Vale", "C-17"), ("OS-FIN-0042", "R. Moss", "A-02"),
        ("OS-OPS-1111", "K. Lin", "C-03"), ("OS-ENG-0007", "T. Aro", "B-11")]


class Vault(unittest.TestCase):
    def setUp(self):
        self.conn = job.open_vault(":memory:")
        job.add_subjects(self.conn, ROWS)

    def tearDown(self):
        self.conn.close()

    def test_row_factory(self):
        self.assertIs(self.conn.row_factory, sqlite3.Row)
        again = job.open_vault(":memory:")
        again.close()

    def test_in_wing(self):
        self.assertEqual(job.in_wing(self.conn, "C"), [
            {"id": "OS-ENG-4471", "name": "Iris Vale", "rack": "C-17"},
            {"id": "OS-OPS-1111", "name": "K. Lin", "rack": "C-03"}])
        self.assertEqual(job.in_wing(self.conn, "Z"), [])
        self.assertEqual(job.in_wing(self.conn, "' OR '1'='1"), [])

    def test_rack_counts(self):
        self.assertEqual(job.rack_counts(self.conn), {"A": 1, "B": 1, "C": 2})

    def test_atomic_insert(self):
        with self.assertRaises(sqlite3.IntegrityError):
            job.add_subjects(self.conn, [("NEW-1", "a", "D-1"), ("OS-ENG-4471", "dup", "D-2")])
        self.assertEqual(job.in_wing(self.conn, "D"), [])

    def test_transfer(self):
        job.transfer(self.conn, "OS-ENG-4471", "D-01")
        self.assertEqual(job.in_wing(self.conn, "D")[0]["id"], "OS-ENG-4471")
        with self.assertRaises(KeyError):
            job.transfer(self.conn, "NOBODY", "A-1")


class Files(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.d = Path(self._tmp.name)

    def tearDown(self):
        self._tmp.cleanup()

    def test_pickle(self):
        state = {"crew": ["dex", "sable"], "stake": 12000, "gap": (3, 14)}
        job.save_state(state, self.d / "s.pkl")
        self.assertEqual(job.load_state(self.d / "s.pkl"), state)

    def test_opcode_names(self):
        names = job.opcode_names(pickle.dumps([1, 2], protocol=2))
        self.assertEqual(names[0], "PROTO")
        self.assertEqual(names[-1], "STOP")
        self.assertIn("EMPTY_LIST", names)
        self.assertIn("STOP", job.opcode_names(pickle.dumps({"a": 1})))

    def test_copyreg(self):
        job.register_beacon_reducer()
        before = job.Beacon.reduced
        b = pickle.loads(pickle.dumps(job.Beacon(99.5)))
        self.assertEqual(b.freq, 99.5)
        self.assertEqual(job.Beacon.reduced, before + 1)

    def test_shelve(self):
        job.shelve_put(self.d / "crew", "dex", {"role": "runner"})
        self.assertEqual(job.shelve_get(self.d / "crew", "dex"), {"role": "runner"})
        self.assertEqual(job.shelve_get(self.d / "crew", "nobody", "?"), "?")

    def test_dbm(self):
        job.dbm_put(self.d / "cache", "gap", "03:14")
        self.assertEqual(job.dbm_get(self.d / "cache", "gap"), "03:14")
        self.assertIsNone(job.dbm_get(self.d / "cache", "nope"))

    def test_marshal(self):
        v = [1, "a", b"b", 2.5, (None, True), {"k": 1}]
        self.assertEqual(job.marshal_roundtrip(v), v)


if __name__ == "__main__":
    unittest.main()

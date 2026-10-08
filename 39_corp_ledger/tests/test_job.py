import unittest

from sqlalchemy import inspect as sa_inspect
from sqlalchemy.exc import IntegrityError

import job

LAYOUT = {
    "C": {"C-17": [("OS-ENG-4471", "Iris Vale")],
          "C-03": [("OS-OPS-1111", "K. Lin"), ("OS-MED-3000", "J. Park")]},
    "A": {"A-02": [("OS-FIN-0042", "R. Moss"), ("OS-FIN-0043", "T. Moss")]},
    "B": {"B-11": []},
}


class Ledger(unittest.TestCase):
    def setUp(self):
        self.engine = job.make_engine("sqlite://")
        job.seed(self.engine, LAYOUT)

    def tearDown(self):
        self.engine.dispose()

    def test_schema(self):
        insp = sa_inspect(self.engine)
        self.assertEqual(sorted(insp.get_table_names()), ["racks", "subjects", "wings"])
        cols = {c["name"]: c for c in insp.get_columns("subjects")}
        self.assertTrue(cols["rack_id"]["nullable"])
        fks = insp.get_foreign_keys("racks")
        self.assertEqual(fks[0]["referred_table"], "wings")

    def test_seed_atomic(self):
        with self.assertRaises(IntegrityError):
            job.seed(self.engine, {"D": {"D-01": [("NEW-1", "x")]}, "C": {"C-99": []}})
        self.assertEqual(job.ids_in_wing(self.engine, "D"), [])

    def test_queries(self):
        self.assertEqual(job.ids_in_wing(self.engine, "C"), ["OS-ENG-4471", "OS-MED-3000", "OS-OPS-1111"])
        self.assertEqual(job.ids_in_wing(self.engine, "B"), [])
        self.assertEqual(job.count_by_status(self.engine), {"archived": 5})
        self.assertEqual(job.rack_code(self.engine, "OS-ENG-4471"), "C-17")
        self.assertIsNone(job.rack_code(self.engine, "NOBODY"))
        self.assertEqual(job.fullest_rack(self.engine), "A-02")

    def test_release_all(self):
        job.release_all(self.engine, ["OS-OPS-1111", "OS-ENG-4471"])
        self.assertEqual(job.count_by_status(self.engine), {"archived": 3, "released": 2})
        self.assertIsNone(job.rack_code(self.engine, "OS-ENG-4471"))
        self.assertEqual(job.ids_in_wing(self.engine, "C"), ["OS-MED-3000"])

    def test_release_all_is_atomic(self):
        with self.assertRaises(KeyError):
            job.release_all(self.engine, ["OS-FIN-0042", "GHOST-0000"])
        self.assertEqual(job.count_by_status(self.engine), {"archived": 5})
        self.assertEqual(job.rack_code(self.engine, "OS-FIN-0042"), "A-02")

    def test_raw_count(self):
        self.assertEqual(job.raw_count(self.engine, "archived"), 5)
        self.assertEqual(job.raw_count(self.engine, "x' OR '1'='1"), 0)


if __name__ == "__main__":
    unittest.main()

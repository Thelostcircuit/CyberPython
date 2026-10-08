import unittest

import pandas as pd

import job

CSV = """id,name,rack,archived,handler_id,status,activity
OS-ENG-4471,  Iris Vale ,C-17,2091-01-14,H1,held,0.99
OS-FIN-0042,R. Moss,A-02,2091-01-20,H2,archived,0.40
OS-OPS-1111,K. Lin,C-03,2091-02-02,H9,archived,
OS-ENG-0007,T. Aro,B-11,2091-02-11,H1,archived,0.75
OS-FIN-0042,R. Moss,A-02,2091-01-20,H2,archived,0.45
OS-MED-3000,J. Park,C-40,2091-03-30,H2,held,0.75
"""

STAFF = pd.DataFrame({"handler_id": ["H1", "H2"], "handler": ["R. Okonkwo", "H. Voss"]})


class DataBroker(unittest.TestCase):
    def setUp(self):
        self.raw = job.load(CSV)
        self.df = job.clean(self.raw)

    def test_load(self):
        self.assertEqual(self.raw.shape, (6, 7))
        self.assertTrue(pd.api.types.is_datetime64_any_dtype(self.raw["archived"]))

    def test_clean(self):
        self.assertEqual(len(self.df), 5)
        self.assertEqual(self.df.loc[0, "name"], "Iris Vale")
        moss = self.df[self.df["id"] == "OS-FIN-0042"]
        self.assertEqual(moss["activity"].tolist(), [0.45])
        self.assertEqual(self.df.loc[self.df["id"] == "OS-OPS-1111", "activity"].item(), 0.0)
        self.assertEqual(list(self.df.index), [0, 1, 2, 3, 4])
        self.assertEqual(len(self.raw), 6)

    def test_with_wing(self):
        w = job.with_wing(self.df)
        self.assertEqual(w["wing"].tolist(), ["C", "C", "B", "A", "C"])
        self.assertNotIn("wing", self.df.columns)

    def test_queries(self):
        self.assertEqual(job.ids_in_wing(self.df, "C"), ["OS-ENG-4471", "OS-MED-3000", "OS-OPS-1111"])
        self.assertEqual(job.count_by_wing(self.df), {"A": 1, "B": 1, "C": 3})

    def test_activity_summary(self):
        s = job.activity_summary(self.df)
        self.assertEqual(list(s.index), ["A", "B", "C"])
        self.assertEqual(list(s.columns), ["mean", "max"])
        self.assertAlmostEqual(s.loc["C", "mean"], (0.99 + 0.0 + 0.75) / 3)
        self.assertEqual(s.loc["C", "max"], 0.99)

    def test_per_month(self):
        self.assertEqual(job.archived_per_month(self.df), {"2091-01": 2, "2091-02": 2, "2091-03": 1})

    def test_handlers(self):
        m = job.with_handlers(self.df, STAFF)
        self.assertEqual(m["id"].tolist(), self.df["id"].tolist())
        self.assertEqual(m["handler"].tolist(),
                         ["R. Okonkwo", "unassigned", "R. Okonkwo", "H. Voss", "H. Voss"])

    def test_release_queue(self):
        self.assertEqual(job.release_queue(self.df, 3), ["OS-ENG-4471", "OS-ENG-0007", "OS-MED-3000"])

    def test_status_table(self):
        self.assertEqual(job.status_table(self.df), {
            "A": {"archived": 1, "held": 0},
            "B": {"archived": 1, "held": 0},
            "C": {"archived": 1, "held": 2}})


if __name__ == "__main__":
    unittest.main()

import json
import unittest
from datetime import date, datetime

from pydantic import ValidationError

import job

GOOD = {"badge_id": "OS-MNT-0311", "name": "R. Okonkwo", "clearance": "3",
        "wings": ["c", "a"], "issued": "2091-01-02", "expires": "2092-01-02"}


class Badges(unittest.TestCase):
    def test_valid(self):
        b = job.check(GOOD)
        self.assertIsInstance(b, job.Badge)
        self.assertEqual((b.clearance, b.wings, b.issued), (3, ["C", "A"], date(2091, 1, 2)))
        self.assertFalse(b.is_admin)
        self.assertIn("is_admin", b.model_dump())
        self.assertEqual(job.Badge(**{**GOOD, "wings": []}).wings, [])
        self.assertTrue(job.check({**GOOD, "clearance": 7}).is_admin)

    def test_default_wings_fresh(self):
        data = {k: v for k, v in GOOD.items() if k != "wings"}
        a, b = job.Badge(**data), job.Badge(**data)
        a.wings.append("Z")
        self.assertEqual(b.wings, [])

    def test_errors(self):
        bad = {**GOOD, "badge_id": "OS-MNT-31", "clearance": 9, "name": ""}
        self.assertEqual(job.check(bad), ["badge_id", "clearance", "name"])
        self.assertEqual(job.check({**GOOD, "wings": ["CC"]}), ["wings"])
        self.assertEqual(job.check({**GOOD, "expires": "2090-01-01"}), ["__model__"])
        self.assertEqual(job.check({"name": "x"}), ["badge_id", "clearance", "expires", "issued"])

    def test_json(self):
        b = job.check(GOOD)
        out = json.loads(job.public_json(b))
        self.assertNotIn("name", out)
        self.assertEqual(out["issued"], "2091-01-02")
        self.assertEqual(out["is_admin"], False)
        again = job.load_json(json.dumps(GOOD))
        self.assertEqual(again, b)
        with self.assertRaises(ValidationError):
            job.load_json('{"badge_id": "OS-MNT-0311"')


class Visits(unittest.TestCase):
    def test_visit(self):
        v = job.Visit(badge=GOOD, purpose="maintenance", at="2091-03-22T03:14:00")
        self.assertIsInstance(v.badge, job.Badge)
        self.assertEqual(v.at, datetime(2091, 3, 22, 3, 14))
        with self.assertRaises(ValidationError):
            v.purpose = "audit"
        with self.assertRaises(ValidationError):
            job.Visit(badge=GOOD, purpose="heist", at="2091-03-22T03:14:00")
        with self.assertRaises(ValidationError):
            job.Visit(badge=GOOD, purpose="audit", at="2091-03-22T03:14:00", crowbar=True)
        with self.assertRaises(ValidationError):
            job.Visit(badge={**GOOD, "clearance": 0}, purpose="audit", at="2091-03-22T03:14:00")


class Adapters(unittest.TestCase):
    def test_ports(self):
        self.assertEqual(job.ports(["80", 443, 7443]), [80, 443, 7443])
        for bad in ([0], [70000], ["http"]):
            with self.subTest(bad=bad), self.assertRaises(ValidationError):
                job.ports(bad)

    def test_required(self):
        self.assertEqual(job.required_fields(job.Badge),
                         ["badge_id", "clearance", "expires", "issued", "name"])
        self.assertEqual(job.required_fields(job.Visit), ["at", "badge", "purpose"])


if __name__ == "__main__":
    unittest.main()

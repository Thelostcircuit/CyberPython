import inspect
import unittest

from fastapi.testclient import TestClient

import job

AUTH = {"X-Token": job.TOKEN}


def t(sid, rack="C-17", priority=3):
    return {"subject_id": sid, "rack": rack, "priority": priority}


class FastLane(unittest.TestCase):
    def setUp(self):
        job.reset()
        self.client = TestClient(job.app)

    def test_health(self):
        self.assertEqual(self.client.get("/health").json(), {"ok": True, "transfers": 0})

    def test_create(self):
        r = self.client.post("/transfers", json=t("OS-ENG-4471", priority=1), headers=AUTH)
        self.assertEqual((r.status_code, r.json()), (201, t("OS-ENG-4471", priority=1)))
        self.assertEqual(job.AUDIT, ["transfer OS-ENG-4471"])
        self.assertEqual(self.client.get("/health").json()["transfers"], 1)
        dup = self.client.post("/transfers", json=t("OS-ENG-4471"), headers=AUTH)
        self.assertEqual((dup.status_code, dup.json()), (409, {"detail": "duplicate"}))
        default = self.client.post("/transfers", json={"subject_id": "OS-FIN-0042", "rack": "A-2"},
                                   headers=AUTH)
        self.assertEqual(default.json()["priority"], 3)

    def test_auth(self):
        r = self.client.post("/transfers", json=t("OS-ENG-4471"))
        self.assertEqual((r.status_code, r.json()), (401, {"detail": "bad token"}))
        r = self.client.post("/transfers", json=t("OS-ENG-4471"), headers={"X-Token": "guess"})
        self.assertEqual(r.status_code, 401)
        self.assertEqual(job.STORE, {})

    def test_validation(self):
        for bad in (t("iris"), t("OS-ENG-4471", rack="C17"), t("OS-ENG-4471", priority=9),
                    {"rack": "C-1"}):
            with self.subTest(bad=bad):
                self.assertEqual(self.client.post("/transfers", json=bad, headers=AUTH).status_code, 422)

    def test_get_and_list(self):
        for body in (t("OS-OPS-1111", "C-03", 2), t("OS-ENG-4471", "C-17", 1),
                     t("OS-FIN-0042", "A-02", 2), t("OS-MED-3000", "C-40", 5)):
            self.client.post("/transfers", json=body, headers=AUTH)
        self.assertEqual(self.client.get("/transfers/OS-FIN-0042").json()["rack"], "A-02")
        r = self.client.get("/transfers/NOPE")
        self.assertEqual((r.status_code, r.json()), (404, {"detail": "not found"}))
        ids = [x["subject_id"] for x in self.client.get("/transfers").json()["transfers"]]
        self.assertEqual(ids, ["OS-ENG-4471", "OS-FIN-0042", "OS-OPS-1111", "OS-MED-3000"])
        c = [x["subject_id"] for x in self.client.get("/transfers?wing=C&limit=2").json()["transfers"]]
        self.assertEqual(c, ["OS-ENG-4471", "OS-OPS-1111"])
        self.assertEqual(self.client.get("/transfers?limit=0").status_code, 422)
        self.assertEqual(self.client.get("/transfers?limit=101").status_code, 422)

    def test_delete(self):
        self.client.post("/transfers", json=t("OS-ENG-4471"), headers=AUTH)
        self.assertEqual(self.client.delete("/transfers/OS-ENG-4471").status_code, 401)
        r = self.client.delete("/transfers/OS-ENG-4471", headers=AUTH)
        self.assertEqual((r.status_code, r.content), (204, b""))
        self.assertEqual(self.client.delete("/transfers/OS-ENG-4471", headers=AUTH).status_code, 404)

    def test_openapi_and_async(self):
        paths = job.app.openapi()["paths"]
        self.assertIn("/transfers", paths)
        self.assertIn("/transfers/{subject_id}", paths)
        self.assertIn("Transfer", job.app.openapi()["components"]["schemas"])
        for route in job.app.routes:
            if getattr(route, "path", "").startswith(("/health", "/transfers")):
                self.assertTrue(inspect.iscoroutinefunction(route.endpoint), route.path)


if __name__ == "__main__":
    unittest.main()

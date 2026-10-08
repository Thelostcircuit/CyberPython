import unittest

import job

IRIS = {"id": "OS-ENG-4471", "name": "Iris Vale", "wing": "C"}


class FrontDoor(unittest.TestCase):
    def setUp(self):
        self.app = job.create_app({"TESTING": True})
        self.client = self.app.test_client()

    def test_home(self):
        r = self.client.get("/")
        self.assertEqual(r.status_code, 200)
        self.assertIn("text/html", r.content_type)
        self.assertEqual(r.get_data(as_text=True), "<h1>You're safe.</h1><p>Welcome back, friend.</p>")
        r = self.client.get("/?name=<script>x</script>")
        self.assertIn("&lt;script&gt;", r.get_data(as_text=True))

    def test_status_and_checkin(self):
        self.assertEqual(self.client.get("/api/status").get_json(), {"status": "up", "checked_in": 0})
        r = self.client.post("/api/checkin", json={**IRIS, "extra": "ignored"})
        self.assertEqual((r.status_code, r.get_json()), (201, IRIS))
        self.assertEqual(self.client.get("/api/status").get_json()["checked_in"], 1)
        self.assertEqual(self.client.post("/api/checkin", json=IRIS).status_code, 409)
        r = self.client.post("/api/checkin", json={"id": "x"})
        self.assertEqual((r.status_code, r.get_json()), (400, {"error": "missing field"}))
        self.assertEqual(self.client.post("/api/checkin", data="not json").status_code, 400)

    def test_lookup_and_roster(self):
        for rec in (IRIS, {"id": "OS-FIN-0042", "name": "R. Moss", "wing": "A"},
                    {"id": "OS-OPS-1111", "name": "K. Lin", "wing": "C"}):
            self.client.post("/api/checkin", json=rec)
        self.assertEqual(self.client.get("/api/checkin/OS-ENG-4471").get_json(), IRIS)
        r = self.client.get("/api/checkin/NOBODY")
        self.assertEqual((r.status_code, r.get_json()), (404, {"error": "not found"}))
        ids = [x["id"] for x in self.client.get("/api/roster").get_json()["roster"]]
        self.assertEqual(ids, ["OS-ENG-4471", "OS-FIN-0042", "OS-OPS-1111"])
        c_ids = [x["id"] for x in self.client.get("/api/roster?wing=C").get_json()["roster"]]
        self.assertEqual(c_ids, ["OS-ENG-4471", "OS-OPS-1111"])

    def test_apps_are_independent(self):
        self.client.post("/api/checkin", json=IRIS)
        other = job.create_app({"TESTING": True}).test_client()
        self.assertEqual(other.get("/api/status").get_json()["checked_in"], 0)

    def test_session(self):
        self.assertEqual(self.client.get("/api/me").status_code, 401)
        self.client.post("/api/login", json={"user": "adder"})
        self.assertEqual(self.client.get("/api/me").get_json(), {"user": "adder"})
        fresh = self.app.test_client()
        self.assertEqual(fresh.get("/api/me").status_code, 401)

    def test_404(self):
        r = self.client.get("/nowhere")
        self.assertEqual((r.status_code, r.get_json()), (404, {"error": "not found"}))

    def test_blueprint(self):
        self.assertIn("api", self.app.blueprints)
        self.assertEqual(self.app.config["SECRET_KEY"], "dev")
        self.assertEqual(job.create_app({"SECRET_KEY": "x"}).config["SECRET_KEY"], "x")


if __name__ == "__main__":
    unittest.main()

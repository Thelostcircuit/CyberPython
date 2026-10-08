import email
import email.policy
import tempfile
import unittest
from pathlib import Path
from wsgiref.util import setup_testing_defaults

import job


class Urls(unittest.TestCase):
    def test_portal_url(self):
        self.assertEqual(job.portal_url("http://portal.ouro/api/", "orders", rack="C-17", n=2),
                         "http://portal.ouro/api/orders?rack=C-17&n=2")
        self.assertEqual(job.portal_url("http://portal.ouro/api/v1", "status"),
                         "http://portal.ouro/api/status")

    def test_query_params(self):
        self.assertEqual(job.query_params("https://p.ouro/o?id=7&rack=C-17&id=8#top"),
                         {"id": "7", "rack": "C-17"})

    def test_status_line(self):
        self.assertEqual(job.status_line(404), "404 Not Found")
        self.assertEqual(job.status_line(201), "201 Created")


class Portal(unittest.TestCase):
    def setUp(self):
        self.server, self.port = job.start_portal()
        self.base = f"http://127.0.0.1:{self.port}"

    def tearDown(self):
        self.server.shutdown()
        self.server.server_close()

    def test_status(self):
        self.assertEqual(job.fetch_json(self.base + "/status"), (200, {"status": "up"}))
        self.assertEqual(job.fetch_json(self.base + "/nope"), (404, {"error": "not found"}))

    def test_orders(self):
        status, data, session = job.lodge_order(self.port, "OS-ENG-4471")
        self.assertEqual(status, 201)
        self.assertEqual(data["subject"], "OS-ENG-4471")
        self.assertEqual(session, f"order-{data['order']}")
        status2, data2, _ = job.lodge_order(self.port, "OS-FIN-0042")
        self.assertEqual(data2["order"], data["order"] + 1)

    def test_bad_order(self):
        import urllib.request, urllib.error, json
        req = urllib.request.Request(self.base + "/orders", data=b"nothing=here", method="POST")
        with self.assertRaises(urllib.error.HTTPError) as ctx:
            urllib.request.urlopen(req, timeout=5)
        self.assertEqual(ctx.exception.code, 400)
        self.assertEqual(json.loads(ctx.exception.read()), {"error": "missing subject"})
        ctx.exception.close()


class Misc(unittest.TestCase):
    def test_robots(self):
        robots = "User-agent: *\nDisallow: /vault/\n"
        self.assertTrue(job.robots_allowed(robots, "http://portal.ouro/status"))
        self.assertFalse(job.robots_allowed(robots, "http://portal.ouro/vault/c-17"))

    def test_wsgi(self):
        env = {}
        setup_testing_defaults(env)
        env["PATH_INFO"] = "/gap"
        seen = {}

        def start_response(status, headers):
            seen["status"], seen["headers"] = status, dict(headers)
        body = b"".join(job.hello_app(env, start_response))
        self.assertEqual(body, b"hello /gap")
        self.assertEqual(seen["status"], "200 OK")
        self.assertEqual(seen["headers"]["Content-Type"], "text/plain")

    def test_email(self):
        raw = job.confirmation("i.vale@ouro.internal", 7, "receipt.pdf", b"%PDF-1.7 ...")
        msg = email.message_from_bytes(raw, policy=email.policy.default)
        self.assertEqual(msg["From"], "portal@ouro.internal")
        self.assertEqual(job.read_confirmation(raw), {
            "subject": "Order 7 lodged",
            "body": "Your release order 7 has been lodged.",
            "attachments": [("receipt.pdf", "application/pdf", 12)]})
        odd = job.read_confirmation(job.confirmation("x@y", 1, "blob.zzqq", b"12"))
        self.assertEqual(odd["attachments"], [("blob.zzqq", "application/octet-stream", 2)])

    def test_mbox(self):
        with tempfile.TemporaryDirectory() as d:
            msgs = [job.confirmation("a@b", n, "r.pdf", b"x") for n in (1, 2)]
            self.assertEqual(job.archive_and_list(str(Path(d) / "inbox"), msgs),
                             ["Order 1 lodged", "Order 2 lodged"])

    def test_rpc(self):
        self.assertEqual(job.rpc_pow(2, 10), 1024)


if __name__ == "__main__":
    unittest.main()

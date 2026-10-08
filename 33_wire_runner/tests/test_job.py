import socket
import tempfile
import unittest
from pathlib import Path

import requests

import job
from tests.fake_ouro import TOKEN, FakeOuro


class WireRunner(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.fake = FakeOuro().__enter__()
        cls.base = cls.fake.base

    @classmethod
    def tearDownClass(cls):
        cls.fake.__exit__(None, None, None)

    def test_status(self):
        self.assertEqual(job.status(self.base), "up")

    def test_search(self):
        self.assertEqual(job.search(self.base, rack="C-17", note="a&b c"),
                         {"rack": "C-17", "note": "a&b c"})

    def test_lodge(self):
        self.assertEqual(job.lodge(self.base, "OS-ENG-4471", TOKEN),
                         {"order": 7, "subject": "OS-ENG-4471"})
        with self.assertRaises(requests.HTTPError) as ctx:
            job.lodge(self.base, "OS-ENG-4471", "wrong")
        self.assertEqual(ctx.exception.response.status_code, 403)

    def test_probe(self):
        self.assertEqual(job.probe(f"{self.base}/status", 5), 200)
        self.assertEqual(job.probe(f"{self.base}/missing", 5), 404)
        self.assertEqual(job.probe(f"{self.base}/slow", 0.3), "timeout")
        with socket.socket() as s:
            s.bind(("127.0.0.1", 0))
            dead_port = s.getsockname()[1]
        self.assertEqual(job.probe(f"http://127.0.0.1:{dead_port}/", 2), "unreachable")

    def test_whoami(self):
        self.assertEqual(job.whoami(self.base, "iris", "first-light"), "I. Vale")
        self.assertIsNone(job.whoami(self.base, "iris", "guess"))

    def test_download(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "blob.bin"
            self.assertEqual(job.download(f"{self.base}/blob", p), 102_400)
            self.assertEqual(p.read_bytes()[:3], b"\x00\x01\x02")

    def test_patient_get(self):
        data = job.patient_get(f"{self.base}/flaky")
        self.assertTrue(data["ok"])
        self.assertEqual(data["hits"] % 3, 0)

    def test_redirect_trail(self):
        self.assertEqual(job.redirect_trail(f"{self.base}/old"), (f"{self.base}/status", 2))


if __name__ == "__main__":
    unittest.main()

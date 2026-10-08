import json
import os
import tempfile
import unittest
from datetime import date, datetime
from decimal import Decimal
from pathlib import Path

import job


class TextFormats(unittest.TestCase):
    def test_to_json(self):
        out = job.to_json({"b": {3, 1}, "a": datetime(2091, 3, 22, 3, 14), "d": date(2091, 1, 2)})
        self.assertEqual(json.loads(out), {"a": "2091-03-22T03:14:00", "b": [1, 3], "d": "2091-01-02"})
        self.assertTrue(out.startswith('{\n  "a"'))
        with self.assertRaises(TypeError):
            job.to_json({"x": object()})

    def test_load_amounts(self):
        data = job.load_amounts('{"stake": 12000.10, "fees": [0.1, 0.2], "n": 3}')
        self.assertEqual(data["stake"], Decimal("12000.10"))
        self.assertEqual(sum(data["fees"]), Decimal("0.3"))
        self.assertEqual(data["n"], 3)

    def test_roster(self):
        text = 'name,role,clearance\nSable,"security, ex",4\nDex,runner,1\n'
        rows = job.read_roster(text)
        self.assertEqual(rows[0], {"name": "Sable", "role": "security, ex", "clearance": 4})
        back = job.write_roster(rows, ["name", "role", "clearance"])
        self.assertEqual(back, text)

    def test_toml(self):
        self.assertEqual(job.toml_server('[server]\nhost = "intake.coil"\nport = 7443\n'),
                         ("intake.coil", 7443))
        self.assertEqual(job.toml_server("[server]\nport = 1\n"), ("localhost", 1))

    def test_ini(self):
        text = ("[DEFAULT]\nroot = /coil\n\n[vault]\npath = %(root)s/vault\n"
                "port = 5432\n\n[intake]\nport = 7443\n")
        self.assertEqual(job.ini_settings(text), {
            "vault": {"root": "/coil", "path": "/coil/vault", "port": "5432"},
            "intake": {"root": "/coil", "port": "7443"}})

    def test_plist(self):
        obj = {"name": "Iris", "rack": "C-17", "flags": [True, 3, 2.5], "blob": b"\x00"}
        self.assertEqual(job.plist_roundtrip(obj), obj)


class Credentials(unittest.TestCase):
    @unittest.skipIf(os.name == "nt", "POSIX permissions")
    def test_netrc(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / ".netrc"
            p.write_text("machine archive.ouro login intern password hunter2\n")
            os.chmod(p, 0o600)
            self.assertEqual(job.netrc_login(str(p), "archive.ouro"), ("intern", "hunter2"))
            self.assertIsNone(job.netrc_login(str(p), "elsewhere"))


class Binary(unittest.TestCase):
    def test_manifest(self):
        blob = job.pack_manifest(1, 0x0003, 3_610_000)
        self.assertEqual(len(blob), 11)
        self.assertEqual(blob[:4], b"OURO")
        self.assertEqual(blob[5:7], b"\x00\x03")
        self.assertEqual(job.unpack_manifest(blob + b"payload..."),
                         {"version": 1, "flags": 3, "length": 3_610_000})
        with self.assertRaises(ValueError):
            job.unpack_manifest(b"EVIL" + blob[4:])

    def test_wrappers(self):
        data = bytes([0xfb, 0xff, 0x00, 0x10])
        w = job.wrap(data)
        self.assertIsInstance(w, str)
        self.assertNotIn("+", w)
        self.assertNotIn("/", w)
        self.assertEqual(job.unwrap(w), data)
        self.assertEqual(job.hex_pairs(b"\xde\xad\xbe\xef"), "de ad be ef")
        self.assertEqual(job.decode_qp(b"caf=C3=A9 cr=C3=A8me"), "café crème")


if __name__ == "__main__":
    unittest.main()

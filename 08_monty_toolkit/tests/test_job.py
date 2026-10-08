import io
import math
import os.path
import subprocess
import sys
import unittest
from contextlib import redirect_stdout
from pathlib import Path

import job


class Deck:
    level = 3

    def ping(self):
        return "pong"

    def add(self, a, b):
        return a + b

    def _secret(self):
        return "hidden"


class Toolkit(unittest.TestCase):
    def test_radix_report(self):
        self.assertEqual(job.radix_report(255), {"bin": "0b11111111", "oct": "0o377", "hex": "0xff"})
        self.assertEqual(job.radix_report(0)["bin"], "0b0")

    def test_rot(self):
        self.assertEqual(job.rot("Iris!", 1), "Jsjt!")
        self.assertEqual(job.rot("abc", -1), "zab")
        self.assertEqual(job.rot("Zz 9", 27), "Aa 9")
        self.assertEqual(job.rot(job.rot("Monty Python", 13), 13), "Monty Python")

    def test_xor_bytes(self):
        self.assertEqual(job.xor_bytes(b"\x0f\xf0", b"\xff"), b"\xf0\x0f")
        secret = job.xor_bytes(b"coil", b"key")
        self.assertIsInstance(secret, bytes)
        self.assertEqual(job.xor_bytes(secret, b"key"), b"coil")

    def test_patch_in_place(self):
        buf = bytearray(b"hello world")
        self.assertEqual(job.patch_in_place(buf, 6, b"WORLD"), 5)
        self.assertEqual(buf, bytearray(b"hello WORLD"))
        self.assertEqual(job.patch_in_place(buf, 9, b"XYZ"), 2)
        self.assertEqual(buf, bytearray(b"hello WORXY"))
        self.assertEqual(job.patch_in_place(buf, 50, b"!"), 0)

    def test_public_api(self):
        self.assertEqual(job.public_api(Deck()), {"add": "method", "level": "value", "ping": "method"})

    def test_dispatch(self):
        d = Deck()
        self.assertEqual(job.dispatch(d, "ping"), "pong")
        self.assertEqual(job.dispatch(d, "add", 2, 3), 5)
        for bad in ("level", "missing", "_secret", "__class__"):
            with self.assertRaisesRegex(AttributeError, "no command"):
                job.dispatch(d, bad)

    def test_load_attr(self):
        self.assertIs(job.load_attr("math:sqrt"), math.sqrt)
        self.assertIs(job.load_attr("os.path:join"), os.path.join)
        with self.assertRaises(ModuleNotFoundError):
            job.load_attr("no_such_module_xyz:thing")

    def test_main_and_guard(self):
        out = io.StringIO()
        with redirect_stdout(out):
            job.main()
        self.assertEqual(out.getvalue(), "PYTHIA-9 // MONTY ONLINE\n")
        here = Path(job.__file__).parent
        run = subprocess.run([sys.executable, "job.py"], cwd=here, capture_output=True, text=True)
        self.assertEqual(run.stdout, "PYTHIA-9 // MONTY ONLINE\n")
        imp = subprocess.run([sys.executable, "-c", "import job"], cwd=here,
                             capture_output=True, text=True)
        self.assertEqual(imp.stdout, "")


if __name__ == "__main__":
    unittest.main()

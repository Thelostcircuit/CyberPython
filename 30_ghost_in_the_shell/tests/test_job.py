import ctypes
import importlib.metadata
import json
import os
import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

import job


def outer():
    return middle()


def middle():
    return job.who_called()


def sample(a, b=2, *rest, key, flag=False, **extra):
    pass


class Introspection(unittest.TestCase):
    def test_runtime(self):
        f = job.runtime_facts()
        self.assertEqual((f["major"], f["minor"]), sys.version_info[:2])
        self.assertEqual(f["implementation"], "cpython")
        self.assertEqual(f["recursion_limit"], sys.getrecursionlimit())
        self.assertEqual(job.in_venv(), sys.prefix != sys.base_prefix)

    def test_who_called(self):
        self.assertEqual(outer(), "outer")

    def test_params(self):
        self.assertEqual(job.params(sample), [
            ("a", "POSITIONAL_OR_KEYWORD", None), ("b", "POSITIONAL_OR_KEYWORD", 2),
            ("rest", "VAR_POSITIONAL", None), ("key", "KEYWORD_ONLY", None),
            ("flag", "KEYWORD_ONLY", False), ("extra", "VAR_KEYWORD", None)])

    def test_own_functions(self):
        names = job.own_functions(json)
        self.assertEqual(names, ["detect_encoding", "dump", "dumps", "load", "loads"])

    def test_gc(self):
        self.assertTrue(job.cycle_is_collected())


class Imports(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.d = Path(self._tmp.name)

    def tearDown(self):
        self._tmp.cleanup()

    def test_load_file(self):
        p = self.d / "tool.py"
        p.write_text("KEY = 'first_light'\ndef shout(x):\n    return x.upper()\n")
        mod = job.load_file("drop_tool", p)
        self.assertEqual((mod.KEY, mod.shout("hi")), ("first_light", "HI"))
        self.assertNotIn("drop_tool", sys.modules)

    def test_submodules(self):
        expected = sorted(p.stem for p in Path(json.__file__).parent.glob("*.py")
                          if p.stem != "__init__")
        self.assertIn("decoder", expected)
        self.assertEqual(job.submodules("json"), expected)

    def test_run_and_get(self):
        p = self.d / "script.py"
        p.write_text("RESULT = sum(range(10))\n")
        self.assertEqual(job.run_and_get(p, "RESULT"), 45)

    def test_zip_and_resources(self):
        z = self.d / "cache.zip"
        with zipfile.ZipFile(z, "w") as zf:
            zf.writestr("zipped_drop/__init__.py", "")
            zf.writestr("zipped_drop/core.py", "SECRET = 'rack C-17'\n")
            zf.writestr("zipped_drop/key.txt", "first light")
        mod = job.import_from_zip(z, "zipped_drop.core")
        self.assertEqual(mod.SECRET, "rack C-17")
        self.assertNotIn(str(z), sys.path)
        self.assertEqual(job.package_data("zipped_drop", "key.txt"), "first light")
        for name in ("zipped_drop.core", "zipped_drop"):
            sys.modules.pop(name, None)

    def test_installed_version(self):
        self.assertIsNone(job.installed_version("definitely-not-installed-xyz"))
        for dist in importlib.metadata.distributions():
            name = dist.metadata["Name"]
            self.assertEqual(job.installed_version(name), dist.version)
            break


class Low(unittest.TestCase):
    def test_header(self):
        self.assertEqual(ctypes.sizeof(job.Header), 12)
        h = job.Header(b"OURO", 2, 3_610_000)
        self.assertEqual((h.magic, h.version, h.length), (b"OURO", 2, 3_610_000))

    @unittest.skipUnless(os.name == "posix", "libc")
    def test_c_abs(self):
        self.assertEqual(job.c_abs(-17), 17)

    def test_is_complete(self):
        self.assertTrue(job.is_complete("x = 1"))
        self.assertFalse(job.is_complete("if x:"))
        self.assertFalse(job.is_complete("def f():"))
        with self.assertRaises(SyntaxError):
            job.is_complete("x = = 1")


class Env(unittest.TestCase):
    def test_fresh_venv(self):
        with tempfile.TemporaryDirectory() as d:
            py = job.fresh_venv(Path(d) / "env")
            self.assertTrue(py.exists())
            out = subprocess.run([str(py), "-c", "import sys; print(sys.prefix != sys.base_prefix)"],
                                 capture_output=True, text=True).stdout
            self.assertEqual(out.strip(), "True")

    def test_doc_text(self):
        text = job.doc_text(job.in_venv)
        self.assertIn("in_venv", text)


if __name__ == "__main__":
    unittest.main()

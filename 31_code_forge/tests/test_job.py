import sys
import tempfile
import unittest
from pathlib import Path

import job


def unlock(a, b):
    return a + b * 2


class Tokens(unittest.TestCase):
    def test_token_pairs(self):
        self.assertEqual(job.token_pairs("rack = 'C-' + str(17)  # go\n"), [
            ("NAME", "rack"), ("OP", "="), ("STRING", "'C-'"), ("OP", "+"),
            ("NAME", "str"), ("OP", "("), ("NUMBER", "17"), ("OP", ")")])

    def test_comments(self):
        self.assertEqual(job.comments("x = 1  # one\n# two\ny = '# not'\n"), ["# one", "# two"])

    def test_reserved(self):
        self.assertEqual([job.reserved(w) for w in ("for", "match", "rack", "None", "type")],
                         ["keyword", "soft keyword", "no", "keyword", "soft keyword"])


SRC = """
import os

def outer(n):
    total = n
    def inner(k):
        return k * scale
    return inner(total)

async def poll():
    await thing
"""


class Trees(unittest.TestCase):
    def test_names_used(self):
        self.assertEqual(job.names_used(SRC), ["inner", "k", "n", "scale", "thing", "total"])

    def test_function_names(self):
        self.assertEqual(job.function_names(SRC), ["outer", "inner", "poll"])

    def test_read_literal(self):
        self.assertEqual(job.read_literal("{'rack': ['C', 17], 'ok': True}"),
                         {"rack": ["C", 17], "ok": True})
        for bad in ("__import__('os')", "1 +", "x"):
            with self.subTest(bad=bad), self.assertRaises(ValueError):
                job.read_literal(bad)

    def test_fold(self):
        self.assertEqual(job.fold_constants("x = 2 * 3 + y\nz = (1 + 2) * (10 - 4)"),
                         "x = 6 + y\nz = 18")
        self.assertEqual(job.fold_constants("s = 'a' + 'b'\nb = True + 1"), "s = 'a' + 'b'\nb = True + 1")
        self.assertEqual(job.fold_constants("d = 7 / 2"), "d = 7 / 2")

    def test_rename(self):
        self.assertEqual(job.rename("key = 1\nprint(key + keys)", "key", "k"), "k = 1\nprint(k + keys)")


class Bytecode(unittest.TestCase):
    def test_opnames(self):
        ops = job.opnames(unlock)
        self.assertEqual(ops[-1], "RETURN_VALUE")
        self.assertEqual(job.count_opcode(unlock, "BINARY_OP"), 2)
        self.assertEqual(job.count_opcode(unlock, "CALL"), 0)
        with self.assertRaises(KeyError):
            job.count_opcode(unlock, "TELEPORT")

    def test_symtable(self):
        self.assertEqual(job.function_locals(SRC, "outer"), ["inner", "n", "total"])
        with self.assertRaises(KeyError):
            job.function_locals(SRC, "missing")


class Files(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.d = Path(self._tmp.name)

    def tearDown(self):
        self._tmp.cleanup()

    def test_outline(self):
        (self.d / "iris_tool.py").write_text("import nothing_real_xyz\nclass Key:\n    pass\n"
                                             "def unlock():\n    pass\nVALUE = 3\n")
        self.assertEqual(job.outline(self.d, "iris_tool"), {"Key": "class", "unlock": "function"})

    def test_compile(self):
        src = self.d / "tool.py"
        src.write_text("X = 1\n")
        pyc = job.build_pyc(src)
        self.assertTrue(pyc.exists())
        self.assertEqual(pyc.suffix, ".pyc")
        self.assertEqual(pyc.parent.name, "__pycache__")
        pkg = self.d / "pkg"
        pkg.mkdir()
        (pkg / "a.py").write_text("A = 1\n")
        self.assertTrue(job.build_tree(pkg))
        (pkg / "broken.py").write_text("def (:\n")
        self.assertFalse(job.build_tree(pkg))

    def test_tabnanny(self):
        good = self.d / "good.py"
        good.write_text("if True:\n    x = 1\n    y = 2\n")
        bad = self.d / "bad.py"
        bad.write_text("if True:\n        x = 1\n\ty = 2\n")
        self.assertFalse(job.tab_trouble(good))
        self.assertTrue(job.tab_trouble(bad))


if __name__ == "__main__":
    unittest.main()

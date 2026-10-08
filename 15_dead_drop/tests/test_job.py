import io
import os
import tempfile
import unittest
from pathlib import Path

import job


class DeadDrop(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)

    def tearDown(self):
        self._tmp.cleanup()

    def make(self, rel, text):
        p = self.root / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text, encoding="utf-8")
        return p

    def test_write_and_read(self):
        p = job.write_note(self.root / "chapel" / "bench", "note.txt", "line one\nline two\n")
        self.assertEqual(p, self.root / "chapel" / "bench" / "note.txt")
        self.assertEqual(job.read_lines(p), ["line one", "line two"])
        job.write_note(str(self.root / "chapel" / "bench"), "u.txt", "héllo")
        self.assertEqual(job.read_lines(self.root / "chapel/bench/u.txt"), ["héllo"])

    def test_find(self):
        self.make("a.txt", "x")
        self.make("sub/b.txt", "x")
        self.make("sub/deep/c.log", "x")
        (self.root / "d.txt").mkdir()
        self.assertEqual(job.find(self.root, "*.txt"), ["a.txt", "sub/b.txt"])
        self.assertEqual(job.find(str(self.root), "*.log"), ["sub/deep/c.log"])

    def test_matching_names(self):
        names = ["map_01.png", "map_2.png", "notes.txt", "map_10.png"]
        self.assertEqual(job.matching_names(names, "map_??.png"), ["map_01.png", "map_10.png"])

    def test_tree_size(self):
        self.make("a", "12345")
        self.make("x/y/z", "123")
        self.assertEqual(job.tree_size(self.root), 8)

    def test_compare_dirs(self):
        self.make("L/same", "s")
        self.make("R/same", "s")
        self.make("L/changed", "one")
        self.make("R/changed", "two")
        self.make("L/only_l", "")
        self.make("R/only_r", "")
        self.assertEqual(job.compare_dirs(self.root / "L", self.root / "R"),
                         {"left_only": ["only_l"], "right_only": ["only_r"], "different": ["changed"]})

    @unittest.skipIf(os.name == "nt", "POSIX permissions")
    def test_lock_down(self):
        p = self.make("secret", "x")
        os.chmod(p, 0o755)
        self.assertEqual(job.lock_down(p), "-rw-------")

    def test_relocate(self):
        p = self.make("loose.txt", "x")
        new = job.relocate(p, self.root / "vault" / "inner")
        self.assertEqual(new, self.root / "vault" / "inner" / "loose.txt")
        self.assertFalse(p.exists())
        self.assertTrue(new.exists())

    def test_scratch(self):
        self.assertEqual(job.scratch_roundtrip(b"\x00ICE"), (b"\x00ICE", False))

    def test_stitched(self):
        a = self.make("a.txt", "one\ntwo\n")
        b = self.make("b.txt", "three")
        self.assertEqual(job.stitched([a, b]),
                         [("a.txt", 1, "one"), ("a.txt", 2, "two"), ("b.txt", 1, "three")])

    def test_line_at(self):
        p = self.make("l.txt", "first\nsecond\nthird\n")
        self.assertEqual(job.line_at(p, 2), "second")
        self.assertEqual(job.line_at(p, 99), "")

    def test_upper_stream(self):
        out = job.upper_stream(io.StringIO("coil\nrack c-17\n"))
        self.assertIsInstance(out, io.StringIO)
        self.assertEqual(out.read(), "COIL\nRACK C-17\n")

    def test_windows_parts(self):
        self.assertEqual(job.windows_parts(r"C:\drops\chapel\map.v2.png"),
                         ("C:", "chapel", "map.v2", ".png"))


if __name__ == "__main__":
    unittest.main()

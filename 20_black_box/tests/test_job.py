import io
import logging
import subprocess
import sys
import tempfile
import unittest
import warnings
from pathlib import Path

import job


def explode():
    raise RuntimeError("vault seal")


class Logging(unittest.TestCase):
    def test_crew_logger(self):
        s = io.StringIO()
        log = job.crew_logger(s)
        log.debug("lift at %d", 3)
        logging.getLogger("crew.dock").info("clear")
        self.assertEqual(s.getvalue(), "DEBUG:crew:lift at 3\nINFO:crew.dock:clear\n")
        s2 = io.StringIO()
        log2 = job.crew_logger(s2)
        self.assertIs(log, log2)
        self.assertEqual(len(log2.handlers), 1)
        self.assertFalse(log2.propagate)
        log2.warning("x")
        self.assertEqual(s2.getvalue(), "WARNING:crew:x\n")

    def test_radio_config(self):
        s = io.StringIO()
        job.radio_config(s)
        radio = logging.getLogger("crew.radio")
        radio.info("chatter")
        radio.error("lost Dex")
        self.assertEqual(s.getvalue(), "ERROR|lost Dex\n")

    def test_blackbox(self):
        box = job.BlackBox()
        box.setFormatter(logging.Formatter("%(name)s>%(message)s"))
        log = logging.getLogger("bbtest")
        log.propagate = False
        log.setLevel(logging.INFO)
        log.addHandler(box)
        log.debug("hidden")
        log.info("at dock")
        log.error("drone")
        self.assertEqual(box.records, [("INFO", "bbtest>at dock"), ("ERROR", "bbtest>drone")])

    def test_risky_read(self):
        box = job.BlackBox()
        log = logging.getLogger("risky")
        log.propagate = False
        log.addHandler(box)
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "ok.txt"
            p.write_text("map")
            self.assertEqual(job.risky_read(log, p), "map")
            self.assertIsNone(job.risky_read(log, Path(d) / "missing.txt"))
        level, text = box.records[-1]
        self.assertEqual(level, "ERROR")
        self.assertIn("read failed", text)
        self.assertIn("Traceback", text)
        self.assertIn("FileNotFoundError", text)

    def test_rotating(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "ops.log"
            log = job.rotating_logger(path, 200, 2)
            for i in range(60):
                log.info("event %03d", i)
            for h in log.handlers:
                h.close()
            names = sorted(p.name for p in Path(d).iterdir())
            self.assertEqual(names, ["ops.log", "ops.log.1", "ops.log.2"])
            self.assertIn("event 059", path.read_text())


class Tracebacks(unittest.TestCase):
    def test_crash_site_and_text(self):
        try:
            explode()
        except RuntimeError as e:
            exc = e
        name, line = job.crash_site(exc)
        self.assertEqual(name, "explode")
        self.assertEqual(line, explode.__code__.co_firstlineno + 1)
        text = job.error_text(exc)
        self.assertTrue(text.startswith("Traceback (most recent call last):"))
        self.assertTrue(text.rstrip().endswith("RuntimeError: vault seal"))


class Warnings(unittest.TestCase):
    def test_old_scan(self):
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            self.assertEqual(job.old_scan(), "scanned")
        self.assertIs(w[0].category, DeprecationWarning)
        self.assertEqual(Path(w[0].filename).name, "test_job.py")

    def test_caught(self):
        def twice():
            job.old_scan()
            job.old_scan()
            warnings.warn("hot")
        self.assertEqual(job.caught_warnings(twice), ["old_scan is deprecated; use scan_v2"] * 2 + ["hot"])

    def test_strictly(self):
        self.assertEqual(job.strictly(lambda: 5), 5)
        with self.assertRaises(DeprecationWarning):
            job.strictly(job.old_scan)
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            job.old_scan()
        self.assertEqual(len(w), 1)


class LastWords(unittest.TestCase):
    def test_on_exit(self):
        here = Path(job.__file__).parent
        run = subprocess.run([sys.executable, "-c", "import job; job.on_exit('bye'); print('main')"],
                             cwd=here, capture_output=True, text=True)
        self.assertEqual(run.stdout, "main\nbye\n")

    def test_stack_dump(self):
        text = job.stack_dump()
        self.assertIn("stack_dump", text)
        self.assertIn("File", text)


if __name__ == "__main__":
    unittest.main()

"""The deck's gate for this chapter: run the pytest suite and require it to pass."""

import subprocess
import sys
import unittest
from pathlib import Path

SUITE = Path(__file__).parent / "suite"


class StressTest(unittest.TestCase):
    def test_pytest_suite_passes(self):
        run = subprocess.run([sys.executable, "-m", "pytest", str(SUITE), "-q",
                              "-p", "no:cacheprovider"],
                             capture_output=True, text=True, cwd=SUITE.parents[1])
        self.assertEqual(run.returncode, 0, run.stdout[-3000:] + run.stderr[-2000:])
        self.assertIn("passed", run.stdout)


if __name__ == "__main__":
    unittest.main()

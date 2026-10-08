import os
import signal
import subprocess
import sys
import tempfile
import time
import unittest
from pathlib import Path

import job

PY = sys.executable
POSIX = os.name == "posix"


def py(code):
    return [PY, "-c", code]


class Subprocess(unittest.TestCase):
    def test_run_tool(self):
        self.assertEqual(job.run_tool(py("import sys; print('up'); print('warn', file=sys.stderr); sys.exit(3)")),
                         (3, "up\n", "warn\n"))
        self.assertEqual(job.run_tool(py("print(input()[::-1])"), "6- roolf\n"), (0, "floor -6\n", ""))

    def test_timeout(self):
        self.assertEqual(job.run_or_timeout(py("print('fast')"), 5), "fast\n")
        start = time.monotonic()
        self.assertEqual(job.run_or_timeout(py("import time; time.sleep(10)"), 0.3), "TIMEOUT")
        self.assertLess(time.monotonic() - start, 5)

    def test_checked(self):
        self.assertEqual(job.checked_output(py("print('ok')")), "ok\n")
        with self.assertRaises(subprocess.CalledProcessError):
            job.checked_output(py("raise SystemExit(3)"))

    def test_pipe(self):
        out = job.pipe(py("print('c-17'); print('a-02')"),
                       py("import sys; print(''.join(sorted(sys.stdin)).upper(), end='')"))
        self.assertEqual(out, "A-02\nC-17\n")

    def test_live_lines(self):
        gen = job.live_lines(py("import time\nfor i in range(3):\n    print(i, flush=True); time.sleep(0.05)"))
        self.assertEqual(next(gen), "0")
        self.assertEqual(list(gen), ["1", "2"])

    @unittest.skipUnless(POSIX, "signals")
    def test_stop_politely(self):
        polite = subprocess.Popen(py("import time\nwhile True: time.sleep(0.05)"))
        self.addCleanup(polite.wait)
        self.addCleanup(polite.kill)
        time.sleep(0.2)
        self.assertEqual(job.stop_politely(polite, 5), -signal.SIGTERM)
        stubborn = subprocess.Popen(py(
            "import signal, time\nsignal.signal(signal.SIGTERM, signal.SIG_IGN)\n"
            "print('ready', flush=True)\nwhile True: time.sleep(0.05)"), stdout=subprocess.PIPE)
        self.addCleanup(stubborn.wait)
        self.addCleanup(stubborn.kill)
        stubborn.stdout.readline()
        self.assertEqual(job.stop_politely(stubborn, 0.3), -signal.SIGKILL)
        stubborn.stdout.close()


@unittest.skipUnless(POSIX, "Unix-only")
class Unix(unittest.TestCase):
    def test_trap(self):
        log = []
        old = job.trap(signal.SIGUSR1, log)
        try:
            os.kill(os.getpid(), signal.SIGUSR1)
            time.sleep(0.05)
            self.assertEqual(log, ["SIGUSR1"])
        finally:
            signal.signal(signal.SIGUSR1, old)

    def test_errno(self):
        self.assertEqual(job.explain_errno(2), "ENOENT: No such file or directory")

    def test_machine(self):
        r = job.machine_report()
        self.assertEqual(set(r), {"system", "machine", "python"})
        self.assertTrue(r["python"].startswith("3."))

    def test_patch_file(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "hdr.bin"
            p.write_bytes(b"XXXX-rest-of-file")
            job.patch_file(p, 0, b"OURO")
            self.assertEqual(p.read_bytes(), b"OURO-rest-of-file")
            with self.assertRaises(ValueError):
                job.patch_file(p, 15, b"too long")
            self.assertEqual(p.stat().st_size, 17)

    def test_owner(self):
        with tempfile.NamedTemporaryFile() as f:
            user, group = job.owner_and_group(f.name)
        import grp, pwd
        self.assertEqual(user, pwd.getpwuid(os.getuid()).pw_name)
        self.assertEqual(group, grp.getgrgid(os.getgid()).gr_name)

    def test_pipes_and_select(self):
        r, w = job.nonblocking_pipe()
        try:
            with self.assertRaises(BlockingIOError):
                os.read(r, 10)
            self.assertFalse(job.wait_readable(r, 0.05))
            os.write(w, b"ping")
            self.assertTrue(job.wait_readable(r, 1))
            self.assertEqual(os.read(r, 10), b"ping")
        finally:
            os.close(r)
            os.close(w)


if __name__ == "__main__":
    unittest.main()

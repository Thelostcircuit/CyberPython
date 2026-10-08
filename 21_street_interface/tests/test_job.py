import contextlib
import io
import unittest

import job


class Argparse(unittest.TestCase):
    def setUp(self):
        self.p = job.build_parser()

    def test_call(self):
        a = self.p.parse_args(["-vv", "--dry-run", "call", "--floor", "-6"])
        self.assertEqual((a.command, a.floor, a.priority, a.verbose, a.dry_run),
                         ("call", -6, "normal", 2, True))
        self.assertEqual(self.p.prog, "liftctl")

    def test_status(self):
        a = self.p.parse_args(["status", "--json"])
        self.assertEqual((a.command, a.json, a.verbose, a.dry_run), ("status", True, 0, False))

    def test_errors(self):
        for bad in ([], ["call"], ["call", "--floor", "99"], ["call", "--floor", "x"],
                    ["call", "--floor", "1", "--priority", "urgent"], ["fly"]):
            with self.subTest(bad=bad), contextlib.redirect_stderr(io.StringIO()):
                with self.assertRaises(SystemExit):
                    self.p.parse_args(bad)


class OldParsers(unittest.TestCase):
    def test_getopt(self):
        self.assertEqual(job.legacy_opts(["-v", "--floor=3", "go", "now"]),
                         ({"verbose": "yes", "floor": "3"}, ["go", "now"]))
        self.assertEqual(job.legacy_opts(["-f", "7"]), ({"floor": "7"}, []))

    def test_optparse(self):
        self.assertEqual(job.optparse_quiet(["-q", "a", "b"]), (True, ["a", "b"]))
        self.assertEqual(job.optparse_quiet(["x"]), (False, ["x"]))


class Shlex(unittest.TestCase):
    def test_split_join(self):
        self.assertEqual(job.split_line('liftctl call --note "cargo, fragile" x\\ y'),
                         ["liftctl", "call", "--note", "cargo, fragile", "x y"])
        line = job.join_args(["echo", "it's here", "plain"])
        self.assertEqual(job.split_line(line), ["echo", "it's here", "plain"])


class Getpass(unittest.TestCase):
    def test_read_code(self):
        prompts = []

        def fake(p):
            prompts.append(p)
            return "  7734\n"
        self.assertEqual(job.read_code(fake), "7734")
        self.assertEqual(prompts, ["access code: "])
        with self.assertRaises(ValueError):
            job.read_code(lambda p: "   ")


class Shell(unittest.TestCase):
    def run_cmds(self, *lines):
        out = io.StringIO()
        sh = job.LiftShell(stdout=out)
        stopped = [sh.onecmd(l) for l in lines]
        return sh, out.getvalue(), stopped

    def test_session(self):
        sh, out, stopped = self.run_cmds("floor -6", "status", "status json", "floor 99",
                                         "floor up", "dance", "quit")
        self.assertEqual(out, "moving to -6\nfloor -6\n{\"floor\": -6}\nbad floor: 99\n"
                              "bad floor: up\nunknown: dance\nbye\n")
        self.assertEqual(sh.floor, -6)
        self.assertTrue(stopped[-1])
        self.assertFalse(any(stopped[:-1]))
        self.assertEqual(sh.prompt, "lift> ")

    def test_completion(self):
        sh = job.LiftShell(stdout=io.StringIO())
        self.assertEqual(sh.complete_status("j", "status j", 7, 8), ["json"])
        self.assertEqual(sh.complete_status("", "status ", 7, 7), ["json", "brief"])

    def test_help_uses_docstrings(self):
        out = io.StringIO()
        sh = job.LiftShell(stdout=out)
        sh.onecmd("help floor")
        self.assertIn("floor N", out.getvalue())


class Completer(unittest.TestCase):
    def test_make_completer(self):
        c = job.make_completer(["status", "stop", "floor"])
        self.assertEqual([c("st", i) for i in range(3)], ["status", "stop", None])
        self.assertIsNone(c("z", 0))


if __name__ == "__main__":
    unittest.main()

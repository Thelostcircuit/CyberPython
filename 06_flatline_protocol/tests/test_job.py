import unittest

import job


class Hierarchy(unittest.TestCase):
    def test_classes(self):
        for name in ("IceError", "TraceDetected", "MalformedPacket"):
            cls = getattr(job, name)
            self.assertTrue(issubclass(cls, job.DeckError), name)
        self.assertTrue(issubclass(job.DeckError, Exception))
        e = job.IceError("black ice", level=5)
        self.assertEqual(str(e), "black ice")
        self.assertEqual(e.level, 5)


class Parsing(unittest.TestCase):
    def test_safe_int(self):
        self.assertEqual(job.safe_int("42"), 42)
        self.assertIsNone(job.safe_int("\x00ICE"))
        self.assertEqual(job.safe_int(None, default=-1), -1)
        self.assertEqual(job.safe_int([1], 0), 0)

    def test_parse_packet(self):
        self.assertEqual(job.parse_packet("5:hello"), "hello")
        self.assertEqual(job.parse_packet("3:a:b"), "a:b")
        self.assertEqual(job.parse_packet("0:"), "")
        with self.assertRaises(job.MalformedPacket):
            job.parse_packet("hello")
        with self.assertRaises(job.MalformedPacket):
            job.parse_packet("9:short")
        with self.assertRaises(job.MalformedPacket) as ctx:
            job.parse_packet("x:abc")
        self.assertIsInstance(ctx.exception.__cause__, ValueError)

    def test_process(self):
        self.assertEqual(job.process(["2:ok", "junk", "1:y", "5:nope", "q:z"]), (["ok", "y"], 3))
        self.assertEqual(job.process([]), ([], 0))
        with self.assertRaises(AttributeError):
            job.process([None])


class Cleanup(unittest.TestCase):
    def test_guarded_ok(self):
        log = []
        self.assertEqual(job.guarded(log, lambda: 7), 7)
        self.assertEqual(log, ["open", "ok", "close"])

    def test_guarded_error(self):
        log = []
        with self.assertRaises(ZeroDivisionError):
            job.guarded(log, lambda: 1 / 0)
        self.assertEqual(log, ["open", "close"])

    def test_shield(self):
        with job.Shield() as s:
            raise job.IceError("x", 1)
        self.assertEqual(len(s.absorbed), 1)
        self.assertIsInstance(s.absorbed[0], job.IceError)

        with job.Shield() as s2:
            pass
        self.assertEqual(s2.absorbed, [])

        with self.assertRaises(KeyError):
            with job.Shield():
                raise KeyError("not ours")


def ice(n):
    def f():
        raise job.IceError(f"ice{n}", n)
    return f


def trace():
    raise job.TraceDetected("seen")


class Groups(unittest.TestCase):
    def test_run_all_ok(self):
        self.assertEqual(job.run_countermeasures([lambda: 1, lambda: 2]), [1, 2])

    def test_run_collects(self):
        ran = []
        actions = [ice(1), lambda: ran.append("ran"), trace, ice(2)]
        with self.assertRaises(ExceptionGroup) as ctx:
            job.run_countermeasures(actions)
        self.assertEqual(ran, ["ran"])
        group = ctx.exception
        self.assertEqual(len(group.exceptions), 3)
        self.assertIsInstance(group.exceptions[1], job.TraceDetected)

    def test_triage(self):
        actions = [ice(1), trace, ice(2), ice(3)]
        self.assertEqual(job.triage(lambda: job.run_countermeasures(actions)),
                         {"ice": 3, "trace": 1})
        self.assertEqual(job.triage(lambda: None), {"ice": 0, "trace": 0})

    def test_triage_propagates_others(self):
        def boom():
            raise ExceptionGroup("g", [job.IceError("a", 1), OSError("disk")])
        with self.assertRaises(ExceptionGroup) as ctx:
            job.triage(boom)
        self.assertIsInstance(ctx.exception.exceptions[0], OSError)


if __name__ == "__main__":
    unittest.main()

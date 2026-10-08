import dataclasses
import io
import tempfile
import unittest
from pathlib import Path
from typing import TypedDict

import job


class Data(unittest.TestCase):
    def test_subject(self):
        s = job.Subject("OS-ENG-4471", "Iris Vale")
        self.assertEqual((s.rack, s.tags, s.notes), ("UNASSIGNED", [], ""))
        t = job.Subject("OS-FIN-0042", "R. Moss")
        s.tags.append("priority")
        self.assertEqual(t.tags, [])
        self.assertEqual(job.Subject("OS-X-1", "a", notes="one"), job.Subject("OS-X-1", "a", notes="two"))
        self.assertNotIn("notes", repr(s))
        with self.assertRaises(ValueError):
            job.Subject("XX-1", "nope")
        self.assertTrue(dataclasses.is_dataclass(job.Subject))

    def test_rackslot(self):
        a = job.RackSlot.parse("C-17")
        self.assertEqual(a, job.RackSlot("C", 17))
        self.assertEqual(sorted([job.RackSlot("C", 17), job.RackSlot("A", 2), job.RackSlot("C", 3)]),
                         [job.RackSlot("A", 2), job.RackSlot("C", 3), job.RackSlot("C", 17)])
        with self.assertRaises(dataclasses.FrozenInstanceError):
            a.number = 1
        self.assertEqual(len({a, job.RackSlot("C", 17)}), 1)


class Interfaces(unittest.TestCase):
    def test_abc(self):
        with self.assertRaises(TypeError):
            job.Scanner()
        self.assertEqual(job.DoorScanner().scan_all(["3", "7"]), ["door 3: sealed", "door 7: sealed"])

        class Half(job.Scanner):
            pass
        with self.assertRaises(TypeError):
            Half()

    def test_protocol(self):
        closed = []

        class Hatch:
            def close(self):
                closed.append("hatch")

        class Rock:
            pass
        self.assertEqual(job.close_everything([Hatch(), Rock(), io.StringIO(), 5]), 2)
        self.assertEqual(closed, ["hatch"])


class Generics(unittest.TestCase):
    def test_stack(self):
        s = job.Stack[int]()
        self.assertIsNone(s.peek())
        s.push(1)
        s.push(2)
        self.assertEqual((len(s), s.peek(), s.pop(), s.pop(), len(s)), (2, 2, 2, 1, 0))
        with self.assertRaises(IndexError):
            s.pop()
        self.assertEqual(job.Stack.__type_params__[0].__name__, "T")

    def test_first(self):
        self.assertEqual(job.first([3, 4]), 3)
        self.assertIsNone(job.first([]))


class Order(TypedDict):
    subject: str
    rack: str
    priority: int


class Typing(unittest.TestCase):
    def test_typed_dict(self):
        self.assertTrue(job.matches_typed_dict({"subject": "a", "rack": "C-17", "priority": 1}, Order))
        self.assertFalse(job.matches_typed_dict({"subject": "a", "rack": "C-17"}, Order))
        self.assertFalse(job.matches_typed_dict({"subject": "a", "rack": "C-17", "priority": "1"}, Order))
        self.assertFalse(job.matches_typed_dict({"subject": "a", "rack": "C", "priority": 1, "x": 0}, Order))

    def test_status(self):
        self.assertEqual(job.next_status("queued"), "sent")
        self.assertEqual(job.next_status("sent"), "confirmed")
        self.assertEqual(job.next_status("confirmed"), "confirmed")
        with self.assertRaises(ValueError):
            job.next_status("lost")

    def test_hint_strings(self):
        def first_light(seed: CoreSeed, depth: int = 3) -> Mind: ...  # noqa: F821
        self.assertEqual(job.hint_strings(first_light),
                         {"seed": "CoreSeed", "depth": "int", "return": "Mind"})


class ContextTools(unittest.TestCase):
    def test_lockdown(self):
        log = []
        with job.lockdown(log, "vault") as token:
            self.assertEqual(token, "token-vault")
            self.assertEqual(log, ["lock vault"])
        self.assertEqual(log, ["lock vault", "unlock vault"])
        log.clear()
        with self.assertRaises(RuntimeError):
            with job.lockdown(log, "crawl"):
                raise RuntimeError("alarm")
        self.assertEqual(log, ["lock crawl", "unlock crawl"])

    def test_captured(self):
        self.assertEqual(job.captured(lambda: print("gap at", "03:14")), "gap at 03:14\n")

    def test_read_all_and_ignore(self):
        with tempfile.TemporaryDirectory() as d:
            paths = []
            for i, text in enumerate(["a", "bb", "ccc"]):
                p = Path(d) / f"{i}.txt"
                p.write_text(text)
                paths.append(p)
            self.assertEqual(job.read_all(paths), ["a", "bb", "ccc"])
            self.assertFalse(job.ignore_missing(paths[0]))
            self.assertFalse(job.ignore_missing(paths[0]))
            with self.assertRaises(FileNotFoundError):
                job.read_all([paths[1], Path(d) / "missing"])


if __name__ == "__main__":
    unittest.main()

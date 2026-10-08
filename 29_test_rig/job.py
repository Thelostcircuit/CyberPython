"""29 // TEST RIG: put MONTY on the bench."""

import bdb
import cProfile
import pstats
import time
import timeit
import trace
import tracemalloc
import unittest
from typing import Any, Callable
from unittest.mock import Mock, patch


def checksum(text: str) -> int:
    """Position-weighted checksum used by MONTY's core (already written; DON'T change it).

    Each character's ord() is multiplied by its 1-BASED position, the products are summed,
    and the total is taken modulo 997.  checksum("") == 0, checksum("A") == 65,
    checksum("AB") == (65*1 + 66*2) % 997 == 197.
    """
    return sum(i * ord(c) for i, c in enumerate(text, start=1)) % 997


class ChecksumTests(unittest.TestCase):
    """Your tests for checksum. Call it ONLY as self.func(...). The deck swaps in buggy
    versions to check that your tests notice. Hint: think about what each kind of bug in the
    docstring's rules would break (the weights, the 1-based start, the modulo)."""

    func = staticmethod(checksum)

    pass  # TODO: write test_ methods


def stamp() -> str:
    """Already written: the current time as whole seconds."""
    return f"{time.time():.0f}"


def frozen_stamp(value: float) -> str:
    """Return stamp() while time.time is patched to return `value`."""
    raise NotImplementedError("TODO")


def fake_door() -> Mock:
    """A Mock where .status == "sealed", the first .open() call returns True, and the second
    raises PermissionError("locked out")."""
    raise NotImplementedError("TODO")


def spy_on(obj: Any, method: str, *args: Any) -> tuple[Any, int]:
    """Inside patch.object(obj, method, wraps=<the real method>), call getattr(obj, method)(*args)
    twice. Return (the result of the second call, the spy's call_count)."""
    raise NotImplementedError("TODO")


def rack_number(slot: str) -> int:
    """The number part of a rack slot like "C-17".

    TODO: write at least THREE doctest examples here, including one showing the ValueError for a slot without a dash.
    """
    raise NotImplementedError("TODO")


def best_time(func: Callable[[], Any], number: int) -> float:
    """min(timeit.repeat(func, number=number, repeat=3))"""
    raise NotImplementedError("TODO")


def hottest(func: Callable[[], Any]) -> str:
    """Profile func() with cProfile.Profile().runcall, load pstats.Stats, and return the
    function NAME with the largest tottime. (Stats(...).stats maps
    (filename, lineno, funcname) -> (cc, nc, tottime, cumtime, callers).)"""
    raise NotImplementedError("TODO")


def lines_run(func: Callable[[], Any]) -> list[int]:
    """Run func with trace.Trace(count=1, trace=0).runfunc. Return the sorted line numbers
    recorded in func's own file (func.__code__.co_filename) between its first line and the
    last line of its code (use func.__code__.co_firstlineno and the max line from
    func.__code__.co_lines())."""
    raise NotImplementedError("TODO")


def peak_bytes(func: Callable[[], Any]) -> int:
    """tracemalloc.start(), run func, read the PEAK from get_traced_memory(), stop, return it."""
    raise NotImplementedError("TODO")


class LineRecorder(bdb.Bdb):
    """A tiny debugger. LineRecorder("target").runcall(fn, *args) runs fn under the debugger,
    appending frame.f_lineno to self.lines every time a line executes in a function whose
    code name is "target". runcall returns fn's result."""

    def __init__(self, target: str):
        super().__init__()
        self.target = target
        self.lines: list[int] = []

    pass  # TODO: override user_line

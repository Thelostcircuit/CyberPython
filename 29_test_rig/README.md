# 29 // TEST RIG

```
[MONTY] self-test coverage: 11% ── known bugs: ? ── BASILISK's knowledge of my bugs: probably 100%
```

**Modules:** `unittest`, `unittest.mock`, `doctest`, `pdb`, `bdb`, `timeit`, `cProfile`, `profile`, `pstats`, `trace`, `tracemalloc`

If BASILISK is built on MONTY's design, then BASILISK knows MONTY's weak spots. The only
defence is to find them first. Sable sets up a **test rig**: a bench where every part of MONTY
gets tested, measured, profiled and stepped through line by line.

> **SABLE:** On the security floor we had a saying: *untested code is just a rumour*.
>
> **MONTY:** A good saying. Python has a full testing workshop built in: `unittest` (which
> you've been running every chapter, by the way), mocks to fake the parts you can't control,
> doctests that keep examples honest, timers, profilers, memory tracers, and a debugger you
> can drive from code. Let's put me on the bench.

---

## ▓ TECH BRIEFING

### `unittest`

```python
import unittest
class RackTests(unittest.TestCase):
    def setUp(self): ...                      # before each test (tearDown after; setUpClass once)
    def test_parse(self):                     # methods starting with test_ are tests
        self.assertEqual(parse("C-17"), ("C", 17))
        self.assertTrue(x); self.assertIn(a, b); self.assertIsNone(x)
        self.assertAlmostEqual(0.1 + 0.2, 0.3)
        with self.assertRaises(ValueError): parse("junk")
        for s in ["A-1", "Z-99"]:
            with self.subTest(s=s):           # each case reported separately
                self.assertTrue(valid(s))
    @unittest.skipIf(cond, "why")
    def test_unix_only(self): ...

unittest.main()                               # or: python -m unittest -v
```

Running a test class from code: `unittest.TestLoader().loadTestsFromTestCase(Cls)`, then
`unittest.TextTestRunner().run(suite)` returns a result with `.wasSuccessful()`, `.failures`
and `.errors`. `IsolatedAsyncioTestCase` tests async code (you used it in ch 24).

### `unittest.mock`: fakes

```python
from unittest.mock import Mock, MagicMock, patch, call

door = Mock()
door.open.return_value = True
door.open()                                   # True
door.open.assert_called_once()
door.lock.side_effect = PermissionError       # raise when called
door.read.side_effect = [1, 2, StopIteration] # successive results
door.mock_calls, door.open.call_count, door.open.call_args

with patch("time.time", return_value=0):     # replace a name WHERE IT IS LOOKED UP
    ...
with patch.object(obj, "method", wraps=obj.method) as spy:   # real behaviour, recorded calls
    ...
Mock(spec=RealClass)                          # only allows attributes RealClass really has
```

### `doctest`: examples that are tests

```python
def rack_number(slot):
    """
    >>> rack_number("C-17")
    17
    """
```

`python -m doctest -v module.py`, `doctest.testmod()`, or load them into unittest with
`doctest.DocTestSuite`.

### Timing and profiling

```python
import timeit
timeit.timeit("sum(range(100))", number=10_000)
min(timeit.repeat(func, number=100, repeat=5))       # take the MIN: least noise

import cProfile, pstats
prof = cProfile.Profile()
prof.runcall(workload)                                # or: with cProfile.Profile() as prof:
stats = pstats.Stats(prof).sort_stats("tottime"); stats.print_stats(5)
# `python -m cProfile -s tottime script.py` does it from the shell
```

`tottime` is time spent *inside* a function. `cumtime` also includes its callees. `profile`
is the pure-Python version of `cProfile` (slower, but extensible).

### `trace` and `tracemalloc`

```python
import trace
t = trace.Trace(count=1, trace=0); t.runfunc(func)
t.results().counts                        # {(filename, lineno): times_executed}  (line coverage)

import tracemalloc
tracemalloc.start()
...
current, peak = tracemalloc.get_traced_memory()
tracemalloc.take_snapshot().statistics("lineno")[:5]   # the lines that allocated the most
tracemalloc.stop()
```

### Debuggers: `pdb` and `bdb`

Put `breakpoint()` anywhere to drop into **pdb**: `n` (next), `s` (step into), `c` (continue),
`p expr`, `pp expr`, `l` (list), `w` (where), `b 42` (break at line 42), `q`.
`python -m pdb script.py` starts a script under the debugger, and `pdb.pm()` inspects the last
crash post-mortem.

`bdb` is the framework pdb is built on. Subclass `bdb.Bdb`, override `user_line(frame)`, and
you have your own programmable debugger. `frame.f_lineno`, `frame.f_code.co_name` and
`frame.f_locals` tell you where you are.

---

## ▓ THE JOB

In `job.py`:

1. **`ChecksumTests`**: write your *own* `unittest.TestCase` for the provided `checksum`. The deck runs it against the real function (it must pass) and against three buggy **mutants** (each must fail). Always call the function under test as `self.func(...)`.
2. **`frozen_stamp(value)`**: `patch` `time.time` so that `stamp()` returns a fixed value.
3. **`fake_door()`**: a `Mock` whose `open()` succeeds once and then raises `PermissionError`, with a `status` of `"sealed"`.
4. **`spy_on(obj, method, *args)`**: call a method through `patch.object(..., wraps=...)` and return `(result, call_count)`.
5. **`rack_number`**: write a docstring with at least **three** doctest examples that pass.
6. **`best_time(func, number)`**: the minimum of `timeit.repeat`.
7. **`hottest(func)`**: profile `func` with `cProfile` and return the name of the function with the most `tottime`.
8. **`lines_run(func)`**: the sorted line numbers `trace` saw execute inside `func`.
9. **`peak_bytes(func)`**: the peak memory while `func` runs, from `tracemalloc`.
10. **`LineRecorder`**: a `bdb.Bdb` that records each line number executed in a named function.

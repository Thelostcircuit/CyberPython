# HINTS // 29 TEST RIG

## ChecksumTests
<details><summary>Hint 1: which bugs?</summary>

The deck tries three plausible bugs: forgetting the position weights, counting positions from
0 instead of 1, and forgetting `% 997`. Write at least one test that *each* of those would
fail.
</details>
<details><summary>Hint 2</summary>

`self.func("A") == 65` catches the 0-based bug (0 × 65 = 0). `self.func("AB") == 197` catches
the missing weights. A long input like `"Z" * 100` has a raw sum far above 997, so assert the
result is `< 997`.
</details>

## frozen_stamp
<details><summary>Hint</summary>

`with patch("time.time", return_value=value): return stamp()`. `stamp` looks up `time.time`
through the `time` module each call, so patching the module attribute works.
</details>

## fake_door
<details><summary>Hint</summary>

`door.open.side_effect = [True, PermissionError("locked out")]`. A list side effect returns
(or raises, for exceptions) one item per call.
</details>

## spy_on
<details><summary>Hint</summary>

`real = getattr(obj, method)`, then `with patch.object(obj, method, wraps=real) as spy:`,
call it twice, and return `(result, spy.call_count)`.
</details>

## rack_number
<details><summary>Hint</summary>

Doctest examples are `>>> call` lines followed by the exact expected output. For an exception,
the expected output starts with `Traceback (most recent call last):`, then `...`, then the
final `ValueError: ...` line.
</details>

## hottest
<details><summary>Hint</summary>

`prof = cProfile.Profile(); prof.runcall(func); stats = pstats.Stats(prof).stats`.
`max(stats.items(), key=lambda kv: kv[1][2])` picks the biggest tottime, and the name is the
key's third element.
</details>

## lines_run
<details><summary>Hint</summary>

`t = trace.Trace(count=1, trace=0); t.runfunc(func)`. `t.results().counts` is keyed by
`(filename, lineno)`. Keep the lines that are in `func`'s file and within its line range.
</details>

## peak_bytes / LineRecorder
<details><summary>Hint</summary>

`tracemalloc.get_traced_memory()` returns `(current, peak)`. Always `stop()` in a `finally`.
For the recorder, `def user_line(self, frame):` appends `frame.f_lineno` when
`frame.f_code.co_name == self.target`. `runcall` handles the rest.
</details>

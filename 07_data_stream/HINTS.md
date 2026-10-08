# HINTS // 07 DATA STREAM

## Task 1: Countdown
<details><summary>Hint</summary>

`__iter__` returns `self`. `__next__` raises `StopIteration` when `self.n <= 0`. Otherwise it
decrements and returns the value it had *before* decrementing.
</details>

## Task 3: chunked
<details><summary>Hint</summary>

Build up a list. When it reaches `size`, `yield` it and start a new one. After the loop,
yield what's left **if** it's non-empty.
</details>

## Task 4: flatten
<details><summary>Hint</summary>

`if isinstance(item, (list, tuple)): yield from flatten(item)` / `else: yield item`.
</details>

## Task 5: take
<details><summary>Hint</summary>

Loop over the iterable, append, and `break` as soon as you have `n` items. Checking the length
*after* appending means you never pull an extra item. Handle `n <= 0` before the loop.
</details>

## Task 6: windows
<details><summary>Hint</summary>

Keep a list of the most recent items. Append each new item, `pop(0)` when it grows past `n`,
and yield `tuple(window)` whenever its length equals `n`. (Ch 11's `collections.deque(maxlen=n)`
does the popping for you.)
</details>

## Task 7: interleave
<details><summary>Hint</summary>

Turn everything into iterators with `iter()`. Loop over the list of live iterators, calling
`next()` on each. The ones that raise `StopIteration` get dropped. Keep going while any are
left.
</details>

## Task 8: Tap
<details><summary>Hint</summary>

`__iter__` increments `self.passes` and returns a *fresh* iterator: `iter(self.source)`.
Don't return `self`. If you do, a nested loop over the same Tap breaks.
</details>

## Task 9: running_max
<details><summary>Hint</summary>

```python
best = None
while True:
    x = yield best
    ...update best...
```
</details>

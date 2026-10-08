# HINTS // 13 CHROME TOOLKIT

## codes
<details><summary>Hint</summary>

`itertools.product(digits, repeat=length)` yields tuples of characters. `"".join` each one.
</details>

## rle
<details><summary>Hint</summary>

`groupby(text)` yields `(key, group_iterator)`. The group has no `len()`, so count it with
`sum(1 for _ in grp)` or `len(list(grp))`.
</details>

## deltas / until_alarm
<details><summary>Hint</summary>

`[b - a for a, b in itertools.pairwise(xs)]` and
`list(itertools.takewhile(lambda e: e != "ALARM", events))`.
</details>

## assign_shifts
<details><summary>Hint</summary>

`zip(tasks, itertools.cycle(crew))` pairs each task with the next crew member, wrapping
forever. `zip` stops when the tasks run out. Pre-fill the dict with `{c: [] for c in crew}`.
</details>

## ways_to_climb
<details><summary>Hint</summary>

Base case `n < 2 → 1`, otherwise `ways(n-1) + ways(n-2)`. `@cache` makes this linear
instead of exponential.
</details>

## hex_reader / product_of
<details><summary>Hint</summary>

`functools.partial(int, base=16)` and `functools.reduce(operator.mul, xs, 1)`.
</details>

## describe
<details><summary>Hint</summary>

```python
@describe.register
def _(x: int) -> str:
    return f"int:{x}"
```
`singledispatch` reads the type annotation of the first parameter.
</details>

## Clearance / Dossier
<details><summary>Hint</summary>

Put `@functools.total_ordering` above `class Clearance`, and write `__eq__` and `__lt__`
comparing `self.level`. For the Dossier, `@functools.cached_property` goes above
`def summary(self)`.
</details>

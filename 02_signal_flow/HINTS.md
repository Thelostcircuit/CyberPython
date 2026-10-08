# HINTS // 02 SIGNAL FLOW

## Task 2: countdown
<details><summary>Hint</summary>

Start with `out = ""`. While `n > 0`: `out += f"{n}.."` and `n -= 1`. Then return `out + "GO"`.
</details>

## Task 3: patrol_path
<details><summary>Hint</summary>

The i-th position is `(start + i * step) % grid`. Loop `i` over `range(count)` and append.
(Or read ahead to ch 03: that's a one-line list comprehension.)
</details>

## Task 4: first_blind_spot
<details><summary>Hint</summary>

```python
for i, c in enumerate(coverage):
    if c == 0:
        return i        # returning from inside the loop is fine too...
else:
    return -1           # ...the else runs only if we never broke/returned out
```
</details>

## Task 5: scan_code
<details><summary>Hint</summary>

Build a string: add `"SCAN"` if divisible by 3, add `"LOCK"` if divisible by 5. Then
`return out or str(n)`, because an empty string is falsy.
</details>

## Task 6: longest_quiet
<details><summary>Hint</summary>

Keep two counters, `run` and `best`. `continue` past `None`. Below threshold: `run += 1`
and update `best`. Otherwise reset `run = 0`.
</details>

## Task 7: walk
<details><summary>Hint 1</summary>

Keep a dict of direction → `(dx, dy)`: `{"north": (0, 1), ...}`.
</details>
<details><summary>Hint 2</summary>

```python
match command.split():
    case ["go", direction]:
        steps = 1
    case ["go", direction, n]:
        steps = int(n)
    case ["jump", nx, ny]:
        ...
    case ["wait"] | ["hide"]:
        continue
    case _:
        raise ValueError(command)
```
</details>

## Task 8: drone_response
<details><summary>Hint</summary>

Mapping patterns look like `case {"type": "scan", "hit": True}:`. Put a guard on the patrol
case: `case {"type": "patrol", "id": drone_id} if drone_id.startswith("W"):`. For the zone:
`case {"type": "alarm", "zone": 1 | 2 | 3 as zone}:`. Order matters: the first match wins.
</details>

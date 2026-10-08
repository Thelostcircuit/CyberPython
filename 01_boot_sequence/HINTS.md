# HINTS // 01 BOOT SEQUENCE

## Task 1: cell_voltage
<details><summary>Hint</summary>

`/` always gives a float. `round(x, 2)` rounds to 2 places.
</details>

## Task 2: split_credits
<details><summary>Hint</summary>

`//` and `%`, or the built-in `divmod(total, crew)`, which already returns a tuple.
</details>

## Task 3: is_safe_level
<details><summary>Hint</summary>

`return 20 <= level <= 95`. A comparison already *is* a bool, so you don't need `if ... return True`.
</details>

## Task 4: callsign
<details><summary>Hint</summary>

`.strip()`, `.upper()`, `.capitalize()`, glued together with an f-string: `f"{a}, {b}"`.
</details>

## Task 5: status_line
<details><summary>Hint 1</summary>

Three format specs: `:<8`, `:>3` and `:6.1f`.
</details>
<details><summary>Hint 2</summary>

`f"{name:<8}|{level:>3}%|{temp:6.1f}C"`
</details>

## Task 6: parse_reading
<details><summary>Hint</summary>

Strip, normalise the case with `.upper()`, then `.removesuffix("C")`. `float()` doesn't mind
trailing spaces, so `"36.6 "` converts fine.
</details>

## Task 7: mask_card
<details><summary>Hint</summary>

`"*" * n` repeats a string. `number[-4:]` is the last four characters. Repeating a string a
negative number of times gives `""`, so `max(..., 0)` isn't even strictly needed.
</details>

## Task 8: signal_label
<details><summary>Hint</summary>

Check `strength is None` **first**, because `None < 30` raises a `TypeError`. Then use
`if/elif/else`, and build the result with an f-string.
</details>

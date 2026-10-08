# HINTS // 08 MONTY'S TOOLKIT

## Task 2: rot
<details><summary>Hint</summary>

For a lowercase letter: `chr((ord(ch) - ord("a") + k) % 26 + ord("a"))`. Do the same with
`"A"` for uppercase. Python's `%` always returns a non-negative result for a positive modulus,
so negative `k` just works.
</details>

## Task 3: xor_bytes
<details><summary>Hint</summary>

Iterating over `bytes` gives ints. `bytes(b ^ key[i % len(key)] for i, b in enumerate(data))`
</details>

## Task 4: patch_in_place
<details><summary>Hint</summary>

Work out how many bytes fit: `n = max(0, min(len(patch), len(buf) - offset))`. Then
`memoryview(buf)[offset:offset + n] = patch[:n]`. A memoryview slice assignment has to be the
same length, which is why you trim first.
</details>

## Task 5: public_api
<details><summary>Hint</summary>

A dict comprehension over `dir(obj)`, filtered with `not name.startswith("_")`, using
`callable(getattr(obj, name))` to choose the label.
</details>

## Task 6: dispatch
<details><summary>Hint</summary>

`getattr(obj, command, None)` returns `None` when the attribute is missing. Then
`if not callable(method): raise AttributeError(...)`.
</details>

## Task 7: load_attr
<details><summary>Hint</summary>

`module_name, _, attr = spec.partition(":")`, then
`getattr(importlib.import_module(module_name), attr)`.
</details>

## Task 8: main
<details><summary>Hint</summary>

At the very bottom of the file, with no indentation:
```python
if __name__ == "__main__":
    main()
```
</details>

# HINTS // 04 GHOST FUNCTIONS

## Task 2: make_payload
<details><summary>Hint</summary>

Put a bare `*` in the signature: `def make_payload(target, *, retries=3, stealth=False):`
</details>

## Task 3: build_request
<details><summary>Hint 1</summary>

The signature is `def build_request(method, /, **headers):`. The `/` makes everything before it
positional-only, which is why a header named `method` can still land in `headers`.
</details>
<details><summary>Hint 2</summary>

`";".join(f"{k}={v}" for k, v in sorted(headers.items()))`
</details>

## Task 4: tag_target
<details><summary>Hint</summary>

Default to `None`, then build a new list: `list(tags or []) + [name]`.
</details>

## Task 5: make_counter
<details><summary>Hint</summary>

```python
n = start
def counter():
    nonlocal n
    n += 1
    return n
return counter
```
</details>

## Task 6: pipeline
<details><summary>Hint</summary>

Return an inner function `run(x)` that loops `for f in funcs: x = f(x)` and returns `x`.
`funcs` is a closure variable.
</details>

## Task 7: log_calls
<details><summary>Hint</summary>

Define `wrapper(*args, **kwargs)`, decorate it with `@functools.wraps(func)`, set
`wrapper.calls = []` **after** defining it, then return it. Inside, append `(args, kwargs)`.
</details>

## Task 8: retry
<details><summary>Hint 1</summary>

Three layers: `retry(times)` returns `decorator(func)`, which returns `wrapper(*args, **kwargs)`.
</details>
<details><summary>Hint 2</summary>

```python
for attempt in range(times):
    try:
        return func(*args, **kwargs)
    except Exception:
        if attempt == times - 1:
            raise          # bare raise re-raises the exception being handled
```
</details>

## Task 9: depth
<details><summary>Hint</summary>

Base case: not a list → 0. Otherwise `1 + max(depth(x) for x in nested)`, and pass
`default=0` to `max` so empty lists work.
</details>

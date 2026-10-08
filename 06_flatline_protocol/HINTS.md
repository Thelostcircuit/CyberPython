# HINTS // 06 FLATLINE PROTOCOL

## Task 1: the hierarchy
<details><summary>Hint</summary>

```python
class DeckError(Exception):
    pass

class IceError(DeckError):
    def __init__(self, message, level):
        super().__init__(message)
        self.level = level
```
The other two need nothing but `pass`.
</details>

## Task 3: parse_packet
<details><summary>Hint 1</summary>

`length_text, sep, data = raw.partition(":")` splits on the first `:` only. `sep` is `""`
if there wasn't one.
</details>
<details><summary>Hint 2</summary>

```python
try:
    length = int(length_text)
except ValueError as err:
    raise MalformedPacket(...) from err
```
</details>

## Task 4: process
<details><summary>Hint</summary>

`try: data = parse_packet(p)` / `except MalformedPacket: bad += 1` / `else: good.append(data)`.
Don't catch anything broader. The test feeds it `None` and expects the `AttributeError` to
escape.
</details>

## Task 5: guarded
<details><summary>Hint</summary>

Put the `return` inside the `try` and the `log.append("close")` in `finally`. `finally` runs
on the way out, whether that's a return or an exception.
</details>

## Task 6: Shield
<details><summary>Hint</summary>

`__exit__(self, exc_type, exc, tb)`: if `isinstance(exc, DeckError)`, append it and
`return True`. Otherwise return `False` (or `None`). `isinstance(None, DeckError)` is simply
False, so the success case is handled too.
</details>

## Task 7: run_countermeasures
<details><summary>Hint</summary>

Two lists, `results` and `errors`. Wrap each call in `try/except Exception as e`. At the end,
`if errors: raise ExceptionGroup("countermeasures", errors)`.
</details>

## Task 8: triage
<details><summary>Hint</summary>

```python
try:
    func()
except* IceError as group:
    counts["ice"] = len(group.exceptions)
except* TraceDetected as group:
    ...
```
</details>

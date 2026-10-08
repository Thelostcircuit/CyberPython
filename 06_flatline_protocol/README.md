# 06 // FLATLINE PROTOCOL

```
[PYTHIA-9] SIMULATION MODE ── target: BASILISK countermeasure replay ── neural link: DAMPED
```

Sable knows what BASILISK's countermeasures look like, because she used to watch them work
from the Ouroboros security floor. She recorded some. Now she's playing them back at your
deck in a sandbox, with the neural link turned down to a tingle.

The first replay hits, and MONTY's screen goes red:

```
Traceback (most recent call last):
  File "<deck>", line 1, in <module>
ValueError: invalid literal for int() with base 10: '\x00\x00ICE'
```

The link tingles. At full power, that would have been your spinal cord.

> **SABLE:** That's the whole trick. BASILISK doesn't need to hack you. It just sends
> garbage your code didn't expect. Your deck throws, nothing catches it, and the deck dies
> with you plugged in.
>
> **MONTY:** Which is why I don't intend to let anything go uncaught. Errors in Python are
> **exceptions**: objects that fly up the call stack until something catches them. Catch the
> ones you can handle, let the rest go to someone who can, and *always* clean up after
> yourself. That's how you survive BASILISK.

---

## ▓ TECH BRIEFING

### try / except / else / finally

```python
try:
    value = int(raw)
except ValueError:                 # catch one type...
    value = 0
except (TypeError, KeyError) as e: # ...or several; `as e` binds the exception object
    print("bad:", e)
    raise                          # bare raise: re-raise the current exception
else:
    print("runs only if NO exception happened")
finally:
    print("runs ALWAYS: success, exception, even return/break")
```

Catch **specific** exceptions. A bare `except:` or `except Exception:` swallows bugs, so only
use it at a top level that logs or re-raises.

### The built-in hierarchy (the parts you'll meet most)

```
BaseException
 ├── KeyboardInterrupt, SystemExit, GeneratorExit    ← not bugs; don't catch these casually
 └── Exception
      ├── ArithmeticError → ZeroDivisionError, OverflowError
      ├── LookupError → KeyError, IndexError
      ├── ValueError → UnicodeError ...
      ├── TypeError, NameError, AttributeError, AssertionError
      ├── OSError → FileNotFoundError, PermissionError, TimeoutError, ConnectionError ...
      ├── RuntimeError → RecursionError, NotImplementedError
      ├── StopIteration, ImportError → ModuleNotFoundError
      └── ExceptionGroup (also derives from BaseExceptionGroup)
```

`except LookupError` catches both `KeyError` and `IndexError`: an except clause matches
subclasses too.

### Raising and custom exceptions

```python
class DeckError(Exception):
    """Base class for everything our deck raises."""

class IceError(DeckError):
    def __init__(self, message: str, level: int):
        super().__init__(message)          # sets str(e) and e.args
        self.level = level

raise IceError("black ice", level=5)
```

Give your library one base exception, so callers can catch all of it at once.

### Chaining

```python
try:
    n = int(text)
except ValueError as err:
    raise MalformedPacket(f"bad length: {text!r}") from err   # sets __cause__
```

The traceback then shows both errors: *"The above exception was the direct cause of..."*.
`raise X from None` hides the original. Raising inside an `except` without `from` sets
`__context__` instead.

`e.add_note("extra context")` attaches notes that print under the traceback (3.11+).

### Exception groups and except*

When several independent things fail at once (think parallel tasks), raise them together:

```python
errors = [IceError("a", 1), TimeoutError("b")]
raise ExceptionGroup("countermeasures", errors)

try:
    ...
except* IceError as group:        # handles ONLY the IceErrors inside the group
    print(len(group.exceptions))
except* TimeoutError:             # ...and separately the TimeoutErrors
    ...
```

Each `except*` clause receives a (smaller) group. Anything left unhandled is re-raised.

### Context managers: `with`

`with` guarantees setup and teardown, like a reusable `try/finally`:

```python
with open("log.txt") as f:        # f.close() happens even if the block raises
    data = f.read()
```

Write your own with `__enter__` and `__exit__`:

```python
class Shield:
    def __enter__(self):
        return self                               # bound to the `as` name
    def __exit__(self, exc_type, exc, tb):
        # called with (None, None, None) on success, or the exception details
        return isinstance(exc, DeckError)         # returning True SUPPRESSES the exception
```

`contextlib` (ch 28) makes this even shorter with `@contextmanager`.

### assert

`assert condition, "message"` raises `AssertionError` if the condition is false. It's for
catching *your own* bugs, not for validating input, because `python -O` strips asserts out.

### EAFP vs LBYL

Pythonic code is often "Easier to Ask Forgiveness than Permission": try it and catch the
failure, rather than checking every precondition first (`if key in d: ...`).

---

## ▓ THE JOB

In `job.py`:

1. Build the hierarchy: **`DeckError`** → **`IceError`** (it carries a `level`),
   **`TraceDetected`** and **`MalformedPacket`**.
2. **`safe_int(raw, default=None)`**: `int(raw)`, or `default` if that raises `ValueError` or `TypeError`.
3. **`parse_packet(raw)`**: parse `"LEN:DATA"`. Raise `MalformedPacket` **chained from** the original error when the length isn't a number, and when the length doesn't match.
4. **`process(packets)`**: parse them all, and return `(good_data, bad_count)`. Use `try/except/else`.
5. **`guarded(log, action)`**: append `"open"`, run `action()`, append `"ok"` on success, and **always** append `"close"`. Don't swallow the exception.
6. **`Shield`**: a context manager that absorbs `DeckError`s (and records them in `.absorbed`) but lets anything else through.
7. **`run_countermeasures(actions)`**: run every action and collect the failures. If any fail, raise one `ExceptionGroup` containing them all.
8. **`triage(func)`**: call `func()` and use `except*` to count how many `IceError`s and `TraceDetected`s were in the group.

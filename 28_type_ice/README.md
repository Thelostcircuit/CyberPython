# 28 // TYPE ICE

```
[MONTY] self-inspection ── locked region: /core/first_light ── visible: type signatures only
```

**Modules:** `typing`, `dataclasses`, `abc`, `contextlib`, `annotationlib`, `__future__`

The locked part of MONTY's code is called `first_light`. Its body is encrypted, but its
*signatures* aren't: the names of its functions and classes, and the declared types of every
argument and return value. Sable is right. A well-typed interface tells you what code does
without showing you how.

> **MONTY:** Python is dynamically typed. Nothing *enforces* these annotations at runtime. But
> type hints are documentation that tools can check (mypy, pyright, your editor), and the
> standard library has serious machinery built on them: `dataclasses` writes your boilerplate
> from annotations, `abc` defines interfaces, `typing` describes shapes. And `contextlib` makes
> the `with` statement a joy.

---

## ▓ TECH BRIEFING

### `typing`: describing shapes

```python
def scan(target: str, retries: int = 3) -> bool: ...
x: list[int]; d: dict[str, list[str]]; t: tuple[int, ...]; opt: str | None
from typing import Any, Literal, Final, TypedDict, Protocol, NamedTuple, NewType, \
    Callable, Iterator, Self, TypeGuard, overload, assert_never, get_type_hints, cast

Status = Literal["queued", "sent", "confirmed"]
MAX_RACKS: Final = 64
SubjectId = NewType("SubjectId", str)          # a distinct type for checkers; plain str at runtime

class Order(TypedDict):                        # the shape of a dict
    subject: str
    rack: str

class Closable(Protocol):                      # structural typing: anything WITH .close() fits
    def close(self) -> None: ...
# add @runtime_checkable to allow isinstance() checks against a Protocol

type Pair[T] = tuple[T, T]                     # a type alias (3.12+)
class Stack[T]:                                # a generic class (3.12+ syntax)
    def push(self, item: T) -> None: ...
def first[T](xs: list[T]) -> T | None: ...     # a generic function
```

`typing.get_type_hints(obj)` resolves annotations to real objects. `typing.reveal_type`
asks the checker what it thinks. `if TYPE_CHECKING:` guards imports only a checker needs.

### Annotations at runtime: `annotationlib` (3.14) and `__future__`

In 3.14, annotations are evaluated **lazily**: only when something asks for them (PEP 649/749).
So a hint can mention a name that doesn't exist yet:

```python
import annotationlib
def f(x: NotDefinedYet) -> int: ...
annotationlib.get_annotations(f, format=annotationlib.Format.STRING)      # {'x': 'NotDefinedYet', 'return': 'int'}
annotationlib.get_annotations(f, format=annotationlib.Format.FORWARDREF)  # unresolved names become ForwardRef
annotationlib.get_annotations(f)                                          # VALUE: raises NameError here
```

`from __future__ import annotations` was the older way to get lazy annotations: it turns them
into strings. `__future__` holds these feature flags, which let old Pythons opt in to future
behaviour one module at a time.

### `dataclasses`

```python
from dataclasses import dataclass, field, asdict, astuple, replace, fields, KW_ONLY

@dataclass
class Subject:
    id: str
    name: str
    rack: str = "UNASSIGNED"
    tags: list[str] = field(default_factory=list)       # NEVER a bare mutable default
    notes: str = field(default="", compare=False, repr=False)

    def __post_init__(self):                            # validation after the generated __init__
        if not self.id.startswith("OS-"):
            raise ValueError(self.id)

@dataclass(frozen=True, order=True, slots=True)       # immutable, sortable, compact
class RackSlot:
    wing: str
    number: int

asdict(s), replace(s, rack="C-17"), fields(Subject)
```

`@dataclass` writes `__init__`, `__repr__` and `__eq__` (plus ordering, hashing and slots when
asked). `order=True` compares fields as a tuple, in definition order.

### `abc`: abstract base classes

```python
from abc import ABC, abstractmethod
class Scanner(ABC):
    @abstractmethod
    def scan(self, target: str) -> str: ...
    def scan_all(self, targets):                  # concrete methods can use the abstract ones
        return [self.scan(t) for t in targets]

Scanner()          # TypeError: can't instantiate abstract class
```

A subclass is instantiable only once it implements every abstract method.
`Scanner.register(SomeClass)` declares a "virtual subclass" without inheritance.

### `contextlib`

```python
from contextlib import contextmanager, suppress, ExitStack, redirect_stdout, closing, chdir, nullcontext

@contextmanager
def lockdown(log):
    log.append("lock")              # __enter__
    try:
        yield "token"               # the value bound by `as`
    finally:
        log.append("unlock")        # __exit__, even on errors

with suppress(FileNotFoundError): os.remove("tmp")      # ignore specific exceptions
with redirect_stdout(buffer): print("captured")
with ExitStack() as stack:                              # a dynamic number of context managers
    files = [stack.enter_context(open(p)) for p in paths]
with chdir("/tmp"): ...                                 # temporarily change directory
```

`@asynccontextmanager` and `AsyncExitStack` are the async versions. `ContextDecorator`
lets a context manager double as a decorator.

---

## ▓ THE JOB

In `job.py`:

1. **`Subject`**: a dataclass with defaults, a `default_factory`, a field left out of comparisons, and a `__post_init__` check.
2. **`RackSlot`**: a frozen, ordered dataclass with a `parse("C-17")` classmethod.
3. **`Scanner`** (an ABC) and **`DoorScanner`** (a concrete subclass).
4. **`Closable`**: a runtime-checkable `Protocol`, and **`close_everything(objs)`**.
5. **`Stack[T]`** and **`first[T]`**: generics with the 3.12+ syntax.
6. **`matches_typed_dict(data, td)`**: check a dict against a `TypedDict`'s required keys and simple types, using `get_type_hints`.
7. **`next_status(status)`**: move through a `Literal` status workflow.
8. **`hint_strings(obj)`**: annotations as strings, even with undefined names (`annotationlib`).
9. **`lockdown`**: a `@contextmanager`.
10. **`captured(func)`**, **`read_all(paths)`** and **`ignore_missing(path)`**: `redirect_stdout`, `ExitStack` and `suppress`.

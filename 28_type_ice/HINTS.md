# HINTS // 28 TYPE ICE

## Subject
<details><summary>Hint</summary>

```python
@dataclass
class Subject:
    id: str
    name: str
    rack: str = "UNASSIGNED"
    tags: list[str] = field(default_factory=list)
    notes: str = field(default="", compare=False, repr=False)
    def __post_init__(self): ...
```
</details>

## RackSlot
<details><summary>Hint</summary>

`@dataclass(frozen=True, order=True)`. A frozen dataclass is also hashable. For `parse`:
`wing, number = text.split("-")`, then `return cls(wing, int(number))`.
</details>

## Scanner / DoorScanner
<details><summary>Hint</summary>

Decorate `scan` with `@abstractmethod` in `Scanner` (which already inherits from `ABC`).
`DoorScanner` just defines `scan`.
</details>

## Closable / close_everything
<details><summary>Hint</summary>

Put `@runtime_checkable` above `class Closable(Protocol)`. Then `isinstance(obj, Closable)`
checks for a `close` attribute.
</details>

## Stack / first
<details><summary>Hint</summary>

The `[T]` is already in the class header. Just write normal methods over `self._items`.
`pop` should raise `IndexError` on an empty stack.
</details>

## matches_typed_dict
<details><summary>Hint</summary>

`hints = typing.get_type_hints(td)`. The keys must match exactly (`set(data) == set(hints)`),
and every value must pass `isinstance(data[k], t)`.
</details>

## hint_strings
<details><summary>Hint</summary>

`annotationlib.get_annotations(obj, format=annotationlib.Format.STRING)`
</details>

## lockdown
<details><summary>Hint</summary>

`log.append(...)`, then `try: yield token` / `finally: log.append(...)`. Without the
`try/finally`, an exception in the `with` body would skip your cleanup.
</details>

## captured / read_all / ignore_missing
<details><summary>Hint</summary>

`with redirect_stdout(buf): func()`. With `ExitStack`:
`files = [stack.enter_context(open(p, encoding="utf-8")) for p in paths]`.
`with suppress(FileNotFoundError): os.remove(path)`.
</details>

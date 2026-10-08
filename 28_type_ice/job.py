"""28 // TYPE ICE: types, dataclasses, interfaces, and context managers."""

import annotationlib
import io
import os
import typing
from abc import ABC, abstractmethod
from contextlib import ExitStack, contextmanager, redirect_stdout, suppress
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable, Iterator, Literal, Protocol, runtime_checkable

# --- 1. Subject --------------------------------------------------------------------------
# A dataclass with fields, in this order:
#   id: str
#   name: str
#   rack: str = "UNASSIGNED"
#   tags: list[str]  (default: a NEW empty list for every instance)
#   notes: str = ""  (excluded from == comparisons and from repr)
# __post_init__ raises ValueError if id doesn't start with "OS-".
pass  # TODO: the Subject dataclass


# --- 2. RackSlot -------------------------------------------------------------------------
# A frozen, ordered dataclass with fields wing: str and number: int.
# RackSlot.parse("C-17") -> RackSlot("C", 17)   (a classmethod)
pass  # TODO: the RackSlot dataclass


class Scanner(ABC):
    """Abstract: subclasses must implement scan(target) -> str.
    scan_all(targets) returns [self.scan(t) for t in targets]."""

    pass  # TODO: the abstract scan method and the concrete scan_all


class DoorScanner(Scanner):
    """scan(target) -> f"door {target}: sealed" """

    pass  # TODO


# TODO: decorate so isinstance() works against this Protocol
class Closable(Protocol):
    def close(self) -> None: ...


def close_everything(objs: list[Any]) -> int:
    """Call .close() on every object that satisfies the Closable protocol (isinstance check);
    skip the rest. Return how many were closed."""
    raise NotImplementedError("TODO")


class Stack[T]:
    """push(item), pop() -> item (IndexError when empty), peek() -> item or None, len()."""

    def __init__(self) -> None:
        self._items: list[T] = []

    pass  # TODO: push, pop, peek, __len__


def first[T](xs: list[T]) -> T | None:
    """The first item, or None for an empty list."""
    raise NotImplementedError("TODO")


def matches_typed_dict(data: dict, td: type) -> bool:
    """True if data has exactly the keys in td's annotations (get_type_hints(td)), and each value
    is an instance of the annotated type. Only simple classes (str, int, float, bool, list,
    dict) are used as annotations here."""
    raise NotImplementedError("TODO")


Status = Literal["queued", "sent", "confirmed"]


def next_status(status: Status) -> Status:
    """queued -> sent -> confirmed -> confirmed. Anything else -> ValueError."""
    raise NotImplementedError("TODO")


def hint_strings(obj: Any) -> dict[str, str]:
    """obj's annotations as strings, via annotationlib.get_annotations with Format.STRING.
    Must work even when an annotation names something that doesn't exist."""
    raise NotImplementedError("TODO")


@contextmanager
def lockdown(log: list[str], door: str) -> Iterator[str]:
    """Append f"lock {door}", yield f"token-{door}", and ALWAYS append f"unlock {door}" on the
    way out (even if the body raises; don't swallow the exception)."""
    raise NotImplementedError("TODO")


def captured(func: Callable[[], Any]) -> str:
    """Run func() and return everything it printed (contextlib.redirect_stdout)."""
    raise NotImplementedError("TODO")


def read_all(paths: list[str | Path]) -> list[str]:
    """Open every file at once with an ExitStack (all must be open together), then return
    their contents in order. All files are closed afterwards."""
    raise NotImplementedError("TODO")


def ignore_missing(path: str | Path) -> bool:
    """Delete the file, ignoring FileNotFoundError with contextlib.suppress.
    Return whether the file exists afterwards."""
    raise NotImplementedError("TODO")

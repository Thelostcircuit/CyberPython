"""07 // DATA STREAM: read the backbone without drowning in it."""

from typing import Any, Generator, Iterable, Iterator


class Countdown:
    """An ITERATOR (write __iter__ and __next__ yourself, no yield):

    list(Countdown(3)) -> [3, 2, 1];  list(Countdown(0)) -> []
    """

    def __init__(self, start: int):
        self.n = start

    pass  # TODO: __iter__ and __next__


def frames(lines: Iterable[str]) -> Iterator[str]:
    """Yield each line stripped of surrounding whitespace, skipping blank lines and lines
    whose stripped text starts with "#". Must be a generator (lazy)."""
    raise NotImplementedError("TODO")


def chunked(iterable: Iterable[Any], size: int) -> Iterator[list[Any]]:
    """chunked(range(7), 3) yields [0, 1, 2], [3, 4, 5], [6]. Lazy: works on infinite input."""
    raise NotImplementedError("TODO")


def flatten(nested: Iterable[Any]) -> Iterator[Any]:
    """Yield every non-list, non-tuple leaf, depth-first. Strings are leaves.
    flatten([1, [2, (3, [4])], "ab"]) yields 1, 2, 3, 4, "ab"."""
    raise NotImplementedError("TODO")


def take(n: int, iterable: Iterable[Any]) -> list[Any]:
    """The first n items (fewer if the iterable is shorter). Must not consume more than n."""
    raise NotImplementedError("TODO")


def windows(iterable: Iterable[Any], n: int) -> Iterator[tuple]:
    """Sliding windows of width n, as tuples. windows([1,2,3,4], 3) -> (1,2,3), (2,3,4).
    Input shorter than n yields nothing. Lazy."""
    raise NotImplementedError("TODO")


def interleave(*iterables: Iterable[Any]) -> Iterator[Any]:
    """Round robin: interleave("abc", [1, 2], "XYZW") yields a 1 X b 2 Y c Z W."""
    raise NotImplementedError("TODO")


class Tap:
    """A RE-iterable view over `source` (a list). Every `for` over a Tap starts from the
    beginning. `.passes` counts how many times iteration has been started."""

    def __init__(self, source: list[Any]):
        self.source = source
        self.passes = 0

    def __iter__(self) -> Iterator[Any]:
        raise NotImplementedError("TODO")


def running_max() -> Generator[Any, Any, None]:
    """A coroutine-style generator.

    g = running_max()
    next(g)       -> None       (priming: nothing seen yet)
    g.send(3)     -> 3
    g.send(1)     -> 3
    g.send(9)     -> 9
    """
    raise NotImplementedError("TODO")

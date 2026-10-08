"""11 // NIGHT MARKET: keep Mother Adder's books with the right containers."""

import bisect
import copy
import heapq
import types
import weakref
from array import array
from collections import ChainMap, Counter, OrderedDict, defaultdict, deque, namedtuple
from collections.abc import Iterable, Mapping, Sequence, Set
from enum import Flag, auto
from graphlib import CycleError, TopologicalSorter
from typing import Any, Iterator


def best_sellers(sales: list[str], n: int) -> list[tuple[str, int]]:
    """The n most common items with their counts, most common first (Counter.most_common)."""
    raise NotImplementedError("TODO")


def by_stall(pairs: list[tuple[str, str]]) -> dict[str, list[str]]:
    """[(stall, item), ...] -> {stall: [items in order]}. Use a defaultdict; return a plain dict."""
    raise NotImplementedError("TODO")


# Item: a namedtuple with fields name, price, qty, where qty defaults to 1.
Item = None  # TODO


def last_n(events: Iterable[Any], n: int) -> list[Any]:
    """The last n events, oldest first. Use deque(maxlen=n)."""
    raise NotImplementedError("TODO")


class LRU:
    """A least-recently-used cache holding at most `capacity` items.

    get(key, default=None): return the value and mark it most recently used.
    put(key, value): insert/update and mark it most recent. If that makes the cache exceed
      capacity, evict the least recently used item.
    len(cache), `key in cache` (membership does NOT count as a use), and keys() returning a
    list of keys from least to most recently used.
    """

    def __init__(self, capacity: int):
        raise NotImplementedError("TODO")

    pass  # TODO: get, put, __len__, __contains__, keys


def resolve_settings(defaults: dict, env: dict, cli: dict) -> dict:
    """Merge with priority cli > env > defaults, using ChainMap. Return a plain dict."""
    raise NotImplementedError("TODO")


def container_kind(x: Any) -> str:
    """"mapping", "sequence", "set", "iterable", or "other", checked in that order with
    collections.abc. Strings count as sequences."""
    raise NotImplementedError("TODO")


def cheapest(offers: list[Item], k: int) -> list[Item]:
    """The k cheapest offers by price (heapq.nsmallest)."""
    raise NotImplementedError("TODO")


def merge_feeds(*feeds: Iterable[int]) -> Iterator[int]:
    """Lazily merge already-sorted feeds into one sorted stream (heapq.merge)."""
    raise NotImplementedError("TODO")


BAND_CUTOFFS = [10, 100, 1000]
BAND_NAMES = ["scrap", "street", "pro", "corp"]


def price_band(price: float) -> str:
    """< 10 scrap, 10-99.99 street, 100-999.99 pro, >= 1000 corp. Use bisect on BAND_CUTOFFS."""
    raise NotImplementedError("TODO")


def pack(readings: list[int]) -> bytes:
    """Pack signed 16-bit readings into bytes with array("h")."""
    raise NotImplementedError("TODO")


def unpack(data: bytes) -> list[int]:
    """The inverse of pack."""
    raise NotImplementedError("TODO")


def job_order(deps: dict[str, set[str]]) -> list[str] | None:
    """deps maps a job to the jobs that must happen before it. Return a valid order with
    graphlib.TopologicalSorter(...).static_order(), or None if there's a cycle."""
    raise NotImplementedError("TODO")


# Access: a Flag enum with members READ, WRITE, EXEC (use auto()) and ALL = all three.
Access = None  # TODO


def can(granted: "Access", needed: "Access") -> bool:
    """True if `granted` includes every flag in `needed`."""
    raise NotImplementedError("TODO")


def clone_loadout(loadout: dict) -> dict:
    """A fully independent copy (changing nested lists in the copy must not touch the original)."""
    raise NotImplementedError("TODO")


class Registry:
    """Tracks live objects by name WITHOUT keeping them alive (weakref.WeakValueDictionary).

    register(name, obj); get(name) -> obj or None; names() -> sorted list of live names.
    """

    def __init__(self):
        raise NotImplementedError("TODO")

    pass  # TODO: register, get, names


def frozen_view(d: dict) -> Mapping:
    """A read-only live view of d (types.MappingProxyType)."""
    raise NotImplementedError("TODO")

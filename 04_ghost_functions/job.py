"""04 // GHOST FUNCTIONS: build Dex a locker-cracking kit."""

import functools
from typing import Any, Callable


def total_loot(*amounts: float, cut: float = 0.0) -> float:
    """Sum all amounts, remove the crew's `cut` (0.25 = 25%), round to 2 places.

    total_loot(100, 50, cut=0.1) -> 135.0
    """
    raise NotImplementedError("TODO")


def make_payload(target, retries=3, stealth=False):  # TODO: make retries/stealth keyword-only
    """Return {"target": target, "retries": retries, "stealth": stealth}.
    `retries` and `stealth` must be KEYWORD-ONLY: make_payload("x", 5) must raise TypeError."""
    raise NotImplementedError("TODO")


def build_request(method, **headers):  # TODO: make `method` positional-only
    """`method` is POSITIONAL-ONLY, so build_request(method="GET") must raise TypeError.
    (That also means a header may itself be called "method".)

    build_request("get", port=9, host="x") -> "GET host=x;port=9"
    build_request("post")                  -> "POST"
    """
    raise NotImplementedError("TODO")


def tag_target(name, tags=[]):  # TODO: this default is a trap
    """Return a NEW list: the given tags followed by `name`.
    Must not modify the caller's list, and calls must never share state."""
    raise NotImplementedError("TODO")


def make_counter(start: int = 0) -> Callable[[], int]:
    """c = make_counter(10); c() -> 11; c() -> 12. Each counter is independent."""
    raise NotImplementedError("TODO")


def pipeline(*funcs: Callable) -> Callable:
    """pipeline(f, g, h)(x) == h(g(f(x))). With no funcs, return x unchanged."""
    raise NotImplementedError("TODO")


def log_calls(func: Callable) -> Callable:
    """Decorator. The wrapper calls func normally, but first appends (args, kwargs) to a list
    stored at `wrapper.calls`. args is a tuple and kwargs a dict. Use functools.wraps."""
    raise NotImplementedError("TODO")


def retry(times: int) -> Callable:
    """Decorator factory. @retry(3) calls the function up to 3 times in total. Return the first
    successful result. If every attempt raises, re-raise the LAST exception."""
    raise NotImplementedError("TODO")


def depth(nested: Any) -> int:
    """Nesting depth. A non-list is 0, [] is 1, [1, 2] is 1, [1, [2]] is 2, [[[]]] is 3."""
    raise NotImplementedError("TODO")

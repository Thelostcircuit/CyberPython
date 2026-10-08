"""08 // MONTY'S TOOLKIT: the built-ins, bytes, and modules."""

import importlib
from typing import Any


def radix_report(n: int) -> dict[str, str]:
    """radix_report(255) -> {"bin": "0b11111111", "oct": "0o377", "hex": "0xff"}"""
    raise NotImplementedError("TODO")


def rot(text: str, k: int) -> str:
    """Rotate ASCII letters k places through the alphabet, keeping case.
    rot("Iris!", 1) -> "Jsjt!"   rot("abc", -1) -> "zab"   Non-letters are unchanged."""
    raise NotImplementedError("TODO")


def xor_bytes(data: bytes, key: bytes) -> bytes:
    """XOR data[i] with key[i % len(key)]. Return bytes."""
    raise NotImplementedError("TODO")


def patch_in_place(buf: bytearray, offset: int, patch: bytes) -> int:
    """Write `patch` into `buf` starting at `offset`, using a memoryview. Bytes that would fall
    past the end of buf are dropped. Return how many bytes were written."""
    raise NotImplementedError("TODO")


def public_api(obj: Any) -> dict[str, str]:
    """For every name in dir(obj) that doesn't start with "_": "method" if the attribute is
    callable, otherwise "value"."""
    raise NotImplementedError("TODO")


def dispatch(obj: Any, command: str, *args: Any) -> Any:
    """Call obj.<command>(*args) and return the result.
    If command starts with "_", or the attribute is missing or not callable, raise
    AttributeError(f"no command {command!r}")."""
    raise NotImplementedError("TODO")


def load_attr(spec: str) -> Any:
    """"module:attr" -> that attribute. "os.path:join" -> os.path.join.
    Use importlib.import_module and getattr."""
    raise NotImplementedError("TODO")


def main() -> None:
    """Print exactly: PYTHIA-9 // MONTY ONLINE"""
    raise NotImplementedError("TODO")


# TODO: call main() only when this file is run directly

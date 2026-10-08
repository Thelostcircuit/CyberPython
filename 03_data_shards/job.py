"""03 // DATA SHARDS: put Iris's data core back together.

A shard is a tuple: (seq: int, owner: str, text: str, checksum: int)
"""

Shard = tuple[int, str, str, int]


def checksum(text: str) -> int:
    """Sum of ord() of every character, modulo 256."""
    raise NotImplementedError("TODO")


def valid_shards(shards: list[Shard]) -> list[Shard]:
    """The shards whose checksum matches checksum(text), in their original order."""
    raise NotImplementedError("TODO")


def reassemble(shards: list[Shard], owner: str) -> str:
    """Join the text of `owner`'s VALID shards in seq order. If several valid shards share a
    seq, use it only once (they're identical copies)."""
    raise NotImplementedError("TODO")


def owners(shards: list[Shard]) -> list[str]:
    """Sorted list of distinct owners (valid or not)."""
    raise NotImplementedError("TODO")


def index_by_owner(shards: list[Shard]) -> dict[str, list[int]]:
    """owner -> sorted list of distinct seq numbers (valid or not)."""
    raise NotImplementedError("TODO")


def split_packet(packet: list[str]) -> tuple[str, list[str], str]:
    """Use star-unpacking: first item is the header, last is the footer, the rest the body.

    split_packet(["H", "a", "b", "F"]) -> ("H", ["a", "b"], "F")
    """
    raise NotImplementedError("TODO")


def shared_contacts(*contact_lists: list[str]) -> list[str]:
    """Names appearing in EVERY list, sorted. No lists at all -> []."""
    raise NotImplementedError("TODO")


def leaderboard(scores: dict[str, int], n: int) -> list[str]:
    """Top `n` names by score, highest first. Equal scores: alphabetical order."""
    raise NotImplementedError("TODO")


def invert(mapping: dict[str, str]) -> dict[str, str | list[str]]:
    """Swap keys and values. If a value appears once, map it to its key. If it appears more
    than once, map it to the sorted list of all its keys.

    invert({"a": "x", "b": "y", "c": "x"}) -> {"x": ["a", "c"], "y": "b"}
    """
    raise NotImplementedError("TODO")


def transpose(grid: list[list[int]]) -> list[list[int]]:
    """[[1, 2, 3], [4, 5, 6]] -> [[1, 4], [2, 5], [3, 6]]"""
    raise NotImplementedError("TODO")

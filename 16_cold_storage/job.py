"""16 // COLD STORAGE: persistence, from SQLite to pickle."""

import copyreg
import dbm
import marshal
import pickle
import pickletools
import shelve
import sqlite3
from pathlib import Path
from typing import Any

SCHEMA = """CREATE TABLE IF NOT EXISTS subjects (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    rack TEXT NOT NULL
)"""


def open_vault(path: str | Path) -> sqlite3.Connection:
    """Connect, set row_factory to sqlite3.Row, execute SCHEMA, return the connection."""
    raise NotImplementedError("TODO")


def add_subjects(conn: sqlite3.Connection, rows: list[tuple[str, str, str]]) -> None:
    """Insert (id, name, rack) rows with executemany inside `with conn:`. If any row fails
    (e.g. duplicate id), NONE of them should be inserted."""
    raise NotImplementedError("TODO")


def in_wing(conn: sqlite3.Connection, wing: str) -> list[dict[str, str]]:
    """Subjects whose rack starts with f"{wing}-", as dicts, ordered by id.
    Pass the pattern as a PARAMETER."""
    raise NotImplementedError("TODO")


def rack_counts(conn: sqlite3.Connection) -> dict[str, int]:
    """{wing letter: number of subjects}, computed in SQL with GROUP BY (substr(rack, 1, 1))."""
    raise NotImplementedError("TODO")


def transfer(conn: sqlite3.Connection, subject_id: str, new_rack: str) -> None:
    """Move a subject to new_rack in a transaction. Raise KeyError(subject_id) if no row changed."""
    raise NotImplementedError("TODO")


def save_state(obj: Any, path: str | Path) -> None:
    """pickle obj into the file at path."""
    raise NotImplementedError("TODO")


def load_state(path: str | Path) -> Any:
    """Load a pickle WE wrote ourselves."""
    raise NotImplementedError("TODO")


def opcode_names(blob: bytes) -> list[str]:
    """The names of the pickle opcodes in blob, in order, via pickletools.genops.
    Must NOT unpickle it."""
    raise NotImplementedError("TODO")


class Beacon:
    """A class we pretend we can't modify. Pickling it should go through our reducer."""

    reduced = 0

    def __init__(self, freq: float):
        self.freq = freq


def _reduce_beacon(b: Beacon):
    Beacon.reduced += 1
    return Beacon, (b.freq,)


def register_beacon_reducer() -> None:
    """Register _reduce_beacon for Beacon with copyreg."""
    raise NotImplementedError("TODO")


def shelve_put(path: str | Path, key: str, value: Any) -> None:
    raise NotImplementedError("TODO")


def shelve_get(path: str | Path, key: str, default: Any = None) -> Any:
    raise NotImplementedError("TODO")


def dbm_put(path: str | Path, key: str, value: str) -> None:
    raise NotImplementedError("TODO")


def dbm_get(path: str | Path, key: str) -> str | None:
    """The stored value decoded as UTF-8, or None if the key is missing."""
    raise NotImplementedError("TODO")


def marshal_roundtrip(value: Any) -> Any:
    raise NotImplementedError("TODO")

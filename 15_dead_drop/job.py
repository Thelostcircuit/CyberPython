"""15 // DEAD DROP: read Iris's offline drives."""

import fileinput
import filecmp
import fnmatch
import io
import linecache
import os
import shutil
import stat
import tempfile
from pathlib import Path, PureWindowsPath
from typing import TextIO

PathLike = str | os.PathLike


def write_note(folder: PathLike, name: str, text: str) -> Path:
    """Create `folder` (with parents) if needed, write `text` (UTF-8) to folder/name, return the Path."""
    raise NotImplementedError("TODO")


def read_lines(path: PathLike) -> list[str]:
    """The file's lines (UTF-8) without line endings."""
    raise NotImplementedError("TODO")


def find(root: PathLike, pattern: str) -> list[str]:
    """Files (not directories) anywhere under root whose NAME matches `pattern`, as sorted
    POSIX-style paths relative to root. find(r, "*.txt") -> ["a.txt", "sub/b.txt"]"""
    raise NotImplementedError("TODO")


def matching_names(names: list[str], pattern: str) -> list[str]:
    """fnmatch.filter, preserving input order."""
    raise NotImplementedError("TODO")


def tree_size(root: PathLike) -> int:
    """Total size in bytes of every file under root, using os.walk."""
    raise NotImplementedError("TODO")


def compare_dirs(a: PathLike, b: PathLike) -> dict[str, list[str]]:
    """Top-level comparison with filecmp.dircmp:
    {"left_only": sorted, "right_only": sorted, "different": sorted diff_files}"""
    raise NotImplementedError("TODO")


def lock_down(path: PathLike) -> str:
    """chmod the file to owner read/write only (0o600); return stat.filemode of its new mode."""
    raise NotImplementedError("TODO")


def relocate(path: PathLike, dest_dir: PathLike) -> Path:
    """Move the file into dest_dir (created if missing). Return its new Path."""
    raise NotImplementedError("TODO")


def scratch_roundtrip(data: bytes) -> tuple[bytes, bool]:
    """Inside a tempfile.TemporaryDirectory, write data to a file and read it back.
    Return (bytes read, whether the temporary directory still exists AFTER the with block)."""
    raise NotImplementedError("TODO")


def stitched(paths: list[PathLike]) -> list[tuple[str, int, str]]:
    """Read all files as one stream with fileinput. For each line give
    (file NAME only, line number within that file starting at 1, line without its newline)."""
    raise NotImplementedError("TODO")


def line_at(path: PathLike, n: int) -> str:
    """Line n (1-based) without its newline, via linecache. Missing line -> ""."""
    raise NotImplementedError("TODO")


def upper_stream(src: TextIO) -> io.StringIO:
    """Read src line by line and write each upper-cased line to a new io.StringIO.
    Return that StringIO rewound to position 0."""
    raise NotImplementedError("TODO")


def windows_parts(path: str) -> tuple[str, str, str, str]:
    """r"C:\\drops\\chapel\\map.v2.png" -> ("C:", "chapel", "map.v2", ".png")
    (drive, name of the containing folder, stem, suffix). Works on any OS."""
    raise NotImplementedError("TODO")

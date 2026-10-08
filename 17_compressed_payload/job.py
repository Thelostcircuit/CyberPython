"""17 // COMPRESSED PAYLOAD: squeeze the release program through the intake port."""

import bz2
import gzip
import lzma
import shutil
import tarfile
import zipapp
import zipfile
import zlib
from compression import zstd
from pathlib import Path
from typing import Iterable

ALGOS = ("zlib", "gzip", "bz2", "lzma", "zstd")


def pack(data: bytes, algo: str) -> bytes:
    """Compress with the named algorithm (default settings). Unknown name -> ValueError."""
    raise NotImplementedError("TODO")


def unpack(blob: bytes, algo: str) -> bytes:
    raise NotImplementedError("TODO")


def best_algo(data: bytes) -> str:
    """The name in ALGOS whose pack() output is smallest (ties: the earlier name in ALGOS)."""
    raise NotImplementedError("TODO")


def stream_pack(chunks: Iterable[bytes]) -> bytes:
    """Compress chunk by chunk with zlib.compressobj(); zlib.decompress must restore the data."""
    raise NotImplementedError("TODO")


def checksums(data: bytes) -> tuple[int, int]:
    """(zlib.crc32(data), zlib.adler32(data))"""
    raise NotImplementedError("TODO")


def gzip_file(src: str | Path, dst: str | Path) -> None:
    """Stream src into a gzip file at dst (shutil.copyfileobj; don't read it all at once)."""
    raise NotImplementedError("TODO")


def build_zip(zip_path: str | Path, files: dict[str, str]) -> None:
    """Write each {archive name: text} into a new ZIP_DEFLATED zip (writestr)."""
    raise NotImplementedError("TODO")


def zip_manifest(zip_path: str | Path) -> list[tuple[str, int]]:
    """Sorted [(name, uncompressed file_size)] for every member."""
    raise NotImplementedError("TODO")


def build_tar(tar_path: str | Path, folder: str | Path) -> None:
    """Create an xz-compressed tar of `folder`, stored under its own folder name
    (so "some/where/release_v7" appears in the archive as "release_v7/...")."""
    raise NotImplementedError("TODO")


def safe_extract(tar_path: str | Path, dest: str | Path) -> list[str]:
    """Extract everything into dest using the "data" filter (dangerous members raise).
    Return the sorted member names."""
    raise NotImplementedError("TODO")


def make_app(src_dir: str | Path, target: str | Path, main: str) -> None:
    """Build a runnable .pyz from src_dir with zipapp; `main` is like "cli:main"."""
    raise NotImplementedError("TODO")

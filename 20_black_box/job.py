"""20 // BLACK BOX: logging, warnings, tracebacks, and last words."""

import atexit
import faulthandler
import logging
import logging.config
import logging.handlers
import tempfile
import traceback
import warnings
from pathlib import Path
from typing import Any, Callable, TextIO


def crew_logger(stream: TextIO) -> logging.Logger:
    """The "crew" logger: level DEBUG, propagate False, and exactly ONE StreamHandler(stream)
    formatted "%(levelname)s:%(name)s:%(message)s". Calling again replaces the handler rather
    than adding another one."""
    raise NotImplementedError("TODO")


def radio_config(stream: TextIO) -> None:
    """Use logging.config.dictConfig so that logger "crew.radio" logs WARNING and above to
    `stream` formatted "%(levelname)s|%(message)s", with propagate False.
    Pass disable_existing_loggers=False so other loggers keep working."""
    raise NotImplementedError("TODO")


class BlackBox(logging.Handler):
    """Keeps every record it receives as (record.levelname, self.format(record)) in .records."""

    def __init__(self, level: int = logging.NOTSET):
        super().__init__(level)
        self.records: list[tuple[str, str]] = []

    def emit(self, record: logging.LogRecord) -> None:
        raise NotImplementedError("TODO")


def risky_read(logger: logging.Logger, path: str | Path) -> str | None:
    """Return the file's text. On OSError, call logger.exception(f"read failed: {path}")
    and return None."""
    raise NotImplementedError("TODO")


def rotating_logger(path: str | Path, max_bytes: int, backups: int) -> logging.Logger:
    """A logger named f"rotor.{path}" at INFO with one RotatingFileHandler(path, maxBytes=...,
    backupCount=..., encoding="utf-8") using the format "%(message)s". propagate False."""
    raise NotImplementedError("TODO")


def crash_site(exc: BaseException) -> tuple[str, int]:
    """(function name, line number) of the LAST frame in exc's traceback."""
    raise NotImplementedError("TODO")


def error_text(exc: BaseException) -> str:
    """The full formatted traceback as one string (traceback.format_exception)."""
    raise NotImplementedError("TODO")


def old_scan() -> str:
    """Emit DeprecationWarning("old_scan is deprecated; use scan_v2") pointing at the CALLER
    (stacklevel=2), then return "scanned"."""
    raise NotImplementedError("TODO")


def caught_warnings(func: Callable[[], Any]) -> list[str]:
    """Call func() and return the messages (as str) of every warning it raised, in order.
    No warning may be suppressed as a duplicate."""
    raise NotImplementedError("TODO")


def strictly(func: Callable[[], Any]) -> Any:
    """Call func() with every warning turned into an exception; return its result.
    The warning filters must be restored afterwards."""
    raise NotImplementedError("TODO")


def on_exit(message: str) -> None:
    """Arrange for print(message) to run when the interpreter exits normally."""
    raise NotImplementedError("TODO")


def stack_dump() -> str:
    """faulthandler.dump_traceback into a temporary file (it needs a real file descriptor),
    then return the file's text."""
    raise NotImplementedError("TODO")

"""23 // SHELL GAME: conduct other programs, and talk to the OS directly."""

import errno
import mmap
import os
import platform
import select
import signal
import subprocess
from pathlib import Path
from typing import Any, Callable, Iterator

if os.name == "posix":
    import fcntl
    import grp
    import pwd


def run_tool(args: list[str], stdin_text: str | None = None) -> tuple[int, str, str]:
    """subprocess.run with captured text output (and stdin_text as input, if given).
    Never raises for a non-zero exit."""
    raise NotImplementedError("TODO")


def run_or_timeout(args: list[str], seconds: float) -> str:
    """The child's stdout, or "TIMEOUT" if it runs longer than `seconds`."""
    raise NotImplementedError("TODO")


def checked_output(args: list[str]) -> str:
    """stdout of a successful run; raise subprocess.CalledProcessError on a non-zero exit."""
    raise NotImplementedError("TODO")


def pipe(first: list[str], second: list[str]) -> str:
    """Run `first | second` with two Popen objects and return second's stdout (text)."""
    raise NotImplementedError("TODO")


def live_lines(args: list[str]) -> Iterator[str]:
    """Yield each output line (without the newline) as the child prints it (Popen + iterate
    over proc.stdout). Wait for the child when the output ends."""
    raise NotImplementedError("TODO")


def stop_politely(proc: subprocess.Popen, grace: float) -> int:
    """proc.terminate(); wait up to `grace` seconds; if it's still running, proc.kill() and wait.
    Return the final returncode."""
    raise NotImplementedError("TODO")


def trap(signum: int, log: list[str]) -> Any:
    """Install a handler for signum that appends signal.Signals(signum).name to log.
    Return the previous handler (so the caller can restore it)."""
    raise NotImplementedError("TODO")


def explain_errno(code: int) -> str:
    """explain_errno(2) -> "ENOENT: No such file or directory" """
    raise NotImplementedError("TODO")


def machine_report() -> dict[str, str]:
    """{"system": platform.system(), "machine": platform.machine(),
        "python": platform.python_version()}"""
    raise NotImplementedError("TODO")


def patch_file(path: str | Path, offset: int, data: bytes) -> None:
    """Overwrite len(data) bytes at offset IN PLACE using mmap (the file size never changes).
    Raise ValueError if the patch would run past the end of the file."""
    raise NotImplementedError("TODO")


def owner_and_group(path: str | Path) -> tuple[str, str]:
    """(user name, group name) owning path, via os.stat + pwd + grp."""
    raise NotImplementedError("TODO")


def nonblocking_pipe() -> tuple[int, int]:
    """os.pipe(), with O_NONBLOCK added to the READ end's flags via fcntl. Return (r, w)."""
    raise NotImplementedError("TODO")


def wait_readable(fd: int, timeout: float) -> bool:
    """True if fd becomes readable within timeout seconds (select.select)."""
    raise NotImplementedError("TODO")

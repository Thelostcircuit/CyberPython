"""30 // GHOST IN THE SHELL: Python looking at itself."""

import codeop
import ctypes
import ctypes.util
import gc
import importlib
import importlib.metadata
import importlib.resources
import importlib.util
import inspect
import os
import pkgutil
import pydoc
import runpy
import sys
import venv
import weakref
from pathlib import Path
from types import ModuleType
from typing import Any, Callable


def runtime_facts() -> dict[str, Any]:
    """{"major": sys.version_info.major, "minor": ..., "implementation": sys.implementation.name,
        "recursion_limit": sys.getrecursionlimit()}"""
    raise NotImplementedError("TODO")


def in_venv() -> bool:
    raise NotImplementedError("TODO")


def who_called() -> str:
    """If f() calls g() and g() calls who_called(), return "f".
    Use inspect.currentframe() and walk .f_back twice."""
    raise NotImplementedError("TODO")


def params(func: Callable) -> list[tuple[str, str, Any]]:
    """[(name, kind name like "POSITIONAL_OR_KEYWORD", default or None if it has none)]"""
    raise NotImplementedError("TODO")


def own_functions(module: ModuleType) -> list[str]:
    """Sorted names of functions whose __module__ is this module's __name__ (so imported
    functions are excluded). Use inspect.getmembers(module, inspect.isfunction)."""
    raise NotImplementedError("TODO")


class _Node:
    def __init__(self):
        self.other = None


def cycle_is_collected() -> bool:
    """Make two _Node objects that point at each other, keep only a weakref.ref to one, delete
    both names, call gc.collect(), and return True if the weakref is now dead (returns None)."""
    raise NotImplementedError("TODO")


def load_file(name: str, path: str | Path) -> ModuleType:
    """Import the Python file at path as a module called `name`
    (spec_from_file_location + module_from_spec + exec_module). Don't add it to sys.modules."""
    raise NotImplementedError("TODO")


def submodules(package: str) -> list[str]:
    """Sorted names of the modules directly inside an importable package (pkgutil.iter_modules
    over the package's __path__)."""
    raise NotImplementedError("TODO")


def run_and_get(path: str | Path, var: str) -> Any:
    """Run a script with runpy.run_path and return the value of the global `var` it defines."""
    raise NotImplementedError("TODO")


def import_from_zip(zip_path: str | Path, module: str) -> ModuleType:
    """Temporarily put zip_path at the front of sys.path, import_module(module), then remove the
    path again (in a finally) and return the module. (zipimport does the work behind the scenes.)"""
    raise NotImplementedError("TODO")


def package_data(package: str, name: str) -> str:
    """Text of a data file inside a package, via importlib.resources.files."""
    raise NotImplementedError("TODO")


def installed_version(dist: str) -> str | None:
    """importlib.metadata.version(dist), or None if it isn't installed."""
    raise NotImplementedError("TODO")


# Header: a ctypes.Structure with _fields_ magic (c_char * 4), version (c_uint8),
# length (c_uint32), in that order.
Header = None  # TODO


def c_abs(n: int) -> int:
    """Call the C library's abs() through ctypes (Unix: ctypes.util.find_library("c"))."""
    raise NotImplementedError("TODO")


def is_complete(source: str) -> bool:
    """True if source is a complete statement, False if it needs more lines
    (codeop.compile_command returns None). Syntax errors propagate."""
    raise NotImplementedError("TODO")


def fresh_venv(path: str | Path) -> Path:
    """venv.create(path, with_pip=False); return the Path of its python executable
    (bin/python on Unix, Scripts/python.exe on Windows)."""
    raise NotImplementedError("TODO")


def doc_text(obj: Any) -> str:
    """pydoc.render_doc(obj, renderer=pydoc.plaintext)"""
    raise NotImplementedError("TODO")

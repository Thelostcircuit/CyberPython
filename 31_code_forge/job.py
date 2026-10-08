"""31 // CODE FORGE: tokens, trees, bytecode."""

import ast
import compileall
import contextlib
import dis
import io
import keyword
import py_compile
import pyclbr
import symtable
import tabnanny
import token
import tokenize
from pathlib import Path
from typing import Any, Callable

WANTED = {token.NAME, token.OP, token.NUMBER, token.STRING}


def token_pairs(source: str) -> list[tuple[str, str]]:
    """(token.tok_name[type], string) for every NAME/OP/NUMBER/STRING token, in order."""
    raise NotImplementedError("TODO")


def comments(source: str) -> list[str]:
    """The text of every COMMENT token (including the #)."""
    raise NotImplementedError("TODO")


def reserved(word: str) -> str:
    """"keyword", "soft keyword", or "no"."""
    raise NotImplementedError("TODO")


def names_used(source: str) -> list[str]:
    """Sorted distinct ids of every ast.Name node."""
    raise NotImplementedError("TODO")


def function_names(source: str) -> list[str]:
    """Names of every FunctionDef and AsyncFunctionDef, nested ones included, in source order
    (sort by (lineno, col_offset))."""
    raise NotImplementedError("TODO")


def read_literal(text: str) -> Any:
    """ast.literal_eval. It raises ValueError (or SyntaxError) for non-literals; convert a
    SyntaxError into ValueError too."""
    raise NotImplementedError("TODO")


class ConstantFolder(ast.NodeTransformer):
    """Replace BinOp(Constant, +|-|*, Constant), where both values are int or float (not bool),
    with a single Constant holding the result. Children first, so nested expressions fold."""

    pass  # TODO: visit_BinOp


def fold_constants(source: str) -> str:
    """Apply ConstantFolder, fix_missing_locations, and return ast.unparse of the result."""
    raise NotImplementedError("TODO")


def rename(source: str, old: str, new: str) -> str:
    """Rename every ast.Name with id `old` to `new` (a NodeTransformer), then unparse."""
    raise NotImplementedError("TODO")


def opnames(func: Callable) -> list[str]:
    raise NotImplementedError("TODO")


def count_opcode(func: Callable, name: str) -> int:
    """How many instructions in func have that opname. Unknown names (not in opcode.opmap)
    raise KeyError."""
    raise NotImplementedError("TODO")


def function_locals(source: str, func: str) -> list[str]:
    """Sorted local names (symtable Function.get_locals()) of the top-level function `func`.
    Raise KeyError if there's no such function."""
    raise NotImplementedError("TODO")


def outline(directory: str | Path, module: str) -> dict[str, str]:
    """{name: "class" or "function"} for the top-level classes and functions in
    <directory>/<module>.py, using pyclbr.readmodule_ex(module, path=[str(directory)])."""
    raise NotImplementedError("TODO")


def build_pyc(path: str | Path) -> Path:
    """py_compile.compile(path, doraise=True); return the .pyc Path."""
    raise NotImplementedError("TODO")


def build_tree(directory: str | Path) -> bool:
    """compileall.compile_dir(directory, quiet=1); return its success flag as a bool."""
    raise NotImplementedError("TODO")


def tab_trouble(path: str | Path) -> bool:
    """Run tabnanny.check(path) while capturing stdout; True if it printed anything."""
    raise NotImplementedError("TODO")

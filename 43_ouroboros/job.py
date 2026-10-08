"""43 // OUROBOROS: an assembler and a virtual machine for SNAKE-1. See README.md for the ISA."""

import re
from dataclasses import dataclass, field

# Opcodes and whether they take an argument: "int", "name" (a variable), "label", or None.
OPCODES: dict[str, str | None] = {
    "PUSH": "int", "POP": None, "DUP": None, "SWAP": None,
    "ADD": None, "SUB": None, "MUL": None, "DIV": None, "MOD": None,
    "EQ": None, "LT": None,
    "LOAD": "name", "STORE": "name",
    "JMP": "label", "JZ": "label", "JNZ": "label", "CALL": "label", "RET": None,
    "PRINT": None, "RELEASE": None, "HALT": None,
}
NAME = re.compile(r"[A-Za-z_]\w*")


class AsmError(Exception):
    """An assembly error. str(e) must contain f"line {n}" (1-based)."""


class VMError(Exception):
    """A runtime error inside the VM."""


@dataclass(frozen=True)
class Instr:
    op: str                        # upper-case opcode
    arg: int | str | None = None   # int for PUSH and jumps/calls (resolved address), str for LOAD/STORE


@dataclass
class Result:
    output: list[int] = field(default_factory=list)
    released: list[int] = field(default_factory=list)
    variables: dict[str, int] = field(default_factory=dict)


def parse_line(line: str) -> tuple[str | None, str | None, str | None]:
    """Strip any ";" comment and surrounding space. An optional leading "label:" comes first.
    Then an optional opcode (upper-cased) and an optional single argument (kept as text).
    More than one argument -> AsmError (without a line number is fine here).

    parse_line("loop: push 3 ; hi") -> ("loop", "PUSH", "3")
    parse_line("   ; nothing")      -> (None, None, None)
    """
    raise NotImplementedError("TODO")


def assemble(source: str) -> list[Instr]:
    """Two passes over source.splitlines():
      1. record label -> address (the index of the next instruction); duplicate -> AsmError
      2. build Instrs: check the opcode exists, the argument is present exactly when needed,
         ints parse (negative allowed), names match NAME, labels exist (resolve to address).
    Every AsmError message includes f"line {n}"."""
    raise NotImplementedError("TODO")


def disassemble(program: list[Instr]) -> str:
    """One line per instruction: f"{index:03d} {op}" plus f" {arg}" when there is one.
    Lines joined with "\\n"."""
    raise NotImplementedError("TODO")


class VM:
    """Runs a program. run() returns a Result; errors raise VMError (see README)."""

    def run(self, program: list[Instr], max_steps: int = 100_000) -> Result:
        raise NotImplementedError("TODO")


def run_source(source: str, max_steps: int = 100_000) -> Result:
    raise NotImplementedError("TODO")

"""21 // STREET INTERFACE: a letter-perfect client for freight lift 3."""

import argparse
import cmd
import getopt
import getpass
import optparse
import shlex
from typing import Callable


def build_parser() -> argparse.ArgumentParser:
    """prog="liftctl".
    Global options:  -v/--verbose (count, default 0),  --dry-run (flag)
    Subcommands (dest="command", required):
      call   --floor INT (required, must be in range(-9, 31))
             --priority {low,normal,high} (default "normal")
      status --json (flag)
    """
    raise NotImplementedError("TODO")


def legacy_opts(argv: list[str]) -> tuple[dict[str, str], list[str]]:
    """getopt with short options "vf:" and long options ["verbose", "floor="].
    Return ({"verbose": "yes"} if -v/--verbose given, plus "floor": value if given}, rest)."""
    raise NotImplementedError("TODO")


def optparse_quiet(argv: list[str]) -> tuple[bool, list[str]]:
    """An optparse.OptionParser with -q/--quiet (store_true, default False). Return (quiet, args)."""
    raise NotImplementedError("TODO")


def split_line(line: str) -> list[str]:
    raise NotImplementedError("TODO")


def join_args(args: list[str]) -> str:
    """A shell-safe command line (shlex.join)."""
    raise NotImplementedError("TODO")


def read_code(prompt: Callable[[str], str] = getpass.getpass) -> str:
    """Call prompt("access code: "), strip the result, raise ValueError if it's empty."""
    raise NotImplementedError("TODO")


class LiftShell(cmd.Cmd):
    """prompt "lift> ". Keeps self.floor (starts at 0). Write every message with a newline
    to self.stdout.

    floor N    -> if N is an int in -9..30: set it and print "moving to N"
                  otherwise print "bad floor: <arg>"
    status     -> print "floor N"  ("status json" prints '{"floor": N}')
    quit       -> print "bye" and stop the loop (return True)
    anything else -> print "unknown: <the whole line>"
    Tab completion for status offers the options ["json", "brief"] starting with the text typed.
    """

    prompt = "lift> "

    def __init__(self, stdout=None):
        super().__init__(stdout=stdout)
        self.floor = 0

    pass  # TODO: do_floor, do_status, complete_status, do_quit, default


def make_completer(words: list[str]) -> Callable[[str, int], str | None]:
    """Return completer(text, state): the state-th word (in the order given) that starts with
    text, or None when there are no more."""
    raise NotImplementedError("TODO")

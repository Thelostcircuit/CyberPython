"""06 // FLATLINE PROTOCOL: survive BASILISK's countermeasures."""

from typing import Callable


# --- The exception hierarchy -------------------------------------------------------------
# DeckError(Exception)                      base class for everything below
# IceError(DeckError)                       IceError("black ice", level=5): str(e) == "black ice",
#                                           e.level == 5
# TraceDetected(DeckError)
# MalformedPacket(DeckError)

pass  # TODO: define the four exception classes described above


def safe_int(raw, default=None):
    """int(raw), or `default` if that raises ValueError or TypeError."""
    raise NotImplementedError("TODO")


def parse_packet(raw: str) -> str:
    """Parse "LEN:DATA" and return DATA.

    parse_packet("5:hello") -> "hello"
    No ":" at all              -> MalformedPacket
    LEN not an integer         -> MalformedPacket raised FROM the ValueError (use `from`)
    len(DATA) != LEN           -> MalformedPacket
    DATA may itself contain ":" (split only on the first one).
    """
    raise NotImplementedError("TODO")


def process(packets: list[str]) -> tuple[list[str], int]:
    """parse_packet every packet. Return (list of good DATA in order, number of bad packets).
    Only MalformedPacket counts as bad. Any other exception should propagate.
    Use try / except / else."""
    raise NotImplementedError("TODO")


def guarded(log: list[str], action: Callable[[], object]) -> object:
    """Append "open" to log, call action(). On success append "ok" and return its result.
    ALWAYS append "close" last, even if action raises. Exceptions must still propagate."""
    raise NotImplementedError("TODO")


class Shield:
    """Context manager.

    with Shield() as s:
        raise IceError("x", 1)       # absorbed: execution continues after the with block
    s.absorbed -> [that IceError]

    Any DeckError (or subclass) is suppressed and appended to .absorbed.
    Any other exception passes through untouched.
    """

    pass  # TODO: __init__, __enter__, __exit__


def run_countermeasures(actions: list[Callable[[], object]]) -> list[object]:
    """Call every action, even after failures. If none raised, return their results in order.
    If any raised an Exception, raise ExceptionGroup("countermeasures", [the exceptions, in
    order])."""
    raise NotImplementedError("TODO")


def triage(func: Callable[[], object]) -> dict[str, int]:
    """Call func(), which may raise an ExceptionGroup. Use `except*` to count what's inside.

    Return {"ice": <number of IceErrors>, "trace": <number of TraceDetected>}.
    Anything else in the group must propagate (except* does this for you).
    If func() doesn't raise, both counts are 0.
    """
    raise NotImplementedError("TODO")

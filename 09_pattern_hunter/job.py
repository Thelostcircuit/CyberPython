"""09 // PATTERN HUNTER: find the shapes in the Ouroboros log dump.

A Coil log line looks like:

    2091-03-14 22:10:05 [WARN] rack=C-17 subject=OS-ENG-4471 msg=priority hold

  - timestamp: YYYY-MM-DD HH:MM:SS
  - level: one of INFO, WARN, ERROR inside square brackets
  - rack: a capital letter, a dash, one or more digits
  - subject: OS-<three capital letters>-<four digits>
  - anything may follow msg= (including nothing)
"""

import re


def subject_ids(text: str) -> list[str]:
    """Every subject ID (OS-XXX-9999) in order. Must be whole words: "XOS-ENG-12345" doesn't count."""
    raise NotImplementedError("TODO")


def parse_line(line: str) -> dict[str, str] | None:
    """Return {"timestamp", "level", "rack", "subject", "msg"} for a valid log line (the whole
    line must match), else None. msg may be empty."""
    raise NotImplementedError("TODO")


def redact_emails(text: str) -> str:
    """Replace each email address with "[REDACTED]".
    An address here is: one or more of [A-Za-z0-9._+-], "@", then one or more dot-separated
    labels of [A-Za-z0-9-], ending in a label of at least 2 letters. e.g. i.vale+work@ouro.corp.os"""
    raise NotImplementedError("TODO")


def squash_ws(text: str) -> str:
    """Collapse runs of any whitespace (spaces, tabs, newlines) to one space; strip the ends."""
    raise NotImplementedError("TODO")


def iso_dates(text: str) -> str:
    """Rewrite DD/MM/YYYY as YYYY-MM-DD everywhere. Days and months are always two digits."""
    raise NotImplementedError("TODO")


def strong_passphrase(s: str) -> bool:
    """True if s is 12+ characters, contains an uppercase letter, a lowercase letter and a
    digit, and contains no whitespace. Use re.fullmatch with lookaheads."""
    raise NotImplementedError("TODO")


def tokens(expr: str) -> list[str]:
    """Split into tokens: numbers (17, 17.5), names (letters/digits/_, not starting with a
    digit), and single-character operators from + - * / ( ). Whitespace is skipped.
    tokens("rack_count*2 + 17.5") -> ["rack_count", "*", "2", "+", "17.5"]"""
    raise NotImplementedError("TODO")


def split_fields(line: str) -> list[str]:
    """Split on "," or ";" with any spaces around them. Leading/trailing spaces on the whole line
    are stripped first. split_fields(" a , b;c ;  d ") -> ["a", "b", "c", "d"]"""
    raise NotImplementedError("TODO")


def censor(text: str, words: list[str]) -> str:
    """Replace each whole-word, case-insensitive occurrence of any of `words` with "*" repeated
    to the same length. Words may contain regex special characters (escape them)."""
    raise NotImplementedError("TODO")

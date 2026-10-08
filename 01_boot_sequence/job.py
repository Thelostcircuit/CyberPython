"""01 // BOOT SEQUENCE: rebuild MONTY's boot checks.

Replace every `raise NotImplementedError("TODO")` with working code.
Run the tests from this folder:  uv run python -m unittest -v
"""


def cell_voltage(total: float, cells: int) -> float:
    """Voltage per cell, rounded to 2 decimal places.

    cell_voltage(11.1, 3) -> 3.7
    """
    raise NotImplementedError("TODO")


def split_credits(total: int, crew: int) -> tuple[int, int]:
    """Split `total` credits evenly between `crew` people.

    Return (each, left_over): split_credits(340, 3) -> (113, 1)
    """
    raise NotImplementedError("TODO")


def is_safe_level(level: int) -> bool:
    """True if 20 <= level <= 95. Use a single chained comparison."""
    raise NotImplementedError("TODO")


def callsign(first: str, last: str) -> str:
    """Strip whitespace, upper-case the surname, capitalise the first name.

    callsign("  iris", "vale ") -> "VALE, Iris"
    """
    raise NotImplementedError("TODO")


def status_line(name: str, level: int, temp: float) -> str:
    """A fixed-width status line: name left-aligned in 8 chars, level right-aligned in 3 chars
    followed by '%', temperature with exactly 1 decimal place right-aligned in 6 chars
    followed by 'C'. Fields are separated by '|'.

    status_line("core", 7, 36.456) -> "core    |  7%|  36.5C"
    """
    raise NotImplementedError("TODO")


def parse_reading(raw: str) -> float:
    """Turn a raw sensor reading like "  36.6C " or "36.6 c" into the float 36.6.

    Surrounding whitespace is ignored, the trailing C may be upper or lower case,
    and there may be spaces before it.
    """
    raise NotImplementedError("TODO")


def mask_card(number: str) -> str:
    """Replace every character except the last four with '*'.

    mask_card("4929123456781234") -> "************1234"
    Numbers of 4 characters or fewer are returned unchanged.
    """
    raise NotImplementedError("TODO")


def signal_label(strength: int | None) -> str:
    """Describe a signal strength (0-100).

    None      -> "no signal"
    0-29      -> "weak (N)"
    30-69     -> "fair (N)"
    70-100    -> "strong (N)"
    where N is the strength, e.g. signal_label(75) -> "strong (75)".
    """
    raise NotImplementedError("TODO")

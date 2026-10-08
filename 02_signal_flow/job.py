"""02 // SIGNAL FLOW: teach MONTY to read (and write) drone logic."""


def threat_level(scans: int) -> str:
    """0 scans -> "clear", 1-2 -> "watch", 3 or more -> "run"."""
    raise NotImplementedError("TODO")


def countdown(n: int) -> str:
    """Use a while loop. countdown(3) -> "3..2..1..GO",  countdown(0) -> "GO"."""
    raise NotImplementedError("TODO")


def patrol_path(start: int, step: int, count: int, grid: int) -> list[int]:
    """A drone starts at `start` on a circular track of `grid` cells (0..grid-1), and moves
    `step` cells each tick. Return the `count` positions it occupies, starting position first.

    patrol_path(8, 3, 4, 10) -> [8, 1, 4, 7]
    """
    raise NotImplementedError("TODO")


def first_blind_spot(coverage: list[int]) -> int:
    """Index of the first 0 in `coverage`, or -1 if there isn't one.
    Write it with a for loop and a loop `else`. No list.index method allowed."""
    raise NotImplementedError("TODO")


def scan_code(n: int) -> str:
    """Multiples of 3 -> "SCAN", multiples of 5 -> "LOCK", multiples of both -> "SCANLOCK",
    anything else -> str(n)."""
    raise NotImplementedError("TODO")


def longest_quiet(readings: list[int | None], threshold: int) -> int:
    """Length of the longest run of consecutive readings strictly below `threshold`.
    `None` readings are sensor dropouts. Ignore them completely (they neither extend nor
    break a run).

    longest_quiet([1, 2, None, 3, 9, 1], 5) -> 3     (1, 2, 3)
    """
    raise NotImplementedError("TODO")


def walk(commands: list[str]) -> tuple[int, int]:
    """Start at (0, 0). x grows east, y grows north. Use `match` on command.split():

    "go <dir>"          move 1 step. dir is north/south/east/west
    "go <dir> <n>"      move n steps
    "jump <x> <y>"      teleport to (x, y)
    "wait" or "hide"    do nothing
    anything else       raise ValueError
    Return the final (x, y).
    """
    raise NotImplementedError("TODO")


def drone_response(event: dict) -> str:
    """React to a drone event. Use `match` with mapping patterns:

    {"type": "scan", "hit": True}                -> "RUN"
    {"type": "scan", "hit": False}               -> "HOLD"
    {"type": "patrol", "id": id} where id starts with "W"   -> "AVOID <id>"
    {"type": "patrol", "id": id} (any other id)  -> "IGNORE <id>"
    {"type": "alarm", "zone": z} with z in 1..3  -> "EVACUATE ZONE <z>"
    anything else                                -> "UNKNOWN"
    Extra keys in the dict are allowed.
    """
    raise NotImplementedError("TODO")

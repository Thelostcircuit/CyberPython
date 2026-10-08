"""14 // TIME HEIST: find the gap, to the second."""

import calendar
import time
from datetime import UTC, date, datetime, timedelta, timezone
from typing import Any, Callable
from zoneinfo import ZoneInfo

TST = timezone(timedelta(hours=9), "TST")   # Tower Standard Time: fixed UTC+9, no DST
GAP_EVERY = timedelta(hours=8 * 11)          # the gap repeats every 11 eight-hour shifts


def parse_stamp(s: str) -> datetime:
    """"2091-03-14 22:10:05" (a TST wall-clock time) -> an aware datetime in TST."""
    raise NotImplementedError("TODO")


def to_utc_iso(dt: datetime) -> str:
    """Convert an aware datetime to UTC and return its isoformat()."""
    raise NotImplementedError("TODO")


def show_in(dt: datetime, zone: str) -> str:
    """The same instant in IANA zone `zone`, formatted "%Y-%m-%d %H:%M %Z"."""
    raise NotImplementedError("TODO")


def offset_hours(day: date, zone: str) -> float:
    """The zone's UTC offset at 12:00 local time on `day`, in hours. (-4.0 for New York in July)"""
    raise NotImplementedError("TODO")


def next_gap(first_gap: datetime, now: datetime) -> datetime:
    """Gaps open at first_gap + k * GAP_EVERY for k = 0, 1, 2, ...
    Return the first one at or after `now` (both aware; may be in different zones).
    The result keeps first_gap's time zone."""
    raise NotImplementedError("TODO")


def hms(seconds: int) -> str:
    """7509 -> "2h 05m 09s".  Hours are not padded, minutes and seconds are 2 digits."""
    raise NotImplementedError("TODO")


def weekdays_between(start: date, end: date) -> int:
    """How many dates d with start <= d < end fall on Monday-Friday."""
    raise NotImplementedError("TODO")


def last_weekday(year: int, month: int, weekday: int) -> date:
    """The last date in that month with that weekday (0 = Monday ... 6 = Sunday).
    Use calendar.monthrange."""
    raise NotImplementedError("TODO")


def from_epoch(ts: float) -> datetime:
    """Seconds since the Unix epoch -> aware datetime in UTC."""
    raise NotImplementedError("TODO")


def timed(func: Callable, *args: Any) -> tuple[Any, float]:
    """Call func(*args); return (result, elapsed seconds measured with time.perf_counter)."""
    raise NotImplementedError("TODO")

# 14 // TIME HEIST

```
[PYTHIA-9] clocks: Coilhaven local ── Tower Standard (TST, UTC+9) ── rota server: America/New_York
```

**Modules:** `datetime`, `zoneinfo`, `time`, `calendar`

The gap opens every eleventh shift, for nine minutes. Shifts are eight hours long. To be at
the intake dock when it opens you need to know *exactly* when that is, and the evidence is
spread across three different clocks.

> **DEX:** It's just adding hours. How hard can it be?
>
> **MONTY:** Every programmer who has ever said that is now in therapy. Time zones shift. Some
> observe daylight saving and some don't. Some hours happen twice a year and some never
> happen at all. The rule is: **store and compute in UTC, with time-zone-aware datetimes, and
> only convert to local time for display.** Python's `datetime` and `zoneinfo` do it
> properly, as long as you let them.

---

## ▓ TECH BRIEFING

### `datetime`: the types

```python
from datetime import date, time, datetime, timedelta, timezone, UTC

date(2091, 3, 14)                         # a calendar date
time(22, 10, 5)                           # a wall-clock time
datetime(2091, 3, 14, 22, 10, 5)          # NAIVE: no time zone. Ambiguous, so avoid for real events
datetime(2091, 3, 14, 13, 10, tzinfo=UTC) # AWARE
datetime.now(UTC)                         # current time, aware
date.today()

timedelta(hours=8, minutes=9)             # a duration
dt + timedelta(days=1)                    # arithmetic
later - earlier                           # a timedelta
td.total_seconds()
```

### Parsing and formatting

```python
datetime.strptime("2091-03-14 22:10:05", "%Y-%m-%d %H:%M:%S")
datetime.fromisoformat("2091-03-14T22:10:05+09:00")
dt.isoformat()                            # '2091-03-14T22:10:05+09:00'
dt.strftime("%a %d %b %Y, %H:%M")         # 'Wed 14 Mar 2091, 22:10'
```

Common codes: `%Y` year, `%m` month, `%d` day, `%H` hour (24h), `%I` hour (12h), `%M` minute,
`%S` second, `%a`/`%A` weekday name, `%b`/`%B` month name, `%j` day of year, `%z` UTC offset,
`%Z` zone name.

### Time zones: `zoneinfo`

```python
from zoneinfo import ZoneInfo
ny = ZoneInfo("America/New_York")         # the IANA database: DST rules included
dt = datetime(2026, 7, 1, 9, 0, tzinfo=ny)
dt.utcoffset()                            # timedelta(hours=-4) in July (EDT)
dt.astimezone(ZoneInfo("Asia/Tokyo"))     # the same instant, shown in another zone
dt.astimezone(UTC)
tst = timezone(timedelta(hours=9), "TST") # a FIXED offset (no DST)
```

`replace(tzinfo=...)` *labels* a datetime without changing the wall-clock numbers.
`astimezone(...)` *converts* the same instant. Mixing them up is the classic bug.

In the hour that happens twice when clocks go back, `fold=0` picks the first occurrence and
`fold=1` the second. On systems without a tz database, `pip install tzdata` supplies one.

### `time`: the low-level clock

```python
import time
time.time()            # seconds since the Unix epoch, as a float (wall clock: can jump!)
time.perf_counter()    # high-resolution monotonic timer: use this to MEASURE durations
time.monotonic()       # never goes backwards
time.sleep(0.5)
time.gmtime(0)         # struct_time for the epoch;  time.localtime(), time.mktime()
time.strftime("%H:%M", time.localtime())
time.time_ns()         # integer nanoseconds
datetime.fromtimestamp(ts, UTC)   # epoch seconds → aware datetime;  dt.timestamp() goes back
```

### `calendar`

```python
import calendar
calendar.isleap(2092)                 # True
calendar.monthrange(2091, 2)          # (weekday of the 1st, number of days) = (calendar.THURSDAY, 28)
calendar.monthcalendar(2091, 3)       # weeks as lists of day numbers (0 = padding)
calendar.weekday(2091, 3, 14)         # 0 = Monday ... 6 = Sunday
calendar.day_name[0]                  # 'Monday'
print(calendar.month(2091, 3))        # a text calendar;  calendar.TextCalendar / HTMLCalendar
calendar.timegm(struct_time)          # UTC struct_time → epoch seconds
```

`date.weekday()` also returns 0–6 from Monday. `date.isoweekday()` returns 1–7.

---

## ▓ THE JOB

In `job.py`:

1. **`parse_stamp(s)`**: parse `"2091-03-14 22:10:05"` as TST (UTC+9) and return an **aware** datetime.
2. **`to_utc_iso(dt)`**: the ISO string of an aware datetime converted to UTC.
3. **`show_in(dt, zone)`**: the same instant in an IANA zone, formatted `"2026-07-01 09:00 EDT"`.
4. **`offset_hours(day, zone)`**: that zone's UTC offset at noon on that day, as a float of hours (so you can see DST).
5. **`next_gap(first_gap, now)`**: gaps repeat every 11 shifts of 8 hours. Find the first gap at or after `now`.
6. **`hms(seconds)`**: format a duration as `"2h 05m 09s"` with `timedelta`/`divmod`.
7. **`weekdays_between(start, end)`**: count the Monday-to-Friday dates in `[start, end)`.
8. **`last_weekday(year, month, weekday)`**: e.g. the last Friday of the month, with `calendar`.
9. **`from_epoch(ts)`**: epoch seconds → aware UTC datetime.
10. **`timed(func, *args)`**: return `(result, elapsed_seconds)` using `time.perf_counter`.

# HINTS // 14 TIME HEIST

## parse_stamp
<details><summary>Hint</summary>

`datetime.strptime(s, "%Y-%m-%d %H:%M:%S")` gives a naive datetime. `.replace(tzinfo=TST)`
labels it, because those numbers really are TST wall-clock numbers.
</details>

## to_utc_iso / show_in
<details><summary>Hint</summary>

`dt.astimezone(UTC).isoformat()` and
`dt.astimezone(ZoneInfo(zone)).strftime("%Y-%m-%d %H:%M %Z")`.
</details>

## offset_hours
<details><summary>Hint</summary>

Build `datetime(day.year, day.month, day.day, 12, tzinfo=ZoneInfo(zone))`. Its
`.utcoffset()` is a timedelta, so divide its `total_seconds()` by 3600.
</details>

## next_gap
<details><summary>Hint 1</summary>

Aware datetimes in different zones subtract correctly. Dividing one timedelta by another
with `//` gives an int: how many whole periods fit.
</details>
<details><summary>Hint 2</summary>

You want the *ceiling* of `(now - first_gap) / GAP_EVERY`. A neat trick is
`k = -((first_gap - now) // GAP_EVERY)`. Then return `first_gap + k * GAP_EVERY`.
</details>

## hms
<details><summary>Hint</summary>

`minutes, secs = divmod(seconds, 60)`, then `hours, minutes = divmod(minutes, 60)`, then
`f"{hours}h {minutes:02d}m {secs:02d}s"`.
</details>

## weekdays_between
<details><summary>Hint</summary>

Loop `i` over `range((end - start).days)` and count the dates where
`(start + timedelta(days=i)).weekday() < 5`.
</details>

## last_weekday
<details><summary>Hint</summary>

`calendar.monthrange(year, month)[1]` is the number of days in the month. From the last day,
step back `(d.weekday() - weekday) % 7` days.
</details>

## timed
<details><summary>Hint</summary>

`start = time.perf_counter()`, call the function, then return the result and
`time.perf_counter() - start`.
</details>

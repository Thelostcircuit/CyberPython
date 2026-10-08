import time
import unittest
from datetime import UTC, date, datetime, timedelta, timezone
from zoneinfo import ZoneInfo

import job


class TimeHeist(unittest.TestCase):
    def test_parse_stamp(self):
        dt = job.parse_stamp("2091-03-14 22:10:05")
        self.assertEqual(dt.utcoffset(), timedelta(hours=9))
        self.assertEqual((dt.hour, dt.minute, dt.second), (22, 10, 5))

    def test_to_utc_iso(self):
        dt = job.parse_stamp("2091-03-14 02:00:00")
        self.assertEqual(job.to_utc_iso(dt), "2091-03-13T17:00:00+00:00")

    def test_show_in(self):
        dt = datetime(2026, 7, 1, 13, 0, tzinfo=UTC)
        self.assertEqual(job.show_in(dt, "America/New_York"), "2026-07-01 09:00 EDT")
        self.assertEqual(job.show_in(dt, "Asia/Tokyo"), "2026-07-01 22:00 JST")
        winter = datetime(2026, 1, 15, 13, 0, tzinfo=UTC)
        self.assertEqual(job.show_in(winter, "America/New_York"), "2026-01-15 08:00 EST")

    def test_offset_hours(self):
        self.assertEqual(job.offset_hours(date(2026, 7, 1), "America/New_York"), -4.0)
        self.assertEqual(job.offset_hours(date(2026, 1, 1), "America/New_York"), -5.0)
        self.assertEqual(job.offset_hours(date(2026, 1, 1), "Asia/Kolkata"), 5.5)

    def test_next_gap(self):
        first = job.parse_stamp("2091-03-01 06:00:00")
        self.assertEqual(job.next_gap(first, first), first)
        self.assertEqual(job.next_gap(first, first - timedelta(days=3)), first)
        nxt = job.next_gap(first, first + timedelta(seconds=1))
        self.assertEqual(nxt, first + timedelta(hours=88))
        self.assertEqual(nxt.tzinfo, first.tzinfo)
        now_utc = datetime(2091, 3, 10, 0, 0, tzinfo=UTC)
        self.assertEqual(job.next_gap(first, now_utc), first + 3 * timedelta(hours=88))
        exact = first + 2 * timedelta(hours=88)
        self.assertEqual(job.next_gap(first, exact.astimezone(UTC)), exact)

    def test_hms(self):
        self.assertEqual(job.hms(7509), "2h 05m 09s")
        self.assertEqual(job.hms(0), "0h 00m 00s")
        self.assertEqual(job.hms(90061), "25h 01m 01s")

    def test_weekdays_between(self):
        self.assertEqual(job.weekdays_between(date(2026, 9, 21), date(2026, 9, 28)), 5)
        self.assertEqual(job.weekdays_between(date(2026, 9, 26), date(2026, 9, 28)), 0)
        self.assertEqual(job.weekdays_between(date(2026, 9, 1), date(2026, 9, 1)), 0)

    def test_last_weekday(self):
        self.assertEqual(job.last_weekday(2026, 9, 4), date(2026, 9, 25))
        self.assertEqual(job.last_weekday(2026, 2, 5), date(2026, 2, 28))
        self.assertEqual(job.last_weekday(2024, 2, 3), date(2024, 2, 29))

    def test_from_epoch(self):
        self.assertEqual(job.from_epoch(0), datetime(1970, 1, 1, tzinfo=UTC))
        self.assertEqual(job.from_epoch(86400.5).microsecond, 500000)
        self.assertIsNotNone(job.from_epoch(0).tzinfo)

    def test_timed(self):
        result, elapsed = job.timed(lambda a, b: (time.sleep(0.02), a + b)[1], 2, 3)
        self.assertEqual(result, 5)
        self.assertGreaterEqual(elapsed, 0.015)
        self.assertLess(elapsed, 2)


if __name__ == "__main__":
    unittest.main()

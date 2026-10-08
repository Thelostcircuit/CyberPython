import asyncio
import threading
import time
import unittest

import job


class AsyncUprising(unittest.IsolatedAsyncioTestCase):
    async def test_probe(self):
        self.assertEqual(await job.probe("door-3", 0.01), "door-3")

    async def test_probe_all_is_concurrent(self):
        start = time.perf_counter()
        out = await job.probe_all([("a", 0.2), ("b", 0.1), ("c", 0.2)])
        self.assertEqual(out, ["a", "b", "c"])
        self.assertLess(time.perf_counter() - start, 0.35)

    async def test_probe_within(self):
        self.assertEqual(await job.probe_within("x", 0.01, 1), "x")
        self.assertEqual(await job.probe_within("x", 5, 0.05), "TIMEOUT")

    async def test_sweep(self):
        start = time.perf_counter()
        self.assertEqual(await job.sweep({"cam": 0.1, "door": 0.1, "rack": 0.1}),
                         {"cam": "cam", "door": "door", "rack": "rack"})
        self.assertLess(time.perf_counter() - start, 0.25)

    async def test_first_answer(self):
        start = time.perf_counter()
        winner, cancelled = await job.first_answer({"slow": 5, "fast": 0.02, "mid": 3})
        self.assertEqual((winner, cancelled), ("fast", ["mid", "slow"]))
        self.assertLess(time.perf_counter() - start, 1)

    async def test_throttled(self):
        self.assertEqual(await job.throttled(20, 3), 3)
        self.assertEqual(await job.throttled(2, 10), 2)

    async def test_relay(self):
        self.assertEqual(await job.relay(["a", "b", "c"]), ["A", "B", "C"])
        self.assertEqual(await job.relay([]), [])

    async def test_ticks(self):
        self.assertEqual(await job.collect(job.ticks(4)), [0, 1, 2, 3])
        self.assertEqual(await job.collect(job.ticks(0)), [])

    async def test_offload(self):
        main = threading.get_ident()

        def blocking(x):
            time.sleep(0.05)
            return x * 2, threading.get_ident()
        value, tid = await job.offload(blocking, 21)
        self.assertEqual(value, 42)
        self.assertNotEqual(tid, main)

    async def test_echo(self):
        self.assertEqual(await job.echo_upper("release order ready"), "RELEASE ORDER READY")

    async def test_vault_session(self):
        s = job.VaultSession()
        async with s as got:
            self.assertIs(got, s)
            self.assertEqual(s.log, ["open"])
        self.assertEqual(s.log, ["open", "close"])
        s2 = job.VaultSession()
        with self.assertRaises(KeyError):
            async with s2:
                raise KeyError("x")
        self.assertEqual(s2.log, ["open", "close"])


if __name__ == "__main__":
    unittest.main()

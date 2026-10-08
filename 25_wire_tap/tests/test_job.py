import socket
import ssl
import struct
import threading
import unittest

import job


class Framing(unittest.TestCase):
    def test_frame(self):
        self.assertEqual(job.frame(b"abc"), b"\x00\x00\x00\x03abc")
        self.assertEqual(job.frame(b""), b"\x00\x00\x00\x00")

    def test_recv_exact_across_chunks(self):
        a, b = socket.socketpair()
        with a, b:
            def trickle():
                for byte in job.frame(b"release order"):
                    a.sendall(bytes([byte]))
            t = threading.Thread(target=trickle)
            t.start()
            self.assertEqual(job.read_frame(b), b"release order")
            t.join()

    def test_recv_exact_peer_closed(self):
        a, b = socket.socketpair()
        with b:
            a.sendall(struct.pack("!I", 10) + b"short")
            a.close()
            with self.assertRaises(ConnectionError):
                job.read_frame(b)


class Servers(unittest.TestCase):
    def test_port_roundtrip(self):
        payloads = [b"OUROLINK/1 HELLO", b"", b"x" * 100_000]
        self.assertEqual(job.port_roundtrip(payloads), [p[::-1] for p in payloads])

    def test_pair_echo(self):
        self.assertEqual(job.pair_echo([b"lift ", b"to ", b"-6"]), b"lift to -6")
        self.assertEqual(job.pair_echo([]), b"")

    def test_udp(self):
        self.assertEqual(job.udp_ping(b"ping"), (b"ping", True))

    def test_drain_ready(self):
        pairs = [socket.socketpair() for _ in range(3)]
        try:
            pairs[0][0].sendall(b"zero")
            pairs[2][0].sendall(b"two")
            got = job.drain_ready([p[1] for p in pairs], 1)
            self.assertEqual(got, {0: b"zero", 2: b"two"})
            self.assertEqual(job.drain_ready([p[1] for p in pairs], 0.05), {})
        finally:
            for a, b in pairs:
                a.close()
                b.close()


class TLSAndIP(unittest.TestCase):
    def test_context(self):
        ctx = job.port_context()
        self.assertEqual(ctx.verify_mode, ssl.CERT_REQUIRED)
        self.assertTrue(ctx.check_hostname)
        self.assertGreaterEqual(ctx.minimum_version, ssl.TLSVersion.TLSv1_2)

    def test_ip(self):
        self.assertTrue(job.in_coil_net("10.44.17.3"))
        self.assertFalse(job.in_coil_net("10.45.0.1"))
        with self.assertRaises(ValueError):
            job.in_coil_net("10.44.300.1")
        subs = job.coil_subnets(18)
        self.assertEqual(subs, ["10.44.0.0/18", "10.44.64.0/18", "10.44.128.0/18", "10.44.192.0/18"])
        self.assertEqual(job.address_kind("127.0.0.1"), "loopback")
        self.assertEqual(job.address_kind("10.44.1.1"), "private")
        self.assertEqual(job.address_kind("8.8.8.8"), "global")
        self.assertEqual(job.address_kind("::1"), "loopback")


if __name__ == "__main__":
    unittest.main()

"""25 // WIRE TAP: bytes on the wire, framed properly."""

import ipaddress
import selectors
import socket
import socketserver
import ssl
import struct
import threading

COIL_NET = ipaddress.ip_network("10.44.0.0/16")


def frame(payload: bytes) -> bytes:
    """4-byte big-endian length, then the payload."""
    raise NotImplementedError("TODO")


def recv_exact(sock: socket.socket, n: int) -> bytes:
    """Read exactly n bytes (loop over recv). If the peer closes early, raise ConnectionError."""
    raise NotImplementedError("TODO")


def read_frame(sock: socket.socket) -> bytes:
    """Read one framed message and return its payload."""
    raise NotImplementedError("TODO")


class ReversingPort(socketserver.BaseRequestHandler):
    """For each frame received on self.request, reply with a frame holding the payload
    reversed. Stop when the client closes the connection (ConnectionError from read_frame)."""

    def handle(self) -> None:
        raise NotImplementedError("TODO")


def port_roundtrip(payloads: list[bytes]) -> list[bytes]:
    """Start socketserver.ThreadingTCPServer(("127.0.0.1", 0), ReversingPort) in a daemon thread
    (serve_forever). Open ONE client connection, and for each payload send its frame and read
    the reply frame. Close the client, shutdown() and server_close() the server, return the
    replies."""
    raise NotImplementedError("TODO")


def pair_echo(chunks: list[bytes]) -> bytes:
    """Make a socket.socketpair(). Send every chunk on one end, then shut down its write side
    (a.shutdown(socket.SHUT_WR)). Read from the other end until b"" and return everything."""
    raise NotImplementedError("TODO")


def udp_ping(payload: bytes) -> tuple[bytes, bool]:
    """Bind a UDP socket on 127.0.0.1 port 0, send payload to it from a second UDP socket,
    recvfrom (timeout 2 s). Return (data, whether the sender's address is loopback)."""
    raise NotImplementedError("TODO")


def drain_ready(socks: list[socket.socket], timeout: float) -> dict[int, bytes]:
    """Register every socket with a selectors.DefaultSelector (data = its index in socks).
    Call select(timeout) ONCE and recv(4096) from each ready socket.
    Return {index: bytes received}. Unregister everything and close the selector."""
    raise NotImplementedError("TODO")


def port_context() -> ssl.SSLContext:
    """ssl.create_default_context() with minimum_version TLS 1.2."""
    raise NotImplementedError("TODO")


def in_coil_net(addr: str) -> bool:
    """Is addr inside COIL_NET? Invalid addresses raise ValueError."""
    raise NotImplementedError("TODO")


def coil_subnets(prefix: int) -> list[str]:
    """COIL_NET split into subnets of the given prefix length, as strings."""
    raise NotImplementedError("TODO")


def address_kind(addr: str) -> str:
    """"loopback", "private", or "global" (checked in that order), else "other"."""
    raise NotImplementedError("TODO")

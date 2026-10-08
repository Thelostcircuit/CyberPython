# 25 // WIRE TAP

```
[PYTHIA-9] intake port protocol: "OUROLINK/1" ── transport: TCP ── framing: length-prefixed ── docs: 50%
```

**Modules:** `socket`, `socketserver`, `selectors`, `ssl`, `ipaddress`

Iris's notes on the intake port stop halfway down a page. What she got down: it's TCP, every
message is a 4-byte big-endian length followed by that many bytes, and the port answers each
message with one of its own. The rest you'll have to work out by building a copy of the port
and talking to it.

> **MONTY:** Everything on a network, from HTTP and email to video calls and BASILISK itself,
> is built on **sockets**: a pair of endpoints trading bytes. TCP gives you a reliable,
> ordered *stream*. UDP gives you individual *datagrams* that may or may not arrive. The
> classic mistake with TCP is assuming one `send` equals one `recv`. It doesn't. A stream has
> no message boundaries, which is exactly why the port **frames** its messages with a length.

---

## ▓ TECH BRIEFING

### TCP clients and servers with `socket`

```python
import socket
# server
srv = socket.create_server(("127.0.0.1", 0))      # port 0: the OS picks a free port
port = srv.getsockname()[1]
conn, addr = srv.accept()                           # blocks until a client connects
data = conn.recv(4096)                              # up to 4096 bytes: MAYBE fewer!
conn.sendall(b"reply")                              # sendall loops until everything is sent
conn.close()

# client
with socket.create_connection(("127.0.0.1", port), timeout=5) as s:
    s.sendall(b"hello")
    s.recv(4096)                                    # b'' means the other side closed
```

`recv(n)` returns *whatever has arrived*, anywhere from 1 to n bytes. To read exactly n bytes,
loop until you have them. Other useful pieces: `socket.socketpair()` (two connected sockets,
great for tests), `settimeout()`, `setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)`, and
`socket.getaddrinfo(host, port)` (DNS).

### UDP

```python
rx = socket.socket(socket.AF_INET, socket.SOCK_DGRAM); rx.bind(("127.0.0.1", 0))
tx = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
tx.sendto(b"ping", rx.getsockname())
data, sender = rx.recvfrom(1024)                    # one datagram, with its sender
```

### Framing with `struct`

```python
import struct
def frame(payload: bytes) -> bytes:
    return struct.pack("!I", len(payload)) + payload
```

### `socketserver`

A framework for servers. You write a request handler class, and it does the accept loop:

```python
import socketserver, threading
class Handler(socketserver.BaseRequestHandler):
    def handle(self):                    # self.request is the connected socket
        data = self.request.recv(1024)
        self.request.sendall(data.upper())

srv = socketserver.ThreadingTCPServer(("127.0.0.1", 0), Handler)   # a thread per client
threading.Thread(target=srv.serve_forever, daemon=True).start()
...
srv.shutdown(); srv.server_close()
```

`StreamRequestHandler` gives you `self.rfile`/`self.wfile` file objects. There's
`UDPServer` too, and `ForkingTCPServer` on Unix.

### `selectors`: many sockets, one thread

```python
import selectors
sel = selectors.DefaultSelector()                   # epoll/kqueue/select, whichever is best here
sel.register(sock, selectors.EVENT_READ, data="client-1")
for key, events in sel.select(timeout=1):
    key.fileobj.recv(4096), key.data
sel.unregister(sock); sel.close()
```

That's how event loops (including asyncio's) work underneath. Put sockets in non-blocking
mode (`sock.setblocking(False)`) when you drive them this way.

### `ssl`: TLS

```python
import ssl
ctx = ssl.create_default_context()                  # secure defaults: verify certs AND hostnames
with socket.create_connection(("example.org", 443)) as raw:
    with ctx.wrap_socket(raw, server_hostname="example.org") as tls:
        tls.version()                                # 'TLSv1.3'
ctx.minimum_version = ssl.TLSVersion.TLSv1_2
```

Don't turn off `check_hostname` or set `verify_mode = CERT_NONE` to "make an error go away".
That's how you end up talking to an impostor.

### `ipaddress`

```python
import ipaddress
ip = ipaddress.ip_address("10.4.17.3")
net = ipaddress.ip_network("10.4.0.0/16")
ip in net                         # True
net.num_addresses, net.netmask, list(net.subnets(new_prefix=18))
ip.is_private, ip.is_loopback, ip.is_global, ip.version
ipaddress.ip_interface("10.4.17.3/24").network
list(ipaddress.summarize_address_range(first, last))
```

---

## ▓ THE JOB

Everything runs on `127.0.0.1` (your own machine). In `job.py`:

1. **`frame(payload)`**, **`recv_exact(sock, n)`** and **`read_frame(sock)`**: OUROLINK framing done right.
2. **`port_roundtrip(payloads)`**: run a copy of the intake port (a `ThreadingTCPServer` whose handler answers each frame with the payload *reversed*), send every payload over one connection, and return the replies.
3. **`pair_echo(chunks)`**: over a `socketpair`, send several chunks and read them all back as one bytes object.
4. **`udp_ping(payload)`**: one datagram over loopback. Return `(data, sender_is_loopback)`.
5. **`drain_ready(socks, timeout)`**: use `selectors` to read whatever is waiting on any of several sockets.
6. **`port_context()`**: an `ssl` client context with secure defaults and TLS 1.2 or newer.
7. **`in_coil_net(addr)`**, **`coil_subnets(prefix)`** and **`address_kind(addr)`**: `ipaddress`.

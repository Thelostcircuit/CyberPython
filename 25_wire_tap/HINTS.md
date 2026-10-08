# HINTS // 25 WIRE TAP

## recv_exact
<details><summary>Hint</summary>

```python
buf = bytearray()
while len(buf) < n:
    chunk = sock.recv(n - len(buf))
    if not chunk:
        raise ConnectionError(...)
    buf += chunk
```
</details>

## read_frame
<details><summary>Hint</summary>

`(length,) = struct.unpack("!I", recv_exact(sock, 4))`, then `recv_exact(sock, length)`.
</details>

## ReversingPort.handle
<details><summary>Hint</summary>

Loop forever. `read_frame(self.request)` in a `try`, and `return` on `ConnectionError`,
which is how you notice the client hung up. Reply with `self.request.sendall(frame(p[::-1]))`.
</details>

## port_roundtrip
<details><summary>Hint</summary>

`srv.server_address` is the `(host, port)` to connect to. Start
`threading.Thread(target=srv.serve_forever, daemon=True)`, and in a `finally` call
`srv.shutdown()` then `srv.server_close()`.
</details>

## pair_echo
<details><summary>Hint</summary>

`a.shutdown(socket.SHUT_WR)` tells the other side "no more data", so its `recv` returns `b""`
once it has read everything. `while chunk := b.recv(4096): ...`
</details>

## drain_ready
<details><summary>Hint</summary>

`sel.register(s, selectors.EVENT_READ, data=i)`. `sel.select(timeout)` returns
`(key, events)` pairs, and `key.fileobj` is the socket.
</details>

## ipaddress
<details><summary>Hint</summary>

`ipaddress.ip_address(addr) in COIL_NET`, `COIL_NET.subnets(new_prefix=prefix)`, and the
`.is_loopback` / `.is_private` / `.is_global` properties.
</details>

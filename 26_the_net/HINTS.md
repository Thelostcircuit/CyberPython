# HINTS // 26 THE NET

## portal_url / query_params / status_line
<details><summary>Hint</summary>

`urljoin(base, path)` then append `"?" + urlencode(params)`.
`{k: v[0] for k, v in parse_qs(urlparse(url).query).items()}`.
`s = HTTPStatus(code)`, then `f"{s.value} {s.phrase}"`.
</details>

## PortalHandler
<details><summary>Hint 1</summary>

Write a helper, `send_json(self, status, data, cookie=None)`, that encodes the body and calls
`send_response`, `send_header` (Content-Type, Content-Length, and Set-Cookie if given),
`end_headers`, then `self.wfile.write(body)`.
</details>
<details><summary>Hint 2</summary>

In `do_POST`: `length = int(self.headers.get("Content-Length", 0))`, then
`parse_qs(self.rfile.read(length).decode())`. Check `self.path` to route.
</details>
<details><summary>Hint 3</summary>

Override `def log_message(self, format, *args): pass` to keep the test output clean.
</details>

## fetch_json
<details><summary>Hint</summary>

`except urllib.error.HTTPError as e:`. The error object is also a response, so `e.code` and
`e.read()` work.
</details>

## lodge_order
<details><summary>Hint</summary>

`conn.request("POST", "/orders", body=urlencode({...}), headers={...})`,
`resp = conn.getresponse()`. Read the body *before* closing. Load
`resp.getheader("Set-Cookie") or ""` into a `SimpleCookie`.
</details>

## robots_allowed
<details><summary>Hint</summary>

`rp = urllib.robotparser.RobotFileParser(); rp.parse(robots_txt.splitlines()); rp.can_fetch(agent, url)`
</details>

## confirmation / read_confirmation
<details><summary>Hint</summary>

`mimetypes.guess_type(name)` returns `(type or None, encoding)`. Split the type on `/` for
`add_attachment(data, maintype=..., subtype=..., filename=...)`. When parsing, use
`msg.get_body(("plain",)).get_content()` and `msg.iter_attachments()`.
</details>

## archive_and_list
<details><summary>Hint</summary>

`box = mailbox.mbox(path)`, `box.add(raw)` for each message, `box.flush()`, then
`[m["Subject"] for m in box]`. Close it in a `finally`.
</details>

## rpc_pow
<details><summary>Hint</summary>

`srv.register_function(pow)`, serve it in a daemon thread, and call
`ServerProxy(f"http://127.0.0.1:{port}/").pow(a, b)`. Shut down in `finally`.
</details>

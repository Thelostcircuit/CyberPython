# 26 // THE NET

```
[PYTHIA-9] target: portal.ouro.internal ── HTTP/1.1 ── sessions: cookie ── confirmations: SMTP ✉
```

**Modules:** `urllib.*`, `http.*`, `wsgiref`, `email`, `smtplib`, `imaplib`, `poplib`, `ftplib`, `mailbox`, `mimetypes`, `xmlrpc`, `webbrowser`

The last piece of bureaucracy between you and the release: the **Ouroboros Orders Portal**,
an internal website where engineers lodge release orders. You fill in a form, it sets a
session cookie, it gives you an order number, and a confirmation email arrives with a PDF
receipt attached.

> **MONTY:** HTTP is just text over a socket: a request line, headers, a blank line, a body.
> Email is the same kind of thing, just older and stranger. Python can be the client *and* the
> server for both. So we'll build a working copy of the portal on this machine, and then write
> the client that talks to it. When we point that client at the real thing, nothing will
> surprise us.

---

## ▓ TECH BRIEFING

### `urllib.parse`: URLs

```python
from urllib.parse import urlparse, urlencode, parse_qs, urljoin, quote, unquote
u = urlparse("https://portal.ouro/orders?id=7&rack=C-17#top")
u.scheme, u.netloc, u.path, u.query, u.fragment
parse_qs(u.query)                           # {'id': ['7'], 'rack': ['C-17']}  (lists!)
urlencode({"q": "iris vale", "n": 3})       # 'q=iris+vale&n=3'
urljoin("https://portal.ouro/api/", "orders")   # 'https://portal.ouro/api/orders'
quote("C-17/rack 2", safe="")               # 'C-17%2Frack%202'
```

### `urllib.request` and `urllib.error`: a built-in HTTP client

```python
import urllib.request, urllib.error, json
with urllib.request.urlopen("http://127.0.0.1:8000/status", timeout=5) as r:
    r.status, r.headers["Content-Type"], json.load(r)

req = urllib.request.Request(url, data=b"a=1", method="POST",
                             headers={"Content-Type": "application/x-www-form-urlencoded"})
try:
    urllib.request.urlopen(req)
except urllib.error.HTTPError as e:         # 4xx/5xx responses raise; e.code, e.read()
    ...
except urllib.error.URLError as e:          # couldn't connect at all
    ...
```

`urllib.robotparser.RobotFileParser` reads `robots.txt` and answers `can_fetch(agent, url)`.
(For real-world HTTP, most people use **requests**, which is ch 33.)

### `http`: status codes, the low-level client, the server, cookies

```python
from http import HTTPStatus
HTTPStatus.NOT_FOUND.value, HTTPStatus(201).phrase         # 404, 'Created'

import http.client
conn = http.client.HTTPConnection("127.0.0.1", port, timeout=5)
conn.request("POST", "/orders", body="subject=OS-ENG-4471", headers={...})
resp = conn.getresponse(); resp.status, resp.getheader("Set-Cookie"), resp.read()

from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        body = b'{"status": "up"}'
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)
    def do_POST(self):
        length = int(self.headers["Content-Length"])
        form = self.rfile.read(length)
    def log_message(self, *args): pass     # silence the default stderr logging
server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
```

`python -m http.server` serves the current folder, which is handy for quick file sharing.

```python
from http.cookies import SimpleCookie
c = SimpleCookie(); c.load("session=abc123; Path=/"); c["session"].value   # 'abc123'
```

`http.cookiejar.CookieJar` with `urllib.request.HTTPCookieProcessor` keeps cookies across
requests automatically, like a browser does.

### `wsgiref`: the WSGI standard

WSGI is the interface between Python web apps and servers (Flask, ch 40, is a WSGI app):

```python
def app(environ, start_response):
    start_response("200 OK", [("Content-Type", "text/plain")])
    return [b"hello " + environ["PATH_INFO"].encode()]

from wsgiref.simple_server import make_server        # a reference server
from wsgiref.util import setup_testing_defaults      # a fake environ for tests
```

### `email`, `mimetypes`, and the mail protocols

```python
from email.message import EmailMessage
msg = EmailMessage()
msg["From"], msg["To"], msg["Subject"] = "portal@ouro", "i.vale@ouro", "Order 7 lodged"
msg.set_content("Your order has been lodged.")
msg.add_attachment(pdf_bytes, maintype="application", subtype="pdf", filename="receipt.pdf")
raw = msg.as_bytes()

import email, email.policy
parsed = email.message_from_bytes(raw, policy=email.policy.default)
parsed["Subject"], parsed.get_body(("plain",)).get_content()
for part in parsed.iter_attachments(): part.get_filename()

import mimetypes
mimetypes.guess_type("receipt.pdf")      # ('application/pdf', None)
```

Sending and receiving use protocol modules. They follow the same pattern: connect, log in,
do things, quit.

```python
import smtplib
with smtplib.SMTP("mail.example", 587) as s:
    s.starttls(); s.login(user, password); s.send_message(msg)
# imaplib.IMAP4_SSL (read mail on the server), poplib.POP3_SSL (download mail),
# ftplib.FTP / FTP_TLS (file transfer). All support context managers.
```

`mailbox` reads and writes local mail stores (`mbox`, `Maildir`, ...).

### `xmlrpc` and `webbrowser`

```python
from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.client import ServerProxy
srv = SimpleXMLRPCServer(("127.0.0.1", 0), logRequests=False); srv.register_function(pow)
ServerProxy(f"http://127.0.0.1:{port}/").pow(2, 10)     # remote procedure call over HTTP + XML

import webbrowser
webbrowser.open("https://docs.python.org")               # open the user's browser
```

---

## ▓ THE JOB

Everything runs locally. In `job.py`:

1. **`portal_url(base, path, **params)`**: join and encode a URL.
2. **`query_params(url)`**: `{key: first value}` from a URL's query string.
3. **`status_line(code)`**: `"404 Not Found"` from `HTTPStatus`.
4. **`PortalHandler`**: `GET /status` returns JSON. `POST /orders` takes a form, returns 201 with JSON and a session cookie. Anything else is a 404 with a JSON error.
5. **`start_portal()`**: start it in a background thread, and return `(server, port)`.
6. **`fetch_json(url)`**: `(status, data)` via `urllib.request`, including for error statuses.
7. **`lodge_order(port, subject)`**: `POST` with `http.client`, returning `(status, order, session_cookie)`.
8. **`robots_allowed(robots_txt, url)`**: `urllib.robotparser`.
9. **`hello_app`**: a WSGI app.
10. **`confirmation(to, order, receipt_name, receipt)`** / **`read_confirmation(raw)`**: build and parse an email with an attachment, using `mimetypes` for its type.
11. **`archive_and_list(path, messages)`**: store messages in an `mbox`, then list their subjects.
12. **`rpc_pow(a, b)`**: call `pow` across `xmlrpc`.

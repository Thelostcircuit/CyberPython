"""A fake Ouroboros API for the tests. Runs on 127.0.0.1 in a background thread."""

import json
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse

TOKEN = "k-4471"


class Handler(BaseHTTPRequestHandler):
    flaky_hits = 0

    def log_message(self, *args):
        pass

    def send(self, status, body=b"", ctype="application/json", headers=()):
        if isinstance(body, (dict, list)):
            body = json.dumps(body).encode()
        self.send_response(status)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        for k, v in headers:
            self.send_header(k, v)
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        url = urlparse(self.path)
        q = {k: v[0] for k, v in parse_qs(url.query).items()}
        if url.path == "/status":
            self.send(200, {"status": "up", "shift": 11})
        elif url.path == "/search":
            self.send(200, {"query": q})
        elif url.path == "/slow":
            time.sleep(2)
            self.send(200, {"ok": True})
        elif url.path == "/missing":
            self.send(404, {"error": "no such rack"})
        elif url.path == "/me":
            cookie = self.headers.get("Cookie", "")
            if "session=iris-ok" in cookie:
                self.send(200, {"name": "I. Vale", "role": "lead systems engineer"})
            else:
                self.send(401, {"error": "login required"})
        elif url.path == "/blob":
            self.send(200, bytes(range(256)) * 400, ctype="application/octet-stream")
        elif url.path == "/flaky":
            Handler.flaky_hits += 1
            if Handler.flaky_hits % 3:
                self.send(503, {"error": "busy"})
            else:
                self.send(200, {"ok": True, "hits": Handler.flaky_hits})
        elif url.path == "/old":
            self.send(301, headers=[("Location", "/older")])
        elif url.path == "/older":
            self.send(302, headers=[("Location", "/status")])
        else:
            self.send(404, {"error": "not found"})

    def do_POST(self):
        url = urlparse(self.path)
        length = int(self.headers.get("Content-Length", 0))
        raw = self.rfile.read(length)
        if url.path == "/orders":
            if self.headers.get("Authorization") != f"Bearer {TOKEN}":
                self.send(403, {"error": "bad token"})
                return
            if self.headers.get("Content-Type") != "application/json":
                self.send(415, {"error": "json only"})
                return
            data = json.loads(raw)
            self.send(201, {"order": 7, "subject": data["subject"]})
        elif url.path == "/login":
            form = {k: v[0] for k, v in parse_qs(raw.decode()).items()}
            if form == {"user": "iris", "password": "first-light"}:
                self.send(200, {"ok": True}, headers=[("Set-Cookie", "session=iris-ok; Path=/")])
            else:
                self.send(401, {"error": "bad login"})
        else:
            self.send(404, {"error": "not found"})


class FakeOuro:
    def __enter__(self):
        Handler.flaky_hits = 0
        self.server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        self.server.daemon_threads = True
        threading.Thread(target=self.server.serve_forever, daemon=True).start()
        self.base = f"http://127.0.0.1:{self.server.server_address[1]}"
        return self

    def __exit__(self, *exc):
        self.server.shutdown()
        self.server.server_close()

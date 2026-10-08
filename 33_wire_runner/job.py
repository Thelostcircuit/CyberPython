"""33 // WIRE RUNNER: HTTP with requests.

The fake Ouroboros API (started by the tests) has these routes:
  GET  /status            -> {"status": "up", "shift": 11}
  GET  /search?...        -> {"query": {the query parameters}}
  GET  /slow              -> answers after 2 seconds
  GET  /missing           -> 404
  POST /orders            -> JSON body {"subject": ...}; needs "Authorization: Bearer <token>";
                             201 {"order": 7, "subject": ...}, 403 on a bad token
  POST /login             -> form user=...&password=...; sets cookie "session" on success
  GET  /me                -> 200 {"name": ...} with the session cookie, else 401
  GET  /blob              -> 102,400 bytes of binary
  GET  /flaky             -> 503, 503, then 200 {"ok": true, ...}
  GET  /old               -> redirects to /older, which redirects to /status
"""

from pathlib import Path

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

TIMEOUT = 5


def status(base: str) -> str:
    raise NotImplementedError("TODO")


def search(base: str, **params: str) -> dict:
    """GET /search with `params` as the query string; return the "query" field of the reply."""
    raise NotImplementedError("TODO")


def lodge(base: str, subject: str, token: str) -> dict:
    """POST /orders with json={"subject": subject} and a Bearer token. raise_for_status(),
    then return the JSON reply."""
    raise NotImplementedError("TODO")


def probe(url: str, timeout: float) -> int | str:
    """GET url with the given timeout. Return the status code (any status, even 404),
    "timeout" on requests.Timeout, or "unreachable" on requests.ConnectionError."""
    raise NotImplementedError("TODO")


def whoami(base: str, user: str, password: str) -> str | None:
    """With a requests.Session: POST /login (form data), then GET /me. Return the "name" from
    /me, or None if /me isn't 200."""
    raise NotImplementedError("TODO")


def download(url: str, path: str | Path) -> int:
    """Stream the body to path in 4096-byte chunks (stream=True + iter_content); return the
    number of bytes written."""
    raise NotImplementedError("TODO")


def patient_get(url: str) -> dict:
    """A Session with HTTPAdapter(max_retries=Retry(total=5, backoff_factor=0,
    status_forcelist=[503])) mounted for "http://". GET url and return the JSON."""
    raise NotImplementedError("TODO")


def redirect_trail(url: str) -> tuple[str, int]:
    """(final URL after following redirects, number of redirects)."""
    raise NotImplementedError("TODO")

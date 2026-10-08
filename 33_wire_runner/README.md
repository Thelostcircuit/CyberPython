# 33 // WIRE RUNNER

```
[CHEESE SHOP] Tier 40 skybridge ── proprietor: Wensleydale ── stock: 600,000+ packages ── purchase: requests
```

**Package:** [`requests`](https://requests.readthedocs.io): HTTP for humans. (`uv sync` has already installed it.)

The Cheese Shop is a long, narrow stall on a skybridge that sways in the wind. The shelves are
lined with glowing data cartridges, each one labelled by hand. Behind the counter a thin,
nervous man in an apron polishes a cartridge that's already spotless.

> **WENSLEYDALE:** Good morning, good morning! Welcome to the finest package emporium in
> Coilhaven. What'll it be?
>
> **MONTY:** Do you have anything for HTTP? Something friendlier than `urllib`?
>
> **WENSLEYDALE:** *(brightening)* Ah, **requests**! Our most popular line. Pulled off the shelf
> a billion times a year. Everyone who's anyone talks HTTP through requests. Sessions, cookies,
> JSON, retries, streaming, all done for you.
>
> **DEX:** Wait, you actually *have* it? I heard this shop never has anything.
>
> **WENSLEYDALE:** That was a different shop, sir. A *very* different shop.

---

## ▓ TECH BRIEFING

### The basics

```python
import requests
r = requests.get("https://portal.ouro/status", timeout=5)   # ALWAYS pass a timeout
r.status_code          # 200
r.ok                   # True for status < 400
r.headers["Content-Type"]
r.text                 # the decoded body
r.json()               # the body parsed as JSON
r.content              # the raw bytes
r.url, r.history       # the final URL after redirects, and the redirect responses
r.raise_for_status()   # raises requests.HTTPError for 4xx/5xx
```

Compare that with ch 26's `urllib` version. That's why requests exists.

### Sending data

```python
requests.get(url, params={"rack": "C-17", "n": 3})       # → ?rack=C-17&n=3, properly encoded
requests.post(url, json={"subject": "OS-ENG-4471"})       # a JSON body + Content-Type header
requests.post(url, data={"user": "iris"})                 # form-encoded
requests.post(url, files={"receipt": open("r.pdf", "rb")})
requests.get(url, headers={"Authorization": "Bearer abc123"})
requests.get(url, auth=("user", "pass"))                  # HTTP basic auth
```

### Sessions

A `Session` keeps cookies, default headers and connection pools across requests, just like a
browser. Use one whenever you make more than a couple of calls to the same place.

```python
with requests.Session() as s:
    s.headers["User-Agent"] = "pythia-9"
    s.post(f"{base}/login", data={"user": "iris", "password": "..."})   # server sets a cookie
    s.get(f"{base}/me")                                                 # the cookie is sent back automatically
    s.cookies.get("session")
```

### Errors

```python
from requests.exceptions import Timeout, ConnectionError, HTTPError, RequestException
try:
    requests.get(url, timeout=0.5).raise_for_status()
except Timeout: ...            # too slow
except ConnectionError: ...    # nobody answered (DNS failure, connection refused...)
except HTTPError as e: e.response.status_code
except RequestException: ...   # the base class of all of the above
```

### Streaming and retries

```python
with requests.get(url, stream=True, timeout=10) as r:     # don't load a big body into memory
    for chunk in r.iter_content(chunk_size=8192):
        f.write(chunk)

from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry                        # urllib3 is requests' engine
retry = Retry(total=3, backoff_factor=0.1, status_forcelist=[502, 503, 504])
s = requests.Session(); s.mount("http://", HTTPAdapter(max_retries=retry))
```

---

## ▓ THE JOB

The tests start a fake Ouroboros API on `127.0.0.1`. Its routes are listed in `job.py`.
Using **requests**:

1. **`status(base)`**: GET `/status` and return the `"status"` field.
2. **`search(base, **params)`**: GET `/search` with query parameters, and return the echoed `"query"` dict.
3. **`lodge(base, subject, token)`**: POST JSON with a bearer token, raising on HTTP errors.
4. **`probe(url, timeout)`**: classify the result as a status code, `"timeout"`, or `"unreachable"`.
5. **`whoami(base, user, password)`**: log in with a `Session` and call `/me` with the cookie.
6. **`download(url, path)`**: stream to disk in chunks, and return the bytes written.
7. **`patient_get(url)`**: a `Session` with retries on 503.
8. **`redirect_trail(url)`**: `(final_url, number_of_redirects)`.

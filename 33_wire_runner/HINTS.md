# HINTS // 33 WIRE RUNNER

## status / search
<details><summary>Hint</summary>

`requests.get(f"{base}/status", timeout=5).json()["status"]`. For search, pass
`params=params`, and requests encodes `&` and spaces for you.
</details>

## lodge
<details><summary>Hint</summary>

`requests.post(url, json={...}, headers={"Authorization": f"Bearer {token}"}, timeout=5)`,
then `r.raise_for_status()`. `json=` sets the Content-Type header for you.
</details>

## probe
<details><summary>Hint</summary>

`requests.Timeout` and `requests.ConnectionError` are the exceptions to catch. A 404 is *not*
an exception unless you call `raise_for_status()`, so don't.
</details>

## whoami
<details><summary>Hint</summary>

`with requests.Session() as s:`, then `s.post(... data={...})` and `s.get(...)`. The Session
stores the `Set-Cookie` and sends it back to you automatically.
</details>

## download
<details><summary>Hint</summary>

`with requests.get(url, stream=True, timeout=5) as r, open(path, "wb") as f:` then
`for chunk in r.iter_content(chunk_size=4096): written += f.write(chunk)`.
</details>

## patient_get
<details><summary>Hint</summary>

`s.mount("http://", HTTPAdapter(max_retries=Retry(total=5, backoff_factor=0,
status_forcelist=[503])))`
</details>

## redirect_trail
<details><summary>Hint</summary>

requests follows redirects by default. `r.url` is where you ended up, and `r.history` is the
list of redirect responses along the way.
</details>

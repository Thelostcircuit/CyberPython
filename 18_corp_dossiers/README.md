# 18 // CORP DOSSIERS

```
[PYTHIA-9] input: adder_stash/ ── dossiers: 212 ── formats: .json .csv .toml .ini .plist .bin .b64
```

**Modules:** `json`, `csv`, `tomllib`, `configparser`, `plistlib`, `netrc`, `struct`, `base64`, `binascii`, `quopri`

Mother Adder's "few dossiers" turn out to be a filing cabinet's worth of stolen Ouroboros
paperwork, bought, bartered and fished out of recycling bins over two decades. Personnel
records, config files from old acquisitions, and, crucially, a dozen real intake-port
manifests to copy the format from.

> **MONTY:** Every format here is in my library. Text formats for people: JSON, CSV, TOML, INI.
> Binary formats for machines: `struct` packs numbers into exact byte layouts. And the
> wrappers that let binary travel through text-only channels: base64, hex, quoted-printable.
> Read them all, write them all, and never parse one by hand when there's a module for it.

---

## ▓ TECH BRIEFING

### `json`

```python
import json
json.dumps({"id": 7, "tags": ["a"]})                  # '{"id": 7, "tags": ["a"]}'
json.dumps(obj, indent=2, sort_keys=True)
json.dumps(obj, default=str)                          # called for anything json can't encode
json.loads('{"x": 1.10}', parse_float=Decimal)        # exact decimals
json.loads(text, object_hook=lambda d: ...)           # transform every decoded dict
json.dump(obj, f); json.load(f)                       # file versions
```

JSON types: object ↔ `dict` (string keys only), array ↔ `list`, string, number ↔
`int`/`float`, `true`/`false` ↔ `True`/`False`, `null` ↔ `None`. Tuples come back as lists.
There's no date type: pick ISO strings. `python -m json` pretty-prints from the command line.

### `csv`

```python
import csv, io
rows = list(csv.DictReader(io.StringIO(text)))        # each row is {header: value} (all strings!)
out = io.StringIO()
w = csv.DictWriter(out, fieldnames=["id", "name"], lineterminator="\n")
w.writeheader(); w.writerows(rows)
csv.reader / csv.writer                               # the list-based versions
```

Open CSV files with `newline=""`. The module handles quoting, embedded commas and newlines
(`csv.QUOTE_MINIMAL` and friends). `csv.Sniffer` guesses dialects.

### `tomllib` (read-only TOML)

```python
import tomllib
cfg = tomllib.loads('[server]\nport = 8080\ntags = ["a"]')
with open("pyproject.toml", "rb") as f: cfg = tomllib.load(f)   # BINARY mode
```

TOML has real types: ints, floats, bools, dates, arrays and tables. The stdlib can only *read*
it (this course's own `pyproject.toml` is TOML).

### `configparser` (INI files)

```python
import configparser
cp = configparser.ConfigParser()
cp.read_string("[db]\nhost = vault\nport = 5432\n")
cp["db"]["host"], cp.getint("db", "port"), cp.getboolean("db", "tls", fallback=False)
cp.sections()
```

Values are strings. `[DEFAULT]` keys are inherited by every section, and `%(name)s`
interpolates other keys.

### `plistlib` and `netrc`

```python
import plistlib
plistlib.dumps({"a": 1}, fmt=plistlib.FMT_BINARY);  plistlib.loads(blob)   # Apple property lists

import netrc
netrc.netrc("path/.netrc").authenticators("host")   # (login, account, password) or None
```

`.netrc` holds credentials for FTP and HTTP tools. `netrc` checks the file's permissions,
because credentials files must not be world-readable.

### `struct`: exact binary layouts

```python
import struct
fmt = "!4sBHI"                   # ! network byte order (big-endian), 4-byte string, uchar, ushort, uint
struct.calcsize(fmt)             # 11
blob = struct.pack(fmt, b"OURO", 1, 0x0003, 3_610_000)
magic, version, flags, length = struct.unpack(fmt, blob)
struct.unpack_from(fmt, buffer, offset)
struct.iter_unpack("<H", data)   # repeated records
```

Byte order: `<` little, `>` or `!` big, `=` native. Codes: `b/B` 1 byte, `h/H` 2, `i/I` 4,
`q/Q` 8, `f` 4-byte float, `d` 8-byte float, `s` bytes, `?` bool, `x` padding.

### `base64`, `binascii`, `quopri`

```python
import base64, binascii, quopri
base64.b64encode(b"\xff\xfe") ; base64.b64decode("//4=")
base64.urlsafe_b64encode(data)          # - and _ instead of + and / (safe in URLs)
base64.b32encode, base64.b16encode, base64.b85encode, base64.a85encode

binascii.hexlify(b"\xde\xad", " ")      # b'de ad'
binascii.unhexlify("dead"), binascii.crc32(data)

quopri.decodestring(b"caf=C3=A9")       # b'caf\xc3\xa9'   quoted-printable (email bodies)
```

---

## ▓ THE JOB

In `job.py`:

1. **`to_json(obj)`**: sorted keys, indent 2. Datetimes become ISO strings and sets become sorted lists (a `default=` function).
2. **`load_amounts(text)`**: parse JSON with `parse_float=Decimal`.
3. **`read_roster(text)`**: CSV → list of dicts, with the `clearance` column converted to `int`.
4. **`write_roster(rows, fields)`**: list of dicts → CSV text with `\n` line endings.
5. **`toml_server(text)`**: `(host, port)` from a `[server]` table.
6. **`ini_settings(text)`**: every section as a dict, including values inherited from `[DEFAULT]`.
7. **`plist_roundtrip(obj)`**: through binary plist and back.
8. **`netrc_login(path, host)`**: `(login, password)` or `None`.
9. **`pack_manifest(...)`** / **`unpack_manifest(blob)`**: the port's binary header, using `struct`.
10. **`wrap(data)`** / **`unwrap(text)`**: URL-safe base64.
11. **`hex_pairs(data)`**: `"de ad be ef"` via `binascii`.
12. **`decode_qp(raw)`**: quoted-printable bytes → text.

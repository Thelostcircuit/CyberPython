# 19 // CIPHER ROOM

```
[PYTHIA-9] subject: Ouroboros release-order signatures ── scheme: HMAC-SHA256 ── keys held: 0
```

**Modules:** `hashlib`, `hmac`, `secrets`, `uuid`

The "cipher room" is what Dex calls the corner of the hideout where MONTY spreads Voss's
personnel file across three screens. Ouroboros release orders are signed. Every order carries
a tag computed from its exact text and a secret key. Change one character of the order and
the tag no longer matches. Without a key, you can't produce a valid tag.

> **SABLE:** So we need Voss's key.
>
> **MONTY:** Or *another* key the system trusts. Let's read the protocol properly before we
> decide. There's an emergency clause in there somewhere. First, though, you need to
> understand what these tools actually do. Hashes are fingerprints. HMACs are fingerprints
> only a key-holder can make. And secure random tokens are numbers nobody can predict.
> Get any of them subtly wrong and the whole thing falls apart.

---

## ▓ TECH BRIEFING

### `hashlib`: cryptographic hashes

A hash maps any amount of data to a fixed-size fingerprint. It's one-way, and even a tiny
change produces a completely different result.

```python
import hashlib
hashlib.sha256(b"release order").hexdigest()     # 64 hex chars
h = hashlib.sha256()                              # incremental: feed it chunks
h.update(b"part 1"); h.update(b"part 2"); h.digest()   # raw bytes
hashlib.file_digest(f, "sha256")                  # hash an open binary file efficiently
hashlib.sha3_256, hashlib.blake2b(data, digest_size=16, key=b"...")
hashlib.algorithms_guaranteed
```

Use SHA-256 or better (or BLAKE2). MD5 and SHA-1 are broken for security. They're only OK as
non-security checksums.

### Storing passwords: slow, salted hashes

Never store a password, and never store a plain hash of one. Use a **salted, deliberately
slow** key-derivation function, so that stolen hashes are expensive to attack:

```python
salt = secrets.token_bytes(16)
key = hashlib.scrypt(pw.encode(), salt=salt, n=2**14, r=8, p=1)          # memory-hard
key = hashlib.pbkdf2_hmac("sha256", pw.encode(), salt, 600_000)          # the classic
# store (salt, key); to check a login, recompute with the same salt and compare
```

### `hmac`: keyed signatures

```python
import hmac
tag = hmac.new(key, msg, "sha256").hexdigest()
hmac.digest(key, msg, "sha256")                   # fast one-shot, raw bytes
hmac.compare_digest(tag, expected)                # CONSTANT-TIME comparison
```

Always compare secrets with `hmac.compare_digest` (or `secrets.compare_digest`), never `==`.
`==` stops at the first differing byte, and that timing difference leaks information about
the secret.

### `secrets`: randomness for security

```python
import secrets
secrets.token_bytes(32)          # 32 random bytes from the OS's secure source
secrets.token_hex(16)            # 32 hex chars
secrets.token_urlsafe(16)        # URL-safe text
secrets.choice(alphabet)         # unpredictable choice
secrets.randbelow(100)
```

`random` (ch 12) is predictable by design. Anything an attacker must not guess (session
tokens, reset links, keys, salts) comes from `secrets`.

### `uuid`

```python
import uuid
uuid.uuid4()                     # random:  UUID('9f1c...')  (use for IDs)
uuid.uuid5(uuid.NAMESPACE_URL, "https://ouro.corp/iris")   # deterministic from a name
uuid.uuid7()                     # 3.14: time-ordered, great for database keys
u = uuid.UUID("12345678-1234-5678-1234-567812345678"); u.hex, u.int, u.version, str(u)
```

`uuid1` embeds the machine's MAC address and a timestamp, so it leaks both. Prefer
`uuid4` or `uuid7`.

---

## ▓ THE JOB

In `job.py`:

1. **`fingerprint(data)`**: the SHA-256 hex digest.
2. **`file_fingerprint(path)`**: SHA-256 of a file, streamed through `hashlib.file_digest`.
3. **`sign(key, order)`** / **`verify(key, order, tag)`**: HMAC-SHA256 hex tags, verified in constant time.
4. **`hash_passphrase(passphrase, salt=None)`**: scrypt with a random 16-byte salt. Returns `(salt, key)`.
5. **`check_passphrase(passphrase, salt, key)`**: recompute and compare in constant time.
6. **`session_token()`**: a URL-safe token from `secrets` with 32 bytes of randomness.
7. **`sealed(key, payload)`** / **`unseal(key, blob)`**: a signed envelope, `payload_b64.tag`. Unsealing raises `ValueError` if the payload was tampered with.
8. **`subject_uuid(subject_id)`**: a stable `uuid5` for a subject ID, so the same ID always gives the same UUID.
9. **`new_record_id()`**: a time-ordered `uuid7` string.

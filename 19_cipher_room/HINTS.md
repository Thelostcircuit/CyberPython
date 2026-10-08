# HINTS // 19 CIPHER ROOM

## file_fingerprint
<details><summary>Hint</summary>

`with open(path, "rb") as f: return hashlib.file_digest(f, "sha256").hexdigest()`
</details>

## sign / verify
<details><summary>Hint</summary>

`hmac.new(key, order.encode("utf-8"), "sha256").hexdigest()`. To verify, recompute the tag
and use `hmac.compare_digest(expected, tag)`.
</details>

## hash_passphrase / check_passphrase
<details><summary>Hint</summary>

`salt = secrets.token_bytes(16)` when none is given. Then
`hashlib.scrypt(passphrase.encode(), salt=salt, **SCRYPT)`. Checking means recomputing with
the *stored* salt and comparing in constant time.
</details>

## sealed / unseal
<details><summary>Hint 1</summary>

Sealing: base64 the payload (`urlsafe_b64encode(...).decode("ascii")`) and HMAC the **raw
payload bytes**. Glue them together with a `.`.
</details>
<details><summary>Hint 2</summary>

Unsealing: `body, sep, tag = blob.rpartition(".")`. If `sep` is empty, raise. Decode the body,
recompute the tag, compare with `hmac.compare_digest`, and raise `ValueError` on a mismatch.
</details>

## uuids
<details><summary>Hint</summary>

`uuid.uuid5(SUBJECT_NAMESPACE, subject_id)` and `str(uuid.uuid7())`.
</details>

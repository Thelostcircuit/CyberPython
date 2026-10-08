"""19 // CIPHER ROOM: fingerprints, keyed signatures, and unpredictable tokens."""

import base64
import hashlib
import hmac
import secrets
import uuid
from pathlib import Path

SUBJECT_NAMESPACE = uuid.UUID("5d1f0a3e-7c2b-4f6a-9e1d-0b0c0aa1c0de")
SCRYPT = {"n": 2**14, "r": 8, "p": 1}


def fingerprint(data: bytes) -> str:
    """SHA-256 hex digest."""
    raise NotImplementedError("TODO")


def file_fingerprint(path: str | Path) -> str:
    """SHA-256 hex digest of a file's bytes, using hashlib.file_digest on the open file."""
    raise NotImplementedError("TODO")


def sign(key: bytes, order: str) -> str:
    """HMAC-SHA256 of the UTF-8 order text, as hex."""
    raise NotImplementedError("TODO")


def verify(key: bytes, order: str, tag: str) -> bool:
    """True if tag is the correct signature. Compare with hmac.compare_digest."""
    raise NotImplementedError("TODO")


def hash_passphrase(passphrase: str, salt: bytes | None = None) -> tuple[bytes, bytes]:
    """(salt, key). Generate a 16-byte salt with secrets if none is given.
    key = hashlib.scrypt(passphrase UTF-8, salt=salt, **SCRYPT)."""
    raise NotImplementedError("TODO")


def check_passphrase(passphrase: str, salt: bytes, key: bytes) -> bool:
    raise NotImplementedError("TODO")


def session_token() -> str:
    """A URL-safe token from 32 random bytes (secrets.token_urlsafe)."""
    raise NotImplementedError("TODO")


def sealed(key: bytes, payload: bytes) -> str:
    """f"{urlsafe_b64(payload)}.{hex HMAC-SHA256 of the payload bytes}" """
    raise NotImplementedError("TODO")


def unseal(key: bytes, blob: str) -> bytes:
    """Reverse of sealed(). Raise ValueError if the format is wrong or the tag doesn't match
    (compare in constant time)."""
    raise NotImplementedError("TODO")


def subject_uuid(subject_id: str) -> uuid.UUID:
    """uuid5 of subject_id in SUBJECT_NAMESPACE."""
    raise NotImplementedError("TODO")


def new_record_id() -> str:
    """str(uuid.uuid7())"""
    raise NotImplementedError("TODO")

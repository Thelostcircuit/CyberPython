import base64
import hashlib
import tempfile
import time
import unittest
import uuid
from pathlib import Path

import job

KEY = b"not-the-real-key"


class Hashes(unittest.TestCase):
    def test_fingerprint(self):
        self.assertEqual(job.fingerprint(b""),
                         "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855")
        self.assertNotEqual(job.fingerprint(b"order 1"), job.fingerprint(b"order 2"))

    def test_file_fingerprint(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "payload.bin"
            p.write_bytes(b"x" * 100_000)
            self.assertEqual(job.file_fingerprint(p), hashlib.sha256(b"x" * 100_000).hexdigest())


class Signatures(unittest.TestCase):
    def test_sign_verify(self):
        tag = job.sign(KEY, "RELEASE OS-ENG-4471")
        self.assertEqual(len(tag), 64)
        self.assertTrue(job.verify(KEY, "RELEASE OS-ENG-4471", tag))
        self.assertFalse(job.verify(KEY, "RELEASE OS-ENG-4472", tag))
        self.assertFalse(job.verify(b"other key", "RELEASE OS-ENG-4471", tag))

    def test_sealed(self):
        blob = job.sealed(KEY, b"release: C-17")
        self.assertEqual(job.unseal(KEY, blob), b"release: C-17")
        body, tag = blob.split(".")
        forged = base64.urlsafe_b64encode(b"release: ALL").decode() + "." + tag
        with self.assertRaises(ValueError):
            job.unseal(KEY, forged)
        with self.assertRaises(ValueError):
            job.unseal(b"wrong", blob)
        with self.assertRaises(ValueError):
            job.unseal(KEY, "no-dot-here")


class Passphrases(unittest.TestCase):
    def test_hash_and_check(self):
        salt, key = job.hash_passphrase("correct horse battery staple")
        self.assertEqual(len(salt), 16)
        self.assertTrue(job.check_passphrase("correct horse battery staple", salt, key))
        self.assertFalse(job.check_passphrase("Correct horse battery staple", salt, key))
        salt2, key2 = job.hash_passphrase("correct horse battery staple")
        self.assertNotEqual(salt, salt2)
        self.assertNotEqual(key, key2)
        self.assertEqual(job.hash_passphrase("x", b"0" * 16), job.hash_passphrase("x", b"0" * 16))


class Tokens(unittest.TestCase):
    def test_session_token(self):
        tokens = {job.session_token() for _ in range(50)}
        self.assertEqual(len(tokens), 50)
        t = tokens.pop()
        self.assertGreaterEqual(len(t), 43)
        self.assertTrue(set(t) <= set("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_"))

    def test_uuids(self):
        a = job.subject_uuid("OS-ENG-4471")
        self.assertEqual(a, job.subject_uuid("OS-ENG-4471"))
        self.assertNotEqual(a, job.subject_uuid("OS-ENG-4472"))
        self.assertEqual(a.version, 5)
        first = job.new_record_id()
        time.sleep(0.002)
        second = job.new_record_id()
        self.assertEqual(uuid.UUID(first).version, 7)
        self.assertLess(first, second)


if __name__ == "__main__":
    unittest.main()

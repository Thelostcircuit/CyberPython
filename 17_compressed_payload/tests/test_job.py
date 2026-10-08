import gzip
import io
import subprocess
import sys
import tarfile
import tempfile
import unittest
import zlib
from pathlib import Path

import job

DATA = (b"NEURAL-MAP " * 2000) + bytes(range(256)) * 4


class Compress(unittest.TestCase):
    def test_roundtrips(self):
        for algo in job.ALGOS:
            blob = job.pack(DATA, algo)
            self.assertLess(len(blob), len(DATA) // 5, algo)
            self.assertEqual(job.unpack(blob, algo), DATA, algo)
        self.assertEqual(job.pack(DATA, "gzip")[:2], b"\x1f\x8b")
        with self.assertRaises(ValueError):
            job.pack(DATA, "rar")
        with self.assertRaises(ValueError):
            job.unpack(b"", "rar")

    def test_best_algo(self):
        sizes = {a: len(job.pack(DATA, a)) for a in job.ALGOS}
        self.assertEqual(sizes[job.best_algo(DATA)], min(sizes.values()))

    def test_stream_pack(self):
        chunks = [DATA[i:i + 1000] for i in range(0, len(DATA), 1000)]
        self.assertEqual(zlib.decompress(job.stream_pack(chunks)), DATA)
        self.assertEqual(zlib.decompress(job.stream_pack([])), b"")

    def test_checksums(self):
        self.assertEqual(job.checksums(b"coil"), (zlib.crc32(b"coil"), zlib.adler32(b"coil")))
        self.assertEqual(job.checksums(b""), (0, 1))


class Archives(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.d = Path(self._tmp.name)

    def tearDown(self):
        self._tmp.cleanup()

    def test_gzip_file(self):
        (self.d / "log.txt").write_bytes(DATA)
        job.gzip_file(self.d / "log.txt", self.d / "log.txt.gz")
        self.assertEqual(gzip.decompress((self.d / "log.txt.gz").read_bytes()), DATA)

    def test_zip(self):
        job.build_zip(self.d / "p.zip", {"b/readme.txt": "hi", "a.txt": "x" * 5000})
        self.assertEqual(job.zip_manifest(self.d / "p.zip"), [("a.txt", 5000), ("b/readme.txt", 2)])
        import zipfile
        with zipfile.ZipFile(self.d / "p.zip") as z:
            self.assertEqual(z.getinfo("a.txt").compress_type, zipfile.ZIP_DEFLATED)

    def test_tar_roundtrip(self):
        src = self.d / "deep" / "release_v7"
        (src / "cfg").mkdir(parents=True)
        (src / "run.py").write_text("print('free')")
        (src / "cfg" / "map.bin").write_bytes(DATA)
        job.build_tar(self.d / "p.tar.xz", src)
        names = job.safe_extract(self.d / "p.tar.xz", self.d / "out")
        self.assertIn("release_v7/cfg/map.bin", names)
        self.assertEqual((self.d / "out" / "release_v7" / "cfg" / "map.bin").read_bytes(), DATA)
        with tarfile.open(self.d / "p.tar.xz") as t:
            self.assertTrue(all(n.startswith("release_v7") for n in t.getnames()))

    def test_safe_extract_blocks_escape(self):
        evil = self.d / "evil.tar"
        with tarfile.open(evil, "w") as t:
            info = tarfile.TarInfo("../escaped.txt")
            payload = b"gotcha"
            info.size = len(payload)
            t.addfile(info, io.BytesIO(payload))
        (self.d / "out").mkdir()
        with self.assertRaises(tarfile.FilterError):
            job.safe_extract(evil, self.d / "out")
        self.assertFalse((self.d / "escaped.txt").exists())

    def test_make_app(self):
        app = self.d / "app"
        app.mkdir()
        (app / "cli.py").write_text("def main():\n    print('release armed')\n")
        job.make_app(app, self.d / "release.pyz", "cli:main")
        run = subprocess.run([sys.executable, str(self.d / "release.pyz")],
                             capture_output=True, text=True)
        self.assertEqual(run.stdout, "release armed\n")


if __name__ == "__main__":
    unittest.main()

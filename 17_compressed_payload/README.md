# 17 // COMPRESSED PAYLOAD

```
[PYTHIA-9] payload: release_v7/ ── 41.8 MB ── intake port limit: 4.0 MB ── container: TBD
```

**Modules:** `zlib`, `gzip`, `bz2`, `lzma`, `compression.zstd`, `zipfile`, `tarfile`, `zipapp`

Iris's release program isn't one file. It's a folder of scripts, configuration, and a very
large table of neural-mapping data that is mostly repeated patterns. That's good news. Data
that repeats is data that compresses.

> **MONTY:** Python ships with five compression algorithms, each with its own trade-off
> between speed and size, plus the two big archive formats: zip and tar. There's even a way to
> turn a whole folder of Python into one runnable file. We'll pick the best algorithm for the
> job, pack the folder, and prove the package unpacks to exactly what we put in.
>
> One thing, though. When you unpack an archive someone *else* built, watch out for filenames
> like `../../etc/passwd`. A careless extractor will write straight through the floor.

---

## ▓ TECH BRIEFING

### The one-shot compressors

All five share the same basic shape: `compress(bytes) -> bytes` and `decompress(bytes) -> bytes`.

```python
import zlib, gzip, bz2, lzma
from compression import zstd                  # new in 3.14: Zstandard

zlib.compress(data, level=9)     # DEFLATE: fast, everywhere (zip, PNG, HTTP)
gzip.compress(data)              # DEFLATE plus a gzip header (.gz files)
bz2.compress(data)               # slower, often smaller on text
lzma.compress(data)              # xz: slow, usually the smallest
zstd.compress(data)              # zstd: very fast, and a great ratio
```

In 3.14 the new `compression` package groups them: `compression.zlib`, `compression.gzip`,
`compression.bz2`, `compression.lzma` and `compression.zstd`. The old top-level names still
work.

Checksums: `zlib.crc32(data)` and `zlib.adler32(data)`.

### Streaming (incremental) compression

For data too big for memory, feed it in chunks:

```python
c = zlib.compressobj()
out = b"".join(c.compress(chunk) for chunk in chunks) + c.flush()
d = zlib.decompressobj(); d.decompress(out) + d.flush()
```

`bz2.BZ2Compressor`, `lzma.LZMACompressor` and `zstd.ZstdCompressor` work the same way.

### Compressed files

```python
with gzip.open("log.gz", "wt", encoding="utf-8") as f:   # "t" = text mode
    f.write("...")
with lzma.open("data.xz", "rb") as f: ...
shutil.copyfileobj(src_file, dst_file)                    # stream one file into another
```

### `zipfile`

```python
import zipfile
with zipfile.ZipFile("payload.zip", "w", compression=zipfile.ZIP_DEFLATED) as z:
    z.write("real_file.txt", arcname="inside/name.txt")
    z.writestr("generated.txt", "made in memory")
with zipfile.ZipFile("payload.zip") as z:
    z.namelist(), z.infolist()          # ZipInfo: .filename .file_size .compress_size
    z.read("generated.txt")             # bytes
    z.extractall("out/")
zipfile.is_zipfile(path)
zipfile.Path(z, "inside/")              # pathlib-style access inside an archive
```

### `tarfile`

```python
import tarfile
with tarfile.open("payload.tar.xz", "w:xz") as t:   # modes: w, w:gz, w:bz2, w:xz, w:zst (3.14)
    t.add("release_v7", arcname="release_v7")        # whole folders, recursively
with tarfile.open("payload.tar.xz") as t:            # "r" auto-detects the compression
    t.getnames(), t.getmembers()
    t.extractall("out/", filter="data")              # ALWAYS pass a filter
```

The `filter="data"` extraction filter refuses members that would escape the target folder
(`../..`), absolute paths, device files, and dangerous links. It's the default from 3.14, but
say it explicitly anyway.

### `zipapp`: a whole program in one file

```python
import zipapp
zipapp.create_archive("myapp/", "myapp.pyz", main="cli:main")
# then:  python myapp.pyz
```

Python can run a zip file directly as long as it contains a `__main__.py` (which `main=`
generates for you). `zipimport` (ch 30) is the machinery that makes that possible.

---

## ▓ THE JOB

In `job.py`:

1. **`pack(data, algo)`** / **`unpack(blob, algo)`**: dispatch on `"zlib"`, `"gzip"`, `"bz2"`, `"lzma"` and `"zstd"`. Raise `ValueError` for anything else.
2. **`best_algo(data)`**: the algorithm name that gives the smallest output.
3. **`stream_pack(chunks)`**: compress an iterable of chunks with `zlib.compressobj`.
4. **`checksums(data)`**: `(crc32, adler32)`.
5. **`gzip_file(src, dst)`**: stream a file into a `.gz`.
6. **`build_zip(zip_path, files)`** and **`zip_manifest(zip_path)`**: write in-memory files into a deflated zip, and list `(name, size)`.
7. **`build_tar(tar_path, folder)`**: an `xz` tarball, with the folder name as its top level.
8. **`safe_extract(tar_path, dest)`**: extract with the `"data"` filter, and return the extracted names.
9. **`make_app(src_dir, target, main)`**: build a runnable `.pyz` with `zipapp`.

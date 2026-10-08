# 15 // DEAD DROP

```
[OFFLINE] ── network: DISABLED ── drives recovered: 7 ── location: the crew's new hideout
```

**Modules:** `pathlib`, `os`, `os.path`, `shutil`, `tempfile`, `glob`, `fnmatch`, `stat`, `filecmp`, `fileinput`, `linecache`, `io`

It takes two days to collect all seven drops. One is taped under a bench in a flooded
chapel. One is inside a vending machine that hasn't worked since 2070. One is in Mother
Adder's own freezer, which she swears she didn't know about.

The crew has moved into an abandoned pump-control room with a steel door and no windows.
MONTY runs with the network radio physically unplugged. Every drive is a filesystem: folders
of notes, logs, scans, half-finished maps.

> **MONTY:** No network means no BASILISK. It also means we do everything by hand, straight
> against the disk. Paths, directories, walking whole trees, comparing copies, temporary
> scratch space that cleans up after itself. Python's file tools are superb. Use `pathlib`
> first, and reach for `os` and `shutil` when you need the heavy machinery.

---

## ▓ TECH BRIEFING

### `pathlib`: paths as objects

```python
from pathlib import Path
drop = Path("drops") / "chapel" / "notes.txt"      # the / operator joins paths
drop.name, drop.stem, drop.suffix, drop.parent      # 'notes.txt', 'notes', '.txt', drops/chapel
drop.parts                                          # ('drops', 'chapel', 'notes.txt')
drop.with_suffix(".bak"), drop.with_name("map.txt")
drop.exists(), drop.is_file(), drop.is_dir()
drop.parent.mkdir(parents=True, exist_ok=True)      # mkdir -p
drop.write_text("hi", encoding="utf-8");  drop.read_text(encoding="utf-8")
drop.write_bytes(b"..");  drop.read_bytes()
drop.stat().st_size;  drop.unlink(missing_ok=True);  drop.rename(new)
Path.home(), Path.cwd(), drop.resolve(), drop.relative_to("drops"), drop.as_posix()
for p in Path("drops").iterdir(): ...                # one level
Path("drops").glob("*.txt");  Path("drops").rglob("*.log")   # rglob recurses
Path("drops").walk()                                  # like os.walk (3.12+)
with drop.open("a", encoding="utf-8") as f: f.write("more\n")
```

`PurePosixPath` / `PureWindowsPath` manipulate paths from *other* operating systems without
touching the disk.

### `open()` and the `io` module

```python
with open(path, "r", encoding="utf-8") as f:     # modes: r w a x (exclusive create), + (read/write), b (binary)
    for line in f:                                # files iterate lazily, line by line
        ...
f.read(), f.readline(), f.readlines(), f.write(s), f.seek(0), f.tell()
```

Always pass `encoding="utf-8"` for text. `io.StringIO` and `io.BytesIO` are in-memory files:
anything that expects a file object will take one. That's perfect for tests. Under the hood,
`open()` stacks `io.FileIO` → `io.BufferedReader` → `io.TextIOWrapper`.

### `os` and `os.path`

```python
import os
os.getcwd(), os.chdir(p), os.listdir(p), os.scandir(p)     # scandir gives DirEntry objects (fast)
os.makedirs(p, exist_ok=True), os.remove(p), os.rmdir(p), os.rename(a, b), os.replace(a, b)
for dirpath, dirnames, filenames in os.walk(root): ...     # every directory in a tree
os.environ["HOME"], os.environ.get("X", "default"), os.getenv("X")
os.sep, os.linesep, os.pathsep, os.name
os.stat(p).st_mode, os.chmod(p, 0o600), os.getpid()

os.path.join("a", "b"), os.path.exists(p), os.path.getsize(p), os.path.splitext("a.tar.gz")
os.path.basename(p), os.path.dirname(p), os.path.abspath(p), os.path.expanduser("~/x")
```

`os.path` is really `posixpath` on Unix and `ntpath` on Windows, with shared helpers in
`genericpath`. You can import `ntpath` on Linux to handle Windows paths.

### `shutil`: high-level file operations

```python
import shutil
shutil.copy(src, dst)       # contents and permissions;  copy2 also keeps timestamps
shutil.copytree(src, dst)   # a whole tree;  shutil.rmtree(p) deletes one (careful!)
shutil.move(src, dst)
shutil.disk_usage("/")      # (total, used, free)
shutil.which("git")         # full path to an executable, or None
shutil.make_archive("backup", "zip", root_dir)   # see ch 17
```

### `tempfile`

```python
import tempfile
with tempfile.TemporaryDirectory() as tmp:       # deleted when the block ends
    ...
with tempfile.NamedTemporaryFile("w+", suffix=".txt") as f: ...
tempfile.mkdtemp(), tempfile.gettempdir()
```

### `glob` and `fnmatch`

```python
import glob, fnmatch
glob.glob("drops/**/*.txt", recursive=True)      # shell-style wildcards against the disk
fnmatch.fnmatch("notes.txt", "*.txt")            # the same wildcards against a plain string
fnmatch.filter(names, "map_??.png")              # * any run, ? one char, [abc] a set
```

### `stat`, `filecmp`, `fileinput`, `linecache`

```python
import stat
mode = os.stat(p).st_mode
stat.S_ISDIR(mode), bool(mode & stat.S_IXUSR), stat.filemode(mode)   # '-rw-------'

import filecmp
filecmp.cmp(a, b, shallow=False)                 # are two files identical?
d = filecmp.dircmp(dir_a, dir_b); d.left_only, d.right_only, d.diff_files

import fileinput
for line in fileinput.input(files=[a, b]):       # many files as one stream (or stdin)
    fileinput.filename(), fileinput.filelineno()

import linecache
linecache.getline("notes.txt", 3)                # one line, cached (tracebacks use this)
```

---

## ▓ THE JOB

Every function takes paths (strings or `Path`s). The tests make their own temporary folders.

1. **`write_note(folder, name, text)`**: create the folder (and its parents), write the file, return its `Path`.
2. **`read_lines(path)`**: the file's lines without their newlines.
3. **`find(root, pattern)`**: every file under `root` matching a glob pattern, recursively, as sorted POSIX-style paths relative to `root`.
4. **`matching_names(names, pattern)`**: `fnmatch` on plain strings.
5. **`tree_size(root)`**: total bytes of every file in the tree (`os.walk`).
6. **`compare_dirs(a, b)`**: `{"left_only", "right_only", "different"}` with `filecmp.dircmp`.
7. **`lock_down(path)`**: `chmod 600` and return the `stat.filemode` string.
8. **`relocate(path, dest_dir)`**: `shutil.move` into a directory, creating it if needed.
9. **`scratch_roundtrip(data)`**: write bytes into a `TemporaryDirectory`, read them back, and return `(data_read, dir_still_exists_after)`.
10. **`stitched(paths)`**: `fileinput` across several files, giving `(file_name, line_no_in_that_file, text)`.
11. **`line_at(path, n)`**: `linecache`.
12. **`upper_stream(src)`**: read any text file-like object line by line and return an `io.StringIO` holding the upper-cased text, rewound to the start.
13. **`windows_parts(path)`**: split a Windows path into `(drive, folder, stem, suffix)` on any OS.

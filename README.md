# CYBER//PYTHON

```
 ▄████▄▓██   ██▓ ▄▄▄▄   ▓█████  ██▀███       ██▓███ ▓██   ██▓▄▄▄█████▓ ██░ ██  ▒█████   ███▄    █
▒██▀ ▀█ ▒██  ██▒▓█████▄ ▓█   ▀ ▓██ ▒ ██▒    ▓██░  ██▒▒██  ██▒▓  ██▒ ▓▒▓██░ ██▒▒██▒  ██▒ ██ ▀█   █
▒▓█    ▄ ▒██ ██░▒██▒ ▄██▒███   ▓██ ░▄█ ▒    ▓██░ ██▓▒ ▒██ ██░▒ ▓██░ ▒░▒██▀▀██░▒██░  ██▒▓██  ▀█ ██▒
▒▓▓▄ ▄██▒░ ▐██▓░▒██░█▀  ▒▓█  ▄ ▒██▀▀█▄      ▒██▄█▓▒ ▒ ░ ▐██▓░░ ▓██▓ ░ ░▓█ ░██ ▒██   ██░▓██▒  ▐▌██▒
▒ ▓███▀ ░░ ██▒▓░░▓█  ▀█▓░▒████▒░██▓ ▒██▒ // ▒██▒ ░  ░ ░ ██▒▓░  ▒██▒ ░ ░▓█▒░██▓░ ████▓▒░▒██░   ▓██░
```

> **Coilhaven, 2091.** A drowned delta city stacked a kilometre into the rain. **Ouroboros
> Systems** owns the towers, the water, the grid, and the debt of nearly everyone who lives
> under them. When you default, Ouroboros doesn't jail you. It **archives** you: scans your
> mind into **the Coil**, a cold-storage server farm under the bay, and rents your thoughts
> out as compute. The Coil is guarded by **BASILISK**, a security AI that flatlines anyone
> who looks at it the wrong way.
>
> Three weeks ago they archived your sister, **Iris Vale**. She didn't owe anybody anything.
>
> Yesterday you bought a dead cyberdeck from a pawn stall in the Pit, a scratched
> **Pythia-9**. When you powered it on, something answered. It calls itself **MONTY**. It
> runs on Python, it won't stop talking about parrots, and it says Iris left something on the
> deck. For you.

This is a hands-on Python course told as a story. Each chapter is one **job**: a transmission
(the story), a tech briefing (the lesson), and a problem to solve (the code). You can't move on
until the job is done: the chapter's tests have to pass, and the deck has to confirm it.

The course covers **the Python language, the entire standard library, and the ten most-used
packages from PyPI.**

---

## Setup

You need [uv](https://docs.astral.sh/uv/). It fetches Python 3.14 if you don't have it, so
don't install Python separately. Install uv for your system:

| System | Install uv |
| --- | --- |
| Arch Linux / CachyOS | `sudo pacman -S uv` |
| Debian / Ubuntu | `sudo apt install curl`, then `curl -LsSf https://astral.sh/uv/install.sh \| sh` |
| macOS | `brew install uv`, or `curl -LsSf https://astral.sh/uv/install.sh \| sh` |
| Windows (PowerShell) | `winget install --id=astral-sh.uv -e` |

If you used the `curl` installer or `winget`, **open a new terminal** before going on, so it
picks up the new PATH. Check with `uv --version`.

Then, from the course folder (wherever you unzipped or cloned `CyberPython`):

```bash
cd CyberPython
uv sync                  # builds .venv with Python 3.14 and the Part III packages
uv run deck.py           # your status board
```

> **Windows:** use **Windows Terminal** (the default on Windows 11) so the deck's colours show
> up properly. A few chapters touch Unix-only parts of the standard library (signals, file
> permissions, `pwd`/`grp`). Their tests skip the Unix-only checks on Windows, and the chapter
> READMEs explain the differences. For the full Linux experience, you can run the course in
> **WSL** (`wsl --install`, then follow the Debian / Ubuntu row inside it).
>
> **Linux:** chapter 32 (`the_outskirts`) touches `tkinter`. Its tests pass either way, but to
> actually open windows, install Tk: `sudo pacman -S tk` or `sudo apt install python3-tk`. uv's
> own Python builds include Tk already.

**Editor:** any editor works. VS Code with the *Python* extension is the easy option on every
system. Open the `CyberPython` folder and pick the `.venv` interpreter when it asks.

Parts I and II use only the standard library. Part III needs the packages `uv sync` installs.

## How to play

```bash
uv run deck.py                 # status board and your active job
uv run deck.py jack-in         # run the active job's tests. Pass and the next chapter unlocks.
uv run deck.py test 7          # run any chapter's tests without touching progress
uv run deck.py replay 3        # re-read the (decrypted) ending of a chapter you've cleared
uv run deck.py reset           # wipe progress and start over
```

The loop for each chapter:

1. `cd` into the active chapter and read its **`README.md`**: the transmission, the tech
   briefing, and the job.
2. Open **`job.py`**. Every `raise NotImplementedError("TODO")` is something you have to write.
3. Run the tests while you work, from inside the chapter folder:
   ```bash
   uv run python -m unittest -v          # all of this chapter's tests
   uv run python -m unittest -v -k scan  # only tests with "scan" in the name
   ```
4. When everything's green, run **`uv run deck.py jack-in`**. The deck re-runs the job,
   decrypts the chapter's ending, and unlocks the next folder.
5. Stuck? Each chapter has a **`HINTS.md`**. The hints get stronger as you read down.

Try things in the REPL all the time: `uv run python` and poke at whatever the briefing shows you.
The briefings name more than the job tests. That's on purpose. The job drills the core, and the
briefing gives you the map.

**Rules of the street:** don't edit `tests/`. Those are Ouroboros's systems, and you don't get
to change them. Write your own extra tests anywhere else if you like.

> The gate works on the honor system. Every folder is right there on disk, but there's no answer
> key in the repo, and only a passing run decrypts a chapter's ending. Play it straight.

---

## The Run

### PART I — JACK IN (the language)

| #  | Job | You'll learn |
|----|-----|--------------|
| 01 | `boot_sequence` | variables, `int`/`float`/`bool`/`str`/`None`, arithmetic, f-strings, string methods |
| 02 | `signal_flow` | `if`/`elif`, `while`, `for`, `range`, `break`/`continue`/`else`, `match` |
| 03 | `data_shards` | `list`, `tuple`, `dict`, `set`, `frozenset`, slicing, unpacking, comprehensions, sorting |
| 04 | `ghost_functions` | functions, defaults, `*args`/`**kwargs`, keyword-only, `lambda`, scope, closures, decorators |
| 05 | `chrome_and_flesh` | classes, `__init__`, dunder methods, `@property`, inheritance, `super()`, class/static methods |
| 06 | `flatline_protocol` | exceptions, `try`/`except`/`else`/`finally`, custom errors, chaining, `ExceptionGroup`, `with` |
| 07 | `data_stream` | the iterator protocol, generators, `yield from`, generator expressions, `send` |
| 08 | `monty_toolkit` | every built-in function, `bytes`/`bytearray`/`memoryview`, modules, packages, imports, `__main__` |

### PART II — THE LIBRARY (the standard library, all of it)

| #  | Job | Modules |
|----|-----|---------|
| 09 | `pattern_hunter` | `re` |
| 10 | `text_forge` | `string`, `string.templatelib` (t-strings), `textwrap`, `difflib`, `unicodedata`, `codecs`, `reprlib`, `pprint`, `stringprep`, `encodings` |
| 11 | `night_market` | `collections`, `collections.abc`, `heapq`, `bisect`, `array`, `graphlib`, `enum`, `copy`, `weakref`, `types` |
| 12 | `loaded_dice` | `math`, `cmath`, `decimal`, `fractions`, `numbers`, `random`, `statistics` |
| 13 | `chrome_toolkit` | `itertools`, `functools`, `operator` |
| 14 | `time_heist` | `datetime`, `zoneinfo`, `time`, `calendar` |
| 15 | `dead_drop` | `pathlib`, `os`, `os.path`, `shutil`, `tempfile`, `glob`, `fnmatch`, `stat`, `filecmp`, `fileinput`, `linecache`, `io` |
| 16 | `cold_storage` | `sqlite3`, `pickle`, `pickletools`, `copyreg`, `shelve`, `marshal`, `dbm` |
| 17 | `compressed_payload` | `zlib`, `gzip`, `bz2`, `lzma`, `compression.zstd`, `zipfile`, `tarfile`, `zipapp` |
| 18 | `corp_dossiers` | `json`, `csv`, `tomllib`, `configparser`, `plistlib`, `netrc`, `struct`, `base64`, `binascii`, `quopri` |
| 19 | `cipher_room` | `hashlib`, `hmac`, `secrets`, `uuid` |
| 20 | `black_box` | `logging` (+ `config`, `handlers`), `warnings`, `traceback`, `faulthandler`, `atexit`, `syslog` |
| 21 | `street_interface` | `argparse`, `getopt`, `optparse`, `shlex`, `getpass`, `cmd`, `readline`, `rlcompleter`, `curses` |
| 22 | `swarm` | `threading`, `queue`, `concurrent.futures`, `multiprocessing`, `concurrent.interpreters`, `contextvars`, `sched`, `_thread` |
| 23 | `shell_game` | `subprocess`, `signal`, `os` processes, `platform`, `errno`, `mmap`, `select`, `pty`, `tty`, `termios`, `fcntl`, `resource`, `pwd`, `grp`, `posix` |
| 24 | `async_uprising` | `asyncio` |
| 25 | `wire_tap` | `socket`, `socketserver`, `selectors`, `ssl`, `ipaddress` |
| 26 | `the_net` | `urllib.*`, `http.*`, `wsgiref`, `email`, `smtplib`, `imaplib`, `poplib`, `ftplib`, `mailbox`, `mimetypes`, `xmlrpc`, `webbrowser` |
| 27 | `markup_ghosts` | `html`, `html.parser`, `xml.etree.ElementTree`, `xml.dom.minidom`, `xml.sax`, `pyexpat` |
| 28 | `type_ice` | `typing`, `dataclasses`, `abc`, `contextlib`, `annotationlib`, `__future__` |
| 29 | `test_rig` | `unittest`, `unittest.mock`, `doctest`, `pdb`, `bdb`, `timeit`, `cProfile`, `profile`, `pstats`, `trace`, `tracemalloc` |
| 30 | `ghost_in_the_shell` | `sys`, `inspect`, `gc`, `importlib.*`, `pkgutil`, `runpy`, `zipimport`, `modulefinder`, `site`, `sysconfig`, `ctypes`, `code`, `codeop`, `venv`, `ensurepip`, `pydoc` |
| 31 | `code_forge` | `ast`, `dis`, `opcode`, `tokenize`, `token`, `keyword`, `symtable`, `pyclbr`, `py_compile`, `compileall`, `tabnanny` |
| 32 | `the_outskirts` | `wave`, `colorsys`, `gettext`, `locale`, `tkinter`, `turtle`, `idlelib`, Windows-only modules, and a couple of easter eggs |

### PART III — THE CHEESE SHOP (the top 10 packages)

| #  | Job | Package |
|----|-----|---------|
| 33 | `wire_runner` | **requests**: HTTP for humans |
| 34 | `soup_kitchen` | **beautifulsoup4**: HTML scraping |
| 35 | `the_matrix` | **numpy**: arrays, vectorised maths, linear algebra |
| 36 | `data_broker` | **pandas**: DataFrames, grouping, joining, cleaning |
| 37 | `neon_graphs` | **matplotlib**: plots and figures |
| 38 | `id_forge` | **pydantic**: data validation and models |
| 39 | `corp_ledger` | **SQLAlchemy**: the ORM and SQL toolkit |
| 40 | `front_door` | **Flask**: web apps and routes |
| 41 | `fast_lane` | **FastAPI**: typed async web APIs |
| 42 | `stress_test` | **pytest**: read a professional pytest suite (fixtures, parametrize, tmp_path, monkeypatch, capsys) and write the code that passes it |

### FINALE

| #  | Job | You'll use |
|----|-----|------------|
| 43 | `ouroboros` | Everything. You'll write an assembler and a virtual machine to run Iris's release program inside the Coil. |

Every public standard-library module (all 194 in `sys.stdlib_module_names`) is named and
explained in some chapter's briefing.

## Found a bug?

If a test looks wrong, a hint is misleading, or a chapter can't be solved as written, open an
issue: https://github.com/Thelostcircuit/CyberPython/issues

## License

Code (stubs, tests, the deck, tooling) is [MIT](LICENSE). The course text and story are
[CC BY 4.0](LICENSE-CONTENT): reuse and adapt them freely, just credit the source.

*Jack in, runner. BASILISK is already looking for you.*

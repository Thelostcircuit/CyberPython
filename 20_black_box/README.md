# 20 // BLACK BOX

```
[PYTHIA-9] ops recorder: OFF ── crew channels: 4 ── last incident: "Dex fell in a canal" (unlogged)
```

**Modules:** `logging` (+ `config`, `handlers`), `warnings`, `traceback`, `faulthandler`, `atexit`, `syslog`

The plan now has moving parts: Sable on the dock, Dex in the lift shaft, you in the crawl,
MONTY running everything. MONTY wants every one of those parts writing to a flight recorder,
so that when something goes wrong you can find out what, when and where.

> **DEX:** I just use `print`.
>
> **MONTY:** Everyone just uses `print`, until the night they have ten thousand lines of it
> with no timestamps and no idea which part of the program said what. The `logging` module
> gives every message a **level**, a **source**, and a **destination** you can change without
> touching the code. Add warnings for "this still works but it's a bad idea", tracebacks for
> post-mortems, and a crash dumper for when even Python goes down.

---

## ▓ TECH BRIEFING

### `logging`: the model

```python
import logging
log = logging.getLogger(__name__)      # one logger per module, named by dotted path
log.debug("detail")  log.info("normal")  log.warning("odd")  log.error("failed")  log.critical("dead")
log.info("rack %s at %d%%", rack, load)  # lazy %-formatting: only done if the message is emitted
try: ...
except Exception:
    log.exception("vault read failed")   # ERROR level PLUS the current traceback
```

- **Loggers** form a tree by name (`crew` → `crew.radio`). Messages **propagate** up to the
  parents' handlers unless `propagate = False`.
- **Levels:** DEBUG 10, INFO 20, WARNING 30 (the default), ERROR 40, CRITICAL 50. Both the
  logger and each handler filter by level.
- **Handlers** decide where messages go: `StreamHandler` (stderr/any stream), `FileHandler`,
  `NullHandler` (libraries add this so they stay silent by default).
- **Formatters** decide what a line looks like:
  `"%(asctime)s %(levelname)s %(name)s: %(message)s"`.
- **Filters** can drop or enrich records.

```python
logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")  # quick app setup

handler = logging.StreamHandler(stream)
handler.setFormatter(logging.Formatter("%(levelname)s:%(name)s:%(message)s"))
log.addHandler(handler); log.setLevel(logging.DEBUG)
```

A custom handler is a subclass of `logging.Handler` with an `emit(self, record)` method.
`self.format(record)` gives you the formatted text.

### `logging.config` and `logging.handlers`

```python
import logging.config
logging.config.dictConfig({
    "version": 1,
    "formatters": {"short": {"format": "%(levelname)s|%(message)s"}},
    "handlers": {"out": {"class": "logging.StreamHandler", "formatter": "short"}},
    "loggers": {"crew.radio": {"level": "WARNING", "handlers": ["out"], "propagate": False}},
})
```

(`fileConfig` reads the same kind of setup from an INI file.)

`logging.handlers` has the heavy-duty handlers: `RotatingFileHandler(path, maxBytes=,
backupCount=)`, `TimedRotatingFileHandler`, `QueueHandler`/`QueueListener` (log from threads
without blocking), `SysLogHandler`, `SMTPHandler`, `HTTPHandler`, `SocketHandler` and
`MemoryHandler`.

### `warnings`

```python
import warnings
warnings.warn("use scan_v2()", DeprecationWarning, stacklevel=2)   # stacklevel points at the CALLER

with warnings.catch_warnings(record=True) as caught:
    warnings.simplefilter("always")        # don't de-duplicate
    old_function()
[str(w.message) for w in caught]

warnings.filterwarnings("error", category=DeprecationWarning)   # turn warnings into exceptions
```

Categories include `UserWarning` (the default), `DeprecationWarning`, `RuntimeWarning` and
`ResourceWarning`. `python -W error` makes every warning fatal, which is great in CI.
`@warnings.deprecated("msg")` (3.13+) marks a function deprecated.

### `traceback`

```python
import traceback
traceback.format_exc()                            # the current exception's traceback, as text
traceback.format_exception(exc)                   # a list of strings for any exception object
tb = traceback.extract_tb(exc.__traceback__)      # FrameSummary objects: .name .lineno .filename
traceback.print_stack()
traceback.TracebackException.from_exception(exc)  # a structured, renderable version
```

### `faulthandler`, `atexit`, `syslog`

```python
import faulthandler
faulthandler.enable()                 # on a hard crash (segfault), dump the Python stack to stderr
faulthandler.dump_traceback(file)     # dump every thread's stack right now
# `python -X faulthandler script.py` turns it on from the command line

import atexit
atexit.register(save_state)           # runs at normal interpreter exit (not on os._exit or a kill)

import syslog                          # Unix only: write to the system log
syslog.syslog(syslog.LOG_WARNING, "deck overheating")
```

---

## ▓ THE JOB

In `job.py`:

1. **`crew_logger(stream)`**: the `"crew"` logger at DEBUG, with exactly one handler writing `LEVEL:name:message` to `stream`. It must not propagate, and calling it twice must not add a second handler.
2. **`radio_config(stream)`**: configure `"crew.radio"` with `dictConfig`: WARNING level, `LEVEL|message` format, to `stream`, not propagating.
3. **`BlackBox`**: a custom `logging.Handler` that keeps `(levelname, formatted message)` tuples in `.records`.
4. **`risky_read(logger, path)`**: read a file. On `OSError`, log it with `logger.exception` and return `None`.
5. **`rotating_logger(path, max_bytes, backups)`**: a logger using `RotatingFileHandler`.
6. **`crash_site(exc)`**: the function name and line number where an exception was *raised* (the last traceback frame).
7. **`error_text(exc)`**: the full formatted traceback as one string.
8. **`old_scan()`**: emit a `DeprecationWarning` that points at the caller. **`caught_warnings(func)`**: run `func` and return the warning messages it raised.
9. **`strictly(func)`**: run `func` with every warning turned into an exception.
10. **`on_exit(message)`**: print `message` when the interpreter exits (`atexit`).
11. **`stack_dump()`**: dump the current thread stacks with `faulthandler` into a temporary file and return the text.

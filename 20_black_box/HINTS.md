# HINTS // 20 BLACK BOX

## crew_logger
<details><summary>Hint</summary>

`logging.getLogger("crew")` always returns the same object. Remove any old handlers first
(`for h in list(log.handlers): log.removeHandler(h)`), then add a fresh `StreamHandler` with
a `Formatter`. Set the level and `propagate = False`.
</details>

## radio_config
<details><summary>Hint</summary>

The dict needs `"version": 1`, `"disable_existing_loggers": False`, and `formatters`,
`handlers` and `loggers` sections. A handler entry can take the stream object directly:
`{"class": "logging.StreamHandler", "stream": stream, "formatter": "short"}`.
</details>

## BlackBox.emit
<details><summary>Hint</summary>

`self.records.append((record.levelname, self.format(record)))`
</details>

## risky_read
<details><summary>Hint</summary>

Call `logger.exception(...)` *inside* the `except OSError:` block, because that's where it
can see the active exception and attach its traceback.
</details>

## crash_site / error_text
<details><summary>Hint</summary>

`traceback.extract_tb(exc.__traceback__)[-1]` has `.name` and `.lineno`.
`"".join(traceback.format_exception(exc))` gives the text.
</details>

## old_scan / caught_warnings / strictly
<details><summary>Hint</summary>

`warnings.warn(msg, DeprecationWarning, stacklevel=2)`. For catching:
`with warnings.catch_warnings(record=True) as caught: warnings.simplefilter("always"); func()`.
For strict mode: `with warnings.catch_warnings(): warnings.simplefilter("error"); return func()`.
The context manager restores the filters on the way out.
</details>

## on_exit / stack_dump
<details><summary>Hint</summary>

`atexit.register(print, message)`: extra arguments are passed to the callback.
`faulthandler.dump_traceback(f)` needs a real OS file, so use `tempfile.TemporaryFile("w+")`,
then `seek(0)` and `read()`.
</details>

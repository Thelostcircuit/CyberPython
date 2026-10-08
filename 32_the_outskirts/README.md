# 32 // THE OUTSKIRTS

```
[PYTHIA-9] library tour: 180 / 194 modules ── remaining: the odd corners ── one voicemail, unplayed
```

**Modules:** `wave`, `colorsys`, `gettext`, `locale`, `tkinter`, `turtle`, `turtledemo`, `idlelib`, `this`, `antigravity`, and the platform-specific `msvcrt`, `winreg`, `winsound`, `nt`, `nturl2path`

There's one file from the dead drops nobody has opened yet: `voicemail.wav`. Twelve seconds of
what sounds like static.

> **MONTY:** Before we go shopping for outside tools, let's walk the last streets of my library.
> The outskirts: sound files, colour spaces, translations, locales, windows and turtles, and a
> couple of jokes Python's authors left lying around. None of them is glamorous. All of them
> are still *mine*, which means they're yours.

---

## ▓ TECH BRIEFING

### `wave`: WAV audio

```python
import wave
with wave.open("voicemail.wav", "rb") as w:
    w.getnchannels(), w.getsampwidth(), w.getframerate(), w.getnframes()
    frames = w.readframes(w.getnframes())       # raw bytes: for 16-bit mono, 2 bytes per sample

with wave.open("tone.wav", "wb") as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(8000)
    w.writeframes(array("h", samples).tobytes())
```

Samples are just numbers. Pair `wave` with `array` or `struct` (ch 11, 18) and `math.sin` to
make or analyse sound.

### `colorsys`

```python
import colorsys
colorsys.rgb_to_hsv(1.0, 0.0, 1.0)       # (0.833, 1.0, 1.0)  magenta; everything is 0.0–1.0
colorsys.hsv_to_rgb(0.5, 1.0, 1.0)       # (0.0, 1.0, 1.0)    cyan
colorsys.rgb_to_hls, hls_to_rgb, rgb_to_yiq, yiq_to_rgb
```

Hue is a position on the colour wheel, so spacing hues evenly gives you a palette.

### `gettext`: translations

```python
import gettext
t = gettext.translation("deck", localedir="locale", languages=["ja"], fallback=True)
_ = t.gettext
print(_("Release order lodged"))
t.ngettext("%d rack", "%d racks", n) % n          # plurals differ between languages
```

Translations live in compiled `.mo` catalogs. `NullTranslations` is the "no translation"
fallback, and you can subclass it to supply your own lookup.

### `locale`

```python
import locale
locale.setlocale(locale.LC_ALL, "")               # adopt the user's settings (process-wide!)
locale.localeconv()["decimal_point"]              # ',' in much of Europe
locale.format_string("%.2f", 1234.5, grouping=True)
locale.getencoding()                              # 'UTF-8'
locale.strxfrm(s)                                 # a sort key for locale-aware sorting
```

The locale is global state for the whole process, so change it carefully and restore it.

### `tkinter` and `turtle`

```python
import tkinter as tk
from tkinter import ttk
root = tk.Tk(); root.title("Pythia-9")
ttk.Button(root, text="Jack in", command=go).pack()
root.mainloop()

import turtle                        # tkinter-based drawing for learning and art
turtle.forward(100); turtle.left(90); turtle.done()
turtle.Vec2D(3, 4)                   # a 2-D vector: +, *, abs(), .rotate(degrees)
```

`tkinter` needs the Tk libraries installed. Some Linux distros ship them separately (on Arch:
`tk`). If `import tkinter` fails with a missing `libtk`, that's why. `python -m turtledemo`
shows a gallery of turtle demos, and **IDLE** (`python -m idlelib`) is Python's own editor,
written in tkinter.

### Platform-specific corners

- **Windows only:** `msvcrt` (console keypresses: `msvcrt.getch()`), `winreg` (the registry),
  `winsound` (beeps and `.wav` playback), `nt` (the low-level module under `os`), and
  `nturl2path` (converting between `file:` URLs and Windows paths, used by `urllib`).
- **Unix only** (ch 23): `posix`, `pwd`, `grp`, `termios`, `tty`, `pty`, `fcntl`, `resource`,
  `syslog`.

### Easter eggs

```python
import this          # prints "The Zen of Python". Its text is stored ROT13'd in this.s
import antigravity   # opens a web comic in your browser (really)
```

---

## ▓ THE JOB

In `job.py`:

1. **`write_tone(path, freq, seconds, rate)`**: write a 16-bit mono sine wave with `wave`.
2. **`wav_info(path)`**: `(channels, sample_width, frame_rate, frames)`.
3. **`hidden_message(path)`**: Iris hid text in the voicemail's **least significant bits**. Read bit 0 of each 16-bit sample, pack each 8 bits (most significant first) into a byte, and stop at a zero byte.
4. **`neon_palette(n)`**: `n` hex colours with evenly spaced hues, via `colorsys`.
5. **`hue_degrees(hex_colour)`**: the hue of `#rrggbb` in whole degrees.
6. **`CatalogTranslations`**: a `gettext.NullTranslations` subclass that looks words up in a dict, including plurals.
7. **`decimal_point_in(locale_name)`**: temporarily switch `LC_NUMERIC`, read the decimal point, and always restore the old setting.
8. **`spiral(n, step, turn)`**: the points of a turtle-style walk (use `turtle.Vec2D` if you have Tk, or plain `math` if you don't. The tests accept both).
9. **`tk_status()`**: `"available"` or `"missing"`, without crashing either way.
10. **`zen(line)`**: a line of the Zen of Python, without letting `import this` print anything.
